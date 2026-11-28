#!/usr/bin/env python3
"""Build the paint prompts and the Higgsfield request list for the "Whole Group Project" ad (script v2).

The film is SQUARE, but the painter only returns 16:9 or 9:16: every clip is painted 16:9 and the middle square is cut
out in the edit (overlays/composite.py).
Usage: build.py <style_media_id> <turnaround_media_id> [first=1] clip=<skeleton_media_id>,<expression_strip_media_id> ...
Writes prompts/0<clip>-paint.txt for each clip named and prints the requests as JSON.
first=1 is for the clip painted before this film has a frame of its own: the style image is then the course's own
card art (Sol on a sandcastle on this same beach at sunset).
Rules (guidelines/current-rules.md): never the word for the opening under a nose, no mood words, numbered beats,
physics as rules, every prop's place named, only what is in frame, every expression named with its time, and NO
lettering anywhere (every word is laid on in the edit, so every board, card, sign and banner is painted blank).
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P1 = ("Repaint this blockout video as a finished hand-painted gouache animation. WIDESCREEN 16:9 landscape frame, frame for frame: "
      "keep the exact camera move, framing, timing and every pose from the source video, and paint only what each source frame shows, "
      "adding no other characters or objects.\n\n"
      "Character: every flame-shaped figure in this video is Sol, exactly the mascot in the reference images (the turnaround sheet "
      "shows his shape from every side; the strip of faces shows every eye shape used in this shot). Round, plump gumdrop body with a "
      "red outer layer, an orange middle layer and a broad cream inner flame for the face. At rest the face is plain smooth cream with "
      "exactly two small tall navy #1C2447 oval eyes set low and close together, solid dark with no whites or highlights, and nothing "
      "else on it: nothing is drawn above the eyes and nothing below them. Eyes change ONLY as the beats below say; copy each "
      "figure's eyes from each source frame exactly, the same shape, size and place. Short stubby rounded red-orange arm nubs and two "
      "tiny blunt stubby red feet; arm nubs stay the same short length in every frame and never stretch or grow. No figure gives off "
      "sparks, particles or smoke. Each figure's layers and face move together as one body with a small soft wobble that settles. "
      "Every figure keeps the same size and the same place in the frame as in the source video; paint exactly as many figures as each "
      "source frame shows, never more and never fewer. The small floating marks near a figure (dots, a light bulb, a question mark, "
      "an exclamation mark, sleep marks, a star, music notes, drops, a little puff, flowers) appear ONLY in the frames where the "
      "source video shows them, in the same place and size, and vanish when the source stops showing them.\n\n")
BEACH = ("Scene: a festive beach at sunset, the same beach as in the key art. Pale warm sand with soft brushed ripples and low dunes "
         "topped with tufts of beach grass. A calm teal sea along the back with thin white foam lines and a ladder of pale golden "
         "glints under the sun. A sunset sky that shades from soft rose at the top through peach to pale gold at the horizon, with "
         "one low pale sun in a soft glow and long two-tone clouds, cream on top and rose underneath. Low mauve hills far away on the "
         "horizon, one tiny white sailboat, and palm trees at the far sides of the beach. Strings of small triangular pennants "
         "(coral, teal, yellow, blue, pink and cream) hang on thin wooden poles right across the back of the beach, in exactly the "
         "places the source shows; they never move. Warm low golden light with soft long shadows, so the beach has depth and glow. A "
         "few small shells and coral starfish lie on the sand where the source shows them. ")
CASTLE0 = ("The sandcastle is only begun: ONE finished round sand tower with a toothed top and one small dark window, a short piece of "
           "sand wall beside it, and one low rounded heap of sand. It is the same in every frame and never changes or grows. ")
CASTLE1 = ("The sandcastle is finished and never changes: one tall round middle tower with a toothed top, two shorter round towers at "
           "its sides, a low toothed wall across the front with one small dark arched gate, all of smooth golden sand, and one thin "
           "pole on the middle tower flying ONE small coral-red triangular flag. A few shells lie around its base. ")
BUCKET = "One red toy bucket stands upright on the sand beside the castle and one red toy shovel lies on the sand near it; they never move. "
BUCKET1 = "One red toy bucket stands upright on the sand beside the castle and one red toy shovel lies on the sand near it. "
BOARD = ("One wooden notice board stands on two wooden legs in the sand, with one sheet of cream paper pinned on it. PAPER RULE: the "
         "cream paper is completely BLANK in every frame: plain cream, with no drawing, no marks and no writing. ")
CLOCK = ("One round clock stands on a wooden post in the sand: a plain white clock face in a wooden rim, with two dark hands and NO "
         "numbers. Under it on the post hangs one small cream board in a coral-red frame. BOARD RULE: every cream board is completely "
         "BLANK in every frame, plain cream with no writing. ")
UMBRELLA = ("One teal beach umbrella on a white pole stands in the sand, and one yellow beach towel with two white stripes lies under "
            "it. One blue beach ball with a white band rests on the sand behind. They never move. ")
RING = ("RING SOL is the figure wearing one plain pink inflatable swim ring around his middle; the ring is the same in every frame "
        "and never comes off. ")
HAT = ("HAT SOL is the figure wearing one small straw hat with a coral band on the tip of his flame; the hat is the same in every "
       "frame and never comes off. ")
SLEEPY = "SLEEPY SOL is the third teammate; he wears nothing. "
OURS = "OUR SOL is the plain one, wearing nothing. "
RIVAL = ("Far in the background at the left: three more plain Sols stand in a row in front of a tall finished sandcastle with a small "
         "blue flag, passing ONE small blue bucket along the row from one to the next, exactly as the source shows. They stay small "
         "and far away. ")
GROUND = "GROUND RULE: every figure's feet rest on the sand and its shadow lies under its feet; after a hop it lands back on the sand. "
ARMS = "ARM RULE: arm nubs stay the same short stubs in every frame; nobody reaches for or holds anything. "
ARC = "two small upward-curved navy arcs, like ^ ^"
RINGS = "two round navy rings with white centres"
GLARE = "two navy half-rings with white centres, each cut flat across its top and slanted down toward the middle of his face"
SHUT = "two small navy curved lines, like gently closed eyes"
HALF = "two navy half-ovals, flat across the top and rounded below, like half-shut eyes"
DOME = "two small navy half-ovals, flat along the bottom and rounded on top"
SCENES = {
    "1": BEACH + "Across the foreground at the start hangs one long cream cloth banner with coral-red edges on two tall wooden poles. BANNER "
         "RULE: the banner is completely BLANK cream cloth in every frame, with no writing. " + CLOCK + BOARD + RIVAL + CASTLE0 + BUCKET1 + OURS,
    "2": BEACH + CASTLE0 + BUCKET + UMBRELLA + OURS + RING + HAT + SLEEPY,
    "3": BEACH + BOARD + OURS,
    "4": BEACH + CASTLE0 + BUCKET + UMBRELLA + OURS + RING + HAT + SLEEPY,
    "5": BEACH + CLOCK + RIVAL + OURS,
    "6": BEACH + BOARD + CASTLE0 + BUCKET + OURS + RING + HAT + SLEEPY,
    "7": BEACH + CASTLE0 + BUCKET + OURS + RING + HAT + SLEEPY,
    "8": BEACH + CASTLE1 + BUCKET + OURS + RING + HAT + SLEEPY,
}
BEATS = {
    "1": ("Beats: 1. CAMERA MOVE: the shot opens high in the air above the beach, looking down at the blank banner, and flies smoothly "
          "down and forward under the banner, past the three far-off Sols passing their bucket, and levels out low on the sand in "
          "front of our Sol and his castle at 1.9 seconds, exactly as in the source video. After that it only creeps in slowly. Only "
          "the camera moves; the beach does not change. 2. From the first frame our Sol is busy beside his castle. His eyes are " +
          GLARE + ". He stands at the tower and bobs down three times, at 0.3, 0.8 and 1.3 seconds. 3. At 1.7 seconds he scurries "
          "to the right on his tiny feet to the red bucket and bumps it with his side at 2.1 seconds: the bucket rocks once and "
          "settles upright. 4. He scurries left to the sand wall (2.55 to 2.9), bobs twice, scurries left to the tower (3.3 to 3.6), "
          "bobs, back to the wall, back to the tower, faster each time. From 3.3 seconds his eyes are " + RINGS + " and three small "
          "pale blue drops fly off above him. 5. At 4.75 seconds he stops in the middle, facing the camera. At 4.8 seconds the drops "
          "are gone; he sags down and forward with his arm nubs hanging, his eyes become " + SHUT + ", and one small pale lilac puff "
          "floats beside him. 6. At 5.8 seconds the puff is gone and his eyes are two navy ovals again; he tilts back and looks up "
          "toward the camera, still sagging a little. 7. At 7.35 seconds he nods once, slowly. " + GROUND + ARMS),
    "2": ("Beats: 1. The shot opens close on our Sol, turned a little to the right, leaning that way with the nub on that side raised. "
          "His eyes are " + GLARE + " and the top of his flame is a deeper red, exactly as much as the source shows, from the first "
          "frame. 2. CAMERA MOVE: from 0.9 to 1.25 seconds the camera whips quickly to the right, to his three teammates, and holds on "
          "them until 2.75 seconds, exactly as in the source video. 3. The three teammates: at the left RING SOL faces the camera, "
          "rocking gently from side to side in his pink swim ring, his eyes " + SHUT + ". In the middle HAT SOL stands with his BACK "
          "to the camera, looking out at the sea: we see only his plain red-orange back and his straw hat. At the right SLEEPY SOL "
          "stands on the yellow towel under the teal umbrella, leaning, his eyes " + SHUT + ", with small navy sleep marks floating "
          "above him. None of the three moves from his place. 4. CAMERA MOVE: from 2.75 to 3.1 seconds the camera whips back to our "
          "Sol and then pushes in very slowly. 5. Our Sol now faces the camera squarely and stands perfectly still. The red is gone: "
          "he is his normal orange and red from here to the last frame. His eyes are " + HALF + ", looking straight at the camera. "
          "6. At 4.4 seconds his eyes become " + GLARE + " (his flame stays normal orange and red); he stretches up tall, raises both "
          "nubs a little and tilts back to look up. He holds that to the last frame. " + GROUND + ARMS),
    "3": ("Beats: 1. CAMERA MOVE: in the first half second the camera sinks from above to a low angle looking up at the wooden "
          "notice board, then it is perfectly still, exactly as in the source video. 2. Our Sol stands at the right of the board, "
          "turned toward it, looking up at the blank cream paper. His eyes are two navy ovals and three small navy dots float above "
          "him. 3. At 0.8 seconds the dots are gone; his eyes become " + RINGS + " and one small yellow light bulb floats above him. "
          "4. At 1.15 seconds he dips, hops toward the board and flaps the nub nearest it once, then lands (1.5). The board does not "
          "move. 5. At 2.7 seconds the light bulb is gone and his eyes are two navy ovals again. He blinks once at 3.0 seconds, then "
          "turns a little toward the camera and looks up. " + GROUND + ARMS),
    "4": ("Beats: 1. CAMERA MOVE: the camera slides steadily sideways from right to left along a row of four Sols, from 0.25 to 4.15 "
          "seconds, and then holds on the last one, exactly as in the source video. 2. FOUR small name signs drop into the sand, one "
          "beside each Sol, at 0.6, 1.7, 2.8 and 3.9 seconds: each is one blank pastel card on a short wooden stick, falling straight "
          "down from above, landing upright in the sand and rocking once. SIGN RULE: each card is completely BLANK, a plain flat "
          "pastel colour with no writing, and after it lands it stays exactly where it is. Their colours in order: pale green, pale "
          "blue, pale peach, pale yellow. 3. SLEEPY SOL, on the yellow towel under the umbrella, never reacts: his eyes stay " + SHUT +
          " with small navy sleep marks above him. 4. HAT SOL starts with his back to the camera; from 1.8 to 2.15 seconds he turns "
          "round to face the sign beside him. At 2.2 seconds he tilts to one side and one small navy question mark floats above him; "
          "his eyes are two navy ovals. 5. RING SOL rocks gently with his eyes " + SHUT + " until 2.85 seconds; then he jolts with a "
          "small hop, both nubs up, his eyes become " + RINGS + " and one small navy exclamation mark floats above him. He looks at "
          "the sign, looks away, and snaps back to it. 6. OUR SOL stands at the left end facing the camera with two navy oval eyes. "
          "When the last sign lands beside him (3.9) he glances at it, then at 4.2 seconds he stretches up tall and tilts back, his "
          "eyes become " + DOME + ", and one small yellow four-point star floats beside him. " + GROUND + ARMS),
    "5": ("Beats: 1. The camera looks up at the clock from a low, slightly tilted angle and pushes in very slowly; the tilt never "
          "changes. Our Sol stands on the sand at the right of the post, turned toward it, looking up at the clock with two navy "
          "oval eyes. 2. At 0.5 seconds the clock's long hand jumps forward a little and the clock shudders once. Our Sol flinches "
          "back with a small hop and both nubs up; his eyes become " + RINGS + ". 3. At 1.5 seconds his eyes are two navy ovals "
          "again and his nubs are down. He blinks once at 2.0 seconds. 4. At 2.3 seconds he dips and hops. A SECOND small cream board "
          "in a coral-red frame, the same size as the first, drops straight down from above and at 2.75 seconds lands on the post "
          "just UNDER the first board, rocks once and stays there to the last frame. It is BLANK cream like the first. 5. At 3.5 "
          "seconds he turns toward the camera and stretches up tall; his eyes become " + DOME + " and one small yellow four-point "
          "star floats beside him. He holds that to the last frame. " + GROUND + ARMS),
    "6": ("Beats: 1. The shot opens close on the blank cream paper pinned to the wooden board. CAMERA MOVE: from 0.5 to 1.7 seconds "
          "the camera pulls back and rises to a high, wide view, exactly as in the source video, and then holds still. 2. OUR SOL "
          "stands beside the board, at its right, turned toward it and looking up at the paper, with two navy oval eyes. 3. The other "
          "three hop into the frame from the right, one after another, each in three small hops, and stop in a row to the right of "
          "our Sol, all turned toward the board: RING SOL arrives from 1.3 to 1.8 seconds, HAT SOL from 1.8 to 2.3, SLEEPY SOL from "
          "2.3 to 2.8. 4. Ring Sol and Hat Sol look up at the paper; Ring Sol's eyes become " + RINGS + " at 2.05 seconds and Hat "
          "Sol's at 2.55. 5. Sleepy Sol hops in with his eyes " + SHUT + " and small navy sleep marks above him. At 3.1 seconds he "
          "jolts upright with both nubs up: the sleep marks are gone, his eyes become " + RINGS + ", and one small navy exclamation "
          "mark floats above him; then he looks up at the paper too. 6. At 3.6 seconds our Sol's eyes become " + ARC + " and he "
          "raises both nubs once. All four stay in their places to the last frame. " + GROUND + ARMS),
    "7": ("Beats: 1. The shot opens looking down from high above at four Sols on the sand in front of the castle: OUR SOL at the left, "
          "facing right toward his three teammates, who stand in a row facing him: RING SOL, then HAT SOL, then SLEEPY SOL at the "
          "right. Sleepy Sol's eyes are " + HALF + " until beat 6. CAMERA MOVE: from 1.2 to 1.9 seconds the camera drops down to "
          "eye level beside our Sol and Ring Sol, exactly as in the source video. 2. From 1.35 to 1.85 seconds our Sol makes one hop "
          "over to Ring Sol, lands right beside him, and from 1.95 to 3.0 seconds holds up the nub nearest him. 3. At 2.2 seconds "
          "Ring Sol jolts with a small hop, both nubs up; his eyes become " + RINGS + " and one small navy exclamation mark floats "
          "above him. 4. At 2.9 seconds the exclamation mark is gone and Ring Sol's eyes become " + GLARE + "; he nods once (3.0 to "
          "3.4). From 3.45 to 4.1 seconds he turns round and hops away in two hops to the heap of sand at the castle behind the "
          "others; from 4.15 seconds he stands there with his BACK to the camera, bobbing down again and again as he pats the sand. "
          "5. CAMERA MOVE: from 3.5 to 4.3 seconds the camera slides right and back a little to show our Sol with Hat Sol and Sleepy "
          "Sol. Our Sol turns to the two of them and from 4.2 to 4.8 seconds flaps both nubs up and down quickly, in turn. 6. At 4.85 "
          "seconds Hat Sol and Sleepy Sol both turn away from him at the same moment, toward the right, and tip their faces up: their "
          "eyes become " + ARC + ", and one pink music note and one blue music note float beside each of them. They sway gently. "
          "7. At 5.3 seconds our Sol lowers his nubs and stands still with two navy oval eyes and one small pale blue drop on the "
          "upper side of his face. " + GROUND + ARMS),
    "8": ("Beats: 1. The shot opens close on the top of the finished castle and its coral-red flag. ONE blue rosette ribbon (a round "
          "blue badge with a plain cream middle and two short blue tails) drops straight down from above and at 0.45 seconds lands "
          "flat on the front of the middle tower, rocks once and stays there to the last frame. RIBBON RULE: its cream middle is "
          "completely BLANK, with no writing. 2. CAMERA MOVE: from 0.55 to 1.9 seconds the camera cranes back and down to a wide "
          "view of the castle and all four Sols, exactly as in the source video, and then holds perfectly still. 3. OUR SOL stands "
          "at the front left; RING SOL stands just behind him at the left; HAT SOL stands at the right of the castle beside the red "
          "bucket; SLEEPY SOL peeks out from behind the castle at the right. All four make one small hop as the ribbon lands. Our "
          "Sol's eyes start as navy ovals with small white sparkles in them, looking at the castle; the other three start with eyes " +
          ARC + ". 4. From about 1.3 seconds all four have plain navy oval eyes; each turns to face the camera, tilts back and looks "
          "UP, and stands listening with a very small gentle idle sway until 8.8 seconds. Our Sol glances to the right once, from 1.9 "
          "to 2.7 seconds, and blinks at 3.4, 5.9 and 7.7 seconds. Nobody changes place. 5. From 8.8 to 9.3 seconds our Sol nods "
          "once, clearly. 6. At 9.4 seconds all four raise both nubs straight up and give one springy bounce with their feet on the "
          "sand; their eyes become " + ARC + ", and small pink and white flowers float around Ring Sol, Hat Sol and Sleepy Sol. They "
          "hold that, nubs up, to the last frame. " + GROUND + ARMS),
}
PAINT = ("PAINT TREATMENT, the most important instruction: the source video is a flat, untextured 3D blockout. Do NOT return it as it "
         "is. Repaint every surface as hand-painted gouache with clearly visible brushwork: the sand in broad warm strokes with "
         "brushed ripples and soft painted shadows, the sea in brushy bands of teal with dabbed foam, the sky blended wet in soft "
         "strokes with dabbed clouds, the props in flat matte paint with softened edges. Paint every Sol flat and matte like the "
         "painted Sol in the reference frame: three flat layers of red, orange and cream with soft painted edges between them, a "
         "little dry-brush texture, and NO smooth 3D gradient, no airbrushed shading, no gloss, no plastic look.\n\n")
STYLE_FIRST = ("\n\nStyle: there are two painted reference images. The beach image is this film's own key art: the same beach at "
               "sunset, the same sandcastle. Match its soft gouache paint treatment, its warm rose, peach and cream colours and its "
               "light. The other painted image, a Sol in a tiled room, is from an earlier film: use it ONLY to see how Sol himself is "
               "painted (flat matte gouache layers with soft edges and plain navy eyes); do not copy its room or anything in it. Do not "
               "copy either image's camera angle or layout; take every object's place and every pose from the source video. ")
STYLE_REST = ("\n\nStyle: match the painted reference frame from this same film exactly: the same beach, the same sand, sea and sunset "
              "sky, the same pennants and palms, the same paint treatment, the same light and the same Sols with the same swim ring "
              "and straw hat. The key-art image shows the same beach and castle. Do not copy either image's camera angle or poses; take "
              "every object's place and every pose from the source video. ")
STYLE_END = ("Soft matte gouache painting with visible brushwork, broad simplified shapes, layered colour, softened painted edges and "
             "subtle paper texture on the Sols, the props and the beach alike. Forms defined by light and colour. No ink outlines, no "
             "black linework, not glossy 3D, not vector art. Smooth natural motion, no motion blur, stable background paint texture. "
             "No text, no letters, no numbers, no captions anywhere in the picture, no speech, no music.")


def prompt(clip, first=False):
    p = PAINT + P1 + SCENES[clip] + "\n\n" + BEATS[clip] + (STYLE_FIRST if first else STYLE_REST) + STYLE_END
    low = p.lower()
    assert "mouth" not in low and "smil" not in low and "happ" not in low and "angr" not in low, clip
    return p


if __name__ == "__main__":
    style, turn = sys.argv[1:3]
    first = "first=1" in sys.argv
    extra = [a.split("=", 1)[1] for a in sys.argv[3:] if a.startswith("also=")]        # more image references (the key art)
    reqs = []
    for arg in sys.argv[3:]:
        if arg == "first=1" or arg.startswith("also="):
            continue
        clip, ids = arg.split("=")
        vid, _, expr = ids.partition(",")
        p = prompt(clip, first)
        medias = [{"value": vid, "role": "video_references"}, {"value": style, "role": "image_references"},
                  {"value": turn, "role": "image_references"}]
        for m in ([expr] if expr else []) + extra:
            medias.append({"value": m, "role": "image_references"})
        (HERE / f"0{clip}-paint.txt").write_text(p + "\n")
        reqs.append({"index": int(clip), "params": {"model": "gemini_omni_flash_1_2", "mode": "edit", "resolution": "720p",
                     "aspect_ratio": "16:9", "medias": medias, "prompt": p}})
    print(json.dumps(reqs))
