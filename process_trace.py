#!/usr/bin/env python3
from scapy.all import *

INFILE = 'lego/server.pcap'
paks = rdpcap(INFILE)

count = 0
for pak in paks:
    if pak[TCP].dport == 9098:
        count += 1
        # print(pak[0].summary(), len(pak))

print('----')
print(count)
