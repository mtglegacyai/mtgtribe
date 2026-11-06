# JetUP + TAG Markets training, engine v2: the ALTRUVA animation system carried forward and upgraded.
# Word-timed pop-ins, spotlight + pointer taps, panel slide-ins, active-word captions, emoji pops,
# animated recap / save-share-comment / links / kinetic slogans / signature outro / end card, sound effects.
# No HeyGen calls: works on the approved voice (voice_tut.wav + voice_tut_words.json).
import os, sys, io, json, math, re, functools, subprocess
import numpy as np, cv2, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/jv')
import render_tut as R
import compose as C
from gfx import F
from scenes import STATES, P, RING, PURPLE, PINK, LIME, ORANGE, TEAL, BLUE

W, H, FPS, COVER, END = R.W, R.H, R.FPS, R.COVER, R.END
WHITE, GREY, ICE = (247, 246, 252), (170, 165, 190), (226, 220, 248)
GOLD, GOLD_L, GOLD_D = (232, 194, 90), (250, 228, 150), (196, 142, 44)
DARK = (15, 12, 25)
CX = W // 2
ICONS = '/home/claude/assets/package/icons/'
GV = '/home/claude/assets/fonts/GreatVibes-Regular.ttf'
EMOJI_FONT = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
lru = functools.lru_cache(maxsize=None)

# ------------------------------------------------------------------ easing (from the ALTRUVA engine)
def ease_out(x): x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def ease_back(x):
    x = min(max(x, 0.0), 1.0); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def smooth(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def env(t, t0, t1, fin=0.3, fout=0.25):
    if t < t0 or t > t1: return 0.0, 0.0
    a_in = ease_out((t - t0) / fin) if fin > 0 else 1
    a_out = ease_out((t1 - t) / fout) if fout > 0 else 1
    return min(a_in, a_out), ease_back((t - t0) / (fin * 1.4)) if fin > 0 else 1
def pulse(t, t0, amp=0.08, dur=0.35): return 1 + amp * max(0.0, 1 - (t - t0) / dur) if t >= t0 else 1

# ------------------------------------------------------------------ drawing helpers
def fnt(kind, size): return ImageFont.truetype(GV, size) if kind == 'sig' else F(kind, size)
fnt = lru(fnt)

@lru
def icon(name, size, color=WHITE, sw=2.0, fill=None):
    s = open(ICONS + name + '.svg').read().replace('currentColor', '#%02x%02x%02x' % color).replace('stroke-width="2"', f'stroke-width="{sw}"')
    if fill is not None: s = s.replace('fill="none"', 'fill="#%02x%02x%02x"' % fill)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=size, output_height=size))).convert('RGBA')

@lru
def emo(ch, size):
    f = ImageFont.truetype(EMOJI_FONT, 109)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)

@lru
def T(txt, size, col=WHITE, kind='b'):
    f = fnt(kind, size); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), txt, font=f, fill=col)
    return im

@lru
def G(txt, size, c1, c2, kind='b', glow_col=None, gr=14, gk=0.55):
    m = T(txt, size, (255, 255, 255), kind); w, h = m.size
    g = np.zeros((h, w, 3), np.float32)
    for i in range(3): g[:, :, i] = np.linspace(c1[i], c2[i], w)[None, :]
    out = Image.fromarray(g.astype(np.uint8)).convert('RGBA'); out.putalpha(m.getchannel('A'))
    return glow(out, gr, glow_col, gk) if glow_col else out

def glow(im, r=14, col=None, k=0.6):
    pad = r * 3; big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    solid = Image.new('RGBA', im.size, (col or (255, 255, 255)) + (255,)); solid.putalpha(im.getchannel('A'))
    big.paste(solid, (pad, pad), solid); g = big.filter(ImageFilter.GaussianBlur(r))
    ga = np.array(g.getchannel('A'), np.float32) * k; g.putalpha(Image.fromarray(np.clip(ga, 0, 255).astype(np.uint8)))
    o = Image.new('RGBA', big.size, (0, 0, 0, 0)); o.paste(im, (pad, pad), im); g.alpha_composite(o)
    return g

def rrect(size, r, fill, outline=None, width=0):
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill, outline=outline, width=width)
    return im

@lru
def ring_icon(name, d, col, emoji_ch=None):
    im = Image.new('RGBA', (d, d), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    dr.ellipse([0, 0, d - 1, d - 1], fill=(26, 20, 44, 255), outline=col + (255,), width=max(3, d // 28))
    ic = icon(name, int(d * 0.5), col, 2.2); im.alpha_composite(ic, ((d - ic.width) // 2, (d - ic.height) // 2))
    g = glow(im, max(8, d // 10), col, 0.55)
    if emoji_ch:
        e = emo(emoji_ch, int(d * 0.36)); g.alpha_composite(e, (g.width - e.width - int(d * 0.12), int(d * 0.12)))
    return g

@lru
def chip(txt, ic=None, col=LIME, size=32, emoji_ch=None, fill=(26, 20, 44, 240), tcol=WHITE):
    f = fnt('sb', size); tw = int(f.getlength(txt)); iw = int(size * 1.25) if (ic or emoji_ch) else 0
    h = int(size * 1.9); w = tw + 56 + (iw + 14 if iw else 0)
    im = rrect((w, h), h // 2, fill, outline=col + (255,), width=3); d = ImageDraw.Draw(im); x = 28
    if emoji_ch: e = emo(emoji_ch, iw); im.alpha_composite(e, (x, (h - e.height) // 2)); x += iw + 14
    elif ic: e = icon(ic, iw, col, 2.3); im.alpha_composite(e, (x, (h - iw) // 2)); x += iw + 14
    d.text((x, h / 2), txt, font=f, fill=tcol, anchor='lm')
    return im

@lru
def url_pill(url, size, bg=LIME, fg=DARK, glow_col=LIME):
    f = fnt('b', size); tw = int(f.getlength(url)); h = int(size * 1.55); w = tw + int(size * 1.1)
    im = rrect((w, h), h // 2, bg + (255,)); ImageDraw.Draw(im).text((w / 2, h / 2), url, font=f, fill=fg, anchor='mm')
    return glow(im, 22, glow_col, 0.6)

PLAT = {'tiktok': ('TikTok', '@joinmtgtribe', '🎵', (37, 244, 238)), 'youtube': ('YouTube', '@mtgtribe', '▶️', (255, 48, 48)),
        'whatsapp': ('WhatsApp', 'mtgtribe.com/group', '💬', (37, 211, 102)), 'telegram': ('Telegram', '@mtgtribe', '✈️', (34, 158, 217)),
        'facebook': ('Facebook', 'facebook.com/mtgtribe', '📘', (24, 119, 242))}

@lru
def plat_badge(key, w=760, h=84):
    name, handle, e, col = PLAT[key]
    im = rrect((w, h), h // 2, (24, 20, 38, 245), outline=col + (255,), width=3); d = ImageDraw.Draw(im)
    d.ellipse([10, 10, h - 10, h - 10], fill=tuple(int(c * 0.35) for c in col) + (255,), outline=col + (255,), width=3)
    em = emo(e, int(h * 0.46)); im.alpha_composite(em, (h // 2 - em.width // 2, h // 2 - em.height // 2))
    d.text((h + 14, h / 2), name, font=fnt('b', 32), fill=WHITE, anchor='lm')
    d.text((h + 14 + fnt('b', 32).getlength(name) + 18, h / 2 + 1), handle, font=fnt('m', 30), fill=col if key != 'tiktok' else ICE, anchor='lm')
    return im

def paste(ov, im, x, y, a=1.0):
    if a <= 0.003: return
    if a < 1:
        im = im.copy(); im.putalpha(Image.fromarray((np.array(im.getchannel('A'), np.float32) * a).astype(np.uint8)))
    ov.alpha_composite(im, (int(round(x)), int(round(y)))) if 0 <= x and 0 <= y and x + im.width <= ov.width and y + im.height <= ov.height else ov.paste(im, (int(round(x)), int(round(y))), im)

def paste_c(ov, im, cx, cy, a=1.0, s=1.0):
    if a <= 0.003: return
    if abs(s - 1) > 1e-3 and s > 0: im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
    paste(ov, im, cx - im.width / 2, cy - im.height / 2, a)

def burst(ov, cx, cy, t, t0, cols, n=12, r1=160, dur=0.65, rx=50, ry=None):
    """particles fly out from an ellipse (rx, ry) around the element, so they never cross its text"""
    u = (t - t0) / dur
    if not 0 <= u <= 1: return
    ry = rx if ry is None else ry; gx = int(rx + r1 + 40); gy = int(ry + r1 * 0.6 + 40)
    lay = Image.new('RGBA', (2 * gx, 2 * gy), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(n):
        ang = 2 * math.pi * k / n + 0.3; g = r1 * ease_out(u); rad = 9 * (1 - u) + 2
        x, y = gx + (rx + g) * math.cos(ang), gy + (ry + g * 0.6) * math.sin(ang); col = cols[k % len(cols)]
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col + (int(255 * (1 - u)),))
    paste(ov, lay, cx - gx, cy - gy)

def comp(dst, rgba, x, y, a=1.0):
    """composite RGBA numpy onto RGB numpy (float or uint8) in place"""
    h, w = rgba.shape[:2]; X0, Y0, X1, Y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if X1 <= X0 or Y1 <= Y0 or a <= 0.003: return
    s = rgba[Y0 - y:Y1 - y, X0 - x:X1 - x].astype(np.float32); al = s[..., 3:4] / 255.0 * a
    dst[Y0:Y1, X0:X1] = dst[Y0:Y1, X0:X1] * (1 - al) + s[..., :3] * al

# ------------------------------------------------------------------ words and timeline
J = json.load(open('voice_tut_words.json'))
WD = [dict(w, start=w['start'] + COVER, end=w['end'] + COVER) for w in J['words']]
SPEECH_END = COVER + J['duration']; TOTAL = SPEECH_END + END
TOK = []
for w in WD:
    for p in C.norm(w['word']).split(): TOK.append((p, w['start'], w['end']))
def _find(phrase, after):
    q = C.norm(phrase).split()
    for k in range(len(TOK) - len(q) + 1):
        if TOK[k][1] >= after - 1e-6 and [x[0] for x in TOK[k:k + len(q)]] == q: return k, k + len(q) - 1
    raise KeyError(phrase)
def S(phrase, after=0.0): return TOK[_find(phrase, after)[0]][1]
def E(phrase, after=0.0): return TOK[_find(phrase, after)[1]][2]

TIMES, _caps, _se, _tot = R.build()
IDX_RECAP = next(i for i, s in enumerate(STATES) if s['trig'] == 'and thats it')
T_RECAP = TIMES[IDX_RECAP]
T_ENG = S('save this video', T_RECAP) - 0.25
T_WE = S('we learn best', T_RECAP) - 0.25
T_CMT = S('now comment done', T_RECAP) - 0.25
T_LINKS = S('everything i showed you', T_RECAP) - 0.25
T_BIO = S('check my bio', T_RECAP)
T_GROUP = S('and if you believe in learning', T_RECAP) - 0.2
T_SLOG = S('it pays to pay attention', T_RECAP) - 0.25
T_OUT = S('quick reminder', T_RECAP) - 0.25
TH = S('thank you for tuning in', T_OUT)
TY = S('and thank yourself', T_OUT)
TWISH = S('i wish you nothing', T_OUT)
TSIG = S('im mtg', TWISH)
END_CARD = S('lets get this crypto', TSIG) + 0.35
PART_T = {s['part']: TIMES[i] for i, s in enumerate(STATES) if s['kind'] == 'part'}

# ------------------------------------------------------------------ captions with the active word lit
def build_chunks():
    sents, cur = [], []
    for w in WD:
        cur.append(w)
        if w['word'][-1] in '.?!' and not re.match(r'^[A-Z]\.$', w['word']): sents.append(cur); cur = []
    if cur: sents.append(cur)
    dlen = lambda ws: len(C.display(' '.join(x['word'] for x in ws)))
    def split(ws):
        if dlen(ws) <= 64: return [ws]
        best = None
        for c_ in [i + 1 for i, x in enumerate(ws[:-1]) if x['word'][-1] in ',:']:
            a_, b_ = dlen(ws[:c_]), dlen(ws[c_:])
            if a_ >= 12 and b_ >= 12 and (best is None or max(a_, b_) < best[0]): best = (max(a_, b_), c_)
        if best is None: tot = dlen(ws); best = (0, min(range(1, len(ws)), key=lambda c_: abs(dlen(ws[:c_]) - tot / 2)))
        return split(ws[:best[1]]) + split(ws[best[1]:])
    chunks = [p for s in sents for p in split(s)]
    out = []
    for k, c in enumerate(chunks):
        a = c[0]['start'] - 0.06; b = c[-1]['end'] + 0.35
        if k + 1 < len(chunks) and chunks[k + 1][0]['start'] - c[-1]['end'] < 1.2: b = chunks[k + 1][0]['start'] - 0.06
        out.append(dict(a=a, b=min(b, SPEECH_END), words=c, text=C.display(' '.join(x['word'] for x in c))))
    return out
CHUNKS = build_chunks()

@lru
def cap_img(text, act, maxw):
    toks = text.split(' ')
    for size in (38, 35, 32):
        f = fnt('sb', size); sp = f.getlength(' '); lines, cur, wcur = [], [], 0
        for k, tk in enumerate(toks):
            tw = f.getlength(tk)
            if cur and wcur + sp + tw > maxw - 52: lines.append(cur); cur, wcur = [], 0
            cur.append(k); wcur += (sp if wcur else 0) + tw
        lines.append(cur)
        if len(lines) <= 2: break
    lh = int(size * 1.32); wl = [sum(f.getlength(toks[k]) for k in ln) + sp * (len(ln) - 1) for ln in lines]
    w = int(max(wl)) + 52; h = lh * len(lines) + 24
    im = rrect((w, h), 20, (0, 0, 0, 215)); d = ImageDraw.Draw(im)
    for li, ln in enumerate(lines):
        x = (w - wl[li]) / 2; y = 12 + li * lh + lh / 2
        for k in ln:
            d.text((x, y), toks[k], font=f, fill=LIME if k == act else WHITE, anchor='lm'); x += f.getlength(toks[k]) + sp
    return np.array(im)

def caption_at(t):
    for c in CHUNKS:
        if c['a'] <= t < c['b']:
            ws = c['words']; i = max([k for k, w in enumerate(ws) if w['start'] - 0.03 <= t] or [0])
            m = len(c['text'].split(' ')); n = len(ws)
            act = i if m == n else min(m - 1, int(i * m / n))
            return c['text'], act
    return None

# ------------------------------------------------------------------ emoji pops on key spoken words (t < T_RECAP)
EMOS = []
for ph, e in [('grab your phone', '📱'), ('hi my name is mtg', '👋'), ('you can pause any step', '⏸️'), ('your email and your phone', '📧'),
              ('for k y c', '🪪'), ('a crypto exchange like', '💱'), ('those are digital dollars', '💵'), ('two codes from your sponsor', '🔑'),
              ('youll use three websites', '🌐'), ('heres the money plan', '💰'), ('exposure is the size', '⚖️'),
              ('make sure its the partner link', '✅'), ('using english letters only', '🔤'), ('without the first zero', '☝️'),
              ('take that seriously', '⚠️'), ('check your email', '📧'), ('check spam or junk mail', '🗑️'), ('never register directly', '🚫'),
              ('answer honestly', '🤝'), ('lose money when trading', '📉'), ('do the face scan', '🤳'), ('so keep moving', '⏱️'),
              ('so check twice', '👀'), ('then payment successful', '🎉'), ('only fifty', '☝️'), ('now the screen most people skip', '🛑'),
              ('liquidated means closed', '⚠️'), ('youll see success', '🎉'), ('write down your c u number', '✍️'),
              ('youll see application received', '📩'), ('profits can be withdrawn', '💵'), ('released after twelve months', '📅'),
              ('rules can change', '🔄')]:
    try: EMOS.append((S(ph), e))
    except KeyError: print('emoji phrase not found:', ph)

def draw_emoji_pops(fr, t, box):
    if box is None: return
    for t0, e in EMOS:
        age = t - t0
        if 0 <= age <= 2.0:
            a = min(1.0, age / 0.15) * min(1.0, (2.0 - age) / 0.3); s = 0.4 + 0.6 * ease_back(age / 0.4)
            im = emo(e, 84); im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
            x = int(box[2] - im.width + 6); y = int(box[1] - im.height - 14 - 8 * ease_out(age / 2.0))
            comp(fr, np.array(im), x, y, a)

# ------------------------------------------------------------------ state rendering (parts 1 to 6 and the intro)
SX0, SY0, SX1, SY1, RX0, RX1 = R.SX0, R.SY0, R.SX1, R.SY1, R.RX0, R.RX1
NO_TAP = {36}
_ptr = icon('mouse-pointer-2', 64, DARK, 1.8, fill=GOLD)
_ps = Image.new('RGBA', _ptr.size, (0, 0, 0, 0)); _ps.putalpha(_ptr.getchannel('A').point(lambda v: int(v * 0.55)))
PTR = np.array(_ptr); PTR_SH = np.array(_ps.filter(ImageFilter.GaussianBlur(4)))

def shot_parts(i):
    st = STATES[i]; img = R.BGIMG.copy(); R.chrome(img, st['part'])
    img, ring = R.place_shot(img, st['shot'], st['plat'], st['hl'], st['labels'])
    c = R.shot_img(st['shot']); sc = min((SX1 - SX0 - 40) / c.width, (SY1 - SY0 - 30) / c.height, 1.5)
    cw, ch = int(c.width * sc), int(c.height * sc); x = SX0 + (SX1 - SX0 - cw) // 2; y = SY0 + (SY1 - SY0 - ch) // 2
    base = np.array(img.convert('RGB')).astype(np.float32)
    dim = base.copy(); dim[y:y + ch, x:x + cw] *= 0.42
    for b in st['hl']:
        bx0, by0 = max(x, int(x + b[0] * cw) - 10), max(y, int(y + b[1] * ch) - 10)
        bx1, by1 = min(x + cw, int(x + b[2] * cw) + 10), min(y + ch, int(y + b[3] * ch) + 10)
        dim[by0:by1, bx0:bx1] = base[by0:by1, bx0:bx1]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); R.panel(lay, st); pb = lay.getbbox()
    out = dict(kind='shot', base=base, dim=dim, rect=(x, y, cw, ch), panel=np.array(lay.crop(pb)), pbox=pb, ring=None, tap=None)
    if st['hl']:
        rb = ring.getbbox(); out['ring'] = (np.array(ring.crop(rb)), rb)
        if st['chips'] and i not in NO_TAP:
            b = st['hl'][0]; out['tap'] = (x + (b[0] + (b[2] - b[0]) * 0.62) * cw, y + (b[1] + b[3]) / 2 * ch, RING[st['plat']])
    return out

RISK_BANDS = None
def card_parts(i):
    global RISK_BANDS
    st = STATES[i]; full = np.array(R.card_img(st).convert('RGB')).astype(np.float32)
    out = dict(kind='card', full=full, pop=None, reveal=None)
    pv = STATES[i - 1] if i > 0 else None
    if pv and pv['kind'] == st['kind'] and st['kind'] in ('list', 'sites', 'money', 'hero', 'engage', 'promo') and pv.get('title') == st.get('title'):
        prev = np.array(R.card_img(pv).convert('RGB')).astype(np.float32)
        diff = np.abs(full - prev).max(2) > 10
        if diff.any() and diff.mean() < 0.4:
            ys, xs = np.where(diff); bb = (max(0, xs.min() - 6), max(0, ys.min() - 6), min(W, xs.max() + 7), min(H, ys.max() + 7))
            out['pop'] = (prev, bb)
    if st['kind'] == 'risk':
        t0 = TIMES[i]
        bands = [((270, 300, W - 270, 356), S('with twenty four times amplify', t0)), ((270, 378, W - 270, 512), S('a drop of about', t0)),
                 ((270, 520, W - 270, 590), S('on the trading balance', t0)), ((270, 592, W - 270, 672), S('is the same size', t0)),
                 ((270, 690, W - 270, 768), S('your whole deposit', t0))]
        empty = full.copy()
        for (x0, y0, x1, y1), _ in bands: empty[y0:y1, x0:x1] = (40, 18, 8)
        out['reveal'] = (empty, bands); RISK_BANDS = bands
    return out

_cache = {}
def parts(i):
    if i not in _cache:
        for k in [k for k in _cache if k < i - 2]: del _cache[k]
        _cache[i] = shot_parts(i) if STATES[i]['kind'] == 'shot' else card_parts(i)
    return _cache[i]

def ripple(fr, x, y, u, col):
    r = 16 + 52 * ease_out(u); lay = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([80 - r, 80 - r, 80 + r, 80 + r], outline=col + (int(255 * (1 - u)),), width=6)
    d.ellipse([68, 68, 92, 92], fill=col + (int(220 * (1 - u)),)); comp(fr, np.array(lay), int(x - 80), int(y - 80))

def state_frame(i, t):
    p = parts(i); age = t - TIMES[i]
    if p['kind'] == 'shot':
        fr = p['base'].copy()
        if p['ring'] is not None:
            a_d = 0.9 * smooth((age - 0.2) / 0.45); x, y, cw, ch = p['rect']
            fr[y:y + ch, x:x + cw] = p['base'][y:y + ch, x:x + cw] * (1 - a_d) + p['dim'][y:y + ch, x:x + cw] * a_d
            r, (bx0, by0, bx1, by1) = p['ring']
            a = min(1.0, age / 0.3) * (0.62 + 0.38 * math.sin(2 * math.pi * age / 1.3) ** 2); comp(fr, r, bx0, by0, a)
        pb = p['pbox']; comp(fr, p['panel'], pb[0], pb[1] + int(30 * (1 - ease_out(age / 0.45))), ease_out(age / 0.35))
        if p['tap']:
            tx, ty, col = p['tap']; T_TAP = 0.62
            if 0.12 <= age <= 2.3:
                u = smooth((age - 0.12) / (T_TAP - 0.12)); sx, sy = tx + 170, ty + 140
                px, py = sx + (tx - sx) * u, sy + (ty - sy) * u; press = 4 if abs(age - T_TAP) < 0.1 else 0
                a = min(1.0, (age - 0.12) / 0.2, (2.3 - age) / 0.3)
                comp(fr, PTR_SH, int(px - 8 + 5 + press), int(py - 8 + 7 + press), a); comp(fr, PTR, int(px - 8 + press), int(py - 8 + press), a)
            if T_TAP <= age <= T_TAP + 0.6: ripple(fr, tx, ty, (age - T_TAP) / 0.6, col)
        return fr
    if p['reveal'] is not None:
        empty, bands = p['reveal']; fr = empty.copy()
        for (x0, y0, x1, y1), tb in bands:
            u = (t - tb + 0.05) / 0.4
            if u <= 0: continue
            crop = p['full'][y0:y1, x0:x1]; s = 0.88 + 0.12 * ease_back(u); a = min(1.0, u / 0.6)
            if s != 1.0:
                cs = cv2.resize(crop, (max(1, int((x1 - x0) * s)), max(1, int((y1 - y0) * s))), interpolation=cv2.INTER_LINEAR)
                ox, oy = x0 + ((x1 - x0) - cs.shape[1]) // 2, y0 + ((y1 - y0) - cs.shape[0]) // 2
                reg = fr[oy:oy + cs.shape[0], ox:ox + cs.shape[1]]; reg[:] = reg * (1 - a) + cs[:reg.shape[0], :reg.shape[1]] * a
            else: fr[y0:y1, x0:x1] = fr[y0:y1, x0:x1] * (1 - a) + crop * a
        return fr
    if p['pop'] is not None:
        prev, (x0, y0, x1, y1) = p['pop']; u = age / 0.42
        if u >= 1: return p['full'].copy()
        fr = prev.copy(); crop = p['full'][y0:y1, x0:x1]; s = 0.86 + 0.14 * ease_back(u); a = min(1.0, u / 0.55)
        cs = cv2.resize(crop, (max(1, int((x1 - x0) * s)), max(1, int((y1 - y0) * s))), interpolation=cv2.INTER_LINEAR)
        ox, oy = x0 + ((x1 - x0) - cs.shape[1]) // 2, y0 + ((y1 - y0) - cs.shape[0]) // 2
        ox, oy = max(0, ox), max(0, oy); hh, ww = min(cs.shape[0], H - oy), min(cs.shape[1], W - ox)
        reg = fr[oy:oy + hh, ox:ox + ww]; reg[:] = reg * (1 - a) + cs[:hh, :ww] * a
        return fr
    if age < 0.5:      # a new card settles in
        s = 1.035 - 0.035 * ease_out(age / 0.5); cw, ch = int(W / s), int(H / s); x0, y0 = (W - cw) // 2, (H - ch) // 2
        return cv2.resize(p['full'][y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LINEAR)
    return p['full'].copy()      # never hand out the cached image: captions are drawn onto the returned frame

# ------------------------------------------------------------------ "A promo is a promo" card (real urgency, honest)
PROMO_ROWS = [('✅', 'Still running when I made this training', WHITE, TEAL),
              ('⏳', "It won't be here forever. Nobody can promise the end date", WHITE, ORANGE),
              ('🚀', "Decided to start? Start while it's still on", WHITE, LIME),
              ('🔎', 'Confirm it on jet-up.ai before you deposit', WHITE, GOLD),
              ('📤', "Send this video to someone who's ready", WHITE, PINK)]
_card_base = R.card_img
def _promo_card(st):
    if st['kind'] != 'promo': return _card_base(st)
    img = R.BGIMG.copy(); R.chrome(img, 6); d = ImageDraw.Draw(img)
    t = G('A PROMO IS A PROMO', 84, ORANGE, GOLD_L, 'b', ORANGE, 16, 0.5); hg = emo('⏳', 88)
    tw = hg.width + 24 + t.width - 96; x0 = CX - tw // 2          # the glow adds 48 px each side
    img.alpha_composite(hg, (x0, 196 - hg.height // 2)); img.alpha_composite(t, (x0 + hg.width + 24 - 48, 196 - t.height // 2))
    y = 330
    for k, (e, txt, col, edge) in enumerate(PROMO_ROWS):
        if st['n'] >= k + 2:
            box = rrect((1340, 96), 30, (26, 20, 44, 245), outline=edge + (255,), width=3); img.alpha_composite(box, (CX - 670, y))
            img.alpha_composite(emo(e, 54), (CX - 670 + 30, y + 21))
            f = F('sb', 37); d.text((CX - 670 + 110, y + 48), txt, font=f, fill=col, anchor='lm')
        y += 112
    return img
R.card_img = _promo_card

# ------------------------------------------------------------------ MTG's face as the profile picture (replaces the crown), FACE=square png
FACE = os.environ.get('FACE')
if FACE:
    sys.path.insert(0, '/home/claude/face')
    from make_profile import badge as _badge
    _sq = cv2.imread(FACE)
    from photo_card import photo_card
    @lru
    def face_badge(d):
        b = _badge(_sq, 600); return b.resize((int(b.width * d / 600), int(b.height * d / 600)), Image.LANCZOS)
    @lru
    def face_small(d=46):
        rgb = Image.fromarray(cv2.cvtColor(_sq, cv2.COLOR_BGR2RGB)).resize((d * 4, d * 4), Image.LANCZOS)
        im = Image.new('RGBA', (d * 4, d * 4), (0, 0, 0, 0)); m = Image.new('L', (d * 4, d * 4), 0)
        ImageDraw.Draw(m).ellipse([6, 6, d * 4 - 7, d * 4 - 7], fill=255); f = rgb.convert('RGBA'); f.putalpha(m); im.alpha_composite(f)
        ImageDraw.Draw(im).ellipse([3, 3, d * 4 - 4, d * 4 - 4], outline=GOLD + (255,), width=10)
        return im.resize((d, d), Image.LANCZOS)
    _chrome0 = R.chrome
    def _chrome(img, part=None):
        _chrome0(img, part); d = ImageDraw.Draw(img)
        d.rounded_rectangle((50, 34, 104, 82), 20, fill=(16, 13, 26, 255))      # hide the crown
        img.alpha_composite(face_small(48), (54, 34))
    R.chrome = _chrome
    _card0 = R.card_img
    def _card(st):
        if st['kind'] != 'mtg': return _card0(st)
        img = R.BGIMG.copy(); R.chrome(img, st.get('part')); d = ImageDraw.Draw(img)
        b = photo_card(600); img.alpha_composite(b, (600 - b.width // 2, 500 - b.height // 2))
        RXm = 1390
        d.text((RXm, 300), 'MTG', font=F('b', 150), fill=GOLD, anchor='ma')
        d.text((RXm, 500), 'Your Digital Architect', font=F('m', 54), fill=WHITE, anchor='ma')
        R.etext(img, (RXm, 610), st['line'], F('sb', 40), LIME, anchor='ma')
        return img
    R.card_img = _card
    R.BGIMG_CHROME = None

# ------------------------------------------------------------------ the animated ending (ALTRUVA outro, upgraded)
OUT_BASE = R.BGIMG.copy(); R.chrome(OUT_BASE)
OUT_BASE = np.array(OUT_BASE.convert('RGB')).astype(np.float32)

def header(ov, txt, t, t0, t1, y=170, c1=PURPLE, c2=PINK, size=64):
    a, p = env(t, t0, t1, 0.4, 0.3); paste_c(ov, G(txt, size, c1, c2, 'b', c2, 14, 0.5), CX, y + (1 - p) * 20, a)

RECAP = [('Account', 'user-plus', '👤'), ('Identity', 'scan-face', '🪪'), ('Deposit', 'wallet', '💵'), ('Strategy', 'trending-up', '📈'), ('Promo', 'gift', '🎁')]
RECAP_T = [S(w.lower(), T_RECAP) for w, _, _ in RECAP]

@lru
def recap_tile(k, done):
    name, ic, e = RECAP[k]; col = LIME if done else (90, 80, 120)
    im = rrect((280, 300), 34, (26, 20, 44, 245), outline=col + (255,), width=4 if done else 2)
    im.alpha_composite(ring_icon(ic, 130, LIME if done else PURPLE), ((280 - ring_icon(ic, 130, LIME if done else PURPLE).width) // 2, 10))
    ImageDraw.Draw(im).text((140, 248), name, font=fnt('b', 40), fill=WHITE, anchor='mm')
    return im

@lru
def tick_badge(d=74):
    im = Image.new('RGBA', (d, d), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse([0, 0, d - 1, d - 1], fill=TEAL + (255,), outline=WHITE + (255,), width=4)
    ic = icon('check', int(d * 0.6), WHITE, 3.2); im.alpha_composite(ic, ((d - ic.width) // 2, (d - ic.height) // 2))
    return glow(im, 10, TEAL, 0.6)

def recap(ov, t):
    t1 = T_ENG + 0.3; a0, _ = env(t, T_RECAP, t1, 0.35, 0.35)
    if a0 <= 0: return
    header(ov, "AND THAT'S IT", t, T_RECAP + 0.05, t1, 175)
    xs = [CX + (k - 2) * 320 for k in range(5)]; y = 470
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([xs[0], y - 4, xs[-1], y + 4], 4, fill=(60, 52, 84, 255))
    last = max([k for k, tt in enumerate(RECAP_T) if t >= tt] or [-1])
    if last >= 0:
        u = smooth((t - RECAP_T[last]) / 0.4); xe = xs[last - 1] + (xs[last] - xs[last - 1]) * u if last > 0 else xs[0]
        d.rounded_rectangle([xs[0], y - 4, xe, y + 4], 4, fill=LIME + (255,))
    paste(ov, lay, 0, 0, a0)
    for k in range(5):
        tt = RECAP_T[k]; done = t >= tt; ak, pk = env(t, T_RECAP + 0.15 + 0.06 * k, t1, 0.35, 0.3)
        paste_c(ov, recap_tile(k, done), xs[k], y + (1 - pk) * 30, ak * a0, (0.92 + 0.08 * pk) * pulse(t, tt, 0.07))
        if done:
            ab, pb = env(t, tt, t1, 0.15, 0.3); paste_c(ov, tick_badge(), xs[k] + 112, y - 132, ab * a0, 1.6 - 0.6 * pb)
            burst(ov, xs[k], y - 40, t, tt, [LIME, TEAL, WHITE], 10, 120, 0.5)
    ac, pc = env(t, S('one tap at a time', T_RECAP) - 0.05, t1, 0.3, 0.3)
    paste_c(ov, chip('One tap at a time', None, LIME, 36, '👆'), CX, 700, ac * a0, 0.9 + 0.1 * pc)
    asx, psx = env(t, S('screens change over time', T_RECAP) - 0.05, t1, 0.3, 0.3)
    paste_c(ov, chip('Screens change over time: look for the same words', 'scan-search', ORANGE, 34), CX, 810 + (1 - psx) * 16, asx * a0)

def engage(ov, t):
    t1 = T_WE + 0.3; a0, _ = env(t, T_ENG, t1, 0.35, 0.35)
    if a0 <= 0: return
    header(ov, 'HELP SOMEONE START RIGHT', t, T_ENG + 0.05, t1, 175)
    items = [('bookmark', '🔖', 'SAVE', "so it's here when you need it", GOLD, S('save this video', T_ENG), S('so its here', T_ENG)),
             ('share-2', '📤', 'SHARE', "with someone who's ready to start", PINK, S('share it with someone', T_ENG), S('whos ready', T_ENG)),
             ('message-circle', '💬', 'COMMENT', 'tell me below', LIME, 1e9, 1e9)]
    for k, (ic, e, lab, sub, col, tt, ts) in enumerate(items):
        x = CX + (k - 1) * 440; y = 470
        if t < tt:
            paste_c(ov, ring_icon(ic, 210, (80, 70, 110)), x, y, a0 * 0.55); continue
        ak, pk = env(t, tt - 0.05, t1, 0.2, 0.3)
        paste_c(ov, ring_icon(ic, 210, col, e), x, y, ak * a0, (0.5 + 0.5 * pk) * pulse(t, tt + 0.25, 0.06))
        burst(ov, x, y, t, tt, [col, WHITE, LIME], 14, 170)
        paste_c(ov, T(lab, 54, col), x, y + 170, ak * a0)
        a2, _ = env(t, ts - 0.05, t1, 0.3, 0.3); paste_c(ov, T(sub, 30, ICE, 'm'), x, y + 232, a2 * a0)

def we_learn(ov, t):
    t1 = T_CMT + 0.3; a0, _ = env(t, T_WE, t1, 0.35, 0.35)
    if a0 <= 0: return
    a1, p1 = env(t, T_WE + 0.05, t1, 0.4, 0.3); paste_c(ov, ring_icon('users', 180, GOLD, '🤝'), CX, 300, a1 * a0, 0.85 + 0.15 * p1)
    paste_c(ov, G('WE LEARN BEST', 92, WHITE, ICE, 'b', PURPLE, 16, 0.6), CX, 500, a1 * a0, 1.15 - 0.15 * p1)
    a2, p2 = env(t, S('when we teach', T_WE) - 0.05, t1, 0.35, 0.3)
    paste_c(ov, G('WHEN WE TEACH OTHERS', 92, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 630, a2 * a0, 1.15 - 0.15 * p2)

PARTS6 = [(k, P[k][2]) for k in range(1, 7)]
def comment(ov, t):
    """Comment DONE when set up; stuck? comment the Part number; the most asked step becomes the next video"""
    t1 = T_LINKS + 0.3; a0, _ = env(t, T_CMT, t1, 0.35, 0.35)
    if a0 <= 0: return
    tc = S('comment done', T_CMT); a1, p1 = env(t, tc - 0.05, t1, 0.2, 0.3)
    paste_c(ov, ring_icon('message-circle', 210, LIME, '💬'), 520, 330, a1 * a0, 0.5 + 0.5 * p1); burst(ov, 520, 330, t, tc, [LIME, PINK, WHITE], 14, 170)
    paste_c(ov, T('COMMENT', 50, LIME), 520, 490, a1 * a0)
    td0, td1 = S('done', T_CMT), E('set up', T_CMT)
    if t >= td0 - 0.05:
        q = 'DONE'; n = int(len(q) * min(1.0, (t - td0 + 0.05) / 0.35))
        bub = Image.new('RGBA', (640, 215), (0, 0, 0, 0)); d = ImageDraw.Draw(bub)
        d.rounded_rectangle([0, 0, 639, 169], 44, fill=(255, 255, 255, 250)); d.polygon([(60, 150), (20, 212), (150, 162)], fill=(255, 255, 255, 250))
        d.text((60, 85), q[:n], font=fnt('b', 92), fill=DARK, anchor='lm')
        if n == len(q): bub.alpha_composite(emo('✅', 86), (60 + int(fnt('b', 92).getlength(q)) + 24, 42))
        ab, pb = env(t, td0 - 0.05, t1, 0.22, 0.3); paste_c(ov, bub, 1080, 300, ab * a0, 0.85 + 0.15 * pb)
        a2, _ = env(t, S('as soon as', T_CMT) - 0.05, t1, 0.3, 0.3)
        paste_c(ov, T('as soon as your account is set up', 36, ICE, 'm'), 1080, 450, a2 * a0)
    ts = S('stuck on a step', T_CMT); a3, p3 = env(t, ts - 0.05, t1, 0.3, 0.3)
    paste_c(ov, chip('Stuck on a step? Comment the Part number', None, ORANGE, 38, '🤔'), CX, 590, a3 * a0, 0.9 + 0.1 * p3)
    tp = S('comment the part number', T_CMT)
    for k, col in PARTS6:
        ak, pk = env(t, tp + 0.08 * k, t1, 0.25, 0.3)
        paste_c(ov, chip(f'Part {k}', None, col, 34), CX + (k - 3.5) * 170, 690, ak * a0, 0.7 + 0.3 * pk)
    tn = S('becomes my next video', T_CMT); a4, p4 = env(t, tn - 0.05, t1, 0.25, 0.3)
    paste_c(ov, chip('The step most of you ask about = my next video', None, PINK, 38, '🎬'), CX, 800, a4 * a0, 0.7 + 0.3 * p4)
    burst(ov, CX, 800, t, tn, [PINK, LIME, WHITE], 14, 120, 0.65, 520, 45)

def links(ov, t):
    t1 = T_SLOG + 0.3; a0, _ = env(t, T_LINKS, t1, 0.35, 0.35)
    if a0 <= 0: return
    mv = smooth((t - T_GROUP) / 0.5)
    ak, _ = env(t, T_LINKS + 0.05, T_GROUP + 0.4, 0.35, 0.35); paste_c(ov, T('EVERYTHING I SHOWED YOU + MY LINKS', 34, LIME), CX, 230, ak * a0)
    tj = S('mtg tribe dot com slash jet up', T_LINKS) - 0.1; aj, pj = env(t, tj, t1, 0.25, 0.3)
    paste_c(ov, url_pill('mtgtribe.com/jetup', 104), CX, 400 - 230 * mv, aj * a0, (1.18 - 0.18 * pj) * (1 - 0.42 * mv))
    ab, pb = env(t, T_BIO - 0.05, T_GROUP + 0.4, 0.2, 0.35)
    if ab > 0:
        paste_c(ov, chip('Check my bio', 'arrow-up', PINK, 46, '📲'), CX, 590, ab * a0, (0.6 + 0.4 * pb) * pulse(t, T_BIO + 0.25, 0.05))
        burst(ov, CX, 590, t, T_BIO, [PINK, LIME, WHITE], 12, 120, 0.65, 230, 55)
        for k, key in enumerate(['tiktok', 'youtube']):
            a2, p2 = env(t, T_BIO + 0.25 + 0.15 * k, T_GROUP + 0.4, 0.3, 0.35)
            paste_c(ov, plat_badge(key, 620, 80), CX + (k - 0.5) * 660, 720 + (1 - p2) * 20, a2 * a0 * ab)
    ag, pg = env(t, T_GROUP + 0.2, t1, 0.35, 0.3)
    if ag > 0:
        paste_c(ov, T('JOIN THE MTG TRIBE', 40, GOLD), CX, 330, ag * a0)
        a2, p2 = env(t, S('if you believe in learning', T_GROUP), t1, 0.3, 0.3)
        paste_c(ov, chip('Learn before you earn', None, GOLD, 36, '📚'), CX, 420, a2 * a0, 0.9 + 0.1 * p2)
        tg = S('mtg tribe dot com slash group', T_GROUP) - 0.1; a3, p3 = env(t, tg, t1, 0.25, 0.3)
        paste_c(ov, url_pill('mtgtribe.com/group', 96, PINK, WHITE, PINK), CX, 580, a3 * a0, 1.18 - 0.18 * p3)
        burst(ov, CX, 580, t, tg + 0.1, [PINK, PURPLE, WHITE], 16, 140, 0.7, 470, 95)
        a4, p4 = env(t, tg + 0.35, t1, 0.3, 0.3); paste_c(ov, plat_badge('whatsapp', 700, 84), CX, 730 + (1 - p4) * 20, a4 * a0)

def slogan(ov, t):
    t1 = T_OUT + 0.3; a0, _ = env(t, T_SLOG, t1, 0.35, 0.35)
    if a0 <= 0: return
    rows = [('IT PAYS TO', WHITE, ICE, S('it pays to', T_SLOG), 270, 76), ('PAY ATTENTION', GOLD_L, GOLD_D, S('pay attention', T_SLOG), 400, 124),
            ('& TAKE', ICE, PINK, S('and take', T_SLOG), 530, 76), ('ACTION', LIME, TEAL, S('action', T_SLOG), 680, 150)]
    for txt, c1, c2, tt, y, sz in rows:
        a, p = env(t, tt - 0.05, t1, 0.22, 0.3)
        paste_c(ov, G(txt, sz, c1, c2, 'b', c2, 16, 0.55), CX, y, a * a0, 1.25 - 0.25 * p)
    ta = S('action', T_SLOG); burst(ov, CX, 680, t, ta, [LIME, TEAL, GOLD, WHITE], 18, 160, 0.8, 360, 110)
    ae, pe = env(t, ta + 0.2, t1, 0.3, 0.3); paste_c(ov, photo_card(330) if FACE else emo('👑', 90), 240 if FACE else CX, 500 if FACE else 830, ae * a0, 0.7 + 0.3 * pe)

def outro(ov, t):
    t1 = END_CARD + 0.25; a0, _ = env(t, T_OUT, t1, 0.3, 0.3)
    if a0 <= 0: return
    if t < TH:
        a, p = env(t, T_OUT + 0.05, TH, 0.3, 0.25)
        paste_c(ov, ring_icon('shield-check', 170, LIME), CX, 330, a * a0, 0.85 + 0.15 * p)
        a1, p1 = env(t, S('none of this', T_OUT) - 0.05, TH, 0.3, 0.25); paste_c(ov, T('Not financial advice', 76), CX, 500, a1 * a0, 1.1 - 0.1 * p1)
        a2, p2 = env(t, S('always do your', T_OUT) - 0.05, TH, 0.3, 0.25)
        paste_c(ov, chip('Always do your own research', None, GOLD, 44, '🔎'), CX, 630, a2 * a0, 0.9 + 0.1 * p2)
    elif t < TY:
        a, p = env(t, TH, TY, 0.3, 0.25); paste_c(ov, G('THANK YOU', 116, PURPLE, PINK, 'b', PINK, 16, 0.55), CX, 230, a * a0, 1.1 - 0.1 * p)
        for k, (ic, e, lab, col, ph) in enumerate([('thumbs-up', '👍', 'Like', LIME, 'like'), ('share-2', '📤', 'Share', PINK, 'share'),
                                                     ('message-circle', '💬', 'Comment', GOLD, 'comment')]):
            tt = S(ph, TH); x = CX + (k - 1) * 360; a2, p2 = env(t, tt - 0.04, TY, 0.18, 0.25)
            paste_c(ov, ring_icon(ic, 200, col, e), x, 500, a2 * a0, (0.45 + 0.55 * p2) * pulse(t, tt + 0.2, 0.06))
            paste_c(ov, T(lab, 44, WHITE), x, 660, a2 * a0); burst(ov, x, 500, t, tt, [col, WHITE], 12, 170)
            if ph == 'like':
                for j in range(5):
                    u = (t - tt - 0.15 * j) / 1.4
                    if 0 <= u <= 1: paste_c(ov, emo('❤️', 40), x + 60 * math.sin(j * 2.1 + u * 3), 420 - 220 * u, (1 - u) * a0)
        a3, p3 = env(t, S('your support', TH) - 0.05, TY, 0.3, 0.25)
        paste_c(ov, chip('Your support means everything', None, PURPLE, 40, '🙏'), CX, 800, a3 * a0, 0.9 + 0.1 * p3)
    elif t < TWISH:
        a, p = env(t, TY, TWISH, 0.3, 0.25)
        paste_c(ov, T('Thank yourself', 80), CX, 250, a * a0); paste_c(ov, T('for taking', 52, ICE, 'm'), CX, 345, a * a0)
        tm = S('massive', TY); a2, p2 = env(t, tm - 0.05, TWISH, 0.22, 0.25)
        paste_c(ov, G('MASSIVE ACTION', 132, GOLD_L, GOLD_D, 'b', GOLD, 18, 0.6), CX, 490, a2 * a0, 1.25 - 0.25 * p2)
        burst(ov, CX, 490, t, tm, [GOLD, GOLD_L, WHITE], 16, 150, 0.8, 560, 105)
        a3, p3 = env(t, S('today', TY) - 0.05, TWISH, 0.3, 0.25)
        paste_c(ov, chip('today, to change your future!', None, LIME, 46, '🚀'), CX, 660, a3 * a0, 0.9 + 0.1 * p3)
    elif t < TSIG:
        a, p = env(t, TWISH, TSIG, 0.3, 0.25); paste_c(ov, T('I wish you nothing but the best,', 62), CX, 300, a * a0)
        tb = S('because you', TWISH); a2, p2 = env(t, tb - 0.05, TSIG, 0.22, 0.25)
        paste_c(ov, G('YOU ARE THE BEST', 138, LIME, TEAL, 'b', LIME, 18, 0.6), CX, 490, a2 * a0, 1.25 - 0.25 * p2)
        burst(ov, CX, 490, t, tb + 0.15, [LIME, GOLD, WHITE, PINK], 18, 150, 0.9, 640, 110)
        for k in range(6):
            ang = k * math.pi / 3 + 0.4; tw = 0.6 + 0.4 * math.sin(t * 6 + k)
            paste_c(ov, emo('✨', 52), CX + 640 * math.cos(ang), 490 + 170 * math.sin(ang), a2 * a0 * tw, 0.8 + 0.2 * tw)
        a3, p3 = env(t, tb + 0.3, TSIG, 0.3, 0.25); paste_c(ov, photo_card(230) if FACE else emo('👑', 96), CX, 755 if FACE else 660, a3 * a0, 0.8 + 0.2 * p3 if FACE else 1.0)
    else:
        a, p = env(t, TSIG, t1, 0.35, 0.25)
        if FACE:
            paste_c(ov, photo_card(580), 560, 470, a * a0, 0.9 + 0.1 * p); RX_ = 1280
            paste_c(ov, T('Crypto-Regards,', 104, GOLD_L, 'sig'), RX_, 300, a * a0)
            paste_c(ov, G('MTG', 190, GOLD_L, GOLD_D, 'b', GOLD_D, 18, 0.6), RX_, 470, a * a0, 0.9 + 0.1 * p)
            a1, _ = env(t, S('your digital architect', TSIG) - 0.05, t1, 0.35, 0.25)
            paste_c(ov, T('Y O U R   D I G I T A L   A R C H I T E C T', 30, LIME), RX_, 610, a1 * a0)
            a2, p2 = env(t, S('see you on the next one', TSIG) - 0.05, t1, 0.3, 0.25)
            paste_c(ov, chip('See you on the next one', None, PINK, 40, '👋'), RX_, 730, a2 * a0, 0.9 + 0.1 * p2)
            return
        paste_c(ov, T('Crypto-Regards,', 112, GOLD_L, 'sig'), CX, 270, a * a0)
        m = G('MTG', 190, GOLD_L, GOLD_D, 'b', GOLD_D, 18, 0.6); paste_c(ov, m, CX - 60, 450, a * a0, 0.9 + 0.1 * p)
        paste_c(ov, emo('👑', 120), CX - 60 + m.width / 2 + 40, 430, a * a0)
        a1, _ = env(t, S('your digital architect', TSIG) - 0.05, t1, 0.35, 0.25)
        paste_c(ov, T('Y O U R   D I G I T A L   A R C H I T E C T', 34, LIME), CX, 610, a1 * a0)
        a2, p2 = env(t, S('see you on the next one', TSIG) - 0.05, t1, 0.3, 0.25)
        paste_c(ov, chip('See you on the next one', None, PINK, 40, '👋'), CX, 730, a2 * a0, 0.9 + 0.1 * p2)

def end_card(ov, t):
    if t < END_CARD: return
    a0 = ease_out((t - END_CARD) / 0.45); LX = 470
    if FACE:
        a, p = env(t, END_CARD + 0.05, 999, 0.45, 0.1); paste_c(ov, photo_card(300), LX, 265, a * a0, 0.88 + 0.12 * p)
        paste_c(ov, T('Crypto-Regards,', 62, GOLD_L, 'sig'), LX, 462, a * a0)
        paste_c(ov, G('MTG', 104, GOLD_L, GOLD_D, 'b', GOLD_D, 16, 0.6), LX, 550, a * a0, 0.88 + 0.12 * p)
        a1, _ = env(t, END_CARD + 0.4, 999, 0.4, 0.1); paste_c(ov, T('YOUR DIGITAL ARCHITECT', 30, LIME), LX, 627, a1 * a0)
        ly0 = 660
    else:
        a, p = env(t, END_CARD + 0.05, 999, 0.45, 0.1); paste_c(ov, T('Crypto-Regards,', 92, GOLD_L, 'sig'), LX, 215, a * a0)
        m = G('MTG', 160, GOLD_L, GOLD_D, 'b', GOLD_D, 18, 0.6); paste_c(ov, m, LX - 50, 375, a * a0, 0.88 + 0.12 * p)
        paste_c(ov, emo('👑', 104), LX - 50 + m.width / 2 + 36, 358, a * a0)
        a1, _ = env(t, END_CARD + 0.4, 999, 0.4, 0.1); paste_c(ov, T('YOUR DIGITAL ARCHITECT', 36, LIME), LX, 510, a1 * a0)
        ly0 = 560
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line([(LX - 190, ly0), (LX + 190, ly0)], fill=GOLD + (255,), width=3); paste(ov, lay, 0, 0, a1 * a0)
    a2, p2 = env(t, END_CARD + 0.8, 999, 0.4, 0.1); sl = T("Let's Get This Crypto!", 56, WHITE)
    paste_c(ov, sl, LX - 36, ly0 + 80, a2 * a0); paste_c(ov, emo('💪', 70), LX - 36 + sl.width / 2 + 46, ly0 + 76 - 10 * abs(math.sin((t - END_CARD) * 4)), a2 * a0)
    a3, p3 = env(t, END_CARD + 1.1, 999, 0.4, 0.1); paste_c(ov, chip('Check my bio', None, PINK, 38, '📲'), LX, ly0 + 195, a3 * a0, 0.9 + 0.1 * p3)
    RXc = 1370
    a4, p4 = env(t, END_CARD + 0.3, 999, 0.35, 0.1); paste_c(ov, url_pill('mtgtribe.com/jetup', 72), RXc, 175, a4 * a0, 0.9 + 0.1 * p4)
    for k, key in enumerate(['tiktok', 'youtube', 'whatsapp', 'telegram', 'facebook']):
        ak, pk = env(t, END_CARD + 0.6 + 0.18 * k, 999, 0.35, 0.1)
        paste_c(ov, plat_badge(key, 760, 82), RXc + (1 - pk) * 40, 300 + k * 100, ak * a0)
    a5, p5 = env(t, END_CARD + 1.7, 999, 0.4, 0.1)
    paste_c(ov, chip('Also watch: 5 checks before you try JetUP', 'play', LIME, 32, '📺'), RXc, 850, a5 * a0, 0.9 + 0.1 * p5)
    a6, _ = env(t, END_CARD + 2.0, 999, 0.4, 0.1)
    paste_c(ov, T('Not financial advice. Trading involves risk. Only use money you can afford to lose.', 28, GREY, 'm'), CX, 1015, a6 * a0)

SCENES = [(T_RECAP, T_ENG + 0.3, recap), (T_ENG, T_WE + 0.3, engage), (T_WE, T_CMT + 0.3, we_learn), (T_CMT, T_LINKS + 0.3, comment),
          (T_LINKS, T_SLOG + 0.3, links), (T_SLOG, T_OUT + 0.3, slogan), (T_OUT, END_CARD + 0.25, outro), (END_CARD, 1e9, end_card)]

def outro_frame(t):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for t0, t1, fn in SCENES:
        if t0 <= t < t1: fn(ov, t)
    fr = OUT_BASE.copy(); comp(fr, np.array(ov), 0, 0); return fr

# ------------------------------------------------------------------ sound effects (synthesised, as in the ALTRUVA engine)
def sfx_times():
    sx = {'whoosh': [], 'tick': [], 'pop': [], 'click': []}
    for i, st in enumerate(STATES[:IDX_RECAP]):
        k = st['kind']
        if k == 'part' or st['trig'] in ('and remember a promo is a promo', 'heres the money plan', 'heres why it matters', 'youll use three websites', 'before we start', 'by the end'):
            sx['whoosh'].append(TIMES[i])
        pv = STATES[i - 1] if i else None
        if pv and k in ('list', 'sites', 'money', 'promo') and pv['kind'] == k and pv.get('title') == st.get('title') and st.get('n', 0) > pv.get('n', 0):
            sx['tick'].append(TIMES[i])
        if k == 'shot' and st['chips'] and st['hl'] and i not in NO_TAP: sx['click'].append(TIMES[i] + 0.62)
        if k == 'risk' and RISK_BANDS is None: card_parts(i)
    sx['tick'] += [tb for _, tb in (RISK_BANDS or [])] + RECAP_T
    sx['whoosh'] += [T_RECAP, T_ENG, T_WE, T_CMT, T_LINKS, T_GROUP, T_SLOG, T_OUT, TH, TY, TWISH, TSIG, END_CARD]
    sx['pop'] += [S('save this video', T_ENG), S('share it with someone', T_ENG), S('comment done', T_CMT), S('becomes my next video', T_CMT), S('then send this video to someone'), T_BIO,
                  S('mtg tribe dot com slash group', T_GROUP), S('action', T_SLOG), S('like', TH), S('share', TH), S('comment', TH),
                  S('massive', TY), S('because you', TWISH) + 0.15]
    return sx

def make_sfx(path):
    from scipy.signal import butter, sosfilt
    SR = 48000; N = int(TOTAL * SR); out = np.zeros(N, np.float32); rng = np.random.default_rng(7)
    def whoosh():
        n = int(0.5 * SR); x = rng.standard_normal(n).astype(np.float32); o = np.zeros(n, np.float32)
        for k in range(10):
            a, b = k * n // 10, (k + 1) * n // 10; fc = 500 + 3500 * (k / 9)
            o[a:b] = sosfilt(butter(2, [fc * 0.6, fc * 1.4], btype='band', fs=SR, output='sos'), x)[a:b]
        o *= np.sin(np.pi * np.linspace(0, 1, n)) ** 2; return o / np.abs(o).max() * 0.08
    def tick():
        n = int(0.08 * SR); tt = np.arange(n) / SR
        x = (np.sin(2 * np.pi * 1760 * tt) + 0.4 * np.sin(2 * np.pi * 3520 * tt)) * np.exp(-tt * 55); return x / np.abs(x).max() * 0.07
    def pop():
        n = int(0.12 * SR); tt = np.arange(n) / SR; f = 380 + 700 * tt / tt[-1]
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30); return x / np.abs(x).max() * 0.12
    def click():
        n = int(0.05 * SR); tt = np.arange(n) / SR
        x = rng.standard_normal(n) * np.exp(-tt * 180) + 0.6 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 120)
        x = sosfilt(butter(2, [900, 6000], btype='band', fs=SR, output='sos'), x); return x / np.abs(x).max() * 0.10
    sx = sfx_times(); fns = dict(whoosh=whoosh, tick=tick, pop=pop, click=click)
    for name, ts in sx.items():
        for t0 in ts:
            s = fns[name]().astype(np.float32); a = int(t0 * SR); b = min(N, a + len(s))
            if 0 <= a < N: out[a:b] += s[:b - a]
    pcm = np.clip(np.stack([out, out], 1) * 32767, -32768, 32767).astype(np.int16)
    import wave
    with wave.open(path, 'wb') as wf: wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
    print('sfx', {k: len(v) for k, v in sx.items()})

# ------------------------------------------------------------------ main
def state_at(t):
    return max(j for j in range(IDX_RECAP) if TIMES[j] <= t + 1e-6) if t >= TIMES[0] else -1

def frame(t, cover):
    if t < COVER: return cover.copy()
    if t >= T_RECAP:
        fr = outro_frame(t)
        if t < T_RECAP + 0.3: k = (t - T_RECAP) / 0.3; fr = state_frame(IDX_RECAP - 1, t) * (1 - k) + fr * k
    else:
        i = state_at(t)
        if i < 0: return cover.copy()
        fr = state_frame(i, t); age = t - TIMES[i]
        if age < 0.24: k = age / 0.24; fr = (state_frame(i - 1, t) if i > 0 else cover) * (1 - k) + fr * k
    # part progress line under the tracker
    if PART_T[1] <= t < T_RECAP and STATES[max(0, state_at(t))].get('part'):
        u = (t - PART_T[1]) / (T_RECAP - PART_T[1]); fr[76:80, 560:950] = (60, 52, 84); fr[76:80, 560:560 + int(390 * u)] = LIME
    # captions (lit word) + emoji pops
    if t < END_CARD:
        c = caption_at(t)
        if c:
            onshot = t < T_RECAP and STATES[max(0, state_at(t))]['kind'] == 'shot'
            maxw = (RX1 - RX0) if onshot else 1500; im = cap_img(c[0], c[1], maxw)
            cx = (RX0 + RX1) // 2 if onshot else CX; x = int(cx - im.shape[1] / 2); y = 1046 - im.shape[0]
            comp(fr, im, x, y); box = (x, y, x + im.shape[1], 1046)
            if t < T_RECAP: draw_emoji_pops(fr, t, box)
    return fr

def main(a=0, b=None, out='tut2_video.mp4'):
    n = int(round(TOTAL * FPS)); b = n if b is None else b
    cover = np.array(R.cover_img().convert('RGB')).astype(np.float32)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for fi in range(a, b):
        ff.stdin.write(np.clip(frame(fi / FPS, cover), 0, 255).astype(np.uint8).tobytes())
        if fi % 500 == 0: print(out, fi, '/', b, flush=True)
    ff.stdin.close(); ff.wait(); print('done', out)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        cover = np.array(R.cover_img().convert('RGB')).astype(np.float32); os.makedirs('qa3', exist_ok=True)
        for ts in sys.argv[2:]:
            Image.fromarray(np.clip(frame(float(ts), cover), 0, 255).astype(np.uint8)).save(f'qa3/f_{float(ts):07.2f}.png')
    elif sys.argv[1] == 'sfx': make_sfx('sfx.wav')
    elif sys.argv[1] == 'times':
        print(dict(T_RECAP=T_RECAP, T_ENG=T_ENG, T_WE=T_WE, T_CMT=T_CMT, T_LINKS=T_LINKS, T_BIO=T_BIO, T_GROUP=T_GROUP, T_SLOG=T_SLOG,
                   T_OUT=T_OUT, TH=TH, TY=TY, TWISH=TWISH, TSIG=TSIG, END_CARD=END_CARD, TOTAL=TOTAL))
    else:
        main(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
