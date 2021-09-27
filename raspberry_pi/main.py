import my_bluetooth as mb
import my_server as ms
import streaming
import global_var
import os
import time

# raspberry Pi bluetooth MAC: DC:A6:32:23:02:AF
if(__name__ == "__main__"):

    global_var.init()
    mb.connect()
    if global_var.verified:
        streaming.start() # v4l2rtspserver -W 640 -H 480 -F 15 -P 8554 /dev/video0
        ms.connect()
    
