import time
import math
import board
import busio
import adafruit_mcp3xxx
from adafruit_mcp3xxx.mcp3008 import MCP3008 as adafruit_MCP3008
import lib.bitbangio as bitbangio
import devices.mqtt_methods as mqtt_methods
import logging

pins = [
    {'pin': 3, 'name': 'soil_moisture_1'},
    {'pin': 4, 'name': 'soil_moisture_2'},
    {'pin': 5, 'name': 'soil_moisture_3'},
    {'pin': 6, 'name': 'soil_moisture_4'},
    {'pin': 7, 'name': 'temperature'},
]

class MCP3008(mqtt_methods.Mixin):
    def __init__(self, mcp23017):
        logging.debug("[MCP3008] Initializing sensor...")

        # spi configuration
        clk = mcp23017.get_pin('clk')
        miso = mcp23017.get_pin('miso')
        mosi = mcp23017.get_pin('mosi')
        cs = mcp23017.get_pin('cs')

        spi = bitbangio.SPI(clk, MOSI=mosi, MISO=miso)
        self.sensor = adafruit_MCP3008(spi, cs)

        # Helpers
        self.pins_by_name = {}
        self.pins_by_number = {}

        for setup in pins:
            self.pins_by_number[setup.get('pin')] = setup
            self.pins_by_name[setup.get('name')] = setup

        logging.debug("[MCP3008] configuration complete")

    def get_pin_info(self, id):
        setup = self.pins_by_name[id] if isinstance(id, str) else self.pins_by_number[id]
        return setup.get('pin'), setup.get('name')

    def read(self, id):
        logging.debug("[MCP3008] reading sensor {}".format(id))
        # Number of attempts to read sensor before giving up
        n = 20
        # Number of nonzero readings that we want to get
        m = 10
        # Number of nonzero readings that's good enough
        k = 5

        pin_number, pin_name = self.get_pin_info(id)

        result = []

        logging.debug("[MCP3008] reading pin {}:".format(pin_name))
        for _ in range(0, n):
            try:
                value = self.sensor.read(pin_number)
                logging.debug(">>>> {}".format(value))
                if value > 0:
                    result.append(value)
                if len(result) >= m:
                    break
                time.sleep(0.5)

            except Exception:
                logging.exception(">>>> [MCP3008] fail")

        # If we didn't get enough nonzero readings
        if len(result) < k:
            raise Exception("Got {} nonzero readings from MCP3008 pin {}".format(len(result), pin_name))

        # Calculate average
        value = sum(result)/len(result)

        # Temperature conversion
        if pin_name == "temperature":
            value = self.convert_temperature(value)

        logging.debug("[MCP3008] pin {} value = {}".format(pin_name, value))

        return {
            pin_name: value
        }

    def convert_temperature(self, value):
        rV = ((1024.0/value) - 1.0)*10000.0
        return round(((1/(1.125614740E-03 + (2.346500768E-04*math.log(rV)) + (0.8600178326E-07*math.pow(math.log(rV), 3))))-273.15), 1)
