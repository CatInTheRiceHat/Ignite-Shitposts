#!/usr/bin/env python3
"""Put Sol's eyes back open where the painter slipped in a blink or squint.

Usage: fix_blinks.py in.mp4 out.mp4 start end [start end ...]     (times in seconds, from check_faces.py)
For every frame in a range, Sol's face (the cream patch with his eyes) is copied from the last good frame
before the range and laid over the blink, moved to follow where his face has gone. Use it only for short
blinks: a face that turns or changes size a lot during the range will not line up.
"""
import sys, cv2, numpy as np, subprocess, os

src, dst = sys.argv[1], sys.argv[2]
spans = [(float(a), float(b)) for a, b in zip(sys.argv[3::2], sys.argv[4::2])]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames = []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    frames.append(fr)
H, W = frames[0].shape[:2]


def face(fr, near=None, size=None):
    """Filled mask, centroid and area of Sol's cream face.
    With no hints (the good frame) it is the biggest cream patch ringed by his orange layer that HOLDS
    his navy eyes: a patch of candle-lit desk is cream and ringed by orange too, but has no eyes.
    With hints (a blink frame, where the eyes are gone) it is the ringed cream patch of about the same
    size nearest to where his face was."""
    b, g, r = [fr[..., i].astype(int) for i in range(3)]
    cream = ((r > 185) & (g > 155) & (b > 100) & (r - b < 135)).astype(np.uint8)   # loose: includes the shaded side of his face
    orange = ((r > 190) & (g > 80) & (g < 200) & (b < 120) & (r - b > 90)).astype(np.uint8)
    navy = ((b > r + 15) & (r < 110)).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(cream, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 1200:
            continue
        sl = (slice(max(y - 12, 0), y + h + 12), slice(max(x - 12, 0), x + w + 12))
        comp = (lab[sl] == i).astype(np.uint8)
        ring = (cv2.dilate(comp, np.ones((17, 17), np.uint8)) > 0) & (comp == 0)
        if orange[sl][ring].mean() < 0.42:                 # 0.5 missed his face when he stands side-on to the candlelight
            continue
        pad = cv2.copyMakeBorder(comp, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
        cv2.floodFill(pad, None, (0, 0), 2)
        filled = (pad[1:-1, 1:-1] != 2).astype(np.uint8)   # the cream plus whatever it encloses (the eyes)
        if near is None:
            if (navy[sl] * filled).sum() < 40:
                continue                                   # no eyes in it: not his face
            score = area
        else:
            if not (0.6 * size < area < 1.6 * size):
                continue
            score = -np.hypot(cen[i][0] - near[0], cen[i][1] - near[1])
        if best is None or score > best[0]:
            full = np.zeros(fr.shape[:2], np.uint8)
            full[sl] = filled
            best = (score, full, area)
    if best is None:
        return None, None, None
    m = cv2.moments(best[1])
    return best[1], (m["m10"] / m["m00"], m["m01"] / m["m00"]), best[2]


done = 0
for a, b in spans:
    i0, i1 = int(round(a * fps)), min(int(round(b * fps)), len(frames) - 1)
    ref_i = max(i0 - 2, 0)
    ref_mask, ref_c, ref_area = face(frames[ref_i])
    if ref_mask is None:
        print(f"{a}-{b}s: no face in the frame before, skipped")
        continue
    ref = frames[ref_i]
    core = cv2.erode(ref_mask, np.ones((5, 5), np.uint8))
    for i in range(i0, i1 + 1):
        m, c, _ = face(frames[i], near=ref_c, size=ref_area)
        if m is None:
            continue
        dx, dy = c[0] - ref_c[0], c[1] - ref_c[1]
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        moved = cv2.warpAffine(ref, M, (W, H), flags=cv2.INTER_LINEAR)
        mask = cv2.warpAffine(core, M, (W, H), flags=cv2.INTER_NEAREST) & cv2.erode(m, np.ones((3, 3), np.uint8))
        soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 2.0)[..., None]
        frames[i] = np.clip(frames[i] * (1 - soft) + moved * soft, 0, 255).astype(np.uint8)
        done += 1
vw = cv2.VideoWriter(dst + ".tmp.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
for fr in frames:
    vw.write(fr)
vw.release()
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", dst + ".tmp.mp4", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst], check=True)
os.remove(dst + ".tmp.mp4")
print(f"eyes restored on {done} frames")
