import json, os, sys
# Clip 4, paint v2 (2026-11-27). Paint v1 added a fifth Sol beside the castle, turned our Sol's back to the camera for
# the last second and a half, and gave Ring Sol eyes with pupils. This rewrites the ring-eye wording and beat 6, and adds
# a count rule. The same file is run on this Mac and in the Higgsfield sandbox, so the prompt is not typed twice.
path = os.path.expanduser(sys.argv[1])
d = json.load(open(path))
p = d["p4"]
ring_old = "two round navy rings with white centres"
ring_new = "two round white eyes, each outlined by one thick navy ring, with no pupil and nothing at all inside the ring"
assert ring_old in p
p = p.replace(ring_old, ring_new)
a = p.index("6. OUR SOL stands at the left end")
b = p.index("GROUND RULE:")
dome = "two small navy half-ovals, flat along the bottom and rounded on top"
p = p[:a] + ("6. OUR SOL is the plain Sol at the left end of the row, standing between the red bucket and Ring Sol. FACE RULE: he FACES THE "
             "CAMERA from the first frame to the last, so his cream face and both eyes are always in view; he never turns round and we "
             "never see his back. His eyes are two navy ovals. When the last sign lands beside him (3.9) he glances at it, then at 4.2 "
             "seconds he stretches up tall and tilts back, his eyes become " + dome + ", and one small yellow four-point star floats "
             "beside HIM, close to his own flame. COUNT RULE: there are exactly FOUR Sols in this shot, the four named above, and never "
             "a fifth; nobody stands at, beside or behind the sandcastle, and no Sol appears or disappears. ") + p[b:]
d["p4v2"] = p
json.dump(d, open(path, "w"))
print(len(p), "mouth" in p.lower(), "happ" in p.lower())
