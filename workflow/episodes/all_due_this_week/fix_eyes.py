#!/usr/bin/env python3
"""Repair a few frames where the painter left Sol's eyes half shut and striped (Elaine, 2026-11-26: "a weird flash").

Usage (workflow/.venv/bin/python):  fix_eyes.py <in.mp4> <out.mp4> <first bad frame> <last bad frame> [margin]   (0-based frames)

The rule (guidelines/current-rules.md, section 1): lay the eye area of a good frame over the bad ones. Here the camera
is moving, so the eye area cannot simply be copied in place. The two navy eyes are found in the last good frame BEFORE
the bad run and the first good frame AFTER it; for each bad frame the eye area of the frame before is placed where a
straight line between those two positions puts it, at the size that line gives. Positions come from two good frames
only, so nothing is measured on a bad frame and nothing can jitter.
"""
import subprocess, sys
import cv2, numpy as np

src, out, b0, b1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    frames.append(fr)
H, W = frames[0].shape[:2]


def eyes(fr, near=None):
    """Bounding box (x0, y0, x1, y1) of his two navy eyes: the two largest very dark blue blobs (not the indigo flame
    top, not the thin worry lines). near = a box to look inside (the eyes of another frame, widened). None if not found."""
    b, g, r = [fr[..., i].astype(int) for i in range(3)]
    m = ((b > r + 15) & (r < 60) & (g < 66) & (b < 118)).astype(np.uint8)
    if near is not None:
        w, h = near[2] - near[0], near[3] - near[1]
        keep = np.zeros_like(m)
        keep[max(int(near[1] - 1.5 * h), 0):int(near[3] + 1.5 * h), max(int(near[0] - 0.8 * w), 0):int(near[2] + 0.8 * w)] = 1
        m &= keep
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    ok = [i for i in range(1, n) if 40 < st[i, cv2.CC_STAT_AREA] < 9000
          and (near is not None or st[i, cv2.CC_STAT_HEIGHT] > st[i, cv2.CC_STAT_WIDTH])]
    big = sorted(ok, key=lambda i: -st[i, cv2.CC_STAT_AREA])[:2]
    if len(big) < 2:
        return None
    xs = [st[i, cv2.CC_STAT_LEFT] for i in big] + [st[i, cv2.CC_STAT_LEFT] + st[i, cv2.CC_STAT_WIDTH] for i in big]
    ys = [st[i, cv2.CC_STAT_TOP] for i in big] + [st[i, cv2.CC_STAT_TOP] + st[i, cv2.CC_STAT_HEIGHT] for i in big]
    return np.float32([min(xs), min(ys), max(xs), max(ys)])


A, B = b0 - 1, b1 + 1
ea = eyes(frames[A])
assert ea is not None, "eyes not found in the frame before the bad run"
eb = eyes(frames[B], near=ea)
assert eb is not None, "eyes not found in the frame after the bad run"
print("eyes before", ea, "after", eb)
M = float(sys.argv[5]) if len(sys.argv) > 5 else 0.28       # margin round the eyes, as a share of their width (wider when
                                                             # he moves during the bad frames and the smear sits off to a side)
wa = ea[2] - ea[0]
pa = [int(ea[0] - M * wa), int(ea[1] - M * wa), int(ea[2] + M * wa), int(ea[3] + M * wa)]
patch = frames[A][pa[1]:pa[3], pa[0]:pa[2]]
for f in range(b0, b1 + 1):
    k = (f - A) / (B - A)
    e = ea + (eb - ea) * k
    w = e[2] - e[0]
    x0, y0, x1, y1 = [int(round(v)) for v in (e[0] - M * w, e[1] - M * w, e[2] + M * w, e[3] + M * w)]
    p = cv2.resize(patch, (x1 - x0, y1 - y0), interpolation=cv2.INTER_CUBIC)
    mask = np.zeros((y1 - y0, x1 - x0), np.float32)
    cv2.ellipse(mask, ((x1 - x0) // 2, (y1 - y0) // 2), (int((x1 - x0) * 0.44), int((y1 - y0) * 0.42)), 0, 0, 360, 1.0, -1)
    mask = cv2.GaussianBlur(mask, (0, 0), 4)[..., None]
    frames[f][y0:y1, x0:x1] = (frames[f][y0:y1, x0:x1] * (1 - mask) + p * mask).astype(np.uint8)
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}", "-i", "-",
                         "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for fr in frames:
    proc.stdin.write(fr.tobytes())
proc.stdin.close()
proc.wait()
print(f"repaired frames {b0}-{b1} of {len(frames)} -> {out}")
