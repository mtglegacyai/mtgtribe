# Cut MTG's banked lines for JetUP explainer #1 ("JetUP and TAG Markets: the simple picture"). No new voice, no credits.
# Edges at real silences nearest the sentences.tsv spans; word times by faster-whisper aligned to the known text.
import subprocess, numpy as np, json, csv, wave, re, difflib
SR = 48000
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
FILES = {'o1': '5-checks/o1.mp3', 'o2': '5-checks/o2.mp3', 'n1': '5-checks/n1.mp3', 'i1': 'zoom-invite/i1.mp3',
         't2': 'signup-training/t2.mp3', 't3': 'signup-training/t3.mp3', 'v3': 'tutorial/p1v3.mp3'}
AUD = {k: load(v.split('/')[-1]) for k, v in FILES.items()}
def find(fid, text):
    for r in rows:
        if r[0] == FILES[fid] and r[3].startswith(text):
            return float(r[1]), float(r[2]), r[3]
    raise SystemExit('missing ' + fid + ' ' + text)
LINES = [
    ('hook', 'i1', 'Want to see how automated gold'), ('hi', 'o1', "Hi, I'm MTG"), ('simple', 'o1', 'Here is the simple picture'),
    ('jet1', 'o1', 'JetUP is a community'), ('jet2', 'o1', 'It does not trade'), ('tag1', 'o1', 'TAG Markets is the broker'),
    ('tag2', 'o1', 'You open a trading account there'), ('copyx', 'o1', 'Then you connect a strategy'),
    ('sonic', 'o1', 'The main one, Sonic AI'), ('gold', 'o1', "That's gold, priced"), ('p70', 'o1', 'When the strategy makes a profit'),
    ('p30', 'o1', 'Thirty percent pays'), ('loss', 'o1', 'And if it makes a loss'), ('lose', 'o2', 'You can lose your whole deposit'),
    ('r88', 't2', 'And eighty eight percent'), ('learn', 'i1', 'Trading carries risk'), ('verify', 'o1', "So let's verify, together"),
    ('every', 'v3', 'Invited by someone else?'),
    ('o_fin', 't3', 'Quick reminder'), ('o_dyor', 't3', 'Always do your own'), ('o_thanks', 't3', 'Thank you for tuning in'),
    ('o_support', 't3', 'Your support means'), ('o_massive', 't3', 'And thank yourself'), ('o_best', 't3', 'I wish you nothing'),
    ('o_im', 't3', "I'm MTG, Your Digital"), ('o_see', 't3', 'See you on the next'), ('o_lgtc', 't3', "Let's Get This Crypto"),
]
def env(x):
    hop = SR // 200; n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
GAPS = {}
for fid, x in AUD.items():
    sil = env(x) < 0.007; gaps = []; i = 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j + 1 < len(sil) and sil[j + 1]: j += 1
            if j - i + 1 >= 22: gaps.append((i / 200, (j + 1) / 200))
            i = j + 1
        else: i += 1
    GAPS[fid] = gaps
from faster_whisper import WhisperModel
WM = WhisperModel('small.en', device='cpu', compute_type='int8')
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def words_for(y, text, dur):
    toks = text.split()
    a16 = np.interp(np.arange(0, len(y), SR / 16000), np.arange(len(y)), y).astype(np.float32)
    segs, _ = WM.transcribe(a16, word_timestamps=True, language='en', beam_size=5)
    ww = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    sm = difflib.SequenceMatcher(None, [norm(t) for t in toks], [norm(w[0]) for w in ww], autojunk=False)
    times = [None] * len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): times[blk.a + k] = (ww[blk.b + k][1], ww[blk.b + k][2])
    i = 0
    while i < len(toks):
        if times[i] is None:
            j = i
            while j < len(toks) and times[j] is None: j += 1
            a = times[i - 1][1] if i > 0 else 0.0; b = times[j][0] if j < len(toks) else dur
            ch = [len(t) + 1 for t in toks[i:j]]; tot = sum(ch); acc = a
            for k, c in zip(range(i, j), ch):
                d = (b - a) * c / tot; times[k] = (acc, acc + d); acc += d
            i = j
        else: i += 1
    return [dict(w=t, a=round(a, 3), b=round(b, 3)) for t, (a, b) in zip(toks, times)]
out, WD = {}, {}
for key, fid, txt in LINES:
    a, b, full = find(fid, txt); x = AUD[fid]
    g_end = min(GAPS[fid], key=lambda g: abs(g[1] - a)); g_st = min(GAPS[fid], key=lambda g: abs(g[0] - b))
    s = g_end[1] - 0.04; en = g_st[0] + 0.10
    y = x[int(s * SR):int(en * SR)].copy()
    f_in, f_out = int(0.012 * SR), int(0.06 * SR)
    y[:f_in] *= np.linspace(0, 1, f_in); y[-f_out:] *= np.linspace(1, 0, f_out)
    p = f'v_{key}.wav'
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    dur = len(y) / SR
    out[key] = dict(file=p, src=fid, a=round(s, 3), b=round(en, 3), dur=round(dur, 3), text=full)
    WD[key] = words_for(y, full, dur)
    print(f'{key:9s} {fid} {dur:5.2f}  {full}')
json.dump(out, open('lines.json', 'w'), indent=1); json.dump(WD, open('words.json', 'w'))
print('total voice', round(sum(v['dur'] for v in out.values()), 1), 's')
