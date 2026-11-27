#!/usr/bin/env python3
"""Lay the PNGs from render_expressions.py out as one labelled sheet.

Run:  ../../../.venv/bin/python make_sheet.py <renders_dir> <sheet.png> [columns]
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

src, out = pathlib.Path(sys.argv[1]), sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8
files = sorted(src.glob("*.png"))
font = ImageFont.truetype(str(pathlib.Path(__file__).resolve().parents[2] / "fonts" / "Poppins-SemiBold.ttf"), 26)
CW, CH, LAB = 300, 343, 44
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * CW, rows * (CH + LAB)), (250, 246, 238))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    x, y = (i % cols) * CW, (i // cols) * (CH + LAB)
    sheet.paste(Image.open(f).convert("RGB").resize((CW, CH), Image.LANCZOS), (x, y))
    label = f.stem.split("-", 1)[1]
    d.text((x + (CW - d.textlength(label, font=font)) / 2, y + CH + 4), label, font=font, fill=(27, 36, 71))
sheet.save(out)
print("sheet", sheet.size, len(files), "poses")
