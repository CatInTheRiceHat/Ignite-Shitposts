import json, sys, os, hashlib
# Sixth round (2026-11-27). Clip 6 on open sand (paint v4 redrew the half-built castle in a new place at 3.8 s) and clip 7
# again (paint v6 drew an opening under Sol's eyes for half a second while he flaps his nubs).
# Run on this Mac and, word for word, in the Higgsfield sandbox; the hashes printed must match.
path = os.path.expanduser(sys.argv[1]); d = json.load(open(path))
OPEN = ("OPEN SAND RULE: there is NO sandcastle, no sand tower, no heap or pile of sand, no bucket and no shovel anywhere in this "
        "shot, in any frame: behind the Sols there is only open sand, the pennants and the sea, and nothing new ever appears. ")
q = d["p6v4"]
a, b = q.index("The sandcastle is only begun"), q.index("OUR SOL is the plain one")
d["p6v5"] = q[:a] + OPEN + q[b:]
q = d["p7v6"]
old = "he flaps both nubs up and down quickly, in turn."
assert old in q
d["p7v7"] = q.replace(old, old + " While he flaps, his face does not change at all: plain smooth cream with his two navy oval eyes "
                      "and nothing else on it, nothing drawn under the eyes.", 1)
json.dump(d, open(path, "w"))
for k in ("p6v5", "p7v7"):
    low = d[k].lower()
    assert "mouth" not in low and "smil" not in low and "happ" not in low and "angr" not in low, k
    print(k, len(d[k]), hashlib.sha256(d[k].encode()).hexdigest()[:16])
