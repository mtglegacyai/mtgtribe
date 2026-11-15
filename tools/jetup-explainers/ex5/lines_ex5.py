# JetUP explainer #5, "The $100 Fast Start Promo" (MTG picked it 9 Nov 2026): all MTG's banked lines, 0 credits.
import subprocess, numpy as np, json, csv, wave, re, difflib, shutil, os
SR = 48000; EX1 = '../ex1'
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def gaps_of(x):
    hop = SR // 200; n = len(x) // hop; env = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12); sil = env < 0.007; g = []; i = 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j + 1 < len(sil) and sil[j + 1]: j += 1
            if j - i + 1 >= 22: g.append((i / 200, (j + 1) / 200))
            i = j + 1
        else: i += 1
    return g
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
def tsv(fid, start):
    for r in rows:
        if r[0] == fid and r[3].startswith(start): return float(r[1]), float(r[2]), r[3]
    raise SystemExit('missing ' + start)

BANK = [('hook', 'o2.mp3', '5-checks/o2.mp3', "JetUP's latest start promo works like this."),
        ('plan', 't1.mp3', 'signup-training/t1.mp3', "Here's the money plan."),
        ('dep', 't1.mp3', 'signup-training/t1.mp3', 'You deposit one hundred and fifty five dollars.'),
        ('fifty', 't1.mp3', 'signup-training/t1.mp3', 'Fifty goes into the Sonic strategy.'),
        ('hundred', 't1.mp3', 'signup-training/t1.mp3', 'One hundred stays in your balance for the Dennis Promo, which adds another one hundred.'),
        ('spare', 't1.mp3', 'signup-training/t1.mp3', 'A few dollars stay spare.'),
        ('claim', 't3.mp3', 'signup-training/t3.mp3', 'Claim the Dennis Fast Start Promo.'),
        ('cu', 't3.mp3', 'signup-training/t3.mp3', 'In TAG Markets, open the menu, tap Profile, and write down your C U number.'),
        ('tile', 't3.mp3', 'signup-training/t3.mp3', 'Go to jet dash up dot A I, and tap the orange Dennis Fast Start Promo tile.'),
        ('form', 't3.mp3', 'signup-training/t3.mp3', 'Enter your name, email and C U number exactly, and tap Join the promo.'),
        ('recv', 't3.mp3', 'signup-training/t3.mp3', "You'll see Application received."),
        ('mail', 't3.mp3', 'signup-training/t3.mp3', 'When the confirmation email arrives, open Copy X, then Follower Hub, then Strategies.'),
        ('two', 't3.mp3', 'signup-training/t3.mp3', "You'll see two Sonic accounts: your fifty dollar account, and your two hundred dollar promo account."),
        ('know', 't3.mp3', 'signup-training/t3.mp3', 'Know the promo rules.'),
        ('anytime', 't3.mp3', 'signup-training/t3.mp3', 'Profits can be withdrawn any time.'),
        ('bonus', 't3.mp3', 'signup-training/t3.mp3', 'The one hundred dollar bonus is released after twelve months.'),
        ('ends', 't3.mp3', 'signup-training/t3.mp3', 'And taking your own money out before then ends the promo.'),
        ('change', 't3.mp3', 'signup-training/t3.mp3', 'Rules can change, so check your dashboard.'),
        ('promo', 't4.mp3', 'signup-training/t4.mp3', 'And remember: a promo is a promo.'),
        ('start', 't4.mp3', 'signup-training/t4.mp3', "So if you've decided to start, start while it's still on, and confirm it on jet dash up dot A I before you deposit.")]
from faster_whisper import WhisperModel
WM = WhisperModel('small.en', device='cpu', compute_type='int8')
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def words_for(y, text, dur):
    toks = text.split(); a16 = np.interp(np.arange(0, len(y), SR / 16000), np.arange(len(y)), y).astype(np.float32)
    segs, _ = WM.transcribe(a16, word_timestamps=True, language='en', beam_size=5); ww = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    sm = difflib.SequenceMatcher(None, [norm(t) for t in toks], [norm(w[0]) for w in ww], autojunk=False); times = [None] * len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): times[blk.a + k] = (ww[blk.b + k][1], ww[blk.b + k][2])
    i = 0
    while i < len(toks):
        if times[i] is None:
            j = i
            while j < len(toks) and times[j] is None: j += 1
            a = times[i - 1][1] if i > 0 else 0.0; b = times[j][0] if j < len(toks) else dur; ch = [len(t) + 1 for t in toks[i:j]]; tot = sum(ch); acc = a
            for k, c in zip(range(i, j), ch): d = (b - a) * c / tot; times[k] = (acc, acc + d); acc += d
            i = j
        else: i += 1
    heard = ' '.join(w[0] for w in ww)
    return [dict(w=t, a=round(a, 3), b=round(b, 3)) for t, (a, b) in zip(toks, times)], heard
def cut(x, gaps, a, b):
    g_end = min(gaps, key=lambda g: abs(g[1] - a)); g_st = min(gaps, key=lambda g: abs(g[0] - b))
    s = g_end[1] - 0.04 if abs(g_end[1] - a) < 0.6 else a - 0.06; en = g_st[0] + 0.10 if abs(g_st[0] - b) < 0.6 else b + 0.15
    y = x[max(0, int(s * SR)):int(en * SR)].copy(); f_in, f_out = int(0.012 * SR), int(0.06 * SR)
    y[:f_in] *= np.linspace(0, 1, f_in); y[-f_out:] *= np.linspace(1, 0, f_out); return y, s, en
def save(p, y):
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
L, WD = {}, {}
AUD = {}
for key, f, fid, txt in BANK:
    a, b = None, None
    for r in rows:
        if r[0] == fid and r[3] == txt: a, b = float(r[1]), float(r[2]); break
    if a is None: raise SystemExit('missing ' + txt)
    if f not in AUD: AUD[f] = (load(f), gaps_of(load(f)))
    x, g = AUD[f]; y, s, en = cut(x, g, a, b); save(f'v_{key}.wav', y); dur = round(len(y) / SR, 3)
    L[key] = dict(file=f'v_{key}.wav', src=fid, a=round(s, 3), b=round(en, 3), dur=dur, text=txt); WD[key], heard = words_for(y, txt, dur)
    print(key, dur, '| heard:', heard)
EX1 = '../ex1'; L1 = json.load(open(f'{EX1}/lines.json')); W1 = json.load(open(f'{EX1}/words.json'))
for k in ('hi', 'n_turn2', 'l_ifme', 'every', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc'):
    shutil.copy(f'{EX1}/{L1[k]["file"]}', L1[k]['file']); L[k] = L1[k]; WD[k] = W1[k]
L2 = json.load(open('../ex2/lines.json')); W2 = json.load(open('../ex2/words.json'))
for k in ('n_save', 'n_share', 'n_we', 'n_slog'):
    shutil.copy(f'../ex2/{L2[k]["file"]}', L2[k]['file']); L[k] = L2[k]; WD[k] = W2[k]
json.dump(L, open('lines.json', 'w'), indent=1); json.dump(WD, open('words.json', 'w')); print(len(L), 'lines')
