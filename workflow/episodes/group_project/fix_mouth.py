#!/usr/bin/env python3
"""Paint out a mouth the painter drew on Sol (he has none, ever). For clip 4b, paint v1 (2026-11-27).

Usage (workflow/.venv/bin/python): fix_mouth.py <in.mp4> <out.mp4> x0 y0 x1 y1 [first_frame=1] [last_frame]
The box holds his face. From first_frame on, anything inside his cream face that is not cream and not one of his navy
eyes, and sits lower than his eyes, is filled in from the cream around it. Frames before first_frame and after last_frame
pass through untouched. (Clip 7, paint v6: an open one for half a second while he flaps his nubs, frames 108 to 130.)
candle_flame_up/remove_mouth.py did most of it but only knew dark red; this mouth starts pink.
"""
import subprocess, sys
import cv2, numpy as np

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(int, sys.argv[3:7])
first = int(sys.argv[7]) if len(sys.argv) > 7 else 1
last = int(sys.argv[8]) if len(sys.argv) > 8 else 10 ** 9
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
w, h = int(cap.get(3)), int(cap.get(4))
out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n, fixed = 0, []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    n += 1
    if first <= n <= last:
        roi = fr[y0:y1, x0:x1]
        b, g, r = (roi[..., i].astype(int) for i in range(3))
        cream = ((r > 205) & (g > 168) & (b > 105) & (r - b < 150)).astype(np.uint8)
        navy = ((r < 120) & (g < 120) & (b < 170) & (b >= r - 5)).astype(np.uint8)
        ff = np.pad(1 - cream, 1, constant_values=1).astype(np.uint8)          # flood the not-cream in from the box edge
        cv2.floodFill(ff, None, (0, 0), 2)
        holes = (ff[1:-1, 1:-1] == 1)                                          # not cream, and walled in by cream: eyes, a mouth
        ys = np.where(navy & holes)[0]
        if len(ys):
            eye_y = int(np.median(ys))
            mouth = holes & (cv2.dilate(navy, np.ones((5, 5), np.uint8)) == 0)
            mouth[:eye_y + 5, :] = False
            if mouth.sum() > 6:
                m = cv2.dilate(mouth.astype(np.uint8), np.ones((5, 5), np.uint8))
                fr[y0:y1, x0:x1] = cv2.inpaint(roi, m, 4, cv2.INPAINT_TELEA)
                fixed.append(n)
    out.stdin.write(fr.tobytes())
out.stdin.close()
out.wait()
print(f"{n} frames; mouth painted out in {len(fixed)}: {fixed[:1]} to {fixed[-1:]}")
