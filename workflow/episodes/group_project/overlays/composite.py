#!/usr/bin/env python3
"""Lay the lettering (and the end card) over a painted clip and cut out the SQUARE: painted 16:9 clip in, 1080 x 1080 out.

Usage (workflow/.venv/bin/python):
  composite.py <clip number> <painted.mp4> <out.mp4> [--shift seconds] [--card art.png] [--no-badge] [--frame t out.png] [--wide]

The painter cannot write words and only returns 16:9. So: every word is drawn once (make_art.py), sits on a plane in
the Blender scene (skeleton/clips.py, OVL_ planes) and is rendered as its own pass for EVERY frame, at 1920 x 1080 with
whatever stands in front of it cut out (render_clip.py MODE=ovlseq -> overlays/<clip>/seq/). Here the painted clip is
scaled to 1920 x 1080, the pass is laid over it, and the MIDDLE SQUARE (x 420 to 1500) is kept.
Clip 8 adds the end card (make_end_card.py, already square), which slides in from the right over half a second and
holds to the end (Elaine's end-card prompt).
--shift moves every overlay time later (+) or earlier (-) if the painted clip drifted from the skeleton.
--frame writes one finished frame as a PNG instead of the clip. --wide keeps the whole 16:9 frame (for checking).
PLAN times are seconds on the clip's own clock and match skeleton/clips.py.
"""
import math, pathlib, subprocess, sys
import cv2, numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE / "art"
W, H = 1920, 1080
X0 = (W - H) // 2                       # the square's left edge in the 16:9 frame
# Elaine on cut v5 (2026-11-27): "the text must move when the signs are moving for example judging 6 pm". A sign the
# painter moves (a board that shudders, a card that drops and rocks) is now FOLLOWED in the painted picture itself: its
# words are a "track" layer. The sign is found in the last painted frame, where it stands still, and then followed
# backwards frame by frame, so the words ride on it the whole time: they fall with a card and shake when it shakes.
#   track keys: side / up / down = how far (px in the 1920 x 1080 frame) the sign may move between two frames;
#   appear = the sign drops into the shot, so before it is first found there are no words; min = least match score.
DROP = {"side": 90, "up": 520, "down": 60, "appear": True}
STILL = {"side": 14, "up": 14, "down": 14}          # a board that only shudders: it never jumps onto another board
PLAN = {
    # 1: only the banner's words, while the banner is in front of the camera; the pass ends when it leaves the frame.
    "1": {"no_seq": True, "layers": [{"dir": "seq_banner", "from": 0.0}]},
    "2": {"no_seq": True},                               # the plan board is outside the square in this shot
    # 3: one stray frame (painted frame 20) had a light bulb half a second early; the frame before it is held instead.
    "3": {"hold": {20: 19}},
    "4": {"no_seq": True, "layers": [{"dir": "seq_moat", "track": DROP}, {"dir": "seq_walls", "track": DROP}]},
    "4b": {"no_seq": True, "layers": [{"dir": "seq_towers", "track": DROP}, {"dir": "seq_flag", "track": DROP}]},
    "6": {},
    # 5: the first board is there from the start and shudders with the clock; the second drops onto the post under it.
    "5": {"no_seq": True, "layers": [{"dir": "seq_judging", "track": STILL},
                                     {"dir": "seq_doneby", "track": {"side": 60, "up": 70, "down": 50, "appear": True}}]},
    # 7: no lettering in the square. The painter put our Sol right on the square's left edge after the camera slides to
    #    him and the other two (the review of cut v6: he was cut by the frame). The square itself slides 52 px to the left
    #    with that camera move, which leaves sand on both sides of the three of them.
    "7": {"no_seq": True, "crop_pan": [3.4, 4.3, -52]},
    # 8: "1st" is placed on the painted rosette itself, found in each frame by its blue and centred on its cream middle,
    #    from the moment it has landed until the end card covers it.
    "8": {"no_seq": True, "badge": {"art": "first.png", "t0": 0.75, "t1": 2.3}, "card": {"art": "end_card.png", "t0": 1.6, "d": 0.5}},
}


def follow(frames, start, tmpl, pos, opt):
    """Follow one sign through the painted frames (uint8 BGR, 1920 x 1080), backwards and forwards from frame `start`,
    where its template `tmpl` sits with its top-left at `pos`. Returns {frame: (x, y)}; a frame is missing when the
    sign is not in the shot yet."""
    th, tw = tmpl.shape[:2]
    out = {start: pos}
    for step in (-1, 1):
        cur, lost, i = pos, 0, start + step
        while 0 <= i < len(frames):
            # First look right beside where it was a frame ago: a sign that only drifts or rocks is there, and a fair match
            # is enough. Only if it is not there, look further (a sign that drops moves a long way in one frame), and then
            # the match has to be a good one: a plain pastel card half-matches plain sky and sea.
            up, down = (opt["up"], opt["down"]) if step < 0 else (opt["down"], opt["up"])   # back in time a dropped sign moves UP
            score = -1.0
            for side, u_, d_, least in ((min(opt["side"], 30), min(up, 12), min(down, 12), 0.60), (opt["side"], up, down, opt.get("min", 0.68))):
                wx0, wy0 = max(0, cur[0] - side), max(0, cur[1] - u_)
                wx1, wy1 = min(W, cur[0] + tw + side), min(H, cur[1] + th + d_)
                if wx1 - wx0 >= tw and wy1 - wy0 >= th:
                    res = cv2.matchTemplate(frames[i][wy0:wy1, wx0:wx1], tmpl, cv2.TM_CCOEFF_NORMED)
                    _, sc, _, loc = cv2.minMaxLoc(res)
                    if sc >= least:
                        score = 1.0
                        break
            if score > 0:
                new = (wx0 + loc[0], wy0 + loc[1])
                for g in range(1, lost + 1):                    # a frame or two it was lost in between: no gap in the words
                    out[i - step * g] = new if g <= lost // 2 else cur
                cur, lost = new, 0
                out[i] = cur
            else:
                lost += 1
                if opt.get("appear") and step < 0:
                    if lost >= 3:
                        break
                else:
                    out[i] = cur                               # hidden or blurred for a moment: the words hold their place
            i += step
    return out


def find_rosette(frame):
    """The blue ribbon in a float BGR frame (1920 x 1080): (centre x, centre y, width) of its plain cream MIDDLE, or of
    its round blue part when no middle shows. (Elaine, 2026-11-27, of "1st" sitting low on the ribbon: "like this isnt
    centered": it had been put at the middle of the whole blue shape, tails and all.)"""
    b, g, r = frame[..., 0], frame[..., 1], frame[..., 2]
    m = ((b > r + 0.22) & (b > g + 0.08) & (b > 0.5)).astype(np.uint8)
    m[:int(H * 0.36)] = 0                                  # the bunting's blue pennants are up there
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8)))
    best = None
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area > 500 and X0 < x + w / 2 < X0 + H and (best is None or area > best[4]):
            best = (x, y, w, h, area)
    if best is None:
        return None
    x, y, w, h, _ = best
    blue = cv2.morphologyEx(m[y:y + h, x:x + w], cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid = np.zeros_like(blue)
    cv2.drawContours(solid, cs, -1, 1, -1)
    hole = cv2.morphologyEx(solid & (1 - blue), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    k, _, hs, hc = cv2.connectedComponentsWithStats(hole)
    holes = [j for j in range(1, k) if hs[j][4] > 0.04 * w * min(w, h)]
    if holes:
        j = max(holes, key=lambda q: hs[q][4])
        return x + hc[j][0], y + hc[j][1], hs[j][2] / 0.62 * 0.8        # the words span 80% of the cream middle
    return x + w / 2, y + min(w, h) * 0.5, w


def ease_out_back(x, s=1.2):
    x = min(1.0, max(0.0, x)) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


def load_rgba(path):
    im = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    assert im is not None and im.shape[2] == 4, path
    return im.astype(np.float32) / 255.0


def over(frame, rgba, x=0, y=0, gain=1.0):
    """Alpha-over a float BGRA image onto the float frame with its top-left at (x, y)."""
    h, w = rgba.shape[:2]
    fh, fw = frame.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, fw), min(y + h, fh)
    if x1 <= x0 or y1 <= y0:
        return
    p = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = p[:, :, 3:4] * gain
    frame[y0:y1, x0:x1] = frame[y0:y1, x0:x1] * (1 - a) + p[:, :, :3] * a


def main():
    args = sys.argv[1:]
    shift, single, wide = 0.0, None, "--wide" in args
    if wide:
        args.remove("--wide")
    if "--shift" in args:
        i = args.index("--shift")
        shift = float(args[i + 1])
        del args[i:i + 2]
    if "--no-badge" in args:                 # the "1st" is in the skeleton, so painted in: nothing is laid on the ribbon
        args.remove("--no-badge")
        PLAN["8"].pop("badge", None)
    if "--card" in args:
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
    seq = HERE / clip / "seq"

    def last(folder):
        """How many lettering frames a pass has: a painted clip can run a frame or two longer than its skeleton, and
        the last lettering frame is then held (without this the TEAM SOL table blinked off at the end of clip 6)."""
        return max((int(f.stem[2:]) for f in folder.glob("f_*.png")), default=0)
    n_seq = last(seq)
    n_layer = {l["dir"]: last(HERE / clip / l["dir"]) for l in plan.get("layers", [])}
    card = load_rgba(ART / plan["card"]["art"]) if "card" in plan else None
    badge = load_rgba(ART / plan["badge"]["art"]) if "badge" in plan else None
    kept, last_badge = {}, None
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    tracks = {}
    if any("track" in l for l in plan.get("layers", [])):
        big = []
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            big.append(cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA))
        cap.release()
        cap = cv2.VideoCapture(src)
        for l in plan["layers"]:
            if "track" not in l:
                continue
            ref = len(big) - 1
            art = load_rgba(HERE / clip / l["dir"] / f"f_{min(ref + 1, n_layer[l['dir']]):04d}.png")
            ys, xs = np.nonzero(art[..., 3] > 0.05)
            box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
            # What is followed is the painted patch under the words plus a rim wide enough to take in the card's own edges
            # (the plain middle of a card has nothing to hold on to). Finding the card by its colour was tried and
            # dropped: the pastel cards run into the sand and the sky.
            mx, my = int(0.16 * (box[2] - box[0])) + 8, int(0.26 * (box[3] - box[1])) + 8
            t0 = (max(0, box[0] - mx), max(0, box[1] - my))
            tmpl = big[ref][t0[1]:min(H, box[3] + my), t0[0]:min(W, box[2] + mx)]
            path = follow(big, ref, tmpl, t0, l["track"])
            tracks[l["dir"]] = (cv2.GaussianBlur(art, (0, 0), 0.6), t0, path)
            seen = sorted(path)
            print(f"  {l['dir']}: on screen from frame {seen[0]} ({seen[0] / fps:.2f} s), "
                  f"moves x {min(p[0] for p in path.values()) - t0[0]}..{max(p[0] for p in path.values()) - t0[0]}, "
                  f"y {min(p[1] for p in path.values()) - t0[1]}..{max(p[1] for p in path.values()) - t0[1]} px")
        del big
    OW = W if wide else H
    proc = None
    if single is None:
        proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OW}x{H}", "-r", f"{fps}",
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
        kept[n - 1] = fr
        kept.pop(n - 4, None)
        fr = kept.get(plan.get("hold", {}).get(n - 1, n - 1), fr)          # a stray painted frame is replaced by an earlier one
        frame = cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32) / 255.0
        ts = t - shift
        ns = max(1, int(round(ts * fps)) + 1)                    # the skeleton frame that belongs to this moment
        f_seq = seq / f"f_{min(plan.get('seq_map', {}).get(ns, ns), max(n_seq, 1)):04d}.png"
        if f_seq.exists() and not plan.get("no_seq") and plan.get("seq_from", 0.0) <= ts <= plan.get("seq_until", 1e9):
            over(frame, cv2.GaussianBlur(load_rgba(f_seq), (0, 0), 0.6), 0, 0, 0.95)
        for layer in plan.get("layers", []):                          # single lettering passes, each with its own start
            if layer["dir"] in tracks:                                # a followed sign: the words go where the painted sign is
                art, t0, path = tracks[layer["dir"]]
                if n - 1 in path:
                    over(frame, art, path[n - 1][0] - t0[0], path[n - 1][1] - t0[1], 0.95)
                continue
            f_l = HERE / clip / layer["dir"] / f"f_{min(ns, max(n_layer[layer['dir']], 1)):04d}.png"
            if ts >= layer.get("from", 0.0) and f_l.exists() and ns <= n_layer[layer["dir"]] + layer.get("hold_last", 0):
                over(frame, cv2.GaussianBlur(load_rgba(f_l), (0, 0), 0.6), 0, 0, 0.95)
        if badge is not None and plan["badge"]["t0"] <= ts <= plan["badge"]["t1"]:
            found = find_rosette(frame)
            if found:
                if last_badge:                                    # smoothed, so the words do not jitter
                    found = tuple(0.5 * a_ + 0.5 * b_ for a_, b_ in zip(last_badge, found))
                last_badge = found
                cx, cy, w = found
                size = max(12, int(round(w * 0.62)))                 # w is the width the art is sized against
                over(frame, cv2.resize(badge, (size, size), interpolation=cv2.INTER_AREA), int(round(cx - size / 2)), int(round(cy - size / 2)), 0.95)
        if not wide:
            x_sq = X0
            if "crop_pan" in plan:                                   # the square slides sideways between two times
                a_, b_, dx = plan["crop_pan"]
                u = min(1.0, max(0.0, (ts - a_) / (b_ - a_)))
                x_sq = X0 + int(round(dx * u * u * (3 - 2 * u)))
            frame = np.ascontiguousarray(frame[:, x_sq:x_sq + H])
        if card is not None:                                     # the end card: in from the right, then it holds
            k = ease_out_back((ts - plan["card"]["t0"]) / plan["card"]["d"]) if ts > plan["card"]["t0"] else 0.0
            if k > 0:
                cx_ = int(round((1 - k) * 700)) + (X0 if wide else 0)
                over(frame, card, cx_, 0)
                if cx_ < (X0 if wide else 0):                        # the card bounces past its place: its orange runs on to
                    edge = np.repeat(card[:, -1:, :], (X0 if wide else 0) - cx_ + 2, axis=1)   # the frame edge, so no gap opens
                    over(frame, edge, cx_ + card.shape[1] - 1, 0)
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
