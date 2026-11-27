#!/usr/bin/env python3
"""Build the paint prompts and the Higgsfield request list for the "All Due This Week" ad (LANDSCAPE 16:9).

Usage: build.py <style_media_id> <turnaround_media_id> <expressions_media_id> [first=1] [garden=<course_art_media_id>] clip=<skeleton_media_id> ...
Writes prompts/0<clip>-paint.txt for each clip named and prints the requests as JSON.
first=1 is for the clip painted before this film has a style frame of its own (the reference is then the science
ad's frame: the same house, used for its paint treatment).
cont=1 (clip 2, repaint): the style image is the LAST moment of the shot before, so Sol starts purple and the pile
already has the extra sheet on the ball. The first paint started him orange, copying the plain style frame.
same=1 (clip 8, repaint): the style image is a frame of this same shot with his sparkle eyes. The first paint
dropped the sparkles for the final nod.
room=1 (clip 3, third paint): the style image is a frame of the first paint of this room. The second paint (lower
boxes) kept every prop but came back flat, with a pale wall, unlike the other scenes. REJECTED: the room frame
brought its tall boxes back and the painter doubled the homework stack and the poster.
swatch=<id> (clip 3, fourth paint): two strips of wall and floor paint from the first paint, as an extra image, with
the usual style frame. Paint only, no objects.
garden=<id> adds the course's card art as a fourth image for clip 4, the pond garden.
Rules (guidelines/current-rules.md): never the word for the opening under a nose, no mood words, numbered beats,
physics as rules, every prop's place named, only what is in frame, every expression named with its time, and NO
lettering is painted (it is laid on afterwards, overlays/composite.py).
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P1 = ("Repaint this blockout video as a finished hand-painted gouache animation. LANDSCAPE 16:9 widescreen frame, frame for frame: "
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
      "layers and face move together as one body with a small soft wobble that settles. He keeps the same size and the same place "
      "in the frame as in the source video.\n\n")
INDIGO = ("Where the source video shows the top of Sol's flame tinted deep indigo-violet, fading down into his normal orange, paint "
          "exactly that tint and exactly as much of it as each source frame shows. The few thin short navy vertical lines high on the "
          "left side of his face belong to that look: copy them only in the frames where the source shows them. ")
BLANK = ("LETTERING RULE: every sheet of paper, sticky note, card, page, board and box in this shot is BLANK. Paint no letters, no "
         "numbers, no words, no symbols, no music notes and no handwriting anywhere in the frame. ")
HOUSE = "Warm morning sunlight with soft cool shadows, so the room has depth and glow. "
DESK = ("Scene: a bedroom desk on a school morning, seen from eye level. A honey-coloured wooden desk top fills the lower third of the "
        "frame. Behind the desk is a dusty-teal wall. At the upper left of the wall is one white-framed window glowing with warm "
        "sunlight, cut off by the top of the frame. On the desk, in the middle of the frame, stands one teal desk lamp with a yellow "
        "shade turned toward the left. " + HOUSE)
PILE = ("On the right half of the desk stands a pile of things, exactly where the source video shows each one, and none of them ever "
        "changes: one thick stack of white worksheets with one blank yellow sticky note on its front; on top of the stack one "
        "black-and-white soccer ball; behind the ball one blank cream sheet of paper standing upright and leaning back; to the "
        "right of the stack one blank white poster board standing on its edge against the wall, with one blank pale-blue sticky note "
        "near its top; and in front of the poster board one blank white calendar page with a red band across its top, leaning back "
        "against the poster board. At the front corners of the desk lie two crumpled balls of paper and two marker pens. ")
SCENES = {
    "1": DESK + PILE + BLANK + INDIGO,
    "2": DESK + PILE + "One more blank white sheet of paper lies on top of the soccer ball and stays there. " + BLANK + INDIGO,
    "3": ("Scene: the floor of the same bedroom, seen from a slightly high angle. A warm wooden floor with a large teal rug, a "
          "dusty-teal wall with a white baseboard. Against the wall on the right stands one low wooden bookshelf with a row of "
          "coloured book spines. On the rug in front of it stand three low open cardboard boxes in a row, the same size, open at the "
          "top, with plain blank fronts. BOX RULE: each box is four plain flat sides and nothing else in every frame: no flaps, "
          "no lids, no folds, and its shape never changes. At the start three things stand to the left of the boxes: one thick stack of white "
          "worksheets with one blank yellow sticky note on its front, on the floor next to Sol; one blank white poster board "
          "standing on its edge against the wall, with one blank pale-blue sticky note near its top; and one blank white calendar "
          "page with a red band across its top, leaning against the wall. " + HOUSE + BLANK + INDIGO),
    "4": ("Scene: a quiet Japanese pond garden in autumn, the same garden as the painted garden reference image: soft warm hazy "
          "light, a still pale blue-green pond filling the right two thirds of the frame, with a few fallen orange maple leaves "
          "floating on it. On the left Sol sits on one flat grey rock capped with green moss at the edge of the water. Behind him "
          "are rounded green bushes and mossy grey stones, and one old grey stone lantern with a mossy roof standing at the edge of "
          "the pond. A maple branch with red and orange leaves reaches in across the top of the frame. On the far bank are soft "
          "pale trees and bushes fading into a warm peach haze. " + INDIGO +
          "LETTERING RULE: paint no letters, numbers or words anywhere. "),
    "5": ("Scene: a home kitchen, the same house, seen from eye level. A honey-coloured wooden kitchen table fills the lower third of "
          "the frame. Behind it is a pale cream counter and a wall of white square tiles with one teal stripe. On the table stand "
          "three things in a row on the right: one thick stack of white worksheets with one blank yellow sticky note on its front; "
          "one blank white poster board standing upright and leaning back, with one blank pale-blue sticky note near its top; and "
          "one blank cream sheet of paper standing upright and leaning back. " + HOUSE + BLANK),
    "6": ("Scene: a hallway of the same family home, seen from a slightly low angle. A wooden floor with a teal rug, a dusty-teal "
          "wall with a white baseboard. On the wall hangs one whiteboard in a pale metal frame, with a narrow tray along its bottom "
          "edge holding exactly one blue marker pen. To the right of the whiteboard stand one potted green plant in a coral pot on "
          "the floor and one plain wooden door in a white door frame with one round brass knob. The whiteboard is clean, empty "
          "white in every frame. " + HOUSE + BLANK),
    "7": ("Scene: the top of the same honey-coloured wooden desk, close, seen from above. On the right lies one blank white sheet of "
          "drawing paper, flat on the desk. At the far edge of the desk lie one yellow pencil, one blue pencil and one pink eraser, "
          "which never move. The desk is painted wood with visible brushwork and soft cool shadows, not a flat blank colour. "
          + HOUSE + BLANK + INDIGO),
    "8": (DESK + "The desk is tidy. To the right of the lamp stands one short neat stack of white worksheets with one blank yellow "
          "sticky note on its front, and one blue pencil cup holding three yellow pencils, with one blank pink sticky note on its "
          "front. On the wall above them hangs one small blank white calendar page with a red band across its top, held by one red "
          "pin. Nothing else is on the desk. " + BLANK),
}
CALM = "He is all warm orange and red for the whole shot: no indigo or purple anywhere on him and no lines on his face. "
ARMS = "ARM RULE: his arm nubs stay short stubs; he never reaches for or touches anything with an arm. "
BEATS = {
    "1": ("Beats: 1. Sol stands on the desk on the left. From the very first frame the top of his flame is tinted indigo-violet and "
          "thin short lines sit high on the left side of his face; he looks up toward the camera and blinks once. 2. At 0.8 seconds "
          "he turns toward the pile and looks at it sideways, holds one short arm nub up toward it, and gives two small bounces on "
          "the spot. 3. At 2.0 seconds one blank white sheet of paper drifts down from the top of the frame, swaying, and at 2.6 "
          "seconds it lands on top of the soccer ball and stays there. PHYSICS RULE: the sheet only falls; nothing else in the pile "
          "moves except a tiny wobble of the ball as the sheet lands. 4. At 2.6 seconds Sol jolts with one hop and both arm nubs up: "
          "his eyes become two round navy rings with white centres and the indigo spreads further down his flame. He lands and "
          "shakes quickly from side to side. 5. At 4.3 seconds his eyes are two navy ovals again; the indigo and the thin lines "
          "stay. He turns to face the camera, looks up, and at 4.7 seconds nods once. In the final quarter second his two navy "
          "oval eyes are open. FACING RULE: his face always points toward the pile or toward the camera, never toward the left edge "
          "of the frame. " + ARMS),
    "2": ("Beats: 1. CAMERA MOVE: the shot opens CLOSE on Sol, who fills most of the frame, and the camera pulls slowly and "
          "smoothly back, exactly as in the source video, until the pile of things is in view on the right. Only the camera "
          "moves; the pile never changes. For the whole shot, from the first frame to the last, the top of his flame is deep indigo-violet fading "
          "down to orange, with thin short lines high on the left side of his face. 2. He leans forward toward the camera. 3. At "
          "2.45 seconds he dips and hunches with both arm nubs raised, and his eyes become two sideways chevrons with rounded tips, "
          "pointing at each other like > <. They stay that way to the last frame."),
    "3": ("Beats: 1. Sol stands on the floor on the left, turned toward the boxes, looking at them sideways. COLOUR RULE: for the "
          "whole shot, from the first frame to the last, the top of his flame is tinted indigo-violet exactly as in the source "
          "video, and there are NO lines on his face. 2. At 1.5 seconds he leans and bumps the stack of worksheets with the side of "
          "his round body. At 1.75 seconds the stack hops up in an arc, turning half round in the air, and at 2.3 seconds drops "
          "into the FIRST box, the one on the left, where it stays to the last frame with the top of the stack showing above the "
          "rim of the box. 3. At 2.9 seconds he holds one short arm nub up toward the poster board. At "
          "3.05 seconds the poster board hops off the wall in an arc, turning half round, and at 3.65 seconds drops into the SECOND "
          "box, the middle one, where it stands upright with its top half sticking out. 4. At 4.1 seconds the calendar page lifts "
          "off the wall and floats slowly across, swaying like paper, and at 5.2 seconds settles into the THIRD box, the one on the "
          "right, with its top edge showing. 5. Each box gives one tiny hop at the moment its thing lands, and "
          "is otherwise perfectly still. PHYSICS RULE: there are exactly three things and exactly three boxes; each thing follows "
          "the source video's path, goes into its own box and stays there, in sight, to the last frame; nothing vanishes, appears or changes shape. In the last "
          "frame all three boxes hold their thing: the stack of worksheets in the first, the poster board in the second, the "
          "calendar page in the third. 6. Sol "
          "watches each one go, then at 5.3 seconds turns to the camera and looks up; he blinks once at 5.0 seconds. " + ARMS),
    "4": ("Beats: 1. Sol sits still on the mossy rock, facing the camera. He slowly swells a little and shrinks again three times, "
          "like three slow breaths: from 0.2 to 1.7 seconds, from 1.8 to 3.3 seconds and from 3.4 to 4.9 seconds. His feet never "
          "leave the rock. 2. COLOUR RULE: at the start the top half of his flame is deep indigo-violet. With each breath out the "
          "indigo shrinks back toward the tip of his flame, exactly as in the source video; by the last frame only the very tip is "
          "faintly violet and the rest of him is warm orange and red. 3. EYES: during the first breath his eyes are two sideways "
          "chevrons with rounded tips, pointing at each other like > <, and thin short lines sit high on the left side of his face. "
          "At 1.8 seconds the lines are gone and his eyes become two short flat closed lines, and stay closed through the second "
          "breath. At 3.6 seconds they open into two navy ovals and stay open. 4. At 1.9 seconds one orange maple leaf drifts down "
          "from the branch, swaying, and at 3.1 seconds it lands on the water on the right; one thin pale ring spreads from it and "
          "fades. Nothing else moves except the gentlest shimmer on the water. " + ARMS),
    "5": ("Beats: 1. Sol stands on the table on the left. At 0.5 seconds he turns toward the three things and looks at them "
          "sideways, and at 0.9 seconds holds one short arm nub up toward the stack of worksheets, the nearest one. 2. At 1.75 "
          "seconds the poster board and the cream sheet slide straight back, away from the camera, a short way and stop; they stay "
          "upright and never change shape. The stack of worksheets never moves. 3. At 1.9 seconds Sol gives one small hop with both "
          "arm nubs up, and his eyes become two round navy rings with white centres. 4. At 3.1 seconds his eyes are two navy ovals "
          "again; he turns to the camera and looks up, and blinks once at 4.0 seconds. " + CALM + ARMS),
    "6": ("Beats: 1. Sol stands on the floor at the lower left corner of the whiteboard, turned toward it, looking up at it; he "
          "blinks once at 0.8 seconds. 2. At 1.5 seconds he crouches, hops up and taps the board's lower left corner with his raised "
          "arm nub, then lands on the floor with a small squash. 3. At 3.0 seconds he hops again with both arm nubs up, and his eyes "
          "become two round navy rings with white centres. He lands. 4. At 4.2 seconds his eyes are two navy ovals again; he turns "
          "to face the camera and looks up, and blinks once near the end. " + CALM + "The whiteboard, its tray, the marker, the "
          "plant and the door never move, and the whiteboard stays empty white."),
    "7": ("Beats: 1. Sol stands on the desk on the left, just beside the sheet of paper, looking down at it. For the first 0.4 "
          "seconds he is all warm orange with two navy oval eyes. 2. From 0.45 to 1.95 seconds the top of his flame turns "
          "indigo-violet and thin short lines sit high on the left side of his face; he leans toward the paper, pulls back, and "
          "leans toward it again. 3. At 1.95 seconds the indigo and the lines are gone completely: he is all warm orange and red "
          "from then to the last frame. He blinks once at 2.15 seconds. 4. At 3.0 seconds he squashes down, springs toward the paper "
          "and nudges its near edge with the side of his round body. PHYSICS RULE: the sheet slides a short way across the desk, "
          "away from him, ONLY while his body is pushing it, turns a little and stops; it lies flat on the desk in every frame and "
          "never lifts, curls or bends. 5. At 3.9 seconds he tilts back and looks up toward the camera with two solid navy oval "
          "eyes, and gives one small bounce on the spot. GROUND RULE: his feet rest on the desk in every frame and his shadow lies "
          "under his feet. ARM RULE: both arm nubs stay tucked at his sides for the whole shot."),
    "8": ("Beats: 1. Sol stands on the desk on the left, facing the camera. At 0.35 seconds he gives one hop with both arm nubs up, "
          "and his eyes become two round navy rings with white centres. He lands. 2. At 1.0 second he turns a little and looks to "
          "the right. 3. At 2.0 seconds his eyes become two navy ovals that each hold one small white four-point sparkle and one "
          "tiny white dot, steady and in the same place in every frame, and he gives two small bounces on the spot with his feet "
          "on the desk. He blinks once at 4.4 seconds and once at 7.6 seconds. 4. At "
          "6.3 seconds he turns to face the camera, tilts back and looks up. 5. At 9.2 seconds he nods once, clearly, and then holds "
          "still, looking up, to the last frame. SPARKLE RULE: from 2.0 seconds to the very last frame, each of his eyes holds its "
          "white four-point sparkle and tiny white dot in every frame: while he looks to the right, while he tilts back, during "
          "the nod and in the final hold. After 2.0 seconds his eyes are never plain dark ovals. He is his brightest warm "
          "orange and red for the whole shot, with no indigo or purple anywhere on him and no lines on his face. " + ARMS +
          "Everything on the desk and the wall stays perfectly still."),
}
STYLE_FIRST = ("\n\nStyle: the painted reference image is an earlier film set in this same bedroom. Use it for its gouache paint "
               "treatment, its palette, its warm morning light and its Sol; do not copy its poster, its clock or its layout. Take "
               "every object's place and colour from the source video. ")
STYLE_REST = ("\n\nStyle: match the painted reference frame from this same film exactly: the same paint treatment, the same palette, "
              "the same warm morning light and the same Sol. Where this shot is a different place, keep the same paint treatment. "
              "Do not copy the reference frame's objects. Take every object's place and colour from the source video. ")
STYLE_CONT = ("\n\nStyle: the painted reference frame is the LAST moment of the shot just before this one, in the same film. This "
              "shot continues from it with no gap: from its very first frame Sol has the same indigo-violet flame top and thin lines "
              "as in the reference frame, and the pile is exactly the pile in the reference frame, with the blank sheet lying on the "
              "soccer ball. Match its paint treatment, palette and light exactly. ")
STYLE_SAME = ("\n\nStyle: the painted reference frame is a frame of this same shot. Match it exactly: the same room, the same paint "
              "treatment, palette and light, the same Sol, and the same sparkle eyes. Take every pose from the source video. ")
STYLE_ROOM = ("\n\nStyle: the painted reference frame is an earlier painting of this same room from this same camera. Paint this "
              "shot exactly like it: the same deep dusty-teal wall with visible brushwork, the same painted wooden floor with "
              "its grain, the same teal rug, the same bookshelf, the same cardboard and the same Sol, in the same rich matte "
              "gouache. One thing differs: the three boxes are LOWER than in the reference frame; take their height, and the "
              "place of every object, from the source video. ")
STYLE_SWATCH = ("The paint swatch reference image is two strips cut from an earlier painting of this room: the top strip shows how "
                "its WALL is painted (deep dusty teal-green with visible brush strokes) and the bottom strip shows how its wooden "
                "FLOOR and teal RUG are painted (warm wood with grain). Paint this room's wall, floor and rug exactly like the "
                "swatch. The swatch shows paint only: take no objects and no layout from it. ")
STYLE_GARDEN = ("The painted garden reference image shows this garden: match its soft hazy light, its foliage, its mossy stones, its "
                "lantern and its water. Do not copy the garden image's composition or its character; the layout and Sol come from "
                "the source video. ")
STYLE_END = ("Soft matte gouache painting with visible brushwork, broad simplified shapes, layered colour, softened painted edges and "
             "subtle paper texture on Sol, the props and the room alike. Forms defined by light and colour. No ink outlines, no black "
             "linework, not glossy 3D, not vector art. Smooth natural motion, no motion blur, stable background paint texture. "
             "No text, no captions, no speech, no music.")

if __name__ == "__main__":
    style, turn, expr = sys.argv[1:4]
    first = "first=1" in sys.argv
    cont, same, room = "cont=1" in sys.argv, "same=1" in sys.argv, "room=1" in sys.argv
    garden = next((a.split("=")[1] for a in sys.argv[4:] if a.startswith("garden=")), None)
    reqs = []
    for arg in sys.argv[4:]:
        if arg in ("first=1", "cont=1", "same=1", "room=1") or arg.startswith("garden=") or arg.startswith("swatch="):
            continue
        clip, vid = arg.split("=")
        p = P1 + SCENES[clip] + "\n\n" + BEATS[clip] + (STYLE_FIRST if first else STYLE_CONT if cont else STYLE_SAME if same else STYLE_ROOM if room else STYLE_REST)
        medias = [{"value": vid, "role": "video_references"}, {"value": style, "role": "image_references"},
                  {"value": turn, "role": "image_references"}, {"value": expr, "role": "image_references"}]
        swatch = next((a.split("=")[1] for a in sys.argv[4:] if a.startswith("swatch=")), None)
        if swatch:
            p += STYLE_SWATCH
            medias.append({"value": swatch, "role": "image_references"})
        if clip == "4" and garden:
            p += STYLE_GARDEN
            medias.append({"value": garden, "role": "image_references"})
        p += STYLE_END
        assert "mouth" not in p.lower() and "smil" not in p.lower()
        (HERE / f"0{clip}-paint.txt").write_text(p + "\n")
        reqs.append({"index": int(clip), "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p", "aspect_ratio": "16:9",
                     "medias": medias, "prompt": p}})
    print(json.dumps(reqs))
