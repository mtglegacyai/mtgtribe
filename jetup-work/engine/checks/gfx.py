# MTG brand graphics for the JetUP "5 Checks" vertical video (1080x1920)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1080, 1920
AV_Y, AV_H = 150, 608            # avatar window (16:9 at full width)
PANEL_Y, PANEL_H = 790, 760      # card panel
CAP_Y = 1585                     # caption block top
GOLD = (232, 194, 90); GOLD2 = (201, 160, 52); WHITE = (245, 245, 240)
GREY = (160, 160, 168); BG = (13, 13, 16); CARD = (26, 26, 31); LINE = (52, 52, 60)
RED = (232, 86, 76); GREEN = (76, 200, 120)
FD = '/usr/share/fonts/truetype/google-fonts/'
EMO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'


def F(w, s):
    return ImageFont.truetype(FD + {'b': 'Poppins-Bold.ttf', 'sb': 'Poppins-SemiBold.ttf', 'm': 'Poppins-Medium.ttf',
                                    'r': 'Poppins-Regular.ttf', 'l': 'Poppins-Light.ttf'}.get(w, 'Poppins-Bold.ttf'), s)


if not os.path.exists(FD + 'Poppins-SemiBold.ttf'):
    _F = F
    def F(w, s):
        return _F('b' if w == 'sb' else w, s)

_emo = ImageFont.truetype(EMO, 109)


def emoji(img, ch, x, y, size):
    t = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((0, 0), ch, font=_emo, embedded_color=True)
    bb = t.getbbox()
    if not bb:
        return
    t = t.crop(bb)
    t = t.resize((size, int(size * t.height / t.width)), Image.LANCZOS)
    img.alpha_composite(t, (int(x), int(y)))


def wrap(d, text, font, maxw):
    out = []
    for para in text.split('\n'):
        words, line = para.split(' '), ''
        for w in words:
            t = (line + ' ' + w).strip()
            if d.textlength(t, font=font) <= maxw:
                line = t
            else:
                if line:
                    out.append(line)
                line = w
        out.append(line)
    return out


def tsize(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1]


def base():
    im = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(im)
    # soft gold glow behind the panel
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse((-200, 900, 1280, 1700), fill=(201, 160, 52, 26))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))
    # top bar
    emoji(im, '👑', 40, 46, 56)
    d.text((110, 44), 'MTG', font=F('b', 44), fill=GOLD)
    d.text((215, 56), '|  Your Digital Architect', font=F('m', 30), fill=WHITE)
    pill = 'JetUP · 5 CHECKS'
    pw = d.textlength(pill, font=F('sb', 24)) + 40
    d.rounded_rectangle((W - 40 - pw, 50, W - 40, 100), 25, outline=GOLD, width=2)
    d.text((W - 40 - pw + 20, 58), pill, font=F('sb', 24), fill=GOLD)
    # avatar frame lines
    d.line((0, AV_Y - 2, W, AV_Y - 2), fill=GOLD2, width=3)
    d.line((0, AV_Y + AV_H + 1, W, AV_Y + AV_H + 1), fill=GOLD2, width=3)
    # footer
    d.text((W // 2, 1872), 'mtgtribe.com/jetup', font=F('sb', 30), fill=GREY, anchor='mm')
    return im


def card(c):
    """Render one card dict into a transparent 1080 x PANEL_H layer."""
    im = Image.new('RGBA', (W, PANEL_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    X0, X1 = 54, W - 54
    blocks = []   # (height, drawfn)

    if c.get('kicker'):
        f = F('sb', 30)
        def k(y, t=c['kicker'], f=f):
            tw = d.textlength(t, font=f)
            d.rounded_rectangle((X0, y, X0 + tw + 44, y + 54), 27, fill=(201, 160, 52, 40), outline=GOLD, width=2)
            d.text((X0 + 22, y + 8), t, font=f, fill=GOLD)
        blocks.append((54, k))
    if c.get('head'):
        size = c.get('hs', 76)
        f = F('b', size)
        lines = wrap(d, c['head'], f, X1 - X0)
        lh = int(size * 1.18)
        col = c.get('hc', WHITE)
        ctr = bool(c.get('big_emoji') or c.get('center'))
        def h(y, lines=lines, f=f, lh=lh, col=col, ctr=ctr):
            for i, l in enumerate(lines):
                if ctr:
                    d.text((W // 2, y + i * lh), l, font=f, fill=col, anchor='ma')
                else:
                    d.text((X0, y + i * lh), l, font=f, fill=col)
        blocks.append((lh * len(lines), h))
    if c.get('strike'):
        f = F('b', 66)
        t1, t2 = c['strike']
        def s(y, f=f, t1=t1, t2=t2):
            tw, th = tsize(d, t1, f)
            d.text((X0, y), t1, font=f, fill=GREY)
            d.line((X0 - 6, y + 52, X0 + tw + 6, y + 40), fill=RED, width=9)
            d.text((X0, y + 100), t2, font=F('b', 72), fill=GOLD)
        blocks.append((200, s))
    if c.get('rows'):
        f = F('sb', c.get('rs', 40))
        rows = []
        for r in c['rows']:
            em, txt = r[0], r[1]
            col = r[2] if len(r) > 2 else WHITE
            ls = wrap(d, txt, f, X1 - X0 - 130)
            rows.append((em, ls, col))
        lh = int(c.get('rs', 40) * 1.3)
        hts = [max(c.get('rmin', 96), len(ls) * lh + 36) for _, ls, _ in rows]
        gap = 16
        def r_(y, rows=rows, f=f, lh=lh, hts=hts):
            for (em, ls, col), ht in zip(rows, hts):
                d.rounded_rectangle((X0, y, X1, y + ht), 22, fill=CARD + (240,), outline=LINE, width=2)
                if em:
                    es = min(60, ht - 30); emoji(im, em, X0 + 26, y + ht // 2 - es // 2, es)
                ty = y + (ht - len(ls) * lh) // 2 - 4
                for i, l in enumerate(ls):
                    d.text((X0 + 110, ty + i * lh), l, font=f, fill=col)
                y += ht + gap
        blocks.append((sum(hts) + gap * (len(hts) - 1), r_))
    if c.get('calc'):
        f = F('b', c.get('cs', 58))
        lines = c['calc']
        lh = int(c.get('cs', 58) * 1.35)
        ht = 90 + lh * len(lines) + 30
        def cl(y, lines=lines, f=f, lh=lh, ht=ht):
            d.rounded_rectangle((X0, y, X1, y + ht), 28, fill=(20, 18, 10, 245), outline=GOLD, width=3)
            emoji(im, '🧮', X0 + 30, y + 22, 48)
            d.text((X0 + 96, y + 26), c.get('ctitle', 'THE MATHS'), font=F('sb', 30), fill=GOLD)
            for i, l in enumerate(lines):
                col = GOLD if (i == len(lines) - 1 and c.get('chl', True)) else WHITE
                d.text((W // 2, y + 90 + i * lh + lh // 2), l, font=f, fill=col, anchor='mm')
        blocks.append((ht, cl))
    if c.get('url'):
        f = F('b', c.get('us', 74))
        def u(y, t=c['url'], f=f):
            tw, th = tsize(d, t, f)
            pw = min(X1 - X0, tw + 80)
            x = (W - pw) // 2
            d.rounded_rectangle((x, y, x + pw, y + 150), 75, fill=GOLD)
            d.text((W // 2, y + 75), t, font=f, fill=(15, 12, 5), anchor='mm')
        blocks.append((150, u))
    if c.get('sub'):
        f = F('m', c.get('ss', 36))
        lines = wrap(d, c['sub'], f, X1 - X0)
        lh = int(c.get('ss', 36) * 1.35)
        def sb(y, lines=lines, f=f, lh=lh):
            for i, l in enumerate(lines):
                d.text((W // 2 if c.get('subc') else X0, y + i * lh), l, font=f, fill=GREY,
                       anchor='ma' if c.get('subc') else 'la')
        blocks.append((lh * len(lines), sb))
    if c.get('big_emoji'):
        def be(y, e=c['big_emoji']):
            emoji(im, e, W // 2 - 90, y, 180)
        blocks.insert(0, (180, be))

    gap = 30
    total = sum(h for h, _ in blocks) + gap * (len(blocks) - 1)
    card.last_total = total
    y = max(10, (PANEL_H - total) // 2)
    for h, fn in blocks:
        fn(y)
        y += h + gap
    return im


def caption_layer(text):
    im = Image.new('RGBA', (W, 230), (0, 0, 0, 0))
    if not text:
        return im
    d = ImageDraw.Draw(im)
    f = F('sb', 50)
    lines = wrap(d, text, f, W - 140)[:2]
    lh = 66
    th = lh * len(lines) + 30
    y0 = (230 - th) // 2
    wmax = max(d.textlength(l, font=f) for l in lines)
    d.rounded_rectangle(((W - wmax) / 2 - 34, y0, (W + wmax) / 2 + 34, y0 + th), 24, fill=(0, 0, 0, 200))
    for i, l in enumerate(lines):
        d.text((W // 2, y0 + 15 + i * lh + lh // 2), l, font=f, fill=WHITE, anchor='mm')
    return im


def frame(card_layer, cap):
    im = base()
    if card_layer is not None:
        im.alpha_composite(card_layer, (0, PANEL_Y))
    im.alpha_composite(caption_layer(cap), (0, CAP_Y))
    return im.convert('RGB')


def cover(still):
    """Thumbnail cover: avatar still on top, hook text below."""
    im = Image.new('RGBA', (W, H), BG + (255,))
    av = still.convert('RGBA').resize((1920 * 1150 // 1080, 1150), Image.LANCZOS)
    x = (av.width - W) // 2 + 120
    im.alpha_composite(av.crop((x, 0, x + W, 1150)), (0, 0))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for i in range(500):
        gd.line((0, 700 + i, W, 700 + i), fill=BG + (min(255, int(i * 0.75)),))
    gd.rectangle((0, 1199, W, H), fill=BG + (255,))
    for i in range(160):
        gd.line((0, i, W, i), fill=BG + (int(220 * (1 - i / 160)),))
    im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    emoji(im, '👑', 40, 46, 56)
    d.text((110, 44), 'MTG', font=F('b', 44), fill=GOLD)
    d.text((215, 56), '|  Your Digital Architect', font=F('m', 30), fill=WHITE)
    d.text((W // 2, 1150), 'LOST MONEY', font=F('b', 120), fill=WHITE, anchor='mm')
    d.text((W // 2, 1290), 'BEFORE?', font=F('b', 150), fill=GOLD, anchor='mm')
    d.text((W // 2, 1440), 'Check these 5 things', font=F('sb', 56), fill=WHITE, anchor='mm')
    d.text((W // 2, 1515), 'before you try again.', font=F('sb', 56), fill=WHITE, anchor='mm')
    d.rounded_rectangle((180, 1610, 900, 1700), 45, outline=GOLD, width=3)
    d.text((W // 2, 1655), 'JetUP  ·  TAG Markets', font=F('sb', 40), fill=GOLD, anchor='mm')
    d.text((W // 2, 1800), 'mtgtribe.com/jetup', font=F('b', 46), fill=WHITE, anchor='mm')
    return im.convert('RGB')


def endcard():
    im = base()
    d = ImageDraw.Draw(im)
    d.rectangle((0, AV_Y, W, AV_Y + AV_H), fill=BG)
    emoji(im, '👑', W // 2 - 110, 260, 220)
    d.text((W // 2, 600), 'MTG', font=F('b', 150), fill=GOLD, anchor='mm')
    d.text((W // 2, 720), 'Your Digital Architect', font=F('m', 52), fill=WHITE, anchor='mm')
    d.text((W // 2, 900), "Let's Get This Crypto! ", font=F('b', 66), fill=WHITE, anchor='mm')
    emoji(im, '💪', W // 2 + 360, 860, 76)
    rows = [('🌐', 'mtgtribe.com/jetup'), ('👥', 'mtgtribe.com/group'), ('✈️', 'Telegram  @mtgtribe'), ('📲', 'Check my bio')]
    y = 1040
    for e, t in rows:
        d.rounded_rectangle((140, y, 940, y + 110), 55, fill=CARD, outline=GOLD, width=2)
        emoji(im, e, 180, y + 25, 60)
        d.text((270, y + 55), t, font=F('sb', 46), fill=WHITE, anchor='lm')
        y += 135
    d.text((W // 2, 1640), 'Not financial advice. Trading involves risk.', font=F('m', 34), fill=GREY, anchor='mm')
    d.text((W // 2, 1690), 'Only invest what you can afford to lose.', font=F('m', 34), fill=GREY, anchor='mm')
    return im.convert('RGB')
