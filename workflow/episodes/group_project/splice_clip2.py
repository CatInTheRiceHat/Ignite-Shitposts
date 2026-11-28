#!/usr/bin/env python3
"""Clip 2 for cut v6: Sol's two close-ups from paint v2, his teammates from paint v3, joined inside the two whip pans.

Usage (workflow/.venv/bin/python): splice_clip2.py   ->  clips/02-paint-v2v3.mp4
Why: paint v3 has the swim ring at Ring Sol's feet (Elaine, 2026-11-27: "HE CANT EVEN SEE ... CAN WE LIKE MAKE IT LOWER"),
but in its second close-up the set redraws itself behind Sol (a shovel grows in, the castle turns into a ball, a second
string of flags fades in: the independent review of cut v6). Paint v2's close-ups are clean, and its teammates have the
ring across Ring Sol's face. Both paints come from the same skeleton, so each half is taken from the paint that got it
right and the joins sit in the middle of the whip pans (0.9-1.25 s and 2.75-3.1 s), where the picture is a blur anyway.
Paint v2 whips back three frames later than v3, so two of its frames are dropped at the second join; the last frame is
held for three frames so the clip is 6.54 s.
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


a, b = frames("02-paint-v2.mp4"), frames("02-paint-v3.mp4")
seq = a[:25] + b[25:72] + a[74:] + [a[-1]] * 3
h, w = seq[0].shape[:2]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "24", "-i", "-",
                      "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(HERE / "02-paint-v2v3.mp4")], stdin=subprocess.PIPE)
for f in seq:
    p.stdin.write(f.tobytes())
p.stdin.close()
p.wait()
print(len(seq), "frames ->", HERE / "02-paint-v2v3.mp4")
