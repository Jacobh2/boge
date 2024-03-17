from sensor.sensor import Sensor
from time import sleep
import logging

logger = logging.getLogger(__name__)


class Voltage(Sensor):
    def __init__(self):
        import automationhat

        self.battery = automationhat.analog.one
        self.solar = automationhat.analog.three

        self.battery_value = None
        self.solar_value = None

    def get_battery(self) -> float:
        return self.battery.read()

    def get_solar(self) -> float:
        return self.solar.read()

    def run(self):

        while True:
            try:
                self.battery_value = self.get_battery()
                sleep(5)
                self.solar_value = self.get_solar()
            except Exception:
                logger.warning("Failed to read voltage", exc_info=True)
            finally:
                sleep(20)

    def get_battery_value(self):
        return self.battery_value

    def get_solar_value(self):
        return self.solar_value
