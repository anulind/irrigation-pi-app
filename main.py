import mqtt
import time
import schedule
import devices
from worker import Worker
import json
from utils import json_dumps
import queue

def main_loop():
    # Set up devices
    d = devices.init()

    # Connect to MQTT broker
    client = mqtt.connect()

    # Job queue
    work_queue = Worker(d, client)

    def read_sensors():
        work_queue.append("read_sensors")

    def handle_request(client, userdata, message):
        try:
            payload = json.loads(message.payload)
            work_queue.append("handle_request", payload)
            client.publish('pi/events', json_dumps({
                **payload,
                "status": "queued",
            }))
        except queue.Full:
            if payload:
                client.publish('pi/events', json_dumps({
                    **payload,
                    "status": "rejected",
                    "message": "Too many jobs in queue",
                }))
        except Exception as inst:
            print('Something wrong with incoming request, ignoring...')
            print(message)
            print(type(inst))
            print(inst.args)
            print(inst)

    def cancel_jobs(client, userdata, message):
        # No need to look at the message, just clean work queue and close everything...
        work_queue.cancel()

    # Handle incoming requests
    client.message_callback_add("pi/requests", handle_request)

    # Abort...
    client.message_callback_add("pi/abort", cancel_jobs)

    # Scheduled jobs
    schedule.every(15 * 60).seconds.do(read_sensors)

    # Process MQTT events on another thread
    client.loop_start()
    print("App ready")

    try:
        while True:
            # Add scheduled jobs to queue
            schedule.run_pending()
            # Pop queue
            work_queue.work()
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
        if client:
            print('Killing MQTT thread...')
            client.loop_stop()

if __name__ == '__main__':
    print("Starting irrigation system...")
    main_loop()
