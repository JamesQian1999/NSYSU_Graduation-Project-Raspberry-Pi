import socket
import time
import picamera
import os

os.system("kill -9 `ps -fA | grep \"[0-9] python3 doc_client.py\" | sed \"s/pi\\ \\ *\\([0-9][0-9]*\\).*/\\1/g\" | tr '\\n' '\\ ' | sed \"s/" + str(os.getpid()) + "//g\"` 2> /dev/null")


# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.178', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.rotation = 180
        camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        #camera.wait_recording(60)
        #camera.stop_recording()
        while(True):
            camera.wait_recording(60)
except:
    #connection.close()
    client_socket.close()