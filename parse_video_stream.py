#!/usr/bin/env python3
import struct
from typing import Dict
import json


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

        results[frame_id] = data

    return results


if __name__ == '__main__':
    results = read_video_stream('lego/client_stream_data.bin')
    for k, v in results.items():
        print(k)
