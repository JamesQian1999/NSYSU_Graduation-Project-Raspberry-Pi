import global_var
import bluetooth
import threading

def connect():
    port = 1
    threads = []
    print("Ready for listening...")
    while(global_var.verified == 0):
        print("client %d"%(port))
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", port))
        server_sock.listen(1)
        client_sock, address = server_sock.accept()
        threads.append(threading.Thread(target = handle_client, args = (client_sock, address)))
        threads[len(threads)-1].start()
        port += 1

    

def handle_client(client_sock, address):
    print("Here is client")
    print("Accepted connection from ", address)

    data = client_sock.recv(1024)
    print("\treceived:",data)
    client_sock.send("ACK")
    print("\tSent: ACK")

    data = client_sock.recv(1024)
    print("\treceived:",data)
    client_sock.send("ACK2")
    print("\tSent: ACK2")

    client_sock.close()
    exit

# for testing
if(__name__ == "__main__"):
    print("hello")
