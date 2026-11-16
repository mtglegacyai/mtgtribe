# Cut MTG's banked closing lines for the consistency upgrade (MTG, 8 Nov 2026), from the sign-up training's own voice file
# (signup-training/t3.mp3, MTG Master Voice V2, the same take the 9:09 training uses). No new voice, no credits.
# Edges at real silences nearest the sentences.tsv spans; word times by faster-whisper aligned to the known text.
import subprocess, numpy as np, json, csv, wave, re, difflib
SR = 48000
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
rows = list(csv.reader(open('sentences.tsv'), delimiter='\t'))
X = load('t3.mp3')
LINES = [('we', 'We learn best when we teach others.'), ('slog', 'It pays to pay attention, and take action.'),
         ('save', "Save this video, so it's here when you need it."), ('share', "Share it with someone who's ready to start.")]
def find(text):
    for r in rows:
        if r[0] == 'signup-training/t3.mp3' and r[3] == text: return float(r[1]), float(r[2])
    raise SystemExit('missing ' + text)
hop = SR // 200; n = len(X) // hop
envl = np.sqrt((X[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12); sil = envl < 0.007; gaps = []; i = 0
while i < len(sil):
    if sil[i]:
        j = i
        while j + 1 < len(sil) and sil[j + 1]: j += 1
        if j - i + 1 >= 22: gaps.append((i / 200, (j + 1) / 200))
        i = j + 1
    else: i += 1
from faster_whisper import WhisperModel
WM = WhisperModel('small.en', device='cpu', compute_type='int8')
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def words_for(y, text, dur):
    toks = text.split()
    a16 = np.interp(np.arange(0, len(y), SR / 16000), np.arange(len(y)), y).astype(np.float32)
    segs, _ = WM.transcribe(a16, word_timestamps=True, language='en', beam_size=5)
    ww = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    print('   heard:', ' '.join(w[0] for w in ww))
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
out = {}
for key, txt in LINES:
    a, b = find(txt)
    g_end = min(gaps, key=lambda g: abs(g[1] - a)); g_st = min(gaps, key=lambda g: abs(g[0] - b))
    s = g_end[1] - 0.04; en = g_st[0] + 0.10
    y = X[int(s * SR):int(en * SR)].copy()
    f_in, f_out = int(0.012 * SR), int(0.06 * SR)
    y[:f_in] *= np.linspace(0, 1, f_in); y[-f_out:] *= np.linspace(1, 0, f_out)
    p = f'v_{key}.wav'
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    dur = round(len(y) / SR, 3)
    print(key, 'tsv', a, b, '-> cut', round(s, 3), round(en, 3), 'dur', dur)
    out[key] = dict(file=p, a=round(s, 3), b=round(en, 3), dur=dur, text=txt, words=words_for(y, txt, dur))
json.dump(out, open('lines_new.json', 'w'), indent=1)
