#!/usr/bin/env python3
import json
import struct
from typing import Dict

from lego_timing import extract_timestamps


def read_video_stream(path: str) -> Dict[int, bytes]:
    with open(path, 'rb') as data_file:
        stream = data_file.read()

    pos = 0
    stream_len = len(stream)
    results = dict()

    while pos < stream_len:
        # stream format:
        # 0 | header_len: int32   |
        # 1 | header: header_len  |
        # 2 | data_len: int32     |
        # 3 | data: data_len      |

        # get header
        h_len_net = stream[pos: pos + 4]
        pos += 4

        (h_len,) = struct.unpack('>I', h_len_net)

        header_net = stream[pos: pos + h_len]
        pos += h_len

        (header,) = struct.unpack('>{}s'.format(h_len), header_net)
        frame_id = json.loads(header.decode('utf-8'))['frame_id']

        # get image
        d_len_net = stream[pos: pos + 4]
        pos += 4

        (d_len,) = struct.unpack('>I', d_len_net)
        data_net = stream[pos: pos + d_len]
        pos += d_len

        (data,) = struct.unpack('>{}s'.format(d_len), data_net)

        assert d_len == len(data)
        results[frame_id] = data

    return results


if __name__ == '__main__':
    data = read_video_stream('lego/client_videostream_data.bin')
    timestamps = extract_timestamps('lego/client.pcap')

    assert len(data) == len(timestamps)
    trace = dict()
    previous_time = 0

    for i, frame in enumerate(sorted(data.keys())):
        if i == 0:
            delta_t = 0
        else:
            delta_t = timestamps[frame] - previous_time

        previous_time = timestamps[frame]
        trace[frame] = {
            'delta_t'   : delta_t,
            'frame_size': len(data[frame]),
            'frame'     : data[frame]
        }

    with open('lego/client_out_video.trace', 'wb') as f:
        for frame_id, frame_data in trace.items():
            metadata = struct.pack('III',
                                   frame_data['delta_t'],
                                   frame_id,
                                   frame_data['frame_size'])
            f.write(metadata)
            f.write(frame_data['frame'])
