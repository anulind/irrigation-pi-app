import unittest
import devices

class TestHCSR04(unittest.TestCase):
    def test_device(self):
        print("Initializing HCSR04...")
        sensor = devices.HCSR04()

        print("Device ready, getting reading...")
        reading = sensor.read()

        print("Got reading: ", reading)

        sensor.cleanup()

        self.assertIsNotNone(reading['range'])

if __name__ == '__main__':
    unittest.main()
