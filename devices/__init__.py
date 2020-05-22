from devices.AM2320 import AM2320 as AM2320

class Devices:
    def __init__(self):
        self.AM2320 = AM2320()

def init():
    return Devices()
