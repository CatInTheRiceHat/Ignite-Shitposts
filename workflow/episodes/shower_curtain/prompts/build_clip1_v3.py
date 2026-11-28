#!/usr/bin/env python3
"""Paint prompt for clip 1, version 3 (2026-11-27). Elaine: "when sol has the furious eyes thats when narrator says sol
why are u mad". In version 2 the painter kept his eyes squeezed (> <) for almost a second after the gray clip had
switched to the glare, so the Narrator asked about a glare that was not there yet. Gray clip: 01-skeleton-v4.mp4 (the
glare from 3.0 s, held to 6.6 s, no stunned beat). This prompt states where the squeezed eyes END and that the glare
holds. The Narrator's start is then set from where the glare shows in the PAINTED clip.
Usage: build_clip1_v3.py -> writes 01-paint-v3.txt and prints the request JSON."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build as B
HERE = pathlib.Path(__file__).resolve().parent
M = json.loads((HERE / "media.json").read_text())
P1 = B.P1.replace("a star, yellow dashes)", "a star, yellow dashes, a red anger mark)")
BEATS = ("Beats: 1. CAMERA MOVE: the shot opens high up near the ceiling, looking down on the whole bathroom, and flies smoothly down "
         "across the room, over the curtain rod and into the tub, levelling out low in front of Sol at 2.2 seconds, exactly as in the "
         "source video. Only the camera moves; the room does not change. 2. From the first frame Sol stands in the tub near the "
         "curtain, swaying gently from side to side, and his eyes are " + B.ARC + ". From 1.0 second one pink music note and one blue "
         "music note float beside him. 3. From 1.75 to 2.1 seconds the near end of the curtain draws back a little, away from him. "
         "4. THE SLAP: at 2.2 seconds the near end of the curtain whips in fast and slaps flat against the side of Sol's face and "
         "body, exactly as the source shows. The music notes are gone. Sol is knocked sideways, tilted and squashed, with both arm "
         "nubs flung up; his eyes become two sideways chevrons with rounded tips, pointing at each other like > <, and two little "
         "fans of yellow dashes flash beside him. The camera jolts. The cloth stays pressed against him until 2.4 seconds, then peels "
         "off and swings back to hang at the left by 2.8 seconds, where it stays to the last frame. At 2.75 seconds the dashes are "
         "gone and he rocks back upright. PHYSICS RULE: the curtain is one sheet of cloth that swings in, hits him and swings back; "
         "it never tears, never wraps round him and never changes length. 5. THE GLARE: the chevron eyes END at 3.0 seconds. At 3.0 "
         "seconds he turns on the curtain and his eyes become " + B.GLARE + ". EYE RULE: from 3.0 seconds to the very last frame his "
         "eyes are these open slanted half-rings in EVERY frame, exactly as the source video shows; they are never chevrons, never "
         "closed and never round again. At the same moment his whole flame turns a deeper red, exactly as much as the source shows, "
         "and one small dark red anger mark, four short curved strokes in a cross, sits on the upper side of his face; the red and "
         "the mark stay to the last frame. He swells up taller and trembles, with both arm nubs raised. The camera pushes in quickly "
         "on him from 3.0 to 3.3 seconds, then only creeps closer. He stamps on the spot twice, at 3.9 and 4.3 seconds. 6. From 4.6 "
         "to 5.8 seconds he stands glaring at the curtain, trembling a little. At 5.8 seconds he turns a little and glances up toward "
         "the camera, still with the slanted half-ring eyes. " + B.GROUND +
         "ARM RULE: his arm nubs stay the same short stubs in every frame; he never holds anything. ")
p = P1 + B.SCENES["1"] + "\n\n" + BEATS + B.STYLE_REST + B.STYLE_END
assert "mouth" not in p.lower() and "smil" not in p.lower() and "happ" not in p.lower()
(HERE / "01-paint-v3.txt").write_text(p + "\n")
medias = [{"value": "be063282-cd46-42f6-9a07-b64646b74c9e", "role": "video_references"},
          {"value": M["style_frame_clip02_end_normal"], "role": "image_references"},
          {"value": M["turnaround"], "role": "image_references"},
          {"value": M["expr_strips"]["1"], "role": "image_references"},
          {"value": M["expr_strips"]["2"], "role": "image_references"}]
print(json.dumps([{"index": 1, "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p",
                   "aspect_ratio": "9:16", "medias": medias, "prompt": p}}]))
