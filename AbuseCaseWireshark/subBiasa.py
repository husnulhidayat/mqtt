import paho.mqtt.client as mqtt
import time
import psutil

def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    client.subscribe("esp/test")

def on_message(client, userdata, msg):
    start = time.time()
    msg = msg.payload
    print(msg.decode())
    end = time.time()

    #processing time
    btos = end-start
    f = open('ptob1.txt').readline()
    timeexec = btos+float(f)
    print("execute time publisher-broker-subscriber (for local testing) : ",timeexec)
    f = open('exec30.txt', 'a')
    f.write(str(timeexec)+"\n")

    cpu_process = psutil.Process()
    print("cpu usage percent : ",cpu_process.cpu_times())
    print("memory usage : ",cpu_process.memory_info()[0] / float(2 ** 20)," MiB")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("husnul", "husnul")
client.connect("35.237.236.241", 1883, 60)

client.loop_forever()