#!/usr/bin/env python3
"""Lay out EVERY frame of a video on contact sheets, in order, each labelled with its time, for the post-check.

Elaine, 2026-11-26: "as a post check procedure be sure to analyze all the frames of the final clip".
A sample is not enough: a prop can lose a part or a mouth can appear for three frames.

Usage (run with workflow/.venv/bin/python):
  frame_review.py cut.mp4 out_dir [--cols 8] [--rows 5] [--width 180] [--edit episodes/<name>/edit.json]
Writes out_dir/sheet-001.png ... (cols x rows frames each; every frame of the video is on exactly one sheet)
and prints:
  - the number of frames and sheets
  - JUMP lines: frames that differ sharply from the frame before although no cut is planned there. A jump inside
    a clip is where a morph, a pop or a swapped prop usually sits, so look at those frames first.
With --edit the planned cut times come from that edit.json, so real cuts are not reported as jumps.
Looking at the sheets is the check. The JUMP list only points at where to look hardest.
"""
import argparse, json, pathlib
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("out")
ap.add_argument("--cols", type=int, default=8)
ap.add_argument("--rows", type=int, default=5)
ap.add_argument("--width", type=int, default=180)
ap.add_argument("--edit")
a = ap.parse_args()

out = pathlib.Path(a.out)
out.mkdir(parents=True, exist_ok=True)
cuts = []
if a.edit:
    t = 0.0
    for _, d in json.loads(pathlib.Path(a.edit).read_text())["clips"]:
        t += d
        cuts.append(t)

cap = cv2.VideoCapture(a.video)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
except Exception:
    font = ImageFont.load_default()

per = a.cols * a.rows
tiles, diffs, prev, n, sheet = [], [], None, 0, 0
th = None


def flush():
    global tiles, sheet
    if not tiles:
        return
    sheet += 1
    im = Image.new("RGB", (a.cols * a.width, a.rows * th), (20, 20, 20))
    for k, (t_, tile) in enumerate(tiles):
        x, y = (k % a.cols) * a.width, (k // a.cols) * th
        im.paste(tile, (x, y))
        d = ImageDraw.Draw(im)
        d.rectangle((x, y, x + 62, y + 18), fill=(0, 0, 0))
        d.text((x + 3, y + 1), f"{t_:6.2f}", font=font, fill=(255, 255, 0))
    im.save(out / f"sheet-{sheet:03d}.png")
    tiles = []


while True:
    ok, fr = cap.read()
    if not ok:
        break
    t = n / fps
    small = cv2.resize(fr, (64, 114), interpolation=cv2.INTER_AREA).astype(np.int16)
    if prev is not None:
        diffs.append((t, float(np.abs(small - prev).mean())))
    prev = small
    h = int(round(fr.shape[0] * a.width / fr.shape[1]))
    th = th or h
    tiles.append((t, Image.fromarray(cv2.cvtColor(cv2.resize(fr, (a.width, th), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB))))
    n += 1
    if len(tiles) == per:
        flush()
flush()

print(f"{n} frames at {fps:.0f} fps = {n / fps:.2f}s, {sheet} sheets of {a.cols}x{a.rows} in {out}")
vals = np.array([d for _, d in diffs]) if diffs else np.array([0.0])
base = float(np.median(vals))
limit = max(base * 5, 6.0)
jumps = [(t, d) for t, d in diffs if d > limit and not any(abs(t - c) < 1.5 / fps for c in cuts)]
print(f"typical frame-to-frame change {base:.2f}; jump threshold {limit:.2f}; planned cuts at " + ", ".join(f"{c:.2f}" for c in cuts[:-1]))
if jumps:
    for t, d in jumps:
        print(f"JUMP at {t:.2f}s (frame {int(round(t * fps))}): change {d:.1f}")
else:
    print("no jumps outside the planned cuts")
