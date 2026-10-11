"""Alternative render modes for the concept scenes: BIM categories, clay, thermal, point clouds."""
import bpy, re, math, os, numpy as np
from lib import mat, emission_mat, light, world_color, camera, render


def objects_meshlike():
    return [o for o in bpy.context.scene.objects if o.type in ("MESH", "CURVE", "FONT")]


def hide_lights(hide=True):
    for o in bpy.context.scene.objects:
        if o.type == "LIGHT":
            o.hide_render = hide


def set_view(transform="AgX", look="None", exposure=0.0):
    vs = bpy.context.scene.view_settings
    vs.view_transform = transform
    try:
        vs.look = look
    except Exception:
        vs.look = "None"
    vs.exposure = exposure


def replace_materials(fn):
    """fn(obj) -> material or None (keep). Works on mesh data (instances share)."""
    done = set()
    for o in objects_meshlike():
        m = fn(o)
        if m is None or o.data is None:
            continue
        key = o.data.name
        if key in done:
            continue
        done.add(key)
        mats = o.data.materials
        if len(mats) == 0:
            mats.append(m)
        else:
            for i in range(len(mats)):
                mats[i] = m
    # instanced collections (trees) – patch their objects too
    for c in bpy.data.collections:
        for o in c.objects:
            if o.type == "MESH" and o.data.name not in done:
                m = fn(o)
                if m is not None:
                    done.add(o.data.name)
                    for i in range(len(o.data.materials)):
                        o.data.materials[i] = m


def bim_material(name, color):
    return mat("bim_" + name, color, rough=0.65, specular=0.3)


def apply_bim(rules, default=("Egyéb", (0.8, 0.8, 0.8))):
    """rules: list of (regex, label, rgb). First match wins, by object (or parent) name."""
    mats = {}
    used = {}

    def pick(o):
        names = [o.name] + ([o.parent.name] if o.parent else [])
        for rx, label, col in rules:
            if any(re.search(rx, n) for n in names):
                break
        else:
            label, col = default
        if label not in mats:
            mats[label] = bim_material(label, col)
        used[label] = col
        return mats[label]
    replace_materials(pick)
    return used


def bim_lighting(sun_dir=(-0.5, -0.8, 1.0), strength=1.0):
    hide_lights(True)
    world_color((0.92, 0.94, 0.97), 0.9 * strength)
    s = light("bim_sun", "SUN", (sun_dir[0] * 50, sun_dir[1] * 50, sun_dir[2] * 50), 2.2 * strength, (1, 0.98, 0.95),
              size=3.0, target=(0, 0, 0))
    return s


def freestyle(on=True, thickness=1.0, color=(0.1, 0.12, 0.15), crease=134):
    sc = bpy.context.scene
    sc.render.use_freestyle = on
    if not on:
        return
    sc.render.line_thickness_mode = "ABSOLUTE"
    sc.render.line_thickness = thickness
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("lines")
    ls.select_by_visibility = True
    ls.select_by_edge_types = True
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = True
    fs.crease_angle = math.radians(crease)
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("bim_lines")
    ls.linestyle.color = color
    ls.linestyle.thickness = thickness


def thermal_material(base_key="temp"):
    """Emission = inferno-like ramp of (object temperature + height gradient + noise)."""
    m = bpy.data.materials.get("__thermal__")
    if m:
        return m
    m = bpy.data.materials.new("__thermal__")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    at = nt.nodes.new("ShaderNodeAttribute")
    at.attribute_type = "OBJECT"
    at.attribute_name = base_key
    zgrad = nt.nodes.new("ShaderNodeAttribute")
    zgrad.attribute_type = "OBJECT"
    zgrad.attribute_name = "tgrad"
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    mz = nt.nodes.new("ShaderNodeMath")
    mz.operation = "MULTIPLY"
    nt.links.new(sep.outputs["Z"], mz.inputs[0])
    nt.links.new(zgrad.outputs["Fac"], mz.inputs[1])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.5
    nz.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], nz.inputs["Vector"])
    nzs = nt.nodes.new("ShaderNodeMath")
    nzs.operation = "MULTIPLY_ADD"
    nt.links.new(nz.outputs["Fac"], nzs.inputs[0])
    nzs.inputs[1].default_value = 0.08
    nzs.inputs[2].default_value = -0.04
    add1 = nt.nodes.new("ShaderNodeMath")
    add1.operation = "ADD"
    nt.links.new(at.outputs["Fac"], add1.inputs[0])
    nt.links.new(mz.outputs[0], add1.inputs[1])
    add2 = nt.nodes.new("ShaderNodeMath")
    add2.operation = "ADD"
    add2.use_clamp = True
    nt.links.new(add1.outputs[0], add2.inputs[0])
    nt.links.new(nzs.outputs[0], add2.inputs[1])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    stops = [(0.0, (0.0, 0.0, 0.02)), (0.2, (0.12, 0.02, 0.32)), (0.42, (0.55, 0.05, 0.45)), (0.62, (0.9, 0.25, 0.1)),
             (0.82, (1.0, 0.65, 0.05)), (1.0, (1.0, 1.0, 0.75))]
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*stops[0][1], 1)
    cr.elements[1].position, cr.elements[1].color = stops[-1][0], (*stops[-1][1], 1)
    for p, c in stops[1:-1]:
        e = cr.elements.new(p)
        e.color = (*c, 1)
    nt.links.new(add2.outputs[0], ramp.inputs["Fac"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    return m


def apply_thermal(temp_rules, default=0.35, zgrad=0.0):
    """temp_rules: list of (regex, temperature 0..1, height gradient per metre)."""
    tm = thermal_material()
    for o in objects_meshlike() + [o for c in bpy.data.collections for o in c.objects if o.type == "MESH"]:
        names = [o.name] + ([o.parent.name] if o.parent else [])
        t, g = default, zgrad
        for rx, tv, gv in temp_rules:
            if any(re.search(rx, n) for n in names):
                t, g = tv, gv
                break
        o["temp"] = t
        o["tgrad"] = g
    bpy.context.scene.view_layers[0].material_override = tm
    hide_lights(True)
    world_color((0.0, 0.0, 0.02), 1.0)
    set_view("Standard", "None", 0.0)


def clay(color=(0.82, 0.82, 0.8)):
    m = mat("__clay__", color, rough=0.7)
    bpy.context.scene.view_layers[0].material_override = m
    return m


def hide_all_meshes(hide=True, keep=()):
    for o in bpy.context.scene.objects:
        if o.type in ("MESH", "CURVE", "FONT", "EMPTY") and o.name not in keep:
            o.hide_render = hide


def load_cloud(path):
    d = np.load(path)
    return d["pts"], d["cols"]


def cloud_to_mesh(name, pts, cols, voxel=0.06, radius=0.07):
    """Reconstruct a surface mesh from a point cloud (points -> SDF volume -> mesh), colour from nearest point."""
    from scan import cloud_object
    ob = cloud_object(name + "_src", pts, cols, radius=0.01)
    ob.modifiers.clear()
    ng = bpy.data.node_groups.new(name + "_rec", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    gi = ng.nodes.new("NodeGroupInput")
    go = ng.nodes.new("NodeGroupOutput")
    mp = ng.nodes.new("GeometryNodeMeshToPoints")
    mp.inputs["Radius"].default_value = radius
    pv = ng.nodes.new("GeometryNodePointsToVolume")
    try:
        pv.inputs["Resolution Mode"].default_value = "Size"
    except Exception:
        try:
            pv.resolution_mode = "VOXEL_SIZE"
        except Exception:
            pass
    for k in ("Voxel Size",):
        if k in pv.inputs:
            pv.inputs[k].default_value = voxel
    if "Density" in pv.inputs:
        pv.inputs["Density"].default_value = 1.0
    vm = ng.nodes.new("GeometryNodeVolumeToMesh")
    if "Threshold" in vm.inputs:
        vm.inputs["Threshold"].default_value = 0.1
    # transfer colour: sample nearest source point
    sn = ng.nodes.new("GeometryNodeSampleNearest")
    si = ng.nodes.new("GeometryNodeSampleIndex")
    si.data_type = "FLOAT_COLOR"
    si.domain = "POINT"
    na = ng.nodes.new("GeometryNodeInputNamedAttribute")
    na.data_type = "FLOAT_COLOR"
    na.inputs["Name"].default_value = "Col"
    sa = ng.nodes.new("GeometryNodeStoreNamedAttribute")
    sa.data_type = "FLOAT_COLOR"
    sa.domain = "POINT"
    sa.inputs["Name"].default_value = "Col"
    ng.links.new(gi.outputs[0], mp.inputs["Mesh"])
    ng.links.new(mp.outputs["Points"], pv.inputs["Points"])
    ng.links.new(pv.outputs["Volume"], vm.inputs["Volume"])
    ng.links.new(gi.outputs[0], sn.inputs["Geometry"])
    ng.links.new(gi.outputs[0], si.inputs["Geometry"])
    ng.links.new(na.outputs["Attribute"], si.inputs["Value"])
    ng.links.new(sn.outputs["Index"], si.inputs["Index"])
    ng.links.new(vm.outputs["Mesh"], sa.inputs["Geometry"])
    ng.links.new(si.outputs["Value"], sa.inputs["Value"])
    ng.links.new(sa.outputs["Geometry"], go.inputs[0])
    mod = ob.modifiers.new("rec", "NODES")
    mod.node_group = ng
    return ob


def vertex_color_material(name="__vcol__", wire=False, emission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    at = nt.nodes.new("ShaderNodeAttribute")
    at.attribute_name = "Col"
    p.inputs["Roughness"].default_value = 0.8
    if wire:
        wf = nt.nodes.new("ShaderNodeWireframe")
        wf.use_pixel_size = True
        wf.inputs["Size"].default_value = 0.5
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = 0.45
        nt.links.new(wf.outputs["Fac"], mul.inputs[0])
        nt.links.new(mul.outputs[0], mix.inputs["Factor"])
        nt.links.new(at.outputs["Color"], mix.inputs[6])
        mix.inputs[7].default_value = (0.02, 0.6, 0.75, 1)
        nt.links.new(mix.outputs[2], p.inputs["Base Color"])
    else:
        nt.links.new(at.outputs["Color"], p.inputs["Base Color"])
    if emission:
        nt.links.new(at.outputs["Color"], p.inputs["Emission Color"])
        p.inputs["Emission Strength"].default_value = emission
    return m
