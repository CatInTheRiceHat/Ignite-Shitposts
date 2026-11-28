"""Airflow arrows for the shower-curtain episode (Elaine, 2026-11-27: "can we annimate arrows to further demonstrate the
flow and how air moves?"). Exec'd by render_arrows.py after a clip is built: ARROWS[clip](sc) adds flat arrows to that
clip's scene and keys them on every frame, in world space, so the clip's own camera sees them. Times are clip seconds.
  clip 3  air dragged DOWN beside the spray, then out along the tub floor
  clip 4  the loop: round the wheel between Sol and the far wall (from 1.7 s, when the camera has swung out)
  clip 5  the loop again, and from 3.4 s small weak arrows from its middle toward the curtain
  clip 6  big arrows from the room pushing on the outside of the curtain (0.2-2.6 s, the glide across the rug)
"""
from mathutils import Vector


def _arrow_mesh(name):
    """A flat arrow pointing along +X, 1 long, drawn twice (in XY and in XZ) so it reads from any side."""
    import bmesh as _bm
    pts = [(-0.5, 0.12), (0.08, 0.12), (0.08, 0.30), (0.5, 0.0), (0.08, -0.30), (0.08, -0.12), (-0.5, -0.12)]
    bm = _bm.new()
    bm.faces.new([bm.verts.new((x, y, 0.0)) for x, y in pts])
    bm.faces.new([bm.verts.new((x, 0.0, y)) for x, y in pts])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    m = bpy.data.materials.get("ARROW") or bpy.data.materials.new("ARROW")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    em, out = nt.nodes.new("ShaderNodeEmission"), nt.nodes.new("ShaderNodeOutputMaterial")
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    m.use_backface_culling = False
    me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    o.rotation_mode = 'QUATERNION'
    S["sc"].collection.objects.link(o)
    return o


def _run(sc, tracks):
    """tracks: list of functions t -> (position, direction, length) or None (hidden)."""
    objs = [_arrow_mesh(f"ARW_{i}") for i in range(len(tracks))]
    for f in range(sc.frame_start, sc.frame_end + 1):
        t = (f - 1) / FPS
        for o, fn in zip(objs, tracks):
            r = fn(t)
            if not r or r[2] < 0.01:
                o.location, o.scale = (0, 0, -50), (0.001, 0.001, 0.001)
            else:
                p, d, s = r
                o.location, o.scale = p, (s, s, s)
                o.rotation_quaternion = Vector(d).normalized().to_track_quat('X', 'Y' if abs(d[2]) > 0.9 * Vector(d).length else 'Z')
            for path in ("location", "scale", "rotation_quaternion"):
                o.keyframe_insert(path, frame=f)
    return len(objs)


def _along(path_fn, u, eps=0.004):
    a, b = Vector(path_fn(u)), Vector(path_fn(min(u + eps, 1.0) if u + eps <= 1.0 else u - eps))
    d = (b - a) if u + eps <= 1.0 else (a - b)
    return tuple(a), tuple(d)


def arrows3(sc):
    tr = []
    # left of the spray: down, then out along the floor. Right of it: straight down only (the camera sinks on that side).
    for P in ([(-0.14, 1.10, 2.55), (-0.14, 1.10, 1.45), (-0.14, 1.10, 0.62), (-0.14, 0.97, 0.30), (-0.14, 0.68, 0.24)],
              [(0.57, 1.24, 2.55), (0.57, 1.24, 1.80), (0.57, 1.24, 1.05), (0.57, 1.24, 0.38)]):
        for k in range(3):
            def fn(t, P=P, k=k):
                u = ((t - 1.9) / 2.1 + k / 3.0) % 1.0
                p, d = _along(lambda v: cr(P, v), u)
                return p, d, 0.40 * min(1.0, u / 0.10, (1 - u) / 0.12) * smooth(t, 1.9, 2.3)
            tr.append(fn)
    return _run(sc, tr)


def _wheel(u, x=0.10, a=0.80, b=0.95):
    yc, _, zc, _ = LOOP
    c, s = math.cos(u), math.sin(u)
    return (x, yc + a * math.copysign(abs(c) ** 0.6, c), max(zc + b * math.copysign(abs(s) ** 0.6, s), 0.2))


def _loop_tracks(n, t_in0, t_in1, period=4.0, size=0.46):
    tr = []
    for k in range(n):
        def fn(t, k=k):
            u = TAU * k / n - TAU * t / period
            a, b = Vector(_wheel(u)), Vector(_wheel(u - 0.02))
            return tuple(a), tuple(b - a), size * smooth(t, t_in0, t_in1)
        tr.append(fn)
    return tr


def arrows4(sc):
    return _run(sc, _loop_tracks(7, 1.7, 2.4))


def arrows5(sc):
    tr = _loop_tracks(7, -0.5, 0.0)
    k = 0
    for y in (-0.05, 0.35, 0.75):
        for z in (0.95, 1.55):
            def fn(t, y=y, z=z, k=k):
                u = (t * 0.8 + k * 0.37) % 1.0
                return (-0.22 - 0.42 * u, y, z), (-1, 0, 0), 0.30 * math.sin(math.pi * u) ** 0.7 * smooth(t, 3.3, 3.7)
            tr.append(fn)
            k += 1
    return _run(sc, tr)


def arrows6(sc):
    tr, k = [], 0
    for y in (-1.0, -0.2, 0.6):
        for z in (0.75, 1.5):
            def fn(t, y=y, z=z, k=k):
                u = (t * 0.9 + k * 0.31) % 1.0
                e = u * u * (3 - 2 * u)
                return ((-2.05 + 0.85 * e, y, z), (1, 0, 0),
                        0.62 * min(1.0, u / 0.15, (1 - u) / 0.15) * smooth(t, 0.2, 0.6) * (1 - smooth(t, 2.3, 2.7)))
            tr.append(fn)
            k += 1
    return _run(sc, tr)


ARROWS = {"3": arrows3, "4": arrows4, "5": arrows5, "6": arrows6}
