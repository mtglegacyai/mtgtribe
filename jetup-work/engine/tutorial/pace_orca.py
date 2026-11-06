# Pause engine for HeyGen Voice (orca) takes: pauses hold natural breaths, so pauses are found from the
# break tags matched to real silences (never from word boundaries), merged across breaths, then set to target.
# Edits only ever touch pure silence. Joins t1..t3 into voice_tut.wav + voice_tut_words.json.
import json, wave, numpy as np
from align import align
from pace import words_with_times, para_ends, TARGET, ptype
from gaps import SR, FR
BREATH_MAX = -32.0      # a gap between two silences is a breath (not a word) if it never gets louder than this
MERGE_GAP = 0.22        # and lasts at most this long
KEEP = 0.10             # never shorten a silence below this
LEAD, MID, TAIL = 0.25, 0.85, 0.7

def kind_of(prev_word, tag):
    if '0.7s' in tag: return 'para'
    return {'.': 'stop', '?': 'q', '!': 'q', ',': 'comma', ':': 'colon'}.get(prev_word[-1], 'stop' if '0.4s' in tag else 'comma')

def spans(seq, e, R, B, match):
    out, used = [], set()
    for bi, i in enumerate(B):
        if bi not in match: continue
        k = match[bi]; lo_k = hi_k = k
        while lo_k > 0 and R[lo_k][0] - R[lo_k - 1][1] <= MERGE_GAP and e[int(R[lo_k - 1][1] / FR):int(R[lo_k][0] / FR)].max(initial=-99) < BREATH_MAX: lo_k -= 1
        while hi_k < len(R) - 1 and R[hi_k + 1][0] - R[hi_k][1] <= MERGE_GAP and e[int(R[hi_k][1] / FR):int(R[hi_k + 1][0] / FR)].max(initial=-99) < BREATH_MAX: hi_k += 1
        runs = list(range(lo_k, hi_k + 1)); used |= set(runs)
        prev = next((seq[j]['word'] for j in range(i - 1, -1, -1) if not seq[j]['word'].startswith('<')), '.')
        out.append(dict(kind=kind_of(prev, seq[i]['word']), t0=R[lo_k][0], t1=R[hi_k][1], runs=runs, prev=prev))
    return out, used

def process(name):
    seq, a, e, R, B, match = align(name)
    S, used = spans(seq, e, R, B, match)
    edits, rep = [], []
    for s in S:
        lo, hi = TARGET[s['kind']]; cur = s['t1'] - s['t0']
        big = max(s['runs'], key=lambda k: R[k][1] - R[k][0]); r = R[big]; mid = (r[0] + r[1]) / 2
        if cur < lo: d = lo - cur
        elif cur > hi: d = -min(cur - hi, (r[1] - r[0]) - KEEP)
        else: continue
        if abs(d) < 0.02: continue
        edits.append((int(mid * SR), int(round(d * SR)))); rep.append((s['prev'], s['kind'], round(cur, 2), round(cur + d, 2)))
    # mid-phrase hesitations: silences not part of any punctuation pause, longer than the 'none' limit
    nhi = TARGET['none'][1]
    for k, r in enumerate(R):
        if k in used or r[0] < 0.2 or r[1] > len(a) / SR - 0.2: continue
        L = r[1] - r[0]
        if L > nhi + 0.04:
            edits.append((int((r[0] + r[1]) / 2 * SR), -int(round((L - nhi) * SR)))); rep.append(('(mid)', 'none', round(L, 2), nhi))
    # room tone: quietest 0.3 s
    from gaps import env_db
    k = int(0.3 / FR); sm = np.convolve(e, np.ones(k) / k, 'valid'); i = int(np.argmin(sm))
    tone = a[i * 220:i * 220 + int(0.3 * SR)].copy()
    tone_n = lambda n: np.tile(tone, n // len(tone) + 2)[:n]
    F = int(0.004 * SR); out = a.copy()
    for pos, d in sorted(edits, key=lambda x: -x[0]):
        if d > 0:
            l, rr = out[:pos].copy(), out[pos:].copy(); l[-F:] *= np.linspace(1, 0, F); rr[:F] *= np.linspace(0, 1, F)
            ins = tone_n(d); ins[:F] *= np.linspace(0, 1, F); ins[-F:] *= np.linspace(1, 0, F)
            out = np.concatenate([l, ins, rr])
        else:
            c0 = pos - (-d) // 2; c1 = c0 + (-d)
            l, rr = out[:c0].copy(), out[c1:].copy(); n = min(F, len(l), len(rr))
            out = np.concatenate([l[:-n], l[-n:] * np.linspace(1, 0, n) + rr[:n] * np.linspace(0, 1, n), rr[n:]])
    cum = sorted(edits)
    def remap(t):
        p = t * SR; return t + sum(d for q, d in cum if q <= p) / SR
    W = words_with_times(name)
    NW = [dict(word=w['word'], start=round(remap(w['start']), 4), end=round(remap(w['end']), 4)) for w in W]
    for j in range(len(NW) - 1):                      # aligner can stretch word ends into the pause
        if NW[j]['end'] > NW[j + 1]['start'] - 0.01: NW[j]['end'] = round(max(NW[j]['start'] + 0.05, NW[j + 1]['start'] - 0.01), 4)
    return out, NW, rep

if __name__ == '__main__':
    from collections import Counter
    names = ['t1', 't2', 't3']
    sil = lambda t: np.zeros(int(t * SR), np.float32)
    chunks, words, pe_all, off = [sil(LEAD)], [], set(), LEAD
    for k, n in enumerate(names):
        o, w, rep = process(n)
        txt = open(f'{n}.txt').read().split(); assert len(txt) == len(w), (n, len(txt), len(w))
        s0 = max(0, int((w[0]['start'] - 0.04) * SR)); s1 = min(len(o), int((w[-1]['end'] + 0.15) * SR))
        o = o[s0:s1]; base = len(words)
        for x in w: words.append(dict(word=x['word'], start=round(x['start'] - s0 / SR + off, 3), end=round(x['end'] - s0 / SR + off, 3), part=k + 1))
        pe_all |= {base + i for i in para_ends(f'{n}.txt')}
        chunks.append(o); off += len(o) / SR
        if k < len(names) - 1: chunks.append(sil(MID)); off += MID
        print(n, 'edits', len(rep), Counter(x[1] for x in rep))
    chunks.append(sil(TAIL)); a = np.concatenate(chunks)
    pcm = np.clip(a * 32767, -32768, 32767).astype(np.int16)
    with wave.open('voice_tut.wav', 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
    json.dump(dict(duration=len(a) / SR, words=words, para_ends=sorted(pe_all)), open('voice_tut_words.json', 'w'), indent=0)
    print('voice_tut.wav', round(len(a) / SR, 2), 's,', len(words), 'words,', round(len(words) / (len(a) / SR) * 60), 'wpm')
