#!/usr/bin/env python3
"""Paint out a mouth the painter drew on Sol (he has none, ever), found from his EYES. For clip 7, paint v6 (2026-11-27):
an open one for half a second while he flaps his nubs.

Usage (workflow/.venv/bin/python): fix_mouth_below_eyes.py <in.mp4> <out.mp4> x0 y0 x1 y1 first_frame last_frame
The box (in the clip's own pixels) holds his face and no other Sol's. In each frame from first_frame to last_frame his two
navy eyes are found in the box; anything dark red or pink in the narrow patch of face just under and between them is a
mouth, and is filled in from the cream around it. Other frames pass through untouched.
fix_mouth.py (clip 4b) looks for a hole walled in by cream; that fails here, where his face is turned and its shaded
side and the sand count as cream too.
"""
import subprocess, sys
import cv2, numpy as np

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1, first, last = map(int, sys.argv[3:9])
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 24
w, h = int(cap.get(3)), int(cap.get(4))
out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n, fixed = 0, []
while True:
    ok, fr = cap.read()
    if not ok:
        break
    n += 1
    if first <= n <= last:
        roi = fr[y0:y1, x0:x1]
        b, g, r = (roi[..., i].astype(int) for i in range(3))
        navy = ((r < 135) & (g < 130) & (b < 180) & (b >= r)).astype(np.uint8)
        k, _, st, cen = cv2.connectedComponentsWithStats(navy)
        # an eye is a small compact blob; the brown motion lines beside his nubs are long thin arcs
        eyes = sorted((j for j in range(1, k) if st[j][4] >= 8 and st[j][2] <= 24 and st[j][3] <= 30 and st[j][4] >= 0.4 * st[j][2] * st[j][3]),
                      key=lambda j: -st[j][4])[:2]
        if len(eyes) == 2:
            (ax, ay), (bx, by) = cen[eyes[0]], cen[eyes[1]]
            gap = abs(ax - bx)
            # The window is the patch of face BETWEEN the eyes and just under them, and nothing else. His face is turned, so
            # its orange rim comes close on one side; a wider or deeper window took that in and smeared his chin.
            lx, rx = min(ax, bx), max(ax, bx)
            ex0, ex1 = int(lx + 0.1 * gap), int(rx - 0.05 * gap)
            ey0, ey1 = int(max(ay, by) + 0.08 * gap), int(max(ay, by) + 0.85 * gap)
            win = np.zeros(navy.shape, np.uint8)
            win[max(0, ey0):ey1, max(0, ex0):ex1] = 1
            # the inside of the opening is dark (r under 172, g under 110) or pink (b high for its g); cream has g over 150
            mouth = (win == 1) & (((r < 172) & (g < 112)) | ((g < 140) & (b > 0.62 * g) & (r > g + 40))) & (navy == 0)
            if mouth.sum() > 12:
                m = cv2.dilate(mouth.astype(np.uint8), np.ones((5, 5), np.uint8)) & cv2.dilate(win, np.ones((7, 7), np.uint8)) & (1 - cv2.erode(cv2.dilate(navy, np.ones((3, 3), np.uint8)), np.ones((3, 3), np.uint8)))
                fr[y0:y1, x0:x1] = cv2.inpaint(roi, m, 4, cv2.INPAINT_TELEA)
                fixed.append(n)
    out.stdin.write(fr.tobytes())
out.stdin.close()
out.wait()
print(f"{n} frames; mouth painted out in {len(fixed)}: {fixed[:1]} to {fixed[-1:]}")
