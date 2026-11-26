#!/usr/bin/env python3
"""Assemble the candle episode draft: painted clips at native 24 fps (no on-twos stepping), narrator, captions, music.

Run from anywhere:  python3 build_edit.py [output-name]
Captions are PNG overlays that follow the fire episode treatment: Rammetto One, white fill, orange #F07B2A outline,
105 px with a 12 px outline at 1080 wide, centred at 82% of frame height.
Caption times inside a phrase are split by character count, so they are close but not word-exact.
"""
import subprocess, sys, pathlib

EP = pathlib.Path(__file__).resolve().parent
WF = EP.parent.parent
OUT = EP / "renders" / (sys.argv[1] if len(sys.argv) > 1 else "candle-v8.mp4")
FONTDIR = WF / "assets" / "fonts"
MUSIC = WF / "assets" / "music" / "BAREFOOT IN THE PARK.mp3"     # one of the two songs Elaine added 2026-11-25
MUSIC_START, MUSIC_GAIN = 3.0, 0.16                    # skip its near-silent first seconds; keep it under the narrator

# clip file, length in seconds
# Elaine, 2026-11-25: "i like the cartoony blinks", so these are the painted takes WITH their blinks (no fix_blinks repair).
CLIPS = [("01-paint-v5.mp4", 7.4), ("02a-paint-v7.mp4", 4.25), ("02b-paint-v7.mp4", 4.8), ("03-paint-v4.mp4", 7.6),
         ("04-paint-v6-ball.mp4", 7.6), ("05-paint-v8-raw.mp4", 5.6)]
# cute sound effects (Elaine 2026-11-25): file, slice start, slice end, clip index, time in clip, volume
SQ = "squeaks-tiny.mp3"
S1, S2, S3, S4, S5, S6 = (0.50, 0.74), (1.08, 1.19), (1.64, 1.76), (1.96, 2.09), (2.48, 2.56), (2.81, 2.91)
BOING, TWINK = ("boing.mp3", 0.0, 0.24), ("twinkle.mp3", 0.0, 1.24)
SFX = [
    (SQ, *S2, 0, 0.30, 0.35), (SQ, *S3, 0, 0.75, 0.35), (SQ, *S4, 0, 1.15, 0.35),      # candle wiggles
    (*BOING, 0, 1.50, 0.30), (SQ, *S5, 0, 6.50, 0.40), (SQ, *S6, 0, 6.95, 0.40),        # look up, two nods
    (SQ, *S2, 2, 0.35, 0.35), (SQ, *S3, 2, 0.85, 0.35), (SQ, *S4, 2, 1.30, 0.35),      # three steps with the stand
    (*TWINK, 2, 1.70, 0.25), (*BOING, 2, 2.55, 0.30),                                  # spiral spins, arms up
    (SQ, *S1, 3, 0.45, 0.35), (SQ, *S4, 3, 3.60, 0.35),                                # duck, straighten
    (*BOING, 4, 0.50, 0.30), (SQ, *S3, 4, 1.70, 0.35), (*TWINK, 4, 4.00, 0.25),         # shrug, turn, blue ball
    (SQ, *S5, 4, 5.30, 0.35),                                                          # touches the glass
    (SQ, *S2, 5, 0.40, 0.35), (*BOING, 5, 2.70, 0.30),       # lifts the dish; the candle drops back down
    (SQ, *S5, 5, 4.75, 0.40), (SQ, *S6, 5, 5.15, 0.40),
]
# take, clip index, start inside the clip, [(phrase start, phrase end inside the take, text)]
# Take 02a.wav starts over the candle close-up (clip 02a) and runs on across the cut into clip 02b.
# The cut sits in the narrator's pause between "hot air rises." and "Slide that paper spiral over it."
VOICE = [
    ("01a.wav", 0, 0.15, [(0.06, 1.20, "What are you doing, Sol?")]),
    ("01b.wav", 0, 2.50, [(0.06, 0.40, "Ohh,"), (0.78, 3.85, "you must be wondering why the flame is still standing straight up.")]),
    ("02a.wav", 1, 0.15, [(0.06, 0.69, "It's the air."), (1.27, 2.23, "The flame heats it,"),
                          (2.83, 4.03, "and hot air rises."), (4.18, 6.02, "Slide that paper spiral over it.")]),
    ("02b.wav", 2, 2.25, [(0.06, 0.35, "See?"), (0.96, 2.27, "The rising air spins it.")]),
    ("03.wav", 3, 0.20, [(0.06, 3.32, "Down low, cooler air slides in to replace it."),
                         (3.58, 6.70, "That upward stream stretches the flame into a teardrop.")]),
    ("04.wav", 4, 0.20, [(0.06, 1.29, "But what if there's no up?"), (1.88, 3.77, "In orbit, hot air doesn't rise,"),
                         (4.17, 6.49, "so the flame becomes a little blue ball.")]),
    ("05.wav", 5, 0.20, [(0.06, 1.17, "So for a flame,"), (1.51, 3.67, "up is just where the hot air goes."),
                         (3.89, 4.30, "Got it?")]),
]
MAX_CHARS = 15          # per caption line group at this size


def chunks(text):
    words, out, cur = text.split(), [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > MAX_CHARS:
            out.append(" ".join(cur))
            cur = []
        cur.append(w)
    if cur:
        out.append(" ".join(cur))
    return out


def ts(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h}:{m:02d}:{t % 60:05.2f}"


offsets, t = [], 0.0
for _, d in CLIPS:
    offsets.append(t)
    t += d
total = t

events = []
for take, ci, start, phrases in VOICE:
    for a, b, text in phrases:
        parts = chunks(text)
        n = sum(len(p) for p in parts)
        cur = offsets[ci] + start + a
        for p in parts:
            dur = (b - a) * len(p) / n
            events.append((cur, cur + dur, p))
            cur += dur
# This ffmpeg build has no subtitle/drawtext filter, so each caption is a transparent PNG overlay.
from PIL import Image, ImageDraw, ImageFont
capdir = EP / "renders" / "captions-v2"
capdir.mkdir(parents=True, exist_ok=True)
font = ImageFont.truetype(str(FONTDIR / "RammettoOne-Regular.ttf"), 105)
caps = []
for i, (a_, b_, txt) in enumerate(events):
    im = Image.new("RGBA", (1080, 300), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((540, 150), txt, font=font, fill="#FFFFFF", anchor="mm",
                            stroke_width=12, stroke_fill="#F07B2A")
    f = capdir / f"cap{i:02d}.png"
    im.save(f)
    caps.append((f, a_, b_))

cmd = ["ffmpeg", "-y", "-v", "error"]
for f, _ in CLIPS:
    cmd += ["-i", str(EP / "clips" / f)]
for take, *_ in VOICE:
    cmd += ["-i", str(EP / "audio" / "v2" / "trim" / take)]
cmd += ["-ss", str(MUSIC_START), "-i", str(MUSIC)]
CAP0 = len(CLIPS) + len(VOICE) + 1
for f, _, _ in caps:
    cmd += ["-i", str(f)]
SFX0 = CAP0 + len(caps)
for f, a_, b_, *_ in SFX:
    cmd += ["-ss", str(a_), "-t", f"{b_ - a_:.3f}", "-i", str(EP / "audio" / "sfx" / f)]
nv = len(CLIPS)
fc = []
for i, (_, d) in enumerate(CLIPS):
    # Elaine 2026-11-25: no on-twos stepping. Keep every painted frame at the model's native 24 fps.
    fc.append(f"[{i}:v]fps=24,trim=duration={d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[v{i}]")
fc.append("".join(f"[v{i}]" for i in range(nv)) + f"concat=n={nv}:v=1:a=0[vc]")
prev = "vc"
for i, (f, a_, b_) in enumerate(caps):
    fc.append(f"[{prev}][{CAP0 + i}:v]overlay=0:1424:enable='between(t,{a_:.3f},{b_:.3f})'[c{i}]")
    prev = f"c{i}"
fc.append(f"[{prev}]null[vout]")
for j, (take, ci, start, _) in enumerate(VOICE):
    ms = int(round((offsets[ci] + start) * 1000))
    fc.append(f"[{nv + j}:a]aresample=48000,adelay={ms}:all=1[a{j}]")
mi = nv + len(VOICE)
fc.append(f"[{mi}:a]aresample=48000,atrim=duration={total},volume={MUSIC_GAIN},afade=t=in:d=0.4,afade=t=out:st={total - 1.0}:d=1.0[mus]")
for j, (f, a_, b_, ci, t_, vol) in enumerate(SFX):
    ms = int(round((offsets[ci] + t_) * 1000))
    fc.append(f"[{SFX0 + j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}:all=1[s{j}]")
fc.append("".join(f"[a{j}]" for j in range(len(VOICE))) + "".join(f"[s{j}]" for j in range(len(SFX)))
          + f"[mus]amix=inputs={len(VOICE) + len(SFX) + 1}:normalize=0:duration=longest,"
          f"atrim=duration={total}[aout]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-r", "24", "-c:v", "libx264", "-crf", "16",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-t", str(total), str(OUT)]
subprocess.run(cmd, check=True)
print(OUT, total)
