"""Drive Sol's separate eyes (sol-eyes.blend). exec() or import inside Blender.

    eyes = find_eyes(objects)                 # objects: any iterable of bpy objects that includes his body and eye rig
    pose_eyes(eyes, "normal")                 # his resting navy ovals
    pose_eyes(eyes, "squeeze")                # > <  with round tips
    pose_eyes(eyes, "surprised")              # O O with white inside
    pose_eyes(eyes, "sparkle")                # normal eyes with white sparkles
    pose_eyes(eyes, "worried")                # normal eyes, a purple shade fading down from the top, thin lines at the side
    pose_eyes(eyes, "shocked")                # the worried shade and lines with the O O eyes
    pose_eyes(eyes, "normal", blink=1.0)      # blink: 0 open .. 1 shut (a flat line)
    pose_eyes(eyes, "normal", look=(-1, 0))   # glance: x -1 his right .. +1 his left, z -1 down .. +1 up
    pose_eyes(eyes, "surprised", size=1.15)   # pop the eyes bigger or smaller for a beat
    pose_eyes(eyes, "worried", shade="face")  # the shade on his face only. The default, "top", runs from his flame tip
                                              # down: Elaine picked that one ("i think i like B")
    pose_eyes(eyes, "worried", gloom=0.5)     # fade the worried shade and lines in or out (0..1)

MORE EMOTIONS (2026-11-26, Elaine: "angry and sad ... and all other emotions that one could need"). The full list
is EXPR below; each is a pair of eye shapes, an optional shade and optional marks:
    pose_eyes(eyes, "angry")                  # her design: the O O eyes cut into half rings that tilt down into the
                                              # middle, with a RED shade from his flame tip instead of the indigo one
    pose_eyes(eyes, "awe", t=1.3)             # sparkle eyes with yellow four-point stars around him; t (seconds)
                                              # makes the marks move: stars twinkle, tears drip, the vein throbs
    pose_eyes(eyes, "normal", marks=("sweat",))   # any marks on any face
Marks: blush tear sweat vein (on his body) and stars burst flowers exclaim question bulb dots notes zzz
brokenheart shiver puff spray (floating just in front of him).

Everything is a location, a scale, a turn or a material dial, so each value can be keyed per frame (key_eyes).
The pieces stay pressed onto his face by their Shrinkwrap modifiers wherever they slide.

EVERY CHANGE OF EMOTION GETS A BOUNCE (Elaine, 2026-11-26: "everytime u swap emotions make sure theres a bounce
that acts as a transition between one emotion to the other"). Do not swap an expression on a still body. Use:

    timeline = [(0.0, "normal"), (1.0, "squeeze"), (2.0, "surprised")]      # (time in seconds, expression)
    expr, squash, size, gloom = emotion_at(t, timeline)
    pose_eyes(eyes, expr, size=size, gloom=gloom)
    body.scale = squash_scale(squash)           # or add `squash` to the squash you already give pose_sol()

He dips into a squash just before the swap, the face changes at the bottom of the dip, then he springs up past
his normal height and settles, and the new eyes pop a little big and settle with him.
"""
import math

# name: eyes (one shape, or (his right eye, his left eye)), shade (None, "indigo", "red"), lines, marks
#   eye shapes: oval chev ring angry half dome arc closed spiral cross heart (sad, u: unused), and "spark" = oval with sparkles
def _e(eyes, shade=None, lines=False, marks=()):
    return {"eyes": eyes if isinstance(eyes, tuple) else (eyes, eyes), "shade": shade, "lines": lines, "marks": tuple(marks)}


EXPR = {
    # the first six are the approved set (2026-11-26)
    "normal": _e("oval"), "squeeze": _e("chev"), "surprised": _e("ring"), "sparkle": _e("spark"),
    "worried": _e("oval", "indigo", True), "shocked": _e("ring", "indigo", True),
    # angry family: half rings tilted down into the middle; the shade is red
    "angry": _e("angry", "red"), "furious": _e("angry", "red", marks=("vein",)), "determined": _e("angry"),
    # sad family: the same closed eyes as bashful. Elaine, 2026-11-26: "can the sad and crying eyes be the same as bashful
    # and also heartbroken and gloomy". (Tried before that, both still in the file and unused: half rings tilted down to
    # the outside, shape "sad"; then two deep letter U's, shape "u".)
    "sad": _e("closed"), "crying": _e("closed", marks=("tear",)), "gloomy": _e("closed", "indigo", True),
    "heartbroken": _e("closed", marks=("brokenheart",)),
    # happy family
    "happy": _e("arc"), "joy": _e("arc", marks=("flowers",)), "excited": _e("arc", marks=("burst",)),
    "laughing": _e("chev", marks=("burst",)), "singing": _e("arc", marks=("notes",)),
    "awe": _e("spark", marks=("stars",)), "love": _e("heart", marks=("blush",)), "wink": _e(("oval", "arc")),
    "content": _e("closed"), "shy": _e("oval", marks=("blush",)), "bashful": _e("closed", marks=("blush",)),
    # thinking and reacting
    "idea": _e("ring", marks=("bulb",)), "thinking": _e("oval", marks=("dots",)), "confused": _e("oval", marks=("question",)),
    "startled": _e("ring", marks=("exclaim",)), "amazed": _e("ring", marks=("burst",)),
    # uneasy
    "nervous": _e("oval", marks=("sweat",)), "panic": _e("ring", marks=("spray",)), "scared": _e("ring", "indigo", marks=("shiver",)),
    # low energy
    "sleepy": _e("half"), "asleep": _e("closed", marks=("zzz",)), "smug": _e("dome", marks=("stars1",)),
    "sigh": _e("closed", marks=("puff",)), "dizzy": _e("spiral"), "ko": _e("cross"),
}
EXPRESSIONS = tuple(EXPR)
SHAPES = ("oval", "chev", "ring", "angry", "sad", "u", "half", "dome", "arc", "closed", "spiral", "cross", "heart")
# the white inside a shape. Sad has none: Elaine, 2026-11-26, "can the sad and crying just be the black eyes without the
# white inners" (the sad_white pieces stay in the file, never shown)
WHITES = {"ring": "ring_white", "angry": "angry_white"}
HIDDEN = ("sad_white",)
MARKS = ("blush", "tear", "sweat", "vein", "stars", "burst", "flowers", "exclaim", "question", "bulb", "dots", "notes",
         "zzz", "brokenheart", "shiver", "puff", "spray")
LOOK_RANGE = (0.030, 0.026)          # metres the eyes travel at look = 1 (he is 1.0 tall)


def find_eyes(objects):
    by = {o.name.split(".")[0]: o for o in objects}
    mats = by["SOL_body"].data.materials
    front, back = mats[0].node_tree.nodes, mats[1].node_tree.nodes
    eyes = {"rig": by["RIG_Sol_eyes"], "gloom": by["RIG_Sol_gloom"],
            "shade": {"face": [front["gloom_face"].outputs[0]],
                      "top": [front["gloom_top"].outputs[0], back["gloom_top"].outputs[0]]},
            "red": [n["shade_red"].outputs[0] for n in (front, back) if "shade_red" in n],
            "marks": {}, "L": {}, "R": {}}
    for s in ("L", "R"):
        e = {"rig": by[f"RIG_Sol_eye_{s}"], "spark": by[f"SOL_eye_{s}_spark"]}
        for shape in SHAPES + tuple(WHITES.values()) + HIDDEN:
            if f"SOL_eye_{s}_{shape}" in by:              # the approved 2026-11-26 file has only the first three
                e[shape] = by[f"SOL_eye_{s}_{shape}"]
        e["white"] = e.get("ring_white")                  # old name, kept for callers
        eyes[s] = e
    for name in MARKS:
        found = sorted((k, o) for k, o in by.items() if k.startswith(f"SOL_mark_{name}_"))
        if found:
            eyes["marks"][name] = [o for _, o in found]
    return eyes


def _show(o, on, k=1.0):
    o.scale = (k, k, k) if on else (0.0, 0.0, 0.0)


def mark_motion(name, i, t):
    """How mark `name` number i moves at time t (seconds): (dx, dz in metres, scale, turn in radians)."""
    if t is None:
        return 0.0, 0.0, 1.0, 0.0
    w = 2 * math.pi
    if name == "stars":            # twinkle: each star swells and shrinks in its own time. Always upright (her note)
        return 0.0, 0.0, 0.80 + 0.26 * abs(math.sin(w * (0.55 * t + 0.19 * i))), 0.0
    if name == "burst":            # the two sets flash in turn
        return 0.0, 0.0, 0.78 + 0.30 * (math.sin(w * (2.2 * t + 0.5 * i)) > 0), 0.0
    if name == "flowers":          # drift up and sway
        return 0.012 * math.sin(w * (0.6 * t + 0.25 * i)), 0.014 * math.sin(w * (0.45 * t + 0.4 * i)), 1.0, 0.5 * math.sin(w * (0.35 * t + 0.2 * i))
    if name in ("tear", "sweat"):  # a drop swells, slides down and is replaced
        u = (0.9 * t + 0.5 * i) % 1.0
        return 0.0, -0.040 * u * u, min(u * 4, 1.0) * (1.0 - max(u - 0.8, 0.0) * 5), 0.0
    if name == "vein":             # throbs
        return 0.0, 0.0, 1.0 + 0.16 * abs(math.sin(w * 1.6 * t)), 0.0
    if name == "exclaim":          # a quick hop
        return 0.0, 0.020 * abs(math.sin(w * 1.5 * t)), 1.0, 0.0
    if name == "question":         # tips from side to side
        return 0.0, 0.0, 1.0, 0.22 * math.sin(w * 0.8 * t)
    if name == "bulb":             # glows
        return 0.0, 0.0, 1.0 + 0.08 * math.sin(w * 1.2 * t), 0.0
    if name == "dots":             # one, two, three, then again
        return 0.0, 0.0, 1.0 if (0.7 * t) % 1.0 * 4 >= i + 0.6 else 0.0, 0.0
    if name == "notes":            # bob
        return 0.0, 0.018 * math.sin(w * (1.0 * t + 0.5 * i)), 1.0, 0.18 * math.sin(w * (1.0 * t + 0.5 * i))
    if name == "zzz":              # rise and fade, one after another
        u = (0.5 * t - 0.22 * i) % 1.0
        return 0.02 * u, 0.03 * u, math.sin(math.pi * min(u * 1.6, 1.0)) ** 0.5, 0.0
    if name == "brokenheart":
        return 0.0, -0.010 * abs(math.sin(w * 0.5 * t)), 1.0, 0.10 * math.sin(w * 0.5 * t)
    if name == "shiver":           # shakes fast
        return 0.007 * math.sin(w * 9 * t + i), 0.0, 1.0, 0.0
    if name == "puff":             # drifts away and thins out
        u = (0.5 * t) % 1.0
        return -0.05 * u, -0.01 * u, 0.6 + 0.6 * u if u < 0.8 else 1.08 * (1 - u) * 5, 0.0
    if name == "spray":            # drops fly outward
        u = (1.3 * t + 0.33 * i) % 1.0
        s = -1 if i != 1 else 1
        return 0.05 * u * s, 0.045 * u, math.sin(math.pi * u) ** 0.5, 0.0
    return 0.0, 0.0, 1.0, 0.0


def pose_eyes(eyes, expr="normal", blink=0.0, look=(0.0, 0.0), size=1.0, shade="top", gloom=None, marks=None, t=None):
    assert expr in EXPR, expr
    spec = EXPR[expr]
    if gloom is None:
        gloom = 1.0 if spec["shade"] else 0.0
    if marks is None:
        marks = spec["marks"]
    eyes["rig"].location = (look[0] * LOOK_RANGE[0], 0.0, look[1] * LOOK_RANGE[1])
    # the worried lines go with the indigo shade (also when a caller fades that shade over a plain face, as before);
    # the red shade and the scared face have none
    lines = gloom > 0.5 and (spec["lines"] or spec["shade"] is None)
    eyes["gloom"].scale = (1.0, 1.0, 1.0) if lines else (0.0, 0.0, 0.0)
    for key, socks in eyes["shade"].items():
        for sock in socks:
            sock.default_value = gloom if key == shade else 0.0
    for sock in eyes["red"]:
        sock.default_value = 1.0 if spec["shade"] == "red" else 0.0
    for s, shape in zip(("L", "R"), spec["eyes"]):
        e = eyes[s]
        base = "oval" if shape == "spark" else shape
        e["rig"].scale = (size * (1.0 + 0.12 * blink), 1.0, size * max(1.0 - 0.86 * blink, 0.14))
        for name in SHAPES + tuple(WHITES.values()) + HIDDEN:
            if name in e:
                _show(e[name], name == base or name == WHITES.get(base))
        _show(e["spark"], shape == "spark" and blink < 0.5)
    want = {}
    for m in marks:
        if m == "stars1":                                  # one star only (smug)
            want["stars"] = (1,)
        else:
            want[m] = None
    for name, objs in eyes["marks"].items():
        for i, o in enumerate(objs):
            on = name in want and (want[name] is None or i in want[name])
            dx, dz, k, turn = mark_motion(name, i, t) if on else (0.0, 0.0, 0.0, 0.0)
            b = o["base"]
            o.location = (b[0] + dx, b[1], b[2] + dz)
            o.rotation_euler = (0.0, turn, 0.0)
            k *= size if on else 0.0
            o.scale = (k, k, k)


def eye_objects(eyes):
    out = [eyes["rig"], eyes["gloom"]]
    for s in ("L", "R"):
        out += [o for k, o in eyes[s].items() if k != "white"]
    for objs in eyes["marks"].values():
        out += objs
    return out


def key_eyes(eyes, frame):
    for o in eye_objects(eyes):
        o.keyframe_insert("location", frame=frame)
        o.keyframe_insert("scale", frame=frame)
        if o.name.startswith("SOL_mark_"):
            o.keyframe_insert("rotation_euler", frame=frame)
    for socks in list(eyes["shade"].values()) + [eyes["red"]]:
        for sock in socks:
            sock.keyframe_insert("default_value", frame=frame)


# ---------------------------------------------------------------- the bounce between emotions
DIP = 0.12            # seconds of squash before the swap
SQUASH = 0.17         # how deep the dip is
SPRING = (9.0, 3.2)   # how fast the spring dies out, and how many wobbles a second


def emotion_bounce(t, switch):
    """Squash for one swap at time `switch`: positive = squashed down, negative = stretched up."""
    if t < switch - DIP:
        return 0.0
    if t < switch:
        x = (t - (switch - DIP)) / DIP
        return SQUASH * x * x * (3 - 2 * x)
    u = t - switch
    return SQUASH * math.exp(-SPRING[0] * u) * math.cos(2 * math.pi * SPRING[1] * u)


def emotion_at(t, timeline):
    """timeline: [(time, expression), ...] in time order; the first entry is the starting face (no bounce for it).
    Returns (expression, squash, eye size, gloom) for time t."""
    expr, last = timeline[0][1], None
    squash = 0.0
    for when, name in timeline[1:]:
        squash += emotion_bounce(t, when)
        if t >= when:
            expr, last = name, when
    size, gloom = 1.0, 1.0 if EXPR[expr]["shade"] else 0.0
    if last is not None:
        u = t - last
        size = 1.0 + 0.28 * math.exp(-10.0 * u) * math.cos(2 * math.pi * 2.4 * u)      # the new eyes pop, then settle
    return expr, squash, size, gloom


def squash_scale(squash):
    """Body scale for a squash value: wider as he gets shorter, so he keeps his volume."""
    return (1.0 + 0.8 * squash, 1.0 + 0.8 * squash, 1.0 - squash)
