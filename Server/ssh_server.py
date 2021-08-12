#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import paramiko
import threading
import sys
import cv2
import numpy as np
import struct
import time
host_key = paramiko.RSAKey(filename='/home/pi/.ssh/id_rsa')
MAC = dict()
MAC_buf = dict()
mutex = threading.Lock()

class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
        
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'username') and (password == 'userpassword'):
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED
    
server = "127.0.0.1"
ssh_port = 66

def apply_socket(server,ssh_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100000)
    return sock
def for_RaspberryPi_video(sock):
    global MAC
    global MAC_buf
    try:
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
        print(client, addr)
    except Exception:
        print('[-] Listen failed: ' + str(Exception))
        sys.exit(1)
    print('[+] Got a connection!')
        
        
    try:
        session = paramiko.Transport(client)
        session.add_server_key(host_key)
        server = Server()
        
        try:
            session.start_server(server=server)
        except Exception:
            print('[-] SSH negotiation failed.')
            
        chan = session.accept(20)
        print('[+] Authenticated!')
        print(chan)
        command = chan.recv(1024)
        chan.send('Welcome to ssh server!!!!')
        if command == b'register':
            register_device = chan.recv(1024)
            if register_device in MAC:
                chan.send('Device has registered')
            else:
                k = 0
                MAC[register_device] = list()
                MAC_buf[register_device] = list()
                chan.send('getvideo')
                while True:
                    # 接收 Header
                    fhead_size = struct.calcsize('l')
                    buf = chan.recv(fhead_size)
                    print(buf)
                    if buf ==b'complete':
                        break
                    if buf:
                        # 取出datasize
                        data_size = struct.unpack('l',buf)[0]
                    # 接收圖片串流長度
                    recvd_size = 0
                    data_total = b''
                    while not recvd_size == data_size:
                        if data_size -recvd_size >1024:
                            data = chan.recv(1024)
                            recvd_size += len(data)
                        else:
                            data = chan.recv(1024)
                            recvd_size = data_size 
                        data_total += data
                    
                    MAC[register_device].append(buf)
                    MAC[register_device].append(data_total)
                   
                    nparr = np.fromstring(data_total, np.uint8)
                    img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    cv2.imshow('result',img_decode)
                    cv2.waitKey(1)
                    time.sleep(0.1)
        
        session.close()
    except Exception as e: 
        print('[-] Caught exception: ' + str(e))
        try:
            session.close()
        except:
            pass
        sys.exit(1)

def for_phone_client(sock):
    global MAC
    global MAC_buf
    try:
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
        print(client, addr)
    except Exception:
        print('[-] Listen failed: ' + str(Exception))
        sys.exit(1)
    print('[+] Got a connection!')
        
        
    try:
        session = paramiko.Transport(client)
        session.add_server_key(host_key)
        server = Server()
        
        try:
            session.start_server(server=server)
        except Exception:
            print('[-] SSH negotiation failed.')
            
        chan = session.accept(20)
        print('[+] Authenticated!')
        print(chan)
        command = chan.recv(1024)
        if command == b'getvideo':
            chan.send('Welcome to ssh server!')
            RaspberryPiMAC = chan.recv(1024)
            if RaspberryPiMAC in MAC:
                chan.send('Device completed')
                for data in MAC[RaspberryPiMAC]:
                    chan.send(data)
                chan.send('complete')
            else:
                chan.send('Not find Device')
                session.close()
                return
        else:
            session.close()
            sys.exit(1)
    except Exception as e: 
        print('[-] Caught exception: ' + str(e))
        try:
            session.close()
        except:
            pass
        sys.exit(1)

sock = apply_socket(server,8877)
sock2 = apply_socket(server,7788)
# # 建立一個子執行緒
t = threading.Thread(target = for_RaspberryPi_video,args=[sock])
t1 = threading.Thread(target = for_phone_client,args=[sock2])
# # 執行該子執行緒
t.start()
t1.start()
# # 等待 t 這個子執行緒結束
t.join()
t1.join()
sock.close()
sock2.close()