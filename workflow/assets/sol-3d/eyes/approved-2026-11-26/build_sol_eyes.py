"""Build Sol with SEPARATE, riggable eyes (Elaine's idea, 2026-11-26: "rigg the eyes like seperately like attach a
3d polygon on top").

Run:  Blender -b ../sol.blend --python build_sol_eyes.py
Reads  ../sol.blend (the approved model, opened read-only: this script never saves over it)
       eye-outlines.json and sol-front-texture-noeyes.png (made from the front art by the tracing step)
Writes sol-eyes.blend  (collection SOL, same names as the approved model plus the eye rig)

What it adds, all parented under RIG_Sol_body so the eyes lean, squash and bounce with him:
  RIG_Sol_eyes            move in X/Z to make him LOOK left/right/up/down (the eyes slide over his face)
    RIG_Sol_eye_L / _R    one per eye, at the eye's centre. Scale Z to blink.
      SOL_eye_*_oval      his normal eye: the exact outline traced from the art, in the art's navy
      SOL_eye_*_chev      the ">" / "<" squeezed-shut eye, drawn as a thick stroke with round tips
      SOL_eye_*_ring      the round surprised "O" eye, with SOL_eye_*_ring_white inside it
      SOL_eye_*_spark     white sparkle highlights that sit on the normal eye
  RIG_Sol_gloom           the worried lines: thin indigo lines hanging on the side of his face above one eye
  material SOL_front_noeyes   has two dials, value nodes "gloom_face" and "gloom_top": a purple shade that is
                          strongest at the top and fades downward, over his face only or from his flame tip
Every piece has a Shrinkwrap modifier that presses it onto the body's front, so it follows the curve of his
face wherever it slides. A piece is hidden by scaling it to nothing. eyes_rig.py has pose_eyes() to drive them.
"""
import bpy, bmesh, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "eye-outlines.json")))
W, H = DATA["size"]
NAVY = tuple(v / 255 for v in DATA["eyes"][0]["bgr"][::-1])
WHITE = (0.985, 0.97, 0.93)
OFFSET = 0.004                      # how far the navy sits off the skin; white pieces sit a little further out
Y_PLANE = -0.6                      # the flat pieces start in front of him and are pressed back onto his face

body = bpy.data.objects["SOL_body"]
coll = bpy.data.collections["SOL"]
rig_body = body.parent
me = body.data

# ---- how the front art maps onto the body: X = a*u + b, Z = c*v + d (the art is laid on from the front) ----
nl = len(me.loops)
vi = np.zeros(nl, np.int32); me.loops.foreach_get("vertex_index", vi)
uv = np.zeros(nl * 2, np.float32); me.uv_layers[0].data.foreach_get("uv", uv); uv = uv.reshape(-1, 2)
co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
pm = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get("material_index", pm)
ls = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get("loop_start", ls)
lt = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get("loop_total", lt)
front = np.zeros(nl, bool)
for s, t in zip(ls[pm == 0], lt[pm == 0]):
    front[s:s + t] = True
P = co[vi[front]]; U = uv[front]
ax, bx = np.polyfit(U[:, 0], P[:, 0], 1)
cz, dz = np.polyfit(U[:, 1], P[:, 2], 1)
err = max(np.abs(ax * U[:, 0] + bx - P[:, 0]).max(), np.abs(cz * U[:, 1] + dz - P[:, 2]).max())
print(f"FIT X={ax:.4f}u+{bx:.4f}  Z={cz:.4f}v+{dz:.4f}  worst error {err:.5f}")


def px(x, y):
    """A pixel of the front art -> (X, Z) on the body."""
    return ax * (x / W) + bx, cz * (1 - y / H) + dz


def material(name, rgb):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = tuple(c ** 2.2 for c in rgb) + (1,)
    b.inputs["Roughness"].default_value = 0.6
    return m


M_NAVY, M_WHITE = material("SOL_eye_navy", NAVY), material("SOL_eye_white", WHITE)


def empty(name, loc, parent):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = 0.03
    o.location = loc
    o.parent = parent
    coll.objects.link(o)
    return o


def piece(name, outline, mat, parent, offset=OFFSET, hidden=False):
    """A flat filled shape (outline in metres, relative to its parent) pressed onto the body's front."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0.0, z)) for x, z in outline]
    f = bm.faces.new(vs)
    bmesh.ops.triangulate(bm, faces=[f])
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    m = bpy.data.meshes.new(name)
    bm.to_mesh(m); bm.free()
    for p in m.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, m)
    o.parent = parent
    m.materials.append(mat)
    coll.objects.link(o)
    sw = o.modifiers.new("onto_face", 'SHRINKWRAP')
    sw.target = body
    sw.wrap_method = 'PROJECT'
    sw.use_project_x, sw.use_project_y, sw.use_project_z = False, True, False
    sw.use_positive_direction, sw.use_negative_direction = True, False
    sw.offset = offset
    if hidden:
        o.scale = (0.0, 0.0, 0.0)
    return o


def ellipse(rx, rz, n=40, cx=0.0, cz_=0.0):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cz_ + rz * math.sin(2 * math.pi * i / n)) for i in range(n)]


def round_chevron(a, b, r, steps=10):
    """Outline of a ">" drawn as a thick stroke with round ends and a round point: A(-a, b) -> T(a, 0) -> B(-a, -b)."""
    A, T, B = (-a, b), (a, 0.0), (-a, -b)

    def unit(p, q):
        dx, dz = q[0] - p[0], q[1] - p[1]
        n = math.hypot(dx, dz)
        return dx / n, dz / n
    d1, d2 = unit(A, T), unit(T, B)
    n1, n2 = (-d1[1], d1[0]), (-d2[1], d2[0])                      # the outer side of each stroke

    def arc(c, a0, a1):
        return [(c[0] + r * math.cos(a0 + (a1 - a0) * i / steps), c[1] + r * math.sin(a0 + (a1 - a0) * i / steps)) for i in range(steps + 1)]
    ang = lambda v: math.atan2(v[1], v[0])
    a_n1, a_n2 = ang(n1), ang(n2)
    pts = arc(T, a_n1, a_n2 if a_n2 < a_n1 else a_n2 - 2 * math.pi)                 # round point
    pts += arc(B, a_n2, a_n2 - math.pi)                                           # round end at B
    # inner corner: where the two inner edges meet
    p1 = (A[0] - n1[0] * r, A[1] - n1[1] * r); p2 = (B[0] - n2[0] * r, B[1] - n2[1] * r)
    det = d1[0] * (-d2[1]) - (-d2[0]) * d1[1]
    t = ((p2[0] - p1[0]) * (-d2[1]) - (-d2[0]) * (p2[1] - p1[1])) / det
    pts.append((p1[0] + d1[0] * t, p1[1] + d1[1] * t))
    pts += arc(A, a_n1 + math.pi, a_n1)                                           # round end at A
    return pts


def star(r, n=4, inner=0.32, cx=0.0, cz_=0.0, turn=math.pi / 2):
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * inner
        a = turn + math.pi * i / n
        pts.append((cx + rr * math.cos(a), cz_ + rr * math.sin(a)))
    return pts


rig_eyes = empty("RIG_Sol_eyes", (0, 0, 0), rig_body)
info = {}
for side, e in zip(("L", "R"), sorted(DATA["eyes"], key=lambda e: px(*e["centre"])[0])):       # L = his eye at -X
    cx, cz0 = px(*e["centre"])
    x0, z1 = px(e["box"][0], e["box"][1]); x1, z0 = px(e["box"][0] + e["box"][2], e["box"][1] + e["box"][3])
    w, h = abs(x1 - x0), abs(z1 - z0)
    rig = empty(f"RIG_Sol_eye_{side}", (cx, Y_PLANE, cz0), rig_eyes)
    oval = [(px(x, y)[0] - cx, px(x, y)[1] - cz0) for x, y in e["outline"]]
    if (oval[1][0] - oval[0][0]) * (oval[1][1] + oval[0][1]) > 0:                               # keep one winding
        pass
    piece(f"SOL_eye_{side}_oval", oval, M_NAVY, rig)
    # ">" for the eye at -X and "<" for the eye at +X, so the pair reads "> <"
    chev = round_chevron(0.70 * w, 0.345 * h, 0.105 * h)          # rounded tips (Elaine, 2026-11-26)
    if side == "R":
        chev = [(-x, z) for x, z in chev]              # mirrored, same point order (reversing it broke the fill)
    piece(f"SOL_eye_{side}_chev", chev, M_NAVY, rig, hidden=True)
    r = 0.47 * h
    piece(f"SOL_eye_{side}_ring", ellipse(r, r), M_NAVY, rig, hidden=True)
    piece(f"SOL_eye_{side}_ring_white", ellipse(0.62 * r, 0.62 * r), M_WHITE, rig, offset=OFFSET + 0.003, hidden=True)
    # sparkle: a four-point star high on the eye and a small dot low on it
    sp = piece(f"SOL_eye_{side}_spark", star(0.34 * w, cx=-0.12 * w, cz_=0.20 * h), M_WHITE, rig, offset=OFFSET + 0.003, hidden=True)
    piece(f"SOL_eye_{side}_spark_dot", ellipse(0.11 * w, 0.11 * w, n=16, cx=0.16 * w, cz_=-0.22 * h), M_WHITE, sp, offset=OFFSET + 0.003)
    info[side] = {"centre": (round(cx, 4), round(cz0, 4)), "w": round(w, 4), "h": round(h, 4)}

# "|||": worried lines hanging over the top of his face, above one eye
GLOOM = json.load(open(os.path.join(HERE, "gloom.json")))
PURPLE = (0.07, 0.12, 0.50)          # bluer and darker (Elaine, 2026-11-26: "lets make the purple like bluer and darker")
M_LINE = material("SOL_gloom_line", (0.13, 0.14, 0.42))
gl = empty("RIG_Sol_gloom", (0, Y_PLANE, 0), rig_body)
for k, (x_px, top_px, length_px) in enumerate(GLOOM["lines"]):
    xa, za = px(x_px - 6, top_px); xb, zb = px(x_px + 6, top_px + length_px)
    piece(f"SOL_gloom_{k}", [(xa, za), (xb, za), (xb, zb), (xa, zb)], M_LINE, gl)
gl.scale = (0.0, 0.0, 0.0)

# the body wears the copy of his art with the eyes painted out; the approved art file is untouched
mat = body.data.materials[0].copy()
mat.name = "SOL_front_noeyes"
img = bpy.data.images.load(os.path.join(HERE, "sol-front-texture-noeyes.png"))
nt = mat.node_tree
tex = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
tex.image = img
bsdf = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'][0]
# the worried shade: a purple wash, strongest at the top and fading downward. Two areas, each with its own dial:
#   "gloom_face" covers his cream face only, "gloom_top" runs from his flame tip down. 0 = off, 1 = full.
total = None
for key in ("face", "top"):
    m_img = bpy.data.images.load(os.path.join(HERE, f"sol-gloom-mask-{key}.png"))
    m_img.colorspace_settings.name = 'Non-Color'
    mt = nt.nodes.new("ShaderNodeTexImage"); mt.image = m_img; mt.name = mt.label = f"gloom_mask_{key}"
    val = nt.nodes.new("ShaderNodeValue"); val.name = val.label = f"gloom_{key}"; val.outputs[0].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'
    nt.links.new(mt.outputs["Color"], mul.inputs[0]); nt.links.new(val.outputs[0], mul.inputs[1])
    if total is None:
        total = mul
    else:
        add = nt.nodes.new("ShaderNodeMath"); add.operation = 'ADD'; add.use_clamp = True
        nt.links.new(total.outputs[0], add.inputs[0]); nt.links.new(mul.outputs[0], add.inputs[1])
        total = add
strength = nt.nodes.new("ShaderNodeMath"); strength.operation = 'MULTIPLY'; strength.inputs[1].default_value = 0.96
nt.links.new(total.outputs[0], strength.inputs[0])
mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'RGBA'; mix.name = "gloom_mix"
nt.links.new(strength.outputs[0], mix.inputs[0])
nt.links.new(tex.outputs["Color"], mix.inputs[6])
mix.inputs[7].default_value = tuple(c ** 2.2 for c in PURPLE) + (1,)
nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
body.data.materials[0] = mat
# the back of his body takes the same top-down shade, so no orange rim shows behind it from the side
back = body.data.materials[1].copy()
back.name = "SOL_back_shade"
bn = back.node_tree
btex = [n for n in bn.nodes if n.type == 'TEX_IMAGE'][0]
bbsdf = [n for n in bn.nodes if n.type == 'BSDF_PRINCIPLED'][0]
bm_img = bn.nodes.new("ShaderNodeTexImage"); bm_img.image = bpy.data.images.load(os.path.join(HERE, "sol-gloom-mask-top.png"), check_existing=True)
bm_img.image.colorspace_settings.name = 'Non-Color'
bval = bn.nodes.new("ShaderNodeValue"); bval.name = bval.label = "gloom_top"; bval.outputs[0].default_value = 0.0
bmul = bn.nodes.new("ShaderNodeMath"); bmul.operation = 'MULTIPLY'
bn.links.new(bm_img.outputs["Color"], bmul.inputs[0]); bn.links.new(bval.outputs[0], bmul.inputs[1])
bstr = bn.nodes.new("ShaderNodeMath"); bstr.operation = 'MULTIPLY'; bstr.inputs[1].default_value = 0.96
bn.links.new(bmul.outputs[0], bstr.inputs[0])
bmix = bn.nodes.new("ShaderNodeMix"); bmix.data_type = 'RGBA'
bn.links.new(bstr.outputs[0], bmix.inputs[0]); bn.links.new(btex.outputs["Color"], bmix.inputs[6])
bmix.inputs[7].default_value = tuple(c ** 2.2 for c in PURPLE) + (1,)
bn.links.new(bmix.outputs[2], bbsdf.inputs["Base Color"])
body.data.materials[1] = back

print("EYES", json.dumps(info))
json.dump(info, open(os.path.join(HERE, "eye-metrics.json"), "w"), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "sol-eyes.blend"), copy=True)
print("SAVED", os.path.join(HERE, "sol-eyes.blend"))
