import serial
import subprocess
import MySQLdb
import time
import datetime
import threading
import SimpleHTTPServer
import SocketServer
import logging
import cgi


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self       .rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        command = form.getvalue("command")
        data = form.getvalue("data")
        if command == "override":
                if data == "on":
                        print "Turning water on"
                        ser.write('\x03')
                        time.sleep(2)
                elif data == "off":
                        print "Turning water off"
                        ser.write('\x04')
                        time.sleep(2)
        elif command == "report":
                day = int(data)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def collect_data():
    running_count = 0
    while True:
        try:
            ser.write('\x01')
            time.sleep(2)
            moisture = ser.read(ser.inWaiting())
            check_moisture(moisture)
            ser.write('\x02')
            time.sleep(2)
            state = ser.read(ser.inWaiting())
            running_count = end_cycle(state, running_count)
            curs.execute("INSERT INTO moisture values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), "
                         + state + ", " + moisture + ")")
            db.commit()
            print datetime.datetime.now(), "Moisture: ", moisture, "    State:", state
            time.sleep(56)
        except Exception:
            print "There was an exception..."


def check_moisture(moisture):
    now = datetime.datetime.now()
    if now.hour == 7 and now.minute == 30 and int(moisture) < 320:
        ser.write('\x03')


def end_cycle(state, running_count):
    if state == '1':
        running_count += 1
        print "Running for %d cycles..." % running_count
        if running_count > 15:
            ser.write('\x04')  # end cycle
            print "Ending cycle..."
            return 0
        else:
            return running_count
    else:
        return 0


print "Waiting 15 seconds to start collecting..."
time.sleep(15)

db = MySQLdb.connect("localhost", "monitor", "password", "moisture")
curs = db.cursor()
ser = serial.Serial('/dev/ttyUSB0', 9600)
read_thread = threading.Thread(name='ReadThread', target=collect_data)
read_thread.start()
Handler = ServerHandler

httpd = SocketServer.TCPServer(("", 8001), Handler)
httpd.serve_forever()
