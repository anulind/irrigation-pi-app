import os
from dotenv import load_dotenv

# Load values from .env-file
load_dotenv()

# MQTT connection
MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))

# Log config
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILENAME = 'pi.log'
