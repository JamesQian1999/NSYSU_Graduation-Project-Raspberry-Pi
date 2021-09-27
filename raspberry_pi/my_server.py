import socket



def connect():
    HOST = '172.20.10.5'
    PORT = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    data = server.recv(2048)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

    data = server.recv(2048)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

    print("\n\033[32mSent:\033[m\t\tpi")
    server.send(b"pi")

    data = server.recv(2048)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

    print("\n\033[32mSent:\033[m\t\tcommand")
    server.send(b"command")

    data = server.recv(2048)
    print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")

    print("\n\033[32mSent:\033[m\t\topen")
    server.send(b"close")

    while True:
        data = server.recv(2048)
        print("\n\033[32mReceived:\t\033[m", data.decode(), sep="")







if(__name__ == "__main__"):
    connect()