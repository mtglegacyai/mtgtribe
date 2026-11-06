# Align the TTS break markers to the real silences in the audio (timestamps drift locally).
import json, os, subprocess, numpy as np
# silence threshold: -58 dB suits the ElevenLabs takes; HeyGen Voice (orca) has breaths and a higher floor, so use -48
SIL_THR = float(os.environ.get('SIL_THR', -48))
from gaps import env_db, SR, FR
def runs_of(e, thr=None, minlen=0.06):
    thr = SIL_THR if thr is None else thr
    out, cur = [], None
    for i, x in enumerate(e):
        if x < thr: cur = (cur[0], i + 1) if cur else (i, i + 1)
        else:
            if cur and (cur[1] - cur[0]) * FR >= minlen: out.append((cur[0] * FR, cur[1] * FR))
            cur = None
    if cur: out.append((cur[0] * FR, cur[1] * FR))
    return out
def align(name):
    js = json.load(open(f'{name}_tts.json'))
    seq = [w for w in js['word_timestamps'] if w['word'] not in ('<start>', '<end>')]
    a = np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', f'{name}_raw.wav', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-']), np.int16).astype(np.float32) / 32768
    e = env_db(a); R = runs_of(e)
    B = [i for i, w in enumerate(seq) if w['word'].startswith('<break')]
    bt = [(seq[i]['start'] + seq[i]['end']) / 2 for i in B]
    rc = [(r[0] + r[1]) / 2 for r in R]
    n, m = len(B), len(R); INF = 1e9; SKIPB, SKIPR = 0.6, 0.25
    D = np.full((n + 1, m + 1), INF); P = np.zeros((n + 1, m + 1), int)
    D[0, :] = np.arange(m + 1) * SKIPR; D[:, 0] = np.arange(n + 1) * SKIPB
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = [D[i - 1, j - 1] + min(abs(bt[i - 1] - rc[j - 1]), 1.5), D[i - 1, j] + SKIPB, D[i, j - 1] + SKIPR]
            k = int(np.argmin(c)); D[i, j] = c[k]; P[i, j] = k
    i, j, match = n, m, {}
    while i > 0 and j > 0:
        k = P[i, j]
        if k == 0: match[i - 1] = j - 1; i, j = i - 1, j - 1
        elif k == 1: i -= 1
        else: j -= 1
    return seq, a, e, R, B, match
if __name__ == '__main__':
    import sys
    seq, a, e, R, B, match = align(sys.argv[1])
    print('breaks', len(B), 'silences', len(R), 'matched', len(match))
    for bi, i in enumerate(B):
        prev = seq[i - 1]['word']; nxt = seq[i + 1]['word'] if i + 1 < len(seq) else ''
        if bi in match:
            r = R[match[bi]]; d = (r[0] + r[1]) / 2 - (seq[i]['start'] + seq[i]['end']) / 2
            flag = '' if r[1] - r[0] >= 0.15 else '  <-- short'
            print(f"{prev:>14} {seq[i]['word'][12:16]} | {nxt:<12} sil={r[1]-r[0]:.2f} drift={d:+.2f}{flag}")
        else:
            print(f"{prev:>14} {seq[i]['word'][12:16]} | {nxt:<12} NO SILENCE FOUND")
