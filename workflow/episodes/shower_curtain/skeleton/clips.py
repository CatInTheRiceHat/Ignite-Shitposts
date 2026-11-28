"""Skeleton clips for the shower-curtain episode, script v2.2 (../script.txt). exec()'d after rig.py by render_clip.py.

The set is from 2026-11-26; the seven clips are from 2026-11-27 (clips_v1.py is the first day's file, one clip).
Render:  SOL_EYES=working SKEL_FPS=24 Blender -b --factory-startup --python render_clip.py -- <n> <out.mp4>
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
    build_duck("tub", (-0.60, -3.35, 0.0), yaw=160)
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
        # slap = the end of the curtain nearest the camera whips in across the front of Sol's face (2026-11-27)
        "slap": lambda c: (1.02 * hz(c.z) ** 0.7 * math.exp(-((c.y + 1.44) / 0.30) ** 2), 0.0,
                           0.10 * hz(c.z) * math.exp(-((c.y + 1.44) / 0.30) ** 2)),
        "ripA": lambda c: (0.03 * hp(c.z) * math.sin(2 * math.pi * c.y / 1.4), 0.0, 0.0),
        "ripB": lambda c: (0.03 * hp(c.z) * math.cos(2 * math.pi * c.y / 1.4), 0.0, 0.0),
    })
    return keys


def curtain(cur, f, t, bow, push=0.0, ripple=1.0, slap=0.0):
    set_shape(cur["bow"], bow, f)
    set_shape(cur["slap"], slap, f)
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


# ================================================================ script v2.2 (2026-11-27): helpers
# Everything above this line is the set from 2026-11-26 (clips_v1.py holds that day's clip 1). Below: the seven clips
# of script v2.2. Elaine's notes: a travelling camera in every clip, opening with a fly-in from the top of the
# bathroom; Sol cartoony, using the whole emotion set; one different gag per clip (singing, catfight, dizzy, slip).
# Render with SOL_EYES=working (the 38-expression file) and SKEL_FPS=24.
PERIOD = 5.0                  # seconds for the steam to go once round the tub
TAU = 2 * math.pi
C["steam"] = (0.80, 0.90, 0.98)


def cr(pts, u):
    """A point on the smooth (Catmull-Rom) path through pts; u runs 0..1 along the whole path."""
    n = len(pts) - 1
    x = min(max(u, 0.0), 1.0) * n
    i = min(int(x), n - 1)
    k = x - i
    p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n)]
    return tuple(0.5 * (2 * b + (c - a) * k + (2 * a - 5 * b + 4 * c - d) * k * k + (3 * b - a - 3 * c + d) * k ** 3)
                 for a, b, c, d in zip(p0, p1, p2, p3))


def build_cam(lens=24):
    """A camera that looks at a target and can also roll. Returns set(position, target, roll in degrees)."""
    cd = bpy.data.cameras.new("CAM")
    cd.lens = lens
    rig, tgt = empty("RIG_cam"), empty("RIG_cam_target")
    c = rig.constraints.new('TRACK_TO')
    c.target, c.track_axis, c.up_axis = tgt, 'TRACK_NEGATIVE_Z', 'UP_Y'
    cam = link(bpy.data.objects.new("CAM", cd), rig)
    S["sc"].camera = cam
    track(rig, "location")
    track(tgt, "location")
    track(cam, "rotation_euler")

    def put(p, tg, roll=0.0):
        rig.location, tgt.location, cam.rotation_euler = p, tg, (0, 0, D(roll))
    return put


def build_sol2(loc, yaw):
    """Sol with his legs and the marks' turns keyed too."""
    sol = build_sol(loc, yaw)
    for c in sol["root"].children:
        nm = c.name.split(".")[0]
        if nm in ("SOL_leg_L", "SOL_leg_R"):
            sol["leg_l" if nm.endswith("L") else "leg_r"] = c
            sol[nm] = tuple(c.location)
            track(c, "location")
    for objs in sol["eyes"]["marks"].values():
        for o in objs:
            track(o, "rotation_euler")
    return sol


def act(sol, t, f, timeline, look=(0.0, 0.0), blinks=(), marks=None, tip=0.0, legs=((0, 0), (0, 0)), **pose):
    """Eyes and marks from the emotion timeline (with its bounce), then the body pose with that bounce added.
    tip: degrees the whole of him is tipped over (-90 = flat on his back). legs: (forward, up) in metres per leg."""
    expr, sq, size, g = emotion_at(t, timeline)
    bl = blink_at(t, blinks) if EXPR[expr]["eyes"][0] in ("oval", "spark") else 0.0
    e = sol["eyes"]
    pose_eyes(e, expr, blink=bl, look=look, size=size, gloom=g, marks=marks, t=t)
    for socks in list(e["shade"].values()) + [e["red"]]:
        for sock in socks:
            sock.keyframe_insert("default_value", frame=f)
    pose["squash"] = pose.get("squash", 0.0) + sq
    pose_sol(sol, **pose)
    if tip:
        sol["root"].rotation_euler = (D(tip), 0, D(pose.get("yaw", 0.0)))
    for key, nm, (fw, up) in (("leg_l", "SOL_leg_L", legs[0]), ("leg_r", "SOL_leg_R", legs[1])):
        b = sol[nm]
        sol[key].location = (b[0], b[1] - fw, b[2] + up)


def build_puffs(n=40, seed=7):
    """The air, made visible: the same 40 pale steam puffs in every science clip, each a little clump of three balls.
    They go round in one big wheel between Sol and the far wall: down with the spray, along the floor toward Sol, up
    in front of him, back along the top. Seen from the side the wheel is about 2 m across with a clear middle."""
    rnd = random.Random(seed)
    P = []
    for i in range(n):
        r = rnd.uniform(0.050, 0.075)
        e = empty(f"RIG_puff_{i}", (0, 0, -5))
        for j, (dy, dz, k) in enumerate(((0, 0, 1.0), (0.75, 0.25, 0.72), (-0.7, 0.2, 0.66))):
            sphere(f"FX_puff_{i}_{j}", "steam", (rnd.uniform(-0.3, 0.3) * r, dy * r, dz * r), (r * k, r * k, r * k * 0.9), parent=e)
        track(e, "location")
        x = rnd.uniform(-0.75, -0.30) if rnd.random() < 0.5 else rnd.uniform(0.30, 0.62)
        P.append({"o": e, "u": TAU * (i + rnd.uniform(-0.3, 0.3)) / n, "x": x, "s": rnd.uniform(0.88, 1.08)})
    return P


LOOP = (0.35, 0.90, 1.30, 1.08)      # the wheel: centre y, half length, centre height, half height


def puffs_at(P, t, t0=0.0):
    yc, a, zc, b = LOOP
    for p in P:
        u = p["u"] - TAU * (t + t0) / PERIOD
        c, s = math.cos(u), math.sin(u)
        p["o"].location = (p["x"], yc + a * p["s"] * math.copysign(abs(c) ** 0.6, c),
                           max(zc + b * p["s"] * math.copysign(abs(s) ** 0.6, s), 0.09))


def stage(name, n, sun=(50, 0, -12), cutaway=False, hide_right=True):
    """cutaway: the tiled wall on the right is left out so the camera can stand outside the tub and see the whole
    wheel side-on; the tub gets its end wall behind Sol and a white apron of floor under the camera."""
    new_scene(name, n)
    key = [o for o in S["sc"].objects if o.name.startswith("LGT_key")][0]
    key.rotation_euler = tuple(D(a) for a in sun)
    build_bathroom()
    if cutaway:
        for o in S["sc"].objects:
            if o.name.startswith("ENV_wall_right") or o.name.startswith("ENV_grout_r"):
                o.hide_render = hide_right
                o.visible_shadow = False
        box("ENV_wall_near", "tile", (-0.1, -2.0, 4.0), (2.2, 0.2, 10)).visible_shadow = False
        for i in range(1, 12):
            box(f"ENV_grout_nh{i}", "grout", (-0.1, -1.895, 0.5 * i), (2.2, 0.02, 0.022))
        for i in range(4):
            box(f"ENV_grout_nv{i}", "grout", (-0.95 + 0.5 * i, -1.895, 3.0), (0.022, 0.02, 6.0))
        box("ENV_apron", "tub", (3.2, -2.05, -0.1), (4.0, 7.9, 0.2))
    return build_curtain(), build_spray()


# ================================================================ clip 1: fly in, singing, the SLAP, the fury
def clip1():
    """Version 4 (2026-11-27). Elaine: "when sol has the furious eyes thats when narrator says sol why are u mad": the
    Narrator's line belongs AFTER the glare is on his face, so the glare comes sooner and the clip runs longer to hold it
    under the whole line. No words until the glare; then Narrator: "Sol, why are you glaring at the shower curtain?".
    The camera flies down from the top of the bathroom into the tub (0-2.2). Sol sways, SINGING (notes from 1.0).
    The curtain draws back (1.75-2.1), then its near end WHIPS in and slaps him (2.2), knocking him sideways with his
    eyes squeezed shut; it peels away (2.42-2.72) and he rocks upright. FURIOUS (3.0): flame red, the vein mark, the
    glare; he swells up and shakes at the curtain; the camera snaps in (3.0-3.3). Two stomps (3.9, 4.3). He holds the
    glare at the curtain to the end and glances up at the voice only at 5.8. clips_v4.py has version 3."""
    n = 198
    cur, drops = stage("shower_1", n)
    sol = build_sol2(SOL, -8)
    cam = build_cam(24)
    TL = [(0.0, "singing"), (2.2, "squeeze"), (3.0, "furious")]
    FLY = [(-4.4, -4.8, 5.2), (-2.2, -4.6, 4.3), (-0.7, -4.4, 3.4), (0.45, -4.2, 1.6), (0.55, -3.9, 0.42)]
    F0 = smooth(0.0, -0.7, 2.2)

    def state(t, f):
        spray(drops, t)
        back = smooth(t, 1.75, 2.08) * (1 - smooth(t, 2.08, 2.2))                 # the wind-up, away from him
        hit = smooth(t, 2.08, 2.2) ** 2 * (1 - smooth(t, 2.42, 2.72))             # the whip, the hold, the peel
        sl = hit + 0.10 * wobble(t, 2.72, freq=13, decay=5)
        curtain(cur, f, t, 0.25 * (1 - back) + 0.10 * smooth(t, 2.7, 3.2), push=2.2 * back, slap=max(sl, -0.12))
        snap, crp = smooth(t, 3.0, 3.3), smooth(t, 3.3, 6.6)
        shake = 0.05 * wobble(t, 2.2, freq=30, decay=7)
        p = lerp3(cr(FLY, (smooth(t, -0.7, 2.2) - F0) / (1 - F0)), lerp3((0.42, -2.75, 0.50), (0.38, -2.50, 0.53), crp), snap)
        cam((p[0] + shake, p[1], p[2] + 0.6 * shake),
            lerp3(lerp3((-1.3, 0.6, 0.9), (-0.05, -0.6, 0.95), smooth(t, 0.2, 2.0)), (0.05, -0.95, 0.62), snap))
        sing = 1 - smooth(t, 2.05, 2.2)
        knock = smooth(t, 2.17, 2.25) * (1 - smooth(t, 2.5, 2.85))                # shoved sideways and squashed
        reel = wobble(t, 2.85, freq=9, decay=5.5)                                  # rocking back upright
        ang = smooth(t, 2.95, 3.2)
        rage = ang * (1 - 0.5 * smooth(t, 4.8, 5.6))
        up = smooth(t, 5.8, 6.2)
        sway = math.sin(TAU * 1.15 * t)
        tremble = rage * math.sin(TAU * 11 * t)
        act(sol, t, f, TL, marks=() if t < 1.0 else (("burst",) if 2.2 <= t < 2.75 else None),
            look=(lerp(0.0, -1.0 + 0.5 * up, ang), lerp(0.0, 0.1 + 0.7 * up, ang)),
            loc=(SOL[0] + 0.24 * knock + 0.04 * reel + 0.012 * tremble, SOL[1], 0),
            yaw=lerp(-8, -30 + 14 * up, ang) + 14 * knock,
            lean=7 * sway * sing + 24 * knock + 9 * reel - 9 * ang * (1 - 0.6 * up) + 1.5 * tremble,
            pitch=5 * sing - 6 * knock + 8 * up,
            squash=idle(t) + 0.035 * sing * math.sin(TAU * 2.3 * t) + 0.16 * knock - 0.10 * rage * (1 - 0.5 * up)
                   + 0.09 * (bump(t, 3.9, 4.15) + bump(t, 4.3, 4.55)),
            arm_l=(-40 + 35 * sing * (0.5 + 0.5 * sway) + 95 * knock + 55 * rage + 10 * tremble, 0),
            arm_r=(-40 + 35 * sing * (0.5 - 0.5 * sway) + 95 * knock + 55 * rage - 10 * tremble, 0))
    return animate(n, state)


# ================================================================ clip 2: the catfight
def clip2():
    """Narrator: "Oh, it creeps toward you when the water's on." [2.05-4.78].
    Opens low beside the curtain, three-quarter on Sol's face. He leans away, eyes squeezed (> <), and slaps at the curtain
    with both nubs in turn, six slaps (0.4-1.4); the hem flutters back. It swings in and boops him (1.5). O O, frozen,
    nubs up. The camera swings round to his front. Nubs drop, he looks up (2.1). NERVOUS sideways look at the curtain
    (3.2-4.1). One nod (4.7-5.15). His nubs never get longer: they flap where they are."""
    n = 156
    cur, drops = stage("shower_2", n)
    sol = build_sol2(SOL, -45)
    cam = build_cam(24)
    TL = [(0.0, "angry"), (0.25, "squeeze"), (1.5, "surprised"), (2.15, "normal"), (3.2, "nervous"), (4.2, "normal")]

    def state(t, f):
        spray(drops, t)
        cat = smooth(t, 0.35, 0.45) * (1 - smooth(t, 1.38, 1.46))
        slap = math.sin(TAU * 3 * (t - 0.4))
        boop = bump(t, 1.36, 1.9)
        curtain(cur, f, t, 0.78 - 0.08 * cat + 0.16 * boop, push=0.8 * cat * abs(slap))
        rnd, push = smooth(t, 1.7, 2.6), smooth(t, 2.6, 5.2)
        whip = -0.12 * cat + 0.16 * boop
        cam(lerp3((-0.30 + whip, -2.55, 0.72 + 0.04 * wobble(t, 1.5, freq=40, decay=9)),
                  lerp3((0.42, -2.45, 0.62), (0.34, -2.20, 0.64), push), rnd),
            lerp3((-0.12, -0.95, 0.55), (0.05, -0.95, 0.60), rnd))
        jolt = smooth(t, 1.5, 1.58)
        frozen = smooth(t, 1.46, 1.52) * (1 - smooth(t, 2.1, 2.3))
        front = smooth(t, 2.1, 2.5)
        nerv = bump(t, 3.2, 4.15)
        nod = bump(t, 4.7, 5.15)
        act(sol, t, f, TL, blinks=(2.75, 4.45),
            look=(lerp(-0.6, -0.95 * nerv, front), lerp(0.0, 0.8 * (1 - nerv), front)),
            loc=(SOL[0] + 0.10 * jolt, SOL[1], 0),
            yaw=lerp(-45, -5, front) - 12 * nerv,
            lean=5 * nerv + 8 * cat * slap,
            pitch=14 * cat + 6 * frozen + 10 * front * (1 - nerv) - 22 * nod,
            squash=idle(t) + 0.03 * cat * math.sin(TAU * 6 * t) + 0.07 * nod,
            arm_l=(-40 + cat * (62 + 58 * slap) + 70 * frozen, 22 * cat + 20 * frozen),
            arm_r=(-40 + cat * (62 - 58 * slap) + 70 * frozen, 22 * cat + 20 * frozen))
    return animate(n, state)


# ================================================================ clip 3: the spray drags air down
def clip3():
    """Narrator: "Watch the spray. Falling water drags air down with it." [0.30-4.38].
    Over Sol's shoulder: he turns to the spray and tilts (0.15-1.1). The camera rushes past him up to the shower head
    (0.8-1.5), then falls beside the drops to the tub floor (1.6-4.2). Steam puffs beside the spray are dragged down
    and spread out along the floor."""
    n = 144
    cur, drops = stage("shower_3", n)
    P = build_puffs()
    sol = build_sol2(SOL, 0)
    cam = build_cam(24)
    TL = [(0.0, "normal")]

    def state(t, f):
        spray(drops, t)
        puffs_at(P, t)
        curtain(cur, f, t, 0.30)
        rush, fall = smooth(t, 0.8, 1.5), smooth(t, 1.6, 4.2)
        cam(lerp3(lerp3((0.60, -2.75, 1.20), (0.86, 0.30, 2.80), rush), (0.88, 0.05, 0.42), fall),
            lerp3(lerp3((0.15, 0.9, 1.5), (0.30, 1.40, 2.62), rush), (0.25, 1.05, 0.22), fall))
        turn, tilt = smooth(t, 0.15, 0.7), smooth(t, 0.7, 1.1)
        act(sol, t, f, TL, look=(0.0, 0.3), yaw=180 * turn, lean=12 * tilt,
            squash=idle(t) + 0.06 * bump(t, 0.1, 0.5))
    return animate(n, state)


# ================================================================ clip 4: the loop
def clip4():
    """Narrator: "That air loops back around like a little sideways whirlwind." [0.30-4.17].
    The camera rides low along the tub floor with the puffs to Sol (0-1.0) and rises past his face (AMAZED 1.0-1.8),
    then peels out sideways (1.4-2.6) to the wide side view, where the whole wheel shows (cut-away wall). Sol turns to
    us and follows a puff round with his whole body in slow circles (2.6 to the end) while the camera eases in a little.
    Version 2 (2026-11-27): the dizzy ending and its snap zoom are gone (Elaine: "the dizzy animation is very sudden so
    just remove that"), so the whole clip can be used. clips_v3.py has the old one."""
    n = 156
    cur, drops = stage("shower_4", n, cutaway=True, hide_right=False)
    # the tiled right wall is there for the ride and is taken away at 1.5 s, while it is out of view, so the
    # camera can peel out through where it stood
    walls = [(o, tuple(o.location)) for o in S["sc"].objects if o.name.startswith("ENV_wall_right") or o.name.startswith("ENV_grout_r")]
    for o, _ in walls:
        track(o, "location")
    P = build_puffs()
    sol = build_sol2(SOL, 180)
    cam = build_cam(24)
    TL = [(0.0, "normal"), (1.0, "amazed"), (1.8, "normal")]

    def state(t, f):
        spray(drops, t)
        puffs_at(P, t, 4.8)
        curtain(cur, f, t, 0.30)
        for o, b in walls:
            o.location = (b[0] + (60.0 if t >= 1.5 else 0.0), b[1], b[2])
        ride, rise, peel, push = smooth(t, 0.0, 1.0), smooth(t, 1.0, 1.5), smooth(t, 1.4, 2.6), smooth(t, 2.6, 5.2)
        zoom = 0.0
        cam(lerp3(lerp3(lerp3(lerp3((0.06, 0.80, 0.30), (0.06, 0.15, 0.42), ride), (0.25, 0.10, 1.15), rise),
                        lerp3((3.9, 0.05, 1.25), (3.55, 0.05, 1.22), push), peel), (2.1, -0.85, 0.72), zoom),
            lerp3(lerp3(lerp3((0.02, -0.95, 0.50), (0.02, -0.95, 0.70), rise), (-0.9, 0.05, 1.25), peel), (0.02, -0.95, 0.52), zoom))
        amz = bump(t, 1.0, 1.85)
        turn = smooth(t, 1.8, 2.6)
        go = smooth(t, 2.6, 2.8)
        a = TAU * (t - 2.6) / 1.6
        diz = 0.0
        act(sol, t, f, TL, blinks=(0.5, 2.2, 4.4),
            look=(go * math.sin(a), lerp(0.2 + 0.7 * amz, 0.0, turn) + go * math.cos(a)),
            yaw=lerp(180, 90, turn),
            lean=12 * go * math.sin(a) + 11 * diz * math.sin(TAU * 1.5 * (t - 4.2)),
            pitch=9 * amz + 4 * go * math.cos(a) + 5 * diz * math.cos(TAU * 1.5 * (t - 4.2)),
            squash=idle(t) - 0.05 * go * math.cos(a),
            arm_l=(-40 + 75 * amz + 25 * diz, 0), arm_r=(-40 + 75 * amz + 25 * diz, 0))
    return animate(n, state)


# ================================================================ clip 5: the low-pressure middle
def clip5():
    """Narrator: "The middle of a whirlwind is low pressure, so it pushes on the curtain a little less." [0.30-6.12].
    A three-quarter view from the shower end of the cut-away side: the spray at the right edge, the wheel of puffs
    turning in the middle, the curtain behind it, Sol small at the left. The camera corkscrews in (0-2.5: a push with
    the roll unwinding) and then holds still. From 3.2 to 6.2 the curtain's lower half eases in toward the middle of
    the wheel (seen from the side, so it reads) and stops short of Sol, who leans away and eyes it.
    Script v2.2 said Sol is not in this shot. A head-on close-up could not show the cloth moving toward the camera, so
    the view is from the side, and from there Sol's spot is in frame."""
    n = 198
    cur, drops = stage("shower_5", n, cutaway=True)
    P = build_puffs()
    sol = build_sol2(SOL, 140)
    cam = build_cam(24)
    TL = [(0.0, "normal")]

    def state(t, f):
        spray(drops, t)
        puffs_at(P, t, 10.0)
        ease = smooth(t, 3.2, 6.2)
        curtain(cur, f, t, lerp(0.30, 0.70, ease), ripple=0.6)
        k = smooth(t, 0.0, 2.5)
        cam(lerp3((2.9, 2.2, 2.5), (2.3, 1.6, 1.7), k), lerp3((-0.6, -0.2, 1.1), (-0.7, -0.3, 0.9), k), roll=26 * (1 - k))
        wary = smooth(t, 4.0, 4.8)
        act(sol, t, f, TL, blinks=(1.2, 3.6), look=(lerp(0.3, 1.0, wary), lerp(0.6, 0.0, wary)),
            yaw=140, lean=-7 * wary, squash=idle(t))
    return animate(n, state)


# ================================================================ clip 6: the room wins (the slip)
def clip6():
    """Narrator: "The room outside pushes like normal, so the room wins and shoves the curtain in." [0.40-6.99].
    The camera glides low across the bathroom rug to the curtain (0-2.6), cranes up and over the rod (2.6-4.4) and
    looks down into the tub. Sol watches the hem creep toward him, NERVOUS (4.4). PANIC (4.8): he turns away and runs
    in place on the wet floor, legs scrabbling, going nowhere (4.8-5.5). His feet shoot out (5.5), he tips backward and
    flops flat on his back (5.8). The hem swings in and boops him where he lies (5.85). KO (X X). One leg twitches."""
    n = 225
    cur, drops = stage("shower_6", n)
    sol = build_sol2(SOL, -30)
    cam = build_cam(24)
    TL = [(0.0, "normal"), (4.4, "nervous"), (4.8, "panic"), (5.8, "ko")]
    CRANE = [(-2.7, -1.9, 0.45), (-2.0, -2.5, 2.1), (-0.95, -3.0, 3.5), (-0.30, -2.75, 2.05)]
    G0 = smooth(0.0, -0.8, 2.6)

    def state(t, f):
        spray(drops, t)
        curtain(cur, f, t, 0.15 + 0.20 * smooth(t, 0.4, 2.8) + 0.25 * smooth(t, 4.2, 5.5) + 0.32 * smooth(t, 5.6, 5.85)
                - 0.06 * smooth(t, 5.9, 6.5))
        p = lerp3((-4.6, -3.0, 0.42), (-2.7, -1.9, 0.45), (smooth(t, -0.8, 2.6) - G0) / (1 - G0))
        if t > 2.6:
            p = cr(CRANE, smooth(t, 2.6, 4.4))
        cam((p[0], p[1], p[2] + 0.03 * wobble(t, 5.85, freq=38, decay=8)),
            lerp3((-1.0, -0.2, 0.95), (0.05, -0.80, 0.38), smooth(t, 2.8, 4.3)))
        turn = smooth(t, 4.75, 4.95)
        run = smooth(t, 4.78, 4.9) * (1 - smooth(t, 5.5, 5.6))
        k = smooth(t, 5.5, 5.8)
        yaw = lerp(-30, 35, turn)
        fx, fy = math.sin(D(yaw)), -math.cos(D(yaw))
        ph = TAU * 7 * t
        kick = bump(t, 5.5, 5.85)
        twitch = bump(t, 6.6, 6.85)
        act(sol, t, f, TL, blinks=(4.55,),
            look=(lerp(-1.0, 0.3, turn), 0.0),
            loc=(SOL[0] + 0.22 * k * fx, SOL[1] + 0.22 * k * fy,
                 0.30 * math.sin(D(90 * k)) + 0.10 * kick + 0.05 * abs(wobble(t, 5.8, freq=16, decay=7))),
            yaw=yaw, tip=-90 * k,
            lean=4 * (1 - turn),
            pitch=-14 * run,
            squash=idle(t) * (1 - k) + 0.03 * run * math.sin(TAU * 14 * t) + 0.10 * bump(t, 5.78, 5.98),
            arm_l=(-40 + run * (25 + 30 * math.sin(ph)) + 75 * k, 30 * run * math.sin(ph)),
            arm_r=(-40 + run * (25 - 30 * math.sin(ph)) + 75 * k, -30 * run * math.sin(ph)),
            legs=((0.10 * run * math.sin(ph) + 0.14 * kick, 0.06 * run * max(0.0, math.cos(ph)) + 0.03 * kick),
                  (-0.10 * run * math.sin(ph) + 0.14 * kick + 0.07 * twitch, 0.06 * run * max(0.0, -math.cos(ph)) + 0.03 * kick)))
    return animate(n, state)


# ================================================================ clip 7: Sol gets it
def clip7():
    """Narrator: "It's not creeping up on you. It's getting pushed. Got it?" [0.20-3.57].
    Opens low and close on the hem and Sol, flat on his back. He pops upright with a wobble (0-0.4). THINKING (dots),
    looking down at the hem. IDEA (bulb, 1.9). He bumps the curtain away with his side (2.1-2.7); it swings out and
    settles back on him by 3.2. SMUG, puffed up (2.8). The camera swings across his front and up to face him (2.0-3.6),
    then a small snap push-in. He looks up, EXCITED (3.6). Two nods with HAPPY eyes (4.55-5.0, 5.1-5.6). Ends on the
    second nod."""
    n = 174
    cur, drops = stage("shower_7", n)
    sol = build_sol2(SOL, 35)
    cam = build_cam(24)
    TL = [(0.0, "ko"), (0.3, "thinking"), (1.9, "idea"), (2.8, "smug"), (3.6, "excited"), (4.5, "happy")]
    ARC = [(-0.55, -2.55, 0.40), (0.15, -2.75, 0.50), (0.70, -2.45, 0.80), (0.22, -2.70, 0.72)]
    F0 = (math.sin(D(35)), -math.cos(D(35)))

    def state(t, f):
        spray(drops, t)
        kick = smooth(t, 2.15, 2.30)
        ret = max(t - 2.30, 0.0)
        curtain(cur, f, t, 0.80 - 0.50 * kick * math.exp(-2.5 * ret) * math.cos(TAU * 0.7 * ret),
                push=kick * (1 - smooth(t, 2.32, 2.7)))
        snap = smooth(t, 3.6, 3.8)
        cam(lerp3(cr(ARC, smooth(t, 2.0, 3.6)), (0.20, -2.35, 0.70), snap),
            lerp3((-0.15, -0.95, 0.55), (0.02, -0.95, 0.62), smooth(t, 1.9, 3.2)))
        up = smooth(t, 0.05, 0.4)
        wind = bump(t, 1.95, 2.25)
        shove = smooth(t, 2.12, 2.26) - smooth(t, 2.32, 2.6)
        smug = bump(t, 2.8, 3.55)
        upv = smooth(t, 3.45, 3.75)
        nod = bump(t, 4.55, 5.0) + bump(t, 5.1, 5.6)
        act(sol, t, f, TL,
            look=(-0.9 * (1 - smooth(t, 2.6, 2.9)), lerp(-0.6 * (1 - smooth(t, 2.6, 2.9)), 0.85, upv) * (1 - 0.6 * nod)),
            loc=(SOL[0] + 0.22 * (1 - up) * F0[0] - 0.20 * shove, SOL[1] + 0.22 * (1 - up) * F0[1],
                 0.30 * math.sin(D(90 * (1 - up)))),
            yaw=lerp(lerp(lerp(35, -16, up), 12, smooth(t, 2.6, 2.9)), 0, upv), tip=-90 * (1 - up),
            lean=9 * wind - 17 * shove + 6 * wobble(t, 0.4, freq=12, decay=5),
            pitch=6 * smug + 12 * upv - 22 * nod,
            squash=idle(t) + 0.06 * wobble(t, 0.4, freq=13, decay=5) + 0.08 * wind - 0.06 * smug + 0.07 * nod,
            arm_l=(-40 + 30 * smug + 60 * bump(t, 3.6, 4.4), 0), arm_r=(-40 + 30 * smug + 60 * bump(t, 3.6, 4.4), 0))
    return animate(n, state)


# ================================================================ clip 8: the ending, version 2 (replaces clip 7 in the cut)
def clip8():
    """Narrator: "It's not creeping up on you. It's getting pushed." [0.45-2.86].
    Elaine, 2026-11-27: "i stil feel like the ending is kind of chopped so instead of having sol like react immediately
    can we have him look up and nod before mkaing happy face". Sol stands by the curtain, still eyeing its hem (0-0.35).
    He turns to the camera and LOOKS UP at the voice (0.35-0.7) and listens, swaying a little, through the whole line.
    When it is over he NODS once, clearly (2.95-3.45). Then HAPPY (3.75): a small bounce, the burst marks until 4.3,
    arc eyes to the end. The camera only eases in, slowly, the whole time: no swing, no snap."""
    n = 144
    cur, drops = stage("shower_8", n)
    sol = build_sol2(SOL, -22)
    cam = build_cam(24)
    TL = [(0.0, "normal"), (3.75, "happy")]

    def state(t, f):
        spray(drops, t)
        curtain(cur, f, t, 0.42)
        k = smooth(t, -0.6, 4.8)
        cam(lerp3((0.30, -2.95, 0.78), (0.20, -2.42, 0.70), k), lerp3((0.02, -0.95, 0.58), (0.03, -0.95, 0.62), k))
        turn = smooth(t, 0.35, 0.7)
        nod = bump(t, 2.95, 3.45)
        joy = smooth(t, 3.72, 3.82)
        hopj = bump(t, 3.75, 4.05)
        act(sol, t, f, TL, blinks=(1.6,), marks=("burst",) if 3.75 <= t < 4.3 else (),
            look=(-0.9 * (1 - turn), 0.8 * turn * (1 - 0.7 * nod)),
            yaw=lerp(-22, -4, turn),
            lean=-5 * (1 - turn) + 2.0 * turn * math.sin(TAU * 0.45 * t) * (1 - joy),
            pitch=11 * turn * (1 - joy * 0.3) - 24 * nod,
            squash=idle(t) + 0.07 * nod + 0.08 * bump(t, 3.68, 3.8) - 0.09 * hopj,
            arm_l=(-40 + 55 * bump(t, 3.75, 4.5), 0), arm_r=(-40 + 55 * bump(t, 3.75, 4.5), 0))
    return animate(n, state)
