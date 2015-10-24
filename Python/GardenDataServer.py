__author__ = 'Justin'

import serial
import MySQLdb
import time

db = MySQLdb.connect("localhost", "monitor", "password", "")
curs = db.cursor()
ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    curs.execute("""INSERT INTO moisture
                 values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 0, 0)""")
    time.sleep(60)
    