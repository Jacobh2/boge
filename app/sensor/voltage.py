class Voltage:
    def __init__(self):
        import automationhat
        self.battery = automationhat.analog.one
        self.solar = automationhat.analog.three

    def get_battery(self) -> float:
        return self.battery.read()

    def get_solar(self) -> float:
        return self.solar.read()
