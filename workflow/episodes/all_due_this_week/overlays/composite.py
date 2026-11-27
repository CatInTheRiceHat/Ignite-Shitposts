#!/usr/bin/env python3
"""Lay the lettering (and the end card) over a painted clip: painted clip in, finished clip out, 1920x1080.

Usage (workflow/.venv/bin/python):  composite.py <clip number> <painted.mp4> <out.mp4> [--shift seconds] [--frame t out.png] [--card art.png]

The painter cannot write words. Every word is drawn once (make_art.py), sits on a plane in the Blender scene
(skeleton/clips.py, OVL_ planes) and is rendered as its own pass in the shot's perspective:
  seq     every lettering plane for EVERY frame, with whatever stands in front of it cut out (render_clip.py
          MODE=ovlseq, overlays/<clip>/seq/). Used wherever the camera or a lettered prop moves.
  stills  one plane alone, from a locked-off shot (MODE=ovl), so it can be written on with a wipe (the whiteboard).
Clip 5 adds the "lights up / dims" of the script from two skeleton masks (MODE=mask with MASKPREFIX): a warm glow
around the math homework, and the other two things darkened. Clip 8 adds the end card, which slides in from the
right over half a second and holds to the end (Elaine's end-card prompt).
--shift moves every overlay time later (+) or earlier (-) if the painted clip drifted from the skeleton.
--frame writes one finished frame as a PNG instead of the clip, for checking.
PLAN times are seconds on the clip's own clock and match skeleton/clips.py.
"""
import json, math, pathlib, subprocess, sys
import cv2, numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE / "art"
W, H = 1920, 1080
PLAN = {
    # clip 1: the painter began Sol plain orange and brought the purple in over the first two thirds of a second. The
    # script starts him "already part purple", so the clip is used from 0.667 s (16 frames in), where he already is.
    "1": {"seq": True, "trim": 16 / 24},
    "2": {"seq": True},
    # clip 3: the paint that kept every prop right (paint v4) left Sol plain orange; the script has him "still purple"
    # here, between the purple of clip 2 and the breathing of clip 4. The tint is laid on his flame top: where the frame
    # is Sol-coloured inside his skeleton silhouette (MODE=mask), fading from his tip down, as the 3D model's shade does.
    "3": {"seq": True, "push": (1.0, 1.035, 0.5, 0.5), "tint": {"mask": "mask.mp4", "reach": 0.6, "strength": 0.85},
          # the painter lifted the homework two frames before the skeleton does: for those two frames the lettering pass
          # of one frame later is used, so "Math homework" stays on its note (nothing else with lettering is moving then)
          "seq_map": {43: 44, 44: 45}},
    "4": {},
    "5": {"seq": True, "lit": {"mask": "mask_lit.mp4", "t0": 1.75, "t1": 2.15}, "dim": {"mask": "mask_dim.mp4", "t0": 1.75, "t1": 2.3, "amount": 0.2},
          "push": (1.0, 1.035, 0.45, 0.5)},
    "6": {"stills": [{"name": "plan_a", "anim": "on"}, {"name": "plan_b", "anim": "wipe", "t0": 2.0, "t1": 2.9}], "push": (1.0, 1.035, 0.45, 0.45)},
    "7": {"seq": True, "push": (1.0, 1.035, 0.45, 0.4)},
    "8": {"seq": True, "seq_until": 1.6, "card": {"art": "end_card.png", "t0": 1.0, "d": 0.5}},
}


def smooth(t, a, b):
    x = min(1.0, max(0.0, (t - a) / (b - a)))
    return x * x * x * (x * (x * 6 - 15) + 10)


def ease_out_back(x, s=1.2):
    x = min(1.0, max(0.0, x)) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


def bump(t, a, b):
    return 0.0 if t <= a or t >= b else math.sin((t - a) / (b - a) * math.pi) ** 2


def load_rgba(path):
    im = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    assert im is not None and im.shape[2] == 4, path
    return im.astype(np.float32) / 255.0


def blend(frame, rgba, x, y, gain=1.0):
    """Alpha-over a float BGRA patch onto the float frame with its top-left at (x, y)."""
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    p = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = p[:, :, 3:4] * gain
    frame[y0:y1, x0:x1] = frame[y0:y1, x0:x1] * (1 - a) + p[:, :, :3] * a


def read_masks(path):
    cap, out = cv2.VideoCapture(str(path)), []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        out.append(fr[:, :, 0])
    return out


def main():
    args = sys.argv[1:]
    shift, single = 0.0, None
    if "--shift" in args:
        i = args.index("--shift")
        shift = float(args[i + 1])
        del args[i:i + 2]
    if "--card" in args:                     # another end card, e.g. --card end_card_web.png (the sign-up address)
        i = args.index("--card")
        PLAN["8"]["card"]["art"] = args[i + 1]
        del args[i:i + 2]
    if "--frame" in args:
        i = args.index("--frame")
        single = (float(args[i + 1]), args[i + 2])
        del args[i:i + 3]
    clip, src = args[0], args[1]
    out = args[2] if len(args) > 2 else None
    plan = PLAN[clip]
    d = HERE / clip
    stills = []
    for s in plan.get("stills", []):
        im = load_rgba(d / f"{s['name']}.png")
        assert im.shape[:2] == (H, W), im.shape
        ys, xs = np.where(im[:, :, 3] > 0.01)
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        stills.append(dict(s, patch=cv2.GaussianBlur(im[y0:y1, x0:x1], (0, 0), 0.6), x=int(x0), y=int(y0)))
    lit = read_masks(d / plan["lit"]["mask"]) if "lit" in plan else None
    dim = read_masks(d / plan["dim"]["mask"]) if "dim" in plan else None
    card = load_rgba(ART / plan["card"]["art"]) if "card" in plan else None
    solmask = read_masks(d / plan["tint"]["mask"]) if "tint" in plan else None

    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    total = max(cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1, 1)
    proc = None
    if single is None:
        proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                                 "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    n = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        t = n / fps
        n += 1
        if single is not None and abs(t - single[0]) > 0.5 / fps:
            continue
        if single is None and t < plan.get("trim", 0.0) - 1e-6:      # frames cut off the head of the clip
            continue
        frame = cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32) / 255.0
        ts = t - shift
        ns = max(1, int(round(ts * fps)) + 1)                    # the skeleton frame that belongs to this moment
        if solmask is not None:                                  # the purple shade on the top of his flame
            m = cv2.resize(solmask[min(ns, len(solmask)) - 1], (W, H), interpolation=cv2.INTER_LINEAR)
            ys = np.where(m.max(axis=1) > 128)[0]
            if len(ys):
                y0, hh = ys[0], ys[-1] - ys[0] + 1
                grad = np.clip(1.0 - (np.arange(H, dtype=np.float32) - (y0 - 0.04 * hh)) / (plan["tint"]["reach"] * hh), 0, 1) ** 0.85
                near = cv2.dilate(m, np.ones((61, 61), np.uint8)).astype(np.float32) / 255.0
                b_, g_, r_ = frame[..., 0], frame[..., 1], frame[..., 2]
                warm = ((r_ > b_ + 0.14) & (r_ > 0.45)).astype(np.float32)            # Sol's reds, oranges and cream, not the wall
                a = cv2.GaussianBlur(warm * near, (0, 0), 2.5) * grad[:, None] * plan["tint"]["strength"]
                luma = (0.114 * b_ + 0.587 * g_ + 0.299 * r_)[..., None]
                indigo = np.float32([0.74, 0.22, 0.31]) * (0.5 + 0.95 * luma)           # BGR, keeps the painted shading
                frame = frame * (1 - a[..., None]) + np.clip(indigo, 0, 1) * a[..., None]
        if dim is not None:                                      # the other two things go dull
            k = smooth(ts, plan["dim"]["t0"], plan["dim"]["t1"])
            if k > 0:
                m = cv2.resize(dim[min(ns, len(dim)) - 1], (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255.0
                m = cv2.GaussianBlur(cv2.dilate(m, np.ones((9, 9), np.uint8)), (0, 0), 7)[..., None] * k
                gray = frame.mean(axis=2, keepdims=True)
                frame = frame * (1 - m) + (0.7 * frame + 0.3 * gray) * (1 - plan["dim"]["amount"]) * m
        if lit is not None:                                      # the homework lights up
            k = smooth(ts, plan["lit"]["t0"], plan["lit"]["t1"])
            if k > 0:
                m = cv2.resize(lit[min(ns, len(lit)) - 1], (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255.0
                halo = cv2.GaussianBlur(cv2.dilate(m, np.ones((41, 41), np.uint8)), (0, 0), 46)
                pulse = 1.0 + 0.12 * math.sin((ts - plan["lit"]["t1"]) * 5.0) * (ts > plan["lit"]["t1"])
                frame = frame + (halo * (1 - 0.9 * cv2.dilate(m, np.ones((15, 15), np.uint8))))[..., None] * np.float32([0.30, 0.72, 1.0]) * 0.5 * k * pulse
                frame = frame * (1 + 0.05 * k * cv2.GaussianBlur(m, (0, 0), 3)[..., None])
        if plan.get("seq") and ts <= plan.get("seq_until", 1e9):
            f_seq = d / "seq" / f"f_{plan.get('seq_map', {}).get(ns, ns):04d}.png"
            if f_seq.exists():
                blend(frame, cv2.GaussianBlur(load_rgba(f_seq), (0, 0), 0.6), 0, 0, 0.95)
        for s in stills:
            p, x, y, gain = s["patch"], s["x"], s["y"], 0.95
            if s["anim"] == "wipe":                               # written on, left to right
                k = smooth(ts, s["t0"], s["t1"])
                if k <= 0:
                    continue
                w = p.shape[1]
                soft = 0.12 * w
                ramp = np.clip((k * (w + soft) - np.arange(w, dtype=np.float32)) / soft, 0, 1)
                p = p.copy()
                p[:, :, 3] *= ramp[None, :]
            blend(frame, p, x, y, gain)
        if "push" in plan:                                       # a slow editorial push on a locked-off shot
            z0, z1, px, py = plan["push"]
            z = z0 + (z1 - z0) * (n - 1) / total
            M = np.float32([[z, 0, (1 - z) * px * W], [0, z, (1 - z) * py * H]])
            frame = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        if card is not None:                                     # the end card: in from the right, then it holds
            k = ease_out_back((ts - plan["card"]["t0"]) / plan["card"]["d"]) if ts > plan["card"]["t0"] else 0.0
            if k > 0:
                blend(frame, card, int(round((1 - k) * 1300)), 0)
        out8 = (np.clip(frame, 0, 1) * 255 + 0.5).astype(np.uint8)
        if single is not None:
            cv2.imwrite(single[1], out8)
            print("wrote", single[1], "t =", round(t, 3))
            return
        proc.stdin.write(out8.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"clip {clip}: {n} frames at {fps:.0f} fps -> {out}")


if __name__ == "__main__":
    main()
