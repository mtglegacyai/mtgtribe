# JetUP explainer #2 ("Five names. One simple picture.", the minibus taxi): MTG's 8 new lines (one HeyGen request,
# MTG Master Voice V2, 8 Nov 2026, 2 credits) plus his banked lines. Edges at real silences; word times by faster-whisper
# aligned to the known text. Reuses explainer #1's cut lines where they are the same.
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
NEW = [('n_hook', 0.256, 10.022, "Jet Up, TAG Markets, Copy X, Sonic AI. Four names, plus you. Mix them up, and nothing makes sense. Here's one picture you'll never forget."),
       ('n_taxi', 10.752, 18.779, "Think of a minibus taxi. You don't drive. You choose a driver, take your seat, and the driver does the driving. Copy trading works the same way."),
       ('n_driver', 19.579, 21.977, "Sonic AI is the driver. It does the trading."),
       ('n_seat', 22.777, 26.222, "Your seat is booked in your name. That's your TAG Markets account."),
       ('n_board', 27.022, 30.273, "Copy X is the route board that puts you in that driver's taxi."),
       ('n_assoc', 31.073, 35.037, "Jet Up is the association. It trains and organises the passengers."),
       ('n_you', 35.837, 39.372, "And you? You decide which taxi to take, and how much to put in."),
       ('n_stops', 40.172, 47.378, "Here's where the picture stops. A taxi gets you there. A strategy can lose money, and a good last trip never promises the next one.")]
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
def tsv(fid, start):
    for r in rows:
        if r[0] == fid and r[3].startswith(start): return float(r[1]), float(r[2]), r[3]
    raise SystemExit('missing ' + start)
a1, b1, t1 = tsv('5-checks/o1.mp3', "Don't take my word"); a2, b2, t2 = tsv('5-checks/o1.mp3', 'Log in yourself')
BANK = [('track', 'o2.mp3', *tsv('5-checks/o2.mp3', 'Sonic AI publishes its track record')),
        ('login', 'o1.mp3', a1, b2, t1 + ' ' + t2),
        ('links', 't3.mp3', *tsv('signup-training/t3.mp3', 'Everything I showed you, plus my links'))]
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
X = load('ex2v1.mp3'); G = gaps_of(X)
for key, a, b, txt in NEW:
    y, s, en = cut(X, G, a, b); save(f'v_{key}.wav', y); dur = round(len(y) / SR, 3)
    L[key] = dict(file=f'v_{key}.wav', src='ex2v1', a=round(s, 3), b=round(en, 3), dur=dur, text=txt); WD[key], heard = words_for(y, txt, dur)
    print(key, dur, '| heard:', heard)
AUD = {}
for key, f, a, b, txt in BANK:
    if f not in AUD: AUD[f] = (load(f), gaps_of(load(f)))
    x, g = AUD[f]; y, s, en = cut(x, g, a, b); save(f'v_{key}.wav', y); dur = round(len(y) / SR, 3)
    L[key] = dict(file=f'v_{key}.wav', src=f, a=round(s, 3), b=round(en, 3), dur=dur, text=txt); WD[key], heard = words_for(y, txt, dur)
    print(key, dur, '| heard:', heard)
L1 = json.load(open(f'{EX1}/lines.json')); W1 = json.load(open(f'{EX1}/words.json'))
for k in ('hi', 'tag1', 'jet2', 'r88', 'learn', 'verify', 'every', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc'):
    shutil.copy(f'{EX1}/{L1[k]["file"]}', L1[k]['file']); L[k] = L1[k]; WD[k] = W1[k]
NL = json.load(open('../consist/lines/lines_new.json'))
for k in ('save', 'share', 'we', 'slog'):
    shutil.copy(f'../consist/lines/{NL[k]["file"]}', f'v_n_{k}.wav'); L['n_' + k] = dict(file=f'v_n_{k}.wav', dur=NL[k]['dur'], text=NL[k]['text']); WD['n_' + k] = NL[k]['words']
json.dump(L, open('lines.json', 'w'), indent=1); json.dump(WD, open('words.json', 'w'))
print(len(L), 'lines')
