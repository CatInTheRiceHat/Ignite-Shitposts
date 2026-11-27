"""Skeleton kit for the "All Due This Week" ad (LANDSCAPE 16:9), copied from the "Due in 5 Minutes" ad's rig.

Original notes: Skeleton kit for the "Due in 5 Minutes" ad. exec() this inside Blender, then clips.py (render_clip.py does both).

Differences from the coffee episode's rig:
  - Sol is the SEPARATE-EYES model (assets/sol-3d/eyes/sol-eyes.blend, approved 2026-11-26), so every expression,
    blink and glance in the script is keyed here and not left to the painter.
  - The rooms are blocked out in simple real colours, not gray, because this ad cuts between five sets and the
    house has to read as one place. The painter follows the colours it is given.
  - Lettering is never in the skeleton. Objects whose names start with OVL_ are overlay planes: they are hidden
    in the skeleton render and rendered alone, with alpha, by render_clip.py in "ovl" mode.
Motion is smooth (keyed every frame).
"""
import bpy, bmesh, math, os

WF = os.path.normpath(os.path.join(RIG_DIR, "..", "..", ".."))
# the APPROVED separate-eyes model (frozen 2026-11-26): its six expressions are exactly the ones the script names.
# The working copy beside it has 38 expressions that Elaine has not approved yet.
EYES_DIR = os.path.join(WF, "assets", "sol-3d", "eyes", "approved-2026-11-26")
SOL_BLEND = os.path.join(EYES_DIR, "sol-eyes.blend")
exec(compile(open(os.path.join(EYES_DIR, "eyes_rig.py")).read(), "eyes_rig.py", "exec"))

D = math.radians
FPS = int(os.environ.get("SKEL_FPS", 24))        # the painter returns 24 fps, so the skeleton is 24 (frame counts in clips.py are written for 30 and converted)
S = {"sc": None, "keys": [], "anchors": {}}

# the house palette: every set uses these, so the rooms belong together
C = {
    "wall": (0.62, 0.78, 0.78), "trim": (0.96, 0.95, 0.91), "wood": (0.76, 0.54, 0.34), "wood_d": (0.55, 0.36, 0.22),
    "floor": (0.80, 0.62, 0.44), "white": (0.97, 0.97, 0.95), "paper": (0.99, 0.97, 0.90), "teal": (0.22, 0.52, 0.55),
    "coral": (0.93, 0.50, 0.42), "yellow": (0.98, 0.80, 0.30), "blue": (0.33, 0.56, 0.84), "ice": (0.80, 0.91, 0.97),
    "steel": (0.72, 0.75, 0.78), "dark": (0.16, 0.18, 0.26), "pink": (0.97, 0.66, 0.74), "mint": (0.62, 0.88, 0.74),
    "sky": (0.99, 0.93, 0.76), "leaf": (0.36, 0.62, 0.40), "fog": (0.95, 0.98, 1.0), "counter": (0.93, 0.90, 0.84),
    "cardA": (1.0, 0.86, 0.66), "cardB": (0.72, 0.87, 0.98), "tag": (0.80, 0.93, 0.74), "page": (1.0, 0.96, 0.72),
    # added for this ad
    "cardboard": (0.80, 0.62, 0.42), "cardboard_d": (0.62, 0.45, 0.28), "red": (0.86, 0.26, 0.22), "sticky": (1.0, 0.88, 0.36),
    "sticky_b": (0.62, 0.84, 0.98), "sticky_p": (0.99, 0.70, 0.80), "water": (0.52, 0.74, 0.76), "water_l": (0.74, 0.88, 0.86),
    "moss": (0.52, 0.66, 0.30), "moss_d": (0.38, 0.52, 0.26), "stone": (0.62, 0.62, 0.58), "stone_d": (0.47, 0.48, 0.46),
    "grass": (0.62, 0.74, 0.40), "bush": (0.42, 0.60, 0.32), "maple": (0.90, 0.42, 0.20), "maple_l": (0.97, 0.66, 0.30),
    "trunk": (0.47, 0.36, 0.28), "haze": (0.99, 0.90, 0.78), "glow": (1.0, 0.93, 0.55), "bed": (0.93, 0.50, 0.42),
    "book": (0.62, 0.50, 0.30),
}


def new_scene(name, nframes):
    nframes = int(round(nframes * FPS / 30))
    sc = bpy.data.scenes.new(name)
    bpy.context.window.scene = sc
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, nframes
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
    sc.render.engine = 'BLENDER_EEVEE'
    try:
        sc.eevee.taa_render_samples = 12
    except Exception:
        pass
    sc.view_settings.view_transform = 'Standard'
    w = bpy.data.worlds.new("skeleton_world")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.62, 0.60, 0.58, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    sc.world = w
    sun_d = bpy.data.lights.new("LGT_key", 'SUN')
    sun_d.energy, sun_d.angle = 2.2, math.radians(25)
    sun = bpy.data.objects.new("LGT_key", sun_d)
    sun.rotation_euler = (math.radians(50), 0, math.radians(-25))
    sc.collection.objects.link(sun)
    S["sc"], S["keys"], S["anchors"] = sc, [], {}
    return sc


def mat(key, alpha=1.0, rough=0.85):
    """Material for a palette key or an (r, g, b) tuple. Colours are display values."""
    rgb = C[key] if isinstance(key, str) else key
    name = "COL_%s_%s" % (key if isinstance(key, str) else "%.2f_%.2f_%.2f" % rgb, alpha)
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


def mesh_obj(name, bm, key, loc=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), parent=None, smooth=True, alpha=1.0):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    o.location, o.scale, o.rotation_euler = loc, scale, rot
    me.materials.append(mat(key, alpha))
    return link(o, parent)


def sphere(name, key, loc, scale, parent=None, rot=(0, 0, 0), alpha=1.0):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    return mesh_obj(name, bm, key, loc, scale, rot, parent, alpha=alpha)


def cone(name, key, loc, r1, r2, depth, parent=None, scale=(1, 1, 1), rot=(0, 0, 0), smooth=True, alpha=1.0):
    """Cone/cylinder with its BASE at the object origin, pointing +Z."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=r1, radius2=r2, depth=depth)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, depth / 2))
    return mesh_obj(name, bm, key, loc, scale, rot, parent, smooth, alpha)


def box(name, key, loc, size, parent=None, rot=(0, 0, 0), alpha=1.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    return mesh_obj(name, bm, key, loc, size, rot, parent, smooth=False, alpha=alpha)


def overlay_plane(name, image, loc, size, rot=(D(90), 0, 0), parent=None):
    """A flat plane carrying a PNG (with alpha) from overlays/art/. Hidden in the skeleton render; render_clip.py's
    "ovl" mode renders each one alone, so the lettering can be laid over the painted clip in exactly this
    perspective. size = (width, height) in metres; by default it stands upright facing the camera (-Y)."""
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    uv = bm.loops.layers.uv.new("uv")
    for f in bm.faces:
        for l in f.loops:
            l[uv].uv = (l.vert.co.x + 0.5, l.vert.co.y + 0.5)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("OVL_" + name, me)
    o.location, o.rotation_euler, o.scale = loc, rot, (size[0], size[1], 1)
    m = bpy.data.materials.new("OVLMAT_" + name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.join(RIG_DIR, "..", "overlays", "art", image))
    tex.image.alpha_mode = 'STRAIGHT'
    em = nt.nodes.new("ShaderNodeEmission")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    m.surface_render_method = 'BLENDED'
    me.materials.append(m)
    o.hide_render = True
    return link(o, parent)


def anchor(name, loc):
    """Remember a world point; render_clip.py writes where it lands on screen (for pop-up labels)."""
    S["anchors"][name] = tuple(loc)


# ---------------- Sol: the approved separate-eyes model ----------------
def build_sol(loc, yaw):
    with bpy.data.libraries.load(SOL_BLEND) as (src, dst):
        dst.collections = ["SOL"]
    coll = dst.collections[0]
    S["sc"].collection.children.link(coll)
    objs = {o.name.split(".")[0]: o for o in coll.all_objects}
    root, body = objs["RIG_Sol"], objs["RIG_Sol_body"]
    root.location, root.rotation_euler = loc, (0, 0, D(yaw))
    eyes = find_eyes(coll.all_objects)
    sol = {"root": root, "body": body, "arm_l": objs["RIG_Sol_arm_L"], "arm_r": objs["RIG_Sol_arm_R"], "eyes": eyes}
    track(root, "rotation_euler", "location")
    track(body, "rotation_euler", "scale")
    track(sol["arm_l"], "rotation_euler")
    track(sol["arm_r"], "rotation_euler")
    for o in eye_objects(eyes):
        track(o, "location", "scale")
    return sol


def pose_sol(sol, yaw=0.0, lean=0.0, pitch=0.0, squash=0.0, arm_l=(-40, 0), arm_r=(-40, 0), loc=None):
    """Angles in degrees. yaw>0 turns him toward screen right. lean>0 tips toward screen right. pitch>0 tilts back
    (looking up), pitch<0 bows forward. arm = (raise above horizontal, swing forward); -40 is how arms hang at rest.
    arm_l is the arm on screen LEFT when he faces the camera, arm_r the one on screen right."""
    if loc is not None:
        sol["root"].location = loc
    sol["root"].rotation_euler = (0, 0, D(yaw))
    sol["body"].rotation_euler = (D(-pitch), D(lean), 0)
    sol["body"].scale = (1 + 0.8 * squash, 1 + 0.8 * squash, 1 - squash)
    sol["arm_l"].rotation_euler = (0, D(90 + arm_l[0]), D(arm_l[1]))
    sol["arm_r"].rotation_euler = (0, -D(90 + arm_r[0]), -D(arm_r[1]))


def face(sol, f, expr="normal", blink=0.0, look=(0.0, 0.0), size=1.0, gloom=None):
    """Set his eyes for this frame and key the two purple-shade dials (everything else is keyed by animate())."""
    e = sol["eyes"]
    pose_eyes(e, expr, blink=blink, look=look, size=size, gloom=gloom)
    for socks in e["shade"].values():
        for sock in socks:
            sock.keyframe_insert("default_value", frame=f)


def blink_at(t, times, d=0.16):
    for b0 in times:
        if b0 <= t < b0 + d:
            return math.sin((t - b0) / d * math.pi)
    return 0.0


def build_camera(lens=30):
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


def hop(t, a, b, h):
    """Height of one hop between a and b (a parabola)."""
    if t <= a or t >= b:
        return 0.0
    u = (t - a) / (b - a)
    return h * 4 * u * (1 - u)


def pop(t, start, d=0.28):
    """0 -> overshoot -> 1: a springy pop-in that starts at `start`."""
    if t <= start:
        return 0.0
    u = (t - start) / d
    return 1.0 + (-math.exp(-5.5 * u) * math.cos(u * 6.0)) if u < 4 else 1.0


def lerp(a, b, k):
    return a + (b - a) * k


def lerp3(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def idle(t):
    return 0.012 * math.sin(t * 3.0)


def track(o, *paths):
    for p in paths:
        S["keys"].append((o, p))


def animate(nframes, state):
    """Call state(t, f) on EVERY frame and key everything tracked."""
    sc = S["sc"]
    nframes = int(round(nframes * FPS / 30))
    for f in range(1, nframes + 1):
        state((f - 1) / FPS, f)
        for o, p in S["keys"]:
            o.keyframe_insert(p, frame=f)
    for o in sc.objects:
        ad = o.animation_data
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
