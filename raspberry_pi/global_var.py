import os
from Crypto.PublicKey import RSA  # pip3 install -U PyCryptodome
from Crypto import Random


def init():
    global verified_sock
    global verified
    global password

    verified = 0
    password = "1129"

    # Let Raspberry Pi's Bluetooth scannable
    os.system("clear ; echo " + password + " | sudo hciconfig hci0 piscan")

    # Kill unrelease process
    os.system("kill -9 `ps -fA | grep \"[0-9] python3 main.py\" | sed \"s/pi\\ \\ *\\([0-9][0-9]*\\).*/\\1/g\" | tr '\\n' '\\ ' | sed \"s/" + str(os.getpid()) + "//g\"` 2> /dev/null")

    # Creat 1024bits RSA Key
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)

    # RSA Private Key
    privateKey = key.export_key()
    with open("private.pem", "wb") as f:
        f.write(privateKey)

    # RSA Public Key
    publicKey = key.publickey().export_key()
    with open("public.pem", "wb") as f:
        f.write(publicKey)
