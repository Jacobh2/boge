from threading import Thread


class Sensor(Thread):

    def __init__(self):
        super().__init__(name=self.__class__.__name__, daemon=True)
