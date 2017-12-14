import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("hermes/intent/resumeMusic")

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

def on_log(client, userdata, level, buf):
    print("log: ", buf)

client = mqtt.Client("command-handler")
client.on_message = on_message
client.on_log = on_log 
client.on_connect = on_connect

client.connect("localhost", 9898)
client.loop_forever()
