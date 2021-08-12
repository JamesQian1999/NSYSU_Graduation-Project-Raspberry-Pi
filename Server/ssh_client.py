#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import paramiko
import subprocess
import cv2
import numpy as np
import struct
import time
cap = cv2.VideoCapture(-1, cv2.CAP_V4L)

def ssh_command(ip, user, passwd, command,port = 80):
    if command=='register':
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
        client.connect(ip, port,username=user, password=passwd)  
        ssh_session = client.get_transport().open_session() 
        if ssh_session.active:
            ssh_session.send(command) 
            print(ssh_session.recv(1024))
            ssh_session.send('RaspberryPiMAC') 
            command = ssh_session.recv(1024)
            if command==b'getvideo':
                ret, frame = cap.read()
                while ret:
                    img_encode = cv2.imencode('.jpg', frame)[1]
                    data_encode = np.array(img_encode)
                    data = data_encode.tostring()
                    
                    fhead = struct.pack('l',len(data))
                    print(fhead,len(data))
                    ssh_session.send(fhead)
                    for i in range(len(data)//1024+1):
                        if 1024*(i+1)>len(data):
                            ssh_session.send(data[1024*i:])
                        else:
                            ssh_session.send(data[1024*i:1024*(i+1)])
                    ret, frame = cap.read()
                    time.sleep(0.1)
                ssh_session.send('complete') 
            client.close()
            print("Transfer complete!!")
            
ssh_command('192.168.0.179', 'username', 'userpassword', 'register',8877)