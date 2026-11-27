#!/usr/bin/env python3
"""Draw the end card for the "All Due This Week" ad, following Elaine's reusable end-card prompt (2026-11-26, kept
word for word in ../end-card-prompt-elaine.txt).

  make_end_card.py                 -> art/end_card.png          (YouTube / social: "Link in description")
  make_end_card.py --web           -> art/end_card_web.png      (website / presentation: the sign-up address)

Output: a 1920 x 1080 PNG, transparent outside the card, so it sits on top of the final shot. The card is on the
right two thirds; the left third is clear for Sol, who nods next to it.
  - rounded card in the Ignite site orange (#F07B2A, --primary-orange in the website's index.css)
  - top: the course's ORIGINAL card art, uncropped (Ignite Website/public/courses/Resilience & Stress Management.jpg,
    2752 x 1536), rounded corners
  - the course name exactly as the website's course card writes it (src/data/program.ts)
  - big: "Join Ignite today!"     small: "Link in description" or the sign-up address
  - fonts: Poppins (the site's heading font, used for course-card titles) and Rammetto One (the site's title font)
The card stops above the caption band, because the narrator is still talking (with captions) while it is up.
In the edit it slides in from the right over about half a second and holds to the end (composite.py).
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[2]
FONTS = WF / "assets" / "fonts"
ART = pathlib.Path.home() / "Documents" / "Ignite Website" / "public" / "courses" / "Resilience & Stress Management.jpg"
WEB = "--web" in sys.argv
COURSE = "Resilience & Stress-Management"            # as written on the website's course card
BIG = "Join Ignite today!"
SMALL = "forms.ignitefindyourfire.org/t/oqB8WMKbJ6us" if WEB else "Link in description"
ORANGE, WHITE, NAVY, CREAM = (240, 123, 42), (255, 253, 247), (27, 36, 71), (255, 243, 224)

W, H = 1920, 1080
X0, X1, Y0, Y1 = 668, 1892, 28, 824                 # the card: the right two thirds, above the caption band
R = 60
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((X0 + 6, Y0 + 16, X1 + 6, Y1 + 16), R, fill=(40, 22, 10, 120))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
d = ImageDraw.Draw(im)
d.rounded_rectangle((X0, Y0, X1, Y1), R, fill=ORANGE + (255,))

f_name = ImageFont.truetype(str(FONTS / "Poppins-SemiBold.ttf"), 50)
f_big = ImageFont.truetype(str(FONTS / "RammettoOne-Regular.ttf"), 92)
f_small = ImageFont.truetype(str(FONTS / "Poppins-SemiBold.ttf"), 38)


def ink(text, font):
    l, t, r, b = font.getbbox(text)
    return l, t, r - l, b - t


def put(text, font, cx, y, fill, shadow=None):
    """Draw text with its ink centred on cx and its ink top at y. Returns the ink height."""
    l, t, w, h = ink(text, font)
    x = cx - w / 2 - l
    if shadow:
        d.text((x + 3, y - t + 5), text, font=font, fill=shadow)
    d.text((x, y - t), text, font=font, fill=fill)
    return h


PAD = 34                                             # the same margin above the art and below the last line
GAPS = (24, 22, 18)                                  # art to name, name to big, big to small
text_h = ink(COURSE, f_name)[3] + ink(BIG, f_big)[3] + ink(SMALL, f_small)[3]
art_h = (Y1 - Y0) - 2 * PAD - sum(GAPS) - text_h
src = Image.open(ART).convert("RGB")
art_w = round(art_h * src.width / src.height)        # uncropped: the art keeps its own shape
art = src.resize((art_w, art_h), Image.LANCZOS)
mask = Image.new("L", (art_w, art_h), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, art_w, art_h), 40, fill=255)
cx = (X0 + X1) // 2
ax, ay = cx - art_w // 2, Y0 + PAD
d.rounded_rectangle((ax - 6, ay - 6, ax + art_w + 6, ay + art_h + 6), 46, fill=CREAM + (255,))     # a thin cream frame
im.paste(art, (ax, ay), mask)
y = ay + art_h + GAPS[0]
y += put(COURSE, f_name, cx, y, WHITE) + GAPS[1]
y += put(BIG, f_big, cx, y, WHITE, shadow=(150, 66, 12)) + GAPS[2]
y += put(SMALL, f_small, cx, y, NAVY)
(HERE / "art").mkdir(exist_ok=True)
out = HERE / "art" / ("end_card_web.png" if WEB else "end_card.png")
im.save(out)
print(out.name, im.size, "card", (X0, Y0, X1, Y1), "art", (art_w, art_h), "last ink ends", round(y), "of", Y1 - PAD)
