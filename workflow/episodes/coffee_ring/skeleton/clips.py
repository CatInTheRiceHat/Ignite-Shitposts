"""Gray skeleton clips for the coffee-ring episode (script v1). exec()'d after rig.py by render_clip.py.

Saucer centre is (CX, 0). Drop radius R is PINNED for the whole drying shot: only its height changes
(that is the physics the episode teaches). Props only move when Sol visibly moves them.
Times are seconds on each clip's own clock; lengths follow the trimmed narrator takes in audio/trim/.
"""
import random

CX, R = 0.2, 0.30


def build_set(ring=0.0, with_cup=True):
    """Table room + white saucer. `ring` 0..1 draws the dried coffee ring on the saucer."""
    build_desk()
    cone("PRP_saucer", "paper", (CX, 0, 0), 0.58, 0.50, 0.04)
    cone("PRP_saucer_well", "frame", (CX, 0, 0.04), 0.42, 0.42, 0.004)
    r = None
    if ring > 0:
        r = torus("PRP_ring", "dark", (CX, 0, 0.046), R, 0.016, scale=(1, 1, 0.45))
    return r


def build_bottle(x, tilt_dir=-1):
    """Dropper bottle standing right of the saucer. Pivots at its base; tilts only while Sol pushes it."""
    piv = empty("RIG_bottle_pivot", (x, 0, 0))
    cone("PRP_bottle_body", "prop", (0, 0, 0), 0.10, 0.10, 0.42, parent=piv)
    cone("PRP_bottle_neck", "prop", (0, 0, 0.42), 0.06, 0.03, 0.22, parent=piv)
    cone("PRP_bottle_cap", "dark", (0, 0, 0.64), 0.03, 0.012, 0.08, parent=piv)
    track(piv, "rotation_euler")
    return piv


def build_drop(h0):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=20, radius=1.0)
    d = mesh_obj("PRP_drop", bm, "water", (CX + 0.0, 0, 0.042), (R, R, h0))
    track(d, "scale")
    return d


def build_specks(n=64, seed=7):
    rnd = random.Random(seed)
    sp = []
    for i in range(n):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.025)
        o = mesh_obj(f"PRP_speck_{i}", bm, "dark", (CX, 0, 0.05))
        track(o, "location")
        sp.append({"o": o, "a": rnd.uniform(0, 2 * math.pi), "r0": math.sqrt(rnd.uniform(0.02, 0.9)) * R,
                   "ph": rnd.random()})
    return sp


def place_specks(sp, u, circulate=False, h=0.07, t=0.0):
    """u 0..1: specks drift from scattered inside the drop to piled on the rim. circulate: loop in place."""
    for s in sp:
        a = s["a"]
        if circulate:
            c = (t * 0.45 + s["ph"]) % 1.0
            if c < 0.5:
                r, z = lerp(0.04, R * 0.96, c / 0.5), 0.05
            else:
                r, z = lerp(R * 0.96, 0.04, (c - 0.5) / 0.5), 0.05 + 0.07
        else:
            k = smooth(u, 0.0, 1.0)
            r, z = lerp(s["r0"], R * 0.97 + 0.012 * (s["ph"] - 0.5), k), 0.05
        s["o"].location = (CX + r * math.cos(a), r * math.sin(a), z)


def sol_look(t, a, b):
    return smooth(t, a, b)


# ---------------------------------------------------------------- 01a
def clip01a():
    """Narrator: "Sol, why are you staring at the table?" 0.12-2.9. Sol taps the dark rim, taps the empty
    middle, then looks up."""
    n = 99
    new_scene("coffee_01a", n)
    build_set(ring=1)
    sol = build_sol((-0.72, -0.25, 0), D(24))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 3.3)
        cam.location = lerp3((-0.25, -1.6, 3.0), (-0.2, -3.5, 1.4), k)
        tgt.location = lerp3((-0.3, -0.1, 0.1), (-0.2, 0, 0.45), k)
        tap1, tap2 = bump(t, 0.35, 0.8), bump(t, 0.95, 1.4)
        up = smooth(t, 1.8, 2.5)
        pose_sol(sol, yaw=24 - 8 * up, lean=-4 * (tap1 + tap2) * (1 - up), pitch=24 * up - 4 * (tap1 + tap2),
                 squash=0.04 * (wobble(t, 0.6) + wobble(t, 1.2)),
                 arm_r=(-40 + 70 * (tap1 + tap2), 18), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 01b
def clip01b():
    """Narrator: "Ohh, you want to know why coffee dries into a ring, not a blob." 0.12-6.55. Sol listens,
    looking up, then nods once at the end."""
    n = 210
    new_scene("coffee_01b", n)
    build_set(ring=1)
    sol = build_sol((-0.68, -0.25, 0), D(14))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 7.0)
        cam.location = lerp3((-0.2, -3.7, 1.35), (-0.2, -2.9, 1.1), k)
        tgt.location = lerp3((-0.2, 0, 0.5), (-0.2, 0, 0.45), k)
        nod = bump(t, 6.0, 6.55)
        idle = 0.8 * math.sin(t * 2.2)
        pose_sol(sol, yaw=14, lean=idle, pitch=22 - 22 * nod, squash=0.015 * math.sin(t * 3.0) + 0.07 * nod,
                 arm_r=(-40, 10), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 02a
def clip02a():
    """Narrator: "Watch." 0-0.45 / "A fresh drop dries fastest at the edge." 1.5-4.4. Sol tips the bottle
    over the saucer with his arm, a drop falls, he lets go and the bottle rocks back upright."""
    n = 147
    BX = CX + 0.72
    new_scene("coffee_02a", n)
    build_set(ring=0)
    bottle = build_bottle(BX)
    drop = build_drop(0.0005)
    sol = build_sol((BX + 0.50, 0.14, 0), D(-16))
    cam, tgt = build_camera(lens=30)
    fall = empty("PRP_falling_drop")
    fd = sphere("PRP_fall_blob", "water", (0, 0, 0), (0.04, 0.04, 0.05), parent=fall)
    track(fall, "location")

    def state(t, f):
        k = smooth(t, 0.4, 4.6)
        cam.location = lerp3((0.8, -4.0, 1.5), (0.9, -3.5, 0.7), k)
        tgt.location = lerp3((0.8, 0, 0.4), (0.9, 0, 0.22), k)
        push = smooth(t, 0.2, 1.1)
        let_go = smooth(t, 2.05, 2.4)
        tilt = 68 * push * (1 - let_go) + 8 * wobble(t, 2.4, freq=14, decay=5)     # rocks back upright
        bottle.rotation_euler = (0, D(-tilt), 0)
        nz = (BX - 0.69 * math.sin(D(tilt)), 0, 0.04 + 0.69 * math.cos(D(tilt)))
        tt = clamp01((t - 1.25) / 0.45)
        fall.location = (lerp(nz[0], CX, tt), 0, lerp(nz[2], 0.07, tt * tt)) if 1.25 < t < 1.7 else (0, 0, -5)
        drop.scale = (R, R, 0.0005 + 0.16 * smooth(t, 1.7, 2.2) - 0.03 * smooth(t, 2.8, 4.6))
        up = smooth(t, 2.4, 3.0)
        sol['root'].location = (BX + 0.50 - 0.16 * push * (1 - let_go), 0.14, 0.0)
        pose_sol(sol, yaw=-16 + 4 * up, lean=-16 * push * (1 - let_go), pitch=16 * up,
                 squash=0.05 * wobble(t, 2.4, decay=4),
                 arm_l=(-40 + 24 * push * (1 - let_go), 22 * push * (1 - let_go)), arm_r=(-40, 0))
    return animate(n, state)


def clamp01(x):
    return min(1.0, max(0.0, x))


# ---------------------------------------------------------------- 02b
def clip02b():
    """Narrator: "But the edge is stuck to the saucer," 0.28-2.15 / "so it can't shrink inward." 2.87-4.7.
    The drop's rim stays put while its top sinks. Sol points at the rim, then looks up."""
    n = 147
    new_scene("coffee_02b", n)
    build_set(ring=0)
    drop = build_drop(0.14)
    sol = build_sol((-0.05, 0.85, 0), D(10))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 4.9)
        cam.location = lerp3((0.0, -1.9, 0.42), (0.35, -1.55, 0.2), k)
        tgt.location = lerp3((CX - 0.05, 0.2, 0.2), (CX + 0.1, 0.2, 0.1), k)
        drop.scale = (R, R, 0.14 - 0.07 * smooth(t, 0.0, 4.9))
        pt = bump(t, 0.4, 1.6)
        up = smooth(t, 3.3, 4.0)
        pose_sol(sol, yaw=10, lean=-5 * pt, pitch=6 + 14 * up, squash=0.03 * wobble(t, 0.5),
                 arm_r=(-40 + 55 * pt, 10), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 03
def clip03():
    """Narrator: "So water rushes out from the middle to refill it." 0.34-2.8. Side cutaway: specks ride
    the flow out along the bottom and back across the top. Sol watches and follows the flow with his gaze."""
    n = 108
    new_scene("coffee_03", n)
    build_set(ring=0)
    drop = build_drop(0.13)
    specks = build_specks()
    sol = build_sol((-0.05, 0.85, 0), D(10))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 3.6)
        cam.location = lerp3((-0.1, -1.9, 0.34), (0.5, -1.7, 0.26), k)
        tgt.location = lerp3((CX - 0.1, 0.2, 0.12), (CX + 0.1, 0.2, 0.12), k)
        drop.scale = (R, R, 0.13)
        place_specks(specks, 0, circulate=True, t=t)
        look = 0.5 + 0.5 * math.sin(t * 2.0)
        pose_sol(sol, yaw=10 - 6 * look, lean=2 * look, pitch=6 + 8 * look, squash=0.015 * math.sin(t * 3),
                 arm_r=(-40, 8), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 04
def clip04():
    """Narrator: "And it carries every coffee speck with it," 0.48-2.75 / "and dumps them at the edge." 3.26-4.4.
    Specks stream out and pile on the rim, the middle clears. Sol pushes his own little pile outward."""
    n = 153
    new_scene("coffee_04", n)
    build_set(ring=0)
    drop = build_drop(0.05)
    specks = build_specks()
    sol = build_sol((-0.6, -0.45, 0), D(34))
    cam, tgt = build_camera(lens=30)
    pile = sphere("PRP_sol_pile", "dark", (-0.28, -0.1, 0.05), (0.035, 0.035, 0.02))
    track(pile, "location")

    def state(t, f):
        k = smooth(t, 0.0, 5.0)
        cam.location = lerp3((-0.45, -3.1, 1.5), (-0.3, -2.5, 1.35), k)
        tgt.location = (-0.4, -0.05, 0.1)
        u = smooth(t, 0.4, 4.4)
        place_specks(specks, u)
        drop.scale = (R, R, 0.05 * (1 - 0.85 * smooth(t, 3.0, 5.0)))
        sweep = smooth(t, 1.0, 3.4)
        pile.location = (lerp(-0.28, -0.08, sweep), lerp(-0.1, -0.02, sweep), 0.05)
        pt = bump(t, 0.7, 3.6)
        up = smooth(t, 4.0, 4.6)
        pose_sol(sol, yaw=34 - 14 * up, lean=-8 * pt, pitch=-2 * pt + 20 * up, squash=0.03 * wobble(t, 3.4),
                 arm_r=(-40 + 45 * pt, 12), arm_l=(-40, 0))
    return animate(n, state)


# ---------------------------------------------------------------- 05
def clip05():
    """Narrator: "So the ring isn't a mess. It's every speck, delivered to the edge. Got it?" 0.12-6.55 (take audio/edit/05.wav).
    Sol points at the finished ring, looks up, nods twice. Ends on the second nod."""
    n = 234
    new_scene("coffee_05", n)
    build_set(ring=1)
    sol = build_sol((-0.72, -0.25, 0), D(22))
    cam, tgt = build_camera(lens=30)

    def state(t, f):
        k = smooth(t, 0.0, 7.8)
        cam.location = lerp3((-0.2, -2.4, 1.0), (-0.2, -3.6, 1.4), k)
        tgt.location = lerp3((-0.25, 0, 0.12), (-0.2, 0, 0.45), k)
        point = bump(t, 1.0, 3.6)
        up = smooth(t, 3.6, 4.4)
        nod = bump(t, 6.6, 7.15) + bump(t, 7.15, 7.7)
        pose_sol(sol, yaw=22 - 8 * up, lean=-6 * point, pitch=24 * up - 22 * nod, squash=0.07 * nod + 0.03 * wobble(t, 1.0),
                 arm_r=(-40 + 62 * point, 15), arm_l=(-40, 0))
    return animate(n, state)
