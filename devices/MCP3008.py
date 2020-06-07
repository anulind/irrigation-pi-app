import time
import math
import board
import busio
import adafruit_mcp3xxx
from adafruit_mcp3xxx.mcp3008 import MCP3008 as adafruit_MCP3008
import lib.bitbangio as bitbangio

pins = [
    {'pin': 3, 'name': 'soil_moisture_1'},
    {'pin': 4, 'name': 'soil_moisture_2'},
    {'pin': 5, 'name': 'soil_moisture_3'},
    {'pin': 6, 'name': 'soil_moisture_4'},
    {'pin': 7, 'name': 'temperature'},
]

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

        spi = bitbangio.SPI(clk, MOSI=mosi, MISO=miso)
        self.sensor = adafruit_MCP3008(spi, cs)

        # Helpers
        self.pins_by_name = {}
        self.pins_by_number = {}

        for setup in pins:
            self.pins_by_number[setup.get('pin')] = setup
            self.pins_by_name[setup.get('name')] = setup

        print("[MCP3008] configuration complete")

    def get_pin_info(self, id):
        setup = self.pins_by_name[id] if isinstance(id, str) else self.pins_by_number[id]
        return setup.get('pin'), setup.get('name')

    def read(self, id):
        print("[MCP3008] reading sensor {}".format(id))
        # Number of attempts to read sensor before giving up
        n = 20
        # Number of nonzero readings that we want to get
        m = 10
        # Number of nonzero readings that's good enough
        k = 5

        pin_number, pin_name = self.get_pin_info(id)

        result = []

        print("[MCP3008] reading pin {}:".format(pin_name), end=' ')
        for _ in range(0, n):
            try:
                value = self.sensor.read(pin_number)
                print(value, end=' ')
                if value > 0:
                    result.append(value)
                if len(result) >= m:
                    break
                time.sleep(0.5)

            except Exception:
                print('fail', end=' ')

        print('')

        # If we didn't get enough nonzero readings
        if len(result) < k:
            print("Error: Got {} nonzero readings from MCP3008 pin {}".format(len(result), pin_name))
            raise Exception("Could not read MCP3008 pin {}".format(pin_name))

        # Calculate average
        value = sum(result)/len(result)

        # Temperature conversion
        if pin_name == "temperature":
            value = self.convert_temperature(value)

        print("[MCP3008] pin {} value = {}".format(pin_name, value))

        return {
            pin_name: value
        }

    def convert_temperature(self, value):
        rV = ((1024.0/value) - 1.0)*10000.0
        return round(((1/(1.125614740E-03 + (2.346500768E-04*math.log(rV)) + (0.8600178326E-07*math.pow(math.log(rV), 3))))-273.15), 3)
