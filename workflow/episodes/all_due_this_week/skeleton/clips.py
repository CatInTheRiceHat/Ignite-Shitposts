"""Skeleton clips for the ad "All Due This Week" (Elaine's script v1). exec()'d after rig.py by render_clip.py.

LANDSCAPE 16:9. In every clip Sol stands on the LEFT THIRD and the stress is on the RIGHT TWO THIRDS; his feet sit
about 70% of the way down the frame so the captions (lower third, centred) have the surface below him to sit on.
Eight paint clips, one per script clip. Times are seconds on each clip's own clock and follow the trimmed takes in
audio/edit/ (voice starts in brackets). Frame counts are written for 30 fps and converted by rig.py (SKEL_FPS=24).
Lettering is never in the skeleton: every OVL_ plane is rendered as its own pass (render_clip.py MODE=ovlseq / ovl)
and laid over the painted clip. Sol never wears goggles (the script allows all clips or none).
Sol is one unit tall. Real things are big next to him: a sheet of paper is about his height.
"""
import random

SOL_D = (-1.75, 1.2, 0)                               # his spot on the desk (clips 1, 2 and 8)
CAM_D = ((0.0, -4.6, 0.75), (0.0, 1.2, 0.60), 40)     # the desk wide: clips 1 and 8 share it exactly
HW_D = (0.3, 1.45)                                    # where the math homework stands on the desk
BX, BZ = 0.35, 1.25                                   # whiteboard centre (the science ad's board)
NOTE = {}                                             # item root name -> its lettering plane


def act(sol, t, f, timeline, gloom=None, look=(0.0, 0.0), blinks=(), blink=None, **pose):
    """Eyes from the emotion timeline (with its bounce), then the body pose with that bounce added."""
    expr, sq, size, g = emotion_at(t, timeline)
    if gloom is not None:
        g = gloom
    bl = blink_at(t, blinks) if expr in ("normal", "worried", "sparkle") else 0.0
    if blink is not None:
        bl = max(bl, blink)
    face(sol, f, expr, blink=bl, look=look, size=size, gloom=g)
    pose["squash"] = pose.get("squash", 0.0) + sq
    pose_sol(sol, **pose)


def aim(cam, tgt, spec):
    cam.location, tgt.location = spec[0], spec[1]


# ================================================================ the things that are due
def build_homework(tag, loc, tall=0.62, neat=False, check=False, pre="PRP_", fit=(1.0, 0.0)):
    """The math homework: a stack of worksheets with a yellow sticky note on its front. One object in every clip."""
    r = empty("RIG_hw_" + tag, loc)
    rnd = random.Random(7)
    n = max(2, int(round(tall / 0.062)))
    for i in range(n):
        dx, rz = (0.0, 0.0) if neat else (rnd.uniform(-0.035, 0.035), D(rnd.uniform(-4, 4)))
        box(f"{pre}hw_{tag}_{i}", "white" if i % 2 else "paper", (dx, 0, tall / n * (i + 0.5)), (0.8, 1.0, tall / n - 0.006), parent=r, rot=(0, 0, rz))
    nz = max(tall * 0.5, 0.2)
    box(f"{pre}hwnote_{tag}", "sticky", (0, -0.53, nz), (0.56, 0.012, 0.38), parent=r)
    # fit = (scale, lift) of the lettering alone: on the short tidy stack the painter draws the note smaller and higher
    # than the skeleton's, and "homework" hung off its bottom edge (frame review of cut v1)
    NOTE[r.name] = overlay_plane("math_" + tag, "note_math.png", (0, -0.545, nz + fit[1]), (0.56 * fit[0], 0.397 * fit[0]), parent=r)
    if check:
        overlay_plane("check_" + tag, "check.png", (0.38, -0.56, nz + fit[1] - 0.02), (0.36, 0.36), parent=r)
    return r


def build_poster(tag, loc, lean=8, pre="PRP_"):
    """The group project: a blank white poster board, 0.9 wide and 1.4 tall, with a blue sticky note near its top."""
    r = empty("RIG_poster_" + tag, loc, rot=(D(-lean), 0, 0))
    box(f"{pre}poster_{tag}", "white", (0, 0, 0.7), (0.9, 0.03, 1.4), parent=r)
    box(f"{pre}posternote_{tag}", "sticky_b", (-0.12, -0.022, 1.14), (0.56, 0.012, 0.38), parent=r)
    NOTE[r.name] = overlay_plane("group_" + tag, "note_group.png", (-0.12, -0.034, 1.14), (0.56, 0.397), parent=r)
    return r


def build_calendar(tag, loc, lean=10, s=1.0, pre="PRP_"):
    """The calendar page: white, a red band across the top, 0.8 wide and 0.9 tall."""
    r = empty("RIG_cal_" + tag, loc, rot=(D(-lean), 0, 0))
    r.scale = (s, s, s)
    box(f"{pre}cal_{tag}", "white", (0, 0, 0.45), (0.8, 0.016, 0.9), parent=r)
    box(f"{pre}calband_{tag}", "red", (0, -0.012, 0.82), (0.8, 0.012, 0.16), parent=r)
    NOTE[r.name] = overlay_plane("test_" + tag, "cal_test.png", (0, -0.022, 0.45), (0.8, 0.889), parent=r)
    return r


def build_music(tag, loc, lean=20, pre="PRP_"):
    """Piano sheet music: one cream page of staves, 0.85 wide and 1.05 tall."""
    r = empty("RIG_music_" + tag, loc, rot=(D(-lean), 0, 0))
    box(f"{pre}music_{tag}", "paper", (0, 0, 0.525), (0.85, 0.016, 1.05), parent=r)
    NOTE[r.name] = overlay_plane("music_" + tag, "music.png", (0, -0.012, 0.525), (0.85, 1.05), parent=r)
    return r


def build_ball(tag, loc, r_=0.36):
    b = empty("RIG_ball_" + tag, loc)
    sphere("PRP_ball_" + tag, "white", (0, 0, 0), (r_, r_, r_), parent=b)
    for i, (x, y, z) in enumerate([(0, -1, 0.15), (0.75, -0.6, -0.3), (-0.75, -0.55, -0.35), (0.45, -0.5, 0.75), (-0.5, -0.45, 0.75),
                                   (0, -0.6, -0.8), (0.95, 0.1, 0.3), (-0.95, 0.1, 0.3), (0, 0.3, 0.95)]):
        n = math.sqrt(x * x + y * y + z * z)
        sphere(f"PRP_ball_patch_{tag}_{i}", "dark", (x / n * 0.21, y / n * 0.21, z / n * 0.21), (0.17, 0.17, 0.17), parent=b)     # flat dark patches
    return b


def strut(tag, parent, h=0.9):
    """A small wooden prop behind a leaning board, so it is not standing by itself."""
    box("PRP_strut_" + tag, "wood_d", (0, 0.2, h * 0.45), (0.07, 0.05, h), parent=parent, rot=(D(-24), 0, 0))


# ================================================================ sets
def build_bedroom():
    """Sol's desk, the science ad's bedroom, framed for landscape: teal wall, window, desk lamp."""
    box("ENV_desk", "wood", (0, -1.2, -0.1), (13, 6.6, 0.2))
    box("ENV_wall", "wall", (0, 2.2, 3.5), (13, 0.2, 10))
    wx, wz = -1.6, 2.3
    box("ENV_window_pane", "sky", (wx, 2.08, wz), (1.9, 0.05, 2.0))
    for nm, loc, size in [("L", (wx - 1.0, 2.04, wz), (0.12, 0.1, 2.24)), ("R", (wx + 1.0, 2.04, wz), (0.12, 0.1, 2.24)),
                          ("B", (wx, 2.0, wz - 1.06), (2.24, 0.2, 0.12)), ("V", (wx, 2.04, wz), (0.07, 0.08, 2.0))]:
        box("ENV_window_" + nm, "trim", loc, size)
    lx, ly = -0.62, 1.85                                # desk lamp, between Sol and the pile, turned toward Sol
    cone("PRP_lamp_base", "teal", (lx, ly, 0), 0.26, 0.22, 0.06)
    cone("PRP_lamp_arm", "teal", (lx, ly, 0.06), 0.03, 0.03, 1.1, rot=(0, D(-12), 0))
    cone("PRP_lamp_shade", "yellow", (lx - 0.19, ly, 1.1), 0.12, 0.3, 0.34, rot=(0, D(-140), 0))


def build_pile():
    """BEFORE: the math homework with the piano music and a soccer ball on top; beside it the group-project poster
    board leaning on the wall with the TEST FRIDAY calendar page leaning in front of it."""
    hw = build_homework("pile", (HW_D[0], HW_D[1], 0))
    music = build_music("pile", (HW_D[0] - 0.14, HW_D[1] + 0.42, 0.62), lean=14)
    ball = build_ball("pile", (HW_D[0] + 0.16, HW_D[1] - 0.12, 0.62 + 0.36))
    poster = build_poster("pile", (1.42, 2.02, 0), lean=5)
    cal = build_calendar("pile", (1.68, 1.82, 0), lean=9)
    # crumpled paper and marker pens at the front corners of the desk, as in the science ad
    for i, (x, y, r) in enumerate([(-2.3, -1.5, 0.12), (2.1, -1.2, 0.1)]):
        sphere(f"PRP_paperball_{i}", "paper", (x, y, r * 0.9), (r, r * 0.92, r * 0.9))
    cone("PRP_pen_blue", "blue", (1.55, -1.75, 0.035), 0.035, 0.035, 0.42, rot=(0, D(90), D(25)))
    cone("PRP_pen_coral", "coral", (-1.9, -0.6, 0.035), 0.035, 0.035, 0.42, rot=(0, D(90), D(-40)))
    return {"hw": hw, "music": music, "ball": ball, "poster": poster, "cal": cal}


def build_floor_room():
    box("ENV_floor", "floor", (0, -1.6, -0.1), (14, 8.4, 0.2))
    box("ENV_wall", "wall", (0, 1.75, 3.5), (14, 0.2, 10))
    box("ENV_baseboard", "trim", (0, 1.635, 0.09), (14, 0.04, 0.18))
    box("ENV_rug", "teal", (1.6, -0.25, 0.01), (6.6, 2.7, 0.02))
    # a low bookshelf against the wall, behind the boxes
    box("PRP_shelf_body", "wood_d", (2.75, 1.42, 0.62), (2.9, 0.4, 1.24))
    box("PRP_shelf_top", "wood", (2.75, 1.4, 1.26), (3.0, 0.46, 0.06))
    rnd = random.Random(2)
    x = 1.45
    while x < 4.05:
        w = rnd.uniform(0.1, 0.17)
        box(f"PRP_shelf_book_{int(x * 100)}", ("coral", "yellow", "blue", "mint", "teal", "pink")[rnd.randrange(6)], (x + w / 2, 1.2, 1.0), (w, 0.06, rnd.uniform(0.28, 0.4)))
        x += w + 0.015


def build_box(tag, x, y, img):
    """An open cardboard box. One piece; it only bounces when something lands in it."""
    r = empty("RIG_box_" + tag, (x, y, 0))
    w, dp, h, t = 1.05, 1.2, 0.58, 0.035      # low, so whatever lands in it stays in sight above the rim (v1's boxes were
    # 0.8 tall: the painter forgot the homework inside one and painted the box empty)
    box("PRP_box_front_" + tag, "cardboard", (0, -dp / 2, h / 2), (w, t, h), parent=r)
    box("PRP_box_back_" + tag, "cardboard_d", (0, dp / 2, h / 2), (w, t, h), parent=r)
    for s in (-1, 1):
        box(f"PRP_box_side{s}_{tag}", "cardboard_d", (s * (w / 2 - t / 2), 0, h / 2), (t, dp, h), parent=r)
    box("PRP_box_bottom_" + tag, "cardboard_d", (0, 0, 0.02), (w, dp, 0.04), parent=r)
    overlay_plane("box_" + tag, img, (0, -dp / 2 - 0.025, h * 0.5), (0.9, 0.3635), parent=r)
    track(r, "location")
    return r


def build_hallway():
    """The science ad's hallway whiteboard, unchanged: frame, board, tray, one blue marker, three small pictures."""
    box("ENV_floor", "floor", (0, -1.6, -0.1), (13, 7.4, 0.2))
    box("ENV_wall", "wall", (0, 1.1, 3.5), (13, 0.2, 10))
    box("ENV_baseboard", "trim", (0, 0.985, 0.09), (13, 0.04, 0.18))
    box("ENV_rug", "teal", (0.1, -0.9, 0.01), (3.4, 2.3, 0.02))
    box("PRP_board_frame", "steel", (BX, 0.975, BZ), (1.92, 0.05, 1.42))
    box("PRP_board", "white", (BX, 0.945, BZ), (1.80, 0.02, 1.30))
    box("PRP_board_tray", "steel", (BX, 0.90, BZ - 0.72), (1.3, 0.13, 0.04))
    cone("PRP_marker", "blue", (BX + 0.2, 0.89, BZ - 0.67), 0.03, 0.03, 0.32, rot=(0, D(90), 0))
    for nm, x, z, key, w, h in (("a", -0.35, 2.95, "coral", 0.62, 0.78), ("b", 0.42, 3.05, "yellow", 0.5, 0.5), ("c", 1.08, 2.92, "mint", 0.56, 0.7)):
        box("PRP_frame_" + nm, "trim", (x, 0.98, z), (w + 0.12, 0.04, h + 0.12))
        box("PRP_picture_" + nm, key, (x, 0.955, z), (w, 0.02, h))
    # the right of the hallway: a door and a potted plant
    box("PRP_door_trim", "trim", (2.95, 0.98, 1.3), (1.5, 0.05, 2.6))
    box("PRP_door", "wood", (2.95, 0.95, 1.24), (1.26, 0.04, 2.48))
    sphere("PRP_door_knob", "yellow", (2.45, 0.9, 1.05), (0.06, 0.06, 0.06))
    cone("PRP_plant_pot", "coral", (1.78, 0.6, 0), 0.17, 0.22, 0.34)
    for i, (dx, dz, k) in enumerate([(0, 0.62, 0.26), (-0.17, 0.5, 0.18), (0.18, 0.52, 0.19), (0.02, 0.86, 0.17)]):
        sphere(f"PRP_plant_leaf_{i}", "leaf", (1.78 + dx, 0.6, 0.34 + dz - 0.2), (k, k * 0.8, k * 1.25))
    overlay_plane("plan_a", "plan_a.png", (BX + 0.33, 0.93, BZ + 0.32), (1.06, 0.54))
    overlay_plane("plan_b", "plan_b.png", (BX + 0.33, 0.93, BZ - 0.31), (1.06, 0.54))


def build_kitchen():
    """The science ad's kitchen (white tiles, one teal stripe), with a wooden table in front of it."""
    box("ENV_table", "wood", (0, -1.2, -0.1), (13, 7.2, 0.2))
    box("ENV_wall", "trim", (0, 3.4, 3.5), (13, 0.2, 10))
    box("ENV_wall_stripe", "teal", (0, 3.29, 1.55), (13, 0.02, 0.16))
    for i in range(1, 9):
        if i != 3:
            box(f"ENV_grout_h{i}", "steel", (0, 3.29, 0.5 * i), (13, 0.02, 0.02))
    for i in range(-10, 11):
        box(f"ENV_grout_v{i}", "steel", (0.62 * i + 0.3, 3.29, 2.1), (0.02, 0.02, 4.2))
    box("ENV_counter", "counter", (0, 2.9, 0.55), (13, 0.8, 1.1))


def build_garden():
    """The pond garden of the course card art, mirrored so the pond fills the right of the frame: Sol's mossy rock,
    a stone lantern, bushes, a maple branch overhead, the far bank in a warm haze."""
    box("ENV_water", "water", (3.0, 2.0, -0.02), (16, 14, 0.04))
    box("ENV_haze", "haze", (0, 11, 4), (40, 0.2, 14))
    box("ENV_far_bank", "grass", (2, 8.6, 0.06), (30, 2.4, 0.2))
    rnd = random.Random(4)
    for i in range(9):                                   # far trees and bushes, pale in the haze
        x = -6 + 2.1 * i + rnd.uniform(-0.4, 0.4)
        k = rnd.uniform(1.0, 1.9)
        sphere(f"ENV_far_bush_{i}", ("bush", "grass", "maple_l")[i % 3], (x, 8.9, 0.5 * k), (1.3 * k, 0.8, 0.8 * k))
    for i, x in enumerate((-1.5, 3.4, 6.4)):
        cone(f"ENV_far_trunk_{i}", "trunk", (x, 9.6, 0), 0.16, 0.1, 3.4)
        sphere(f"ENV_far_crown_{i}", ("grass", "bush", "grass")[i], (x, 9.6, 3.6), (1.7, 1.0, 1.3))
    # the near bank on the left, where Sol sits
    box("ENV_bank", "grass", (-5.2, 2.2, 0.05), (6.6, 12, 0.3))
    sphere("ENV_bank_edge", "moss_d", (-2.2, 1.6, 0.0), (1.5, 3.4, 0.22))
    sphere("PRP_rock_sol", "stone", (-1.5, 0.6, 0.12), (1.15, 0.85, 0.36))
    sphere("PRP_rock_sol_moss", "moss", (-1.56, 0.64, 0.36), (0.95, 0.7, 0.13))
    for i, (x, y, sx, sz) in enumerate([(-0.45, 1.25, 0.42, 0.26), (-2.7, 0.2, 0.5, 0.3), (-0.85, 2.1, 0.55, 0.36), (-3.2, 2.6, 0.8, 0.6)]):
        sphere(f"PRP_rock_{i}", "stone_d", (x, y, sz * 0.5), (sx, sx * 0.8, sz))
        sphere(f"PRP_rock_moss_{i}", "moss", (x - 0.03, y, sz * 0.86), (sx * 0.8, sx * 0.62, sz * 0.4))
    for i, (x, y, k) in enumerate([(-2.35, 2.2, 0.9), (-1.35, 2.75, 0.75), (-3.6, 1.6, 0.8), (-1.6, 3.6, 0.9), (-2.9, 3.4, 1.2)]):
        sphere(f"ENV_bush_{i}", "bush" if i % 2 else "moss_d", (x, y, 0.6 * k), (0.95 * k, 0.75 * k, 0.75 * k))
    lx, ly = -0.35, 2.5                                   # stone lantern, behind him, at the edge of the pond
    cone("PRP_lantern_base", "stone", (lx, ly, 0.15), 0.42, 0.34, 0.2)
    cone("PRP_lantern_post", "stone", (lx, ly, 0.35), 0.17, 0.15, 0.62)
    cone("PRP_lantern_shelf", "stone_d", (lx, ly, 0.97), 0.26, 0.36, 0.12)
    box("PRP_lantern_box", "stone", (lx, ly, 1.3), (0.5, 0.5, 0.44))
    box("PRP_lantern_window", "glow", (lx, ly - 0.255, 1.3), (0.22, 0.02, 0.24))
    cone("PRP_lantern_roof", "stone_d", (lx, ly, 1.5), 0.62, 0.1, 0.34)
    sphere("PRP_lantern_moss", "moss", (lx - 0.1, ly, 1.74), (0.34, 0.34, 0.08))
    sphere("PRP_lantern_top", "stone", (lx, ly, 1.93), (0.11, 0.11, 0.13))
    # a maple branch overhead, top left
    cone("PRP_branch", "trunk", (-4.2, 1.9, 2.42), 0.09, 0.03, 3.6, rot=(0, D(80), 0))
    for i in range(16):
        x = -3.6 + 0.3 * i + rnd.uniform(-0.1, 0.1)
        sphere(f"PRP_maple_{i}", "maple" if i % 3 else "maple_l", (x, 1.9 + rnd.uniform(-0.3, 0.3), 2.62 + 0.2 * math.sin(i * 1.7) - 0.012 * i),
               (0.3, 0.18, 0.2), rot=(0, D(rnd.uniform(-30, 30)), 0))
    for i, (x, y) in enumerate([(0.9, 0.2), (2.3, 1.6), (1.6, 3.4), (3.3, -0.2), (0.2, 2.4)]):     # leaves already on the water
        sphere(f"PRP_leaf_water_{i}", "maple" if i % 2 else "maple_l", (x, y, 0.012), (0.13, 0.08, 0.008), rot=(0, 0, D(40 * i)))


# ================================================================ clip 1: the hook
def clip1():
    """Narrator: "Sol, what's all that?" [0.25] / "Wait, is all of this due this week?" [2.65].
    The desk wide, locked off. Sol stands on the left, already part purple and worried. He turns to the pile and
    holds an arm nub up at it (0.9-2.2). One more worksheet drops out of the air and lands on the soccer ball at
    2.6: Shocked, a hop, full purple. Worried again at 4.3, and at 4.65 he looks up and nods."""
    n = 165
    new_scene("due_1", n)
    build_bedroom()
    pile = build_pile()
    extra = empty("RIG_extra_sheet", (0, 0, 5))
    box("PRP_extra_sheet", "white", (0, 0, 0), (0.78, 1.0, 0.012), parent=extra)
    track(extra, "location", "rotation_euler")
    track(pile["ball"], "location", "rotation_euler")
    sol = build_sol(SOL_D, 0)
    cam, tgt = build_camera(lens=CAM_D[2])
    TL = [(0.0, "worried"), (2.6, "shocked"), (4.3, "worried")]
    bx, by, bz = HW_D[0] + 0.16, HW_D[1] - 0.12, 0.62 + 0.36
    LAND = 2.6

    def state(t, f):
        aim(cam, tgt, CAM_D)
        k = smooth(t, 2.0, LAND)
        sway = (1 - k) * math.sin(t * 9.0)
        extra.location = (bx + 0.05 + 0.3 * sway, by, lerp(3.4, bz + 0.372, k * k * (3 - 2 * k)) if t > 1.9 else 5.0)
        extra.rotation_euler = (D(4), D(lerp(32 * sway, 8, k) + 5 * wobble(t, LAND, freq=13, decay=6)), D(14))
        pile["ball"].location = (bx + 0.012 * wobble(t, LAND, freq=15, decay=5), by, bz - 0.012 * abs(wobble(t, LAND, freq=15, decay=5)))
        turn = smooth(t, 0.75, 1.1) * (1 - smooth(t, 4.2, 4.6))
        point = smooth(t, 0.9, 1.2) * (1 - smooth(t, 2.3, 2.6))
        jolt = smooth(t, LAND, LAND + 0.15)
        calm = smooth(t, 4.2, 4.6)
        nod = bump(t, 4.65, 5.25)
        panic = jolt * (1 - smooth(t, 3.5, 4.0))
        act(sol, t, f, TL, gloom=lerp(0.62, 1.0, smooth(t, LAND - 0.05, LAND + 0.1)), blinks=(0.45,),
            look=(lerp(0.0, 0.95, turn), lerp(0.55, 0.3, turn) + 0.4 * calm - 0.5 * nod),
            loc=(SOL_D[0] - 0.1 * jolt * (1 - calm), SOL_D[1], hop(t, LAND, LAND + 0.36, 0.2) + hop(t, 3.25, 3.5, 0.08)),
            yaw=lerp(4, 30, turn), lean=7 * point * (1 - jolt) + 5 * panic * math.sin(t * 24) - 4 * jolt * (1 - calm),
            pitch=lerp(8, 2, turn) + 6 * jolt * (1 - calm) + 10 * calm - 24 * nod,
            squash=idle(t) + 0.06 * (bump(t, 1.2, 1.5) + bump(t, 1.65, 1.95)) + 0.05 * wobble(t, LAND + 0.36, decay=5) + 0.07 * nod,
            arm_l=(-40 + 80 * jolt * (1 - smooth(t, 3.6, 4.2)), 10 * jolt),
            arm_r=(-40 + 90 * point * (1 - jolt) + 80 * jolt * (1 - smooth(t, 3.6, 4.2)), 10 * jolt))
    return animate(n, state)


# ================================================================ clip 2: the setup
def clip2():
    """Narrator: "Okay, here are five things that'll help." [0.2]. Same desk, the pile now with the extra sheet on
    the ball. The shot OPENS CLOSE on Sol's face and the camera pulls slowly back until the pile is in frame on the
    right (her note on cut v1; the script had a push in). He is worried, full purple; he leans in toward the camera,
    and at 2.45 squeezes his eyes shut, bracing."""
    n = 105
    new_scene("due_2", n)
    build_bedroom()
    build_pile()
    bx, by, bz = HW_D[0] + 0.16, HW_D[1] - 0.12, 0.62 + 0.36
    box("PRP_extra_sheet", "white", (bx + 0.05, by, bz + 0.372), (0.78, 1.0, 0.012), rot=(D(4), D(8), D(14)))
    sol = build_sol(SOL_D, 6)
    cam, tgt = build_camera(lens=CAM_D[2])
    TL = [(0.0, "worried"), (2.45, "squeeze")]

    def state(t, f):
        # Elaine, 2026-11-26, on cut v1: "the cut from first clip to 2nd clip is a bit unusual ... we can resolve this by
        # starting the camera from a close up of sol's face and zooming out instead". v1 began on clip 1's own wide
        # framing and pushed in, so the cut was wide-to-the-same-wide. Now it opens close on his face and pulls back
        # until the pile is in frame on the right.
        k = smooth(t, 0.15, 3.3)
        cam.location = lerp3((-1.5, -1.05, 0.52), (-0.62, -3.05, 0.7), k)
        tgt.location = lerp3((-1.5, 1.2, 0.36), (-0.78, 1.2, 0.58), k)
        brace = smooth(t, 2.35, 2.7)
        act(sol, t, f, TL, gloom=1.0, look=(0.0, 0.5 * (1 - brace)),
            yaw=6, pitch=9 - 17 * smooth(t, 0.4, 2.0), lean=2 * math.sin(t * 2.5),
            squash=idle(t) + 0.07 * brace,
            arm_l=(-40 + 62 * brace, 28 * brace), arm_r=(-40 + 62 * brace, 28 * brace))
    return animate(n, state)


# ================================================================ clip 3: tip 1, control / influence / accept
def flight(t, t0, t1, a, b, h):
    """Position of something thrown from a to b between t0 and t1, in an arc h high."""
    k = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
    return (lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k) + h * 4 * k * (1 - k)), k


def clip3():
    """Narrator: "First, sort it into what you control, what you can influence, and what you have to accept." [0.2].
    His bedroom floor from a slightly high angle, locked off. Three open cardboard boxes in a row on the right. The
    three things stand beside Sol: the math homework next to him, the poster board and the calendar page leaning
    on the wall. He bumps the homework with his side and it hops into the first box (1.75-2.3). He holds an arm nub
    up at the poster and it hops into the second (3.05-3.65). The calendar page lifts and floats into the third
    (4.1-5.2). Each box gives a small bounce. He is still part purple, with no lines on his face."""
    n = 180
    new_scene("due_3", n)
    build_floor_room()
    boxes = [build_box(nm, x, 0.45, f"box_{nm}.png") for nm, x in (("control", 1.1), ("influence", 2.3), ("accept", 3.5))]
    HW0, P0, C0 = (-1.5, 0.3, 0), (-0.72, 1.44, 0), (0.12, 1.47, 0)
    hw = build_homework("floor", HW0)
    poster = build_poster("floor", P0, lean=7)
    cal = build_calendar("floor", C0, lean=9)
    for o in (hw, poster, cal):
        track(o, "location", "rotation_euler")
    home = (-2.5, 0.42, 0)
    sol = build_sol(home, 16)
    cam, tgt = build_camera(lens=36)
    TL = [(0.0, "normal")]
    T = ((1.75, 2.3), (3.05, 3.65), (4.1, 5.2))

    def state(t, f):
        cam.location, tgt.location = (0.52, -7.1, 2.95), (0.52, 0.6, 0.78)
        # 1. the homework: bumped, then an arc into "Control"
        p, k = flight(t, *T[0], HW0, (1.1, 0.45, 0.05), 1.0)
        hw.location = p
        hw.rotation_euler = (0, D(-14 * math.sin(k * math.pi)), D(180 * smooth(k, 0.05, 0.6)))      # each thing turns half round in the air,
        # 2. the poster: off the wall, an arc into "Influence", standing in the box
        p, k = flight(t, *T[1], P0, (2.3, 0.6, 0.05), 0.75)
        poster.location = p
        poster.rotation_euler = (D(lerp(-7, 6, k)), D(-22 * math.sin(k * math.pi)), D(180 * smooth(k, 0.05, 0.6)))   # so it lands with its blank back to us
        # 3. the calendar page: lifts off the wall and floats across, swaying, down into "Accept"
        k = smooth(t, *T[2])
        up = math.sin(min(1.0, max(0.0, (t - T[2][0]) / (T[2][1] - T[2][0]))) * math.pi)
        cal.location = (lerp(C0[0], 3.5, k) + 0.07 * up * math.sin(t * 7), lerp(C0[1], 0.6, k), lerp(0.0, 0.05, k) + 1.0 * up ** 0.8)
        cal.rotation_euler = (D(lerp(-9, 4, k)), D(9 * up * math.sin(t * 6)), D(180 * smooth(t, T[2][0], T[2][0] + 0.55) + 5 * up * math.sin(t * 5 + 1)))
        for b, x, (_, t1) in zip(boxes, (1.1, 2.3, 3.5), T):          # each box gives one tiny rigid hop as its item lands
            b.location = (x, 0.45, hop(t, t1, t1 + 0.2, 0.06))        # (v1 squashed the box, and the painter drew flaps opening)
        bumpk = bump(t, 1.5, 1.95)
        point = smooth(t, 2.8, 3.02) * (1 - smooth(t, 3.4, 3.8))
        watch = smooth(t, 4.0, 4.4) * (1 - smooth(t, 5.25, 5.5))
        upv = smooth(t, 5.3, 5.6)
        act(sol, t, f, TL, gloom=0.5, blinks=(5.0,),
            look=(lerp(0.95, 0.1, upv), lerp(0.1 + 0.5 * watch, 0.6, upv)),
            loc=(home[0] + 0.2 * bumpk, home[1], hop(t, 3.7, 3.98, 0.1)),
            yaw=lerp(26, 8, upv), lean=13 * bumpk + 5 * point, pitch=4 + 5 * watch + 6 * upv,
            squash=idle(t) + 0.08 * bump(t, 1.35, 1.6) - 0.05 * bump(t, 1.6, 1.9) + 0.05 * wobble(t, 3.98, decay=5),
            arm_r=(-40 + 92 * point, 0))
    return animate(n, state)


# ================================================================ clip 4: tip 2, slow breaths
def clip4():
    """Narrator: "Second, take a few slow breaths so your body can calm down." [0.25].
    The pond garden from the course card, medium, locked off, soft warm light. Sol sits on the mossy rock on the
    left; the pond fills the right. He swells and shrinks three times, like breathing (0.2-1.7, 1.8-3.3, 3.4-4.9),
    and with each breath out more of the purple drains from his flame. Eyes: > < for the first breath, a flat
    closed line for the second, open navy ovals for the third. One maple leaf drifts down onto the water during the
    second breath (lands 3.1) and a ring spreads from it."""
    n = 150
    new_scene("due_4", n)
    build_garden()
    home = (-1.55, 0.6, 0.47)
    sol = build_sol(home, 5)
    track(sol["root"], "scale")
    leaf = sphere("PRP_leaf_fall", "maple", (0, 0, 9), (0.14, 0.085, 0.01))
    track(leaf, "location", "rotation_euler")
    rings = []
    for i in range(2):
        bm = bmesh.new()
        bmesh.ops.create_circle(bm, cap_ends=False, segments=48, radius=1.0)
        geom = bmesh.ops.extrude_edge_only(bm, edges=bm.edges[:])
        for v in [g for g in geom["geom"] if isinstance(g, bmesh.types.BMVert)]:
            v.co.x *= 1.1
            v.co.y *= 1.1
        o = mesh_obj(f"FX_ring_{i}", bm, "water_l", (1.1, 0.9, -5), (0.1, 0.1, 1))
        track(o, "location", "scale")
        rings.append(o)
    cam, tgt = build_camera(lens=40)
    TL = [(0.0, "squeeze"), (1.82, "normal")]
    B = ((0.2, 1.7), (1.8, 3.3), (3.4, 4.9))
    LAND, LX, LY = 3.1, 1.1, 0.9

    def breath(t):
        return sum(math.sin((min(max(t, a), b) - a) / (b - a) * math.pi) ** 2 for a, b in B)

    def state(t, f):
        cam.location, tgt.location = (0.15, -5.2, 1.35), (0.15, 0.6, 1.14)
        br = breath(t)
        k = 1.0 + 0.075 * br
        sol["root"].scale = (k, k, k)
        # the purple leaves on each breath OUT (the second half of each breath)
        g = 1.0 - 0.28 * smooth(t, 0.95, 1.75) - 0.27 * smooth(t, 2.55, 3.35) - 0.25 * smooth(t, 4.1, 4.85)
        shut = smooth(t, 1.7, 1.82) * (1 - smooth(t, 3.5, 3.72))
        act(sol, t, f, TL, gloom=max(g, 0.0), blink=shut, look=(0.0, 0.15 * smooth(t, 3.6, 4.0)),
            loc=home, yaw=5, lean=0.0, pitch=2 + 5 * br, squash=-0.035 * br,
            arm_l=(-40 + 14 * br, 0), arm_r=(-40 + 14 * br, 0))
        u = smooth(t, 1.9, LAND)
        if t < 1.85:
            leaf.location = (0, 0, 9)
        else:
            leaf.location = (LX + 0.9 * (1 - u) + 0.22 * (1 - u) * math.sin(t * 6.5), LY, lerp(2.9, 0.014, u))
        leaf.rotation_euler = (D(28 * (1 - u) * math.sin(t * 6.5 + 1)), D(30 * (1 - u) * math.cos(t * 6.5)), D(60 * t))
        for i, o in enumerate(rings):
            a = (t - LAND - 0.3 * i) / 1.5
            if 0 < a < 1:
                o.location, o.scale = (LX, LY, 0.006), (0.16 + 0.5 * a, 0.16 + 0.5 * a, 1)
            else:
                o.location, o.scale = (LX, LY, -5), (0.1, 0.1, 1)
    return animate(n, state)


# ================================================================ clip 5: tip 3, one thing first
def clip5():
    """Narrator: "Third, pick the one thing that matters most and start there." [0.2].
    The kitchen table, medium, eye level, locked off. Three things in a row on the right: the math homework, the
    group-project poster and the piano music (the last two leaning on small wooden props). Sol turns and holds an
    arm nub up at the homework (0.9-1.7). At 1.75 it lights up (a warm glow, added in the edit) and the other two
    slide back a little and dim. O O surprised at 1.9 with a small hop; Normal at 3.1; he looks up at 3.4."""
    n = 138
    new_scene("due_5", n)
    build_kitchen()
    hw = build_homework("table", (0.1, 0.9, 0), pre="PRP_lit_")
    poster = build_poster("table", (1.25, 1.0, 0), lean=12, pre="PRP_dim_")
    strut("poster", poster, h=1.0)
    music = build_music("table", (2.3, 1.0, 0), lean=14, pre="PRP_dim_")
    strut("music", music, h=0.8)
    for o in (poster, music):
        track(o, "location")
    home = (-1.6, 0.9, 0)
    sol = build_sol(home, 10)
    cam, tgt = build_camera(lens=40)
    TL = [(0.0, "normal"), (1.9, "surprised"), (3.1, "normal")]

    def state(t, f):
        cam.location, tgt.location = (0.2, -4.9, 0.85), (0.2, 1.0, 0.62)
        back = smooth(t, 1.75, 2.3)
        poster.location = (1.25, 1.0 + 0.5 * back, 0)
        music.location = (2.3, 1.0 + 0.5 * back, 0)
        turn = smooth(t, 0.5, 0.85) * (1 - smooth(t, 3.3, 3.6))
        point = smooth(t, 0.9, 1.15) * (1 - smooth(t, 1.75, 1.95))
        jolt = smooth(t, 1.88, 2.02) * (1 - smooth(t, 3.0, 3.3))
        upv = smooth(t, 3.35, 3.7)
        act(sol, t, f, TL, gloom=0.0, blinks=(4.05,),
            look=(lerp(0.3, 0.95, turn), lerp(0.5, 0.2, turn) + 0.4 * upv),
            loc=(home[0] - 0.08 * jolt, home[1], hop(t, 1.9, 2.22, 0.14)),
            yaw=lerp(8, 30, turn), lean=7 * point - 3 * jolt, pitch=lerp(8, 2, turn) + 5 * jolt + 9 * upv,
            squash=idle(t) + 0.05 * wobble(t, 2.22, decay=5),
            arm_r=(-40 + 92 * point + 45 * jolt, 0), arm_l=(-40 + 45 * jolt, 0))
    return animate(n, state)


# ================================================================ clip 6: tip 4, a backup plan
def clip6():
    """Narrator: "Fourth, have a backup plan, so one thing going wrong doesn't wreck everything." [0.2].
    The hallway whiteboard from the science ad, medium, a slight low angle, locked off. "Plan A" is written on the
    right side of the board (lettering is laid on in the edit). Sol stands at the board's lower left corner,
    reading it. At 1.55 he hops and taps the board with a raised arm nub; "Plan B" is written on under Plan A from
    2.0. At 3.0 he hops, O O surprised with both nubs up; Normal at 4.2, looking up."""
    n = 165
    new_scene("due_6", n)
    build_hallway()
    home = (-1.02, 0.56, 0)
    sol = build_sol(home, 26)
    cam, tgt = build_camera(lens=36)
    TL = [(0.0, "normal"), (3.0, "surprised"), (4.2, "normal")]
    T1 = (1.55, 2.0)

    def state(t, f):
        cam.location, tgt.location = (0.66, -4.75, 0.32), (0.66, 0.9, 0.7)
        tap = bump(t, T1[0] - 0.06, T1[1] + 0.12)
        crouch = bump(t, T1[0] - 0.24, T1[0] + 0.04)
        jolt = smooth(t, 2.98, 3.12) * (1 - smooth(t, 4.0, 4.4))
        upv = smooth(t, 4.3, 4.7)
        act(sol, t, f, TL, gloom=0.0, blinks=(0.8, 4.95),
            look=(lerp(0.95, 0.1, upv), lerp(0.6, 0.7, upv)),
            loc=(home[0] + 0.1 * tap - 0.06 * jolt, home[1], hop(t, *T1, 0.3) + hop(t, 3.0, 3.36, 0.2)),
            yaw=lerp(26, 10, upv), lean=6 * tap - 3 * jolt, pitch=5 + 5 * jolt + 6 * upv,
            squash=idle(t) + 0.09 * crouch + 0.05 * (wobble(t, T1[1], decay=5) + wobble(t, 3.36, decay=5)),
            arm_r=(-40 + 105 * tap + 70 * jolt, 0), arm_l=(-40 + 25 * tap + 70 * jolt, 0))
    return animate(n, state)


# ================================================================ clip 7: tip 5, let it be messy
def clip7():
    """Narrator: "And fifth, let your first try be messy." [0.2-2.6] "Rough drafts are supposed to be rough." [3.1].
    His desk, close, from above, locked off. On the right lies one sheet of paper: his rough-draft sketch for the
    group poster. He looks down at it, and from 0.45 to 1.95 he is Worried with a quick purple flicker, leaning in
    and pulling back (the urge to fix it). Blink at 2.15, Normal and orange again. At 3.0 he squashes, springs
    toward the sheet and nudges its edge with his side: it slides away across the desk (3.1-3.5) like it is done.
    Then he tilts back and looks up. His arm nubs stay at his sides."""
    n = 159
    new_scene("due_7", n)
    box("ENV_desk", "wood", (0, -1.2, -0.1), (13, 8.6, 0.2))
    box("ENV_wall", "wall", (0, 3.2, 3.5), (13, 0.2, 10))
    box("PRP_eraser", "pink", (1.75, 1.75, 0.05), (0.34, 0.18, 0.1), rot=(0, 0, D(25)))
    cone("PRP_pencil_a", "yellow", (0.2, 1.9, 0.03), 0.03, 0.03, 0.9, rot=(0, D(90), D(-12)))
    cone("PRP_pencil_b", "blue", (1.1, 1.72, 0.03), 0.03, 0.03, 0.8, rot=(0, D(90), D(35)))
    P0 = (0.62, 0.52, 0.008)
    paper = empty("RIG_sketch", P0, rot=(0, 0, D(5)))
    box("PRP_sketch_paper", "white", (0, 0, 0), (1.3, 1.0, 0.012), parent=paper)
    overlay_plane("sketch", "sketch.png", (0, 0, 0.012), (1.3, 1.0), rot=(0, 0, 0), parent=paper)
    track(paper, "location", "rotation_euler")
    home = (-0.82, 0.5, 0)
    sol = build_sol(home, 14)
    cam, tgt = build_camera(lens=40)
    TL = [(0.0, "normal"), (0.45, "worried"), (1.95, "normal")]

    def state(t, f):
        cam.location, tgt.location = (0.1, -2.95, 3.25), (0.1, 0.52, 0.22)
        slide = smooth(t, 3.1, 3.5)
        paper.location = (P0[0] + 0.3 * slide, P0[1] + 0.16 * slide, P0[2])
        paper.rotation_euler = (0, 0, D(5 - 7 * slide + 1.5 * wobble(t, 3.5, freq=14, decay=7)))
        hes = (bump(t, 0.5, 1.05) + bump(t, 1.3, 1.85)) * 1.0
        nudge = bump(t, 2.95, 3.6)
        upv = smooth(t, 3.9, 4.3)
        g = smooth(t, 0.4, 0.6) * (1 - smooth(t, 1.85, 2.05)) * 0.95
        act(sol, t, f, TL, gloom=g, blinks=(2.15,),
            look=(lerp(0.9, 0.0, upv), lerp(-0.75, 0.6, upv)),
            loc=(home[0] + 0.07 * hes + 0.2 * nudge, home[1], 0),
            yaw=lerp(22, 2, upv), lean=6 * hes + 11 * nudge, pitch=lerp(10, 18, upv) - 4 * hes,
            squash=idle(t) + 0.12 * bump(t, 2.85, 3.1) - 0.07 * bump(t, 3.1, 3.4) + 0.05 * wobble(t, 3.6, decay=5)
                   + 0.07 * bump(t, 4.3, 4.6) - 0.04 * bump(t, 4.55, 4.8))
    return animate(n, state)


# ================================================================ clip 8: the payoff
def clip8():
    """Narrator: "Ignite's free Resilience and Stress Management course teaches all of this and more." [0.2-6.15]
    "So, does this week feel doable now?" [6.5-9.2].
    The desk wide, the SAME camera as clip 1. The desk is tidy: the math homework in one short neat stack with a
    check mark, a pencil cup with a "Plan B" sticky note, the calendar page small and pinned to the wall. Sol hops
    once (0.35, O O surprised mid-bounce). The end card slides in over the right two thirds at 1.0 (edit); he
    looks at it. Sparkles at 2.0, brightest orange. At 6.4 he tilts back and looks up at the camera; at 9.2 he nods,
    in Sparkles, and holds to the last frame."""
    n = 300
    new_scene("due_8", n)
    build_bedroom()
    build_homework("tidy", (HW_D[0], HW_D[1], 0), tall=0.38, neat=True, check=True, fit=(0.72, 0.085))
    cone("PRP_cup", "blue", (1.5, 1.2, 0), 0.19, 0.22, 0.5)
    for i, (dx, dy, tilt) in enumerate([(-0.06, 0.0, 9), (0.07, 0.03, -7), (0.0, -0.06, 3)]):
        cone(f"PRP_pencil_{i}", "yellow", (1.5 + dx, 1.2 + dy, 0.3), 0.022, 0.022, 0.52, rot=(0, D(tilt), 0))
    box("PRP_planb_note", "sticky_p", (1.5, 0.975, 0.27), (0.4, 0.012, 0.4))
    overlay_plane("planb", "note_planb.png", (1.5, 0.96, 0.27), (0.4, 0.4))
    cal = build_calendar("wall", (1.1, 2.085, 1.0), lean=0, s=0.72)
    sphere("PRP_pin", "red", (1.1, 2.05, 1.0 + 0.6), (0.045, 0.045, 0.045))
    sol = build_sol(SOL_D, 4)
    cam, tgt = build_camera(lens=CAM_D[2])
    TL = [(0.0, "normal"), (0.38, "surprised"), (2.0, "sparkle")]

    def state(t, f):
        aim(cam, tgt, CAM_D)
        card = smooth(t, 1.0, 1.4) * (1 - smooth(t, 5.9, 6.4))          # looking at the card
        upv = smooth(t, 6.3, 6.75)
        nod = bump(t, 9.15, 9.75)
        joy = bump(t, 2.0, 2.5) + bump(t, 2.7, 3.2)
        act(sol, t, f, TL, blinks=(4.4, 7.6), look=(0.9 * card, lerp(0.3, 0.85, upv) - 0.5 * nod),
            loc=(SOL_D[0], SOL_D[1], hop(t, 0.36, 0.76, 0.24)),
            yaw=4 + 20 * card, lean=2 * math.sin(t * 2.0) * (1 - nod), pitch=lerp(6, 14, upv) - 24 * nod,
            squash=idle(t) + 0.08 * bump(t, 0.2, 0.4) + 0.05 * wobble(t, 0.76, decay=5) + 0.08 * joy - 0.05 * (bump(t, 2.4, 2.7) + bump(t, 3.1, 3.4)) + 0.07 * nod,
            arm_l=(-40 + 60 * bump(t, 0.3, 1.0) + 45 * joy, 0), arm_r=(-40 + 60 * bump(t, 0.3, 1.0) + 45 * joy, 0))
    return animate(n, state)
