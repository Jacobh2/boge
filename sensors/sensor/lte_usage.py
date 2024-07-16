"""
Read LTE usage
"""

import json
import subprocess
from pathlib import Path
import re
import time
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
        # Setup the local file store
        self.local_store = Path(settings.LOCAL_FILE_STORE_PATH)

    def get_usb0_data(self) -> tuple[int | None, int | None]:
        # Run the ifconfig command
        result = subprocess.run(["ifconfig"], stdout=subprocess.PIPE)

        if result.returncode != 0:
            logger.warning("The subprocess did not return code 0: %s", result)
            return None, None

        logger.info("Result from command: %s", result)

        # Decode the byte string to a regular string
        ifconfig_output = result.stdout.decode("utf-8")

        # Find the usb0 section
        usb0_section = re.search(r"usb0:\sflags((\n|.)*)", ifconfig_output, re.DOTALL)

        if usb0_section:
            usb0_text = usb0_section.group(0)

            # Extract RX bytes
            rx_bytes_match = re.search(r"RX packets \d+  bytes (\d+)", usb0_text)
            if rx_bytes_match:
                rx_bytes = int(rx_bytes_match.group(1))
            else:
                logger.warning("Failed to find rx")
                rx_bytes = None

            # Extract TX bytes
            tx_bytes_match = re.search(r"TX packets \d+  bytes (\d+)", usb0_text)
            if tx_bytes_match:
                tx_bytes = int(tx_bytes_match.group(1))
            else:
                logger.warning("Failed to find tx")
                tx_bytes = None

            return rx_bytes, tx_bytes
        else:
            return None, None

    def _setup_cache(self) -> None | tuple[int, int]:
        try:
            # Check if the file exist, if it does, try to
            # read existing data from it. otherwise skip
            if not self.local_store.exists():
                return None

            with self.local_store.open() as f:
                existing = json.load(f)

            return existing.get("rx"), existing.get("tx")
        except Exception:
            logger.warning("Failed to read cache!", exc_info=True)

        return None

    def _store_cache(self, rx_bytes: int, tx_bytes: int):
        try:
            with self.local_store.open("w") as f:
                json.dump({"rx": rx_bytes, "tx": tx_bytes}, f)
        except Exception:
            logger.warning("Failed to store cache!", exc_info=True)

    def run(self):
        self.connect()

        rx_bytes = 0
        tx_bytes = 0

        if existing := self._setup_cache():
            maybe_rx_bytes, maybe_tx_bytes = existing
            logger.info(
                "Found existing data, starting at rx=%s & tx=%s", rx_bytes, tx_bytes
            )
            # Now we need to check if this existing data actually should be used:
            # Only if the read data is less than the stored data. Otherwise it
            # can be that we have been restarted without the raspberry pi being
            # restarted, hence we will already have the correct values when reading.
            # So we only store/use the data if it less than the last read state.
            current_rx, current_tx = self.get_usb0_data()
            if current_rx is not None and current_tx is not None:
                # Check if the read values are below cache,
                # if so, then use it!
                logger.info("Current values are rx=%s, tx=%s", current_rx, current_tx)
                logger.info("Last cache is rx=%s & tx=%s", maybe_rx_bytes, maybe_tx_bytes)
                if current_rx < maybe_rx_bytes and current_tx < maybe_tx_bytes:
                    logger.info("Current is less than cache, so setting cache as base")
                    rx_bytes = maybe_rx_bytes
                    tx_bytes = maybe_tx_bytes
                else:
                    logger.info("Current is more or equal to cache, so skip setting a new base")

        last_save_time = 0

        while self.running:
            try:
                rx_bytes_delta, tx_bytes_delta = self.get_usb0_data()
                logger.info("Receied data rx=%s, tx=%s", rx_bytes, tx_bytes)

                rx_bytes += rx_bytes_delta
                tx_bytes += tx_bytes_delta

                data = {"rx": rx_bytes, "tx": tx_bytes}

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
                # Only store cache every hour
                hour = 3600
                if time.time() - last_save_time > hour:
                    logger.info("Storing cache")
                    self._store_cache(rx_bytes, tx_bytes)

                sleep(60)

            if self.retries > self.max_retries:
                self.running = False

        raise Exception(
            f"Have retried {self.retries} times, will crash and let docker restart us!"
        )


if __name__ == "__main__":
    from log import setup_logging

    settings = Settings()

    setup_logging(settings)

    switch = USB0Usage(settings)

    logger.info("Starting USB0 Sensor")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
