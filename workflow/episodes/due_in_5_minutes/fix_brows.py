#!/usr/bin/env python3
"""Paint out eyebrow strokes the painter added above Sol's eyes. Sol has no eyebrows (script v4, character notes).

Usage (workflow/.venv/bin/python):  fix_brows.py in.mp4 out.mp4 x,y,w,h [t0 t1] [--redraw]
  x,y,w,h : a box (in the clip's own pixels) that holds Sol's face for the whole clip
  t0 t1   : only touch frames between these times (default: the whole clip)
  --redraw: also lay clean navy oval eyes back over his eyes. For frames where the brow is fused to the eye and has
            cut its top off (the worried beat of clip 7). Do not use where the eyes carry sparkles.

How a brow is told apart:
  - his eyes are the fat navy blobs (found by opening the dark mask with a round brush, which erases thin strokes);
  - the worried look's thin lines are vertical, so they survive an opening with a tall 1-pixel brush and are kept;
  - any other stroke clearly darker than the face around it, in a band above an open eye, is a brow.
It is filled in from the face colour around it. Frames with no open eye (a blink) are left alone. Nothing outside
the box is touched. The input file is kept.
"""
import subprocess, sys
import cv2, numpy as np

REF = None                                   # --ref a,b : measure his clean eye size in this time window instead
for a in list(sys.argv):
    if a.startswith("--ref="):
        REF = [float(v) for v in a[6:].split(",")]
args = [a for a in sys.argv[1:] if a not in ("--redraw", "--sparkle") and not a.startswith("--ref=")]
SPARKLE = "--sparkle" in sys.argv          # redraw, and put the white four-point sparkle and dot back in each eye
REDRAW = "--redraw" in sys.argv or SPARKLE
src, dst = args[0], args[1]
X, Y, W, H = [int(v) for v in args[2].split(",")]
T0, T1 = (float(args[3]), float(args[4])) if len(args) > 4 else (0.0, 1e9)
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
w, h = int(cap.get(3)), int(cap.get(4))
ROUND = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
TALL = np.ones((7, 1), np.uint8)


def find_eyes(roi):
    """His two eyes: a pair of navy ovals side by side. Returns (navy mask, mask of the two eyes, [(stats, centre)])."""
    b, g, r = [roi[..., i].astype(int) for i in range(3)]
    navy = ((np.maximum(np.maximum(r, g), b) < 135) & (b >= r - 12) & (r < 110)).astype(np.uint8)
    solid = cv2.morphologyEx(navy, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    flood = cv2.copyMakeBorder(solid, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.floodFill(flood, None, (0, 0), 2)
    solid = (flood[1:-1, 1:-1] != 2).astype(np.uint8)                     # sparkles are holes in the eye: fill them
    solid = cv2.morphologyEx(solid, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))   # drop hair-thin strokes hanging off an eye
    k, lab, stats, cent = cv2.connectedComponentsWithStats(solid, 8)
    cands = []
    for i in range(1, k):
        x, y, w_, h_, area = stats[i]
        if 45 <= area <= 2500 and 0.75 <= h_ / max(w_, 1) <= 2.6 and area / (w_ * h_) > 0.5 and h_ >= 8:
            cands.append(i)
    best = None
    for a in cands:
        for b_ in cands:
            if stats[a][0] >= stats[b_][0]:
                continue
            sa, sb = stats[a], stats[b_]
            gap = sb[0] - (sa[0] + sa[2])
            if abs(cent[a][1] - cent[b_][1]) < 0.6 * max(sa[3], sb[3]) and 0.5 < sa[4] / sb[4] < 2.0 and 0.3 * sa[2] < gap < 5 * sa[2]:
                score = sa[4] + sb[4]
                if best is None or score > best[0]:
                    best = (score, a, b_)
    if best is None:
        return navy, np.zeros_like(navy), lab, []
    pair = [best[1], best[2]]
    fat = np.isin(lab, pair).astype(np.uint8)
    return navy, fat, lab, [(stats[i], cent[i], i) for i in pair]


# the size his clean eyes have in this clip: the median over frames outside the span being fixed
frames, sizes = [], []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    frames.append(fr)
    t = (len(frames) - 1) / fps
    if REDRAW and ((REF[0] <= t <= REF[1]) if REF else not (T0 <= t <= T1)):
        _, _, _, eyes = find_eyes(fr[Y:Y + H, X:X + W])
        if len(eyes) == 2:
            sizes += [(e[0][2], e[0][3]) for e in eyes]
EW, EH = (np.median([s[0] for s in sizes]), np.median([s[1] for s in sizes])) if sizes else (0, 0)

out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
fixed = 0
for n, fr in enumerate(frames):
    t = n / fps
    if T0 <= t <= T1:
        roi = fr[Y:Y + H, X:X + W]
        navy, fat, lab, eyes = find_eyes(roi)
        if len(eyes) == 2:
            lum = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            around = cv2.medianBlur(lum, 31)
            dark = ((around.astype(int) - lum.astype(int) > 28) | (navy > 0)).astype(np.uint8)
            lines = cv2.dilate(cv2.morphologyEx(dark & (1 - cv2.dilate(fat, np.ones((5, 5), np.uint8))), cv2.MORPH_OPEN, TALL), np.ones((3, 3), np.uint8))
            band = np.zeros_like(dark)
            for st, _, _ in eyes:
                ex, ey, ew, eh = st[:4]
                band[max(ey - int(1.2 * eh), 0):ey + (eh if REDRAW else eh // 3), max(ex - int(0.8 * ew), 0):ex + ew + int(0.8 * ew)] = 1
            eye_keep = np.zeros_like(dark) if REDRAW else cv2.dilate(fat, np.ones((5, 5), np.uint8))
            brow = dark & band & (1 - lines) & (1 - eye_keep)
            if brow.sum() >= 6:
                mask = cv2.dilate(brow, np.ones((5, 5), np.uint8)) & (1 - lines)
                if not REDRAW:
                    mask &= 1 - cv2.dilate(fat, np.ones((3, 3), np.uint8))
                fixed_roi = cv2.inpaint(roi, mask * 255, 5, cv2.INPAINT_TELEA)
                if REDRAW:
                    layer = np.zeros(roi.shape[:2], np.float32)
                    colour = np.array([71.0, 36.0, 28.0])                   # navy #1C2447, as BGR
                    for st, c, i in eyes:
                        # the fused brow sits on top of the eye, so the eye's own bottom edge is the part to trust
                        bottom = st[1] + st[3]
                        cv2.ellipse(layer, (int(round(c[0] * 16)), int(round((bottom - EH / 2) * 16))), (int(round(EW * 8)), int(round(EH * 8))), 0, 0, 360, 1.0, -1, cv2.LINE_AA, 4)
                    layer = cv2.GaussianBlur(layer, (0, 0), 0.7)[..., None]
                    fixed_roi = (fixed_roi * (1 - layer) + colour[None, None, :] * layer).astype(np.uint8)
                    if SPARKLE:
                        white = np.zeros(roi.shape[:2], np.float32)
                        for st, c, i in eyes:
                            cx, cy = c[0], st[1] + st[3] - EH / 2 - 0.06 * EH
                            pts = []
                            for k_ in range(8):                               # a four-point star: long points up and down
                                ang = np.pi / 4 * k_
                                rad = (0.11 * EW) if k_ % 2 else (0.40 * EW if k_ % 4 else 0.50 * EW)
                                pts.append([(cx + rad * np.sin(ang)) * 16, (cy - rad * np.cos(ang)) * 16])
                            cv2.fillPoly(white, [np.int32(np.round(pts))], 1.0, cv2.LINE_AA, 4)
                            cv2.circle(white, (int(round((cx + 0.2 * EW) * 16)), int(round((cy + 0.33 * EH) * 16))), int(round(0.075 * EW * 16)), 1.0, -1, cv2.LINE_AA, 4)
                        white = cv2.GaussianBlur(white, (0, 0), 0.5)[..., None]
                        fixed_roi = (fixed_roi * (1 - white) + 255.0 * white).astype(np.uint8)
                fr[Y:Y + H, X:X + W] = fixed_roi
                fixed += 1
    out.stdin.write(fr.tobytes())
out.stdin.close()
out.wait()
print(f"{src} -> {dst}: {len(frames)} frames, fixed {fixed}" + (f", clean eye size {EW:.0f}x{EH:.0f}" if REDRAW else ""))
