# -*- coding: utf-8 -*-

import logging
import time

#third party libs
from daemon import runner

import Queue
import os
import paho.mqtt.client as paho
import serial
from xbee import XBee
from struct import *

serial_port = serial.Serial("/dev/ttyUSB0", 9600)
xbee = XBee(serial_port)

mypid = os.getpid()
client = paho.Client()

commands=Queue.Queue(0)

def on_message(mosq, obj, msg):
    #called when we get an MQTT message that we subscribe to
    #Puts the command in the queue

    #if(args.verbosity>1):
    #    print("DISPATCHER: Message received on topic "+msg.topic+" with payload "+msg.payload)
    #    print msg.topic.split("/")[2]

    arduinoCommand=msg.topic.split("/")[2]+":"+msg.topic.split("/")[3]+":"+msg.payload
    commands.put(arduinoCommand)

def connectall():
    print("DISPATCHER: Connecting")
    client.connect("localhost",1883, 60)
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
        
class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/mqttconsumer.pid'
        self.pidfile_timeout = 5
        
    
    def run(self):
        
        while True:
            try:
                while client.loop()==0:
                    # Look for commands in the queue and execute them
                    if(not commands.empty()):
                        command=commands.get()
                        logger.debug("DISPATCHER: sending to Xbee: "+command)
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
                
app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/mqttconsumer/mqttconsumer.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
