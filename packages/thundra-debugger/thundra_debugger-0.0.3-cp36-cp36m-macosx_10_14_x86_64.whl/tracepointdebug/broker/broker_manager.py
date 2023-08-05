import logging
import socket
import time
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread
from uuid import uuid4

import simplejson as json

from thundra.config import config_names
from thundra.config.config_provider import ConfigProvider
from tracepointdebug.application import utils
from tracepointdebug.application.application import Application
from tracepointdebug.broker.application.application_status import ApplicationStatus
from tracepointdebug.broker.broker_client import BrokerConnection
from tracepointdebug.broker.broker_credentials import BrokerCredentials
from tracepointdebug.broker.broker_message_callback import BrokerMessageCallback
from tracepointdebug.broker.event.application_status_event import ApplicationStatusEvent
from tracepointdebug.tracepoint.application.application_status_tracepoint_provider import \
    ApplicationStatusTracePointProvider
from tracepointdebug.tracepoint.encoder import JSONEncoder

API_KEY = ConfigProvider.get(config_names.THUNDRA_APIKEY)
BROKER_HOST = utils.get_from_environment_variables("THUNDRA_AGENT_BROKER_HOST", "wss://broker.thundra.io", str)
BROKER_PORT = utils.get_from_environment_variables("THUNDRA_AGENT_BROKER_PORT", 443, int)

APPLICATION_STATUS_PUBLISH_PERIOD_IN_SECS = 60

logger = logging.getLogger(__name__)


class BrokerManager(object):
    __instance = None
    hostname = socket.gethostname()

    def __init__(self):
        self.broker_connection = None
        self.initialized = False
        self._event_executor = ThreadPoolExecutor()
        self.application_status_thread = Thread(target=self.application_status_sender, daemon=True)

        self.application_status_providers = [ApplicationStatusTracePointProvider()]

    @staticmethod
    def instance():
        return BrokerManager() if BrokerManager.__instance is None else BrokerManager.__instance

    def initialize(self):
        if not self.initialized:
            self.connect_to_broker()
            self.initialized = True

    def connect_to_broker(self):
        try:
            application_info = Application.get_application_info()
            broker_credentials = BrokerCredentials(api_key=API_KEY,
                                                   app_instance_id=application_info['applicationInstanceId'],
                                                   app_name=application_info['applicationName'],
                                                   app_stage=application_info['applicationStage'],
                                                   app_version=application_info['applicationVersion'],
                                                   runtime=application_info['applicationRuntime'],
                                                   hostname=BrokerManager.hostname)

            broker_message_callback = BrokerMessageCallback()
            self.broker_connection = BrokerConnection(host=BROKER_HOST, port=BROKER_PORT,
                                                      broker_credentials=broker_credentials,
                                                      message_callback=broker_message_callback.on_message)

            self.broker_connection.connect()
            self.application_status_thread.start()
        except Exception as e:
            logger.error("Error connecting to broker %s" % e)

    @staticmethod
    def prepare_event(event):
        if event.id is None:
            event.id = str(uuid4())
        if event.time is None:
            event.time = int(time.time() * 1000)
        if event.hostname is None:
            event.hostname = socket.gethostname()
        application_info = Application.get_application_info()
        event.application_instance_id = application_info['applicationInstanceId']
        event.application_name = application_info['applicationName']

    def do_publish_event(self, event):
        self.prepare_event(event)
        try:
            serialized = json.dumps(event, cls=JSONEncoder)
            self.broker_connection.send(serialized)
        except Exception as e:
            logger.error("Error serializing event %s" % e)

    def publish_event(self, event):
        self._event_executor.submit(self.do_publish_event, event)

    def application_status_sender(self):
        while self.broker_connection is not None and self.broker_connection.is_running():
            self.broker_connection.connected.wait()
            self.publish_application_status()
            time.sleep(APPLICATION_STATUS_PUBLISH_PERIOD_IN_SECS)

    def publish_application_status(self, client=None):
        application_info = Application.get_application_info()
        application_status = ApplicationStatus()
        application_status.name = application_info['applicationName']
        application_status.instance_id = application_info['applicationInstanceId']
        application_status.version = application_info['applicationVersion']
        application_status.stage = application_info['applicationStage']
        application_status.runtime = application_info['applicationRuntime']
        try:
            hostname = socket.gethostname()
            application_status.hostname = hostname
            host_ip = socket.gethostbyname(hostname)
            application_status.ip = host_ip
        except:
            pass

        for status_provider in self.application_status_providers:
            status_provider.provide(application_status, client)

        event = ApplicationStatusEvent(client=client, application=application_status)
        self.publish_event(event)
