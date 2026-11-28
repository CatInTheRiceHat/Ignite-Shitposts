#!/usr/bin/env python3
"""Write edit.json for the "Whole Group Project" ad: clips, takes, word-accurate captions, sound effects, music.

Usage (workflow/.venv/bin/python):  make_edit.py [--no-music] [--web]   -> edit.json / edit-nomusic.json / edit-web.json

SQUARE 1080 x 1080. Captions: the words are the SCRIPT's words (so the captions match the narration text exactly), and
each caption's time comes from Whisper's word times for that take. A take whose words differ from its script line
stops the script: that take said something else and must be regenerated.
Captions sit in the lower third, centred, Rammetto One 76 px, white with the orange outline, centred at y = 880:
above the bottom 10% of the frame and below the end card.
A line is said when the thing it is about is on screen (Elaine, 2026-11-27): every START below was set against the
PAINTED clip. Sound effects: one on the beats that matter, none on the faces in between, and every sound ends at
least 0.25 s before its clip does.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from check_narration import words, norm
from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[1]
SIZE, STROKE = 76, 10
FONT = ImageFont.truetype(str(WF / "assets" / "fonts" / "RammettoOne-Regular.ttf"), SIZE)
MAXW, MAXC = 980, 22
NOMUSIC = "--no-music" in sys.argv
WEB = "--web" in sys.argv
VERSION = "v14"     # Elaine on v13: the approved hands-on-hips look on the smirk at the end too (clip 8 repainted)
# Elaine on cut v5 (2026-11-27): "after every time arthur says smth there needs to be a pause ... be really aware of like
# the pauses make sure that the video flows nicely". In v5 "…challenge going?" and "Wait, are you…" were 0.19 s apart.
# Every line now has at least MIN_PAUSE of quiet before the next one starts, and the build stops if one does not.
MIN_PAUSE = 0.75

# clip file (in clips/), seconds used (whole frames at 24 fps).
# Cut v8: the narration is re-recorded with Eleven v4 (Elaine, 2026-11-27: "i changed the voice so in higgsfield u can now
# see we use eleven labs but i kept arthur. can we redo the voice lines"). Arthur reads slower there, so two lines are
# longer than the shots painted for them. Nothing is sped up and none of his pauses are cut: clip 6 runs 19 frames longer
# (clip 4 did too, by 6 frames, until it was re-shot at 3.8 s for v10). In v8 that was a held last frame (Elaine: "somehow its just frozen"); from v9 the last
# frames play back and forth instead (extend_tail.py), so the idle sway goes on. clips/04-comp-nohold.mp4 and
# 06-comp-nohold.mp4 are the clips before they are lengthened.
CLIPS = [["01-comp.mp4", 8.5], ["02-comp.mp4", 6.7917], ["03-comp.mp4", 4.0], ["04-comp.mp4", 3.7917], ["04b-comp.mp4", 2.9167],
         ["05-comp.mp4", 5.0], ["06-comp.mp4", 5.2917], ["07-comp.mp4", 6.7917], ["08-comp-web.mp4" if WEB else "08-comp.mp4", 11.5833]]
# take, clip index, start in that clip, the script's words for it (the caption text)
TAKES = [
    ("01a.wav", 0, 0.50, "Sol, how's the sandcastle challenge going?"),                # over Sol rushing about; then a second of just him
    ("01b.wav", 0, 4.60, "Wait, are you building the whole thing by yourself?"),       # as he stops and sags (4.75)
    ("02a.wav", 1, 1.25, "And that's your team?"),                                     # as the whip lands on the three of them
    ("02b.wav", 1, 3.30, "Okay, here are five things that'll fix this."),              # he plants his nubs on his sides at "five things" (4.4)
    ("03.wav", 2, 0.25, "First, split the project into small pieces."),
    ("04.wav", 3, 0.25, "Second, put one name on each piece."),                        # clip 4 is re-shot 3.8 s long, words painted on its signs
    ("05.wav", 5, 0.70, "Third, set a deadline before the real deadline."),
    ("06.wav", 6, 0.40, "Fourth, keep everything in one doc the whole team can see."),  # "Fourth," is off again before Sol rises past the caption band (0.96)
    ("07.wav", 7, 0.50, "And fifth, ask one specific person, instead of saying, can someone."),
    ("08.wav", 8, 1.70, "Ignite's free Social Impact and Project Development course teaches you how to take an idea and actually make it happen."),
]
# A first caption that waits (seconds into its take) although the voice has begun: in clip 8 "Ignite's free Social" would
# lie across the ribbon as it lands and across Sol's face as the camera cranes back past him (review of cut v6).
CAPTION_FROM = {"08.wav": 0.55}        # the line starts at 1.7 s; its first caption appears at 2.25 s, when the slow pull-back has passed Sol's face
# what Whisper may write for a script word (same sound)
SAME = {("thatll", "thatwill"), ("doc", "dock"), ("sol", "saul"), ("sol", "soul"), ("ignites", "ignites")}
S, B, T = "squeaks-tiny.mp3", "boing.mp3", "twinkle.mp3"
SQ = [(1.08, 1.19), (1.64, 1.76), (2.48, 2.56), (2.81, 2.91), (0.5, 0.74)]


def sq(i, clip, t, vol=0.32):
    return [S, SQ[i][0], SQ[i][1], clip, t, vol]


def boing(clip, t, vol=0.26):
    return [B, 0.0, 0.24, clip, t, vol]


def twinkle(clip, t, vol=0.18):
    return [T, 0.0, 1.24, clip, t, vol]


def emo(name, length, clip, t, vol=0.3):
    return [f"emo-{name}.mp3", 0.0, length, clip, t, vol]


SFX = [
    sq(0, 0, 0.3), sq(1, 0, 0.8), boing(0, 2.1), sq(2, 0, 2.95), sq(3, 0, 3.62), emo("sighing", 0.86, 0, 4.82),      # 1: pats, the bucket, more pats, the sag
    emo("bewilderment", 0.55, 1, 0.12), emo("sleepy", 1.3, 1, 1.35, 0.2), boing(1, 4.4, 0.2),                        # 2: the glare, the snoring three, squaring up
    emo("inspiration", 1.52, 2, 0.8), sq(1, 2, 1.7, 0.22), sq(2, 2, 2.1, 0.22), sq(3, 2, 2.5, 0.22),                 # 3: the bulb, the cards
    boing(3, 0.6, 0.2), boing(3, 1.7, 0.2), sq(0, 3, 2.2),                                                           # 4: two signs land; the question mark
    boing(4, 0.35, 0.2), emo("exclamation", 0.81, 4, 0.42), boing(4, 1.4, 0.2), emo("pleased", 0.72, 4, 1.78),       # 4b: sign, "me?", sign, pleased with himself
    emo("surprise", 1.13, 5, 0.5), boing(5, 2.75, 0.24), emo("pride", 1.03, 5, 3.5),                                 # 5: the tick, the board, smug
    sq(0, 6, 1.3), sq(1, 6, 1.8), sq(2, 6, 2.3), emo("exclamation", 0.81, 6, 3.1),                                   # 6: three arrive, the jolt awake
    boing(7, 1.35, 0.2), emo("exclamation", 0.81, 7, 2.2), sq(2, 7, 3.0), sq(0, 7, 3.55, 0.22), sq(1, 7, 3.95, 0.22),  # 7: the hop, "me?", the nod, off he hops
    emo("laughter", 0.9, 7, 4.9, 0.22),                                                                              #    the whistlers
    twinkle(8, 0.45, 0.2), sq(2, 8, 9.9), emo("pleased", 0.72, 8, 10.5),                                              # 8: the ribbon, the nod, the cheer
]


def width(text):
    return FONT.getlength(text) + 2 * STROKE


def key(w):
    return "".join(norm(w)).replace("'", "")


voice, spans = [], []
for take, clip, start, line in TAKES:
    heard = words(HERE / "audio" / "edit" / take)
    spoken = line.split()
    # join what Whisper split ("that will" for "that'll")
    i = 0
    while i < len(heard) - 1 and len(heard) > len(spoken):
        if (key(spoken[i]), key(heard[i][0] + heard[i + 1][0])) in SAME or key(spoken[i]) == key(heard[i][0] + heard[i + 1][0]):
            heard[i:i + 2] = [(heard[i][0] + heard[i + 1][0], heard[i][1], heard[i + 1][2])]
        i += 1
    if len(heard) != len(spoken):
        sys.exit(f"{take}: heard {len(heard)} words, the line has {len(spoken)}: {[w for w, _, _ in heard]}")
    for (hw, _, _), sw in zip(heard, spoken):
        if key(hw) != key(sw) and (key(sw), key(hw)) not in SAME:
            sys.exit(f"{take}: heard '{hw}' where the line says '{sw}'")
    times = [(a, b) for _, a, b in heard]
    at = sum(d_ for _, d_ in CLIPS[:clip]) + start
    spans.append((take, at + heard[0][1], at + heard[-1][2]))
    script = spoken
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
        phrases.append([round(times[g[0][1]][0], 2), round(times[g[-1][1]][1], 2), " ".join(w for w, _ in g)])
    for i in range(len(phrases) - 1):                                         # hold each caption until the next one starts
        if phrases[i + 1][0] - phrases[i][1] < 0.45:
            phrases[i][1] = phrases[i + 1][0]
    nxt = min([s_ for t_, c_, s_, _ in TAKES if c_ == clip and s_ > start] + [CLIPS[clip][1]])      # the next take in this clip, or the cut
    phrases[-1][1] = round(min(phrases[-1][1] + 0.3, nxt - start - 0.05), 2)
    phrases[0][0] = max(phrases[0][0], CAPTION_FROM.get(take, 0.0))
    assert " ".join(p[2] for p in phrases) == line
    voice.append({"take": take, "clip": clip, "start": start, "phrases": phrases})

# the pause after every line (the end of its last word to the start of the next line's first word)
short = []
print("pauses between lines:")
for (t0, _, e0), (t1, s1, _) in zip(spans, spans[1:]):
    print(f"  {t0} -> {t1}: {s1 - e0:.2f} s")
    if s1 - e0 < MIN_PAUSE:
        short.append(f"{t0} -> {t1}: only {s1 - e0:.2f} s")
if short:
    sys.exit("NOT ENOUGH PAUSE between lines (need %.2f s): %s" % (MIN_PAUSE, "; ".join(short)))
tag = ("-web" if WEB else "") + ("-nomusic" if NOMUSIC else "")
cfg = {
    "out": f"group-project-{VERSION}{tag}.mp4",
    "width": 1080, "height": 1080, "caption_size": SIZE, "caption_stroke": STROKE,
    # Music: a song no earlier video used (the tracker's Music column, both tabs, read 2026-11-27).
    "music": None if NOMUSIC else {"file": "So Happy World 4.mp3", "start": 0.0, "gain": 0.10},
    "voice_dir": "audio/edit", "sfx_dir": "../shower_curtain/audio/sfx",
    "caption_y": 730, "caption_max_width": MAXW, "caption_max_chars": MAXC,
    "clips": CLIPS, "voice": voice, "sfx": SFX,
}
out = HERE / f"edit{tag}.json"
out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("wrote", out.name, "total", round(sum(d for _, d in CLIPS), 2), "s")
for v in voice:
    print(v["take"], " | ".join(f"{p[2]} [{p[0]}-{p[1]}]" for p in v["phrases"]))
