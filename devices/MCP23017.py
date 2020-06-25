import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017 as adafruit_MCP23017
import time
import devices.mqtt_methods as mqtt_methods
import logging

pins = [
    {'pin': 9,  'name': 'pump1',     'output': True},
    {'pin': 8,  'name': 'pump2',     'output': True},
    {'pin': 11, 'name': 'pump3',     'output': True},
    {'pin': 12, 'name': 'pump4',     'output': True},
    {'pin': 13, 'name': 'pump5',     'output': True},
    {'pin': 14, 'name': 'pump6',     'output': True},
    {'pin': 15, 'name': 'pump7',     'output': True},
    {'pin': 7,  'name': 'got_water', 'output': False},
    {'pin': 5,  'name': 'clk',       'output': False},
    {'pin': 4,  'name': 'miso',      'output': False},
    {'pin': 2,  'name': 'mosi',      'output': False},
    {'pin': 3,  'name': 'cs',        'output': True},
]

class MCP23017(mqtt_methods.Mixin):
    def __init__(self):
        logging.debug("[MCP23017] Initializing sensor...")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_MCP23017(i2c)

        # Helpers
        self.pins_by_name = {}
        self.pins_by_number = {}

        for setup in pins:
            pin_number = setup.get('pin')
            pin_name = setup.get('name')

            # Fill in helpers for later usage
            self.pins_by_name[pin_name] = setup
            self.pins_by_number[pin_number] = setup

            pin = self.sensor.get_pin(pin_number)
            # Set pin as output
            if setup['output']:
                pin.switch_to_output(value=False)
        logging.debug("[MCP23017] configuration complete")

    def get_pin_info(self, id):
        setup = self.pins_by_name[id] if isinstance(id, str) else self.pins_by_number[id]
        return setup.get('pin'), setup.get('name')

    # Get pin by human readable id or pin number
    def get_pin(self, id):
        if isinstance(id, str):
            return self.sensor.get_pin(self.pins_by_name[id]['pin'])
        return self.sensor.get_pin(id)

    def read(self, id):
        logging.debug("[MCP23017] reading pin {}".format(id))
        pin_number, pin_name = self.get_pin_info(id)
        pin = self.sensor.get_pin(pin_number)
        value = int(pin.value == True)
        logging.debug("[MCP23017] pin {} = {}".format(id, value))
        return {
            pin_name: value
        }

    def set_value(self, id, target):
        logging.debug("[MCP23017] setting pin {} to {}".format(id, target))
        pin = self.get_pin(id)
        pin.value = target
        logging.debug("[MCP23017] target set")

    def disconnect(self, mqtt=None):
        logging.debug("[MCP23017] disconnecting device")
        # Make sure all relays are off
        for setup in pins:
            if setup['output'] and setup['name'] != 'cs':
                try:
                    # Check if relay is already off
                    status = self.read(setup['name'])[setup['name']]
                    # If not, try to turn it off
                    if status == 1:
                        if mqtt:
                            self.set_and_publish(mqtt, setup['name'], 0, origin="disconnect")
                        else:
                            self.set_value(setup['name'], 0)
                        logging.info("Relay {} off".format(setup['name']))
                except Exception as e:
                    logging.error("Failed to make sure pin {} is off".format(setup['name']))
                    logging.error(e, exc_info=True)
        logging.debug("[MCP23017] disconnected")
