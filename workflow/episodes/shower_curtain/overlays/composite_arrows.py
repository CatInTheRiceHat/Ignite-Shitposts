#!/usr/bin/env python3
"""Lay the rendered airflow arrows over a painted clip.   (run with workflow/.venv/bin/python)

Usage: composite_arrows.py painted.mp4 arrows_dir out.mp4 [fill "r,g,b" 0-255, default white]
Each arrow gets the fill colour and a navy outline, like the painted emotion marks. Frame i of the painted clip takes
arrows_dir/a_%04d.png (i+1); painted frames past the last arrow frame are left as they are. The output is never an
existing file."""
import sys, pathlib, subprocess, tempfile, shutil
import cv2, numpy as np

src, adir, out = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
fill = np.array([float(v) for v in (sys.argv[4] if len(sys.argv) > 4 else "255,255,255").split(",")][::-1])     # BGR
if out.exists():
    sys.exit(f"{out} exists")
NAVY = np.array([71.0, 36.0, 28.0])
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="arw_"))
ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
i = 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    i += 1
    a = cv2.imread(str(adir / f"a_{i:04d}.png"), cv2.IMREAD_UNCHANGED)
    if a is not None and a.shape[2] == 4 and a[..., 3].max() > 0:
        al = cv2.GaussianBlur(a[..., 3].astype(np.float32) / 255.0, (0, 0), 0.8)
        ol = cv2.GaussianBlur(cv2.dilate((al > 0.35).astype(np.float32), ker), (0, 0), 1.0) * 0.92
        f = fr.astype(np.float32)
        f = f * (1 - ol[..., None]) + NAVY * ol[..., None]
        f = f * (1 - al[..., None]) + fill * al[..., None]
        fr = np.clip(f, 0, 255).astype(np.uint8)
    cv2.imwrite(str(tmp / f"f_{i:04d}.png"), fr)
subprocess.check_call(["ffmpeg", "-v", "error", "-framerate", f"{fps:g}", "-i", str(tmp / "f_%04d.png"),
                       "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(out)])
shutil.rmtree(tmp)
print("wrote", out, i, "frames")
