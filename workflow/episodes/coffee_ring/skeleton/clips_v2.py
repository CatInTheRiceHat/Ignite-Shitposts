"""Skeleton clips for the coffee-ring episode, VERSION 2 (after Elaine sent v1 back, 2026-11-26).

What changed from clips.py, and why (her notes are in guidelines/checklist.md):
  - New backdrop: a sunny morning kitchen with a white counter, not the candle's night desk.
  - No dropper bottle. Sol nudges a one-piece mug and a drop hops out. Nothing has a part that can come off.
  - The demonstration is one object, modelled in its real colours and reused in every clip: the same brown
    drop (same place, same outline R), the same dark specks (same seed), the same ring. Three close-up shots
    show what happens to it. The camera is slow in those shots so a change that should not happen is visible.
Layout on the counter (z = 0): old dried ring A front-left, fresh drop B front-centre, Sol back-left,
mug back-right. exec()'d after rig.py by render_clip.py with CLIPS=clips_v2.py.
Times are seconds on each clip's own clock and follow the takes in audio/v2/edit/.
"""
import random

GRAY.update({"counter": 0.80, "tile": 0.50, "grout": 0.40, "sky": 0.93, "vapor": 0.97, "leaf": 0.36})
A_POS = (-1.3, -0.45)        # old ring
B_POS = (0.0, -0.55)          # fresh drop
SOL_POS = (-0.42, 0.6)
MUG_POS = (0.52, 0.62)
R = 0.30                      # the drop's outline. It never changes once the drop has landed.
COFFEE = (0.38, 0.17, 0.05)
DARK = (0.13, 0.06, 0.03)
MUG = (0.56, 0.70, 0.82)


def color_material(name, rgb, alpha=1.0, rough=0.55):
    m = bpy.data.materials.get(name)
    if not m:
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (rgb[0] ** 2.2, rgb[1] ** 2.2, rgb[2] ** 2.2, 1)
        b.inputs["Roughness"].default_value = rough
        if alpha < 1.0:
            b.inputs["Alpha"].default_value = alpha
            m.surface_render_method = 'BLENDED'
    return m


def paint(o, mat):
    o.data.materials.clear()
    o.data.materials.append(mat)
    return o


def build_kitchen(ring_a=True):
    box("ENV_counter", "counter", (0, -1.4, -0.1), (11, 7.0, 0.2))
    box("ENV_wall", "tile", (0, 2.2, 3.0), (11, 0.2, 9))
    for i in range(4):                                             # tile grout, backsplash only
        box(f"ENV_grout_h{i}", "grout", (0, 2.09, 0.5 + 0.5 * i), (11, 0.02, 0.025))
    for i in range(-10, 11):
        box(f"ENV_grout_v{i}", "grout", (0.5 * i + 0.25, 2.09, 1.0), (0.025, 0.02, 2.0))
    box("ENV_window_pane", "sky", (0.3, 2.08, 3.35), (2.4, 0.05, 2.2))
    for nm, loc, size in [("L", (-0.95, 2.04, 3.35), (0.14, 0.1, 2.48)), ("R", (1.55, 2.04, 3.35), (0.14, 0.1, 2.48)),
                          ("T", (0.3, 2.04, 4.52), (2.64, 0.1, 0.14)), ("B", (0.3, 1.98, 2.2), (2.9, 0.24, 0.14)),
                          ("V", (0.3, 2.04, 3.35), (0.08, 0.08, 2.2))]:
        box("ENV_window_" + nm, "frame", loc, size)
    # moka pot, back left
    cone("PRP_moka_base", "prop", (-1.9, 1.45, 0), 0.22, 0.14, 0.34)
    cone("PRP_moka_top", "prop", (-1.9, 1.45, 0.34), 0.14, 0.22, 0.32)
    cone("PRP_moka_lid", "dark", (-1.9, 1.45, 0.66), 0.2, 0.03, 0.1)
    box("PRP_moka_handle", "dark", (-1.62, 1.45, 0.5), (0.1, 0.05, 0.3))
    # potted herb, back right
    cone("PRP_pot", "prop", (1.95, 1.55, 0), 0.2, 0.27, 0.32)
    for i, (dx, dy, dz, s) in enumerate([(0, 0, 0.5, 0.26), (-0.17, 0.05, 0.42, 0.18), (0.17, -0.04, 0.44, 0.19), (0.03, 0.08, 0.72, 0.17)]):
        sphere(f"PRP_herb_{i}", "leaf", (1.95 + dx, 1.55 + dy, dz), (s, s, s))
    if ring_a:
        build_ring(A_POS, "A")


def build_ring(pos, tag):
    r = torus("PRP_ring_" + tag, "dark", (pos[0], pos[1], 0.006), R - 0.012, 0.02, scale=(1, 1, 0.45))
    paint(r, color_material("COL_dark", DARK, rough=0.8))
    track(r, "scale")
    return r


def build_mug():
    """One-piece mug with its handle on the +X side, away from Sol. Pivots at its base; it only rocks."""
    piv = empty("RIG_mug_pivot", (MUG_POS[0], MUG_POS[1], 0))
    mat = color_material("COL_mug", MUG, rough=0.35)
    paint(cone("PRP_mug_body", "prop", (0, 0, 0), 0.24, 0.24, 0.5, parent=piv), mat)
    paint(torus("PRP_mug_handle", "prop", (0.30, 0, 0.26), 0.12, 0.032, parent=piv, rot=(D(90), 0, 0)), mat)
    paint(cone("PRP_mug_coffee", "dark", (0, 0, 0.45), 0.205, 0.205, 0.045, parent=piv), color_material("COL_coffee_top", COFFEE, rough=0.2))
    track(piv, "rotation_euler")
    return piv


def build_drop():
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=1.0)
    d = mesh_obj("PRP_drop", bm, "dark", (B_POS[0], B_POS[1], 0.0), (R, R, 0.14))
    paint(d, color_material("COL_coffee", COFFEE, alpha=0.82, rough=0.15))
    track(d, "scale", "location")
    return d


def build_specks(n=64, seed=11):
    rnd = random.Random(seed)
    mat = color_material("COL_dark", DARK, rough=0.8)
    sp = []
    for i in range(n):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.021)
        o = paint(mesh_obj(f"PRP_speck_{i}", bm, "dark", (0, 0, -5)), mat)
        track(o, "location")
        sp.append({"o": o, "a": rnd.uniform(0, 2 * math.pi), "r0": math.sqrt(rnd.uniform(0.01, 0.72)) * R,
                   "zf": rnd.uniform(0.15, 0.85), "ph": rnd.random(), "jit": rnd.uniform(-0.012, 0.012)})
    return sp


def place_specks(sp, u, h, t=0.0, hidden=False):
    """u 0..1: how far the outward flow has carried the specks, 0 = scattered through the drop, 1 = all at the rim.
    h is the drop's height now, so the specks stay inside it."""
    for s in sp:
        if hidden:
            s["o"].location = (0, 0, -5)
            continue
        k = smooth(u * 1.35 - 0.35 * s["ph"], 0.0, 1.0)             # staggered: they do not all leave at once
        r = lerp(s["r0"], R * 0.955 + s["jit"], k)
        a = s["a"] + 0.05 * math.sin(t * 1.3 + s["ph"] * 6)         # a tiny drift so the liquid looks alive
        roof = h * math.sqrt(max(0.0, 1 - (r / R) ** 2))
        z = 0.012 + lerp(s["zf"], 0.1, k) * max(roof - 0.02, 0.0)
        s["o"].location = (B_POS[0] + r * math.cos(a), B_POS[1] + r * math.sin(a), z)


def build_wisps(n=10):
    w = []
    for i in range(n):
        o = sphere(f"FX_vapor_{i}", "vapor", (0, 0, -5), (0.02, 0.01, 0.05))
        track(o, "location", "scale")
        w.append({"o": o, "a": 2 * math.pi * i / n + 0.3, "ph": (i * 0.37) % 1.0})
    return w


def pose_wisps(w, t, on=1.0):
    """Thin wisps of vapour rise from the drop's RIM only: that is where it dries fastest."""
    for s in w:
        c = (t / 1.5 + s["ph"]) % 1.0
        x = B_POS[0] + R * 0.97 * math.cos(s["a"]) + 0.03 * math.sin(c * 6 + s["ph"] * 9)
        y = B_POS[1] + R * 0.97 * math.sin(s["a"])
        k = math.sin(c * math.pi) * on
        s["o"].location = (x, y, 0.04 + 0.42 * c) if k > 0.02 else (0, 0, -5)
        s["o"].scale = (0.022 * k, 0.010 * k, 0.07 * k)


def idle(t):
    return 0.012 * math.sin(t * 3.0)


# ---------------------------------------------------------------- 01
def clip01():
    """Narrator: "Sol, what are you staring at?" 0.3-2.3 / "Oh, you want to know why coffee dries into a ring,
    not a blob." 3.3-7.8. Opens close on the old ring, pulls back to Sol and the kitchen. He taps toward the
    ring twice, looks up, listens, nods once."""
    n = 258
    new_scene("coffee2_01", n)
    build_kitchen()
    build_mug()
    sol = build_sol((SOL_POS[0], SOL_POS[1], 0), D(-22))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.5, 3.6)
        cam.location = lerp3((-1.3, -1.75, 0.7), (-1.02, -2.7, 1.05), k)
        tgt.location = lerp3((-1.15, -0.3, 0.12), (-1.0, 0.15, 0.34), k)
        tap = bump(t, 0.5, 1.0) + bump(t, 1.1, 1.6)
        up = smooth(t, 2.3, 3.0)
        nod = bump(t, 7.85, 8.4)
        pose_sol(sol, yaw=-22 + 12 * up, lean=-7 * (1 - up) - 3 * tap, pitch=-8 * (1 - up) + 24 * up - 22 * nod,
                 squash=0.04 * (wobble(t, 0.75) + wobble(t, 1.35)) + 0.07 * nod + idle(t) * up,
                 arm_l=(-40 + 60 * tap, 20 * tap), arm_r=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 02
def clip02():
    """Narrator: "Watch a fresh drop." 0.2-2.1. Sol hops over and nudges the mug with his arm. The mug rocks
    once and settles where it stands; one drop hops from its rim and lands on the counter at B. The mug keeps
    its handle and its shape and never leaves its spot."""
    n = 108
    new_scene("coffee2_02", n)
    build_kitchen()
    mug = build_mug()
    drop = build_drop()
    specks = build_specks()
    sol = build_sol((SOL_POS[0], SOL_POS[1], 0), D(20))
    cam, tgt = build_camera(lens=30)
    blob = paint(sphere("PRP_flying_drop", "dark", (0, 0, -5), (0.075, 0.075, 0.09)), color_material("COL_coffee", COFFEE, alpha=0.82, rough=0.15))
    track(blob, "location")
    rim = (MUG_POS[0] - 0.06, MUG_POS[1] - 0.22, 0.52)
    T0, T1 = 0.82, 1.45

    def state(t, f):
        k = smooth(t, 0.9, 3.3)
        cam.location = lerp3((0.1, -3.0, 1.15), (0.05, -2.05, 0.6), k)
        tgt.location = lerp3((0.1, 0.35, 0.4), (0.05, -0.45, 0.1), k)
        step = smooth(t, 0.25, 0.65) - smooth(t, 1.25, 1.75)
        sol["root"].location = (SOL_POS[0] + 0.20 * step, SOL_POS[1], 0.05 * (bump(t, 0.25, 0.65) + bump(t, 1.25, 1.75)))
        nudge = bump(t, 0.45, 1.05)
        tilt = 10 * bump(t, 0.62, 0.98) + 3.0 * wobble(t, 0.98, freq=16, decay=6)
        mug.rotation_euler = (0, D(tilt), 0)
        u = (t - T0) / (T1 - T0)
        if 0 <= u <= 1:
            p = lerp3(rim, (B_POS[0], B_POS[1], 0.05), u)
            blob.location = (p[0], p[1], p[2] + 0.5 * 4 * u * (1 - u))
        else:
            blob.location = (0, 0, -5)
        land = smooth(t, T1, T1 + 0.18)
        h = 0.14 * smooth(t, T1, T1 + 0.3) + 0.02 * wobble(t, T1 + 0.3, freq=14, decay=6)
        drop.scale = (max(R * land, 0.001), max(R * land, 0.001), max(h, 0.001))
        drop.location = (B_POS[0], B_POS[1], 0.0 if t >= T1 else -1.0)
        place_specks(specks, 0.0, max(h, 0.02), t, hidden=t < T1 + 0.25)
        look = smooth(t, 1.5, 2.2)
        pose_sol(sol, yaw=20 - 22 * look, lean=10 * nudge, pitch=-9 * look,
                 squash=0.05 * (bump(t, 0.6, 0.75) + wobble(t, 1.75, decay=5)) + idle(t),
                 arm_r=(-40 + 58 * nudge, 10 * nudge), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 03
def clip03():
    """CLOSE-UP 1. Narrator: "It dries fastest at its edge," 0.25-3.3 / "but the edge is stuck to the counter,"
    3.6-5.7 / "so it can't shrink inward." 6.3-7.7. The drop fills the frame. Vapour rises from its rim only.
    Its outline stays exactly where it is while its top sinks. Sol and the mug stand behind, out of the way."""
    n = 240
    new_scene("coffee2_03", n)
    build_kitchen()
    build_mug()
    drop = build_drop()
    specks = build_specks()
    wisps = build_wisps()
    sol = build_sol((SOL_POS[0], SOL_POS[1], 0), D(12))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 8.0)
        cam.location = lerp3((-0.16, -2.0, 0.56), (0.06, -1.9, 0.46), k)
        tgt.location = (-0.04, -0.45, 0.12)
        h = lerp(0.14, 0.085, smooth(t, 0.3, 7.7))
        drop.scale = (R, R, h)
        place_specks(specks, 0.0, h, t)
        pose_wisps(wisps, t, on=smooth(t, 0.2, 0.8) * (1 - smooth(t, 5.6, 6.3)))
        pose_sol(sol, yaw=12, lean=1.5 * math.sin(t * 1.1), pitch=-7, squash=idle(t), arm_r=(-40, 0), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 04
def clip04():
    """CLOSE-UP 2. Narrator: "So water rushes out from the middle to refill it," 0.25-4.0 / "and it carries every
    coffee speck with it." 4.0-6.4. Same drop, lower angle. The specks drift outward toward the rim."""
    n = 204
    new_scene("coffee2_04", n)
    build_kitchen()
    build_mug()
    drop = build_drop()
    specks = build_specks()
    sol = build_sol((SOL_POS[0], SOL_POS[1], 0), D(12))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 6.8)
        cam.location = lerp3((0.06, -1.85, 0.30), (-0.14, -1.8, 0.27), k)
        tgt.location = (-0.04, -0.5, 0.08)
        h = lerp(0.085, 0.06, smooth(t, 0.0, 6.8))
        drop.scale = (R, R, h)
        place_specks(specks, 0.72 * smooth(t, 0.4, 6.5), h, t)
        pose_sol(sol, yaw=12, lean=1.5 * math.sin(t * 1.1 + 1), pitch=-7, squash=idle(t), arm_r=(-40, 0), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 05
def clip05():
    """CLOSE-UP 3, from straight above. Narrator: "Then the water dries away," 0.25-2.2 / "and the specks stay,
    piled at the edge." 2.8-5.2. The last specks reach the rim, the water thins to nothing, the ring is left."""
    n = 174
    new_scene("coffee2_05", n)
    build_kitchen()
    build_mug()
    drop = build_drop()
    specks = build_specks()
    ring = build_ring(B_POS, "B")
    fading = color_material("COL_coffee", COFFEE, alpha=0.82, rough=0.15).copy()
    fading.name = "COL_coffee_fading"
    paint(drop, fading)
    alpha = fading.node_tree.nodes["Principled BSDF"].inputs["Alpha"]
    sol = build_sol((SOL_POS[0], SOL_POS[1], 0), D(12))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 5.8)
        cam.location = lerp3((0.0, -0.66, 1.32), (0.0, -0.66, 1.2), k)
        tgt.location = (0.0, -0.74, 0.0)
        h = lerp(0.06, 0.004, smooth(t, 0.4, 3.9))
        drop.scale = (R, R, h)
        # the water thins away gradually: its own copy of the coffee material fades from 0.82 to clear
        fade = smooth(t, 1.0, 4.3)
        alpha.default_value = 0.82 * (1 - fade)
        alpha.keyframe_insert("default_value", frame=f)
        drop.location = (B_POS[0], B_POS[1], -1.0 if fade >= 0.999 else 0.0)
        place_specks(specks, 0.72 + 0.28 * smooth(t, 0.2, 2.9), h, t * (1 - smooth(t, 2.5, 3.2)))
        g = smooth(t, 2.0, 3.5)
        ring.scale = (1, 1, max(0.45 * g, 0.001))
        ring.location = (B_POS[0], B_POS[1], 0.006 if g > 0.01 else -1)
        pose_sol(sol, yaw=12, lean=0, pitch=-7, squash=idle(t), arm_r=(-40, 0), arm_l=(-40, 0))
    track(ring, "location")
    return animate(n, state)


# ---------------------------------------------------------------- 06
def clip06():
    """Narrator: "So the ring isn't a mess. It's every speck, delivered to the edge. Got it?" 0.2-5.15.
    Opens close on the new ring, pulls back to Sol and the kitchen. He points at it, looks up, nods twice.
    The clip ends on the second nod."""
    n = 201
    new_scene("coffee2_06", n)
    build_kitchen()
    build_mug()
    build_ring(B_POS, "B")
    sol = build_sol((SOL_POS[0], SOL_POS[1], 0), D(14))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.3, 5.2)
        cam.location = lerp3((0.05, -1.75, 0.8), (0.05, -2.75, 1.1), k)
        tgt.location = lerp3((0.0, -0.4, 0.1), (0.05, 0.1, 0.32), k)
        point = bump(t, 0.7, 3.3)
        up = smooth(t, 3.4, 4.2)
        nod = bump(t, 5.4, 5.95) + bump(t, 5.95, 6.5)
        pose_sol(sol, yaw=14 - 6 * up, lean=4 * point, pitch=-9 * point + 24 * up - 22 * nod,
                 squash=0.03 * wobble(t, 0.9) + 0.07 * nod + idle(t),
                 arm_r=(-40 + 58 * point, 35 * point), arm_l=(-40, 0))
    return animate(n, state)
