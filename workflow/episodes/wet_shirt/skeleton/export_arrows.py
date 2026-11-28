"""Work out where each airflow arrow is ON SCREEN for every frame of a clip (no rendering).

Usage:  Blender -b --factory-startup --python export_arrows.py -- <clip> <out.json>
Builds the clip as render_clip.py does (for its camera), then for each frame projects the arrows of arrows2.py
through the camera (arrows.py: light rays, each with its own colour). out.json: {"fps", "size": [720, 1280], "frames": [[{"pts": [[x, y], ...], "alpha", "px", "kind"}, ...], ...]}
with pixel points from tail to head and px = the arrow's width in pixels at that distance.
"""
import bpy, sys, os, json
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
WHICH, OUT = argv[0], argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {"RIG_DIR": HERE, "__name__": "skel"}
for src in ("rig.py", os.environ.get("CLIPS", "clips.py")):
    exec(compile(open(os.path.join(HERE, src)).read(), src, "exec"), ns)
ns["clip" + WHICH]()
exec(compile(open(os.path.join(HERE, "arrows.py")).read(), "arrows.py", "exec"), ns)
sc, FPS = ns["S"]["sc"], ns["FPS"]
W, H = 720, 1280
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
FOCAL = sc.camera.data.lens / sc.camera.data.sensor_width * max(W, H)          # pixels per metre at 1 m
tracks = ns["TRACKS"][WHICH]()
frames = []
for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    t, row = (f - 1) / FPS, []
    for fn in tracks:
        r = fn(t)
        if not r or r["alpha"] < 0.01:
            continue
        pr = [world_to_camera_view(sc, sc.camera, Vector(p)) for p in r["pts"]]
        if min(p.z for p in pr) < 0.25:
            continue                                   # at or behind the lens
        row.append({"pts": [[round(p.x * W, 2), round((1 - p.y) * H, 2)] for p in pr], "alpha": round(r["alpha"], 3),
                    "px": round(r["width"] * FOCAL / pr[-1].z, 2), "rgb": r["rgb"], "clamp": r.get("clamp", (12, 30))})
    frames.append(row)
json.dump({"fps": FPS, "size": [W, H], "frames": frames}, open(OUT, "w"))
print("EXPORTED", OUT, len(frames), "frames", max(len(r) for r in frames), "arrows at most")
