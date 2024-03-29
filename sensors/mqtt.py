import json
import time
import paho.mqtt.client as c_mqtt
from paho.mqtt.client import MQTTMessage
from settings import Settings
import logging


logger = logging.getLogger(__name__)


class MQTT:

    def __init__(self, settings: Settings):
        self.host = settings.MQTT_BROKER
        self.port = settings.MQTT_PORT
        self.topic = settings.MQTT_TOPIC
        self.topic_set = f"{self.topic}/set"
        self.topic_state = f"{self.topic}/state"
        self.client = c_mqtt.Client(c_mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(
            settings.MQTT_USER, settings.MQTT_PASSWORD.get_secret_value()
        )

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Connect to the MQTT broker
        self.client.connect(self.host, self.port, keepalive=60)
        logger.info("Connected to %s", self.host)
        # Start the network loop in a separate thread
        self.client.loop_start()

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info("Connected to MQTT Broker!")
            client.subscribe(self.topic_set)
        else:
            logger.error("Failed to connect, return code %s", reason_code)

    # Callback when the client receives a CONNACK response from the server.
    def on_message(client, userdata, msg: MQTTMessage):
        pass

    def publish(self, value) -> bool:
        message = json.dumps({"value": value, "time": time.time()})
        logger.info("About to publish %s", message)
        result = self.client.publish(self.topic_state, message, qos=1, retain=True)
        return result[0] == 0
