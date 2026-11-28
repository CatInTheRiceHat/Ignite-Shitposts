"""Render ONLY the airflow arrows of a clip, on a transparent background, from that clip's own camera.

Usage:  Blender -b --factory-startup --python render_arrows.py -- <clip> <out_dir>
Builds the clip exactly as render_clip.py does, makes the set and Sol hold-outs (so an arrow behind Sol or a wall is
cut away), adds the arrows from arrows.py and writes out_dir/a_0001.png ... (720x1280 RGBA at SKEL_FPS).
overlays/composite_arrows.py lays them over the painted clip.
"""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
WHICH, OUT = argv[0], argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {"RIG_DIR": HERE, "__name__": "skel"}
for src in ("rig.py", os.environ.get("CLIPS", "clips.py")):
    exec(compile(open(os.path.join(HERE, src)).read(), src, "exec"), ns)
ns["clip" + WHICH]()
sc = ns["S"]["sc"]
for o in sc.objects:
    if o.type != 'MESH':
        continue
    if o.name.startswith(("FX_", "PRP_puddle")):      # drops, puffs and the puddle: left out, they do not cut the arrows
        o.hide_render = True
    else:
        o.is_holdout = True
exec(compile(open(os.path.join(HERE, "arrows.py")).read(), "arrows.py", "exec"), ns)
print("ARROWS", ns["ARROWS"][WHICH](sc))
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 720, 1280, 100
sc.render.film_transparent = True
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
os.makedirs(OUT, exist_ok=True)
sc.render.filepath = os.path.join(OUT, "a_")
bpy.ops.render.render(animation=True)
print("RENDERED", OUT)
