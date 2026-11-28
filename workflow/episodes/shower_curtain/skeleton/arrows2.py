"""Airflow arrows, version 2 (2026-11-27). Elaine on version 1: "the arrows look svery choppy ... theres random stuff
poking out of them". Version 1 rendered flat 3D arrows (two crossed planes, cut by hold-outs), so bits stuck out and
got clipped. Version 2 only DESCRIBES each arrow as a short ribbon of points in the scene, tail to head, following the
air's path; export_arrows.py projects those points through the clip's camera for every frame and
overlays/draw_arrows.py draws clean 2D arrows along them. Arrows fade in and out instead of popping.
TRACKS[clip] is a list of functions t -> None or {"pts": [(x, y, z), ...], "alpha": 0..1, "width": metres, "kind": "air"|"room"|"weak"}.
"""


def _fade(u, a=0.12, b=0.12):
    return smooth(u, 0.0, a) * (1 - smooth(u, 1 - b, 1.0))


def _tracks3():
    tr = []
    for P in ([(-0.14, 1.10, 2.55), (-0.14, 1.10, 1.45), (-0.14, 1.10, 0.62), (-0.14, 0.97, 0.30), (-0.14, 0.68, 0.24)],
              [(0.57, 1.24, 2.55), (0.57, 1.24, 1.80), (0.57, 1.24, 1.05), (0.57, 1.24, 0.38)]):
        for k in range(3):
            def fn(t, P=P, k=k):
                u = ((t - 1.9) / 2.3 + k / 3.0) % 1.0
                return {"pts": [cr(P, max(u - 0.17 * (1 - i / 13.0), 0.0)) for i in range(14)],
                        "alpha": _fade(u) * smooth(t, 1.9, 2.3), "width": 0.085, "kind": "air"}
            tr.append(fn)
    return tr


def _wheel(u, x=0.10, a=0.72, b=0.92):
    yc, _, zc, _ = LOOP
    c, s = math.cos(u), math.sin(u)
    return (x, yc + a * math.copysign(abs(c) ** 0.6, c), max(zc + b * math.copysign(abs(s) ** 0.6, s), 0.22))


def _loop(n, t0, t1, period=4.2):
    tr = []
    for k in range(n):
        def fn(t, k=k):
            th = TAU * k / n - TAU * t / period
            return {"pts": [_wheel(th + 0.58 * (1 - i / 15.0)) for i in range(16)],
                    "alpha": smooth(t, t0, t1), "width": 0.075, "kind": "air"}
        tr.append(fn)
    return tr


def _tracks5():
    tr = _loop(6, -0.4, 0.3)
    for k, (y, z) in enumerate(((0.05, 1.0), (0.65, 1.55), (0.65, 1.0), (0.05, 1.55))):
        def fn(t, y=y, z=z, k=k):
            u = (t * 0.6 + k * 0.25) % 1.0
            xh = -0.30 - 0.38 * u
            return {"pts": [(xh + 0.24 * (1 - i / 7.0), y, z) for i in range(8)],
                    "alpha": _fade(u, 0.3, 0.3) * smooth(t, 3.3, 3.9), "width": 0.05, "kind": "weak"}
        tr.append(fn)
    return tr


def _tracks6():
    tr, k = [], 0
    for y in (-1.0, -0.2, 0.6):
        for z in (0.75, 1.5):
            def fn(t, y=y, z=z, k=k):
                u = (t * 0.75 + k * 0.31) % 1.0
                xh = -1.78 + 0.80 * (u * u * (3 - 2 * u))
                return {"pts": [(xh - 0.58 * (1 - i / 7.0), y, z) for i in range(8)],
                        "alpha": _fade(u, 0.2, 0.2) * smooth(t, 0.2, 0.7) * (1 - smooth(t, 2.2, 2.7)), "width": 0.11, "kind": "room"}
            tr.append(fn)
            k += 1
    return tr


TRACKS = {"3": _tracks3, "4": lambda: _loop(6, 1.7, 2.5), "5": _tracks5, "6": _tracks6}
