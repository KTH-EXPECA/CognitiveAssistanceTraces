from parse_video_stream import read_video_stream
from typing import Dict
from scapy.all import *

def find_videoframe_timestamps(pcap: str) -> Dict:
    with rdpcap(pcap) as trace:
        for pkt in trace:


