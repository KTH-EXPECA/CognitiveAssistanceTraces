#!/usr/bin/env python3
from scapy.all import *

INFILE = 'lego/server.pcap'
paks = rdpcap(INFILE)
sessions = paks.sessions()
video_stream_session = sessions['TCP 128.237.191.147:33086 > 128.237.192.28:9098']

s = conf.L3socket(iface='wlp59s0')

raw_data = bytes()

for pkt in video_stream_session:
    if Raw in pkt:
        # print(type(pkt[Raw].load))
        # exit()
        raw_data = raw_data + pkt[Raw].load

pos = 0
count = 0
while pos < len(raw_data):
    h_len_net = raw_data[pos:pos + 4]
    pos += 4

    (h_len,) = struct.unpack('>I', h_len_net)
    header_net = raw_data[pos:pos + h_len]
    pos += h_len

    (header,) = struct.unpack('>{}s'.format(h_len), header_net)
    print(header.decode('utf-8'))

    # get image
    d_len_net = raw_data[pos: pos + 4]
    pos += 4

    (d_len,) = struct.unpack('>I', d_len_net)

    data_net = raw_data[pos: pos + d_len]
    pos += d_len

    (data,) = struct.unpack('>{}s'.format(d_len), data_net)

    with open('imgs/{}.jpeg'.format(count), 'wb') as f:
        f.write(data)

    count += 1
