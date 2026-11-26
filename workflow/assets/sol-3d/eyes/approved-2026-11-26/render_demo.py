"""Render a short test clip of Sol changing emotion, with the bounce between each one.

Run:  Blender -b sol-eyes.blend --python render_demo.py -- <frames_dir>
"""
import bpy, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index("--") + 1]
os.makedirs(OUT, exist_ok=True)
exec(compile(open(os.path.join(HERE, "eyes_rig.py")).read(), "eyes_rig.py", "exec"))
FPS = 30
TIMELINE = [(0.0, "normal"), (1.0, "squeeze"), (2.1, "surprised"), (3.2, "shocked"), (4.4, "worried"), (5.6, "sparkle"), (6.8, "normal")]
END = 7.8

sc = bpy.data.scenes.new("demo")
bpy.context.window.scene = sc
sc.collection.children.link(bpy.data.collections["SOL"])
sc.render.engine = 'BLENDER_EEVEE'
sc.view_settings.view_transform = 'Standard'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 560, 640, 100
sc.render.image_settings.file_format = 'PNG'
sc.render.fps = FPS
w = bpy.data.worlds.new("demo_world"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.86, 0.84, 0.80, 1)
sc.world = w
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", 'SUN'))
sun.data.energy, sun.data.angle = 2.0, math.radians(25)
sun.rotation_euler = (math.radians(50), 0, math.radians(-25))
sc.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.type, cam.data.ortho_scale = 'ORTHO', 1.3
cam.location, cam.rotation_euler = (0, -3, 0.52), (math.radians(90), 0, 0)
sc.collection.objects.link(cam); sc.camera = cam
eyes = find_eyes(bpy.data.objects)
body = eyes["rig"].parent
n = int(END * FPS)
for f in range(n):
    t = f / FPS
    expr, squash, size, gloom = emotion_at(t, TIMELINE)
    # a natural blink while he is at rest, so the clip also shows blinking
    blink = 0.0
    for b0 in (0.45, 7.3):
        if b0 <= t < b0 + 0.2:
            blink = math.sin((t - b0) / 0.2 * math.pi)
    pose_eyes(eyes, expr, size=size, gloom=gloom, blink=blink if expr == "normal" else 0.0)
    body.scale = squash_scale(squash)
    sc.render.filepath = os.path.join(OUT, f"f_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
print("RENDERED", n)
