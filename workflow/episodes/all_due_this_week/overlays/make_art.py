#!/usr/bin/env python3
"""Draw every piece of lettering for the "All Due This Week" ad ONCE, as PNGs with alpha, into overlays/art/.

The painter cannot be trusted with words, so every word in the film is drawn here and laid over the painted clips
(overlays/composite.py). Each piece is INK ONLY on a transparent canvas: the paper, sticky note, box or board under
it is real geometry in the skeleton, painted blank. The same file is used every time the piece appears (the math
homework's note is the same note in the pile, on the floor, on the kitchen table and on the tidy desk).
Run with workflow/.venv/bin/python (needs Pillow). Handwriting: Patrick Hand (OFL, overlays/fonts/).
"""
import math, pathlib, random
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE / "art"
ART.mkdir(exist_ok=True)
HAND = str(HERE / "fonts" / "PatrickHand-Regular.ttf")
# The rough-draft sketch is small and seen at an angle: there Patrick Hand's "g" (a straight tail, no hook) read as a
# "q" ("Rouqh draft", "Our Biq Idea": the independent frame review of cut v1). Caveat Brush has a looped g.
SKETCH = str(HERE / "fonts" / "CaveatBrush-Regular.ttf")
INK = (27, 36, 71, 255)            # Sol's navy
RED = (214, 66, 56, 255)
GREEN = (58, 150, 84, 255)
MARKER = (62, 44, 30, 255)         # dark brown marker on cardboard


def font(px, face=None):
    return ImageFont.truetype(face or HAND, px)


def fit(text, width, start, face=None):
    px = start
    while font(px, face).getlength(text) > width:
        px -= 4
    return font(px, face)


def lines(size, rows, pad=0.06, gap=0.98, ink=INK, bold=38, top=None, face=None):
    """Transparent image with centred lines of ink. rows = [(text, px)]. bold: stroke = size / bold."""
    w, h = size
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fonts = [fit(t, w * (1 - 2 * pad), px, face) for t, px in rows]
    hs = [f.size * gap for f in fonts]
    y = (h - sum(hs)) / 2 if top is None else top
    for (t, _), f, lh in zip(rows, fonts, hs):
        d.text((w / 2, y + lh / 2), t, font=f, fill=ink, anchor="mm", stroke_width=max(1, f.size // bold), stroke_fill=ink)
        y += lh
    return im


def wobbly(d, pts, seed, fill=INK, width=12, jitter=5, step=70):
    """A hand-drawn line through pts: each segment is broken into short pieces that wander a little."""
    rnd = random.Random(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            k = i / n
            out.append((x0 + (x1 - x0) * k + rnd.uniform(-jitter, jitter), y0 + (y1 - y0) * k + rnd.uniform(-jitter, jitter)))
    out.append(pts[-1])
    d.line(out, fill=fill, width=width, joint="curve")


# 1. sticky notes (0.62 m x 0.44 m at 2000 px/m): the labels of the math homework and the group project
lines((1240, 880), [("Math", 430), ("homework", 400)]).save(ART / "note_math.png")
lines((1240, 880), [("Group", 430), ("project", 400)]).save(ART / "note_group.png")
lines((1000, 1000), [("Plan B", 420)]).save(ART / "note_planb.png")                       # the sticky on the tidy desk

# 2. the calendar page (0.9 m x 1.0 m at 2000 px/m). The red band across the top is geometry.
c = Image.new("RGBA", (1800, 2000), (0, 0, 0, 0))
c.alpha_composite(lines((1800, 1100), [("TEST", 520), ("FRIDAY", 470)], pad=0.2, bold=34), (0, 640))
d = ImageDraw.Draw(c)
ring = [(900 + 790 * math.cos(a / 40 * 2 * math.pi + 0.3), 1200 + 610 * math.sin(a / 40 * 2 * math.pi + 0.3)) for a in range(43)]
wobbly(d, ring, 3, fill=RED, width=26, jitter=8, step=90)
c.save(ART / "cal_test.png")

# 3. sheet music (0.85 m x 1.05 m at 2000 px/m): staves and notes, no words
m = Image.new("RGBA", (1700, 2100), (0, 0, 0, 0))
d = ImageDraw.Draw(m)
rnd = random.Random(11)
d.line((500, 170, 1200, 170), fill=INK, width=16)                     # the title, a plain line
for s in range(5):
    y0 = 400 + 330 * s
    for k in range(5):
        d.line((150, y0 + 34 * k, 1550, y0 + 34 * k), fill=INK, width=7)
    for bx in (150, 620, 1090, 1550):
        d.line((bx, y0, bx, y0 + 136), fill=INK, width=9)
    x = 230
    while x < 1500:
        ny = y0 + 17 * rnd.randrange(0, 9)
        d.ellipse((x - 26, ny - 19, x + 26, ny + 19), fill=INK)
        up = ny > y0 + 68
        d.line((x + (22 if up else -22), ny, x + (22 if up else -22), ny + (-120 if up else 120)), fill=INK, width=8)
        x += rnd.choice((95, 120, 150))
m.save(ART / "music.png")

# 4. the three boxes (label plane 1.04 m x 0.42 m at 2000 px/m), dark marker on cardboard
for name in ("Control", "Influence", "Accept"):
    lines((2080, 840), [(name, 600)], pad=0.03, ink=MARKER, bold=27).save(ART / f"box_{name.lower()}.png")

# 5. the whiteboard (each block 1.1 m x 0.56 m at 2000 px/m)
lines((2200, 1120), [("Plan A:", 390), ("finish project", 340), ("Thursday", 340)], pad=0.02, bold=36).save(ART / "plan_a.png")
lines((2200, 1120), [("Plan B:", 390), ("ask my group to", 340), ("split the poster", 340)], pad=0.02, bold=36).save(ART / "plan_b.png")

# 6. the rough-draft sketch of the group poster (paper 1.3 m x 1.0 m at 2000 px/m)
s = Image.new("RGBA", (2600, 2000), (0, 0, 0, 0))
d = ImageDraw.Draw(s)
s.alpha_composite(lines((1200, 330), [("Rough draft", 330)], pad=0.0, bold=60, face=SKETCH), (110, 50))
wobbly(d, [(130, 385), (1250, 372)], 1, width=16)                                        # underline
wobbly(d, [(170, 520), (2440, 500), (2460, 1880), (150, 1900), (170, 520)], 2, width=18, jitter=9)   # the poster's outline
s.alpha_composite(lines((1000, 260), [("Our Plan", 260)], pad=0.0, bold=60, face=SKETCH), (300, 580))        # a title, crossed out
wobbly(d, [(280, 720), (1280, 690)], 4, fill=RED, width=20)
wobbly(d, [(300, 760), (1260, 660)], 5, fill=RED, width=16)
s.alpha_composite(lines((1000, 260), [("Our Big Idea", 260)], pad=0.0, bold=60, face=SKETCH), (300, 860))     # the second try
for k, y in enumerate((1220, 1380, 1540)):                                             # wobbly lines of "writing"
    wobbly(d, [(320, y), (1250 - 220 * (k == 2), y - 10)], 6 + k, width=14, jitter=8, step=60)
box = [(1500, 700), (2300, 680), (2320, 1280), (1490, 1300), (1500, 700)]               # a lopsided picture box
wobbly(d, box, 9, width=16, jitter=8)
star = [(1900 + (250 if i % 2 == 0 else 105) * math.sin(i * math.pi / 5), 985 - (250 if i % 2 == 0 else 105) * math.cos(i * math.pi / 5)) for i in range(11)]
wobbly(d, star, 10, width=16, jitter=7, step=80)
wobbly(d, [(1560, 1440), (2260, 1430)], 12, width=14, step=60)                         # a caption line, scribbled out
wobbly(d, [(1540, 1500), (1700, 1390), (1840, 1500), (1990, 1390), (2130, 1500), (2280, 1390)], 13, fill=RED, width=14)
wobbly(d, [(1340, 1700), (1480, 1560), (1480, 1640)], 14, width=14, jitter=6)           # an arrow
wobbly(d, [(1340, 1700), (1500, 1720)], 15, width=14, jitter=6)
s.save(ART / "sketch.png")

# 7. the check mark on the finished homework (0.5 m x 0.5 m)
k = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
d = ImageDraw.Draw(k)
d.line([(170, 540), (410, 790), (850, 220)], fill=GREEN, width=120, joint="curve")
for x, y in ((170, 540), (850, 220)):
    d.ellipse((x - 60, y - 60, x + 60, y + 60), fill=GREEN)
k.save(ART / "check.png")

# contact sheet, to look at the pieces together
names = ["note_math", "note_group", "note_planb", "cal_test", "music", "box_control", "box_influence", "box_accept",
         "plan_a", "plan_b", "sketch", "check"]
sheet = Image.new("RGB", (2200, 1700), (236, 226, 200))
x = y = 20
rowh = 0
for n in names:
    im = Image.open(ART / f"{n}.png")
    q = min(520 / im.width, 400 / im.height)
    im = im.resize((int(im.width * q), int(im.height * q)))
    if x + im.width > 2180:
        x, y, rowh = 20, y + rowh + 20, 0
    sheet.paste(im, (x, y), im)
    x += im.width + 20
    rowh = max(rowh, im.height)
sheet.save(ART / "_contact.png")
print("wrote", len(names), "pieces to", ART)
