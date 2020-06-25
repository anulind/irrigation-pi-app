import devices
import unittest
import sys
import time

class TestMCP23017(unittest.TestCase):
    def test_device(self):
        print("Initializing MCP23017...")
        self.MCP23017 = devices.MCP23017()

        # Pin must be specified as command line argument
        args = sys.argv
        self.assertGreater(len(args), 2, "Please specify pin")

        pin = args[2]

        pin_number, pin_name = self.MCP23017.get_pin_info(pin)

        print("Device ready, testing pin {} ({})".format(pin_name, pin_number))

        output = self.MCP23017.pins_by_name[pin_name]['output']
        if output:
            self.MCP23017.set_value(pin_number, 1)
            time.sleep(5)
            self.MCP23017.set_value(pin_number, 0)
        else:
            status = self.MCP23017.read(pin_number)
            print("Result: {}".format(status))

        self.MCP23017.disconnect()

if __name__ == '__main__':
    unittest.main()
