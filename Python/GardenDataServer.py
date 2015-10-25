__author__ = 'Justin'

import serial
import MySQLdb
import time

db = MySQLdb.connect("localhost", "monitor", "password", "moisture")
curs = db.cursor()
ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    ser.write('\x01')
    time.sleep(2)
    moisture = int(ser.read(ser.inWaiting()))
    ser.write('\x02')
    time.sleep(2)
    state = int(ser.read(ser.inWaiting()))
    curs.execute("""INSERT INTO moisture
                 values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), state, moisture)""")
    time.sleep(60)
