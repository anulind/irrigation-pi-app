import time
import math
import board
import busio
import adafruit_mcp3xxx
from adafruit_mcp3xxx.mcp3008 import MCP3008 as adafruit_MCP3008
import adafruit_bitbangio as bitbangio

pins = {
    'soil_moisture1': {'pin': 3},
    'soil_moisture2': {'pin': 4},
    'soil_moisture3': {'pin': 5},
    'soil_moisture4': {'pin': 6},
    'temperature':    {'pin': 7},
}

class MCP3008:
    def __init__(self, mcp23017):
        print("[MCP3008] Initializing sensor...")

        # spi configuration
        clk_pin = 5
        miso_pin = 4
        mosi_pin = 2
        cs_pin = 3

        clk = mcp23017.sensor.get_pin(clk_pin)
        miso = mcp23017.sensor.get_pin(miso_pin)
        mosi = mcp23017.sensor.get_pin(mosi_pin)
        cs = mcp23017.sensor.get_pin(cs_pin)
        cs.switch_to_output(value=False)

        # Ugly trick to be able to use MCP23017 pins with bitbangio.SPI
        # digitalio.DigitalInOut calls pin.id in the constructor, but MCP23017.DigitalInOut
        # pins don't have that property...
        clk.id = clk_pin
        miso.id = miso_pin
        mosi.id = mosi_pin

        spi = bitbangio.SPI(clk, MOSI=mosi, MISO=miso)
        self.sensor = adafruit_MCP3008(spi, cs)
        print("[MCP3008] configuration complete")

    def read(self, id):
        print("[MCP3008] reading sensor {}".format(id))
        # Number of attempts to read sensor before giving up
        n = 20
        # Number of nonzero readings that we want to get
        m = 10
        # Number of nonzero readings that's good enough
        k = 5

        pin = pins[id]['pin']

        result = []
        for _ in range(0, n):
            try:
                value = self.sensor.read(pin)
                print("[MCP3008] got reading from pin {}: {}".format(pin, value))
                time.sleep(0.5)
                if value > 0:
                    result.append(value)
                if len(result) >= m:
                    break

            except Exception as inst:
                print("[MCP3008] failed to read pin {}, retrying...".format(pin))
                print(type(inst))
                print(inst.args)
                print(inst)

        # If we didn't get enough nonzero readings
        if len(result) < k:
            print("Error: Got {} nonzero readings from MCP3008 pin {}".format(len(result), pin))
            raise Exception("Could not read MCP3008 pin {}".format(pin))

        # Calculate average
        value = sum(result)/len(result)

        # Temperature conversion
        if id == "temperature":
            value = self.convert_temperature(value)

        print("[MCP3008] pin {} value = {}".format(pin, value))

        return {
            id: value
        }

    def convert_temperature(self, value):
        rV = ((1024.0/value) - 1.0)*10000.0
        return round(((1/(1.125614740E-03 + (2.346500768E-04*math.log(rV)) + (0.8600178326E-07*math.pow(math.log(rV), 3))))-273.15), 3)
