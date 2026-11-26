#!/usr/bin/env python3
"""Build the version 2 paint prompts and the Higgsfield request list.

Usage: build_v2.py <style_media_id> <turnaround_media_id> clip=<skeleton_media_id> [clip=<id> ...]
Writes prompts/v2-<clip>-paint.txt for each clip named and prints the requests as JSON.
"First" clips (painted before a style frame from this episode exists) pass STYLE_NOTE_FIRST by adding first=1.
Paint prompt rules are in guidelines/current-rules.md: never the word for the opening under a nose, no mood
words, numbered beats, physics as rules, every prop's place named.
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P1 = ("Repaint this blockout video as a finished hand-painted gouache animation. VERTICAL 9:16 portrait frame, frame for frame: "
      "keep the exact camera move, framing, timing and every pose from the source video, and paint only what each source frame shows, "
      "adding no other characters or objects.\n\n"
      "Character: the flame-shaped figure is Sol, exactly the mascot in the reference images (use the turnaround sheet for his shape from "
      "every side). Round, plump gumdrop body with a red outer layer, an orange middle layer and a broad cream inner flame for the face. "
      "His face is plain smooth cream with exactly two small tall navy #1C2447 oval eyes set low and close together, solid dark with no "
      "whites or highlights, and nothing else on it. Short stubby rounded red-orange arm nubs and two tiny blunt stubby red feet. Sol gives "
      "off no sparks, particles or smoke. His layers and face move together as one body with a small soft wobble that settles.\n\n")
ROOM = ("Scene: a bright, cozy kitchen on a sunny morning. A smooth white stone counter fills the lower part of the frame. Behind it is a "
        "wall of soft sage-green square tiles, and where the source video shows a window above the tiles it is a wooden-framed window with "
        "warm morning sunlight. Warm sunlight with soft cool shadows, so the room has depth and glow. ")
MUGTXT = ("The pale blue cylinder is a pale blue ceramic mug of coffee with exactly ONE handle, on its right side: it is one solid mug that "
          "never changes shape, never loses its handle and never leaves its spot. ")
MOKA = "On the counter in the background, to the left, stands one small silver moka pot; it never moves or changes. "
COFFEE = ("\n\nThe coffee on the counter is already shown in its real colours in the source video. Keep every brown shape exactly where it "
          "is, the same size and the same outline as in the source frame, in every frame; do not add, remove, move or reshape any of them. ")
RING = "The thin dark brown ring lying on the counter is a dried coffee ring: a complete, unbroken thin circle with an empty white middle. "
DROP = ("The glossy brown dome is a fresh drop of coffee, translucent like dark tea, with tiny dark specks of coffee grounds inside it; "
        "it is the same drop, the same size and the same colour in every frame. ")
# what is actually in frame in each clip: describing a prop that is out of frame makes the painter add it
SCENES = {
    "01": ROOM + MOKA + "There is no mug, no cup and no saucer in this shot." + COFFEE + RING,
    "02": ROOM + MUGTXT + "There is no saucer and no other dish." + COFFEE + DROP,
    "03": ROOM + MUGTXT + "There is no saucer and no other dish." + COFFEE + DROP,
    "04": ROOM + MUGTXT + "There is no saucer and no other dish." + COFFEE + DROP,
    "05": ("Scene: a smooth white stone kitchen counter in warm morning sunlight with soft cool shadows, seen from straight above. "
           "Nothing else is in the frame.") + COFFEE + DROP,
    "06": ROOM + MUGTXT + MOKA + "There is no saucer and no other dish." + COFFEE + RING,
}
STYLE_FIRST = ("\n\nStyle: use the painted reference image ONLY for its gouache paint treatment and brushwork; do not copy its room, its "
               "night lighting or any of its objects. ")
STYLE_REST = ("\n\nStyle: match the painted kitchen reference image exactly: the same room, the same colours, the same light, the same "
              "paint treatment. ")
STYLE_END = ("Soft matte gouache painting with visible brushwork, broad simplified shapes, layered colour, softened painted edges and "
             "subtle paper texture on Sol, the props and the room alike. Forms defined by light and colour. No ink outlines, no black "
             "linework, not glossy 3D, not vector art. Smooth natural motion, no motion blur, stable background paint texture. "
             "No text, no captions, no speech, no music.")
BEATS = {
    "01": ("Beats: 1. The shot opens low and close on a dried coffee ring on the white counter, with Sol leaning over it from behind; the "
           "camera then pulls back and up to a medium shot of Sol, the ring and the kitchen. 2. Sol dips toward the ring twice, tapping "
           "the air above it with one arm. 3. He tilts back and looks up, and stays looking up with a gentle small wobble. 4. Near the "
           "end he nods once. In the final half second his two navy oval eyes are open. The ring never changes."),
    "02": ("Beats: 1. Sol stands left of the pale blue mug. He takes one small hop toward it and nudges its side with his arm. 2. PHYSICS "
           "RULE: the mug rocks a little ONLY while Sol's arm touches it, then settles upright on the same spot and stays still. It is the "
           "same mug with the same single handle in every frame. 3. One small brown drop of coffee hops out over the mug's rim, arcs "
           "through the air and lands on the counter in front, where it settles into a round glossy brown dome that stays there. "
           "4. Sol hops back and looks down at the drop while the camera pushes in toward it."),
    "03": ("Beats: 1. CLOSE-UP. A fresh drop of coffee, a glossy brown dome with tiny dark specks inside it, sits on the white counter and "
           "fills most of the frame. Sol and the pale blue mug stand behind it, watching. 2. PHYSICS RULE: the drop's round outline on the "
           "counter is glued in place. It never gets wider, never gets narrower and never slides. The ONLY change is that its top slowly "
           "sinks a little. 3. The pale shapes rising from the drop are thin wisps of vapour: they rise ONLY from the drop's outer rim, "
           "none from its middle, and they fade away near the end. 4. The specks inside stay scattered. The camera slides slowly."),
    "04": ("Beats: 1. CLOSE-UP from a low angle. The same drop of coffee, a glossy brown dome on the white counter, with Sol and the pale "
           "blue mug behind it. 2. The tiny dark specks inside the drop drift steadily OUTWARD from its middle toward its rim, exactly as "
           "they move in the source video. 3. PHYSICS RULE: the drop's outline on the counter never moves; it only gets a little flatter. "
           "4. Sol watches with a gentle small wobble. The camera slides slowly."),
    "05": ("Beats: 1. CLOSE-UP from straight above. Only the white counter and the round drop of coffee are in the frame: no character, no "
           "mug, no other object. 2. The last dark specks reach the drop's rim and pile up there into a dark brown ring. 3. The brown water "
           "inside thins and dries away to nothing, leaving the clean white counter inside the ring. 4. PHYSICS RULE: the round outline "
           "never moves and never shrinks. The shot ends on a complete, unbroken, thin dark brown ring with an empty white middle."),
    "06": ("Beats: 1. The shot opens close on the finished dried coffee ring on the white counter, a complete unbroken thin dark brown "
           "circle with an empty middle, with Sol and the pale blue mug behind it; the camera then pulls back and up. 2. Sol points down "
           "at the ring with one arm. 3. He tilts back and looks up. 4. At the end he nods twice. In the final half second his two navy "
           "oval eyes are open. The ring never changes."),
}

style, turn = sys.argv[1], sys.argv[2]
first = "first=1" in sys.argv
reqs = []
for arg in sys.argv[3:]:
    if arg == "first=1":
        continue
    clip, vid = arg.split("=")
    p = P1 + SCENES[clip] + "\n\n" + BEATS[clip] + (STYLE_FIRST if first else STYLE_REST) + STYLE_END
    assert "mouth" not in p.lower()
    (HERE / f"v2-{clip}-paint.txt").write_text(p + "\n")
    reqs.append({"index": int(clip), "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p", "aspect_ratio": "9:16",
                 "medias": [{"value": vid, "role": "video_references"}, {"value": style, "role": "image_references"},
                            {"value": turn, "role": "image_references"}], "prompt": p}})
print(json.dumps(reqs))
