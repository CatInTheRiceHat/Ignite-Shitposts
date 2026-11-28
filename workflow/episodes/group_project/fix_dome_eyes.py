#!/usr/bin/env python3
"""Turn painted ^ ^ arc eyes back into the SMUG half-moons (filled, flat along the bottom) on one Sol.

Usage (workflow/.venv/bin/python): fix_dome_eyes.py <in.mp4> <out.mp4> x0 y0 x1 y1 first_frame [last_frame]
The box (in the clip's own pixels) holds that Sol's eyes and no other Sol's. In each frame of the range, each navy eye
mark in the box is filled out to its convex hull: an upward arc becomes a half-moon with a flat base, which is the smug
eye in the skeleton. An eye that is already a filled half-moon or an oval is left as it is (its hull is itself).
Why: clip 8, paints v5 and v6 (2026-11-27). Elaine asked for our Sol to "do the smirk animation" on the last beat; the
skeleton has the half-moons, and the painter drew them for a quarter of a second and then thinned them into happy arcs.
"""
import subprocess, sys
import cv2, numpy as np

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1, first = map(int, sys.argv[3:8])
last = int(sys.argv[8]) if len(sys.argv) > 8 else 10 ** 9
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
w, h = int(cap.get(3)), int(cap.get(4))
out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n, fixed = 0, 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    n += 1
    if first <= n <= last:
        roi = fr[y0:y1, x0:x1]
        b, g, r = (roi[..., i].astype(int) for i in range(3))
        navy = ((r < 150) & (g < 135) & (b < 190) & (r + g + b < 400)).astype(np.uint8)       # any dark mark on the cream face: thin arcs come back nearly black
        k, lab, st, _ = cv2.connectedComponentsWithStats(navy)
        eyes = sorted((j for j in range(1, k) if st[j][4] >= 6), key=lambda j: -st[j][4])[:2]
        big = cv2.resize(roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)          # drawn at 4x and scaled back: smooth edges
        for j in eyes:
            ys, xs = np.nonzero(lab == j)
            hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
            col = tuple(int(v) for v in np.median(roi[lab == j], axis=0))
            cv2.fillConvexPoly(big, (hull * 4 + 2).astype(np.int32), col, lineType=cv2.LINE_AA)
        if eyes:
            fr[y0:y1, x0:x1] = cv2.resize(big, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
            fixed += 1
    out.stdin.write(fr.tobytes())
out.stdin.close()
out.wait()
print(f"{n} frames; eyes filled in {fixed}")
