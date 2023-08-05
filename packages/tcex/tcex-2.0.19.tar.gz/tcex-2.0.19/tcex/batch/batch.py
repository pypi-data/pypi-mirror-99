"""ThreatConnect Batch Import Module."""
# standard library
import gzip
import hashlib
import json
import math
import os
import re
import shelve
import sys
import threading
import time
import traceback
import uuid
from collections import deque
from typing import Any, Callable, Optional, Tuple, Union

from .group import (
    Adversary,
    Campaign,
    Document,
    Email,
    Event,
    Group,
    Incident,
    IntrusionSet,
    Report,
    Signature,
    Threat,
)
from .indicator import (
    ASN,
    CIDR,
    URL,
    Address,
    EmailAddress,
    File,
    Host,
    Indicator,
    Mutex,
    RegistryKey,
    UserAgent,
    custom_indicator_class_factory,
)

# import local modules for dynamic reference
module = __import__(__name__)


class Batch:
    """ThreatConnect Batch Import Module"""

    def __init__(
        self,
        tcex: object,
        owner: str,
        action: Optional[str] = 'Create',
        attribute_write_type: Optional[str] = 'Replace',
        halt_on_error: Optional[bool] = True,
        playbook_triggers_enabled: Optional[bool] = False,
    ):
        """Initialize Class properties.

        Args:
            tcex: An instance of TcEx object.
            owner: The ThreatConnect owner for Batch action.
            action: Action for the batch job ['Create', 'Delete'].
            attribute_write_type: Write type for Indicator attributes ['Append', 'Replace'].
            halt_on_error: If True any batch error will halt the batch job.
            playbook_triggers_enabled: **DEPRECATED**
        """
        self.tcex = tcex
        self._action = action
        self._attribute_write_type = attribute_write_type
        self._halt_on_error = halt_on_error
        self._owner = owner
        self._playbook_triggers_enabled = playbook_triggers_enabled

        # properties
        self._batch_max_chunk = 5000
        self._batch_max_size = 75_000_000  # max size in bytes
        self._file_merge_mode = None
        self._file_threads = []
        self._hash_collision_mode = None
        self._submit_thread = None

        # shelf settings
        self._group_shelf_fqfn = None
        self._indicator_shelf_fqfn = None

        # global overrides on batch/file errors
        self._halt_on_batch_error = None
        self._halt_on_file_error = None
        self._halt_on_poll_error = None

        # debug/saved flags
        self._saved_xids = None
        self._saved_groups = None  # indicates groups shelf file was provided
        self._saved_indicators = None  # indicates indicators shelf file was provided
        self.enable_saved_file = False

        # default properties
        self._batch_data_count = None
        self._poll_interval = None
        self._poll_interval_times = []
        self._poll_timeout = 3600

        # containers
        self._groups = None
        self._groups_shelf = None
        self._indicators = None
        self._indicators_shelf = None

        # build custom indicator classes
        self._gen_indicator_class()

        # batch debug/replay variables
        self._debug = None
        self.debug_path = os.path.join(self.tcex.args.tc_temp_path, 'DEBUG')
        self.debug_path_batch = os.path.join(self.debug_path, 'batch_data')
        self.debug_path_group_shelf = os.path.join(self.debug_path, 'groups-saved')
        self.debug_path_indicator_shelf = os.path.join(self.debug_path, 'indicators-saved')
        self.debug_path_files = os.path.join(self.debug_path, 'batch_files')
        self.debug_path_xids = os.path.join(self.debug_path, 'xids-saved')

    @property
    def _critical_failures(self):  # pragma: no cover
        """Return Batch critical failure messages."""
        return [
            'Encountered an unexpected Exception while processing batch job',
            'would exceed the number of allowed indicators',
        ]

    def _gen_indicator_class(self):  # pragma: no cover
        """Generate Custom Indicator Classes."""
        for entry in self.tcex.indicator_types_data.values():
            name = entry.get('name')
            class_name = name.replace(' ', '')
            # temp fix for API issue where boolean are returned as strings
            entry['custom'] = self.tcex.utils.to_bool(entry.get('custom'))

            if class_name in globals():
                # skip Indicator Type if a class already exists
                continue

            # Custom Indicator can have 3 values. Only add the value if it is set.
            value_fields = []
            if entry.get('value1Label'):
                value_fields.append(entry['value1Label'])
            if entry.get('value2Label'):
                value_fields.append(entry['value2Label'])
            if entry.get('value3Label'):
                value_fields.append(entry['value3Label'])
            value_count = len(value_fields)

            class_data = {}
            # Add Class for each Custom Indicator type to this module
            custom_class = custom_indicator_class_factory(name, Indicator, class_data, value_fields)
            setattr(module, class_name, custom_class)

            # Add Custom Indicator Method
            self._gen_indicator_method(name, custom_class, value_count)

    def _gen_indicator_method(
        self, name: str, custom_class: object, value_count: int
    ) -> None:  # pragma: no cover
        """Dynamically generate custom Indicator methods.

        Args:
            name (str): The name of the method.
            custom_class (object): The class to add.
            value_count (int): The number of value parameters to support.
        """
        method_name = name.replace(' ', '_').lower()

        # Add Method for each Custom Indicator class
        def method_1(value1: str, xid, **kwargs):  # pylint: disable=possibly-unused-variable
            """Add Custom Indicator data to Batch object"""
            indicator_obj = custom_class(value1, xid, **kwargs)
            return self._indicator(indicator_obj, kwargs.get('store', True))

        def method_2(
            value1: str, value2: str, xid, **kwargs
        ):  # pylint: disable=possibly-unused-variable
            """Add Custom Indicator data to Batch object"""
            indicator_obj = custom_class(value1, value2, xid, **kwargs)
            return self._indicator(indicator_obj, kwargs.get('store', True))

        def method_3(
            value1: str, value2: str, value3: str, xid, **kwargs
        ):  # pylint: disable=possibly-unused-variable
            """Add Custom Indicator data to Batch object"""
            indicator_obj = custom_class(value1, value2, value3, xid, **kwargs)
            return self._indicator(indicator_obj, kwargs.get('store', True))

        method = locals()[f'method_{value_count}']
        setattr(self, method_name, method)

    def _group(
        self, group_data: Union[dict, object], store: Optional[bool] = True
    ) -> Union[dict, object]:
        """Return previously stored group or new group.

        Args:
            group_data: An Group dict or instance of Group object.
            store: If True the group data will be stored in instance list.

        Returns:
            Union[dict, object]: The new Group dict/object or the previously stored dict/object.
        """
        if store is False:
            return group_data

        if isinstance(group_data, dict):
            # get xid from dict
            xid = group_data.get('xid')
        else:
            # get xid from object
            xid = group_data.xid

        if self.groups.get(xid) is not None:
            # return existing group from memory
            group_data = self.groups.get(xid)
        elif self.groups_shelf.get(xid) is not None:
            # return existing group from shelf
            group_data = self.groups_shelf.get(xid)
        else:
            # store new group
            self.groups[xid] = group_data
        return group_data

    def _indicator(
        self, indicator_data: Union[dict, object], store: Optional[bool] = True
    ) -> Union[dict, object]:
        """Return previously stored indicator or new indicator.

        Args:
            indicator_data: An Indicator dict or instance of Indicator object.
            store: If True the indicator data will be stored in instance list.

        Returns:
            Union[dict, object]: The new Indicator dict/object or the previously stored dict/object.
        """
        if store is False:
            return indicator_data

        if isinstance(indicator_data, dict):
            # get xid from dict
            xid = indicator_data.get('xid')
        else:
            # get xid from object
            xid = indicator_data.xid

        if self.indicators.get(xid) is not None:
            # return existing indicator from memory
            indicator_data = self.indicators.get(xid)
        elif self.indicators_shelf.get(xid) is not None:
            # return existing indicator from shelf
            indicator_data = self.indicators_shelf.get(xid)
        else:
            # store new indicators
            self.indicators[xid] = indicator_data
        return indicator_data

    @staticmethod
    def _indicator_values(indicator: str) -> list:
        """Process indicators expanding file hashes/custom indicators into multiple entries.

        Args:
            indicator: Indicator value represented as " : " delimited string.

        Returns:
            list: The list of indicators split on " : ".
        """
        indicator_list = [indicator]
        if indicator.count(' : ') > 0:
            # handle all multi-valued indicators types (file hashes and custom indicators)
            indicator_list = []

            # group 1 - lazy capture everything to first <space>:<space> or end of line
            iregx_pattern = r'^(.*?(?=\s\:\s|$))?'
            iregx_pattern += r'(?:\s\:\s)?'  # remove <space>:<space>
            # group 2 - look behind for <space>:<space>, lazy capture everything
            #           to look ahead (optional <space>):<space> or end of line
            iregx_pattern += r'((?<=\s\:\s).*?(?=(?:\s)?\:\s|$))?'
            iregx_pattern += r'(?:(?:\s)?\:\s)?'  # remove (optional <space>):<space>
            # group 3 - look behind for <space>:<space>, lazy capture everything
            #           to look ahead end of line
            iregx_pattern += r'((?<=\s\:\s).*?(?=$))?$'
            iregx = re.compile(iregx_pattern)

            indicators = iregx.search(indicator)
            if indicators is not None:
                indicator_list = list(indicators.groups())

        return indicator_list

    @property
    def action(self):
        """Return batch action."""
        return self._action

    @action.setter
    def action(self, action):
        """Set batch action."""
        self._action = action

    def add_group(self, group_data: dict, **kwargs) -> Union[dict, object]:
        """Add a group to Batch Job.

        .. code-block:: javascript

            {
                "name": "Example Incident",
                "type": "Incident",
                "attribute": [{
                    "type": "Description",
                    "displayed": false,
                    "value": "Example Description"
                }],
                "xid": "e336e2dd-5dfb-48cd-a33a-f8809e83e904",
                "associatedGroupXid": [
                    "e336e2dd-5dfb-48cd-a33a-f8809e83e904:58",
                ],
                "tag": [{
                    "name": "China"
                }]
            }

        Args:
            group_data: The full Group data including attributes, labels, tags, and
                associations.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Union[dict, object]: The new group dict/object or the previously stored dict/object.
        """
        return self._group(group_data, kwargs.get('store', True))

    def add_indicator(self, indicator_data: dict, **kwargs) -> Union[dict, object]:
        """Add an indicator to Batch Job.

        .. code-block:: javascript

            {
                "type": "File",
                "rating": 5.00,
                "confidence": 50,
                "summary": "53c3609411c83f363e051d455ade78a7
                            : 57a49b478310e4313c54c0fee46e4d70a73dd580
                            : db31cb2a748b7e0046d8c97a32a7eb4efde32a0593e5dbd58e07a3b4ae6bf3d7",
                "associatedGroups": [
                    {
                        "groupXid": "e336e2dd-5dfb-48cd-a33a-f8809e83e904"
                    }
                ],
                "attribute": [{
                    "type": "Source",
                    "displayed": true,
                    "value": "Malware Analysis provided by external AMA."
                }],
                "fileOccurrence": [{
                    "fileName": "drop1.exe",
                    "date": "2017-03-03T18:00:00-06:00"
                }],
                "tag": [{
                    "name": "China"
                }],
                "xid": "e336e2dd-5dfb-48cd-a33a-f8809e83e904:170139"
            }

        Args:
            indicator_data: The Full Indicator data including attributes, labels, tags,
                and associations.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Union[dict, object]: The new group dict/object or the previously stored dict/object.
        """
        if indicator_data.get('type') not in ['Address', 'EmailAddress', 'File', 'Host', 'URL']:
            # for custom indicator types the valueX fields are required.
            # using the summary we can build the values
            index = 1
            for value in self._indicator_values(indicator_data.get('summary')):
                indicator_data[f'value{index}'] = value
                index += 1
        if indicator_data.get('type') == 'File':
            # convert custom field name to the appropriate value for batch v2
            size = indicator_data.pop('size', None)
            if size is not None:
                indicator_data['intValue1'] = size
        if indicator_data.get('type') == 'Host':
            # convert custom field name to the appropriate value for batch v2
            dns_active = indicator_data.pop('dnsActive', None)
            if dns_active is not None:
                indicator_data['flag1'] = dns_active
            whois_active = indicator_data.pop('whoisActive', None)
            if whois_active is not None:
                indicator_data['flag2'] = whois_active
        return self._indicator(indicator_data, kwargs.get('store', True))

    def address(self, ip: str, **kwargs) -> Address:
        """Add Address data to Batch object.

        Args:
            ip: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Address: An instance of the Address class.
        """
        indicator_obj = Address(ip, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def adversary(self, name: str, **kwargs) -> Adversary:
        """Add Adversary data to Batch object.

        Args:
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Adversary: An instance of the Adversary class.
        """
        group_obj = Adversary(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def asn(self, as_number: str, **kwargs) -> ASN:
        """Add ASN data to Batch object.

        Args:
            as_number: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            ASN: An instance of the ASN class.
        """
        indicator_obj = ASN(as_number, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    @property
    def attribute_write_type(self):
        """Return batch attribute write type."""
        return self._attribute_write_type

    @attribute_write_type.setter
    def attribute_write_type(self, attribute_write_type: str):
        """Set batch attribute write type."""
        self._attribute_write_type = attribute_write_type

    def campaign(self, name: str, **kwargs) -> Campaign:
        """Add Campaign data to Batch object.

        Args:
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            first_seen (str, kwargs): The first seen datetime expression for this Group.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Campaign: An instance of the Campaign class.
        """
        group_obj = Campaign(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def cidr(self, block: str, **kwargs) -> CIDR:
        """Add CIDR data to Batch object.

        Args:
            block: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            CIDR: An instance of the CIDR class.
        """
        indicator_obj = CIDR(block, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def close(self) -> None:
        """Cleanup batch job."""
        # allow pol thread to complete before wrapping up
        if hasattr(self._submit_thread, 'is_alive'):
            self._submit_thread.join()

        # allow file threads to complete before wrapping up job
        for t in self._file_threads:
            t.join()

        self.groups_shelf.close()
        self.indicators_shelf.close()
        if not self.debug and not self.enable_saved_file:
            # delete saved files
            if os.path.isfile(self.group_shelf_fqfn):
                os.remove(self.group_shelf_fqfn)
            if os.path.isfile(self.group_shelf_fqfn):
                os.remove(self.indicator_shelf_fqfn)

    @property
    def data(self):
        """Return the batch indicator/group and file data to be sent to the ThreatConnect API.

        **Processing Order:**
        * Process groups in memory up to max batch size.
        * Process groups in shelf to max batch size.
        * Process indicators in memory up to max batch size.
        * Process indicators in shelf up to max batch size.

        This method will remove the group/indicator from memory and/or shelf.

        Returns:
            dict: A dictionary of group, indicators, and/or file data.
        """
        data = {'file': {}, 'group': [], 'indicator': []}
        tracker = {'count': 0, 'bytes': 0}

        # process group from memory, returning if max values have been reached
        if self.data_groups(data, self.groups, tracker) is True:
            return data

        # process group from shelf file, returning if max values have been reached
        if self.data_groups(data, self.groups_shelf, tracker) is True:
            return data

        # process indicator from memory, returning if max values have been reached
        if self.data_indicators(data, self.indicators, tracker) is True:
            return data

        # process indicator from shelf file, returning if max values have been reached
        if self.data_indicators(data, self.indicators_shelf, tracker) is True:
            return data

        return data

    def data_group_association(self, data: dict, tracker: dict, xid: str) -> None:
        """Return group dict array following all associations.

        The *data* dict is passed by reference to make it easier to update both the group data
        and file data inline versus passing the data all the way back up to the calling methods.

        Args:
            data: The data dict to update with group and file data.
            tracker: A dict containing total count of all entities collected and
                the total size in bytes of all entities collected.
            xid: The xid of the group to retrieve associations.
        """
        xids = deque()
        xids.append(xid)

        while xids:
            xid = xids.popleft()  # remove current xid
            group_data = None

            if xid in self.groups:
                group_data = self.groups.get(xid)
                del self.groups[xid]
            elif xid in self.groups_shelf:
                group_data = self.groups_shelf.get(xid)
                del self.groups_shelf[xid]

            if group_data:
                file_data, group_data = self.data_group_type(group_data)
                data['group'].append(group_data)
                if file_data:
                    data['file'][xid] = file_data

                # update entity trackers
                tracker['count'] += 1
                tracker['bytes'] += sys.getsizeof(json.dumps(group_data))

                # extend xids with any groups associated with the same object
                xids.extend(group_data.get('associatedGroupXid', []))

    @staticmethod
    def data_group_type(group_data: Union[dict, object]) -> Tuple[dict, dict]:
        """Return dict representation of group data and file data.

        Args:
            group_data: The group data dict or object.

        Returns:
            Tuple[dict, dict]: A tuple containing file_data and group_data.
        """
        file_data = {}
        if isinstance(group_data, dict):
            # process file content
            file_content = group_data.pop('fileContent', None)
            if file_content is not None:
                file_data = {
                    'fileContent': file_content,
                    'fileName': group_data.get('fileName'),
                    'type': group_data.get('type'),
                }
        else:
            # get the file data from the object and return dict format of object
            if group_data.data.get('type') in ['Document', 'Report']:
                file_data = group_data.file_data
            group_data = group_data.data

        return file_data, group_data

    def data_groups(self, data: dict, groups: list, tracker: dict) -> bool:
        """Process Group data.

        Args:
            data: The data dict to update with group and file data.
            groups: The list of groups to process.
            tracker: A dict containing total count of all entities collected and
                the total size in bytes of all entities collected.

        Returns:
            bool: True if max values have been hit, else False.
        """
        # convert groups.keys() to a list to prevent dictionary change error caused by
        # the data_group_association function deleting items from the object.

        # process group objects
        for xid in list(groups.keys()):
            # get association from group data
            self.data_group_association(data, tracker, xid)

            if tracker.get('count') % 2_500 == 0:
                # log count/size at a sane level
                self.tcex.log.info(
                    '''feature=batch, action=data-groups, '''
                    f'''count={tracker.get('count'):,}, bytes={tracker.get('bytes'):,}'''
                )

            if (
                tracker.get('count') >= self._batch_max_chunk
                or tracker.get('bytes') >= self._batch_max_size
            ):
                # stop processing xid once max limit are reached
                self.tcex.log.info(
                    '''feature=batch, event=max-value-reached, '''
                    f'''count={tracker.get('count'):,}, bytes={tracker.get('bytes'):,}'''
                )
                return True
        return False

    def data_indicators(self, data: dict, indicators: list, tracker: dict) -> bool:
        """Process Indicator data.

        Args:
            data: The data dict to update with group and file data.
            indicators: The list of indicators to process.
            tracker: A dict containing total count of all entities collected and
                the total size in bytes of all entities collected.

        Returns:
            bool: True if max values have been hit, else False.
        """
        # process indicator objects
        for xid, indicator_data in list(indicators.items()):
            if not isinstance(indicator_data, dict):
                indicator_data = indicator_data.data
            data['indicator'].append(indicator_data)
            del indicators[xid]

            # update entity trackers
            tracker['count'] += 1
            tracker['bytes'] += sys.getsizeof(json.dumps(indicator_data))

            if tracker.get('count') % 2_500 == 0:
                # log count/size at a sane level
                self.tcex.log.info(
                    '''feature=batch, action=data-indicators, '''
                    f'''count={tracker.get('count'):,}, bytes={tracker.get('bytes'):,}'''
                )

            if (
                tracker.get('count') >= self._batch_max_chunk
                or tracker.get('bytes') >= self._batch_max_size
            ):
                # stop processing xid once max limit are reached
                self.tcex.log.info(
                    '''feature=batch, event=max-value-reached, '''
                    f'''count={tracker.get('count'):,}, bytes={tracker.get('bytes'):,}'''
                )
                return True
        return False

    @property
    def debug(self):
        """Return debug setting"""
        if self._debug is None:
            self._debug = False

            # switching DEBUG file to a directory
            if os.path.isfile(self.debug_path):
                os.remove(self.debug_path)
                os.makedirs(self.debug_path, exist_ok=True)

            if os.path.isdir(self.debug_path) and os.access(self.debug_path, os.R_OK):
                # create directories only required when debug is enabled
                # batch_json - store the batch*.json files
                # documents - store the file downloads (e.g., *.pdf)
                # reports - store the file downloads (e.g., *.pdf)
                os.makedirs(self.debug_path, exist_ok=True)
                os.makedirs(self.debug_path_batch, exist_ok=True)
                os.makedirs(self.debug_path_files, exist_ok=True)
                self._debug = True
        return self._debug

    def document(self, name: str, file_name: str, **kwargs) -> Document:
        """Add Document data to Batch object.

        Args:
            name: The name for this Group.
            file_name: The name for the attached file for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            file_content (str;method, kwargs): The file contents or
                callback method to retrieve file content.
            malware (bool, kwargs): If true the file is considered malware.
            password (bool, kwargs): If malware is true a password for the zip archive is
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Document: An instance of the Document class.
        """
        group_obj = Document(name, file_name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def email(self, name: str, subject: str, header: str, body: str, **kwargs) -> Email:
        """Add Email data to Batch object.

        Args:
            name: The name for this Group.
            subject: The subject for this Email.
            header: The header for this Email.
            body: The body for this Email.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            from_addr (str, kwargs): The **from** address for this Email.
            to_addr (str, kwargs): The **to** address for this Email.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Email: An instance of the Email class.
        """
        group_obj = Email(name, subject, header, body, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def email_address(self, address: str, **kwargs) -> EmailAddress:
        """Add Email Address data to Batch object.

        Args:
            address: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            EmailAddress: An instance of the EmailAddress class.
        """
        indicator_obj = EmailAddress(address, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    @property
    def error_codes(self):
        """Return static list of Batch error codes and short description"""
        return {
            '0x1001': 'General Error',
            '0x1002': 'Permission Error',
            '0x1003': 'JsonSyntax Error',
            '0x1004': 'Internal Error',
            '0x1005': 'Invalid Indicator Error',
            '0x1006': 'Invalid Group Error',
            '0x1007': 'Item Not Found Error',
            '0x1008': 'Indicator Limit Error',
            '0x1009': 'Association Error',
            '0x100A': 'Duplicate Item Error',
            '0x100B': 'File IO Error',
            '0x2001': 'Indicator Partial Loss Error',
            '0x2002': 'Group Partial Loss Error',
            '0x2003': 'File Hash Merge Error',
        }

    def errors(self, batch_id: int, halt_on_error: Optional[bool] = True) -> list:
        """Retrieve Batch errors to ThreatConnect API.

        .. code-block:: javascript

            [{
                "errorReason": "Incident incident-001 has an invalid status.",
                "errorSource": "incident-001 is not valid."
            }, {
                "errorReason": "Incident incident-002 has an invalid status.",
                "errorSource":"incident-002 is not valid."
            }]

        Args:
            batch_id: The ID returned from the ThreatConnect API for the current batch job.
            halt_on_error: If True any exception will raise an error.

        Returns:
            list: A list of batch errors.
        """
        errors = []
        try:
            self.tcex.log.debug(f'feature=batch, event=retrieve-errors, batch-id={batch_id}')
            r = self.tcex.session.get(f'/v2/batch/{batch_id}/errors')
            # API does not return correct content type
            if r.ok:
                errors = json.loads(r.text)
            # temporarily process errors to find "critical" errors.
            # FR in core to return error codes.
            for error in errors:
                error_reason = error.get('errorReason')
                for error_msg in self._critical_failures:
                    if re.findall(error_msg, error_reason):
                        self.tcex.handle_error(10500, [error_reason], halt_on_error)
            return errors
        except Exception as e:
            self.tcex.handle_error(560, [e], halt_on_error)
            return None

    def event(self, name: str, **kwargs) -> Event:
        """Add Event data to Batch object.

        Args:
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            event_date (str, kwargs): The event datetime expression for this Group.
            status (str, kwargs): The status for this Group.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Event: An instance of the Event class.
        """
        group_obj = Event(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def file(
        self,
        md5: Optional[str] = None,
        sha1: Optional[str] = None,
        sha256: Optional[str] = None,
        **kwargs,
    ) -> File:
        """Add File data to Batch object.

        .. note:: A least one file hash value must be specified.

        Args:
            md5: The md5 value for this Indicator.
            sha1: The sha1 value for this Indicator.
            sha256: The sha256 value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            size (str, kwargs): The file size for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            File: An instance of the File class.

        """
        indicator_obj = File(md5, sha1, sha256, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def file_merge_mode(self, value: str) -> None:
        """Set the file merge mode for the entire batch job.

        Args:
            value: A value of Distribute or Merge.
        """
        self._file_merge_mode = value

    @staticmethod
    def generate_xid(identifier: Optional[Union[list, str]] = None):
        """Generate xid from provided identifiers.

        .. Important::  If no identifier is provided a unique xid will be returned, but it will
                        not be reproducible. If a list of identifiers are provided they must be
                        in the same order to generate a reproducible xid.

        Args:
            identifier:  Optional *string* value(s) to be
               used to make a unique and reproducible xid.

        """
        if identifier is None:
            identifier = str(uuid.uuid4())
        elif isinstance(identifier, list):
            identifier = '-'.join([str(i) for i in identifier])
            identifier = hashlib.sha256(identifier.encode('utf-8')).hexdigest()
        return hashlib.sha256(identifier.encode('utf-8')).hexdigest()

    def group(self, group_type: str, name: str, **kwargs) -> object:
        """Add Group data to Batch object.

        Args:
            group_type: The ThreatConnect define Group type.
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            object: An instance of one of the Group classes.
        """
        group_obj = Group(group_type, name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    @property
    def group_shelf_fqfn(self):
        """Return groups shelf fully qualified filename.

        For testing/debugging a previous shelf file can be copied into the tc_temp_path directory
        instead of creating a new shelf file.
        """
        if self._group_shelf_fqfn is None:
            # new shelf file
            self._group_shelf_fqfn = os.path.join(
                self.tcex.args.tc_temp_path, f'groups-{str(uuid.uuid4())}'
            )

            # saved shelf file
            if self.saved_groups:
                self._group_shelf_fqfn = self.debug_path_group_shelf
        return self._group_shelf_fqfn

    @property
    def groups(self) -> dict:
        """Return dictionary of all Groups data."""
        if self._groups is None:
            # plain dict, but could be something else in future
            self._groups = {}
        return self._groups

    @property
    def groups_shelf(self) -> object:
        """Return dictionary of all Groups data."""
        if self._groups_shelf is None:
            self._groups_shelf = shelve.open(self.group_shelf_fqfn, writeback=False)
        return self._groups_shelf

    @property
    def halt_on_error(self) -> bool:
        """Return batch halt on error setting."""
        return self._halt_on_error

    @halt_on_error.setter
    def halt_on_error(self, halt_on_error: bool):
        """Set batch halt on error setting."""
        self._halt_on_error = halt_on_error

    @property
    def halt_on_batch_error(self) -> bool:
        """Return halt on batch error value."""
        return self._halt_on_batch_error

    @halt_on_batch_error.setter
    def halt_on_batch_error(self, value: bool):
        """Set batch halt on batch error value."""
        if isinstance(value, bool):
            self._halt_on_batch_error = value

    @property
    def halt_on_file_error(self) -> bool:
        """Return halt on file post error value."""
        return self._halt_on_file_error

    @halt_on_file_error.setter
    def halt_on_file_error(self, value: bool):
        """Set halt on file post error value."""
        if isinstance(value, bool):
            self._halt_on_file_error = value

    @property
    def halt_on_poll_error(self) -> bool:
        """Return halt on poll error value."""
        return self._halt_on_poll_error

    @halt_on_poll_error.setter
    def halt_on_poll_error(self, value: bool):
        """Set batch halt on poll error value."""
        if isinstance(value, bool):
            self._halt_on_poll_error = value

    def hash_collision_mode(self, value: str):
        """Set the file hash collision mode for the entire batch job.

        Args:
            value: A value of Split, IgnoreIncoming, IgnoreExisting, FavorIncoming,
                and FavorExisting.
        """
        self._hash_collision_mode = value

    def host(self, hostname: str, **kwargs) -> Host:
        """Add Host data to Batch object.

        Args:
            hostname: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            dns_active (bool, kwargs): If True DNS active is enabled for this indicator.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            whois_active (bool, kwargs): If True WhoIs active is enabled for this indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Host: An instance of the Host class.
        """
        indicator_obj = Host(hostname, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def incident(self, name: str, **kwargs) -> Incident:
        """Add Incident data to Batch object.

        Args:
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            event_date (str, kwargs): The event datetime expression for this Group.
            status (str, kwargs): The status for this Group.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Incident: An instance of the Incident class.
        """
        group_obj = Incident(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def indicator(self, indicator_type: str, summary: str, **kwargs) -> object:
        """Add Indicator data to Batch object.

        Args:
            indicator_type: The ThreatConnect define Indicator type.
            summary: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            object: An instance of one of the Indicator classes.
        """
        indicator_obj = Indicator(indicator_type, summary, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    @property
    def indicator_shelf_fqfn(self) -> str:
        """Return indicator shelf fully qualified filename.

        For testing/debugging a previous shelf file can be copied into the tc_temp_path directory
        instead of creating a new shelf file.
        """
        if self._indicator_shelf_fqfn is None:
            # new shelf file
            self._indicator_shelf_fqfn = os.path.join(
                self.tcex.args.tc_temp_path, f'indicators-{str(uuid.uuid4())}'
            )

            # saved shelf file
            if self.saved_indicators:
                self._indicator_shelf_fqfn = self.debug_path_indicator_shelf
        return self._indicator_shelf_fqfn

    @property
    def indicators(self) -> dict:
        """Return dictionary of all Indicator data."""
        if self._indicators is None:
            # plain dict, but could be something else in future
            self._indicators = {}
        return self._indicators

    @property
    def indicators_shelf(self) -> object:
        """Return dictionary of all Indicator data."""
        if self._indicators_shelf is None:
            self._indicators_shelf = shelve.open(self.indicator_shelf_fqfn, writeback=False)
        return self._indicators_shelf

    def intrusion_set(self, name: str, **kwargs) -> IntrusionSet:
        """Add Intrusion Set data to Batch object.

        Args:
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            IntrusionSet: An instance of the IntrusionSet class.
        """
        group_obj = IntrusionSet(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def mutex(self, mutex: str, **kwargs) -> Mutex:
        """Add Mutex data to Batch object.

        Args:
            mutex: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Mutex: An instance of the Mutex class.
        """
        indicator_obj = Mutex(mutex, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def poll(
        self,
        batch_id: int,
        retry_seconds: Optional[int] = None,
        back_off: Optional[float] = None,
        timeout: Optional[int] = None,
        halt_on_error: Optional[bool] = True,
    ) -> dict:
        """Poll Batch status to ThreatConnect API.

        .. code-block:: javascript

            {
                "status": "Success",
                "data": {
                    "batchStatus": {
                        "id":3505,
                        "status":"Completed",
                        "errorCount":0,
                        "successCount":0,
                        "unprocessCount":0
                    }
                }
            }

        Args:
            batch_id: The ID returned from the ThreatConnect API for the current batch job.
            retry_seconds: The base number of seconds used for retries when job is not completed.
            back_off: A multiplier to use for backing off on
                each poll attempt when job has not completed.
            timeout: The number of seconds before the poll should timeout.
            halt_on_error: If True any exception will raise an error.

        Returns:
            dict: The batch status returned from the ThreatConnect API.
        """
        # check global setting for override
        if self.halt_on_poll_error is not None:
            halt_on_error = self.halt_on_poll_error

        # initial poll interval
        if self._poll_interval is None and self._batch_data_count is not None:
            # calculate poll_interval base off the number of entries in the batch data
            # with a minimum value of 5 seconds.
            self._poll_interval = max(math.ceil(self._batch_data_count / 300), 5)
        elif self._poll_interval is None:
            # if not able to calculate poll_interval default to 15 seconds
            self._poll_interval = 15

        # poll retry back_off factor
        poll_interval_back_off = float(2.5 if back_off is None else back_off)

        # poll retry seconds
        poll_retry_seconds = int(5 if retry_seconds is None else retry_seconds)

        # poll timeout
        if timeout is None:
            timeout = self.poll_timeout
        else:
            timeout = int(timeout)
        params = {'includeAdditional': 'true'}

        poll_count = 0
        poll_time_total = 0
        data = {}
        while True:
            poll_count += 1
            poll_time_total += self._poll_interval
            time.sleep(self._poll_interval)
            self.tcex.log.info(f'feature=batch, event=progress, poll-time={poll_time_total}')
            try:
                # retrieve job status
                r = self.tcex.session.get(f'/v2/batch/{batch_id}', params=params)
                if not r.ok or 'application/json' not in r.headers.get('content-type', ''):
                    self.tcex.handle_error(545, [r.status_code, r.text], halt_on_error)
                    return data
                data = r.json()
                if data.get('status') != 'Success':
                    self.tcex.handle_error(545, [r.status_code, r.text], halt_on_error)
            except Exception as e:
                self.tcex.handle_error(540, [e], halt_on_error)

            if data.get('data', {}).get('batchStatus', {}).get('status') == 'Completed':
                # store last 5 poll times to use in calculating average poll time
                modifier = poll_time_total * 0.7
                self._poll_interval_times = self._poll_interval_times[-4:] + [modifier]

                weights = [1]
                poll_interval_time_weighted_sum = 0
                for poll_interval_time in self._poll_interval_times:
                    poll_interval_time_weighted_sum += poll_interval_time * weights[-1]
                    # weights will be [1, 1.5, 2.25, 3.375, 5.0625] for all 5 poll times depending
                    # on how many poll times are available.
                    weights.append(weights[-1] * 1.5)

                # pop off the last weight so its not added in to the sum
                weights.pop()

                # calculate the weighted average of the last 5 poll times
                self._poll_interval = math.floor(poll_interval_time_weighted_sum / sum(weights))

                if poll_count == 1:
                    # if completed on first poll, reduce poll interval.
                    self._poll_interval = self._poll_interval * 0.85

                self.tcex.log.debug(f'feature=batch, poll-time={poll_time_total}, status={data}')
                return data

            # update poll_interval for retry with max poll time of 20 seconds
            self._poll_interval = min(
                poll_retry_seconds + int(poll_count * poll_interval_back_off), 20
            )

            # time out poll to prevent App running indefinitely
            if poll_time_total >= timeout:
                self.tcex.handle_error(550, [timeout], True)

    @property
    def poll_timeout(self) -> int:
        """Return current poll timeout value."""
        return self._poll_timeout

    @poll_timeout.setter
    def poll_timeout(self, seconds: int):
        """Set the poll timeout value."""
        self._poll_timeout = int(seconds)

    def process_all(self, process_files: Optional[bool] = True) -> None:
        """Process Batch request to ThreatConnect API.

        Args:
            process_files: Send any document or report attachments to the API.
        """
        while True:
            content = self.data
            file_data = content.pop('file', {})
            if not content.get('group') and not content.get('indicator'):
                break

            # special code for debugging App using batchV2.
            self.write_batch_json(content)

            # store the length of the batch data to use for poll interval calculations
            self.tcex.log.info(
                '''feature=batch, event=process-all, type=group, '''
                f'''count={len(content.get('group')):,}'''
            )
            self.tcex.log.info(
                '''feature=batch, event=process-all, type=indicator, '''
                f'''count={len(content.get('indicator')):,}'''
            )

        if process_files:
            self.process_files(file_data)

    def process_files(self, file_data: dict) -> None:
        """Process Files for Documents and Reports to ThreatConnect API.

        Args:
            file_data: The file data to be processed.
        """
        for xid, content_data in list(file_data.items()):
            del file_data[xid]  # win or loose remove the entry

            # define the saved filename
            api_branch = 'documents' if content_data.get('type') == 'Report' else 'reports'
            fqfn = os.path.join(
                self.debug_path_files,
                f'''{api_branch}--{xid}--{content_data.get('fileName').replace('/', ':')}''',
            )

            # used for debug/testing to prevent upload of previously uploaded file
            if self.debug and xid in self.saved_xids:
                self.tcex.log.debug(
                    f'feature=batch-submit-files, action=skip-previously-saved-file, xid={xid}'
                )
                continue

            if os.path.isfile(fqfn):
                self.tcex.log.debug(
                    f'feature=batch-submit-files, action=skip-previously-saved-file, xid={xid}'
                )
                continue

            # process the file content
            content = content_data.get('fileContent')
            if callable(content):
                content_callable_name = getattr(content, '__name__', repr(content))
                self.tcex.log.trace(
                    f'feature=batch-submit-files, method={content_callable_name}, xid={xid}'
                )
                content = content_data.get('fileContent')(xid)

            if content is None:
                self.tcex.log.warning(f'feature=batch-submit-files, xid={xid}, event=content-null')
                continue

            # write the file to disk
            with open(fqfn, 'wb') as fh:
                fh.write(content)

    def registry_key(
        self, key_name: str, value_name: str, value_type: str, **kwargs
    ) -> RegistryKey:
        """Add Registry Key data to Batch object.

        Args:
            key_name: The key_name value for this Indicator.
            value_name: The value_name value for this Indicator.
            value_type: The value_type value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            RegistryKey: An instance of the Registry Key class.
        """
        indicator_obj = RegistryKey(key_name, value_name, value_type, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def report(self, name: str, **kwargs) -> Report:
        """Add Report data to Batch object.

        Args:
            name: The name for this Group.
            file_name (str): The name for the attached file for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            file_content (str;method, kwargs): The file contents or callback method to retrieve
                file content.
            publish_date (str, kwargs): The publish datetime expression for this Group.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Report: An instance of the Report class.
        """
        group_obj = Report(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def save(self, resource: Union[dict, object]) -> None:
        """Save group|indicator dict or object to shelve.

        Best effort to save group/indicator data to disk.  If for any reason the save fails
        the data will still be accessible from list in memory.

        Args:
            resource: The Group or Indicator dict or object.
        """
        resource_type = None
        xid = None
        if isinstance(resource, dict):
            resource_type = resource.get('type')
            xid = resource.get('xid')
        else:
            resource_type = resource.type
            xid = resource.xid

        if resource_type is not None and xid is not None:
            saved = True

            if resource_type in self.tcex.group_types:
                try:
                    # groups
                    self.groups_shelf[xid] = resource
                except Exception:
                    saved = False

                if saved:
                    try:
                        del self._groups[xid]
                    except KeyError:
                        # if group was saved twice it would already be delete
                        pass
            elif resource_type in self.tcex.indicator_types_data.keys():
                try:
                    # indicators
                    self.indicators_shelf[xid] = resource
                except Exception:
                    saved = False

                if saved:
                    try:
                        del self._indicators[xid]
                    except KeyError:
                        # if indicator was saved twice it would already be delete
                        pass

    @property
    def saved_groups(self) -> bool:
        """Return True if saved group files exits, else False."""
        if self._saved_groups is None:
            self._saved_groups = False
            if (
                self.enable_saved_file
                and os.path.isfile(self.debug_path_group_shelf)
                and os.access(self.debug_path_group_shelf, os.R_OK)
            ):
                self._saved_groups = True
                self.tcex.log.debug('feature=batch, event=saved-groups-file-found')
        return self._saved_groups

    @property
    def saved_indicators(self) -> bool:
        """Return True if saved indicators files exits, else False."""
        if self._saved_indicators is None:
            self._saved_indicators = False
            if (
                self.enable_saved_file
                and os.path.isfile(self.debug_path_indicator_shelf)
                and os.access(self.debug_path_indicator_shelf, os.R_OK)
            ):
                self._saved_indicators = True
                self.tcex.log.debug('feature=batch, event=saved-indicator-file-found')
        return self._saved_indicators

    @property
    def saved_xids(self) -> list:
        """Return previously saved xids."""
        if self._saved_xids is None:
            self._saved_xids = []
            if self.debug:
                if os.path.isfile(self.debug_path_xids) and os.access(
                    self.debug_path_xids, os.R_OK
                ):
                    with open(self.debug_path_xids) as fh:
                        self._saved_xids = fh.read().splitlines()
        return self._saved_xids

    @saved_xids.setter
    def saved_xids(self, xid: str):
        """Append xid to xids saved file."""
        with open(self.debug_path_xids, 'a') as fh:
            fh.write(f'{xid}\n')

    @property
    def settings(self) -> dict:
        """Return batch job settings."""
        _settings = {
            'action': self._action,
            # not supported in v2 batch
            # 'attributeWriteType': self._attribute_write_type,
            'attributeWriteType': 'Replace',
            'haltOnError': str(self._halt_on_error).lower(),
            'owner': self._owner,
            'version': 'V2',
        }
        if self._playbook_triggers_enabled is not None:
            _settings['playbookTriggersEnabled'] = str(self._playbook_triggers_enabled).lower()
        if self._hash_collision_mode is not None:
            _settings['hashCollisionMode'] = self._hash_collision_mode
        if self._file_merge_mode is not None:
            _settings['fileMergeMode'] = self._file_merge_mode
        return _settings

    def signature(
        self, name: str, file_name: str, file_type: str, file_text: str, **kwargs
    ) -> Signature:
        """Add Signature data to Batch object.

        Valid file_types:
        + Snort ®
        + Suricata
        + YARA
        + ClamAV ®
        + OpenIOC
        + CybOX ™
        + Bro
        + Regex
        + SPL - Splunk ® Search Processing Language

        Args:
            name: The name for this Group.
            file_name: The name for the attached signature for this Group.
            file_type: The signature type for this Group.
            file_text: The signature content for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Signature: An instance of the Signature class.
        """
        group_obj = Signature(name, file_name, file_type, file_text, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def submit(
        self,
        poll: Optional[bool] = True,
        errors: Optional[bool] = True,
        process_files: Optional[bool] = True,
        halt_on_error: Optional[bool] = True,
    ) -> dict:
        """Submit Batch request to ThreatConnect API.

        By default this method will submit the job request and data and if the size of the data
        is below the value **synchronousBatchSaveLimit** set in System Setting it will process
        the request synchronously and return the batch status.  If the size of the batch is greater
        than the value set the batch job will be queued.
        Errors are not retrieve automatically and need to be enabled.

        If any of the submit, poll, or error methods fail the entire submit will halt at the point
        of failure. The behavior can be changed by setting halt_on_error to False.

        Each of these methods can also be called on their own for greater control of the submit
        process.

        Args:
            poll: If True poll batch for status.
            errors: If True retrieve any batch errors (only if poll is True).
            process_files: If true send any document or report attachments to the API.
            halt_on_error: If True any exception will raise an error.

        Returns.
            dict: The Batch Status from the ThreatConnect API.
        """
        # get file, group, and indicator data
        content = self.data

        # pop any file content to pass to submit_files
        file_data = content.pop('file', {})
        batch_data = (
            self.submit_create_and_upload(content=content, halt_on_error=halt_on_error)
            .get('data', {})
            .get('batchStatus', {})
        )
        batch_id = batch_data.get('id')
        if batch_id is not None:
            self.tcex.log.info(f'feature=batch, event=submit, batch-id={batch_id}')
            # job hit queue
            if poll:
                # poll for status
                batch_data = (
                    self.poll(batch_id=batch_id, halt_on_error=halt_on_error)
                    .get('data', {})
                    .get('batchStatus')
                )
                if errors:
                    # retrieve errors
                    error_groups = batch_data.get('errorGroupCount', 0)
                    error_indicators = batch_data.get('errorIndicatorCount', 0)
                    if error_groups > 0 or error_indicators > 0:
                        batch_data['errors'] = self.errors(batch_id)
            else:
                # can't process files if status is unknown (polling must be enabled)
                process_files = False

        if process_files:
            # submit file data after batch job is complete
            self._file_threads.append(
                self.submit_thread(
                    name='submit-files', target=self.submit_files, args=(file_data, halt_on_error,),
                )
            )
        return batch_data

    def submit_all(
        self,
        poll: Optional[bool] = True,
        errors: Optional[bool] = True,
        process_files: Optional[bool] = True,
        halt_on_error: Optional[bool] = True,
    ) -> dict:
        """Submit Batch request to ThreatConnect API.

        By default this method will submit the job request and data and if the size of the data
        is below the value **synchronousBatchSaveLimit** set in System Setting it will process
        the request synchronously and return the batch status.  If the size of the batch is greater
        than the value set the batch job will be queued.
        Errors are not retrieve automatically and need to be enabled.

        If any of the submit, poll, or error methods fail the entire submit will halt at the point
        of failure. The behavior can be changed by setting halt_on_error to False.

        Each of these methods can also be called on their own for greater control of the submit
        process.

        Args:
            poll: If True poll batch for status.
            errors: If True retrieve any batch errors (only if poll is True).
            process_files: If true send any document or report attachments to the API.
            halt_on_error: If True any exception will raise an error.

        Returns.
            dict: The Batch Status from the ThreatConnect API.
        """
        batch_data_array = []
        file_data = {}
        while True:
            batch_data = {}
            batch_id = None

            # get file, group, and indicator data
            content = self.data

            # break loop when end of data is reached
            if not content.get('group') and not content.get('indicator'):
                break

            if self.action.lower() == 'delete':
                # no need to process files on a delete batch job
                process_files = False

                # while waiting of FR for delete support in createAndUpload submit delete request
                # the old way (submit job + submit data), still using V2.
                if len(content) > 0:  # pylint: disable=len-as-condition
                    batch_id = self.submit_job(halt_on_error)
                    if batch_id is not None:
                        batch_data = self.submit_data(
                            batch_id=batch_id, content=content, halt_on_error=halt_on_error
                        )
                else:
                    batch_data = {}
            else:
                # pop any file content to pass to submit_files
                file_data = content.pop('file', {})
                batch_data = (
                    self.submit_create_and_upload(content=content, halt_on_error=halt_on_error)
                    .get('data', {})
                    .get('batchStatus', {})
                )
                batch_id = batch_data.get('id')

            if batch_id is not None:
                self.tcex.log.info(f'feature=batch, event=status, batch-id={batch_id}')
                # job hit queue
                if poll:
                    # poll for status
                    batch_data = (
                        self.poll(batch_id, halt_on_error=halt_on_error)
                        .get('data', {})
                        .get('batchStatus')
                    )
                    if errors:
                        # retrieve errors
                        error_count = batch_data.get('errorCount', 0)
                        error_groups = batch_data.get('errorGroupCount', 0)
                        error_indicators = batch_data.get('errorIndicatorCount', 0)
                        if error_count > 0 or error_groups > 0 or error_indicators > 0:
                            batch_data['errors'] = self.errors(batch_id)
                else:
                    # can't process files if status is unknown (polling must be enabled)
                    process_files = False

            if process_files:
                # submit file data after batch job is complete
                self._file_threads.append(
                    self.submit_thread(
                        name='submit-files',
                        target=self.submit_files,
                        args=(file_data, halt_on_error,),
                    )
                )
            batch_data_array.append(batch_data)

            # write errors for debugging
            self.write_error_json(batch_data.get('errors'))

        return batch_data_array

    def submit_callback(
        self,
        callback: Callable[..., Any],
        content: Optional[dict] = None,
        halt_on_error: Optional[bool] = True,
    ) -> bool:
        """Submit batch data to ThreatConnect and poll in a separate thread.

        The "normal" submit methods run in serial which will block when the batch poll is running.
        Using this method the submit is done in serial, but the poll method is run in a thread,
        which should allow the App to continue downloading and processing data while the batch
        poll process is running. Only one batch submission is allowed at a time so that any
        critical errors returned from batch can be handled before submitting a new batch job.

        Args:
            callback: The callback method that will handle
                the batch status when polling is complete.
            content: The dict of groups and indicator data (e.g., {"group": [], "indiciator": []}).
            halt_on_error: If True the process should halt if any errors are encountered.

        Raises:
            RuntimeError: Raised on invalid callback method.

        Returns:
            bool: False when there is not data to process, else True
        """
        # user provided content or grab content from local group/indicator lists
        if content is not None:
            # process content
            pass
        else:
            content = self.data
        file_data = content.pop('file', {})

        # return False when end of data is reached
        if not content.get('group') and not content.get('indicator'):
            return False

        # block here is there is already a batch submission being processed
        if hasattr(self._submit_thread, 'is_alive'):
            self.tcex.log.info(
                'feature=batch, event=progress, status=blocked, '
                f'is-alive={self._submit_thread.is_alive()}'
            )
            self._submit_thread.join()
            self.tcex.log.debug(
                'feature=batch, event=progress, status=released, '
                f'is-alive={self._submit_thread.is_alive()}'
            )

        # submit the data and collect the response
        batch_data: dict = (
            self.submit_create_and_upload(content=content, halt_on_error=halt_on_error)
            .get('data', {})
            .get('batchStatus', {})
        )
        self.tcex.log.trace(f'feature=batch, event=submit-callback, batch-data={batch_data}')

        # launch batch polling in a thread
        self._submit_thread = self.submit_thread(
            name='submit-poll',
            target=self.submit_callback_thread,
            args=(batch_data, callback, file_data),
        )

        return True

    def submit_callback_thread(
        self,
        batch_data: int,
        callback: Callable[..., Any],
        file_data: dict,
        halt_on_error: Optional[bool] = True,
    ) -> None:
        """Submit data in a thread."""
        batch_id = batch_data.get('id')
        self.tcex.log.info(f'feature=batch, event=progress, batch-id={batch_id}')
        if batch_id:
            # when batch_id is None it indicates that batch submission was small enough to be
            # processed inline (without being queued)

            # poll for status
            batch_status = (
                self.poll(batch_id, halt_on_error=halt_on_error).get('data', {}).get('batchStatus')
            )

            # retrieve errors
            error_count = batch_status.get('errorCount', 0)
            error_groups = batch_status.get('errorGroupCount', 0)
            error_indicators = batch_status.get('errorIndicatorCount', 0)
            if error_count > 0 or error_groups > 0 or error_indicators > 0:
                batch_status['errors'] = self.errors(batch_id)
        else:
            batch_status = batch_data

        # launch file upload in a thread *after* batch status is returned. while only one batch
        # submission thread is allowed, there is no limit on file upload threads. the upload
        # status returned by file upload will be ignored when running in a thread.
        if file_data:
            self._file_threads.append(
                self.submit_thread(
                    name='submit-files', target=self.submit_files, args=(file_data, halt_on_error,),
                )
            )

        # send batch_status to callback
        if callable(callback):
            self.tcex.log.debug('feature=batch, event=calling-callback')
            try:
                callback(batch_status)
            except Exception as e:
                self.tcex.log.warning(f'feature=batch, event=callback-error, err="""{e}"""')

    def submit_create_and_upload(self, content: dict, halt_on_error: Optional[bool] = True) -> dict:
        """Submit Batch request to ThreatConnect API.

        Args:
            content: The dict of groups and indicator data.
            halt_on_error: If True the process should halt if any errors are encountered.

        Returns.
            dict: The Batch Status from the ThreatConnect API.
        """
        # check global setting for override
        if self.halt_on_batch_error is not None:
            halt_on_error = self.halt_on_batch_error

        # special code for debugging App using batchV2.
        self.write_batch_json(content)

        # store the length of the batch data to use for poll interval calculations
        self.tcex.log.info(
            '''feature=batch, event=submit-create-and-upload, type=group, '''
            f'''count={len(content.get('group')):,}'''
        )
        self.tcex.log.info(
            '''feature=batch, event=submit-create-and-upload, type=indicator, '''
            f'''count={len(content.get('indicator')):,}'''
        )

        try:
            files = (('config', json.dumps(self.settings)), ('content', json.dumps(content)))
            params = {'includeAdditional': 'true'}
            r = self.tcex.session.post('/v2/batch/createAndUpload', files=files, params=params)
            if not r.ok or 'application/json' not in r.headers.get('content-type', ''):
                self.tcex.handle_error(10510, [r.status_code, r.text], halt_on_error)
            return r.json()
        except Exception as e:
            self.tcex.handle_error(10505, [e], halt_on_error)

        return {}

    def submit_data(
        self, batch_id: int, content: dict, halt_on_error: Optional[bool] = True
    ) -> dict:
        """Submit Batch request to ThreatConnect API.

        Args:
            batch_id: The batch id of the current job.
            content: The dict of groups and indicator data.
            halt_on_error (Optional[bool] = True): If True the process
                should halt if any errors are encountered.

        Returns:
            dict: The response data
        """
        # check global setting for override
        if self.halt_on_batch_error is not None:
            halt_on_error = self.halt_on_batch_error

        # store the length of the batch data to use for poll interval calculations
        self._batch_data_count = len(content.get('group')) + len(content.get('indicator'))
        self.tcex.log.info(
            f'feature=batch, action=submit-data, batch-size={self._batch_data_count:,}'
        )

        headers = {'Content-Type': 'application/octet-stream'}
        try:
            r = self.tcex.session.post(f'/v2/batch/{batch_id}', headers=headers, json=content)
            if not r.ok or 'application/json' not in r.headers.get('content-type', ''):
                self.tcex.handle_error(10525, [r.status_code, r.text], halt_on_error)
            return r.json()
        except Exception as e:
            self.tcex.handle_error(10520, [e], halt_on_error)

        return None

    def submit_files(self, file_data: dict, halt_on_error: Optional[bool] = True) -> dict:
        """Submit Files for Documents and Reports to ThreatConnect API.

        Critical Errors

        * There is insufficient document storage allocated to this account.

        Args:
            halt_on_error: If True any exception will raise an error.
            file_data: The file data to be submitted.

        Returns:
            dict: The upload status for each xid.
        """
        # check global setting for override
        if self.halt_on_file_error is not None:
            halt_on_error = self.halt_on_file_error

        upload_status = []
        self.tcex.log.info(f'feature=batch, action=submit-files, count={len(file_data)}')
        for xid, content_data in list(file_data.items()):
            del file_data[xid]  # win or loose remove the entry
            status = True

            # used for debug/testing to prevent upload of previously uploaded file
            if self.debug and xid in self.saved_xids:
                self.tcex.log.debug(
                    f'feature=batch-submit-files, action=skip-previously-saved-file, xid={xid}'
                )
                continue

            # process the file content
            content = content_data.get('fileContent')
            if callable(content):
                try:
                    content_callable_name = getattr(content, '__name__', repr(content))
                    self.tcex.log.trace(
                        f'feature=batch-submit-files, method={content_callable_name}, xid={xid}'
                    )
                    content = content_data.get('fileContent')(xid)
                except Exception as e:
                    self.tcex.log.warning(
                        f'feature=batch, event=file-download-exception, err="""{e}"""'
                    )

            if content is None:
                upload_status.append({'uploaded': False, 'xid': xid})
                self.tcex.log.warning(f'feature=batch-submit-files, xid={xid}, event=content-null')
                continue

            api_branch = 'documents'
            if content_data.get('type') == 'Report':
                api_branch = 'reports'

            if self.debug and content_data.get('fileName'):
                # special code for debugging App using batchV2.
                fqfn = os.path.join(
                    self.debug_path_files,
                    f'''{api_branch}--{xid}--{content_data.get('fileName').replace('/', ':')}''',
                )
                with open(fqfn, 'wb') as fh:
                    if not isinstance(content, bytes):
                        content = content.encode()
                    fh.write(content)

            # Post File
            url = f'/v2/groups/{api_branch}/{xid}/upload'
            headers = {'Content-Type': 'application/octet-stream'}
            params = {'owner': self._owner, 'updateIfExists': 'true'}
            r = self.submit_file_content('POST', url, content, headers, params, halt_on_error)
            if r.status_code == 401:
                # use PUT method if file already exists
                self.tcex.log.info('feature=batch, event=401-from-post, action=switch-to-put')
                r = self.submit_file_content('PUT', url, content, headers, params, halt_on_error)
            if not r.ok:
                status = False
                self.tcex.handle_error(585, [r.status_code, r.text], halt_on_error)
            elif self.debug and self.enable_saved_file and xid not in self.saved_xids:
                # save xid "if" successfully uploaded and not already saved
                self.saved_xids = xid

            self.tcex.log.info(
                f'feature=batch, event=file-upload, status={r.status_code}, '
                f'xid={xid}, remaining={len(file_data)}'
            )
            upload_status.append({'uploaded': status, 'xid': xid})

        return upload_status

    def submit_file_content(
        self,
        method: str,
        url: str,
        data: Union[bytes, str],
        headers: dict,
        params: dict,
        halt_on_error: Optional[bool] = True,
    ) -> object:
        """Submit File Content for Documents and Reports to ThreatConnect API.

        Args:
            method: The HTTP method for the request (POST, PUT).
            url: The URL for the request.
            data: The body (data) for the request.
            headers: The headers for the request.
            params: The query string parameters for the request.
            halt_on_error: If True any exception will raise an error.

        Returns:
            requests.models.Response: The response from the request.
        """
        r = None
        try:
            r = self.tcex.session.request(method, url, data=data, headers=headers, params=params)
        except Exception as e:
            self.tcex.handle_error(580, [e], halt_on_error)
        return r

    def submit_job(self, halt_on_error: Optional[bool] = True) -> int:
        """Submit Batch request to ThreatConnect API.

        Args:
            halt_on_error: If True any exception will raise an error.

        Returns:
            int: The batch id from the API response.
        """
        # check global setting for override
        if self.halt_on_batch_error is not None:
            halt_on_error = self.halt_on_batch_error

        try:
            r = self.tcex.session.post('/v2/batch', json=self.settings)
        except Exception as e:
            self.tcex.handle_error(10505, [e], halt_on_error)

        if not r.ok or 'application/json' not in r.headers.get('content-type', ''):
            self.tcex.handle_error(10510, [r.status_code, r.text], halt_on_error)
        data = r.json()
        if data.get('status') != 'Success':
            self.tcex.handle_error(10510, [r.status_code, r.text], halt_on_error)
        self.tcex.log.debug(f'feature=batch, event=submit-job, status={data}')
        return data.get('data', {}).get('batchId')

    def submit_thread(
        self,
        name: str,
        target: Callable[[], bool],
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
    ) -> None:
        """Start a submit thread.

        Args:
            name: The name of the thread.
            target: The method to call for the thread.
            args: The args to pass to the target method.
            kwargs: Additional args.
        """
        self.tcex.log.info(f'feature=batch, event=submit-thread, name={name}')
        args = args or ()
        t = None
        try:
            t = threading.Thread(name=name, target=target, args=args, kwargs=kwargs, daemon=True)
            t.start()
        except Exception:
            self.tcex.log.trace(traceback.format_exc())
        return t

    def threat(self, name: str, **kwargs) -> Threat:
        """Add Threat data to Batch object

        Args:
            name: The name for this Group.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            xid (str, kwargs): The external id for this Group.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            Threat: An instance of the Threat class.
        """
        group_obj = Threat(name, **kwargs)
        return self._group(group_obj, kwargs.get('store', True))

    def user_agent(self, text: str, **kwargs) -> UserAgent:
        """Add User Agent data to Batch object

        Args:
            text: The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            UserAgent: An instance of the UserAgent class.
        """
        indicator_obj = UserAgent(text, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def url(self, text: str, **kwargs) -> URL:
        """Add URL Address data to Batch object.

        Args:
            text (str): The value for this Indicator.
            confidence (str, kwargs): The threat confidence for this Indicator.
            date_added (str, kwargs): The date timestamp the Indicator was created.
            last_modified (str, kwargs): The date timestamp the Indicator was last modified.
            rating (str, kwargs): The threat rating for this Indicator.
            xid (str, kwargs): The external id for this Indicator.
            store: (bool, kwargs): Advanced - Defaults to True. If True
                the indicator data will be stored in instance list.

        Returns:
            URL: An instance of the URL class.
        """
        indicator_obj = URL(text, **kwargs)
        return self._indicator(indicator_obj, kwargs.get('store', True))

    def write_error_json(self, errors: list) -> None:
        """Write the errors to a JSON file for debuging purposes.

        Args:
            errors: A list of errors to write out.
        """
        if self.debug:
            if not errors:
                errors = []
            # get timestamp as a string without decimal place and consistent length
            timestamp = str(int(time.time() * 10000000))
            error_json_file = os.path.join(self.debug_path_batch, f'errors-{timestamp}.json.gz')
            with gzip.open(error_json_file, mode='wt', encoding='utf-8') as fh:
                json.dump(errors, fh)

    def write_batch_json(self, content: dict) -> None:
        """Write batch json data to a file."""
        if self.debug and content:
            # get timestamp as a string without decimal place and consistent length
            timestamp = str(int(time.time() * 10000000))
            batch_json_file = os.path.join(self.debug_path_batch, f'batch-{timestamp}.json.gz')
            with gzip.open(batch_json_file, mode='wt', encoding='utf-8') as fh:
                json.dump(content, fh)

    @property
    def group_len(self) -> int:
        """Return the number of current groups."""
        return len(self.groups) + len(self.groups_shelf)

    @property
    def indicator_len(self) -> int:
        """Return the number of current indicators."""
        return len(self.indicators) + len(self.indicators_shelf)

    def __len__(self) -> int:
        """Return the number of groups and indicators."""
        return self.group_len + self.indicator_len

    def __str__(self) -> str:  # pragma: no cover
        """Return string represtentation of object."""
        groups = []
        for group_data in self.groups.values():
            if isinstance(group_data, dict):
                groups.append(group_data)
            else:
                groups.append(group_data.data)
        for group_data in self.groups_shelf.values():
            if isinstance(group_data, dict):
                groups.append(group_data)
            else:
                groups.append(group_data.data)

        indicators = []
        for indicator_data in self.indicators.values():
            if isinstance(indicator_data, dict):
                indicators.append(indicator_data)
            else:
                indicators.append(indicator_data.data)
        for indicator_data in self.indicators_shelf.values():
            if isinstance(indicator_data, dict):
                indicators.append(indicator_data)
            else:
                indicators.append(indicator_data.data)

        data = {'group': groups, 'indicators': indicators}
        return json.dumps(data, indent=4, sort_keys=True)
