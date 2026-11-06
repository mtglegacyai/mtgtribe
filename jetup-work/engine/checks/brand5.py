# JetUP + TAG Markets rebrand for the "5 Checks" video (v4): same layout and timing as v3, new theme.
# JetUP purple / pink, TAG Markets lime, near-black base (as in the sign-up training); MTG's gold stays for his signature;
# MTG's profile photo (mtgTribe.com tee) replaces the crown wherever it stood for MTG.
import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import gfx, gfx16
sys.path.insert(0, '/home/claude/face')
from make_profile import badge as _badge
from photo_card import photo_card

PURPLE, PINK, LIME = (140, 108, 231), (227, 113, 252), (203, 251, 97)
MTG_GOLD = (232, 194, 90)
BG, CARD, LINE = (11, 9, 18), (24, 20, 36), (52, 44, 74)
FACE = cv2.imread('/home/claude/face/p4_square.png')

# ---- theme constants used by the card engine
gfx.BG, gfx.CARD, gfx.LINE = BG, CARD, LINE
gfx.GOLD, gfx.GOLD2 = LIME, PURPLE            # accents: highlighted heads, maths answers, url pill
gfx16.BG, gfx16.CARD, gfx16.GOLD = BG, CARD, LIME
F, emoji, W16, H16 = gfx.F, gfx.emoji, gfx16.W, gfx16.H

_cache = {}
def face_badge(size):
    if size not in _cache:
        b = _badge(FACE, 600)
        _cache[size] = b.resize((size, size), Image.LANCZOS)
    return _cache[size].copy()

def face_small(d):
    k = ('s', d)
    if k not in _cache:
        rgb = Image.fromarray(cv2.cvtColor(FACE, cv2.COLOR_BGR2RGB)).resize((d * 4, d * 4), Image.LANCZOS)
        im = Image.new('RGBA', (d * 4, d * 4), (0, 0, 0, 0)); m = Image.new('L', (d * 4, d * 4), 0)
        ImageDraw.Draw(m).ellipse([6, 6, d * 4 - 7, d * 4 - 7], fill=255); f = rgb.convert('RGBA'); f.putalpha(m); im.alpha_composite(f)
        ImageDraw.Draw(im).ellipse([3, 3, d * 4 - 4, d * 4 - 4], outline=MTG_GOLD + (255,), width=10)
        _cache[k] = im.resize((d, d), Image.LANCZOS)
    return _cache[k]

def grad_text(img, xy, text, font, c1=PURPLE, c2=PINK, anchor='la'):
    d = ImageDraw.Draw(img); bb = d.textbbox(xy, text, font=font, anchor=anchor)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    if w <= 0 or h <= 0: return
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((xy[0] - bb[0], xy[1] - bb[1]), text, font=font, fill=255, anchor=anchor)
    g = np.zeros((h, w, 4), np.uint8); t = np.linspace(0, 1, w)[None, :]
    for i in range(3): g[..., i] = (c1[i] * (1 - t) + c2[i] * t).astype(np.uint8)
    g[..., 3] = np.array(m); img.alpha_composite(Image.fromarray(g), (bb[0], bb[1]))

def brand_pair(img, x, y, h=58, size=28):
    """JetUP x TAG Markets pill, left edge x, top y"""
    d = ImageDraw.Draw(img); f = F('b', size)
    w = int(d.textlength('JetUP', font=f) + d.textlength('×', font=F('m', size - 2)) + d.textlength('TAG Markets', font=f) + 28 * 2 + 40)
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=(16, 13, 26, 225), outline=(80, 70, 110), width=2)
    cy = y + h // 2; xx = x + 28
    grad_text(img, (xx, cy), 'JetUP', f, anchor='lm'); xx += d.textlength('JetUP', font=f) + 14
    d.text((xx, cy), '×', font=F('m', size - 2), fill=(170, 165, 190), anchor='lm'); xx += d.textlength('×', font=F('m', size - 2)) + 14
    d.text((xx, cy), 'TAG Markets', font=f, fill=LIME, anchor='lm')
    return w

# ---- cards: re-colour the hard-coded chip and maths-box fills, then put MTG's face on the MTG card
import inspect
_src = inspect.getsource(gfx.card)
for old, rep in (("fill=(201, 160, 52, 40), outline=GOLD", "fill=(140, 108, 231, 55), outline=(140, 108, 231)"),
                 ("fill=(20, 18, 10, 245), outline=GOLD", "fill=(22, 17, 38, 245), outline=(140, 108, 231)"),
                 ("fill=(15, 12, 5), anchor='mm')", "fill=(16, 13, 26), anchor='mm')")):
    assert old in _src, old
    _src = _src.replace(old, rep)
exec(compile(_src, gfx.__file__, 'exec'), gfx.__dict__)
_card0 = gfx.card
def card(c):
    if c.get('big_emoji') == '👑' and c.get('head') == 'MTG':     # MTG card: full photo, then name and line
        im = Image.new('RGBA', (gfx.W, gfx.PANEL_H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        ph = photo_card(560); im.alpha_composite(ph, (gfx.W // 2 - ph.width // 2, 20))
        y = 20 + ph.height - 10
        d.text((gfx.W // 2, y), 'MTG', font=F('b', 104), fill=MTG_GOLD, anchor='ma')
        lines = gfx.wrap(d, c.get('sub', ''), F('m', 36), gfx.W - 108)
        for i, l in enumerate(lines): d.text((gfx.W // 2, y + 140 + i * 48), l, font=F('m', 36), fill=(170, 165, 190), anchor='ma')
        gfx.card.last_total = gfx.PANEL_H
        return im
    return _card0(c)
gfx.card = card

# ---- 16:9 chrome, panel, cover, end card
def chrome(img):
    d = ImageDraw.Draw(img); PX = gfx16.PX
    d.rounded_rectangle((PX, 30, PX + 520, 92), 31, fill=(16, 13, 26, 225), outline=MTG_GOLD, width=2)
    img.alpha_composite(face_small(50), (PX + 12, 36))
    d.text((PX + 72, 36), 'MTG', font=F('b', 36), fill=MTG_GOLD)
    d.text((PX + 160, 46), '|  Your Digital Architect', font=F('m', 24), fill=gfx.WHITE)
    brand_pair(img, PX + 520 + 24, 32)
    t = 'mtgtribe.com/jetup'; f = F('sb', 28); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W16 - 48 - tw - 48, 32, W16 - 48, 90), 29, fill=(16, 13, 26, 225), outline=LIME, width=2)
    d.text((W16 - 48 - tw - 24, 61), t, font=f, fill=gfx.WHITE, anchor='lm')
gfx16.chrome = chrome

def overlay(card_layer, cap):
    PX, PY, PW, PH = gfx16.PX, gfx16.PY, gfx16.PW, gfx16.PH
    im = Image.new('RGBA', (W16, H16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((PX, PY, PX + PW, PY + PH), 30, fill=(14, 11, 24, 205), outline=PURPLE + (255,), width=2)
    d.line((PX + 40, PY + 1, PX + PW - 40, PY + 1), fill=PINK + (180,), width=2)      # thin JetUP highlight on the top edge
    if card_layer is not None: im.alpha_composite(card_layer, (PX, PY))
    chrome(im); gfx16.caption(im, cap)
    return im
gfx16.overlay = overlay

def cover(still):
    im = Image.new('RGBA', (W16, H16), BG + (255,))
    av = still.convert('RGBA').resize((W16, H16), Image.LANCZOS)
    im.alpha_composite(av, (gfx16.SHIFT, 0))
    g = Image.new('RGBA', (W16, H16), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for x in range(1000): gd.line((x, 0, x, H16), fill=BG + (int(255 * min(1, max(0, (1000 - x) / 420))),))
    im.alpha_composite(g)
    glow = Image.new('RGBA', (W16, H16), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((-300, 150, 900, 1050), fill=PURPLE + (60,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(140)))
    d = ImageDraw.Draw(im); chrome(im)
    d.text((80, 300), 'LOST MONEY', font=F('b', 118), fill=gfx.WHITE)
    grad_text(im, (80, 430), 'BEFORE?', F('b', 150), PURPLE, PINK)
    d.text((84, 630), 'Check these 5 things', font=F('sb', 54), fill=gfx.WHITE)
    d.text((84, 700), 'before you try again.', font=F('sb', 54), fill=LIME)
    brand_pair(im, 84, 810, h=80, size=36)
    return im.convert('RGB')
gfx16.cover = cover

def endcard():
    im = Image.new('RGBA', (W16, H16), BG + (255,))
    g = Image.new('RGBA', (W16, H16), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((-100, 150, 900, 1150), fill=PURPLE + (55,)); gd.ellipse((1100, 300, 2100, 1300), fill=LIME + (22,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(170)))
    d = ImageDraw.Draw(im)
    ph = photo_card(400); im.alpha_composite(ph, (390 - ph.width // 2, 245 - ph.height // 2))
    d.text((390, 540), 'MTG', font=F('b', 120), fill=MTG_GOLD, anchor='mm')
    d.text((390, 630), 'Your Digital Architect', font=F('m', 44), fill=gfx.WHITE, anchor='mm')
    d.text((390, 730), "Let's Get This Crypto!", font=F('b', 50), fill=gfx.WHITE, anchor='mm')
    emoji(im, '💪', 672, 698, 62)
    rows = [('🌐', 'mtgtribe.com/jetup', LIME), ('👥', 'mtgtribe.com/group', PURPLE), ('✈️', 'Telegram  @mtgtribe', PURPLE), ('📲', 'Check my bio', PINK)]
    y = 230
    for e, t, col in rows:
        d.rounded_rectangle((900, y, 1760, y + 120), 60, fill=CARD, outline=col, width=3)
        emoji(im, e, 945, y + 28, 64)
        d.text((1040, y + 60), t, font=F('sb', 50), fill=gfx.WHITE, anchor='lm')
        y += 150
    brand_pair(im, 390 - 230, 815, h=64, size=30)
    d.text((W16 // 2, 985), 'Not financial advice. Trading involves risk. Only invest what you can afford to lose.',
           font=F('m', 32), fill=(170, 165, 190), anchor='mm')
    return im.convert('RGB')
gfx16.endcard = endcard

# ---- headline highlights in cards.py: TAG lime, except MTG's own name in his gold
import cards
for _trig, _spec in cards.CARDS:
    if _spec.get('hc') == (232, 194, 90):
        _spec['hc'] = MTG_GOLD if _spec.get('head') == 'MTG' else LIME
