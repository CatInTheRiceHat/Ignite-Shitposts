#!/usr/bin/env python3
"""Cut a strip of just the faces each clip uses from the expression sheet (labels left off: a labelled sheet invites
the painter to write). Usage: workflow/.venv/bin/python make_strips.py  ->  expr-clip0N.png"""
import pathlib
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
SHEET = Image.open(HERE.parents[2] / "assets" / "sol-3d" / "eyes" / "sol-eyes-expressions-v9.png").convert("RGB")
ORDER = ("normal squeeze surprised sparkle worried shocked angry furious determined sad crying gloomy heartbroken happy joy "
         "excited laughing singing awe love wink content shy bashful idea thinking confused startled amazed nervous panic scared "
         "sleepy asleep smug sigh dizzy ko").split()
CLIPS = {
    1: "normal determined panic sigh",
    2: "normal angry sleepy determined content asleep",
    3: "normal thinking idea",
    4: "normal asleep confused content startled smug",
    5: "normal surprised smug determined",
    6: "normal surprised asleep startled happy",
    7: "normal startled determined sleepy singing nervous",
    8: "normal sparkle happy joy",
}
for clip, names in CLIPS.items():
    names = names.split()
    strip = Image.new("RGB", (300 * len(names), 343), (238, 235, 229))
    for i, n in enumerate(names):
        k = ORDER.index(n)
        x, y = (k % 8) * 300, (k // 8) * 387
        strip.paste(SHEET.crop((x, y, x + 300, y + 343)), (i * 300, 0))
    strip.save(HERE / f"expr-clip0{clip}.png")
    print(clip, names, strip.size)
