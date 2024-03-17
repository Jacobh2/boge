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
        self.errors_in_row_temperature = 0
        self.errors_in_row_humidity = 0

    def try_get_temperature(self):
        try:
            self.prev_temperature = self.device.temperature
            self.errors_in_row_temperature = 0
        except RuntimeError:
            self.errors_in_row_temperature += 1
            if self.errors_in_row_temperature > self.ERROR_IN_ROW_LIMIT:
                logger.warning(
                    "Failed to read temperature after %s",
                    self.errors_in_row_temperature,
                    exc_info=True,
                )
        return self.prev_temperature

    def try_get_humidity(self):
        try:
            self.prev_humidity = self.device.humidity
            self.errors_in_row_humidity = 0
        except RuntimeError:
            self.errors_in_row_humidity += 1
            if self.errors_in_row_humidity > self.ERROR_IN_ROW_LIMIT:
                logger.warning(
                    "Failed to read humidity after %s",
                    self.errors_in_row_humidity,
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

    def get_temperature_status(self) -> bool:
        logger.info("Temperature status: Errors=%s and is alive=%s", self.errors_in_row_temperature, self.is_alive())
        return self.errors_in_row_temperature == 0 and self.is_alive()

    def get_humidity_status(self) -> bool:
        logger.info("Humidity status: Errors=%s and is alive=%s", self.errors_in_row_humidity, self.is_alive())
        return self.errors_in_row_humidity == 0 and self.is_alive()
