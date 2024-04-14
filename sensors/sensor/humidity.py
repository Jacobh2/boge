from settings import Settings
from mqtt import MQTT
from sensor.sensor import Sensor
from time import sleep
import logging


logger = logging.getLogger(__name__)


class Humidity(MQTT, Sensor):

    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        import adafruit_dht
        import board

        self.device = adafruit_dht.DHT22(board.D17)
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
            if self.errors_in_row_temperature > self.max_retries:
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
            if self.errors_in_row_humidity > self.max_retries:
                logger.warning(
                    "Failed to read humidity after %s",
                    self.errors_in_row_humidity,
                    exc_info=True,
                )
        return self.prev_humidity
    
    def _shutdown(self):
        logger.info("Shutting down")
        try:
            self.device.exit()
        except Exception:
            pass

    def run(self):
        self.connect()

        while self.running:
            try:
                temperature = self.try_get_temperature()
                sleep(5)
                humidity = self.try_get_humidity()

                # Publish!
                self.publish({"temperature": temperature, "humidity": humidity})
                self.retries = 0
            except Exception:
                logger.warning("Failed to read humidity or temperature", exc_info=True)
                self.retries += 1
            finally:
                sleep(30)

            if self.retries > self.max_retries:
                self.running = False
                

        self._shutdown()

        raise Exception(f"Have retried {self.retries} times, will crash and let docker restart us!")


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = Humidity(settings)

    logger.info("Starting humidity")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
