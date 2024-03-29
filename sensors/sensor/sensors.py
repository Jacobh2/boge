"""
Collects all sensors
"""

from datetime import datetime
from os import getenv
from random import randint
import logging
import time

from sensor.humidity import get_humidity
from sensor.moisture import Moisture
from boge.sensors.sensor.switch import Relay
from sensor.voltage import Voltage
from sensor.water import Waterflow
from database import Database

logger = logging.getLogger(__name__)


class Sensors:
    def __init__(self, db: Database):
        self.db = db
        self.debug = getenv("DEBUG") == "true"
        if not self.debug:
            logger.info("Initialising sensors")
            self.humidity = get_humidity()
            self.moisture = Moisture()
            self.relay = Relay()
            self.voltage = Voltage()
            self.waterflow = Waterflow()

    def start_all(self):
        if self.debug:
            return
        self.humidity.start()
        self.moisture.start()
        self.voltage.start()
        self.waterflow.start()

    def stop_all(self):
        if self.debug:
            return
        
        self.humidity.shutdown()

    def switch(self, on: bool):
        if self.debug:
            logger.info("Debugging switch turned to %s", on)
        else:
            self.relay.switch(on)

    def _get_waterflow_data(self):
        # Get total waterflow since last turn-on of pump
        query_timestamp = """
        SELECT
            MAX(src_created_at) AS earliest_timestamp
        FROM (
            SELECT
                src_created_at, 
                LEAD(value, 1, 0) OVER (ORDER BY src_created_at DESC) AS next_value
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
        AND src_created_at >= ?
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
        logger.info("Reading data values...")
        time_start = time.time()
        if self.debug:
            return self.get_random()

        data = {
            "relay_on": self.relay.is_on(),
            "waterflow": self.waterflow.get_flow(),
            "voltage_battery": self.voltage.get_battery_value(),
            "voltage_solar": self.voltage.get_solar_value(),
            "temperature_air": self.humidity.get_temperature(),
            "humidity_air": self.humidity.get_humidity(),
            "moisture_ground": self.moisture.get_moisture(),
            "temperature_ground": None,
        }

        time_sensors = (time.time() - time_start) * 1000
        time_start = time.time()

        waterflow_sum, waterflow_since = self._get_waterflow_data()
        data["waterflow_sum"] = waterflow_sum
        data["waterflow_since"] = waterflow_since

        logger.info(
            "Sensors read after %s ms. Calculated from db after %s ms",
            time_sensors,
            (time.time() - time_start) * 1000,
        )

        return data

    def check_sensor_status(self) -> dict[str, bool]:
        if self.debug:
            logger.info("In debug mode")
            return {
                "relay_on": randint(1, 2) == 1,
                "waterflow": randint(1, 2) == 1,
                "voltage_battery": randint(1, 2) == 1,
                "voltage_solar": randint(1, 2) == 1,
                "temperature_air": randint(1, 2) == 1,
                "humidity_air": randint(1, 2) == 1,
                "moisture_ground": randint(1, 2) == 1,
                "temperature_ground": randint(1, 2) == 1,
                "waterflow_sum": randint(1, 2) == 1,
                "waterflow_since": randint(1, 2) == 1,
            }

        return {
            "relay_on": self.relay.get_status(),
            "waterflow": self.waterflow.get_status(),
            "voltage_battery": self.voltage.get_battery_status(),
            "voltage_solar": self.voltage.get_solar_status(),
            "temperature_air": self.humidity.get_temperature_status(),
            "humidity_air": self.humidity.get_humidity_status(),
            "moisture_ground": self.moisture.get_status(),
            "temperature_ground": False,
        }
