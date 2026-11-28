#!/usr/bin/env python3
"""Make a finished clip a little longer WITHOUT freezing its last frame: the last few frames play backwards and then
forwards again (a ping-pong), so a Sol who is standing with his small idle sway keeps swaying.

Usage (workflow/.venv/bin/python): extend_tail.py <in.mp4> <out.mp4> <extra frames>
Why: Elaine, 2026-11-27, on cut v8: "somehow its just frozen". The Eleven v4 narrator reads slower than the takes the
shots were painted to, so clips 4 and 6 needed 6 and 19 more frames; in v8 that was a held last frame, which is a freeze.
Only for a clip that ENDS on a held pose with idle motion. Not for a clip that ends in the middle of an action.
"""
import subprocess, sys
import cv2

src, dst, extra = sys.argv[1], sys.argv[2], int(sys.argv[3])
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
fr = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    fr.append(f)
back = (extra + 1) // 2                                  # frames walked backwards, then forwards again
tail = [fr[-2 - i] for i in range(back)]                 # n-2, n-3, ...
tail += [fr[len(fr) - 1 - back + i] for i in range(1, extra - back + 1)]
assert len(tail) == extra
h, w = fr[0].shape[:2]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
for f in fr + tail:
    p.stdin.write(f.tobytes())
p.stdin.close()
p.wait()
print(f"{len(fr)} + {extra} frames -> {dst}")
