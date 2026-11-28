#!/usr/bin/env python3
"""Draw the airflow arrows over a painted clip as clean 2D shapes.   (run with workflow/.venv/bin/python)

Usage: draw_arrows.py painted.mp4 arrows2-N.json out.mp4
The json comes from skeleton/export_arrows.py: for every frame, each arrow's path on screen from tail to head.
Each arrow is one smooth filled shape (a tapering body that bends along its path, and a head), drawn at 3x size and
scaled down so its edges are soft, with a navy outline like the painted emotion marks. Arrows fade, they never pop.
Each arrow carries its own colour ("rgb", 0-255) and width limits ("clamp", px at 720 wide), so a light ray can dim
from gold to bronze as it loses energy (wet-shirt episode, 2026-11-27). The output is never an existing file."""
import sys, json, pathlib, subprocess, tempfile, shutil
import cv2, numpy as np

src, spec, out = sys.argv[1], json.loads(pathlib.Path(sys.argv[2]).read_text()), pathlib.Path(sys.argv[3])
if out.exists():
    sys.exit(f"{out} exists")
SS = 3
NAVY = np.array([71.0, 36.0, 28.0])                                          # BGR of #1C2447
EDGE = 3.2                                                                   # outline in px


def shape(pts, w):
    """Outline polygon of an arrow along pts (tail -> tip), body width w."""
    p = np.asarray(pts, dtype=np.float64)
    seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
    L = seg.sum()
    if L < 8:
        return None
    w = min(w, L / 3.4)
    s = np.concatenate([[0], np.cumsum(seg)])
    q = np.stack([np.interp(np.linspace(0, L, 40), s, p[:, i]) for i in (0, 1)], axis=1)      # even steps along the path
    hl = 2.3 * w                                                             # head length
    d = np.linspace(0, L, 40)
    body = q[d <= L - hl]
    if len(body) < 2:
        body = q[:2]
    tang = np.gradient(body, axis=0)
    tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9
    nor = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
    half = (0.5 * w * (0.62 + 0.38 * np.linspace(0, 1, len(body))))[:, None]                 # a little thinner at the tail
    neck, tip = body[-1], q[-1]
    hd = tip - neck
    hd /= np.linalg.norm(hd) + 1e-9
    hn = np.array([-hd[1], hd[0]])
    tip = neck + hd * hl
    return np.concatenate([body + nor * half, [neck + hn * 1.25 * w, tip, neck - hn * 1.25 * w], (body - nor * half)[::-1]])


cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = spec["size"]
tmp = pathlib.Path(tempfile.mkdtemp(prefix="arw_"))
r = int(round(EDGE * SS))
ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
i = 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    row = spec["frames"][i] if i < len(spec["frames"]) else []
    i += 1
    if row:
        f = fr.astype(np.float32)
        for a in sorted(row, key=lambda a: a["px"]):                         # far (small) ones first
            lo, hi = a.get("clamp", (12, 30))
            poly = shape(a["pts"], float(np.clip(a["px"], lo, hi)))
            if poly is None:
                continue
            x0, y0 = np.floor(poly.min(axis=0)).astype(int) - 12
            x1, y1 = np.ceil(poly.max(axis=0)).astype(int) + 12
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
            if x1 <= x0 or y1 <= y0:
                continue
            m = np.zeros(((y1 - y0) * SS, (x1 - x0) * SS), np.uint8)
            cv2.fillPoly(m, [np.round((poly - (x0, y0)) * SS * 16).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=4)
            o = cv2.dilate(m, ker)
            m = cv2.resize(m, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255 * a["alpha"]
            o = cv2.resize(o, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255 * a["alpha"]
            roi = f[y0:y1, x0:x1]
            roi[:] = roi * (1 - o) + NAVY * o
            roi[:] = roi * (1 - m) + np.array(a["rgb"][::-1], dtype=np.float64) * m
        fr = np.clip(f, 0, 255).astype(np.uint8)
    cv2.imwrite(str(tmp / f"f_{i:04d}.png"), fr)
subprocess.check_call(["ffmpeg", "-v", "error", "-framerate", f"{fps:g}", "-i", str(tmp / "f_%04d.png"),
                       "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(out)])
shutil.rmtree(tmp)
print("wrote", out, i, "frames")
