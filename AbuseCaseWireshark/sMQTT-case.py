import paho.mqtt.client as mqtt
import time

def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    client.subscribe("esp/test")

def on_message(client, userdata, msg):
	msg = msg.payload
	print(msg.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("husnul", "husnul")
client.connect("35.237.236.241", 1883, 60)

client.loop_forever()