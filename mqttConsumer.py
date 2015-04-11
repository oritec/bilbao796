# -*- coding: utf-8 -*-
import Queue
import os
import argparse
import paho.mqtt.client as paho
import serial
from xbee import XBee
from struct import *

parser = argparse.ArgumentParser()
parser.add_argument("-p","--port", default="/dev/ttyUSB0", help="The port where the ZigBee is attached")
parser.add_argument("-s","--server", default="localhost", help="The IP address of the MQTT server")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],  default=2,
                    help="increase output verbosity")
args = parser.parse_args()

serial_port = serial.Serial(args.port, 9600)
xbee = XBee(serial_port)

mypid = os.getpid()
client = paho.Client()

commands=Queue.Queue(0)

def on_message(mosq, obj, msg):
    #called when we get an MQTT message that we subscribe to
    #Puts the command in the queue

    if(args.verbosity>1):
        print("DISPATCHER: Message received on topic "+msg.topic+" with payload "+msg.payload)
        print msg.topic.split("/")[2]

    arduinoCommand=msg.topic.split("/")[2]+":"+msg.topic.split("/")[3]+":"+msg.payload
    commands.put(arduinoCommand)

def connectall():
    print("DISPATCHER: Connecting")
    client.connect(args.server,1883, 60)
    client.subscribe("/lights/#", 0)
    client.on_message = on_message

def disconnectall():
    print("DISPATCHER: Disconnecting")
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
            address=pack('>h',int(command.split(":")[0]))
            port='D'+command.split(":")[1]
            sent=command.split(":")[2]
            if sent == '1':
                 msg= pack('>b',4)
            elif sent == '0':
                msg= pack('>b',5)
            
            xbee.remote_at(dest_addr=address, command=port,  parameter=msg)
            

except KeyboardInterrupt:
    print "Interrupt received"
    disconnectall()
