import io
import os
import picamera
import logging
import socketserver
from http import server
import bluetooth
import cv2



PAGE="""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

'''
PAGE2 = """\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><h2>Ehter password and click the link below</h2><a href="http://192.168.0.142:8001">Access the camara</a></center>
</body>
</html>
"""
'''


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        #self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            self.buffer.truncate()
            self.frame = self.buffer.getvalue()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header(
                'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while not (cv2.waitKey(1) & 0xFF == ord('q')):
                    frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
            except KeyboardInterrupt:
                global server
                server.server_close()
                exit()
        else:
            self.send_error(404)
            self.end_headers()


class Test(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE2.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)


# raspberry Pi bluetooth MAC: DC:A6:32:23:02:AF
'''
target_name = "J"
target_address = None
fin = 1
while(fin):
    print("\nFinding...")
    nearby_devices = bluetooth.discover_devices()
    if(len(nearby_devices) == 0):
        print("\tNo found.")
    for bdaddr in nearby_devices:
        tmp = bluetooth.lookup_name(bdaddr)
        print("\tName:", tmp)
        print("\tAddr:", bdaddr)
        if target_name == tmp:
            target_address = bdaddr
            fin = 0
            break

print("\n===============Found===============")
print("Name:", target_name)
print("Addr:", target_address)
'''
'''
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

print("listening...")
client_sock, address = server_sock.accept()
print("Accepted connection from ", address)

data = client_sock.recv(1024)
print("\treceived:",data)
client_sock.send("ACK")
print("\tSent: ACK")

data = client_sock.recv(1024)
print("\treceived:",data)
client_sock.send("ACK2")
print("\tSent: ACK2")

client_sock.close()
server_sock.close()
'''


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    print("Hello")
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    camera.rotation = 180
    address = ('', 8001)
    camera.start_recording(output, format='mjpeg')
    try:
        print("Server is ready ...")
        server = socketserver.TCPServer(address, StreamingHandler)
        while 1:
            server.handle_request()
    finally:
        camera.stop_recording()

        
# ./ngrok http 8001

# amixer cset numid=3 1         //set audio output
# amixer scontrols              
# amixer sset 'Master' 100%     //set volume to 100%

