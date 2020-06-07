import mqtt
import time
import schedule
import devices
from worker import Worker
import json

def main_loop():
    # Set up devices
    d = devices.init()

    # Connect to MQTT broker
    client = mqtt.connect()

    # Job queue
    queue = Worker(d, client)

    def periodic_reading():
        queue.append("periodic_reading")

    def handle_request(client, userdata, message):
        try:
            payload = json.loads(message.payload)
            queue.append("handle_request", payload)
        except Exception as inst:
            print('Something wrong with incoming request, ignoring...')
            print(message)
            print(type(inst))
            print(inst.args)
            print(inst)

    # Handle incoming requests
    client.message_callback_add("pi/requests", handle_request)

    # Scheduled jobs
    schedule.every(15 * 60).seconds.do(periodic_reading)

    print("App ready")

    try:
        while True:
            # Process MQTT events
            client.loop()
            # Add scheduled jobs to queue
            schedule.run_pending()
            # Pop queue
            queue.work()
            time.sleep(1)

    except KeyboardInterrupt:
        print('Process ended by user.')

    except Exception as inst:
        print('Unexpected error!')
        print(type(inst))
        print(inst.args)
        print(inst)

    finally:
        if d:
            print('Shutting down gracefully...')
            d.disconnect()
            print('Cleanup complete')

if __name__ == '__main__':
    print("Starting irrigation system...")
    main_loop()
