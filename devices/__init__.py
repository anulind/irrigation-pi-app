from devices.AM2320 import AM2320 as AM2320
from devices.BMP280 import BMP280 as BMP280
from devices.TSL2561 import TSL2561 as TSL2561
from devices.HCSR04 import HCSR04 as HCSR04
from devices.MCP23017 import MCP23017 as MCP23017
from devices.MCP3008 import MCP3008 as MCP3008

class Devices:
    def __init__(self):
        self.AM2320 = AM2320()
        self.BMP280 = BMP280()
        self.TSL2561 = TSL2561()
        self.HCSR04 = HCSR04()
        self.MCP23017 = MCP23017()
        self.MCP3008 = MCP3008(self.MCP23017)

    def disconnect(self):
        self.HCSR04.cleanup()
        self.MCP23017.disconnect()

def init():
    return Devices()
