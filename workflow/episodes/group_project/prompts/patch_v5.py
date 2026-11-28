import json, sys, os, hashlib
# Fifth round of prompts (2026-11-27), after Elaine's notes on cut v5: the ring low on Ring Sol in every shot, the fly-in
# passes under the banner, plain eyes at the clock, the "ask one person" shot on open sand with Ring Sol hopping out of
# the frame, clip 4 as the short two-Sol slide, and the later nods of the longer clips 1 and 8.
# Run on this Mac and, word for word, in the Higgsfield sandbox; the hashes printed must match.
path = os.path.expanduser(sys.argv[1]); d = json.load(open(path))


def cut(p, a, b):
    return p[p.index(a):p.index(b)]


p1, p3, p4, p5, p7, p8 = d["p1"], d["p3"], d["p4"], d["p5"], d["p7v4"], d["p8"]
pre = p3[:p3.index("Scene:")]
suf = p3[p3.index("\n\nStyle:"):]
beach = cut(p3, "Scene:", "One wooden notice board")
ground = cut(p3, "GROUND RULE:", "\n\nStyle:")
castle0 = cut(p7, "The sandcastle is only begun", "OUR SOL is the plain one")          # castle, bucket and shovel
umbrella = cut(p4, "One teal beach umbrella", "OUR SOL is the plain one")
OURS = "OUR SOL is the plain one, wearing nothing. "
RING = ("RING SOL is the figure wearing one plain pink inflatable swim ring LOW around the very bottom of his body, down at his "
        "feet, well below his face; the ring is the same in every frame and never comes off. ")
HAT = cut(p7, "HAT SOL is the figure", "SLEEPY SOL is the third")
SLEEPY = "SLEEPY SOL is the third teammate; he wears nothing. "
EYES = ("EYE RULE: in this shot every eye is a plain solid navy oval, or a small navy curved line when it is shut, except where a "
        "beat names another shape. No eye ever has a white part, a pupil, a ring, a highlight or a lash. FACE RULE: every face is plain "
        "smooth cream with only its two eyes on it; nothing is ever drawn under the eyes. ")
COUNT = "COUNT RULE: paint exactly the Sols named here, never one more; no Sol appears from nowhere, disappears or is drawn twice. "
RINGRULE = ("RING RULE: Ring Sol's pink swim ring sits LOW around the very bottom of his body, at his feet; his whole cream face "
            "and his two navy eyes are always clearly visible ABOVE the ring, with plain cream face between the ring and his eyes, "
            "and the ring never covers or touches his eyes. ")
SEA = ("SEA RULE: the calm teal sea is visible as a band across the picture behind the Sols, under the rose and peach sunset sky, "
       "as in the painted reference frame; the sky is not plain orange. ")
SHUT = "two small navy curved lines, like gently closed eyes"
HALF = "two navy half-ovals, flat across the top and rounded below, like half-shut eyes"
ARC = "two small upward-curved navy arcs, like ^ ^"
GLARE = "two navy half-rings with white centres, each cut flat across its top and slanted down toward the middle of his face"
old_ring = "RING SOL is the figure wearing one plain pink inflatable swim ring around his middle; the ring is the same in every frame and never comes off. "

# ---- clip 1: no plan board, the camera passes UNDER the banner, the nod half a second later
board = cut(p1, "One wooden notice board", "Far in the background")
q = p1.replace(board, "", 1)
a, b = q.index("Beats: 1. CAMERA MOVE:"), q.index("2. From the first frame our Sol is busy")
q = (q[:a] + "Beats: 1. CAMERA MOVE: the shot opens high in the air in front of the long blank banner, looking straight at it, and "
     "flies smoothly forward and down. It passes UNDER the banner, between its two poles: the cloth rises and slides out through the "
     "TOP of the frame, whole and solid. The camera never passes through the cloth, and the cloth never fades, splits or dissolves. "
     "Then the camera levels out low on the sand in front of our Sol and his castle at 1.9 seconds, exactly as in the source video. "
     "After that it only creeps in slowly. Only the camera moves; the beach does not change. " + q[b:])
old = "7. At 7.35 seconds he nods once, slowly."
assert old in q
d["p1v2"] = q.replace(old, "He keeps looking up, sagging a little, with a very small idle sway. 7. At 7.85 seconds he nods once, slowly.")

# ---- clip 2: the same beats as paint v2, this film's own style frame, the ring low
d["p2v3"] = (pre + beach + castle0 + umbrella + OURS + RING + HAT + SLEEPY + "\n\nBeats: 1. The shot opens close on our Sol, turned a "
             "little to the right, leaning that way with the nub on that side raised. His eyes are " + GLARE + " and the top of his "
             "flame is a deeper red, exactly as much as the source shows, from the first frame. 2. CAMERA MOVE: from 0.9 to 1.25 "
             "seconds the camera whips quickly to the right, to his three teammates, and holds on them until 2.75 seconds, exactly as "
             "in the source video. 3. The three teammates: at the left RING SOL faces the camera, rocking gently from side to side in "
             "his pink swim ring, his eyes " + SHUT + ", clearly visible on his cream face above the ring. In the middle HAT SOL "
             "stands with his BACK to the camera, looking out at the sea: we see only his plain red-orange back and his straw hat. At "
             "the right SLEEPY SOL stands on the yellow towel under the teal umbrella, leaning, his eyes " + SHUT + ", with small navy "
             "sleep marks floating above him. None of the three moves from his place. 4. CAMERA MOVE: from 2.75 to 3.1 seconds the "
             "camera whips back to our Sol and then pushes in very slowly. 5. Our Sol now faces the camera squarely and stands "
             "perfectly still. The red is gone: he is his normal orange and red from here to the last frame. His eyes are " + HALF +
             ", looking straight at the camera. 6. At 4.4 seconds his eyes become " + GLARE + " (his flame stays normal orange and "
             "red); he stretches up tall, raises both nubs a little and tilts back to look up. He holds that to the last frame. " +
             "FACE RULE: every face is plain smooth cream with only its two eyes on it; nothing is ever drawn under the eyes. " +
             COUNT + RINGRULE + ground + suf)

# ---- clip 4: the short slide past Sleepy Sol and Hat Sol only
d["p4v3"] = (pre + beach + umbrella + HAT + SLEEPY + "\n\nBeats: 1. Only TWO Sols are in this shot: HAT SOL on the left and SLEEPY SOL "
             "on the right, who stands on the yellow towel under the teal umbrella. There is no sandcastle and no bucket in this shot. "
             "CAMERA MOVE: from 0.25 to 2.4 seconds the camera slides slowly sideways from right to left and then holds still, exactly "
             "as in the source video. 2. TWO small name signs drop into the sand: each is one blank pastel card on a short wooden "
             "stick, falling straight down from above, landing upright in the sand and rocking once. The first, a pale green card, "
             "lands at 0.6 seconds just to the LEFT of Sleepy Sol, between the two Sols. The second, a pale blue-grey card, lands at "
             "1.7 seconds just to the left of Hat Sol. SIGN RULE: each card is completely BLANK, a plain flat pastel colour with no "
             "writing, and after it lands it stays exactly where it is. 3. SLEEPY SOL never reacts: he leans a little, his eyes stay " +
             SHUT + ", and small navy sleep marks float above him. 4. HAT SOL starts with his BACK to the camera, looking out at the "
             "sea: we see only his plain red-orange back and his straw hat. From 1.8 to 2.15 seconds he turns round on the spot to "
             "face the camera. At 2.2 seconds he tilts to one side and one small navy question mark floats above him; his eyes are "
             "two plain navy ovals. He holds that to the last frame. " + EYES + COUNT + SEA + ground + suf)

# ---- clip 5: plain eyes to the end (Elaine: "why is he doing this can we just keep it like this")
a, b = p5.index("5. At 3.5 seconds he turns toward the camera"), p5.index("GROUND RULE:")
d["p5v2"] = (p5[:a] + "5. At 3.5 seconds he turns a little toward the camera and stretches up tall, with both nubs raised a little, "
             "and holds that to the last frame. PLAIN EYE RULE: from 1.5 seconds to the last frame our Sol's eyes are two plain solid "
             "tall navy ovals and nothing else, apart from the one blink. They are never half-shut and never get a flat top, a lid, a "
             "line or a brow above them. No star and no other mark floats beside him. " + EYES + p5[b:])

# ---- clip 6: as paint v3, with the ring low
q = d["p6v3"]
assert old_ring in q
d["p6v4"] = q.replace(old_ring, RING, 1).replace("GROUND RULE:", RINGRULE + SEA + "GROUND RULE:", 1)

# ---- clip 7: open sand, Ring Sol at the left; he is asked, nods and hops out of the frame
d["p7v6"] = (pre + beach + "OPEN SAND RULE: this shot is on open, empty sand. There is NO sandcastle, no sand tower, no heap or pile of "
             "sand, no bucket, no shovel and no notice board anywhere in it, in any frame, and nothing new ever appears on the sand. " +
             OURS + RING + HAT + SLEEPY + "\n\nBeats: 1. The shot opens from a high three-quarter angle, looking down a little at four "
             "Sols standing in a row on the open sand, each one clearly a round flame-shaped Sol with his face in view. From left to "
             "right: RING SOL, then OUR SOL, then a wider gap of sand, then HAT SOL and SLEEPY SOL. Ring Sol faces right, toward our "
             "Sol; our Sol faces left, toward Ring Sol; Hat Sol and Sleepy Sol face left, toward our Sol. Sleepy Sol's eyes are " + HALF +
             " until beat 6. CAMERA MOVE: from 1.2 to 1.9 seconds the camera drops down to eye level in front of Ring Sol and our "
             "Sol, exactly as in the source video. 2. From 1.35 to 1.85 seconds our Sol makes one hop toward Ring Sol and lands a "
             "little way to his right, with a clear gap of sand between the two of them; from 1.95 to 3.0 seconds he holds up the nub "
             "nearest Ring Sol. STAY RULE: our Sol stays in full view from the first frame to the last; he never leaves, never hides "
             "behind anyone and never fades out. 3. At 2.2 seconds Ring Sol jolts with a small hop, both nubs up, and one small navy "
             "exclamation mark floats above him; his eyes stay two plain navy ovals. 4. At 2.9 seconds the exclamation mark is gone; "
             "he nods once (3.0 to 3.4). From 3.45 to 4.3 seconds he turns to the left, away from our Sol, and hops away to the left "
             "in four quick hops, straight out past the LEFT edge of the picture. EXIT RULE: Ring Sol leaves only by hopping out past "
             "the left edge; he does not fade, shrink, melt or vanish. After 4.3 seconds he is gone and never comes back: from then "
             "on exactly THREE Sols are in the picture. 5. CAMERA MOVE: from 3.5 to 4.3 seconds the camera slides to the right and "
             "back a little, to show our Sol at the left with Hat Sol and Sleepy Sol at the right. From 3.5 to 3.9 seconds our Sol "
             "turns round on the spot to face right, toward the two of them, and from 4.2 to 4.8 seconds he flaps both nubs up and "
             "down quickly, in turn. 6. At 4.85 seconds Hat Sol and Sleepy Sol both turn away from him at the same moment, toward the "
             "right, and tip their faces up: their eyes become " + ARC + ", and one pink music note and one blue music note float "
             "beside each of them. They sway gently. 7. At 5.3 seconds our Sol lowers his nubs and stands still with two navy oval "
             "eyes and one small pale blue drop on the upper side of his face. He holds that to the last frame. " + EYES +
             "COUNT RULE: four Sols until Ring Sol hops out, then three; no Sol appears from nowhere or is drawn twice. " +
             RINGRULE + SEA + ground + suf)

# ---- clip 8: Ring Sol and our Sol side by side at the left, the nod and the cheer half a second later
q = p8
assert old_ring in q
q = q.replace(old_ring, RING, 1)
for old, new in (("OUR SOL stands at the front left; RING SOL stands just behind him at the left;",
                  "At the left of the picture RING SOL and OUR SOL stand side by side with a small gap of sand between them: Ring Sol "
                  "at the far left, our Sol just to his right. Both are whole and in full view in every frame of the wide view, and "
                  "neither one hides the other;"),
                 ("until 8.8 seconds.", "until 9.3 seconds."),
                 ("5. From 8.8 to 9.3 seconds our Sol nods once, clearly.", "5. From 9.3 to 9.8 seconds our Sol nods once, clearly."),
                 ("6. At 9.4 seconds all four raise both nubs", "6. At 9.9 seconds all four raise both nubs")):
    assert old in q, old
    q = q.replace(old, new, 1)
d["p8v2"] = q.replace("GROUND RULE:", "FACE RULE: every face is plain smooth cream with only its two eyes on it; nothing is ever drawn "
                      "under the eyes, in any frame. " + COUNT + RINGRULE + SEA + "GROUND RULE:", 1)

json.dump(d, open(path, "w"))
for k in ("p1v2", "p2v3", "p4v3", "p5v2", "p6v4", "p7v6", "p8v2"):
    low = d[k].lower()
    assert "mouth" not in low and "smil" not in low and "happ" not in low and "angr" not in low, k
    print(k, len(d[k]), hashlib.sha256(d[k].encode()).hexdigest()[:16])
