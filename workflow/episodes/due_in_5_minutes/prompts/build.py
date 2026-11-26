#!/usr/bin/env python3
"""Build the paint prompts and the Higgsfield request list for the "Due in 5 Minutes" ad.

Usage: build.py <style_media_id> <turnaround_media_id> <expressions_media_id> [first=1] clip=<skeleton_media_id> ...
Writes prompts/0<clip>-paint.txt for each clip named and prints the requests as JSON.
first=1 is for the clip painted before this film has a style frame of its own (the reference is then another
episode's frame, used for paint treatment only).
Rules (guidelines/current-rules.md): never the word for the opening under a nose, no mood words, numbered beats,
physics as rules, every prop's place named, only what is in frame. New here: every expression is named with its
time, and NO lettering is painted (it is laid on afterwards, overlays/composite.py).
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P1 = ("Repaint this blockout video as a finished hand-painted gouache animation. VERTICAL 9:16 portrait frame, frame for frame: "
      "keep the exact camera, framing, timing and every pose from the source video, and paint only what each source frame shows, "
      "adding no other characters or objects.\n\n"
      "Character: the flame-shaped figure is Sol, exactly the mascot in the reference images (the turnaround sheet shows his shape from "
      "every side; the expression sheet shows every eye shape he makes). Round, plump gumdrop body with a red outer layer, an orange "
      "middle layer and a broad cream inner flame for the face. At rest his face is plain smooth cream with exactly two small tall navy "
      "#1C2447 oval eyes set low and close together, solid dark with no whites or highlights, and nothing else on it: nothing is "
      "drawn above his eyes and nothing below them. He stands on the ground: his feet touch the surface and his shadow in every "
      "frame except in the middle of a hop, and after a hop he lands again. His eyes change "
      "ONLY as the beats below say; copy his eyes from each source frame exactly, the same shape, size and place. Short stubby rounded "
      "red-orange arm nubs and two tiny blunt stubby red feet; his arm nubs stay the same short length in every frame and never "
      "stretch or grow. Sol wears nothing. Sol gives off no sparks, particles or smoke. His "
      "layers and face move together as one body with a small soft wobble that settles.\n\n")
INDIGO = ("Where the source video shows Sol's flame tip tinted deep indigo-violet, fading down into his normal orange, paint exactly "
          "that tint and exactly as much of it as each source frame shows. The few thin short navy vertical lines high on the left "
          "side of his face belong to that look: copy them only in the frames where the source shows them. ")
BLANK = ("LETTERING RULE: every board, sheet of paper, card, tag and page in this shot is BLANK. Paint no letters, no numbers, no "
         "words, no symbols and no handwriting anywhere in the frame. ")
HOUSE = "Warm morning sunlight with soft cool shadows, so the room has depth and glow. "
DESK = ("Scene: a bedroom desk on a school morning. A honey-coloured wooden desk top fills the lower part of the frame; on it lie three "
        "crumpled balls of white paper and marker pens, exactly where the source video shows them. Behind the desk is a dusty-teal "
        "wall with one round wall clock (teal rim, white face with plain tick marks and no numerals, two dark hands that never move), "
        "one wooden shelf holding a small potted plant and three books, and at the right edge a white-framed window glowing with "
        "sunlight. At the back left of the desk stands a teal desk lamp with a yellow shade. " + HOUSE)
POSTER_BLANK = ("In the middle of the desk stands one white trifold poster board: a flat middle panel, two side wings angled toward "
                "the camera, and a white header board across its top. The whole poster is clean, empty white. It never moves. ")
POSTER_DONE = ("In the middle of the desk stands one white trifold poster board: a flat middle panel, two side wings angled toward the "
               "camera, and a white header board across its top. The poster is finished: paper pieces are stuck on it exactly where "
               "the source video shows them, and every piece is blank. On the left wing: one peach card, one pale blue card below it, "
               "and three small pale green tags in a column below that. On the middle panel: one cream sheet with a simple bar graph "
               "made of two dark axis lines, one tall blue bar on the left and one shorter yellow bar on the right. On the right "
               "wing: one pale yellow page. The header board is empty white. The poster and every piece on it stay exactly the same "
               "in every frame. ")
SCENES = {
    "1": DESK + POSTER_BLANK + BLANK + INDIGO,
    "2": DESK + POSTER_BLANK + BLANK + INDIGO,
    "3": ("Scene: a hallway of a family home. A wooden floor with a teal rug, a dusty-teal wall with a white baseboard. On the wall "
          "hangs one whiteboard in a pale metal frame, with a narrow tray along its bottom edge holding exactly one blue marker pen. "
          "Above it hang three small white-framed pictures of plain flat colour: coral, yellow and mint. The whiteboard is clean, empty "
          "white in every frame. " + HOUSE + BLANK),
    "4": ("Scene: a kitchen counter seen from high above. A pale cream stone counter. On it lies one teal cloth with two white bowls of "
          "ice cubes side by side. Behind the bowls, in a row: one small white salt shaker with a rounded silver cap on the left, Sol "
          "in the middle, and one round yellow kitchen timer with a white dial on the right. The counter is painted stone with "
          "visible brushwork and soft cool shadows, not a flat blank colour. " + HOUSE + BLANK),
    "5": ("Scene: a home kitchen. A pale cream stone counter in front of a wall of white square tiles with one teal stripe. On the "
          "counter stands one small white freezer with a single door hinged on its RIGHT side and one vertical metal handle near the "
          "door's left edge. Inside the freezer: pale blue walls, two wire shelves, and three identical blue ice-cube trays filled with "
          "white ice cubes, one on each level. " + HOUSE + BLANK),
    "6": ("Scene: a hallway of a family home. A wooden floor with a blue rug, a dusty-teal wall with a white baseboard. On the wall is "
          "one large cream sheet of paper with a simple bar graph: two dark axis lines, one tall blue bar on the left and one shorter "
          "yellow bar on the right. At the start the sheet is completely covered by a grid of small square sticky notes in yellow, "
          "pink, mint, pale blue and peach; each note carries three short dark pencil strokes and nothing else. " + HOUSE +
          "LETTERING RULE: paint no letters, no numbers and no words anywhere; the graph has no labels. "),
    "7": ("Scene: a kitchen counter seen from above. A pale cream stone counter. In front lies one open notebook with a teal cover, "
          "two pale yellow pages and a metal spine down the middle. To the left of the notebook is one small shallow puddle of clear "
          "water with one small half-melted ice cube in it. The counter is painted stone with visible brushwork and soft cool "
          "shadows, not a flat blank colour. " + HOUSE + BLANK),
    "8": DESK + POSTER_DONE + BLANK,
    "9": DESK + POSTER_DONE + BLANK,
}
CALM = 'He is calm and all warm orange and red for the whole shot: no indigo or purple anywhere on him and no lines on his face. '
BEATS = {
    "1": ("Beats: 1. Sol stands on the desk just to the left of the poster, turned toward the poster and looking at it sideways, "
          "holding up one short arm nub toward it, and gives two small bounces on the spot. 2. At 1.75 seconds he lowers the nub, "
          "tilts back and looks up at the wall clock. 3. At 2.5 seconds he jolts with one hop and both arm nubs up: his eyes become "
          "two round navy rings with white centres, his flame tip turns deep indigo-violet, and thin short lines appear high on the "
          "left side of his face. 4. He lands and shakes quickly from side to side, does one more small hop, and glances back at the "
          "poster. At 4.7 seconds his eyes are two navy ovals again; the indigo tip and the thin lines stay. 5. At 5.5 seconds he "
          "faces the camera and nods once. In the final half second his two navy oval eyes are open. FACING RULE: his face always "
          "points toward the poster or toward the camera, never toward the left edge of the frame. ARM RULE: his arm nubs stay "
          "short stubs and never touch the poster."),
    "2": ("Beats: 1. The camera pushes slowly in on Sol, who stands on the desk in front of the poster. For the whole shot his flame "
          "tip is deep indigo-violet fading down to orange, with thin short lines high on the left side of his face. 2. He leans "
          "forward toward the camera. 3. At 1.95 seconds he dips and hunches with both arm nubs raised, and his eyes become two "
          "sideways chevrons with rounded tips, pointing at each other like > <. They stay that way to the last frame."),
    "3": ("Beats: 1. Sol stands on the floor at the lower left corner of the whiteboard, turned toward it, looking at it. 2. At 1.3 "
          "seconds he crouches, hops up and taps the board's lower left corner with his raised arm nub, then lands on the floor with "
          "a small squash. 3. He turns to face the camera and looks up, and at 3.3 seconds he blinks once. 4. At 4.2 seconds he hops "
          "and taps the board again, and lands on the floor again. " + CALM + "The whiteboard, its tray, the marker and the pictures "
          "never move, and the whiteboard stays empty white."),
    "4": ("Beats: 1. The salt shaker stands right against Sol's side. He looks to the left at it, leans over and bumps it with the "
          "side of his round body. PHYSICS RULE: the shaker slides a little to the left ONLY while his body is touching it, rocks "
          "once and stays upright where it stops; it is the same one-piece shaker in every frame. 2. At 2.2 seconds he turns and "
          "looks to the right at the kitchen timer, which stands right beside him, and does one small hop toward it, leaning its way. "
          "The timer never moves. ARM RULE: both arm nubs stay tucked at his sides for the whole shot; he never reaches, points or "
          "touches anything with an arm. 3. " + CALM + "The bowls, the ice cubes and the cloth never change."),
    "5": ("Beats: 1. Sol stands on the counter to the left of the freezer, looking at its door, which is open only a crack. He nudges "
          "the door's left edge with his arm nub. 2. PHYSICS RULE: the door swings open toward the right on its hinges ONLY after his "
          "nudge, slows down and stays wide open; it never swings back and never changes shape. 3. The pale blobs spilling from the "
          "bottom of the freezer are cold white fog rolling out low over the counter and thinning away; the fog never hides the three "
          "ice trays. 4. At 1.45 seconds Sol hops back with both arm nubs up, and his eyes become two round navy rings with white "
          "centres. 5. At 3.3 seconds his eyes are two navy ovals again, and he blinks once near the end. He is all warm orange and red for the whole shot: no indigo or "
          "purple anywhere on him and no lines on him. The three trays never move."),
    "6": ("Beats: 1. Sol stands on the floor at the right edge of the sticky notes with his side to the wall, leaning into the wall "
          "and pushing against it with his arm nub. His eyes are two sideways chevrons with rounded tips, pointing at each other like "
          "> <. The notes tremble. 2. From 1.1 seconds the notes let go, the ones nearest Sol first: each one peels off, flutters and "
          "tumbles down, and lands flat on the floor in a loose pile. PHYSICS RULE: notes only fall downward; none rises, vanishes or "
          "appears, and none is left on the wall at the end. 3. The bar graph underneath is uncovered and never changes: the same two "
          "bars, blue and tall on the left, yellow and shorter on the right. 4. At 2.0 seconds Sol springs away from the wall with a "
          "hop and both arm nubs up, his eyes two round navy rings with white centres, looking up at the graph. 5. At 3.9 seconds his "
          "eyes are two navy ovals again. He is all warm orange and red, with no indigo."),
    "7": ("Beats: 1. Sol stands on the counter right behind the notebook and looks down to the left at the puddle. 2. At 1.6 "
          "seconds he squashes down and springs back up once, a little bounce on the spot: his feet never leave the counter. "
          "GROUND RULE: his feet rest on the counter in every frame and his shadow lies under his feet, touching them. ARM RULE: both "
          "arm nubs stay tucked at his sides for the whole shot. PHYSICS RULE: the notebook lies open and flat on the counter in "
          "every frame: its pages never lift, curl, bend or turn. 3. At 2.7 seconds he blinks once, then tilts back and looks up "
          "toward the camera with two solid navy oval eyes. " + CALM + "The notebook and the puddle never move or change, and both "
          "pages stay empty."),
    "8": ("Beats: 1. CAMERA MOVE: only the camera moves in this shot; the poster and everything on the desk stand perfectly still. "
          "The shot opens on the whole finished poster. The camera then glides in close and travels slowly across the poster exactly "
          "as in the source video: first the pale yellow page on the right wing, then the bar graph on the middle panel, then the "
          "peach card, the pale blue card and the three pale green tags on the left wing. Every paper piece keeps its exact place, "
          "size and colour from the source frame and stays blank. 2. At 6 seconds the camera swings left to Sol, who stands on the "
          "desk to the left of the poster, clear of it, facing the camera. His eyes are two navy ovals that each hold one small "
          "white four-point sparkle and one tiny white dot, steady and in the same place in every frame. 3. He gives two small "
          "bounces on the spot with both arm nubs up a little; his feet never leave the desk. He blinks once at 8.1 seconds. He is "
          "his brightest warm orange, with no indigo. The camera settles on him and holds."),
    "9": ("Beats: 1. Sol stands on the desk in front of the finished poster, tilted back, looking up toward the camera with two navy "
          "oval eyes. He blinks once at 0.7 seconds. 2. At 1.95 seconds his eyes become two navy ovals that each hold one small white "
          "four-point sparkle and one tiny white dot, and he nods twice. 3. He holds still, looking up, to the last frame. In the "
          "final half second his sparkle eyes are open. He is his brightest warm orange, with no indigo."),
}
STYLE_FIRST = ("\n\nStyle: use the painted reference image ONLY for its gouache paint treatment and brushwork; do not copy its room, "
               "its objects or its layout. Take every colour from the source video. ")
STYLE_REST = ("\n\nStyle: match the painted reference frame from this same film exactly: the same paint treatment, the same palette, "
              "the same warm morning light and the same Sol. Where this shot is a different room, it is another room of the same "
              "house. Take every object's colour from the source video. ")
STYLE_END = ("Soft matte gouache painting with visible brushwork, broad simplified shapes, layered colour, softened painted edges and "
             "subtle paper texture on Sol, the props and the room alike. Forms defined by light and colour. No ink outlines, no black "
             "linework, not glossy 3D, not vector art. Smooth natural motion, no motion blur, stable background paint texture. "
             "No text, no captions, no speech, no music.")

if __name__ == "__main__":
    style, turn, expr = sys.argv[1:4]
    first = "first=1" in sys.argv
    reqs = []
    for arg in sys.argv[4:]:
        if arg == "first=1":
            continue
        clip, vid = arg.split("=")
        p = P1 + SCENES[clip] + "\n\n" + BEATS[clip] + (STYLE_FIRST if first else STYLE_REST) + STYLE_END
        assert "mouth" not in p.lower() and "smil" not in p.lower()
        (HERE / f"0{clip}-paint.txt").write_text(p + "\n")
        reqs.append({"index": int(clip), "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p", "aspect_ratio": "9:16",
                     "medias": [{"value": vid, "role": "video_references"}, {"value": style, "role": "image_references"},
                                {"value": turn, "role": "image_references"}, {"value": expr, "role": "image_references"}], "prompt": p}})
    print(json.dumps(reqs))
