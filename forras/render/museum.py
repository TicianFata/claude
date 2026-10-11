"""Procedural top-lit picture gallery with sculptures and vitrines – Brick+Data concept scene."""
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

L, W, H = 32.0, 12.0, 7.2      # hall length (y), width (x), cornice height
ART = os.path.join(TEX, "art")
ART_SIZES = {"cf3.jpg": [900, 700], "ls2.jpg": [1200, 800], "cf1.jpg": [800, 1000], "g2.jpg": [800, 1100], "cf2.jpg": [800, 1000], "ls1.jpg": [1200, 800], "g3.jpg": [1200, 700], "g1.jpg": [900, 900], "ls3.jpg": [1000, 1300]}


def art_mat(name, fname):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Roughness"].default_value = 0.55
    it = nt.nodes.new("ShaderNodeTexImage")
    it.image = bpy.data.images.load(os.path.join(ART, fname), check_existing=True)
    nt.links.new(it.outputs["Color"], p.inputs["Base Color"])
    return m


def plane_uv(name, w, h, material, coll):
    v = [(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)]
    ob = mesh_obj(name, v, [(0, 1, 2, 3)], material, coll)
    uv = ob.data.uv_layers.new()
    for i, (a, b) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[i].uv = (a, b)
    return ob


def painting(name, fname, center, width, wall_side, M, coll):
    """wall_side: +1 → on wall at +x facing -x; -1 → on wall at -x facing +x; 'yN'/'yS' end walls."""
    aspect = ART_SIZES[fname][1] / ART_SIZES[fname][0]
    h = width * aspect
    fw = 0.09
    x, y, z = center
    canvas = plane_uv(name, width, h, art_mat(name + "_m", fname), coll)
    parts = [canvas]
    parts.append(box(name + "_ft", (0, -0.02, h / 2 + fw / 2), (width + 2 * fw, 0.07, fw), M["frame"], coll, bevel=0.012))
    parts.append(box(name + "_fb", (0, -0.02, -h / 2 - fw / 2), (width + 2 * fw, 0.07, fw), M["frame"], coll, bevel=0.012))
    parts.append(box(name + "_fl", (-width / 2 - fw / 2, -0.02, 0), (fw, 0.07, h), M["frame"], coll, bevel=0.012))
    parts.append(box(name + "_fr", (width / 2 + fw / 2, -0.02, 0), (fw, 0.07, h), M["frame"], coll, bevel=0.012))
    parts.append(box(name + "_back", (0, 0.03, 0), (width + 0.1, 0.04, h + 0.1), M["frame"], coll))
    canvas.location = (0, -0.005, 0)
    ob = bpy.data.objects.new(name + "_grp", None)
    coll.objects.link(ob)
    for p in parts:
        p.parent = ob
    if wall_side == 1:
        ob.rotation_euler[2] = math.radians(-90)
    elif wall_side == -1:
        ob.rotation_euler[2] = math.radians(90)
    elif wall_side == "yN":
        ob.rotation_euler[2] = 0
    elif wall_side == "yS":
        ob.rotation_euler[2] = math.radians(180)
    ob.location = (x, y, z)
    return ob, h


def build():
    sc = reset(samples=96)
    sc.view_settings.exposure = -0.55
    world_color((0.55, 0.62, 0.72), 0.25)
    M = dict(
        wall=mat("m_wall", (0.09, 0.15, 0.145), rough=0.85, noise_var=0.12, noise_scale=1.5),
        trim=mat("m_trim", (0.82, 0.8, 0.74), rough=0.5),
        floor=mat("m_floor", (0.5, 0.4, 0.3), rough=0.35, tex="woodfloor_col.jpg", tex_scale=0.45,
                  tex_tint=(1.25, 1.1, 0.95), normal="woodfloor_nor.jpg", coat=0.25),
        frame=mat("m_frame", (0.78, 0.58, 0.3), rough=0.3, metal=1.0),
        dframe=mat("m_dframe", (0.06, 0.05, 0.05), rough=0.4),
        plinth=mat("m_plinth", (0.88, 0.87, 0.84), rough=0.6),
        marble=mat("m_marble", (0.9, 0.89, 0.86), rough=0.18, noise_var=0.18, noise_scale=3, coat=0.4),
        bronze=mat("m_bronze", (0.45, 0.3, 0.16), rough=0.32, metal=1.0),
        glass=mat("m_glass", (1, 1, 1), rough=0.0, transmission=1.0, ior=1.5),
        leather=mat("m_leather", (0.12, 0.07, 0.05), rough=0.45, coat=0.2),
        metal=mat("m_metal", (0.05, 0.05, 0.05), rough=0.35, metal=1.0),
        sky=emission_mat("m_skylight", (0.86, 0.92, 1.0), 4.0),
        lamp=emission_mat("m_lamp", (1.0, 0.86, 0.68), 30.0),
        banner=mat("m_banner", (0.62, 0.17, 0.12), rough=0.7),
        white=mat("m_white", (0.85, 0.84, 0.8), rough=0.7),
    )
    C = {k: collection(k) for k in ("architecture", "art", "furniture", "lighting", "ceiling", "exhibits")}

    # floor, walls, cornice
    box("floor", (0, 0, -0.1), (W, L, 0.2), M["floor"], C["architecture"])
    box("wall_W", (-W / 2 - 0.15, 0, H / 2), (0.3, L, H), M["wall"], C["architecture"])
    box("wall_E", (W / 2 + 0.15, 0, H / 2), (0.3, L, H), M["wall"], C["architecture"])
    # end walls with arched doorways (approximate with lintel + side pieces)
    for sy, nm in ((1, "N"), (-1, "S")):
        y = sy * (L / 2 + 0.15)
        box(f"end_{nm}_L", (-W / 2 + 2.25, y, H / 2), (4.5, 0.3, H), M["wall"], C["architecture"])
        box(f"end_{nm}_R", (W / 2 - 2.25, y, H / 2), (4.5, 0.3, H), M["wall"], C["architecture"])
        box(f"end_{nm}_T", (0, y, (4.2 + H) / 2), (3.0, 0.3, H - 4.2), M["wall"], C["architecture"])
        # door surround
        for x in (-1.6, 1.6):
            box(f"door_{nm}_{x}", (x, y - sy * 0.17, 2.1), (0.25, 0.08, 4.2), M["trim"], C["architecture"], bevel=0.02)
        box(f"door_{nm}_top", (0, y - sy * 0.17, 4.3), (3.45, 0.08, 0.25), M["trim"], C["architecture"], bevel=0.02)
        # adjacent room glimpse
        box(f"next_{nm}_floor", (0, y + sy * 4, -0.1), (8, 8, 0.2), M["floor"], C["architecture"])
        box(f"next_{nm}_back", (0, y + sy * 8, 3.5), (8, 0.3, 7), M["wall"], C["architecture"])
        box(f"next_{nm}_side1", (-4, y + sy * 4, 3.5), (0.3, 8, 7), M["wall"], C["architecture"])
        box(f"next_{nm}_side2", (4, y + sy * 4, 3.5), (0.3, 8, 7), M["wall"], C["architecture"])
        box(f"next_{nm}_ceil", (0, y + sy * 4, 6.0), (8, 8, 0.2), M["trim"], C["architecture"])
        light(f"next_{nm}_l", "AREA", (0, y + sy * 4, 5.8), 400, (1.0, 0.9, 0.78), size=4, target=(0, y + sy * 4, 0),
              coll=C["lighting"])
    # skirting + dado rail + cornice
    for sx in (-1, 1):
        x = sx * (W / 2 - 0.02)
        box(f"skirt_{sx}", (x, 0, 0.12), (0.06, L, 0.24), M["trim"], C["architecture"])
        box(f"cornice_{sx}", (sx * (W / 2 - 0.2), 0, H - 0.15), (0.5, L, 0.35), M["trim"], C["architecture"], bevel=0.05)
        box(f"cornice2_{sx}", (sx * (W / 2 - 0.08), 0, H - 0.5), (0.2, L, 0.12), M["trim"], C["architecture"], bevel=0.03)
    # coved ceiling with laylight
    def cove(u, v):
        a = math.pi / 2 * u
        x = (W / 2 - 0.45) - 1.6 * (1 - math.cos(a))
        z = H + 1.6 * math.sin(a)
        return (x, -L / 2 + L * v, z)
    for sx in (-1, 1):
        ob = grid_surface(f"cove_{sx}", 10, 2, lambda u, v, sx=sx: (sx * cove(u, v)[0], cove(u, v)[1], cove(u, v)[2]),
                          M["trim"], C["ceiling"])
    zc = H + 1.6
    xin = W / 2 - 0.45 - 1.6
    for sx in (-1, 1):
        box(f"ceilflat_{sx}", (sx * (xin - 0.5), 0, zc), (1.0, L, 0.1), M["trim"], C["ceiling"])
    box("laylight", (0, 0, zc + 0.6), (2 * xin - 2.0, L, 0.05), M["sky"], C["ceiling"])
    box("laylight_diff", (0, 0, zc), (2 * xin - 2.0, L, 0.02), mat("m_diffuser", (1, 1, 1), rough=0.6, transmission=0.9),
        C["ceiling"])
    for k in range(-15, 16, 2):
        box(f"mullion_{k}", (0, k, zc - 0.05), (2 * xin - 2.0, 0.08, 0.12), M["trim"], C["ceiling"])
    for x in (-1.6, 0, 1.6):
        box(f"mullionx_{x}", (x, 0, zc - 0.05), (0.08, L, 0.12), M["trim"], C["ceiling"])
    for sy in (-1, 1):
        box(f"ceil_end_{sy}", (0, sy * (L / 2 - 0.1), zc - 0.4), (W, 0.25, 1.2), M["trim"], C["ceiling"])
    light("sky_fill", "AREA", (0, 0, zc - 0.2), 6000, (0.9, 0.95, 1.0), size=6, target=(0, 0, 0), coll=C["lighting"])
    light("sky_fill2", "AREA", (0, 9, zc - 0.2), 2500, (0.9, 0.95, 1.0), size=5, target=(0, 9, 0), coll=C["lighting"])
    light("sky_fill3", "AREA", (0, -9, zc - 0.2), 2500, (0.9, 0.95, 1.0), size=5, target=(0, -9, 0), coll=C["lighting"])

    # paintings along long walls + track spots
    hang = [("ls1.jpg", 2.6), ("cf1.jpg", 1.6), ("g1.jpg", 1.8), ("ls2.jpg", 2.6), ("cf2.jpg", 1.6), ("g3.jpg", 2.8)]
    hang2 = [("g2.jpg", 1.6), ("ls3.jpg", 1.9), ("cf3.jpg", 2.2), ("g1.jpg", 1.6), ("ls1.jpg", 2.4), ("cf1.jpg", 1.5)]
    ys = [-12.5, -7.5, -2.5, 2.5, 7.5, 12.5]
    for side, seq in ((1, hang), (-1, hang2)):
        for i, (y, (f, w)) in enumerate(zip(ys, seq)):
            x = side * (W / 2 - 0.06)
            ob, h = painting(f"art_{side}_{i}", f, (x, y, 2.35), w, side, M, C["art"])
            ob.location.z = 1.6 + h / 2
            light(f"spot_{side}_{i}", "SPOT", (side * (W / 2 - 2.6), y, H + 0.5), 900, (1.0, 0.86, 0.7), size=0.08,
                  target=(x, y, 1.6 + h / 2), spot_deg=24, blend=0.45, coll=C["lighting"])
    # track rails
    for sx in (-1, 1):
        box(f"track_{sx}", (sx * (W / 2 - 2.6), 0, H + 0.62), (0.05, L - 1, 0.05), M["metal"], C["lighting"])
        for y in ys:
            cylinder(f"spotbody_{sx}_{y}", (sx * (W / 2 - 2.6), y, H + 0.5), 0.06, 0.22, M["metal"], C["lighting"])

    # free-standing exhibition wall (temporary show) with banner
    box("fs_wall", (0, 10.5, 1.75), (5.0, 0.35, 3.5), M["white"], C["exhibits"])
    box("fs_banner", (0, 10.31, 2.3), (3.4, 0.02, 1.6), M["banner"], C["exhibits"])
    txt = bpy.data.curves.new("title", "FONT")
    txt.body = "FÉNY ÉS TÉR"
    txt.align_x = "CENTER"
    txt.size = 0.42
    txt.extrude = 0.004
    tob = bpy.data.objects.new("title", txt)
    C["exhibits"].objects.link(tob)
    tob.location = (0, 10.29, 2.45)
    tob.rotation_euler = (math.radians(90), 0, 0)
    tob.data.materials.append(mat("m_title", (0.95, 0.9, 0.82), rough=0.5))
    txt2 = bpy.data.curves.new("sub", "FONT")
    txt2.body = "IDŐSZAKOS KIÁLLÍTÁS"
    txt2.align_x = "CENTER"
    txt2.size = 0.14
    t2 = bpy.data.objects.new("subtitle", txt2)
    C["exhibits"].objects.link(t2)
    t2.location = (0, 10.29, 2.05)
    t2.rotation_euler = (math.radians(90), 0, 0)
    t2.data.materials.append(tob.data.materials[0])
    light("fs_spot", "SPOT", (0, 6.5, H + 0.3), 1500, (1.0, 0.88, 0.72), size=0.1, target=(0, 10.3, 2.2), spot_deg=30,
          coll=C["lighting"])

    # plinths with sculptures
    def plinth(name, x, y, h=1.0, w=0.7):
        box(name, (x, y, h / 2), (w, w, h), M["plinth"], C["exhibits"], bevel=0.01)
        return h
    # 1) bronze torus-knot (procedural)
    plinth("pl_knot", 0, -8.0, 0.9, 0.9)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.45, minor_radius=0.12, major_segments=96, minor_segments=24,
                                     location=(0, -8.0, 1.55))
    knot = bpy.context.active_object
    knot.name = "sc_torus"
    knot.data.materials.append(M["bronze"])
    knot.rotation_euler = (math.radians(70), 0, math.radians(30))
    sw = knot.modifiers.new("tw", "SIMPLE_DEFORM")
    sw.deform_method = "TWIST"
    sw.angle = math.radians(160)
    for c in knot.users_collection:
        c.objects.unlink(knot)
    C["exhibits"].objects.link(knot)
    bpy.ops.object.shade_smooth()
    # 2) marble split sphere
    plinth("pl_sphere", -3.0, -1.0, 1.0)
    for k, dx in enumerate((-0.04, 0.04)):
        s = sphere(f"sc_half{k}", (-3.0 + dx * 2, -1.0, 1.42), 0.4, M["marble"], C["exhibits"], segs=48, rings=24)
        s.scale = (0.48, 1, 1)
        s.location.x = -3.0 + (-0.2 if k == 0 else 0.2)
    # 3) tall twisted column
    plinth("pl_col", 3.0, -1.0, 0.5, 0.8)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(3.0, -1.0, 1.75))
    col = bpy.context.active_object
    col.name = "sc_column"
    col.scale = (0.32, 0.32, 2.4)
    bpy.ops.object.transform_apply(scale=True)
    sub = col.modifiers.new("sub", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 1
    tw = col.modifiers.new("tw", "SIMPLE_DEFORM")
    tw.deform_method = "TWIST"
    tw.angle = math.radians(200)
    col.data.materials.append(M["marble"])
    for c in col.users_collection:
        c.objects.unlink(col)
    C["exhibits"].objects.link(col)
    # 4) antique camera (CC0, UX3D) on plinth
    plinth("pl_cam", -3.2, 5.0, 0.15, 1.4)
    try:
        root, objs = import_glb(os.path.join(MODELS, "AntiqueCamera.glb"), loc=(-2.95, 4.8, 0.15), rot_z=math.radians(35),
                                scale=0.2, coll=C["exhibits"])
    except Exception as e:
        print("camera import failed", e)
    # 5) vitrines with small objects
    for i, (x, y, model, sc_, rz, zoff) in enumerate([(3.2, 5.0, "ABeautifulGame.glb", 1.0, 0.5, 0.0),
                                                       (3.2, -12.0, "MosquitoInAmber.glb", 2.5, 0.4, 0.13)]):
        box(f"vit_base_{i}", (x, y, 0.45), (1.0, 1.0 if i == 0 else 0.7, 0.9), M["plinth"], C["exhibits"], bevel=0.01)
        box(f"vit_glass_{i}", (x, y, 1.32), (0.98, 0.98 if i == 0 else 0.68, 0.84), M["glass"], C["exhibits"])
        try:
            import_glb(os.path.join(MODELS, model), loc=(x, y, 0.9 + zoff), rot_z=rz, scale=sc_, coll=C["exhibits"])
        except Exception as e:
            print("import failed", model, e)
        light(f"vit_spot_{i}", "SPOT", (x, y - 1.2, H + 0.3), 700, (1.0, 0.9, 0.75), size=0.05, target=(x, y, 1.1),
              spot_deg=14, coll=C["lighting"])
    for nm, (x, y, z) in [("knot", (0, -8, 1.5)), ("sphere", (-3, -1, 1.4)), ("col", (3, -1, 2.0)), ("cam", (-3.2, 5, 0.9))]:
        light(f"sc_spot_{nm}", "SPOT", (x + 1.5, y - 2.0, H + 0.4), 1100, (1.0, 0.88, 0.72), size=0.1, target=(x, y, z),
              spot_deg=18, blend=0.5, coll=C["lighting"])
    # benches
    for y in (-4.5, 2.0):
        box(f"bench_{y}", (0, y, 0.42), (2.2, 0.6, 0.12), M["leather"], C["furniture"], bevel=0.03)
        for x in (-0.95, 0.95):
            box(f"bench_leg_{y}_{x}", (x, y, 0.18), (0.06, 0.5, 0.36), M["metal"], C["furniture"])
    # rope barriers
    for x in (-1.0, 1.0):
        cylinder(f"post_{x}", (x, -9.3, 0.45), 0.03, 0.9, M["frame"], C["furniture"])
    return sc, M, C


if __name__ == "__main__":
    build()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "museum.blend"))
