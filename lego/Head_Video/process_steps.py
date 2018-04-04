import pathlib
from typing import Tuple
import json
import struct

STEPDIR = './frames'


def get_steps() -> Tuple:
    p = pathlib.Path(STEPDIR)
    steps_p = [x for x in p.iterdir() if x.is_dir()]
    return tuple(sorted(steps_p))


def process_step(step_dir: pathlib.Path) -> None:
    name = step_dir.parts[-1]

    frames = [x for x in step_dir.iterdir()
              if str(x).startswith('frame') and str(x).endswith('.jpeg')]
    frames.sort()

    header = {
        'name'      : name,
        'num_frames': len(frames)
    }

    header_b = json.dumps(header, separators=(',', ':')).encode('utf-8')

    with open(name, 'wb') as f:
        packed_header = struct.pack('>I{len}s'.format(len=len(header_b)),
                                    len(header_b), header_b)
        f.write(packed_header)
        for frame in frames:
            data = frame.read_bytes()
            packed_frame = struct.pack('>I{len}s'.format(len=len(data)),
                                       len(data), data)
            f.write(packed_frame)


if __name__ == '__main__':
    step_dirs = get_steps()
    for step in step_dirs:
        process_step(step)
