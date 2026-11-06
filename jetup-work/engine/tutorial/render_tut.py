# JetUP + TAG Markets sign-up training: renders the 16:9 video frames from scenes.py, synced to voice_tut_words.json.
import json, re, subprocess, sys, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/jv')
import compose as C
from gfx import F, emoji, wrap
from shots import SHOTS
from scenes import STATES, P, RING, PURPLE, PINK, LIME, ORANGE, TEAL, BLUE, SITES


from fontTools.ttLib import TTFont
_CMAP = set(TTFont('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf').getBestCmap())
def _runs(text):
    out, i = [], 0
    while i < len(text):
        if ord(text[i]) in _CMAP:
            j = i
            while j < len(text) and ord(text[j]) in _CMAP: j += 1
            out.append(('t', text[i:j])); i = j
        else:
            j = i + 1
            while j < len(text) and text[j] in '\ufe0f\u200d': j += 1
            out.append(('e', text[i:j])); i = j
    return out

def etext(img, xy, text, font, fill, anchor='la'):
    """Text with colour emoji runs; anchor la/lm/ma/mm/rm."""
    d = ImageDraw.Draw(img); rs = _runs(text)
    if all(k == 't' for k, _ in rs):
        d.text(xy, text, font=font, fill=fill, anchor=anchor); return
    asc, desc = font.getmetrics(); es = int(font.size * 0.95); h = asc + desc
    ws = [d.textlength(s_, font=font) if k == 't' else es + font.size * 0.12 for k, s_ in rs]
    x, y = xy; tw = sum(ws)
    if anchor[0] == 'm': x -= tw / 2
    elif anchor[0] == 'r': x -= tw
    top = y - h / 2 if anchor[1] == 'm' else y
    for (k, s_), w in zip(rs, ws):
        if k == 't': d.text((x, top), s_, font=font, fill=fill, anchor='la')
        else: emoji(img, s_.replace('\ufe0f', ''), x, top + (asc - es) * 0.55 + font.size * 0.06, es)
        x += w

def ewidth(d, text, font):
    return sum(d.textlength(s_, font=font) if k == 't' else font.size * 1.07 for k, s_ in _runs(text))

W, H, FPS = 1920, 1080, 25
COVER, END = 1.0, 5.0
WHITE, GREY, BG = (247, 246, 252), (170, 165, 190), (11, 9, 18)
PANEL, LINE = (24, 20, 36), (52, 44, 74)
GOLD = (232, 194, 90)
SX0, SY0, SX1, SY1 = 70, 120, 870, 1010          # screenshot zone
RX0, RX1 = 930, 1860                              # right panel zone
CAP_Y0, CAP_Y1 = 912, 1046

# ---------- background ----------
def make_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32) + np.array(BG, np.float32)
    def glow(cx, cy, r, col, a):
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r
        m = np.clip(1 - d, 0, 1) ** 2 * a
        return m[..., None] * (np.array(col, np.float32) - img)
    img += glow(250, 120, 900, PURPLE, 0.30)
    img += glow(1750, 1000, 900, LIME, 0.10)
    img += glow(1500, 120, 700, PINK, 0.10)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')
BGIMG = make_bg()

def grad_text(img, xy, text, font, c1=PURPLE, c2=PINK, anchor='la'):
    d = ImageDraw.Draw(img); bb = d.textbbox(xy, text, font=font, anchor=anchor)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    mask = Image.new('L', (w + 4, h + 8), 0); ImageDraw.Draw(mask).text((xy[0] - bb[0], xy[1] - bb[1]), text, font=font, fill=255, anchor=anchor)
    g = np.linspace(0, 1, w + 4)[None, :, None]
    col = (np.array(c1) * (1 - g) + np.array(c2) * g).repeat(h + 8, 0)
    layer = Image.fromarray(col.astype(np.uint8)).convert('RGBA'); layer.putalpha(mask)
    img.alpha_composite(layer, (bb[0], bb[1]))

def pill(d, x, y, text, font, fg, bg, pad=(22, 10), outline=None, r=None):
    tw = d.textlength(text, font=font); bb = font.getbbox('Hg')
    h = bb[3] - bb[1] + pad[1] * 2
    d.rounded_rectangle((x, y, x + tw + pad[0] * 2, y + h), r or h // 2, fill=bg, outline=outline, width=2 if outline else 0)
    d.text((x + pad[0], y + h / 2), text, font=font, fill=fg, anchor='lm')
    return x + tw + pad[0] * 2, y + h

def chrome(img, part=None):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 30, 520, 86), 28, fill=(16, 13, 26, 230), outline=GOLD, width=2)
    emoji(img, '👑', 58, 40, 38)
    d.text((108, 58), 'MTG', font=F('b', 32), fill=GOLD, anchor='lm')
    d.text((186, 58), '|  Your Digital Architect', font=F('m', 22), fill=WHITE, anchor='lm')
    # brand pair, top right
    x = W - 40 - 420
    d.rounded_rectangle((x, 30, W - 40, 86), 28, fill=(16, 13, 26, 230), outline=(80, 70, 110), width=2)
    grad_text(img, (x + 28, 58), 'JetUP', F('b', 28), anchor='lm')
    d.text((x + 128, 58), '×', font=F('m', 26), fill=GREY, anchor='lm')
    d.text((x + 160, 58), 'TAG Markets', font=F('b', 28), fill=LIME, anchor='lm')
    # part progress
    if part:
        px = 560
        for k in range(1, 7):
            col = P[k][2]; on = k == part; done = k < part
            fill = col + (255,) if on else ((col + (110,)) if done else (60, 52, 84, 255))
            d.rounded_rectangle((px, 50, px + (120 if on else 44), 66), 8, fill=fill)
            if on: d.text((px + 60, 58), f'PART {k}', font=F('b', 13), fill=(15, 12, 25), anchor='mm')
            px += (130 if on else 54)

# ---------- screenshots ----------
_pg = {}
def page(p):
    if p not in _pg: _pg[p] = Image.open(f'../src16/pg-{p:02d}.png').convert('RGB')
    return _pg[p]

def shot_img(name):
    s = SHOTS[name]; im = page(s['p']).copy()
    for box, smp in s.get('fill', []):
        col = im.getpixel((smp[0] * 2, smp[1] * 2)); ImageDraw.Draw(im).rectangle([v * 2 for v in box], fill=col)
    for b in s.get('blur', []):
        bb = tuple(v * 2 for v in b); reg = im.crop(bb)
        small = reg.resize((max(1, reg.width // 14), max(1, reg.height // 14)), Image.BILINEAR).resize(reg.size, Image.NEAREST)
        im.paste(small.filter(ImageFilter.GaussianBlur(6)), bb)
    for b, lab in s.get('cover', []):
        bb = tuple(v * 2 for v in b); d = ImageDraw.Draw(im)
        d.rounded_rectangle(bb, 10, fill=(28, 22, 44), outline=PINK, width=3)
        fs = 22
        f = F('b', fs)
        while d.textlength(lab, font=f) > (bb[2] - bb[0]) - 16 and fs > 12:
            fs -= 1; f = F('b', fs)
        d.text(((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2), lab, font=f, fill=LIME, anchor='mm')
    return im.crop(tuple(v * 2 for v in s['box']))

def place_shot(img, name, plat, hl, labels, ring_alpha=1.0):
    """Returns (base image with screenshot, ring layer RGBA)."""
    c = shot_img(name)
    maxw, maxh = SX1 - SX0 - 40, SY1 - SY0 - 30
    sc = min(maxw / c.width, maxh / c.height, 1.5)
    c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
    x = SX0 + (SX1 - SX0 - c.width) // 2; y = SY0 + (SY1 - SY0 - c.height) // 2
    edge = {'jetup': PURPLE, 'tag': LIME, 'valr': BLUE, 'hub': ORANGE}[plat]
    # shadow + frame
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x - 6, y - 6, x + c.width + 6, y + c.height + 6), 30, fill=edge + (90,))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    mask = Image.new('L', c.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 22, fill=255)
    img.paste(c.convert('RGBA'), (x, y), mask)
    ImageDraw.Draw(img).rounded_rectangle((x - 2, y - 2, x + c.width + 2, y + c.height + 2), 24, outline=edge + (255,), width=3)
    ring = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
    rc = RING[plat]
    for i, b in enumerate(hl):
        bx0, by0 = x + b[0] * c.width - 8, y + b[1] * c.height - 8
        bx1, by1 = x + b[2] * c.width + 8, y + b[3] * c.height + 8
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle((bx0, by0, bx1, by1), 16, outline=rc + (200,), width=14)
        ring.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
        rd.rounded_rectangle((bx0, by0, bx1, by1), 16, outline=rc + (255,), width=5)
        if i < len(labels):
            f = F('b', 24); tw = rd.textlength(labels[i], font=f)
            lx = min(max(bx0, SX0), SX1 - tw - 40); ly = by1 + 10 if by1 + 56 < SY1 else by0 - 52
            rd.rounded_rectangle((lx, ly, lx + tw + 32, ly + 42), 21, fill=rc + (255,))
            rd.text((lx + 16, ly + 21), labels[i], font=f, fill=(15, 12, 25), anchor='lm')
    return img, ring

# ---------- right panel ----------
def panel(img, st):
    d = ImageDraw.Draw(img)
    tag, ptitle, pc = P[st['part']]
    x0, y = RX0, 128
    pill(d, x0, y, f'{tag}  ·  {ptitle.upper()}', F('b', 22), (15, 12, 25), pc + (255,))
    y += 70
    f = F('b', 50)
    for ln in wrap(d, st['title'], f, RX1 - RX0)[:3]:
        etext(img, (x0, y), ln, f, WHITE); y += 64
    y += 12
    if st.get('url'):
        _, y2 = pill(d, x0, y, '🌐 ' if False else st['url'], F('b', 46), (15, 12, 25), LIME + (255,), pad=(30, 14))
        y = y2 + 22
    if st['chips']:
        cx = x0; fch = F('sb', 32)
        d.text((x0, y), 'Tap / type:', font=F('m', 24), fill=GREY); y += 38
        for ch in st['chips']:
            tw = ewidth(d, ch, fch) + 48
            if cx + tw > RX1: cx = x0; y += 70
            pill(d, cx, y, ch, fch, WHITE, (40, 32, 62, 255), pad=(24, 10), outline=PINK if st['plat'] in ('tag', 'valr') else LIME, r=14)
            cx += tw + 16
        y += 82
    fl = F('m', 32)
    for ln in st['lines']:
        for k, w_ in enumerate(wrap(d, ln, fl, RX1 - RX0 - 30)):
            if k == 0: d.ellipse((x0, y + 15, x0 + 10, y + 25), fill=pc)
            etext(img, (x0 + 26, y), w_, fl, WHITE); y += 44
        y += 6
    if st['calc']:
        fc = F('sb', 32); lines = st['calc']; bh = len(lines) * 50 + 34
        d.rounded_rectangle((x0, y, RX1, y + bh), 20, fill=(20, 17, 32, 255), outline=pc, width=2)
        for i, ln in enumerate(lines):
            etext(img, (x0 + 28, y + 18 + i * 50), ln, fc, LIME if '=' in ln.split()[-2:] else WHITE)
        y += bh + 18
    for term, mean in st['defs']:
        fd = F('m', 29); body = wrap(d, mean, fd, RX1 - RX0 - 60); bh = 70 + len(body) * 40
        d.rounded_rectangle((x0, y, RX1, y + bh), 20, fill=(32, 26, 52, 255), outline=PURPLE, width=2)
        d.text((x0 + 24, y + 16), f'📖  {term}' if False else term, font=F('b', 34), fill=PINK)
        for i, b in enumerate(body): d.text((x0 + 24, y + 60 + i * 40), b, font=fd, fill=WHITE)
        y += bh + 16
    if st.get('warn'):
        fw = F('sb', 29); body = []
        for part_ in st['warn'].split('\n'): body += wrap(d, part_, fw, RX1 - RX0 - 90)
        bh = 30 + len(body) * 40
        d.rounded_rectangle((x0, y, RX1, y + bh), 20, fill=(58, 26, 10, 255), outline=ORANGE, width=3)
        emoji(img, '⚠️', x0 + 20, y + 16, 40)
        for i, b in enumerate(body): d.text((x0 + 74, y + 15 + i * 40), b, font=fw, fill=WHITE)
        y += bh + 16
    if st.get('note'):
        fn = F('m', 29); body = wrap(d, st['note'], fn, RX1 - RX0 - 50); bh = 26 + len(body) * 40
        d.rounded_rectangle((x0, y, RX1, y + bh), 18, fill=(30, 26, 48, 255), outline=(90, 80, 130), width=2)
        for i, b in enumerate(body): etext(img, (x0 + 24, y + 13 + i * 40), b, fn, WHITE)
        y += bh + 16
    if st.get('ok'):
        fo = F('sb', 29); body = wrap(d, 'Success check: ' + st['ok'], fo, RX1 - RX0 - 90); bh = 26 + len(body) * 40
        d.rounded_rectangle((x0, y, RX1, y + bh), 18, fill=(8, 52, 44, 255), outline=TEAL, width=3)
        emoji(img, '✅', x0 + 20, y + 13, 36)
        for i, b in enumerate(body): d.text((x0 + 70, y + 13 + i * 40), b, font=fo, fill=WHITE)
        y += bh + 16
    return y

# ---------- full-screen cards ----------
def centered(d, y, text, font, fill=WHITE):
    for ln in text.split('\n'):
        d.text((W // 2, y), ln, font=font, fill=fill, anchor='ma'); y += int(font.size * 1.22)
    return y

def card_img(st):
    img = BGIMG.copy(); d = ImageDraw.Draw(img); k = st['kind']
    chrome(img, st.get('part'))
    if k == 'hero':
        d.text((W // 2, 220), st['kicker'], font=F('b', 30), fill=LIME, anchor='ma')
        y = 280
        for ln in st['title'].split('\n'):
            grad_text(img, (W // 2, y), ln, F('b', 96), PURPLE if y == 280 else PINK, PINK if y == 280 else LIME, anchor='ma'); y += 118
        etext(img, (W // 2, y + 40), st['sub'], F('sb', 50), WHITE, anchor='ma')
        bx = W // 2 - 380; by = 720
        d.rounded_rectangle((bx, by, bx + 340, by + 120), 30, fill=(30, 22, 52, 255), outline=PURPLE, width=3)
        grad_text(img, (bx + 170, by + 60), 'JetUP', F('b', 58), anchor='mm')
        d.text((W // 2, by + 60), '+', font=F('b', 60), fill=GREY, anchor='mm')
        d.rounded_rectangle((W // 2 + 40, by, W // 2 + 380, by + 120), 30, fill=(20, 20, 20, 255), outline=LIME, width=3)
        d.text((W // 2 + 210, by + 60), 'TAG Markets', font=F('b', 50), fill=LIME, anchor='mm')
    elif k == 'mtg':
        emoji(img, '👑', W // 2 - 110, 210, 220)
        d.text((W // 2, 470), 'MTG', font=F('b', 170), fill=GOLD, anchor='ma')
        d.text((W // 2, 680), 'Your Digital Architect', font=F('m', 54), fill=WHITE, anchor='ma')
        etext(img, (W // 2, 800), st['line'], F('sb', 46), LIME, anchor='ma')
    elif k == 'list':
        d.text((W // 2, 150), st['title'], font=F('b', 66), fill=WHITE, anchor='ma')
        items, n = st['items'], st['n']
        if st.get('row'):
            cw = 300; gap = 30; x = (W - (cw * 5 + gap * 4)) // 2
            for i, (e, t, s) in enumerate(items):
                on = i < n
                d.rounded_rectangle((x, 380, x + cw, 640), 30, fill=(28, 24, 44, 255), outline=LIME if on else LINE, width=3)
                emoji(img, e, x + cw // 2 - 45, 420, 90)
                d.text((x + cw // 2, 560), t, font=F('b', 40), fill=WHITE, anchor='mm'); x += cw + gap
            if st.get('note'): etext(img, (W // 2, 760), st['note'], F('sb', 40), LIME, anchor='ma')
            return img
        y = 270; rh = 112
        for i, (e, t, s) in enumerate(items):
            on = i < n
            d.rounded_rectangle((360, y, W - 360, y + rh - 16), 26, fill=(28, 24, 44, 255) if on else (20, 17, 30, 255),
                                outline=(LIME if on else LINE), width=3 if on else 2)
            if on:
                emoji(img, e, 392, y + 18, 58)
                if s:
                    d.text((480, y + 30), t, font=F('b', 38), fill=WHITE, anchor='lm')
                    d.text((480, y + 70), s, font=F('m', 26), fill=GREY, anchor='lm')
                else:
                    d.text((480, y + 48), t, font=F('b', 40), fill=WHITE, anchor='lm')
            else:
                d.text((480, y + 46), '·  ·  ·', font=F('b', 34), fill=(70, 62, 96), anchor='lm')
            y += rh
        if st.get('defn'):
            t, m = st['defn']; y += 6
            d.rounded_rectangle((360, y, W - 360, y + 100), 24, fill=(36, 28, 60, 255), outline=PINK, width=3)
            d.text((396, y + 50), t, font=F('b', 42), fill=PINK, anchor='lm')
            d.text((396 + d.textlength(t, font=F('b', 42)) + 30, y + 50), '= ' + m, font=F('sb', 36), fill=WHITE, anchor='lm')
        if st.get('note'):
            etext(img, (W // 2, y + 20), st['note'], F('sb', 38), LIME, anchor='ma')
    elif k == 'url':
        d.text((W // 2, 300), st['kicker'], font=F('b', 36), fill=LIME, anchor='ma')
        f = F('b', 120); tw = d.textlength(st['url'], font=f)
        d.rounded_rectangle((W // 2 - tw / 2 - 60, 400, W // 2 + tw / 2 + 60, 590), 95, fill=LIME + (255,))
        d.text((W // 2, 495), st['url'], font=f, fill=(14, 12, 22), anchor='mm')
        etext(img, (W // 2, 680), st['sub'], F('sb', 52), WHITE, anchor='ma')
    elif k == 'sites':
        d.text((W // 2, 150), "You'll use three websites", font=F('b', 66), fill=WHITE, anchor='ma')
        y = 300
        for i, (u, name, what, col) in enumerate(SITES):
            on = i < st['n']
            d.rounded_rectangle((230, y, W - 230, y + 200), 34, fill=(28, 24, 44, 255) if on else (20, 17, 30, 255), outline=col if on else LINE, width=4 if on else 2)
            if on:
                d.text((280, y + 44), name.upper(), font=F('b', 30), fill=col, anchor='lm')
                d.text((W - 280, y + 44), what, font=F('m', 30), fill=GREY, anchor='rm')
                d.text((280, y + 128), u, font=F('b', 72), fill=WHITE, anchor='lm')
            y += 230
    elif k == 'money':
        n = st['n']
        d.text((W // 2, 140), 'The money plan', font=F('b', 66), fill=WHITE, anchor='ma')
        # left column: the deposit split
        lx, ly = 110, 270
        rows = [('$155', 'your deposit', WHITE, 1), ('$50', 'Sonic strategy, now', LIME, 2), ('$100', 'kept in your balance for the promo', PINK, 3),
                ('+ $100', 'Dennis Promo bonus', ORANGE, 4), ('$5', 'spare, for small differences', GREY, 5)]
        for v, t, col, lvl in rows:
            if n >= lvl:
                d.rounded_rectangle((lx, ly, lx + 840, ly + 108), 24, fill=(28, 24, 44, 255), outline=col if col != WHITE else LINE, width=3)
                d.text((lx + 30, ly + 54), v, font=F('b', 52), fill=col, anchor='lm')
                d.text((lx + 230, ly + 54), t, font=F('m', 31), fill=WHITE, anchor='lm')
            ly += 126
        # right column: 24x
        if n >= 6:
            rx = 1000; ry = 270
            d.rounded_rectangle((rx, ry, rx + 760, ry + 360), 28, fill=(20, 17, 32, 255), outline=LIME, width=3)
            d.text((rx + 30, ry + 26), '24x AMPLIFY', font=F('b', 30), fill=LIME)
            d.text((rx + 30, ry + 90), '$50 × 24 = $1,200', font=F('b', 50), fill=WHITE)
            d.text((rx + 30, ry + 170), '($100 + $100) × 24 = $4,800', font=F('b', 46), fill=WHITE)
            if n >= 7:
                d.line((rx + 30, ry + 250, rx + 730, ry + 250), fill=LINE, width=2)
                d.text((rx + 30, ry + 270), '$1,200 + $4,800 = $6,000', font=F('b', 50), fill=LIME)
            if n >= 8:
                d.rounded_rectangle((rx, ry + 390, rx + 760, ry + 600), 26, fill=(58, 26, 10, 255), outline=ORANGE, width=3)
                d.text((rx + 30, ry + 430), 'EXPOSURE', font=F('b', 30), fill=ORANGE, anchor='lm')
                d.text((rx + 30, ry + 492), 'the size you trade with,', font=F('sb', 40), fill=WHITE, anchor='lm')
                d.text((rx + 30, ry + 550), 'NOT money you own', font=F('b', 40), fill=WHITE, anchor='lm')
    elif k == 'part':
        tag, title, col = P[st['part']]
        d.text((W // 2, 300), tag, font=F('b', 60), fill=col, anchor='ma')
        emoji(img, st['icon'], W // 2 - 70, 400, 140)
        y = 590
        for ln in wrap(d, title, F('b', 84), 1500): d.text((W // 2, y), ln, font=F('b', 84), fill=WHITE, anchor='ma'); y += 104
        if st.get('sub'): etext(img, (W // 2, y + 30), st['sub'], F('sb', 44), ORANGE, anchor='ma')
    elif k == 'risk':
        d.text((W // 2, 140), "Here's why it matters", font=F('b', 66), fill=WHITE, anchor='ma')
        d.rounded_rectangle((260, 270, W - 260, 820), 34, fill=(40, 18, 8, 255), outline=ORANGE, width=4)
        d.text((W // 2, 310), '24x AMPLIFY: YOUR DEPOSIT IS 1/24 OF THE TRADING BALANCE', font=F('b', 32), fill=ORANGE, anchor='ma')
        d.text((W // 2, 390), '1 ÷ 24 = 4.2%', font=F('b', 96), fill=WHITE, anchor='ma')
        d.text((W // 2, 530), 'Example: $50 × 24 = $1,200 trading balance', font=F('sb', 44), fill=WHITE, anchor='ma')
        d.text((W // 2, 600), '4.2% × $1,200 = $50', font=F('b', 56), fill=LIME, anchor='ma')
        d.text((W // 2, 700), 'A 4.2% drop = the size of your whole deposit', font=F('b', 46), fill=ORANGE, anchor='ma')
    elif k == 'engage':
        d.text((W // 2, 180), 'Help someone start right', font=F('b', 66), fill=WHITE, anchor='ma')
        items = [('🔖', 'SAVE', 'so it\'s here when you need it'), ('📤', 'SHARE', 'with someone ready to start'), ('💬', 'COMMENT', 'tell me below')]
        x = 220; cw = 470
        for i, (e, t, s) in enumerate(items):
            on = i < st['n']
            d.rounded_rectangle((x, 330, x + cw, 700), 34, fill=(28, 24, 44, 255) if on else (20, 17, 30, 255), outline=LIME if on else LINE, width=3)
            if on:
                emoji(img, e, x + cw // 2 - 60, 380, 120)
                d.text((x + cw // 2, 560), t, font=F('b', 52), fill=LIME, anchor='ma')
                d.text((x + cw // 2, 630), s, font=F('m', 28), fill=GREY, anchor='ma')
            x += cw + 35
        if st.get('q'): d.text((W // 2, 780), st['q'], font=F('b', 52), fill=PINK, anchor='ma')
    elif k == 'slogan':
        y = 400 if '\n' in st['text'] else 450
        for ln in st['text'].split('\n'):
            if st.get('gold'): d.text((W // 2, y), ln, font=F('b', 110), fill=GOLD, anchor='ma')
            else: grad_text(img, (W // 2, y), ln, F('b', 96), PINK, LIME, anchor='ma')
            y += 130
        emoji(img, '👑', W // 2 - 40, y + 30, 80)
    elif k == 'notice':
        d.text((W // 2, 250), 'Quick reminder', font=F('b', 72), fill=WHITE, anchor='ma')
        rows = ['Not financial advice', 'Always do your own research', 'Trading involves risk: only use money you can afford to lose']
        y = 420
        for r in rows:
            d.rounded_rectangle((300, y, W - 300, y + 100), 26, fill=(28, 24, 44, 255), outline=ORANGE, width=3)
            d.text((W // 2, y + 50), r, font=F('sb', 40), fill=WHITE, anchor='mm'); y += 130
    elif k == 'thanks':
        emoji(img, '🙏', W // 2 - 80, 250, 160)
        d.text((W // 2, 480), 'Thank you for every', font=F('b', 72), fill=WHITE, anchor='ma')
        d.text((W // 2, 580), 'like, share and comment', font=F('b', 72), fill=LIME, anchor='ma')
        d.text((W // 2, 730), 'Thank yourself for taking massive action today!', font=F('sb', 44), fill=GREY, anchor='ma')
    return img

def cover_img():
    img = BGIMG.copy(); d = ImageDraw.Draw(img); chrome(img)
    d.text((110, 230), 'STEP-BY-STEP TRAINING', font=F('b', 34), fill=LIME)
    grad_text(img, (110, 290), 'Join JetUP', F('b', 120), PURPLE, PINK)
    d.text((110, 430), '+ TAG Markets', font=F('b', 120), fill=LIME)
    d.text((114, 600), 'Every tap shown: sign up, KYC,', font=F('sb', 52), fill=WHITE)
    d.text((114, 670), 'deposit, Sonic and the $100 promo', font=F('sb', 52), fill=WHITE)
    pill(d, 114, 790, '6 parts  ·  phone friendly', F('b', 36), (15, 12, 25), LIME + (255,), pad=(30, 14))
    # phones collage
    for i, (nm, ang, x, y) in enumerate([('wallet', -6, 1090, 230), ('copyx', 5, 1390, 250)]):
        c = shot_img(nm); sc = 540 / c.height; c = c.resize((int(c.width * sc), 540), Image.LANCZOS).convert('RGBA')
        m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, fill=255); c.putalpha(m)
        fr = Image.new('RGBA', (c.width + 24, c.height + 24), (0, 0, 0, 0))
        ImageDraw.Draw(fr).rounded_rectangle((0, 0, fr.width - 1, fr.height - 1), 34, fill=(12, 10, 20, 255), outline=(LIME if i == 0 else PURPLE) + (255,), width=4)
        fr.alpha_composite(c, (12, 12)); fr = fr.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(fr, (x, y))
    return img

def end_img():
    img = BGIMG.copy(); d = ImageDraw.Draw(img)
    emoji(img, '👑', 290, 190, 200)
    d.text((390, 520), 'MTG', font=F('b', 170), fill=GOLD, anchor='mm')
    d.text((390, 640), 'Your Digital Architect', font=F('m', 46), fill=WHITE, anchor='mm')
    d.text((390, 760), "Let's Get This Crypto!", font=F('b', 52), fill=WHITE, anchor='mm')
    emoji(img, '💪', 680, 726, 64)
    rows = [('🌐', 'mtgtribe.com/jetup'), ('👥', 'mtgtribe.com/group'), ('✈️', 'Telegram  @mtgtribe'), ('📲', 'Check my bio')]
    y = 230
    for e, t in rows:
        d.rounded_rectangle((900, y, 1760, y + 120), 60, fill=(28, 24, 44, 255), outline=LIME, width=2)
        emoji(img, e, 945, y + 28, 64); d.text((1040, y + 60), t, font=F('sb', 50), fill=WHITE, anchor='lm'); y += 150
    d.text((W // 2, 940), 'Not financial advice. Trading involves risk. Only invest what you can afford to lose.', font=F('m', 32), fill=GREY, anchor='mm')
    return img

# ---------- captions ----------
C.DISPLAY[:0] = [
    (r'[Jj]et up dot I B portal dot I O', 'jetup.ibportal.io'), (r'[Pp]ortal dot tag markets dot com', 'portal.tagmarkets.com'),
    (r'jet dash up dot A I', 'jet-up.ai'), (r'MTG tribe dot com slash jet up', 'mtgtribe.com/jetup'), (r'MTG tribe dot com slash group', 'mtgtribe.com/group'),
    (r'\bK Y C\b', 'KYC'), (r'\bU S D T\b', 'USDT'), (r'\bU S D C\b', 'USDC'), (r'\bU S D\b', 'USD'), (r'\bC F Ds\b', 'CFDs'), (r'\bC F D\b', 'CFD'),
    (r'T R C twenty', 'TRC-20'), (r'E R C twenty', 'ERC-20'), (r'\bC U number', 'CU number'), (r'\bCopy X\b', 'CopyX'), (r'\bValr\b', 'VALR'),
    (r'\bSum sub\b', 'Sumsub'), (r'Self hosted Wallet', 'Self-hosted Wallet'), (r'sign up form', 'sign-up form'),
    (r'one hundred and fifty five dollars', '$155'), (r'one hundred and fifty five', '155'), (r'eighty eight percent', '88%'),
    (r'twenty four times', '24x'), (r'twelve hundred', '$1,200'), (r'two hundred becomes forty eight hundred', '$200 becomes $4,800'),
    (r'six thousand dollars', '$6,000'), (r'fifteen minutes', '15 minutes'), (r'seventy one cents', '71 cents'), (r'thirty percent', '30%'),
    (r'four point two percent', '4.2%'), (r'ten percent', '10%'), (r'five percent', '5%'), (r'two hundred dollar', '$200'),
    (r'one hundred dollar', '$100'), (r'fifty dollar', '$50'), (r'twelve months', '12 months'), (r'\bOne hundred stays', '$100 stays'),
    (r'another one hundred', 'another $100'), (r'the other one hundred', 'the other $100'), (r'\bFifty goes', '$50 goes'),
    (r'fifty becomes', '$50 becomes'), (r'type fifty', 'type 50'), (r'Only fifty', 'Only 50'), (r'\bpart five\b', 'Part 5'),
    (r'Crypto!!', 'Crypto!'),
]
C.DISPLAY.append((r'\bjetup\.ibportal\.io', 'jetup.ibportal.io'))   # runs after the JetUP casing rule, keeps the URL lower case

def build():
    J = json.load(open('voice_tut_words.json')); Wd = [dict(w, start=w['start'] + COVER, end=w['end'] + COVER) for w in J['words']]
    speech_end = COVER + J['duration']; total = speech_end + END
    toks, tt = [], []
    for w in Wd:
        for p_ in C.norm(w['word']).split(): toks.append(p_); tt.append(w['start'])
    times, pos = [], 0
    for st in STATES:
        q = C.norm(st['trig']).split(); hit = None
        for k in range(pos, len(toks) - len(q) + 1):
            if toks[k:k + len(q)] == q: hit = k; break
        if hit is None: raise SystemExit('MISSING trigger: ' + st['trig'])
        pos = hit + 1; times.append(round(max(COVER, tt[hit] - 0.1) * FPS) / FPS)
    # captions (sentences, split at commas when long)
    sents, cur = [], []
    for w in Wd:
        cur.append(w)
        if w['word'][-1] in '.?!' and not re.match(r'^[A-Z]\.$', w['word']): sents.append(cur); cur = []
    if cur: sents.append(cur)
    def dlen(ws): return len(C.display(' '.join(x['word'] for x in ws)))
    def split(ws):
        if dlen(ws) <= 64: return [ws]
        cuts = [i + 1 for i, x in enumerate(ws[:-1]) if x['word'][-1] in ',:']
        best = None
        for c_ in cuts:
            a_, b_ = dlen(ws[:c_]), dlen(ws[c_:])
            if a_ >= 12 and b_ >= 12 and (best is None or max(a_, b_) < best[0]): best = (max(a_, b_), c_)
        if best is None:
            tot = dlen(ws); best = (0, min(range(1, len(ws)), key=lambda c_: abs(dlen(ws[:c_]) - tot / 2)))
        return split(ws[:best[1]]) + split(ws[best[1]:])
    chunks = [p_ for s in sents for p_ in split(s)]
    caps = []
    for k, c_ in enumerate(chunks):
        a_ = c_[0]['start'] - 0.06; b_ = c_[-1]['end'] + 0.35
        if k + 1 < len(chunks) and chunks[k + 1][0]['start'] - c_[-1]['end'] < 1.2: b_ = chunks[k + 1][0]['start'] - 0.06
        caps.append((a_, min(b_, speech_end), C.display(' '.join(x['word'] for x in c_))))
    return times, caps, speech_end, total

def caption_layer(text):
    lay = Image.new('RGBA', (RX1 - RX0, CAP_Y1 - CAP_Y0), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = F('sb', 38); lines = wrap(d, text, f, RX1 - RX0 - 60)[:2]
    lh = 50; th = lh * len(lines) + 24; wmax = max(d.textlength(l, font=f) for l in lines)
    y0 = lay.height - th; cx = lay.width // 2
    d.rounded_rectangle((cx - wmax / 2 - 26, y0, cx + wmax / 2 + 26, lay.height), 20, fill=(0, 0, 0, 215))
    for i, l in enumerate(lines): d.text((cx, y0 + 12 + i * lh + lh // 2), l, font=f, fill=WHITE, anchor='mm')
    return np.array(lay).astype(np.float32)

def state_frames(st):
    """(base RGB float array, ring RGBA float array or None)"""
    if st['kind'] != 'shot':
        return np.array(card_img(st).convert('RGB')).astype(np.float32), None
    img = BGIMG.copy(); chrome(img, st['part'])
    img, ring = place_shot(img, st['shot'], st['plat'], st['hl'], st['labels'])
    panel(img, st)
    if not st['hl']: return np.array(img.convert('RGB')).astype(np.float32), None
    bb = ring.getbbox(); r = np.array(ring.crop(bb)).astype(np.float32)
    return np.array(img.convert('RGB')).astype(np.float32), (r, bb)

def main(out='tut_video.mp4', preview=None):
    times, caps, speech_end, total = build()
    json.dump(dict(times=times, caps=caps, speech_end=speech_end, total=total), open('tut_timeline.json', 'w'), indent=0)
    if preview is not None:          # still frames for QA
        for i in preview:
            b, r = state_frames(STATES[i]); img = b.copy()
            if r is not None:
                rr, (x0, y0, x1, y1) = r; a = rr[..., 3:4] / 255
                img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + rr[..., :3] * a
            Image.fromarray(img.astype(np.uint8)).save(f'qa/state_{i:03d}.png')
        return
    n = int(round(total * FPS))
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    cover = np.array(cover_img().convert('RGB')).astype(np.float32); endc = np.array(end_img().convert('RGB')).astype(np.float32)
    cache, capcache = {}, {}
    def get(i):
        if i not in cache:
            for k in list(cache):
                if k < i - 1: del cache[k]
            cache[i] = state_frames(STATES[i])
        return cache[i]
    def render_state(i, t):
        base, ring = get(i)
        if ring is None: return base
        r, (x0, y0, x1, y1) = ring
        age = t - times[i]; a = min(1.0, age / 0.3) * (0.62 + 0.38 * math.sin(2 * math.pi * age / 1.3) ** 2)
        al = r[..., 3:4] / 255 * a
        out = base.copy(); out[y0:y1, x0:x1] = base[y0:y1, x0:x1] * (1 - al) + r[..., :3] * al
        return out
    ci = 0
    for fi in range(n):
        t = fi / FPS
        if t < COVER: fr = cover
        elif t >= speech_end:
            k = min(1.0, (t - speech_end) / 0.4); last = render_state(len(STATES) - 1, t)
            fr = last * (1 - k) + endc * k
        else:
            i = max(j for j in range(len(STATES)) if times[j] <= t + 1e-6) if t >= times[0] else -1
            if i < 0: fr = cover
            else:
                fr = render_state(i, t)
                age = t - times[i]
                if age < 0.24:
                    prev = render_state(i - 1, t) if i > 0 else cover
                    k = age / 0.24; fr = prev * (1 - k) + fr * k
            # caption
            while ci < len(caps) and caps[ci][1] <= t: ci += 1
            if ci < len(caps) and caps[ci][0] <= t < caps[ci][1]:
                key = caps[ci][2]
                if key not in capcache:
                    capcache.clear(); capcache[key] = caption_layer(key)
                lay = capcache[key]; al = lay[..., 3:4] / 255
                reg = fr[CAP_Y0:CAP_Y1, RX0:RX1]
                if STATES[i]['kind'] != 'shot':   # full-screen cards: centre captions at the bottom
                    x0 = (W - lay.shape[1]) // 2; reg = fr[CAP_Y0:CAP_Y1, x0:x0 + lay.shape[1]]
                    fr = fr.copy(); fr[CAP_Y0:CAP_Y1, x0:x0 + lay.shape[1]] = reg * (1 - al) + lay[..., :3] * al
                else:
                    fr = fr.copy(); fr[CAP_Y0:CAP_Y1, RX0:RX1] = reg * (1 - al) + lay[..., :3] * al
        ff.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
        if fi % 1000 == 0: print('frame', fi, '/', n, flush=True)
    ff.stdin.close(); ff.wait()
    print('done', out, round(total, 2), 's')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'qa':
        os.makedirs('qa', exist_ok=True); main(preview=[int(x) for x in sys.argv[2:]])
    else:
        main()
