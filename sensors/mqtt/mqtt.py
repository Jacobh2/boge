import time
import paho.mqtt.client as mqtt
from settings import Settings


settings = Settings()


# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


# Callback when the client receives a CONNACK response from the server.
def on_publish(client, userdata, mid):
    print("Message Published...")


# Set up the MQTT client
client = mqtt.Client(settings.MQTT_CLIENT_ID)
client.username_pw_set(
    settings.MQTT_USER, settings.MQTT_PASSWORD
)  # Set authentication if needed
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)

# Start the network loop in a separate thread
client.loop_start()

try:
    # Send a message every 10 seconds
    while True:
        message = "Hello MQTT!"  # Replace with your message
        result = client.publish(settings.MQTT_TOPIC, message)

        print("Result:", result)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{settings.MQTT_TOPIC}`")
        else:
            print(f"Failed to send message to topic {settings.MQTT_TOPIC}")

        time.sleep(10)

except KeyboardInterrupt:
    print("Script interrupted by the user")

finally:
    client.loop_stop()
    client.disconnect()