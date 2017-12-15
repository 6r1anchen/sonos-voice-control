import paho.mqtt.client as mqtt
import json
import soco

# soco
def get_soco_devices():
    return soco.discover()

def stop_device(device):
    print("device: {0}, status: {1}".format(device.player_name, device.get_current_transport_info()['current_transport_state']))
    result = device.group.coordinator.pause()
    print("device: {0}, stop command: {1}".format(device.player_name, result))

def play_device(device):
    print("device: {0}, status: {1}".format(device.player_name, device.get_current_transport_info()['current_transport_state']))
    result = device.group.coordinator.play()
    print("device: {0}, play command: {1}".format(device.player_name, result))

# MQTT

assistant_id = "user_nGGBl4zY2BV__"
intent_prefix = "hermes/intent/" + assistant_id

topics = [
    (intent_prefix + "addSong", 2),
    (intent_prefix + "getInfos", 2),
    (intent_prefix + "nextSong", 2),
    (intent_prefix + "playAlbum", 2),
    (intent_prefix + "playArtist", 2),
    (intent_prefix + "playPlaylist", 2),
    (intent_prefix + "playPlaylist", 2),
    (intent_prefix + "playSong", 2),
    (intent_prefix + "previousSong", 2),
    (intent_prefix + "radioOn", 2),
    (intent_prefix + "resumeMusic", 2),
    (intent_prefix + "speakerInterrupt", 2),
    (intent_prefix + "volumeDown", 2),
    (intent_prefix + "volumeUp", 2),
]

def on_play_music(client, userdata, message):
    print("on_play_music: ", str(message.payload.decode("utf-8")))
    msg = json.loads(str(message.payload.decode("utf-8")))
    input = msg["input"]
    if "play" in input or "queue" in input:
        for zone in get_soco_devices():
            play_device(zone)

def on_stop_music(client, userdata, message):
    print("on_stop_music: ", str(message.payload.decode("utf-8")))
    msg = json.loads(str(message.payload.decode("utf-8")))
    if "stop" in msg["input"]:
        for zone in get_soco_devices():
            stop_device(zone)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topics)

    client.message_callback_add(intent_prefix + "resumeMusic", on_play_music)
    client.message_callback_add(intent_prefix + "playSong", on_play_music)
    client.message_callback_add(intent_prefix + "speakerInterrupt", on_stop_music)

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
