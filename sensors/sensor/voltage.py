from sensor.sensor import Sensor
from time import sleep
import logging

logger = logging.getLogger(__name__)


class Voltage(Sensor):
    def __init__(self):
        super().__init__()
        import automationhat

        self.battery = automationhat.analog.one
        self.solar = automationhat.analog.three

        self.battery_value = None
        self.solar_value = None

        self.last_battery_value_ok = False
        self.last_solar_value_ok = False

    def get_battery(self) -> float:
        return self.battery.read()

    def get_solar(self) -> float:
        return self.solar.read()

    def run(self):

        while True:
            try:
                self.battery_value = self.get_battery()
                self.last_battery_value_ok = True
            except Exception:
                self.last_battery_value_ok = False
                logger.warning("Failed to read battery voltage", exc_info=True)

            try:
                sleep(5)
                self.solar_value = self.get_solar()
                self.last_solar_value_ok = True
            except Exception:
                logger.warning("Failed to read voltage", exc_info=True)
                self.last_solar_value_ok = False
            finally:
                sleep(20)

    def get_battery_value(self):
        return self.battery_value

    def get_solar_value(self):
        return self.solar_value

    def get_battery_status(self) -> bool:
        logger.info("Battery read ok: %s and is alive: %s", self.last_battery_value_ok, self.is_alive())
        return self.last_battery_value_ok and self.is_alive()

    def get_solar_status(self) -> bool:
        logger.info("Solar read ok: %s and is alive: %s", self.last_solar_value_ok, self.is_alive())
        return self.last_solar_value_ok and self.is_alive()