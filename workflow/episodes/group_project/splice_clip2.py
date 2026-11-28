#!/usr/bin/env python3
"""Clip 2: Sol's two close-ups from one paint, his teammates from another, joined inside the two whip pans.

Usage (workflow/.venv/bin/python): splice_clip2.py   ->  clips/02-paint-v5v4.mp4
Both paints come from the same skeleton (02-skeleton-v5: the confident ending Elaine asked for on cut v7), so each
part is taken from the paint that got it right and the joins sit in the middle of the whip pans (0.9-1.25 s and
2.75-3.1 s), where the picture is a blur anyway.
  paint v5: the close-ups are steady (the same bucket and shovel behind him from first frame to last) and he ends with
            his nubs on his sides; but its teammates came back flat, unpainted.
  paint v4: the teammates are painted, with the ring at Ring Sol's feet; but the castle behind Sol vanishes at 4.7 s.
Line the two up by eye before changing the frame numbers: paints do not whip on the same frame.
(Cut v7 used the same trick with paints v2 and v3 -> 02-paint-v2v3.mp4, from the earlier skeleton with the glare.)
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


a, b = frames("02-paint-v5.mp4"), frames("02-paint-v4.mp4")
seq = a[:25] + b[25:72] + a[72:]
h, w = seq[0].shape[:2]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "24", "-i", "-",
                      "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(HERE / "02-paint-v5v4.mp4")], stdin=subprocess.PIPE)
for f in seq:
    p.stdin.write(f.tobytes())
p.stdin.close()
p.wait()
print(len(seq), "frames ->", HERE / "02-paint-v5v4.mp4")
