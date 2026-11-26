"""Headless gray-skeleton renderer (no Blender bridge needed).

Usage:  Blender -b --factory-startup --python render_clip.py -- <clip> <out.mp4> [frames "a-b" or "a,b,c"] [stills_dir]
Renders 720x1280 at 30 fps. With a frame list it writes only those PNG stills (for checking) and no mp4.
"""
import bpy, sys, os, subprocess, shutil, tempfile

argv = sys.argv[sys.argv.index("--") + 1:]
WHICH, OUT = argv[0], argv[1]
FRAMES = argv[2] if len(argv) > 2 and argv[2] != "-" else None
STILLS = argv[3] if len(argv) > 3 else None

HERE = os.path.dirname(os.path.abspath(__file__))
RIG_DIR = HERE
ns = {"RIG_DIR": RIG_DIR, "__name__": "skel"}
exec(compile(open(os.path.join(HERE, "rig.py")).read(), "rig.py", "exec"), ns)
CLIPS = os.environ.get("CLIPS", "clips.py")          # CLIPS=clips_v2.py renders version 2
exec(compile(open(os.path.join(HERE, CLIPS)).read(), CLIPS, "exec"), ns)
info = ns["clip" + WHICH]()
sc = ns["S"]["sc"]
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 720, 1280, 100
sc.render.image_settings.file_format = "PNG"

if FRAMES:
    if "-" in FRAMES:
        a, b = FRAMES.split("-")
        frames = list(range(int(a), int(b) + 1))
    else:
        frames = [int(x) for x in FRAMES.split(",")]
    d = STILLS or os.path.dirname(OUT)
    os.makedirs(d, exist_ok=True)
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(d, f"{WHICH}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
    print("STILLS", info)
else:
    tmp = tempfile.mkdtemp(prefix="skel_")
    sc.render.filepath = os.path.join(tmp, "f_")
    bpy.ops.render.render(animation=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", os.path.join(tmp, "f_%04d.png"),
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", OUT])
    shutil.rmtree(tmp)
    print("RENDERED", OUT, info)
