# Join paced parts t1..t3 into voice_tut.wav (+ words json), then a second pass on every punctuation pause.
import json, wave, numpy as np, subprocess
from pace import process, TARGET, ptype, para_ends, FADE
from gaps import env_db, SR
from align import runs_of
LEAD, MID, TAIL = 0.25, 0.85, 0.7
names = ['t1', 't2', 't3']
sil = lambda t: np.zeros(int(t * SR), np.float32)
chunks, words, pe_all, off = [sil(LEAD)], [], set(), LEAD
for k, n in enumerate(names):
    o, w, rep = process(n, f'{n}.txt')
    s0 = max(0, int((w[0]['start'] - 0.04) * SR)); s1 = min(len(o), int((w[-1]['end'] + 0.12) * SR))
    o = o[s0:s1]
    base = len(words)
    for x in w: words.append(dict(word=x['word'], start=round(x['start'] - s0 / SR + off, 3), end=round(x['end'] - s0 / SR + off, 3), part=k + 1))
    pe_all |= {base + i for i in para_ends(f'{n}.txt')}
    chunks.append(o); off += len(o) / SR
    if k < len(names) - 1: chunks.append(sil(MID)); off += MID
    print(n, 'adjusted', len(rep), 'pauses')
chunks.append(sil(TAIL))
a = np.concatenate(chunks)
# second pass on the joined track
e = env_db(a); R = runs_of(e); edits = []
for j in range(len(words) - 1):
    kd = ptype(words[j]['word'], j in pe_all); lo, hi = TARGET[kd]
    if kd == 'none': continue
    g0, g1 = words[j]['end'], words[j + 1]['start']
    c = [r for r in R if r[1] > g0 - 0.03 and r[0] < g1 + 0.03]
    if not c: continue
    tot = max(r[1] for r in c) - min(r[0] for r in c); big = max(c, key=lambda r: r[1] - r[0])
    if tot < lo - 0.02: edits.append((int((big[0] + big[1]) / 2 * SR), int((lo - tot) * SR)))
    elif tot > hi + 0.05:
        cut = min(tot - hi, (big[1] - big[0]) - 0.12)
        if cut > 0.03: edits.append((int((big[0] + big[1]) / 2 * SR), -int(cut * SR)))
for pos, d in sorted(edits, key=lambda x: -x[0]):
    if d > 0:
        l, r = a[:pos].copy(), a[pos:].copy(); l[-FADE:] *= np.linspace(1, 0, FADE); r[:FADE] *= np.linspace(0, 1, FADE)
        a = np.concatenate([l, np.zeros(d, np.float32), r])
    else:
        c0 = pos + d // 2; c1 = c0 - d
        l, r = a[:c0].copy(), a[c1:].copy(); n = FADE
        a = np.concatenate([l[:-n], l[-n:] * np.linspace(1, 0, n) + r[:n] * np.linspace(0, 1, n), r[n:]])
cum = sorted(edits); rm = lambda t: t + sum(d for q, d in cum if q <= t * SR) / SR
for w in words: w['start'] = round(rm(w['start']), 3); w['end'] = round(rm(w['end']), 3)
pcm = np.clip(a * 32767, -32768, 32767).astype(np.int16)
with wave.open('voice_tut.wav', 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
json.dump(dict(duration=len(a) / SR, words=words, para_ends=sorted(pe_all)), open('voice_tut_words.json', 'w'), indent=0)
print('second pass edits', len(edits), '| voice_tut.wav', round(len(a) / SR, 2), 's,', len(words), 'words,', round(len(words) / (len(a) / SR) * 60), 'wpm')
