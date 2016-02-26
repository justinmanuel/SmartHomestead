import serial
import MySQLdb
import time
import datetime
import threading
import SimpleHTTPServer
import SocketServer
import logging
import cgi
import httplib, urllib


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
    server = "data.sparkfun.com" # base URL of your feed
    publicKey = "G2qxLpKZxGtwgdJXqz64" # public key, everyone can see this
    privateKey = "NW4rxmvwrlhderowPnb7"  # private key, only you should know
    fields = ["date", "time", "state", "moisture"] # Your feed's data fields
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
            data = {}
            data[fields[0]] = time.strftime("%Y-%m-%d")
            data[fields[1]] = time.strftime("%H:%M:%S")
            data[fields[2]] = state
            data[fields[3]] = moisture
            params = urllib.urlencode(data)

            # Now we need to set up our headers:
            headers = {} # start with an empty set
            # These are static, should be there every time:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["Connection"] = "close"
            headers["Content-Length"] = len(params) # length of data
            headers["Phant-Private-Key"] = privateKey # private key header

            # Now we initiate a connection, and post the data
            c = httplib.HTTPConnection(server)
            # Here's the magic, our reqeust format is POST, we want
            # to send the data to data.sparkfun.com/input/PUBLIC_KEY.txt
            # and include both our data (params) and headers
            c.request("POST", "/input/" + publicKey + ".txt", params, headers)
            r = c.getresponse() # Get the server's response and print it
            time.sleep(56)
        except Exception as e:
            print "There was an exception..."
            print e


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
