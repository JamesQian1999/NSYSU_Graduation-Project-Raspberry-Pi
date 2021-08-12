#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import paramiko
import subprocess
import cv2
import numpy as np
import struct
import time

def ssh_command(ip, user, passwd, command,port = 80):
    if command!='getvideo':
        return
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
    client.connect(ip, port,username=user, password=passwd)  
    ssh_session = client.get_transport().open_session() 
    if ssh_session.active:
        ssh_session.send(command)  
        print(ssh_session.recv(1024))
        ssh_session.send('RaspberryPiMAC')
        find_device = ssh_session.recv(16)
        print(find_device)
        if find_device == b'Device completed':
            while True:
                # 接收 Header
                fhead_size = struct.calcsize('l')
                buf = ssh_session.recv(fhead_size)
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
                        data = ssh_session.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = ssh_session.recv(1024)
                        recvd_size = data_size
                    data_total = ssh_session.recv(data_size)
        
                #將接收到的圖片顯示
                # print(data_total)
                nparr = np.fromstring(data_total, np.uint8)
                img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow('result',img_decode)
                cv2.waitKey(1)
                time.sleep(0.1)

        client.close()

ssh_command('127.0.0.1', 'username', 'userpassword', 'getvideo',778)
