# Cut MTG's voice lines for tutorial part 2 (banked lines + the part 2 request), edges at real silences; word times by
# faster-whisper aligned to the known text (proportional fill where whisper and the text differ).
import subprocess, numpy as np, json, csv, wave, re, difflib
SR = 48000
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
AUD = {'t1': load('t1.mp3'), 't2': load('t2.mp3'), 't3': load('t3.mp3'), 'v2': load('p1v2_raw.wav'), 'v3': load('p1v3_raw.wav'),
       'p2': load('p2v1_raw.wav')}
V2 = json.load(open('p1v2_lines.json'))
V2SPANS = [(0.256, 2.112), (2.688, 7.941), (8.366, 13.132), (13.785, 18.357), (19.181, 23.294), (23.832, 27.345), (28.246, 32.235),
           (32.811, 37.658), (38.653, 41.67), (42.322, 45.492), (45.992, 49.012), (50.086, 52.027), (52.603, 55.73), (56.23, 57.717),
           (58.426, 61.178), (61.754, 66.332), (67.216, 71.043), (71.696, 76.696), (77.537, 81.864), (82.401, 89.548)]
for (k, t), (a, b) in zip(V2, V2SPANS):
    rows.append(['signup-training/v2.mp3', str(a), str(b), t])
V3 = json.load(open('p1v3_lines.json'))
for (k, t), (a, b) in zip(V3, [(0.256, 6.639), (7.253, 11.738), (12.16, 18.0)]):
    rows.append(['signup-training/v3.mp3', str(a), str(b), t])
P2 = json.load(open('p2v1_lines.json'))
for (k, t), (a, b) in zip(P2, json.load(open('p2v1_tts_meta.json'))['spans']):
    rows.append(['signup-training/p2.mp3', str(a), str(b), t])
def find(fid, text):
    for r in rows:
        if r[0] == f'signup-training/{fid}.mp3' and r[3].startswith(text):
            return float(r[1]), float(r[2]), r[3]
    raise SystemExit('missing ' + text)
LINES = [
    ('hi', 't1', 'Hi, my name is MTG'), ('takeyour', 't1', 'Take your time.'), ('pause', 't1', 'You can pause any step'),
    ('inbox', 't1', 'Not in your inbox?'), ('spam', 't1', 'Check spam or junk mail.'),
    ('jlogin', 't2', 'Log in at jet up dot'), ('never', 't2', 'Never register directly'), ('syncing', 't2', "You'll see Syncing"),
    ('active', 't2', "When it's done, the banner"), ('tagin', 't2', 'Log in at portal dot tag'),
    ('links', 't3', 'Everything I showed you'), ('save', 't3', 'Save this video'), ('share', 't3', "Share it with someone who's ready"),
    ('o_fin', 't3', 'Quick reminder'), ('o_dyor', 't3', 'Always do your own'), ('o_thanks', 't3', 'Thank you for tuning in'),
    ('o_support', 't3', 'Your support means'), ('o_massive', 't3', 'And thank yourself'), ('o_best', 't3', 'I wish you nothing'),
    ('o_im', 't3', "I'm MTG, Your Digital"), ('o_see', 't3', 'See you on the next'), ('o_lgtc', 't3', "Let's Get This Crypto"),
    ('n_thanks', 'v2', 'Thank you for taking'), ('r_intro', 'v2', "Let's recap"), ('l_every', 'v3', 'Invited by someone else?'),
] + [(k, 'p2', t) for k, t in P2]
def env(x):
    hop = SR // 200
    n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
ENV = {k: env(v) for k, v in AUD.items()}
GAPS = {}
for fid, e in ENV.items():
    sil = e < 0.007; gaps = []; i = 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j + 1 < len(sil) and sil[j + 1]:
                j += 1
            if j - i + 1 >= 22:
                gaps.append((i / 200, (j + 1) / 200))
            i = j + 1
        else:
            i += 1
    GAPS[fid] = gaps
from faster_whisper import WhisperModel
WM = WhisperModel('small.en', device='cpu', compute_type='int8')
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def words_for(path, text, dur):
    toks = text.split()
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a16 = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = WM.transcribe(a16, word_timestamps=True, language='en', beam_size=5)
    ww = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    sm = difflib.SequenceMatcher(None, [norm(t) for t in toks], [norm(w[0]) for w in ww], autojunk=False)
    times = [None] * len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (ww[blk.b + k][1], ww[blk.b + k][2])
    # fill gaps proportionally by characters between known neighbours
    i = 0
    while i < len(toks):
        if times[i] is None:
            j = i
            while j < len(toks) and times[j] is None:
                j += 1
            a = times[i - 1][1] if i > 0 else 0.0
            b = times[j][0] if j < len(toks) else dur
            ch = [len(t) + 1 for t in toks[i:j]]; tot = sum(ch); acc = a
            for k, c in zip(range(i, j), ch):
                d = (b - a) * c / tot; times[k] = (acc, acc + d); acc += d
            i = j
        else:
            i += 1
    matched = sum(blk.size for blk in sm.get_matching_blocks())
    return [dict(w=t, a=round(a, 3), b=round(b, 3)) for t, (a, b) in zip(toks, times)], matched, len(toks)
out, WD = {}, {}
for key, fid, txt in LINES:
    a, b, full = find(fid, txt)
    x = AUD[fid]
    g_end = min(GAPS[fid], key=lambda g: abs(g[1] - a))
    g_st = min(GAPS[fid], key=lambda g: abs(g[0] - b))
    s = g_end[1] - 0.04
    en = g_st[0] + 0.10
    y = x[int(s * SR):int(en * SR)].copy()
    f_in, f_out = int(0.012 * SR), int(0.06 * SR)
    y[:f_in] *= np.linspace(0, 1, f_in); y[-f_out:] *= np.linspace(1, 0, f_out)
    p = f'v_{key}.wav'
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    dur = len(y) / SR
    out[key] = dict(file=p, src=fid, a=round(s, 3), b=round(en, 3), dur=round(dur, 3), text=full)
    WD[key], m, n = words_for(p, full, dur)
    flag = '' if m == n else f'  (whisper matched {m}/{n})'
    print(f'{key:9s} {fid} tsv {a:8.3f} {b:8.3f} cut {s:8.3f} {en:8.3f} {dur:6.2f}{flag}  {full}')
json.dump(out, open('lines.json', 'w'), indent=1)
json.dump(WD, open('words.json', 'w'))
