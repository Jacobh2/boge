class Relay:
    def __init__(self):
        import automationhat

    def switch(self, on: bool):
        if on:
            automationhat.relay.one.on()
        else:
            automationhat.relay.one.off()

    def is_on(self) -> bool:
        return automationhat.relay.one.is_on()
