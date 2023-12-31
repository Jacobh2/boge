
class Humidity:
    ERROR_IN_ROW_LIMIT = 10

    def __init__(self):
        import adafruit_dht
        import board
        self.device = adafruit_dht.DHT22(board.D4)
        self.prev_humidity: float = -999
        self.prev_temperature: float = -999
        self.errors_in_row = 0

    def try_get_temperature(self):
        try:
            self.prev_temperature = self.device.temperature
        except RuntimeError as e:
            self.errors_in_row += 1
            if self.errors_in_row > self.ERROR_IN_ROW_LIMIT:
                print("Failed to read temperature after", self.errors_in_row, "-", e)
        return self.prev_temperature

    def try_get_humidity(self):
        try:
            self.prev_humidity = self.device.humidity
        except RuntimeError as e:
            self.errors_in_row += 1
            if self.errors_in_row > self.ERROR_IN_ROW_LIMIT:
                print("Failed to read humidity after", self.errors_in_row, "-", e)
        return self.prev_humidity
