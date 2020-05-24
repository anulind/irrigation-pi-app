import unittest
import devices

class TestTSL2561(unittest.TestCase):
    def test_device(self):
        print("Initializing TSL2561...")
        sensor = devices.TSL2561()

        print("Device ready, getting reading...")
        reading = sensor.read()

        print("Got reading: ", reading)

        self.assertIsNotNone(reading['light'])

if __name__ == '__main__':
    unittest.main()
