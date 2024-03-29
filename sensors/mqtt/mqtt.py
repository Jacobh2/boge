import json
import time
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
from settings import Settings


settings = Settings()

status = True


# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to swtich return topic
        client.subscribe(f"{settings.MQTT_TOPIC}/set")
    else:
        print("Failed to connect, return code %d\n", reason_code)


# Callback when the client receives a CONNACK response from the server.
def on_message(client, userdata, msg: MQTTMessage):
    global status

    print("Message Published...:", msg)
    if msg.topic == f"{settings.MQTT_TOPIC}/set":
        print("Switch!")
        print("Msg:", msg.state, msg.info, msg.payload)
        print("*"*100)

        # Fake work
        time.sleep(2)
        status = not status
        # Say that it is updated
        publish(client, status)


def publish(client, switch):
    message = json.dumps({
            "time": time.time(),
            "status": switch
        })
    return client.publish(f"{settings.MQTT_TOPIC}/state", message)


# Set up the MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(
    settings.MQTT_USER, settings.MQTT_PASSWORD.get_secret_value()
)  # Set authentication if needed
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)

# Start the network loop in a separate thread
client.loop_start()

try:
    # Send a message every 10 seconds
    while True:
        result = publish(client, status)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{status}` to topic `{settings.MQTT_TOPIC}`")
        else:
            print(f"Failed to send message to topic {settings.MQTT_TOPIC}")

        time.sleep(10)

except KeyboardInterrupt:
    print("Script interrupted by the user")

finally:
    client.loop_stop()
    client.disconnect()
