import json
import socket

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, DROP_OLDEST


class IotPusher:

    def __init__(self, iot_endpoint, rootca_file, topic):
        self.client = AWSIoTMQTTClient(socket.gethostname(), useWebsocket=True)
        self.client.configureEndpoint(iot_endpoint, 443)
        self.client.configureCredentials(rootca_file)

        # wait 30 sec before reconnect, max backoff 5 minutes
        self.client.configureAutoReconnectBackoffTime(30, 300, 20)
        # buffer for 2 hours
        self.client.configureOfflinePublishQueueing(3600, DROP_OLDEST)

        self.client.connect()
        self.topic = topic

    def push(self, event_type, payload):
        self.client.publishAsync("{}/{}".format(self.topic, event_type), json.dumps(payload), 1)
