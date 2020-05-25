import unittest
import devices

class TestMCP3008(unittest.TestCase):
    def test_device(self):
        print("Initializing MCP3008...")
        mcp23017 = devices.MCP23017()
        device = devices.MCP3008(mcp23017)

        print("Device ready, getting reading...")
        reading = device.read('temperature')

        print("Got reading: ", reading)

        self.assertIsNotNone(reading['temperature'])

if __name__ == '__main__':
    unittest.main()
