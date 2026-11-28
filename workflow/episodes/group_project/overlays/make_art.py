#!/usr/bin/env python3
"""Draw every piece of lettering for the "Whole Group Project" ad, once each, into art/ (transparent PNGs).

The painter never writes words. Each PNG sits on an OVL_ plane in the Blender scenes (skeleton/clips.py), is rendered
as its own pass for every frame (render_clip.py MODE=ovlseq) and laid over the painted clip (composite.py).
Ink only, except the four task cards and the "1st" badge, which are whole little cards (nothing painted under them).
Fonts: Rammetto One for printed signs (the banner, the clock boards), Patrick Hand for handwriting.
Usage: workflow/.venv/bin/python make_art.py
"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[2]
ART = HERE / "art"
ART.mkdir(exist_ok=True)
RAM = str(WF / "assets" / "fonts" / "RammettoOne-Regular.ttf")
HAND = str(HERE / "fonts" / "PatrickHand-Regular.ttf")
NAVY, CORAL, BLUE = (27, 36, 71, 255), (214, 84, 60, 255), (39, 96, 200, 255)


def canvas(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def fit(text, path, w, h, start=400):
    """The biggest font size at which text fits in w x h."""
    size = start
    while size > 8:
        f = ImageFont.truetype(path, size)
        l, t, r, b = f.getbbox(text)
        if r - l <= w and b - t <= h:
            return f
        size -= 2
    return ImageFont.truetype(path, 8)


def centre(d, text, font, cx, cy, fill):
    """Centred on cx. Vertically it is the CAPITAL height that is centred on cy, so every word in a row sits on the same
    baseline whether or not it has a g, p or y. (Elaine, 2026-11-27, on the TEAM SOL table: "make sure that the names
    are aligned correctly because some are spaced middle some up": each word had been centred on its own ink.)"""
    _, cap_top, _, cap_bot = font.getbbox("H")
    l, _, r, _ = font.getbbox(text)
    d.text((cx - (r - l) / 2 - l, cy - (cap_top + cap_bot) / 2), text, font=font, fill=fill)


def printed(name, text, w, h, fill=NAVY, pad=0.06):
    im, d = canvas(w, h)
    centre(d, text, fit(text, RAM, w * (1 - 2 * pad), h * (1 - 2 * pad * 2)), w / 2, h / 2, fill)
    im.save(ART / name)


def two_lines(name, top, bottom, w, h, fill_top=CORAL, fill_bottom=NAVY):
    im, d = canvas(w, h)
    f1 = fit(top, HAND, w * 0.86, h * 0.36)
    f2 = fit(bottom, HAND, w * 0.90, h * 0.40)
    centre(d, top, f1, w / 2, h * 0.28, fill_top)
    centre(d, bottom, f2, w / 2, h * 0.70, fill_bottom)
    im.save(ART / name)


# ---------------------------------------------------------------- little ink drawings
def tower(d, x, y, w, h, lw, fill=None, flag=None):
    """A castle tower standing on y (its base line), w wide and h tall, with three teeth on top."""
    d.rectangle((x - w / 2, y - h, x + w / 2, y), outline=NAVY, width=lw, fill=fill)
    tw = w / 5
    for i in (0, 2, 4):
        d.rectangle((x - w / 2 + i * tw, y - h - tw, x - w / 2 + (i + 1) * tw, y - h), outline=NAVY, width=lw, fill=fill)
    d.rounded_rectangle((x - w * 0.14, y - h * 0.62, x + w * 0.14, y - h * 0.34), w * 0.13, outline=NAVY, width=lw)
    if flag:
        d.line((x, y - h - tw, x, y - h - tw - w * 0.9), fill=NAVY, width=lw)
        d.polygon([(x, y - h - tw - w * 0.9), (x + w * 0.62, y - h - tw - w * 0.66), (x, y - h - tw - w * 0.42)], fill=flag, outline=NAVY)


def castle(d, cx, base, s, lw):
    tower(d, cx - 190 * s, base, 130 * s, 200 * s, lw)
    tower(d, cx + 190 * s, base, 130 * s, 200 * s, lw)
    tower(d, cx, base, 180 * s, 330 * s, lw, flag=CORAL)
    for x0, x1 in ((cx - 125 * s, cx - 90 * s), (cx + 90 * s, cx + 125 * s)):
        d.line((x0, base - 120 * s, x1, base - 120 * s), fill=NAVY, width=lw)
    d.line((cx - 330 * s, base, cx + 330 * s, base), fill=NAVY, width=lw)
    d.arc((cx - 46 * s, base - 110 * s, cx + 46 * s, base - 10 * s), 180, 360, fill=NAVY, width=lw)
    d.line((cx - 46 * s, base - 60 * s, cx - 46 * s, base), fill=NAVY, width=lw)
    d.line((cx + 46 * s, base - 60 * s, cx + 46 * s, base), fill=NAVY, width=lw)
    for i in range(3):                                           # the moat: three little waves
        x = cx - 250 * s + i * 190 * s
        d.arc((x, base + 22 * s, x + 110 * s, base + 62 * s), 200, 340, fill=BLUE, width=lw)


def icon(d, kind, cx, cy, s, lw):
    if kind == "towers":
        tower(d, cx - 46 * s, cy + 70 * s, 62 * s, 110 * s, lw)
        tower(d, cx + 46 * s, cy + 70 * s, 62 * s, 110 * s, lw)
    elif kind == "walls":
        d.rectangle((cx - 100 * s, cy - 10 * s, cx + 100 * s, cy + 70 * s), outline=NAVY, width=lw)
        for i in range(4):
            x = cx - 100 * s + i * 58 * s
            d.rectangle((x, cy - 42 * s, x + 28 * s, cy - 10 * s), outline=NAVY, width=lw)
    elif kind == "moat":
        for j in range(3):
            for i in range(3):
                x = cx - 105 * s + i * 72 * s + (18 * s if j % 2 else 0)
                y = cy - 40 * s + j * 44 * s
                d.arc((x, y, x + 66 * s, y + 36 * s), 200, 340, fill=BLUE, width=lw)
    elif kind == "flag":
        d.line((cx - 34 * s, cy - 80 * s, cx - 34 * s, cy + 78 * s), fill=NAVY, width=lw)
        d.polygon([(cx - 34 * s, cy - 80 * s), (cx + 78 * s, cy - 38 * s), (cx - 34 * s, cy + 4 * s)], fill=CORAL, outline=NAVY)


# ---------------------------------------------------------------- the pieces
printed("banner.png", "SANDCASTLE CHALLENGE", 3000, 273, fill=CORAL, pad=0.03)
printed("judging.png", "JUDGING 6:00", 1200, 360)
printed("doneby.png", "DONE BY 5:00", 1200, 360, fill=CORAL)

# the plan board in clips 1 to 3: a drawing of the whole castle
im, d = canvas(1300, 920)
castle(d, 650, 800, 1.42, 9)                    # no title: the flag needs the room at the top
im.save(ART / "plan_castle.png")

# the four task cards that pop out of it (whole cards: paper, a little drawing, the word)
for kind, word, paper in (("towers", "Towers", (255, 219, 168)), ("walls", "Walls", (184, 222, 250)),
                          ("moat", "Moat", (204, 237, 189)), ("flag", "Flag", (255, 240, 158))):
    im, d = canvas(870, 570)
    d.rounded_rectangle((16, 22, 866, 566), 44, fill=(60, 40, 20, 70))                 # a soft shadow
    d.rounded_rectangle((6, 6, 856, 550), 44, fill=paper + (255,), outline=(120, 90, 60, 255), width=5)
    icon(d, kind, 205, 275, 1.3, 9)
    centre(d, word, fit(word, HAND, 390, 200), 615, 270, NAVY)
    im.save(ART / f"card_{kind}.png")

# the plan board from clip 6 on: the team doc, with the course's own three columns (Task / Team Member / Due)
im, d = canvas(1300, 920)
centre(d, "TEAM SOL", fit("TEAM SOL", HAND, 560, 120), 650, 86, NAVY)
X, Y0, RH = (60, 470, 900, 1240), 170, 148
for i in range(6):
    d.line((X[0], Y0 + i * RH, X[3], Y0 + i * RH), fill=NAVY, width=7 if i in (0, 1, 5) else 4)
for x in X:
    d.line((x, Y0, x, Y0 + 5 * RH), fill=NAVY, width=7 if x in (X[0], X[3]) else 4)
rows = (("Task", "Who", "Done by"), ("Towers", "Ring Sol", "4:00"), ("Walls", "Hat Sol", "4:30"), ("Moat", "Sleepy Sol", "4:45"), ("Flag", "Me", "5:00"))
f_head, f_row = ImageFont.truetype(HAND, 92), ImageFont.truetype(HAND, 96)
for r, row in enumerate(rows):
    for c, text in enumerate(row):
        centre(d, text, f_head if r == 0 else f_row, (X[c] + X[c + 1]) / 2, Y0 + (r + 0.5) * RH, CORAL if r == 0 else NAVY)
im.save(ART / "plan_table.png")

# the four name signs of clip 4 (ink only: the painted sign is a blank card on a stick)
for name, top, bottom in (("moat", "Moat:", "Sleepy Sol"), ("walls", "Walls:", "Hat Sol"), ("towers", "Towers:", "Ring Sol"), ("flag", "Flag:", "Me")):
    two_lines(f"sign_{name}.png", top, bottom, 930, 540)

# the blue ribbon's middle (ink only: the painted rosette has a plain cream middle)
im, d = canvas(300, 300)
centre(d, "1st", fit("1st", RAM, 230, 170), 150, 150, BLUE)
im.save(ART / "first.png")

for p in sorted(ART.glob("*.png")):
    print(p.name, Image.open(p).size)
