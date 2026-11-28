"""Skeleton clips for the wet-shirt episode (../script.txt, written by Gemini 4 Neon, 2026-11-27).
exec()'d after rig.py by render_clip.py.

Render:  SOL_EYES=working SKEL_FPS=24 Blender -b --factory-startup --python render_clip.py -- <n> <out.mp4>
Layout (metres; Sol is 1.0 tall): a sunny back garden on laundry day. The camera's home side is -Y. A flagstone patio
in the foreground, lawn round it, a cream picket fence at the back with trees behind it. The drying rack stands on the
patio with ONE plain light-gray T-shirt hanging from its top bar, facing the camera. Sol stands at its left front.
The sprinkler sits on the lawn at the right front and never moves.
The thing being explained is modelled in its real colours: the shirt, its wet patch, and (clips 3 and 4) the weave.
"""
import random

TAU = 2 * math.pi
C.update({
    "sky": (0.62, 0.84, 0.98), "lawn": (0.47, 0.74, 0.36), "lawn_d": (0.40, 0.66, 0.32), "stone": (0.90, 0.80, 0.66),
    "stone_d": (0.80, 0.69, 0.56), "fence": (0.99, 0.96, 0.86), "trunk": (0.55, 0.38, 0.26), "tree": (0.33, 0.60, 0.36),
    "tree_l": (0.45, 0.70, 0.40), "terra": (0.85, 0.48, 0.32), "sunf": (0.99, 0.80, 0.16), "sunc": (0.45, 0.28, 0.16),
    "hyd": (0.45, 0.58, 0.93), "hyd_l": (0.62, 0.70, 0.97), "stem": (0.35, 0.62, 0.34), "red": (0.92, 0.33, 0.30),
    "teal": (0.25, 0.70, 0.68), "yellow": (0.99, 0.82, 0.30), "rack": (0.80, 0.60, 0.38), "wicker": (0.86, 0.68, 0.42),
    "tw_pink": (0.98, 0.74, 0.78), "tw_mint": (0.68, 0.90, 0.80), "tw_lilac": (0.78, 0.72, 0.94),
    "shirt": (0.72, 0.74, 0.77), "wet": (0.33, 0.345, 0.376), "brass": (0.86, 0.68, 0.30), "hose": (0.22, 0.56, 0.36),
    "drop": (0.42, 0.70, 0.96), "fiber": (0.66, 0.68, 0.73), "fiber_d": (0.54, 0.56, 0.62), "fiber_e": (0.60, 0.62, 0.68), "water": (0.62, 0.84, 0.97),
    "void": (0.17, 0.19, 0.27),
})

# ---- fixed places
SOL = (-0.55, -0.55, 0.0)          # Sol's home spot, left front of the rack
RACK_Y, BAR_Z = 0.30, 1.32         # the rack's top bar
SH_X, SH_Y = 0.80, 0.22            # the shirt's centre line and its plane (it faces -Y)
SH_TOP, SH_HEM = 1.30, 0.26        # shoulders and hem
PATCH = (0.80, 0.68)               # the wet patch: x and height of its centre on the shirt
PATCH_R = 0.21
SPR = (2.35, -1.75, 0.0)           # the sprinkler
NOZ = (2.30, -1.70, 0.34)          # where its water leaves


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
    """A camera that looks at a target and can also roll. Returns put(position, target, roll in degrees)."""
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


def act(sol, t, f, timeline, look=(0.0, 0.0), blinks=(), marks=None, legs=((0, 0), (0, 0)), **pose):
    """Eyes and marks from the emotion timeline (with its bounce), then the body pose with that bounce added.
    legs: (forward, up) in metres per leg, for a waddle."""
    expr, sq, size, g = emotion_at(t, timeline)
    bl = blink_at(t, blinks) if EXPR[expr]["eyes"][0] in ("oval", "spark") else 0.0
    e = sol["eyes"]
    pose_eyes(e, expr, blink=bl, look=look, size=size, gloom=g, marks=marks, t=t)
    for socks in list(e["shade"].values()) + [e["red"]]:
        for sock in socks:
            sock.keyframe_insert("default_value", frame=f)
    pose["squash"] = pose.get("squash", 0.0) + sq
    pose_sol(sol, **pose)
    for key, nm, (fw, up) in (("leg_l", "SOL_leg_L", legs[0]), ("leg_r", "SOL_leg_R", legs[1])):
        b = sol[nm]
        sol[key].location = (b[0], b[1] - fw, b[2] + up)


def tri(name, key, a, b, c, parent=None):
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in (a, b, c)]
    bm.faces.new(vs)
    return mesh_obj(name, bm, key, parent=parent, smooth=False)


# ================================================================ the garden
def build_bunting(tag, a, b, sag, n, seed):
    """A string of blank cloth flags between two points (no poles in view: it runs off both sides of the frame)."""
    rnd = random.Random(seed)
    cols = ["red", "yellow", "teal"]
    pts = []
    for i in range(n * 2 + 1):
        u = i / (n * 2)
        pts.append((lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u) - sag * 4 * u * (1 - u)))
    for i in range(n * 2):
        p, q = pts[i], pts[i + 1]
        L = math.dist(p, q)
        mid = tuple((x + y) / 2 for x, y in zip(p, q))
        ang = math.atan2(q[2] - p[2], q[0] - p[0])
        yaw = math.atan2(q[1] - p[1], q[0] - p[0])
        cone(f"PRP_bunt_line_{tag}{i}", "fence", mid, 0.012, 0.012, L * 1.02, rot=(0, D(90) - ang, yaw)).location = \
            (mid[0] - math.cos(ang) * L / 2, mid[1], mid[2] - math.sin(ang) * L / 2)
    for i in range(n):
        p, q = pts[2 * i], pts[2 * i + 2]
        m = pts[2 * i + 1]
        w = 0.42 * math.dist(p, q)
        tri(f"PRP_flag_{tag}{i}", cols[(i + seed) % 3], (m[0] - w, m[1], m[2] + 0.01), (m[0] + w, m[1], m[2] + 0.01),
            (m[0] + rnd.uniform(-0.03, 0.03), m[1], m[2] - 0.46))


def build_pot(tag, loc, kind, s=1.0):
    e = empty("RIG_pot_" + tag, loc)
    cone("PRP_pot_" + tag, "terra", (0, 0, 0), 0.17 * s, 0.24 * s, 0.34 * s, parent=e)
    if kind == "sun":
        for i, (dx, h) in enumerate(((-0.10, 0.95), (0.08, 1.20), (0.0, 0.70))):
            cone(f"PRP_stem_{tag}{i}", "stem", (dx * s, 0, 0.3 * s), 0.022 * s, 0.022 * s, h * s, parent=e)
            sphere(f"PRP_sunf_{tag}{i}", "sunf", (dx * s, -0.03 * s, (0.3 + h) * s), (0.19 * s, 0.05 * s, 0.19 * s), parent=e)
            sphere(f"PRP_sunc_{tag}{i}", "sunc", (dx * s, -0.07 * s, (0.3 + h) * s), (0.085 * s, 0.03 * s, 0.085 * s), parent=e)
            sphere(f"PRP_leaf_{tag}{i}", "stem", ((dx + 0.09) * s, 0, (0.3 + h * 0.5) * s), (0.11 * s, 0.03 * s, 0.05 * s), parent=e)
    else:
        sphere(f"PRP_bush_{tag}", "stem", (0, 0, 0.50 * s), (0.30 * s, 0.30 * s, 0.24 * s), parent=e)
        for i, (dx, dy, dz, r) in enumerate(((0, -0.05, 0.72, 0.17), (-0.2, 0.0, 0.60, 0.14), (0.2, -0.02, 0.62, 0.15),
                                             (0.05, 0.12, 0.66, 0.13))):
            sphere(f"PRP_hyd_{tag}{i}", "hyd" if i % 2 == 0 else "hyd_l", (dx * s, dy * s, dz * s), (r * s, r * s, r * s * 0.9), parent=e)
    return e


def build_garden(sky=True):
    w = S["sc"].world
    w.node_tree.nodes["Background"].inputs["Color"].default_value = tuple(c ** 2.2 for c in C["sky"]) + (1,)
    # ground: lawn everywhere, the flagstone patio in front
    box("ENV_lawn", "lawn", (0, 0, -0.1), (40, 40, 0.2))
    for i in range(9):                                            # mown stripes, so the lawn is not one flat green
        box(f"ENV_lawn_stripe{i}", "lawn_d", (-12 + 3.0 * i, 3.5, 0.002), (1.5, 9.0, 0.004))
    box("ENV_patio", "stone", (-0.4, -2.2, 0.01), (5.4, 7.4, 0.04))
    rnd = random.Random(3)
    for i in range(6):
        box(f"ENV_seam_x{i}", "stone_d", (-0.4, -5.6 + 1.25 * i + rnd.uniform(-0.1, 0.1), 0.031), (5.4, 0.035, 0.004))
    for i in range(5):
        box(f"ENV_seam_y{i}", "stone_d", (-2.6 + 1.1 * i + rnd.uniform(-0.1, 0.1), -2.2, 0.031), (0.035, 7.4, 0.004))
    # the picket fence at the back and along the left
    for i in range(52):
        x = -9.0 + 0.36 * i
        box(f"ENV_picket_{i}", "fence", (x, 5.4, 0.80), (0.24, 0.06, 1.6))
        tri(f"ENV_picket_tip_{i}", "fence", (x - 0.12, 5.4, 1.6), (x + 0.12, 5.4, 1.6), (x, 5.4, 1.80))
    for z in (0.45, 1.25):
        box(f"ENV_rail_{z}", "fence", (0.3, 5.46, z), (18.8, 0.05, 0.12))
    # trees and sky-filling canopy behind the fence
    for i, (x, y, h, r) in enumerate(((-5.2, 7.6, 3.4, 2.1), (-1.6, 8.4, 4.2, 2.5), (2.2, 7.8, 3.6, 2.2), (5.8, 8.6, 4.4, 2.6),
                                      (-8.6, 8.8, 3.9, 2.4), (9.2, 7.9, 3.5, 2.2))):
        cone(f"ENV_trunk_{i}", "trunk", (x, y, 0), 0.26, 0.20, h)
        sphere(f"ENV_canopy_{i}", "tree", (x, y, h + r * 0.55), (r, r, r * 0.92))
        sphere(f"ENV_canopy_b{i}", "tree_l", (x - r * 0.45, y - 0.5, h + r * 0.25), (r * 0.62, r * 0.62, r * 0.58))
    # pots along the fence and at the patio's back edge
    for tag, loc, kind, s in (("a", (-3.3, 4.7, 0), "sun", 1.25), ("b", (-2.1, 4.9, 0), "hyd", 1.2), ("c", (2.9, 4.8, 0), "sun", 1.3),
                              ("d", (4.2, 4.7, 0), "hyd", 1.25), ("e", (-0.3, 4.9, 0), "hyd", 1.1), ("f", (1.6, 4.9, 0), "sun", 1.1),
                              ("g", (-2.75, 1.25, 0.03), "hyd", 0.9), ("h", (2.05, 1.30, 0.03), "sun", 0.85)):
        build_pot(tag, loc, kind, s)
    # bunting: one string over the patio's front (the fly-in passes under it), one near the fence
    build_bunting("front", (-6.5, -3.0, 4.3), (6.5, -3.0, 4.3), 0.75, 13, 0)
    build_bunting("back", (-7.5, 4.2, 3.9), (7.5, 4.2, 3.9), 0.7, 15, 1)
    # the laundry basket with folded towels, back left on the patio; it never moves
    b = empty("RIG_basket", (-2.05, 0.35, 0.03))
    cone("PRP_basket", "wicker", (0, 0, 0), 0.34, 0.42, 0.44, parent=b)
    torus("PRP_basket_rim", "wicker", (0, 0, 0.44), 0.42, 0.035, parent=b)
    for i, (key, dz) in enumerate((("tw_pink", 0.44), ("tw_mint", 0.53), ("tw_lilac", 0.62))):
        box(f"PRP_towel_{i}", key, (0.02 * i, 0, dz + 0.04), (0.56 - 0.05 * i, 0.44 - 0.04 * i, 0.09), parent=b, rot=(0, 0, D(8 * i)))
    # a little terracotta garden turtle on the patio's left edge; it never moves
    tt = empty("RIG_turtle", (-2.55, -1.55, 0.03), rot=(0, 0, D(-40)))
    sphere("PRP_turtle_shell", "terra", (0, 0, 0.10), (0.20, 0.24, 0.13), parent=tt)
    sphere("PRP_turtle_head", "terra", (0, -0.27, 0.11), (0.075, 0.085, 0.07), parent=tt)
    for i, (dx, dy) in enumerate(((-0.16, -0.14), (0.16, -0.14), (-0.16, 0.14), (0.16, 0.14))):
        sphere(f"PRP_turtle_foot{i}", "terra", (dx, dy, 0.04), (0.06, 0.07, 0.04), parent=tt)
    # the sprinkler on the lawn, right front, with its coiled hose; nothing on it moves
    sp = empty("RIG_sprinkler", SPR, rot=(0, 0, D(35)))
    cone("PRP_spr_base", "hose", (0, 0, 0), 0.20, 0.16, 0.07, parent=sp)
    cone("PRP_spr_stem", "brass", (0, 0, 0.07), 0.04, 0.04, 0.22, parent=sp)
    sphere("PRP_spr_head", "brass", (0, 0, 0.33), (0.075, 0.075, 0.065), parent=sp)
    for i in range(3):
        torus(f"PRP_hose_{i}", "hose", (SPR[0] + 0.75, SPR[1] + 0.15, 0.04 + 0.07 * i), 0.30 - 0.02 * i, 0.04)
    cone("PRP_hose_lead", "hose", (SPR[0] + 0.18, SPR[1] + 0.05, 0.04), 0.04, 0.04, 0.34, rot=(0, D(90), D(10)))


def build_rack():
    """The wooden A-frame drying rack: one piece, it never moves."""
    for sx, x in (("l", 0.02), ("r", 1.58)):
        for sy, dy in (("f", -0.42), ("b", 0.42)):
            L = math.hypot(dy, BAR_Z)
            cone(f"PRP_rack_leg_{sx}{sy}", "rack", (x, RACK_Y + dy, 0.03), 0.028, 0.028, L, rot=(math.atan2(dy, BAR_Z), 0, 0))
        box(f"PRP_rack_tie_{sx}", "rack", (x, RACK_Y, 0.42), (0.045, 0.58, 0.045))
    cone("PRP_rack_bar", "rack", (-0.06, RACK_Y, BAR_Z), 0.026, 0.026, 1.72, rot=(0, D(90), 0))
    cone("PRP_rack_rail", "rack", (0.02, RACK_Y + 0.27, 0.48), 0.02, 0.02, 1.56, rot=(0, D(90), 0))


def shirt_inside(x, z):
    """Is (x, z) inside the T-shirt's outline? x is measured from its centre line."""
    ax = abs(x)
    if z > SH_TOP or z < SH_HEM:
        return False
    if z > SH_TOP - 0.06 and ax < 0.13 - 0.9 * (SH_TOP - z):         # the neck scoop
        return False
    if ax <= 0.36:
        return True
    top = SH_TOP - 0.24 * (ax - 0.13) / 0.50                         # the shoulder slopes down to the sleeve end
    return ax <= 0.63 and z <= top and z >= top - 0.30 + 0.25 * (ax - 0.36)   # the sleeve


def build_shirt():
    """ONE plain light-gray T-shirt hanging from the rack's bar, facing the camera, with two wooden pegs.
    sway = its lower part swings back (+Y) and a little sideways, used only while Sol's side pushes it."""
    NX, NZ = 85, 71
    bm = bmesh.new()
    x0, x1 = SH_X - 0.66, SH_X + 0.66
    vs = [[bm.verts.new((lerp(x0, x1, i / (NX - 1)), SH_Y, lerp(SH_HEM, SH_TOP, k / (NZ - 1)))) for k in range(NZ)] for i in range(NX)]
    for i in range(NX - 1):
        for k in range(NZ - 1):
            cx = lerp(x0, x1, (i + 0.5) / (NX - 1)) - SH_X
            cz = lerp(SH_HEM, SH_TOP, (k + 0.5) / (NZ - 1))
            if shirt_inside(cx, cz):
                bm.faces.new((vs[i][k], vs[i + 1][k], vs[i + 1][k + 1], vs[i][k + 1]))
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    o = mesh_obj("PRP_shirt", bm, "shirt", smooth=False)
    sol = o.modifiers.new("thick", 'SOLIDIFY')
    sol.thickness, sol.offset = 0.022, 1.0

    def hang(z):
        return min(1.0, max(0.0, (SH_TOP - z) / (SH_TOP - SH_HEM)))
    keys = shape_keys(o, {"sway": lambda c: (0.03 * hang(c.z) ** 1.5, 0.11 * hang(c.z) ** 1.5, 0.012 * hang(c.z) ** 2)})
    for s in (-1, 1):
        box(f"PRP_peg_{s}", "rack", (SH_X + s * 0.26, SH_Y - 0.012, SH_TOP - 0.03), (0.035, 0.03, 0.12))
    # the wet patch: one round dark-gray patch lying on the shirt's chest. It grows once (clip 1) and then never changes.
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=1.0)
    p = mesh_obj("PRP_wet_patch", bm, "wet", (PATCH[0], SH_Y - 0.026, PATCH[1]), (PATCH_R, PATCH_R, PATCH_R), rot=(D(90), 0, 0), smooth=False)
    track(p, "location", "scale")
    return {"keys": keys, "patch": p, "hang": hang}


def shirt(sh, f, wet=1.0, sway=0.0):
    """wet: 0 = dry shirt, 1 = the full patch. sway: how far the lower part is pushed back."""
    set_shape(sh["keys"]["sway"], sway, f)
    h = sh["hang"](PATCH[1]) ** 1.5
    r = PATCH_R * wet
    sh["patch"].scale = (r, r, r)
    sh["patch"].location = (PATCH[0] + 0.03 * h * sway, SH_Y - 0.026 + 0.11 * h * sway, PATCH[1] + 0.012 * sh["hang"](PATCH[1]) ** 2 * sway)


def build_jet(n=46, seed=5):
    """The one arc of water drops from the sprinkler to the shirt's chest (clip 1 only)."""
    rnd = random.Random(seed)
    drops = []
    for i in range(n):
        o = sphere(f"FX_drop_{i}", "drop", (0, 0, -5), (0.034, 0.034, 0.05), alpha=0.95)
        track(o, "location")
        drops.append({"o": o, "ph": i / n + rnd.uniform(-0.01, 0.01), "j": (rnd.uniform(-1, 1), rnd.uniform(-1, 1))})
    return drops


def jet(drops, t, t0, t1, flight=0.34):
    """Drops leave the nozzle between t0 and t1 and fly a low arc to the patch. Outside that they are hidden."""
    tgt = (PATCH[0] + 0.02, SH_Y - 0.03, PATCH[1])
    for d in drops:
        born = lerp(t0, t1 - flight, d["ph"])
        u = (t - born) / flight
        if u < 0 or u > 1:
            d["o"].location = (0, 0, -5)
            continue
        sp = 0.05 + 0.10 * u
        d["o"].location = (lerp(NOZ[0], tgt[0], u) + sp * d["j"][0] * 0.5, lerp(NOZ[1], tgt[1], u),
                           lerp(NOZ[2], tgt[2], u) + 0.55 * 4 * u * (1 - u) + sp * d["j"][1] * 0.5)


def stage(name, n, sun=(52, 0, -28), jet_drops=False):
    new_scene(name, n)
    key = [o for o in S["sc"].objects if o.name.startswith("LGT_key")][0]
    key.rotation_euler = tuple(D(a) for a in sun)
    build_garden()
    build_rack()
    sh = build_shirt()
    return sh, (build_jet() if jet_drops else None)


# ================================================================ the weave, close up (clips 3 and 4)
# The shirt's cloth seen very close: the SAME chunky light-gray yarns in both close-ups, modelled in the shirt's colour.
# Two layers of plain weave. Weft yarns run away from the camera (+Y) and are cut off flat at y = 0, so a side-on
# camera sees their round ends; warp yarns run across (X) and wave over and under them.
WP, WR, WA = 0.50, 0.125, 0.25        # pitch, yarn radius, how far the warp waves up and down
LAYERS = ((0.0, 0.0), (-0.86, 0.5))   # (height, sideways shift in pitches) of the two layers
WTOP = 0.56                           # the water's smooth top surface (clip 4)
XWET = -2.75                          # the water starts here; left of it the cloth is dry


def tube(name, key, pts, r, seg=10):
    bm = bmesh.new()
    rings = []
    n = len(pts)
    for i, p in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        tx, tz = b[0] - a[0], b[2] - a[2]
        L = math.hypot(tx, tz) or 1.0
        nx, nz = -tz / L, tx / L                                   # the normal in the XZ plane; the other axis is Y
        rings.append([bm.verts.new((p[0] + r * math.cos(TAU * k / seg) * nx, p[1] + r * math.sin(TAU * k / seg),
                                    p[2] + r * math.cos(TAU * k / seg) * nz)) for k in range(seg)])
    for i in range(n - 1):
        for k in range(seg):
            bm.faces.new((rings[i][k], rings[i + 1][k], rings[i + 1][(k + 1) % seg], rings[i][(k + 1) % seg]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return mesh_obj(name, bm, key)


def build_weave(wet=False, x0=-12, x1=12, depth=8, y_from=0):
    for li, (lz, sh) in enumerate(LAYERS):
        key = "fiber" if li == 0 else "fiber_d"
        for i in range(x0, x1 + 1):
            x = (i + sh) * WP
            cone(f"PRP_weft_{li}_{i}", key, (x, 0.0, lz), WR, WR, WP * depth + 0.4, rot=(D(-90), 0, 0))
            cone(f"PRP_weft_end_{li}_{i}", "fiber_e" if li == 0 else "fiber", (x, -0.004, lz), WR * 0.5, WR * 0.5, 0.004, rot=(D(-90), 0, 0))
        for j in range(y_from, depth):
            y = 0.20 + j * WP
            pts = [((x0 - 1 + k / 8.0 + sh) * WP, y, lz + WA * math.cos(math.pi * (x0 - 1 + k / 8.0) + math.pi * j))
                   for k in range((x1 - x0 + 2) * 8 + 1)]
            tube(f"PRP_warp_{li}_{j}", key, pts, WR)
    # what lies under the two layers: more cloth, plain and soft, so the lower half of the frame is calm for captions
    box("ENV_cloth_below", "fiber_d", (0, WP * depth / 2, -3.6), (40, WP * depth + 0.6, 4.4))
    box("ENV_cloth_face", "fiber_d", (0, 0.05, -3.6), (40, 0.1, 4.4))
    if wet:
        # clear pale water fills every gap from XWET to the right and lies in one smooth level sheet over the top yarns
        w = box("PRP_water", "water", ((XWET + 20) / 2, 2.0, (WTOP - 1.40) / 2), (20 - XWET, 4.3, WTOP + 1.40), alpha=0.50)
        w.visible_shadow = False
        box("PRP_water_top", "white", ((XWET + 20) / 2, 2.0, WTOP), (20 - XWET, 4.3, 0.035), alpha=0.85).visible_shadow = False


def stage_weave(name, n, wet, sun=(38, 0, -30), depth=8):
    new_scene(name, n)
    key = [o for o in S["sc"].objects if o.name.startswith("LGT_key")][0]
    key.rotation_euler = tuple(D(a) for a in sun)
    key.data.energy = 1.7
    w = S["sc"].world
    w.node_tree.nodes["Background"].inputs["Color"].default_value = tuple(c ** 2.2 for c in (0.99, 0.95, 0.80)) + (1,)
    build_weave(wet, depth=depth)


# ================================================================ test views of the set (not clips of the film)
def clip0():
    n = 48
    sh, drops = stage("wet_0", n, jet_drops=True)
    sol = build_sol2(SOL, 12)
    cam = build_cam(24)
    TL = [(0.0, "normal")]

    def state(t, f):
        shirt(sh, f, wet=smooth(t, 0.5, 0.8))
        jet(drops, t, 0.1, 0.8)
        k = smooth(t, 0.0, 2.0)
        cam(lerp3((-4.6, -8.4, 6.4), (0.15, -4.1, 1.05), k), lerp3((0.4, 1.5, 0.6), (0.25, 0.0, 0.72), k))
        act(sol, t, f, TL, yaw=12, squash=idle(t))
    return animate(n, state)


def clip90():
    """Test: the dry weave from above."""
    n = 24
    stage_weave("weave_dry", n, False, depth=20)
    cam = build_cam(30)

    def state(t, f):
        cam((-1.6, 0.9, 3.3), (0.5, 4.4, 0.0))
    return animate(n, state)


def clip91():
    """Test: the wet weave side-on."""
    n = 24
    stage_weave("weave_wet", n, True)
    cam = build_cam(30)

    def state(t, f):
        k = smooth(t, 0.0, 0.7)
        cam((lerp(-4.4, 0.2, k), -4.6, 0.25), (lerp(-4.4, 0.2, k), 0.0, -1.35))
    return animate(n, state)
