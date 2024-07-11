from sensor.sensor import Sensor
from settings import Settings
from mqtt import MQTT
from time import sleep
import logging

logger = logging.getLogger(__name__)


class Moisture(MQTT, Sensor):

    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        import automationhat

        self.sleep_time = settings.SLEEP_TIME

        self.HIGH = settings.MOISTURE_HIGH
        self.LOW = settings.MOISTURE_LOW
        self.rounding = settings.MOISTURE_ROUND
        self.moisture = automationhat.analog[settings.MOISTURE_INPUT]
        self.running = True


    def get_percentage(self) -> float | None:
        try:
            value = self.moisture.read()
            logger.info("Read %s", value)

            # Set high / low
            if value > self.HIGH:
                logger.info("Updating high from %s to %s", self.HIGH, value)
                self.HIGHT = value
            if value < self.LOW:
                logger.info("Updating low from %s to %s", self.LOW, value)
                self.LOW = value

            normalize = (value - self.LOW) / (self.HIGH - self.LOW)
            inverted = 1 - normalize
            percentage = inverted * 100
            rounded = round(percentage, self.rounding)
            return max(min(rounded, 100.0), 0.0)
        except Exception:
            logger.warning("Failed to read moisture", exc_info=True)
        return None

    def run(self):
        self.connect()
        while self.running:
            try:
                value = self.get_percentage()
                # Publish!
                self.publish(value)
                self.retries = 0
            except Exception:
                logger.warning("Failed to read moisture", exc_info=True)
                self.retries += 1
            finally:
                sleep(self.sleep_time)

            if self.retries > self.max_retries:
                self.running = False

        raise Exception(f"Have retried {self.retries} times, will crash and let docker restart us!")


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    logger.info("Starting moisture with settings: %s", settings)

    switch = Moisture(settings)

    logger.info("Starting moisture")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
