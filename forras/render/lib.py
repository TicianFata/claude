"""Shared Blender helpers for the Brick+Data concept scenes (procedural, CC0 textures only)."""
import bpy, bmesh, math, os, addon_utils
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
MODELS = os.path.join(HERE, "..", "dl", "models")


# ---------------------------------------------------------------- scene setup
def reset(samples=96):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon_utils.enable("cycles", default_set=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 5
    sc.cycles.diffuse_bounces = 2
    sc.cycles.glossy_bounces = 2
    sc.cycles.transmission_bounces = 4
    sc.cycles.adaptive_threshold = 0.025
    sc.cycles.light_sampling_threshold = 0.02
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 1.0
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    sc.render.image_settings.file_format = "PNG"
    sc.render.resolution_percentage = 100
    world = bpy.data.worlds.new("World")
    sc.world = world
    world.use_nodes = True
    return sc


def world_color(rgb=(0.01, 0.01, 0.012), strength=1.0):
    w = bpy.context.scene.world
    bg = w.node_tree.nodes.get("Background")
    for l in list(bg.inputs["Color"].links):
        w.node_tree.links.remove(l)
    bg.inputs["Color"].default_value = (*rgb, 1)
    bg.inputs["Strength"].default_value = strength


def world_sky(sun_elev_deg=12, sun_rot_deg=200, strength=1.0, air=1.0, dust=1.0):
    w = bpy.context.scene.world
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    sky = nt.nodes.new("ShaderNodeTexSky")
    for t in ("NISHITA", "SINGLE_SCATTERING", "MULTIPLE_SCATTERING"):
        try:
            sky.sky_type = t
            break
        except Exception:
            continue
    try:
        sky.sun_elevation = math.radians(sun_elev_deg)
        sky.sun_rotation = math.radians(sun_rot_deg)
        sky.air_density = air
        sky.aerosol_density = dust
    except Exception:
        pass
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    return sky


def render(path, res=(1920, 1080), samples=None):
    sc = bpy.context.scene
    if os.environ.get("QTEST"):
        res = (max(64, res[0] // 6), max(64, res[1] // 6))
        samples = min(samples or 4, 4)
        path = path.replace("/final/", "/final_test/")
        os.makedirs(os.path.dirname(path), exist_ok=True)
    sc.render.resolution_x, sc.render.resolution_y = res
    if samples:
        sc.cycles.samples = samples
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


def camera(name, loc, target, lens=24, sensor=36, shift=(0, 0)):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = sensor
    cd.shift_x, cd.shift_y = shift
    cd.clip_start = 0.05
    cd.clip_end = 2000
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    look_at(ob, target)
    return ob


def look_at(ob, target):
    d = Vector(target) - Vector(ob.location)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def pano_camera(name, loc):
    cd = bpy.data.cameras.new(name)
    cd.type = "PANO"
    try:
        cd.panorama_type = "EQUIRECTANGULAR"
    except Exception:
        cd.cycles.panorama_type = "EQUIRECTANGULAR"
    cd.clip_start = 0.05
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    # equirect: camera looks along -Z; rotate so horizon is level, forward = +Y
    ob.rotation_euler = (math.radians(90), 0, 0)
    return ob


# ---------------------------------------------------------------- materials
_mat_cache = {}


def _img(name, colorspace="sRGB"):
    p = os.path.join(TEX, name)
    im = bpy.data.images.load(p, check_existing=True)
    im.colorspace_settings.name = colorspace
    return im


def mat(name, color=(0.8, 0.8, 0.8), rough=0.5, metal=0.0, sheen=0.0, sheen_tint=(1, 1, 1),
        emit=None, emit_strength=0.0, transmission=0.0, coat=0.0, alpha=1.0, ior=1.45,
        tex=None, tex_scale=1.0, tex_tint=None, normal=None, normal_strength=0.6, bump_noise=0.0,
        noise_var=0.0, noise_scale=6.0, specular=0.5):
    if name in _mat_cache:
        return _mat_cache[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Specular IOR Level"].default_value = specular
    p.inputs["IOR"].default_value = ior
    if sheen:
        p.inputs["Sheen Weight"].default_value = sheen
        p.inputs["Sheen Tint"].default_value = (*sheen_tint, 1)
    if transmission:
        p.inputs["Transmission Weight"].default_value = transmission
    if coat:
        p.inputs["Coat Weight"].default_value = coat
    if emit is not None:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = emit_strength
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
    tc = None
    if tex or normal or bump_noise or noise_var:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (tex_scale, tex_scale, tex_scale)
        nt.links.new(tc.outputs["Object"] if tex == "__obj__" else tc.outputs["UV"], mp.inputs["Vector"])
    if tex:
        it = nt.nodes.new("ShaderNodeTexImage")
        it.image = _img(tex)
        it.projection = "BOX"
        it.projection_blend = 0.25
        # box projection needs object/generated coords; use object coords
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], it.inputs["Vector"])
        out = it.outputs["Color"]
        if tex_tint:
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            mix.blend_type = "MULTIPLY"
            mix.inputs["Factor"].default_value = 1.0
            nt.links.new(out, mix.inputs[6])
            mix.inputs[7].default_value = (*tex_tint, 1)
            out = mix.outputs[2]
        nt.links.new(out, p.inputs["Base Color"])
    if normal:
        nm = nt.nodes.new("ShaderNodeTexImage")
        nm.image = _img(normal, "Non-Color")
        nm.projection = "BOX"
        nm.projection_blend = 0.25
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], nm.inputs["Vector"])
        nn = nt.nodes.new("ShaderNodeNormalMap")
        nn.inputs["Strength"].default_value = normal_strength
        nt.links.new(nm.outputs["Color"], nn.inputs["Color"])
        nt.links.new(nn.outputs["Normal"], p.inputs["Normal"])
    if noise_var and not tex:
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = noise_scale
        nz.inputs["Detail"].default_value = 8
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.inputs["Factor"].default_value = noise_var
        mix.blend_type = "MULTIPLY"
        ramp = nt.nodes.new("ShaderNodeMapRange")
        ramp.inputs["From Min"].default_value = 0.3
        ramp.inputs["From Max"].default_value = 0.7
        ramp.inputs["To Min"].default_value = 0.75
        ramp.inputs["To Max"].default_value = 1.15
        nt.links.new(nz.outputs["Fac"], ramp.inputs["Value"])
        mix.inputs[6].default_value = (*color, 1)
        nt.links.new(ramp.outputs["Result"], mix.inputs[7])
        nt.links.new(mix.outputs[2], p.inputs["Base Color"])
    if bump_noise:
        nz2 = nt.nodes.new("ShaderNodeTexNoise")
        nz2.inputs["Scale"].default_value = 40
        nz2.inputs["Detail"].default_value = 6
        nt.links.new(tc.outputs["Object"], nz2.inputs["Vector"])
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump_noise
        bp.inputs["Distance"].default_value = 0.02
        nt.links.new(nz2.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], p.inputs["Normal"])
    _mat_cache[name] = m
    return m


def emission_mat(name, color, strength):
    if name in _mat_cache:
        return _mat_cache[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*color, 1)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    _mat_cache[name] = m
    return m


def gradient_emission_mat(name, c_bottom, c_top, z0, z1, strength=1.0):
    """Vertical gradient emission (e.g. lit cyclorama / sky backdrop)."""
    if name in _mat_cache:
        return _mat_cache[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = z0
    mr.inputs["From Max"].default_value = z1
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    nt.links.new(mr.outputs["Result"], mix.inputs["Factor"])
    mix.inputs[6].default_value = (*c_bottom, 1)
    mix.inputs[7].default_value = (*c_top, 1)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Strength"].default_value = strength
    nt.links.new(mix.outputs[2], e.inputs["Color"])
    nt.links.new(e.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    _mat_cache[name] = m
    return m


# ---------------------------------------------------------------- geometry
def link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def mesh_obj(name, verts, faces, material=None, coll=None, smooth=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.validate()
    me.update()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    link(ob, coll)
    return ob


def box(name, center, size, material=None, coll=None, bevel=0.0, rot_z=0.0):
    cx, cy, cz = center
    sx, sy, sz = [s / 2 for s in size]
    v = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
         (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = mesh_obj(name, v, f, material, coll)
    ob.location = (cx, cy, cz)
    ob.rotation_euler[2] = rot_z
    if bevel:
        bv = ob.modifiers.new("bevel", "BEVEL")
        bv.width = bevel
        bv.segments = 2
        bv.limit_method = "ANGLE"
    return ob


def cylinder(name, center, radius, depth, material=None, coll=None, segments=24, axis="Z", rot=None, cap=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=cap, segments=segments, radius1=radius, radius2=radius, depth=depth)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    link(ob, coll)
    ob.location = center
    if axis == "X":
        ob.rotation_euler = (0, math.radians(90), 0)
    elif axis == "Y":
        ob.rotation_euler = (math.radians(90), 0, 0)
    if rot:
        ob.rotation_euler = rot
    return ob


def sphere(name, center, radius, material=None, coll=None, segs=16, rings=10):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=radius)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    link(ob, coll)
    ob.location = center
    return ob


def sweep(name, profile, path, material=None, coll=None, closed_path=False, smooth=True, cap=True):
    """Sweep a 2D profile [(u, v)] along a 3D path; u = horizontal offset (left of travel), v = up."""
    n = len(path)
    verts, faces = [], []
    P = [Vector(p) for p in path]
    for i in range(n):
        if closed_path:
            t = (P[(i + 1) % n] - P[i - 1])
        else:
            t = (P[min(i + 1, n - 1)] - P[max(i - 1, 0)])
        t.z = 0
        t.normalize()
        side = Vector((-t.y, t.x, 0))
        for (u, v) in profile:
            verts.append(P[i] + side * u + Vector((0, 0, v)))
    m = len(profile)
    segs = n if closed_path else n - 1
    for i in range(segs):
        a, b = i, (i + 1) % n
        for j in range(m - 1):
            faces.append((a * m + j, b * m + j, b * m + j + 1, a * m + j + 1))
    if cap and not closed_path:
        faces.append(tuple(range(m))[::-1])
        faces.append(tuple(range((n - 1) * m, n * m)))
    return mesh_obj(name, verts, faces, material, coll, smooth=smooth)


def ribbon(name, curve_a, curve_b, material=None, coll=None, thickness=0.0):
    """Surface between two equal-length polylines (e.g. balcony slab)."""
    n = len(curve_a)
    verts = [tuple(p) for p in curve_a] + [tuple(p) for p in curve_b]
    faces = [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)]
    ob = mesh_obj(name, verts, faces, material, coll)
    if thickness:
        so = ob.modifiers.new("solid", "SOLIDIFY")
        so.thickness = thickness
        so.offset = -1
    return ob


def grid_surface(name, nx, ny, fn, material=None, coll=None, smooth=True):
    """Parametric surface: fn(u, v) -> (x, y, z), u,v in [0,1]."""
    verts = []
    for j in range(ny + 1):
        for i in range(nx + 1):
            verts.append(fn(i / nx, j / ny))
    faces = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    return mesh_obj(name, verts, faces, material, coll, smooth=smooth)


def instance(src, name, loc, rot_z=0.0, coll=None, scale=None):
    ob = src.copy()  # linked mesh data
    ob.name = name
    ob.location = loc
    ob.rotation_euler = (src.rotation_euler[0], src.rotation_euler[1], rot_z)
    if scale:
        ob.scale = scale
    link(ob, coll)
    return ob


def join(objs, name):
    """Join objects (applying modifiers) into one mesh object."""
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    mats = []
    for ob in objs:
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        me.transform(ob.matrix_world)
        offset = len(mats)
        for m in me.materials:
            mats.append(m)
        tmp = bmesh.new()
        tmp.from_mesh(me)
        for f in tmp.faces:
            f.material_index += offset
        me2 = bpy.data.meshes.new("tmp")
        tmp.to_mesh(me2)
        bm.from_mesh(me2)
        tmp.free()
        ev.to_mesh_clear()
        bpy.data.meshes.remove(me2)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    link(ob)
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    return ob


# ---------------------------------------------------------------- lights
def light(name, kind, loc, energy, color=(1, 0.9, 0.8), size=0.5, target=None, spot_deg=40, blend=0.4,
          coll=None):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = color
    if kind in ("POINT", "SPOT"):
        ld.shadow_soft_size = size
    if kind == "AREA":
        ld.size = size
    if kind == "SPOT":
        ld.spot_size = math.radians(spot_deg)
        ld.spot_blend = blend
    if kind == "SUN":
        ld.angle = math.radians(size)
    ob = bpy.data.objects.new(name, ld)
    link(ob, coll)
    ob.location = loc
    if target is not None:
        look_at(ob, target)
    return ob


def import_glb(path, loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    root = bpy.data.objects.new(os.path.basename(path) + "_root", None)
    link(root, coll)
    for o in new:
        if o.parent is None:
            o.parent = root
        if coll is not None:
            for c in o.users_collection:
                c.objects.unlink(o)
            coll.objects.link(o)
    root.location = loc
    root.rotation_euler[2] = rot_z
    root.scale = (scale, scale, scale)
    return root, new


# ---------------------------------------------------------------- helpers
def horseshoe(R, y_straight, y_center, n_arc=48, n_straight=6, offset=0.0):
    """Plan path (x, y): straight from (-R, y_straight) back to arc centre, semicircle to +R, straight forward."""
    r = R + offset
    pts = []
    for i in range(n_straight):
        t = i / n_straight
        pts.append((-r, y_straight + (y_center - y_straight) * t))
    for i in range(n_arc + 1):
        a = math.pi + math.pi * i / n_arc  # from 180deg to 360deg
        pts.append((r * math.cos(a), y_center + r * math.sin(a)))
    for i in range(1, n_straight + 1):
        t = i / n_straight
        pts.append((r, y_center + (y_straight - y_center) * t))
    return pts


def world_gradient(horizon=(1.0, 0.52, 0.28), mid=(0.42, 0.38, 0.55), zenith=(0.06, 0.11, 0.3),
                   ground=(0.05, 0.045, 0.04), strength=1.0, mid_pos=0.12):
    """Dusk sky as a world gradient by view-direction elevation."""
    w = bpy.context.scene.world
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -0.05
    mr.inputs["From Max"].default_value = 0.85
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0
    cr.elements[0].color = (*ground, 1)
    cr.elements[1].position = 1.0
    cr.elements[1].color = (*zenith, 1)
    e = cr.elements.new(0.06)
    e.color = (*horizon, 1)
    e2 = cr.elements.new(0.06 + mid_pos)
    e2.color = (*mid, 1)
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength


def tree_proto(name, rnd, leaf_mats, bark, leaf_tex, kind=0):
    """Build a tree prototype in its own (unlinked) collection; returns (collection, height)."""
    coll = bpy.data.collections.new(name)
    h = 10.0
    trunk_h = 3.6 if kind != 1 else 2.0
    cylinder(name + "_trunk", (0, 0, trunk_h / 2 + 0.6), 0.22, trunk_h + 1.2, bark, coll, segments=8)
    if kind == 1:  # columnar
        rx, rz, cz, n = 1.6, 4.4, 5.6, 26
    elif kind == 2:  # conifer-ish
        rx, rz, cz, n = 2.6, 4.0, 5.2, 30
    else:
        rx, rz, cz, n = 3.6, 3.0, 6.6, 34
    for k in range(n):
        # sample inside ellipsoid, biased to shell
        while True:
            x, y, z = rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            if x * x + y * y + z * z <= 1:
                break
        s = 0.55 + 0.45 * (x * x + y * y + z * z) ** 0.5
        r = rnd.uniform(0.9, 1.5) * (rx / 3.6) ** 0.5
        if kind == 2:
            rr = rx * (1 - (z + 1) / 2) + 0.3
            x, y = x * rr / rx, y * rr / rx
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r)
        me = bpy.data.meshes.new(f"{name}_c{k}")
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = True
        ob = bpy.data.objects.new(f"{name}_c{k}", me)
        ob.data.materials.append(leaf_mats[rnd.randrange(len(leaf_mats))])
        coll.objects.link(ob)
        ob.location = (x * rx * s, y * rx * s, cz + z * rz * s)
        ob.scale = (1, 1, 0.8)
        d = ob.modifiers.new("d", "DISPLACE")
        d.texture = leaf_tex
        d.strength = r * 0.45
        d.texture_coords = "GLOBAL"
    return coll, h


def place_tree(proto, h_proto, name, loc, h, rot, coll=None):
    e = bpy.data.objects.new(name, None)
    e.instance_type = "COLLECTION"
    e.instance_collection = proto
    e.location = loc
    s = h / h_proto
    e.scale = (s, s, s)
    e.rotation_euler[2] = rot
    (coll or bpy.context.scene.collection).objects.link(e)
    return e
