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
        print("Device ready, testing pin {}".format(pin))

        if pin in ['pump1', 'pump2', 'pump3', 'pump4']:
            self._pump(pin)
        elif pin == 'pow1':
            self._pow1()
        elif pin == 'watertank_empty':
            self._watertank()

        self.MCP23017.disconnect()

    def _pump(self, id):
        self.MCP23017.set_value(id, 1)
        time.sleep(5)
        self.MCP23017.set_value(id, 0)

    def _pow1(self):
        self.MCP23017.set_value('pow1', 1)
        time.sleep(5)
        self.MCP23017.set_value('pow1', 0)

    def _watertank(self):
        status = self.MCP23017.read('watertank_empty')
        print("Watertank empty: {}".format(status))

if __name__ == '__main__':
    unittest.main()
