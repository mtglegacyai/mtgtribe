# Forced-align the HeyGen render's own soundtrack, word by word, using the v3 word list and its times as search windows.
import json, re, subprocess, numpy as np
from pocketsphinx import Decoder
from align5 import toks, fa
V = json.load(open('voice_v3_words.json'))['words']
pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', '../raw/avatar_v3.mp4', '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
dur = len(pcm) / 32000
sents, cur = [], []
for i, w in enumerate(V):
    cur.append(i)
    if w['word'][-1] in '.?!' or (w['word'][-1] in ',:;' and len(cur) >= 9): sents.append(cur); cur = []
if cur: sents.append(cur)
out = [None] * len(V); fails = 0
for k, s in enumerate(sents):
    a, b = V[s[0]]['start'], V[s[-1]]['end']
    lo = (V[sents[k - 1][-1]]['end'] + a) / 2 if k else 0.0
    hi = (b + V[sents[k + 1][0]]['start']) / 2 if k + 1 < len(sents) else dur
    tk, owner = [], []
    for i in s:
        t = toks(V[i]['word']); tk += t; owner += [i] * len(t)
    seg = None
    for pl, ph in ((0, 0), (0.15, 0.2), (0.35, 0.4), (0.6, 0.6)):
        t0, t1 = max(0, lo - pl), min(dur, hi + ph)
        seg = fa(pcm[int(t0 * 16000) * 2:int(t1 * 16000) * 2], tk)
        if seg is not None: break
    ws = [x for x in (seg or []) if x[0] not in ('<sil>', '<s>', '</s>', '[NOISE]', '+NSN+', '+SPN+')]
    if seg is None or len(ws) != len(tk):
        fails += 1
        for i in s: out[i] = dict(word=V[i]['word'], start=V[i]['start'], end=V[i]['end'], src='v3')
        continue
    for (wd, st, en), i in zip(ws, owner):
        st, en = t0 + st, t0 + en
        if out[i] is None: out[i] = dict(word=V[i]['word'], start=round(st, 3), end=round(en, 3), src='fa')
        else: out[i]['end'] = round(en, 3)
json.dump(dict(duration=dur, words=out), open('render_words.json', 'w'), indent=0)
d = np.array([o['start'] - v['start'] for o, v in zip(out, V)])
print(f'{len(sents)} chunks, {fails} kept old times; render minus v3 start: ' + ', '.join(f'{p}s {np.median(d[(np.array([v["start"] for v in V]) >= p) & (np.array([v["start"] for v in V]) < p + 40)]):+.3f}' for p in (0, 60, 120, 180, 240, 300)))
