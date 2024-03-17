from functools import lru_cache
from os import getenv

from sensor.sensors import Sensors
from database import Database


def get_db_path() -> str:
    return getenv("DB_PATH", "sensors.db")


@lru_cache()
def get_db() -> Database:
    db = Database(get_db_path())
    db.connect()
    return db


@lru_cache()
def get_sensors() -> Sensors:
    return Sensors(get_db())
