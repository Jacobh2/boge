from functools import lru_cache
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
        self.prev_humidity = None
        self.prev_temperature = None
        self.errors_in_row_temperature = 0
        self.errors_in_row_humidity = 0
        self.last_temperature_read_ok = False
        self.last_humidity_read_ok = False
        self.running = True

    def try_get_temperature(self):
        try:
            self.prev_temperature = self.device.temperature
            self.errors_in_row_temperature = 0
            self.last_temperature_read_ok = True
        except RuntimeError:
            self.errors_in_row_temperature += 1
            self.last_temperature_read_ok = False
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
            self.last_humidity_read_ok = True
        except RuntimeError:
            self.errors_in_row_humidity += 1
            self.last_humidity_read_ok = False
            if self.errors_in_row_humidity > self.ERROR_IN_ROW_LIMIT:
                logger.warning(
                    "Failed to read humidity after %s",
                    self.errors_in_row_humidity,
                    exc_info=True,
                )
        return self.prev_humidity

    def run(self):
        while self.running:
            self.try_get_temperature()
            sleep(5)
            self.try_get_humidity()
            sleep(30)

        logger.info("Shutting down")
        try:
            self.device.exit()
        except Exception:
            pass

    def shutdown(self):
        self.running = False

    def get_temperature(self):
        return self.prev_temperature

    def get_humidity(self):
        return self.prev_humidity

    def get_temperature_status(self) -> bool:
        logger.info(
            "Temperature status: Errors=%s and is alive=%s",
            self.errors_in_row_temperature,
            self.is_alive(),
        )
        return self.last_temperature_read_ok == 0 and self.is_alive()

    def get_humidity_status(self) -> bool:
        logger.info(
            "Humidity status: Errors=%s and is alive=%s",
            self.errors_in_row_humidity,
            self.is_alive(),
        )
        return self.last_humidity_read_ok == 0 and self.is_alive()


@lru_cache()
def get_humidity() -> Humidity:
    return Humidity()
