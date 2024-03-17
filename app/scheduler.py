from apscheduler.schedulers.background import BackgroundScheduler
from database import Database
from sensor.sensors import Sensors
import logging


logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self, sensors: Sensors, db: Database):
        self.sensors = sensors
        self.db = db
        self.scheduler = BackgroundScheduler()

        # Every 5th minute
        self.scheduler.add_job(
            self.save_data_to_database,
            trigger="interval",
            minutes=5
        )

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown(wait=True)

    def save_data_to_database(self):
        logger.info("Reading data")
        # Get data
        data = self.sensors.get_dict()

        logger.info("Got data %s, saving to db", data)
        try:
            for name, value in data.items():
                if value is not None:
                    self.db.add_new_value(name, str(value))
        except:
            logger.exception("Failed to save data to database")
