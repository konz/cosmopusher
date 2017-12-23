import json
import socket

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class IotPusher:

    def __init__(self, iot_endpoint, rootca_file, topic):
        self.client = AWSIoTMQTTClient(socket.gethostname(), useWebsocket=True)
        self.client.configureEndpoint(iot_endpoint, 443)
        self.client.configureCredentials(rootca_file)
        self.client.connect()
        self.topic = topic

    def push(self, payload):
        self.client.publishAsync(self.topic, json.dumps(payload), 1)