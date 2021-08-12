import socket
#import picamera
import time
import io
import sys

HOST = '192.168.0.111'
PORT = 10010
buff= 2048
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen(0)
print("\nListening...")
connection, addr = server_socket.accept()

#with picamera.PiCamera() as camera:
if True:
    #camera.resolution = (640, 480)
    #camera.rotation = 180
    print("\033[33mStarting Camera...\033[m")
    time.sleep(2)
    
    try:
        while True:
            stream = io.BytesIO()
            stream.flush()
            fd = open("in.jpg","rb")
            stream.write(fd.read())
            #camera.capture(stream, 'jpeg', use_video_port=True)
            size = stream.tell()
            print("size: %f KB"%(size/1024))
            print("size: %d bytes"%(size))

            size = bytes(str(size),"utf-8")
            print("len(size) =",len(size))
            connection.send(size)
            stream.seek(0)
            count = 1
            while True:
                partition = stream.read(buff)
                print(count,". ",len(partition),sep="")
                connection.send(partition)
                count+=1
                if(len(partition) != buff):
                    break
                
            break

            stream.seek(0)
            stream.truncate()
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
    except:
        pass

connection.close()
print("Finish streaming!")

'''
stream.seek(0)
count = 0
fd = open("test.jpg", "wb+")
while True:
    test = stream.read(1024)
    #print(len(test))
    if(len(test) != 1024):
        print(count)
        fd.write(test)
        break
    fd.write(test)
    count += 1
    
'''

# fd = open("test.jpg", "wb+")

