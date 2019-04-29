# Cognitive assistance traces

Workload traces for cognitive assistance applications.

## Using the traces

You can find the actual per task step traces in the ```lego\HeadTrace1``` and ```lego\HeadTrace2``` directories.
The traces are provided in a binary format (extension .trace) with the following byte structure:

```
1   8|9   16|17  32
-------------------
| hdr_len: int32  |
-------------------
|                 |
|  header: JSON   |
|                 |
|       ...       |
-------------------
| frme_len: int32 |
-------------------
|                 |
|   frame: JPEG   |
|                 |
|       ...       |
-------------------
| frme_len: int32 |
-------------------
|                 |
|   frame: JPEG   |
|                 |
|       ...       |
-------------------
|       ...       |
```

The first element of the binary stream corresponds to a 4-byte integer detailing the byte length of the file header.
The file header itself comes directly after this value, and corresponds to a JSON string with the following structure:

```json5
{
    "name": "Trace1",   // <Trace Name: str>,
    "index": 2,         // <Task step index: int>,
    "num_frames": 212,  // <Number of frames in trace: int>,
    "key_frame": 170    // <Key frame: int>
}
```

The ```key_frame``` key refers to the 1-based index of the first frame we expect to pass the recognition threshold on the Computer Vision backend, and thus trigger a transition to the next task step.

The JPEG frames are packed sequentially after the header, each frame preceded by a 4-byte integer detailing its byte length.

If needed, the raw JPEG image frames are present in the respective ```frames``` subdirectories, organized into additional subdirectories for each step in the task.

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Copyright © KTH Royal Institute of Technology, Carnegie Mellon University

These files are provided under a CC-BY-4.0 License.

See [LICENSE](LICENSE) for details.
