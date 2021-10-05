import global_var
from verification import *
import bluetooth             # sudo apt-get install python3-bluez
import threading
from Crypto.PublicKey import RSA   # pip3 install -U PyCryptodome
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64
import time
import os


def connect(t = 0):
    #count = 1
    threads = []
    print("\033[33mRaspberry Pi is ready for listening bluetooth socket...\033[m")
    while (t==1) or (not global_var.verified):
        #print("client %d"%(count))
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))  # ps -fA | grep python
        server_sock.listen(1)

        port = server_sock.getsockname()[1]
        
        uuid = "00001101-0000-1000-8000-00805F9B34FB"

        bluetooth.advertise_service(server_sock, "IoT Server",
                                    service_id = uuid,
                                    service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                                    profiles = [ bluetooth.SERIAL_PORT_PROFILE ])

        print("Waiting for connection on RFCOMM channel %d" % port)
        client_sock, address = server_sock.accept()

        print("\n\033[34mAccepted connection from ", address, "\033[m")

        data = client_sock.recv(2048)
        print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")
            
        print("\n\033[32mSent:\033[m\t\tACK")
        client_sock.send("ACK")

        data = client_sock.recv(2048)
        print("\n\033[32mReceived:\t\033[m",data.decode(),"\t\033[m",  sep="")


        if data.decode() == "Owner":
            print("At owner")
            handle_client(client_sock, address)
            # t1 = threading.Thread(target=handle_client, args=(client_sock, address))
            # t1.start()
        else:
            print("At tenant")
            tenant_connect(client_sock, address)
        #threads.append()
        # threads[len(threads)-1].start()
        #count += 1



def tenant_connect(client_sock, address):

    rev_buff = 2048

    if(verify(client_sock)):
        data = client_sock.recv(rev_buff)
        print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

        i = os.popen("ifconfig | egrep -o 'inet [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ' | sed '1d;s/inet //g'")
        i = i.read()
        i = "rtsp://"+i[:-2]+":8555/unicast"
        print("\n\033[32mSent:\033[m\t\t",i)
        client_sock.send(i)

    print("\033[33mSocket close\033[m")
    client_sock.close()


def handle_client(client_sock, address):
    rev_buff = 2048

    if(verify(client_sock)):

        print("\033[33mVerification finish!\033[m")

        data = client_sock.recv(rev_buff)
        print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

        print("\n\033[32mSent:\033[m\t\tACK")
        client_sock.send("ACK")

        data = client_sock.recv(rev_buff)
        print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

        i = os.popen("ifconfig | egrep -o 'inet [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ' | sed '1d;s/inet //g'")
        i = i.read()
        i = "rtsp://"+i[:-2]+":8555/unicast"
        print("\n\033[32mSent:\033[m\t\t",i)
        client_sock.send(i)

       
    print("\033[33mSocket close\033[m")
    client_sock.close()


# for testing
if(__name__ == "__main__"):
    connect(1)
