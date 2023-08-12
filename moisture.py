import automationhat
from time import sleep
from textwrap import dedent

class Moisture:

    # Approx values for when in air and in water.
    # Low = The value when in water
    # High = The value when dry in air
    LOW = 2.0
    HIGH = 4.966

    def __init__(self):
        self.high_calc = self.HIGH-self.LOW

    def read_raw(self) -> float:
        return automationhat.analog.two.read()

    def get_percentage(self, value: float) -> float:
        normalize = (value - self.LOW) / self.high_calc
        inverted = 1 - normalize
        percentage = inverted * 100
        rounded = round(percentage, 2)
        return max(min(rounded, 100.0), 0.0)


def format(value: float, calc: float) -> str:
    text = f"""
    Raw:  {value}
    Calc: {calc}%
    """
    text = dedent(text).strip()
    return text

if __name__ == "__main__":
    m = Moisture()

    while True:
        value = m.read_raw()
        calc = m.get_percentage(value)
        text = format(value, calc)
        print(text)
        sleep(1)

