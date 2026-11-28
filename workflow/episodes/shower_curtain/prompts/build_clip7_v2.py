#!/usr/bin/env python3
"""Paint prompt for the ending, version 2 (2026-11-27). Elaine: "i stil feel like the ending is kind of chopped so
instead of having sol like react immediately can we have him look up and nod before mkaing happy face".
Gray clip: skeleton/07-skeleton-v3.mp4 (clips.py clip8). Style frame: the normal-face frame of clip 2.
Usage: build_clip7_v2.py -> writes 07-paint-v2.txt and prints the request JSON."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build as B
HERE = pathlib.Path(__file__).resolve().parent
M = json.loads((HERE / "media.json").read_text())
P1 = B.P1.replace("(the turnaround sheet shows his shape from every side; the strip of faces shows every eye shape he makes in this shot)",
                  "(the turnaround sheet shows his shape from every side)")
assert P1 != B.P1
BEATS = ("Beats: 1. CAMERA: one steady shot. The camera faces Sol from the first frame and only eases slowly closer to him until the "
         "last frame, exactly as in the source video. It never swings, jumps or changes angle, and the curtain, the wall and the "
         "shower stay in the same places in the frame the whole time. 2. Sol stands on the tub floor beside the curtain's cream hem. "
         "For the first 0.35 seconds he is turned a little toward the curtain and looks sideways at its hem; his eyes are two navy "
         "ovals. 3. From 0.35 to 0.7 seconds he turns to face the camera, tilts back and looks UP above the camera. He holds that "
         "upward look, listening, with a very small slow sway, until 2.9 seconds. His eyes stay two navy ovals. He blinks once at 1.6 "
         "seconds. 4. From 2.95 to 3.45 seconds he nods once, clearly: his whole body dips forward and comes back up, and his eyes "
         "are still two navy ovals. 5. At 3.75 seconds his eyes become " + B.ARC + ", he gives one small bounce with both arm nubs "
         "lifted, and two little fans of yellow dashes appear above his sides; at 4.3 seconds the dashes are gone and his nubs are "
         "down. His eyes stay " + B.ARC + " to the last frame. PUDDLE RULE: the shallow pale-blue puddle under his feet is there in "
         "the first frame, exactly as in the reference frame, and stays the same size and shape to the last frame; nothing else "
         "appears on the floor. " + B.GROUND + B.ARMS)
p = P1 + B.SCENES["7"] + "\n\n" + BEATS + B.STYLE_REST + B.STYLE_END
assert "mouth" not in p.lower() and "smil" not in p.lower() and "happ" not in p.lower()
(HERE / "07-paint-v2.txt").write_text(p + "\n")
medias = [{"value": "abe640a5-022e-4201-8bb5-ff77188d48f6", "role": "video_references"},
          {"value": M["style_frame_clip02_end_normal"], "role": "image_references"},
          {"value": M["turnaround"], "role": "image_references"}]
print(json.dumps([{"index": 7, "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p",
                   "aspect_ratio": "9:16", "medias": medias, "prompt": p}}]))
