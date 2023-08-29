class Relay:
    def __init__(self):
        import automationhat
        self.relay = automationhat.relay.one


    def switch(self, on: bool):
        if on:
            self.relay.on()
        else:
            self.relay.off()

    def is_on(self) -> bool:
        return self.relay.is_on()
