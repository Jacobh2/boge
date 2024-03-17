"""
Collects all sensors
"""

from datetime import datetime
from os import getenv
from random import randint
import logging
import time

from sensor.humidity import Humidity
from sensor.moisture import Moisture
from sensor.relay import Relay
from sensor.voltage import Voltage
from sensor.water import Waterflow
from database import Database

logger = logging.getLogger(__name__)


class Sensors:
    def __init__(self, db: Database):
        self.db = db
        self.debug = getenv("DEBUG") == "true"
        if not self.debug:
            self.humidity = Humidity()
            self.moisture = Moisture()
            self.relay = Relay()
            self.voltage = Voltage()
            self.waterflow = Waterflow()

    def switch(self, on: bool):
        if self.debug:
            logger.info("Debugging switch turned to %s", on)
        else:
            self.relay.switch(on)

    def _get_waterflow_data(self):
        # Get total waterflow since last turn-on of pump
        query_timestamp = """
        SELECT
            MAX(created_at) AS earliest_timestamp
        FROM (
            SELECT
                created_at, 
                LEAD(value, 1, 0) OVER (ORDER BY created_at DESC) AS next_value
            FROM sensor
            WHERE name = 'relay_on'
        )
        WHERE next_value = 'False'
        """
        cur = self.db.conn.execute(query_timestamp)
        if result := cur.fetchone():
            waterflow_since = result[0]
        else:
            waterflow_since = None

        query = """
        SELECT
            sum(cast(value as float))
        FROM sensor
        WHERE name='waterflow'
        AND created_at >= ?
        GROUP BY name
        """
        cur = self.db.conn.execute(query, (waterflow_since,))
        if result := cur.fetchone():
            waterflow_sum = round(result[0], 1)
        else:
            waterflow_sum = None

        return waterflow_sum, waterflow_since

    def get_random(self):
        return {
            "relay_on": randint(1, 2) == 1,
            "waterflow": randint(0, 20) / 10,
            "voltage_battery": randint(110, 130) / 10,
            "voltage_solar": randint(20, 140) / 10,
            "temperature_air": randint(190, 250) / 10,
            "humidity_air": randint(0, 1000) / 1000,
            "moisture_ground": randint(0, 1000) / 1000,
            "temperature_ground": None,
            "waterflow_sum": round(time.time() / 10000000),
            "waterflow_since": datetime.now(),
        }

    def get_dict(self) -> dict:
        if self.debug:
            return self.get_random()

        data = {
            "relay_on": self.relay.is_on(),
            "waterflow": self.waterflow.get_flow(),
            "voltage_battery": self.voltage.get_battery(),
            "voltage_solar": self.voltage.get_solar(),
            "temperature_air": self.humidity.try_get_temperature(),
            "humidity_air": self.humidity.try_get_humidity(),
            "moisture_ground": self.moisture.get_percentage(),
            "temperature_ground": None,
        }

        waterflow_sum, waterflow_since = self._get_waterflow_data()
        data["waterflow_sum"] = waterflow_sum
        data["waterflow_since"] = waterflow_since

    def check_sensor_status(self):
        logger.info("Watersensor thread alive: %s", self.waterflow.is_alive())
