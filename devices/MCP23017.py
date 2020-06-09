import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017 as adafruit_MCP23017
import time
import devices.mqtt_methods as mqtt_methods

pins = [
    {'pin': 9,  'name': 'pow1',            'output': True},
    {'pin': 9,  'name': 'pump1',           'output': True},
    {'pin': 11, 'name': 'pump2',           'output': True},
    {'pin': 13, 'name': 'pump3',           'output': True},
    {'pin': 15, 'name': 'pump4',           'output': True},
    {'pin': 7,  'name': 'watertank_empty', 'output': False},
]

class MCP23017(mqtt_methods.Mixin):
    def __init__(self):
        print("[MCP23017] Initializing sensor...")
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
        print("[MCP23017] configuration complete")

    def get_pin_info(self, id):
        setup = self.pins_by_name[id] if isinstance(id, str) else self.pins_by_number[id]
        return setup.get('pin'), setup.get('name')

    # Get pin by human readable id or pin number
    def get_pin(self, id):
        if isinstance(id, str):
            return self.sensor.get_pin(self.pins_by_name[id]['pin'])
        return self.sensor.get_pin(id)

    def read(self, id):
        print("[MCP23017] reading pin {}".format(id))
        pin_number, pin_name = self.get_pin_info(id)
        pin = self.sensor.get_pin(pin_number)
        value = pin.value
        print("[MCP23017] pin {} = {}".format(id, value))
        return {
            pin_name: value
        }

    def set_value(self, id, target):
        print("[MCP23017] setting pin {} to {}".format(id, target))
        pin = self.get_pin(id)
        pin.value = target
        print("[MCP23017] target set")

    def disconnect(self):
        print("[MCP23017] disconnecting device")
        # Make sure all relays are off
        for setup in pins:
            if setup['output']:
                try:
                    # Check if relay is already off
                    status = self.read(setup['name'])
                    # If not, try to turn it off
                    if status == 1:
                        self.set_value(setup['name'], 0)
                        print("Relay {} off".format(setup['name']))
                except Exception as inst:
                    print("Failed to make sure pin {} is off".format(setup['name']))
                    print(type(inst))
                    print(inst.args)
                    print(inst)
        print("[MCP23017] disconnected")
