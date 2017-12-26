import json
import socket
from unittest import TestCase
from unittest.mock import patch

from cosmopusher.iot_pusher import IotPusher


class IotPusherTests(TestCase):

    @patch("cosmopusher.iot_pusher.AWSIoTMQTTClient")
    def test_connect(self, mqtt_client_mock):
        IotPusher("endpoint", "rootca_file", "topic")

        mqtt_client_mock.assert_called_with(socket.gethostname(), useWebsocket=True)
        mqtt_client_mock.return_value.configureEndpoint.assert_called_with("endpoint", 443)
        mqtt_client_mock.return_value.configureCredentials.assert_called_with("rootca_file")
        mqtt_client_mock.return_value.connect.assert_called()

    @patch("cosmopusher.iot_pusher.AWSIoTMQTTClient")
    def test_push_data(self, mqtt_client_mock):
        pusher = IotPusher("endpoint", "rootca_file", "topic")

        payload = {'key': 'value'}
        pusher.push("type", payload)

        mqtt_client_mock.return_value.publishAsync.assert_called_with("topic/type", json.dumps(payload), 1)
