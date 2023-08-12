from time import sleep
import adafruit_dht


class Humidity:

    DHT_PIN = 4

    def __init__(self):
        self.device = adafruit_dht.DHT22(self.DHT_PIN)
        self.prev_humidity = None
        self.prev_temperature = None

    def try_get_temperature(self):
        try:
            self.prev_temperature = self.device.temperature
        except RuntimeError as e:
            print("Error reading:", e)
        return self.prev_temperature

    def try_get_humidity(self):
        try:
            self.prev_humidity = self.device.humidity
        except RuntimeError as e:
            print("Error reading:", e)
        return self.prev_humidity


if __name__ == "__main__":
    h = Humidity()

    while True:

        humidity = h.try_get_humidity()
        temperature = h.try_get_temperature()

        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))

        sleep(2)