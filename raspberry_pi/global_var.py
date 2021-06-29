import os


def init():
    global verified_sock
    global verified
    global password
    
    verified = 0
    password = "1129"

    # Let Raspberry Pi's Bluetooth scannable
    os.system("echo " + password + " | sudo hciconfig hci0 piscan")
