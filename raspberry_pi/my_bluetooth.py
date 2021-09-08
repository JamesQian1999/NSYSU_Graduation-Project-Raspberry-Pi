import global_var
from verification import *
import bluetooth             # sudo apt-get install python3-bluez
import threading
from Crypto.PublicKey import RSA   # pip3 install -U PyCryptodome
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64
import time


def connect():
    #count = 1
    threads = []
    print("\033[33mRaspberry Pi is ready for listening bluetooth socket...\033[m")
    while(global_var.verified == 0):
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

        handle_client(client_sock, address)
        #threads.append(threading.Thread(target=handle_client, args=(client_sock, address)))
        # threads[len(threads)-1].start()
        #count += 1


def handle_client(client_sock, address):
    rev_buff = 2048


    print("\n\033[34mAccepted connection from ", address, "\033[m")

    data = client_sock.recv(rev_buff)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")
        
    print("\n\033[32mSent:\033[m\t\tACK")
    client_sock.send("ACK")

    data = client_sock.recv(rev_buff)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

    if(verify(client_sock)):

        print("")

        # print("\n\033[32mReceived Phone Public Key:\033[m")
        # print(data.decode('utf-8'))

        # Save phone public key
        # phone_public = "phone"+str(threading.get_ident())+"_public.pem"
        # fd = open(phone_public, "wb")
        # fd.write(data)

        # Read Private Key
        # encodedKey = open("private.pem", "rb")
        # pre_key = RSA.import_key(encodedKey.read())

        # print("\n\033[32mSent Raspberry Pi Public Key:\033[m")
        # print(pre_key.publickey().export_key().decode('utf-8'))
        # client_sock.send(pre_key.publickey().export_key())

        # Receive msg with RSA
        # data = client_sock.recv(rev_buff)
        # print("\n\033[32mReceived Data:\033[m")
        # print("Before decrypt:", data.decode('utf-8'))
        # cipher = PKCS1_cipher.new(pre_key)
        # back_text = cipher.decrypt(base64.b64decode(data), 0)
        # print("After decrypt:", back_text.decode('utf-8'))

        # Sent msg with RSA
        # msg = "This is secret too!"
        # fd = open(phone_public)
        # phone_key = fd.read()
        # phone_key = RSA.importKey(str(phone_key))
        # cipher = PKCS1_cipher.new(phone_key)
        # rsa_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
        # print("\n\033[32mSent Data:\033[m")
        # print("Before encrypt: ", msg)
        # print("After encrypt: ", rsa_text.decode('utf-8'))
        # client_sock.send(rsa_text)

    print("\033[33mSocket close\033[m")
    client_sock.close()


# for testing
if(__name__ == "__main__"):
    print("hello")
