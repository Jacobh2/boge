import sqlite3


class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS sensor (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
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
            SELECT value, created_at
            FROM sensor
            WHERE name = ?
            ORDER BY created_at DESC
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
            SELECT DISTINCT name, value, created_at
            FROM sensor
            INNER JOIN (
                SELECT name, MAX(created_at) AS max_created_at
                FROM sensor
                GROUP BY name
            ) latest ON sensor.name = latest.name AND sensor.created_at = latest.max_created_at;
        """
        cursor = self.conn.execute(query)
        results = cursor.fetchall()
        return results
    
    def cleanup_data(self):
        query = """
        DELETE FROM sensor
        WHERE created_at < datetime('now', '-1 month');
        """
        self.conn.execute(query)
        self.conn.commit()
        
