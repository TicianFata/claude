"""Virtual terrestrial laser scan: equirect colour + depth renders per station -> coloured point cloud."""
import bpy, os, math, numpy as np
from lib import pano_camera, render


def depth_material():
    m = bpy.data.materials.get("__depth__")
    if m:
        return m
    m = bpy.data.materials.new("__depth__")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    cd = nt.nodes.new("ShaderNodeCameraData")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(cd.outputs["View Distance"], em.inputs["Strength"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    return m


def scan_station(name, loc, outdir, res=(2048, 1024), samples=48, keep_color=True):
    sc = bpy.context.scene
    cam = pano_camera("scan_" + name, loc)
    sc.camera = cam
    col_path = os.path.join(outdir, f"{name}_rgb.png")
    dep_path = os.path.join(outdir, f"{name}_depth.exr")
    # colour pass (also usable as 360 panorama)
    if keep_color or not os.path.exists(col_path):
        render(col_path, res, samples)
    # depth pass
    vl = sc.view_layers[0]
    saved = dict(samples=sc.cycles.samples, den=sc.cycles.use_denoising, fw=sc.cycles.filter_width,
                 ad=sc.cycles.use_adaptive_sampling, fmt=sc.render.image_settings.file_format,
                 vt=sc.view_settings.view_transform, look=sc.view_settings.look, exp=sc.view_settings.exposure)
    world = sc.world
    bg = world.node_tree.nodes.get("Background")
    bg_strength = bg.inputs["Strength"].default_value
    bg.inputs["Strength"].default_value = 0.0
    # sky texture would still be zero-strength; good
    vl.material_override = depth_material()
    hidden = []
    for ob in sc.objects:
        if ob.type == "LIGHT" and not ob.hide_render:
            ob.hide_render = True
            hidden.append(ob)
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.cycles.use_adaptive_sampling = False
    sc.cycles.filter_width = 0.01
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0
    render(dep_path, res, 1)
    # restore
    vl.material_override = None
    for ob in hidden:
        ob.hide_render = False
    bg.inputs["Strength"].default_value = bg_strength
    sc.cycles.samples = saved["samples"]
    sc.cycles.use_denoising = saved["den"]
    sc.cycles.use_adaptive_sampling = saved["ad"]
    sc.cycles.filter_width = saved["fw"]
    sc.render.image_settings.file_format = saved["fmt"]
    sc.view_settings.view_transform = saved["vt"]
    sc.view_settings.look = saved["look"]
    sc.view_settings.exposure = saved["exp"]
    return col_path, dep_path


def load_pixels(path):
    im = bpy.data.images.load(path, check_existing=False)
    w, h = im.size
    a = np.empty(w * h * 4, dtype=np.float32)
    im.pixels.foreach_get(a)
    bpy.data.images.remove(im)
    return a.reshape(h, w, 4)[::-1]  # row 0 = top


def reconstruct(col_path, dep_path, loc, max_range=45.0, rng=None, keep=1.0):
    rng = rng or np.random.default_rng(1)
    col = load_pixels(col_path)[..., :3]
    dep = load_pixels(dep_path)[..., 0]
    h, w = dep.shape
    v, u = np.mgrid[0:h, 0:w]
    lon = (u + 0.5) / w * 2 * np.pi - np.pi
    lat = np.pi / 2 - (v + 0.5) / h * np.pi
    m = (dep > 0.05) & (dep < max_range)
    # equal-angle sampling like a TLS: thin rows towards the poles
    m &= rng.random(dep.shape) < np.cos(lat) * keep
    lon, lat, d = lon[m], lat[m], dep[m]
    dirs = np.stack([np.sin(lon) * np.cos(lat), np.cos(lon) * np.cos(lat), np.sin(lat)], -1)
    pts = np.asarray(loc, dtype=np.float32) + dirs * d[:, None]
    # range noise ~ 2 mm + tiny angular noise for scan realism
    pts += rng.normal(0, 0.002, pts.shape)
    c = col[m]
    # PNG pixels from bpy are already display-referred (sRGB values 0..1)
    return pts.astype(np.float32), np.clip(c * 255, 0, 255).astype(np.uint8), d


def voxel_downsample(pts, cols, voxel=0.015):
    key = np.floor(pts / voxel).astype(np.int64)
    key = key[:, 0] * 73856093 ^ key[:, 1] * 19349663 ^ key[:, 2] * 83492791
    _, idx = np.unique(key, return_index=True)
    return pts[idx], cols[idx]


def run(stations, outdir, res=(2048, 1024), samples=48, voxel=0.015, max_range=45.0):
    os.makedirs(outdir, exist_ok=True)
    P, Cc, S = [], [], []
    for i, (name, loc) in enumerate(stations):
        cp, dp = scan_station(name, loc, outdir, res, samples)
        p, c, _ = reconstruct(cp, dp, loc, max_range=max_range, rng=np.random.default_rng(i))
        P.append(p)
        Cc.append(c)
        S.append(np.full(len(p), i, np.uint8))
        print("station", name, len(p))
    P = np.concatenate(P)
    Cc = np.concatenate(Cc)
    S = np.concatenate(S)
    key_idx = np.arange(len(P))
    Pd, Cd = voxel_downsample(P, Cc, voxel)
    np.savez_compressed(os.path.join(outdir, "cloud.npz"), pts=Pd, cols=Cd)
    print("cloud total", len(P), "->", len(Pd))
    return Pd, Cd


# ---------------------------------------------------------------- render helpers for clouds
def cloud_object(name, pts, cols, radius=0.012, emission=1.0, coll=None, color_mode="rgb"):
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(pts))
    me.vertices.foreach_set("co", pts.astype(np.float32).ravel())
    attr = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
    c = cols.astype(np.float32) / 255.0
    # display sRGB -> linear for emission
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    rgba = np.concatenate([c, np.ones((len(c), 1), np.float32)], 1)
    attr.data.foreach_set("color", rgba.ravel())
    ob = bpy.data.objects.new(name, me)
    (coll or bpy.context.scene.collection).objects.link(ob)
    # geometry nodes: mesh to points
    ng = bpy.data.node_groups.new(name + "_gn", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    gi = ng.nodes.new("NodeGroupInput")
    go = ng.nodes.new("NodeGroupOutput")
    mp = ng.nodes.new("GeometryNodeMeshToPoints")
    mp.inputs["Radius"].default_value = radius
    sm = ng.nodes.new("GeometryNodeSetMaterial")
    pm = bpy.data.materials.new(name + "_mat")
    pm.use_nodes = True
    nt = pm.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    at = nt.nodes.new("ShaderNodeAttribute")
    at.attribute_name = "Col"
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = emission
    nt.links.new(at.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    sm.inputs["Material"].default_value = pm
    ng.links.new(gi.outputs[0], mp.inputs["Mesh"])
    ng.links.new(mp.outputs["Points"], sm.inputs["Geometry"])
    ng.links.new(sm.outputs["Geometry"], go.inputs[0])
    mod = ob.modifiers.new("pts", "NODES")
    mod.node_group = ng
    return ob


def height_colors(pts, zmin=None, zmax=None):
    """Classic scanner 'elevation' colouring (deep blue -> cyan -> amber)."""
    z = pts[:, 2]
    zmin = z.min() if zmin is None else zmin
    zmax = z.max() if zmax is None else zmax
    t = np.clip((z - zmin) / (zmax - zmin), 0, 1)[:, None]
    stops = np.array([[20, 40, 120], [0, 170, 220], [120, 230, 200], [255, 200, 90], [255, 110, 60]], np.float32)
    pos = np.linspace(0, 1, len(stops))
    out = np.zeros((len(t), 3), np.float32)
    for k in range(3):
        out[:, k] = np.interp(t[:, 0], pos, stops[:, k])
    return out.astype(np.uint8)
