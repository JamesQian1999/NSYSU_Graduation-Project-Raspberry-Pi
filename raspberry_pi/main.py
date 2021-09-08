import my_bluetooth as mb
import streaming
import global_var

# raspberry Pi bluetooth MAC: DC:A6:32:23:02:AF
if(__name__ == "__main__"):
    global_var.init()
    mb.connect()
    #streaming.start() # v4l2rtspserver -W 640 -H 480 -F 15 -P 8554 /dev/video0
