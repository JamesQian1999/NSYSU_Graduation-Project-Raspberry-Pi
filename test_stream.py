import socket
import picamera
import time
import io
import sys
import struct

HOST = "192.168.0.179"
PORT = 9967
TEST = 0
buff= 2048
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST,PORT))
# server_socket.listen(1)
# print("(%s:%s) Listening..."%("192.168.0.111",PORT))
# connection, addr = server_socket.accept()

client_socket.connect((HOST,PORT))

rcv = client_socket.recv(buff)
print(rcv.decode())
rcv = client_socket.recv(buff)
print(rcv.decode())
client_socket.send(b'pi')

rcv = client_socket.recv(buff)
print(rcv.decode())
client_socket.send(b'Raspberry Pi 4')

rcv = client_socket.recv(buff)
print(rcv.decode())
client_socket.send(b'device')

#sys.exit(0)

connection = client_socket.makefile('wb')

with picamera.PiCamera() as camera:
#if True:
    camera.resolution = (640, 480)
    camera.rotation = 180
    print("\033[33mStarting Camera...\033[m")
    time.sleep(2)
    i = 0
    try:
        while True:
            i+=1
            stream = io.BytesIO()
            stream.flush()

            if TEST:
                fd = open("in.jpg","rb")
                stream.write(fd.read())

            camera.capture(stream, 'jpeg', use_video_port=True)
            size = stream.tell()
            #print("size: %f KB"%(size/1024))
            print("No.%d, size: %d bytes"%(i,size))
            #size = bytes(str(size),"utf-8")
            
            connection.write(struct.pack('!i', size))
            connection.flush()
            
            stream.seek(0)
            connection.write(stream.read())
                
            #break
            stream.seek(0)
            stream.truncate()
            sys.stdout.write("\033[F")
            time.sleep(1.3)
    except Exception as e:
        print(e)
        camera.close()

connection.close()
client_socket.close()
print("Finish streaming!")
