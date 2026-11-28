#!/usr/bin/env python3
"""Paint prompt for clip 4, version 2 (2026-11-27). Elaine on version 1: "can we get rid of the water puddle appearing
lol redo the clip" (a puddle faded in under Sol near the end), and earlier "the dizzy animation is very sudden so just
remove that". The gray clip is 04-skeleton-v3.mp4 (no dizzy, no snap zoom). The style frame is the wide view of the
first paint, taken before the puddle appeared, so the set stays the one she has seen.
Usage: build_clip4_v2.py -> writes 04-paint-v2.txt and prints the request JSON."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build as B
HERE = pathlib.Path(__file__).resolve().parent
M = json.loads((HERE / "media.json").read_text())
P1 = B.P1.replace("(the turnaround sheet shows his shape from every side; the strip of faces shows every eye shape he makes in this shot)",
                  "(the turnaround sheet shows his shape from every side)")
assert P1 != B.P1
DRY = ("DRY FLOOR RULE: the floor under and around Sol is dry and white in every frame, from the first to the last, with only his "
       "soft shadow under his feet. No water, no puddle and no wet patch ever appears or grows near him. The only water on the floor "
       "is the one round puddle at the right where the spray lands, and it stays the same size. ")
BEATS = ("Beats: 1. CAMERA MOVE: the shot opens low on the tub floor, moving toward Sol, who stands facing the camera in front of the "
         "tiled end wall. The camera rises in front of his face at 1.0 second, then from 1.4 to 2.6 seconds swings out sideways to a "
         "wide view from outside the tub, and from 2.6 seconds to the last frame it eases in very slowly, exactly as in the source "
         "video. There is no sudden zoom. 2. At 1.0 second his eyes become " + B.RING + ", two little fans of yellow dashes appear "
         "above his sides, and he raises both arm nubs; at 1.8 seconds the dashes are gone and his eyes are two navy ovals again, and "
         "they stay two navy ovals to the last frame. 3. In the wide view the steam puffs travel round in ONE big slow wheel in front "
         "of the curtain: down beside the spray at the right, along the tub floor to the left, up in front of Sol, and back along the "
         "top to the right. The middle of the wheel stays empty. 4. Sol stands at the left, small, facing the camera. From 2.6 "
         "seconds to the last frame he leans his whole body round in slow circles, his eyes following a puff round the wheel. He "
         "blinks once at 4.4 seconds. " + DRY + B.GROUND + B.ARMS)
STYLE = ("\n\nStyle: the painted reference frame is the wide view of THIS shot as it must look from 2.6 seconds on. Match it "
         "exactly: the same tub and white tiled floor, the same aqua tiles, the same yellow curtain on its rod, the same shower "
         "head and spray at the right, the same cream wall above, the same paint treatment and light, and the same Sol standing on "
         "a dry floor. Take every pose and the steam puffs from the source video. ")
p = P1 + B.SCENES["4"] + "\n\n" + BEATS + STYLE + B.STYLE_END
assert "mouth" not in p.lower() and "smil" not in p.lower() and "happ" not in p.lower()
(HERE / "04-paint-v2.txt").write_text(p + "\n")
medias = [{"value": "5b1e8723-cd1d-4ac5-83b6-6bbeb937374c", "role": "video_references"},
          {"value": "1205bf44-41cb-4e4c-9323-52b196465160", "role": "image_references"},
          {"value": M["turnaround"], "role": "image_references"}]
print(json.dumps([{"index": 4, "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p",
                   "aspect_ratio": "9:16", "medias": medias, "prompt": p}}]))
