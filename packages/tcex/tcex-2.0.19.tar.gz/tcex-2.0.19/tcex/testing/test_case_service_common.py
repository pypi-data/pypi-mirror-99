"""TcEx Service Common Module"""
# standard library
import base64
import json
import os
import subprocess
import sys
import time
import uuid
from multiprocessing import Process
from random import randint
from threading import Event, Lock, Thread
from typing import Any, Optional

from ..services import MqttMessageBroker
from .test_case_playbook_common import TestCasePlaybookCommon


class TestCaseServiceCommon(TestCasePlaybookCommon):
    """Service App TestCase Class"""

    _mqtt_client = None
    _message_broker = None
    app_process = None
    client_topic = f'client-topic-{randint(100, 999)}'
    lock = Lock()  # lock for subscription management
    server_topic = f'server-topic-{randint(100, 999)}'
    service_ready = Event()
    service_run_method = 'subprocess'  # run service as subprocess, multiprocess, or thread
    shutdown = False
    shutdown_complete = False
    sleep_after_publish_config = 0.5
    sleep_after_publish_webhook_event = 0.5
    sleep_after_service_start = 5
    sleep_before_delete_config = 2
    sleep_before_shutdown = 0.5
    subscriptions = {}  # dictionary of events, posted to by MID by on_subscribe
    trigger_requests = {}
    trigger_responses = {}

    def _app_callback(self, app):
        """Set app object from run.py callback"""
        self.app = app

    @property
    def default_args(self):
        """Return App default args."""
        args = super().default_args.copy()
        args.update(
            {
                'tc_svc_broker_host': os.getenv('TC_SVC_BROKER_HOST', 'localhost'),
                'tc_svc_broker_port': int(os.getenv('TC_SVC_BROKER_PORT', '1883')),
                'tc_svc_broker_service': os.getenv('TC_SVC_BROKER_SERVICE', 'mqtt'),
                'tc_svc_broker_conn_timeout': int(os.getenv('TC_SVC_BROKER_CONN_TIMEOUT', '15')),
                'tc_svc_broker_token': os.getenv('TC_SVC_BROKER_TOKEN'),
                'tc_svc_client_topic': self.client_topic,
                'tc_svc_server_topic': self.server_topic,
                'tc_svc_hb_timeout_seconds': int(os.getenv('TC_SVC_HB_TIMEOUT_SECONDS', '300')),
            }
        )
        return args

    @property
    def message_broker(self):
        """Return an instance of MqttMessageBroker."""
        if self._message_broker is None:
            self._message_broker = MqttMessageBroker(
                broker_host=self.default_args.get('tc_svc_broker_host'),
                broker_port=self.default_args.get('tc_svc_broker_port'),
                broker_timeout=self.default_args.get('tc_svc_broker_conn_timeout'),
                logger=self.log,
            )
            self._message_broker.register_callbacks()

        return self._message_broker

    @property
    def mqtt_client(self):
        """Return a mqtt client instance."""
        return self.message_broker.client

    def on_message(self, client, userdata, message):  # pylint: disable=unused-argument
        """Handle message broker on_message shutdown command events."""

        try:
            m = json.loads(message.payload)
        except ValueError:
            raise RuntimeError(f'Could not parse API service response JSON. ({message})')

        command = m.get('command').lower()
        if command == 'ready':
            self.service_ready.set()

        trigger_id = str(m.get('triggerId'))
        cmd_type = m.get('type', command).lower()
        key = f'{trigger_id}-{cmd_type}'
        if key in self.trigger_responses:
            self.log.warning(f'Additional response arrived for trigger {key} -- discarded')
        else:
            self.trigger_responses[key] = m
        if self.trigger_requests.get(key) is not None:
            self.trigger_requests.pop(key).set()

    # pylint: disable=unused-argument
    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Handle on subscribe callback after subscription completes"""

        with self.lock:
            event = self.subscriptions.pop(mid)
            if event:
                event.set()

    def publish(self, message: str, topic: Optional[str] = None):
        """Publish message on server channel.

        Args:
            message: The message to send.
            topic: The message broker topic. Defaults to None.
        """
        self.message_broker.publish(message, topic)

    def publish_create_config(self, message: dict) -> dict:
        """Send create config message.

        Args:
            trigger_id (str): The trigger id for the config message.
            message (dict): The entire message with trigger_id and config.

        Returns:
            dict: CreateConfig Acknowledge response data.
        """
        # merge the message config (e.g., optional, required)
        message_config = message.pop('config')
        config = message_config.get('optional', {})
        config.update(message_config.get('required', {}))
        message['config'] = config

        # build config message
        message['apiToken'] = self.tc_token
        message['expireSeconds'] = int(time.time() + 86400)
        message['command'] = 'CreateConfig'
        message['config']['tc_playbook_out_variables'] = self.profile.tc_playbook_out_variables
        message['triggerId'] = message.pop('trigger_id')
        self.log.data('run', 'create config', f'{message["triggerId"]}')
        self.message_broker.publish(json.dumps(message), self.server_topic)

        # create thread wait event
        event = Event()
        key = f'{message["triggerId"]}-createconfig'
        self.trigger_requests[key] = event
        event.wait(10)  # wait for 10 seconds
        # time.sleep(self.sleep_after_publish_config)
        result = self.trigger_responses.pop(key, {})
        self.log.data(
            'run',
            'create config',
            f'{message["triggerId"]} {result.get("status", "No Status")} '
            f'{result.get("message", "No Message")}',
        )
        return dict(status=result.get('status', False), message=result.get('message'))

    def publish_delete_config(self, message):
        """Send delete config message.

        Args:
            message (str): The message coming in on Broker channel
        """
        time.sleep(self.sleep_before_delete_config)
        # using triggerId here instead of trigger_id do to pop in publish_create_config
        config_msg = {'command': 'DeleteConfig', 'triggerId': message.get('triggerId')}
        self.log.data('run', 'delete config', f'{message["triggerId"]}')
        self.message_broker.publish(json.dumps(config_msg), self.server_topic)

    def publish_heartbeat(self):
        """Send heartbeat message to service."""
        shutdown_msg = {'command': 'Heartbeat', 'metric': {}, 'memoryPercent': 0, 'cpuPercent': 0}
        self.message_broker.publish(json.dumps(shutdown_msg), self.server_topic)

    def publish_shutdown(self):
        """Publish shutdown message."""
        config_msg = {'command': 'Shutdown'}
        self.log.data('run', 'service', 'shutdown requested')
        self.message_broker.publish(json.dumps(config_msg), self.server_topic)

    def publish_webhook_event(
        self,
        trigger_id: int,
        body: Optional[Any] = None,
        headers: Optional[list] = None,
        method: Optional[str] = 'GET',
        query_params: Optional[list] = None,
        request_key: Optional[str] = None,
    ):
        """Send create config message.

        Args:
            trigger_id: The trigger ID.
            body: The HTTP request body.
            headers: The HTTP request headers name/value pairs.
            method: The HTTP request method.
            query_params: The HTTP request query param name/value pairs.
            request_key: The current request key.
        """
        body = body or ''
        request_key = request_key or str(uuid.uuid4())
        if isinstance(body, dict):
            body = json.dumps(body)

        body = self.redis_client.hset(
            request_key, 'request.body', base64.b64encode(body.encode('utf-8'))
        )
        event = {
            'command': 'WebhookEvent',
            'method': method,
            'queryParams': query_params or [],
            'headers': headers or [],
            'body': 'request.body',
            'requestKey': request_key,
            'triggerId': trigger_id,
        }

        trigger_id = str(trigger_id)
        self.log.data('run', 'webhook event', trigger_id)
        ready = Event()
        key = f'{trigger_id}-webhookevent'
        self.trigger_requests[key] = ready
        self.message_broker.publish(json.dumps(event), self.server_topic)
        ready.wait(10)  # wait for 10 seconds
        status = 'Complete' if ready.isSet() else 'Timed Out'
        self.trigger_responses.pop(key, {})
        self.log.data('run', 'webhook event', f'{trigger_id} {status}')

    def publish_marshall_webhook_event(
        self,
        trigger_id: int,
        body: Optional[Any] = None,
        headers: Optional[list] = None,
        request_key: Optional[str] = None,
        status_code: Optional[int] = 200,
    ):
        """Send create config message.

        Args:
            trigger_id: The trigger ID.
            body: The HTTP response Body.
            headers: The HTTP response headers name/value pairs.
            request_key: The request key to reply with.
            status_code: The HTTP response status code.
            request_key: The current request key.
        """
        body = body or ''
        request_key = request_key or str(uuid.uuid4())
        if isinstance(body, dict):
            body = json.dumps(body)

        body = self.redis_client.hset(
            request_key, 'request.body', base64.b64encode(body.encode('utf-8'))
        )
        event = {
            'command': 'WebhookMarshallEvent',
            'headers': headers or [],
            'body': 'request.body',
            'requestKey': request_key,
            'triggerId': trigger_id,
            'statusCode': status_code,
        }
        trigger_id = str(trigger_id)
        self.log.data('run', 'webhook marshal', trigger_id)
        ready = Event()
        key = f'{trigger_id}-webhookmarshallevent'
        self.trigger_requests[key] = ready
        self.message_broker.publish(json.dumps(event), self.server_topic)
        ready.wait(10)  # wait for 10 seconds
        status = 'Complete' if ready.isSet() else 'Timed Out'
        self.trigger_responses.pop(key, {})
        self.log.data('run', 'webhook marshal', f'{trigger_id} {status}')

    def run(self):
        """Implement in Child Class"""
        raise NotImplementedError('Child class must implement this method.')

    def run_service(self):
        """Run the micro-service."""
        self.log.data('run', 'service method', self.service_run_method)
        # backup sys.argv
        sys_argv_orig = sys.argv

        # clear sys.argv
        sys.argv = sys.argv[:1]

        # create required .app_params encrypted file. args are set in custom.py
        self.args['tcex_testing_context'] = self.tcex_testing_context
        self.create_config(self.args)

        # run the service App in 1 of 3 ways
        if self.service_run_method == 'subprocess':
            # run the Service App as a subprocess
            self.app_process = subprocess.Popen(['python', 'run.py'])
        elif self.service_run_method == 'thread':
            # run App in a thread
            t = Thread(target=self.run, args=(), daemon=True)
            t.start()
        elif self.service_run_method == 'multiprocess':
            p = Process(target=self.run, args=(), daemon=True)
            p.start()

        # restore sys.argv
        sys.argv = sys_argv_orig

    @classmethod
    def setup_class(cls):
        """Run once before all test cases."""
        super().setup_class()
        cls.args = {}
        cls.service_file = 'SERVICE_STARTED'  # started file flag

        # generate a context used in service.py to write context during fire event
        cls.tcex_testing_context = str(uuid.uuid4())

    def setup_method(self):
        """Run before each test method runs."""
        super().setup_method()
        self.stager.redis.from_dict(self.redis_staging_data)
        self.redis_client = self.tcex.redis_client

        for key in list(self.trigger_requests.keys()):
            del self.trigger_requests[key]

        for key in list(self.trigger_responses.keys()):
            del self.trigger_responses[key]

        self.service_ready.clear()

        # register on_message shutdown monitor
        self.message_broker.add_on_message_callback(
            callback=self.on_message, topics=[self.client_topic]
        )

        # register on_subscribe notification
        self.message_broker.add_on_subscribe_callback(callback=self.on_subscribe)

        self.message_broker.client.loop_start()

        self.subscribe(self.client_topic)

        # only start service if it hasn't been started already base on file flag.
        if not os.path.isfile(self.service_file):
            open(self.service_file, 'w+').close()  # create service started file flag
            self.run_service()

            # start shutdown monitor thread
            t = Thread(target=self.shutdown_monitor, daemon=True)
            t.start()

        self.service_ready.wait(30)
        if not self.service_ready.isSet():
            self.log.data('run', 'service', 'failed to start')
        else:
            self.log.data('run', 'service', 'ready')

    def shutdown_monitor(self):
        """Monitor for shutdown flag."""
        while not self.shutdown:
            time.sleep(0.5)

        # shutdown the App
        self.publish_shutdown()

        # give Service App x seconds to shutdown before terminating
        if self.service_run_method == 'subprocess':
            for _ in range(1, 10):
                time.sleep(0.5)
                if self.app_process.poll() is not None:
                    break
            else:
                self.log.data('run', 'Terminating Process', f'PID: {self.app_process.pid}', 'debug')
                self.app_process.terminate()  # terminate subprocess

        # remove started file flag
        try:
            os.remove(self.service_file)
        except OSError:
            pass

        # set shutdown_complete
        self.shutdown_complete = True

    def stage_data(self, staged_data):
        """Stage the data in the profile."""
        for key, value in list(staged_data.get('redis', {}).items()):
            self.stager.redis.stage(key, value)

    def subscribe(self, topic):
        """Subscribe to a topic and wait for the subscription to complete"""
        event = Event()
        with self.lock:
            # don't try to subscribe outside of lock, since
            # it could come back *before* we wait on it
            _, mid = self.message_broker.client.subscribe(topic)
            self.subscriptions[mid] = event

        event.wait(10)
        if mid in self.subscriptions:  # failed to subscribe
            self.log.error(f'Failed to subscribe to topic {topic}')

    @classmethod
    def teardown_class(cls):
        """Run once before all test cases."""
        super().teardown_class()
        # set shutdown flag for shutdown_monitor and wait until shutdown is done
        cls.shutdown = True
        for _ in range(1, 12):
            if cls.shutdown_complete:
                break
            time.sleep(0.5)

    def teardown_method(self):
        """Run after each test method runs."""
        time.sleep(self.sleep_before_shutdown)
        # run test_case_playbook_common teardown_method
        super().teardown_method()

        self.message_broker.client.loop_stop()

        # clean up tcex testing context after populate_output has run
        self.clear_context(self.tcex_testing_context)
