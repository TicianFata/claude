"""Export scanned clouds for the web viewer as data scripts (quantised uint16 xyz + uint8 rgb, base64)."""
import os, sys, json, base64
import numpy as np

W = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/user/claude/portfolio/assets/cloud"
os.makedirs(OUT, exist_ok=True)


def export(name, pts, cols, n_max, views, path, extra=None):
    rng = np.random.default_rng(0)
    if len(pts) > n_max:
        idx = rng.choice(len(pts), n_max, replace=False)
        pts, cols = pts[idx], cols[idx]
    mn, mx = pts.min(0), pts.max(0)
    q = np.round((pts - mn) / np.maximum(mx - mn, 1e-6) * 65535).astype("<u2")
    d = {"n": int(len(pts)), "min": [float(v) for v in mn], "max": [float(v) for v in mx],
         "pos": base64.b64encode(q.tobytes()).decode(), "col": base64.b64encode(cols.astype(np.uint8).tobytes()).decode(),
         "views": views, "path": path}
    if extra:
        d.update(extra)
    js = "window.BD_CLOUDS=window.BD_CLOUDS||{};window.BD_CLOUDS[%s]=%s;\n" % (json.dumps(name), json.dumps(d, ensure_ascii=False))
    open(os.path.join(OUT, name + ".js"), "w").write(js)
    print(name, len(pts), round(len(js) / 1e6, 1), "MB")


def V(name, pos, target):
    return {"name": name, "pos": list(pos), "target": list(target)}


which = sys.argv[1:] or ["muzeum", "szinhaz", "rendezveny"]
if "muzeum" in which and os.path.exists(os.path.join(W, "scan_museum", "cloud.npz")):
    d = np.load(os.path.join(W, "scan_museum", "cloud.npz"))
    p, c = d["pts"], d["cols"]
    k = (p[:, 2] < 7.2) & (np.abs(p[:, 1]) < 16.4)
    export("muzeum", p[k], c[k], 650000,
           [V("Bejárat", (0, -15, 1.7), (0, 0, 1.6)), V("Kiállítási fal", (1.5, 4.5, 1.7), (0, 10.4, 2.2)),
            V("Felülnézet", (-14, -22, 17), (0, -1, 0.5))],
           [{"pos": [-12, -24, 15], "target": [0, -2, 0.5]}, {"pos": [0, -15.5, 1.8], "target": [0, 0, 1.6]},
            {"pos": [-1.5, -8, 1.7], "target": [0, -3, 1.4]}, {"pos": [2.0, -1.0, 1.8], "target": [-3, 2, 1.5]},
            {"pos": [0.5, 5.0, 1.8], "target": [0, 10.4, 2.2]}, {"pos": [-3.5, 9.5, 3.2], "target": [3, 0, 1.2]},
            {"pos": [-13, -18, 13], "target": [0, 0, 0.5]}],
           {"size": 0.05, "fog": 0.012, "gain": 1.5, "pathSeconds": 26, "zrange": [0, 7]})
if "szinhaz" in which and os.path.exists(os.path.join(W, "scan_theater", "cloud.npz")):
    d = np.load(os.path.join(W, "scan_theater", "cloud.npz"))
    p, c = d["pts"], d["cols"]
    k = p[:, 2] < 13.9
    export("szinhaz", p[k], c[k], 750000,
           [V("Páholy", (0, -24.5, 6.0), (0, 4, 4.4)), V("Színpad", (0, 5.5, 2.8), (0, -14, 6)),
            V("Felülnézet", (-30, -48, 36), (0, -9, 0))],
           [{"pos": [-30, -48, 36], "target": [0, -9, 0]}, {"pos": [0, -24.5, 6.0], "target": [0, 4, 4.4]},
            {"pos": [-2, -14, 2.4], "target": [0, 4, 3.5]}, {"pos": [0, -3, 2.6], "target": [0, 8, 3.5]},
            {"pos": [2.5, 6.5, 3.0], "target": [0, -14, 6]}, {"pos": [-8, -10, 10], "target": [4, -14, 6]},
            {"pos": [-28, -44, 30], "target": [0, -9, 0]}],
           {"size": 0.072, "fog": 0.006, "gain": 1.9, "pathSeconds": 28, "zrange": [-1, 14]})
if "rendezveny" in which and os.path.exists(os.path.join(W, "scan_estate", "cloud.npz")):
    d = np.load(os.path.join(W, "scan_estate", "cloud.npz"))
    p, c = d["pts"], d["cols"]
    k = (np.abs(p[:, 0]) < 110) & (p[:, 1] > -150) & (p[:, 1] < 60) & (p[:, 2] < 30)
    p, c = p[k], c[k]
    rng = np.random.default_rng(1)
    if len(p) > 520000:
        i = rng.choice(len(p), 520000, replace=False)
        p, c = p[i], c[i]
    pl = os.path.join(W, "scan_estate", "plan.npz")
    if os.path.exists(pl):
        e = np.load(pl)
        pp, pc = e["pts"], e["cols"]
        if len(pp) > 260000:
            i = rng.choice(len(pp), 260000, replace=False)
            pp, pc = pp[i], pc[i]
        p, c = np.concatenate([p, pp]), np.concatenate([c, pc])
    export("rendezveny", p, c, 900000,
           [V("Rendezvénytér", (62, -128, 42), (-8, -58, 0)), V("Színpad elől", (-14, -62, 6), (-44, -62, 4)),
            V("Kastély", (6, -64, 9), (0, -7, 6))],
           [{"pos": [95, -150, 70], "target": [-5, -50, 0]}, {"pos": [62, -128, 42], "target": [-8, -58, 0]},
            {"pos": [20, -95, 12], "target": [-10, -60, 1]}, {"pos": [-14, -62, 6], "target": [-44, -62, 4]},
            {"pos": [-20, -40, 10], "target": [0, -7, 5]}, {"pos": [40, -30, 30], "target": [-8, -58, 0]},
            {"pos": [95, -150, 70], "target": [-5, -50, 0]}],
           {"size": 0.3, "fog": 0.002, "gain": 1.3, "pathSeconds": 30, "zrange": [0, 20]})
