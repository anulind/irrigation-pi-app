import board
import busio
import adafruit_mcp230xx
import time

pins = {
    'pow1':            {'pin': 9, 'output': True},
    'pump1':           {'pin': 9,  'output': True},
    'pump2':           {'pin': 11, 'output': True},
    'pump3':           {'pin': 13, 'output': True},
    'pump4':           {'pin': 15, 'output': True},
    'watertank_empty': {'pin': 7,  'output': False},
}

class MCP23017:
    def __init__(self):
        print("[MCP23017] Initializing sensor...")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_mcp230xx.MCP23017(i2c)
        for _, setup in pins.items():
            pin = self.sensor.get_pin(setup['pin'])
            # Set pin as output
            if setup['output']:
                pin.switch_to_output(value=False)
        print("[MCP23017] configuration complete")

    def input(self, id):
        print("[MCP23017] reading pin {}".format(id))
        pin = self.sensor.get_pin(pins[id]['pin'])
        value = pin.value
        print("[MCP23017] pin {} = {}".format(id, value))
        return value

    def output(self, id, target):
        print("[MCP23017] setting pin {} to {}".format(id, target))
        pin = self.sensor.get_pin(pins[id]['pin'])
        pin.value = target
        print("[MCP23017] target set")

    def run_pump(self, id, payload):
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

        # Validate pump id
        pumps = ['pump1', 'pump2', 'pump3', 'pump4']
        if id not in pumps:
            raise ValueError("Invalid pump id (given: {})".format(id))

        # Run pump
        # Turn relay on
        self.output(id, 1)
        # Wait for `duration` seconds
        print("[MCP23017] pump turned on, sleeping for {} seconds".format(duration))
        time.sleep(duration)
        # Check if pump is on
        status = self.input(id)
        if status == 0:
            raise Exception("Failed to run pump - could not turn on relay or job cancelled")
        # Turn relay off
        self.output(id, 0)
        print("[MCP23017] job complete")

    def disconnect(self):
        print("[MCP23017] disconnecting device")
        # Make sure all relays are off
        for id, setup in pins.items():
            if setup['output']:
                try:
                    # Check if relay is already off
                    status = self.input(id)
                    print("Relay {} status: {}".format(id, status))
                    # If not, try to turn it off
                    if status == 1:
                        self.output(id, 0)
                        print("Relay {} off".format(id))
                except Exception as inst:
                    print("Failed to make sure pin {} is off".format(id))
                    print(type(inst))
                    print(inst.args)
                    print(inst)
        print("[MCP23017] disconnected")
