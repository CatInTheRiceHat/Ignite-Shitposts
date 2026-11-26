#!/usr/bin/env python3
"""Assemble an episode cut from its edit.json: painted clips, narrator takes, captions, music, sound effects.

Usage:  python3 scripts/episode_edit.py episodes/<name> [output-name.mp4]

This is the candle episode's build_edit.py with the per-episode numbers moved into <episode>/edit.json, so a new
episode needs a config file and no new script. The look is unchanged (guidelines/current-rules.md):
  - painted clips at their native 24 fps, smooth, upscaled to 1080x1920
  - captions: Rammetto One, 105 px, white with a 12 px orange #F07B2A outline, centred at 82% of frame height,
    never wider than the frame (a group is split by measured width as well as by character count)
  - the video stops on the last frame of the last clip: no fade, no black, audio trimmed to the picture
Caption times inside a phrase are split by character count, so they are close but not word-exact.

edit.json:
  "out":    default output file name (written to <episode>/renders/)
  "music":  {"file": name in assets/music, "start": seconds to skip, "gain": 0..1}
  "clips":  [[file in <episode>/clips, seconds used], ...]
  "voice_dir", "sfx_dir": folders relative to the episode
  "voice":  [{"take": wav, "clip": index, "start": seconds into that clip, "phrases": [[from, to, text], ...]}]
  "sfx":    [[file, slice start, slice end, clip index, seconds into that clip, volume], ...]

After building it checks the result and prints PASS/FAIL lines: length, picture and sound ending together, and no
black at the end. It exits 1 if a check fails.
"""
import json, pathlib, subprocess, sys

EP = pathlib.Path(sys.argv[1]).resolve()
WF = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((EP / "edit.json").read_text())
OUT = EP / "renders" / (sys.argv[2] if len(sys.argv) > 2 else CFG["out"])
if OUT.exists():
    sys.exit(f"{OUT} already exists; pick a new name (earlier cuts are never overwritten)")
OUT.parent.mkdir(parents=True, exist_ok=True)
FONTDIR = WF / "assets" / "fonts"
MUSIC = WF / "assets" / "music" / CFG["music"]["file"]
MUSIC_START, MUSIC_GAIN = CFG["music"].get("start", 0.0), CFG["music"].get("gain", 0.16)
CLIPS = [tuple(c) for c in CFG["clips"]]
VOICE = [(v["take"], v["clip"], v["start"], [tuple(p) for p in v["phrases"]]) for v in CFG["voice"]]
SFX = [tuple(s) for s in CFG.get("sfx", [])]
VOICE_DIR, SFX_DIR = EP / CFG["voice_dir"], EP / CFG.get("sfx_dir", "audio/sfx")
MAX_CHARS = 15          # per caption line group at this size
MAX_WIDTH = 960         # px at 1080 wide, outline included. 15 characters of wide letters ("know why coffee") overflow
                        # the frame, so a group is also split when it would be wider than this (coffee cut v2, 2026-11-26)
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype(str(FONTDIR / "RammettoOne-Regular.ttf"), 105)


def width(text):
    return font.getlength(text) + 2 * 12


def chunks(text):
    words, out, cur = text.split(), [], []
    for w in words:
        trial = " ".join(cur + [w])
        if cur and (len(trial) > MAX_CHARS or width(trial) > MAX_WIDTH):
            out.append(" ".join(cur))
            cur = []
        cur.append(w)
    if cur:
        out.append(" ".join(cur))
    return out


def probe(path, stream):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip().splitlines()[0])


for f, d in CLIPS:
    have = probe(EP / "clips" / f, "v:0")
    if have + 0.05 < d:
        sys.exit(f"{f} is {have:.2f}s but edit.json uses {d}s of it")

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
capdir = EP / "renders" / ("captions-" + OUT.stem)
capdir.mkdir(parents=True, exist_ok=True)
wide = [(round(width(t)), t) for _, _, t in events if width(t) > 1040]
if wide:
    sys.exit(f"caption wider than the frame: {wide}")
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
    cmd += ["-i", str(VOICE_DIR / take)]
cmd += ["-ss", str(MUSIC_START), "-i", str(MUSIC)]
CAP0 = len(CLIPS) + len(VOICE) + 1
for f, _, _ in caps:
    cmd += ["-i", str(f)]
SFX0 = CAP0 + len(caps)
for f, a_, b_, *_ in SFX:
    cmd += ["-ss", str(a_), "-t", f"{b_ - a_:.3f}", "-i", str(SFX_DIR / f)]
nv = len(CLIPS)
fc = []
for i, (_, d) in enumerate(CLIPS):
    fc.append(f"[{i}:v]fps=24,trim=duration={d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[v{i}]")
fc.append("".join(f"[v{i}]" for i in range(nv)) + f"concat=n={nv}:v=1:a=0[vc]")
prev = "vc"
for i, (f, a_, b_) in enumerate(caps):
    fc.append(f"[{prev}][{CAP0 + i}:v]overlay=0:1424:enable='between(t,{a_:.3f},{b_:.3f})'[c{i}]")
    prev = f"c{i}"
fc.append(f"[{prev}]null[vout]")
for j, (take, ci, start, _) in enumerate(VOICE):
    ms = int(round((offsets[ci] + start) * 1000))
    fc.append(f"[{nv + j}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}:all=1[a{j}]")
mi = nv + len(VOICE)
fc.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={total},volume={MUSIC_GAIN},"
          f"afade=t=in:d=0.4,afade=t=out:st={total - 1.0}:d=1.0[mus]")
for j, (f, a_, b_, ci, t_, vol) in enumerate(SFX):
    ms = int(round((offsets[ci] + t_) * 1000))
    fc.append(f"[{SFX0 + j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}:all=1[s{j}]")
fc.append("".join(f"[a{j}]" for j in range(len(VOICE))) + "".join(f"[s{j}]" for j in range(len(SFX)))
          + f"[mus]amix=inputs={len(VOICE) + len(SFX) + 1}:normalize=0:duration=longest,"
          f"atrim=duration={total}[aout]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-r", "24", "-c:v", "libx264", "-crf", "16",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-t", str(total), str(OUT)]
subprocess.run(cmd, check=True)

# ---- checks on the finished file ----
vd, ad = probe(OUT, "v:0"), probe(OUT, "a:0")
r = subprocess.run(["ffmpeg", "-v", "info", "-sseof", "-1.5", "-i", str(OUT), "-vf", "blackdetect=d=0.04:pix_th=0.10",
                    "-an", "-f", "null", "-"], capture_output=True, text=True)
black = [l for l in r.stderr.splitlines() if "black_start" in l]
checks = [
    ("length matches the clips", abs(vd - total) < 0.1, f"video {vd:.2f}s, planned {total:.2f}s"),
    ("picture and sound end together", abs(vd - ad) < 0.08, f"video {vd:.2f}s, audio {ad:.2f}s"),
    ("no black at the end", not black, black[0].split("]")[-1].strip() if black else "last 1.5s clean"),
]
ok = True
for name, good, detail in checks:
    ok &= good
    print(("PASS " if good else "FAIL ") + name + ": " + detail)
print(OUT)
sys.exit(0 if ok else 1)
