"""
Read and delete sms
"""

from mqtt import MQTT
from sensor.sensor import Sensor
from settings import Settings
from time import sleep
import logging
from zte_modem import ZTEModem

logger = logging.getLogger(__name__)


class ZTESMSSensor(MQTT, Sensor):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        Sensor.__init__(self)
        self.modem = ZTEModem()
        self.running = True

    def run(self):
        self.connect()
        while self.running:
            try:
                self.modem.auth()

                sms = self.modem.list_sms()

                # Publish sms
                publish_success = self.publish(sms)
                
                # Delete the sms from the modem
                for s in sms:
                    self.modem.delete_sms(s)

                if publish_success:
                    self.retries = 0
                else:
                    self.retries += 1
                    logger.info("Failed tp publish to MQTT")
            except Exception:
                logger.warning("Failed to handle sms", exc_info=True)
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

    switch = ZTESMSSensor(settings)

    logger.info("Starting SMS Sensor")
    switch.start()

    logger.info("Waiting for join")
    switch.join()
