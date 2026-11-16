# Redact one clip of MTG's recording at 30 fps -> clips/<id>/00000.jpg ... (+ meta.json)
import sys, os, json, subprocess, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from redact_lib import *
from PIL import Image

# usage: redact_clip.py spec.json CLIP_ID [--redraw | --kbscan]
#   --kbscan: re-read only the frames with a keyboard (or a dark sheet that looks like one) below the blanked strip, add
#             those hits to meta.json, then redraw (for clips analysed before below_kb_hits existed)
# spec.json: {"video": "raw/part1.mp4", "out": "clips", "clips": {"A": [44.0, 49.6, {}], "C": [54.6, 62.0, {"focus_label": "Your name"}], ...}}
#   options: focus_label (label for the field being typed in), focus: [[t0, t1, label or null to leave visible]], kb: false,
#            ignore: [[t0, t1, [x0, y0, x1, y1]]] OCR hits centred in that box between t0 and t1 (source seconds) are false
#            alarms (for example a button label read as a password); they are skipped when drawing (works with --redraw),
#            cover: [[t0, t1, [x0, y0, x1, y1], label]] a forced cover (for example a password manager sheet that shows the
#            email on a dark overlay OCR missed); drawn on every frame between t0 and t1 (works with --redraw),
#            nokb: [[t0, t1]] no keyboard in that stretch (dark pages such as a Cloudflare check look like one)
SPEC = json.load(open(sys.argv[1]))
CLIPS = {k: tuple(v) for k, v in SPEC['clips'].items()}
VIDEO = SPEC['video']
FPS = 30
cid = sys.argv[2]
S, E, OPT = CLIPS[cid]
OUT = os.path.join(SPEC.get('out', 'clips'), cid)
os.makedirs(OUT, exist_ok=True)


def frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(S), '-to', str(E), '-i', VIDEO, '-vf', f'fps={FPS}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()


def focus_label(t, rect):
    for t0, t1, lab in OPT.get('focus', []):
        if t0 <= t < t1:
            return lab if lab else False
    lab = OPT.get('focus_label', 'Hidden')
    x0, y0, x1, y1 = rect
    if x1 - x0 < 400 and lab in ('Your name', 'Your email', 'Your password'):
        # a half-width field on the sign-up form is a name field
        return 'First name' if x1 < 420 else 'Last name'
    return lab


def ignored(t, b):
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    for t0, t1, (x0, y0, x1, y1) in OPT.get('ignore', []):
        if t0 <= t < t1 and x0 <= cx <= x1 and y0 <= cy <= y1:
            return True
    return False


def no_kb(t):
    """nokb: [[t0, t1]] stretches with no keyboard, where a dark page (a Cloudflare check) only looks like one; the strip
    is then not blanked. Use it only where that strip shows nothing personal."""
    return any(t0 <= t < t1 for t0, t1 in OPT.get('nokb', []))


def below_kb_hits(f, kb):
    """A dark bottom sheet (a password manager's 'Use saved password?', a share sheet) can pass for a keyboard, and it
    shows the email. Read what is below the blanked strip too; digit runs there are keys, not phone numbers."""
    y0 = kb + 228
    if y0 > 1480:
        return []
    h, _ = ocr_hits(f, y0, 1520)
    return [(c, b) for c, b in h if c != 'phone']


REDRAW = '--redraw' in sys.argv or '--kbscan' in sys.argv
if REDRAW:
    M = json.load(open(os.path.join(OUT, 'meta.json')))
    uniq, fmap = M['uniq'], M['fmap']
    for u in uniq:                            # kb: false and nokb also apply to clips analysed before they were set
        if OPT.get('kb', True) is False or no_kb(u['t']):
            u['kb'] = None
    if '--kbscan' in sys.argv:
        done = set(); last_bc = None; added = 0
        for i, f in enumerate(frames()):
            k = fmap[i]
            u = uniq[k]
            if u['bc']:
                last_bc = tuple(u['bc'])
            if k in done or not u['kb']:
                continue
            done.add(k)
            remove_bubble(f, u['bc'] or last_bc)
            extra = below_kb_hits(f, u['kb'])
            u['hits'] += [(c, list(map(int, b))) for c, b in extra]
            added += len(extra)
        print(cid, 'kbscan frames', len(done), 'hits added', added, flush=True)
else:
    # ---------- pass 1: analyse unique frames ----------
    uniq = []      # per unique frame: dict
    fmap = []      # output frame -> unique index
    prev_h = None; prev_prof = None; chain = 0; S_acc = 0; last_bc = None
    for i, f in enumerate(frames()):
        h = hashlib.md5(f[::3, ::3].tobytes()).hexdigest()
        if h == prev_h:
            fmap.append(len(uniq) - 1); continue
        prev_h = h
        t = S + i / FPS
        bc = bubble_centre(f)
        if bc is not None:
            last_bc = bc
        remove_bubble(f, bc or last_bc)
        g = gray(f)
        kb = kb_top(g) if OPT.get('kb', True) and not no_kb(t) else None
        y1 = kb if kb else 1520
        foc = [r for r in focused_fields(g, 130, y1)]
        hits, words = ocr_hits(f, 130, y1)
        if kb:
            hits += below_kb_hits(f, kb)
        prof = profile(g, kb)
        d, err = (0, 0.0) if prev_prof is None else row_shift(prev_prof, prof)
        if prev_prof is not None and err > 5:
            chain += 1; d = 0
        S_acc += d
        prev_prof = prof
        uniq.append(dict(t=t, bc=bc, kb=kb, foc=[list(map(int, r)) for r in foc], hits=[(c, list(map(int, b))) for c, b in hits],
                         S=S_acc, chain=chain, err=round(err, 2)))
        fmap.append(len(uniq) - 1)
    print(cid, 'frames', len(fmap), 'unique', len(uniq), 'chains', chain + 1, flush=True)


bcs = [u['bc'] for u in uniq if u['bc']]
med = tuple(int(v) for v in np.median(np.array(bcs), 0)) if bcs else None

# ---------- pass 2: masks with propagation, draw, save ----------
R = 6
last_ok = None
for k_out, f in enumerate(frames()):
    k = fmap[k_out]
    u = uniq[k]
    bc = bubble_centre(f, last_ok or med)
    if bc is not None:
        last_ok = bc
    remove_bubble(f, bc or last_ok or med)
    g = gray(f)
    masks = []
    for j in range(max(0, k - R), min(len(uniq), k + R + 1)):
        v = uniq[j]
        if v['chain'] != u['chain']:
            continue
        dy = u['S'] - v['S']
        for c, b in v['hits']:
            if ignored(v['t'], b):
                continue
            masks.append((c, pad_box(c, (b[0], b[1] + dy, b[2], b[3] + dy), g)))
        if abs(j - k) <= 2:
            for r in v['foc']:
                lab = focus_label(v['t'], r)
                if lab is False:
                    continue
                masks.append(('focus', (r[0] + 3, r[1] + 3 + dy, r[2] - 3, r[3] - 3 + dy)))
    masks = merge(masks)
    labels = []
    for (c, b), lab in zip(masks, name_labels(masks)):
        labels.append(focus_label(u['t'], b) if c == 'focus' else lab)
    t_now = S + k_out / FPS
    for t0, t1, box, lab in OPT.get('cover', []):
        if t0 <= t_now < t1:
            masks.append(('cover', tuple(box)))
            labels.append(lab)
    out = f
    if u['kb']:
        kb = u['kb']
        col = np.median(f[kb + 5:min(H, kb + 220), 2:8].reshape(-1, 3), 0).astype(np.uint8)
        out[kb:min(H, kb + 228), :] = col
    out = draw_masks(out, masks, labels)
    Image.fromarray(out).save(os.path.join(OUT, f'{k_out:05d}.jpg'), quality=93)
n_out = k_out + 1
if n_out < len(fmap):                      # the clip was shortened in the spec: drop the frames past its new end
    for i in range(n_out, len(fmap)):
        p = os.path.join(OUT, f'{i:05d}.jpg')
        if os.path.exists(p):
            os.remove(p)
    fmap = fmap[:n_out]
json.dump(dict(id=cid, start=S, end=E, fps=FPS, n=len(fmap), fmap=fmap, uniq=uniq), open(os.path.join(OUT, 'meta.json'), 'w'))
print(cid, 'done', flush=True)
