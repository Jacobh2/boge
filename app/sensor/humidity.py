from sensor.sensor import Sensor
from time import sleep
import logging


logger = logging.getLogger(__name__)


class Humidity(Sensor):
    ERROR_IN_ROW_LIMIT = 10

    def __init__(self):
        super().__init__()
        import adafruit_dht
        import board

        self.device = adafruit_dht.DHT22(board.D4)
        self.prev_humidity: float = -999
        self.prev_temperature: float = -999
        self.errors_in_row = 0

    def try_get_temperature(self):
        try:
            self.prev_temperature = self.device.temperature
        except RuntimeError:
            self.errors_in_row += 1
            if self.errors_in_row > self.ERROR_IN_ROW_LIMIT:
                logger.warning(
                    "Failed to read temperature after %s",
                    self.errors_in_row,
                    exc_info=True,
                )
        return self.prev_temperature

    def try_get_humidity(self):
        try:
            self.prev_humidity = self.device.humidity
        except RuntimeError:
            self.errors_in_row += 1
            if self.errors_in_row > self.ERROR_IN_ROW_LIMIT:
                logger.warning(
                    "Failed to read humidity after %s",
                    self.errors_in_row,
                    exc_info=True,
                )
        return self.prev_humidity

    def run(self):
        while True:
            self.try_get_temperature()
            sleep(5)
            self.try_get_humidity()
            sleep(30)

    def get_temperature(self):
        return self.prev_temperature

    def get_humidity(self):
        return self.prev_humidity
