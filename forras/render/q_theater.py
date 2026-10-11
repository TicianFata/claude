import bpy, sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import theater, modes, scan
from mathutils import Vector

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "final", "theater")
os.makedirs(OUT, exist_ok=True)
stage = sys.argv[sys.argv.index("--") + 1]
RES = (1920, 1080)
CAMS = {
    "hero": ((0, -24.4, 6.1), (0, 4, 4.4), 21),
    "stage": ((0, 6.5, 2.7), (0, -14, 6.5), 16),
    "stalls": ((-1.5, -15.5, 2.6), (0, 6, 4.2), 24),
    "cut": ((-34, -52, 52), (0, -9, 0), 32),
    "cloud_over": ((-21, -45, 38), (0, -9, -1), 27),
}
BIM_RULES = [
    (r"^tier_|^gal_step", "Födém / erkély", (0.86, 0.78, 0.6)),
    (r"parapet|fascia", "Mellvéd", (0.95, 0.6, 0.32)),
    (r"seat", "Nézőtéri ülés", (0.28, 0.52, 0.86)),
    (r"^stage_floor|^apron|^pit_", "Színpad", (0.96, 0.84, 0.4)),
    (r"^step|^platform|^col_|^colcap|^colbase|^entablature|^flat_|^cyclorama", "Díszlet", (0.68, 0.52, 0.86)),
    (r"curtain|valance", "Függöny", (0.86, 0.34, 0.4)),
    (r"^bar_|^fix_|^fly_|^leg_|^border_", "Színpadtechnika", (0.3, 0.74, 0.64)),
    (r"chain|ch_ring|bulb|drop|ch_bowl|sconce", "Világítás", (1.0, 0.85, 0.3)),
    (r"ceiling|dome|ceil_band", "Mennyezet", (0.93, 0.93, 0.91)),
    (r"floor", "Padló", (0.72, 0.7, 0.66)),
    (r"outer_wall|^part_|prosc|^pil|^frame_|cartouche|frieze|stage_wall|stage_back|stage_roof", "Fal / szerkezet",
     (0.8, 0.83, 0.88)),
]


def cam(name):
    loc, tgt, lens = CAMS[name]
    c = camera("cam_" + name, loc, tgt, lens)
    bpy.context.scene.camera = c
    return c


def cutaway(C):
    for o in list(C["ceiling"].objects):
        o.hide_render = True
    for n in ("stage_roof", "outer_wall", "stage_wall_L", "stage_wall_R", "stage_back"):
        o = bpy.data.objects.get(n)
        if o:
            o.hide_render = True
    for o in C["stage"].objects:
        if o.name.startswith("fly_"):
            o.hide_render = True


t0 = time.time()
if stage == "photo":
    sc, M, C = theater.build()
    for s in ("hero", "stage", "stalls"):
        if os.path.exists(os.path.join(OUT, f"photo_{s}.png")):
            continue
        cam(s)
        render(os.path.join(OUT, f"photo_{s}.png"), RES, 64)
        print("done", s, time.time() - t0, flush=True)
elif stage == "panos":
    sc, M, C = theater.build()
    for name, loc, yaw in (("szinpad", (0, 1.2, 2.65), 180), ("nezoter", (0.0, -12.0, 1.85), 0),
                           ("paholy", (0, -25.3, 5.95), 0)):
        pc = pano_camera("p_" + name, loc)
        pc.rotation_euler[2] = math.radians(yaw)
        sc.camera = pc
        render(os.path.join(OUT, f"pano_{name}.png"), (3072, 1536), 28)
        print("done pano", name, time.time() - t0, flush=True)
elif stage == "vr":
    sc, M, C = theater.build()
    loc, tgt = Vector((0, -10.5, 2.1)), Vector((0, 7, 3.6))
    fwd = (tgt - loc).normalized()
    right = fwd.cross(Vector((0, 0, 1))).normalized()
    for eye, s in (("L", -1), ("R", 1)):
        c = camera("vr_" + eye, tuple(loc + right * 0.032 * s), tuple(tgt + right * 0.032 * s), 14)
        sc.camera = c
        render(os.path.join(OUT, f"vr_{eye}.png"), (1100, 1100), 40)
elif stage == "cut":
    sc, M, C = theater.build()
    cutaway(C)
    world_color((0.6, 0.62, 0.66), 0.6)
    light("cut_sun", "SUN", (-30, -40, 60), 2.0, (1.0, 0.95, 0.88), size=2.0, target=(0, 0, 0))
    cam("cut")
    render(os.path.join(OUT, "photo_cut.png"), RES, 48)
elif stage == "bim":
    sc, M, C = theater.build()
    used = modes.apply_bim(BIM_RULES)
    modes.bim_lighting()
    modes.set_view("AgX", "None", -0.7)
    inner = []
    for (x, y, z, sz, e) in [(0, -12, 13.8, 14, 5000), (0, 4, 12, 10, 3000), (-10, -12, 10.5, 6, 900), (10, -12, 10.5, 6, 900),
                             (0, -22, 10.5, 8, 900), (0, -12, 3.6, 12, 1200), (-11.5, -10, 7.0, 3, 500), (11.5, -10, 7.0, 3, 500),
                             (-11.5, -10, 3.6, 3, 500), (11.5, -10, 3.6, 3, 500), (0, -26, 7.0, 4, 500), (0, -26, 3.6, 4, 500)]:
        inner.append(light(f"bim_in_{x}_{y}_{z}", "AREA", (x, y, z), e, (1, 1, 1), size=sz, target=(x, y, -5)))
    cam("hero")
    render(os.path.join(OUT, "bim_hero.png"), RES, 48)
    for l in inner:
        l.hide_render = True
    cutaway(C)
    sc.view_settings.exposure = -0.9
    c = camera("cam_cutb", CAMS["cut"][0], CAMS["cut"][1], 37)
    sc.camera = c
    render(os.path.join(OUT, "bim_cut.png"), RES, 48)
    import json
    json.dump({k: v for k, v in used.items()}, open(os.path.join(OUT, "bim_legend.json"), "w"), ensure_ascii=False)
elif stage == "cloud":
    sc, M, C = theater.build()
    modes.hide_all_meshes(True)
    modes.hide_lights(True)
    world_color((0.008, 0.01, 0.016), 1.0)
    modes.set_view("Standard", "None", 0.0)
    sc.cycles.use_denoising = False
    pts, cols = modes.load_cloud(os.path.join(os.path.dirname(OUT), "..", "scan_theater", "cloud.npz"))
    print("cloud", len(pts))
    ob = scan.cloud_object("cloud", pts, cols, radius=0.015, emission=1.6)
    cam("hero")
    render(os.path.join(OUT, "cloud_hero.png"), RES, 24)
    # height colouring
    hc = scan.height_colors(pts, -1.0, 16.0)
    bpy.data.objects.remove(ob)
    ob = scan.cloud_object("cloud_h", pts, hc, radius=0.015, emission=1.0)
    render(os.path.join(OUT, "cloud_height_hero.png"), RES, 24)
    bpy.data.objects.remove(ob)
    # overview of the whole scan (crop away ceiling for readability)
    keep = pts[:, 2] < 13.8
    ob = scan.cloud_object("cloud_o", pts[keep], cols[keep], radius=0.022, emission=1.6)
    cam("cloud_over")
    render(os.path.join(OUT, "cloud_over.png"), RES, 24)
    bpy.data.objects.remove(ob)
    ob = scan.cloud_object("cloud_oh", pts[keep], hc[keep], radius=0.022)
    render(os.path.join(OUT, "cloud_over_height.png"), RES, 24)
elif stage in ("mesh", "meshover"):
    sc, M, C = theater.build()
    modes.hide_all_meshes(True)
    modes.hide_lights(True)
    pts, cols = modes.load_cloud(os.path.join(os.path.dirname(OUT), "..", "scan_theater", "cloud.npz"))
    rng = __import__("numpy").random.default_rng(0)
    sel = rng.random(len(pts)) < 0.5
    if stage == "meshover":
        sel &= pts[:, 2] < 13.8
    ob = modes.cloud_to_mesh("mesh", pts[sel], cols[sel], voxel=0.07, radius=0.08)
    ob.data.materials.append(modes.vertex_color_material("__vcol_wire__", wire=True, emission=1.7))
    world_color((0.55, 0.58, 0.62), 1.0)
    for (x, y, z, sz, e) in [(0, -12, 13.5, 14, 4000), (0, 4, 12, 10, 2500), (0, -12, 3.6, 12, 900)]:
        light(f"mesh_in_{x}_{y}", "AREA", (x, y, z), e, (1, 1, 1), size=sz, target=(x, y, -5))
    light("mesh_sun", "SUN", (-20, -40, 40), 1.2, (1, 0.97, 0.92), size=3, target=(0, 0, 0))
    modes.set_view("AgX", "None", 0.0)
    if stage == "mesh":
        cam("hero")
        render(os.path.join(OUT, "mesh_hero.png"), RES, 48)
    else:
        cam("cloud_over")
        render(os.path.join(OUT, "mesh_over.png"), RES, 48)
print("TOTAL", stage, time.time() - t0)
