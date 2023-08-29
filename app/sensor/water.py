"""
When the water preassure is higher, it is more accurate!

At low preassure (aka low L/min), it tends to be lower,
by approd 23%, so an increase of 30% (factor of 1.3) could
be applied to be more accurate. This should only be applied
on values up to at most 8.8 L/min, then we remove the factor
"""
import time
from threading import Thread


class Waterflow(Thread):
    # We will most prob take pin 9
    # due to the automation phat used
    FLOW_SENSOR_GPIO = 9
    # Sleep time
    SLEEP_TIME = 1
    # Pulse frequency (Hz) = 7.50
    PULSE_FREQUENCY = 7.5
    # Factor to apply below 8.8 L/m
    FACTOR = 1.3

    def __init__(self):
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.count = 0
        self.flow = 0
        self.running = True

        GPIO.add_event_detect(
            self.FLOW_SENSOR_GPIO, GPIO.FALLING, callback=self._count_pulse
        )

    def _count_pulse(self, channel):
        self.count += 1

    def run(self):
        while self.running:
            try:
                time.sleep(self.SLEEP_TIME)
                self.flow = self.count / self.PULSE_FREQUENCY / self.SLEEP_TIME
                if self.flow < 8.8:
                    self.flow *= self.FACTOR
                self.count = 0
            except Exception as e:
                print("Failure to read flow:", e)
                time.sleep(20)

        GPIO.cleanup()

    def get_flow(self) -> float:
        return self.flow