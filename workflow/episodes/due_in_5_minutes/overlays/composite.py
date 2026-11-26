#!/usr/bin/env python3
"""Lay the lettering over a painted clip: painted clip in, finished clip out (1080x1920, same frame rate).

Usage (workflow/.venv/bin/python):  composite.py <clip number> <painted.mp4> <out.mp4> [--shift seconds] [--frame t out.png]

Why: the painter cannot write words, and every piece Sol makes in clips 3 to 7 has to be the same piece on the
finished poster. So the words are drawn once (make_art.py), placed in the Blender scene on the real surfaces
(skeleton/clips.py, OVL_ planes), rendered alone in the shot's own perspective (render_clip.py MODE=ovl), and laid
over the painted clip here. Pop-up labels (clips 4 and 5) are flat cards pinned to a point of the scene
(anchors.json). Where Sol stands in front of lettering (clips 8 and 9) his silhouette from the skeleton
(MODE=mask), grown a little, keeps the lettering behind him.
--shift moves every overlay time later (+) or earlier (-) if the painted clip drifted from the skeleton.
--frame writes one finished frame as a PNG instead of the clip, for checking.
PLAN times are seconds on the clip's own clock and match skeleton/clips.py.
"""
import json, math, pathlib, subprocess, sys
import cv2, numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE / "art"
W, H = 1080, 1920
POSTER = ["title", "changed", "measured", "trial1", "trial2", "trial3", "graph", "wrong"]
# The blue card and the green tags are drawn only where the painted clip shows blue or green card: a per-pixel test
# of what is actually in front, so Sol's painted edge hides them cleanly (the skeleton silhouette alone left ghosts
# of letters on his flame in cut v1).
KEYS = {"measured": {"key": "blue"}, "trial1": {"key": "green"}, "trial2": {"key": "green"}, "trial3": {"key": "green"}}
PLAN = {
    "1": {"push": (1.0, 1.04, 0.1, 0.45)},        # pushes toward Sol, who stands at the left edge
    "2": {},
    "3": {"stills": [{"name": "title", "anim": "wipe", "t0": 1.52, "t1": 2.4, "pulse": [4.38]}], "push": (1.0, 1.04, 0.5, 0.36)},
    "4": {"cards": [{"art": "card_changed.png", "x": 255, "y": 405, "w": 400, "rot": -4, "t0": 1.9},
                    {"art": "card_measured.png", "x": 845, "y": 395, "w": 400, "rot": 3, "t0": 3.3}]},
    "5": {"cards": [{"art": "tag_trial1.png", "anchor": "trial1", "w": 215, "rot": -3, "t0": 1.7},
                    {"art": "tag_trial2.png", "anchor": "trial2", "w": 215, "rot": 2, "t0": 2.0},
                    {"art": "tag_trial3.png", "anchor": "trial3", "w": 215, "rot": -2, "t0": 2.3}], "push": (1.0, 1.03, 0.08, 0.4)},
    "6": {"stills": [{"name": "graph", "anim": "fade", "t0": 3.0, "t1": 3.4}], "push": (1.0, 1.04, 0.5, 0.34)},
    "7": {"stills": [{"name": "wrong", "anim": "wipe", "t0": 1.95, "t1": 2.65, "dx": 18}], "push": (1.0, 1.04, 0.6, 0.45)},
    # clip 8 (from cut v6): the camera travels across the poster, so its lettering is a pass rendered for EVERY frame
    # (render_clip.py MODE=ovlseq, overlays/8/seq/). Sol stands clear of all lettering in this shot: nothing is cut
    # out around him, which is where the flicker beside him in the earlier wide shot came from.
    "8": {"seq": True, "seq_clear_top": (6.3, 0.245),
          # the painter drew Sol smaller and lower at the end than the skeleton has him, which put the captions right
          # under his eyes: a push-in on him as the camera arrives lifts his face clear of the caption band
          "reframe": {"t0": 5.9, "t1": 7.1, "z": 1.3, "cx": 0.40, "cy": 0.92}, "ui": [{"art": "course_card.png", "x": 540, "y": 330, "w": 880, "t0": 1.6}]},
    # clip 9: the header board is behind the course card, so its lettering is left off (a sliver would peek out)
    "9": {"stills": [dict({"name": n, "anim": "on"}, **KEYS.get(n, {})) for n in POSTER if n != "title"], "mask": True, "push": (1.0, 1.03, 0.4, 0.45),
          "ui": [{"art": "course_card.png", "x": 540, "y": 330, "w": 880, "t0": -9}]},
}
INK = {"title", "graph", "wrong"}          # lettering written straight on a painted surface: a touch see-through


def smooth(t, a, b):
    x = min(1.0, max(0.0, (t - a) / (b - a)))
    return x * x * x * (x * (x * 6 - 15) + 10)


def pop(t, start, d=0.28):
    if t <= start:
        return 0.0
    u = (t - start) / d
    return 1.0 - math.exp(-5.5 * u) * math.cos(u * 6.0) if u < 4 else 1.0


def bump(t, a, b):
    return 0.0 if t <= a or t >= b else math.sin((t - a) / (b - a) * math.pi) ** 2


def load_rgba(path):
    im = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    assert im is not None and im.shape[2] == 4, path
    return im.astype(np.float32) / 255.0


def blend(frame, rgba, x, y, gain=1.0, keep=None):
    """Alpha-over a float BGRA patch onto the float frame with its top-left at (x, y). keep: per-pixel 0..1 that
    multiplies the patch's alpha (the area NOT hidden behind Sol)."""
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    p = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = p[:, :, 3:4] * gain
    if keep is not None:
        a = a * keep[y0:y1, x0:x1, None]
    frame[y0:y1, x0:x1] = frame[y0:y1, x0:x1] * (1 - a) + p[:, :, :3] * a


def scaled(rgba, k, rot=0.0):
    """The patch scaled by k about its centre (and turned rot degrees), on a canvas big enough to hold it."""
    h, w = rgba.shape[:2]
    pad = int(max(w, h) * 0.25)
    M = cv2.getRotationMatrix2D((w / 2 + pad, h / 2 + pad), rot, k)
    big = cv2.copyMakeBorder(rgba, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
    return cv2.warpAffine(big, M, (w + 2 * pad, h + 2 * pad), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0)), pad


def main():
    args = sys.argv[1:]
    shift, single = 0.0, None
    if "--shift" in args:
        i = args.index("--shift")
        shift = float(args[i + 1])
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
        if len(xs) == 0:                                   # this piece is outside the frame in this shot
            continue
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        patch = cv2.GaussianBlur(im[y0:y1, x0:x1], (0, 0), 0.6)
        if s.get("scale"):                                 # shrink about the piece's own centre
            k = s["scale"]
            small = cv2.resize(patch, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
            x0 += (patch.shape[1] - small.shape[1]) // 2
            y0 += (patch.shape[0] - small.shape[0]) // 2
            patch = small
        stills.append(dict(s, patch=patch, x=int(x0) + s.get("dx", 0), y=int(y0) + s.get("dy", 0), gain=0.93 if s["name"] in INK else 1.0))
    anchors = json.loads((d / "anchors.json").read_text()) if (d / "anchors.json").exists() else {}
    cards = []
    for group, masked in (("cards", False), ("ui", False)):
        for c in plan.get(group, []):
            im = load_rgba(ART / c["art"])
            k = c["w"] / im.shape[1]
            im = cv2.resize(im, (c["w"], int(round(im.shape[0] * k))), interpolation=cv2.INTER_AREA)
            cx, cy = (c["x"], c["y"]) if "x" in c else (anchors[c["anchor"]][0] + c.get("dx", 0), anchors[c["anchor"]][1] + c.get("dy", 0))
            cards.append(dict(c, im=im, cx=cx, cy=cy, group=group))
    masks = []
    if plan.get("mask"):
        cap = cv2.VideoCapture(str(d / "mask.mp4"))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))          # at 540 wide: grows Sol by about 12 px at 1080
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            m = cv2.dilate(fr[:, :, 0], kernel)
            masks.append(cv2.GaussianBlur(m, (0, 0), 1.0))

    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
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
        frame = cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32) / 255.0
        ts = t - shift
        keep = None
        if masks:
            m = masks[min(int(round(ts * 30)), len(masks) - 1)]
            keep = 1.0 - cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255.0
        b_, g_, r_ = frame[..., 0], frame[..., 1], frame[..., 2]
        keys = {"blue": ((b_ > r_ + 0.05) & (b_ > 0.55)), "green": ((g_ > r_ + 0.03) & (g_ > b_ + 0.03) & (g_ > 0.55))}
        keys = {k_: cv2.GaussianBlur(cv2.erode(v.astype(np.float32), np.ones((3, 3), np.uint8)), (0, 0), 0.8) for k_, v in keys.items()} if any(s.get("key") for s in stills) else {}
        for s in stills:
            p, x, y, gain = s["patch"], s["x"], s["y"], s["gain"]
            keep_s = keep if not s.get("key") else (keys[s["key"]] if keep is None else keep * keys[s["key"]])
            if s["anim"] == "fade":
                gain *= smooth(ts, s["t0"], s["t1"])
            elif s["anim"] == "wipe":                      # written on, left to right
                k = smooth(ts, s["t0"], s["t1"])
                if k <= 0:
                    continue
                w = p.shape[1]
                soft = 0.12 * w
                ramp = np.clip((k * (w + soft) - np.arange(w, dtype=np.float32)) / soft, 0, 1)
                p = p.copy()
                p[:, :, 3] *= ramp[None, :]
            if gain <= 0:
                continue
            pulse = sum(bump(ts, a - 0.1, a + 0.3) for a in s.get("pulse", []))
            if pulse > 0:
                p, pad = scaled(p, 1.0 + 0.07 * pulse)
                x, y = x - pad, y - pad
            blend(frame, p, x, y, gain, keep_s)
        if plan.get("seq"):
            f_seq = d / "seq" / f"f_{n:04d}.png"
            if f_seq.exists():
                sq = load_rgba(f_seq)
                if plan.get("seq_clear_top") and ts >= plan["seq_clear_top"][0]:      # the header's lettering, once the card hides it
                    sq[:int(plan["seq_clear_top"][1] * H), :, 3] = 0
                dx, dy = plan.get("seq_shift", {}).get(n, (0, 0))
                blend(frame, cv2.GaussianBlur(sq, (0, 0), 0.6), int(dx), int(dy))
        for c in cards:
            if c["group"] != "cards":
                continue
            k = pop(ts, c["t0"])
            if k <= 0.02:
                continue
            p, pad = scaled(c["im"], k, c.get("rot", 0.0))
            blend(frame, p, int(c["cx"] - c["im"].shape[1] / 2) - pad, int(c["cy"] - c["im"].shape[0] / 2) - pad)
        if "reframe" in plan:                              # push in on a part of the frame over a stretch of the shot
            r = plan["reframe"]
            z = 1.0 + (r["z"] - 1.0) * smooth(ts, r["t0"], r["t1"])
            if z > 1.001:
                M = np.float32([[z, 0, (1 - z) * r["cx"] * W], [0, z, (1 - z) * r["cy"] * H]])
                frame = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        if "push" in plan:                                 # a slow editorial push on a locked-off shot
            z0, z1, px, py = plan["push"]
            z = z0 + (z1 - z0) * (n - 1) / max(cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1, 1)
            M = np.float32([[z, 0, (1 - z) * px * W], [0, z, (1 - z) * py * H]])
            frame = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        for c in cards:                                    # the course card is screen furniture: on top, never pushed
            if c["group"] != "ui":
                continue
            k = pop(ts, c["t0"], d=0.32)
            if k <= 0.02:
                continue
            p, pad = scaled(c["im"], k)
            blend(frame, p, int(c["cx"] - c["im"].shape[1] / 2) - pad, int(c["cy"] - c["im"].shape[0] / 2) - pad)
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
