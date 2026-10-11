"""Procedural boutique-hotel suite at blue hour – Brick+Data concept scene.
Furniture models: Khronos glTF Sample Assets (SheenChair CC0, GlamVelvetSofa CC BY 4.0 Wayfair,
DiffuseTransmissionPlant CC BY 4.0, GlassVaseFlowers CC0)."""
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

X0, X1, Y0, Y1, H = -4.0, 4.0, -5.0, 5.0, 3.1


def city_mat(name, seed):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.35
    br.inputs["Brick Width"].default_value = 1.6
    br.inputs["Row Height"].default_value = 3.2
    br.inputs["Color1"].default_value = (1.0, 0.66, 0.32, 1)
    br.inputs["Color2"].default_value = (0.02, 0.025, 0.04, 1)
    br.inputs["Mortar"].default_value = (0.012, 0.014, 0.022, 1)
    br.inputs["Bias"].default_value = 0.55
    br.offset = 0.0
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 3.0
    nt.links.new(br.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    return m


def soft_box(name, center, size, material, coll, bevel=0.06, sub=2, noise=0.0):
    ob = box(name, center, size, material, coll)
    bv = ob.modifiers.new("bv", "BEVEL")
    bv.width = bevel
    bv.segments = 3
    if sub:
        s = ob.modifiers.new("sub", "SUBSURF")
        s.levels = sub
        s.render_levels = sub
    if noise:
        tex = bpy.data.textures.new(name + "_n", "CLOUDS")
        tex.noise_scale = 0.25
        d = ob.modifiers.new("disp", "DISPLACE")
        d.texture = tex
        d.strength = noise
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def build():
    sc = reset(samples=96)
    sc.view_settings.exposure = -1.0
    world_color((0.05, 0.08, 0.16), 0.6)
    M = dict(
        floor=mat("h_floor", (0.6, 0.45, 0.32), rough=0.38, tex="woodfloor_col.jpg", tex_scale=0.5,
                  tex_tint=(1.25, 1.1, 0.95), normal="woodfloor_nor.jpg", coat=0.03),
        wall=mat("h_wall", (0.72, 0.66, 0.58), rough=0.85, noise_var=0.08, noise_scale=2),
        ceiling=mat("h_ceiling", (0.85, 0.83, 0.8), rough=0.9),
        slats=mat("h_slats", (0.32, 0.2, 0.12), rough=0.45, tex="wood_col.jpg", tex_scale=1.5, tex_tint=(1.6, 1.3, 1.1)),
        headboard=mat("h_headboard", (0.06, 0.18, 0.2), rough=0.8, sheen=1.0, sheen_tint=(0.6, 0.9, 0.9)),
        linen=mat("h_linen", (0.88, 0.87, 0.84), rough=0.9, sheen=0.5),
        throw=mat("h_throw", (0.62, 0.36, 0.18), rough=0.9, sheen=0.8, tex="fabric_col.jpg", tex_scale=5,
                  tex_tint=(1.4, 1.0, 0.7)),
        rug=mat("h_rug", (0.42, 0.38, 0.33), rough=0.98, noise_var=0.25, noise_scale=60, bump_noise=0.25),
        brass=mat("h_brass", (0.8, 0.6, 0.32), rough=0.25, metal=1.0),
        marble=mat("h_marble", (0.9, 0.88, 0.85), rough=0.12, noise_var=0.15, noise_scale=4, coat=0.5),
        darkwood=mat("h_darkwood", (0.18, 0.1, 0.06), rough=0.35, tex="wood_col.jpg", tex_scale=2.0, coat=0.4),
        frame=mat("h_frame", (0.02, 0.02, 0.02), rough=0.35, metal=0.6),
        glass=mat("h_glass", (1, 1, 1), rough=0.0, transmission=1.0, ior=1.45),
        sheer=mat("h_sheer", (0.95, 0.93, 0.9), rough=0.8, transmission=0.55, sheen=0.4),
        drape=mat("h_drape", (0.08, 0.2, 0.22), rough=0.85, sheen=1.0, sheen_tint=(0.6, 0.9, 0.9)),
        shade=emission_mat("h_shade", (1.0, 0.72, 0.45), 6.0),
        led=emission_mat("h_led", (1.0, 0.74, 0.45), 14.0),
        sky=gradient_emission_mat("h_sky", (1.0, 0.5, 0.25), (0.05, 0.09, 0.3), -14, 26, 2.2),
        city=city_mat("h_city", 1),
        dark=mat("h_dark", (0.015, 0.018, 0.025), rough=0.8),
        tv=mat("h_tv", (0.01, 0.01, 0.012), rough=0.08, coat=1.0),
    )
    C = {k: collection(k) for k in ("architecture", "furniture", "lighting", "glazing", "outside")}

    # shell
    box("floor", (0, 0, -0.1), (X1 - X0, Y1 - Y0, 0.2), M["floor"], C["architecture"])
    box("ceiling", (0, 0, H + 0.1), (X1 - X0, Y1 - Y0, 0.2), M["ceiling"], C["architecture"])
    box("wall_L", (X0 - 0.1, 0, H / 2), (0.2, Y1 - Y0, H), M["wall"], C["architecture"])
    box("wall_R", (X1 + 0.1, 0, H / 2), (0.2, Y1 - Y0, H), M["wall"], C["architecture"])
    box("wall_back", (0, Y0 - 0.1, H / 2), (X1 - X0, 0.2, H), M["wall"], C["architecture"])
    # entrance door on back wall
    box("door", (2.6, Y0 + 0.02, 1.1), (1.0, 0.06, 2.2), M["darkwood"], C["architecture"], bevel=0.01)
    cylinder("door_handle", (2.2, Y0 + 0.08, 1.05), 0.012, 0.16, M["brass"], C["architecture"], axis="X")
    # lowered ceiling cove + LED strip
    for (cx, cy, sx, sy) in [(0, Y1 - 0.35, X1 - X0, 0.7), (0, Y0 + 0.35, X1 - X0, 0.7), (X0 + 0.35, 0, 0.7, Y1 - Y0),
                             (X1 - 0.35, 0, 0.7, Y1 - Y0)]:
        box(f"soffit_{cx}_{cy}", (cx, cy, H - 0.2), (sx, sy, 0.4), M["ceiling"], C["architecture"])
    for (cx, cy, sx, sy) in [(0, Y1 - 0.72, X1 - X0 - 1.5, 0.03), (0, Y0 + 0.72, X1 - X0 - 1.5, 0.03),
                             (X0 + 0.72, 0, 0.03, Y1 - Y0 - 1.5), (X1 - 0.72, 0, 0.03, Y1 - Y0 - 1.5)]:
        box(f"led_{cx}_{cy}", (cx, cy, H - 0.38), (sx, sy, 0.03), M["led"], C["lighting"])
    # window wall (y = Y1): glazing + mullions
    box("win_sill", (0, Y1 + 0.1, 0.05), (X1 - X0, 0.2, 0.1), M["frame"], C["glazing"])
    box("win_head", (0, Y1 + 0.1, H - 0.15), (X1 - X0, 0.2, 0.3), M["frame"], C["glazing"])
    for x in (-4.0, -1.33, 1.33, 4.0):
        box(f"mullion_{x}", (x, Y1 + 0.1, H / 2), (0.08, 0.2, H), M["frame"], C["glazing"])
    box("glass", (0, Y1 + 0.12, H / 2), (X1 - X0, 0.02, H), M["glass"], C["glazing"])
    # sheer curtains + drapes (folded)
    def fold(name, x0, x1, folds, depth, y0, material):
        def fn(u, v):
            return (x0 + (x1 - x0) * u, y0 + depth * math.sin(u * folds * 2 * math.pi), 0.02 + (H - 0.45) * v)
        ob = grid_surface(name, folds * 8, 6, fn, material, C["glazing"])
        s = ob.modifiers.new("s", "SOLIDIFY")
        s.thickness = 0.01
        return ob
    fold("sheer_L", -3.95, -2.6, 6, 0.05, Y1 - 0.12, M["sheer"])
    fold("sheer_R", 2.6, 3.95, 6, 0.05, Y1 - 0.12, M["sheer"])
    fold("drape_L", -3.95, -3.2, 4, 0.07, Y1 - 0.3, M["drape"])
    fold("drape_R", 3.2, 3.95, 4, 0.07, Y1 - 0.3, M["drape"])
    # outside: dusk sky + city silhouettes with lit windows
    box("sky", (0, 70, 5), (260, 1, 80), M["sky"], C["outside"])
    rnd = random.Random(3)
    for i in range(26):
        x = -60 + i * 4.8 + rnd.uniform(-1, 1)
        y = rnd.uniform(28, 55)
        h = rnd.uniform(6, 30)
        w = rnd.uniform(3, 7)
        box(f"bldg_{i}", (x, y, h / 2 - 22), (w, w, h), M["city"], C["outside"])
    box("ground_out", (0, 40, -22.5), (220, 70, 1), M["dark"], C["outside"])
    light("window_fill", "AREA", (0, Y1 - 0.3, 1.6), 900, (0.55, 0.65, 1.0), size=6, target=(0, 0, 1.0),
          coll=C["lighting"])

    # bed wall: slatted wood panel + upholstered headboard
    for k in range(34):
        y = -3.3 + k * 0.1
        box(f"slat_{k}", (X0 + 0.04, y, H / 2 - 0.2), (0.05, 0.06, H - 0.4), M["slats"], C["architecture"])
    hb_y0, hb_y1 = -2.1, 0.9
    for k in range(10):
        y = hb_y0 + 0.15 + k * 0.3
        soft_box(f"hb_{k}", (X0 + 0.16, y, 1.05), (0.12, 0.28, 1.3), M["headboard"], C["furniture"], bevel=0.04, sub=1)
    # bed
    by = (hb_y0 + hb_y1) / 2
    soft_box("bed_base", (X0 + 1.3, by, 0.2), (2.2, 2.1, 0.32), M["headboard"], C["furniture"], bevel=0.04, sub=1)
    soft_box("mattress", (X0 + 1.3, by, 0.48), (2.15, 2.0, 0.28), M["linen"], C["furniture"], bevel=0.08, sub=2)
    soft_box("duvet", (X0 + 1.55, by, 0.66), (1.75, 2.12, 0.12), M["linen"], C["furniture"], bevel=0.06, sub=2,
             noise=0.035)
    soft_box("throw", (X0 + 2.1, by, 0.72), (0.55, 2.16, 0.06), M["throw"], C["furniture"], bevel=0.03, sub=2, noise=0.02)
    for k, y in enumerate((by - 0.5, by + 0.5)):
        p = soft_box(f"pillow_{k}", (X0 + 0.55, y, 0.82), (0.28, 0.85, 0.5), M["linen"], C["furniture"], bevel=0.12,
                     sub=2, noise=0.02)
        p.rotation_euler[1] = math.radians(-18)
    p = soft_box("pillow_acc", (X0 + 0.8, by, 0.78), (0.18, 0.55, 0.32), M["throw"], C["furniture"], bevel=0.08, sub=2)
    p.rotation_euler[1] = math.radians(-15)
    # nightstands + lamps
    for k, y in enumerate((hb_y0 - 0.45, hb_y1 + 0.45)):
        box(f"ns_{k}", (X0 + 0.32, y, 0.27), (0.55, 0.5, 0.54), M["darkwood"], C["furniture"], bevel=0.01)
        box(f"ns_top_{k}", (X0 + 0.32, y, 0.555), (0.57, 0.52, 0.03), M["marble"], C["furniture"], bevel=0.005)
        cylinder(f"lamp_base_{k}", (X0 + 0.32, y, 0.75), 0.07, 0.36, M["brass"], C["lighting"])
        cyl = cylinder(f"lamp_shade_{k}", (X0 + 0.32, y, 1.04), 0.18, 0.26, M["shade"], C["lighting"], segments=32,
                       cap=False)
        light(f"lamp_l_{k}", "POINT", (X0 + 0.32, y, 1.02), 35, (1.0, 0.7, 0.42), size=0.12, coll=C["lighting"])
        # wall reading light glow
        light(f"wash_{k}", "SPOT", (X0 + 0.25, y, H - 0.1), 120, (1.0, 0.75, 0.5), size=0.05, target=(X0 + 0.05, y, 0.5),
              spot_deg=45, blend=0.8, coll=C["lighting"])
    # rugs
    box("rug_bed", (X0 + 1.9, by, 0.006), (3.0, 3.6, 0.012), M["rug"], C["furniture"])
    box("rug_lounge", (1.6, 2.4, 0.006), (3.2, 2.6, 0.012), M["rug"], C["furniture"])
    # bench at bed foot
    soft_box("bench", (X0 + 2.75, by, 0.42), (0.45, 1.6, 0.12), M["throw"], C["furniture"], bevel=0.03, sub=1)
    for y in (by - 0.7, by + 0.7):
        box(f"bench_leg_{y}", (X0 + 2.75, y, 0.18), (0.04, 0.04, 0.36), M["brass"], C["furniture"])
    # lounge: sofa, chairs, coffee table, plant, vase
    try:
        import_glb(os.path.join(MODELS, "GlamVelvetSofa.glb"), loc=(3.35, 2.3, 0.01), rot_z=math.radians(-90), scale=1.0,
                   coll=C["furniture"])
        import_glb(os.path.join(MODELS, "SheenChair.glb"), loc=(0.55, 1.6, 0.01), rot_z=math.radians(122), scale=1.0,
                   coll=C["furniture"])
        import_glb(os.path.join(MODELS, "SheenChair.glb"), loc=(0.6, 3.25, 0.01), rot_z=math.radians(55), scale=1.0,
                   coll=C["furniture"])
        import_glb(os.path.join(MODELS, "DiffuseTransmissionPlant.glb"), loc=(3.45, 4.5, 0.0), rot_z=0.3, scale=1.6,
                   coll=C["furniture"])
        import_glb(os.path.join(MODELS, "GlassVaseFlowers.glb"), loc=(1.75, 2.35, 0.42), rot_z=0.4, scale=1.6,
                   coll=C["furniture"])
    except Exception as e:
        print("import failed", e)
    cylinder("ct_top", (1.8, 2.4, 0.4), 0.55, 0.04, M["marble"], C["furniture"], segments=48)
    cylinder("ct_base", (1.8, 2.4, 0.19), 0.2, 0.38, M["brass"], C["furniture"], segments=32)
    # pendant over lounge
    cylinder("pend_cord", (1.8, 2.4, H - 0.45), 0.006, 0.9, M["frame"], C["lighting"])
    sphere("pend_globe", (1.8, 2.4, H - 0.95), 0.22, emission_mat("h_globe", (1.0, 0.8, 0.55), 5.0), C["lighting"], segs=32,
           rings=16)
    light("pend_l", "POINT", (1.8, 2.4, H - 0.95), 120, (1.0, 0.75, 0.48), size=0.2, coll=C["lighting"])
    # console + TV + art on right wall
    box("console", (X1 - 0.25, -2.0, 0.42), (0.45, 2.2, 0.06), M["darkwood"], C["furniture"], bevel=0.01)
    for y in (-3.0, -1.0):
        box(f"console_leg_{y}", (X1 - 0.25, y, 0.2), (0.4, 0.04, 0.4), M["brass"], C["furniture"])
    box("tv", (X1 - 0.04, -2.0, 1.45), (0.05, 1.6, 0.92), M["tv"], C["furniture"], bevel=0.005)
    # art frame above bench wall (back wall)
    box("art_back", (-1.0, Y0 + 0.03, 1.7), (1.4, 0.04, 1.0), M["frame"], C["furniture"])
    art = mat("h_art", (0.6, 0.4, 0.3), rough=0.6)
    nt = art.node_tree
    it = nt.nodes.new("ShaderNodeTexImage")
    it.image = bpy.data.images.load(os.path.join(TEX, "art", "ls2.jpg"), check_existing=True)
    nt.links.new(it.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    v = [(-0.65, 0, -0.45), (0.65, 0, -0.45), (0.65, 0, 0.45), (-0.65, 0, 0.45)]
    cv = mesh_obj("art_canvas", v, [(0, 3, 2, 1)], art, C["furniture"])
    uv = cv.data.uv_layers.new()
    for i, (a, b2) in enumerate([(0, 0), (0, 1), (1, 1), (1, 0)]):
        uv.data[i].uv = (1 - a if False else a, b2)
    cv.location = (-1.0, Y0 + 0.06, 1.7)
    # downlights
    for x, y in [(-1.2, -3.8), (1.5, -3.8), (0.5, 0.0), (2.6, -1.8)]:
        cylinder(f"dl_{x}_{y}", (x, y, H - 0.005), 0.05, 0.01, M["led"], C["lighting"])
        light(f"dls_{x}_{y}", "SPOT", (x, y, H - 0.02), 150, (1.0, 0.8, 0.6), size=0.04, target=(x, y, 0), spot_deg=60,
              blend=0.7, coll=C["lighting"])
    light("room_fill", "AREA", (0, -1, H - 0.1), 160, (1.0, 0.78, 0.55), size=4, target=(0, -1, 0), coll=C["lighting"])
    return sc, M, C


if __name__ == "__main__":
    build()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "hotel.blend"))
