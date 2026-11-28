import json, sys, os, hashlib
# Seventh round (2026-11-27), after Elaine's notes on cut v7: clip 2 ends CONFIDENT with his nubs on his sides (no glare),
# clip 7 has the hash marks and the fast nubs rigged in the skeleton, clip 8 has "1st" on the ribbon in the skeleton and
# flowers and sparkles round every Sol on the cheer.
# Run on this Mac and, word for word, in the Higgsfield sandbox; the hashes printed must match.
path = os.path.expanduser(sys.argv[1]); d = json.load(open(path))

# ---- clip 2
q = d["p2v3"]
a, b = q.index("6. At 4.4 seconds his eyes become"), q.index("FACE RULE:")
d["p2v4"] = (q[:a] + "6. At 4.4 seconds he dips once and then stands up tall and sure of himself: he plants BOTH nubs on his sides, tucked "
             "against his body like hands on hips, puffs up a little and tilts back to look up. His eyes become two plain solid navy "
             "ovals; he blinks once at 5.6 seconds. He holds that pose, nubs on his sides, to the last frame. PLAIN EYE RULE: from 4.4 "
             "seconds to the last frame his eyes are two plain solid tall navy ovals and nothing else: no white in them, no flat top, "
             "no lid, no slant. STILL SET RULE: the sandcastle, the bucket, the shovel, the pennants and the poles behind him stay "
             "exactly as they are in every frame of the close view; nothing behind him changes, appears or disappears. " + q[b:])

# ---- clip 7
q = d["p7v7"]
old = "The small floating marks near a figure (dots, a light bulb, a question mark, an exclamation mark, sleep marks, a star, music notes, drops, a little puff, flowers)"
assert old in q
q = q.replace(old, "The small floating marks near a figure (dots, a light bulb, a question mark, an exclamation mark, sleep marks, a star, "
              "music notes, drops, a little puff, flowers, short curved motion lines)", 1)
old = ("he flaps both nubs up and down quickly, in turn. While he flaps, his face does not change at all: plain smooth cream with his "
       "two navy oval eyes and nothing else on it, nothing drawn under the eyes.")
assert old in q
d["p7v8"] = q.replace(old, "he flaps both nubs up and down VERY fast, in turn, about six times a second, exactly as the source shows. "
                      "MOTION LINE RULE: while he flaps, three short curved brown motion lines, like ))) , shake beside each nub, exactly "
                      "where the source shows them, the same size and the same number; copy them from the source and add no others. At "
                      "4.9 seconds they are gone. While he flaps, his face does not change at all: plain smooth cream with his two navy "
                      "oval eyes and nothing else on it, nothing drawn under the eyes.", 1)

# ---- clip 8
q = d["p8v2"]
for old, new in (("RIBBON RULE: its cream middle is completely BLANK, with no writing.",
                  "RIBBON RULE: in the source video the ribbon's cream middle carries three blue characters, 1st, in a rounded heavy "
                  "letter. Keep those three characters EXACTLY as the source shows them in every frame: the same shapes, the same "
                  "size, the same place in the middle of the ribbon, always sharp and readable. Do not redraw, restyle, move or "
                  "blur them, and write nothing else anywhere."),
                 ("and small pink and white flowers float around Ring Sol, Hat Sol and Sleepy Sol. They hold that, nubs up, to the last frame.",
                  "and small pink and white flowers and small yellow four-point sparkles float around ALL FOUR of them, our Sol "
                  "included, exactly where the source shows them. FLOWER RULE: from 9.9 seconds to the very last frame the flowers "
                  "and the sparkles stay in the picture around Ring Sol and our Sol, as many as the source shows; they drift and "
                  "twinkle gently and never fade out. They hold that, nubs up, to the last frame."),
                 ("No text, no letters, no numbers, no captions anywhere in the picture, no speech, no music.",
                  "No text, no letters, no numbers and no captions anywhere in the picture EXCEPT the 1st on the ribbon, which stays "
                  "exactly as the source shows it; no speech, no music.")):
    assert old in q, old[:50]
    q = q.replace(old, new, 1)
d["p8v3"] = q

json.dump(d, open(path, "w"))
for k in ("p2v4", "p7v8", "p8v3"):
    low = d[k].lower()
    assert "mouth" not in low and "smil" not in low and "happ" not in low and "angr" not in low, k
    print(k, len(d[k]), hashlib.sha256(d[k].encode()).hexdigest()[:16])
