from netifaces import interfaces, ifaddresses, AF_INET
import os

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