"""Reusable 3D Sol: Mascot.png traced and inflated (Elaine's method, 2026-11-25).

Step 1 (plain python, see prepare_sol.py): trace the real outline from Mascot.png's alpha, inflate it
like a balloon (solve laplace(h) = -1 inside the outline, depth = sqrt(h)), and make the textures.
Step 2 (this file, inside Blender with OUT_DIR set): build the mesh from sol-inflate.npz, wrap the
actual mascot art on the front and plain body red on the back, add two stubby arms, render a turnaround
and write sol.blend. Scene "sol_model", collection "SOL", root RIG_Sol at the feet, height 1.0.
"""
import bpy, bmesh, math, os
import numpy as np

D = math.radians
OUT = OUT_DIR
LIMBS = globals().get("LIMBS", True)                   # False builds the logo version: the body alone, no arms or legs
TAG = "sol" if LIMBS else "sol-logo"
SCENE, COLL, SUF = ("sol_model", "SOL", "") if LIMBS else ("sol_logo_model", "SOL_LOGO", "_logo")
data = np.load(os.path.join(OUT, "sol-inflate.npz"))
M, DEPTH, GX, GY, XS, ZS = data["M"], data["depth"], data["gx"], data["gy"], data["X"], data["Z"]
IMG_H, IMG_W = [int(v) for v in data["size"]]

old = bpy.data.scenes.get(SCENE)
if old:
    for o in list(old.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.scenes.remove(old)
sc = bpy.data.scenes.new(SCENE)
bpy.context.window.scene = sc
coll = bpy.data.collections.get(COLL)
if coll:
    bpy.data.collections.remove(coll)
coll = bpy.data.collections.new(COLL)
sc.collection.children.link(coll)


def material(name, image=None, colour=None):
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.9
    for nm in ("Specular IOR Level", "Specular"):
        if nm in bsdf.inputs:
            bsdf.inputs[nm].default_value = 0.1
    if image:
        old_img = bpy.data.images.get(os.path.basename(image))
        if old_img:
            bpy.data.images.remove(old_img)
        t = m.node_tree.nodes.new("ShaderNodeTexImage")
        t.image, t.extension = bpy.data.images.load(image), 'EXTEND'
        m.node_tree.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = colour
        m.diffuse_color = colour
    return m


M_FRONT = material("SOL_front", image=os.path.join(OUT, "sol-front-texture.png"))
M_BACK = material("SOL_back", image=os.path.join(OUT, "sol-back-texture.png"))
def lin8(r, g, b):
    return tuple((v / 255 / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4) for v in (r, g, b)) + (1.0,)


LIMB_LEN = 0.062                                       # leg length in Mascot.png (re-measured exactly below)
M_LIMB = material("SOL_limb", colour=lin8(185, 51, 44))
nt = M_LIMB.node_tree                                  # Mascot.png's leg colours: darker where it joins, lighter at the tip
tc, sep = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ")
mr, ramp = nt.nodes.new("ShaderNodeMapRange"), nt.nodes.new("ShaderNodeValToRGB")
mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = 0.0, LIMB_LEN * 1.1
ramp.color_ramp.elements[0].color, ramp.color_ramp.elements[1].color = lin8(196, 63, 45), lin8(169, 43, 41)
nt.links.new(tc.outputs["Object"], sep.inputs[0])
nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])

bm = bmesh.new()
uv = bm.loops.layers.uv.new("UV")
vf, vb = {}, {}
rows, cols = M.shape
FULL = np.ones(M.shape, bool)                             # rim = inside cells touching the outside, diagonals included,
for di in (-1, 0, 1):                                  # so the front and back sheets meet along every outline step
    for dj in (-1, 0, 1):
        FULL &= np.roll(np.roll(M, di, 0), dj, 1)
RIM = M & ~FULL
for i in range(rows):
    for j in range(cols):
        if M[i, j]:
            if RIM[i, j]:                              # front and back halves share one vertex on the outline
                vf[i, j] = vb[i, j] = bm.verts.new((XS[j], 0.0, ZS[i]))
            else:
                vf[i, j] = bm.verts.new((XS[j], -DEPTH[i, j], ZS[i]))
                vb[i, j] = bm.verts.new((XS[j], DEPTH[i, j], ZS[i]))
STEPX = float(XS[1] - XS[0])


def set_uv(face):
    for lp in face.loops:
        co = lp.vert.co
        px_x = GX[0] + (co.x - XS[0]) / STEPX * (GX[1] - GX[0])
        px_y = GY[0] + (ZS[0] - co.z) / STEPX * (GY[1] - GY[0])
        lp[uv].uv = (px_x / IMG_W, 1 - px_y / IMG_H)


for i in range(rows - 1):
    for j in range(cols - 1):
        q = [(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)]
        if all(c in vf for c in q):
            f = bm.faces.new([vf[c] for c in q])
            f.material_index = 0
            set_uv(f)
            if not all(RIM[c] for c in q):             # a cell lying wholly on the rim is one thin membrane
                f = bm.faces.new([vb[c] for c in reversed(q)])
                f.material_index = 1
                set_uv(f)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
for _ in range(30):                                    # soften the pixel-grid stair-steps on the outline
    bmesh.ops.smooth_vert(bm, verts=bm.verts[:], factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
rim_verts = list({vf[i, j] for i in range(rows) for j in range(cols) if M[i, j] and RIM[i, j]})
for _ in range(12):                                    # extra pass along the outline itself: no stair-steps
    bmesh.ops.smooth_vert(bm, verts=rim_verts, factor=0.5, use_axis_x=True, use_axis_y=False, use_axis_z=True)
zc = float((ZS.max() + ZS.min()) / 2)                    # smoothing pulls the outline in about 2%: put it back
for v in bm.verts:                                     # so the silhouette lands on Mascot.png's outline (see compare.py)
    v.co.x *= 1.022
    v.co.z = zc + (v.co.z - zc) * 1.022
for f in bm.faces:                                     # uvs follow the smoothed positions
    set_uv(f)


def add(name, bm_, mats, parent, loc=(0, 0, 0), scale=(1, 1, 1)):
    me = bpy.data.meshes.new(name)
    bm_.to_mesh(me)
    bm_.free()
    for p in me.polygons:
        p.use_smooth = True
    for m in mats:
        me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    o.location, o.scale, o.parent = loc, scale, parent
    coll.objects.link(o)
    return o


def empty(name, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = 0.08
    o.location, o.rotation_euler, o.parent = loc, rot, parent
    coll.objects.link(o)
    return o


root = empty("RIG_Sol" + SUF)
body = empty("RIG_Sol_body" + SUF, root)
if not LIMBS:
    body.location.z = -float(data["body_bottom"])      # the logo rests on the ground: no legs to stand on
sol_body = add("SOL_body" + SUF, bm, [M_FRONT, M_BACK], body)
# Legs and arms share ONE shape: the mascot's own leg. Its outline is read off Mascot.png row by row in
# prepare_sol.py (half-width vs distance from the tip) and spun into a round limb with NO reshaping:
# wide where it joins the body, sides closing in, and a blunt rounded tip. Earlier versions that I
# narrowed or made into tapered ovals came out too pointy and Elaine rejected them (2026-11-25).
LEG_D, LEG_R, LEG_X = data["leg_d"], data["leg_r"], float(data["leg_x"])
LIMB_LEN = float(LEG_D[-1])                              # the part of the leg that shows below the body


ARM_STRETCH = 1.9                                      # arms: the leg shape, made longer (Elaine: "make the arms longer")


def limb_mesh(stretch=1.0):
    d, r = [v * stretch for v in LEG_D], list(LEG_R)
    slope = (r[-1] - r[-12]) / (d[-1] - d[-12])          # carry the leg's own widening on up into the body
    slope /= stretch
    for k in range(1, 30):
        d.append(d[-1] + 0.004)
        r.append(min(r[-1] + slope * 0.004 * max(0.0, 1 - k / 20), 0.075))
    b = bmesh.new()
    seg = 40
    rings = [[b.verts.new((0, 0, 0))]]
    for rad, dist in zip(r, d):
        rings.append([b.verts.new((rad * math.cos(t), rad * math.sin(t), dist)) for t in (2 * math.pi * k / seg for k in range(seg))])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(seg):
            j = (k + 1) % seg
            if len(r0) == 1:
                b.faces.new((r0[0], r1[j], r1[k]))
            else:
                b.faces.new((r0[k], r0[j], r1[j], r1[k]))
    b.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(b, faces=b.faces[:])
    return b


for sx in ((-1, 1) if LIMBS else ()):                  # legs: exactly where Mascot.png has them, tip on the ground
    add(f"SOL_leg_{'L' if sx < 0 else 'R'}", limb_mesh(), [M_LIMB], root, (sx * LEG_X, 0, 0))
ARM_Z = 0.33
for sx in ((-1, 1) if LIMBS else ()):                  # arms: the same shape, pointing out and down from his sides
    side = "L" if sx < 0 else "R"
    row = M[int(np.argmin(np.abs(ZS - ARM_Z)))]
    edge = float(XS[np.where(row)[0].max()] if sx > 0 else XS[np.where(row)[0].min()])     # body outline at arm height
    arm = empty(f"RIG_Sol_arm_{side}", body, (edge - sx * 0.03, -0.03, ARM_Z + 0.03), (0, D(-50) * sx, 0))
    add(f"SOL_arm_{side}", limb_mesh(ARM_STRETCH), [M_LIMB], arm, (0, 0, -LIMB_LEN * ARM_STRETCH))

# ---- turnaround render: white background, soft light ----
cd = bpy.data.cameras.new("CAM_sol")
cd.type, cd.ortho_scale = 'ORTHO', 1.3
cam = bpy.data.objects.new("CAM_sol", cd)
sc.collection.objects.link(cam)
tgt = bpy.data.objects.new("CAM_sol_target", None)
sc.collection.objects.link(tgt)
tgt.location = (0, 0, 0.5)
c = cam.constraints.new('TRACK_TO')
c.target, c.track_axis, c.up_axis = tgt, 'TRACK_NEGATIVE_Z', 'UP_Y'
sc.camera = cam
sun_d = bpy.data.lights.new("LGT_sol_key", 'SUN')
sun_d.energy, sun_d.angle = 1.6, D(50)
sun_d.use_shadow = False                               # no self-shadow streaks along the rim
sun = bpy.data.objects.new("LGT_sol_key", sun_d)
sc.collection.objects.link(sun)
sun.parent = cam
sun.rotation_euler = (D(-25), D(-20), 0)
w = bpy.data.worlds.new("sol_world")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.85
sc.world = w
sc.render.engine = 'BLENDER_EEVEE'
sc.view_settings.view_transform = 'Standard'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 800, 800, 100
sc.render.image_settings.file_format = 'PNG'
paths = []
for name, ang in (("front", 0), ("three-quarter", 40), ("side", 90), ("back", 180)):
    a = D(ang)
    cam.location = (4 * math.sin(a), -4 * math.cos(a), 0.5)
    sc.render.filepath = os.path.join(OUT, f"{TAG}-{name}.png")
    bpy.ops.render.render(write_still=True, scene=sc.name)
    paths.append(sc.render.filepath)
blend = os.path.join(OUT, TAG + ".blend")
bpy.data.libraries.write(blend, {coll}, fake_user=True)
result = {"views": paths, "blend": blend, "verts": len(vf) * 2}
