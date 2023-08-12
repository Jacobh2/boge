import automationhat
from time import sleep

while True:
    v = automationhat.analog.one.read()
    print(f"{v=}")
    sleep(0.3)
    