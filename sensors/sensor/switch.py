import time
from settings import Settings
from mqtt import MQTT
from paho.mqtt.client import MQTTMessage
from sensor.sensor import Sensor
import logging


logger = logging.getLogger(__name__)


class Switch(MQTT, Sensor):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        import automationhat

        self.switch = automationhat.relay.one
        self.running = True

    def on_message(self, client, userdata, msg: MQTTMessage):
        should_switch = msg.payload == b"True"
        logger.info("Receiving message to switch: %s (%s)", should_switch, msg.payload)
        if should_switch:
            self.switch.on()
            value = True
        else:
            self.switch.off()
            value = False

        # Update back
        self.publish(value)

    def run(self):
        self.connect()
        while self.running:
            try:
                logger.info("Reading switch value")
                # Read current value
                value = self.switch.is_on()
                # Publish it!
                self.publish(value)
            except Exception:
                logger.warning("Failed to read value", exc_info=True)
            finally:
                # Sleep a bit
                time.sleep(30)


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = Switch(settings)

    logger.info("Starting switch")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
