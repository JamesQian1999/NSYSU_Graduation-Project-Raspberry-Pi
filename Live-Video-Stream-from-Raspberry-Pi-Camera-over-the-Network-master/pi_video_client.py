import io
import socket
import struct
import time
from typing import Counter
import picamera
import sys
from PIL import Image
import cv2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.178", 10001))

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.rotation = 180
    print("starting Camera...........")
    stream = "test.jpg"
    f = open(stream, 'wb')
    count = 0
    cap = camera.capture_continuous(f, 'jpeg', use_video_port=True)
    f = open(stream, 'rb')
    l = f.read(1024)
    print(type(cap))
    for foo in cap:
        client_socket.send(l)

camera.close()


'''
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.178", 10001))

connection = client_socket.makefile('wb')
count = 1
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.rotation = 180
        print("starting Camera...........")
        time.sleep(2)
        stream = io.BytesIO()
        count = 0
        loop = time.time_ns()
        cap = camera.capture_continuous(stream, 'jpeg', use_video_port = True)
        print(type(cap))
        for foo in cap:
            print("\nloop\t", (time.time_ns()-loop)/10**9)

            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()

            a = time.time_ns()
            stream.seek(0)
            connection.write(stream.read())
            print("a\t", (time.time_ns()-a)/10**9)

            b = time.time_ns()
            stream.seek(0)
            stream.truncate()
            print("b\t", (time.time_ns()-b)/10**9)

            loop = time.time_ns()
except:
    # connection.close()
    client_socket.close()
'''
