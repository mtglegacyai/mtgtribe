# JetUP 5 Checks v5 renderer: avatar re-timed to the new voice, animated cards on the exact word,
# word-lit captions, a 1-to-5 check tracker, framing punch-ins, two full-screen scenes, circle photo, end card.
#   python3 render.py frame <t> <out.png>     one still for checking
#   python3 render.py all                     full render (4 workers) -> v5_video.mp4
import json, os, re, sys, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cards_v5 as CV

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..'))
FONTS = os.path.join(HERE, '..', 'fonts')
ENGINE_FONTS = os.path.join(HERE, '..', 'jetup-work', 'engine', 'fonts')
AVATAR = os.path.join(HERE, '..', 'raw', 'avatar_v3.mp4')
PHOTO = os.path.join(SCR, 'brand', 'mtg-profile-photo.png')
FACE = os.path.join(SCR, 'brand', 'mtg-profile-face-crop.png')
MARK = os.path.join(SCR, 'brand', 'jetup-mark.png')
TRAIN = os.path.join(SCR, 'brand', 'JetUP_TAG_SignUp_Training_MTG_v4.2_thumbnail.jpg')
EMO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'

W, H, FPS = 1920, 1080, 25
PX, PY, PW, PH = 48, 118, 764, 830
SHIFT = 330
IW = PW - 80; X0 = PX + 40
CAP_CX, CAP_W, CAP_B = 1366, 1000, 1048
ZOOM_IN, Z_AX, Z_AY = 1.08, 990, 330
BG = (11, 9, 18); CARD = (28, 23, 44); LINE = (72, 61, 104)
LIME, PURPLE, PINK, RED, GREEN, GOLD, WHITE = CV.LIME, CV.PURPLE, CV.PINK, CV.RED, CV.GREEN, CV.GOLD, CV.WHITE
GREY = (178, 170, 204)
JP1, JP2 = (140, 108, 231), (227, 113, 252)

TL = json.load(open(os.path.join(HERE, 'tl.json')))
WORDS = TL['words']; SPEECH_END = TL['speech_end']; TOTAL = TL['total']; END0 = TOTAL - 5.0
NFR = len(TL['frames'])
NSRC = int(round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', AVATAR])) * FPS))

# ------------------------------------------------------------------ fonts, text and emoji
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc:
        name = {'b': 'Poppins-Bold', 'sb': 'Poppins-SemiBold', 'm': 'Poppins-Medium', 'r': 'Poppins-Regular', 'xb': 'Poppins-ExtraBold', 'k': 'Poppins-Black'}.get(w)
        path = os.path.join(FONTS, name + '.ttf') if name else os.path.join(ENGINE_FONTS, 'GreatVibes-Regular.ttf') if w == 'script' else os.path.join(FONTS, 'Anton-Regular.ttf')
        _fc[k] = ImageFont.truetype(path, s)
    return _fc[k]
_emo_font = ImageFont.truetype(EMO, 109)
_ec = {}
def emoji_img(ch, size):
    k = (ch, size)
    if k not in _ec:
        t = Image.new('RGBA', (300, 160), (0, 0, 0, 0))
        ImageDraw.Draw(t).text((4, 4), ch, font=_emo_font, embedded_color=True)
        bb = t.getbbox()
        if not bb: _ec[k] = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        else:
            t = t.crop(bb); _ec[k] = t.resize((size, max(1, int(size * t.height / t.width))), Image.LANCZOS)
    return _ec[k]

EMO_RE = re.compile('([\U0001F000-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿][️‍\U0001F3FB-\U0001F3FF\U0001F000-\U0001FAFF☀-➿]*)')
def rich_width(d, text, font):
    w = 0
    for part in EMO_RE.split(text):
        if not part: continue
        w += font.size * 1.1 if EMO_RE.fullmatch(part) else d.textlength(part, font=font)
    return w
def rich_draw(img, xy, text, font, fill):
    d = ImageDraw.Draw(img); x, y = xy
    for part in EMO_RE.split(text):
        if not part: continue
        if EMO_RE.fullmatch(part):
            e = emoji_img(part, int(font.size * 0.95)); img.alpha_composite(e, (int(x + font.size * 0.06), int(y + font.size * 0.18))); x += font.size * 1.1
        else:
            d.text((x, y), part, font=font, fill=fill); x += d.textlength(part, font=font)

def wrap(text, font, maxw):
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    out, line = [], ''
    for w in text.split(' '):
        t = (line + ' ' + w).strip()
        if rich_width(d, t, font) <= maxw: line = t
        else:
            if line: out.append(line)
            line = w
    if line: out.append(line)
    return out

def grad_fill(size, c1, c2, vertical=False):
    w, h = size; t = np.linspace(0, 1, h if vertical else w)
    g = np.zeros((h, w, 4), np.uint8)
    for i in range(3):
        col = (c1[i] * (1 - t) + c2[i] * t).astype(np.uint8)
        g[..., i] = col[:, None] if vertical else col[None, :]
    g[..., 3] = 255
    return Image.fromarray(g)

def text_sprite(text, font, fill=WHITE, grad=None, spacing=0):
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    if spacing:
        w = int(sum(d.textlength(ch, font=font) + spacing for ch in text)) + 4
    else:
        w = int(rich_width(d, text, font)) + 6
    asc, desc = font.getmetrics(); h = asc + desc + 6
    im = Image.new('RGBA', (max(1, w), h), (0, 0, 0, 0))
    if spacing:
        dd = ImageDraw.Draw(im); x = 0
        for ch in text: dd.text((x, 2), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + spacing
    else:
        rich_draw(im, (2, 2), text, font, fill)
    if grad:
        g = grad_fill(im.size, *grad); g.putalpha(im.split()[3]); im = g
    return im

def shadow(im, r=10, a=120, off=(0, 8)):
    s = Image.new('RGBA', (im.width + 4 * r, im.height + 4 * r), (0, 0, 0, 0))
    m = Image.new('L', s.size, 0); m.paste(im.split()[3].point(lambda v: min(255, v * a // 255)), (2 * r + off[0], 2 * r + off[1]))
    s.putalpha(m.filter(ImageFilter.GaussianBlur(r)))
    s.alpha_composite(im, (2 * r, 2 * r))
    return s, 2 * r

# ------------------------------------------------------------------ MTG photo: a circle with a gold ring (MTG, 6 Nov 2026)
_pc = {}
def photo_circle(d):
    if d in _pc: return _pc[d]
    ring = max(5, d // 40); glow = d // 7; S = d + 2 * ring + 2 * glow
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    g = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((glow - 6, glow - 6, S - glow + 5, S - glow + 5), fill=GOLD + (150,))
    out.alpha_composite(g.filter(ImageFilter.GaussianBlur(glow * 0.6)))
    rg = grad_fill((S, S), (255, 236, 170), (190, 132, 40)); m = Image.new('L', (S, S), 0)
    ImageDraw.Draw(m).ellipse((glow, glow, S - glow - 1, S - glow - 1), fill=255); rg.putalpha(m); out.alpha_composite(rg)
    ph = Image.open(PHOTO).convert('RGB').resize((d * 3, d * 3), Image.LANCZOS).convert('RGBA')
    pm = Image.new('L', (d * 3, d * 3), 0); ImageDraw.Draw(pm).ellipse((0, 0, d * 3 - 1, d * 3 - 1), fill=255); ph.putalpha(pm)
    out.alpha_composite(ph.resize((d, d), Image.LANCZOS), (glow + ring, glow + ring))
    _pc[d] = out
    return out

def face_small(d):
    k = ('face', d)
    if k not in _pc:
        f = Image.open(FACE).convert('RGB').resize((d * 4, d * 4), Image.LANCZOS).convert('RGBA')
        m = Image.new('L', (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse((6, 6, d * 4 - 7, d * 4 - 7), fill=255); f.putalpha(m)
        ImageDraw.Draw(f).ellipse((3, 3, d * 4 - 4, d * 4 - 4), outline=GOLD + (255,), width=10)
        _pc[k] = f.resize((d, d), Image.LANCZOS)
    return _pc[k]

# ------------------------------------------------------------------ the spoken word sequence and triggers
def norm(t): return re.sub(r'[^a-z0-9 ]', '', t.lower().replace('-', ' ').replace('’', "'").replace("'", ''))
TOK, TOK_T, TOK_W = [], [], []
for i, w in enumerate(WORDS):
    for p in norm(w['w']).split():
        TOK.append(p); TOK_T.append(w['s']); TOK_W.append(i)
def find(phrase, k0=0, k1=None):
    q = norm(phrase).split(); k1 = len(TOK) if k1 is None else k1
    for k in range(k0, k1 - len(q) + 1):
        if TOK[k:k + len(q)] == q: return k
    return None

# ------------------------------------------------------------------ captions with display spellings and the active word lit
DISP = [('x a u u s d', 'XAU/USD'), ('m t five', 'MT5'), ('metatrader five', 'MetaTrader 5'), ('f s c a', 'FSCA'), ('f s c', 'FSC'),
        ('f s p number five five two three seven', 'FSP number 55237'), ('t m financials', 'TM Financials'), ('my f x book', 'Myfxbook'),
        ('mtg tribe dot com slash jet up', 'mtgtribe.com/jetup'), ('mtg tribe dot com slash group', 'mtgtribe.com/group'),
        ('telegram at mtg tribe', 'Telegram @mtgtribe'), ('plus thirty point one percent', '+30.1%'),
        ('thirty point one times seventy percent', '30.1% × 70%'), ('twenty one percent', '21%'), ('twenty three months', '23 months'),
        ('forty percent', '40%'), ('november twenty twenty four', 'November 2024'), ('october twenty twenty six', 'October 2026'),
        ('seventy thirty', '70/30'), ('seventy percent', '70%'), ('thirty percent', '30%'), ('ten dollars', '$10'), ('seven dollars', '$7'),
        ('one hundred and fifty dollars', '$150'), ('adds one hundred', 'adds $100'), ('two hundred and fifty dollars', '$250'),
        ('twenty four times', '24 times'), ('six thousand dollars', '$6,000'), ('one million dollars', '$1,000,000'),
        ('twelve months', '12 months'), ('five checks', '5 checks'), ('check number four', 'check number 4'), ('check all five', 'check all 5'),
        ('check one', 'Check 1'), ('check two', 'Check 2'), ('check three', 'Check 3'), ('check four', 'Check 4'), ('check five', 'Check 5'),
        ('one to five', '1 to 5'), ('u s dollars', 'US dollars')]
DISP = sorted([(d.split(), r) for d, r in DISP], key=lambda x: -len(x[0]))
def disp_tokens(ws):
    """[(display text, [word indexes])] for a run of word indexes"""
    toks = [norm(WORDS[i]['w']).split() for i in ws]
    flat = [(p, i) for t, i in zip(toks, ws) for p in t]
    out, k = [], 0
    while k < len(flat):
        hit = None
        for pat, rep in DISP:
            n = len(pat)
            if [p for p, _ in flat[k:k + n]] == pat:
                hit = (rep, n); break
        if hit:
            idxs = sorted(set(i for _, i in flat[k:k + hit[1]])); last = WORDS[idxs[-1]]['w']
            punct = last[-1] if last[-1] in '.,?!:;' and idxs[-1] == flat[min(len(flat) - 1, k + hit[1] - 1)][1] else ''
            if hit[0].endswith('%') or hit[0].endswith('$7'): pass
            out.append((hit[0] + punct, idxs)); k += hit[1]
        else:
            i = flat[k][1]
            # the word itself as written (keeps capitals and punctuation); skip its other parts
            n = len(norm(WORDS[i]['w']).split())
            out.append((WORDS[i]['w'].replace('JetUP\'s', "JetUP's"), [i])); k += max(1, n)
    return out

def build_captions():
    sents, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(i)
        if w['w'][-1] in '.?!' or (i + 1 < len(WORDS) and WORDS[i + 1]['kind'] != w['kind']): sents.append(cur); cur = []
    if cur: sents.append(cur)
    LIM = 40
    chunks = []
    def L(ws): return len(' '.join(t for t, _ in disp_tokens(ws)))
    def split(ws):
        if L(ws) <= LIM or len(ws) < 3: return [ws]
        best = None
        for c in range(1, len(ws)):
            a, b = L(ws[:c]), L(ws[c:])
            if min(a, b) < 10: continue
            score = max(a, b) - (14 if WORDS[ws[c - 1]]['w'][-1] in ',:;' else 0)
            if best is None or score < best[0]: best = (score, c)
        if best is None: return [ws]
        return split(ws[:best[1]]) + split(ws[best[1]:])
    for s in sents: chunks += split(s)
    caps = []
    for k, c in enumerate(chunks):
        a = WORDS[c[0]]['s'] - 0.08
        b = WORDS[c[-1]]['e'] + 0.3
        if k + 1 < len(chunks): b = min(max(b, WORDS[chunks[k + 1][0]]['s'] - 0.08) if WORDS[chunks[k + 1][0]]['s'] - WORDS[c[-1]]['e'] < 1.0 else b, WORDS[chunks[k + 1][0]]['s'] - 0.08)
        caps.append(dict(a=a, b=min(b, SPEECH_END + 0.4), toks=disp_tokens(c)))
    return caps
CAPS = build_captions()

_capc = {}
def caption_sprite(ci, active_word, scene=False):
    k = (ci, active_word, scene)
    if k in _capc: return _capc[k]
    toks = CAPS[ci]['toks']; f = F('sb', 46 if not scene else 44)
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    sp = d.textlength(' ', font=f)
    widths = [d.textlength(t, font=f) for t, _ in toks]
    maxw = (CAP_W if not scene else 1500) - 60
    lines, cur, cw = [], [], 0
    for j, w_ in enumerate(widths):
        if cur and cw + sp + w_ > maxw: lines.append(cur); cur, cw = [j], w_
        else: cur.append(j); cw = cw + (sp if cur[:-1] else 0) + w_
    if cur: lines.append(cur)
    lines = lines[:2]
    lh = 60; bw = int(max(sum(widths[j] for j in ln) + sp * (len(ln) - 1) for ln in lines)) + 60; bh = lh * len(lines) + 28
    im = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle((0, 0, bw - 1, bh - 1), 22, fill=(8, 6, 14, 218))
    for li, ln in enumerate(lines):
        lw = sum(widths[j] for j in ln) + sp * (len(ln) - 1); x = (bw - lw) / 2; y = 12 + li * lh
        for j in ln:
            on = active_word in toks[j][1]
            dd.text((x, y + 4), toks[j][0], font=f, fill=LIME if on else WHITE)
            x += widths[j] + sp
    _capc[k] = im
    return im

# ------------------------------------------------------------------ card layout into animated elements
class El:
    def __init__(self, img, x, y, t_in, kind='pop', t_out=None, extra=None):
        self.img, self.x, self.y, self.t_in, self.kind, self.t_out, self.extra = img, int(x), int(y), t_in, kind, t_out, extra or {}

def kicker_sprite(t, center=False):
    f = F('sb', 23); ts = text_sprite(t, f, LIME, spacing=2)
    w, h = ts.width + 44, 50
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 25, fill=LIME + (26,), outline=LIME + (230,), width=2)
    im.alpha_composite(ts, (22, (h - ts.height) // 2 + 1))
    return im

def row_sprite(r, size, compact):
    f = F('sb', size); lines = wrap(r['t'], f, IW - 118); lh = int(size * 1.3)
    hgt = max(70 if compact else 90, lh * len(lines) + 32)
    im = Image.new('RGBA', (IW, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = r.get('c') or WHITE
    d.rounded_rectangle((0, 0, IW - 1, hgt - 1), 18, fill=CARD + (238,), outline=(col + (150,)) if r.get('c') else LINE + (255,), width=2)
    if r.get('c'): d.rounded_rectangle((0, 10, 6, hgt - 11), 3, fill=col + (255,))
    e = emoji_img(r['e'], 50 if not compact else 42); im.alpha_composite(e, (24, (hgt - e.height) // 2))
    ty = (hgt - lh * len(lines)) // 2 - 2
    for i, l in enumerate(lines): rich_draw(im, (100, ty + i * lh), l, f, col)
    return im

def layout_card(card, t0, t1, k0, k1):
    """Returns [El] positioned in frame coordinates."""
    els = card['els']; check = card.get('check')
    centered = any(e['k'] in ('emoji', 'photo', 'num', 'slogan') for e in els)
    blocks = []   # (height, [(sprite, dx(None=center), dy, at, kind, extra)])
    def at_time(phrase, default):
        if not phrase: return default
        k = find(phrase, k0, k1)
        if k is None:
            print('  missing element trigger:', phrase, '| card', card['at']); return default
        return max(t0 + 0.12, TOK_T[k] - 0.06)
    for e in els:
        k = e['k']
        if k == 'kicker':
            sp = kicker_sprite(e['t']); blocks.append((sp.height, [(sp, None if centered else 0, 0, None, 'pop', None)]))
        elif k in ('head', 'sub'):
            s = int(e.get('s', 60 if k == 'head' else 28) * 1.08); f = F('b' if k == 'head' else 'm', s)
            col = e.get('c', WHITE if k == 'head' else GREY)
            lines = wrap(e['t'], f, IW); lh = int(s * (1.12 if k == 'head' else 1.4)); parts = []
            for i, l in enumerate(lines):
                sp = text_sprite(l, f, col)
                parts.append((sp, None if (e.get('center') or centered) else 0, i * lh, e.get('at'), 'pop', None))
            blocks.append((lh * len(lines), parts))
        elif k == 'rows':
            s = int(e.get('s', 31) * 1.1); parts = []; y = 0
            for r in e['rows']:
                sp = row_sprite(r, s, e.get('compact')); parts.append((sp, 0, y, r.get('at'), 'row', None)); y += sp.height + 12
            blocks.append((y - 12, parts))
        elif k == 'calc':
            lines = e['lines']; s = 56; lh = int(s * 1.32); hgt = 92 + lh * len(lines) + 26
            box = Image.new('RGBA', (IW, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
            d.rounded_rectangle((0, 0, IW - 1, hgt - 1), 24, fill=(22, 17, 38, 245), outline=JP1 + (255,), width=3)
            box.alpha_composite(emoji_img('🧮', 40), (28, 22)); box.alpha_composite(text_sprite('THE MATHS', F('sb', 22), LIME, spacing=2), (84, 30))
            parts = [(box, 0, 0, None, 'pop', None)]
            for i, (ln, at) in enumerate(lines):
                last = i == len(lines) - 1
                sp = text_sprite(ln, F('b', s), LIME if last else WHITE)
                parts.append((sp, None, 84 + i * lh, at, 'row', None))
            blocks.append((hgt, parts))
        elif k == 'url':
            f = F('b', 48); ts = text_sprite(e['t'], f, (16, 13, 26)); w = min(IW, ts.width + 96); hh = 104
            im = Image.new('RGBA', (w, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rounded_rectangle((0, 0, w - 1, hh - 1), 48, fill=LIME + (255,)); im.alpha_composite(ts, ((w - ts.width) // 2, (hh - ts.height) // 2))
            blocks.append((hh, [(im, None, 0, e.get('at'), 'pop', None)]))
        elif k == 'chip':
            f = F('sb', 27); lines = wrap(e['t'], f, IW - 60); lh = 38; hh = lh * len(lines) + 28
            w = int(max(rich_width(ImageDraw.Draw(Image.new('RGBA', (8, 8))), l, f) for l in lines)) + 52
            im = Image.new('RGBA', (w, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rounded_rectangle((0, 0, w - 1, hh - 1), 22, fill=(40, 30, 64, 240), outline=PINK + (200,), width=2)
            for i, l in enumerate(lines): rich_draw(im, (26, 11 + i * lh), l, f, WHITE)
            blocks.append((hh, [(im, None if centered else 0, 0, e.get('at'), 'pop', None)]))
        elif k == 'strike':
            f1, f2 = F('b', 58), F('b', 70)
            a = text_sprite(e['old'], f1, (150, 142, 176)); b = text_sprite(e['new'], f2, LIME)
            line = Image.new('RGBA', (a.width + 20, 14), (0, 0, 0, 0)); ImageDraw.Draw(line).rounded_rectangle((0, 0, a.width + 19, 13), 7, fill=RED + (255,))
            blocks.append((a.height + 30 + b.height, [(a, 0, 0, None, 'pop', None), (line, -10, a.height // 2 - 2, None, 'strike', None),
                                                     (b, 0, a.height + 30, e.get('at2'), 'pop', None)]))
        elif k == 'emoji':
            sp = emoji_img(e['e'], 130); blocks.append((sp.height, [(sp, None, 0, e.get('at'), 'pop', None)]))
        elif k == 'photo':
            sp = photo_circle(e['d']); blocks.append((sp.height - 40, [(sp, None, -20, None, 'pop', None)]))
        elif k == 'sig':
            sp = text_sprite(e['t'], F('script', 76), GOLD); blocks.append((sp.height, [(sp, None, 0, e.get('at'), 'pop', None)]))
        elif k == 'split':
            parts = []
            parts.append((text_sprite('You keep 70%', F('b', 40), WHITE), 0, 0, None, 'pop', None))
            parts.append((text_sprite('$7 of every $10', F('m', 26), GREY), 0, 52, None, 'pop', None))
            parts.append((Image.new('RGBA', (IW, 34), (0, 0, 0, 0)), 0, 96, None, 'bar', dict(frac=0.7, col=GREEN)))
            parts.append((text_sprite('30% performance fee', F('b', 40), WHITE), 0, 168, e.get('at2'), 'pop', None))
            parts.append((Image.new('RGBA', (IW, 34), (0, 0, 0, 0)), 0, 264 - 40, e.get('at2'), 'bar', dict(frac=0.3, col=JP2)))
            yy = 290
            for i, (txt, at) in enumerate([('🏦 Broker', 'the broker'), ('🤖 Strategy provider', 'strategy provider'), ('👥 Partner program', 'partner program')]):
                f = F('sb', 24); w = int(rich_width(ImageDraw.Draw(Image.new('RGBA', (8, 8))), txt, f)) + 40
                im = Image.new('RGBA', (w, 50), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, 49), 25, fill=(40, 30, 64, 240), outline=JP1 + (220,), width=2)
                rich_draw(im, (20, 9), txt, f, WHITE)
                parts.append((im, [0, 210, 470][i] if i < 2 else 0, yy + (0 if i < 2 else 64), at, 'pop', None))
            blocks.append((yy + 114, parts))
        elif k == 'num':
            parts = []; n = e['n']
            parts.append((emoji_img(e['e'], 110), None, 0, None, 'pop', None))
            ck = text_sprite('CHECK', F('k', 46), WHITE, spacing=6); parts.append((ck, None, 130, None, 'pop', None))
            num = text_sprite(str(n), F('k', 230), grad=(JP1, JP2)); parts.append((num, None, 168, None, 'pop', None))
            of = text_sprite('OF 5', F('sb', 30), GREY, spacing=4); parts.append((of, None, 420, None, 'pop', None))
            q = text_sprite(e['q'], F('b', 54), WHITE); parts.append((q, None, 476, None, 'pop', None))
            hgt = 476 + q.height
            if e.get('note'):
                nt = text_sprite(e['note'], F('sb', 28), LIME); parts.append((nt, None, hgt + 14, e.get('note_at'), 'pop', None)); hgt += 14 + nt.height
            blocks.append((hgt, parts))
        elif k == 'slogan':
            parts = []; ph = photo_circle(200); parts.append((ph, None, -10, None, 'pop', None)); y = ph.height - 10
            for t, at in (('IT PAYS TO', None), ('PAY ATTENTION', 'pay attention'), ('& TAKE', 'and take'), ('ACTION', 'action')):
                sp = text_sprite(t, F('k', 74), LIME if t == 'ACTION' else WHITE, grad=(JP1, JP2) if t == 'PAY ATTENTION' else None)
                parts.append((sp, None, y, at, 'pop', None)); y += 84
            blocks.append((y, parts))
    gap = 28
    top = PY + (86 if check else 34); avail = PH - (86 if check else 34) - 30
    total = sum(h for h, _ in blocks) + gap * (len(blocks) - 1)
    if total > avail and len(blocks) > 1:
        gap = max(12, (avail - sum(h for h, _ in blocks)) // (len(blocks) - 1)); total = sum(h for h, _ in blocks) + gap * (len(blocks) - 1)
    if total > avail: print('  card too tall:', card['at'], total, '>', avail)
    y = top + max(0, (avail - total) // 2)
    out = []; stagger = 0
    for h, parts in blocks:
        for sp, dx, dy, at, kind, extra in parts:
            x = X0 + (IW - sp.width) // 2 if dx is None else X0 + dx
            ti = at_time(at, t0 + 0.1 + stagger * 0.07)
            if not at: stagger += 1
            out.append(El(sp, x, y + dy, ti, kind, t1 + 0.12, extra))
        y += h + gap
    return out

# timings for every card
CARD_T = []
pos = 0
for c in CV.CARDS:
    k = find(c['at'], pos)
    if k is None: print('MISSING card trigger:', c['at']); continue
    CARD_T.append([c, max(TL['cover'], TOK_T[k] - 0.12), k]); pos = k + 1
ELS, CHECK_AT = [], []
for i, (c, t0, k0) in enumerate(CARD_T):
    t1 = CARD_T[i + 1][1] if i + 1 < len(CARD_T) else END0
    k1 = CARD_T[i + 1][2] if i + 1 < len(CARD_T) else len(TOK)
    # the panel goes quiet during the full-screen scenes
    for sc in TL['scenes']:
        if t0 < sc['t0'] < t1: t1 = sc['t0']
    ELS += layout_card(c, t0, t1, k0, k1)
    CHECK_AT.append((t0, c.get('check')))
POPS = []
for ph, e in CV.POPS:
    k = find(ph)
    if k is None: print('missing pop:', ph); continue
    POPS.append((TOK_T[k] + 0.05, e))
POPS.sort()

# ------------------------------------------------------------------ full-screen scenes (the two new voice-over lines) and the end card
def scene_t(phrase, t0):
    k = find(phrase, next(i for i, t in enumerate(TOK_T) if t >= t0 - 0.01))
    return TOK_T[k] - 0.06 if k is not None else t0 + 0.2

def laptop_sprite(wid):
    th = Image.open(TRAIN).convert('RGBA'); sw = wid - 28; sh = int(sw * 9 / 16)
    th = th.resize((sw, sh), Image.LANCZOS)
    im = Image.new('RGBA', (wid + 60, sh + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((30, 0, 30 + wid - 1, sh + 28), 18, fill=(30, 24, 48, 255), outline=JP1 + (255,), width=2)
    im.alpha_composite(th, (44, 14))
    base = grad_fill((wid + 60, 22), (205, 189, 245), (60, 46, 96), vertical=True); m = Image.new('L', base.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, wid + 59, 21), 10, fill=255); base.putalpha(m); im.alpha_composite(base, (0, sh + 30))
    # play button
    pb = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); pd = ImageDraw.Draw(pb); pd.ellipse((0, 0, 119, 119), fill=(255, 255, 255, 240))
    pd.polygon([(48, 34), (48, 86), (90, 60)], fill=(26, 15, 46)); im.alpha_composite(pb, (30 + wid // 2 - 60, 14 + sh // 2 - 60))
    return im

def pill(text, size=30, fg=WHITE, fill=(40, 30, 64, 240), outline=PINK + (200,), pad=28, h=None):
    f = F('sb', size); d = ImageDraw.Draw(Image.new('RGBA', (8, 8))); w = int(rich_width(d, text, f)) + pad * 2; h = h or int(size * 2.1)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=fill, outline=outline, width=2)
    rich_draw(im, (pad, (h - size * 1.45) / 2), text, f, fg)
    return im

def scene_bg():
    im = Image.new('RGBA', (W, H), BG + (255,)); g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((-300, 100, 900, 1200), fill=JP1 + (70,)); gd.ellipse((1150, -200, 2200, 800), fill=JP2 + (40,)); gd.ellipse((900, 700, 2000, 1500), fill=LIME + (22,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(180)))
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gr = ImageDraw.Draw(grid)
    for x in range(0, W, 64): gr.line((x, 0, x, H), fill=(255, 255, 255, 7))
    for y in range(0, H, 64): gr.line((0, y, W, y), fill=(255, 255, 255, 7))
    im.alpha_composite(grid)
    return im

SCENES = []
def build_scenes():
    s1, s2 = TL['scenes']
    a = s1['t0']; els = []
    els.append(El(kicker_sprite('YOUR NEXT STEP'), 120, 200, a + 0.15))
    h1 = text_sprite('Watch the', F('k', 86), WHITE); h2 = text_sprite('step-by-step', F('k', 86), grad=(JP1, JP2)); h3 = text_sprite('training.', F('k', 86), WHITE)
    tw = scene_t('watch my', a)
    els += [El(h1, 112, 268, tw), El(h2, 112, 372, scene_t('step by step', a)), El(h3, 112, 476, scene_t('training', a))]
    els.append(El(pill('👆  Every tap, from sign-up to the promo', 32), 120, 640, scene_t('every tap', a)))
    els.append(El(pill('📱  Follow along on your phone', 32), 120, 730, scene_t('follow along', a)))
    els.append(El(pill('mtgtribe.com/jetup', 40, fg=(16, 13, 26), fill=LIME + (255,), outline=LIME + (255,), pad=40, h=92), 120, 850, scene_t('right after', a)))
    lap = laptop_sprite(820); els.append(El(lap, 1000, 250, scene_t('step by step', a), 'slide'))
    cap = pill('JetUP + TAG Markets sign-up training · 6 parts', 26, fill=(20, 16, 32, 230), outline=JP1 + (200,)); els.append(El(cap, 1000 + (lap.width - cap.width) // 2, 250 + lap.height + 22, scene_t('every tap', a)))
    SCENES.append(dict(t0=s1['t0'], t1=s1['t1'], els=els))
    b = s2['t0']; els = []
    els.append(El(kicker_sprite('COMMENT NOW'), 120, 170, b + 0.15))
    els.append(El(emoji_img('💬', 120), 1680, 150, b + 0.2))
    g1 = text_sprite('Comment the number', F('k', 78), WHITE); g2 = text_sprite('of the check you\'ll do first', F('k', 78), grad=(JP1, JP2))
    els += [El(g1, 112, 236, scene_t('comment the number', b)), El(g2, 112, 336, scene_t('of the check', b))]
    qs = ['Who holds my money?', 'Who regulates the broker?', 'Are the results real?', 'What can go wrong?', 'Can I get out?']
    t15 = scene_t('one to five', b)
    for i, q in enumerate(qs):
        tile = Image.new('RGBA', (316, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(tile)
        d.rounded_rectangle((0, 0, 315, 299), 28, fill=CARD + (245,), outline=(LIME if i == 3 else JP1) + (255,), width=3)
        n = text_sprite(str(i + 1), F('k', 120), grad=(JP1, JP2) if i != 3 else None, fill=LIME); tile.alpha_composite(n, ((316 - n.width) // 2, 14))
        for j, l in enumerate(wrap(q, F('sb', 28), 270)):
            sp = text_sprite(l, F('sb', 28), WHITE); tile.alpha_composite(sp, ((316 - sp.width) // 2, 186 + j * 40))
        els.append(El(tile, 120 + i * 340, 500, t15 + i * 0.12, 'row'))
    els.append(El(pill('🎬  The check most of you pick becomes my next video', 32, outline=LIME + (220,)), 120, 870, scene_t('most of you pick', b)))
    SCENES.append(dict(t0=s2['t0'], t1=s2['t1'], els=els))
build_scenes()

def endcard_els():
    a = END0; els = []
    ph = photo_circle(330); els.append(El(ph, 390 - ph.width // 2, 300 - ph.height // 2, a + 0.1))
    m = text_sprite('MTG', F('b', 110), GOLD); els.append(El(m, 390 - m.width // 2, 500, a + 0.25))
    s = text_sprite('Your Digital Architect', F('m', 40), WHITE); els.append(El(s, 390 - s.width // 2, 640, a + 0.35))
    sl = text_sprite("Let's Get This Crypto! 💪", F('b', 46), LIME); els.append(El(sl, 390 - sl.width // 2, 712, a + 0.45))
    nx = Image.new('RGBA', (960, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(nx)
    d.rounded_rectangle((0, 0, 959, 329), 30, fill=CARD + (250,), outline=LIME + (255,), width=3)
    lp = laptop_sprite(380); nx.alpha_composite(lp, (14, (330 - lp.height) // 2))
    nx.alpha_composite(text_sprite('NEXT', F('sb', 26), LIME, spacing=4), (470, 52))
    for j, l in enumerate(['Watch the', 'step-by-step', 'training']):
        nx.alpha_composite(text_sprite(l, F('b', 42), WHITE if j == 0 else LIME), (470, 88 + j * 54))
    nx.alpha_composite(text_sprite('mtgtribe.com/jetup', F('sb', 30), GREY), (470, 262))
    els.append(El(nx, 860, 150, a + 0.3))
    rows = [('👥', 'Join the tribe: mtgtribe.com/group'), ('✈️', 'Telegram  @mtgtribe'), ('📲', 'Check my bio')]
    for i, (e, t) in enumerate(rows):
        r = row_sprite(dict(e=e, t=t), 32, False).resize((960, 88)) if False else None
        im = Image.new('RGBA', (960, 92), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.rounded_rectangle((0, 0, 959, 91), 46, fill=CARD + (240,), outline=JP1 + (230,), width=2)
        im.alpha_composite(emoji_img(e, 48), (30, 22)); rich_draw(im, (100, 22), t, F('sb', 34), WHITE)
        els.append(El(im, 860, 510 + i * 110, a + 0.5 + i * 0.12))
    dc = text_sprite('Not financial advice. Trading involves risk. Only invest what you can afford to lose.', F('m', 28), GREY)
    els.append(El(dc, (W - dc.width) // 2, 1000, a + 0.8))
    return els
END_ELS = endcard_els()

# ------------------------------------------------------------------ chrome: brand bar, JetUP x TAG pill with the mark, url, check tracker
_chrome = {}
def chrome_sprite():
    if 'c' in _chrome: return _chrome['c']
    im = Image.new('RGBA', (W, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((PX, 30, PX + 520, 92), 31, fill=(16, 13, 26, 230), outline=GOLD + (255,), width=2)
    im.alpha_composite(face_small(50), (PX + 7, 36))
    d.text((PX + 68, 36), 'MTG', font=F('b', 36), fill=GOLD)
    d.text((PX + 160, 46), '|  Your Digital Architect', font=F('m', 24), fill=WHITE)
    x = PX + 544
    mk = Image.open(MARK).convert('RGBA'); mk.thumbnail((44, 44), Image.LANCZOS)
    f = F('b', 28); w = int(44 + 12 + d.textlength('JetUP', font=f) + 14 + d.textlength('×', font=F('m', 26)) + 14 + d.textlength('TAG Markets', font=f) + 48)
    d.rounded_rectangle((x, 32, x + w, 90), 29, fill=(16, 13, 26, 230), outline=(86, 74, 120), width=2)
    im.alpha_composite(mk, (x + 18, 39)); xx = x + 18 + 44 + 12
    jt = text_sprite('JetUP', f, grad=(JP1, JP2)); im.alpha_composite(jt, (int(xx), 41)); xx += d.textlength('JetUP', font=f) + 14
    d.text((xx, 61), '×', font=F('m', 26), fill=(170, 165, 190), anchor='lm'); xx += d.textlength('×', font=F('m', 26)) + 14
    d.text((xx, 61), 'TAG Markets', font=f, fill=LIME, anchor='lm')
    t = 'mtgtribe.com/jetup'; f2 = F('sb', 28); tw = d.textlength(t, font=f2)
    d.rounded_rectangle((W - 48 - tw - 48, 32, W - 48, 90), 29, fill=(16, 13, 26, 230), outline=LIME + (255,), width=2)
    d.text((W - 48 - tw - 24, 61), t, font=f2, fill=WHITE, anchor='lm')
    _chrome['c'] = im
    return im

def tracker_sprite(cur, pulse):
    k = ('trk', cur, round(pulse, 2))
    if k in _chrome: return _chrome[k]
    im = Image.new('RGBA', (IW, 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    gw = (IW - 4 * 10) / 5
    for i in range(5):
        x = i * (gw + 10); n = i + 1
        if n < cur: fill, tc, out = JP1 + (255,), WHITE, JP1
        elif n == cur: fill, tc, out = LIME + (255,), (16, 13, 26), LIME
        else: fill, tc, out = (30, 25, 46, 255), (120, 112, 150), LINE
        grow = 3 * pulse if n == cur else 0
        d.rounded_rectangle((x - grow, 6 - grow, x + gw + grow, 44 + grow), 19, fill=fill, outline=out + (255,), width=2)
        lab = f'CHECK {n}'
        f = F('sb', 17); tw = d.textlength(lab, font=f) + (20 if n < cur else 0)
        lx = x + gw / 2 - tw / 2
        if n < cur:
            d.line([(lx, 25), (lx + 5, 31), (lx + 13, 18)], fill=tc, width=3); lx += 20
        d.text((lx, 14), lab, font=f, fill=tc)
    _chrome[k] = im
    return im

# ------------------------------------------------------------------ animation helpers
def ease_back(p):
    c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2
def ease_out(p): return 1 - (1 - p) ** 3

def draw_el(base, el, t):
    if t < el.t_in or (el.t_out is not None and t > el.t_out + 0.2): return
    p = min(1.0, (t - el.t_in) / 0.32)
    a = min(1.0, (t - el.t_in) / 0.18)
    if el.t_out is not None and t > el.t_out - 0.18: a *= max(0.0, (el.t_out - t) / 0.18) if t < el.t_out else 0.0
    if a <= 0.01: return
    img = el.img; x, y = el.x, el.y
    if el.kind == 'bar':
        q = ease_out(min(1.0, (t - el.t_in) / 0.7)); fr = el.extra['frac'] * q
        img = Image.new('RGBA', el.img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(img); w, h = img.size
        d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=(255, 255, 255, 16), outline=(255, 255, 255, 30), width=1)
        if fr > 0.02: d.rounded_rectangle((0, 0, int((w - 1) * fr), h - 1), h // 2, fill=el.extra['col'] + (255,))
    elif el.kind == 'strike':
        q = ease_out(min(1.0, max(0.0, (t - el.t_in - 0.25) / 0.35)))
        if q <= 0: return
        img = el.img.crop((0, 0, max(1, int(el.img.width * q)), el.img.height))
    elif el.kind == 'slide':
        dx = int((1 - ease_out(p)) * 140); x += dx
    else:
        s = 0.86 + 0.14 * ease_back(p) if el.kind == 'pop' else 1.0
        dy = int((1 - ease_out(p)) * (18 if el.kind == 'row' else 10)); y += dy
        if el.kind == 'row': x += int((1 - ease_out(p)) * -24)
        if abs(s - 1) > 0.004:
            nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
            img = img.resize((nw, nh), Image.BILINEAR); x += (el.img.width - nw) // 2; y += (el.img.height - nh) // 2
    if a < 0.999:
        img = img.copy(); al = img.split()[3].point(lambda v, a=a: int(v * a)); img.putalpha(al)
    base.alpha_composite(img, (int(x), int(y)))

_pop_sprites = {}
def draw_pops(base, t):
    for i, (t0, e) in enumerate(POPS):
        dt = t - t0
        if dt < 0 or dt > 1.25: continue
        x0, y0 = [(1700, 430), (1745, 560), (1690, 330)][i % 3]
        p = min(1.0, dt / 0.3); s = 0.4 + 0.6 * ease_back(p); a = 1.0 if dt < 0.95 else max(0.0, (1.25 - dt) / 0.3)
        im = emoji_img(e, int(118 * s)); y = y0 - int(dt * 36)
        if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v, a=a: int(v * a)))
        base.alpha_composite(im, (x0 + (118 - im.width) // 2, y + (118 - im.height) // 2))
        if dt < 0.6:   # little burst
            d = ImageDraw.Draw(base); q = dt / 0.6
            for k in range(10):
                ang = k * 2 * math.pi / 10 + i; r = 40 + 110 * ease_out(q); cx, cy = x0 + 59 + math.cos(ang) * r, y0 + 59 + math.sin(ang) * r
                rad = 7 * (1 - q) + 1; col = [LIME, JP2, JP1][k % 3] + (int(230 * (1 - q)),)
                d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=col)

def caption_at(t):
    for ci, c in enumerate(CAPS):
        if c['a'] <= t < c['b']:
            act = None
            for j, w in enumerate(WORDS):
                if w['s'] - 0.04 <= t < (WORDS[j + 1]['s'] - 0.04 if j + 1 < len(WORDS) else w['e'] + 0.3): act = j; break
            return ci, act
    return None, None

def check_at(t):
    cur = None; since = 0
    for t0, ch in CHECK_AT:
        if t0 <= t: cur, since = ch, t0
    return cur, since

# ------------------------------------------------------------------ the cover (thumbnail, first second)
def cover_img(still):
    im = Image.new('RGBA', (W, H), BG + (255,))
    av = Image.fromarray(still).convert('RGBA'); im.alpha_composite(av, (SHIFT, 0))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for x in range(1100): gd.line((x, 0, x, H), fill=BG + (int(255 * min(1, max(0, (1100 - x) / 460))),))
    im.alpha_composite(g)
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((-300, 150, 900, 1050), fill=JP1 + (60,)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(140)))
    im.alpha_composite(chrome_sprite(), (0, 0))
    im.alpha_composite(text_sprite('LOST MONEY', F('b', 122), WHITE), (76, 280))
    im.alpha_composite(text_sprite('BEFORE?', F('b', 158), grad=(JP1, JP2)), (76, 410))
    im.alpha_composite(text_sprite('Check these 5 things', F('sb', 56), WHITE), (82, 640))
    im.alpha_composite(text_sprite('before you try again.', F('sb', 56), LIME), (82, 712))
    im.alpha_composite(pill('JetUP  ×  TAG Markets', 34, fg=WHITE, fill=(16, 13, 26, 230), outline=(86, 74, 120, 255), pad=34, h=78), (84, 830))
    return np.array(im.convert('RGB'))

# ------------------------------------------------------------------ one output frame
_dis = None
def interp(fa, fb, q):
    global _dis
    if _dis is None: _dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_FAST)
    sa = cv2.cvtColor(cv2.resize(fa, (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY)
    sb = cv2.cvtColor(cv2.resize(fb, (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY)
    fab = cv2.resize(_dis.calc(sa, sb, None), (W, H)) * 2; fba = cv2.resize(_dis.calc(sb, sa, None), (W, H)) * 2
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    wa = cv2.remap(fa, gx - q * fab[..., 0], gy - q * fab[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(fb, gx - (1 - q) * fba[..., 0], gy - (1 - q) * fba[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return cv2.addWeighted(wa, 1 - q, wb, q, 0)

ZOOM_EVENTS = sorted([c for c in TL['cuts']] + [s['t1'] for s in TL['scenes']] + [t for (c, t, k) in CARD_T if c.get('els') and c['els'][0]['k'] == 'num'])
def zoom_at(t):
    z = 0
    for e in ZOOM_EVENTS:
        if e <= t: z ^= 1
    return ZOOM_IN if z else 1.0

def compose(t, src):
    z = zoom_at(t)
    if z != 1.0:
        cw, ch = W / z, H / z; x0, y0 = Z_AX - Z_AX / z, Z_AY - Z_AY / z
        M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]]); src = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR)
    bg = cv2.resize(cv2.GaussianBlur(cv2.resize(src, (240, 135), interpolation=cv2.INTER_AREA), (0, 0), 3), (W, H), interpolation=cv2.INTER_LINEAR)
    bg = (bg.astype(np.float32) * 0.78).astype(np.uint8)
    out = bg; out[:, SHIFT:] = src[:, :W - SHIFT]
    reg = out[PY:PY + PH, PX:PX + PW]
    out[PY:PY + PH, PX:PX + PW] = cv2.resize(cv2.GaussianBlur(cv2.resize(reg, (PW // 4, PH // 4), interpolation=cv2.INTER_AREA), (0, 0), 4), (PW, PH))
    im = Image.fromarray(out).convert('RGBA')
    pan = _chrome.get('panel')
    if pan is None:
        pan = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(pan)
        d.rounded_rectangle((0, 0, PW - 1, PH - 1), 30, fill=(14, 11, 24, 206), outline=JP1 + (255,), width=2)
        d.line((40, 1, PW - 40, 1), fill=JP2 + (190,), width=2); _chrome['panel'] = pan
    im.alpha_composite(pan, (PX, PY))
    cur, since = check_at(t)
    if cur:
        im.alpha_composite(tracker_sprite(cur, max(0.0, 1 - (t - since) / 0.35) if t - since < 0.35 else 0.0), (X0, PY + 22))
    for el in ELS:
        if el.t_in - 0.01 <= t <= (el.t_out or 1e9) + 0.25: draw_el(im, el, t)
    draw_pops(im, t)
    im.alpha_composite(chrome_sprite(), (0, 0))
    ci, act = caption_at(t)
    if ci is not None:
        cs = caption_sprite(ci, act); im.alpha_composite(cs, (CAP_CX - cs.width // 2, CAP_B - cs.height))
    # full-screen scenes
    for sc in SCENES:
        if sc['t0'] - 0.01 <= t <= sc['t1'] + 0.35:
            a = min(1.0, (t - sc['t0']) / 0.3) if t < sc['t0'] + 0.3 else (max(0.0, 1 - (t - sc['t1']) / 0.3) if t > sc['t1'] else 1.0)
            layer = scene_bg()
            for el in sc['els']: draw_el(layer, el, t)
            layer.alpha_composite(chrome_sprite(), (0, 0))
            if ci is not None:
                cs = caption_sprite(ci, act, True); layer.alpha_composite(cs, (W // 2 - cs.width // 2, CAP_B - cs.height + 10))
            im = Image.blend(im, layer, a) if a < 1 else layer
    if t >= END0 - 0.4:
        a = min(1.0, (t - (END0 - 0.4)) / 0.4)
        layer = scene_bg()
        for el in END_ELS: draw_el(layer, el, t)
        im = Image.blend(im, layer, a) if a < 1 else layer
    return np.array(im.convert('RGB'))

_scene_bg = None
_sbg = scene_bg
def scene_bg():
    global _scene_bg
    if _scene_bg is None: _scene_bg = _sbg()
    return _scene_bg.copy()

# ------------------------------------------------------------------ source frames and workers
def reader(start):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{start / FPS:.4f}', '-i', AVATAR, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
    return p

def src_getter(start):
    p = reader(start); state = dict(i=start - 1, cur=None, prev=None, p=p)
    def get(n):
        n = max(start, n)
        while state['i'] < n:
            raw = p.stdout.read(W * H * 3)
            if len(raw) < W * H * 3: break
            state['prev'], state['cur'] = state['cur'], np.frombuffer(raw, np.uint8).reshape(H, W, 3)
            state['i'] += 1
        return state
    return get

XF = TL['xfades']
def frame_at(f, get):
    t = f / FPS
    v = min(TL['frames'][f], NSRC - 2)
    if t < TL['cover']:
        st = get(int(v) + 3); return cover_img(st['cur'].copy())
    n = int(math.floor(v)); q = v - n
    nxt_v = min(TL['frames'][min(f + 1, NFR - 1)], NSRC - 2); prv_v = min(TL['frames'][max(f - 1, 0)], NSRC - 2)
    slow = (nxt_v - prv_v) / 2 < 0.97
    if slow and 0.18 < q < 0.82:
        st = get(n + 1); fa, fb = st['prev'], st['cur']
        src = interp(fa, fb, q) if fa is not None else fb.copy()
    else:
        st = get(int(round(v))); src = st['cur'].copy()
    # soft blend across a skipped stretch of an old pause
    for x in XF:
        if 0 <= t - x < 3 / FPS and f > 0:
            pass
    return compose(t, src)

def render_range(a, b, out):
    start = max(0, min(int(min(TL['frames'][a:b])) - 1, NSRC - 3))
    get = src_getter(start)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-g', '50', '-threads', '1', out], stdin=subprocess.PIPE)
    prev = None
    for f in range(a, b):
        fr = frame_at(f, get)
        t = f / FPS
        if prev is not None and any(0 <= t - x < 2.5 / FPS for x in XF):
            fr = cv2.addWeighted(prev, 0.5, fr, 0.5, 0)
        enc.stdin.write(fr.tobytes()); prev = fr
    enc.stdin.close(); enc.wait()

if __name__ == '__main__':
    if sys.argv[1] == 'frame':
        t = float(sys.argv[2]); f = int(round(t * FPS)); v = TL['frames'][f]
        get = src_getter(max(0, min(int(v), NSRC - 3) - 2))
        Image.fromarray(frame_at(f, get)).save(sys.argv[3]); print('saved', sys.argv[3], 'src', v)
    elif sys.argv[1] == 'range':
        render_range(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif sys.argv[1] == 'info':
        print('cards', len(CARD_T), 'elements', len(ELS), 'captions', len(CAPS), 'pops', len(POPS), 'frames', NFR)
        json.dump(dict(cards=[t for _, t, _ in CARD_T], els=[(e.t_in, e.kind) for e in ELS], pops=[p[0] for p in POPS],
                       scenes=[(s['t0'], s['t1'], [(e.t_in, e.kind) for e in s['els']]) for s in SCENES], end=END0,
                       checks=[t for (c, t, k) in CARD_T if c['els'][0]['k'] == 'num']), open(os.path.join(HERE, 'events.json'), 'w'))
