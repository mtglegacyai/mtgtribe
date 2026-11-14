# Renders the CoinZoom narrated video frame by frame (1920x1080, 30 fps): MTG's dark explainer stage, CoinZoom's own clip
# in a slim gold-titanium window with a camera that zooms to each tap, rings, taps, chips, step pills, the In this video
# and recap panels, captions with the spoken word lit, emoji pops, privacy blur on the card details, and the signature
# ending (mtg_ending.py, with the CoinZoom logo disc and mtgtribe.com).
#   python3 render.py range <f0> <f1> <outdir>     frames f0..f1-1 as f%05d.jpg
#   python3 render.py test <t1,t2,...> <outdir>    stills at those times as t<time>.png
# Needs MTG_FONTS, MTG_ICONS, MTG_LOGO, MTG_URL in the environment (see build.sh).
import json, math, os, sys, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mtg_ending as ME
from mtg_ending import ease_out, ease_back, smooth, env, paste, paste_c, glow, chip, emo, logo_card, burst
lru = functools.lru_cache(maxsize=None)

TL = json.load(open(os.path.join(HERE, 'timeline.json'))); KC = json.load(open(os.path.join(HERE, 'kitcues.json')))
SRCDIR = os.path.join(HERE, '..', 'src720')
W, H = 1920, 1080
WX, WY, WW, WH, WR = 240, 112, 1440, 810, 28
FONTS = os.environ['MTG_FONTS']
LIME, GOLD, GOLD_HI, GOLD_D = (203, 251, 97), (232, 194, 90), (255, 224, 143), (154, 118, 40)
TEXT, MUTED, PANEL, VIO = (246, 243, 255), (156, 149, 184), (21, 17, 42), (155, 124, 255)
DARK = (20, 17, 11)
KIT = ME.Ending(KC['cues'], 'h', KC.get('nxt'), KC.get('links', True))

@lru
def F(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)
ANTON, MXB, MB, MSB = 'Anton-Regular.ttf', 'Manrope-ExtraBold.ttf', 'Manrope-Bold.ttf', 'Manrope-SemiBold.ttf'

# ------------------------------------------------------------------ static layers
@lru
def stage_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    a = math.radians(160); dx, dy = math.sin(a), -math.cos(a); Ln = abs(W * dx) + abs(H * dy)
    p = np.clip(((x - W / 2) * dx + (y - H / 2) * dy) / Ln + .5, 0, 1)[..., None]
    c0, c1, c2 = np.array([0x13, 0x0c, 0x28], np.float32), np.array([0x0b, 0x09, 0x12], np.float32), np.array([0x08, 0x06, 0x0f], np.float32)
    img = np.where(p < .55, c0 + (c1 - c0) * (p / .55), c1 + (c2 - c1) * ((p - .55) / .45))
    def rad(cx, cy, rx, ry, col, al, stop=.7):
        r = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2); m = (al * np.clip(1 - r / stop, 0, 1))[..., None]
        return m, np.array(col, np.float32)
    for cx, cy, rx, ry, col, al in [(.82 * W, .18 * H, 900, 600, (140, 108, 231), .30), (.10 * W, .90 * H, 800, 600, (232, 194, 90), .14),
                                    (.20 * W, .15 * H, 700, 500, (203, 251, 97), .07)]:
        m, c = rad(cx, cy, rx, ry, col, al); img = img * (1 - m) + c * m
    grid = ((x % 80) < 1) | ((y % 80) < 1)
    r = np.sqrt(((x - W / 2) / 1100) ** 2 + ((y - .45 * H) / 700) ** 2); gm = np.clip((.8 - r) / .5, 0, 1)
    ga = (grid * .6 * .07 * gm)[..., None]; img = img * (1 - ga) + 255 * ga
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')

def rr_mask(w, h, r, k=4):
    m = Image.new('L', (w * k, h * k), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w * k - 1, h * k - 1], r * k, fill=255)
    return m.resize((w, h), Image.LANCZOS)

@lru
def win_mask(): return rr_mask(WW, WH, WR)

@lru
def win_frame():
    """shadow, soft gold glow and the 5 px gold-titanium rim around the window"""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle([WX, WY + 26, WX + WW, WY + WH + 26], WR, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(34)); lay.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [sh]))
    gl = Image.new('L', (W, H), 0); ImageDraw.Draw(gl).rounded_rectangle([WX - 6, WY - 6, WX + WW + 6, WY + WH + 6], WR + 6, fill=70)
    gl = gl.filter(ImageFilter.GaussianBlur(22)); g = Image.new('RGBA', (W, H), GOLD + (0,)); g.putalpha(gl); lay.alpha_composite(g)
    rw, rh = WW + 10, WH + 10
    yy, xx = np.mgrid[0:rh, 0:rw].astype(np.float32); u = (xx / rw * .6 + yy / rh * .4)
    stops = [(0, (255, 241, 191)), (.3, (232, 194, 90)), (.55, (138, 106, 34)), (.8, (232, 194, 90)), (1, (255, 236, 170))]
    col = np.zeros((rh, rw, 3), np.float32)
    for (a0, c0), (a1, c1) in zip(stops, stops[1:]):
        m = (u >= a0) & (u <= a1); f = ((u - a0) / (a1 - a0))[..., None]
        col = np.where(m[..., None], np.array(c0) + (np.array(c1) - np.array(c0)) * f, col)
    rim = Image.fromarray(col.astype(np.uint8)).convert('RGBA'); rim.putalpha(rr_mask(rw, rh, WR + 5))
    lay.alpha_composite(rim, (WX - 5, WY - 5))
    return lay

# ------------------------------------------------------------------ timeline helpers
def src_time(t):
    for a, b, s0, s1 in TL['SRC']:
        if a <= t < b: return s0 + (s1 - s0) * ((t - a) / (b - a) if b > a else 0)
    return TL['SRC'][-1][3]

def cam(t):
    cx, cy, z = TL['CAM0']
    for t0, t1, x1, y1, z1 in TL['CAM']:
        if t <= t0: break
        u = smooth((t - t0) / (t1 - t0)) if t < t1 else 1.0
        cx, cy, z = cx + (x1 - cx) * u, cy + (y1 - cy) * u, z + (z1 - z) * u
    return cx, cy, z

def view(t):
    cx, cy, z = cam(t); w, h = 1280 / z, 720 / z
    x0 = min(max(cx - w / 2, 0), 1280 - w); y0 = min(max(cy - h / 2, 0), 720 - h)
    return x0, y0, w, h, WW / w

def to_win(r, v):
    x0, y0, w, h, sc = v
    return ((r[0] - x0) * sc, (r[1] - y0) * sc, (r[2] - x0) * sc, (r[3] - y0) * sc)

@functools.lru_cache(maxsize=16)
def src_frame(n): return Image.open(os.path.join(SRCDIR, f'f{n:04d}.jpg')).convert('RGB')

@lru
def plate_mask():
    m = np.zeros((720, 1280), np.float32); m[:, :772] = 1; m[:, 772:780] = np.linspace(1, 0, 8)[None, :]
    return m[..., None]
@lru
def plate(): return np.asarray(src_frame(165), np.float32)

def cleaned(n, a):
    """the phone scenes (frames 196 to 454) sit on the same green as frame 165: while zoomed, its side text is taken off"""
    if a <= 0 or not 196 <= n <= 454: return src_frame(n)
    f = np.asarray(src_frame(n), np.float32); m = plate_mask() * a
    return Image.fromarray((f * (1 - m) + plate() * m).astype(np.uint8))

# ------------------------------------------------------------------ drawing helpers
@functools.lru_cache(maxsize=256)
def ring_img(w, h, col, width=5):
    pad = 26; im = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    k = 3; big = Image.new('RGBA', ((w + 2 * pad) * k, (h + 2 * pad) * k), (0, 0, 0, 0))
    ImageDraw.Draw(big).rounded_rectangle([pad * k, pad * k, (pad + w) * k, (pad + h) * k], 12 * k, outline=col + (255,), width=width * k)
    line = big.resize(im.size, Image.LANCZOS)
    g = Image.new('RGBA', im.size, col + (0,)); g.putalpha(line.getchannel('A').filter(ImageFilter.GaussianBlur(9)).point(lambda a: int(a * .8)))
    im.alpha_composite(g); im.alpha_composite(line)
    return im, pad

def draw_ring(lay, r, a, s, col):
    x0, y0, x1, y1 = r; p = 8
    w, h = int(x1 - x0 + 2 * p), int(y1 - y0 + 2 * p)
    im, pad = ring_img(max(8, w), max(8, h), col)
    paste_c(lay, im, (x0 + x1) / 2, (y0 + y1) / 2, a, s)

def draw_tap(lay, cxy, t, tt):
    cx, cy = cxy; d = ImageDraw.Draw(lay)
    if tt - .35 <= t < tt + .08:
        a = ease_out((t - tt + .35) / .2); r = 15
        tmp = Image.new('RGBA', lay.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(tmp)
        dd.ellipse([cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7], fill=LIME + (int(90 * a),))
        dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, int(235 * a)), outline=LIME + (int(255 * a),), width=4)
        lay.alpha_composite(tmp)
    u = (t - tt) / .55
    if 0 <= u <= 1:
        r = 18 + 62 * ease_out(u); al = int(255 * (1 - u))
        tmp = Image.new('RGBA', lay.size, (0, 0, 0, 0))
        ImageDraw.Draw(tmp).ellipse([cx - r, cy - r, cx + r, cy + r], outline=LIME + (al,), width=6); lay.alpha_composite(tmp)

@lru
def txt(s, font, size, col=TEXT, track=0.0):
    f = F(font, size)
    if not track:
        bb = f.getbbox(s); im = Image.new('RGBA', (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), s, font=f, fill=col); return im
    sp = size * track; wsum = sum(f.getlength(c) for c in s) + sp * (len(s) - 1)
    asc, desc = f.getmetrics(); im = Image.new('RGBA', (int(wsum) + 8, asc + desc + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 4
    for c in s: d.text((x, 4), c, font=f, fill=col); x += f.getlength(c) + sp
    return im.crop(im.getbbox())

def shadowed(im, r=8, k=.85):
    pad = r * 3; out = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new('L', out.size, 0); a.paste(im.getchannel('A'), (pad, pad + 3))
    a = a.filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * k))
    out.alpha_composite(Image.merge('RGBA', [Image.new('L', out.size, 8)] * 3 + [a])); out.alpha_composite(im, (pad, pad))
    return out

@lru
def glass(w, h, col=LIME, r=30, fill_a=.94):
    pad = 40; im = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    g = Image.new('L', im.size, 0); ImageDraw.Draw(g).rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=80)
    gg = Image.new('RGBA', im.size, col + (0,)); gg.putalpha(g.filter(ImageFilter.GaussianBlur(18))); im.alpha_composite(gg)
    body = Image.new('RGBA', (w, h), PANEL + (int(255 * fill_a),))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); u = np.clip((xx / w * .45 + yy / h * .55), 0, 1)
    sheen = (np.clip(1 - u / .34, 0, 1) * .13 + np.clip((u - .7) / .3, 0, 1) * .07)[..., None]
    arr = np.array(body, np.float32); arr[..., :3] = arr[..., :3] * (1 - sheen) + np.array(col, np.float32) * sheen
    body = Image.fromarray(arr.astype(np.uint8)); m = rr_mask(w, h, r); body.putalpha(Image.fromarray((np.array(m, np.float32) * fill_a).astype(np.uint8)))
    im.alpha_composite(body, (pad, pad))
    ImageDraw.Draw(im).rounded_rectangle([pad, pad, pad + w - 1, pad + h - 1], r, outline=col + (220,), width=3)
    return im

@lru
def num_circle(n, d=60, done=False):
    k = 3; im = Image.new('RGBA', (d * k, d * k), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    if done:
        dr.ellipse([0, 0, d * k - 1, d * k - 1], fill=LIME + (255,))
        dr.line([(d * k * .28, d * k * .52), (d * k * .44, d * k * .68), (d * k * .74, d * k * .34)], fill=DARK + (255,), width=int(d * k * .1), joint='curve')
        im = im.resize((d, d), Image.LANCZOS)
    else:
        dr.ellipse([0, 0, d * k - 1, d * k - 1], fill=GOLD + (255,), outline=GOLD_HI + (255,), width=k * 2)
        im = im.resize((d, d), Image.LANCZOS); s = txt(str(n), MXB, int(d * .52), DARK)
        im.alpha_composite(s, ((d - s.width) // 2, (d - s.height) // 2))
    return im

@lru
def label_row(segs, size=46):
    """a row of text where the on-screen label sits in a lime-outlined highlight"""
    parts = []; x = 0; h = 0
    for s, hl in segs:
        im = txt(s, MXB, size, TEXT)
        if hl:
            pw, ph = im.width + 26, im.height + 14
            box = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
            ImageDraw.Draw(box).rounded_rectangle([0, 0, pw - 1, ph - 1], 12, fill=(203, 251, 97, 34), outline=LIME + (255,), width=3)
            box.alpha_composite(im, (13, 7)); im = box
        parts.append((x, im)); x += im.width + (6 if s.endswith(' ') or hl else 0); h = max(h, im.height)
    out = Image.new('RGBA', (x, h), (0, 0, 0, 0))
    for px, im in parts: out.alpha_composite(im, (px, (h - im.height) // 2))
    return out

@lru
def two_tone(a, b, font, size, ca=TEXT, cb=LIME):
    ia, ib = txt(a, font, size, ca), txt(b, font, size, cb)
    out = Image.new('RGBA', (ia.width + ib.width - 4, max(ia.height, ib.height)), (0, 0, 0, 0))
    out.alpha_composite(ia, (0, out.height - ia.height)); out.alpha_composite(ib, (ia.width - 4, out.height - ib.height))
    return out

@lru
def mask_pill(w, h, label):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=(236, 233, 245, 250), outline=(186, 180, 205, 255), width=2)
    e = emo('🔒', int(h * .52)); s = txt(label, MB, max(12, int(h * .44)), (62, 56, 84))
    tw = e.width + 8 + s.width; x = (w - tw) // 2
    im.alpha_composite(e, (x, (h - e.height) // 2)); im.alpha_composite(s, (x + e.width + 8, (h - s.height) // 2))
    return im

# ------------------------------------------------------------------ the window (CoinZoom's clip)
def window_layer(t):
    st = src_time(t); n = min(max(int(round(st * 30)) + 1, 1), 512)
    v = view(t); x0, y0, w, h, sc = v
    z = 1280 / w; ca = min(1.0, max(0.0, (z - 1.03) / .45))
    content = cleaned(n, ca).resize((WW, WH), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert('RGBA')
    # privacy: blur the card number, name and expiry in every frame the details screen can show, labelled pills on top
    m0, m1 = TL['MASK_FRAMES']
    if m0 <= n <= m1:
        la = TL['LABEL_ALPHA'].get(str(n), 1.0 if 421 <= n <= 455 else 0.0)
        for rect, label in TL['MASKS']:
            X0, Y0, X1, Y1 = to_win((rect[0] - 3, rect[1] - 3, rect[2] + 3, rect[3] + 3), v)
            box = tuple(int(round(q)) for q in (max(0, X0), max(0, Y0), min(WW, X1), min(WH, Y1)))
            if box[2] - box[0] < 4 or box[3] - box[1] < 4: continue
            reg = content.crop(box).filter(ImageFilter.GaussianBlur(max(6, (box[3] - box[1]) * .35)))
            reg = Image.blend(reg, Image.new('RGBA', reg.size, (240, 238, 246, 255)), .45); content.paste(reg, box[:2])
            if la > 0:
                ph = int((box[3] - box[1]) * .86); pw = int(min(box[2] - box[0] - 6, max(ph * 5.2, (box[2] - box[0]) * .8)))
                paste_c(content, mask_pill(pw, ph, label), (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, la)
    # the In this video panel dims the clip behind it
    P = TL['PLAN']; dpl, _ = env(t, P['t0'], P['t1'], .35, .3)
    if dpl > 0:
        bl = content.filter(ImageFilter.GaussianBlur(10 * dpl))
        content = Image.blend(bl, Image.new('RGBA', content.size, (8, 6, 16, 255)), .62 * dpl)
    # rings, taps, chips
    for key, t0, t1, col in TL['RINGS']:
        a, p = env(t, t0, t1, .22, .2)
        if a > 0: draw_ring(content, to_win(TL['B'][key], v), a, (1.18 - .18 * p) * ME.pulse(t, t0 + .3, .05), LIME if col == 'lime' else GOLD)
    for key, tt in TL['TAPS']:
        if tt - .4 <= t <= tt + .6:
            X0, Y0, X1, Y1 = to_win(TL['B'][key], v); draw_tap(content, ((X0 + X1) / 2, (Y0 + Y1) / 2), t, tt)
    for e, label, t0, t1 in TL['CHIPS']:
        a, p = env(t, t0, t1, .25, .25)
        if a > 0:
            c = chip(label, None, LIME, 30, e); paste_c(content, c, WW - 36 - c.width / 2, WH - 64, a, .85 + .15 * p)
    return content

# ------------------------------------------------------------------ panels on the stage
def plan_panel(ov, t):
    P = TL['PLAN']; a0, _ = env(t, P['t0'], P['t1'], .35, .3)
    if a0 <= 0: return
    a1, p1 = env(t, P['t0'] + .1, P['t1'], .4, .3)
    paste_c(ov, glass(1060, 620), 960, 515, a0 * a1, .94 + .06 * p1)
    paste_c(ov, two_tone('IN THIS ', 'VIDEO', ANTON, 84), 960, 282, a0 * a1, 1.1 - .1 * p1)
    a2, _ = env(t, P['sub'], P['t1'], .35, .3)
    paste_c(ov, txt('Find your virtual CoinZoom Visa debit card', MB, 34, (201, 195, 224)), 960, 358, a0 * a2)
    rows = [(('Tap ', False), ('Spend', True)), (('Tap ', False), ('Reveal', True)), (('Double tap', True), (' to confirm', False))]
    for i, (tt, segs) in enumerate(zip(P['rows'], rows)):
        a, p = env(t, tt - .08, P['t1'], .3, .3)
        if a <= 0: continue
        y = 470 + i * 102; x = 560 + (1 - p) * -40
        paste_c(ov, num_circle(i + 1, 62), x, y, a0 * a, .7 + .3 * p)
        r = label_row(segs); paste(ov, r, x + 52, y - r.height / 2, a0 * a)
    ap, pp = env(t, P['pause'], P['t1'], .3, .3)
    if ap > 0: paste_c(ov, chip('Pause any step and follow along', None, LIME, 30, '⏸️'), 960, 780, a0 * ap, .85 + .15 * pp)

def recap_panel(ov, t):
    R = TL['RECAP']; a0, _ = env(t, R['t0'], R['t1'], .35, .3)
    if a0 <= 0: return
    a1, p1 = env(t, R['t0'] + .05, R['t1'], .4, .3)
    paste_c(ov, two_tone("LET'S ", 'RECAP', ANTON, 104), 960, 250, a0 * a1, 1.12 - .12 * p1)
    cards = [('💳', 'Tap Spend', 'Your card screen opens'), ('👀', 'Tap Reveal', 'With Virtual Card selected'),
             ('👆', 'Double tap', 'Confirm, and your details appear')]
    for i, (e, ttl, sub) in enumerate(cards):
        cx, cy = 410 + i * 550, 575; ak, pk = env(t, R['t0'] + .15 + .12 * i, R['t1'], .3, .3)
        if ak <= 0: continue
        done = t >= R['ticks'][i]; pd = ease_back((t - R['ticks'][i]) / .35) if done else 0
        paste_c(ov, glass(470, 320, LIME if done else VIO, 30, .92), cx, cy, a0 * ak, (.9 + .1 * pk) * ME.pulse(t, R['ticks'][i], .05))
        paste_c(ov, num_circle(i + 1, 64, done), cx - 235 + 52, cy - 160 + 52, a0 * ak, .7 + .3 * (pd if done else 1))
        paste_c(ov, emo(e, 72), cx, cy - 62, a0 * ak)
        paste_c(ov, txt(ttl, MXB, 46, LIME if done else TEXT), cx, cy + 30, a0 * ak)
        paste_c(ov, txt(sub, MSB, 27, (201, 195, 224)), cx, cy + 88, a0 * ak)

def turn_panel(ov, t):
    U = TL['TURN']; a0, _ = env(t, U['t0'], U['t1'], .3, .3)
    if a0 <= 0: return
    a1, p1 = env(t, U['t0'] + .05, U['t1'], .35, .3)
    paste_c(ov, two_tone("NOW IT'S ", 'YOUR TURN', ANTON, 132), 960, 300, a0 * a1, 1.15 - .15 * p1)
    paste_c(ov, logo_card(230), 960, 560, a0 * a1, .8 + .2 * p1)
    a2, p2 = env(t, U['turn'] - .1, U['t1'], .3, .3)
    paste_c(ov, chip('Open your CoinZoom app: Spend, Reveal, confirm', None, LIME, 36, '📱'), 960, 800, a0 * a2, .85 + .15 * p2)
    burst(ov, 960, 800, t, U['turn'], [LIME, ME.GOLD, ME.WHITE], 14, 130, .7, 440, 50)

def top_bar(ov, t):
    paste_c(ov, logo_card(58), 66, 56)
    paste(ov, txt('MTG', MXB, 30, TEXT), 108, 30); paste(ov, txt('YOUR DIGITAL ARCHITECT', MB, 14, GOLD, .14), 110, 68)
    s = txt('COINZOOM · VIRTUAL CARD', MXB, 19, DARK, .14); pw = s.width + 48
    pill = Image.new('RGBA', (pw, 48), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle([0, 0, pw - 1, 47], 24, fill=LIME + (255,))
    pill.alpha_composite(s, (24, (48 - s.height) // 2)); paste(ov, pill, W - 40 - pw, 32)
    for n, segs, t0, t1 in TL['STEPS']:
        a, p = env(t, t0, t1, .3, .25)
        if a > 0: paste_c(ov, step_pill(n, tuple((x, bool(hl)) for x, hl in segs)), 960, 56, a, .85 + .15 * p)

@lru
def step_pill(n, segs):
    parts = [txt(x.strip(), MXB, 32, LIME if hl else TEXT) for x, hl in segs]; sp = F(MXB, 32).getlength(' ')
    h = 62; tw = sum(p.width for p in parts) + sp * (len(parts) - 1); w = int(12 + 42 + 14 + tw + 26)
    im = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    g = Image.new('L', im.size, 0); ImageDraw.Draw(g).rounded_rectangle([30, 30, 30 + w, 30 + h], h // 2, fill=70)
    gg = Image.new('RGBA', im.size, LIME + (0,)); gg.putalpha(g.filter(ImageFilter.GaussianBlur(13))); im.alpha_composite(gg)
    ImageDraw.Draw(im).rounded_rectangle([30, 30, 30 + w, 30 + h], h // 2, fill=PANEL + (240,), outline=LIME + (220,), width=3)
    c = Image.new('RGBA', (42, 42), (0, 0, 0, 0)); ImageDraw.Draw(c).ellipse([0, 0, 41, 41], fill=LIME + (255,))
    d = txt(str(n), MXB, 24, DARK); c.alpha_composite(d, ((42 - d.width) // 2, (42 - d.height) // 2))
    im.alpha_composite(c, (30 + 12, 30 + 10)); x = 30 + 12 + 42 + 14; d = ImageDraw.Draw(im); f = F(MXB, 32)
    for (s_, hl), p in zip(segs, parts):                   # one shared baseline
        d.text((x, 30 + h / 2 + 11), s_.strip(), font=f, fill=LIME if hl else TEXT, anchor='ls'); x += p.width + sp
    return im

# ------------------------------------------------------------------ captions and emoji
CAPF, CAPS, CAPW = MB, 40, 1560
@lru
def caption_img(ci, lit):
    c = TL['CAPS'][ci]; f = F(CAPF, CAPS); sp = f.getlength(' ')
    words = [w['w'] for w in c['words']]; wl = [f.getlength(w) for w in words]
    width = lambda a, b: sum(wl[a:b]) + sp * (b - a - 1)
    if width(0, len(words)) <= CAPW: lines = [list(range(len(words)))]
    else:                                                  # two lines, as even as possible
        k = min(range(1, len(words)), key=lambda k: max(width(0, k), width(k, len(words))))
        lines = [list(range(0, k)), list(range(k, len(words)))]
    lh = 56; im = Image.new('RGBA', (W, lh * len(lines) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ends = []
    for li, idx in enumerate(lines):
        tw = sum(f.getlength(words[i]) for i in idx) + sp * (len(idx) - 1); x = (W - tw) / 2; y = 10 + li * lh
        for i in idx:
            d.text((x, y), words[i], font=f, fill=LIME if i == lit else TEXT); x += f.getlength(words[i]) + sp
        ends.append((x - sp, y + lh / 2))
    return shadowed(im, 7, .9), ends, len(lines)

def captions(ov, t):
    last = None
    for ci, c in enumerate(TL['CAPS']):
        if not (c['t0'] <= t <= c['t1']): continue
        a = min(ease_out((t - c['t0']) / .12), ease_out((c['t1'] - t) / .15))
        lit = -1
        for i, w in enumerate(c['words']):
            if w['a'] - .03 <= t: lit = i
        if lit >= 0 and t > c['words'][lit]['b'] + .25: lit = -1
        im, ends, nl = caption_img(ci, lit); pad = 21
        y0 = 1000 - (nl * 56) / 2 - 10 - pad
        paste(ov, im, -pad, y0, a); last = (ends[-1][0], y0 + pad + ends[-1][1])
    return last

def emojis(ov, t, anchor):
    for te, ch in TL['EMOS']:
        u = t - te
        if 0 <= u <= 2.0:
            a = min(1.0, ease_out(u / .2), ease_out((2.0 - u) / .3)); s = .4 + .6 * ease_back(u / .35)
            x, y = (anchor[0] + 62, anchor[1] - 6) if anchor else (1700, 1000)
            paste_c(ov, emo(ch, 84), min(x, W - 70), y - 6 * math.sin(u * 5), a, s)

# ------------------------------------------------------------------ one frame
def frame(t):
    im = stage_bg().copy()
    Wn = TL['WIN']; wa = 1.0 if t < Wn['out0'] else max(0.0, 1 - ease_out((t - Wn['out0']) / (Wn['out1'] - Wn['out0'])))
    if wa > 0:
        fr = win_frame()
        if wa < 1: fr = fr.copy(); fr.putalpha(fr.getchannel('A').point(lambda v: int(v * wa)))
        im.alpha_composite(fr)
        c = window_layer(t); m = win_mask()
        if wa < 1: m = m.point(lambda v: int(v * wa))
        c.putalpha(m); im.alpha_composite(c, (WX, WY))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    plan_panel(ov, t); recap_panel(ov, t); turn_panel(ov, t)
    top_bar(ov, t)
    anchor = captions(ov, t) if t < TL['END_CARD'] else None
    emojis(ov, t, anchor)
    im.alpha_composite(ov)
    if t >= KIT.start - .01: im.alpha_composite(KIT.overlay(t))
    return im.convert('RGB')

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'test':
        out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        for s in sys.argv[2].split(','):
            frame(float(s)).save(os.path.join(out, f't{float(s):07.2f}.png'))
    else:
        f0, f1, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; os.makedirs(out, exist_ok=True)
        for f in range(f0, f1):
            frame(f / TL['fps']).save(os.path.join(out, f'f{f:05d}.jpg'), quality=93)
            if f % 150 == 0: print('frame', f, flush=True)
