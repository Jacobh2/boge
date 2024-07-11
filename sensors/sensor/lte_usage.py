"""
Read LTE usage
"""

import subprocess
import re
from mqtt import MQTT
from sensor.sensor import Sensor
from settings import Settings
from time import sleep
import logging

logger = logging.getLogger(__name__)


class USB0Usage(MQTT, Sensor):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        self.running = True

    def get_usb0_data(self) -> tuple[int | None, int | None]:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE)

        logger.info("Result from command: %s", result)
        
        # Decode the byte string to a regular string
        ifconfig_output = result.stdout.decode('utf-8')
        
        # Find the usb0 section
        usb0_section = re.search(r'usb0:\sflags((\n|.)*)', ifconfig_output, re.DOTALL)
        
        if usb0_section:
            usb0_text = usb0_section.group(0)
            
            # Extract RX bytes
            rx_bytes_match = re.search(r'RX packets \d+  bytes (\d+)', usb0_text)
            if rx_bytes_match:
                rx_bytes = int(rx_bytes_match.group(1))
            else:
                logger.warning("Failed to find rx")
                rx_bytes = None
            
            # Extract TX bytes
            tx_bytes_match = re.search(r'TX packets \d+  bytes (\d+)', usb0_text)
            if tx_bytes_match:
                tx_bytes = int(tx_bytes_match.group(1))
            else:
                logger.warning("Failed to find tx")
                tx_bytes = None
            
            return rx_bytes, tx_bytes
        else:
            return None, None

    def run(self):
        self.connect()
        while self.running:
            try:
                rx_bytes, tx_bytes = self.get_usb0_data()

                logger.info("Receied data rx=%s, tx=%s", rx_bytes, tx_bytes)
                data = {
                    "rx": rx_bytes,
                    "tx": tx_bytes
                }

                publish_success = self.publish(data)
                
                if publish_success:
                    self.retries = 0
                else:
                    self.retries += 1
                    logger.info("Failed tp publish to MQTT")
            except Exception:
                logger.warning("Failed to handle usb0 data", exc_info=True)
                self.retries += 1
            finally:
                sleep(60)

            if self.retries > self.max_retries:
                self.running = False

        raise Exception(f"Have retried {self.retries} times, will crash and let docker restart us!")


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = USB0Usage(settings)

    logger.info("Starting USB0 Sensor")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
