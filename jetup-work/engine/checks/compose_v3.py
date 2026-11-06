# v3 timeline (16:9, native 25 fps): overlay PNG sequence driven by forced-aligned word times.
# Inputs: v3/av.mp4 (single HeyGen render), v3/voice_v3_words.json, v3/still.png
import re, json, os, shutil
from PIL import Image
import compose as C, cards, gfx16

FPS, COVER, END = 25, 1.0, 5.0
C.DISPLAY += [
    (r'F S P number five five, two three seven', 'FSP number 55237'), (r'\bfive checks\b', '5 checks'),
    (r'check number four', 'check number 4'), (r'\bCheck one\b', 'Check 1'), (r'\bCheck two\b', 'Check 2'),
    (r'\bCheck three\b', 'Check 3'), (r'\bCheck four\b', 'Check 4'), (r'\bCheck five\b', 'Check 5'),
    (r'\bcheck all five\b', 'check all 5'), (r'thirty point one, times seventy percent', '30.1% × 70%'),
    (r'twenty-one percent', '21%'), (r'\bT M Financials\b', 'TM Financials'), (r"Crypto!!", 'Crypto!'),
]

def frame_round(t):
    return round(t * FPS) / FPS

def main():
    J = json.load(open('v3/voice_v3_words.json'))
    W = [dict(w, start=w['start'] + COVER, end=w['end'] + COVER) for w in J['words']]
    av_dur = C.dur('v3/av.mp4') if os.path.exists('v3/av.mp4') else round(J['duration'] * FPS) / FPS
    speech_end = COVER + av_dur
    total = speech_end + END

    # ---- card triggers on the word sequence
    toks, tok_t = [], []
    for w in W:
        for p in C.norm(w['word']).split():
            toks.append(p); tok_t.append(w['start'])
    card_ev, pos = [], 0
    for trig, spec in cards.CARDS:
        hit = None
        for alt in trig.split('|'):
            q = C.norm(alt).split()
            for k in range(pos, len(toks) - len(q) + 1):
                if toks[k:k + len(q)] == q:
                    if hit is None or k < hit: hit = k
                    break
        if hit is None:
            print('MISSING trigger:', trig); continue
        pos = hit + 1
        card_ev.append((frame_round(max(COVER, tok_t[hit] - 0.12)), spec))

    # ---- captions: one sentence per line when it fits, otherwise split at commas, then at the middle word
    LIM = 70
    def dlen(ws): return len(C.display(' '.join(x['word'] for x in ws)))
    sents, cur = [], []
    for w in W:
        cur.append(w)
        if w['word'][-1] in '.?!': sents.append(cur); cur = []
    if cur: sents.append(cur)
    def split(ws):
        if dlen(ws) <= LIM: return [ws]
        # candidate cut points after commas (not after single letters like "U,")
        single = lambda w: len(w.strip(',:.?!')) == 1 and w.strip(',:.?!').isupper()
        cuts = [i + 1 for i, x in enumerate(ws[:-1]) if x['word'][-1] in ',:' and not (single(x['word']) and single(ws[i + 1]['word']))]
        best = None
        for c in cuts:
            a, b = dlen(ws[:c]), dlen(ws[c:])
            if a >= 14 and b >= 14:
                score = max(a, b)
                if best is None or score < best[0]: best = (score, c)
        if best is None:   # no usable comma: cut at the word nearest the middle
            tot = dlen(ws); ok = [c for c in range(1, len(ws)) if not single(ws[c - 1]['word']) and not single(ws[c]['word'])] or list(range(1, len(ws)))
            best = (0, min(ok, key=lambda c: abs(dlen(ws[:c]) - tot / 2)))
        c = best[1]
        return split(ws[:c]) + split(ws[c:])
    chunks = [p for s_ in sents for p in split(s_)]
    caps = []
    for k, c in enumerate(chunks):
        a = frame_round(c[0]['start'] - 0.06)
        nxt = chunks[k + 1][0]['start'] - 0.06 if k + 1 < len(chunks) else None
        b = c[-1]['end'] + 0.35
        if nxt is not None and nxt - c[-1]['end'] < 1.2: b = nxt     # hold through the pause until the next line
        caps.append((a, frame_round(min(b, speech_end)), C.display(' '.join(x['word'] for x in c))))

    bounds = sorted(set([COVER, frame_round(speech_end)] + [t for t, _ in card_ev] + [x for c in caps for x in c[:2]]))
    bounds = [b for b in bounds if COVER <= b <= speech_end]
    def card_at(t):
        cur = None
        for i, (ct, _) in enumerate(card_ev):
            if ct <= t + 1e-6: cur = i
        return cur
    def cap_at(t):
        for a, b, x in caps:
            if a - 1e-6 <= t < b - 1e-6: return x
        return ''
    if os.path.isdir('f3'): shutil.rmtree('f3')
    os.makedirs('f3')
    layers, seq = {}, []
    gfx16.cover(Image.open('v3/still.png')).convert('RGBA').save('f3/cover.png'); seq.append(('f3/cover.png', COVER))
    prev_img, prev_card, n = None, None, 0
    for i in range(len(bounds) - 1):
        t0, t1 = bounds[i], bounds[i + 1]
        if t1 - t0 < 1 / FPS / 2: continue
        ci = card_at(t0)
        if ci not in layers and ci is not None:
            layers[ci] = gfx16.card_small(card_ev[ci][1])
        img = gfx16.overlay(layers.get(ci), cap_at(t0 + 1e-4))
        left = t1 - t0
        if prev_img is not None and ci != prev_card and left > 0.3:
            for k in range(1, 5):          # 4-frame cross-fade into a new card
                p = f'f3/{n:05d}.png'; n += 1
                Image.blend(prev_img, img, k / 5).save(p)
                seq.append((p, 1 / FPS)); left -= 1 / FPS
        p = f'f3/{n:05d}.png'; n += 1
        img.save(p); seq.append((p, left))
        prev_img, prev_card = img, ci
    gfx16.endcard().convert('RGBA').save('f3/end.png'); seq.append(('f3/end.png', END))
    with open('seq3.txt', 'w') as f:
        for p, d in seq:
            f.write(f"file '{p}'\nduration {d:.4f}\n")
        f.write(f"file '{seq[-1][0]}'\n")
    json.dump(dict(av_dur=av_dur, speech_end=speech_end, total=total, cards=[t for t, _ in card_ev],
                   captions=caps), open('timeline3.json', 'w'), indent=1)
    print(f'frames {n}, total {total:.2f}s, cards {len(card_ev)}/{len(cards.CARDS)}, captions {len(caps)}')

if __name__ == '__main__':
    main()
