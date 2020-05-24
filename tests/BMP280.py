import unittest
import devices

class TestBMP280(unittest.TestCase):
    def test_device(self):
        print("Initializing BMP280...")
        bmp280 = devices.BMP280()

        print("Device ready, getting reading...")
        reading = bmp280.read()

        print("Got reading: ", reading)

        self.assertIsNotNone(reading['temperature'])
        self.assertIsNotNone(reading['pressure'])

if __name__ == '__main__':
    unittest.main()
