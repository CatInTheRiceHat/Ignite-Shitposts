#!/usr/bin/env python3
"""Draw the course card that appears in the payoff (script: "Course card + sign-up link appear at 0:33. The link is
on screen only, not spoken"). Writes overlays/art/course_card.png, 1760 x 800 with alpha (shown at 880 x 400).

The picture is the course's own card art from the website (Ignite Website/public/courses/Science Research.jpeg).
The link is the site's courses page; /apply redirects there too.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
WF = HERE.parents[2]
FONTS = WF / "assets" / "fonts"
ART = pathlib.Path.home() / "Documents" / "Ignite Website" / "public" / "courses" / "Science Research.jpeg"
LINK = "ignitefindyourfire.org/program"
NAVY, ORANGE, WHITE = (27, 36, 71), (240, 123, 42), (255, 253, 247)

W, H, M = 1760, 800, 60                     # M: margin kept clear for the shadow
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((M + 10, M + 22, W - M + 10, H - M + 22), 70, fill=(30, 25, 50, 130))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
d = ImageDraw.Draw(im)
d.rounded_rectangle((M, M, W - M, H - M), 70, fill=WHITE + (255,), outline=ORANGE + (255,), width=12)

# course art, cropped to the mascot at his bench, with rounded corners
src = Image.open(ART).convert("RGB")
side = 600
crop = src.crop((1500, 260, 2700, 1460)).resize((side, side), Image.LANCZOS)
mask = Image.new("L", (side, side), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, side, side), 48, fill=255)
im.paste(crop, (M + 40, (H - side) // 2), mask)

x0 = M + 40 + side + 50
xr = W - M - 50
top, bottom = (H - side) // 2, (H + side) // 2            # the text column runs the height of the picture
f_badge = ImageFont.truetype(str(FONTS / "RammettoOne-Regular.ttf"), 58)
f_title = ImageFont.truetype(str(FONTS / "Poppins-SemiBold.ttf"), 86)
f_link = ImageFont.truetype(str(FONTS / "Poppins-SemiBold.ttf"), 54)
TITLE = ("Scientific Research", "& Data Analysis")
while max(f_title.getlength(t) for t in TITLE) > xr - x0:
    f_title = ImageFont.truetype(str(FONTS / "Poppins-SemiBold.ttf"), f_title.size - 2)
while f_link.getlength(LINK) > xr - x0:
    f_link = ImageFont.truetype(str(FONTS / "Poppins-SemiBold.ttf"), f_link.size - 2)


def ink(text, font):
    """The box the letters actually fill, so spacing is measured from the ink and not from the font's line box."""
    l, t, r, b = font.getbbox(text)
    return l, t, r - l, b - t


def put(text, font, x, y, fill):
    l, t, w, h = ink(text, font)
    d.text((x - l, y - t), text, font=font, fill=fill)
    return h


# Elaine, 2026-11-26: "make the spacing the same". The badge's letters get the same padding on all four sides, and
# the four spaces in the column (above the badge, badge to title, title to link, below the link) are equal.
PAD = 26
_, _, bw_, bh_ = ink("FREE COURSE", f_badge)
badge_h = bh_ + 2 * PAD
line_gap = 22
title_h = sum(ink(t, f_title)[3] for t in TITLE) + line_gap
link_h = ink(LINK, f_link)[3]
space = (bottom - top - badge_h - title_h - link_h) / 4
y = top + space
d.rounded_rectangle((x0, y, x0 + bw_ + 2 * PAD, y + badge_h), badge_h / 2, fill=ORANGE + (255,))
put("FREE COURSE", f_badge, x0 + PAD, y + PAD, WHITE)
y += badge_h + space
for t in TITLE:
    y += put(t, f_title, x0, y, NAVY) + line_gap
y += space - line_gap
put(LINK, f_link, x0, y, ORANGE)
(HERE / "art").mkdir(exist_ok=True)
im.save(HERE / "art" / "course_card.png")
print("course card", im.size, "title", f_title.size, "link", f_link.size, "equal space", round(space))
