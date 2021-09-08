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

i = os.popen("ifconfig")
i = i.read()
print("\n\n",i)


