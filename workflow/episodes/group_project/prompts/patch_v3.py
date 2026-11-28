import json, sys, os, hashlib
# Third round of prompts (2026-11-27): clip 4b (new two-Sol shot), clip 6 and clip 7 without ring eyes on the teammates.
# Run on this Mac and, word for word, in the Higgsfield sandbox; the hashes printed must match.
path = os.path.expanduser(sys.argv[1]); d = json.load(open(path))
p3, p6, p7 = d["p3"], d["p6"], d["p7"]
pre = p3[:p3.index("Scene:")]
suf = p3[p3.index("\n\nStyle:"):]
beach = p3[p3.index("Scene:"):p3.index("One wooden notice board")]
castle = p7[p7.index("The sandcastle is only begun"):p7.index("OUR SOL is the plain one")]
ours_ring = p7[p7.index("OUR SOL is the plain one"):p7.index("HAT SOL is the figure")]
ground = p3[p3.index("GROUND RULE:"):p3.index("\n\nStyle:")]
EYES = ("EYE RULE: in this shot every eye is a plain solid navy oval, or a small navy curved line when it is shut, except where a "
        "beat names another shape. No eye ever has a white part, a pupil, a ring, a highlight or a lash. FACE RULE: every face is plain "
        "smooth cream with only its two eyes on it; nothing is ever drawn under the eyes. COUNT RULE: paint exactly the Sols named "
        "here, never one more; no Sol appears from nowhere, disappears or is drawn twice. ")
SHUT = "two small navy curved lines, like gently closed eyes"
DOME = "two small navy half-ovals, flat along the bottom and rounded on top"
d["p4b"] = (pre + beach + castle + ours_ring + "\n\nBeats: 1. The camera is low and pushes in very slowly; nothing else about the view "
            "changes. TWO Sols stand side by side facing the camera: OUR SOL on the left and RING SOL on the right. 2. Ring Sol rocks "
            "gently from side to side with his eyes " + SHUT + ". 3. At 0.35 seconds one small name sign drops straight down from above "
            "and lands upright in the sand just to the left of Ring Sol, between the two Sols: a blank pale peach card on a short "
            "wooden stick; it rocks once and stays. 4. At 0.4 seconds Ring Sol jolts with a small hop and both nubs up; his eyes open "
            "as two plain navy ovals and one small navy exclamation mark floats above him until 1.25 seconds. He looks at the sign, "
            "looks away, and snaps back to it. 5. At 1.4 seconds a second name sign drops and lands upright in the sand just to the "
            "left of our Sol: a blank pale yellow card on a short wooden stick; it rocks once and stays. 6. Our Sol glances at it, then "
            "at 1.7 seconds he stretches up tall and tilts back, his eyes become " + DOME + ", and one small yellow four-point star "
            "floats beside him. He holds that to the last frame. SIGN RULE: each card is completely BLANK, a plain flat pastel colour "
            "with no writing, and after it lands it stays exactly where it is. " + EYES + ground + suf)
a, b = p6.index("4. Ring Sol and Hat Sol look up"), p6.index("6. At 3.6 seconds")
q = (p6[:a] + "4. Ring Sol and Hat Sol look up at the paper with their plain navy oval eyes; their eyes never change. 5. Sleepy Sol hops "
     "in with his eyes " + SHUT + " and small navy sleep marks above him. At 3.1 seconds he jolts upright with both nubs up: the sleep "
     "marks are gone, his eyes open as two plain navy ovals, and one small navy exclamation mark floats above him; then he looks up at "
     "the paper too. " + p6[b:])
d["p6v3"] = q.replace("GROUND RULE:", EYES + "BOARD RULE: the notice board is one plain smooth wooden frame on two plain wooden legs, "
                      "exactly as the source shows it, not rough planks. GROUND RULE:", 1)
old = "over to Ring Sol, lands right beside him, and from 1.95 to 3.0 seconds holds up the nub nearest him."
assert old in p7
q = p7.replace(old, "toward Ring Sol and lands a little way to his left, with a clear gap of sand between the two of them; from 1.95 to 3.0 "
               "seconds he holds up the nub nearest Ring Sol. STAY RULE: our Sol stays in view at the left of the frame, in front of "
               "everything, from this moment to the last frame; he never leaves, never hides behind anyone and never fades out.")
a, b = q.index("3. At 2.2 seconds Ring Sol jolts"), q.index(" From 3.45 to 4.1 seconds")
q = (q[:a] + "3. At 2.2 seconds Ring Sol jolts with a small hop, both nubs up, and one small navy exclamation mark floats above him; "
     "his eyes stay two plain navy ovals. 4. At 2.9 seconds the exclamation mark is gone; he nods once (3.0 to 3.4)." + q[b:])
d["p7v3"] = q.replace("GROUND RULE:", EYES + "GROUND RULE:", 1)
json.dump(d, open(path, "w"))
for k in ("p4b", "p6v3", "p7v3"):
    low = d[k].lower()
    assert "mouth" not in low and "smil" not in low and "happ" not in low
    print(k, len(d[k]), hashlib.sha256(d[k].encode()).hexdigest()[:16])
