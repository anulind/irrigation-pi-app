import paho.mqtt.client as paho_client
from config import MQTT_HOST, MQTT_PORT

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def connect():
    client = paho_client.Client()
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    return client
