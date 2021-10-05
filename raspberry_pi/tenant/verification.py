import global_var
import RPi.GPIO as GPIO
import time
from Crypto.PublicKey import RSA   # pip3 install -U PyCryptodome
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64

pin = 15
code = 0

def setup():
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def binary_aquire(pin, duration):
    # aquired data as quickly as possible
    t0 = time.time()
    results = []
    while (time.time() - t0) < duration:
        results.append(GPIO.input(pin))
    return results


def on_ir_receive(pinNo, bouncetime=150):
    # when edge detect is called (which requires less CPU than constant
    # data acquisition), we acquire data as quickly as possible
    data = binary_aquire(pinNo, bouncetime/1000.0) # pin = 13, duration = 0.15s
    if len(data) < bouncetime:
        return
    rate = len(data) / (bouncetime / 1000.0) # data per second
    pulses = []
    i_break = 0
    # detect run lengths using the acquisition rate to turn the times in to microseconds
    for i in range(1, len(data)):
        if (data[i] != data[i-1]) or (i == len(data)-1):
            pulses.append((data[i-1], int((i-i_break)/rate*1e6))) # (i-i_break)/rate*1e6) duration in microseconds
            i_break = i
    # decode ( < 1 ms "1" pulse is a 1, > 1 ms "1" pulse is a 1, longer than 2 ms pulse is something else)
    # does not decode channel, which may be a piece of the information after the long 1 pulse in the middle
    outbin = ""
    for val, us in pulses:
        if val != 1:
            continue
        if outbin and us > 2000:
            break
        elif us < 1000:
            outbin += "0"
        elif 1000 < us < 2000:
            outbin += "1"
    try:
        print("Bin:",outbin)
        return int(outbin, 2)
    except ValueError:
        # probably an empty code
        return None


def destroy():
    GPIO.cleanup()



def verify(client_sock):
    # verified

    # Read Private Key
    encodedKey = open("private.pem", "rb")
    pi_key = RSA.import_key(encodedKey.read())

    pi_key = pi_key.publickey().export_key()
    pi_key = pi_key[27:-25]
    first_pi = pi_key[:5]
    print(first_pi.decode())
    print("\n\033[32mSent Raspberry Pi Public Key:\033[m")
    print(pi_key,"\nlen:",len(pi_key))
    client_sock.send(pi_key)

    #Receive phone Key    
    phone_key = client_sock.recv(2048)
    phone_key = "-----BEGIN PUBLIC KEY-----\n"+phone_key.decode()+"\n-----END PUBLIC KEY-----"
    print("Phone Public Key:\n",phone_key)
    pre_key_RSA = RSA.import_key(phone_key)


    # pi_pub_key = ""
    # print("\n\033[32mSent:\033[m\t\t",pi_pub_key,sep="")
    # if(client_sock!=None):
    #     client_sock.send(pi_pub_key)
    # v = 0

    code = 0
    for i in first_pi:
        code+=(i-65)
    print("\nverification code =",code)

    setup()
    try:
        print("\nStarting IR Listener\n")
        c = 0
        v = 0
        while (c!=10):
            c+=1
            print("Waiting for signal...")
            GPIO.wait_for_edge(pin, GPIO.FALLING)
            ir = on_ir_receive(pin)
            if ir:
                print("Hex:",str(hex(ir)))
                print("Dec:",str(ir),"\n")
                if ir == code:
                    client_sock.send(b"verification successful")
                    print("\033[33mVerification successful!\033[m")
                    global_var.verified = 1
                    global_var.verified_sock = client_sock
                    return True
            else:
                print("Invalid code\n")
            client_sock.send(b"F")

    except Exception as e:
        print("Quitting:",e)
        destroy()

    print("\033[33mVerification failure!\033[m")
    return False

    

if(__name__ == "__main__"):
    verify(None)