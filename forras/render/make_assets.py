"""Turn renders into web assets for /home/user/claude/portfolio (run with system python3 -I)."""
import os, sys, json, math, base64, io, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(W, "final")
P = "/home/user/claude/portfolio/assets"
IMG, PANO, CLOUD, VID = (os.path.join(P, d) for d in ("img", "pano", "cloud", "video"))
for d in (IMG, PANO, CLOUD, VID):
    os.makedirs(d, exist_ok=True)
FONT = "/home/user/claude/portfolio/assets/fonts"
missing = []


def src(rel):
    p = os.path.join(F, rel)
    if not os.path.exists(p):
        missing.append(rel)
        return None
    return p


def save(im, name, w=1920, q=84):
    im = im.convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, name), quality=q, optimize=True, progressive=True)


def put(rel, *names, w=1920, q=84):
    p = src(rel)
    if not p:
        return None
    im = Image.open(p).convert("RGB")
    for n in names:
        save(im, n, w, q)
    return im


def font(size, bold=False):
    # Inter variable is woff2 (PIL can't read) – fall back to DejaVu
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


# ------------------------------------------------------------------ straight copies
put("theater/photo_hero.png", "hero-foto.jpg", "same-latvany.jpg")
put("theater/cloud_hero.png", "hero-pontfelho.jpg", "same-pontfelho.jpg")
put("theater/cloud_height_hero.png", "same-magassag.jpg")
put("theater/mesh_hero.png", "same-mesh.jpg")
put("theater/bim_hero.png", "same-bim.jpg")
put("theater/photo_stage.png", "szinhaz-hero.jpg")
put("theater/photo_stalls.png", "szinhaz-nezoter.jpg")
put("theater/photo_cut.png", "svc-3dmodell.jpg")
put("theater/bim_cut.png", "svc-bim.jpg")
put("theater/cloud_over.png", "svc-pontfelho.jpg")
put("theater/cloud_over_height.png", "proc-feldolgozas.jpg")
put("theater/mesh_over.png", "svc-mesh.jpg")
put("museum/photo_hero.png", "muzeum-hero.jpg")
put("museum/cloud_hero.png", "muzeum-pontfelho.jpg")
put("museum/photo_diag.png", "muzeum-terem.jpg")
put("museum/cloud_over.png", "muzeum-pontfelho-felul.jpg")
put("museum/bim_over.png", "muzeum-bim.jpg")
put("museum/thermal_hero.png", "muzeum-hokep.jpg")
put("museum/photo_over.png", "muzeum-3dmodell.jpg")
put("hotel/photo_hero.png", "szalloda-hero.jpg")
put("hotel/bim_hero.png", "szalloda-bim.jpg")
put("hotel/photo_lounge.png", "szalloda-lounge.jpg")
put("hotel/photo_bed.png", "szalloda-agy.jpg")
put("hotel/photo_cut.png", "szalloda-3dmodell.jpg")
put("hotel/bim_cut.png", "szalloda-bim-metszet.jpg")
put("estate/drone_event.png", "rendezveny-hero.jpg")
put("estate/layout_model.png", "rendezveny-terv.jpg")
put("estate/layout_axo.png", "rendezveny-3dmodell.jpg")
put("estate/drone_hotel.png", "svc-dronfoto.jpg")
put("estate/drone_hotel_day.png", "szalloda-dron-nappal.jpg")
put("estate/thermal_facade.png", "svc-hoterkep.jpg")
put("estate/cloudplan_event.png", "rendezveny-pontfelho-terv.jpg")
put("estate/cloud_venue.png", "rendezveny-pontfelho.jpg")

# ------------------------------------------------------------------ overlays
def play_overlay(im, label=None):
    im = im.convert("RGB").copy()
    d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    r = int(h * 0.075)
    cx, cy = w // 2, h // 2
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(12, 15, 19, 150), outline=(255, 255, 255, 220), width=max(2, r // 18))
    d.polygon([(cx - r * 0.3, cy - r * 0.45), (cx - r * 0.3, cy + r * 0.45), (cx + r * 0.5, cy)], fill=(255, 255, 255, 235))
    # timeline
    y = h - int(h * 0.07)
    d.rectangle((int(w * 0.04), y - 3, int(w * 0.96), y + 3), fill=(255, 255, 255, 70))
    d.rectangle((int(w * 0.04), y - 3, int(w * 0.38), y + 3), fill=(201, 162, 90, 255))
    d.ellipse((int(w * 0.38) - 9, y - 9, int(w * 0.38) + 9, y + 9), fill=(255, 255, 255, 255))
    if label:
        f = font(int(h * 0.028), True)
        d.text((int(w * 0.04), y - int(h * 0.06)), label, font=f, fill=(255, 255, 255, 230))
    return im


p = src("estate/drone_wide.png")
if p:
    save(play_overlay(Image.open(p), "DRÓNVIDEÓ  00:12 / 00:30"), "svc-dronvideo.jpg")
p = src("estate/drone_event.png")
if p:
    save(play_overlay(Image.open(p), "DRÓNVIDEÓ"), "rendezveny-dronvideo.jpg")


def pano_ui(eq, label, video=False, yaw0=0.0, out_w=1920, out_h=1200, fov=100):
    """Rectilinear view of an equirect panorama + 360° badge (+ optional player bar)."""
    a = np.asarray(eq.convert("RGB")).astype(np.float32)
    H, Wd, _ = a.shape
    f = (out_w / 2) / math.tan(math.radians(fov) / 2)
    xs = np.arange(out_w) - out_w / 2 + 0.5
    ys = np.arange(out_h) - out_h / 2 + 0.5
    X, Y = np.meshgrid(xs, ys)
    Z = np.full_like(X, f)
    # pitch slight down
    pitch = math.radians(-6)
    Y2 = Y * math.cos(pitch) - Z * math.sin(pitch)
    Z2 = Y * math.sin(pitch) + Z * math.cos(pitch)
    lon = np.arctan2(X, Z2) + math.radians(yaw0)
    lat = -np.arctan2(Y2, np.sqrt(X ** 2 + Z2 ** 2))
    u = ((lon + math.pi) / (2 * math.pi) * Wd) % Wd
    v = np.clip((math.pi / 2 - lat) / math.pi * H, 0, H - 1)
    out = a[v.astype(int), u.astype(int)]
    im = Image.fromarray(out.astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    # 360 compass badge
    cx, cy, r = out_w - 110, 110, 62
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(12, 15, 19, 150), outline=(255, 255, 255, 200), width=3)
    d.pieslice((cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), -125, -55, fill=(201, 162, 90, 200))
    f = font(30, True)
    d.text((cx, cy + 4), "360°", font=f, fill=(255, 255, 255, 255), anchor="mm")
    if video:
        im = play_overlay(im, label)
    else:
        f2 = font(30, True)
        d.text((60, out_h - 80), label, font=f2, fill=(255, 255, 255, 235))
    return im


def tour_ui(eq, label, spots, yaw0=0.0):
    im = pano_ui(eq, label, False, yaw0)
    d = ImageDraw.Draw(im, "RGBA")
    for (x, y, t) in spots:
        d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=(201, 162, 90, 80))
        d.ellipse((x - 19, y - 19, x + 19, y + 19), fill=(201, 162, 90, 240), outline=(255, 255, 255, 255), width=4)
        f = font(24, True)
        tw = d.textlength(t, font=f)
        rounded(d, (x - tw / 2 - 14, y - 82, x + tw / 2 + 14, y - 42), 8, (12, 15, 19, 210))
        d.text((x, y - 62), t, font=f, fill=(255, 255, 255, 255), anchor="mm")
    # mini map strip
    rounded(d, (60, 60, 520, 120), 12, (12, 15, 19, 170))
    d.text((84, 90), "◀  Előző pont      1 / 3      Következő  ▶", font=font(22), fill=(255, 255, 255, 230), anchor="lm")
    return im


eqs = {}
for seg, files in (("szinhaz", ["theater/pano_szinpad.png", "theater/pano_nezoter.png", "theater/pano_paholy.png"]),
                   ("szalloda", ["hotel/pano_bejarat.png", "hotel/pano_agy.png", "hotel/pano_ablak.png"]),
                   ("muzeum", ["museum/pano_bejarat.png", "museum/pano_kozep.png", "museum/pano_kiallitas.png"]),
                   ("rendezveny", ["estate/pano_asztalok.png", "estate/pano_szinpad.png", "estate/pano_bejarat.png"])):
    for rel in files:
        p = src(rel)
        if not p:
            continue
        name = seg + "-" + os.path.basename(rel)[5:-4]
        im = Image.open(p).convert("RGB")
        eqs[name] = im
        im.save(os.path.join(PANO, name + ".jpg"), quality=82, optimize=True, progressive=True)
        b = base64.b64encode(open(os.path.join(PANO, name + ".jpg"), "rb").read()).decode()
        open(os.path.join(PANO, name + ".js"), "w").write(
            "window.BD_PANO=window.BD_PANO||{};window.BD_PANO[%s]='data:image/jpeg;base64,%s';\n" % (json.dumps(name), b))

if "szalloda-agy" in eqs:
    e = eqs["szalloda-agy"]
    # full equirect strip with badge -> unmistakably "360° panorama"
    strip = e.resize((1920, 960), Image.LANCZOS)
    d = ImageDraw.Draw(strip, "RGBA")
    rounded(d, (40, 40, 330, 104), 14, (12, 15, 19, 170))
    d.text((60, 72), "360° × 180°", font=font(30, True), fill=(255, 255, 255, 255), anchor="lm")
    save(strip, "svc-pano360.jpg")
    save(pano_ui(e, "360°-OS VIDEÓ  ·  SZOBA", video=True, yaw0=-40), "szalloda-video360.jpg")
if "muzeum-kozep" in eqs:
    save(pano_ui(eqs["muzeum-kozep"], "360°-OS VIDEÓ  ·  KIÁLLÍTÁS", video=True, yaw0=0), "svc-video360.jpg")
    m = eqs["muzeum-kozep"].resize((1920, 960), Image.LANCZOS)
    save(m, "muzeum-pano360.jpg")
if "rendezveny-asztalok" in eqs:
    save(eqs["rendezveny-asztalok"].resize((1920, 960), Image.LANCZOS), "rendezveny-pano360.jpg")
    save(pano_ui(eqs["rendezveny-asztalok"], "360°-OS VIDEÓ  ·  VENDÉGTÉR", video=True), "rendezveny-video360.jpg")
if "szinhaz-szinpad" in eqs:
    save(eqs["szinhaz-szinpad"].resize((1920, 960), Image.LANCZOS), "szinhaz-pano360.jpg")
if "szinhaz-nezoter" in eqs:
    save(pano_ui(eqs["szinhaz-nezoter"], "360°-OS VIDEÓ  ·  NÉZŐTÉR", video=True), "szinhaz-video360.jpg")
# ------------------------------------------------------------------ tours.js (hotspots from scene geometry)
NODES = {
    "szinhaz": ("Színház", "assets/img/szinhaz-nezoter.jpg", [
        ("szinpad", "Színpad", (0, 1.2, 2.65), 180, 1.0), ("nezoter", "Nézőtér", (0, -12, 1.85), 0, 0.56),
        ("paholy", "Páholy", (0, -25.3, 5.95), 0, 4.2)]),
    "szalloda": ("Szállodai lakosztály", "assets/img/szalloda-lounge.jpg", [
        ("bejarat", "Bejárat", (2.4, -3.6, 1.55), 0, 0.0), ("agy", "Ágy", (0.2, -0.9, 1.55), 0, 0.0),
        ("ablak", "Ablak", (2.0, 3.9, 1.55), 180, 0.0)]),
    "rendezveny": ("Rendezvényhelyszín", "assets/img/rendezveny-hero.jpg", [
        ("asztalok", "Vendégtér", (-2.5, -62.0, 1.7), 90, 0.0), ("szinpad", "Színpad előtt", (-32.0, -62.0, 1.7), -90, 0.0),
        ("bejarat", "Kastély előtt", (0.0, -24.0, 1.7), 180, 0.0)]),
    "muzeum": ("Múzeum", "assets/img/muzeum-terem.jpg", [
        ("bejarat", "Bejárat", (0, -10.5, 1.6), 0, 0.0), ("kozep", "Terem közepe", (1.2, 0.5, 1.6), 0, 0.0),
        ("kiallitas", "Időszakos kiállítás", (-1.5, 7.2, 1.6), 0, 0.0)]),
}


def yaw_pitch(node, tgt):
    (_, _, p, rot, _), (_, _, q, _, fz) = node, tgt
    d = (q[0] - p[0], q[1] - p[1], fz + 0.05 - p[2])
    th = math.radians(rot)
    fwd, right = (-math.sin(th), math.cos(th)), (math.cos(th), math.sin(th))
    yaw = math.degrees(math.atan2(d[0] * right[0] + d[1] * right[1], d[0] * fwd[0] + d[1] * fwd[1]))
    pitch = math.degrees(math.atan2(d[2], math.hypot(d[0], d[1])))
    return round(yaw, 2), round(pitch, 2)


tours = {}
for seg, (label, poster, nodes) in NODES.items():
    scenes = []
    for n in nodes:
        hs = []
        for m in nodes:
            if m is n:
                continue
            y, pch = yaw_pitch(n, m)
            hs.append({"yaw": y, "pitch": pch, "scene": m[0], "text": m[1]})
        scenes.append({"id": n[0], "title": n[1], "pano": seg + "-" + n[0], "yaw": 0, "pitch": -4, "hotspots": hs})
    tours[seg] = {"label": label, "poster": poster, "scenes": scenes}


def spot_px(yaw, pitch, yaw0=0.0, out_w=1920, out_h=1200, fov=100, tilt=-6):
    f = (out_w / 2) / math.tan(math.radians(fov) / 2)
    y_ = math.radians(yaw - yaw0)
    p_ = math.radians(pitch)
    X, Y2, Z2 = math.cos(p_) * math.sin(y_), -math.sin(p_), math.cos(p_) * math.cos(y_)
    t = math.radians(tilt)
    Y = Y2 * math.cos(t) + Z2 * math.sin(t)
    Z = -Y2 * math.sin(t) + Z2 * math.cos(t)
    return (out_w / 2 + f * X / Z, out_h / 2 + f * Y / Z)


for seg, nm, img, lab in (("szinhaz", "paholy", "svc-tura.jpg", "VIRTUÁLIS TÚRA · PÁHOLY"),
                          ("szalloda", "bejarat", "szalloda-tura.jpg", "VIRTUÁLIS TÚRA · LAKOSZTÁLY"),
                          ("muzeum", "bejarat", "muzeum-tura.jpg", "VIRTUÁLIS TÚRA · KIÁLLÍTÓTEREM"),
                          ("rendezveny", "bejarat", "rendezveny-tura.jpg", "VIRTUÁLIS TÚRA · RENDEZVÉNYTÉR")):
    key = seg + "-" + nm
    if key not in eqs:
        continue
    sc_ = [x for x in tours[seg]["scenes"] if x["id"] == nm][0]
    spots = []
    for h in sc_["hotspots"]:
        x, y = spot_px(h["yaw"], h["pitch"])
        if 0 < x < 1920 and 0 < y < 1200:
            spots.append((x, y, h["text"]))
    save(tour_ui(eqs[key], lab, spots), img)

CLOUDS = [
    {"id": "muzeum", "label": "Múzeum – kiállítóterem", "poster": "assets/img/muzeum-pontfelho-felul.jpg", "seg": ["muzeum"]},
    {"id": "rendezveny", "label": "Rendezvényhelyszín – tervezett elrendezéssel", "poster": "assets/img/rendezveny-pontfelho-terv.jpg", "seg": ["rendezveny"]},
    {"id": "szinhaz", "label": "Színházterem", "poster": "assets/img/svc-pontfelho.jpg", "seg": ["szinhaz"]},
]
open(os.path.join(P, "tours.js"), "w").write(
    "/* generálva: make_assets.py – a túrák csomópontjai és a pontfelhő-bemutatók listája */\n"
    "window.BD_TOURS = " + json.dumps(tours, ensure_ascii=False, indent=1) + ";\n"
    "window.BD_CLOUD_LIST = " + json.dumps([c for c in CLOUDS if os.path.exists(os.path.join(CLOUD, c["id"] + ".js"))],
                                           ensure_ascii=False, indent=1) + ";\n")

# ------------------------------------------------------------------ VR composite
pl, pr = src("theater/vr_L.png"), src("theater/vr_R.png")
if pl and pr:
    L, R = Image.open(pl).convert("RGB"), Image.open(pr).convert("RGB")
    out = Image.new("RGB", (1920, 1080), (6, 7, 9))
    for i, im in enumerate((L, R)):
        s = 860
        im = im.resize((s, s), Image.LANCZOS)
        # barrel-ish vignette mask
        mask = Image.new("L", (s, s), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle((0, 0, s, s), radius=int(s * 0.36), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(10))
        x = 960 - s - 30 if i == 0 else 960 + 30
        out.paste(im, (x, 110), mask)
    d = ImageDraw.Draw(out, "RGBA")
    d.line((960, 120, 960, 960), fill=(255, 255, 255, 40), width=2)
    d.text((960, 1010), "VR-NÉZET · SZTEREÓ KÉPPÁR · DÍSZLETTERV A SZÍNPADON", font=font(26, True), fill=(220, 220, 220, 230), anchor="mm")
    save(out, "svc-xr.jpg")

# ------------------------------------------------------------------ map / environment tour
p = src("estate/map_top.png")
if p:
    im = Image.open(p).convert("RGB")
    w, h = im.size
    d = ImageDraw.Draw(im, "RGBA")
    # ortho: x in [-130,130] over width 2000 => 7.69 px/m ; centre (0,-30)
    sc_ = w / 260.0
    def px(x, y):
        return (w / 2 + x * sc_, h / 2 - (y + 30) * sc_)
    route = [(0, -155), (0, -125), (0, -100), (0, -40), (0, -22), (0, -16)]
    d.line([px(*q) for q in route], fill=(201, 162, 90, 255), width=10, joint="curve")
    for i, q in enumerate(route[::2] + [route[-1]]):
        x, y = px(*q)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(12, 15, 19, 220), outline=(255, 255, 255, 255), width=4)
        d.text((x, y), str(i + 1), font=font(22, True), fill=(255, 255, 255, 255), anchor="mm")
    x, y = px(0, -8)
    rounded(d, (x + 30, y - 32, x + 300, y + 22), 10, (12, 15, 19, 210))
    d.text((x + 46, y - 5), "Főbejárat · parkoló", font=font(24, True), fill=(255, 255, 255, 255), anchor="lm")
    # mini street-view frame from the drone image
    pe = src("estate/drone_wide.png")
    if pe:
        th = Image.open(pe).convert("RGB").resize((560, 315), Image.LANCZOS)
        im.paste(th, (w - 600, h - 360))
        d.rectangle((w - 600, h - 360, w - 40, h - 45), outline=(255, 255, 255, 255), width=4)
        rounded(d, (w - 590, h - 352, w - 330, h - 312), 8, (12, 15, 19, 200))
        d.text((w - 574, h - 332), "Megközelítés · 2. pont", font=font(20, True), fill=(255, 255, 255, 255), anchor="lm")
    save(im, "svc-kornyezet.jpg")

for rel, name, lab in (("theater/photo_stalls.png", "szinhaz-berepulo.jpg", "VIRTUÁLIS BERÉPÜLŐ VIDEÓ"),
                       ("hotel/photo_lounge.png", "szalloda-berepulo.jpg", "VIRTUÁLIS BERÉPÜLŐ VIDEÓ"),
                       ("museum/photo_diag.png", "muzeum-berepulo.jpg", "VIRTUÁLIS BERÉPÜLŐ VIDEÓ"),
                       ("estate/drone_hotel.png", "szalloda-dronvideo.jpg", "DRÓNVIDEÓ")):
    p = src(rel)
    if p:
        save(play_overlay(Image.open(p), lab), name)
p = src("estate/drone_wide.png")
if p:
    save(Image.open(p), "muzeum-dron.jpg")

# ------------------------------------------------------------------ video
fr = os.path.join(F, "estate", "video_frames")
if os.path.isdir(fr) and len(os.listdir(fr)) >= 140:
    outv = os.path.join(VID, "kastely-berepulo.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(fr, "f%04d.png"),
                    "-vf", "scale=1280:-2,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "21",
                    "-movflags", "+faststart", outv], check=True)
    mid = Image.open(os.path.join(fr, "f0075.png"))
    save(mid, "video-poster.jpg", w=1280)
    save(play_overlay(mid, "VIRTUÁLIS BERÉPÜLŐ VIDEÓ"), "svc-berepulo.jpg")
else:
    missing.append("estate/video_frames")
    p = src("estate/drone_wide.png")
    if p:
        save(Image.open(p), "video-poster.jpg", w=1280)
        save(play_overlay(Image.open(p), "VIRTUÁLIS BERÉPÜLŐ VIDEÓ"), "svc-berepulo.jpg")

# ------------------------------------------------------------------ process images
p = os.path.join(W, "scan_theater", "royal_rgb.png")
if os.path.exists(p):
    e = Image.open(p).convert("RGB").resize((1600, 800), Image.LANCZOS)
    d = ImageDraw.Draw(e, "RGBA")
    rounded(d, (30, 30, 470, 90), 12, (12, 15, 19, 180))
    d.text((50, 60), "SZKENNERÁLLÁS · 360° RÖGZÍTÉS", font=font(24, True), fill=(255, 255, 255, 255), anchor="lm")
    save(e, "proc-rogzites.jpg", w=1600)


def collage(paths, name, cols=2, w=1600, h=1200, gap=10):
    ims = [Image.open(os.path.join(IMG, q)).convert("RGB") for q in paths if os.path.exists(os.path.join(IMG, q))]
    if len(ims) < len(paths):
        missing.append(name)
        return
    rows = math.ceil(len(ims) / cols)
    cw, ch = (w - gap * (cols - 1)) // cols, (h - gap * (rows - 1)) // rows
    out = Image.new("RGB", (w, h), (12, 15, 19))
    for i, im in enumerate(ims):
        r = max(cw / im.width, ch / im.height)
        t = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
        l, tp = (t.width - cw) // 2, (t.height - ch) // 2
        out.paste(t.crop((l, tp, l + cw, tp + ch)), ((i % cols) * (cw + gap), (i // cols) * (ch + gap)))
    save(out, name, w=w)


collage(["svc-pano360.jpg", "svc-mesh.jpg", "svc-3dmodell.jpg", "svc-bim.jpg"], "proc-kimenetek.jpg")
collage(["szinhaz-hero.jpg", "rendezveny-hero.jpg", "szalloda-hero.jpg", "muzeum-hero.jpg"], "proc-felhasznalas.jpg")
p = os.path.join(IMG, "muzeum-pontfelho-felul.jpg")
if os.path.exists(p):
    save(Image.open(p), "svc-repulheto.jpg")

print("MISSING:", sorted(set(missing)))
