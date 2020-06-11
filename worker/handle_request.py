from utils import json_dumps

event_topic = 'pi/events'

class Mixin:
    def handle_request(self, message):
        try:
            action = message.get('action')
            requestId = message.get('requestId')
            payload = message.get('payload')
            print("[handle request]: processing request id = {}, action = {}, payload = {}".format(requestId, action, payload))
            self.mqtt.publish(event_topic, json_dumps({
                **message,
                "status": "initiated",
            }))

            if action == "read":
                device_name = payload.get('device')
                if device_name:
                    device = getattr(self.devices, device_name)
                    device.read_and_publish(self.mqtt, pin=payload.get('pin'), origin=requestId)
                else:
                    # If device not specified, get new values for everything
                    self.read_sensors()

                self.mqtt.publish(event_topic, json_dumps({
                    **message,
                    "status": "completed",
                }))

            elif action == "set":
                device = getattr(self.devices, payload['device'])
                device.set_and_publish(
                    self.mqtt,
                    payload.get('pin'),
                    payload['target'],
                    origin=requestId,
                )
                self.mqtt.publish(event_topic, json_dumps({
                    **message,
                    "status": "completed",
                }))

            elif action == "run":
                device = getattr(self.devices, payload['device'])
                device.run_and_publish(
                    self.mqtt,
                    payload.get('pin'),
                    payload['duration'],
                    origin=requestId,
                )
                self.mqtt.publish(event_topic, json_dumps({
                    **message,
                    "status": "completed",
                }))

            else:
                print("[handle request]: Request {} not recognized".format(action))
                self.mqtt.publish(event_topic, json_dumps({
                    **message,
                    "status": "rejected",
                    "message": "Invalid payload",
                }))

        except Exception as e:
            print("[handle request]: unexpected error occured")
            print(type(e))
            print(e.args)
            print(e)
            self.mqtt.publish(event_topic, json_dumps({
                **message,
                "status": "failed",
                "message": str(e),
            }))

        print("[handle request]: job done")
