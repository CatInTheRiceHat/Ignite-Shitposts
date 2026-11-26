#!/usr/bin/env python3
"""Turn the space clip's blue teardrop flame into the round blue ball the script calls for.

Usage: fix_flame_ball.py in.mp4 out.mp4
The painter turned the flame blue but kept giving it a pointed tip, in three separate paint passes, while
the narrator says "a little blue ball". This finds the blue flame in each frame, paints it out with the
surrounding picture, and draws a soft round blue ball sitting on the wick in its place. The orange flame
at the start of the clip is left alone, and the ball fades in over the first frames after it turns blue.
"""
import sys, cv2, numpy as np

src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames = []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    frames.append(fr)
H, W = frames[0].shape[:2]
X0, Y0 = int(W * 0.50), int(H * 0.36)                  # the candle box sits in the right, lower-middle of frame


def find(fr):
    roi = fr[Y0:int(H * 0.80), X0:].astype(int)
    b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
    blue = ((b > 215) & (b - r > 95)).astype(np.uint8)      # the saturated blue of the flame, not its pale halo
    blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(blue, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a > 180 and h < 220 and w < 160 and (best is None or a > best[4]):
            best = (x + X0, y + Y0, w, h, a)
    return best


found = [find(f) for f in frames]
first = next((i for i, v in enumerate(found) if v), None)
if first is None:
    sys.exit("no blue flame found")
sm = None
out = cv2.VideoWriter(dst + ".tmp.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
fixed = 0
for i, fr in enumerate(frames):
    v = found[i]
    if v is None and sm is not None and i > first:
        v = last                                           # a dropped detection: keep the last position
    if v is None:
        out.write(fr)
        continue
    last = v
    x, y, w, h, _ = v
    cur = np.array([x + w / 2, y + h, max(w, 40) * 0.38])  # wick x, wick y (bottom of the flame), ball radius: a LITTLE ball
    sm = cur if sm is None else 0.6 * sm + 0.4 * cur     # smooth so the ball does not jitter
    bx, by, rad = sm[0], sm[1], sm[2]
    # paint the teardrop (and its tip) out
    mask = np.zeros((H, W), np.uint8)
    cv2.rectangle(mask, (x - 8, y - 12), (x + w + 8, y + h - 4), 255, -1)       # stop above the wax
    clean = cv2.inpaint(fr, mask, 5, cv2.INPAINT_TELEA)
    # the ball: bright core, blue rim, soft glow, sitting on the wick
    cy = by - rad * 0.92
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - bx, yy - cy)
    core = np.hypot(xx - (bx - rad * 0.12), yy - (cy - rad * 0.10)) / rad
    t = np.clip(core, 0, 1)[..., None]
    col = (1 - t) * np.array([255, 250, 232.0]) + t * np.array([250, 170, 70.0])      # BGR: white-cyan to blue
    col = np.where(t > 0.72, (1 - (t - 0.72) / 0.28) * col + ((t - 0.72) / 0.28) * np.array([235, 130, 50.0]), col)
    inside = np.clip((rad - d) / 1.6 + 0.5, 0, 1)[..., None]
    glow = (np.exp(-np.clip(d - rad, 0, None) ** 2 / (2 * (rad * 0.55) ** 2)) * 0.22)[..., None] * (1 - inside)
    ball = clean.astype(float) * (1 - inside) + col * inside
    ball = ball + glow * np.array([255, 190, 110.0])
    k = min(1.0, (i - first + 1) / 10)                    # fade in as the flame turns blue
    res = fr.astype(float) * (1 - k) + ball * k
    out.write(np.clip(res, 0, 255).astype(np.uint8))
    fixed += 1
out.release()
import subprocess, os
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", dst + ".tmp.mp4", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst], check=True)
os.remove(dst + ".tmp.mp4")
print(f"blue flame from {first / fps:.2f}s; ball drawn on {fixed} of {len(frames)} frames")
