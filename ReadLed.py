import serial
from xbee import XBee

import sys

#print sys.argv[1]

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(serial_port)


xbee.remote_at(frame_id='A', dest_addr='\x00\x02', command='D0', parameter=None) 
#xbee.remote_at(dest_addr='\x00\x02', command='WR')
packet = xbee.wait_read_frame()
#print packet


if packet['id'] == 'remote_at_response':
	if packet['parameter'] == '\x04':
		print 'LED esta apagado'
	elif packet['parameter']=='\x05':
		print 'LED esta prendido'
