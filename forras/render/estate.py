"""Procedural Hungarian baroque manor with park – event layout in front, hotel pool garden behind.
Brick+Data concept scene (all geometry generated here, CC0 textures only)."""
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

BW, BD, F1, F2, CORN = 46.0, 14.0, 5.2, 10.2, 10.6   # block width/depth, floor heights, cornice


def leaf_mat(name, col):
    m = mat(name, col, rough=0.75, noise_var=0.45, noise_scale=3.0)
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Subsurface Weight"].default_value = 0.0
    return m


def grass_mat():
    m = mat("e_grass", (0.16, 0.3, 0.08), rough=0.9)
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # mowing stripes
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"
    wave.bands_direction = "X"
    wave.inputs["Scale"].default_value = 0.07
    wave.inputs["Distortion"].default_value = 0.0
    nt.links.new(tc.outputs["Object"], wave.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.08
    nz.inputs["Detail"].default_value = 6
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mix1 = nt.nodes.new("ShaderNodeMix")
    mix1.data_type = "RGBA"
    nt.links.new(wave.outputs["Fac"], mix1.inputs["Factor"])
    mix1.inputs[6].default_value = (0.06, 0.13, 0.03, 1)
    mix1.inputs[7].default_value = (0.075, 0.155, 0.035, 1)
    mix2 = nt.nodes.new("ShaderNodeMix")
    mix2.data_type = "RGBA"
    mix2.blend_type = "MULTIPLY"
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.75
    mr.inputs["To Max"].default_value = 1.2
    nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
    mix2.inputs["Factor"].default_value = 1.0
    nt.links.new(mix1.outputs[2], mix2.inputs[6])
    nt.links.new(mr.outputs["Result"], mix2.inputs[7])
    nt.links.new(mix2.outputs[2], p.inputs["Base Color"])
    return m


def window_glass(name, lit):
    if lit:
        m = mat(name, (0.05, 0.05, 0.05), rough=0.08, emit=(1.0, 0.68, 0.36), emit_strength=lit)
    else:
        m = mat(name, (0.03, 0.04, 0.05), rough=0.06, coat=1.0)
    return m


_PROTOS = []


def tree(name, x, y, h, rnd, M, coll, kind=0):
    if not _PROTOS:
        prnd = random.Random(42)
        for k in range(5):
            _PROTOS.append(tree_proto(f"proto{k}", prnd, M["leaves"], M["bark"], M["leaf_tex"],
                                      kind=[0, 0, 1, 2, 0][k]))
    if kind == 1:
        proto, hp = _PROTOS[2]
    else:
        proto, hp = _PROTOS[rnd.choice([0, 1, 3, 4])]
    place_tree(proto, hp, name, (x, y, 0), h, rnd.uniform(0, 6.28), coll)


def build(event=True, pool=True, dusk=True):
    sc = reset(samples=64)
    sc.view_settings.exposure = 0.0 if not dusk else -0.2
    _PROTOS.clear()
    if dusk:
        world_gradient(strength=0.9)
    else:
        world_gradient(horizon=(0.75, 0.82, 0.9), mid=(0.45, 0.62, 0.85), zenith=(0.16, 0.34, 0.7), strength=1.2)
    sun = light("sun", "SUN", (-200, -120, 30 if dusk else 95), 3.2 if dusk else 4.5,
                (1.0, 0.62, 0.38) if dusk else (1.0, 0.9, 0.8), size=1.5, target=(0, 0, 0))
    leaf_tex = bpy.data.textures.new("leafnoise", "CLOUDS")
    leaf_tex.noise_scale = 0.35
    M = dict(
        facade=mat("e_facade", (0.86, 0.6, 0.22), rough=0.8, noise_var=0.18, noise_scale=1.2),
        trim=mat("e_trim", (0.92, 0.9, 0.84), rough=0.6),
        roof=mat("e_roof", (0.16, 0.07, 0.05), rough=0.7, noise_var=0.3, noise_scale=0.5),
        copper=mat("e_copper", (0.32, 0.56, 0.48), rough=0.5, metal=0.3),
        lit=window_glass("e_win_lit", 3.5 if dusk else 0),
        dark=window_glass("e_win_dark", 0),
        grass=grass_mat(),
        gravel=mat("e_gravel", (0.72, 0.66, 0.56), rough=0.95, noise_var=0.3, noise_scale=8, bump_noise=0.3),
        stone=mat("e_stone", (0.75, 0.72, 0.66), rough=0.7, noise_var=0.2, noise_scale=2),
        water=mat("e_water", (0.02, 0.18, 0.25), rough=0.03, coat=1.0, specular=0.8),
        pool=mat("e_pool", (0.1, 0.55, 0.65), rough=0.05, transmission=0.0, coat=1.0),
        bark=mat("e_bark", (0.18, 0.13, 0.09), rough=0.9),
        hedge=leaf_mat("e_hedge", (0.08, 0.2, 0.06)),
        leaves=[leaf_mat("e_leaf1", (0.045, 0.11, 0.03)), leaf_mat("e_leaf2", (0.07, 0.15, 0.035)),
                leaf_mat("e_leaf3", (0.11, 0.17, 0.04)), leaf_mat("e_leaf4", (0.05, 0.09, 0.035))],
        leaf_tex=leaf_tex,
        tent=mat("e_tent", (0.93, 0.93, 0.92), rough=0.6, transmission=0.15),
        cloth=mat("e_cloth", (0.95, 0.95, 0.94), rough=0.8),
        chair=mat("e_chair", (0.82, 0.68, 0.45), rough=0.5),
        truss=mat("e_truss", (0.75, 0.75, 0.77), rough=0.3, metal=1.0),
        black=mat("e_black", (0.02, 0.02, 0.02), rough=0.6),
        deck=mat("e_deck", (0.35, 0.22, 0.14), rough=0.6, tex="wood_col.jpg", tex_scale=0.5, tex_tint=(1.6, 1.3, 1.0)),
        container=mat("e_container", (0.78, 0.8, 0.82), rough=0.5, metal=0.2),
        bulb=emission_mat("e_bulb", (1.0, 0.75, 0.45), 40.0 if dusk else 0.0),
        led=gradient_emission_mat("e_led", (0.95, 0.35, 0.15), (0.2, 0.15, 0.6), 1.5, 8.0, 4.0 if dusk else 1.0),
        lounger=mat("e_lounger", (0.95, 0.94, 0.9), rough=0.6),
        umbrella=mat("e_umbrella", (0.92, 0.88, 0.8), rough=0.7),
    )
    C = {k: collection(k) for k in ("terrain", "building", "park", "event", "pool", "lighting")}

    # terrain + paths
    box("ground", (0, -20, -0.25), (600, 600, 0.5), M["grass"], C["terrain"])
    box("forecourt", (0, -14.5, 0.01), (60, 9, 0.04), M["gravel"], C["terrain"])
    box("avenue", (0, -190, 0.01), (10, 180, 0.04), M["gravel"], C["terrain"])
    box("event_path", (0, -26, 0.012), (8, 12, 0.04), M["gravel"], C["terrain"])
    box("cross_path", (0, -21, 0.012), (120, 4, 0.04), M["gravel"], C["terrain"])
    box("rear_terrace", (0, 11.5, 0.01), (50, 9, 0.04), M["stone"], C["terrain"])

    # ---------------- manor
    by0 = -BD / 2
    box("block", (0, 0, CORN / 2), (BW, BD, CORN), M["facade"], C["building"])
    box("risalit", (0, by0 - 1.0, (CORN + 1.2) / 2), (15, 2.0, CORN + 1.2), M["facade"], C["building"])
    for sx in (-1, 1):
        box(f"pavilion_{sx}", (sx * (BW / 2 - 4), by0 - 0.6, CORN / 2), (8, 1.2, CORN), M["facade"], C["building"])
    # plinth, string course, cornice
    box("plinth", (0, -0.05, 0.4), (BW + 0.4, BD + 0.4, 0.8), M["stone"], C["building"])
    box("plinth_ris", (0, by0 - 1.05, 0.4), (15.4, 2.3, 0.8), M["stone"], C["building"])
    for z, hgt, ext in ((F1, 0.35, 0.18), (CORN - 0.2, 0.6, 0.45)):
        box(f"band_{z}", (0, 0, z), (BW + ext * 2, BD + ext * 2, hgt), M["trim"], C["building"], bevel=0.05)
        box(f"band_ris_{z}", (0, by0 - 1.0, z + (0.6 if z > 6 else 0)), (15 + ext * 2, 2.0 + ext * 2, hgt), M["trim"],
            C["building"], bevel=0.05)
    # pilasters on risalit
    for x in (-6.6, -2.2, 2.2, 6.6):
        box(f"pil_{x}", (x, by0 - 2.08, CORN / 2 + 0.3), (0.9, 0.25, CORN + 0.2), M["trim"], C["building"], bevel=0.03)
    # pediment
    ped_z = CORN + 1.2
    v = [(-7.8, by0 - 2.2, ped_z), (7.8, by0 - 2.2, ped_z), (0, by0 - 2.2, ped_z + 3.0),
         (-7.8, by0 - 0.2, ped_z), (7.8, by0 - 0.2, ped_z), (0, by0 - 0.2, ped_z + 3.0)]
    mesh_obj("pediment", v, [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], M["trim"], C["building"])
    # windows
    def windows(y_face, xs, zs, w, h, normal_sign, rnd, coll):
        for x in xs:
            for zi, z in enumerate(zs):
                lit = rnd.random() < 0.6
                g = box(f"win_{x:.1f}_{z}_{y_face:.1f}", (x, y_face + normal_sign * 0.02, z + h / 2), (w, 0.1, h),
                        M["lit"] if lit else M["dark"], coll)
                # surround
                box(f"wsur_t_{x:.1f}_{z}_{y_face:.1f}", (x, y_face + normal_sign * 0.12, z + h + 0.2), (w + 0.5, 0.2, 0.3),
                    M["trim"], coll, bevel=0.03)
                box(f"wsur_b_{x:.1f}_{z}_{y_face:.1f}", (x, y_face + normal_sign * 0.12, z - 0.1), (w + 0.4, 0.22, 0.18),
                    M["trim"], coll, bevel=0.03)
                for sx in (-1, 1):
                    box(f"wsur_s_{x:.1f}_{z}_{sx}_{y_face:.1f}", (x + sx * (w / 2 + 0.1), y_face + normal_sign * 0.08,
                                                                  z + h / 2), (0.2, 0.14, h), M["trim"], coll)
    rnd = random.Random(11)
    xs_main = [x for x in [-20.4, -17.2, -14.0, -10.8, 10.8, 14.0, 17.2, 20.4]]
    xs_ris = [-4.4, 0.0, 4.4]
    windows(by0 - 0.0, xs_main, [1.3, 6.1], 1.4, 2.8, -1, rnd, C["building"])
    windows(by0 - 2.0, xs_ris, [1.3, 6.1], 1.5, 3.0, -1, rnd, C["building"])
    windows(BD / 2, xs_main + xs_ris, [1.3, 6.1], 1.4, 2.8, 1, rnd, C["building"])
    # entrance door
    box("door", (0, by0 - 2.05, 1.9), (2.0, 0.12, 3.6), mat("e_door", (0.18, 0.1, 0.05), rough=0.4), C["building"])
    # roof (hip) – mansard-like
    def hip(name, cx, cy, w, d, z0, hgt, inset, material):
        v = [(cx - w / 2, cy - d / 2, z0), (cx + w / 2, cy - d / 2, z0), (cx + w / 2, cy + d / 2, z0), (cx - w / 2, cy + d / 2, z0),
             (cx - w / 2 + inset, cy, z0 + hgt), (cx + w / 2 - inset, cy, z0 + hgt)]
        f = [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]
        return mesh_obj(name, v, f, material, C["building"])
    hip("roof_main", 0, 0, BW + 0.8, BD + 0.8, CORN + 0.1, 5.5, 6.0, M["roof"])
    hip("roof_ris", 0, by0 - 1.0, 15.4, 2.6, CORN + 1.2, 1.2, 0.5, M["roof"])
    # cupola
    cylinder("cupola_base", (0, 0, CORN + 6.2), 2.2, 1.8, M["trim"], C["building"], segments=8)
    cylinder("cupola_drum", (0, 0, CORN + 7.6), 1.8, 1.2, M["facade"], C["building"], segments=8)
    cu = sphere("cupola_dome", (0, 0, CORN + 8.2), 2.0, M["copper"], C["building"], segs=8, rings=8)
    cu.scale = (1, 1, 1.1)
    cylinder("lantern", (0, 0, CORN + 10.6), 0.35, 1.4, M["copper"], C["building"], segments=8)
    # chimneys + dormers
    for x in (-15, -5, 5, 15):
        box(f"chimney_{x}", (x, 2.0, CORN + 5.0), (0.8, 0.8, 2.6), M["facade"], C["building"])
    for x in (-18, -12, 12, 18):
        box(f"dormer_{x}", (x, -4.2, CORN + 1.8), (1.4, 1.6, 1.6), M["trim"], C["building"])
        box(f"dormer_win_{x}", (x, -5.02, CORN + 1.8), (0.8, 0.05, 1.0), M["lit"], C["building"])

    # fountain in forecourt
    cylinder("fountain_rim", (0, -124, 0.35), 5.5, 0.7, M["stone"], C["park"], segments=64)
    cylinder("fountain_water", (0, -124, 0.62), 5.1, 0.1, M["water"], C["park"], segments=64)
    cylinder("fountain_col", (0, -124, 1.4), 0.5, 2.0, M["stone"], C["park"], segments=24)
    # parterre hedges
    for sx in (-1, 1):
        for k in range(3):
            x = sx * (12 + k * 8)
            box(f"parterre_{sx}_{k}", (x, -15, 0.35), (6, 0.7, 0.7), M["hedge"], C["park"], bevel=0.15)
    # trees: avenue + park clumps
    rnd = random.Random(5)
    for k in range(14):
        y = -45 - k * 12
        if y > -112:
            continue
        for sx in (-1, 1):
            tree(f"ave_{k}_{sx}", sx * 9.0, y, rnd.uniform(11, 14), rnd, M, C["park"])
    for k in range(70):
        ang = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(70, 150)
        x = r * math.cos(ang)
        y = r * math.sin(ang) * 0.9 - 10
        if abs(x) < 52 and -115 < y < 0:
            continue
        tree(f"park_{k}", x, y, rnd.uniform(10, 18), rnd, M, C["park"], kind=1 if rnd.random() < 0.2 else 0)
    for k in range(260):  # forest belt on the horizon
        ang = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(160, 260)
        tree(f"forest_{k}", r * math.cos(ang), r * math.sin(ang) - 20, rnd.uniform(14, 22), rnd, M, C["park"],
             kind=1 if rnd.random() < 0.25 else 0)
    for k in range(18):  # side groves framing the lawn
        x = rnd.choice((-1, 1)) * rnd.uniform(50, 66)
        y = rnd.uniform(-105, -20)
        tree(f"grove_{k}", x, y, rnd.uniform(11, 16), rnd, M, C["park"])

    # ---------------- event layout (front lawn)
    if event:
        # stage on the west side of the lawn, facing east (+x) towards the tables
        sx0, sy0 = -44.0, -62.0
        box("stage_deck", (sx0, sy0, 0.6), (9, 16, 1.2), M["black"], C["event"])
        for dx in (-4.2, 4.2):
            for dy in (-7.8, 7.8):
                cylinder(f"tower_{dx}_{dy}", (sx0 + dx, sy0 + dy, 4.8), 0.2, 8.4, M["truss"], C["event"], segments=10)
        for dx in (-4.2, 4.2):
            cylinder(f"truss_y_{dx}", (sx0 + dx, sy0, 9.0), 0.2, 15.8, M["truss"], C["event"], axis="Y", segments=10)
        for dy in (-7.8, 7.8):
            cylinder(f"truss_x_{dy}", (sx0, sy0 + dy, 9.0), 0.2, 8.4, M["truss"], C["event"], axis="X", segments=10)
        box("stage_roof", (sx0, sy0, 9.5), (9.5, 16.5, 0.15), M["black"], C["event"])
        box("led_wall", (sx0 - 4.0, sy0, 4.8), (0.2, 12, 6.5), M["led"], C["event"])
        for dy in (-1, 1):
            box(f"array_{dy}", (sx0 + 3.5, sy0 + dy * 9.6, 6.0), (0.8, 0.8, 3.2), M["black"], C["event"])
        box("dance_floor", (sx0 + 13, sy0, 0.03), (12, 14, 0.06), M["deck"], C["event"])
        # pagoda tents
        def pagoda(name, x, y, s=6.0):
            h0 = 2.6
            for dx in (-1, 1):
                for dy in (-1, 1):
                    cylinder(f"{name}_p{dx}{dy}", (x + dx * s / 2, y + dy * s / 2, h0 / 2), 0.05, h0, M["truss"], C["event"],
                             segments=8)
            v = [(x - s / 2, y - s / 2, h0), (x + s / 2, y - s / 2, h0), (x + s / 2, y + s / 2, h0), (x - s / 2, y + s / 2, h0),
                 (x, y, h0 + 3.4)]
            ob = mesh_obj(name, v, [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)], M["tent"], C["event"])
            sub = ob.modifiers.new("s", "SUBSURF")
            sub.levels = 2
            sub.render_levels = 2
            sub.subdivision_type = "SIMPLE"
            sm = ob.modifiers.new("sm", "SMOOTH")
            sm.factor = 0.6
            sm.iterations = 3
            box(f"{name}_valance", (x, y, h0 - 0.15), (s, s, 0.3), M["tent"], C["event"])
            light(f"{name}_l", "POINT", (x, y, h0 - 0.4), 300, (1.0, 0.75, 0.45), size=0.6, coll=C["lighting"])
        for k in range(5):
            pagoda(f"tent_N{k}", -14 + k * 7, -36)
            pagoda(f"tent_S{k}", -14 + k * 7, -88)
        # round tables with chairs
        tbl = cylinder("tbl_src", (0, 0, -50), 0.9, 0.76, M["cloth"], C["event"], segments=32)
        chair = box("ch_src", (0, 0, -50), (0.42, 0.42, 0.9), M["chair"], C["event"], bevel=0.03)
        for i in range(5):
            for j in range(5):
                x = -16 + i * 7
                y = -48 - j * 7
                instance(tbl, f"tbl_{i}_{j}", (x, y, 0.38), 0, C["event"])
                for c in range(8):
                    a = c * 2 * math.pi / 8
                    instance(chair, f"ch_{i}_{j}_{c}", (x + 1.25 * math.cos(a), y + 1.25 * math.sin(a), 0.45), a, C["event"])
        # festoon light strings over the tables (catenaries)
        xa, xb, ya, yb = -20.0, 16.0, -44.0, -80.0
        poles = [(xa, ya), (xb, ya), (xa, yb), (xb, yb), ((xa + xb) / 2, ya), ((xa + xb) / 2, yb)]
        for (x, y) in poles:
            cylinder(f"pole_{x}_{y}", (x, y, 2.75), 0.06, 5.5, M["black"], C["event"], segments=8)
        strings = [((xa, ya), (xb, yb)), ((xb, ya), (xa, yb)), ((xa, ya), (xa, yb)), ((xb, ya), (xb, yb)),
                   (((xa + xb) / 2, ya), ((xa + xb) / 2, yb)), ((xa, ya), (xb, ya)), ((xa, yb), (xb, yb))]
        bulb_src = sphere("bulb_src", (0, 0, -50), 0.09, M["bulb"], C["lighting"], segs=8, rings=5)
        for si, (a, b) in enumerate(strings):
            ax, ay = a
            bx_, by_ = b
            dist = math.hypot(bx_ - ax, by_ - ay)
            n = int(dist / 1.2)
            for k in range(n + 1):
                t = k / n
                x = ax + (bx_ - ax) * t
                y = ay + (by_ - ay) * t
                z = 5.4 - 1.6 * 4 * t * (1 - t)
                instance(bulb_src, f"bulb_{si}_{k}", (x, y, z), 0, C["lighting"])
        if dusk:
            light("festoon_fill", "AREA", (-2, -62, 6), 2500, (1.0, 0.72, 0.42), size=30, target=(-2, -62, 0),
                  coll=C["lighting"])
            for dy in (-1, 1):
                light(f"stage_spot_{dy}", "SPOT", (sx0 + 3.8, sy0 + dy * 6, 8.8), 3000,
                      (0.6, 0.4, 1.0) if dy < 0 else (1.0, 0.5, 0.3), size=0.2, target=(sx0, sy0, 1.2), spot_deg=40,
                      coll=C["lighting"])
        # toilets + catering stands
        for k in range(3):
            box(f"wc_{k}", (44, -84 - k * 3.2, 1.3), (2.6, 2.8, 2.6), M["container"], C["event"], bevel=0.03)
        for k in range(3):
            box(f"stand_{k}", (36, -44 - k * 9, 1.4), (5.0, 3.0, 2.8), M["cloth"], C["event"], bevel=0.03)
            box(f"awning_{k}", (34.2, -44 - k * 9, 2.9), (1.4, 3.2, 0.12), mat("e_awning", (0.75, 0.2, 0.15), rough=0.6),
                C["event"])
        box("bar", (24, -62, 0.55), (1.0, 8, 1.1), M["black"], C["event"], bevel=0.02)

    # ---------------- hotel pool garden (behind)
    if pool:
        box("pool_deck", (0, 32, 0.02), (36, 20, 0.06), M["stone"], C["pool"])
        box("pool_water", (0, 32, 0.04), (26, 10, 0.05), M["pool"], C["pool"])
        box("pool_edge", (0, 32, 0.03), (27, 11, 0.04), M["trim"], C["pool"])
        for k in range(8):
            x = -12 + k * 3.4
            for sy in (-1, 1):
                b = box(f"lounger_{k}_{sy}", (x, 32 + sy * 7.6, 0.3), (0.75, 2.0, 0.12), M["lounger"], C["pool"], bevel=0.04)
                bk = box(f"lounger_bk_{k}_{sy}", (x, 32 + sy * 8.4, 0.55), (0.75, 0.7, 0.1), M["lounger"], C["pool"],
                         bevel=0.04)
                bk.rotation_euler[0] = math.radians(-50 * sy)
            if k % 2 == 0:
                for sy in (-1, 1):
                    cylinder(f"umb_pole_{k}_{sy}", (x + 1.7, 32 + sy * 8.2, 1.25), 0.03, 2.5, M["truss"], C["pool"])
                    cone = bpy.data.meshes.new("umb")
                    import bmesh as _bm
                    bm = _bm.new()
                    _bm.ops.create_cone(bm, cap_ends=False, segments=16, radius1=1.5, radius2=0.05, depth=0.6)
                    bm.to_mesh(cone)
                    bm.free()
                    ob = bpy.data.objects.new(f"umb_{k}_{sy}", cone)
                    ob.data.materials.append(M["umbrella"])
                    C["pool"].objects.link(ob)
                    ob.location = (x + 1.7, 32 + sy * 8.2, 2.5)
        for k in range(10):
            tree(f"pool_tree_{k}", -22 + k * 4.9, 46, rnd.uniform(6, 8), rnd, M, C["park"], kind=1)
        if dusk:
            light("pool_glow", "AREA", (0, 32, -0.2), 1200, (0.3, 0.8, 1.0), size=10, target=(0, 32, 5), coll=C["lighting"])
    return sc, M, C


if __name__ == "__main__":
    build()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "estate.blend"))
