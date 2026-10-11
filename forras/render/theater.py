"""Procedural horseshoe opera house – Brick+Data concept scene (all geometry generated here)."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from mathutils import Vector

R = 10.5          # horseshoe inner radius (balcony fronts)
YS = -0.5         # straight part starts here (near proscenium)
YC = -13.5        # arc centre
DEPTH = 3.6       # box depth
TIERS = [4.2, 7.6, 11.0]
CEIL = 14.6
STAGE_Z = 1.0
OPEN_W, OPEN_TOP = 13.0, 9.6


def rake(y):
    return max(0.0, (-4.6 - y)) * 0.075


def damask(name, base, dark):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = mat(name, base, rough=0.75, sheen=0.4)
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 9.0
    vor.feature = "SMOOTH_F1"
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 0.15
    mr.inputs["From Max"].default_value = 0.35
    nt.links.new(vor.outputs["Distance"], mr.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    nt.links.new(mr.outputs["Result"], mix.inputs["Factor"])
    mix.inputs[6].default_value = (*dark, 1)
    mix.inputs[7].default_value = (*base, 1)
    nt.links.new(mix.outputs[2], p.inputs["Base Color"])
    return m


def fresco(name):
    m = mat(name, (0.5, 0.6, 0.7), rough=0.8)
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.35
    nz.inputs["Detail"].default_value = 6
    nz.inputs["Roughness"].default_value = 0.6
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position = 0.35
    cr.elements[0].color = (0.30, 0.42, 0.55, 1)
    cr.elements[1].position = 0.7
    cr.elements[1].color = (0.95, 0.86, 0.72, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
    return m


def build(with_ceiling=True, house_level=0.35):
    sc = reset(samples=96)
    sc.view_settings.exposure = -0.3
    try:
        sc.view_settings.look = "AgX - Punchy"
    except Exception:
        pass
    world_color((0.004, 0.004, 0.006), 1.0)

    # --- materials
    M = dict(
        cream=mat("cream", (0.78, 0.68, 0.52), rough=0.55, noise_var=0.25, noise_scale=3),
        gold=mat("gold", (0.85, 0.62, 0.28), rough=0.28, metal=1.0),
        velvet=mat("velvet", (0.42, 0.03, 0.04), rough=0.85, sheen=1.0, sheen_tint=(1.0, 0.45, 0.45),
                   tex="fabric_col.jpg", tex_scale=6, tex_tint=(0.95, 0.35, 0.35), normal="fabric_nor.jpg"),
        curtain=mat("curtain", (0.36, 0.02, 0.03), rough=0.9, sheen=1.0, sheen_tint=(1, 0.5, 0.5)),
        carpet=mat("carpet", (0.28, 0.03, 0.04), rough=0.95, noise_var=0.3, noise_scale=40),
        wall=damask("damask", (0.40, 0.05, 0.06), (0.26, 0.02, 0.03)),
        stagefloor=mat("stagefloor", (0.2, 0.2, 0.2), rough=0.55, tex="woodfloor_col.jpg", tex_scale=0.35,
                       tex_tint=(0.55, 0.5, 0.45), normal="woodfloor_nor.jpg"),
        black=mat("black", (0.012, 0.012, 0.012), rough=0.95, sheen=0.4),
        metal=mat("metal", (0.08, 0.08, 0.09), rough=0.4, metal=1.0),
        darkwood=mat("darkwood", (0.2, 0.1, 0.05), rough=0.4, tex="wood_col.jpg", tex_scale=2.0, coat=0.3),
        stone=mat("setstone", (0.72, 0.68, 0.62), rough=0.7, noise_var=0.35, noise_scale=2.5, bump_noise=0.15),
        fresco=fresco("fresco"),
        bulb=emission_mat("bulb", (1.0, 0.72, 0.42), 45 * house_level),
        glass=mat("crystal", (1, 1, 1), rough=0.02, transmission=1.0, ior=1.5),
        cyc=gradient_emission_mat("cyc", (1.0, 0.36, 0.12), (0.04, 0.07, 0.30), 1.0, 9.0, 2.2),
        lamp=emission_mat("lamp", (1.0, 0.85, 0.65), 12),
    )
    C = {k: collection(k) for k in ("architecture", "stage", "seating", "set", "lighting", "ceiling", "curtains")}

    # --- proscenium wall + frame
    W = R + DEPTH
    box("prosc_L", (-(W + OPEN_W / 2) / 2, 0, CEIL / 2), (W - OPEN_W / 2, 0.8, CEIL), M["cream"], C["architecture"])
    box("prosc_R", ((W + OPEN_W / 2) / 2, 0, CEIL / 2), (W - OPEN_W / 2, 0.8, CEIL), M["cream"], C["architecture"])
    box("prosc_T", (0, 0, (OPEN_TOP + CEIL) / 2), (OPEN_W, 0.8, CEIL - OPEN_TOP), M["cream"], C["architecture"])
    for k, (w, d) in enumerate([(0.55, 0.12), (0.32, 0.22)]):
        y = -0.4 - d / 2
        box(f"frame_L{k}", (-OPEN_W / 2 - w / 2 + 0.05, y, (STAGE_Z + OPEN_TOP) / 2), (w, d, OPEN_TOP - STAGE_Z + w),
            M["gold"], C["architecture"], bevel=0.03)
        box(f"frame_R{k}", (OPEN_W / 2 + w / 2 - 0.05, y, (STAGE_Z + OPEN_TOP) / 2), (w, d, OPEN_TOP - STAGE_Z + w),
            M["gold"], C["architecture"], bevel=0.03)
        box(f"frame_T{k}", (0, y, OPEN_TOP + w / 2 - 0.05), (OPEN_W + 2 * w, d, w), M["gold"], C["architecture"],
            bevel=0.03)
    # cartouche
    car = cylinder("cartouche", (0, -0.62, OPEN_TOP + 1.55), 1.25, 0.15, M["gold"], C["architecture"], segments=48,
                   axis="Y")
    car.scale = (1.0, 0.65, 1.0)
    cylinder("cartouche_in", (0, -0.72, OPEN_TOP + 1.55), 0.9, 0.12, M["velvet"], C["architecture"], segments=48,
             axis="Y").scale = (1.0, 0.6, 1.0)
    # damask panels + gold bands on proscenium wall
    for sx in (-1, 1):
        x0, x1 = OPEN_W / 2 + 0.75, R + DEPTH - 0.4
        box(f"prosc_panel_{sx}", (sx * (x0 + x1) / 2, -0.43, CEIL / 2), (x1 - x0, 0.06, CEIL - 2.0), M["wall"],
            C["architecture"])
        for z in TIERS + [1.2]:
            box(f"prosc_band_{sx}_{z}", (sx * (x0 + x1) / 2, -0.5, z), (x1 - x0, 0.1, 0.16), M["gold"],
                C["architecture"], bevel=0.02)
    box("frieze", (0, -0.45, OPEN_TOP + 1.55), (OPEN_W + 1.2, 0.06, 1.9), M["wall"], C["architecture"])
    for z in (OPEN_TOP + 0.55, OPEN_TOP + 2.55):
        box(f"frieze_band_{z}", (0, -0.52, z), (OPEN_W + 1.4, 0.12, 0.16), M["gold"], C["architecture"], bevel=0.02)
    # pilasters on the proscenium splay
    for sx in (-1, 1):
        for x in (OPEN_W / 2 + 1.6, OPEN_W / 2 + 4.6):
            box(f"pil_{sx}_{x}", (sx * x, -0.48, CEIL / 2), (0.7, 0.18, CEIL), M["cream"], C["architecture"], bevel=0.04)
            box(f"pilcap_{sx}_{x}", (sx * x, -0.6, CEIL - 0.6), (0.95, 0.3, 0.35), M["gold"], C["architecture"],
                bevel=0.04)
            box(f"pilbase_{sx}_{x}", (sx * x, -0.6, 0.5), (0.9, 0.3, 1.0), M["gold"], C["architecture"], bevel=0.04)

    # --- stage house
    box("stage_floor", (0, 7.0, STAGE_Z - 0.5), (20, 15.0, 1.0), M["stagefloor"], C["stage"])
    box("apron", (0, -1.6, STAGE_Z - 0.5), (OPEN_W + 1.0, 2.4, 1.0), M["stagefloor"], C["stage"])
    box("apron_face", (0, -2.85, STAGE_Z / 2), (OPEN_W + 1.0, 0.1, STAGE_Z), M["black"], C["stage"])
    box("stage_wall_L", (-10.2, 7, 10), (0.4, 15, 20), M["black"], C["stage"])
    box("stage_wall_R", (10.2, 7, 10), (0.4, 15, 20), M["black"], C["stage"])
    box("stage_back", (0, 14.6, 10), (21, 0.4, 20), M["black"], C["stage"])
    box("stage_roof", (0, 7, 20), (21, 15, 0.4), M["black"], C["stage"])
    # orchestra pit
    box("pit_floor", (0, -4.0, -1.0), (OPEN_W + 1.0, 2.4, 0.2), M["black"], C["stage"])
    box("pit_wall", (0, -5.25, 0.0), (OPEN_W + 3.0, 0.25, 2.1), M["darkwood"], C["stage"])
    cylinder("pit_rail", (0, -5.25, 1.1), 0.045, OPEN_W + 3.0, M["gold"], C["stage"], axis="X")

    # cyclorama (curved) + set
    def cyc_fn(u, v):
        x = -8.5 + 17 * u
        return (x, 13.2 - 0.02 * x * x, STAGE_Z + v * 10.5)
    grid_surface("cyclorama", 40, 4, cyc_fn, M["cyc"], C["set"])
    # staircase
    for i in range(6):
        box(f"step{i}", (0, 5.2 + i * 0.42, STAGE_Z + 0.09 + i * 0.18), (7.5 - i * 0.25, 0.42, 0.18 + i * 0.36 * 0 + 0.18),
            M["stone"], C["set"], bevel=0.01)
    box("platform", (0, 8.6, STAGE_Z + 0.55), (9.0, 2.6, 1.1), M["stone"], C["set"], bevel=0.02)
    for sx in (-1, 1):
        for x in (3.0, 4.6):
            cylinder(f"col_{sx}_{x}", (sx * x, 8.0, STAGE_Z + 1.1 + 2.6), 0.32, 5.2, M["stone"], C["set"], segments=20)
            box(f"colcap_{sx}_{x}", (sx * x, 8.0, STAGE_Z + 1.1 + 5.35), (0.9, 0.9, 0.3), M["stone"], C["set"], bevel=0.02)
            box(f"colbase_{sx}_{x}", (sx * x, 8.0, STAGE_Z + 1.25), (0.85, 0.85, 0.3), M["stone"], C["set"], bevel=0.02)
    box("entablature", (0, 8.0, STAGE_Z + 1.1 + 5.85), (11.0, 1.0, 0.7), M["stone"], C["set"], bevel=0.03)
    # arch flat behind
    arch_pts = []
    for i in range(25):
        a = math.pi * i / 24
        arch_pts.append((2.6 * math.cos(a), 9.9, STAGE_Z + 1.1 + 4.0 + 2.6 * math.sin(a)))
    # side flats
    for sx in (-1, 1):
        box(f"flat_{sx}", (sx * 4.6, 10.0, STAGE_Z + 1.1 + 3.2), (2.8, 0.15, 6.4), M["stone"], C["set"])
    # legs & borders (masking)
    for y in (2.2, 5.6, 9.2):
        for sx in (-1, 1):
            box(f"leg_{y}_{sx}", (sx * 7.6, y, STAGE_Z + 5.0), (1.8, 0.08, 10.0), M["black"], C["stage"])
        box(f"border_{y}", (0, y, 10.8), (17, 0.08, 1.8), M["black"], C["stage"])
        # light bar
        cylinder(f"bar_{y}", (0, y - 0.35, 9.7), 0.03, 15, M["metal"], C["lighting"], axis="X")
        for k in range(-6, 7, 2):
            cylinder(f"fix_{y}_{k}", (k * 1.0, y - 0.35, 9.45), 0.13, 0.42, M["metal"], C["lighting"], segments=12)
    # fly bars further up
    for k in range(12):
        cylinder(f"fly_{k}", (0, 1.0 + k * 1.1, 15.5 + (k % 3) * 0.6), 0.025, 16, M["metal"], C["stage"], axis="X")

    # --- house curtain (gathered side panels + valance)
    def curtain_panel(name, x0, x1, z0, z1, folds, depth=0.13, y0=0.55, droop=0.0):
        def fn(u, v):
            x = x0 + (x1 - x0) * u
            y = y0 + depth * math.sin(u * folds * 2 * math.pi) * (0.6 + 0.4 * v)
            z = z0 + (z1 - z0) * v - droop * math.sin(math.pi * u) * (1 - v)
            return (x, y, z)
        ob = grid_surface(name, folds * 8, 12, fn, M["curtain"], C["curtains"])
        s = ob.modifiers.new("s", "SOLIDIFY")
        s.thickness = 0.03
        return ob
    curtain_panel("curtain_L", -OPEN_W / 2, -OPEN_W / 2 + 1.7, STAGE_Z, OPEN_TOP, 7)
    curtain_panel("curtain_R", OPEN_W / 2 - 1.7, OPEN_W / 2, STAGE_Z, OPEN_TOP, 7)
    for k, (z0, dr) in enumerate([(OPEN_TOP - 1.6, 0.7), (OPEN_TOP - 1.0, 0.45)]):
        for seg in range(3):
            x0 = -OPEN_W / 2 + seg * OPEN_W / 3
            curtain_panel(f"valance_{k}_{seg}", x0, x0 + OPEN_W / 3, z0, OPEN_TOP + 0.05, 5, depth=0.08,
                          y0=0.25 - k * 0.12, droop=dr)

    # --- stalls floor (raked) and side/back walls
    def floor_fn(u, v):
        x = -(R + DEPTH) + 2 * (R + DEPTH) * u
        y = -5.4 - (YC - R - DEPTH + 5.4) * -v
        y = -5.4 + (YC - R - DEPTH - 5.4) * v
        return (x, y, rake(y))
    fp = horseshoe(R, YS, YC, n_arc=64, n_straight=8, offset=DEPTH)
    ribbon("stalls_floor", [(x, y, rake(y)) for x, y in fp], [(0.0, y, rake(y)) for x, y in fp], M["carpet"],
           C["architecture"])
    box("pit_side_floor", (0, -1.6, -0.02), (2 * (R + DEPTH), 2.4, 0.04), M["carpet"], C["architecture"])
    box("front_floor", (0, -4.3, 0.0), (2 * (R + DEPTH), 2.4, 0.04), M["carpet"], C["architecture"])

    outer = horseshoe(R, YS, YC, offset=DEPTH)
    sweep("outer_wall", [(0, 0), (-0.3, 0), (-0.3, CEIL), (0, CEIL)], [(x, y, 0) for x, y in outer],
          M["wall"], C["architecture"], smooth=True)

    # --- tiers
    path0 = horseshoe(R, YS, YC, n_arc=64, n_straight=8)
    pathD = horseshoe(R, YS, YC, n_arc=64, n_straight=8, offset=DEPTH)
    seg_len = []
    for z in TIERS:
        ribbon(f"tier_{z}", [(x, y, z) for x, y in path0], [(x, y, z) for x, y in pathD], M["carpet"],
               C["architecture"], thickness=0.3)
        # soffit band + parapet
        sweep(f"fascia_{z}", [(0.0, -0.75), (0.06, -0.7), (0.06, -0.05), (0.0, 0.0)],
              [(x, y, z) for x, y in path0], M["cream"], C["architecture"])
        sweep(f"fascia_gold_{z}", [(0.06, -0.78), (0.11, -0.74), (0.11, -0.66), (0.06, -0.62)],
              [(x, y, z) for x, y in path0], M["gold"], C["architecture"])
        sweep(f"parapet_{z}", [(0.0, 0.0), (0.12, 0.08), (0.2, 0.45), (0.16, 0.8), (0.06, 0.92), (-0.12, 0.92),
                               (-0.12, 0.0)], [(x, y, z) for x, y in path0], M["cream"], C["architecture"])
        sweep(f"parapet_band_{z}", [(0.18, 0.36), (0.235, 0.42), (0.235, 0.5), (0.18, 0.56)],
              [(x, y, z) for x, y in path0], M["gold"], C["architecture"])
        sweep(f"parapet_cushion_{z}", [(0.1, 0.9), (0.12, 1.0), (0.0, 1.06), (-0.14, 1.0), (-0.14, 0.9)],
              [(x, y, z) for x, y in path0], M["velvet"], C["architecture"])
    # box partitions + sconces + seats in tiers
    seat = make_seat(M, C["seating"])
    stool = seat
    for ti, z in enumerate(TIERS):
        s_acc = 0.0
        next_part = 1.3
        next_seat = 0.35
        rows = [0.85, 1.75] if ti < 2 else [0.8, 1.6, 2.4]
        for i in range(len(path0) - 1):
            a = Vector((*path0[i], 0))
            b = Vector((*path0[i + 1], 0))
            seg = (b - a).length
            t = (b - a).normalized()
            inward = Vector((-t.y, t.x, 0))
            while next_seat < s_acc + seg:
                p = a + t * (next_seat - s_acc)
                for ri, off in enumerate(rows):
                    q = p - inward * off
                    if q.y > -0.9:
                        continue
                    zz = z + (0.32 * ri if ti == 2 else 0)
                    rot = math.atan2(-inward.x, inward.y)
                    instance(seat, f"tseat_{ti}_{next_seat:.1f}_{ri}", (q.x, q.y, zz), rot, C["seating"])
                next_seat += 0.62
            while ti < 2 and next_part < s_acc + seg:
                p = a + t * (next_part - s_acc)
                rot = math.atan2(-inward.x, inward.y)
                q = p - inward * (DEPTH / 2 + 0.05)
                royal = abs(q.x) < 2.2 and q.y < YC - R + 2
                if q.y < -0.6 and not royal:
                    box(f"part_{ti}_{next_part:.1f}", (q.x, q.y, z + 1.3), (0.08, DEPTH - 0.1, 2.6), M["wall"],
                        C["architecture"], rot_z=rot)
                    if int(next_part / 2.6) % 2 == 0:
                        lp = p - inward * 0.05
                        sphere(f"sconce_{ti}_{next_part:.1f}", (lp.x, lp.y, z + 1.32), 0.055, M["lamp"], C["lighting"])
                        cylinder(f"sconce_arm_{ti}_{next_part:.1f}", (lp.x, lp.y, z + 1.12), 0.012, 0.3, M["gold"],
                                 C["lighting"])
                next_part += 2.6
            s_acc += seg
        # step risers in gallery
        if ti == 2:
            for ri, (o0, o1) in enumerate([(1.2, DEPTH), (2.0, DEPTH)]):
                pa = horseshoe(R, YS, YC, n_arc=64, n_straight=8, offset=o0)
                ribbon(f"gal_step_{ri}", [(x, y, z + 0.32 * (ri + 1)) for x, y in pa],
                       [(x, y, z + 0.32 * (ri + 1)) for x, y in pathD], M["carpet"], C["architecture"], thickness=0.32)

    # --- stalls seating (curved rows facing stage)
    cen = Vector((0, 3.5, 0))
    for k in range(17):
        r = 9.6 + k * 0.95
        n = int(math.pi * r / 0.56)
        for j in range(n + 1):
            th = -math.pi / 2 + math.pi * j / n
            x = r * math.sin(th)
            y = cen.y - r * math.cos(th)
            if y > -6.2:
                continue
            if 2.9 < abs(x) < 4.0:
                continue
            # inside horseshoe interior (R - 0.9)
            if y > YC:
                if abs(x) > R - 0.9:
                    continue
            elif (x * x + (y - YC) ** 2) ** 0.5 > R - 0.9:
                continue
            d = cen - Vector((x, y, 0))
            rot = math.atan2(-d.x, d.y)
            instance(seat, f"seat_{k}_{j}", (x, y, rake(y)), rot, C["seating"])

    # --- ceiling + dome + chandelier
    if with_ceiling:
        box("ceiling", (0, YC + 1, CEIL + 0.2), (2 * (R + DEPTH) + 1, 2 * (R + DEPTH) + 6, 0.4), M["cream"], C["ceiling"])
        cylinder("dome", (0, YC, CEIL - 0.02), 8.0, 0.06, M["fresco"], C["ceiling"], segments=96)
        ring = [(8.0 * math.cos(a * 2 * math.pi / 96), YC + 8.0 * math.sin(a * 2 * math.pi / 96), CEIL - 0.05)
                for a in range(96)]
        sweep("dome_ring", [(-0.05, -0.2), (0.3, -0.2), (0.35, 0.0), (-0.05, 0.0)], ring, M["gold"], C["ceiling"],
              closed_path=True)
        ring2 = [(10.2 * math.cos(a * 2 * math.pi / 96), YC + 10.2 * math.sin(a * 2 * math.pi / 96), CEIL - 0.05)
                 for a in range(96)]
        sweep("dome_ring2", [(-0.05, -0.12), (0.2, -0.12), (0.2, 0.0), (-0.05, 0.0)], ring2, M["gold"], C["ceiling"],
              closed_path=True)
        # proscenium ceiling band
        box("ceil_band", (0, -0.9, CEIL - 0.3), (2 * (R + DEPTH), 1.0, 0.6), M["cream"], C["ceiling"], bevel=0.05)
        # chandelier
        cz = CEIL - 2.6
        cylinder("chain", (0, YC, (CEIL + cz) / 2 + 0.4), 0.03, CEIL - cz - 0.8, M["gold"], C["lighting"])
        for ri, (rr, zz, nb) in enumerate([(1.7, cz, 28), (1.2, cz + 0.45, 20), (0.7, cz + 0.85, 12), (0.45, cz - 0.35, 10)]):
            pts = [(rr * math.cos(a * 2 * math.pi / 48), YC + rr * math.sin(a * 2 * math.pi / 48), zz) for a in range(48)]
            sweep(f"ch_ring{ri}", [(-0.03, -0.03), (0.03, -0.03), (0.03, 0.03), (-0.03, 0.03)], pts, M["gold"],
                  C["lighting"], closed_path=True)
            for b in range(nb):
                a = b * 2 * math.pi / nb
                sphere(f"bulb_{ri}_{b}", (rr * math.cos(a), YC + rr * math.sin(a), zz + 0.12), 0.05, M["bulb"],
                       C["lighting"], segs=10, rings=6)
                sphere(f"drop_{ri}_{b}", (rr * math.cos(a + 0.1), YC + rr * math.sin(a + 0.1), zz - 0.22), 0.04,
                       M["glass"], C["lighting"], segs=10, rings=6)
        sphere("ch_bowl", (0, YC, cz - 0.1), 0.55, M["glass"], C["lighting"], segs=24, rings=12).scale = (1, 1, 0.6)
        light("chand_light", "POINT", (0, YC, cz), 2500 * house_level, (1.0, 0.72, 0.45), size=1.2, coll=C["lighting"])

    # --- lights
    for sx in (-1, 1):
        light(f"foh_{sx}", "SPOT", (sx * 6, -9, CEIL - 0.8), 9000, (1.0, 0.88, 0.72), size=0.3, target=(sx * 1.5, 7.5, 3.5),
              spot_deg=26, blend=0.5, coll=C["lighting"])
        light(f"side_{sx}", "SPOT", (sx * 9.0, 6.5, 7.5), 7000, (1.0, 0.55, 0.2) if sx < 0 else (0.35, 0.5, 1.0),
              size=0.3, target=(0, 7.5, 2.5), spot_deg=35, blend=0.6, coll=C["lighting"])
    light("back_top", "SPOT", (0, 11.5, 12.5), 6000, (1.0, 0.7, 0.45), size=0.5, target=(0, 6, 1.5), spot_deg=55,
          blend=0.7, coll=C["lighting"])
    light("apron_wash", "AREA", (0, -6, 12), 1500, (1.0, 0.85, 0.7), size=8, target=(0, -1, 1), coll=C["lighting"])
    # house fill
    for x, y in [(-7, -8), (7, -8), (-7, -19), (7, -19), (0, -14)]:
        light(f"house_{x}_{y}", "AREA", (x, y, CEIL - 0.6), 1100 * house_level, (1.0, 0.78, 0.55), size=4,
              target=(x, y, 0), coll=C["lighting"])
    for ti, z in enumerate(TIERS):
        light(f"box_fill_{ti}", "POINT", (0, YC - R - DEPTH / 2, z + 2.2), 250 * house_level, (1.0, 0.7, 0.45), size=0.6,
              coll=C["lighting"])
    return sc, M, C


def make_seat(M, coll):
    parts = [
        box("s_cush", (0, 0.0, 0.46), (0.5, 0.48, 0.12), M["velvet"], bevel=0.04),
        box("s_back", (0, -0.27, 0.78), (0.5, 0.1, 0.62), M["velvet"], bevel=0.04),
        box("s_shell", (0, -0.33, 0.74), (0.52, 0.04, 0.66), M["darkwood"], bevel=0.015),
        box("s_armL", (-0.27, -0.02, 0.6), (0.05, 0.46, 0.05), M["darkwood"], bevel=0.015),
        box("s_armR", (0.27, -0.02, 0.6), (0.05, 0.46, 0.05), M["darkwood"], bevel=0.015),
        box("s_stdL", (-0.27, -0.1, 0.28), (0.05, 0.3, 0.56), M["metal"]),
        box("s_stdR", (0.27, -0.1, 0.28), (0.05, 0.3, 0.56), M["metal"]),
    ]
    parts[1].rotation_euler[0] = math.radians(-10)
    seat = join(parts, "seat_src")
    for c in seat.users_collection:
        c.objects.unlink(seat)
    coll.objects.link(seat)
    seat.location = (0, 0, -100)  # hidden master
    return seat


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else os.path.join(os.path.dirname(__file__), "theater.blend")
    build()
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("saved", out)
