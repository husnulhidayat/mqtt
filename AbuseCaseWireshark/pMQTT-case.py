import paho.mqtt.client as mqtt
import time
import psutil,os

def on_connect( client, userdata, flags, rc):
    print ("Connected with Code : " +str(rc))
    #client.subscribe(topic)

def on_message( client, userdata, msg):
    print(str(msg.payload))

def on_log(client, userdata, level, buf):
    print("log: ",buf)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("husnul", "husnul")
client.connect("35.237.236.241", 1883, 60)

client.loop_start()
time.sleep(1)

start = time.clock()

pesann = "Hello".encode('utf-8')
client.on_log = on_log
client.publish("Test",pesann)

end = time.clock()

cpu_process = psutil.Process(os.getpid())
print("cpu usage percent : ", cpu_process.cpu_percent())
print("memory usage : ", cpu_process.memory_info()[0] / float(2 ** 20), " MiB",cpu_process.memory_percent(), "%")

ptob = end - start
print("execute publish time : ", ptob)

client.loop_stop()
client.disconnect()
