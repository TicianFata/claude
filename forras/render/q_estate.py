import bpy, sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import estate, modes
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "final", "estate")
os.makedirs(OUT, exist_ok=True)
stage = sys.argv[sys.argv.index("--") + 1]
RES = (1920, 1080)
CAMS = {
    "event": ((62, -128, 42), (-8, -58, 0), 30),
    "hotel": ((58, 78, 34), (-2, 22, 1), 30),
    "wide": ((-150, -175, 95), (0, -35, 0), 34),
    "layout": ((62, -128, 42), (-8, -58, 0), 30),
    "layout_axo": ((70, -125, 70), (-6, -58, 0), 34),
    "facade": ((0, -58, 7.5), (0, -7, 7.2), 36),
}
LAYOUT_RULES = [
    (r"^stage|^tower|^truss|^array|^led_wall", "Színpad", (0.2, 0.22, 0.28)),
    (r"^dance", "Táncparkett", (0.55, 0.45, 0.4)),
    (r"^tent", "Sátor", (0.97, 0.97, 0.97)),
    (r"^tbl|^ch_|^bar", "Asztal / szék", (0.96, 0.6, 0.25)),
    (r"^wc", "Mosdókonténer", (0.28, 0.52, 0.86)),
    (r"^stand|^awning", "Büfé / stand", (0.86, 0.34, 0.4)),
    (r"^pole|^bulb", "Fényfüzér", (1.0, 0.82, 0.3)),
    (r"proto|^ave_|^park_|^grove_|^forest_|^pool_tree|parterre", "Növényzet", (0.62, 0.74, 0.58)),
    (r"^ground", "Terep", (0.86, 0.88, 0.84)),
    (r"forecourt|avenue|path|terrace", "Út / burkolat", (0.93, 0.92, 0.89)),
    (r"pool|lounger|umb", "Medencekert", (0.62, 0.8, 0.95)),
    (r"fountain", "Szökőkút", (0.62, 0.8, 0.95)),
]
THERMAL = [
    (r"^win_.*", 0.62, 0.0),
    (r"^dormer_win", 0.7, 0.0),
    (r"^door", 0.58, 0.0),
    (r"^chimney", 0.8, 0.0),
    (r"^wsur", 0.4, 0.0),
    (r"^roof|^cupola|^lantern", 0.18, 0.004),
    (r"^plinth", 0.42, 0.0),
    (r"^band|^pil|pediment", 0.33, 0.004),
    (r"^block|^risalit|^pavilion", 0.3, 0.008),
    (r"^ground|forecourt|avenue|path|terrace", 0.1, 0.0),
    (r"proto|^ave_|^park_|^grove_|^forest_|parterre", 0.14, 0.0),
]


def cam(name):
    loc, tgt, lens = CAMS[name]
    c = camera("cam_" + name, loc, tgt, lens)
    bpy.context.scene.camera = c
    return c


t0 = time.time()
if stage == "dusk":
    sc, M, C = estate.build(event=True, pool=True, dusk=True)
    for s in ("event", "hotel", "wide"):
        cam(s)
        render(os.path.join(OUT, f"drone_{s}.png"), RES, 48)
        print("done", s, time.time() - t0, flush=True)
elif stage == "video":
    sc, M, C = estate.build(event=True, pool=True, dusk=True)
    sc.render.use_persistent_data = True
    c = camera("vid", (0, 0, 0), (0, 0, 1), 28)
    sc.camera = c
    n = 150
    vdir = os.path.join(OUT, "video_frames")
    os.makedirs(vdir, exist_ok=True)
    for f in range(n):
        t = f / (n - 1)
        e = 0.5 - 0.5 * math.cos(math.pi * t)  # ease in/out
        a = math.radians(-115 + 95 * e)
        r = 135 - 40 * e
        loc = Vector((r * math.cos(a), -40 + r * math.sin(a), 52 - 18 * e))
        tgt = Vector((-6 + 4 * e, -48 + 18 * e, 2))
        c.location = loc
        look_at(c, tgt)
        p = os.path.join(vdir, f"f{f:04d}.png")
        if not os.path.exists(p):
            render(p, (1280, 720), 14)
        print("frame", f, time.time() - t0, flush=True)
elif stage == "day":
    sc, M, C = estate.build(event=True, pool=True, dusk=False)
    # top-down map (orthographic)
    cd = bpy.data.cameras.new("map")
    cd.type = "ORTHO"
    cd.ortho_scale = 260
    cd.clip_end = 1000
    mc = bpy.data.objects.new("map", cd)
    sc.collection.objects.link(mc)
    mc.location = (0, -30, 300)
    mc.rotation_euler = (0, 0, 0)
    sc.camera = mc
    render(os.path.join(OUT, "map_top.png"), (2000, 1300), 48)
    print("map", time.time() - t0, flush=True)
    cam("hotel")
    render(os.path.join(OUT, "drone_hotel_day.png"), RES, 64)
elif stage == "layout":
    sc, M, C = estate.build(event=True, pool=True, dusk=False)
    used = modes.apply_bim(LAYOUT_RULES, default=("Épület", (0.96, 0.95, 0.92)))
    modes.bim_lighting(sun_dir=(-0.6, -0.5, 0.9))
    modes.set_view("AgX", "None", -0.6)
    modes.freestyle(True, 0.8, crease=140)
    for o in sc.objects:
        if o.name.startswith(("forest_", "park_")):
            o.hide_render = True
    cam("layout")
    render(os.path.join(OUT, "layout_model.png"), RES, 48)
    cam("layout_axo")
    render(os.path.join(OUT, "layout_axo.png"), RES, 48)
elif stage == "thermal":
    sc, M, C = estate.build(event=False, pool=False, dusk=True)
    modes.apply_thermal(THERMAL, default=0.25)
    sc.cycles.use_denoising = True
    cam("facade")
    render(os.path.join(OUT, "thermal_facade.png"), RES, 32)
elif stage == "pano":
    sc, M, C = estate.build(event=True, pool=True, dusk=True)
    for name, loc, yaw in (("asztalok", (-2.5, -62.0, 1.7), 90), ("szinpad", (-32.0, -62.0, 1.7), -90),
                           ("bejarat", (0.0, -24.0, 1.7), 180)):
        pc = pano_camera("p_" + name, loc)
        pc.rotation_euler[2] = math.radians(yaw)
        sc.camera = pc
        render(os.path.join(OUT, f"pano_{name}.png"), (3072, 1536), 28)
        print("done pano", name, time.time() - t0, flush=True)
elif stage == "scan":
    import scan
    sc, M, C = estate.build(event=False, pool=True, dusk=False)
    st = [("e1", (-30, -50, 1.8)), ("e2", (0, -62, 1.8)), ("e3", (25, -45, 1.8)), ("e4", (-8, -28, 1.8)),
          ("e5", (30, -86, 1.8)), ("e6", (-38, -88, 1.8)), ("e7", (14, -16, 1.8)), ("e8", (-20, -14, 1.8))]
    scan.run(st, os.path.join(HERE, "scan_estate"), res=(2400, 1200), samples=24, voxel=0.05, max_range=130)
elif stage == "cloudplan":
    import scan, numpy as np, bmesh, json
    sc, M, C = estate.build(event=True, pool=True, dusk=False)
    used = modes.apply_bim(LAYOUT_RULES, default=("Épület", (0.96, 0.95, 0.92)))
    # sample planned event objects into coloured points (for the web viewer)
    dg = bpy.context.evaluated_depsgraph_get()
    rng = np.random.default_rng(3)
    P, Cl = [], []
    for o in C["event"].objects:
        if o.type != "MESH" or o.location.z < -10:
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        col = np.array(me.materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3]) if len(me.materials) else np.array([.8, .8, .8])
        mw = np.array(o.matrix_world)
        for tri in me.loop_triangles:
            v = np.array([me.vertices[i].co[:] for i in tri.vertices])
            area = tri.area * (o.scale[0] * o.scale[1])
            n = rng.poisson(area * 220)
            if n == 0:
                continue
            r1, r2 = rng.random(n), rng.random(n)
            s1 = np.sqrt(r1)
            pts = (1 - s1)[:, None] * v[0] + (s1 * (1 - r2))[:, None] * v[1] + (s1 * r2)[:, None] * v[2]
            pts = pts @ mw[:3, :3].T + mw[:3, 3]
            P.append(pts)
            Cl.append(np.repeat((col ** (1 / 2.2) * 255).astype(np.uint8)[None], n, 0))
        ev.to_mesh_clear()
    np.savez_compressed(os.path.join(HERE, "scan_estate", "plan.npz"), pts=np.concatenate(P).astype(np.float32),
                        cols=np.concatenate(Cl))
    # still: venue point cloud + planned elements as solid model
    for o in sc.objects:
        if o.type in ("MESH", "EMPTY", "CURVE") and o.name not in C["event"].objects:
            o.hide_render = True
    for o in C["lighting"].objects:
        if o.type == "MESH":
            o.hide_render = False
    pts, cols = modes.load_cloud(os.path.join(HERE, "scan_estate", "cloud.npz"))
    cl = scan.cloud_object("venue", pts, cols, radius=0.07, emission=1.2)
    modes.hide_lights(True)
    world_color((0.008, 0.01, 0.016), 1.0)
    light("plan_sun", "SUN", (-40, -60, 80), 2.5, (1, 0.97, 0.92), size=3, target=(0, 0, 0))
    modes.set_view("AgX", "None", 0.0)
    cam("event")
    render(os.path.join(OUT, "cloudplan_event.png"), RES, 32)
    cl.hide_render = True
    for o in C["event"].objects:
        o.hide_render = True
    cl.hide_render = False
    render(os.path.join(OUT, "cloud_venue.png"), RES, 24)
print("TOTAL", stage, time.time() - t0)
