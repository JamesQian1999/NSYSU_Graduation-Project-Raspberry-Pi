import global_var
import io
import socket
import struct
import time
import picamera
import sys


def start():
    server_ip = "192.168.0.178"
    server_port = 10001

    print("\n\033[33mConnecting to Server...\033[m")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(True):
        try:
            client_socket.connect((server_ip, server_port))
            print("\n\tConnected to %s:%d" % (server_ip, server_port))
            break
        except:
            continue
    print("\n\033[33mConnect Complete.\033[m")

    connection = client_socket.makefile('wb')
    connect(connection)
    client_socket.close()
    print("\033[33mstream end.\033[m")


def connect(connection):
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.rotation = 180
            print("\n\n\033[33mStarting Camera...\033[m")
            time.sleep(2)
            stream = io.BytesIO()
            count = 0
            loop = time.time_ns()
            cap = camera.capture_continuous(
                stream, 'jpeg', use_video_port=True)
            print("\n\n\033[33mCamera Ready.\033[m")
            # print(type(cap))
            print("\n\n\033[33mStart Streaming...\033[m")
            for foo in cap:
                print("\tLoop latency:\t",
                      (time.time_ns()-loop)/10**9, "s", sep="")
                print("\tData size:\t", stream.tell(), sep="")
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[F")

                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()

                stream.seek(0)
                connection.write(stream.read())

                stream.seek(0)
                stream.truncate()

                loop = time.time_ns()
    except:
        return
