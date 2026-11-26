#!/usr/bin/env python3
"""Step 1 of the 3D Sol: trace Logo.png (Sol's body without legs) and inflate it. Writes sol-inflate.npz and the two textures.

Elaine's method (2026-11-25): trace over the mascot outline, then inflate it. The outline is the real
alpha edge of Logo.png, which Elaine picked because it is the body with no legs. Inflating solves laplace(h) = -1 inside the outline with h = 0 on it and takes
depth = sqrt(h), which swells thick parts into a round belly and keeps the flame tip and tufts slim.
The legs are not inflated: they are added as separate round nubs in Blender, at Mascot.png's positions.
"""
import numpy as np, pathlib
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "reference-art" / "Logo.png"
a = np.array(Image.open(SRC).convert("RGBA"))
alpha = a[..., 3]
mask = alpha > 128
ys, xs = np.where(mask)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
BODY_SHARE, FOOT_Z = 0.935, 0.065                 # measured in Mascot.png: body is 93.5% of his height, its underside sits 6.5% up
H = (y1 - y0 + 1) / BODY_SHARE                    # pixels per unit, so that body + feet = 1.0 tall
cx = (x0 + x1) / 2
body_bottom = y1
body = mask


def runs(row):
    d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0] - 1))


def solve(m, h, iters):
    for _ in range(iters):
        h = np.where(m, (np.roll(h, 1, 0) + np.roll(h, -1, 0) + np.roll(h, 1, 1) + np.roll(h, -1, 1) + 1) / 4, 0)
    return h


def grid(step):
    gx = np.arange(x0 - step * 4, x1 + step * 5, step)
    gy = np.arange(y0 - step * 4, body_bottom + step * 5, step)
    return gx, gy, body[np.ix_(gy.clip(0, a.shape[0] - 1), gx.clip(0, a.shape[1] - 1))]


gx2, gy2, m2 = grid(12)                            # coarse solve first, then refine
h2 = solve(m2, np.zeros(m2.shape), 12000)
gx, gy, m = grid(4)
h = np.kron(h2, np.ones((3, 3)))[:m.shape[0], :m.shape[1]] * 9
h = np.pad(h, ((0, max(0, m.shape[0] - h.shape[0])), (0, max(0, m.shape[1] - h.shape[1]))))
h = solve(m, np.where(m, h, 0), 14000)
d = np.sqrt(h)
d *= 0.31 / d.max()                                # half depth: about 0.62 deep for a body 0.81 wide
# ---- legs: read their exact outline off Mascot.png, row by row (no guessing, no reshaping) ----
ma = np.array(Image.open(HERE.parent / "reference-art" / "Mascot.png").convert("RGBA"))[..., 3] > 128
mys, mxs = np.where(ma)
m_y0, m_y1, m_cx = mys.min(), mys.max(), (mxs.min() + mxs.max()) / 2
MH = m_y1 - m_y0 + 1                              # the mascot's full height in pixels = 1.0 unit
split = min(y for y in range(m_y1 - 200, m_y1 + 1) if len(runs(ma[y])) == 2)      # first row where the two legs separate
leg_d, leg_r, leg_cx = [], [], []
for y in range(m_y1, split - 1, -1):
    rr = runs(ma[y])
    if len(rr) == 2:
        s0, e0 = rr[1]                             # the right leg
        leg_d.append((m_y1 + 0.5 - y) / MH)
        leg_r.append((e0 - s0 + 1) / 2 / MH)
        leg_cx.append(((s0 + e0) / 2 - m_cx) / MH)
leg_d, leg_r = np.array(leg_d), np.array(leg_r)
leg_x = float(np.mean(leg_cx[len(leg_cx) // 2:]))
print("leg: visible length", round(float(leg_d[-1]), 4), "top half-width", round(float(leg_r[-1]), 4), "centre x", round(leg_x, 4))
np.savez(HERE / "sol-inflate.npz", M=m, depth=d, leg_d=leg_d, leg_r=leg_r, leg_x=leg_x, X=(gx - cx) / H, Z=(y1 - gy) / H + FOOT_Z, gx=gx, gy=gy,
         size=np.array(a.shape[:2]), feet=np.array([[-0.134, 0.116], [0.134, 0.116]]), body_bottom=FOOT_Z)

rgb = a[..., :3].astype(np.float32)
have = alpha > 250
for _ in range(7):                                 # drop the art's soft brownish edge fringe: only clean interior
    have &= np.roll(have, 1, 0) & np.roll(have, -1, 0) & np.roll(have, 1, 1) & np.roll(have, -1, 1)   # colour spreads outward
acc, cnt = np.where(have[..., None], rgb, 0), have.astype(np.float32)
for _ in range(70):                                # bleed edge colours outward so the rim never samples transparency
    s, n = np.zeros_like(acc), np.zeros_like(cnt)
    for ax, sh in ((0, 1), (0, -1), (1, 1), (1, -1)):
        s += np.roll(acc * cnt[..., None], sh, ax)
        n += np.roll(cnt, sh, ax)
    new = (cnt == 0) & (n > 0)
    acc[new] = s[new] / n[new][:, None]
    cnt[new] = 1
front = np.where(cnt[..., None] > 0, acc, np.array([196, 58, 44], np.float32)).astype(np.uint8)
Image.fromarray(front).save(HERE / "sol-front-texture.png")
# Back texture: plain body red. It copies the front's colours in a thin band along the outline and lets
# them flow smoothly across the middle, so front and back match where they meet and there is no seam.
small = Image.fromarray(front).resize((a.shape[1] // 4, a.shape[0] // 4), Image.LANCZOS)
sm = np.array(small).astype(np.float32)
msk = np.array(Image.fromarray((mask * 255).astype(np.uint8)).resize(small.size, Image.LANCZOS)) > 128
core = msk.copy()
for _ in range(9):                                 # seed = a thin band just inside the outline (the rim's own red)
    core &= np.roll(core, 1, 0) & np.roll(core, -1, 0) & np.roll(core, 1, 1) & np.roll(core, -1, 1)
seed = msk & ~core
inner = core.copy()
for _ in range(3):
    inner |= np.roll(inner, 1, 0) | np.roll(inner, -1, 0) | np.roll(inner, 1, 1) | np.roll(inner, -1, 1)
seed &= ~inner | seed                              # keep the whole band
acc = np.where(seed[..., None], sm, sm[seed].mean(0))
for _ in range(3000):                              # smooth harmonic fill: the rim colours flow evenly across the back
    avg = (np.roll(acc, 1, 0) + np.roll(acc, -1, 0) + np.roll(acc, 1, 1) + np.roll(acc, -1, 1)) / 4
    acc = np.where(seed[..., None], sm, avg)
back = Image.fromarray(acc.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
back.resize((a.shape[1], a.shape[0]), Image.BICUBIC).save(HERE / "sol-back-texture.png")
print("grid", m.shape, "max half depth", float(d.max()))
