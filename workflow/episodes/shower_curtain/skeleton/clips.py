"""Skeleton clips for the shower-curtain episode. exec()'d after rig.py by render_clip.py.

Only clip 1 is built so far (Elaine, 2026-11-26: "just do one clip"). The other five are planned in ../script.txt.
Layout (metres; Sol is 1.0 tall): the tub runs along Y, away from the camera. The shower head is on the far wall,
the curtain hangs along the left side (x = XC), the tiled wall is on the right. The near end is cut away for the camera.
Times are seconds on each clip's own clock and follow the trimmed takes in ../audio/edit/.
"""
import random

XC = -0.90                    # the curtain's plane
Y0, Y1 = -1.60, 1.80          # the curtain's two ends
ZH, ZT = 0.22, 3.00           # its hem and its top
YB = -0.40                    # where along its length it bows in the most
BOW = 0.50                    # how far the hem swings in at bow = 1 (it touches Sol's side there)
HEAD = (0.30, 1.395, 2.70)    # the face of the shower head
SPRAY = (0.30, 1.25)          # where the spray lands
SOL = (0.02, -0.95, 0)


def act(sol, t, f, timeline, gloom=None, look=(0.0, 0.0), blinks=(), **pose):
    """Eyes from the emotion timeline (with its bounce), then the body pose with that bounce added."""
    expr, sq, size, g = emotion_at(t, timeline)
    if gloom is not None:
        g = gloom
    bl = blink_at(t, blinks) if expr in ("normal", "worried", "sparkle") else 0.0
    face(sol, f, expr, blink=bl, look=look, size=size, gloom=g)
    pose["squash"] = pose.get("squash", 0.0) + sq
    pose_sol(sol, **pose)


def hz(z):
    """0 at the curtain's top, 1 at its hem."""
    return min(1.0, max(0.0, (ZT - z) / (ZT - ZH)))


def gy(y):
    return 0.45 + 0.55 * math.exp(-((y - YB) / 1.3) ** 2)


# ================================================================ the set
def build_duck(tag, loc, yaw=0.0):
    """A one-piece rubber duck. It never moves."""
    d = empty("RIG_duck_" + tag, loc, rot=(0, 0, D(yaw)))
    sphere("PRP_duck_body_" + tag, "duck", (0, 0, 0.10), (0.13, 0.17, 0.10), parent=d)
    sphere("PRP_duck_tail_" + tag, "duck", (0, 0.15, 0.15), (0.05, 0.07, 0.05), parent=d)
    sphere("PRP_duck_head_" + tag, "duck", (0, -0.09, 0.25), (0.085, 0.085, 0.085), parent=d)
    sphere("PRP_duck_beak_" + tag, "beak", (0, -0.18, 0.235), (0.04, 0.05, 0.02), parent=d)
    for s in (-1, 1):
        sphere(f"PRP_duck_eye_{tag}{s}", "dark", (s * 0.045, -0.155, 0.275), (0.014, 0.014, 0.014), parent=d)
    return d


def build_bathroom():
    # floors: the white tub on the right of the curtain, the room's floor on its left
    box("ENV_floor", "floor", (-4.2, -1.0, -0.1), (6.0, 12, 0.2))
    box("ENV_tub_floor", "tub", (0.0, -2.05, -0.1), (2.4, 7.9, 0.2))
    box("ENV_tub_rim", "tub", (-1.1, -2.05, 0.25), (0.2, 7.9, 0.5))
    # tiled walls of the alcove: the far wall (shower head) and the right wall
    box("ENV_wall_far", "tile", (-0.1, 2.0, 4.0), (2.2, 0.2, 10))
    box("ENV_wall_right", "tile", (1.1, -2.0, 4.0), (0.2, 8.2, 10))
    for i in range(1, 12):
        box(f"ENV_grout_fh{i}", "grout", (-0.1, 1.895, 0.5 * i), (2.2, 0.02, 0.022))
        box(f"ENV_grout_rh{i}", "grout", (0.995, -2.0, 0.5 * i), (0.02, 8.0, 0.022))
    for i in range(4):
        box(f"ENV_grout_fv{i}", "grout", (-0.95 + 0.5 * i, 1.895, 3.0), (0.022, 0.02, 6.0))
    for i in range(14):
        box(f"ENV_grout_rv{i}", "grout", (0.995, 1.65 - 0.5 * i, 3.0), (0.02, 0.022, 6.0))
    # shower head, its arm and the lever, on the far wall
    cone("PRP_shower_arm", "steel", (0.30, 1.9, 2.85), 0.035, 0.035, 0.46, rot=(D(90), 0, 0))
    cone("PRP_shower_head", "steel", (0.30, 1.45, 2.85), 0.05, 0.20, 0.16, rot=(D(160), 0, 0))
    cone("PRP_lever_plate", "steel", (0.30, 1.9, 1.30), 0.15, 0.15, 0.04, rot=(D(90), 0, 0))
    box("PRP_lever", "steel", (0.30, 1.80, 1.22), (0.07, 0.10, 0.30), rot=(0, D(35), 0))
    # a round window and a shelf with bottles and a duck, on the far wall
    cone("PRP_window_rim", "white", (-0.45, 1.9, 2.85), 0.36, 0.36, 0.05, rot=(D(90), 0, 0))
    cone("PRP_window_pane", "sky", (-0.45, 1.86, 2.85), 0.29, 0.29, 0.02, rot=(D(90), 0, 0))
    box("PRP_shelf", "white", (-0.42, 1.76, 1.75), (0.64, 0.28, 0.05))
    cone("PRP_bottle_a", "coral", (-0.64, 1.78, 1.775), 0.065, 0.055, 0.30)
    cone("PRP_bottle_a_cap", "white", (-0.64, 1.78, 2.075), 0.035, 0.035, 0.06)
    cone("PRP_bottle_b", "lilac", (-0.47, 1.78, 1.775), 0.07, 0.07, 0.20)
    build_duck("shelf", (-0.25, 1.76, 1.775), yaw=12)
    # the curtain rod and its rings
    cone("PRP_rod", "steel", (XC, -6.0, 3.06), 0.03, 0.03, 7.9, rot=(D(-90), 0, 0))
    for i in range(12):
        torus(f"PRP_ring_{i}", "steel", (XC, Y0 + 0.08 + 0.30 * i, 3.06), 0.055, 0.012, rot=(D(90), 0, 0))
    # the room beyond the curtain: a cream wall, a rug, a sink with a round mirror, a towel
    box("ENV_room_wall", "wall", (-4.2, 2.0, 4.0), (6.0, 0.2, 10))
    box("ENV_room_side", "wall", (-6.0, -1.0, 4.0), (0.2, 12, 10))
    box("PRP_rug", "rug", (-2.5, -0.9, 0.01), (1.5, 2.4, 0.02))
    box("PRP_cabinet", "wood", (-2.6, 1.55, 0.48), (1.3, 0.62, 0.96))
    box("PRP_basin", "white", (-2.6, 1.53, 0.99), (1.42, 0.70, 0.07))
    cone("PRP_tap", "steel", (-2.6, 1.72, 1.02), 0.035, 0.035, 0.26)
    cone("PRP_mirror_rim", "steel", (-2.6, 1.9, 2.25), 0.56, 0.56, 0.05, rot=(D(90), 0, 0))
    cone("PRP_mirror", "sky", (-2.6, 1.86, 2.25), 0.50, 0.50, 0.02, rot=(D(90), 0, 0))
    cone("PRP_towel_bar", "steel", (-4.9, 1.82, 1.9), 0.022, 0.022, 1.0, rot=(0, D(90), 0))
    box("PRP_towel", "towel", (-4.4, 1.80, 1.45), (0.7, 0.06, 0.92))
    cone("PRP_pot", "coral", (-3.05, 1.5, 1.025), 0.10, 0.14, 0.2)
    for i, (dx, dz, s) in enumerate([(0, 0.36, 0.17), (-0.11, 0.28, 0.11), (0.12, 0.30, 0.12)]):
        sphere(f"PRP_leaf_{i}", "leaf", (-3.05 + dx, 1.5, 1.025 + dz), (s, s, s * 1.2))
    build_duck("rim", (-1.1, -2.35, 0.5), yaw=-35)
    # in the tub, near the camera: a second duck and a bar of soap, so the foreground is not bare
    build_duck("tub", (-0.42, -2.25, 0.0), yaw=160)
    sphere("PRP_soap", "pink", (0.62, -2.55, 0.06), (0.20, 0.13, 0.06), rot=(0, 0, D(25)))


def build_curtain():
    """The shower curtain: one pleated sheet with a pale hem. It bends with shape keys:
    bow  = its lower part swings into the shower (the thing this episode explains),
    push = a dent outward where Sol shoves it,
    ripA and ripB together = a small ripple that travels along it while the water runs."""
    NY, NZ = 137, 44
    bm = bmesh.new()
    vs = [[bm.verts.new((XC + 0.045 * math.sin(2 * math.pi * lerp(Y0, Y1, j / (NY - 1)) / 0.36),
                         lerp(Y0, Y1, j / (NY - 1)), lerp(ZH, ZT, k / (NZ - 1)))) for k in range(NZ)] for j in range(NY)]
    for j in range(NY - 1):
        for k in range(NZ - 1):
            bm.faces.new((vs[j][k], vs[j + 1][k], vs[j + 1][k + 1], vs[j][k + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    o = mesh_obj("PRP_curtain", bm, "curtain")
    o.data.materials.append(mat("hem"))
    for p in o.data.polygons:
        if p.center.z < ZH + 0.26:
            p.material_index = 1
    o.visible_shadow = False            # it would put the whole tub in shade

    def hp(z):
        return hz(z) ** 1.5
    keys = shape_keys(o, {
        "bow": lambda c: (BOW * hp(c.z) * gy(c.y) / 0.80, 0.0, 0.09 * hz(c.z) ** 2 * gy(c.y)),
        "push": lambda c: (-0.12 * hp(c.z) * math.exp(-((c.y - SOL[1]) / 0.6) ** 2), 0.0, 0.0),
        "ripA": lambda c: (0.03 * hp(c.z) * math.sin(2 * math.pi * c.y / 1.4), 0.0, 0.0),
        "ripB": lambda c: (0.03 * hp(c.z) * math.cos(2 * math.pi * c.y / 1.4), 0.0, 0.0),
    })
    return keys


def curtain(cur, f, t, bow, push=0.0, ripple=1.0):
    set_shape(cur["bow"], bow, f)
    set_shape(cur["push"], push, f)
    set_shape(cur["ripA"], ripple * math.sin(t * 5.2), f)
    set_shape(cur["ripB"], ripple * math.cos(t * 5.2), f)


def build_spray(n=64, seed=4):
    """The water: drops falling from the shower head in a narrow cone, and a puddle where they land."""
    rnd = random.Random(seed)
    cone("PRP_puddle", "water", (SPRAY[0], SPRAY[1], 0.002), 0.50, 0.50, 0.006, alpha=0.55)
    drops = []
    for i in range(n):
        o = sphere(f"FX_drop_{i}", "water", (0, 0, -5), (0.02, 0.02, 0.085), alpha=0.9)
        track(o, "location")
        an, rr = rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random())
        drops.append({"o": o, "ph": rnd.random(), "ax": math.cos(an) * rr, "ay": math.sin(an) * rr})
    return drops


def spray(drops, t, period=0.62):
    for d in drops:
        u = (t / period + d["ph"]) % 1.0
        k = u ** 1.4                                          # it speeds up as it falls
        d["o"].location = (lerp(HEAD[0] + 0.13 * d["ax"], SPRAY[0] + 0.34 * d["ax"], k),
                           lerp(HEAD[1] + 0.13 * d["ay"], SPRAY[1] + 0.34 * d["ay"], k),
                           lerp(HEAD[2] - 0.03, 0.05, k))


def stage(name, n, sun=(50, 0, -12)):
    new_scene(name, n)
    key = [o for o in S["sc"].objects if o.name.startswith("LGT_key")][0]
    key.rotation_euler = tuple(D(a) for a in sun)
    build_bathroom()
    return build_curtain(), build_spray()


# ================================================================ clip 1: the question
def clip1():
    """Narrator: "Sol, why are you glaring at the shower curtain?" [0.3-2.6] / "Oh, it creeps toward you when the
    water's on." [5.1-7.83].
    Low and wide, looking up the tub: Sol in the middle, the curtain bowed in beside him on the left, the shower
    running at the far end. He glares at the curtain, leaning toward it, with two huffy little bounces, and glances
    up at the voice (1.9-2.6). His answer: he winds up (2.72) and shoves the curtain with his side (2.96-3.4); it
    swings out, swings straight back and boops him (3.88). Surprised, he hops away from it, arms up; the camera
    snaps in on him. He turns and looks up at the voice (4.65). Normal eyes again (5.5). He glances back at the
    curtain on "creeps toward you" (6.2-7.1) and nods once (7.95-8.5). His feet are on the tub floor except in the
    one hop. No arm reaches for anything."""
    n = 262
    cur, drops = stage("shower_1", n)
    sol = build_sol(SOL, -38)
    cam, tgt = build_camera(lens=24)
    TL = [(0.0, "normal"), (3.9, "surprised"), (5.5, "normal")]

    def state(t, f):
        spray(drops, t)
        kick = smooth(t, 2.98, 3.12)
        ret = max(t - 3.12, 0.0)
        bow = 0.78 - 0.55 * kick * math.exp(-1.0 * ret) * math.cos(2 * math.pi * 0.68 * ret)
        curtain(cur, f, t, bow, push=kick * (1 - smooth(t, 3.14, 3.5)))
        drift, snap, creep = smooth(t, 0.0, 3.8), smooth(t, 3.92, 4.22), smooth(t, 4.22, 8.75)
        cam.location = lerp3(lerp3((0.55, -4.35, 0.28), (0.50, -4.10, 0.30), drift), lerp3((0.48, -3.05, 0.45), (0.46, -2.9, 0.47), creep), snap)
        tgt.location = lerp3((-0.15, 0.2, 1.30), (0.22, -0.95, 0.70), snap)
        early = bump(t, 1.8, 2.7)                               # a glance up at the voice while it asks
        side = smooth(t, 2.7, 2.96)                             # turns his side to the curtain
        wind = bump(t, 2.70, 3.02)
        shove = smooth(t, 2.96, 3.10) - smooth(t, 3.16, 3.45)
        jolt = smooth(t, 3.88, 4.05)
        upv = smooth(t, 4.65, 5.05)                             # up at the voice
        glance = bump(t, 6.2, 7.1)                              # back at the curtain
        nod = bump(t, 7.95, 8.5)
        act(sol, t, f, TL, blinks=(1.45, 6.0, 7.5),
            look=(lerp(-1.0 + 0.6 * early, -0.85 * glance, upv), lerp(0.1 + 0.7 * early, 0.85 - 0.65 * glance, upv)),
            loc=(SOL[0] - 0.20 * shove + 0.30 * jolt, SOL[1], hop(t, 3.9, 4.26, 0.16)),
            yaw=lerp(lerp(lerp(-38, -16, side), -12, jolt), 3 - 14 * glance, upv),
            lean=-6 * (1 - side) + 9 * wind - 17 * shove + 8 * jolt * (1 - upv),
            pitch=7 * early + 12 * upv - 22 * nod,
            squash=idle(t) + 0.06 * (bump(t, 0.4, 0.7) + bump(t, 1.0, 1.3)) + 0.08 * wind
                   + 0.05 * wobble(t, 4.26, decay=5) + 0.07 * nod,
            arm_l=(-40 + 18 * (1 - side) + 85 * jolt * (1 - upv), 0),
            arm_r=(-40 + 18 * (1 - side) + 85 * jolt * (1 - upv), 0))
    return animate(n, state)
