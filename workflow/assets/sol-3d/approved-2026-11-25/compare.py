#!/usr/bin/env python3
"""Check the 3D Sol against Mascot.png. Writes sol-turnaround.png, sol-vs-mascot.png and sol-legs-check.png.

The front render is orthographic at a known scale, so the mascot art can be laid over it exactly.
sol-legs-check.png shows, enlarged: the mascot's legs, the model's legs, and the model with the
mascot's outline drawn on top in cyan. Where the cyan line hugs the model, the shapes match.
"""
import numpy as np, pathlib, subprocess
from PIL import Image, ImageFilter

H = pathlib.Path(__file__).resolve().parent
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "sol-front.png", "-i", "sol-three-quarter.png", "-i", "sol-side.png",
                "-i", "sol-back.png", "-filter_complex", "hstack=inputs=4,scale=2400:-1", "-update", "1",
                "sol-turnaround.png"], cwd=H, check=True)
BG = (236, 236, 236)
m = Image.open(H.parent / "reference-art" / "Mascot.png").convert("RGBA")
alpha = np.array(m)[..., 3] > 128
ys, xs = np.where(alpha)
cx, y1, MH = (xs.min() + xs.max()) / 2, ys.max(), ys.max() - ys.min() + 1
PPU = 800 / 1.3                                      # render pixels per unit (ortho scale 1.3 at 800 px)
k = PPU / MH
ms = m.resize((round(m.width * k), round(m.height * k)), Image.LANCZOS)
ox, oy = round(400 - cx * k), round(400 + 0.5 * PPU - (y1 + 1) * k)     # mascot's feet line on the model's ground
ref = Image.new("RGBA", (800, 800), BG + (255,))
ref.alpha_composite(ms, (ox, oy))
model = Image.open(H / "sol-front.png").convert("RGB")
a = np.array(ref)[..., :3]
sil = np.zeros((800, 800), bool)
sa = np.array(ms)[..., 3] > 128
sil[max(oy, 0):oy + sa.shape[0], max(ox, 0):ox + sa.shape[1]] = sa[max(-oy, 0):800 - oy, max(-ox, 0):800 - ox]
edge = sil & ~(np.roll(sil, 1, 0) & np.roll(sil, -1, 0) & np.roll(sil, 1, 1) & np.roll(sil, -1, 1))
over = np.array(model).copy()
over[edge] = (0, 200, 255)
side = Image.new("RGB", (1600, 800), BG)
side.paste(ref.convert("RGB"), (0, 0))
side.paste(model, (800, 0))
side.save(H / "sol-vs-mascot.png")
box = (230, 620, 570, 730)                           # the legs
tiles = [im.crop(box).resize((1020, 330), Image.LANCZOS) for im in (ref.convert("RGB"), model, Image.fromarray(over))]
chk = Image.new("RGB", (1020, 990), BG)
for i, t in enumerate(tiles):
    chk.paste(t, (0, 330 * i))
chk.save(H / "sol-legs-check.png")
Image.fromarray(over).save(H / "sol-outline-check.png")
ren = np.abs(np.array(model).astype(int) - np.array(BG)).sum(2) > 40
print("silhouette mismatch in the legs box: %.1f%% of pixels" % (100 * (ren ^ sil)[box[1]:box[3], box[0]:box[2]].mean()))
