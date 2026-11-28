#!/usr/bin/env python3
"""Clip 2: the opening and the teammates from one paint, the ending from another, joined inside the whip back.

Usage (workflow/.venv/bin/python): splice_clip2.py   ->  clips/02-paint-v11v5.mp4
Elaine on cut v12 (2026-11-28), of the built hands-on-hips arms: "can we bring back the old hands on hips thing like the
first one u did before". The first one is paint v5 (cuts v8 to v10): his nubs tucked against his sides, as the painter
drew them. So:
  paint v11 (frames 0-71): the glare with the LEVEL pointing nub, the whip, the three teammates (ring at Ring Sol's feet,
            all three whole), and the start of the whip back.
  paint v5  (frames 72-163): Sol's close-up after the whip, ending in the first hands-on-hips pose.
Both follow the same camera, both have the same bucket and shovel behind him, and the join is in the middle of the whip
back, where the picture is a blur anyway. Line paints up by eye before changing the frame numbers.
(Earlier joins: v2 + v3 for cut v7, v5 + v4 for cuts v8 to v10, v6 + v4 never shown.)
"""
import pathlib, subprocess
import cv2

HERE = pathlib.Path(__file__).resolve().parent / "clips"


def frames(name):
    cap = cv2.VideoCapture(str(HERE / name))
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            return out
        out.append(f)


a, b = frames("02-paint-v11.mp4"), frames("02-paint-v5.mp4")
seq = a[:72] + b[72:]
h, w = seq[0].shape[:2]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "24", "-i", "-",
                      "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(HERE / "02-paint-v11v5.mp4")], stdin=subprocess.PIPE)
for f in seq:
    p.stdin.write(f.tobytes())
p.stdin.close()
p.wait()
print(len(seq), "frames ->", HERE / "02-paint-v11v5.mp4")
