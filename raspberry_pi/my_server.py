import socket



def connect():
    print("My server")
    HOST = '192.168.0.101'
    PORT = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    print("\n\033[32mSent:\033[m\t\tpi")
    server.send(b"ACK")

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

    print("\n\033[32mSent:\033[m\t\tclose")
    server.send(b"close")

    while True:
        print("\n\033[33mWaiting for command...\033[m")

        data = server.recv(2048)
        print("\033[32mReceived:\t\033[m", data.decode(), sep="")
        
        print("\033[32mSent:\033[m\t\tACK")
        server.send(b"ACK")







if(__name__ == "__main__"):
    connect()