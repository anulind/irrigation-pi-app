import unittest
import mqtt

class TestMQTT(unittest.TestCase):
    def test_connection(self):
        print('Connecting to MQTT...')
        client = mqtt.connect()
        print('Publishing messages...')
        client.publish('AM2320', '{"humidity":98.0,"temperature":13.1}')
        client.publish('BMP280', '{"pressure":101.2,"temperature":12.9}')
        client.publish('TSL2561', '{"light":10.0}')
        print('Messages published')
        client.loop()

if __name__ == '__main__':
    unittest.main()
