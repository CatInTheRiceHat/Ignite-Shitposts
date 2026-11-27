"""Render the expression sheet for Sol's separate eyes.

Run:  Blender -b sol-eyes.blend --python render_expressions.py -- <out_dir> [pose names, to render only those]
Writes one PNG per pose into out_dir; make_sheet.py <out_dir> <sheet.png> lays them out with labels.
"""
import bpy, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index("--") + 1]
os.makedirs(OUT, exist_ok=True)
exec(compile(open(os.path.join(HERE, "eyes_rig.py")).read(), "eyes_rig.py", "exec"))

sc = bpy.data.scenes.new("expressions")
bpy.context.window.scene = sc
sc.collection.children.link(bpy.data.collections["SOL"])
sc.render.engine = 'BLENDER_EEVEE'
sc.view_settings.view_transform = 'Standard'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 560, 640, 100
sc.render.image_settings.file_format = 'PNG'
w = bpy.data.worlds.new("sheet_world")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.86, 0.84, 0.80, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
sc.world = w
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", 'SUN'))
sun.data.energy, sun.data.angle = 2.0, math.radians(25)
sun.rotation_euler = (math.radians(50), 0, math.radians(-25))
sc.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.type, cam.data.ortho_scale = 'ORTHO', 1.62          # wide enough for the marks that float around him
sc.collection.objects.link(cam)
sc.camera = cam
eyes = find_eyes(bpy.data.objects)
body_rig = eyes["rig"].parent


def view(deg):
    a = math.radians(deg)
    cam.location = (3 * math.sin(a), -3 * math.cos(a), 0.60)
    cam.rotation_euler = (math.radians(90), 0, a)


# every expression from the front, then the extras: blink, glances, three-quarter views, one mid-bounce
POSES = [(name, dict(expr=name), 0) for name in EXPRESSIONS]
POSES += [("blink", dict(expr="normal", blink=1.0), 0), ("look-side", dict(expr="normal", look=(-1, 0)), 0),
          ("look-up", dict(expr="normal", look=(0, 1)), 0), ("angry-34", dict(expr="angry"), -38),
          ("furious-34", dict(expr="furious"), 38), ("sad-34", dict(expr="sad"), -38), ("awe-34", dict(expr="awe"), 38)]
ONLY = [a for a in sys.argv[sys.argv.index("--") + 2:]]
for k, (name, kw, deg) in enumerate(POSES):
    if ONLY and name not in ONLY:
        continue
    pose_eyes(eyes, **kw)
    body_rig.scale = (1, 1, 1)
    view(deg)
    sc.render.filepath = os.path.join(OUT, f"{k + 1:02d}-{name}.png")
    bpy.ops.render.render(write_still=True)
if not ONLY:
    # and one squashed, to show the eyes ride the body when he bounces
    pose_eyes(eyes, "surprised")
    body_rig.scale = (1.12, 1.12, 0.86)
    view(0)
    sc.render.filepath = os.path.join(OUT, f"{len(POSES) + 1:02d}-surprised-squash.png")
    bpy.ops.render.render(write_still=True)
print("RENDERED", len(POSES) + 1)
