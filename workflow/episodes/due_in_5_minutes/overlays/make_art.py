#!/usr/bin/env python3
"""Draw every piece of lettering for the ad ONCE, as PNGs with alpha, into overlays/art/.

The painter cannot be trusted with words, and the script says every piece made in clips 3 to 7 must match the
finished poster exactly. So the words are drawn here, one file per piece, and the same file is used in the clip
where Sol makes the piece and again on the poster in the last shot.
Run with workflow/.venv/bin/python (needs Pillow). Fonts are OFL (overlays/fonts/).
"""
import pathlib, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE / "art"
ART.mkdir(exist_ok=True)
# Patrick Hand, not Gochi Hand: in Gochi the "l" and "t" of "salt" and "melt" join and read as a capital H
# (found in the frame review of cut v1). Patrick Hand is thin, so every stroke is thickened a little.
HAND = str(HERE / "fonts" / "PatrickHand-Regular.ttf")
INK = (27, 36, 71, 255)            # Sol's navy
CARD_A, CARD_B, TAG = (255, 219, 168), (184, 222, 250), (204, 237, 189)


def font(px):
    return ImageFont.truetype(HAND, px)


def fit(text, width, start):
    px = start
    while font(px).getlength(text) > width:
        px -= 4
    return font(px)


def lines(size, rows, pad=0.06, gap=1.02):
    """Transparent image with centred lines of ink. rows = [(text, px)]."""
    w, h = size
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fonts = [fit(t, w * (1 - 2 * pad), px) for t, px in rows]
    hs = [f.size * gap for f in fonts]
    y = (h - sum(hs)) / 2
    for (t, _), f, lh in zip(rows, fonts, hs):
        d.text((w / 2, y + lh / 2), t, font=f, fill=INK, anchor="mm", stroke_width=max(1, f.size // 38), stroke_fill=INK)
        y += lh
    return im


def card(size, colour, rows, radius=0.16):
    """A paper card: soft shadow, coloured face, a darker edge, ink on top."""
    w, h = size
    m = int(h * 0.10)                                   # margin for the shadow
    im = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((m + m * 0.25, m + m * 0.45, m + w + m * 0.25, m + h + m * 0.45), radius * h, fill=(40, 30, 50, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(m * 0.35)))
    edge = tuple(int(c * 0.78) for c in colour) + (255,)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((m, m, m + w, m + h), radius * h, fill=colour + (255,), outline=edge, width=max(4, h // 60))
    im.alpha_composite(lines((w, h), rows), (m, m))
    return im


def scribble(d, x0, x1, y, seed, width):
    rnd = random.Random(seed)
    pts, x = [], x0
    while x < x1:
        pts.append((x, y + rnd.uniform(-9, 9)))
        x += rnd.uniform(18, 40)
    d.line(pts, fill=INK[:3] + (150,), width=width, joint="curve")


# 1. the question: two lines for the whiteboard, one line for the poster header
lines((1500, 820), [("Does salt make", 330), ("ice melt faster?", 330)]).save(ART / "title2.png")
lines((2400, 300), [("Does salt make ice melt faster?", 290)], pad=0.02).save(ART / "title1.png")

# 2. what changed and what was measured (the pop-up labels of clip 4, and the cards on the poster)
card((1240, 640), CARD_A, [("Changed:", 250), ("amount of salt", 200)]).save(ART / "card_changed.png")
card((1240, 640), CARD_B, [("Measured:", 250), ("minutes to melt", 200)]).save(ART / "card_measured.png")

# 3. the three trials
for i in (1, 2, 3):
    card((800, 300), TAG, [(f"Trial {i}", 210)], radius=0.22).save(ART / f"tag_trial{i}.png")

# 4. graph labels. Canvas = the graph sheet, 1.25 m x 1.3 m at 1000 px per metre; the bars and axes are geometry.
g = Image.new("RGBA", (1250, 1300), (0, 0, 0, 0))
d = ImageDraw.Draw(g)
f = font(96)
d.text((455, 1150), "plain ice", font=f, fill=INK, anchor="mm", stroke_width=max(1, f.size // 38), stroke_fill=INK)
d.text((865, 1150), "salted ice", font=f, fill=INK, anchor="mm", stroke_width=max(1, f.size // 38), stroke_fill=INK)
side = Image.new("RGBA", (800, 130), (0, 0, 0, 0))
ImageDraw.Draw(side).text((400, 65), "minutes to melt", font=font(96), fill=INK, anchor="mm", stroke_width=max(1, font(96).size // 38), stroke_fill=INK)
side = side.rotate(90, expand=True)
g.alpha_composite(side, (95 - side.width // 2, 620 - side.height // 2))
g.save(ART / "graph_labels.png")

# 5. the notebook page: heading and three lines of handwriting. Canvas = the page, 0.58 m x 0.8 m at 2000 px/m.
p = Image.new("RGBA", (1160, 1600), (0, 0, 0, 0))
d = ImageDraw.Draw(p)
d.text((580, 300), "What went", font=font(215), fill=INK, anchor="mm", stroke_width=max(1, font(215).size // 38), stroke_fill=INK)
d.text((580, 530), "wrong", font=font(215), fill=INK, anchor="mm", stroke_width=max(1, font(215).size // 38), stroke_fill=INK)
d.line((250, 670, 910, 670), fill=INK, width=14)
for k, y in enumerate((900, 1080, 1260)):
    scribble(d, 150, 1010 - 180 * (k == 2), y, 40 + k, 12)
p.save(ART / "page_wrong.png")

# contact sheet, to look at the pieces together
names = ["title2", "title1", "card_changed", "card_measured", "tag_trial1", "tag_trial2", "tag_trial3", "graph_labels", "page_wrong"]
sheet = Image.new("RGB", (1800, 1500), (236, 232, 222))
x = y = 20
rowh = 0
for n in names:
    im = Image.open(ART / f"{n}.png")
    k = min(560 / im.width, 420 / im.height)
    im = im.resize((int(im.width * k), int(im.height * k)))
    if x + im.width > 1780:
        x, y, rowh = 20, y + rowh + 20, 0
    sheet.paste(im, (x, y), im)
    x += im.width + 20
    rowh = max(rowh, im.height)
sheet.save(ART / "_contact.png")
print("wrote", len(names), "pieces to", ART)
