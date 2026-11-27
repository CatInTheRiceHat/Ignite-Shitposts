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


def rotate(pts, deg):
    a = math.radians(deg)
    return [(x * math.cos(a) - z * math.sin(a), x * math.sin(a) + z * math.cos(a)) for x, z in pts]


def shift(pts, dx, dz):
    return [(x + dx, z + dz) for x, z in pts]


def scaled(pts, k):
    return [(x * k, z * k) for x, z in pts]


def half_disc(r, cut=0.0, n=28):
    """The part of a disc of radius r that lies below the line z = -cut (a semicircle when cut = 0)."""
    a0 = math.asin(max(min(cut / r, 0.999), -0.999))
    return [(r * math.cos(-a0 - (math.pi - 2 * a0) * i / n), r * math.sin(-a0 - (math.pi - 2 * a0) * i / n)) for i in range(n + 1)]


def arc_path(r, a0, a1, n=24, cx=0.0, cz_=0.0):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cz_ + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def line(a, b, n=8):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]


def segs(path):
    """A path with sharp corners, as separate straight strokes (their round ends make round corners)."""
    return [[path[i], path[i + 1]] for i in range(len(path) - 1)]


def heart(r, n=48):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        pts.append((r * 16 * math.sin(t) ** 3 / 17, r * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17 + 0.12 * r))
    return pts[::-1]


def drop(wd, ht, n=24):
    """A teardrop, point up, centred on its round part."""
    pts = [(wd / 2 * math.cos(math.pi * (1 + i / n)), wd / 2 * math.sin(math.pi * (1 + i / n))) for i in range(n + 1)]
    return pts + [(wd * 0.16, ht * 0.45), (0.0, ht - wd / 2), (-wd * 0.16, ht * 0.45)]


def sparkle(r, wide=0.66, pinch=0.10, n=10):
    """A four-point sparkle: tall points up and down, shorter ones to the sides, the sides curved inward."""
    tips = [(0.0, r), (wide * r, 0.0), (0.0, -r), (-wide * r, 0.0)]
    pts = []
    for k in range(4):
        (x0, z0), (x1, z1) = tips[k], tips[(k + 1) % 4]
        cx_, cz2 = (x0 + x1) * pinch, (z0 + z1) * pinch                    # pulled in toward the middle
        for i in range(n):
            t = i / n
            pts.append(((1 - t) ** 2 * x0 + 2 * t * (1 - t) * cx_ + t * t * x1, (1 - t) ** 2 * z0 + 2 * t * (1 - t) * cz2 + t * t * z1))
    return pts[::-1]                                                        # anticlockwise


def puffy_star(r, wide=0.80, waist=0.40, rounds=4):
    """A soft four-point star: points up, down and to the sides, rounded tips, sides curved in. Made to be inflated."""
    tips = [(0.0, r), (wide * r, 0.0), (0.0, -r), (-wide * r, 0.0)]
    pts = []
    for k in range(4):
        (x0, z0), (x1, z1) = tips[k], tips[(k + 1) % 4]
        pts += [(x0, z0), ((x0 + x1) / 2 * waist, (z0 + z1) / 2 * waist)]
    for _ in range(rounds):                                              # corner cutting: rounds every corner
        pts = [q for i in range(len(pts)) for q in (
            (0.75 * pts[i][0] + 0.25 * pts[(i + 1) % len(pts)][0], 0.75 * pts[i][1] + 0.25 * pts[(i + 1) % len(pts)][1]),
            (0.25 * pts[i][0] + 0.75 * pts[(i + 1) % len(pts)][0], 0.25 * pts[i][1] + 0.75 * pts[(i + 1) % len(pts)][1]))]
    k = r / max(z for _, z in pts)                                       # the cutting shrank it: back to radius r
    return [(x * k, z * k) for x, z in pts]


def puff_into(bm, pts, thick, y=0.0, rings=8):
    """Inflate an outline (one that can be seen whole from its middle) into a pillow: flat edge, domed front and back."""
    made = []
    rim = [bm.verts.new((x, y, z)) for x, z in pts]
    n = len(pts)
    for sign in (-1, 1):                                                 # -1: the front, toward the camera
        prev = rim
        for k in range(1, rings + 1):
            a = math.pi / 2 * k / rings
            sc_, yy = math.cos(a), y + sign * thick * math.sin(a)
            if k == rings:
                c = bm.verts.new((0.0, yy, 0.0))
                made += [bm.faces.new((prev[i], prev[(i + 1) % n], c)) for i in range(n)]
            else:
                ring = [bm.verts.new((x * sc_, yy, z * sc_)) for x, z in pts]
                made += [bm.faces.new((prev[i], prev[(i + 1) % n], ring[(i + 1) % n], ring[i])) for i in range(n)]
                prev = ring
    bmesh.ops.recalc_face_normals(bm, faces=made)
    return made


def grown(pts, d, limit=3.2):
    """The outline pushed outward by d everywhere (pts anticlockwise), so an edge drawn behind it is one even width."""
    if sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(len(pts))) < 0:
        pts = pts[::-1]                                                     # make it anticlockwise
    out = []
    for i, (x, z) in enumerate(pts):
        (xa, za), (xb, zb) = pts[i - 1], pts[(i + 1) % len(pts)]
        n1 = (z - za, -(x - xa)); n2 = (zb - z, -(xb - x))
        l1, l2 = math.hypot(*n1) or 1.0, math.hypot(*n2) or 1.0
        n1 = (n1[0] / l1, n1[1] / l1); n2 = (n2[0] / l2, n2[1] / l2)
        mx, mz = n1[0] + n2[0], n1[1] + n2[1]
        ml = math.hypot(mx, mz) or 1.0
        mx, mz = mx / ml, mz / ml
        k = min(1.0 / max(mx * n1[0] + mz * n1[1], 1e-3), limit)
        out.append((x + mx * d * k, z + mz * d * k))
    return out


def stroke_into(bm, paths, r, y=0.0, caps=8):
    """Thick round-ended strokes along paths (lists of (x, z)), as quad strips: arcs, spirals, crosses, letters.
    A filled n-gon cannot hold a spiral; a strip can, and it has enough vertices to wrap onto his face."""
    for path in paths:
        left, right = [], []
        for i, (x, z) in enumerate(path):
            x0, z0 = path[max(i - 1, 0)]; x1, z1 = path[min(i + 1, len(path) - 1)]
            d = math.hypot(x1 - x0, z1 - z0) or 1.0
            nx, nz = -(z1 - z0) / d, (x1 - x0) / d
            left.append(bm.verts.new((x + nx * r, y, z + nz * r)))
            right.append(bm.verts.new((x - nx * r, y, z - nz * r)))
        for i in range(len(path) - 1):
            bm.faces.new((left[i], left[i + 1], right[i + 1], right[i]))
        for a, b in ((path[0], path[1]), (path[-1], path[-2])):                       # a round cap on each end
            ang = math.atan2(a[1] - b[1], a[0] - b[0])
            c = bm.verts.new((a[0], y, a[1]))
            ring = [bm.verts.new((a[0] + r * math.cos(ang - math.pi / 2 + math.pi * k / caps), y,
                                  a[1] + r * math.sin(ang - math.pi / 2 + math.pi * k / caps))) for k in range(caps + 1)]
            for k in range(caps):
                bm.faces.new((c, ring[k], ring[k + 1]))


def finish(bm, name, mats, parent, loc, wrap, offset, hidden):
    loc = tuple(float(c) for c in loc)
    bm.normal_update()
    solid = bm.faces.layers.int.get("solid")
    for f in bm.faces:                                   # every flat face looks at the camera side (-Y)
        if f.normal.y > 0 and not (solid and f[solid]):
            f.normal_flip()
    m = bpy.data.meshes.new(name)
    bm.to_mesh(m); bm.free()
    o = bpy.data.objects.new(name, m)
    o.parent = parent
    o.location = loc
    o["base"] = list(loc)                                 # where it rests, so an animation can move it and come back
    for mt_ in mats:
        m.materials.append(mt_)
    coll.objects.link(o)
    if wrap:
        sw = o.modifiers.new("onto_face", 'SHRINKWRAP')
        sw.target = body
        sw.wrap_method = 'PROJECT'
        sw.use_project_x, sw.use_project_y, sw.use_project_z = False, True, False
        sw.use_positive_direction, sw.use_negative_direction = True, False
        sw.offset = offset
    if hidden:
        o.scale = (0.0, 0.0, 0.0)
    return o


def stroke_piece(name, paths, r, mat, parent, offset=OFFSET, hidden=True):
    """One eye shape drawn as a stroke, pressed onto his face."""
    bm = bmesh.new()
    stroke_into(bm, paths, r)
    return finish(bm, name, [mat], parent, (0, 0, 0), True, offset, hidden)


EDGE = 0.0065        # the dark edge round a floating mark, in metres; marks pressed on his face get a finer one


def _mark_mesh(parts, wrap):
    bm = bmesh.new()
    mats = []
    done = bm.faces.layers.int.new("part")
    solid = bm.faces.layers.int.new("solid")
    for k, part in enumerate(parts):
        kind, data, mat_ = part[:3]
        if mat_ not in mats:
            mats.append(mat_)
        y = 0.0 if wrap else -0.002 * k
        if kind == "puff":
            for fc in puff_into(bm, data, part[3], y):
                fc[solid] = 1
                fc.smooth = True
        elif kind == "fan":                   # a flat fill made as wedges from the middle: safe for a deeply notched star
            c = bm.verts.new((0.0, y, 0.0))
            vs = [bm.verts.new((x, y, z)) for x, z in data]
            for i in range(len(vs)):
                bm.faces.new((c, vs[i - 1], vs[i]))
        elif kind == "fill":
            f = bm.faces.new([bm.verts.new((x, y, z)) for x, z in data])
            new = bmesh.ops.triangulate(bm, faces=[f])["faces"]
            if wrap:
                bmesh.ops.subdivide_edges(bm, edges=list({e for fc in new for e in fc.edges}), cuts=2, use_grid_fill=True)
        else:
            stroke_into(bm, data, part[3], y)
        for fc in bm.faces:
            if fc[done] == 0:
                fc.material_index = mats.index(mat_)
                fc[done] = k + 1
    return bm, mats


MARK_SIZE = 1.4      # Elaine, 2026-11-26: "can you make all particle effects larger". Every mark is drawn this much bigger


def mark(name, at, parts, parent, wrap=False, offset=OFFSET, hidden=True, edge="auto", size=None):
    """A mark made of flat parts, its origin at `at` (X, Z) so it can pop, pulse and turn about its own centre.
    parts: ("fill", outline, material) or ("stroke", paths, material, half_width), in metres around `at`.
    wrap=True presses it onto his body; otherwise it floats on a plane just in front of him, later parts in front.
    Every coloured part gets a thin dark edge (Elaine, 2026-11-26: "for all of the elements like tear drops and music
    notes and like laughin and stuff can we have outlines"): the same shapes, a little bigger, in navy, behind
    all the colour. Parts that are navy already need none. edge=None leaves it off."""
    size = MARK_SIZE if size is None else size
    parts = [(p_[0], scaled(p_[1], size), p_[2]) if p_[0] in ("fill", "fan") else
             (p_[0], scaled(p_[1], size), p_[2], p_[3] * size) if p_[0] == "puff" else
             (p_[0], [scaled(path, size) for path in p_[1]], p_[2], p_[3] * size) for p_ in parts]
    d = (EDGE if not wrap else 6.0 * SC) if edge == "auto" else edge
    d = d and d * (1 + 0.4 * (size - 1))
    rim = []
    if d:
        for part in parts:
            if part[2] is M_NAVY:
                continue
            rim.append(("fill", grown(part[1], d), M_NAVY) if part[0] == "fill" else
                       ("fan", grown(part[1], d), M_NAVY) if part[0] == "puff" else ("stroke", part[1], M_NAVY, part[3] + d))
    if wrap and rim:                       # pressed on: the edge is its own object underneath, the colour rides on it
        bm, mats = _mark_mesh(rim, True)
        o = finish(bm, name, mats, parent, (at[0], 0.0, at[1]), True, offset, hidden)
        bm, mats = _mark_mesh(parts, True)
        finish(bm, name.replace("SOL_mark_", "SOL_marksub_"), mats, o, (0.0, 0.0, 0.0), True, offset + 0.003, False)
        return o
    bm, mats = _mark_mesh(rim + list(parts), wrap)
    return finish(bm, name, mats, parent, (at[0], 0.0, at[1]), wrap, offset, hidden)


M_PINK = material("SOL_eye_pink", (0.96, 0.33, 0.47))
M_BLUSH = material("SOL_mark_blush", (0.97, 0.55, 0.52))
M_WATER = material("SOL_mark_water", (0.55, 0.82, 0.98))
M_RED = material("SOL_mark_red", (1.0, 0.16, 0.12))
M_DARKRED = material("SOL_mark_darkred", (0.13, 0.03, 0.07))      # the near-black edge of the anger mark
M_YELLOW = material("SOL_mark_yellow", (1.0, 0.82, 0.14))
M_BLUE = material("SOL_mark_blue", (0.30, 0.38, 0.92))
M_LAV = material("SOL_mark_lavender", (0.74, 0.72, 0.92))
M_GREY = material("SOL_mark_grey", (0.48, 0.49, 0.58))
M_PETAL = material("SOL_mark_petal", (0.99, 0.60, 0.74))

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
    # ---- more eye shapes (2026-11-26, Elaine: "angry and sad ... and all other emotions that one could need") ----
    inner = 1 if side == "L" else -1                    # which way the middle of his face is from this eye
    # ANGRY, her design: "like the OO circle eyes but like they're cut so like its two semicircles that rotate down
    # into the middle". The lower part of the ring eye, its flat edge tilted down toward the middle of his face.
    # SAD is the same cut ring tilted the other way, down toward the outside.
    for nm, tilt in (("angry", -24 * inner), ("sad", 20 * inner)):
        piece(f"SOL_eye_{side}_{nm}", shift(rotate(half_disc(r, cut=-0.12 * r), tilt), 0, 0.30 * r), M_NAVY, rig, hidden=True)
        piece(f"SOL_eye_{side}_{nm}_white", shift(rotate(half_disc(0.62 * r, cut=0.14 * r), tilt), 0, 0.30 * r), M_WHITE, rig,
              offset=OFFSET + 0.003, hidden=True)
    # HALF: sleepy, smug, unimpressed. His normal eye with the top part shut
    piece(f"SOL_eye_{side}_half", [(x, z) for x, z in oval if z <= 0.06 * h], M_NAVY, rig, hidden=True)
    # DOME: smug. Elaine, 2026-11-26: "for smug can u turn the eyes around 180 so its like upsidedown gumdrops".
    # The half eye turned half a turn: flat edge at the bottom, round on top, set back down to eye level.
    piece(f"SOL_eye_{side}_dome", [(-x, -z - 0.22 * h) for x, z in oval if z <= 0.06 * h], M_NAVY, rig, hidden=True)
    # ARC "^ ^": happy.   CLOSED "u u": content, asleep
    stroke_piece(f"SOL_eye_{side}_arc", [arc_path(0.62 * w, 25, 155, cz_=-0.30 * h)], 0.105 * h, M_NAVY, rig)
    stroke_piece(f"SOL_eye_{side}_closed", [arc_path(0.62 * w, 205, 335, cz_=0.24 * h)], 0.105 * h, M_NAVY, rig)
    # U "u u": sad. Elaine, 2026-11-26: "we do two U's like uu" (after "can the sad and crying just be the black eyes
    # without the white inners"). A real letter U, deeper than the shallow closed arc above, so the two do not mix.
    ua, ut = 0.50 * w, 0.20 * h
    u_path = line((-ua, ut), (-ua, 0.0), 3)[:-1] + arc_path(ua, 180, 360, n=18) + line((ua, 0.0), (ua, ut), 3)[1:]
    stroke_piece(f"SOL_eye_{side}_u", [shift(u_path, 0, (ua - ut) / 2)], 0.105 * h, M_NAVY, rig)
    # SPIRAL: dizzy
    turns, n_sp = 2.1, 70
    spiral = [((0.02 + 0.50 * i / n_sp) * h * math.cos(2 * math.pi * turns * i / n_sp), (0.02 + 0.50 * i / n_sp) * h * math.sin(2 * math.pi * turns * i / n_sp))
              for i in range(n_sp + 1)]
    stroke_piece(f"SOL_eye_{side}_spiral", [spiral], 0.052 * h, M_NAVY, rig)
    # CROSS "X X": knocked out
    k = 0.34 * h
    stroke_piece(f"SOL_eye_{side}_cross", [line((-k, k), (k, -k)), line((-k, -k), (k, k))], 0.095 * h, M_NAVY, rig)
    # HEART: love
    piece(f"SOL_eye_{side}_heart", heart(0.52 * h), M_PINK, rig, hidden=True)
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

# ---------------------------------------------------------------------------------------------------------------
# MARKS (2026-11-26). Elaine: "all other emotions that one could need", with a game's reaction list as the kind of
# thing she means, and "use these stars for like awe stricken ... dont use the lines just the stars". These are the
# usual comic marks (sweat drop, tears, anger vein, sparkles, light bulb, notes, Zs), drawn here as our own shapes.
# Each mark is SOL_mark_<name>_<n>, hidden at scale 0; eyes_rig.py shows and animates them.
#   on his body (pressed on like the eyes):  blush, tear, sweat, vein
#   floating on a flat plane just in front of him:  everything else
SC = abs(ax) / W                                           # metres per pixel of the front art
X0, X1, Z0, Z1 = co[:, 0].min(), co[:, 0].max(), co[:, 2].min(), co[:, 2].max()
HW, HH, XC = (X1 - X0) / 2, Z1 - Z0, (X0 + X1) / 2
FRONT_Y = co[:, 1].min() - 0.015
print(f"BODY x {X0:.3f}..{X1:.3f}  z {Z0:.3f}..{Z1:.3f}  front y {co[:, 1].min():.3f}")
on_body = empty("RIG_Sol_marks", (0, Y_PLANE, 0), rig_body)
floats = empty("RIG_Sol_marks_float", (0, FRONT_Y, 0), rig_body)


def spot(u, v):
    """A place around him: u in half-widths from his middle (-1 and 1 are his sides), v in heights (0 feet, 1 top)."""
    return XC + u * HW, Z0 + v * HH


def circle(r, n=24, cx=0.0, cz_=0.0):
    return ellipse(r, r, n, cx, cz_)


# --- on his body ---
for i, x_px in enumerate((448, 902)):                        # BLUSH: a soft oval under the outside of each eye
    mark(f"SOL_mark_blush_{i}", px(x_px, 1300), [("fill", ellipse(54 * SC, 24 * SC, n=28), M_BLUSH)], on_body, wrap=True, edge=None, size=1.0)   # a soft flush: no edge
for i, x_px in enumerate((517, 832)):                        # TEAR: a drop under each eye
    mark(f"SOL_mark_tear_{i}", px(x_px, 1322), [("fill", drop(52 * SC, 108 * SC), M_WATER)], on_body, wrap=True, offset=OFFSET + 0.003)
mark("SOL_mark_sweat_0", px(1010, 850), [("fill", drop(72 * SC, 146 * SC), M_WATER)], on_body, wrap=True)     # SWEAT: one drop on his temple
# VEIN: the anger mark. Elaine's reference: four thin red curves with a dark edge, bowed in toward a middle point.
v = 92 * SC
vein = [arc_path(v, d + 180 - 40, d + 180 + 40, n=14, cx=1.75 * v * math.cos(math.radians(d)), cz_=1.75 * v * math.sin(math.radians(d))) for d in (45, 135, 225, 315)]
vo = mark("SOL_mark_vein_0", px(975, 760), [("stroke", vein, M_DARKRED, 13.5 * SC)], on_body, wrap=True, edge=None, size=1.25)   # its edge is this dark stroke
vi_ = mark("SOL_marksub_vein_red", (0, 0), [("stroke", vein, M_RED, 7.0 * SC)], vo, wrap=True, offset=OFFSET + 0.003, hidden=False, edge=None, size=1.25)
vi_.location = (0, 0, 0)

# --- floating ---
# STARS (awe): yellow four-point stars around him. Her reference image, the stars only.
# Elaine's notes, 2026-11-26: first "the awe stars look weird" (stubby flat stars that tilted), then on the slim flat
# sparkles "the stars are still kind of fucked lets see if we can make the star shape and then inflate them". So each
# star is now a real solid: a soft rounded star outline puffed out front and back like his own body, with the dark
# edge as a flat plate behind it. Always upright.
for i, (u, vv, rad) in enumerate(((-1.14, 1.00, 0.110), (1.19, 0.90, 0.085), (-1.30, 0.52, 0.068), (1.30, 0.45, 0.098), (-0.60, 1.21, 0.058), (0.70, 1.22, 0.072))):
    sp_ = puffy_star(rad)
    mark(f"SOL_mark_stars_{i}", spot(u, vv), [("puff", sp_, M_YELLOW, 0.34 * rad)], floats, edge=0.0065)
# BURST: yellow dashes fanning out above his shoulders, a set on each side (excited, laughing, amazed).
# Elaine, 2026-11-26: "can these be like tapered out like the tip of an exclamation mark yk also put it closer to sol's
# body". Each dash is a wedge: thin at the end near him, widening to a round fat end, like the bar of a "!". The sets
# sit just above the tips of his side lobes (they were a hand's width higher, as even round-ended strokes).
def wedge(a, r0, r1, w0, w1, n=10):
    """A tapered dash along direction a (radians) from distance r0 (half-width w0) out to r1 (half-width w1)."""
    c, s_ = math.cos(a), math.sin(a)
    far = [(r1 + w1 * math.cos(t), w1 * math.sin(t)) for t in (math.pi * (k / n - 0.5) for k in range(n + 1))]
    near = [(r0 - w0 * math.cos(t), -w0 * math.sin(t)) for t in (math.pi * (k / n - 0.5) for k in range(n + 1))]
    return [(x * c - z * s_, x * s_ + z * c) for x, z in far + near]


for i, sgn in enumerate((-1, 1)):
    parts = []
    for ang, r0, r1 in ((110, 0.030, 0.115), (135, 0.036, 0.165), (160, 0.030, 0.115)):
        parts.append(("fill", wedge(math.radians(ang if sgn < 0 else 180 - ang), r0, r1, 0.0055, 0.0185), M_YELLOW))
    mark(f"SOL_mark_burst_{i}", spot(0.62 * sgn, 0.80), parts, floats)
# FLOWERS: small five-petal flowers around him (joy)
for i, (u, vv, k, pm) in enumerate(((-1.14, 0.93, 1.35, M_PETAL), (1.18, 0.74, 1.1, M_PETAL), (0.86, 1.14, 0.95, M_WHITE), (-1.24, 0.50, 0.85, M_WHITE))):
    parts = [("fill", circle(0.030 * k, cx=0.036 * k * math.cos(math.radians(90 + 72 * j)), cz_=0.036 * k * math.sin(math.radians(90 + 72 * j))), pm) for j in range(5)]
    mark(f"SOL_mark_flowers_{i}", spot(u, vv), parts + [("fill", circle(0.022 * k), M_YELLOW)], floats)
# EXCLAIM "!" and QUESTION "?" above his shoulder
mark("SOL_mark_exclaim_0", spot(0.98, 1.13), [("fill", [(-0.026, 0.11), (0.026, 0.11), (0.014, -0.005), (-0.014, -0.005)], M_NAVY),
                                             ("fill", circle(0.021, cz_=-0.05), M_NAVY)], floats)
qr = 0.045
mark("SOL_mark_question_0", spot(0.98, 1.13), [("stroke", [arc_path(qr, 165, -70, n=22, cz_=0.06) + [(0.002, -0.022)]], M_NAVY, 0.015),
                                              ("fill", circle(0.021, cz_=-0.07), M_NAVY)], floats)
# BULB: an idea. Elaine, 2026-11-26: "the lightbulb is rly weird ... can we make the metal part like a octagon like
# rectangle octagon" (a rectangle with cut corners, picture v10), then "lets make it a trapezoid the longer side is
# toucing the circle and then move the lightbulb closer to ignite". So the grey base is a trapezoid, wide where it
# meets the glass and narrower below, and the bulb sits nearer his body (it was at spot(0.98, 1.12)).
mark("SOL_mark_bulb_0", spot(0.74, 0.97), [("fill", [(-0.024, -0.090), (0.024, -0.090), (0.043, -0.030), (-0.043, -0.030)], M_GREY),
                                          ("fill", circle(0.062, n=32, cz_=0.022), M_YELLOW),
                                          ("fill", ellipse(0.014, 0.022, n=16, cx=-0.024, cz_=0.040), M_WHITE),
                                          ("stroke", [[(0.0, 0.112), (0.0, 0.150)], [(-0.074, 0.082), (-0.102, 0.108)], [(0.074, 0.082), (0.102, 0.108)]], M_YELLOW, 0.010)], floats)
# DOTS: "..." thinking, three dots that come one by one
for i in range(3):
    mark(f"SOL_mark_dots_{i}", spot(0.70 + 0.27 * i, 1.10 + 0.045 * i), [("fill", circle(0.017 + 0.004 * i), M_NAVY)], floats)
# NOTES: two music notes (singing, glee)
for i, (u, vv, k, nm_) in enumerate(((-1.16, 0.95, 1.0, M_PINK), (1.18, 0.80, 0.8, M_BLUE))):
    head = rotate(ellipse(0.034 * k, 0.025 * k, n=20), 20)
    stem = [(0.028 * k, 0.008 * k), (0.028 * k, 0.125 * k)]
    flag = [(0.028 * k, 0.125 * k), (0.060 * k, 0.100 * k), (0.066 * k, 0.065 * k)]
    mark(f"SOL_mark_notes_{i}", spot(u, vv), [("fill", head, nm_), ("stroke", [stem, flag], nm_, 0.0085 * k)], floats)
# ZZZ: asleep, three Zs that grow as they rise
for i, (dx, dz, k) in enumerate(((0.0, 0.0, 0.020), (0.085, 0.085, 0.029), (0.200, 0.200, 0.040))):
    x_, z_ = spot(0.62, 1.03)
    mark(f"SOL_mark_zzz_{i}", (x_ + dx, z_ + dz), [("stroke", segs([(-k, k), (k, k), (-k, -k), (k, -k)]), M_NAVY, 0.24 * k)], floats)
# BROKEN HEART
mark("SOL_mark_brokenheart_0", spot(0.98, 1.10), [("fill", heart(0.098), M_PINK),
                                                 ("stroke", segs([(0.0, 0.044), (0.026, 0.010), (-0.021, -0.018), (0.013, -0.050), (0.0, -0.089)]), M_WHITE, 0.008)], floats)
# SHIVER: a blue zigzag on each side (scared, cold)
zig = [(0.0, 0.085), (0.024, 0.050), (-0.024, 0.016), (0.024, -0.018), (-0.024, -0.052), (0.0, -0.085)]
for i, sgn in enumerate((-1, 1)):
    mark(f"SOL_mark_shiver_{i}", spot(1.22 * sgn, 0.60), [("stroke", segs(zig), M_BLUE, 0.0085)], floats)
# PUFF: a sigh
mark("SOL_mark_puff_0", spot(-1.40, 0.42), [("fill", circle(0.036, cx=c[0], cz_=c[1]), M_LAV) for c in ((-0.036, 0.0), (0.036, 0.004), (0.0, 0.026), (0.0, -0.012))] +
     [("fill", circle(0.014, cx=0.075, cz_=-0.035), M_LAV)], floats)
# SPRAY: three drops flying off him (panic, distress)
for i, (u, vv, turn, k) in enumerate(((-1.02, 1.02, -125, 1.45), (1.04, 1.00, 125, 1.3), (-1.28, 0.72, -100, 1.1))):
    mark(f"SOL_mark_spray_{i}", spot(u, vv), [("fill", rotate(drop(0.050 * k, 0.105 * k), turn), M_WATER)], floats)

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
# "make sol like have the red gradient instead of purple" (Elaine, 2026-11-26, for angry): dial "shade_red" turns
# the shade from indigo (0) to a hot deep red (1)
RED = (0.66, 0.02, 0.04)
tint = nt.nodes.new("ShaderNodeMix"); tint.data_type = 'RGBA'; tint.name = "shade_tint"
red_dial = nt.nodes.new("ShaderNodeValue"); red_dial.name = red_dial.label = "shade_red"; red_dial.outputs[0].default_value = 0.0
nt.links.new(red_dial.outputs[0], tint.inputs[0])
tint.inputs[6].default_value = tuple(c ** 2.2 for c in PURPLE) + (1,)
tint.inputs[7].default_value = tuple(c ** 2.2 for c in RED) + (1,)
nt.links.new(tint.outputs[2], mix.inputs[7])
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
btint = bn.nodes.new("ShaderNodeMix"); btint.data_type = 'RGBA'
bred = bn.nodes.new("ShaderNodeValue"); bred.name = bred.label = "shade_red"; bred.outputs[0].default_value = 0.0
bn.links.new(bred.outputs[0], btint.inputs[0])
btint.inputs[6].default_value = tuple(c ** 2.2 for c in PURPLE) + (1,)
btint.inputs[7].default_value = tuple(c ** 2.2 for c in RED) + (1,)
bn.links.new(btint.outputs[2], bmix.inputs[7])
bn.links.new(bmix.outputs[2], bbsdf.inputs["Base Color"])
body.data.materials[1] = back

print("EYES", json.dumps(info))
json.dump(info, open(os.path.join(HERE, "eye-metrics.json"), "w"), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "sol-eyes.blend"), copy=True)
print("SAVED", os.path.join(HERE, "sol-eyes.blend"))
