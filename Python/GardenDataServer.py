__author__ = 'Justin'

import serial
import subprocess
import MySQLdb
import time
import datetime
import logging

print "Waiting 15 seconds to start collecting..."
time.sleep(15)
db = MySQLdb.connect("localhost", "monitor", "password", "moisture")
curs = db.cursor()
ser = serial.Serial('/dev/ttyUSB0', 9600)
#logging.basicConfig(level=logging.DEBUG, filename='/error.log')

while True:
    try:
    	ser.write('\x01')
    	time.sleep(2)
    	moisture = ser.read(ser.inWaiting())
    	ser.write('\x02')
    	time.sleep(2)
    	state = ser.read(ser.inWaiting())
    	curs.execute("INSERT INTO moisture values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), "
    	             + state + ", " + moisture + ")")
    	db.commit()
    	print datetime.datetime.now(), "Moisture: ", moisture, "    State:", state
	time.sleep(60)
    except:
#	logging.exception("Oops:")
	command = "/usr/bin/sudo /sbin/restart"
	process = subprocess.Popen(command.split(), stdout.subprocess.PIPE)

