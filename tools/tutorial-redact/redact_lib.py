# Privacy redaction for MTG's phone screen recordings (JetUP tutorial).
# Every frame: remove the screen recorder's timer bubble, blank the keyboard's suggestion/autofill strip, cover the
# focused input field while he types, and cover every personal word OCR finds (names, emails, password, phone, ID),
# carried across neighbouring frames by measured scrolling so a missed OCR frame never leaks.
import os
import re
import numpy as np
import pytesseract
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 720, 1562
FONT = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 18)
LABEL = {'name': 'Your name', 'first': 'First name', 'last': 'Last name', 'email': 'Your email',
         'password': 'Your password', 'phone': 'Your number', 'id': 'Your ID', 'ref': 'Hidden'}


# Personal words (names, the person's own emails, phone and ID fragments) are NOT in this file: they live in a private,
# uncommitted patterns file, one "category<TAB>regex" per line (categories: name, email, password, phone, id).
# Path: $TUTORIAL_PRIVATE_PATTERNS, default ~/.tutorial-private-patterns.tsv
PRIVATE = []
_pp = os.environ.get('TUTORIAL_PRIVATE_PATTERNS', os.path.expanduser('~/.tutorial-private-patterns.tsv'))
if os.path.exists(_pp):
    for line in open(_pp):
        if line.strip() and not line.startswith('#') and '\t' in line:
            c, rx = line.rstrip('\n').split('\t', 1)
            PRIVATE.append((c, re.compile(rx, re.I)))


def classify(w):
    wl = w.lower()
    if re.search(r'gmail|yahoo|outlook|hotmail|icloud', wl) or re.search(r'\w@\w+\.\w', wl):
        return 'email'
    for c, rx in PRIVATE:
        if rx.search(wl):
            return c
    if '@' in wl and re.search(r'\d', wl) and re.search(r'[a-z]', wl):
        return 'password'
    if re.search(r'\b(ib|cu|1b)\s?\d{5,}', wl):
        return 'id'
    if re.search(r'\d{6,}', wl):
        return 'phone'
    return None


def gray(f):
    return f.astype(np.float32).mean(2)


def bubble_centre(f, prev=None):
    """Screen recorder timer: a navy disk (#171B36) about 82 px wide, x 627..709. It never touches the screen edges, which
    rules out keyboards and bars (they are navy-ish across the full width)."""
    a = f.astype(np.int16)
    navy = (abs(a[:, :, 0] - 23) < 14) & (abs(a[:, :, 1] - 27) < 14) & (abs(a[:, :, 2] - 54) < 16)
    band = navy[:, 600:720]
    rows = band.sum(1) >= 30
    cands = []
    y = 0
    while y < H:
        if rows[y]:
            y2 = y
            while y2 + 1 < H and rows[y2 + 1]:
                y2 += 1
            if 45 <= y2 - y + 1 <= 100:
                cy = (y + y2) // 2
                xs = np.where(band[y:y2 + 1].any(0))[0] + 600
                edge = navy[y:y2 + 1, 713:720].mean() + navy[y:y2 + 1, 595:612].mean()
                wid = band[y:y2 + 1].sum(1)
                if xs.min() >= 612 and xs.max() <= 716 and edge < 0.3 and wid[min(8, len(wid) - 1)] < wid.max() * 0.85:
                    cands.append((int((xs.min() + xs.max()) / 2), cy))
            y = y2 + 1
        else:
            y += 1
    if not cands:
        return None
    if prev:
        return min(cands, key=lambda c: abs(c[1] - prev[1]))
    return cands[0]


def remove_bubble(f, c, r=46):
    if c is None:
        return
    cx, cy = c
    for y in range(max(0, cy - r), min(H, cy + r + 1)):
        dx = int((r * r - (y - cy) ** 2) ** 0.5)
        x0, x1 = max(0, cx - dx), min(W, cx + dx + 1)
        src = max(0, cx - r - 4)
        f[y, x0:x1] = f[y, src]


def kb_top(g):
    """Top row of an on-screen keyboard (a full-width dark block at least 60 px tall), or None."""
    rowdark = (g.mean(1) < 75) & (g[:, 3] < 95) & (g[:, 716] < 95)
    for y in range(500, 1300):
        if rowdark[y] and rowdark[y:y + 60].all():
            # include the autofill chip row just above the keys (dark edges, lighter chips)
            top = y
            while top > y - 150 and g[top - 1, 3] < 95 and g[top - 1, 716] < 95 and g[top - 1].mean() < 150:
                top -= 1
            return top
    return None


def dark_runs(row, minlen=120):
    d = np.concatenate([[0], (row < 110).astype(np.int8), [0]])
    diff = np.diff(d)
    st, en = np.where(diff == 1)[0], np.where(diff == -1)[0]
    return [(s, e) for s, e in zip(st, en) if e - s >= minlen]


def focused_fields(g, y0, y1):
    """Input fields with the thick black focus border; returns interior rectangles."""
    lines = []
    for y in range(y0, y1):
        for s, e in dark_runs(g[y]):
            if lines and abs(lines[-1][1] - s) < 10 and abs(lines[-1][2] - e) < 10 and y - lines[-1][4] <= 2:
                lines[-1][4] = y
            else:
                lines.append([y, s, e, None, y])
    out = []
    for a in lines:
        for b in lines:
            if b is a:
                continue
            gap = b[0] - a[4]
            # left edges must match; right edges may differ where the timer bubble was painted over a border
            if 30 <= gap <= 90 and abs(a[1] - b[1]) < 14 and min(a[2], b[2]) - max(a[1], b[1]) > 100:
                xs0, xs1 = min(a[1], b[1]) - 10, min(a[2], b[2]) + 10
                inner = g[a[4] + 4:b[0] - 3, xs0 + 8:xs1 - 8]
                if inner.size and inner.mean() > 170 and (inner < 110).mean() < 0.3:
                    out.append((max(0, xs0), a[0], min(W, xs1), b[4] + 1))
    # keep distinct rectangles
    res = []
    for r in out:
        if not any(abs(r[1] - q[1]) < 8 and abs(r[0] - q[0]) < 14 for q in res):
            res.append(r)
    return res


def ocr_hits(f, y0, y1, invert=True):
    """Sensitive words with boxes (frame coordinates). OCR runs on overlapping horizontal bands at 2x (more reliable than
    one full-frame pass), plus an inverted pass on dark bands (white text on dark sheets and keyboards)."""
    hits, words = [], []
    band, step = 420, 340
    ys = list(range(y0, max(y0 + 1, y1 - band + step), step))
    for by in ys:
        by1 = min(y1, by + band)
        if by1 - by < 40:
            continue
        crop = Image.fromarray(f[by:by1]).convert('L')
        big = crop.resize((crop.width * 2, crop.height * 2))
        srcs = [big]
        if invert and np.asarray(crop).mean() < 150:
            srcs.append(ImageOps.invert(big))
        for src, psm in [(x, p) for x in srcs for p in (11, 6)]:   # psm 6 reads underlined autofill text psm 11 misses
            d = pytesseract.image_to_data(src, config=f'--psm {psm}', output_type=pytesseract.Output.DICT)
            for i, w in enumerate(d['text']):
                w = w.strip()
                if not w:
                    continue
                box = (d['left'][i] // 2, by + d['top'][i] // 2, (d['left'][i] + d['width'][i]) // 2,
                       by + (d['top'][i] + d['height'][i]) // 2)
                words.append((w, box))
                c = classify(w)
                if c:
                    hits.append((c, box))
                if w.lower().startswith('referrer'):
                    hits.append(('ref', (box[2] + 4, box[1] - 2, box[2] + 70, box[3] + 2)))
    return hits, words


def row_shift(pa, pb, maxs=240):
    """Vertical shift d so that pb[y] ~ pa[y - d]; returns (d, error)."""
    n = min(len(pa), len(pb))
    pa, pb = pa[:n], pb[:n]
    best = (1e9, 0)
    for d in range(-maxs, maxs + 1):
        if d >= 0:
            a, b = pa[:n - d], pb[d:]
        else:
            a, b = pa[-d:], pb[:n + d]
        if len(a) < 200:
            continue
        e = float(np.abs(a - b).mean())
        if e < best[0]:
            best = (e, d)
    return best[1], best[0]


def profile(g, kb):
    y1 = (kb - 5) if kb else 1380
    return g[215:y1, 20:620].mean(1)


def pad_box(c, b, g):
    x0, y0, x1, y1 = b
    x0, y0, x1, y1 = x0 - 9, y0 - 8, x1 + 9, y1 + 8
    if c != 'ref' and x1 - x0 < 150:
        x1 = x0 + 150
    return (max(0, x0), max(0, y0), min(W - 2, x1), min(H, y1))


def merge(boxes):
    """Merge overlapping or same-line touching boxes of the same category."""
    boxes = list(boxes)
    changed = True
    while changed:
        changed = False
        out = []
        for c, b in boxes:
            for i, (c2, b2) in enumerate(out):
                same_line = abs((b[1] + b[3]) / 2 - (b2[1] + b2[3]) / 2) < 14
                overlap = not (b[2] < b2[0] - 14 or b2[2] < b[0] - 14 or b[3] < b2[1] or b2[3] < b[1])
                if overlap and (same_line or c == c2):
                    order = ['focus', 'password', 'email', 'phone', 'id', 'name', 'ref']
                    cc = min((c, c2), key=lambda k: order.index(k) if k in order else 99)
                    out[i] = (cc, (min(b[0], b2[0]), min(b[1], b2[1]), max(b[2], b2[2]), max(b[3], b2[3])))
                    changed = True
                    break
            else:
                out.append((c, b))
        boxes = out
    return boxes


def lock(d, x, y, col):
    d.rounded_rectangle((x, y + 7, x + 14, y + 18), radius=2, fill=col)
    d.arc((x + 2, y, x + 12, y + 13), 180, 360, fill=col, width=2)


def draw_masks(f, masks, labels):
    im = Image.fromarray(f)
    d = ImageDraw.Draw(im)
    g = gray(f)
    for (c, b), lab in zip(masks, labels):
        x0, y0, x1, y1 = [int(v) for v in b]
        x0, x1 = max(0, x0), min(W - 1, x1)
        y0, y1 = max(0, y0), min(H - 1, y1)
        if x1 - x0 < 4 or y1 - y0 < 4:
            continue                     # a box carried off the edge of the screen by scrolling
        inner = g[y0 + 2:y1 - 1, x0 + 2:x1 - 1]
        darkbg = c != 'focus' and inner.size and np.median(inner) < 110     # a dark sheet, not a field with a black border
        fill = (60, 58, 76) if darkbg else (236, 233, 247)
        ink = (196, 190, 220) if darkbg else (112, 102, 150)
        d.rounded_rectangle((x0, y0, x1, y1), radius=min(9, (y1 - y0) // 2), fill=fill)
        if lab and y1 - y0 >= 20:
            tw = d.textlength(lab, font=FONT)
            ty = (y0 + y1) // 2 - 10
            if x1 - x0 >= tw + 40:
                tx = x0 + 12
                lock(d, tx, ty + 1, ink)
                d.text((tx + 21, ty - 1), lab, font=FONT, fill=ink)
    return np.array(im)


def name_labels(masks):
    """Two name boxes side by side on one row are First name / Last name."""
    labs = []
    for c, b in masks:
        lab = LABEL.get(c, '')
        if c == 'name':
            mid = (b[1] + b[3]) / 2
            peers = [q for cc, q in masks if cc == 'name' and q is not b and abs((q[1] + q[3]) / 2 - mid) < 14]
            if peers:
                lab = 'First name' if b[0] < peers[0][0] else 'Last name'
        labs.append(lab)
    return labs
