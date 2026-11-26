"""Skeleton clips for the ad "Due in 5 Minutes" (script v4). exec()'d after rig.py by render_clip.py.

Nine paint clips for the script's eight: clip 8 (the payoff) needs 12.6 s of narration and a paint clip can be at
most 10 s, so it is two shots, 8 (wide, the finished poster) and 9 (closer, "So, is it ready now?", the nod).
Times are seconds on each clip's own clock and follow the trimmed takes in audio/edit/ (voice starts in brackets).
Every camera with lettering in the shot is locked off, so the lettering can be laid over the painted clip exactly.
Sol never wears goggles (the script allows all clips or none).
"""
import random

PX, PY, WA = 0.45, 1.05, 40          # poster: centre of its middle panel on the desk, wing angle
SOL_A = (-0.85, -0.6, 0)           # clips 1, 2 and 9: in front of the poster, nearer the camera
SOL_B = (-1.15, 0.3, 0)            # clip 8: beside the poster
BX, BZ = 0.35, 1.25                  # whiteboard centre


def act(sol, t, f, timeline, gloom=None, look=(0.0, 0.0), blinks=(), **pose):
    """Eyes from the emotion timeline (with its bounce), then the body pose with that bounce added."""
    expr, sq, size, g = emotion_at(t, timeline)
    if gloom is not None:
        g = gloom
    bl = blink_at(t, blinks) if expr in ("normal", "worried", "sparkle") else 0.0
    face(sol, f, expr, blink=bl, look=look, size=size, gloom=g)
    pose["squash"] = pose.get("squash", 0.0) + sq
    pose_sol(sol, **pose)


def card_size(w, h):
    """Plane size for a card PNG: the art has a 10%-of-height margin all round for its shadow."""
    return (w + 0.2 * h, h * 1.2)


# ================================================================ sets
def build_bedroom():
    box("ENV_desk", "wood", (0, -1.2, -0.1), (11, 6.6, 0.2))
    box("ENV_wall", "wall", (0, 2.2, 3.5), (11, 0.2, 10))
    box("ENV_window_pane", "sky", (2.75, 2.08, 3.0), (1.7, 0.05, 2.4))
    for nm, loc, size in [("L", (1.86, 2.04, 3.0), (0.12, 0.1, 2.64)), ("T", (2.75, 2.04, 4.26), (1.9, 0.1, 0.12)),
                          ("B", (2.75, 2.0, 1.74), (2.0, 0.2, 0.12)), ("V", (2.75, 2.04, 3.0), (0.07, 0.08, 2.4))]:
        box("ENV_window_" + nm, "trim", loc, size)
    cx, cz = 0.3, 3.2                                   # wall clock: five minutes to eight
    cone("PRP_clock_rim", "teal", (cx, 2.1, cz), 0.5, 0.5, 0.07, rot=(D(90), 0, 0))
    cone("PRP_clock_face", "white", (cx, 2.02, cz), 0.42, 0.42, 0.02, rot=(D(90), 0, 0))
    for i in range(12):
        th = D(30 * i)
        box(f"PRP_clock_tick_{i}", "dark", (cx + 0.35 * math.sin(th), 1.992, cz + 0.35 * math.cos(th)), (0.022, 0.01, 0.07), rot=(0, th, 0))
    for nm, th, L, w in (("min", 330, 0.33, 0.034), ("hour", 237.5, 0.21, 0.05)):
        box("PRP_clock_" + nm, "dark", (cx + math.sin(D(th)) * L / 2, 1.985, cz + math.cos(D(th)) * L / 2), (w, 0.02, L), rot=(0, D(th), 0))
    cone("PRP_clock_hub", "coral", (cx, 1.985, cz), 0.04, 0.04, 0.02, rot=(D(90), 0, 0))
    # desk lamp, back left
    cone("PRP_lamp_base", "teal", (-2.45, 1.35, 0), 0.26, 0.22, 0.06)
    cone("PRP_lamp_arm", "teal", (-2.45, 1.35, 0.06), 0.03, 0.03, 1.1, rot=(0, D(12), 0))
    cone("PRP_lamp_shade", "yellow", (-2.26, 1.35, 1.1), 0.12, 0.3, 0.34, rot=(0, D(140), 0))
    # crumpled paper and two markers in the foreground: a project left to the last minute
    for i, (x, y, r) in enumerate([(0.75, -1.35, 0.11), (1.2, -1.85, 0.09), (-0.1, -2.05, 0.1)]):
        sphere(f"PRP_paperball_{i}", "paper", (x, y, r * 0.9), (r, r * 0.92, r * 0.9))
    cone("PRP_pen_blue", "blue", (0.25, -1.2, 0.035), 0.035, 0.035, 0.42, rot=(0, D(90), D(25)))
    cone("PRP_pen_coral", "coral", (-1.5, -1.9, 0.035), 0.035, 0.035, 0.42, rot=(0, D(90), D(-40)))
    # a shelf with a plant and books, on the wall at the left
    box("PRP_shelf", "wood_d", (-1.75, 1.95, 2.3), (1.5, 0.3, 0.06))
    cone("PRP_shelf_pot", "coral", (-2.1, 1.92, 2.33), 0.12, 0.16, 0.22)
    for i, (dx, dz, sc_) in enumerate([(0, 0.4, 0.2), (-0.13, 0.32, 0.13), (0.13, 0.34, 0.14)]):
        sphere(f"PRP_shelf_leaf_{i}", "leaf", (-2.1 + dx, 1.92, 2.33 + dz), (sc_, sc_, sc_ * 1.2))
    for i, key in enumerate(("yellow", "blue", "coral")):
        box(f"PRP_shelf_book_{i}", key, (-1.6 + 0.13 * i, 1.93, 2.56), (0.1, 0.24, 0.46 - 0.05 * i))
    # books and a pencil cup, back right
    box("PRP_book_1", "coral", (2.5, 1.45, 0.08), (0.95, 0.62, 0.16), rot=(0, 0, D(7)))
    box("PRP_book_2", "teal", (2.47, 1.47, 0.23), (0.85, 0.56, 0.14), rot=(0, 0, D(-5)))
    cone("PRP_cup", "blue", (2.45, 0.55, 0), 0.17, 0.2, 0.42)
    for i, (dx, dy, tilt) in enumerate([(-0.06, 0.0, 9), (0.07, 0.03, -7), (0.0, -0.06, 3)]):
        cone(f"PRP_pencil_{i}", "yellow", (2.45 + dx, 0.55 + dy, 0.25), 0.022, 0.022, 0.5, rot=(0, D(tilt), 0))


def build_graph(tag, loc, s=1.0, parent=None):
    """The bar graph: plain ice (blue, tall) and salted ice (yellow, short). The SAME object in clip 6 and on the poster."""
    g = empty("RIG_graph_" + tag, loc, parent=parent)
    g.scale = (s, s, s)
    box("PRP_graph_sheet_" + tag, "paper", (0, 0, 0.65), (1.25, 0.012, 1.3), parent=g)
    box("PRP_graph_axis_v_" + tag, "dark", (-0.42, -0.012, 0.69), (0.022, 0.008, 0.92), parent=g)
    box("PRP_graph_axis_h_" + tag, "dark", (0.04, -0.012, 0.24), (0.94, 0.008, 0.022), parent=g)
    box("PRP_graph_bar1_" + tag, "blue", (-0.17, -0.014, 0.65), (0.26, 0.01, 0.80), parent=g)
    box("PRP_graph_bar2_" + tag, "yellow", (0.24, -0.014, 0.47), (0.26, 0.01, 0.44), parent=g)
    overlay_plane("graph", "graph_labels.png", (0, -0.03, 0.65), (1.25, 1.3), parent=g)
    return g


def build_poster(finished=False):
    """Trifold board on the desk with a header board across the top. finished=True adds the five pieces."""
    a = D(WA)
    root = empty("RIG_poster", (PX, PY, 0))
    box("PRP_poster_c", "white", (0, 0, 0.85), (1.5, 0.03, 1.7), parent=root)
    for s, nm in ((-1, "L"), (1, "R")):
        box("PRP_poster_" + nm, "white", (s * (0.75 + 0.375 * math.cos(a)), -0.375 * math.sin(a), 0.85), (0.75, 0.03, 1.7),
            parent=root, rot=(0, 0, -s * a))
    hy = -0.30
    box("PRP_poster_header", "white", (0, hy, 1.89), (2.66, 0.03, 0.38), parent=root)
    if not finished:
        return root

    def on_wing(s, u, z, off):                      # a point on a wing, u metres out from its hinge
        return (s * (0.75 + math.cos(a) * u) - s * math.sin(a) * off, -math.sin(a) * u - math.cos(a) * off, z)

    overlay_plane("title", "title1.png", (0, hy - 0.03, 1.89), (2.4, 0.30), parent=root)                # 1 the question
    for nm, img, key, z in (("changed", "card_changed.png", "cardA", 1.37), ("measured", "card_measured.png", "cardB", 0.98)):   # 2
        box("PRP_card_" + nm, key, on_wing(-1, 0.375, z, 0.02), (0.62, 0.012, 0.32), parent=root, rot=(0, 0, a))
        overlay_plane(nm, img, on_wing(-1, 0.375, z, 0.035), card_size(0.62, 0.32), rot=(D(90), 0, a), parent=root)
    for i, z in enumerate((0.66, 0.46, 0.26)):                                                         # 3 the trials
        box(f"PRP_tag_{i + 1}", "tag", on_wing(-1, 0.375, z, 0.02), (0.40, 0.012, 0.15), parent=root, rot=(0, 0, a))
        overlay_plane(f"trial{i + 1}", f"tag_trial{i + 1}.png", on_wing(-1, 0.375, z, 0.035), card_size(0.40, 0.15), rot=(D(90), 0, a), parent=root)
    build_graph("poster", (0, -0.025, 0.2), parent=root)                                               # 4 the graph
    box("PRP_page", "page", on_wing(1, 0.375, 0.95, 0.02), (0.58, 0.012, 0.80), parent=root, rot=(0, 0, -a))      # 5 what went wrong
    overlay_plane("wrong", "page_wrong.png", on_wing(1, 0.375, 0.95, 0.035), (0.58, 0.80), rot=(D(90), 0, -a), parent=root)
    return root


def build_hall_shell():
    box("ENV_floor", "floor", (0, -1.6, -0.1), (11, 7.4, 0.2))
    box("ENV_wall", "wall", (0, 1.1, 3.5), (11, 0.2, 10))
    box("ENV_baseboard", "trim", (0, 0.985, 0.09), (11, 0.04, 0.18))


def build_hallway():
    build_hall_shell()
    box("ENV_rug", "teal", (0.1, -0.9, 0.01), (3.4, 2.3, 0.02))
    box("PRP_board_frame", "steel", (BX, 0.975, BZ), (1.92, 0.05, 1.42))
    box("PRP_board", "white", (BX, 0.945, BZ), (1.80, 0.02, 1.30))
    box("PRP_board_tray", "steel", (BX, 0.90, BZ - 0.72), (1.3, 0.13, 0.04))
    cone("PRP_marker", "blue", (BX + 0.2, 0.89, BZ - 0.67), 0.03, 0.03, 0.32, rot=(0, D(90), 0))
    for nm, x, z, key, w, h in (("a", -0.35, 2.95, "coral", 0.62, 0.78), ("b", 0.42, 3.05, "yellow", 0.5, 0.5), ("c", 1.08, 2.92, "mint", 0.56, 0.7)):
        box("PRP_frame_" + nm, "trim", (x, 0.98, z), (w + 0.12, 0.04, h + 0.12))
        box("PRP_picture_" + nm, key, (x, 0.955, z), (w, 0.02, h))
    overlay_plane("title", "title2.png", (BX, 0.93, BZ + 0.03), (1.74, 0.95))


def build_counter(tiles=True):
    box("ENV_counter", "counter", (0, -1.2, -0.1), (11, 6.8, 0.2))
    box("ENV_wall", "trim", (0, 2.3, 3.5), (11, 0.2, 10))
    box("ENV_wall_stripe", "teal", (0, 2.19, 1.55), (11, 0.02, 0.16))
    if tiles:
        for i in range(1, 9):
            if i != 3:
                box(f"ENV_grout_h{i}", "steel", (0, 2.19, 0.5 * i), (11, 0.02, 0.02))
        for i in range(-8, 9):
            box(f"ENV_grout_v{i}", "steel", (0.62 * i + 0.3, 2.19, 2.1), (0.02, 0.02, 4.2))


def build_bowl(tag, x, y, seed):
    """A white bowl of ice cubes. One piece; it never moves."""
    cone("PRP_bowl_" + tag, "white", (x, y, 0), 0.24, 0.43, 0.27)
    cone("PRP_bowl_in_" + tag, "teal", (x, y, 0.262), 0.40, 0.40, 0.012)
    rnd = random.Random(seed)
    for i in range(7):
        an, r = rnd.uniform(0, 6.28), rnd.uniform(0.0, 0.24)
        box(f"PRP_ice_{tag}_{i}", "ice", (x + r * math.cos(an), y + r * math.sin(an), 0.31 + 0.05 * (i % 3)), (0.15, 0.15, 0.15),
            rot=(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), rnd.uniform(0, 1.5)))


def build_ice_tray(tag, x, y, z):
    box("PRP_tray_" + tag, "blue", (x, y, z + 0.05), (1.0, 0.5, 0.1))
    for i in range(5):
        for j in range(2):
            box(f"PRP_traycube_{tag}_{i}{j}", "ice", (x - 0.38 + 0.19 * i, y - 0.11 + 0.22 * j, z + 0.12), (0.14, 0.16, 0.1))


# ================================================================ clip 1: the hook
def clip1():
    """Narrator: "Sol, what are you doing?" [0.25] / "Wait, your science project's due in five minutes?" [2.5].
    Bedroom desk, a blank trifold poster, a wall clock. Locked-off medium wide.
    Elaine, 2026-11-26: "he should start by pointing at the poster at the beginning and then freaking out", and
    "sol is also looking the wrong way". So he stands beside the poster, turned toward it, one arm nub up toward it,
    bouncing ("this!"). He glances up at the clock (1.75), and at "Wait" he freaks out: Shocked, a hop, both arms up,
    indigo snap, a frantic side-to-side shake, a second hop, a look back at the poster. Worried (4.7), nod (5.5).
    He always faces the poster or the camera, never the frame edge."""
    n = 189
    new_scene("ad_1", n)
    build_bedroom()
    build_poster(False)
    sol = build_sol(SOL_B, 28)
    cam, tgt = build_camera(lens=24)
    TL = [(0.0, "normal"), (2.55, "shocked"), (4.7, "worried")]

    def state(t, f):
        cam.location, tgt.location = (-0.4, -3.6, 0.6), (-0.4, 1.0, 0.6)
        point = 1.0 - smooth(t, 1.65, 1.95)
        voice = bump(t, 1.05, 1.75)                          # a glance up at the voice while he points
        up = smooth(t, 1.75, 2.1)                            # then up at the clock
        back = smooth(t, 2.5, 2.68)                          # the freak-out
        panic = smooth(t, 2.85, 3.05) * (1 - smooth(t, 4.2, 4.6))
        poster = bump(t, 3.2, 4.4)                           # a look back at the blank poster
        nod = bump(t, 5.5, 6.05)
        fall = smooth(t, 4.3, 4.8)
        lookx = lerp(lerp(1.0 - 0.7 * voice, 0.5, up), 0.9 * poster, back)
        lookz = lerp(lerp(0.15 + 0.6 * voice, 1.0, up), 0.45 * (1 - poster), back)
        act(sol, t, f, TL, look=(lookx, lookz),
            loc=(SOL_B[0], SOL_B[1], hop(t, 2.5, 2.86, 0.2) + hop(t, 3.3, 3.58, 0.12)),
            yaw=lerp(lerp(28, 22, up), 13 + 16 * poster, back),
            lean=8 * point * (1 - up) + 9 * panic * math.sin(t * 24),
            pitch=lerp(lerp(0, 14, up), 8, back) - 22 * nod,
            squash=idle(t) + 0.06 * (bump(t, 0.3, 0.6) + bump(t, 0.85, 1.15)) + 0.05 * wobble(t, 2.86, decay=5) + 0.05 * wobble(t, 3.58, decay=5) + 0.07 * nod,
            arm_l=(-40 + 80 * back * (1 - 0.8 * fall), 10 * back),
            arm_r=(-40 + 88 * point * (1 - back) + 80 * back * (1 - 0.8 * fall), 10 * back))
    return animate(n, state)


# ================================================================ clip 2: the setup
def clip2():
    """Narrator: "Okay, here are five things that'll save it." [0.2]. Same desk. A slow push in on Sol. He is
    worried, flame tip indigo; he leans in toward the camera and at 1.95 squeezes his eyes shut, bracing."""
    n = 90
    new_scene("ad_2", n)
    build_bedroom()
    build_poster(False)
    sol = build_sol(SOL_A, 6)
    cam, tgt = build_camera(lens=24)
    TL = [(0.0, "worried"), (1.95, "squeeze")]

    def state(t, f):
        k = smooth(t, 0.0, 3.0)
        cam.location = lerp3((-0.3, -3.7, 0.6), (-0.8, -2.75, 0.5), k)
        tgt.location = lerp3((-0.3, 1.0, 0.6), (-0.95, -0.6, 0.46), k)
        brace = smooth(t, 1.85, 2.2)
        act(sol, t, f, TL, gloom=1.0, look=(0.0, 0.45 * (1 - brace)),
            yaw=6, pitch=8 - 17 * smooth(t, 0.3, 1.7), lean=2 * math.sin(t * 2.5),
            squash=idle(t) + 0.07 * brace,
            arm_l=(-40 + 62 * brace, 28 * brace), arm_r=(-40 + 62 * brace, 28 * brace))
    return animate(n, state)


# ================================================================ clip 3: tip 1, the question
def clip3():
    """Narrator: "First, write your question at the top so judges know what you were testing." [0.2].
    Hallway whiteboard, a slight low angle, locked off. Sol hops and taps the board (1.28-1.76); the question
    is written on from 1.52. He blinks, the indigo starts to fade, and he taps it again (4.15-4.6)."""
    n = 162
    new_scene("ad_3", n)
    build_hallway()
    home = (-0.88, 0.58, 0)
    sol = build_sol(home, 28)
    cam, tgt = build_camera(lens=26)
    TL = [(0.0, "normal")]                 # calm: Elaine, 2026-11-26, no distress during the tips
    T1, T2 = (1.28, 1.76), (4.15, 4.6)

    def state(t, f):
        cam.location, tgt.location = (-0.17, -3.3, 0.32), (-0.17, 0.9, 0.62)
        tap = bump(t, T1[0] - 0.06, T1[1] + 0.12) + bump(t, T2[0] - 0.06, T2[1] + 0.12)
        crouch = bump(t, T1[0] - 0.24, T1[0] + 0.04) + bump(t, T2[0] - 0.24, T2[0] + 0.04)
        g = 0.0
        listen = smooth(t, 2.7, 3.2) - smooth(t, 3.9, 4.1)
        act(sol, t, f, TL, gloom=g, blinks=(3.25,), look=(lerp(1.0, 0.1, listen), lerp(0.55, 0.7, listen)),
            loc=(home[0], home[1], hop(t, *T1, 0.3) + hop(t, *T2, 0.3)),
            yaw=28 - 12 * listen, lean=6 * tap, pitch=4 + 6 * listen,
            squash=idle(t) + 0.09 * crouch + 0.05 * (wobble(t, T1[1], decay=5) + wobble(t, T2[1], decay=5)),
            arm_r=(-40 + 105 * tap, 0), arm_l=(-40 + 25 * tap, 0))
    return animate(n, state)


# ================================================================ clip 4: tip 2, changed and measured
def clip4():
    """Narrator: "Second, say the one thing you changed and what you measured." [0.2].
    Kitchen counter from high above, locked off. Two bowls of ice, a salt shaker, a kitchen timer. Sol bumps the
    salt shaker with his side (0.95-1.5; label "Changed" pops at 1.9), then turns and hops toward the timer (2.45;
    "Measured" at 3.3). His arms stay at his sides: reaching arms came back long or detached in two paints."""
    n = 120
    new_scene("ad_4", n)
    build_counter(tiles=False)
    box("PRP_cloth", "teal", (0, 0.0, 0.006), (2.5, 1.2, 0.012))
    build_bowl("plain", -0.72, 0.0, 3)
    build_bowl("salted", 0.72, 0.0, 8)
    salt = empty("RIG_salt", (-0.56, 1.0, 0))       # right against his side: two paints stretched or detached his arm when he reached
    cone("PRP_salt_body", "white", (0, 0, 0), 0.105, 0.085, 0.27, parent=salt)
    sphere("PRP_salt_cap", "steel", (0, 0, 0.27), (0.088, 0.088, 0.06), parent=salt)
    track(salt, "location", "rotation_euler")
    cone("PRP_timer_body", "yellow", (0.66, 1.0, 0), 0.23, 0.2, 0.17)
    cone("PRP_timer_dial", "white", (0.66, 1.0, 0.17), 0.16, 0.16, 0.012)
    box("PRP_timer_hand", "dark", (0.66, 1.06, 0.19), (0.03, 0.14, 0.012))
    cone("PRP_timer_knob", "coral", (0.66, 1.0, 0.182), 0.035, 0.035, 0.03)
    home = (0.0, 1.05, 0)
    sol = build_sol(home, 0)
    cam, tgt = build_camera(lens=30)
    anchor("changed", (-0.56, 1.0, 0.33))
    anchor("measured", (0.66, 1.0, 0.2))
    TL = [(0.0, "normal")]

    def state(t, f):
        cam.location, tgt.location = (0.0, -1.35, 3.45), (0.0, 0.62, 0.2)
        nudge = bump(t, 0.95, 1.5)
        slide = smooth(t, 1.12, 1.34)
        salt.location = (-0.56 - 0.15 * slide, 1.0, 0)
        salt.rotation_euler = (0, D(-9 * bump(t, 1.1, 1.36) + 2.5 * wobble(t, 1.36, freq=17, decay=7)), 0)
        turn = smooth(t, 2.15, 2.45)
        point = smooth(t, 2.45, 2.8)
        act(sol, t, f, TL, gloom=0.0, blinks=(2.25,),
            look=(lerp(-1.0, 1.0, turn) * smooth(t, 0.2, 0.5), -0.3),
            loc=(home[0] - 0.12 * nudge + 0.07 * point, home[1], hop(t, 2.45, 2.8, 0.12)),
            yaw=lerp(-16, 16, turn) * smooth(t, 0.2, 0.5), lean=-14 * nudge + 10 * point, pitch=20,
            squash=idle(t) + 0.06 * bump(t, 0.8, 1.0) + 0.05 * wobble(t, 1.5, decay=5) + 0.05 * wobble(t, 2.8, decay=5))
    return animate(n, state)


# ================================================================ clip 5: tip 3, how many times
def clip5():
    """Narrator: "Third, say how many times you ran it, because one try could just be luck." [0.2].
    A small white freezer on the kitchen counter, eye level, locked off. Sol nudges the door (0.45-1.05) and it
    swings open (0.75-1.7). Cold fog rolls out. Three ice trays inside; tags Trial 1, 2, 3 pop at 1.7, 2.0, 2.3."""
    n = 146
    new_scene("ad_5", n)
    build_counter()
    W, Hh, Dp = 1.7, 2.2, 1.2
    box("PRP_frz_back", "white", (0, 0.6, Hh / 2), (W, 0.06, Hh))
    box("PRP_frz_inner", "ice", (0, 0.56, Hh / 2), (W - 0.12, 0.02, Hh - 0.12))
    for s in (-1, 1):
        box(f"PRP_frz_side{s}", "white", (s * (W / 2 - 0.03), 0, Hh / 2), (0.06, Dp, Hh))
    box("PRP_frz_top", "white", (0, 0, Hh - 0.03), (W, Dp, 0.06))
    box("PRP_frz_bottom", "white", (0, 0, 0.03), (W, Dp, 0.06))
    box("PRP_frz_kick", "white", (0, -0.1, 0.22), (W - 0.12, Dp - 0.2, 0.44))        # solid base: the trays sit above the fog
    for i, z in enumerate((1.0, 1.55)):
        box(f"PRP_frz_shelf{i}", "steel", (0, 0, z), (W - 0.12, Dp - 0.1, 0.03))
    for i, z in enumerate((1.57, 1.02, 0.46)):                      # trial 1 on top
        build_ice_tray(str(i + 1), -0.22, -0.2, z)
        anchor(f"trial{i + 1}", (0.56, -0.58, z + 0.2))
    door = empty("RIG_door", (W / 2, -Dp / 2, 0))
    box("PRP_door", "white", (-W / 2, -0.04, Hh / 2), (W, 0.08, Hh), parent=door)
    box("PRP_door_handle", "steel", (-W + 0.16, -0.12, Hh / 2), (0.06, 0.08, 0.9), parent=door)
    track(door, "rotation_euler")
    fog = []
    rnd = random.Random(5)
    for i in range(12):
        o = sphere(f"FX_fog_{i}", "fog", (0, 0, -5), (0.1, 0.1, 0.1), alpha=0.3)
        track(o, "location", "scale")
        fog.append({"o": o, "x": rnd.uniform(-0.65, 0.55), "z": rnd.uniform(0.3, 0.5), "ph": i / 12.0, "dx": rnd.uniform(-0.25, 0.25)})
    home = (-1.35, -0.95, 0)
    sol = build_sol(home, 30)
    cam, tgt = build_camera(lens=26)
    TL = [(0.0, "normal"), (1.45, "surprised"), (3.3, "normal")]

    def state(t, f):
        cam.location, tgt.location = (-0.42, -5.0, 0.55), (-0.42, 0.0, 0.78)
        door.rotation_euler = (0, 0, D(12 + 96 * smooth(t, 0.75, 1.7) + 4 * wobble(t, 1.7, freq=9, decay=4)))
        nudge = bump(t, 0.45, 1.05)
        jolt = smooth(t, 1.42, 1.6)
        for s in fog:
            u = ((t - 1.0) / 2.4 + s["ph"]) % 1.0
            on = smooth(t, 1.0 + 0.5 * s["ph"], 1.5 + 0.5 * s["ph"]) * (1 - smooth(u, 0.8, 1.0)) * smooth(u, 0.0, 0.12)
            k = (0.12 + 0.3 * u) * on
            s["o"].location = (s["x"] + s["dx"] * u, -0.68 - 1.5 * u, s["z"] * (1 - u) ** 2 + 0.08) if on > 0.02 else (0, 0, -5)
            s["o"].scale = (k * 1.5, k, k * 0.55)
        calm = smooth(t, 3.2, 3.6)
        act(sol, t, f, TL, gloom=0.0, blinks=(3.9,),      # no tint at all: the first paint turned a faint tint into a second Shocked
            look=(lerp(1.0, 0.35, calm), lerp(0.25 + 0.3 * jolt, 0.5, calm)),
            loc=(home[0] + 0.2 * nudge - 0.16 * jolt, home[1], hop(t, 1.42, 1.78, 0.15) + hop(t, 0.42, 0.72, 0.08)),
            yaw=30 + 6 * nudge - 14 * calm, lean=15 * nudge - 4 * jolt * (1 - calm), pitch=3 + 6 * jolt,
            squash=idle(t) + 0.06 * bump(t, 0.3, 0.5) + 0.05 * wobble(t, 1.78, decay=5),
            arm_r=(-40 + 75 * nudge + 40 * jolt * (1 - calm), 18 * nudge), arm_l=(-40 + 40 * jolt * (1 - calm), 0))
    return animate(n, state)


# ================================================================ clip 6: tip 4, make a graph
def clip6():
    """Narrator: "Fourth, turn your numbers into a graph, since nobody reads a wall of numbers." [0.2].
    A wall covered in sticky notes of numbers, wide, eye level, locked off. Sol pushes against the wall, eyes
    squeezed shut (0.15-1.1). From 1.1 the notes let go and flutter to the floor, and the bar graph is underneath.
    At 2.0 he bounces back, surprised."""
    n = 155
    new_scene("ad_6", n)
    build_hall_shell()
    box("ENV_rug", "blue", (0.0, -1.0, 0.01), (3.6, 2.2, 0.02))
    build_graph("wall", (-0.28, 0.975, 0.95), s=1.36)
    rnd = random.Random(21)
    notes, cols = [], ("yellow", "pink", "mint", "cardB", "cardA")
    for r in range(6):
        for c in range(6):
            x = -1.13 + 0.17 + 0.313 * c + rnd.uniform(-0.03, 0.03)
            z = 2.72 - 0.17 - 0.303 * r + rnd.uniform(-0.03, 0.03)
            piv = empty(f"RIG_note_{r}{c}", (x, 0.95, z))
            box(f"PRP_note_{r}{c}", cols[(r * 2 + c * 3 + rnd.randrange(2)) % 5], (0, 0, 0), (0.30, 0.012, 0.30), parent=piv)
            for k in range(3):
                box(f"PRP_note_ln_{r}{c}{k}", "dark", (rnd.uniform(-0.02, 0.02), -0.008, 0.07 - 0.07 * k), (rnd.uniform(0.14, 0.22), 0.004, 0.018), parent=piv)
            track(piv, "location", "rotation_euler")
            notes.append({"o": piv, "x": x, "z": z, "tilt": D(rnd.uniform(-7, 7)),
                          "go": 1.1 + 0.16 * (5 - c) + 0.07 * r + rnd.uniform(0, 0.18),       # the side nearest Sol lets go first
                          "ph": rnd.uniform(0, 6.28), "dx": rnd.uniform(-0.35, 0.35), "dy": rnd.uniform(0.25, 1.15),
                          "spin": rnd.uniform(-3, 3), "rest": D(rnd.uniform(0, 360)), "stack": 0.012 + 0.004 * rnd.randrange(6)})
    home = (0.98, 0.6, 0)
    sol = build_sol(home, -42)
    cam, tgt = build_camera(lens=26)
    TL = [(0.0, "squeeze"), (2.0, "surprised"), (3.9, "normal")]

    def state(t, f):
        cam.location, tgt.location = (0.3, -3.5, 0.5), (0.3, 1.0, 0.78)
        push = smooth(t, 0.1, 0.4) - smooth(t, 1.0, 1.15)
        shake = push * math.sin(t * 38) * 0.012
        for s in notes:
            tau = t - s["go"]
            if tau <= 0:
                s["o"].location = (s["x"] + shake, 0.95, s["z"])
                s["o"].rotation_euler = (0, s["tilt"] + shake * 2, 0)
                continue
            fallz = s["z"] - 2.6 * tau * tau - 0.25 * tau
            if fallz <= s["stack"]:
                T = (-0.25 + math.sqrt(0.0625 + 10.4 * (s["z"] - s["stack"]))) / 5.2     # when it landed
                s["o"].location = (s["x"] + s["dx"] * T, 0.95 - s["dy"] * min(T, 1.0), s["stack"])
                s["o"].rotation_euler = (D(90), 0, s["rest"])
            else:
                k = min(1.0, tau * 4)
                s["o"].location = (s["x"] + s["dx"] * tau + 0.06 * math.sin(tau * 7 + s["ph"]), 0.95 - s["dy"] * min(tau, 1.0), fallz)
                s["o"].rotation_euler = (k * D(70) * math.sin(tau * 8 + s["ph"]), s["tilt"] + k * s["spin"] * tau, k * 0.6 * math.sin(tau * 5 + s["ph"]))
        jolt = smooth(t, 1.98, 2.15)
        calm = smooth(t, 3.8, 4.2)
        act(sol, t, f, TL, blinks=(4.5,),
            look=(-1.0 * jolt * (1 - 0.6 * calm), 0.7 * jolt),
            loc=(home[0] + 0.05 * jolt, home[1] - 0.12 * jolt, hop(t, 1.98, 2.36, 0.2) + hop(t, 2.36, 2.62, 0.07)),
            yaw=-42 + 14 * jolt + 12 * calm, lean=-13 * push + 3 * push * math.sin(t * 30) + 4 * jolt * (1 - calm), pitch=-4 * push + 10 * jolt,
            squash=idle(t) * (1 - push) + 0.07 * push + 0.05 * wobble(t, 2.62, decay=5),
            arm_l=(-40 + 62 * push + 30 * jolt * (1 - calm), 10 * push), arm_r=(-40 + 20 * push + 30 * jolt * (1 - calm), 0))
    return animate(n, state)


# ================================================================ clip 7: tip 5, what went wrong
def clip7():
    """Narrator: "And fifth, write down what went wrong, because real scientists always do." [0.2].
    The kitchen counter, later; close, from above, locked off. A small puddle where one ice cube melted early, an
    open notebook beside it. Sol looks down at the puddle (worried at 1.0, a quick indigo flicker), taps the
    notebook (1.65-2.1; the heading appears from 1.9), blinks, and is back to orange."""
    n = 150
    new_scene("ad_7", n)
    build_counter(tiles=False)
    sphere("PRP_puddle", "ice", (-0.86, 0.12, 0.0), (0.40, 0.27, 0.014), alpha=0.75)
    sphere("PRP_puddle_b", "ice", (-0.62, -0.02, 0.0), (0.24, 0.17, 0.012), alpha=0.75)
    sphere("PRP_puddle_c", "ice", (-1.08, 0.3, 0.0), (0.2, 0.15, 0.012), alpha=0.75)
    box("PRP_puddle_cube", "ice", (-0.9, 0.16, 0.035), (0.11, 0.11, 0.07), rot=(0, 0, D(20)))
    nb = empty("RIG_notebook", (0.34, -0.02, 0), rot=(0, 0, D(-5)))
    box("PRP_nb_cover", "teal", (0, 0, 0.012), (1.36, 0.90, 0.024), parent=nb)
    box("PRP_nb_page_l", "page", (-0.325, 0, 0.032), (0.61, 0.82, 0.02), parent=nb)
    box("PRP_nb_page_r", "page", (0.325, 0, 0.032), (0.61, 0.82, 0.02), parent=nb)
    box("PRP_nb_spine", "steel", (0, 0, 0.04), (0.035, 0.84, 0.03), parent=nb)
    overlay_plane("wrong", "page_wrong.png", (0.325, 0, 0.046), (0.58, 0.80), rot=(0, 0, 0), parent=nb)
    home = (0.42, 0.76, 0)        # right behind the right-hand page, so his short arm reaches its edge without stretching
    sol = build_sol(home, -18)
    cam, tgt = build_camera(lens=30)
    TL = [(0.0, "normal")]                 # calm, and no hop: the hop came back with him left hanging in the air

    def state(t, f):
        cam.location, tgt.location = (0.08, -2.0, 2.7), (0.08, 0.18, 0.2)
        down = smooth(t, 0.1, 0.45)
        tap = bump(t, 1.62, 2.14)
        page = smooth(t, 1.45, 1.7)
        upv = smooth(t, 2.9, 3.3)
        g = 0.0
        act(sol, t, f, TL, gloom=g, blinks=(2.72,),
            look=(lerp(lerp(-0.95, 0.75, page), 0.0, upv) * down, lerp(-0.85 * down, 0.55, upv)),
            yaw=lerp(lerp(-24, 4, page), 0, upv), lean=lerp(-8, 0, page) * down, pitch=lerp(12 - 4 * down, 16, upv) - 6 * tap,
            squash=idle(t) + 0.14 * bump(t, 1.5, 1.86) - 0.09 * bump(t, 1.8, 2.1) + 0.05 * wobble(t, 2.1, decay=5))
    return animate(n, state)


# ================================================================ clip 8: the payoff, a move across the poster
def spline(t, keys):
    """Catmull-Rom through keys [(time, (x, y, z)), ...]: one continuous camera path, no stop at each key."""
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    i = max(k for k in range(len(keys) - 1) if keys[k][0] <= t)
    u = (t - keys[i][0]) / (keys[i + 1][0] - keys[i][0])
    p0, p1, p2, p3 = keys[max(i - 1, 0)][1], keys[i][1], keys[i + 1][1], keys[min(i + 2, len(keys) - 1)][1]
    return tuple(0.5 * (2 * b + (c - a) * u + (2 * a - 5 * b + 4 * c - d) * u * u + (-a + 3 * b - 3 * c + d) * u ** 3)
                 for a, b, c, d in zip(p0, p1, p2, p3))


def clip8():
    """Narrator: "Ignite's free Scientific Research and Data Analysis course teaches you how real research works,
    from collecting data to analyzing it." [0.25-9.2].
    Elaine, 2026-11-26: the wide on the finished poster was "kind of scuffed" (flicker beside Sol), "for this long
    duration can we just replace this clip with like a 3d like motion that looks through his poster and then pivot
    to him with sparkle eyes". So: the camera starts on the whole finished poster (the question readable), glides
    in and travels across it at close range, right wing ("What went wrong") -> the graph -> left wing (Changed,
    Measured, the three trials), then swings left to Sol, who stands beside the poster with sparkle eyes and
    bounces with his feet planted. He stands clear of every piece of lettering, so nothing has to be cut out
    around him. The course card goes on top in the edit."""
    n = 279
    new_scene("ad_8", n)
    build_bedroom()
    build_poster(True)
    home = (-1.5, 0.3, 0)
    sol = build_sol(home, 12)
    cam, tgt = build_camera(lens=24)
    CAM = [(0.0, (0.45, -2.6, 1.2)), (2.0, (1.0, -0.95, 0.98)), (4.1, (0.45, -1.4, 0.98)), (6.0, (0.0, -0.9, 0.93)),
           (7.5, (-1.16, -1.75, 0.62)), (9.4, (-1.2, -1.68, 0.62))]
    TGT = [(0.0, (0.45, 1.0, 1.3)), (2.0, (1.49, 0.81, 1.2)), (4.1, (0.45, 1.03, 1.12)), (6.0, (-0.59, 0.81, 1.08)),
           (7.5, (-1.6, 0.3, 0.74)), (9.4, (-1.6, 0.3, 0.72))]
    TL = [(0.0, "sparkle")]

    def state(t, f):
        cam.location, tgt.location = spline(t, CAM), spline(t, TGT)
        b1, b2 = bump(t, 7.55, 7.95), bump(t, 8.35, 8.75)                 # two happy bounces, feet on the desk
        act(sol, t, f, TL, blinks=(8.15,), look=(0.1, 0.35),
            yaw=12, lean=3 * math.sin(t * 2.6), pitch=5,
            squash=idle(t) + 0.11 * (b1 + b2) - 0.07 * (bump(t, 7.85, 8.15) + bump(t, 8.65, 8.95)),
            arm_l=(-40 + 55 * (b1 + b2), 0), arm_r=(-40 + 55 * (b1 + b2), 0))
    return animate(n, state)


# ================================================================ clip 9: the payoff, the nod
def clip9():
    """Narrator: "So, is it ready now?" [0.25-1.9]. Same desk, closer on Sol with the poster behind him, locked
    off. He is looking up at the voice. At 1.95 his eyes sparkle and he nods twice (2.0-2.9), then holds, looking
    up, to the last frame."""
    n = 99
    new_scene("ad_9", n)
    build_bedroom()
    build_poster(True)
    sol = build_sol(SOL_A, 4)
    cam, tgt = build_camera(lens=24)
    TL = [(0.0, "normal"), (1.95, "sparkle")]

    def state(t, f):
        cam.location, tgt.location = (-0.56, -2.9, 0.3), (-0.56, 1.0, 0.3)
        nod = bump(t, 2.0, 2.46) + bump(t, 2.46, 2.92)
        act(sol, t, f, TL, blinks=(0.7,), look=(0.0, 0.9 - 0.5 * nod),
            yaw=4, lean=1.5 * math.sin(t * 2.0), pitch=13 - 24 * nod,
            squash=idle(t) + 0.07 * nod + 0.04 * wobble(t, 2.92, decay=5),
            arm_l=(-40 + 30 * smooth(t, 1.9, 2.2), 0), arm_r=(-40 + 30 * smooth(t, 1.9, 2.2), 0))
    return animate(n, state)
