"""Five gray skeleton clips for the narrator-only candle episode (script v2).

Usage inside Blender:  exec(rig.py source); exec(this source with WHICH = "01".."05" in the namespace).
Motion is smooth (keyed every frame). Times are seconds on the clip's own clock and follow the trimmed narrator takes in audio/v2/trim/.
"""


def clip01():
    """Narrator: "What are you doing, Sol?" 0.15-1.35 / "Ohh, you must be wondering why the flame is still
    standing straight up." 2.5-6.35. Sol wiggles the candle, looks up to show the Narrator, then nods."""
    n = 222
    new_scene("candle_01", n)
    build_desk()
    candle = build_candle()
    stand = build_stand(0.6)
    sol = build_sol((-0.74, -0.05, 0), D(20))
    cam, tgt = build_camera()

    def state(t, f):
        k = smooth(t, 0.0, 3.0)
        k2 = smooth(t, 3.0, 7.2)
        cam.location = lerp3(lerp3((-1.6, -6.3, 1.6), (0.55, -4.6, 1.2), k), (0.7, -4.35, 1.15), k2)
        tgt.location = lerp3((-0.3, 0, 1.0), (-0.42, 0, 0.68), k)
        tilt = 22 * smooth(t, 0.1, 0.5) - 16 * smooth(t, 0.55, 0.9) + 17 * smooth(t, 0.95, 1.35) \
            + 2.5 * wobble(t, 1.35, freq=13, decay=5)
        candle["piv"].rotation_euler = (0, D(tilt), 0)
        pose_flame(candle, f)
        up = smooth(t, 1.45, 2.15)                       # looks up to the Narrator, stays there
        nod = bump(t, 6.4, 6.85) + bump(t, 6.85, 7.3)          # two clear nods
        squash = 0.04 * (wobble(t, 0.5) - wobble(t, 0.9) + wobble(t, 1.35)) + 0.06 * wobble(t, 1.6, decay=4) \
            + 0.07 * nod
        pose_sol(sol, yaw=lerp(20, 14, up), lean=tilt * 0.42, pitch=24 * up - 34 * nod, squash=squash,
                 arm_r=(-6 + tilt * 0.5, 14), arm_l=(-40 + 55 * bump(t, 1.5, 2.3), 0),
                 blink=f in (119, 120), gaze=up * (1 - nod))

    return animate(n, state)


def clip02():
    """Narrator: "It's the air. The flame heats it, and hot air rises. Slide that paper spiral over it."
    0.15-6.2 / "See? The rising air spins it." 6.6-8.9. Sol slides the stand over and the spiral spins."""
    n = 276
    new_scene("candle_02", n)
    build_desk()
    candle = build_candle()
    stand = build_stand(0.48)
    sol = build_sol((1.66, 0.42, 0), D(-22))
    cam, tgt = build_camera()
    spin = {"a": 0.0}

    def state(t, f):
        k = smooth(t, 2.6, 5.8)
        cam.location = lerp3((0.12, -2.4, 0.9), (-0.2, -6.2, 1.55), k)
        tgt.location = lerp3((0.0, 0, 0.74), (0.6, 0, 1.12), k)
        pose_flame(candle, f)
        push = smooth(t, 4.5, 6.0)
        stand["root"].location = (lerp(0.48, 0.0, push) + stand["dx"], stand["dy"], 0)
        step = bump(t, 4.6, 5.2) + bump(t, 5.3, 5.9)        # two small shuffles while he pushes
        sol["root"].location = (lerp(1.66, 1.18, push), 0.42, 0.03 * step)
        rate = 2.6 * smooth(t, 6.1, 7.1)                   # rad/s once the spiral sits over the flame
        spin["a"] += rate * (1 / FPS)
        stand["spin"].rotation_euler = (0, 0, spin["a"])
        watch = smooth(t, 2.9, 4.2) * (1 - smooth(t, 4.3, 4.7))      # eyes follow the rising air
        up = smooth(t, 6.3, 7.0)                           # then up at the spinning spiral
        cheer = bump(t, 6.9, 7.7)
        pose_sol(sol, yaw=-22, lean=-11 * bump(t, 4.4, 6.2), pitch=8 * watch + 14 * up,
                 squash=0.05 * step + 0.06 * wobble(t, 6.9, decay=4),
                 arm_l=(-40 + 52 * smooth(t, 4.3, 4.7) * (1 - smooth(t, 6.0, 6.4)) + 85 * cheer, 10),
                 arm_r=(-40 + 85 * cheer, 0), blink=f in (61, 62), gaze=0.6 * watch + up)

    return animate(n, state)


def clip03():
    """Narrator: "Down low, cooler air slides in to replace it." 0.2-3.5 / "That upward stream stretches
    the flame into a teardrop." 3.8-7.1. Sol ducks down to watch the incense smoke get pulled in and up."""
    n = 228
    new_scene("candle_03", n)
    build_desk()
    candle = build_candle()
    stand = build_stand(0.0)
    sol = build_sol((-1.22, 0.15, 0), D(25))
    cam, tgt = build_camera()
    hold = empty("RIG_incense", (-0.62, 0, 0))
    cone("PRP_incense_dish", "prop", (0, 0, 0), 0.09, 0.11, 0.04, parent=hold)
    cone("PRP_incense_stick", "dark", (0, 0, 0.03), 0.012, 0.012, 0.5, parent=hold, rot=(0, D(12), 0))
    tip = (0.105, 0.0, 0.52)

    def path(kind, u):
        if kind == "A":                                    # straight up, undisturbed
            return (tip[0] + 0.02 * math.sin(u * 5), tip[2] + 1.7 * u)
        if kind == "B":                                    # bends low toward the base of the flame
            return (tip[0] + 0.50 * smooth(u, 0.0, 0.75), tip[2] + 0.12 * smooth(u, 0.0, 0.6) + 0.10 * u)
        ux = smooth(u, 0.0, 0.42)                          # in low, turn the corner, out high along the flame
        return (tip[0] + 0.47 * ux + 0.04 * smooth(u, 0.42, 1.0), tip[2] + 0.12 * ux + 1.45 * smooth(u, 0.36, 1.0) ** 1.3)

    bm = bmesh.new()
    pts, ring = 44, 6
    verts = []
    for i in range(pts):
        x, z = path("A", i / (pts - 1))
        verts.append([bm.verts.new((x + 0.02 * math.cos(a), 0.02 * math.sin(a), z))
                      for a in (2 * math.pi * j / ring for j in range(ring))])
    for a, b in zip(verts, verts[1:]):
        for j in range(ring):
            bm.faces.new((a[j], a[(j + 1) % ring], b[(j + 1) % ring], b[j]))
    smoke = mesh_obj("PRP_smoke_thread", bm, "smoke", parent=hold)
    smoke.shape_key_add(name="A")
    kbs = {}
    for kind in ("B", "C"):
        kb = smoke.shape_key_add(name=kind)
        for i in range(pts):
            x, z = path(kind, i / (pts - 1))
            for j in range(ring):
                a = 2 * math.pi * j / ring
                kb.data[i * ring + j].co = (x + 0.02 * math.cos(a), 0.02 * math.sin(a), z)
        track(kb, "value")
        kbs[kind] = kb
    spin = {"a": 0.0}

    def state(t, f):
        k = smooth(t, 0.2, 3.2)
        k2 = smooth(t, 3.4, 6.2)
        cam.location = lerp3(lerp3((-1.35, -3.6, 0.8), (-0.4, -4.3, 0.85), k), (-0.35, -5.0, 1.1), k2)
        tgt.location = lerp3(lerp3((-0.78, 0, 0.6), (-0.52, 0, 0.7), k), (-0.52, 0, 1.0), k2)
        sb, sc_ = smooth(t, 0.6, 2.8), smooth(t, 2.9, 4.5)
        kbs["B"].value = sb * (1 - sc_)
        kbs["C"].value = sc_
        pose_flame(candle, f, stretch=1.0 + 0.38 * smooth(t, 4.0, 5.5))
        spin["a"] += 2.6 * (1 / FPS)
        stand["spin"].rotation_euler = (0, 0, spin["a"])
        duck = smooth(t, 0.35, 1.0) * (1 - smooth(t, 3.3, 4.2))     # ducks on "Down low"
        up = smooth(t, 3.5, 5.0)                                     # follows the smoke up
        pose_sol(sol, yaw=25, lean=5 * duck, pitch=-13 * duck + 12 * up,
                 squash=0.11 * duck + 0.04 * wobble(t, 0.4) + 0.04 * wobble(t, 3.5),
                 arm_l=(-40 + 30 * duck, 20), arm_r=(-40 + 30 * duck, 20),
                 blink=f in (89, 90), gaze=-0.7 * duck + up)

    return animate(n, state)


def clip04():
    """Narrator: "But what if there's no up?" 0.2-1.5 / "In orbit, hot air doesn't rise, so the flame
    becomes a little blue ball." 2.1-6.7. Space station: Sol shrugs up at the Narrator, turns, watches."""
    n = 228
    new_scene("candle_04", n)
    box("ENV_bench", "desk", (0, -1.4, -0.1), (11, 7.0, 0.2))
    box("ENV_wall", "wall", (0, 2.0, 3.0), (11, 0.2, 9))
    for i, x in enumerate((-2.3, -0.75, 2.55)):
        box(f"ENV_panel_{i}", "frame", (x, 1.88, 2.2), (1.35, 0.08, 3.4))
    cone("ENV_port_ring", "prop", (1.0, 1.92, 2.35), 0.78, 0.78, 0.14, rot=(D(90), 0, 0))
    cone("ENV_port_pane", "pane", (1.0, 1.80, 2.35), 0.62, 0.62, 0.05, rot=(D(90), 0, 0))
    bx, hw, hd, hh, bar = 0.62, 0.48, 0.38, 1.05, 0.035
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"PRP_case_post_{sx}{sy}", "glass", (bx + sx * hw, sy * hd, hh / 2), (bar, bar, hh))
        for z in (bar / 2, hh):
            box(f"PRP_case_side_{sx}{z:.1f}", "glass", (bx + sx * hw, 0, z), (bar, 2 * hd, bar))
            box(f"PRP_case_front_{sx}{z:.1f}", "glass", (bx, sx * hd, z), (2 * hw, bar, bar))
    candle = build_candle(x=bx, height=0.26)
    sol = build_sol((-0.5, 0, 0), 0.0)
    box("PRP_foot_strap", "prop", (-0.5, -0.02, 0.075), (0.46, 0.2, 0.03))
    pencil = cone("PRP_float_pencil", "frame", (-1.2, 0.5, 2.3), 0.03, 0.03, 0.6, rot=(D(70), D(20), 0))
    fspin = build_spiral(top=(1.85, 0.6, 1.7), drop=0.5, name="PRP_float_spiral")
    track(pencil, "location", "rotation_euler")
    track(fspin, "location")
    # two small Sols in bubble helmets floating in the background (Elaine: "stimulating and cute")
    floaters = []
    for loc, sc_ in (((-0.62, 1.2, 1.95), 0.62), ((0.12, 1.3, 2.42), 0.5)):
        fs = build_sol(loc, 0.0)
        fs["root"].scale = (sc_, sc_, sc_)
        sphere("PRP_helmet", "glass", (0, 0, 0.52), (0.62, 0.58, 0.62), parent=fs["body"])       # clear bubble helmet
        cone("PRP_helmet_collar", "prop", (0, 0, 0.0), 0.36, 0.38, 0.06, parent=fs["body"])
        floaters.append((fs, loc))
    cam, tgt = build_camera()

    def state(t, f):
        k = smooth(t, 0.3, 6.6)
        cam.location = lerp3((-1.35, -5.5, 1.25), (1.1, -4.4, 1.0), k)
        tgt.location = lerp3((-0.05, 0, 0.8), (0.08, 0, 0.62), k)
        pencil.location = (-1.2 + 0.05 * t, 0.5, 2.3 + 0.04 * t)
        pencil.rotation_euler = (D(70) + 0.12 * t, D(20) + 0.2 * t, 0)
        fspin.location = (1.85 - 0.03 * t, 0.6, 1.7 + 0.05 * t)
        fspin.rotation_euler = (0.1 * t, 0.06 * t, 0.25 * t)
        for i, (fs, loc) in enumerate(floaters):
            ph = t * (0.9 + 0.3 * i) + 2.0 * i
            fs["root"].location = (loc[0] + 0.12 * math.sin(ph * 0.7) + (0.03 if i else -0.02) * t,
                                   loc[1], loc[2] + 0.14 * math.sin(ph) + 0.03 * t)
            wave = 0.5 + 0.5 * math.sin(t * 7.0) if i == 0 else 0.0
            pose_sol(fs, yaw=(-18 if i else 14) + 10 * math.sin(ph * 0.5), lean=(16 if i else -12) + 14 * math.sin(ph * 0.6),
                     pitch=6 * math.sin(ph * 0.8), arm_l=(-30, 0), arm_r=(10 + 50 * wave if i == 0 else -20, 0),
                     blink=False, gaze=0.0)
        ball = smooth(t, 2.6, 5.0)
        candle["ball"].value = ball
        pose_flame(candle, f, stretch=1.0 - 0.15 * ball, amount=1.0 - 0.8 * ball)
        up = 1 - smooth(t, 1.6, 2.4)                       # starts looking up at the Narrator
        shrug = bump(t, 0.4, 1.5)
        turn = smooth(t, 1.6, 2.4)
        lean_in = smooth(t, 5.0, 5.8)
        pose_sol(sol, yaw=30 * turn, lean=-8 * shrug + 11 * lean_in, pitch=24 * up,
                 squash=0.05 * wobble(t, 0.5) + 0.05 * wobble(t, 5.0, decay=4),
                 arm_l=(-40 + 62 * shrug, 0), arm_r=(-40 + 62 * shrug + 52 * lean_in, 10 * lean_in),
                 blink=f in (97, 98), gaze=up)

    return animate(n, state)


def clip05():
    """Narrator: "So for a flame, up is just where the hot air goes. Got it?" 0.2-4.5.
    Sol tips the candle again, sweeps an arm up toward the spinning spiral, looks up and nods."""
    n = 168
    new_scene("candle_05", n)
    build_desk()
    candle = build_candle()
    stand = build_stand(0.0)
    sol = build_sol((-0.74, -0.05, 0), D(20))
    cam, tgt = build_camera()
    spin = {"a": 0.0}

    def state(t, f):
        k = smooth(t, 0.9, 3.3)
        cam.location = lerp3((0.3, -3.3, 0.8), (0.25, -6.1, 1.6), k)
        tgt.location = lerp3((-0.38, 0, 0.55), (-0.3, 0, 1.12), k)
        tilt = 22 * smooth(t, 0.3, 1.1) + 2.5 * wobble(t, 1.1, freq=13, decay=5)
        candle["piv"].rotation_euler = (0, D(tilt), 0)
        pose_flame(candle, f)
        spin["a"] += 2.6 * (1 / FPS)
        stand["spin"].rotation_euler = (0, 0, spin["a"])
        sweep = smooth(t, 1.7, 2.8) * (1 - smooth(t, 3.3, 3.9))      # free arm traces the hot air upward
        up = smooth(t, 3.3, 3.9)
        nod = bump(t, 4.65, 5.05) + bump(t, 5.05, 5.45)        # two clear nods
        pose_sol(sol, yaw=lerp(20, 14, up), lean=tilt * 0.42, pitch=9 * sweep + 24 * up - 34 * nod,
                 squash=0.04 * wobble(t, 1.1) + 0.04 * wobble(t, 2.8) + 0.07 * nod,
                 arm_r=(-6 + tilt * 0.5, 14), arm_l=(-40 + 120 * sweep, 0),
                 blink=f in (95, 96), gaze=0.7 * sweep * (1 - up) + up * (1 - nod))

    return animate(n, state)


result = {"01": clip01, "02": clip02, "03": clip03, "04": clip04, "05": clip05}[WHICH]()
