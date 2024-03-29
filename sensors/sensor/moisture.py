from sensor.sensor import Sensor
from time import sleep
import logging

logger = logging.getLogger(__name__)


class Moisture(Sensor):
    # Approx values for when in air and in water.
    # Low = The value when in water
    # High = The value when dry in air
    LOW = 2.0
    HIGH = 4.966

    def __init__(self):
        super().__init__()
        import automationhat

        self.high_calc = self.HIGH - self.LOW
        self.moisture = automationhat.analog.two
        self.value = None
        self.last_read_ok = False

    def get_percentage(self) -> float:
        value = self.moisture.read()
        normalize = (value - self.LOW) / self.high_calc
        inverted = 1 - normalize
        percentage = inverted * 100
        rounded = round(percentage, 2)
        return max(min(rounded, 100.0), 0.0)

    def run(self):
        while True:
            try:
                self.value = self.get_percentage()
                self.last_read_ok = True
            except Exception:
                self.last_read_ok = False
                logger.warning("Failed to read moisture", exc_info=True)
            finally:
                sleep(10)

    def get_moisture(self):
        return self.value

    def get_status(self) -> bool:
        return self.last_read_ok and self.is_alive()
