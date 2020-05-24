from devices.AM2320 import AM2320 as AM2320
from devices.BMP280 import BMP280 as BMP280

class Devices:
    def __init__(self):
        self.AM2320 = AM2320()
        self.BMP280 = BMP280()

def init():
    return Devices()
