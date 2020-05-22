import unittest
import devices

class TestAM2320(unittest.TestCase):
    def test_device(self):
        print("Initializing AM2320...")
        am2303 = devices.AM2320()

        print("Device ready, getting reading...")
        reading = am2303.read()

        print("Got reading: ", reading)
        print("Test complete")

        self.assertIsNotNone(reading['temperature'])
        self.assertIsNotNone(reading['humidity'])

if __name__ == '__main__':
    unittest.main()
