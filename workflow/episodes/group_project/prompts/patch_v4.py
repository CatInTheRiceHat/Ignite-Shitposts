import json, sys, os, hashlib
# Fourth round (2026-11-27), after the frame review of cut v2: clip 7 and clip 4b re-shot from higher cameras.
path = os.path.expanduser(sys.argv[1]); d = json.load(open(path))
RULES = ("RING RULE: Ring Sol's pink swim ring sits LOW around the bottom of his body, below his face; his two navy oval eyes are "
         "always clearly visible above the ring whenever he faces the camera, and the ring never covers them. SEA RULE: the calm "
         "teal sea is visible as a band across the picture behind the Sols, under the rose and peach sunset sky, as in the painted "
         "reference frame; the sky is not plain orange. ")
p = d["p7v3"]
old = "1. The shot opens looking down from high above at four Sols on the sand in front of the castle:"
assert old in p
p = p.replace(old, "1. The shot opens from a high three-quarter angle, looking down a little at four Sols on the sand in front of the castle, "
              "each one clearly a round flame-shaped Sol with his face in view:")
d["p7v4"] = p.replace("GROUND RULE:", RULES + "GROUND RULE:", 1)
d["p4bv2"] = d["p4b"].replace("GROUND RULE:", RULES + "GROUND RULE:", 1)
json.dump(d, open(path, "w"))
for k in ("p7v4", "p4bv2"):
    print(k, len(d[k]), hashlib.sha256(d[k].encode()).hexdigest()[:16])
