#!/usr/bin/env python3
"""Listen to narrator takes (or a finished video) and compare what was SAID with what should have been said.

Elaine, 2026-11-26: the first coffee cut "said arthur smth smth and that clearly doesnt match with the captions".
Nobody had listened to the takes. This script does: it transcribes each file with a local Whisper model and
compares the words with the expected text.

Usage (run with workflow/.venv/bin/python):
  check_narration.py --expect "Sol, why are you staring?" take.wav        one take against its line
  check_narration.py --episode episodes/<name>                            every take in edit.json against its phrases
  check_narration.py --video renders/cut.mp4 --episode episodes/<name>    the finished cut against the whole script
  check_narration.py --words take.wav                                     print each word with its start and end time
It prints PASS/FAIL per file and exits 1 on any FAIL. A FAIL means the words differ: listen before using the take.
Whisper mishears now and then, so read the transcript it prints rather than trusting PASS/FAIL blindly.
"""
import argparse, json, pathlib, re, subprocess, sys
import numpy as np

_model = None


def model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("small.en", device="cpu", compute_type="int8")
    return _model


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def words(path):
    segs, _ = model().transcribe(load(path), word_timestamps=True, vad_filter=False)
    return [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]


def norm(text):
    return re.sub(r"[^a-z0-9' ]", " ", text.lower().replace("’", "'")).split()


def compare(heard, expected):
    h, e = norm(heard), norm(expected)
    return h == e, " ".join(h), " ".join(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--expect")
    ap.add_argument("--episode")
    ap.add_argument("--video")
    ap.add_argument("--words", action="store_true")
    a = ap.parse_args()
    jobs = []
    if a.episode:
        ep = pathlib.Path(a.episode)
        cfg = json.loads((ep / "edit.json").read_text())
        if a.video:
            jobs.append((a.video, " ".join(p[2] for v in cfg["voice"] for p in v["phrases"])))
        else:
            for v in cfg["voice"]:
                jobs.append((ep / cfg["voice_dir"] / v["take"], " ".join(p[2] for p in v["phrases"])))
    for f in a.files:
        jobs.append((f, a.expect))
    bad = 0
    for path, expected in jobs:
        ws = words(path)
        heard = " ".join(w for w, _, _ in ws)
        if a.words:
            print(pathlib.Path(path).name, " ".join(f"{w}[{s}-{e}]" for w, s, e in ws))
        if expected is None:
            print(f"HEARD {pathlib.Path(path).name}: {heard}")
            continue
        ok, h, e = compare(heard, expected)
        bad += not ok
        print(("PASS " if ok else "FAIL ") + pathlib.Path(path).name)
        if not ok:
            print("   heard:    " + h)
            print("   expected: " + e)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
