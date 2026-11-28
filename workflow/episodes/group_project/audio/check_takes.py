#!/usr/bin/env python3
"""Is any narrator take cut off? Elaine, 2026-11-27: "the 'second' from arthur is cut off. make sure that you put full
audio for each thing". Take 04 began with sound on its very first sample, so the S of "Second" was gone.

Usage (workflow/.venv/bin/python): check_takes.py <folder of wav takes> [more folders]
For each take: where the first and last sound are, and how loud the first and last 20 ms are. A take is CLIPPED when
it is not quiet at its very start or very end (louder than -60 dB): the voice was already going, or still going.
Exits 1 if any take is clipped.
"""
import pathlib, subprocess, sys
import numpy as np


def load(p, sr=24000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def db(x):
    return 20 * np.log10(max(float(np.sqrt(np.mean(x ** 2))), 1e-6))


bad = 0
for folder in sys.argv[1:]:
    for f in sorted(pathlib.Path(folder).glob("*.wav")):
        a = load(f)
        env = np.array([db(a[i:i + 240]) for i in range(0, len(a) - 240, 240)])
        loud = np.where(env > env.max() - 30)[0]
        head, tail = db(a[:480]), db(a[-480:])
        clipped = head > -60 or tail > -60
        bad += clipped
        print(f"{'CLIPPED' if clipped else 'ok     '} {f.parent.name}/{f.name:14} {len(a) / 24000:5.2f}s  sound {loud[0] * 0.01:4.2f}-{(loud[-1] + 1) * 0.01:4.2f}s  "
              f"first 20 ms {head:6.1f} dB  last 20 ms {tail:6.1f} dB")
sys.exit(1 if bad else 0)
