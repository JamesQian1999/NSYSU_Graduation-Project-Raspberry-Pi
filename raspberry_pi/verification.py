import global_var
import RPi.GPIO as GPIO
import time

set_pin_R = 13
set_pin_P = 15
codeR = 0
codeP = 0

def setup():
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(set_pin_R, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(set_pin_P, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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
        count = 0
        bits = ''
        for bit in outbin:
            count+=1
            bits += bit
            if(not count%4):
                print(bits,'=>',"dec:",int(bits,2),"hex:",str(hex(int(bits,2))))
                bits = ''
        print("Bin:",outbin)
        return int(outbin, 2)
    except ValueError:
        # probably an empty code
        return None


def destroy():
    GPIO.cleanup()


def verify(client_sock):
    # verified

    msg = "ABCE"
    print("\n\033[32mSent:\033[m\t\t",msg,sep="")
    if(client_sock!=None):
        client_sock.send(msg)
    v = 0

    for i in msg:
        v+=(ord(i)-65)
    print("verification code =",v)

    setup()
    try:
        print("Starting IR Listener")
        codeR = -1
        #while codeR != v:
        if True:
            print("Waiting for signal...")
            GPIO.wait_for_edge(set_pin_P, GPIO.FALLING)
            codeR = on_ir_receive(set_pin_P)
            if codeR:
                print("Hex:",str(hex(codeR)))
                print("Dec:",str(codeR),"\n")
            else:
                print("Invalid code")
    except Exception as e:
        print("Quitting:",e)
        destroy()

    global_var.verified = 1
    global_var.verified_sock = client_sock
    return True

if(__name__ == "__main__"):
    verify(None)