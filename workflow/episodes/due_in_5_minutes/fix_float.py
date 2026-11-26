#!/usr/bin/env python3
"""Put Sol back on the ground when the painter leaves him hanging in the air.

Elaine, 2026-11-26, on the notebook shot of the "Due in 5 Minutes" ad: "sol is floating which goes against nature".
After his hop the painter never brought him down: his feet stayed about 45 px above his own shadow to the end.

Usage (workflow/.venv/bin/python):
  fix_float.py --measure clip.mp4 x,y,w,h              print where his feet are, every quarter second
  fix_float.py clip.mp4 out.mp4 x,y,w,h t_apex t_land  land him: from t_apex he falls, by t_land his feet are back
                                                       on the line they stood on before the hop, and stay there
x,y,w,h is a box (the clip's own pixels) that holds Sol for the whole clip and nothing else red, orange or purple.
Works on a locked-off shot only. Sol is cut out by colour (red, orange and the indigo tint; his face and eyes are
the holes inside), the wall behind him is rebuilt from the frames where he is not in front of it, and he is laid
back in lower down. Nothing outside the box changes. The input file is kept.
"""
import subprocess, sys
import cv2, numpy as np

args = [a for a in sys.argv[1:] if a != "--measure"]
MEASURE = "--measure" in sys.argv
src = args[0]
box = args[1] if MEASURE else args[2]
X, Y, W, H = [int(v) for v in box.split(",")]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
frames = []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    frames.append(fr)


def sol_mask(roi):
    b, g, r = [roi[..., i].astype(int) for i in range(3)]
    warm = (r > 140) & (r - b > 75) & (r >= g)
    purple = (b > 80) & (b > g + 18) & (r > 50)
    core = cv2.morphologyEx((warm | purple).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    k, lab, stats, _ = cv2.connectedComponentsWithStats(core, 8)
    if k < 2:
        return np.zeros_like(core)
    big = 1 + int(np.argmax(stats[1:, 4]))
    m = (lab == big).astype(np.uint8)
    flood = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.floodFill(flood, None, (0, 0), 2)
    return (flood[1:-1, 1:-1] != 2).astype(np.uint8)          # holes filled: his face, eyes and worry lines


masks = [sol_mask(fr[Y:Y + H, X:X + W]) for fr in frames]
feet = np.array([np.where(m.any(axis=1))[0].max() if m.any() else -1 for m in masks], float)
if MEASURE:
    for i in range(0, len(frames), max(int(fps / 4), 1)):
        print(f"{i / fps:5.2f}s  feet at y={Y + feet[i]:.0f}")
    sys.exit(0)

dst, T_APEX, T_LAND = args[1], float(args[3]), float(args[4])
ground = float(np.median(feet[int(0.2 * fps):int((T_APEX - 0.45) * fps)]))       # where he stood before the hop
# the wall behind him: for each pixel, the median of the frames in which he is not in front of it
stack = np.stack([fr[Y:Y + H, X:X + W] for fr in frames]).astype(np.float32)
clear = np.stack([cv2.dilate(m, np.ones((13, 13), np.uint8)) == 0 for m in masks])
count = clear.sum(axis=0)
plate = np.zeros(stack.shape[1:], np.float32)
masked = np.where(clear[..., None], stack, np.nan)
with np.errstate(all="ignore"):
    med = np.nanmedian(masked, axis=0)
plate = np.where((count > 0)[..., None], med, 0).astype(np.uint8)
if (count == 0).any():
    plate = cv2.inpaint(plate, (count == 0).astype(np.uint8) * 255, 5, cv2.INPAINT_TELEA)

h_, w_ = frames[0].shape[:2]
out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w_}x{h_}", "-r", f"{fps}", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
apex = int(round(T_APEX * fps))
moved = 0
for i, fr in enumerate(frames):
    t = i / fps
    if t > T_APEX and masks[i].any():
        u = min((t - T_APEX) / (T_LAND - T_APEX), 1.0)
        want = feet[apex] + (ground - feet[apex]) * u * u                     # he falls: slow at the top, fast at the bottom
        shift = want - feet[i]
        if shift > 0.5:
            roi = fr[Y:Y + H, X:X + W]
            m = masks[i]
            grown = cv2.dilate(m, np.ones((7, 7), np.uint8))
            soft = cv2.GaussianBlur(grown.astype(np.float32), (0, 0), 1.2)[..., None]
            cleared = (roi * (1 - soft) + plate * soft).astype(np.uint8)        # take him out
            M = np.float32([[1, 0, 0], [0, 1, shift]])
            sol = cv2.warpAffine(roi, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            a = cv2.warpAffine(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8), M, (W, H), flags=cv2.INTER_LINEAR)[..., None]
            fr[Y:Y + H, X:X + W] = (cleared * (1 - a) + sol * a).astype(np.uint8)   # put him back, lower
            moved += 1
    out.stdin.write(fr.tobytes())
out.stdin.close()
out.wait()
print(f"{src} -> {dst}: ground line y={Y + ground:.0f}, {moved} of {len(frames)} frames moved, final drop {ground - feet[-1]:.0f} px")
