"""Headless skeleton renderer for the "All Due This Week" ad (LANDSCAPE: skeleton 1280x720, lettering 1920x1080).

Usage:  Blender -b --factory-startup --python render_clip.py -- <clip> <out.mp4> [frames "a-b" or "a,b,c"] [stills_dir]
  no frame list : render the whole clip to <out.mp4>, 1280x720 at 24 fps (this is what the painter gets)
  frame list    : write only those PNG stills (for checking) and no mp4. SHOWOVL=1 also shows the lettering planes.
  MODE=ovlseq   : render ALL lettering planes together, with alpha, for every frame into ../overlays/<clip>/seq/
                  (for a shot whose camera moves; use the same SKEL_FPS as the skeleton that gets painted)
  MODE=ovl      : render every OVL_ lettering plane ALONE, with alpha, at 1920x1080, into ../overlays/<clip>/,
                  and write anchors.json (where the named anchor points land on a 1920x1080 screen).
                  OVLFRAME picks the frame (default: the last one). The cameras in lettering shots do not move.
"""
import bpy, sys, os, subprocess, shutil, tempfile, json

argv = sys.argv[sys.argv.index("--") + 1:]
WHICH, OUT = argv[0], argv[1]
FRAMES = argv[2] if len(argv) > 2 and argv[2] != "-" else None
STILLS = argv[3] if len(argv) > 3 else None

HERE = os.path.dirname(os.path.abspath(__file__))
RIG_DIR = HERE
ns = {"RIG_DIR": RIG_DIR, "__name__": "skel"}
exec(compile(open(os.path.join(HERE, "rig.py")).read(), "rig.py", "exec"), ns)
CLIPS = os.environ.get("CLIPS", "clips.py")
exec(compile(open(os.path.join(HERE, CLIPS)).read(), CLIPS, "exec"), ns)
info = ns["clip" + WHICH]()
sc = ns["S"]["sc"]
sc.render.image_settings.file_format = "PNG"

if os.environ.get("MODE") == "ovl":
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    d = os.path.join(HERE, "..", "overlays", WHICH)
    os.makedirs(d, exist_ok=True)
    sc.frame_set(int(os.environ.get("OVLFRAME", sc.frame_end)))
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = 'RGBA'
    try:
        sc.eevee.taa_render_samples = 32
    except Exception:
        pass
    ovl = [o for o in sc.objects if o.name.startswith("OVL_")]
    for o in sc.objects:
        o.hide_render = True
    for o in ovl:
        o.hide_render = False
        sc.render.filepath = os.path.join(d, o.name[4:] + ".png")
        bpy.ops.render.render(write_still=True)
        o.hide_render = True
    anchors = {}
    for name, p in ns["S"]["anchors"].items():
        v = world_to_camera_view(sc, sc.camera, Vector(p))
        anchors[name] = [round(v.x * 1920, 1), round((1 - v.y) * 1080, 1)]
    json.dump(anchors, open(os.path.join(d, "anchors.json"), "w"), indent=1)
    print("OVERLAYS", [o.name for o in ovl], anchors)
elif os.environ.get("MODE") == "ovlseq":
    # every lettering plane together, with alpha, for EVERY frame: for a shot whose camera moves (clip 8)
    d = os.path.join(HERE, "..", "overlays", WHICH, "seq")
    os.makedirs(d, exist_ok=True)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = 'RGBA'
    if os.environ.get("OVLEND"):
        sc.frame_end = min(sc.frame_end, int(os.environ["OVLEND"]))
    for o in sc.objects:
        if o.name.startswith("OVL_"):
            o.hide_render = False
        elif o.type == 'MESH' and not o.name.startswith("FX_"):
            o.is_holdout = True          # hides the lettering behind whatever stands in front of it (Sol, a box wall)
        else:
            o.hide_render = o.type not in ('LIGHT', 'CAMERA', 'EMPTY')
    try:
        sc.eevee.taa_render_samples = 8
    except Exception:
        pass
    sc.render.filepath = os.path.join(d, "f_")
    bpy.ops.render.render(animation=True)
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    track = {}
    for name, ob in ns["S"].get("follow", {}).items():
        pts = []
        for f in range(sc.frame_start, sc.frame_end + 1):
            sc.frame_set(f)
            v = world_to_camera_view(sc, sc.camera, ob.matrix_world.translation)
            pts.append([round(v.x * 1920, 1), round((1 - v.y) * 1080, 1)])
        track[name] = pts
    json.dump(track, open(os.path.join(HERE, "..", "overlays", WHICH, "follow.json"), "w"))
    print("OVLSEQ", info)
elif os.environ.get("MODE") == "mask":
    # Sol's silhouette, white on black, every frame: lets the lettering pass BEHIND him where he stands in front of it
    d = os.path.join(HERE, "..", "overlays", WHICH)
    os.makedirs(d, exist_ok=True)

    def flat(name, v):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        for n_ in list(nt.nodes):
            nt.nodes.remove(n_)
        em, out = nt.nodes.new("ShaderNodeEmission"), nt.nodes.new("ShaderNodeOutputMaterial")
        em.inputs["Color"].default_value = (v, v, v, 1)
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        return m
    white, black = flat("MASK_white", 1.0), flat("MASK_black", 0.0)
    PREFIX = os.environ.get("MASKPREFIX", "SOL_")            # which objects are white: Sol by default, or e.g. PRP_lit_
    MASKNAME = os.environ.get("MASKNAME", "mask")
    for o in sc.objects:
        if o.type != 'MESH' or o.name.startswith("OVL_"):
            continue
        o.data = o.data.copy()
        o.data.materials.clear()
        o.data.materials.append(white if o.name.startswith(PREFIX) else black)
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 960, 540, 100
    tmp = tempfile.mkdtemp(prefix="mask_")
    sc.render.filepath = os.path.join(tmp, "f_")
    bpy.ops.render.render(animation=True)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-framerate", str(ns["FPS"]), "-i", os.path.join(tmp, "f_%04d.png"),
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", os.path.join(d, MASKNAME + ".mp4")])
    shutil.rmtree(tmp)
    print("MASK", info)
elif FRAMES:
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
    if os.environ.get("SHOWOVL"):
        for o in sc.objects:
            if o.name.startswith("OVL_"):
                o.hide_render = False
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
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
    tmp = tempfile.mkdtemp(prefix="skel_")
    sc.render.filepath = os.path.join(tmp, "f_")
    bpy.ops.render.render(animation=True)
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-framerate", str(ns["FPS"]), "-i", os.path.join(tmp, "f_%04d.png"),
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", OUT])
    shutil.rmtree(tmp)
    print("RENDERED", OUT, info)
