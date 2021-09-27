from netifaces import interfaces, ifaddresses, AF_INET
import os
from Crypto.PublicKey import RSA   # pip3 install -U PyCryptodome
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

# for ifaceName in interfaces():
#     addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
#     print(addresses)

# msg = "ABC"
# count = 0

# for i in msg:
#     print("i =", i)
#     count+=(ord(i)-65)

# print("count =", count)

i = os.popen("ifconfig | egrep -o 'inet [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ' | sed '1d;s/inet //g'")
i = i.read()
i = "rtsp://"+i[:-2]+":8554/unicast"
print(i)

# # Read Private Key
# encodedKey = open("private.pem", "rb")
# pi_key = RSA.import_key(encodedKey.read())

# print("\n\033[32mSent Raspberry Pi Public Key:\033[m")
# print(pi_key.publickey().export_key().decode('utf-8'))
# pi_key = pi_key.publickey().export_key()
# pi_key = pi_key[27:-25]
# first_pi = pi_key[:5]
# print(first_pi)

# code = 0
# for i in first_pi:
#     code+=(i-65)
# print("verification code =",code)