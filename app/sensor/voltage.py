class Voltage:
    def __init__(self):
        import automationhat

    def get_battery(self) -> float:
        return automationhat.analog.one.read()

    def get_solar(self) -> float:
        return automationhat.analog.two.read()
