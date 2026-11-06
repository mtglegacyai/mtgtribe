# Splice the two new lines (t4) into voice_tut.wav at the pauses; rewrite voice_tut_words.json. Keeps the old files as *_pre_t4.
import json, wave, shutil, numpy as np
import pace_orca as P
from gaps import SR, env_db, FR

def load_wav(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; return a
def speech_bounds(a, t0, t1, thr=-42):
    e = env_db(a[int(t0 * SR):int(t1 * SR)]); idx = np.where(e > thr)[0]
    return (t0 + idx[0] * FR, t0 + (idx[-1] + 1) * FR) if len(idx) else None

V = load_wav('voice_tut_pre_t4.wav'); J = json.load(open('voice_tut_words_pre_t4.json')); Wd = J['words']
# ---- the new take, paced like the rest
out, NW, rep = P.process('t4')
k = next(i for i, w in enumerate(NW) if w['word'] == 'too.')
gap = speech_bounds(out, NW[k]['start'], NW[k + 1]['end'] + 0.3)
e_too = speech_bounds(out, NW[k]['start'], NW[k + 1]['start'] - 0.02)[1]
s_now = speech_bounds(out, NW[k]['end'] - 0.05, NW[k + 1]['end'] + 0.05)
s_now = s_now[0] if s_now and s_now[0] > e_too + 0.2 else NW[k + 1]['start']
def clip(t0, t1):
    b = speech_bounds(out, t0, t1); s, e = b[0] - 0.03, b[1] + 0.05
    return out[int(s * SR):int(e * SR)], s
promo, p0 = clip(max(0, NW[0]['start'] - 0.15), e_too + 0.02)
comm, c0 = clip(s_now - 0.05, NW[-1]['end'] + 0.3)
promo_words = [dict(word=w['word'], start=w['start'] - p0, end=w['end'] - p0) for w in NW[:k + 1]]
comm_words = [dict(word=w['word'], start=w['start'] - c0, end=w['end'] - c0) for w in NW[k + 1:]]
# room tone from the main narration
kk = int(0.3 / FR); e = env_db(V); sm = np.convolve(e, np.ones(kk) / kk, 'valid'); i = int(np.argmin(sm)); tone = V[i * 220:i * 220 + int(0.3 * SR)].copy()
tone_n = lambda sec: np.tile(tone, int(sec * SR) // len(tone) + 2)[:int(sec * SR)]
F = int(0.004 * SR)
def fade(x):
    x = x.copy(); x[:F] *= np.linspace(0, 1, F); x[-F:] *= np.linspace(1, 0, F); return x
# ---- locate the two places in the main narration
jd = next(j for j, w in enumerate(Wd) if w['word'] == 'dashboard.' and Wd[j + 1]['word'] == 'And' and Wd[j + 2]['word'] == "that's")
jc0 = next(j for j, w in enumerate(Wd) if w['word'] == 'And' and Wd[j + 1]['word'] == 'tell')
jc1 = next(j for j, w in enumerate(Wd) if w['word'] == 'longest?')
def longest_silence(t0, t1, thr=-42):
    e = env_db(V[int(t0 * SR):int(t1 * SR)]); q = e < thr; best, cur = None, None
    for i, v in enumerate(q):
        if v: cur = (cur[0], i + 1) if cur else (i, i + 1)
        else: cur = None
        if cur and (best is None or cur[1] - cur[0] > best[1] - best[0]): best = cur
    return t0 + best[0] * FR, t0 + best[1] * FR
s1 = longest_silence(Wd[jd]['end'] - 0.15, Wd[jd + 1]['start'] + 0.8)        # pause between "dashboard." and "And that's it"
a1, b1 = s1[0] + 0.02, s1[1] - 0.02
s2a = longest_silence(Wd[jc0 - 1]['end'] - 0.15, Wd[jc0]['start'] + 0.6)       # pause between "others." and "And tell me"
s2b = longest_silence(Wd[jc1]['end'] - 0.15, Wd[jc1 + 1]['start'] + 0.6)       # pause between "longest?" and "Everything"
a2, b2 = s2a[0] + 0.02, s2b[1] - 0.02
print('promo goes in at %.2f-%.2f (pause %.2f s), comment replaces %.2f-%.2f' % (a1, b1, b1 - a1, a2, b2))
seg1 = np.concatenate([fade(tone_n(0.48)), promo, fade(tone_n(0.40))])
seg2 = np.concatenate([fade(tone_n(0.48)), comm, fade(tone_n(0.48))])
A1, B1, A2, B2 = (int(x * SR) for x in (a1, b1, a2, b2))
newV = np.concatenate([V[:A1], seg1, V[B1:A2], seg2, V[B2:]])
d1 = len(seg1) / SR - (b1 - a1); d2 = len(seg2) / SR - (b2 - a2)
# ---- words
W2 = []
for j, w in enumerate(Wd):
    if j <= jd: W2.append(dict(w)); continue
    if j == jd + 1:
        off = a1 + 0.48
        W2 += [dict(word=x['word'], start=round(x['start'] + off, 3), end=round(x['end'] + off, 3), part=3) for x in promo_words]
    if jc0 <= j <= jc1:
        if j == jc0:
            off = a2 + d1 + 0.48
            W2 += [dict(word=x['word'], start=round(x['start'] + off, 3), end=round(x['end'] + off, 3), part=3) for x in comm_words]
        continue
    sh = d1 + (d2 if j > jc1 else 0)
    W2.append(dict(w, start=round(w['start'] + sh, 3), end=round(w['end'] + sh, 3)))
pcm = np.clip(newV * 32767, -32768, 32767).astype(np.int16)
with wave.open('voice_tut.wav', 'wb') as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
J2 = dict(duration=len(newV) / SR, words=W2, para_ends=J.get('para_ends', []))
json.dump(J2, open('voice_tut_words.json', 'w'), indent=0)
print('old %.2f s -> new %.2f s; words %d -> %d; shifts +%.2f, +%.2f' % (len(V) / SR, len(newV) / SR, len(Wd), len(W2), d1, d2))
