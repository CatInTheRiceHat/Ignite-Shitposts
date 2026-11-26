#!/usr/bin/env python3
"""Scan EVERY frame of painted clips for Sol's face going off-model. Sol is mouthless (Elaine, 2026-11-25).

Usage: check_faces.py clip.mp4 [clip2.mp4 ...]
For each frame it finds Sol's cream face (a cream patch ringed by his orange layer) and reports:
  MOUTH   a non-navy patch enclosed in the cream face (a mouth, tongue, teeth, blush or smile line)
  EYES    the navy eye area, as a share of the face, collapsing against the clip's normal
          (eyes closed, squinting or missing)
It prints the offending time ranges. A clean clip prints "clean". This is a detector, not proof of a
good clip: still look at the footage.
"""
import sys, cv2, numpy as np


def analyse(frame):
    b, g, r = [frame[..., i].astype(int) for i in range(3)]
    cream = ((r > 215) & (g > 185) & (b > 120) & (r - b < 130)).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cream, 8)
    orange = ((r > 190) & (g > 80) & (g < 200) & (b < 120) & (r - b > 90)).astype(np.uint8)
    mouth_px, eye_share, found = 0, 0.0, False
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < 1200:
            continue
        x0, y0, x1, y1 = max(x - 12, 0), max(y - 12, 0), min(x + w + 12, frame.shape[1]), min(y + h + 12, frame.shape[0])
        comp = (lab[y0:y1, x0:x1] == i).astype(np.uint8)
        ring = (cv2.dilate(comp, np.ones((17, 17), np.uint8)) > 0) & (comp == 0)
        if orange[y0:y1, x0:x1][ring].mean() < 0.55:
            continue                                       # not ringed by his orange layer: a candle, a page
        pad = cv2.copyMakeBorder(comp, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
        ff = pad.copy()
        cv2.floodFill(ff, None, (0, 0), 2)                 # everything reachable from outside
        holes = (ff[1:-1, 1:-1] == 0)                      # enclosed, not cream: eyes, or a mouth
        rr, bb = r[y0:y1, x0:x1], b[y0:y1, x0:x1]
        navy = holes & (bb > rr + 15) & (rr < 110)
        other = (holes & ~navy).astype(np.uint8)
        other = cv2.morphologyEx(other, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))    # ignore 1 px fringes
        guard = cv2.dilate(navy.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0      # eye edges are not mouths
        mouth_px = max(mouth_px, int((other.astype(bool) & ~guard).sum()))
        if not found or navy.sum() / area > eye_share:
            eye_share = navy.sum() / area
        found = True
    return mouth_px, (eye_share if found else -1.0)


def ranges(flags, fps):
    out, start = [], None
    for i, f in enumerate(list(flags) + [False]):
        if f and start is None:
            start = i
        if not f and start is not None:
            if i - start >= 2:                             # at least two frames in a row
                out.append(f"{start / fps:.2f}-{i / fps:.2f}s")
            start = None
    return out


bad = False
for path in sys.argv[1:]:
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    rows = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        rows.append(analyse(fr))
    m = np.array([a for a, _ in rows])
    e = np.array([b for _, b in rows])
    seen = e[e > 0]
    normal = np.median(seen) if len(seen) else 0
    mouth = ranges(m > 40, fps)
    eyes = ranges((e >= 0) & (e < 0.45 * normal), fps) if normal else ["no face found"]     # e < 0: no face in shot
    name = path.split("/")[-1]
    if mouth or eyes:
        bad = True
        print(f"{name}: " + ("MOUTH at " + ", ".join(mouth) if mouth else "") + ("  " if mouth and eyes else "")
              + ("EYES closed or hidden at " + ", ".join(eyes) if eyes else ""))
    else:
        print(f"{name}: clean ({len(rows)} frames)")
sys.exit(1 if bad else 0)
