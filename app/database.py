import sqlite3


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.create_table()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def create_table(self):
        queries = [
            """
                CREATE TABLE IF NOT EXISTS sensor (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value TEXT NOT NULL,
                    src_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """,
            "CREATE INDEX IF NOT EXISTS sensor_name_time_hour ON sensor (name, strftime('%Y-%m-%d %H:00:00', src_created_at));",
            "CREATE INDEX IF NOT EXISTS sensor_name_time ON sensor (name, src_created_at DESC);",
        ]
        for query in queries:
            self.conn.execute(query)
            self.conn.commit()

    def add_new_value(self, name: str, value: str):
        query = """
            INSERT INTO sensor (name, value)
            VALUES (?, ?);
        """
        self.conn.execute(query, (name, value))
        self.conn.commit()

    def get_latest_value_by_name(self, name: str):
        query = """
            SELECT value, src_created_at
            FROM sensor
            WHERE name = ?
            ORDER BY src_created_at DESC
            LIMIT 1;
        """
        cursor = self.conn.execute(query, (name,))
        result = cursor.fetchone()
        if result:
            value, timestamp = result
            return value, timestamp
        return None, None

    def get_latest_values_for_all_sensors(self):
        query = """
            SELECT DISTINCT name, value, src_created_at
            FROM sensor
            INNER JOIN (
                SELECT name, MAX(src_created_at) AS max_created_at
                FROM sensor
                GROUP BY name
            ) latest ON sensor.name = latest.name AND sensor.src_created_at = latest.max_created_at;
        """
        cursor = self.conn.execute(query)
        results = cursor.fetchall()
        return results

    def cleanup_data(self):
        query = """
        DELETE FROM sensor
        WHERE src_created_at < datetime('now', '-1 month');
        """
        self.conn.execute(query)
        self.conn.commit()
