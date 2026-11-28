"""Skeleton clips for the ad "POV: You're Doing the Whole Group Project" (script v2, ../script.txt).
exec()'d after rig.py by render_clip.py.

SQUARE film. The painter only returns 16:9 or 9:16, so every clip is rendered and painted 16:9 and the MIDDLE SQUARE is
the film (composite.py crops it). Frame every shot for the middle square; what is left and right of it is spare beach.
Render:  SKEL_FPS=24 Blender -b --factory-startup --python render_clip.py -- <n> <out.mp4>
Sol is the working 38-expression model. He is 1.0 tall. The camera mostly looks toward +Y (the sea).
Times are seconds on each clip's own clock and follow the trimmed takes in ../audio/edit/ (voice starts in brackets).
Frame counts are written for 30 fps and converted by rig.py.

The beach (metres): our castle at CAS, the plan board at BOARD (left of it), the contest clock at CLOCK (further
left), the other team's plot at RIVAL (far left, back), our three lazy teammates at LOUNGE (right), the banner on
two poles at y = -5.5 (behind every camera except the fly-in of clip 1).
Lettering is never in the skeleton: every OVL_ plane is rendered as its own pass (MODE=ovlseq).
"""
import random

TAU = 2 * math.pi
CAS = (0.5, 1.2, 0)
BUCKET = (1.55, 0.95, 0)
BOARD = (-3.0, 1.6, 0)
CLOCK = (-6.6, 3.2, 0)
RIVAL = (-9.5, 9.0, 0)
LOUNGE = {"ring": (3.5, 1.0, 0), "hat": (5.0, 1.3, 0), "sleepy": (6.5, 1.0, 0)}
UMB = (7.05, 1.55)


# ================================================================ helpers
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
    cd.clip_end = 3000
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
    """Sol with his legs and the marks' turns keyed too. sol["mesh"] is his body mesh."""
    sol = build_sol(loc, yaw)
    for c in sol["root"].children_recursive:
        nm = c.name.split(".")[0]
        if nm in ("SOL_leg_L", "SOL_leg_R"):
            sol["leg_l" if nm.endswith("L") else "leg_r"] = c
            sol[nm] = tuple(c.location)
            track(c, "location")
        if nm == "SOL_body":
            sol["mesh"] = c
    for objs in sol["eyes"]["marks"].values():
        for o in objs:
            track(o, "rotation_euler")
    return sol


def act(sol, t, f, timeline, look=(0.0, 0.0), blinks=(), marks=None, legs=((0, 0), (0, 0)), **pose):
    """Eyes and marks from the emotion timeline (with its bounce), then the body pose with that bounce added.
    legs: (forward, up) in metres per leg."""
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


def scurry(t, on, rate=7.0):
    """Leg positions for running on the spot or along the ground: the two feet in turn."""
    ph = math.sin(TAU * rate * t) * on
    return ((0.05 * ph, 0.045 * max(ph, 0.0)), (-0.05 * ph, 0.045 * max(-ph, 0.0)))


def moves(t, p0, mv):
    """Where he is at time t: starts at p0 and makes each move (start, end, (x, y)) in turn."""
    p = p0
    for ts, te, q in mv:
        k = smooth(t, ts, te)
        p = (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
    return p


def hops(t, t0, t1, p0, p1, n=2, h=0.16):
    """Hopping from p0 to p1 between t0 and t1 in n hops: returns (x, y, z)."""
    k = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
    z = h * abs(math.sin(math.pi * n * k)) if 0 < k < 1 else 0.0
    return (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k), z)


def tri(name, key, pts, loc, parent=None, rot=(0, 0, 0)):
    """A flat triangle (a pennant)."""
    bm = bmesh.new()
    bm.faces.new([bm.verts.new(p) for p in pts])
    return mesh_obj(name, bm, key, loc, parent=parent, rot=rot, smooth=False)


# ================================================================ the things on the beach
def tower(tag, x, y, r, h, parent, teeth=6):
    cone(f"PRP_castle_tower_{tag}", "castle", (x, y, 0), r, r * 0.86, h, parent=parent)
    cone(f"PRP_castle_rim_{tag}", "castle", (x, y, h - 0.02), r * 0.97, r * 0.97, 0.07, parent=parent)
    for i in range(teeth):
        a = TAU * i / teeth + 0.26
        box(f"PRP_castle_tooth_{tag}_{i}", "castle", (x + r * 0.78 * math.cos(a), y + r * 0.78 * math.sin(a), h + 0.085),
            (r * 0.36, r * 0.36, 0.09), parent=parent, rot=(0, 0, a))
    box(f"PRP_castle_window_{tag}", "castle_d", (x, y - r * 0.9, h * 0.62), (r * 0.34, 0.04, r * 0.5), parent=parent)


def build_castle(tag, loc, stage_="done", flag="coral", s=1.0):
    """The sandcastle. "start": one tower, half a wall and a heap of sand. "done": the course card's castle: a tall
    middle tower with a flag, two side towers, a front wall with a gate, shells."""
    r = empty("RIG_castle_" + tag, loc)
    r.scale = (s, s, s)
    sphere(f"PRP_castle_base_{tag}", "castle", (0, 0.06, 0.0), (1.3, 0.9, 0.09), parent=r)
    if stage_ == "done":
        tower(tag + "c", 0, 0.28, 0.40, 0.95, r)
        tower(tag + "l", -0.7, -0.02, 0.29, 0.6, r)
        tower(tag + "r", 0.7, -0.02, 0.29, 0.6, r)
        box(f"PRP_castle_wall_{tag}", "castle", (0, -0.12, 0.2), (1.2, 0.26, 0.4), parent=r)
        for i, x in enumerate((-0.24, 0.0, 0.24)):
            box(f"PRP_castle_walltooth_{tag}_{i}", "castle", (x, -0.12, 0.445), (0.13, 0.27, 0.09), parent=r)
        box(f"PRP_castle_gate_{tag}", "castle_d", (0, -0.25, 0.13), (0.22, 0.04, 0.26), parent=r)
        cone(f"PRP_castle_gatetop_{tag}", "castle_d", (0, -0.23, 0.26), 0.11, 0.11, 0.04, parent=r, rot=(D(90), 0, 0))
        cone(f"PRP_flagpole_{tag}", "wood_d", (0, 0.28, 1.0), 0.016, 0.016, 0.56, parent=r)
        tri(f"PRP_flag_{tag}", flag, [(0, 0, 0), (0.32, 0, -0.115), (0, 0, -0.23)], (0.012, 0.28, 1.55), parent=r)
        for i, (x, y, key) in enumerate([(-0.95, -0.55, "shell"), (0.2, -0.62, "shell2"), (0.9, -0.5, "shell"), (-0.3, -0.7, "shell2")]):
            sphere(f"PRP_shell_{tag}_{i}", key, (x, y, 0.03), (0.09, 0.075, 0.035), parent=r, rot=(0, 0, D(40 * i)))
    else:
        tower(tag + "l", -0.7, -0.02, 0.29, 0.6, r)
        box(f"PRP_castle_wall_{tag}", "castle", (-0.17, -0.12, 0.17), (0.56, 0.26, 0.34), parent=r)
        sphere(f"PRP_castle_heap_{tag}", "castle", (0.5, 0.12, 0.0), (0.52, 0.44, 0.27), parent=r)
        sphere(f"PRP_shell_{tag}_0", "shell", (-0.95, -0.55, 0.03), (0.09, 0.075, 0.035), parent=r)
    return r


def build_bucket(loc, down=False):
    """The red bucket: one piece, standing beside the castle in every clip (as on the course card)."""
    r = empty("RIG_bucket", loc)
    cone("PRP_bucket", "red", (0, 0, 0), 0.19, 0.26, 0.36, parent=r)
    cone("PRP_bucket_rim", "red", (0, 0, 0.34), 0.275, 0.275, 0.035, parent=r)
    cone("PRP_bucket_inside", "red_d", (0, 0, 0.372), 0.235, 0.235, 0.006, parent=r)
    track(r, "location", "rotation_euler")
    if down:
        r.location, r.rotation_euler = (loc[0] + 0.14, loc[1], 0.255), (0, D(96), 0)
    return r


def build_shovel(loc, yaw):
    r = empty("RIG_shovel", loc, rot=(0, 0, D(yaw)))
    box("PRP_shovel_blade", "red", (0, 0.12, 0.02), (0.2, 0.26, 0.03), parent=r)
    cone("PRP_shovel_handle", "red", (0, 0.22, 0.03), 0.022, 0.022, 0.42, parent=r, rot=(D(-90), 0, 0))
    box("PRP_shovel_grip", "red", (0, 0.66, 0.03), (0.16, 0.05, 0.04), parent=r)


def build_board(state):
    """The plan board: a wooden board on two legs with one cream page. state: "castle" (the drawing), "split" (the drawing,
    which clip 3 swaps for the four task cards), "cards" (the four cards), "table" (the team doc). Returns the four card planes (clip 3 pops them)."""
    r = empty("RIG_board", BOARD, rot=(0, 0, D(12)))
    for s in (-1, 1):
        cone(f"PRP_board_leg{s}", "wood_d", (s * 0.6, 0.06, 0), 0.04, 0.04, 1.95, parent=r)
    box("PRP_board", "wood", (0, 0, 1.3), (1.52, 0.05, 1.12), parent=r)
    box("PRP_board_page", "cream", (0, -0.035, 1.3), (1.38, 0.02, 0.98), parent=r)
    cards = {}
    if state in ("castle", "split"):
        o = overlay_plane("plan_castle", "plan_castle.png", (0, -0.05, 1.3), (1.3, 0.92), parent=r)
        track(o, "scale")
        cards["drawing"] = o
    if state in ("split", "cards"):
        for i, (k, dx, dz) in enumerate((("towers", -0.338, 0.235), ("walls", 0.338, 0.235), ("moat", -0.338, -0.235), ("flag", 0.338, -0.235))):
            o = overlay_plane("card_" + k, f"card_{k}.png", (dx, -0.058 - 0.002 * i, 1.3 + dz), (0.66, 0.432), parent=r)
            track(o, "scale")
            cards[k] = o
    if state == "table":
        overlay_plane("plan_table", "plan_table.png", (0, -0.05, 1.3), (1.3, 0.92), parent=r)
    return cards


def sign_board(name, art, parent, z):
    """A cream board in a coral frame with one line of printed lettering laid over it."""
    r = empty("RIG_" + name, (0, -0.05, z), parent=parent)
    box("PRP_" + name + "_frame", "coral", (0, 0.03, 0), (1.46, 0.04, 0.56), parent=r)
    box("PRP_" + name, "cream", (0, 0, 0), (1.34, 0.05, 0.46), parent=r)
    overlay_plane(name, art, (0, -0.03, 0), (1.2, 0.36), parent=r)
    return r


def build_clock(second=None):
    """The contest clock on its post, with the JUDGING 6:00 board under it. second: None (no second board), "drop"
    (clip 5 drops it in) or "on". Returns (hand pivot, second board)."""
    r = empty("RIG_clock", CLOCK)
    cone("PRP_clock_post", "wood_d", (0, 0, 0), 0.075, 0.065, 1.75, parent=r)
    cone("PRP_clock_rim", "wood", (0, 0.06, 2.25), 0.62, 0.62, 0.1, parent=r, rot=(D(90), 0, 0))
    cone("PRP_clock_face", "white", (0, -0.035, 2.25), 0.54, 0.54, 0.03, parent=r, rot=(D(90), 0, 0))
    sphere("PRP_clock_hub", "dark", (0, -0.08, 2.25), (0.05, 0.03, 0.05), parent=r)
    box("PRP_clock_hour", "dark", (0.1, -0.075, 2.34), (0.3, 0.02, 0.055), parent=r, rot=(0, D(-40), 0))
    hand = empty("RIG_clock_hand", (0, -0.085, 2.25), parent=r)
    box("PRP_clock_hand", "dark", (0, 0, 0.2), (0.045, 0.02, 0.42), parent=hand)
    track(hand, "rotation_euler")
    track(r, "rotation_euler")
    sign_board("judging", "judging.png", r, 1.38)
    b2 = None
    if second:
        b2 = sign_board("doneby", "doneby.png", r, 0.84)
        track(b2, "location", "rotation_euler")
    return r, hand, b2


def rod(name, key, p, q, r=0.012):
    """A thin straight rod from p to q (both in the same X-Z plane)."""
    dx, dz = q[0] - p[0], q[2] - p[2]
    return cone(name, key, p, r, r, math.hypot(dx, dz), rot=(0, math.atan2(dx, dz), 0))


def build_bunting(y=4.4, x0=-13.5, x1=13.5, span=4.5, h=2.75):
    """Strings of little coloured pennants on poles right across the back of the contest: the festival look."""
    cols = ("coral", "teal", "towel", "blue", "pink", "cream")
    n, k = int(round((x1 - x0) / span)), 0
    for i in range(n + 1):
        cone(f"PRP_bunting_pole_{i}", "wood_d", (x0 + i * span, y, 0), 0.05, 0.04, h)
    for i in range(n):
        xa = x0 + i * span
        pts = [(xa + u * span, y, h - 0.05 - 0.55 * 4 * u * (1 - u)) for u in [j / 10 for j in range(11)]]
        for j in range(10):
            rod(f"PRP_bunting_string_{i}_{j}", "cream", pts[j], pts[j + 1])
            m = ((pts[j][0] + pts[j + 1][0]) / 2, y, (pts[j][2] + pts[j + 1][2]) / 2)
            tri(f"PRP_pennant_{i}_{j}", cols[k % 6], [(-0.15, 0, 0), (0.15, 0, 0), (0, 0, -0.36)], m)
            k += 1


def build_palm(tag, x, y, s=1.0, lean=0.3):
    """A palm tree for the back of the beach: a leaning trunk and a crown of drooping fronds."""
    px = x
    for i in range(5):
        cone(f"PRP_palm_trunk_{tag}_{i}", "trunk", (px, y, i * 1.0 * s), 0.17 * s * (1 - 0.06 * i), 0.15 * s * (1 - 0.06 * i), 1.04 * s,
             rot=(0, D(lean * 22 * (i + 1) / 3), 0))
        px += math.sin(D(lean * 22 * (i + 1) / 3)) * 1.0 * s
    top = (px, y, 5.0 * s)
    for i in range(8):
        a = TAU * i / 8 + 0.3
        sphere(f"PRP_palm_frond_{tag}_{i}", "palm" if i % 2 else "palm_d", (top[0] + math.cos(a) * 1.25 * s, top[1] + math.sin(a) * 1.25 * s, top[2] - 0.3 * s),
               (1.55 * s, 0.34 * s, 0.11 * s), rot=(0, D(24), a))
    for i in range(2):
        sphere(f"PRP_palm_nut_{tag}_{i}", "trunk", (top[0] + 0.18 * (i * 2 - 1) * s, top[1] - 0.1, top[2] - 0.22 * s), (0.15 * s,) * 3)


def build_beach(banner=True):
    """Sand, the sea and a peach sunset sky: the course card's beach, dressed for a contest day. The banner hangs on
    two poles behind the cameras. The first painted test (2026-11-27) came back as flat as the blockout, with bare
    sand and three flat bands of sky, so the set carries the life itself: dunes with grass, ripples in the sand,
    palms, bunting across the back, clouds in two tones, far hills, and the sun's glint on the water."""
    C.update({"sand_l": (1.0, 0.93, 0.78), "sand_d": (0.90, 0.78, 0.58), "sky_mid": (1.0, 0.81, 0.62), "halo": (1.0, 0.92, 0.72),
              "cloud_l": (1.0, 0.95, 0.88), "cloud_d": (0.97, 0.68, 0.62), "hill": (0.84, 0.62, 0.62), "glint": (1.0, 0.94, 0.76),
              "palm": (0.38, 0.60, 0.42), "palm_d": (0.26, 0.48, 0.38), "trunk": (0.62, 0.44, 0.31), "grass": (0.64, 0.72, 0.42),
              "star": (0.95, 0.45, 0.36)})
    C["sky"] = (0.98, 0.68, 0.58)
    box("ENV_sand", "sand", (0, -13.5, -0.1), (1400, 53, 0.2))
    box("ENV_sand_wet", "sand_wet", (0, 12.3, -0.098), (1400, 1.6, 0.2))
    box("ENV_sea", "sea", (0, 160, -0.06), (1400, 294, 0.1))
    box("ENV_sea_far", "sea_d", (0, 215, -0.055), (1400, 170, 0.1))
    for i, (y, w) in enumerate(((13.15, 0.42), (15.6, 0.16), (19.0, 0.14), (24.5, 0.14), (33.0, 0.16), (47.0, 0.2))):
        box(f"ENV_foam_{i}", "foam", (0, y, -0.008), (1400, w, 0.02))
    box("ENV_sky", "sky", (0, 300.4, 130), (1900, 0.2, 420))        # 300 m away, so the horizon stays level when the camera turns
    box("ENV_sky_mid", "sky_mid", (0, 300.2, 46), (1900, 0.2, 92))
    box("ENV_sky_low", "sky_low", (0, 300.0, 16), (1900, 0.2, 32))
    sphere("ENV_sun_halo", "halo", (-72, 299, 34), (33, 0.5, 33))
    sphere("ENV_sun", "sun", (-72, 298, 34), (17.5, 0.5, 17.5))
    for i, (x, z, k) in enumerate([(-22, 15, 1.0), (4, 19, 1.3), (20, 13, 0.9), (-6, 25, 0.8), (13, 7.5, 0.7), (-17, 8.5, 0.6), (30, 22, 1.1), (-34, 21, 1.2)]):
        sphere(f"ENV_cloud_{i}", "cloud_d", (x * 6.5, 297.5, z * 6.5 - 2.2 * k), (44 * k, 0.5, 8.5 * k))
        sphere(f"ENV_cloud_top_{i}", "cloud_l", (x * 6.5 - 4 * k, 297, z * 6.5 + 2.0 * k), (34 * k, 0.5, 6.5 * k))
        sphere(f"ENV_cloud_puff_{i}", "cloud_l", (x * 6.5 + 14 * k, 297, z * 6.5 + 4.5 * k), (15 * k, 0.5, 6.0 * k))
    for i, (x, sx, sz) in enumerate([(-230, 90, 15), (-150, 55, 9), (215, 80, 12), (300, 60, 17)]):      # far hills on the horizon
        sphere(f"ENV_hill_{i}", "hill", (x, 290, 0), (sx, 2, sz))
    for i in range(16):                                   # the sun's glint: a ladder of pale streaks on the water
        y = 15 + 5.5 * i ** 1.35
        sphere(f"ENV_glint_{i}", "glint", (-72 * y / 298 + (0.8 if i % 2 else -0.8), y, -0.004), (1.4 + 0.5 * i, 0.10 + 0.05 * i, 0.01))
    rnd = random.Random(11)
    for i, (x, y, sx, sy, sz) in enumerate([(-13, 9.0, 6.5, 2.2, 0.55), (-3.5, 10.2, 5.0, 1.6, 0.4), (6.5, 9.2, 6.0, 2.0, 0.5), (15, 8.0, 5.5, 2.2, 0.6),
                                            (-19, 5.5, 4.5, 2.0, 0.5), (19.5, 4.5, 4.5, 2.0, 0.5), (11.5, 6.4, 3.2, 1.3, 0.3), (-1.0, 7.4, 3.0, 1.0, 0.22)]):
        sphere(f"ENV_dune_{i}", "sand_l", (x, y, 0), (sx, sy, sz))                      # low dunes behind the contest
        sphere(f"ENV_dune_shade_{i}", "sand_d", (x + 0.5, y - sy * 0.55, 0), (sx * 0.9, sy * 0.5, sz * 0.35))
        if i not in (1, 7):
            for j in range(7):                            # a tuft of beach grass on top
                gx = x + rnd.uniform(-0.25, 0.25) * sx
                cone(f"PRP_grass_{i}_{j}", "grass", (gx + 0.12 * j - 0.4, y + 0.1, sz * 0.8), 0.045, 0.004, rnd.uniform(0.5, 0.95),
                     rot=(0, D(rnd.uniform(-28, 28)), 0))
    for i in range(34):                                   # soft ripples in the sand
        x, y = rnd.uniform(-9, 9.5), rnd.uniform(-4.2, 3.6)
        sphere(f"ENV_ripple_{i}", "sand_d" if i % 3 else "sand_l", (x, y, 0), (rnd.uniform(0.7, 1.7), rnd.uniform(0.07, 0.13), 0.012), rot=(0, 0, D(rnd.uniform(-10, 10))))
    build_palm("a", 11.6, 7.6, 1.0, 0.3)
    build_palm("b", 12.6, 9.2, 0.82, -0.2)
    build_palm("c", -14.5, 8.6, 0.92, -0.3)
    build_bunting()
    for i, (x, y) in enumerate([(-1.7, -0.9), (3.0, -0.55), (-4.3, 0.4)]):               # starfish
        for j in range(5):
            a = TAU * j / 5 + i
            sphere(f"PRP_starfish_{i}_{j}", "star", (x + 0.085 * math.cos(a), y + 0.085 * math.sin(a), 0.02), (0.1, 0.04, 0.022), rot=(0, 0, a))
    box("PRP_boat_hull", "white", (10.5, 31, 0.25), (2.0, 0.5, 0.5))
    tri("PRP_boat_sail", "sail", [(0, 0, 0), (1.3, 0, 0), (0, 0, 2.3)], (10.4, 31, 0.6))
    rnd = random.Random(3)
    for i in range(9):                                    # shells and pebbles scattered on the sand
        x, y = rnd.uniform(-7, 8), rnd.uniform(-2.2, 5.5)
        if abs(x - CAS[0]) < 2.2 and abs(y - CAS[1]) < 1.8:
            continue
        sphere(f"PRP_beachshell_{i}", ("shell", "shell2", "cream")[i % 3], (x, y, 0.025), (0.085, 0.07, 0.03), rot=(0, 0, rnd.uniform(0, 3)))
    sphere("PRP_ball", "blue", (4.25, 3.1, 0.3), (0.3, 0.3, 0.3))
    torus("PRP_ball_band", "white", (4.25, 3.1, 0.3), 0.292, 0.035, rot=(D(70), D(20), 0))
    if banner:
        for s in (-1, 1):
            cone(f"PRP_banner_pole{s}", "wood_d", (s * 5.2, -5.5, 0), 0.07, 0.06, 5.2)
        b = box("PRP_banner", "cream", (0, -5.5, 4.35), (10.2, 0.05, 1.0))       # high: the camera flies UNDER it (Elaine, 2026-11-27)
        b.visible_shadow = False
        for i, z in enumerate((4.88, 3.82)):
            box(f"PRP_banner_trim{i}", "coral", (0, -5.5, z), (10.2, 0.06, 0.1)).visible_shadow = False
        overlay_plane("banner", "banner.png", (0, -5.54, 4.35), (9.0, 0.82))


def build_lounge():
    """Where the three lazy ones lie about: a teal beach umbrella and a yellow striped towel."""
    a = D(-8)
    cone("PRP_umbrella_pole", "white", (UMB[0], UMB[1], 0), 0.035, 0.035, 2.25, rot=(0, a, 0))
    top = (UMB[0] + math.sin(a) * 1.78, UMB[1], math.cos(a) * 1.78)
    cone("PRP_umbrella", "teal", top, 1.3, 0.05, 0.5, rot=(0, a, 0))
    sphere("PRP_umbrella_tip", "white", (UMB[0] + math.sin(a) * 2.3, UMB[1], math.cos(a) * 2.3), (0.06, 0.06, 0.06))
    t = empty("RIG_towel", (LOUNGE["sleepy"][0], LOUNGE["sleepy"][1] - 0.05, 0.012), rot=(0, 0, D(6)))
    box("PRP_towel", "towel", (0, 0, 0), (1.5, 1.15, 0.024), parent=t)
    for s in (-1, 1):
        box(f"PRP_towel_stripe{s}", "white", (s * 0.5, 0, 0.006), (0.14, 1.15, 0.024), parent=t)


def mate(kind, loc, yaw):
    """One of the other Sols: the same model, plus the one thing that tells him apart (it never comes off).
    ring: a pink swim ring round his middle. hat: a small straw hat on his flame tip. sleepy: nothing."""
    sol = build_sol2(loc, yaw)
    if kind == "ring":
        # Elaine, 2026-11-27, of the ring across his face: "HE CANT EVEN SEE LMFAOO CAN WE LIKE MAKE IT LOWER", and of the
        # shot where it sat at the very bottom of his body: "this si what floaty sol should look like". So it sits right
        # down at his feet, a thinner tube, with clear cream face between it and his eyes from every camera height.
        torus("ACC_ring", "pink", (0, 0, 0.085), 0.345, 0.092, parent=sol["body"], scale=(1.0, 0.80, 1.0))
    if kind == "hat":
        tip = max(sol["mesh"].data.vertices, key=lambda v: v.co.z).co
        h = empty("RIG_hat", (tip.x, tip.y, tip.z - 0.085), parent=sol["body"], rot=(D(5), D(-9), 0))
        cone("ACC_hat_brim", "straw", (0, 0, 0), 0.25, 0.25, 0.03, parent=h)
        cone("ACC_hat_crown", "straw", (0, 0, 0.03), 0.15, 0.125, 0.14, parent=h)
        cone("ACC_hat_band", "coral", (0, 0, 0.03), 0.156, 0.15, 0.045, parent=h)
    return sol


def build_rival():
    """The other team: three plain Sols passing one blue bucket along a line in front of their tall castle (blue flag).
    Background only."""
    build_castle("rival", RIVAL, "done", flag="blue", s=1.35)
    spots = [(RIVAL[0] - 1.5, RIVAL[1] - 1.75), (RIVAL[0] - 0.35, RIVAL[1] - 2.0), (RIVAL[0] + 0.8, RIVAL[1] - 1.75)]
    sols = [build_sol2((x, y, 0), 10 - 10 * i) for i, (x, y) in enumerate(spots)]
    b = empty("RIG_rival_bucket", (0, 0, 0))
    cone("PRP_rival_bucket", "blue", (0, 0, 0), 0.15, 0.2, 0.28, parent=b)
    track(b, "location")
    return {"sols": sols, "spots": spots, "bucket": b}


def rival_at(R, t, f):
    """The bucket goes hand to hand along the line and back, one pass every 0.6 s; each Sol dips as he gets it."""
    per = 0.6
    i = int(t / per)
    k = (t / per) % 1.0
    seq = (0, 1, 2, 1)
    a, b = R["spots"][seq[i % 4]], R["spots"][seq[(i + 1) % 4]]
    kk = smooth(k, 0.15, 0.85)
    R["bucket"].location = (lerp(a[0], b[0], kk), lerp(a[1], b[1], kk) - 0.42, 0.62 + 0.35 * math.sin(math.pi * kk))
    for j, s in enumerate(R["sols"]):
        got = (seq[i % 4] == j) * (1 - smooth(k, 0.0, 0.3)) + (seq[(i + 1) % 4] == j) * smooth(k, 0.7, 1.0)
        act(s, t, f, [(0.0, "happy" if j == 1 else "determined")], yaw=10 - 10 * j, squash=idle(t + j) + 0.07 * got,
            arm_l=(-40 + 70 * got, 20 * got), arm_r=(-40 + 70 * got, 20 * got))


def stage(name, n, castle="start", bucket="down", board="castle", lounge=True, rival=False, clock=None, banner=False, sun=(52, 0, -28)):
    new_scene(name, n)
    key = [o for o in S["sc"].objects if o.name.startswith("LGT_key")][0]
    key.rotation_euler = tuple(D(a) for a in sun)
    key.data.color = (1.0, 0.93, 0.82)
    build_beach(banner)
    out = {}
    if castle:                                   # castle=None: open sand, no castle, bucket or shovel (clip 7)
        out = {"castle": build_castle("ours", CAS, castle), "bucket": build_bucket(BUCKET)}
        build_shovel((2.35, 1.45, 0), 20)
    out["cards"] = build_board(board) if board else None      # board=None: no plan board (shots where its words cannot be laid on)
    out["clock"] = build_clock(clock)
    if lounge:
        build_lounge()
    if rival:
        out["rival"] = build_rival()
    return out


# ================================================================ clip 1: the fly-in, Sol doing everything
def clip1():
    """Narrator: "Sol, how's the sandcastle challenge going?" [0.45-3.5] (a pause: he keeps rushing about) "Wait, are you
    building the whole thing by yourself?" [4.5-7.6].
    The camera starts high in front of the banner, comes down, passes UNDER it between its two poles and lands low in
    front of our Sol (0-1.9). The other team (three Sols passing a bucket in front of a tall castle) is far off at the left.
    Sol, alone, zips between three jobs: pats the tower (0.3, 0.8, 1.3), dashes to the bucket and bumps it with his side so it rocks (2.1),
    dashes to the wall (pats 2.95, 3.12), back to the tower (3.6), the wall (4.16), the tower: faster each time, PANIC
    from 3.3. He stops in the middle (4.75) and sags: SIGH (4.8). At 5.8 he opens his eyes and looks up, still sagging;
    one tired nod (7.85-8.35). His three teammates are not in this shot (they are revealed in clip 2)."""
    n = 255        # 8.5 s: room for a pause between the two lines and for the nod after the second
    st = stage("gp_1", n, castle="start", bucket="up", board=None, lounge=False, rival=True, banner=True)   # the plan board would fly past blank
    T, B, W, M = (-0.72, 0.5), (0.93, 0.6), (0.42, 0.3), (0.2, -0.1)
    MV = [(1.7, 2.05, B), (2.55, 2.9, W), (3.3, 3.58, T), (3.9, 4.14, W), (4.2, 4.42, T), (4.46, 4.75, M)]
    PATS = (0.3, 0.8, 1.3, 2.95, 3.12, 3.62, 3.78, 4.16)
    sol = build_sol2((T[0], T[1], 0), 30)
    cam = build_cam(24)
    TL = [(0.0, "determined"), (3.3, "panic"), (4.8, "sigh"), (5.8, "normal")]
    # Elaine on cut v5: "when u fly in u should fly through the bottom cuz rn it just fazes through the flag". The camera
    # now comes straight in: high in front of the banner (its words square to the lens), down, UNDER the cloth between
    # the two poles with the cloth passing overhead, and lands in front of Sol. No swing out to the side.
    FLY = [(0.6, -16.0, 8.2), (0.58, -12.0, 5.6), (0.55, -8.6, 2.9), (0.5, -5.9, 1.4), (0.5, -4.2, 0.82)]
    TGT = [(0.3, -5.5, 4.35), (0.3, -5.5, 3.9), (0.3, -2.0, 1.9), (0.25, 0.6, 0.75), (0.25, 0.6, 0.62)]
    F0 = smooth(0.0, -0.5, 1.9)

    def state(t, f):
        rival_at(st["rival"], t, f)
        u = (smooth(t, -0.5, 1.9) - F0) / (1 - F0)
        creep = smooth(t, 1.9, 8.5)
        cam(lerp3(cr(FLY, u), (0.5, -3.7, 0.74), creep), cr(TGT, u))
        st["bucket"].rotation_euler = (0, D(7 * wobble(t, 2.2, freq=15, decay=5)), 0)       # he bumps it: it rocks and settles
        p, q = moves(t, T, MV), moves(t + 0.03, T, MV)
        v = max(-1.0, min(1.0, (q[0] - p[0]) / 0.03 / 5.0))
        run = min(1.0, abs(v) * 2.5)
        pat = sum(bump(t, a - 0.1, a + 0.14) for a in PATS)
        hit = bump(t, 2.05, 2.4)
        work = 1 - smooth(t, 4.5, 4.8)
        sag = smooth(t, 4.75, 5.1)
        up = smooth(t, 5.8, 6.2)
        nod = bump(t, 7.85, 8.35)
        act(sol, t, f, TL, look=(0.6 * work * (1 - run), 0.25 * work + 0.8 * up - 0.5 * nod), legs=scurry(t, run),
            loc=(p[0], p[1], 0), yaw=(28 + 50 * v) * work, lean=15 * v + 9 * pat * work + 12 * hit,
            pitch=-4 * work - 14 * sag * (1 - up) + 7 * up - 22 * nod,
            squash=idle(t) + 0.08 * pat - 0.03 * run + 0.08 * sag * (1 - 0.5 * up) + 0.06 * nod,
            arm_l=(-40 + 30 * run - 18 * sag, 0), arm_r=(-40 + 75 * pat * work + 30 * run - 18 * sag, 0))
    return animate(n, state)


def akimbo(sol):
    """HANDS ON HIPS arms for a Sol: each arm is ONE plain bend, a < on screen left and a > on screen right: out from
    the shoulder to an elbow, then back in to rest on his side. Elaine, 2026-11-27: "can we not have the las segment of
    the hands be like pointed out so just an angle like this <>". His ordinary nubs are straight and cannot bend, and
    the painter, left to invent the pose, drew a bend and then flared the tip outward again. So the bend is built here.
    Returns the two bent arms; akimbo_at() swaps them in for the straight nubs."""
    import mathutils
    out = []
    body = sol["body"]
    for vl in S["sc"].view_layers:                      # the model has only just been linked: let Blender place it first
        vl.update()
    for key in ("arm_l", "arm_r"):
        piv = sol[key]
        mesh = [c for c in piv.children_recursive if c.type == 'MESH'][0]
        sh = body.matrix_world.inverted() @ piv.matrix_world.translation
        sx = -1.0 if sh.x < 0 else 1.0
        r = empty("RIG_akimbo_" + key, tuple(sh), parent=body)
        # SMALL, like his own nubs, hugging his side: a stubby upper piece out to a little elbow and a stubby lower piece
        # back in to his body. Elaine on cut v11, of a bigger version that read as long bent arms: "wtf are these arms i
        # meant like the ones before but u remove the tips at the end ... so it doesnt have that stick out portion".
        pts = [mathutils.Vector((0, 0, 0.02)), mathutils.Vector((sx * 0.082, -0.02, -0.05)), mathutils.Vector((sx * 0.012, -0.03, -0.125))]
        rad = [0.056, 0.053, 0.048]
        for j in range(2):
            p0, p1 = pts[j], pts[j + 1]
            L = (p1 - p0).length
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=False, segments=24, radius1=rad[j], radius2=rad[j + 1], depth=L)
            bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, L / 2))
            for z, rr in ((0.0, rad[j]), (L, rad[j + 1])):
                ball = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=rr)
                bmesh.ops.translate(bm, verts=ball["verts"], vec=(0, 0, z))
            me = bpy.data.meshes.new(f"FX_akimbo_{key}_{j}")
            bm.to_mesh(me)
            bm.free()
            for poly in me.polygons:
                poly.use_smooth = True
            for m in mesh.data.materials:
                me.materials.append(m)
            o = bpy.data.objects.new(f"SOL_akimbo_{key}_{j}", me)
            o.location = p0
            o.rotation_euler = (p1 - p0).to_track_quat('Z', 'Y').to_euler()
            link(o, r)
        r.scale = (0, 0, 0)
        track(r, "scale")
        track(piv, "scale")
        out.append(r)
    sol["akimbo"] = out
    return out


def akimbo_at(sol, k):
    """k = 0: his ordinary nubs. k = 1: hands on hips. In between the nubs shrink away as the bent arms grow."""
    k = min(1.0, max(0.0, k))
    for r, key in zip(sol["akimbo"], ("arm_l", "arm_r")):
        r.scale = (k, k, k)
        sol[key].scale = (1 - k, 1 - k, 1 - k)


# ================================================================ clip 2: "and that's your team?"
def clip2():
    """Narrator: "And that's your team?" [1.4-2.5] "Okay, here are five things that'll fix this." [3.45-6.45].
    Opens CLOSE on Sol: ANGRY (flame top red), turned to the right, one nub up, pointing off to the right (0-0.9).
    The camera WHIPS right (0.9-1.25) to his three teammates and holds: Sleepy Sol asleep under the umbrella, Hat Sol
    with his back to us, staring at the sea, Ring Sol bobbing in his swim ring with his eyes shut.
    It WHIPS back (2.75-3.1): Sol faces the camera, perfectly still, with flat half-shut eyes (the deadpan). At 4.4 he
    plants both nubs on his sides and stands tall, CONFIDENT (plain eyes), looking up."""
    n = 204
    stage("gp_2", n, castle="start", bucket="down", board="castle")
    M = (0.2, -0.1)
    sol = build_sol2((M[0], M[1], 0), 18)
    akimbo(sol)
    ring = mate("ring", LOUNGE["ring"], 12)
    hat = mate("hat", LOUNGE["hat"], 172)
    sleepy = mate("sleepy", LOUNGE["sleepy"], -14)
    cam = build_cam(24)
    # Elaine on cut v7, of the glare with his nubs out at "that'll fix this": "this doesnt make sense can we like make sol
    # like hold his hands on his sides like hes confident after hearing the 5 tips". So from 4.4 he is CONFIDENT: plain
    # eyes, both nubs planted on his sides, standing tall with his chest out, looking up. No glare.
    TL = [(0.0, "angry"), (2.0, "sleepy"), (4.4, "normal")]

    def state(t, f):
        w1, w2 = smooth(t, 0.9, 1.25), smooth(t, 2.75, 3.1)
        a_p, a_t = (0.5, -1.85, 0.6), (0.2, -0.1, 0.36)
        b_p, b_t = (4.75 + 0.12 * smooth(t, 1.25, 2.75), -3.95, 0.86), (4.85, 1.15, 0.5)
        c_p, c_t = lerp3((0.2, -2.15, 0.58), (0.2, -1.95, 0.6), smooth(t, 3.1, 6.8)), (0.2, -0.1, 0.36)
        cam(lerp3(lerp3(a_p, b_p, w1), c_p, w2), lerp3(lerp3(a_t, b_t, w1), c_t, w2))
        front = smooth(t, 1.4, 2.4)                     # he turns to the camera while we are looking at the others
        point = smooth(t, 0.1, 0.35) * (1 - front)
        dead = smooth(t, 2.0, 2.3) * (1 - smooth(t, 4.3, 4.5))
        det = smooth(t, 4.35, 4.6)
        plant = bump(t, 4.35, 4.75)                      # the little bounce as he plants his nubs
        akimbo_at(sol, 0.0)       # the built < > arms are not used: Elaine asked for the first hands-on-hips look back (v12)
        act(sol, t, f, TL, blinks=(5.6,), look=(0.85 * (1 - front), 0.75 * det), loc=(M[0], M[1], 0),
            yaw=18 * (1 - front), lean=9 * point, pitch=10 * det,
            squash=idle(t) * (1 - dead) - 0.08 * det + 0.05 * plant,
            # the pointing nub is LEVEL: straight out to the side at his team (Elaine on cut v10, of a nub raised 65 degrees:
            # "hand points up like this but it should look like this", the second picture being a nub sticking straight out)
            arm_l=(-40 + 34 * plant - 24 * det, 26 * det), arm_r=(-40 + 46 * point + 34 * plant - 24 * det, 26 * det))
        bob = math.sin(TAU * 0.9 * t)
        act(ring, t, f, [(0.0, "content")], loc=LOUNGE["ring"], yaw=12, lean=7 * bob, squash=0.035 * math.sin(TAU * 1.8 * t),
            arm_l=(-40 + 12 * bob, 0), arm_r=(-40 - 12 * bob, 0))
        act(hat, t, f, [(0.0, "normal")], loc=LOUNGE["hat"], yaw=172, lean=2 * math.sin(t * 1.4), squash=idle(t + 1))
        act(sleepy, t, f, [(0.0, "asleep")], loc=LOUNGE["sleepy"], yaw=-14, lean=-9, pitch=-5,
            squash=0.03 + 0.035 * math.sin(TAU * 0.45 * t))
    return animate(n, state)


# ================================================================ clip 3: tip 1, small pieces
def clip3():
    """Narrator: "First, split the project into small pieces." [0.5-3.2] ("split" at 1.24).
    Low angle looking up at the plan board (a drawing of the castle on it), Sol standing at its right. The camera
    cranes down into place in the first half second and then holds still.
    Sol looks at the board, THINKING (three dots). IDEA at 0.8 (light bulb). At 1.15 he hops at the board and flaps
    the nub nearest it; four task cards pop out over the drawing, one at a time (1.3, 1.7, 2.1, 2.5; laid on in the
    edit). Normal at 2.7; at 3.1 he looks up."""
    n = 120
    st = stage("gp_3", n, castle="start", bucket="down", board="split", lounge=False)
    H = (-1.9, 1.05)
    sol = build_sol2((H[0], H[1], 0), -28)
    cam = build_cam(24)
    TL = [(0.0, "thinking"), (0.8, "idea"), (2.7, "normal")]
    POPS = (("towers", 1.3), ("walls", 1.7), ("moat", 2.1), ("flag", 2.5))

    def state(t, f):
        k = smooth(t, 0.0, 0.5)
        cam(lerp3((-2.4, -2.5, 1.7), (-2.55, -1.8, 0.45), k), lerp3((-2.62, 1.4, 1.1), (-2.62, 1.4, 0.7), k))
        g = 1 - smooth(t, 1.24, 1.34)                  # the drawing gives way to the cards
        st["cards"]["drawing"].scale = (1.3 * g, 0.92 * g, 1)
        for name, t0 in POPS:
            s = pop(t, t0)
            st["cards"][name].scale = (0.66 * s, 0.432 * s, 1)
        tap = bump(t, 1.12, 1.6)
        up = smooth(t, 3.1, 3.45)
        act(sol, t, f, TL, blinks=(3.0,), look=(-0.85 * (1 - up), 0.55 + 0.25 * up),
            loc=(H[0] - 0.12 * tap, H[1], hop(t, 1.15, 1.48, 0.16)),
            yaw=-28 + 20 * up, lean=-7 * tap, pitch=7 + 3 * up,
            squash=idle(t) + 0.08 * bump(t, 1.0, 1.18) + 0.05 * wobble(t, 1.48, decay=5),
            arm_l=(-40 + 95 * tap, 0), arm_r=(-40 + 20 * tap, 0))
    return animate(n, state)


# ================================================================ clip 4: tip 2, one name each
def sign(tag, art, x, y, key):
    """A name sign: a blank pastel card on a stick. It drops into the sand; the words are laid on in the edit."""
    r = empty("RIG_sign_" + tag, (x, y, 5))
    cone("PRP_sign_stick_" + tag, "wood_d", (0, 0.02, 0), 0.028, 0.028, 0.8, parent=r)
    box("PRP_sign_card_" + tag, key, (0, 0, 0.84), (0.66, 0.035, 0.4), parent=r)
    overlay_plane("sign_" + tag, art, (0, -0.025, 0.84), (0.62, 0.36), parent=r)
    track(r, "location", "rotation_euler")
    return r


def drop(o, t, t0, x, y, d=0.26):
    """Falls in from above, lands at t0 and rocks once."""
    k = smooth(t, t0 - d, t0)
    o.location = (x, y, 3.2 * (1 - k) ** 1.6 if t < t0 else 0.0)
    o.rotation_euler = (0, D(7 * wobble(t, t0, freq=15, decay=6)), 0)


def clip4():
    """Narrator: "Second, put one name on each piece." [0.45-2.85].
    Version 3 (2026-11-27). The camera slides from Sleepy Sol to Hat Sol and stops; only those two are in this shot
    (the long slide past all four fell apart in two paints, and Ring Sol and our Sol get their signs in clip 4b).
    A name sign drops into the sand beside each of them (0.6 and 1.7; the words are laid on in the edit).
    Sleepy Sol sleeps straight through it. Hat Sol turns round from the sea (1.8-2.15) and tilts, a question mark
    over him (2.2).
    Version 4: 3.8 s long (the Eleven v4 "Second, ..." take is 3.3 s), and the words are ON the two signs in the skeleton
    (render with SHOWOVL=sign_moat,sign_walls). Elaine on cut v9, of words laid on afterwards that slid off the card while
    the camera moved: "the letters are still fucked up"."""
    n = 114
    stage("gp_4", n, castle=None, board="cards")
    hat = mate("hat", LOUNGE["hat"], 172)
    sleepy = mate("sleepy", LOUNGE["sleepy"], -14)
    SG = [("moat", "sign_moat.png", 5.72, 0.62, "cardC", 0.6), ("walls", "sign_walls.png", 4.22, 0.72, "cardB", 1.7)]
    signs = [(sign(tag, art, x, y, key), x, y, t0) for tag, art, x, y, key, t0 in SG]
    cam = build_cam(24)

    def state(t, f):
        x = lerp(6.15, 4.85, smooth(t, 0.25, 2.4))
        cam((x, -2.95, 0.85), (x, 1.0, 0.6))
        for o, sx, sy, t0 in signs:
            drop(o, t, t0, sx, sy)
        act(sleepy, t, f, [(0.0, "asleep")], loc=LOUNGE["sleepy"], yaw=-14, lean=-9, pitch=-5,
            squash=0.03 + 0.035 * math.sin(TAU * 0.45 * t))
        turn = smooth(t, 1.8, 2.15)
        tilt = smooth(t, 2.2, 2.5)
        act(hat, t, f, [(0.0, "normal")], marks=("question",) if t >= 2.2 else None, look=(-0.8 * turn, 0.1), loc=LOUNGE["hat"],
            yaw=lerp(172, -22, turn), lean=-13 * tilt, squash=idle(t + 1) + 0.06 * bump(t, 2.15, 2.45))
    return animate(n, state)


def clip4b():
    """No narration (the line ends in clip 4). The second half of tip 2, as a shot of its own: paint v1 and v2 of the long
    slide both fell apart once Ring Sol and our Sol came into frame (a fifth Sol, two Ring Sols, pupils, an open laughing
    face), so clip 4 is used up to 2.8 s (Sleepy Sol and Hat Sol) and these two get a simple locked-off two-shot.
    Low angle, a slow push. Our Sol on the left, Ring Sol on the right, rocking with his eyes shut. A name sign drops
    beside Ring Sol (0.35): he jolts with a hop, eyes open, an exclamation mark, and does a double take at it. A sign
    drops beside our Sol (1.4, "Flag: Me"): he glances at it and at 1.7 puffs up tall, SMUG. Hold to 3.0."""
    n = 90
    stage("gp_4b", n, castle="start", board="cards", lounge=False)
    SP_, RP = (2.3, 0.7), (3.5, 1.0)
    sol = build_sol2((SP_[0], SP_[1], 0), 0)
    ring = mate("ring", (RP[0], RP[1], 0), 10)
    s_ring = sign("towers", "sign_towers.png", 2.92, 0.5, "cardA")
    # Version 3 (2026-11-27): the words are ON the two signs in the skeleton (SHOWOVL=sign_towers,sign_flag) and painted
    # with them (Elaine: "the judging text glitches and also the Me task text"). The Flag card stands nearer our Sol and
    # the camera sits a little to the left, so the whole card is inside the square; and our Sol's smug face has no star
    # here, because the star sat on the T of "Towers".
    s_me = sign("flag", "sign_flag.png", 1.62, 0.35, "cardD")
    cam = build_cam(24)

    def state(t, f):
        k = smooth(t, 0.0, 3.0)
        cam(lerp3((2.5, -3.1, 0.9), (2.5, -2.85, 0.9), k), (2.5, 0.8, 0.5))
        drop(s_ring, t, 0.35, 2.92, 0.5)
        drop(s_me, t, 1.4, 1.62, 0.35)
        jolt = smooth(t, 0.37, 0.45)
        take = jolt * (-32 + 52 * smooth(t, 0.66, 0.78) - 56 * smooth(t, 0.92, 1.04))        # at the sign, away, back at it
        bob = math.sin(TAU * 0.9 * t) * (1 - jolt)
        act(ring, t, f, [(0.0, "content"), (0.4, "normal")], marks=("exclaim",) if 0.4 <= t < 1.25 else None,
            look=(-0.9 * jolt * (1 - smooth(t, 0.66, 0.78) + smooth(t, 0.92, 1.04)), 0.0),
            loc=(RP[0] + 0.1 * jolt, RP[1], hop(t, 0.39, 0.65, 0.12)),
            yaw=10 + take, lean=7 * bob + 5 * jolt, squash=0.035 * math.sin(TAU * 1.8 * t) * (1 - jolt) + 0.04 * wobble(t, 0.65, decay=5),
            arm_l=(-40 + 12 * bob + 60 * jolt * (1 - smooth(t, 1.05, 1.4)), 0), arm_r=(-40 - 12 * bob + 60 * jolt * (1 - smooth(t, 1.05, 1.4)), 0))
        see = smooth(t, 1.38, 1.55)
        smug = smooth(t, 1.68, 1.9)
        act(sol, t, f, [(0.0, "normal"), (1.72, "smug")], marks=(), blinks=(0.9,), look=(0.5 * (1 - see) * smooth(t, 0.4, 0.6) - 0.9 * see * (1 - smug), 0.1),
            loc=(SP_[0], SP_[1], 0), yaw=-22 * see * (1 - 0.6 * smug), pitch=9 * smug, lean=-3 * smug,
            squash=idle(t) - 0.07 * smug, arm_l=(-40 + 22 * smug, 0), arm_r=(-40 + 22 * smug, 0))
    return animate(n, state)


# ================================================================ clip 5: tip 3, the early deadline
def clip5():
    """Narrator: "Third, set a deadline before the real deadline." [0.9-4.6] ("before" at 2.58).
    A tilted low angle looking up at the contest clock on its post; the board under it says JUDGING 6:00 (laid on in
    the edit). Sol stands at the foot of the post, looking up at it. Far behind: the other team's tall castle.
    At 0.5 the clock's hand jumps forward and the clock shudders: Sol flinches back with a hop, nubs up, eyes O O.
    Normal at 1.5. At 2.3 he hops, and a second board drops onto the post under the first (lands 2.75). At 3.5 he
    stretches up, pleased with himself (plain eyes, no smug face), and at 4.2 looks up."""
    n = 150
    st = stage("gp_5", n, castle="start", bucket="down", board="cards", lounge=False, rival=True, clock="drop")
    clock, hand, b2 = st["clock"]
    H = (CLOCK[0] + 1.35, CLOCK[1] - 0.45)
    sol = build_sol2((H[0], H[1], 0), -24)
    cam = build_cam(24)
    # Elaine on cut v5 (2026-11-27), of the half-shut smug eyes at the end: "why is he doing this can we just keep it
    # like this" (the plain eyes). So no smug face: he stands tall, pleased, with his ordinary eyes.
    TL = [(0.0, "normal"), (0.55, "surprised"), (1.5, "normal")]

    def state(t, f):
        rival_at(st["rival"], t, f)
        k = smooth(t, 0.0, 5.0)
        cam(lerp3((CLOCK[0] + 0.8, CLOCK[1] - 5.5, 0.5), (CLOCK[0] + 0.75, CLOCK[1] - 5.15, 0.52), k), (CLOCK[0] + 0.45, CLOCK[1], 1.0), roll=6)
        tick = smooth(t, 0.48, 0.54)
        hand.rotation_euler = (0, D(-58 + 30 * tick + 9 * wobble(t, 0.54, freq=22, decay=8)), 0)
        clock.rotation_euler = (0, D(1.6 * wobble(t, 0.5, freq=24, decay=6)), 0)
        kd = smooth(t, 2.45, 2.75)
        b2.location = (0, -0.05, 0.84 + 3.0 * (1 - kd) ** 1.6 if t < 2.75 else 0.84)
        b2.rotation_euler = (0, D(4 * wobble(t, 2.75, freq=16, decay=6)), 0)
        fl = smooth(t, 0.52, 0.62) * (1 - smooth(t, 1.35, 1.7))
        smug = smooth(t, 3.45, 3.7)
        up = smooth(t, 4.2, 4.5)
        act(sol, t, f, TL, blinks=(2.0,), look=(-0.7 * (1 - smug), 0.85 - 0.5 * smug + 0.4 * up),
            loc=(H[0] + 0.14 * fl, H[1] - 0.05 * fl, hop(t, 0.54, 0.8, 0.14) + hop(t, 2.3, 2.62, 0.2)),
            yaw=-24 + 18 * smug, lean=6 * fl - 3 * smug, pitch=13 - 4 * smug + 4 * up,
            squash=idle(t) + 0.08 * bump(t, 2.14, 2.32) + 0.05 * wobble(t, 2.62, decay=5) - 0.07 * smug,
            arm_l=(-40 + 85 * fl + 22 * smug, 0), arm_r=(-40 + 85 * fl + 22 * smug, 0))
    return animate(n, state)


# ================================================================ clip 6: tip 4, one doc
def clip6():
    """Narrator: "Fourth, keep everything in one doc the whole team can see." [0.5-3.6] ("the whole team" 2.34-2.94).
    Opens tight on the page pinned to the plan board: the team doc (laid on in the edit). The camera pulls back and
    up (0.5-1.7) to a high wide shot: our Sol under the board, and the others hop into the frame from the right one at
    a time: Ring Sol (1.3-1.8), Hat Sol (1.8-2.3), Sleepy Sol, hopping in his sleep (2.3-2.8). He wakes with a jolt at
    3.1 (eyes open, an exclamation mark). All four stand turned toward the board, looking up at the page."""
    n = 132
    # Paint v4 redrew the half-built castle in a new place at 3.8 s (and paint v5 of clip 7 did the same kind of thing: Elaine,
    # "sand appears in somehow"). The castle and bucket stood half hidden behind the row of Sols, so this shot is on open
    # sand too: the board, the clock, the four Sols and nothing else.
    stage("gp_6", n, castle=None, board="table", lounge=False)
    H = (-2.05, 0.95)
    END = {"ring": (-1.3, 0.35), "hat": (-0.5, 0.5), "sleepy": (0.3, 0.15)}
    IN = {"ring": (1.3, 1.8), "hat": (1.8, 2.3), "sleepy": (2.3, 2.8)}
    sol = build_sol2((H[0], H[1], 0), -30)
    ring, hat, sleepy = mate("ring", (5, 0, 0), -45), mate("hat", (6, 0, 0), -45), mate("sleepy", (7, 0, 0), -45)
    cam = build_cam(24)

    def state(t, f):
        k = smooth(t, 0.5, 1.7)
        cam(lerp3((-2.85, -0.45, 1.36), (-1.5, -4.75, 1.6), k), lerp3((-3.0, 1.6, 1.3), (-1.52, 1.0, 0.45), k))
        act(sol, t, f, [(0.0, "normal"), (3.6, "happy")], blinks=(1.2,), look=(-0.8, 0.8), loc=(H[0], H[1], 0), yaw=-30,
            pitch=10, squash=idle(t), arm_l=(-40 + 40 * bump(t, 3.6, 4.2), 0), arm_r=(-40 + 40 * bump(t, 3.6, 4.2), 0))
        for who, s, tl in ((ring, "ring", [(0.0, "normal")]), (hat, "hat", [(0.0, "normal")]),
                           (sleepy, "sleepy", [(0.0, "asleep"), (3.1, "normal")])):
            t0, t1 = IN[s]
            e = END[s]
            p = hops(t, t0, t1, (e[0] + 3.4, e[1] - 0.25), e, n=3, h=0.15)
            land = wobble(t, t1, decay=5)
            wake = smooth(t, 3.08, 3.2) if s == "sleepy" else 1.0
            jolt = bump(t, 3.08, 3.5) if s == "sleepy" else 0.0
            act(who, t, f, tl, look=(-0.8 * wake, 0.8 * wake), loc=(p[0], p[1], p[2] + 0.12 * jolt),
                marks=("exclaim",) if s == "sleepy" and 3.1 <= t < 4.0 else None, blinks=(t1 + 0.5,),
                yaw=-42, lean=-8 * (1 - wake), pitch=10 * wake - 5 * (1 - wake),
                squash=idle(t + t0) + 0.05 * land, arm_l=(-40 + 70 * jolt, 0), arm_r=(-40 + 70 * jolt, 0))
    return animate(n, state)


def hash_marks(tag, side):
    """Three short curved motion lines beside a flapping nub, like ))) : a rig of their own, in 3D, so the painter copies
    them and does not make up his own. (Elaine, 2026-11-27, of the painter's smudged version: "can we try to rig this
    in 3d instead? like make the hash marks vibrate and the arms move rly fast".) side = -1 for screen left, +1 for
    screen right. They stand upright facing the camera; hash_at() shows, places and shakes them."""
    r = empty("RIG_hash_" + tag, (0, 0, -5))
    for i, R in enumerate((0.11, 0.185, 0.26)):
        bm = bmesh.new()
        half, w, d, N = math.radians(34 - 4 * i), 0.032, 0.02, 10
        rings = []
        for k in range(N + 1):
            ang = (0.0 if side > 0 else math.pi) - half + 2 * half * k / N
            taper = 0.35 + 0.65 * math.sin(math.pi * k / N)                # thin at both ends, like a brush stroke
            ring = [bm.verts.new(((R + sr * w * taper / 2) * math.cos(ang), sy * d / 2, (R + sr * w * taper / 2) * math.sin(ang)))
                    for sr, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            rings.append(ring)
        for k in range(N):
            for j in range(4):
                bm.faces.new((rings[k][j], rings[k][(j + 1) % 4], rings[k + 1][(j + 1) % 4], rings[k + 1][j]))
        bm.faces.new(rings[0])
        bm.faces.new(rings[-1])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        o = mesh_obj(f"FX_hash_{tag}_{i}", bm, (0.62, 0.33, 0.16), parent=r, smooth=False)
        o.visible_shadow = False
    track(r, "location", "rotation_euler", "scale")
    return r


def hash_at(r, t, on, at, phase=0.0):
    """on: 0 hidden .. 1 full size. at: the nub's place (x, y, z). They shake fast: a quick tilt to and fro, a pulse."""
    if on <= 0.01:
        r.location, r.scale = (at[0], at[1], -5), (0, 0, 0)
        return
    q = math.sin(TAU * 8.0 * t + phase)                        # 8 shakes a second: three frames each at 24 fps
    r.location = (at[0], at[1], at[2] + 0.018 * q)
    r.rotation_euler = (0, D(13 * q), 0)
    k = on * (1.0 + 0.14 * math.sin(TAU * 4.0 * t + phase))
    r.scale = (k, k, k)


# ================================================================ clip 7: tip 5, ask one person
def clip7():
    """Narrator: "And fifth, [0.5] ask one specific person, [1.5-3.3] instead of saying, [3.7-4.6] can someone." [4.9-5.7].
    Version 6 (2026-11-27). Elaine on cut v5: "sand appears in somehow": the castle's heap of sand came and went behind
    them and the bucket popped in beside Ring Sol. So this shot is on OPEN SAND, with no castle, heap, bucket or shovel
    in it, and Ring Sol no longer walks to the back to pat sand: he is asked, nods, and hops out of the picture to get
    to work. Nothing is left in the frame that could appear or vanish.
    Ring Sol stands at the LEFT, our Sol in the middle, Hat Sol and Sleepy Sol in a row at the right.
    A high three-quarter angle on all four (0-1.2); the camera drops to eye level beside Ring Sol and our Sol (1.2-1.9).
    Sol hops up to Ring Sol (1.35-1.85) and holds one nub up at him. Ring Sol jolts (2.2, an exclamation mark), nods
    (3.0-3.4), turns and hops away to the left, out of the frame (3.45-4.3). The camera slides right (3.5-4.3) to our
    Sol, Hat Sol and Sleepy Sol. Sol turns round to the two of them (3.5-3.9) and flaps both nubs (4.2-4.8). At 4.85
    both turn away, tip their faces up and whistle (music notes). Sol just stands there with a sweat drop (5.3).
    Version 8: while he flaps, his nubs go really fast (six flaps a second) and three curved hash marks shake beside
    each nub; the marks are their own 3D rig (hash_marks), not left to the painter."""
    n = 204
    stage("gp_7", n, castle=None, board=None, lounge=False)
    S0, S1 = (0.9, -0.2), (0.6, -0.15)          # a clear gap of sand to Ring Sol: paint v1 lost our Sol when they touched
    R0, R1 = (-0.6, -0.05), (-3.6, 0.5)
    HP, SP = (2.5, 0.15), (3.3, -0.1)
    sol = build_sol2((S0[0], S0[1], 0), -40)
    ring, hat, sleepy = mate("ring", (R0[0], R0[1], 0), 40), mate("hat", (HP[0], HP[1], 0), -40), mate("sleepy", (SP[0], SP[1], 0), -40)
    hl, hr = hash_marks("L", -1), hash_marks("R", 1)
    cam = build_cam(24)

    def state(t, f):
        d1, d2 = smooth(t, 1.2, 1.9), smooth(t, 3.5, 4.3)
        cam(lerp3(lerp3((1.35, -5.6, 2.5), (0.0, -3.3, 0.9), d1), (1.95, -4.5, 0.92), d2),
            lerp3(lerp3((1.35, 0.1, 0.35), (0.0, -0.1, 0.45), d1), (1.95, 0.05, 0.45), d2))
        p = hops(t, 1.35, 1.85, S0, S1, n=1, h=0.2)
        ask = smooth(t, 1.9, 2.1) * (1 - smooth(t, 3.0, 3.3))
        to2 = smooth(t, 3.5, 3.9)
        wave = smooth(t, 4.15, 4.3) * (1 - smooth(t, 4.8, 5.0))
        flap = math.sin(TAU * 6.0 * t)                    # really fast: a full flap every four frames
        oh = smooth(t, 5.25, 5.5)
        hash_at(hl, t, wave, (p[0] - 0.43, p[1] - 0.12, 0.47))
        hash_at(hr, t, wave, (p[0] + 0.43, p[1] - 0.12, 0.47), phase=2.1)
        act(sol, t, f, [(0.0, "normal"), (5.3, "nervous")], blinks=(0.7, 3.2), look=(lerp(-0.85, 0.85, to2) - 0.5 * oh, 0.05),
            loc=p, yaw=lerp(-40, 44, to2) - 18 * oh, lean=-6 * ask + 4 * wave * flap,
            squash=idle(t) + 0.06 * bump(t, 1.2, 1.38) + 0.05 * wobble(t, 1.85, decay=5) + 0.04 * oh + 0.05 * bump(t, 3.5, 3.9),
            arm_l=(-40 + 95 * ask + wave * (62 - 58 * flap), 0), arm_r=(-40 + wave * (62 + 58 * flap), 0))
        jolt = smooth(t, 2.17, 2.25) * (1 - smooth(t, 2.8, 3.0))
        nod = bump(t, 3.0, 3.4)
        q = hops(t, 3.45, 4.3, R0, R1, n=4, h=0.18)
        go = smooth(t, 3.4, 3.65)
        act(ring, t, f, [(0.0, "normal")], look=(0.85 * (1 - go) - 0.6 * go, 0.0), blinks=(1.0,),
            marks=("exclaim",) if 2.2 <= t < 2.9 else None,       # startled without ring eyes: the painter gave those pupils
            loc=(q[0] - 0.1 * jolt, q[1], q[2] + hop(t, 2.2, 2.45, 0.12)), yaw=lerp(40, -80, go), lean=-4 * jolt,
            pitch=4 * jolt + 20 * nod, squash=idle(t + 2) + 0.06 * nod,
            arm_l=(-40 + 60 * jolt, 0), arm_r=(-40 + 60 * jolt, 0))
        away = smooth(t, 4.82, 5.1)
        sway = math.sin(TAU * 0.8 * t) * away
        for who, pos, base, tl, ph in ((hat, HP, -40, [(0.0, "normal"), (4.85, "singing")], 0.0),
                                       (sleepy, SP, -46, [(0.0, "sleepy"), (4.85, "singing")], 1.3)):
            act(who, t, f, tl, blinks=(1.6 + ph,), look=(-0.8 * (1 - away) + 0.5 * away, 0.6 * away),
                loc=(pos[0], pos[1], 0), yaw=lerp(base, 62, away), lean=5 * sway, pitch=11 * away,
                squash=idle(t + ph) + 0.03 * away * math.sin(TAU * 1.6 * t + ph))
    return animate(n, state)


# ================================================================ clip 8: the payoff
def clip8():
    """Narrator: "Ignite's free Social Impact and Project Development course teaches you how to take an idea and
    actually make it happen." [0.9-9.0].
    Opens close on the flag on top of the finished castle; a blue rosette ribbon drops in and sticks on the front of
    the middle tower (0.45). The camera cranes back and down (0.55-1.9) to a wide shot: our Sol front left, Ring Sol
    behind him, the castle in the middle, Hat Sol and Sleepy Sol on the right. (The end card slides in over the right
    60% at 1.6 in the edit and covers the right-hand two.)
    Sol hops as the ribbon lands, SPARKLE eyes on the castle. At 1.3 he turns to the camera, looks UP and listens,
    with a small idle, to the end of the line (a glance at the card, 1.9-2.7). He nods (9.3-9.8). Then (9.9) he SMIRKS:
    the smug face with one star, standing tall. The other three cheer, nubs up, with flowers round them. Hold."""
    n = 348
    st = stage("gp_8", n, castle="done", bucket="up", board=None, lounge=False)
    SP_, RP, HP, ZP = (-0.6, -0.1), (-1.5, 0.55), (2.4, 0.25), (1.62, 1.85)
    sol = build_sol2((SP_[0], SP_[1], 0), 34)
    akimbo(sol)
    ring, hat, sleepy = mate("ring", (RP[0], RP[1], 0), 30), mate("hat", (HP[0], HP[1], 0), -30), mate("sleepy", (ZP[0], ZP[1], 0), -14)
    rb = empty("RIG_ribbon", (0, 0, 5))
    cone("PRP_ribbon", "blue", (0, 0, 0), 0.19, 0.19, 0.03, parent=rb, rot=(D(90), 0, 0))
    cone("PRP_ribbon_middle", "cream", (0, -0.03, 0), 0.115, 0.115, 0.012, parent=rb, rot=(D(90), 0, 0))
    for s in (-1, 1):
        box(f"PRP_ribbon_tail{s}", "blue", (s * 0.07, -0.01, -0.25), (0.085, 0.02, 0.26), parent=rb, rot=(0, D(s * 14), 0))
    # Elaine, 2026-11-27: "same with this please just put the text in blender". The "1st" is part of the skeleton clip the
    # painter gets (render with SHOWOVL=first); nothing is laid over the ribbon in the edit any more.
    overlay_plane("first", "first.png", (0, -0.05, 0), (0.17, 0.17), parent=rb)
    track(rb, "location", "rotation_euler")
    RX, RY, RZ = CAS[0], CAS[1] + 0.28 - 0.42, 0.62
    cam = build_cam(24)
    # Elaine on cut v9, of flowers and sparkles round both: "i meant just the floaty has the flowers and i think the sol in
    # front does the smirk animation". So on the last beat Ring Sol (and the two behind the end card) cheer with flowers,
    # and OUR Sol smirks: the smug face (half-moon eyes, one twinkling star), standing tall, nubs only a little raised.
    # Elaine on cut v10: "theres a weird cut with the medal ... it zooms out and then it snaps": the pull-back took 1.35 s and
    # the painter fell behind it and dissolved to the wide view. It now takes 2 s (0.7 to 2.7), so everything after it is
    # 0.6 s later and the clip is 11.6 s. And of our Sol's raised nubs on the smirk: "can we do another hands on hips
    # smirk confident looking": he ends with the < > arms on his sides.
    TL = [(0.0, "sparkle"), (2.1, "normal"), (10.5, "smug")]

    def state(t, f):
        k = smooth(t, 0.7, 2.7)
        # the wide view is far enough back that Ring Sol and our Sol stand side by side, whole, left of the end card
        cam(lerp3((0.5, -1.35, 1.58), (0.39, -5.7, 1.0), k), lerp3((0.5, 1.45, 1.28), (0.39, 0.5, 0.66), k))
        kd = smooth(t, 0.2, 0.45)
        rb.location = (RX, RY, RZ + 2.2 * (1 - kd) ** 1.6 if t < 0.45 else RZ)
        rb.rotation_euler = (0, D(9 * wobble(t, 0.45, freq=15, decay=6)), 0)
        front = smooth(t, 2.0, 2.4)
        card = bump(t, 2.9, 3.6)
        nod = bump(t, 9.9, 10.4)
        yay = smooth(t, 10.48, 10.6)
        bounce = bump(t, 10.5, 10.85) - 0.6 * bump(t, 10.8, 11.1)
        # Elaine on cut v12: "can we bring back the old hands on hips thing like the first one u did before". The first one was
        # his own straight nubs tucked down against his sides (clip 2, skeleton v5), which the painter drew as hands on hips.
        # The built akimbo() arms are not used; the same tucked nubs are used here on the smirk.
        akimbo_at(sol, 0.0)
        # Elaine on cut v7, of the last frames: "noooooooouuu wheres the flowers and the sparkles". The cheer has flowers AND
        # sparkles floating round every Sol, our Sol included.
        act(sol, t, f, TL, blinks=(4.0, 6.5, 8.6), look=(0.9 * (1 - front) + 0.8 * card, lerp(0.4, 0.85, front) - 0.5 * card - 0.5 * nod),
            loc=(SP_[0], SP_[1], hop(t, 0.46, 0.8, 0.2)), yaw=34 * (1 - front) + 14 * card, lean=1.5 * math.sin(t * 2.0) * (1 - nod),
            pitch=lerp(4, 10, front) - 22 * nod + 5 * yay,
            squash=idle(t) + 0.05 * wobble(t, 0.8, decay=5) + 0.06 * nod + 0.05 * bounce - 0.07 * yay,
            # In this wide view he is small: nubs swung forward (26) vanish against his body and the painter then invents a raised
            # nub. So here they hang straight DOWN along his sides (-72, a little forward), where both show in his outline.
            arm_l=(-40 + 60 * bump(t, 0.4, 1.0) - 32 * yay, 7 * yay), arm_r=(-40 + 60 * bump(t, 0.4, 1.0) - 32 * yay, 7 * yay))
        for i, (who, pos, base) in enumerate(((ring, RP, 30), (hat, HP, -30), (sleepy, ZP, -14))):
            ph = 0.07 * (i + 1)
            b2 = bump(t, 10.5 + ph, 10.85 + ph) - 0.6 * bump(t, 10.8 + ph, 11.1 + ph)
            y2 = smooth(t, 10.48 + ph, 10.6 + ph)
            f2 = smooth(t, 2.1 + ph, 2.5 + ph)
            act(who, t, f, [(0.0, "happy"), (2.3 + ph, "normal"), (10.5 + ph, "joy")], blinks=(4.7 + i, 7.2 + 0.4 * i),
                look=(0.0, 0.8 * f2), loc=(pos[0], pos[1], hop(t, 0.5 + ph, 0.82 + ph, 0.16)), yaw=base * (1 - 0.6 * f2),
                pitch=9 * f2 + 4 * y2, squash=idle(t + i) + 0.05 * wobble(t, 0.82 + ph, decay=5) + 0.09 * b2,
                arm_l=(-40 + 55 * bump(t, 0.45, 1.1) + 85 * y2, 0), arm_r=(-40 + 55 * bump(t, 0.45, 1.1) + 85 * y2, 0))
    return animate(n, state)
