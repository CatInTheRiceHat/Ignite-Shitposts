#!/usr/bin/env python3
"""Write edit.json for the ad: clips, takes, word-accurate captions, sound effects, music.

Usage (workflow/.venv/bin/python):  make_edit.py [--no-music]   -> edit.json (or edit-nomusic.json)

Captions: the words are the SCRIPT's words (so the captions match the narration text exactly), and each caption's
time comes from Whisper's word times for that take, not from pause guessing. A take whose word count differs from
its script line stops the script: that take said something else and must be regenerated.
Captions sit in a band centred at 70% of the height, at most 840 px wide: out of the bottom fifth and off the right
edge, where the platform's buttons are (script v4, framing rule).
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from check_narration import words, norm
from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[1]
FONT = ImageFont.truetype(str(WF / "assets" / "fonts" / "RammettoOne-Regular.ttf"), 105)
MAXW, MAXC = 840, 14
NOMUSIC = "--no-music" in sys.argv

# clip file (in clips/), seconds used
CLIPS = [["01-comp.mp4", 6.3], ["02-comp.mp4", 3.0], ["03-comp.mp4", 5.4], ["04-comp.mp4", 4.0], ["05-comp.mp4", 4.85],
         ["06-comp.mp4", 5.15], ["07-comp.mp4", 5.0], ["08-comp.mp4", 9.3], ["09-comp.mp4", 3.3]]
# take, clip index, start in that clip, the script's words for it
TAKES = [
    ("01a.wav", 0, 0.25, "Sol, what are you doing?"),
    ("01b.wav", 0, 2.50, "Wait, your science project's due in five minutes?"),
    ("02.wav", 1, 0.20, "Okay, here are five things that'll save it."),
    ("03.wav", 2, 0.20, "First, write your question at the top so judges know what you were testing."),
    ("04.wav", 3, 0.12, "Second, say the one thing you changed and what you measured."),
    ("05.wav", 4, 0.20, "Third, say how many times you ran it, because one try could just be luck."),
    ("06.wav", 5, 0.20, "Fourth, turn your numbers into a graph, since nobody reads a wall of numbers."),
    ("07.wav", 6, 0.20, "And fifth, write down what went wrong, because real scientists always do."),
    ("08a.wav", 7, 0.25, "Ignite's free Scientific Research and Data Analysis course teaches you how real research works, from collecting data to analyzing it."),
    ("08b.wav", 8, 0.25, "So, is it ready now?"),
]
S, B, T = "squeaks-tiny.mp3", "boing.mp3", "twinkle.mp3"
SQ = [(1.08, 1.19), (1.64, 1.76), (2.48, 2.56), (2.81, 2.91), (0.5, 0.74)]


def sq(i, clip, t, vol=0.35):
    return [S, SQ[i][0], SQ[i][1], clip, t, vol]


def boing(clip, t, vol=0.28):
    return [B, 0.0, 0.24, clip, t, vol]


def twinkle(clip, t, vol=0.2):
    return [T, 0.0, 1.24, clip, t, vol]


SFX = [
    boing(0, 2.5), sq(2, 0, 5.6),                                                   # 1: the jolt, the nod
    sq(4, 1, 1.9),                                                                  # 2: bracing
    boing(2, 1.28), sq(0, 2, 1.5), twinkle(2, 1.55), boing(2, 4.15), sq(1, 2, 4.38),   # 3: two taps, the question
    sq(0, 3, 1.1), twinkle(3, 1.9, 0.16), sq(1, 3, 2.55), twinkle(3, 3.3, 0.16),      # 4: nudge, label, point, label
    sq(0, 4, 0.6), boing(4, 1.42), sq(2, 4, 1.7), sq(3, 4, 2.0), sq(2, 4, 2.3),       # 5: nudge, hop back, three tags
    sq(4, 5, 0.3), twinkle(5, 1.2), boing(5, 1.98), twinkle(5, 3.0, 0.14),            # 6: push, notes fall, bounce, labels
    sq(0, 6, 1.78), twinkle(6, 1.9),                                                  # 7: pat, heading
    boing(7, 0.15), boing(7, 0.7), twinkle(7, 1.6, 0.22), boing(7, 2.2), twinkle(7, 2.25), boing(7, 7.0),   # 8
    twinkle(8, 1.95), sq(2, 8, 2.1), sq(3, 8, 2.55),                                  # 9: sparkle, two nods
]


def width(text):
    return FONT.getlength(text) + 24


voice = []
for take, clip, start, line in TAKES:
    heard = words(HERE / "audio" / "edit" / take)
    script = line.split()
    if len(heard) != len(script):
        sys.exit(f"{take}: heard {len(heard)} words, the script has {len(script)}: {[w for w, _, _ in heard]}")
    for (hw, _, _), sw in zip(heard, script):
        if norm(hw) != norm(sw) and (norm(hw), norm(sw)) not in ((["saul"], ["sol"]), (["analysing"], ["analyzing"])):
            sys.exit(f"{take}: heard '{hw}' where the script says '{sw}'")
    groups, cur = [], []
    for i, sw in enumerate(script):
        trial = " ".join([w for w, _ in cur] + [sw])
        if cur and (len(trial) > MAXC or width(trial) > MAXW):
            groups.append(cur)
            cur = []
        cur.append((sw, i))
        if sw[-1] in ",.?!" and len(" ".join(w for w, _ in cur)) >= 5:      # a pause in the sentence ends the caption
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    phrases = []
    for g in groups:
        a, b = heard[g[0][1]][1], heard[g[-1][1]][2]
        phrases.append([round(a, 2), round(b, 2), " ".join(w for w, _ in g)])
    for i in range(len(phrases) - 1):                                         # hold each caption until the next one starts
        if phrases[i + 1][0] - phrases[i][1] < 0.45:
            phrases[i][1] = phrases[i + 1][0]
    phrases[-1][1] = round(min(phrases[-1][1] + 0.25, CLIPS[clip][1] - start - 0.05), 2)   # never past the cut
    assert " ".join(p[2] for p in phrases) == line
    voice.append({"take": take, "clip": clip, "start": start, "phrases": phrases})

cfg = {
    "out": "due-in-5-v7-nomusic.mp4" if NOMUSIC else "due-in-5-v7.mp4",
    "music": None if NOMUSIC else {"file": "試験中… (P3R ver.) 4.mp3", "start": 0.0, "gain": 0.10},
    "voice_dir": "audio/edit", "sfx_dir": "../candle_flame_up/audio/sfx",
    "caption_y": 1194, "caption_max_width": MAXW, "caption_max_chars": MAXC,
    "clips": CLIPS, "voice": voice, "sfx": SFX,
}
out = HERE / ("edit-nomusic.json" if NOMUSIC else "edit.json")
out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("wrote", out.name, "total", round(sum(d for _, d in CLIPS), 2), "s")
for v in voice:
    print(v["take"], " | ".join(f"{p[2]} [{p[0]}-{p[1]}]" for p in v["phrases"]))
