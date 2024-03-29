from mqtt import MQTT
from sensor.sensor import Sensor
from settings import Settings
from time import sleep
import logging

logger = logging.getLogger(__name__)


class Voltage(MQTT, Sensor):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        import automationhat

        self.battery = automationhat.analog.one
        self.solar = automationhat.analog.three

        self.running = True

    def get_battery(self) -> float | None:
        try:
            return self.battery.read()
        except Exception:
            logger.warning("Failed to read battery voltage", exc_info=True)
        return None

    def get_solar(self) -> float | None:
        try:
            return self.solar.read()
        except Exception:
            logger.warning("Failed to read solar voltage", exc_info=True)
        return None

    def run(self):
        self.connect()
        while self.running:
            try:
                battery_value = self.get_battery()
                sleep(0.5)
                solar_value = self.get_solar()
                # Publish
                self.publish({"battery": battery_value, "solar": solar_value})
                self.retries = 0
            except Exception:
                logger.warning("Failed to read value", exc_info=True)
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

    switch = Voltage(settings)

    logger.info("Starting voltage")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
