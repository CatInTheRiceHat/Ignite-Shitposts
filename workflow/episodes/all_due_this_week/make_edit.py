#!/usr/bin/env python3
"""Write edit.json for the "All Due This Week" ad: clips, takes, word-accurate captions, sound effects, music.

Usage (workflow/.venv/bin/python):  make_edit.py [--no-music] [--web]   -> edit.json / edit-nomusic.json / edit-web.json

LANDSCAPE 1920 x 1080. Captions: the words are the SCRIPT's words (so the captions match the narration text exactly),
and each caption's time comes from Whisper's word times for that take. A take whose words differ from its script
line stops the script: that take said something else and must be regenerated.
Captions sit in the lower third, centred (script), Rammetto One 72 px, white with the orange outline, centred at
y = 895: above the bottom 10% of the frame and below the end card.
--web uses the end card that shows the sign-up address instead of "Link in description" (clips/08-comp-web.mp4).
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from check_narration import words, norm
from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[1]
SIZE, STROKE = 72, 9
FONT = ImageFont.truetype(str(WF / "assets" / "fonts" / "RammettoOne-Regular.ttf"), SIZE)
MAXW, MAXC = 1500, 34
NOMUSIC = "--no-music" in sys.argv
WEB = "--web" in sys.argv
VERSION = "v4"

# clip file (in clips/), seconds used. Clip 3 stops at 5.33 s: after that the painter put white glints in his eyes.
CLIPS = [["01-comp.mp4", 4.83], ["02-comp.mp4", 3.5], ["03-comp.mp4", 5.33], ["04-comp.mp4", 5.0], ["05-comp.mp4", 4.58],
         ["06-comp.mp4", 5.5], ["07-comp.mp4", 5.29], ["08-comp-web.mp4" if WEB else "08-comp.mp4", 10.0]]
# take, clip index, start in that clip, the script's words for it
TAKES = [
    ("01a.wav", 0, 0.20, "Sol, what's all that?"),          # clip 1 is used from 0.667 s of its paint (see composite.py)
    ("01b.wav", 0, 1.98, "Wait, is all of this due this week?"),
    ("02.wav", 1, 0.20, "Okay, here are five things that'll help."),
    ("03.wav", 2, 0.20, "First, sort it into what you control, what you can influence, and what you have to accept."),
    ("04.wav", 3, 0.25, "Second, take a few slow breaths so your body can calm down."),
    ("05.wav", 4, 0.20, "Third, pick the one thing that matters most and start there."),
    ("06.wav", 5, 0.20, "Fourth, have a backup plan, so one thing going wrong doesn't wreck everything."),
    ("07.wav", 6, 0.20, "And fifth, let your first try be messy. Rough drafts are supposed to be rough."),
    ("08a.wav", 7, 0.20, "Ignite's free Resilience and Stress Management course teaches all of this and more."),
    ("08b.wav", 7, 6.50, "So, does this week feel doable now?"),
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
    sq(0, 0, 0.58), sq(1, 0, 1.03), boing(0, 1.93), sq(2, 0, 4.08),                      # 1: two bounces at the pile, the jolt, the nod
    sq(4, 1, 2.4),                                                                     # 2: bracing
    sq(0, 2, 1.55), boing(2, 2.28, 0.24), sq(1, 2, 2.95), boing(2, 3.63, 0.24), twinkle(2, 4.2, 0.14), boing(2, 5.18, 0.2),   # 3: three things, three boxes
    twinkle(3, 3.1, 0.12),                                                             # 4: the leaf on the water
    sq(0, 4, 1.0), twinkle(4, 1.75, 0.24), boing(4, 1.9),                              # 5: point, it lights up, the hop
    boing(5, 1.55), sq(0, 5, 1.8), twinkle(5, 2.0, 0.16), boing(5, 3.0),               # 6: hop-tap, Plan B, the hop
    sq(4, 6, 0.6, 0.25), sq(0, 6, 3.05), sq(2, 6, 4.35),                               # 7: the wobble, the nudge, the little bounce
    boing(7, 0.36), twinkle(7, 1.05, 0.22), twinkle(7, 2.0), sq(2, 7, 2.1), sq(3, 7, 2.75), sq(2, 7, 9.2),   # 8: hop, card, sparkle, the nod
]


def width(text):
    return FONT.getlength(text) + 2 * STROKE


voice = []
for take, clip, start, line in TAKES:
    heard = words(HERE / "audio" / "edit" / take)
    script = line.split()
    hw_ = [w for w, _, _ in heard]
    if len(hw_) == len(script) + 1 and "".join(norm(" ".join(hw_))) == "".join(norm(line)):     # "back -up" heard as two words
        for i in range(len(heard) - 1):
            if norm(heard[i][0] + heard[i + 1][0]) == norm(script[i]):
                heard[i:i + 2] = [(heard[i][0] + heard[i + 1][0], heard[i][1], heard[i + 1][2])]
                break
    if len(heard) != len(script):
        sys.exit(f"{take}: heard {len(heard)} words, the script has {len(script)}: {[w for w, _, _ in heard]}")
    for (hw, _, _), sw in zip(heard, script):
        if norm(hw) != norm(sw) and (norm(hw), norm(sw)) not in ((["saul"], ["sol"]), (["soul"], ["sol"])):
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
    for i in range(len(groups) - 1):                     # no caption of one lonely word: it takes a word from the one before
        a_, b_ = groups[i], groups[i + 1]
        if len(b_) == 1 and len(a_) >= 3 and a_[-1][0][-1] not in ",.?!":
            b_.insert(0, a_.pop())
    phrases = []
    for g in groups:
        a, b = heard[g[0][1]][1], heard[g[-1][1]][2]
        phrases.append([round(a, 2), round(b, 2), " ".join(w for w, _ in g)])
    for i in range(len(phrases) - 1):                                         # hold each caption until the next one starts
        if phrases[i + 1][0] - phrases[i][1] < 0.45:
            phrases[i][1] = phrases[i + 1][0]
    nxt = min([s_ for t_, c_, s_, _ in TAKES if c_ == clip and s_ > start] + [CLIPS[clip][1]])      # the next take in this clip, or the cut
    phrases[-1][1] = round(min(phrases[-1][1] + 0.3, nxt - start - 0.05), 2)
    assert " ".join(p[2] for p in phrases) == line
    voice.append({"take": take, "clip": clip, "start": start, "phrases": phrases})

tag = ("-web" if WEB else "") + ("-nomusic" if NOMUSIC else "")
cfg = {
    "out": f"all-due-this-week-{VERSION}{tag}.mp4",
    "width": 1920, "height": 1080, "caption_size": SIZE, "caption_stroke": STROKE,
    # Music: Elaine picked it on cut v3: "can we do no more what ifs royal version as the music". The file in assets/music/ is the
    # instrumental version of that Persona 5 Royal song. (v1 "A Little Lesson", the coffee episode's song; v2 and v3 "Days of
    # Sisters", my pick when she asked for a song the tracker sheet did not already list.)
    "music": None if NOMUSIC else {"file": "No More What Ifs -instrumental version- 4.mp3", "start": 0.0, "gain": 0.10},
    "voice_dir": "audio/edit", "sfx_dir": "../candle_flame_up/audio/sfx",
    "caption_y": 745, "caption_max_width": MAXW, "caption_max_chars": MAXC,
    "clips": CLIPS, "voice": voice, "sfx": SFX,
}
out = HERE / f"edit{tag}.json"
out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("wrote", out.name, "total", round(sum(d for _, d in CLIPS), 2), "s")
for v in voice:
    print(v["take"], " | ".join(f"{p[2]} [{p[0]}-{p[1]}]" for p in v["phrases"]))
