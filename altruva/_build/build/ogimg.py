"""Compose the 1200x630 social preview thumbnails: python3 build/ogimg.py [key ...]
Needs the phone shots from og/thumbs.js (og/shots/{key}.png). Writes img/og-{key}.jpg."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, '/tmp/eng')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from ogcfg import OG
from gfx import icon, emoji

ROOT = '/home/claude/site'
F = '/tmp/assets/fonts/'
W, H = 1200, 630
NIGHT, ABYSS, ROYAL, ELECTRIC, CYAN = (1, 8, 27), (1, 4, 16), (4, 72, 182), (47, 159, 249), (12, 225, 242)
GOLD, GOLD_L, GOLD_D, ICE, WHITE, MUTED = (238, 189, 92), (250, 234, 156), (199, 139, 54), (205, 224, 240), (255, 255, 255), (147, 169, 201)


def font(name, size):
    return ImageFont.truetype(F + name + '.ttf', size)


def background():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = yy / H
    bg = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        bg[..., i] = NIGHT[i] * (1 - t) + ABYSS[i] * t

    def blob(cx, cy, r, col, a):
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        k = np.clip(1 - d, 0, 1) ** 2 * a
        for i in range(3):
            bg[..., i] += col[i] * k
    blob(140, 60, 760, ROYAL, 0.55)
    blob(980, 600, 620, (5, 148, 205), 0.30)
    blob(900, 300, 420, (4, 50, 140), 0.35)
    g = ((xx % 34 < 2) & (yy % 34 < 2)).astype(np.float32) * 14
    bg += g[..., None] * np.array([0.4, 0.7, 1.0])
    return Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA')


def grad_text(txt, f, c1, c2, tracking=0):
    w = int(sum(f.getlength(ch) + tracking for ch in txt)) + 8
    asc, desc = f.getmetrics()
    m = Image.new('L', (w, asc + desc + 8), 0)
    d = ImageDraw.Draw(m); x = 2
    for ch in txt:
        d.text((x, 2), ch, font=f, fill=255); x += f.getlength(ch) + tracking
    m = m.crop(m.getbbox())
    tt = np.linspace(0, 1, m.height)[:, None]
    arr = np.zeros((m.height, m.width, 4), np.uint8)
    for i in range(3):
        arr[..., i] = (c1[i] * (1 - tt) + c2[i] * tt).astype(np.uint8)
    arr[..., 3] = np.array(m)
    return Image.fromarray(arr)


def title_font(txt, size):
    return font('Montserrat-800', int(size * 1.04)) if any(c.isdigit() for c in txt) else font('Orbitron-800', size)


def wrap(txt, f, maxw):
    words, lines, cur = txt.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if f.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    return lines


def glow(im, r, col, k=1.0):
    a = im.getchannel('A').filter(ImageFilter.GaussianBlur(r))
    g = Image.new('RGBA', im.size, col + (0,))
    g.putalpha(a.point(lambda v: min(255, int(v * k))))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(im)
    return out


def phone(shot):
    sw, sh = 282, 508
    pad = 40
    frame = Image.new('RGBA', (sw + 20 + pad * 2, sh + 20 + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    x0, y0 = pad, pad
    d.rounded_rectangle([x0, y0, x0 + sw + 19, y0 + sh + 19], 44, fill=(6, 14, 34, 255))
    # glowing electric-to-cyan border
    ring = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).rounded_rectangle([x0, y0, x0 + sw + 19, y0 + sh + 19], 44, outline=(255, 255, 255, 255), width=3)
    tt = np.linspace(0, 1, frame.height)[:, None]
    arr = np.zeros((frame.height, frame.width, 4), np.uint8)
    for i, (a, b) in enumerate(zip(ELECTRIC, CYAN)):
        arr[..., i] = (a * (1 - tt) + b * tt).astype(np.uint8)
    arr[..., 3] = np.array(ring.getchannel('A'))
    ring = Image.fromarray(arr)
    frame = Image.alpha_composite(glow(ring, 16, ELECTRIC, 1.4), frame)
    frame.alpha_composite(ring)
    scr = Image.open(shot).convert('RGB')
    r = sw / scr.width
    scr = scr.resize((sw, int(scr.height * r)), Image.LANCZOS).crop((0, 0, sw, sh))
    m = Image.new('L', (sw, sh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, sw - 1, sh - 1], 34, fill=255)
    frame.paste(scr, (x0 + 10, y0 + 10), m)
    return frame


def chip(icon_name, txt):
    f = font('Montserrat-800', 22)
    ic = icon(icon_name, 26, GOLD, 2.4)
    w = int(f.getlength(txt)) + 26 + 14 + 40
    im = Image.new('RGBA', (w, 52), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 51], 26, fill=(5, 16, 40, 245), outline=GOLD + (255,), width=2)
    im.alpha_composite(ic, (18, 13))
    d.text((18 + 26 + 12, 26), txt, font=f, fill=WHITE, anchor='lm')
    return glow(im, 10, (0, 0, 0), 0.9)


def compose(key):
    kicker, l1, l2, hook, chp, _ = OG[key]
    im = background()
    d = ImageDraw.Draw(im)
    X = 64
    em = Image.open('/home/claude/altruva-assets/altruva-emblem-192.png').convert('RGBA').resize((52, 52), Image.LANCZOS)
    im.alpha_composite(em, (X, 42))
    f = font('Orbitron-600', 19)
    x = X + 66
    for ch in 'ALTRUVA GUIDE BY MTG':
        d.text((x, 68), ch, font=f, fill=CYAN, anchor='lm'); x += f.getlength(ch) + 2.5
    cr = emoji('👑', 24)
    im.alpha_composite(cr, (int(x) + 6, 68 - cr.height // 2 - 1))
    # kicker pill
    fk = font('Montserrat-800', 18)
    kw = int(sum(fk.getlength(c) + 2 for c in kicker)) + 36
    d.rounded_rectangle([X, 120, X + kw, 156], 18, outline=GOLD + (255,), width=2, fill=(30, 22, 6, 120))
    x = X + 18
    for ch in kicker:
        d.text((x, 138), ch, font=fk, fill=GOLD, anchor='lm'); x += fk.getlength(ch) + 2
    # title: two lines, auto-fit to 600 px
    size = 66
    while size > 38 and max(title_font(l1, size).getlength(l1), title_font(l2, size).getlength(l2)) > 600:
        size -= 2
    t1 = grad_text(l1, title_font(l1, size), WHITE, ICE)
    t2 = grad_text(l2, title_font(l2, size), GOLD_L, GOLD_D)
    y = 186
    im.alpha_composite(glow(t1, 10, ELECTRIC, 0.5), (X - 2, y)); y += int(size * 1.22)
    im.alpha_composite(glow(t2, 12, GOLD_D, 0.55), (X - 2, y)); y += int(size * 1.2) + 18
    # hook
    fh = font('Montserrat-700', 27)
    lines = wrap(hook, fh, 590)
    if len(lines) > 1:  # balance the lines so no word sits alone
        ws = hook.split(); n = len(lines); best = None
        import itertools
        for cuts in itertools.combinations(range(1, len(ws)), n - 1):
            parts = [' '.join(ws[a:b]) for a, b in zip((0,) + cuts, cuts + (len(ws),))]
            mx = max(fh.getlength(p_) for p_ in parts)
            if mx <= 590 and (best is None or mx < best[0]):
                best = (mx, parts)
        if best:
            lines = best[1]
    for ln in lines[:3]:
        d.text((X, y), ln, font=fh, fill=ICE); y += 38
    # footer
    dom = {'root': 'mtgtribe.com', 'group': 'mtgtribe.com/group'}.get(key, 'mtgtribe.com/altruva')
    ff = font('Montserrat-800', 27)
    d.text((X, 572), dom, font=ff, fill=GOLD, anchor='lm')
    d.text((X + ff.getlength(dom) + 18, 573), 'Independent guide by MTG', font=font('Montserrat-700', 20), fill=MUTED, anchor='lm')
    # phone with this page's real content
    ph = phone(f'{ROOT}/og/shots/{key}.png')
    im.alpha_composite(ph, (W - ph.width + 6, (H - ph.height) // 2))
    if chp:
        c = chip(*chp)
        im.alpha_composite(c, (W - ph.width + 6 - c.width // 2 + 70, 488))
    out = f'{ROOT}/img/og-{key}.jpg'
    im.convert('RGB').save(out, quality=84, optimize=True)
    return out, os.path.getsize(out)


if __name__ == '__main__':
    keys = sys.argv[1:] or list(OG)
    for k in keys:
        p, n = compose(k)
        print(f'{k:8s} {n / 1024:.0f} KB')
