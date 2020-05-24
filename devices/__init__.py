from devices.AM2320 import AM2320 as AM2320
from devices.BMP280 import BMP280 as BMP280
from devices.TSL2561 import TSL2561 as TSL2561

class Devices:
    def __init__(self):
        self.AM2320 = AM2320()
        self.BMP280 = BMP280()
        self.TSL2561 = TSL2561()

def init():
    return Devices()
