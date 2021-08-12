import bluetooth             # sudo apt-get install python3-bluez
import os


def connect():
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
    data = client_sock.recv(1024)
    client_sock.send("ACK")

    handle_client(client_sock, address)


def handle_client(client_sock, address):
    rev_buff = 2048


    print("\n\033[34mAccepted connection from ", address, "\033[m")

    data = client_sock.recv(rev_buff)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")
    data = client_sock.recv(rev_buff)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

    print("\n\033[32mSent:\033[m\t\tACK")
    client_sock.send("hey")

    client_sock.close()


# for testing
if(__name__ == "__main__"):
    os.system("clear")
    # Let Raspberry Pi's Bluetooth scannable
    os.system("clear ; echo " + "1129" + " | sudo hciconfig hci0 piscan")

    # Kill unrelease process
    os.system("kill -9 `ps -fA | grep \"[0-9] python3 main.py\" | sed \"s/pi\\ \\ *\\([0-9][0-9]*\\).*/\\1/g\" | tr '\\n' '\\ ' | sed \"s/" + str(os.getpid()) + "//g\"` 2> /dev/null")

    connect()
