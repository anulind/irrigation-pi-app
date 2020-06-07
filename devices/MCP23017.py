import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017 as adafruit_MCP23017
import time

pins = [
    {'pin': 9,  'name': 'pow1',            'output': True},
    {'pin': 9,  'name': 'pump1',           'output': True},
    {'pin': 11, 'name': 'pump2',           'output': True},
    {'pin': 13, 'name': 'pump3',           'output': True},
    {'pin': 15, 'name': 'pump4',           'output': True},
    {'pin': 7,  'name': 'watertank_empty', 'output': False},
]

class MCP23017:
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

    # Get pin by human readable id or pin number
    def get_pin(self, id):
        if isinstance(id, str):
            return self.sensor.get_pin(self.pins_by_name[id]['pin'])
        return self.sensor.get_pin(id)

    def read(self, id):
        print("[MCP23017] reading pin {}".format(id))
        pin = self.get_pin(id)
        value = pin.value
        print("[MCP23017] pin {} = {}".format(id, value))
        return value

    def set_value(self, id, target):
        print("[MCP23017] setting pin {} to {}".format(id, target))
        pin = self.get_pin(id)
        pin.value = target
        print("[MCP23017] target set")

    def run(self, id, payload):
        print("[MCP23017] running pump {} with payload {}".format(id, payload))

        # Validate duration
        max_duration = 30
        duration = payload.get('duration', None)
        if not isinstance(duration, int):
            raise ValueError("Duration must be integer (given: {})".format(duration))
        if duration > max_duration:
            raise ValueError("Duration can be at most {}".format(max_duration))
        if duration < 1:
            raise ValueError("Duration must be at least 1")

        # Turn relay on
        self.set_value(id, 1)
        # Wait for `duration` seconds
        print("[MCP23017] pump {} turned on, sleeping for {} seconds".format(id, duration))
        time.sleep(duration)
        # Check if pump is on
        status = self.read(id)
        if status == 0:
            raise Exception("Failed to run pump - could not turn on relay or job cancelled")
        # Turn relay off
        self.set_value(id, 0)
        print("[MCP23017] job complete")

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
