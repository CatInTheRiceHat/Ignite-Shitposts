#!/usr/bin/env python3
"""Paint out a mouth the painter added to Sol. Sol is mouthless (Elaine, 2026-11-25).

Usage: remove_mouth.py <frames_in_dir> <frames_out_dir> x0 y0 x1 y1
Inside the box (where Sol's face is), a reddish patch enclosed by his cream face, sitting just below
and between his two navy eyes, is a mouth: it is filled with the surrounding cream. His navy eyes are left alone. Frames with no mouth pass through
unchanged. Prints which frames were repaired.
"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
x0, y0, x1, y1 = map(int, sys.argv[3:7])
fixed = []
for f in sorted(src.glob("*.png")):
    im = Image.open(f).convert("RGB")
    a = np.array(im).astype(int)
    roi = a[y0:y1, x0:x1]
    R, G, B = roi[..., 0], roi[..., 1], roi[..., 2]
    cream = (R > 215) & (G > 185) & (B > 120) & (R - B < 130)
    outside = np.zeros(cream.shape, bool)              # flood the non-cream area in from the box edges
    outside[0, :] = ~cream[0, :]; outside[-1, :] = ~cream[-1, :]
    outside[:, 0] = ~cream[:, 0]; outside[:, -1] = ~cream[:, -1]
    while True:
        grow = outside.copy()
        grow[1:, :] |= outside[:-1, :]; grow[:-1, :] |= outside[1:, :]
        grow[:, 1:] |= outside[:, :-1]; grow[:, :-1] |= outside[:, 1:]
        grow &= ~cream
        if (grow == outside).all():
            break
        outside = grow
    enclosed = ~cream & ~outside                       # eyes, and a mouth if there is one
    eyes = enclosed & (B > R + 15) & (R < 110)         # his two navy eyes
    mouth = enclosed & (R > B + 25)                    # reddish, unlike the navy eyes
    ok = False
    if eyes.sum() > 60:
        ey, ex = np.where(eyes)
        gap = max(ex.max() - ex.min(), 20)             # eye-to-eye span sets the scale of his face
        zone = np.zeros(mouth.shape, bool)             # a mouth can only be just below and between his eyes
        zone[int(ey.mean()):ey.max() + int(1.3 * gap), max(0, ex.min() - gap // 3):ex.max() + gap // 3] = True   # from eye level down
        ok = (mouth & zone).sum() >= 60                # a real reddish mouth is there
        guard = eyes.copy()                            # keep well clear of the eyes themselves
        for _ in range(4):
            g = guard.copy()
            g[1:, :] |= guard[:-1, :]; g[:-1, :] |= guard[1:, :]; g[:, 1:] |= guard[:, :-1]; g[:, :-1] |= guard[:, 1:]
            guard = g
        mouth = enclosed & zone & ~guard               # then take everything non-cream there: lips, outline, teeth
    if not ok:
        im.save(dst / f.name)
        continue
    for _ in range(5):                                 # take the soft edge of the mouth too, but never the eyes
        m = mouth.copy()
        m[1:, :] |= mouth[:-1, :]; m[:-1, :] |= mouth[1:, :]; m[:, 1:] |= mouth[:, :-1]; m[:, :-1] |= mouth[:, 1:]
        mouth = m & ~guard & (cream | enclosed)        # never spill past his cream face into the orange
    src_ok = cream & ~mouth
    fill = np.zeros(roi.shape)
    w = np.array(Image.fromarray((src_ok * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(14))).astype(float) + 1e-6
    for c in range(3):
        ch = np.array(Image.fromarray((roi[..., c] * src_ok).astype(np.uint8)).filter(ImageFilter.BoxBlur(14))).astype(float)
        fill[..., c] = ch / w * 255
    out = roi.copy()
    out[mouth] = fill[mouth]
    soft = np.array(Image.fromarray((mouth * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)[..., None] / 255
    a[y0:y1, x0:x1] = (roi * (1 - soft) + out * soft).round()
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(dst / f.name)
    fixed.append(f.stem)
print("repaired", len(fixed), "frames:", fixed[0] if fixed else "-", "to", fixed[-1] if fixed else "-")
