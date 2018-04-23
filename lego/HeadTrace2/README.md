# Turtle Head assembly video trace

Folder "./frames" includes the frames extracted from the original head assembly video (640x360@15FPS) in JPEG format.
Original video can be found on: https://kth.box.com/s/omg0ke7razr819y3iw0rw9yn6tzxwtz8 

Command for extracting frames from original video using ffmpeg:

```bash
$ ffmpeg -i VID_20180411_111745.mp4 -r 15.0 -s 640x360 -qscale:v 11 frames/frame_%03d.jpeg
```

Copyright © 2018 - : KTH Royal Institute of Technology, Carnegie Mellon University
