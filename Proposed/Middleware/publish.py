import time
import paho.mqtt.client as mqtt
import pyaes
import configparser
import hashlib
import time
import psutil
import getopt
import os

config = configparser.RawConfigParser()
config.read('config/config-publisher.txt')
username = config.get('credential','username')
password = config.get('credential','password')
topic = config.get('credential','topic')
server = config.get('host','server')
port = config.getint('host','port')
keepalive = config.getint('host','keep-alive')
secretkey = config.get('key','key')
qosval = config.getint('credential','qos')


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

client.username_pw_set(username, password)
client.connect(server, port, keepalive)

client.loop_start()
time.sleep(1)

key = secretkey
key = key.encode('utf-8')
counter = pyaes.Counter(initial_value=0)
aes = pyaes.AESModeOfOperationCTR(key,counter=counter)

def main():

    # if opt == '-h':
    #     print(".py -m -p")
    #     sys.exit()
    while True:
        print("Start publishing your message")
        pesan = input("message : ")
        client.on_log = on_log

        start = time.clock()

        encstart = time.clock()

        m = hashlib.sha512()
        m.update(pesan.encode('utf-8'))
        digest = m.hexdigest()
        #print("digest : ",digest)

        #joinvalue#
        join = digest+pesan
        #print("join    :",join)
        #join = enc+digest

        #createdigitalsignature
        digitalsignature = aes.encrypt(join)
        encend = time.clock()

        end = time.clock()


        #show send time to broker
        #showing ds value
        print("digital signature ",digitalsignature.hex())
        #end

        client.publish(topic,digitalsignature,qos=qosval)

        #memoryUSAGEtest
        cpu_process = psutil.Process()
        print("memory usage : ",cpu_process.memory_info()[0] / float(2 ** 20))
        memUSAGE = cpu_process.memory_percent()
        #print("memUSAGE : ",memUSAGE)
        f = open('ptob-memtest.txt','a')
        f.write(str(memUSAGE)+"\n")
        #memoryUSAGEtest

        f.close()
        end = time.clock()

        client.on_log = on_log

        #processing time
        #u can give # if u dont want to see this processing
        ptob = end-start
        ptobds = encend-encstart

        print("execute time (digital signature system) : ",ptob)
        print("enc time : ",ptobds)

        f = open('ptob.txt','w')
        f.write(str(ptob))
        f.close()

        f = open('ptob-ds.txt','w')
        f.write(str(ptobds))
        f.close()

        print("cpu usage percent : ",cpu_process.cpu_percent())



        time.sleep(1)
        print("")
        #end



    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()