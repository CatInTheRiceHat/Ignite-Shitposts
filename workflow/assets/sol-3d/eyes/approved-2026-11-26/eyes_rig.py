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

Everything is a location, a scale or one of two material dials, so each value can be keyed per frame (key_eyes).
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
EXPRESSIONS = ("normal", "squeeze", "surprised", "sparkle", "worried", "shocked")
LOOK_RANGE = (0.030, 0.026)          # metres the eyes travel at look = 1 (he is 1.0 tall)


def find_eyes(objects):
    by = {o.name.split(".")[0]: o for o in objects}
    mats = by["SOL_body"].data.materials
    front, back = mats[0].node_tree.nodes, mats[1].node_tree.nodes
    eyes = {"rig": by["RIG_Sol_eyes"], "gloom": by["RIG_Sol_gloom"],
            "shade": {"face": [front["gloom_face"].outputs[0]],
                      "top": [front["gloom_top"].outputs[0], back["gloom_top"].outputs[0]]}, "L": {}, "R": {}}
    for s in ("L", "R"):
        eyes[s] = {"rig": by[f"RIG_Sol_eye_{s}"], "oval": by[f"SOL_eye_{s}_oval"], "chev": by[f"SOL_eye_{s}_chev"],
                   "ring": by[f"SOL_eye_{s}_ring"], "white": by[f"SOL_eye_{s}_ring_white"], "spark": by[f"SOL_eye_{s}_spark"]}
    return eyes


def _show(o, on, k=1.0):
    o.scale = (k, k, k) if on else (0.0, 0.0, 0.0)


def pose_eyes(eyes, expr="normal", blink=0.0, look=(0.0, 0.0), size=1.0, shade="top", gloom=None):
    assert expr in EXPRESSIONS, expr
    if gloom is None:
        gloom = 1.0 if expr in ("worried", "shocked") else 0.0
    eyes["rig"].location = (look[0] * LOOK_RANGE[0], 0.0, look[1] * LOOK_RANGE[1])
    eyes["gloom"].scale = (1.0, 1.0, 1.0) if gloom > 0.5 else (0.0, 0.0, 0.0)
    for key, socks in eyes["shade"].items():
        for sock in socks:
            sock.default_value = gloom if key == shade else 0.0
    round_eyes = expr in ("surprised", "shocked")
    for s in ("L", "R"):
        e = eyes[s]
        e["rig"].scale = (size * (1.0 + 0.12 * blink), 1.0, size * max(1.0 - 0.86 * blink, 0.14))
        _show(e["oval"], expr in ("normal", "sparkle", "worried"))
        _show(e["chev"], expr == "squeeze")
        _show(e["ring"], round_eyes)
        _show(e["white"], round_eyes)
        _show(e["spark"], expr == "sparkle" and blink < 0.5)


def eye_objects(eyes):
    out = [eyes["rig"], eyes["gloom"]]
    for s in ("L", "R"):
        out += list(eyes[s].values())
    return out


def key_eyes(eyes, frame):
    for o in eye_objects(eyes):
        o.keyframe_insert("location", frame=frame)
        o.keyframe_insert("scale", frame=frame)
    for socks in eyes["shade"].values():
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
    size, gloom = 1.0, 1.0 if expr in ("worried", "shocked") else 0.0
    if last is not None:
        u = t - last
        size = 1.0 + 0.28 * math.exp(-10.0 * u) * math.cos(2 * math.pi * 2.4 * u)      # the new eyes pop, then settle
    return expr, squash, size, gloom


def squash_scale(squash):
    """Body scale for a squash value: wider as he gets shorter, so he keeps his volume."""
    return (1.0 + 0.8 * squash, 1.0 + 0.8 * squash, 1.0 - squash)
