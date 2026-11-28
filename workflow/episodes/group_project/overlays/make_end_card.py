#!/usr/bin/env python3
"""Draw the end card for the "Whole Group Project" ad, following Elaine's reusable end-card prompt (2026-11-26, kept
word for word in ../../all_due_this_week/end-card-prompt-elaine.txt), laid out for a SQUARE film.

  make_end_card.py                 -> art/end_card.png          (YouTube / social: "Link in description")
  make_end_card.py --web           -> art/end_card_web.png      (website / presentation: the sign-up address)
  make_end_card.py --name "Project & Nonprofit Building" --out end_card_pnb.png      another course name

Output: a 1080 x 1080 PNG, transparent outside the card. Her prompt gives the card's place for 16:9 (the right two
thirds) and 9:16 (the top two thirds); a square was not covered, so this follows the 16:9 rule: the card is on the right
60% and Sol stays on the left. It stops above the caption band, because the narrator is still talking while it is up.
  - rounded card in the Ignite site orange (#F07B2A)
  - top: the course's ORIGINAL card art, uncropped (Ignite Website/public/courses/Project and Nonprofit Building.jpeg)
  - the course name exactly as the website's course card writes it (src/data/program.ts): "Social Impact & Project
    Development" (the site gave this course's card art that name; "Project & Nonprofit Building" was the summer course)
  - big: "Join Ignite today!"     small: "Link in description" or the sign-up address without "https://"
  - fonts: Poppins and Rammetto One, the course cards' fonts. No em dashes, no slogans, no emojis.
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[2]
FONTS = WF / "assets" / "fonts"
ART = pathlib.Path.home() / "Documents" / "Ignite Website" / "public" / "courses" / "Project and Nonprofit Building.jpeg"
args = sys.argv[1:]
WEB = "--web" in args
COURSE = args[args.index("--name") + 1] if "--name" in args else "Social Impact & Project Development"
OUT = args[args.index("--out") + 1] if "--out" in args else ("end_card_web.png" if WEB else "end_card.png")
BIG = "Join Ignite today!"
SMALL = "forms.ignitefindyourfire.org/t/oqB8WMKbJ6us" if WEB else "Link in description"
ORANGE, WHITE, NAVY, CREAM = (240, 123, 42), (255, 253, 247), (27, 36, 71), (255, 243, 224)

W = H = 1080
X0, X1, R = 440, 1056, 44          # X1 is where the card's CONTENT ends; the orange itself runs off the right edge of the
BLEED = 1130                        # frame, so nothing behind it shows in a sliver beside it (Hat Sol's hat did, cut v2)
PAD, GAPS, FRAME = 28, (22, 20, 16), 5
INNER = X1 - X0 - 2 * PAD


def fit(text, path, width, start):
    size = start
    while size > 10 and ImageFont.truetype(path, size).getlength(text) > width:
        size -= 1
    return ImageFont.truetype(path, size)


def ink(text, font):
    l, t, r, b = font.getbbox(text)
    return l, t, r - l, b - t


# the course name on one line if it fits at a readable size, otherwise broken after "&"
f_name = fit(COURSE, str(FONTS / "Poppins-SemiBold.ttf"), INNER, 44)
lines = [COURSE]
if f_name.size < 36 and " & " in COURSE:
    a, b = COURSE.split(" & ", 1)
    lines = [a + " &", b]
    f_name = fit(max(lines, key=len), str(FONTS / "Poppins-SemiBold.ttf"), INNER, 44)
f_big = fit(BIG, str(FONTS / "RammettoOne-Regular.ttf"), INNER, 80)
f_small = fit(SMALL, str(FONTS / "Poppins-SemiBold.ttf"), INNER, 32)
src = Image.open(ART).convert("RGB")
art_w = INNER
art_h = round(art_w * src.height / src.width)          # uncropped: the art keeps its own shape
name_h = sum(ink(l, f_name)[3] for l in lines) + 12 * (len(lines) - 1)
card_h = 2 * PAD + art_h + sum(GAPS) + name_h + ink(BIG, f_big)[3] + ink(SMALL, f_small)[3]
Y0 = max(40, (790 - card_h) // 2 + 20)                 # sits above the caption band (captions are centred near y = 880)
Y1 = Y0 + card_h
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((X0 + 5, Y0 + 12, BLEED, Y1 + 12), R, fill=(40, 22, 10, 120))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
d = ImageDraw.Draw(im)
d.rounded_rectangle((X0, Y0, BLEED, Y1), R, fill=ORANGE + (255,))
cx = (X0 + X1) // 2


def put(text, font, y, fill, shadow=None):
    l, t, w, h = ink(text, font)
    x = cx - w / 2 - l
    if shadow:
        d.text((x + 2, y - t + 4), text, font=font, fill=shadow)
    d.text((x, y - t), text, font=font, fill=fill)
    return h


art = src.resize((art_w, art_h), Image.LANCZOS)
mask = Image.new("L", (art_w, art_h), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, art_w, art_h), 30, fill=255)
ax, ay = cx - art_w // 2, Y0 + PAD
d.rounded_rectangle((ax - FRAME, ay - FRAME, ax + art_w + FRAME, ay + art_h + FRAME), 34, fill=CREAM + (255,))
im.paste(art, (ax, ay), mask)
y = ay + art_h + GAPS[0]
for i, l in enumerate(lines):
    y += put(l, f_name, y, WHITE) + (12 if i < len(lines) - 1 else 0)
y += GAPS[1]
y += put(BIG, f_big, y, WHITE, shadow=(150, 66, 12)) + GAPS[2]
y += put(SMALL, f_small, y, NAVY)
(HERE / "art").mkdir(exist_ok=True)
im.save(HERE / "art" / OUT)
print(OUT, "card", (X0, Y0, X1, Y1), "art", (art_w, art_h), "name", lines, f_name.size, "big", f_big.size, "small", f_small.size, "last ink ends", round(y), "of", Y1 - PAD)
