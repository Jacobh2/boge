"""
Boch BME280 sensor
"""

from mqtt import MQTT
from sensor.sensor import Sensor
from settings import Settings
from time import sleep
import logging
from smbus2 import SMBus
from bme280 import BME280

logger = logging.getLogger(__name__)


class Multi(MQTT, Sensor):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        bus = SMBus(1)
        self.bme280 = BME280(i2c_dev=bus)

        self.running = True

    def run(self):
        self.connect()
        while self.running:
            try:
                temperature = self.bme280.get_temperature()
                pressure = self.bme280.get_pressure()
                humidity = self.bme280.get_humidity()
                # Publish
                self.publish(
                    {
                        "temperature": temperature,
                        "pressure": pressure,
                        "humidity": humidity,
                    }
                )
            except Exception:
                logger.warning("Failed to read value", exc_info=True)
            finally:
                sleep(10)


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = Multi(settings)

    logger.info("Starting BME280")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
