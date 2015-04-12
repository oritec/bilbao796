import serial
from xbee import XBee

import sys

#print sys.argv[1]

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(serial_port)

if sys.argv[1] == '0':
	print 'Se apaga la luz'
	xbee.remote_at(dest_addr='\x00\x02', command='D0',  parameter='\x04')
else:
	print 'Se prende la luz'
	xbee.remote_at(dest_addr='\x00\x02', command='D0',  parameter='\x05')
  
xbee.remote_at(dest_addr='\x00\x02', command='WR')
