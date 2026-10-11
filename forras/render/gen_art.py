# Generative artworks (own work) for the museum scene: colour-field, landscape, geometric.
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
rng = np.random.default_rng(7); random.seed(7)
def noise2(h, w, scale, oct=5):
    out = np.zeros((h, w))
    amp = 1
    for o in range(oct):
        s = max(2, int(scale * 2**o))
        n = rng.random((s, s))
        im = Image.fromarray((n*255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(im)/255 * amp
        amp *= 0.5
    return out/out.max()
def canvas_tex(a):
    h, w, _ = a.shape
    g = noise2(h, w, 60, 2)*0.06 - 0.03
    return np.clip(a + g[..., None], 0, 1)
def colorfield(w, h, cols):
    a = np.zeros((h, w, 3)); a[:] = cols[0]
    n = noise2(h, w, 6)
    bands = [(0.07, 0.42), (0.5, 0.93)] if len(cols) == 3 else [(0.08, 0.6), (0.66, 0.92)]
    for (y0, y1), c in zip(bands, cols[1:]):
        m = np.zeros((h, w)); m[int(y0*h):int(y1*h), int(0.08*w):int(0.92*w)] = 1
        m = np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(w*0.012)))/255
        m *= 0.85 + 0.15*n
        a = a*(1-m[..., None]) + np.array(c)*m[..., None]
    return canvas_tex(a)
def landscape(w, h, sky_top, sky_bot, hills, sun=None):
    y = np.linspace(0, 1, h)[:, None, None]
    a = np.array(sky_top)*(1-y) + np.array(sky_bot)*y
    a = np.repeat(a, w, 1)
    if sun:
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.sqrt((xx-sun[0]*w)**2 + (yy-sun[1]*h)**2)/w
        a += (np.exp(-d*14)*0.6)[..., None]*np.array([1, 0.8, 0.5])
    xs = np.linspace(0, 1, w)
    for i, (base, amp, col) in enumerate(hills):
        prof = base + amp*np.interp(xs, np.linspace(0,1,9), rng.random(9))
        prof = np.convolve(np.pad(prof, 20, mode='edge'), np.ones(41)/41, mode='valid')
        yy = np.arange(h)[:, None]/h
        m = (yy > prof[None, :]).astype(float)
        a = a*(1-m[..., None]) + np.array(col)*m[..., None]
    a = np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)))/255
    return canvas_tex(a)
def geometric(w, h, bg, shapes):
    im = Image.new('RGB', (w, h), tuple(int(c*255) for c in bg)); d = ImageDraw.Draw(im)
    for kind, box, col in shapes:
        b = [box[0]*w, box[1]*h, box[2]*w, box[3]*h]; c = tuple(int(v*255) for v in col)
        if kind == 'c': d.ellipse(b, fill=c)
        elif kind == 'r': d.rectangle(b, fill=c)
        elif kind == 't': d.polygon([(b[0], b[3]), ((b[0]+b[2])/2, b[1]), (b[2], b[3])], fill=c)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(1)))/255
    return canvas_tex(a)
works = [
 ("cf1", colorfield(800, 1000, [(0.55,0.12,0.08),(0.85,0.45,0.15),(0.25,0.05,0.06)])),
 ("cf2", colorfield(800, 1000, [(0.08,0.12,0.22),(0.18,0.32,0.45),(0.75,0.68,0.5)])),
 ("cf3", colorfield(900, 700, [(0.85,0.8,0.68),(0.62,0.18,0.12)])),
 ("ls1", landscape(1200, 800, (0.95,0.75,0.55),(0.98,0.88,0.7), [(0.55,0.15,(0.45,0.38,0.42)),(0.65,0.12,(0.3,0.26,0.3)),(0.78,0.1,(0.16,0.14,0.18))], sun=(0.7,0.42))),
 ("ls2", landscape(1200, 800, (0.35,0.5,0.68),(0.85,0.82,0.75), [(0.5,0.2,(0.55,0.6,0.62)),(0.66,0.12,(0.3,0.42,0.4)),(0.8,0.08,(0.15,0.25,0.2))])),
 ("ls3", landscape(1000, 1300, (0.12,0.1,0.2),(0.7,0.35,0.3), [(0.6,0.12,(0.2,0.12,0.18)),(0.75,0.1,(0.08,0.06,0.1))], sun=(0.35,0.55))),
 ("g1", geometric(900, 900, (0.92,0.88,0.8), [('c',(0.15,0.12,0.6,0.57),(0.85,0.25,0.15)),('r',(0.45,0.45,0.88,0.88),(0.12,0.2,0.45)),('t',(0.1,0.55,0.5,0.92),(0.95,0.72,0.2))])),
 ("g2", geometric(800, 1100, (0.1,0.1,0.12), [('r',(0.12,0.1,0.88,0.3),(0.85,0.82,0.75)),('c',(0.25,0.38,0.75,0.75),(0.75,0.2,0.18)),('r',(0.12,0.8,0.88,0.9),(0.9,0.68,0.25))])),
 ("g3", geometric(1200, 700, (0.86,0.84,0.78), [('r',(0.05,0.1,0.35,0.9),(0.15,0.3,0.35)),('r',(0.4,0.1,0.65,0.9),(0.8,0.55,0.25)),('r',(0.7,0.1,0.95,0.9),(0.6,0.2,0.18))])),
]
for name, a in works:
    Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).save(f"tex/art/{name}.jpg", quality=92)
ims=[Image.open(f"tex/art/{n}.jpg").resize((200,200)) for n,_ in works]
c=Image.new('RGB',(200*len(ims),200)); [c.paste(im,(i*200,0)) for i,im in enumerate(ims)]; c.save('out/art_contact.jpg')
