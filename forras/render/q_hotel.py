import bpy, sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import hotel, modes

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "final", "hotel")
os.makedirs(OUT, exist_ok=True)
stage = sys.argv[sys.argv.index("--") + 1]
RES = (1920, 1080)
CAMS = {
    "hero": ((3.6, -4.6, 1.45), (-1.2, 2.6, 1.0), 18),
    "lounge": ((-1.6, -1.2, 1.35), (3.2, 4.2, 0.9), 22),
    "bed": ((2.6, -0.4, 1.25), (-3.6, -0.6, 0.75), 26),
    "cut": ((11.5, -13.5, 11.0), (-0.3, 0.3, 0.2), 30),
}
BIM_RULES = [
    (r"^glass|^mullion|^win_", "Nyílászáró / üvegezés", (0.62, 0.8, 0.95)),
    (r"sheer|drape", "Függöny / textil", (0.86, 0.36, 0.42)),
    (r"bed|mattress|duvet|throw|pillow|^hb_", "Ágy", (0.95, 0.62, 0.3)),
    (r"Sofa|Chair|^ns_|console|bench|^ct_|^tv", "Bútor", (0.28, 0.52, 0.86)),
    (r"Plant|Vase", "Növény / dekoráció", (0.45, 0.75, 0.4)),
    (r"lamp|^led_|^dl_|pend", "Világítás / elektromos", (1.0, 0.85, 0.3)),
    (r"^rug", "Szőnyeg", (0.75, 0.66, 0.85)),
    (r"^door|^art", "Ajtó / dekoráció", (0.68, 0.52, 0.86)),
    (r"floor", "Padló", (0.75, 0.72, 0.66)),
    (r"ceiling|soffit", "Mennyezet", (0.93, 0.93, 0.91)),
    (r"wall|slat", "Fal / burkolat", (0.8, 0.83, 0.88)),
]


def cam(name):
    loc, tgt, lens = CAMS[name]
    c = camera("cam_" + name, loc, tgt, lens)
    bpy.context.scene.camera = c
    return c


def cutaway():
    for o in bpy.context.scene.objects:
        if o.name in ("ceiling", "wall_R", "wall_back", "door", "door_handle", "tv", "art_back", "art_canvas") \
                or o.name.startswith(("soffit", "led_", "dl_", "pend", "bldg_", "sky", "ground_out", "console")):
            o.hide_render = True


t0 = time.time()
if stage == "photo":
    sc, M, C = hotel.build()
    for s in ("hero", "lounge", "bed"):
        cam(s)
        render(os.path.join(OUT, f"photo_{s}.png"), RES, 56)
        print("done", s, time.time() - t0, flush=True)
elif stage == "panos":
    sc, M, C = hotel.build()
    for name, loc, yaw in (("bejarat", (2.4, -3.6, 1.55), 0), ("agy", (0.2, -0.9, 1.55), 0),
                           ("ablak", (2.0, 3.9, 1.55), 180)):
        pc = pano_camera("p_" + name, loc)
        pc.rotation_euler[2] = math.radians(yaw)
        sc.camera = pc
        render(os.path.join(OUT, f"pano_{name}.png"), (3072, 1536), 28)
        print("done pano", name, time.time() - t0, flush=True)
elif stage == "cut":
    sc, M, C = hotel.build()
    cutaway()
    world_color((0.6, 0.62, 0.66), 0.7)
    sc.view_settings.exposure = -0.3
    light("cut_sun", "SUN", (20, -30, 40), 2.5, (1.0, 0.95, 0.88), size=2.0, target=(0, 0, 0))
    cam("cut")
    render(os.path.join(OUT, "photo_cut.png"), RES, 48)
elif stage == "bim":
    sc, M, C = hotel.build()
    modes.apply_bim(BIM_RULES)
    modes.hide_lights(True)
    for o in sc.objects:
        if o.name.startswith(("bldg_", "sky", "ground_out")):
            o.hide_render = True
    world_color((0.92, 0.94, 0.97), 1.0)
    light("bim_in1", "AREA", (0, -2, 2.95), 900, (1, 1, 1), size=5, target=(0, -2, 0))
    light("bim_in2", "AREA", (1, 3, 2.95), 700, (1, 1, 1), size=4, target=(1, 3, 0))
    modes.set_view("AgX", "None", -0.45)
    modes.freestyle(True, 0.9)
    cam("hero")
    render(os.path.join(OUT, "bim_hero.png"), RES, 48)
    for o in sc.objects:
        if o.name.startswith("bim_in"):
            o.hide_render = True
    cutaway()
    modes.bim_lighting(sun_dir=(0.4, -0.6, 0.8))
    modes.set_view("AgX", "None", -0.85)
    modes.freestyle(True, 0.9)
    cam("cut")
    render(os.path.join(OUT, "bim_cut.png"), RES, 48)
print("TOTAL", stage, time.time() - t0)
