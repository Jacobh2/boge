

class Humidity:
    DHT_PIN = 4
    ERROR_IN_ROW_LIMIT = 10

    def __init__(self):
        import adafruit_dht
        self.device = adafruit_dht.DHT22(self.DHT_PIN)
        self.prev_humidity: float = -999
        self.prev_temperature: float = -999
        self.errors_in_row = 0

    def try_get_temperature(self):
        try:
            self.prev_temperature = self.device.temperature
        except RuntimeError as e:
            self.errors_in_row += 1
            if self.errors_in_row > self.ERROR_IN_ROW_LIMIT:
                self.errors_in_row = 0
                raise Exception(f"Failed to read temperature: {e}") from e
        return self.prev_temperature

    def try_get_humidity(self):
        try:
            self.prev_humidity = self.device.humidity
        except RuntimeError as e:
            self.errors_in_row += 1
            if self.errors_in_row > self.ERROR_IN_ROW_LIMIT:
                self.errors_in_row = 0
                raise Exception(f"Failed to read humidity: {e}") from e
        return self.prev_humidity
