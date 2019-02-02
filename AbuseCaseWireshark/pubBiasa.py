import time
import paho.mqtt.client as mqtt
import pyaes
import configparser
import hashlib
import time
import psutil
import getopt
import sys


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

def main():

    while True:
        print("Start publishing your message")
        pesan = input("message : ")
        client.on_log = on_log

        start = time.clock()

        client.publish("esp/test",pesan,qos=2)
        end = time.clock()

        client.on_log = on_log

        #processing time
        #u can give # if u dont want to see this processing
        ptob = end-start
        print("execute time (digital signature system) : ",ptob)

        f = open('ptob1.txt','w')
        f.write(str(ptob))
        f.close()

        cpu_process = psutil.Process()
        print("cpu usage percent : ",cpu_process.cpu_percent())
        print("memory usage : ",cpu_process.memory_info()[0] / float(2 ** 20)," MiB",cpu_process.memory_percent(), "%")

        time.sleep(1)
        print("")
        #end



    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()