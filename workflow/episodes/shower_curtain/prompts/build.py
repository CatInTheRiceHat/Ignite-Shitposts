#!/usr/bin/env python3
"""Build the paint prompts and the Higgsfield request list for the shower-curtain episode (script v2.2, VERTICAL 9:16).

Usage: build.py <style_media_id> <turnaround_media_id> [first=1] clip=<skeleton_media_id>[,<expression_strip_media_id>] ...
Writes prompts/0<clip>-paint.txt for each clip named and prints the requests as JSON.
first=1 is for the clip painted before this film has a style frame of its own: the style image is then a frame of
the coffee episode (a sunny tiled kitchen), used only for its paint treatment.
Each clip can take a strip of just the faces it uses, cut from the expression sheet with the labels left off
(refs/expr-clip0N.png): the painter has not been tried on the 32 newer faces, and a labelled sheet invites lettering.
Rules (guidelines/current-rules.md): never the word for the opening under a nose, no mood words, numbered beats,
physics as rules, every prop's place named, only what is in frame, every expression named with its time.
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P1 = ("Repaint this blockout video as a finished hand-painted gouache animation. VERTICAL 9:16 portrait frame, frame for frame: "
      "keep the exact camera move, framing, timing and every pose from the source video, and paint only what each source frame shows, "
      "adding no other characters or objects.\n\n"
      "Character: the flame-shaped figure is Sol, exactly the mascot in the reference images (the turnaround sheet shows his shape from "
      "every side; the strip of faces shows every eye shape he makes in this shot). Round, plump gumdrop body with a red outer layer, an "
      "orange middle layer and a broad cream inner flame for the face. At rest his face is plain smooth cream with exactly two small "
      "tall navy #1C2447 oval eyes set low and close together, solid dark with no whites or highlights, and nothing else on it: nothing "
      "is drawn above his eyes and nothing below them. His eyes change ONLY as the beats below say; copy his eyes from each source frame "
      "exactly, the same shape, size and place. Short stubby rounded red-orange arm nubs and two tiny blunt stubby red feet; his arm nubs "
      "stay the same short length in every frame and never stretch or grow. Sol wears nothing. Sol gives off no sparks, particles or "
      "smoke. His layers and face move together as one body with a small soft wobble that settles. He keeps the same size and the same "
      "place in the frame as in the source video. The small floating marks near him (music notes, an exclamation mark, a sweat drop, "
      "dots, a light bulb, a star, yellow dashes) appear ONLY in the frames where the source video shows them, in the same place and "
      "size, and vanish when the source stops showing them.\n\n")
TUB = ("Scene: a small sunny bathroom, inside a white bathtub alcove. The tub floor is smooth glossy white. The walls of the alcove are "
       "pale aqua square tiles with white grout lines. Warm daylight with soft cool shadows, so the room has depth and glow. ")
FAR = ("On the far wall are one silver shower head, one round window glowing with warm cream light, one small white shelf holding one "
       "coral bottle, one lilac bottle and one yellow rubber duck, and one silver lever tap; none of them ever moves or changes. ")
SPRAY = ("The shower is running: blue water drops fall straight down from the shower head in a narrow spray and land in one round "
         "pale-blue puddle on the tub floor. Paint the drops as falling water, exactly where the source video shows them. ")
CURTAIN = ("Along the left side of the tub hangs ONE mustard-yellow shower curtain with soft vertical pleats and a pale cream band "
           "along its bottom hem, on one silver rod with silver rings. CURTAIN RULE: it is the same single curtain in every frame, the "
           "same colour, with the same pleats and the same cream hem; it bends and swings ONLY as the source video shows and never "
           "tears, opens, wraps around Sol or changes length. ")
ROOM = ("Beyond the curtain is the rest of the bathroom: cream walls, a sand-coloured floor with one coral rug, one wooden sink cabinet "
        "with a white top, one round mirror above it, one small potted plant and one blue towel on a rail. ")
STEAM = ("The small pale blue-white clumps floating in the air are little puffs of steam. Paint each one as a small soft round puff of "
         "pale steam, the same size, in the same place and moving along the same path as in the source video, in every frame. STEAM "
         "RULE: add no other steam, fog, mist or cloud anywhere, and never let the puffs spread into a haze. ")
CUT = ("The camera stands OUTSIDE the tub, as if the near side wall had been cut away: the white tub floor runs toward the camera, the "
       "yellow curtain hangs across the back of the tub like a backdrop with a plain cream wall above it, and the tiled walls stand at "
       "the two ends of the tub. Paint no wall between the camera and the tub. ")
GROUND = "GROUND RULE: his feet rest on the tub floor in every frame and his shadow lies under his feet. "
ARMS = "ARM RULE: his arm nubs stay the same short stubs in every frame; he never reaches for or holds anything. "
SCENES = {
    "1": TUB + FAR + SPRAY + CURTAIN + ROOM + "One yellow rubber duck sits on the white rim of the tub and one on the tub floor at the "
         "left, and one pink bar of soap lies on the tub floor at the right, where the source video shows them; they never move. ",
    "2": TUB + FAR + SPRAY + CURTAIN,
    "3": TUB + FAR + SPRAY + CURTAIN + STEAM,
    "4": TUB + SPRAY + CURTAIN + STEAM + "At the start a tiled end wall of the tub stands behind Sol. After the camera moves out sideways: " + CUT,
    "5": TUB + SPRAY + CURTAIN + STEAM + CUT + "The view is from a high three-quarter angle near the shower end. ",
    "6": TUB + FAR + SPRAY + CURTAIN + ROOM + "One yellow rubber duck sits on the tub floor at the bottom of the frame and one pink bar "
         "of soap lies at the lower right, where the source video shows them; they never move. ",
    "7": TUB + FAR + SPRAY + CURTAIN,
}
ARC = "two small upward-curved navy arcs, like ^ ^"
RING = "two round navy rings with white centres"
GLARE = "two navy half-rings with white centres, each cut flat across its top and slanted down toward the middle of his face"
BEATS = {
    "1": ("Beats: 1. CAMERA MOVE: the shot opens high up near the ceiling, looking down on the whole bathroom, and flies smoothly down "
          "across the room, over the curtain rod and into the tub, levelling out low in front of Sol at 2.2 seconds, exactly as in the "
          "source video. Only the camera moves; the room does not change. 2. From the first frame Sol stands in the tub near the "
          "curtain, swaying gently from side to side, and his eyes are " + ARC + ". From 1.0 second one pink music note and one blue "
          "music note float beside him. 3. From 1.3 to 1.95 seconds the lower part of the curtain swings slowly in toward him, and at "
          "1.95 seconds its hem touches his side. 4. At 1.95 seconds the music notes are gone; he jolts with both arm nubs up, his eyes "
          "become " + RING + ", and one small navy exclamation mark floats beside him. 5. At 2.5 seconds the exclamation mark is "
          "gone. He turns toward the curtain and leans at it; his eyes become " + GLARE + ", and the top of his flame turns a deeper "
          "red, exactly as much as the source shows. The camera pushes in quickly on him from 2.5 to 2.8 seconds. He gives two short "
          "bounces on the spot, at 2.9 and 3.4 seconds. 6. At 4.4 seconds he turns a little and glances up toward the camera; his "
          "eyes stay the slanted half-rings and his flame top stays red to the last frame. " + GROUND + ARMS),
    "2": ("Beats: 1. Sol stands beside the curtain, turned toward it; its cream hem hangs right at his side. In the first quarter "
          "second his eyes are " + GLARE + " and the top of his flame is a deeper red. 2. At 0.25 seconds the red is gone and he is "
          "his normal orange and red from then to the last frame. His eyes become two sideways chevrons with rounded tips, pointing "
          "at each other like > <, and he leans back away from the curtain. From 0.4 to 1.4 seconds he flaps both short arm nubs up "
          "and down in turn, fast, six flaps, slapping at the curtain, and his body rocks with each flap. FLAP RULE: the nubs stay "
          "the same short length and only swing up and down at his sides; they never stretch toward the curtain. The curtain's hem "
          "flutters a little with each flap. 3. At 1.4 seconds the curtain swings in and at 1.5 seconds its hem bumps into him; the "
          "camera jolts. His eyes become " + RING + " and he holds still with both nubs raised until 2.1 seconds. 4. From 1.7 to 2.6 "
          "seconds the camera swings round to face him and then pushes in slowly. At 2.15 seconds his eyes are two navy ovals again; "
          "he lowers his nubs, turns to the camera and looks up. He blinks once at 2.75 seconds. 5. From 3.2 to 4.1 seconds he looks "
          "sideways at the curtain and one pale blue sweat drop sits on the upper right side of his face; at 4.2 seconds the drop is "
          "gone. 6. At 4.7 seconds he nods once. In the final quarter second his two navy oval eyes are open. " + GROUND),
    "3": ("Beats: 1. The shot opens behind Sol's shoulder: he stands in the lower left, facing the camera. From 0.15 to 0.7 seconds he "
          "turns round to face the shower, so we see his plain red-orange back, and then tips a little to one side. 2. CAMERA MOVE: "
          "from 0.8 to 1.5 seconds the camera rushes forward past him and up to the shower head; from 1.6 to 4.2 seconds it sinks "
          "straight down beside the falling water, all the way to the tub floor, exactly as in the source video. 3. The steam puffs "
          "near the spray travel DOWN beside the falling drops and, at the bottom, slide away from the spray along the tub floor, "
          "toward the camera. 4. The shot ends low, looking at the puddle where the water lands, with a few puffs sliding across the "
          "white floor. Sol's eyes are two navy ovals whenever his face is seen. " + ARMS),
    "4": ("Beats: 1. CAMERA MOVE: the shot opens low on the tub floor, moving toward Sol, who stands facing the camera in front of the "
          "tiled end wall. The camera rises in front of his face at 1.0 second, then from 1.4 to 2.6 seconds swings out sideways to a "
          "wide view from outside the tub, exactly as in the source video. 2. At 1.0 second his eyes become " + RING + ", two little "
          "fans of yellow dashes appear above his sides, and he raises both arm nubs; at 1.8 seconds the dashes are gone and his eyes "
          "are two navy ovals again. 3. In the wide view the steam puffs travel round in ONE big slow wheel in front of the curtain: "
          "down beside the spray at the right, along the tub floor to the left, up in front of Sol, and back along the top to the "
          "right. The middle of the wheel stays empty. 4. Sol stands at the left, small, facing the camera. From 2.6 to 4.2 seconds he "
          "leans his whole body round in one slow circle, his eyes following a puff round the wheel. 5. At 4.2 seconds his eyes "
          "become two small navy spirals and he sways from side to side; the camera pushes in quickly on him from 4.2 to 4.5 seconds "
          "and holds. His eyes stay spirals to the last frame. " + GROUND + ARMS),
    "5": ("Beats: 1. CAMERA MOVE: for the first 2.5 seconds the camera pushes in while its tilt levels out, exactly as in the source "
          "video; after 2.5 seconds the camera is perfectly still. 2. The steam puffs travel round in ONE big slow wheel in front of "
          "the curtain for the whole shot: down beside the spray at the right, along the tub floor toward the left, up, and back "
          "along the top. The middle of the wheel stays empty. 3. From 3.2 to 6.2 seconds the lower half of the curtain eases slowly "
          "in, away from the wall and toward the middle of the wheel, exactly as far as the source shows, and stops just short of "
          "Sol. Its top stays on the rod. 4. Sol stands small at the left, watching, with two navy oval eyes; he blinks once at 1.2 "
          "and once at 3.6 seconds. From 4.0 seconds he leans a little away from the curtain and looks at it sideways. " + GROUND + ARMS),
    "6": ("Beats: 1. CAMERA MOVE: the shot opens low on the bathroom floor outside the tub, gliding across the coral rug toward the "
          "outside of the yellow shower curtain, which hangs above the white side of the tub. From 2.6 to 4.4 seconds the camera "
          "rises up and over the curtain rod and looks down into the tub, exactly as in the source video. 2. While the camera glides, "
          "the lower part of the curtain sinks slowly away from the camera, into the tub. 3. From 4.4 seconds we look down at Sol "
          "standing in the tub beside the curtain. He looks sideways at its hem, which is creeping toward him, and one pale blue "
          "sweat drop sits on the upper right side of his face. 4. At 4.8 seconds the sweat drop is gone; his eyes become " + RING +
          " and three small pale blue drops fly off above him. He turns away from the curtain and runs on the spot: his two tiny "
          "feet scrabble fast, his body leans forward and bobs, and he does not move from his place. 5. At 5.5 seconds both feet "
          "shoot out from under him and he tips over backward; at 5.8 seconds he lands flat on his back on the tub floor, feet toward "
          "the camera, with one small bounce. The flying drops are gone. 6. From 5.8 seconds to the last frame he lies still on his "
          "back with his face toward the ceiling, and his eyes are two small navy X shapes. At 5.85 seconds the curtain's hem swings "
          "in and touches the top of his flame. At 6.6 seconds one foot twitches once. FALL RULE: he is one solid body the whole "
          "time: he tips over in one piece and lies flat on the white floor, touching it, with his shadow under him. " + ARMS),
    "7": ("Beats: 1. The shot opens with Sol lying flat on his back on the tub floor beside the curtain's cream hem, his eyes two small "
          "navy X shapes. By 0.4 seconds he has popped back up onto his feet, with a small wobble that settles. 2. From 0.3 to 1.9 "
          "seconds his eyes are two navy ovals looking down toward the hem at his side, and three small navy dots float above him at "
          "the right, appearing one, two, three. 3. At 1.9 seconds the dots are gone; his eyes become " + RING + " and one small "
          "yellow light bulb floats above him. 4. At 2.15 seconds he leans and bumps the curtain with the side of his round body. "
          "PHYSICS RULE: the curtain swings away ONLY because his body pushes it, then swings back and by 3.2 seconds rests against "
          "his side again, where it stays. 5. At 2.8 seconds the light bulb is gone; he turns to the camera and stretches up tall, his "
          "eyes become two small navy half-ovals, flat along the bottom and rounded on top, and one small yellow four-point star "
          "floats beside him. CAMERA MOVE: from 2.0 to 3.6 seconds the camera swings across in front of him and rises to face him, "
          "then pushes in quickly at 3.6 seconds, exactly as in the source video. 6. At 3.6 seconds the star is gone; he tilts back "
          "and looks up, his eyes become " + ARC + ", and two little fans of yellow dashes appear above his sides until 4.5 seconds. "
          "7. From 4.5 seconds the dashes are gone and his eyes stay " + ARC + ". He nods twice, clearly, at 4.55 and at 5.1 seconds, "
          "and the shot ends as the second nod finishes. " + GROUND + ARMS),
}
STYLE_FIRST = ("\n\nStyle: the painted reference image is from an earlier film in a different room. Use it ONLY for its gouache paint "
               "treatment, its brushwork, its sunny light and its Sol; do not copy its room, its counter or any of its objects. Take "
               "every object's place and colour from the source video. ")
STYLE_REST = ("\n\nStyle: match the painted reference frame from this same film exactly: the same bathroom, the same aqua tiles, the "
              "same yellow curtain, the same shallow pale-blue puddle of water on the white tub floor around Sol's feet, the same paint "
              "treatment, the same light and the same Sol. Do not copy the reference frame's "
              "camera angle or pose; take every object's place and every pose from the source video. ")
STYLE_CONT = ("\n\nStyle: the painted reference frame is the LAST moment of the shot just before this one, in the same film. This "
              "shot continues from it: the same bathroom, the same aqua tiles, the same yellow curtain with its cream hem, the same "
              "shallow pale-blue puddle of water on the white tub floor under Sol, the same paint treatment and light, and the same "
              "Sol, who starts this shot with the same slanted glare eyes and deeper red flame top. Do not copy the reference "
              "frame's camera angle; take every object's place and every pose from the source video. ")
STYLE_END = ("Soft matte gouache painting with visible brushwork, broad simplified shapes, layered colour, softened painted edges and "
             "subtle paper texture on Sol, the props and the room alike. Forms defined by light and colour. No ink outlines, no black "
             "linework, not glossy 3D, not vector art. Smooth natural motion, no motion blur, stable background paint texture. "
             "No text, no letters, no captions, no speech, no music.")

if __name__ == "__main__":
    style, turn = sys.argv[1:3]
    first, cont = "first=1" in sys.argv, "cont=1" in sys.argv
    reqs = []
    for arg in sys.argv[3:]:
        if arg in ("first=1", "cont=1"):
            continue
        clip, ids = arg.split("=")
        vid, _, expr = ids.partition(",")
        p = P1 + SCENES[clip] + "\n\n" + BEATS[clip] + (STYLE_FIRST if first else STYLE_CONT if cont else STYLE_REST) + STYLE_END
        assert "mouth" not in p.lower() and "smil" not in p.lower() and "happ" not in p.lower()
        medias = [{"value": vid, "role": "video_references"}, {"value": style, "role": "image_references"},
                  {"value": turn, "role": "image_references"}]
        if expr:
            medias.append({"value": expr, "role": "image_references"})
        (HERE / f"0{clip}-paint.txt").write_text(p + "\n")
        reqs.append({"index": int(clip), "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p",
                     "aspect_ratio": "9:16", "medias": medias, "prompt": p}})
    print(json.dumps(reqs))
