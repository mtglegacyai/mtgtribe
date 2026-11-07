# Redact one clip of MTG's recording at 30 fps -> clips/<id>/00000.jpg ... (+ meta.json)
import sys, os, json, subprocess, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from redact_lib import *
from PIL import Image

# usage: redact_clip.py spec.json CLIP_ID [--redraw]
# spec.json: {"video": "raw/part1.mp4", "out": "clips", "clips": {"A": [44.0, 49.6, {}], "C": [54.6, 62.0, {"focus_label": "Your name"}], ...}}
#   options: focus_label (label for the field being typed in), focus: [[t0, t1, label or null to leave visible]], kb: false
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


REDRAW = '--redraw' in sys.argv
if REDRAW:
    M = json.load(open(os.path.join(OUT, 'meta.json')))
    uniq, fmap = M['uniq'], M['fmap']
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
        kb = kb_top(g) if OPT.get('kb', True) else None
        y1 = kb if kb else 1520
        foc = [r for r in focused_fields(g, 130, y1)]
        hits, words = ocr_hits(f, 130, y1)
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
    out = f
    if u['kb']:
        kb = u['kb']
        col = np.median(f[kb + 5:min(H, kb + 220), 2:8].reshape(-1, 3), 0).astype(np.uint8)
        out[kb:min(H, kb + 228), :] = col
    out = draw_masks(out, masks, labels)
    Image.fromarray(out).save(os.path.join(OUT, f'{k_out:05d}.jpg'), quality=93)
json.dump(dict(id=cid, start=S, end=E, fps=FPS, n=len(fmap), fmap=fmap, uniq=uniq), open(os.path.join(OUT, 'meta.json'), 'w'))
print(cid, 'done', flush=True)
