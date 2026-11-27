#!/usr/bin/env python3
"""Trim dead air from the narrator takes: raw/ -> edit/. The voice itself is never sped up or stretched.

Head and tail silence is cut, and any pause inside a take longer than MAXGAP is shortened to MAXGAP.
Usage: python3 trim_takes.py            (run from anywhere)
"""
import pathlib, re, subprocess

HERE = pathlib.Path(__file__).resolve().parent
RAW, OUT = HERE / "raw", HERE / "edit"
OUT.mkdir(exist_ok=True)
MAXGAP, PAD = 0.30, 0.04


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


for wav in sorted(RAW.glob("*.wav")):
    total = dur(wav)
    err = subprocess.run(["ffmpeg", "-i", str(wav), "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    if len(ends) < len(starts):
        ends.append(total)
    keep, cur = [], 0.0                       # spans of sound to keep
    for s, e in zip(starts, ends):
        if s <= 0.01:                         # silence at the head
            cur = max(e - PAD, 0.0)
            continue
        if e >= total - 0.01:                 # silence at the tail
            keep.append((cur, min(s + 0.08, total)))
            cur = None
            break
        if e - s > MAXGAP:                    # a long pause: keep MAXGAP of it, half on each side
            keep.append((cur, s + MAXGAP / 2))
            cur = e - MAXGAP / 2
    if cur is not None:
        keep.append((cur, total))
    parts = ";".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={b - a - 0.008:.3f}:d=0.008[p{i}]"
                     for i, (a, b) in enumerate(keep))
    fc = parts + ";" + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-filter_complex", fc, "-map", "[o]", str(OUT / wav.name)], check=True)
    print(f"{wav.name}: {total:.2f}s -> {dur(OUT / wav.name):.2f}s  kept {[(round(a, 2), round(b, 2)) for a, b in keep]}")
