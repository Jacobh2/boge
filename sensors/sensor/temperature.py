"""
Reading the DS18B20 sensor

This sensor requires 3.3v
Data pin goes to pin GPIO4
"""
from settings import Settings
from mqtt import MQTT
from sensor.sensor import Sensor
from time import sleep
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


class Temperature(MQTT, Sensor):

    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        self.running = True
        self.device_path = Path(f"/sys/bus/w1/devices/{settings.DEVICE_ID}/w1_slave")
        assert self.device_path.exists(), f"Wrong device or no device ID set: {self.device_path}"

    def _try_read_temperature(self) -> float | None:
        try:
            with self.device_path.open() as f:
                lines = f.readlines()

            # Check if OK read
            if not lines[0].strip().endswith("YES"):
                return None
            
            raw_temp_idx = lines[1].strip().find("t=")
            if raw_temp_idx < 0:
                return None
            
            temperature = float(lines[1].strip()[raw_temp_idx+2:]) / 1000.0

            return temperature
        except Exception:
            logger.exception("Failed to read temperature!")


    def run(self):
        self.connect()

        while self.running:
            try:
                temperature = self._try_read_temperature()

                # Publish!
                if temperature:
                    self.publish(temperature)
            except Exception:
                logger.warning("Failed to read temperature", exc_info=True)
            finally:
                sleep(30)

        logger.info("Shutting down")

if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = Temperature(settings)

    logger.info("Starting temperature")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
