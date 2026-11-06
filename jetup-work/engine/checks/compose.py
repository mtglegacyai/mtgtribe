# Build the vertical JetUP "5 Checks" video from the two HeyGen A-roll parts.
# Usage: python3 compose.py   (expects part1.mp4 part2.mp4 part1.srt part2.srt track.mp3 in cwd)
import re, json, subprocess, os
from PIL import Image
import gfx, cards

FPS = 30
COVER, GAP, END = 1.0, 0.45, 5.0
MUSIC_LEN = 51.36


def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))


def srt(p, off):
    out = []
    for blk in re.split(r'\n\s*\n', open(p, encoding='utf-8-sig').read().strip()):
        ls = blk.strip().splitlines()
        tl = [l for l in ls if '-->' in l]
        if not tl:
            continue
        a, b = [x.strip() for x in tl[0].split('-->')]
        def ts(x):
            h, m, s = x.replace(',', '.').split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
        txt = ' '.join(ls[ls.index(tl[0]) + 1:]).strip()
        out.append((ts(a) + off, ts(b) + off, txt))
    return out


def norm(t):
    return re.sub(r'[^a-z0-9 ]', '', t.lower().replace('-', ' ').replace('’', "'").replace("'", ''))


DISPLAY = [
    (r"\bgonna\b", 'going to'), (r'\bXAUUSD\b', 'XAU/USD'), (r'\bMT Five\b', 'MT5'), (r'\bMyFXBook\b', 'Myfxbook'),
    (r'Telegram at MTGTribe', 'Telegram @mtgtribe'), (r'(?<![/.])\bJetUp\b', 'JetUP'), (r'your digital architect', 'Your Digital Architect'),
    (r"Let's get this crypto\.?", "Let's Get This Crypto!"), (r'seventy/thirty', '70/30'), (r'\bauthorized\b', 'authorised'),
    (r'number five five two three seven', 'number 55237'),
    (r'\bM T five\b', 'MT5'), (r'\bMetaTrader five\b', 'MetaTrader 5'), (r'X A U,? U S D', 'XAU/USD'),
    (r'\bF S C A\b', 'FSCA'), (r'\bF S C\b', 'FSC'), (r'F S P number five, five, two, three, seven', 'FSP number 55237'),
    (r'\bT M Financials\b', 'TM Financials'), (r'My F X Book', 'Myfxbook'),
    (r'MTG tribe dot com slash jet up', 'mtgtribe.com/jetup'), (r'MTG tribe dot com slash group', 'mtgtribe.com/group'),
    (r'Telegram at MTG tribe', 'Telegram @mtgtribe'),
    (r'plus thirty point one percent', '+30.1%'), (r'thirty point one, times seventy percent', '30.1% × 70%'),
    (r'twenty-one percent', '21%'), (r'twenty-three months', '23 months'), (r'forty percent', '40%'),
    (r'November twenty twenty-four', 'November 2024'), (r'October twenty twenty-six', 'October 2026'),
    (r'seventy thirty', '70/30'), (r'seventy percent', '70%'), (r'Thirty percent', '30%'),
    (r'ten dollars', '$10'), (r'seven dollars', '$7'), (r'one hundred and fifty dollars', '$150'),
    (r'adds one hundred', 'adds $100'), (r'two hundred and fifty dollars', '$250'),
    (r'twenty-four times', '24 times'), (r'six thousand dollars', '$6,000'), (r'one million dollars', '$1,000,000'),
    (r'twelve months', '12 months'), (r'(?<![/.])\bJetUP\b', 'JetUP'), (r'mtgtribe\.com/jetup', 'mtgtribe.com/jetup'),
]


def display(t):
    for a, b in DISPLAY:
        t = re.sub(a, b, t, flags=re.I)
    return t


def chunks(cue, maxc=58):
    a, b, txt = cue
    txt = display(txt)
    words, out, cur = txt.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > maxc and cur:
            out.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        out.append(cur)
    tot = sum(len(x) for x in out)
    res, t = [], a
    for x in out:
        d = (b - a) * len(x) / tot
        res.append((t, t + d, x)); t += d
    return res


def main():
    d1, d2 = dur('part1.mp4'), dur('part2.mp4')
    p2s = COVER + d1 + GAP
    speech_end = p2s + d2
    total = speech_end + END
    cues = srt('part1.srt', COVER) + srt('part2.srt', p2s)

    # char-level time map for card triggers
    text, times = '', []
    for a, b, t in cues:
        n = norm(t) + ' '
        for i, ch in enumerate(n):
            text += ch; times.append(a + (b - a) * i / max(1, len(n)))
    card_ev, pos = [], 0
    for trig, spec in cards.CARDS:
        hit = None
        for alt in trig.split('|'):
            k = text.find(norm(alt), pos)
            if k >= 0 and (hit is None or k < hit):
                hit = k
        if hit is None:
            print('MISSING trigger:', trig); continue
        pos = hit + 1
        card_ev.append((max(COVER, times[hit] - 0.15), spec))

    # sentence-level captions: spread words across cue times, rebuild whole sentences, then chunk
    words = []
    for a, b, t in cues:
        ws = t.split(); tot = sum(len(w) + 1 for w in ws); acc = 0
        for w in ws:
            ws_ = a + (b - a) * acc / tot; acc += len(w) + 1
            words.append((ws_, a + (b - a) * acc / tot, w))
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w[2][-1] in '.?!' and not re.match(r'^[A-Z]\.$', w[2]):
            sents.append(cur); cur = []
    if cur: sents.append(cur)
    caps = [c for snt in sents for c in chunks((snt[0][0], snt[-1][1], ' '.join(x[2] for x in snt)))]
    # event boundaries
    bounds = sorted(set([COVER, speech_end] + [t for t, _ in card_ev] + [x for c in caps for x in c[:2]]))
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

    os.makedirs('fr', exist_ok=True)
    layers = {}
    seq = []   # (png, duration)
    still = Image.open('still.png')
    gfx.cover(still).save('fr/cover.jpg', quality=95); seq.append(('fr/cover.jpg', COVER))
    prev_img, prev_card, n = None, None, 0
    for i in range(len(bounds) - 1):
        t0, t1 = bounds[i], bounds[i + 1]
        if t1 - t0 < 1 / FPS / 2: continue
        ci = card_at(t0)
        if ci not in layers and ci is not None:
            layers[ci] = gfx.card(card_ev[ci][1])
        img = gfx.frame(layers.get(ci), cap_at(t0 + 1e-4))
        dur_left = t1 - t0
        if prev_img is not None and ci != prev_card and dur_left > 0.3:
            for k in range(1, 6):   # 5-frame cross-fade into the new card
                p = f'fr/{n:05d}.jpg'; n += 1
                Image.blend(prev_img, img, k / 6).save(p, quality=95)
                seq.append((p, 1 / FPS)); dur_left -= 1 / FPS
        p = f'fr/{n:05d}.jpg'; n += 1
        img.save(p, quality=95); seq.append((p, dur_left))
        prev_img, prev_card = img, ci
    gfx.endcard().save('fr/end.jpg', quality=95); seq.append(('fr/end.jpg', END))
    with open('seq.txt', 'w') as f:
        for p, d in seq:
            f.write(f"file '{p}'\nduration {d:.4f}\n")
        f.write(f"file '{seq[-1][0]}'\n")
    json.dump(dict(d1=d1, d2=d2, p2s=p2s, speech_end=speech_end, total=total, cards=[t for t, _ in card_ev]),
              open('timeline.json', 'w'), indent=1)
    print(f'frames {n}, total {total:.2f}s, cards {len(card_ev)}/{len(cards.CARDS)}')


if __name__ == '__main__':
    main()
