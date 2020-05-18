import os
from dotenv import load_dotenv

# Load values from .env-file
load_dotenv()

# MQTT connection
MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
