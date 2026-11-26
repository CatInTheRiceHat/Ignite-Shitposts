"""Shared gray-skeleton kit for the candle episode. exec() this inside Blender, then a clip script.

Everything is plain gray blockout: Higgsfield does the painting. Sol is a round gumdrop
(Elaine, 2026-11-25) with the mascot's close-set eyes, arm nubs and stubby feet.
All motion is keyed on twos (new state every 2 frames at 30 fps, constant interpolation).
"""
import bpy, bmesh, math

D = math.radians
FPS = 30
GRAY = {"body": 0.42, "orange": 0.60, "face": 0.82, "eye": 0.03, "limb": 0.36, "prop": 0.55,
        "desk": 0.30, "wall": 0.20, "pane": 0.10, "frame": 0.48, "flame": 0.96,
        "paper": 0.88, "dark": 0.14, "smoke": 0.74, "glass": 0.66}
S = {"sc": None, "keys": []}


def new_scene(name, nframes):
    old = bpy.data.scenes.get(name)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.scenes.remove(old)
    sc = bpy.data.scenes.new(name)
    bpy.context.window.scene = sc
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, nframes
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, 100
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading
    sh.light, sh.color_type, sh.show_shadows, sh.shadow_intensity, sh.show_cavity = 'STUDIO', 'OBJECT', True, 0.35, True
    sc.display.render_aa = '8'
    sc.view_settings.view_transform = 'Standard'
    S["sc"], S["keys"] = sc, []
    return sc


def link(o, parent=None):
    S["sc"].collection.objects.link(o)
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = 0.1
    o.location, o.rotation_euler = loc, rot
    return link(o, parent)


def mesh_obj(name, bm, key, loc=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), parent=None, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    o.location, o.scale, o.rotation_euler = loc, scale, rot
    v = GRAY[key]
    o.color = (v, v, v, 1)
    return link(o, parent)


def sphere(name, key, loc, scale, parent=None, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    return mesh_obj(name, bm, key, loc, scale, rot, parent)


def cone(name, key, loc, r1, r2, depth, parent=None, scale=(1, 1, 1), rot=(0, 0, 0), smooth=True):
    """Cone/cylinder with its BASE at the object origin, pointing +Z."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=r1, radius2=r2, depth=depth)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, depth / 2))
    return mesh_obj(name, bm, key, loc, scale, rot, parent, smooth)


def box(name, key, loc, size, parent=None, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    return mesh_obj(name, bm, key, loc, size, rot, parent, smooth=False)


# ---------------- Sol: round gumdrop ----------------
# Taller than wide, like the website mascots: egg body rising into ONE simple straight flame tip.
PROFILE = [(0.0, 0.055), (0.18, 0.055), (0.29, 0.085), (0.345, 0.16), (0.365, 0.27), (0.355, 0.38),
           (0.32, 0.49), (0.27, 0.59), (0.21, 0.69), (0.15, 0.78), (0.09, 0.87), (0.04, 0.95), (0.0, 1.0)]


def build_sol(loc, yaw):
    root = empty("RIG_Sol", loc, rot=(0, 0, yaw))
    body = empty("RIG_Sol_body", (0, 0, 0.06), parent=root)      # lean / pitch pivot above the feet
    bm = bmesh.new()
    seg, rings = 32, []
    for r, z in PROFILE:
        lean = 0.035 * max(0.0, (z - 0.55) / 0.45)                # tip sits a touch off-centre, no curl or twist
        if r == 0.0:
            rings.append([bm.verts.new((lean, 0, z - 0.06))])
        else:
            rings.append([bm.verts.new((math.cos(a) * r + lean, math.sin(a) * r * 0.86, z - 0.06))
                          for a in (2 * math.pi * i / seg for i in range(seg))])
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh_obj("HERO_Sol_body", bm, "body", parent=body)
    cone("HERO_Sol_lobe_L", "body", (-0.275, 0, 0.42), 0.085, 0.015, 0.17, parent=body, scale=(1, 0.8, 1), rot=(0, D(-20), 0))
    cone("HERO_Sol_lobe_R", "body", (0.285, 0, 0.40), 0.085, 0.015, 0.16, parent=body, scale=(1, 0.8, 1), rot=(0, D(20), 0))
    sphere("HERO_Sol_orange", "orange", (0, -0.245, 0.30), (0.27, 0.11, 0.30), parent=body)
    sphere("HERO_Sol_face", "face", (0, -0.275, 0.25), (0.20, 0.10, 0.215), parent=body)
    eyes = [sphere("HERO_Sol_eye_L", "eye", (-0.08, -0.366, 0.215), (0.033, 0.014, 0.056), parent=body),
            sphere("HERO_Sol_eye_R", "eye", (0.08, -0.366, 0.215), (0.033, 0.014, 0.056), parent=body)]
    arm_l = empty("RIG_Sol_arm_L", (-0.335, -0.06, 0.24), parent=body)
    arm_r = empty("RIG_Sol_arm_R", (0.335, -0.06, 0.24), parent=body)
    sphere("HERO_Sol_armnub_L", "limb", (-0.06, 0, 0), (0.09, 0.065, 0.065), parent=arm_l)
    sphere("HERO_Sol_armnub_R", "limb", (0.06, 0, 0), (0.09, 0.065, 0.065), parent=arm_r)
    sphere("HERO_Sol_foot_L", "limb", (-0.125, 0, 0.05), (0.052, 0.062, 0.06), parent=root)   # feet stay planted
    sphere("HERO_Sol_foot_R", "limb", (0.125, 0, 0.05), (0.052, 0.062, 0.06), parent=root)
    sol = {"root": root, "body": body, "eyes": eyes, "arm_l": arm_l, "arm_r": arm_r}
    track(root, "rotation_euler", "location")
    track(body, "rotation_euler", "scale")
    track(arm_l, "rotation_euler")
    track(arm_r, "rotation_euler")
    for e in eyes:
        track(e, "scale", "location")
    return sol


def pose_sol(sol, yaw=0.0, lean=0.0, pitch=0.0, squash=0.0, arm_l=(-50, 0), arm_r=(-50, 0), blink=False, gaze=0.0):
    """Angles in degrees. lean>0 tips toward his own right-hand side (+X). pitch>0 tilts back to look up,
    pitch<0 bows forward. arm = (raise above horizontal, swing forward). gaze = eye pair shift, -1..1."""
    sol["root"].rotation_euler = (0, 0, D(yaw))
    sol["body"].rotation_euler = (D(-pitch), D(lean), 0)
    sol["body"].scale = (1 + squash, 1 + squash, 1 - squash)
    sol["arm_l"].rotation_euler = (0, D(arm_l[0]), D(arm_l[1]))
    sol["arm_r"].rotation_euler = (0, D(-arm_r[0]), D(-arm_r[1]))
    for e, x in zip(sol["eyes"], (-0.08, 0.08)):
        e.scale = (0.033, 0.014, 0.056 * (0.08 if blink else 1.0))
        e.location = (x, -0.366, 0.215 + 0.03 * gaze)


# ---------------- desk set ----------------
def build_desk():
    box("ENV_desk", "desk", (0, -1.4, -0.1), (11, 7.0, 0.2))
    box("ENV_wall", "wall", (0, 2.2, 3.0), (11, 0.2, 9))
    box("ENV_window_pane", "pane", (1.6, 2.08, 2.5), (1.9, 0.05, 2.6))
    for nm, loc, size in [("L", (0.6, 2.04, 2.5), (0.12, 0.1, 2.84)), ("R", (2.6, 2.04, 2.5), (0.12, 0.1, 2.84)),
                          ("T", (1.6, 2.04, 3.86), (2.12, 0.1, 0.12)), ("B", (1.6, 2.0, 1.14), (2.3, 0.2, 0.14)),
                          ("V", (1.6, 2.04, 2.5), (0.07, 0.08, 2.6)), ("H", (1.6, 2.04, 2.65), (1.9, 0.08, 0.07))]:
        box("ENV_window_" + nm, "frame", loc, size)
    box("PRP_book_1", "prop", (-1.9, 1.2, 0.09), (1.0, 0.72, 0.18), rot=(0, 0, D(8)))
    box("PRP_book_2", "frame", (-1.93, 1.23, 0.25), (0.9, 0.64, 0.14), rot=(0, 0, D(-6)))
    cone("PRP_cup", "prop", (2.3, 1.2, 0), 0.2, 0.23, 0.5)
    for i, (dx, dy, tilt) in enumerate([(-0.06, 0.0, 9), (0.07, 0.03, -7), (0.0, -0.06, 3)]):
        cone(f"PRP_pencil_{i}", "frame", (2.3 + dx, 1.2 + dy, 0.3), 0.022, 0.022, 0.55, rot=(0, D(tilt), 0))


def build_candle(x=0.0, y=0.0, z=0.0, height=0.52):
    """Candle in a dish. Tips about the far (+X) edge of the dish; the flame follows the wick but stays upright."""
    px = 0.22
    piv = empty("RIG_candle_pivot", (x + px, y, z))
    cone("PRP_dish", "prop", (-px, 0, 0), 0.21, 0.24, 0.05, parent=piv)
    cone("PRP_candle", "paper", (-px, 0, 0.05), 0.11, 0.11, height, parent=piv)
    cone("PRP_wick", "dark", (-px, 0, 0.05 + height), 0.008, 0.008, 0.05, parent=piv)
    tip = empty("RIG_wick_tip", (-px, 0, 0.09 + height), parent=piv)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=1.0)
    ball = [(v.co.x, v.co.y, v.co.z + 1.0) for v in bm.verts]
    for v in bm.verts:
        if v.co.z > 0:
            k = (1 - v.co.z) ** 0.6
            v.co.x *= k
            v.co.y *= k
            v.co.z *= 2.4
        v.co.z += 1.0
    flame = mesh_obj("PRP_flame", bm, "flame", (x, y, z + 0.09 + height), (0.075, 0.075, 0.075))
    flame.shape_key_add(name="teardrop")
    kb = flame.shape_key_add(name="ball")
    for i, co in enumerate(ball):
        kb.data[i].co = co
    kb.value = 0.0
    c = flame.constraints.new('COPY_LOCATION')
    c.target = tip
    track(piv, "rotation_euler")
    track(flame, "scale")
    track(kb, "value")
    return {"piv": piv, "flame": flame, "ball": kb}


FLICK = [1.0, 1.06, 0.97, 1.09, 1.02, 0.94, 1.05, 0.99, 1.08, 0.96, 1.03, 1.0]


def pose_flame(candle, f, stretch=1.0, amount=1.0):
    fl = 1.0 + (FLICK[(f // 3) % len(FLICK)] - 1.0) * amount
    candle["flame"].scale = (0.075 / math.sqrt(fl * stretch), 0.075 / math.sqrt(fl * stretch), 0.075 * fl * stretch)


def build_spiral(parent=None, top=(0, 0, 2.0), drop=0.75, name="PRP_spiral"):
    """Paper spiral hanging from `top` on a short thread; returns the spin empty."""
    spin = empty("RIG_spiral_spin", top, parent=parent)
    bm = bmesh.new()
    turns, steps, prev = 3.0, 96, None
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        r = 0.05 + 0.25 * t
        z = -0.12 - drop * t
        vi = bm.verts.new((math.cos(a) * (r - 0.045), math.sin(a) * (r - 0.045), z + 0.02))
        vo = bm.verts.new((math.cos(a) * (r + 0.045), math.sin(a) * (r + 0.045), z - 0.02))
        if prev:
            bm.faces.new((prev[0], prev[1], vo, vi))
        prev = (vi, vo)
    sp = mesh_obj(name, bm, "paper", parent=spin)
    sp.modifiers.new("solid", 'SOLIDIFY').thickness = 0.012
    cone(name + "_thread", "paper", (0, 0, -0.12), 0.006, 0.006, 0.12, parent=spin)
    track(spin, "rotation_euler")
    return spin


def build_stand(x, dx=0.55, dy=0.55):
    """Wire stand whose pole stands right of and behind the candle; the arm reaches diagonally so the
    spiral hangs over (x, 0), clear of the pole. `x` is where the spiral hangs."""
    root = empty("RIG_stand", (x + dx, dy, 0))
    cone("PRP_stand_base", "prop", (0, 0, 0), 0.17, 0.15, 0.05, parent=root)
    cone("PRP_stand_pole", "prop", (0, 0, 0.05), 0.022, 0.022, 2.1, parent=root)
    length = math.hypot(dx, dy)
    cone("PRP_stand_arm", "prop", (0, 0, 2.13), 0.018, 0.018, length, parent=root,
         rot=(D(90), 0, math.atan2(dy, dx) - math.pi / 2 + math.pi))
    spin = build_spiral(parent=root, top=(-dx, -dy, 2.13))
    track(root, "location")
    return {"root": root, "spin": spin, "dx": dx, "dy": dy}


def build_camera(lens=50):
    cd = bpy.data.cameras.new("CAM")
    cd.lens = lens
    cam = link(bpy.data.objects.new("CAM", cd))
    tgt = empty("RIG_cam_target")
    c = cam.constraints.new('TRACK_TO')
    c.target, c.track_axis, c.up_axis = tgt, 'TRACK_NEGATIVE_Z', 'UP_Y'
    S["sc"].camera = cam
    track(cam, "location")
    track(tgt, "location")
    return cam, tgt


# ---------------- timing helpers ----------------
def smooth(t, a, b):
    x = min(1.0, max(0.0, (t - a) / (b - a)))
    return x * x * x * (x * (x * 6 - 15) + 10)


def bump(t, a, b):
    """0 -> 1 -> 0 between a and b."""
    if t <= a or t >= b:
        return 0.0
    return math.sin((t - a) / (b - a) * math.pi) ** 2


def wobble(t, start, amp=1.0, freq=11.0, decay=3.2):
    return amp * math.exp(-decay * (t - start)) * math.sin((t - start) * freq) if t > start else 0.0


def lerp(a, b, k):
    return a + (b - a) * k


def lerp3(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def track(o, *paths):
    for p in paths:
        S["keys"].append((o, p))


def animate(nframes, state):
    """Call state(t, f) on EVERY frame and key everything tracked (smooth; Elaine dropped on-twos 2026-11-25)."""
    sc = S["sc"]
    for f in range(1, nframes + 1):
        state((f - 1) / FPS, f)
        for o, p in S["keys"]:
            o.keyframe_insert(p, frame=f)
    ads = []
    for o in sc.objects:
        ads.append(o.animation_data)
        sk = getattr(o.data, "shape_keys", None) if o.data else None
        if sk:
            ads.append(sk.animation_data)
    for ad in ads:
        if not ad or not ad.action:
            continue
        act, fcs = ad.action, []
        if hasattr(act, "layers"):
            for layer in act.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        fcs.extend(cb.fcurves)
        else:
            fcs = list(act.fcurves)
        for fc in fcs:
            for kp in fc.keyframe_points:
                kp.interpolation = 'LINEAR'
            fc.update()
    sc.frame_set(1)
    return {"scene": sc.name, "objects": len(sc.objects), "frames": nframes}
