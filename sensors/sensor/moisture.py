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

        self.HIGH = settings.MOISTURE_HIGH
        self.LOW = settings.MOISTURE_LOW
        self.rounding = settings.MOISTURE_ROUND
        self.high_calc = self.HIGH - self.LOW
        self.moisture = automationhat.analog[settings.MOISTURE_INPUT]
        self.running = True


    def get_percentage(self) -> float | None:
        try:
            value = self.moisture.read()
            normalize = (value - self.LOW) / self.high_calc
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
                sleep(10)

            if self.retries > self.max_retries:
                self.running = False

        raise Exception(f"Have retried {self.retries} times, will crash and let docker restart us!")


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = Moisture(settings)

    logger.info("Starting moisture")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
