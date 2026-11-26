"""Clip 01 gray skeleton: Sol tips the candle, flame stays up. Run inside Blender.

Builds its own scene "candle_01" (rebuilt from scratch each run; other scenes untouched).
30 fps, 120 frames, every pose and camera position keyed on twos with constant interpolation.
"""
import bpy, bmesh, math
from mathutils import Vector

SCENE = "candle_01"
FPS, NFRAMES = 30, 120
D = math.radians

# ---------- scene (idempotent) ----------
old = bpy.data.scenes.get(SCENE)
if old:
    for o in list(old.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.scenes.remove(old)
sc = bpy.data.scenes.new(SCENE)
bpy.context.window.scene = sc
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, NFRAMES
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = 100
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'
sh.color_type = 'OBJECT'
sh.show_shadows = True
sh.shadow_intensity = 0.35
sh.show_cavity = True
sc.display.render_aa = '8'
sc.view_settings.view_transform = 'Standard'

GRAY = {"body": 0.42, "face": 0.80, "eye": 0.03, "limb": 0.36, "prop": 0.55,
        "desk": 0.30, "wall": 0.20, "pane": 0.10, "frame": 0.48, "flame": 0.95,
        "paper": 0.88, "dark": 0.16, "orange": 0.60}


def col(o, key):
    v = GRAY[key]
    o.color = (v, v, v, 1)
    return o


def link(o, parent=None):
    sc.collection.objects.link(o)
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = 0.1
    o.location = loc
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
    col(o, key)
    return link(o, parent)


def sphere(name, key, loc, scale, parent=None, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    return mesh_obj(name, bm, key, loc, scale, rot, parent)


def cone(name, key, loc, r1, r2, depth, parent=None, scale=(1, 1, 1), rot=(0, 0, 0), smooth=True):
    """Cone/cylinder whose BASE sits at the object origin, pointing +Z."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=r1, radius2=r2, depth=depth)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, depth / 2))
    return mesh_obj(name, bm, key, loc, scale, rot, parent, smooth)


def box(name, key, loc, size, parent=None, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    return mesh_obj(name, bm, key, loc, size, rot, parent, smooth=False)


# ---------- environment ----------
box("ENV_desk", "desk", (0, -1.4, -0.1), (11, 7.0, 0.2))
box("ENV_wall", "wall", (0, 2.2, 3.0), (11, 0.2, 9))
box("ENV_window_pane", "pane", (1.25, 2.08, 2.3), (1.9, 0.05, 2.6))
for nm, loc, size in [("L", (0.25, 2.04, 2.3), (0.12, 0.1, 2.84)), ("R", (2.25, 2.04, 2.3), (0.12, 0.1, 2.84)),
                      ("T", (1.25, 2.04, 3.66), (2.12, 0.1, 0.12)), ("B", (1.25, 2.0, 0.94), (2.3, 0.2, 0.14)),
                      ("V", (1.25, 2.04, 2.3), (0.07, 0.08, 2.6)), ("H", (1.25, 2.04, 2.45), (1.9, 0.08, 0.07))]:
    box("ENV_window_" + nm, "frame", loc, size)
box("PRP_book_1", "prop", (1.45, 0.75, 0.09), (1.0, 0.72, 0.18), rot=(0, 0, D(8)))
box("PRP_book_2", "frame", (1.42, 0.78, 0.25), (0.9, 0.64, 0.14), rot=(0, 0, D(-6)))
cone("PRP_cup", "prop", (-1.75, 0.95, 0), 0.2, 0.23, 0.5)
for i, (dx, dy, tilt) in enumerate([(-0.06, 0.0, 9), (0.07, 0.03, -7), (0.0, -0.06, 3)]):
    cone(f"PRP_pencil_{i}", "frame", (-1.75 + dx, 0.95 + dy, 0.3), 0.022, 0.022, 0.55, rot=(0, D(tilt), 0))

# paper spiral on a thread above the candle
bm = bmesh.new()
turns, steps, z_top, z_bot = 3.0, 96, 2.35, 1.5
prev = None
for i in range(steps + 1):
    t = i / steps
    a = t * turns * 2 * math.pi
    r = 0.05 + 0.27 * t
    z = z_top - (z_top - z_bot) * t
    v_in = bm.verts.new((math.cos(a) * (r - 0.045), math.sin(a) * (r - 0.045), z + 0.02))
    v_out = bm.verts.new((math.cos(a) * (r + 0.045), math.sin(a) * (r + 0.045), z - 0.02))
    if prev:
        bm.faces.new((prev[0], prev[1], v_out, v_in))
    prev = (v_in, v_out)
spiral = mesh_obj("PRP_spiral", bm, "paper", (0, 0, 0))
spiral.modifiers.new("solid", 'SOLIDIFY').thickness = 0.012
cone("PRP_spiral_thread", "paper", (0, 0, z_top), 0.006, 0.006, 3.5)

# ---------- candle (pivots on the far edge of its dish) ----------
PIV_X = 0.22
piv = empty("RIG_candle_pivot", (PIV_X, 0, 0))
cone("PRP_dish", "prop", (-PIV_X, 0, 0), 0.21, 0.24, 0.05, parent=piv)
cone("PRP_candle", "paper", (-PIV_X, 0, 0.05), 0.11, 0.11, 0.52, parent=piv)
cone("PRP_wick", "dark", (-PIV_X, 0, 0.57), 0.008, 0.008, 0.05, parent=piv)
wick_tip = empty("RIG_wick_tip", (-PIV_X, 0, 0.61), parent=piv)

bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=1.0)
for v in bm.verts:  # teardrop: taper the top half and stretch it
    if v.co.z > 0:
        k = (1 - v.co.z) ** 0.6
        v.co.x *= k
        v.co.y *= k
        v.co.z *= 2.4
    v.co.z += 1.0
flame = mesh_obj("PRP_flame", bm, "flame", (0, 0, 0.61), (0.075, 0.075, 0.075))
c = flame.constraints.new('COPY_LOCATION')  # follows the wick, never its tilt
c.target = wick_tip

# ---------- Sol: flat slab traced from Mascot.png (1920 px art, total height 1.0) ----------
def px(pts):
    return [((x - 960) / 1560.0, (1750 - y) / 1560.0) for x, y in pts]


BODY = px([(1112, 190), (1140, 260), (1148, 400), (1185, 520), (1250, 620), (1318, 690), (1352, 610), (1378, 603),
           (1450, 720), (1540, 900), (1590, 1100), (1580, 1300), (1500, 1480), (1350, 1580), (1150, 1620),
           (960, 1626), (770, 1620), (570, 1580), (420, 1480), (340, 1300), (330, 1100), (380, 900), (470, 720),
           (548, 600), (575, 572), (602, 600), (640, 668), (682, 640), (720, 560), (800, 440), (900, 340),
           (1000, 260), (1075, 205)])
ORANGE = px([(1075, 505), (1090, 650), (1150, 790), (1215, 872), (1250, 815), (1300, 900), (1390, 1100),
             (1420, 1280), (1360, 1450), (1200, 1540), (960, 1560), (720, 1540), (560, 1450), (500, 1280),
             (520, 1100), (600, 920), (660, 800), (690, 812), (722, 872), (760, 800), (850, 660), (950, 570),
             (1040, 515)])
CREAM = px([(1050, 765), (1070, 900), (1130, 1010), (1172, 985), (1220, 1060), (1280, 1200), (1290, 1330),
            (1230, 1440), (1100, 1500), (960, 1515), (820, 1500), (690, 1440), (630, 1330), (640, 1200),
            (700, 1060), (742, 985), (776, 1012), (810, 950), (900, 850), (1000, 780)])


def slab(name, key, pts, y, thick, parent, bevel):
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0, z)) for x, z in pts]
    bm.faces.new(vs)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    for f_ in bm.faces:
        if f_.normal.y > 0:
            f_.normal_flip()
    o = mesh_obj(name, bm, key, (0, y, 0), parent=parent, smooth=False)
    m = o.modifiers.new("solid", 'SOLIDIFY')
    m.thickness, m.offset = thick, 0
    if bevel:
        bv = o.modifiers.new("bevel", 'BEVEL')
        bv.width, bv.segments, bv.limit_method, bv.angle_limit = bevel, 4, 'ANGLE', D(50)
    return o


SOL_X = -0.70
root = empty("RIG_Sol", (SOL_X, -0.05, 0))
root.rotation_euler = (0, 0, D(20))       # three-quarter toward the candle
bodyrig = empty("RIG_Sol_body", (0, 0, 0.07), parent=root)   # lean/pitch pivot just above the feet
B = bodyrig
OFF = -0.07                                # art coordinates are measured from the foot line
sol_body = slab("HERO_Sol_body", "body", BODY, 0.0, 0.26, B, 0.09)
sol_orange = slab("HERO_Sol_orange", "orange", ORANGE, -0.125, 0.03, B, 0.0)
sol_cream = slab("HERO_Sol_face", "face", CREAM, -0.145, 0.03, B, 0.0)
for o in (sol_body, sol_orange, sol_cream):
    o.location.z = OFF
eyes = [sphere("HERO_Sol_eye_L", "eye", (-0.0946, -0.162, 0.301 + OFF), (0.034, 0.012, 0.058), parent=B),
        sphere("HERO_Sol_eye_R", "eye", (0.0946, -0.162, 0.301 + OFF), (0.034, 0.012, 0.058), parent=B)]
arm_L = empty("RIG_Sol_arm_L", (-0.385, -0.03, 0.27), parent=B)
arm_R = empty("RIG_Sol_arm_R", (0.385, -0.03, 0.27), parent=B)   # the arm nearest the candle
sphere("HERO_Sol_armnub_L", "limb", (-0.055, 0, 0), (0.085, 0.06, 0.06), parent=arm_L)
sphere("HERO_Sol_armnub_R", "limb", (0.055, 0, 0), (0.085, 0.06, 0.06), parent=arm_R)
sphere("HERO_Sol_foot_L", "limb", (-0.137, 0, 0.05), (0.05, 0.06, 0.06), parent=root)   # feet stay planted
sphere("HERO_Sol_foot_R", "limb", (0.137, 0, 0.05), (0.05, 0.06, 0.06), parent=root)

# ---------- camera ----------
cam_data = bpy.data.cameras.new("CAM_clip01")
cam_data.lens = 50
cam = link(bpy.data.objects.new("CAM_clip01", cam_data))
target = empty("RIG_cam_target")
tc = cam.constraints.new('TRACK_TO')
tc.target, tc.track_axis, tc.up_axis = target, 'TRACK_NEGATIVE_Z', 'UP_Y'
sc.camera = cam

# ---------- animation on twos ----------
def smooth(t, a, b):
    """0 before a, 1 after b, smootherstep between (seconds)."""
    x = min(1.0, max(0.0, (t - a) / (b - a)))
    return x * x * x * (x * (x * 6 - 15) + 10)


def settle(t, a, b, over=0.12):
    """Ease to 1 with a small overshoot that damps out after b."""
    s = smooth(t, a, b)
    if t > a:
        s += over * math.exp(-5.0 * max(0.0, t - b)) * math.sin(min(1.0, (t - a) / (b - a)) * math.pi) \
             + (over * 0.5 * math.exp(-7.0 * (t - b)) * math.sin((t - b) * 14.0) if t > b else 0.0)
    return s


def lerp(a, b, k):
    return a + (b - a) * k


prefs = bpy.context.preferences.edit
old_interp = prefs.keyframe_new_interpolation_type
prefs.keyframe_new_interpolation_type = 'CONSTANT'
FLICK = [1.0, 1.06, 0.97, 1.09, 1.02, 0.94, 1.05, 0.99, 1.08, 0.96, 1.03, 1.0]
try:
    for f in range(1, NFRAMES + 1, 2):      # a new state every 2 frames, held 2 frames
        t = (f - 1) / FPS

        # camera: wide and left of Sol, pushing in and arcing ~25 deg toward the candle
        k = smooth(t, 0.0, 2.9)
        cam.location = (lerp(-1.75, 0.62, k), lerp(-6.4, -4.25, k), lerp(1.65, 1.15, k))
        target.location = (lerp(-0.32, -0.30, k), 0, lerp(1.02, 0.62, k))

        # Sol's near arm: hangs low, lifts onto the candle (0.4-0.8s), stays on it
        reach = smooth(t, 0.40, 0.80)
        arm_R.rotation_euler = (0, lerp(D(48), D(-8), reach), lerp(0, D(-12), reach))
        arm_L.rotation_euler = (0, D(-48), 0)

        # candle tips 25 deg away from Sol (0.75-1.4s), small overshoot, then rests
        tip = settle(t, 0.75, 1.40, over=0.10)
        piv.rotation_euler = (0, D(25) * tip, 0)

        # Sol follows the push a little, then leans over to compare (1.5-2.3s), wobble settles
        lean = 0.35 * smooth(t, 0.75, 1.40) + 0.65 * settle(t, 1.50, 2.30, over=0.16)
        bodyrig.rotation_euler = (0, D(12) * lean, 0)
        wob = 0.0
        for start in (0.75, 1.50):
            if t > start:
                wob += math.exp(-3.2 * (t - start)) * math.sin((t - start) * 11.0)
        bodyrig.scale = (1 + 0.035 * wob, 1, 1 - 0.035 * wob)

        # brief blink at 3.0s (one held pair), same ovals before and after
        blink = 0.08 if f in (91, 92) else 1.0
        for e in eyes:
            e.scale = (0.034, 0.012, 0.058 * blink)

        # candle flame: always world-up, tip flickers, base fixed on the wick
        fl = FLICK[(f // 2) % len(FLICK)]
        flame.scale = (0.075 / math.sqrt(fl), 0.075 / math.sqrt(fl), 0.075 * fl)

        for o, paths in ((cam, ["location"]), (target, ["location"]), (arm_R, ["rotation_euler"]),
                         (arm_L, ["rotation_euler"]), (piv, ["rotation_euler"]), (bodyrig, ["rotation_euler", "scale"]),
                         (flame, ["scale"]), (eyes[0], ["scale"]), (eyes[1], ["scale"])):
            for p in paths:
                o.keyframe_insert(p, frame=f)
finally:
    prefs.keyframe_new_interpolation_type = old_interp

# Blender 5 ignores the new-key interpolation preference here, so force every key to CONSTANT
for o in sc.objects:
    ad = o.animation_data
    if not ad or not ad.action:
        continue
    act = ad.action
    fcs = []
    if hasattr(act, "layers"):
        for layer in act.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    fcs.extend(cb.fcurves)
    else:
        fcs = list(act.fcurves)
    for fc in fcs:
        for kp in fc.keyframe_points:
            kp.interpolation = 'CONSTANT'
        fc.update()

sc.frame_set(1)
result = {"scene": sc.name, "objects": len(sc.objects), "frames": NFRAMES, "blender": bpy.app.version_string}
