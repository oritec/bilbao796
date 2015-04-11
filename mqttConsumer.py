import Queue
import os
import argparse
import paho.mqtt.client as paho
import serial
from xbee import XBee

parser = argparse.ArgumentParser()
parser.add_argument("-p","--port", default="/dev/ttyUSB0", help="The port where the ZigBee is attached")
parser.add_argument("-s","--server", default="127.0.0.1", help="The IP address of the MQTT server")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],  default=0,
                    help="increase output verbosity")
args = parser.parse_args()

serial_port = serial.Serial(args.port, 9600)
xbee = XBee(serial_port)

mypid = os.getpid()
client = paho.Client("consumerXbee_"+str(mypid))

commands=Queue.Queue(0)

def on_message(mosq, obj, msg):
    #called when we get an MQTT message that we subscribe to
    #Puts the command in the queue

    if(args.verbosity>1):
        print("DISPATCHER: Message received on topic "+msg.topic+" with payload "+msg.payload)

    arduinoCommand=msg.payload
    commands.put(arduinoCommand)

def connectall():
    print("DISPATCHER: Connecting")
    client.connect(args.server)
    client.subscribe("/lights/#", 0)
    client.on_message = on_message

def disconnectall():
    print("DISPATCHER: Disconnecting")
    arduino.close()
    client.unsubscribe("/lights/#")
    client.disconnect()

def reconnect():
    disconnectall()
    connectall()

connectall()

try:
    while client.loop()==0:
        # Look for commands in the queue and execute them
        if(not commands.empty()):
            command=commands.get()
            if(args.verbosity>0):
                print("DISPATCHER: sending to Xbee: "+command)
            # start=time.time()
            # #arduino.write(command+'|')
            # 
            # # wait until we get OK back
            # response=''
            # ack=False
            # while not ack:
            #     response=arduino.readline()
            #     if (len(response)>0):
            #         ack=True
            # 
            # end=time.time()
            # print('Response {} to {} took {:G} millis'.format(response,command,(end-start)*1000))

except KeyboardInterrupt:
    print "Interrupt received"
    disconnectall()