import bpy, sys, os, time, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import museum, modes, scan
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "final", "museum")
SCAN = os.path.join(HERE, "scan_museum")
os.makedirs(OUT, exist_ok=True)
stage = sys.argv[sys.argv.index("--") + 1]
RES = (1920, 1080)
CAMS = {
    "hero": ((0, -15.2, 1.65), (0, 4, 2.6), 20),
    "diag": ((4.6, -6.5, 1.55), (-3.5, 2.5, 1.9), 22),
    "over": ((-17, -27, 21), (0, -1.5, 0.3), 30),
}
BIM_RULES = [
    (r"^art_", "Műtárgy (festmény)", (0.95, 0.62, 0.3)),
    (r"^sc_|^pl_|^vit_|AntiqueCamera|ABeautifulGame|Mosquito", "Műtárgy / installáció", (0.68, 0.52, 0.86)),
    (r"^fs_|^title|^subtitle", "Kiállítási fal", (0.86, 0.36, 0.42)),
    (r"^bench|^post", "Bútor", (0.3, 0.74, 0.64)),
    (r"^track|^spotbody", "Világítás", (1.0, 0.85, 0.3)),
    (r"laylight|mullion|^cove|ceilflat|ceil_end", "Mennyezet / felülvilágító", (0.62, 0.8, 0.95)),
    (r"floor", "Padló", (0.75, 0.72, 0.66)),
    (r"^skirt|^cornice|^door_", "Tagozat / ajtókeret", (0.96, 0.84, 0.4)),
    (r"wall|^end_|^next_", "Fal / szerkezet", (0.8, 0.83, 0.88)),
]
THERMAL = [
    (r"^spotbody", 1.0, 0.0),
    (r"^track", 0.86, 0.0),
    (r"laylight|^mullion", 0.04, 0.0),
    (r"^cove|ceilflat|ceil_end", 0.3, 0.025),
    (r"^art_", 0.64, 0.0),
    (r"^fs_|^title|^subtitle", 0.58, 0.0),
    (r"^bench", 0.6, 0.0),
    (r"^vit_|^pl_|^sc_|AntiqueCamera|ABeautifulGame|Mosquito", 0.4, 0.0),
    (r"floor", 0.16, 0.0),
    (r"^next_", 0.5, 0.0),
    (r"^skirt", 0.2, 0.0),
    (r"^cornice", 0.5, 0.0),
    (r"^end_|^door_", 0.24, 0.04),
    (r"wall", 0.22, 0.045),
]


def cam(name):
    loc, tgt, lens = CAMS[name]
    c = camera("cam_" + name, loc, tgt, lens)
    bpy.context.scene.camera = c
    return c


def no_ceiling():
    for o in bpy.context.scene.objects:
        if any(o.name.startswith(p) for p in ("cove", "ceilflat", "laylight", "mullion", "ceil_end", "next_", "wall_W",
                                               "skirt_-1", "cornice_-1", "cornice2_-1", "art_-1", "spot_-1", "track_-1",
                                               "spotbody_-1", "end_S", "door_S")):
            o.hide_render = True
        if o.parent and o.parent.name.startswith("art_-1"):
            o.hide_render = True


t0 = time.time()
if stage == "photo":
    sc, M, C = museum.build()
    for s in ("hero", "diag"):
        cam(s)
        render(os.path.join(OUT, f"photo_{s}.png"), RES, 56)
        print("done", s, time.time() - t0, flush=True)
elif stage == "panos":
    sc, M, C = museum.build()
    for name, loc in (("bejarat", (1.7, -11.2, 1.6)), ("kozep", (1.2, 0.5, 1.6)), ("kiallitas", (-1.5, 7.2, 1.6))):
        if name != "bejarat" and os.path.exists(os.path.join(OUT, f"pano_{name}.png")):
            continue
        sc.camera = pano_camera("p_" + name, loc)
        render(os.path.join(OUT, f"pano_{name}.png"), (3072, 1536), 28)
        print("done pano", name, time.time() - t0, flush=True)
elif stage == "scan":
    sc, M, C = museum.build()
    st = [("s1", (0, -12.5, 1.7)), ("s2", (0.4, -4.0, 1.7)), ("s3", (-0.4, 4.0, 1.7)), ("s4", (3.0, 12.6, 1.7)),
          ("s5", (-4.0, -8.5, 1.7)), ("s6", (4.2, 1.5, 1.7))]
    scan.run(st, SCAN, res=(1600, 800), samples=32, voxel=0.01, max_range=40)
elif stage == "cloud":
    sc, M, C = museum.build()
    modes.hide_all_meshes(True)
    modes.hide_lights(True)
    world_color((0.008, 0.01, 0.016), 1.0)
    modes.set_view("Standard", "None", 0.0)
    pts, cols = modes.load_cloud(os.path.join(SCAN, "cloud.npz"))
    ob = scan.cloud_object("cloud", pts, cols, radius=0.009, emission=1.3)
    cam("hero")
    render(os.path.join(OUT, "cloud_hero.png"), RES, 24)
    bpy.data.objects.remove(ob)
    keep = (pts[:, 2] < 7.0) & (pts[:, 0] > -5.5) & (pts[:, 1] > -15.9)
    ob = scan.cloud_object("cloud_o", pts[keep], cols[keep], radius=0.016, emission=1.3)
    cam("over")
    render(os.path.join(OUT, "cloud_over.png"), RES, 24)
elif stage == "bim":
    sc, M, C = museum.build()
    modes.apply_bim(BIM_RULES)
    modes.bim_lighting()
    modes.set_view("AgX", "None", -0.9)
    modes.freestyle(True, 0.9)
    no_ceiling()
    cam("over")
    render(os.path.join(OUT, "bim_over.png"), RES, 48)
elif stage == "thermal":
    sc, M, C = museum.build()
    modes.apply_thermal(THERMAL, default=0.35)
    sc.cycles.use_denoising = True
    cam("hero")
    render(os.path.join(OUT, "thermal_hero.png"), RES, 32)
elif stage == "cut":
    sc, M, C = museum.build()
    no_ceiling()
    light("cut_sun", "SUN", (-30, -40, 60), 2.0, (1.0, 0.96, 0.9), size=2.0, target=(0, 0, 0))
    cam("over")
    render(os.path.join(OUT, "photo_over.png"), RES, 48)
print("TOTAL", stage, time.time() - t0)
