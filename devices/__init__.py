from devices.AM2320 import AM2320 as AM2320
from devices.BMP280 import BMP280 as BMP280
from devices.TSL2561 import TSL2561 as TSL2561
from devices.HCSR04 import HCSR04 as HCSR04

class Devices:
    def __init__(self):
        self.AM2320 = AM2320()
        self.BMP280 = BMP280()
        self.TSL2561 = TSL2561()
        self.HCSR04 = HCSR04()

    def disconnect(self):
        self.HCSR04.cleanup()

def init():
    return Devices()
