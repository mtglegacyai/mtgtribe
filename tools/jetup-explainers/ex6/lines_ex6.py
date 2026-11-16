# JetUP explainer #6, "The partner plan: the rule most people miss" (MTG approved 11 Nov 2026): his nine new lines in
# MTG Master Voice V3 (one request, 1 credit), cut on their pauses and levelled to -18.5 LUFS like his other V3 lines,
# plus the shared greeting, close and signature lines from explainers #1 and #2 (via #4).
import json, subprocess, re, wave, numpy as np
SR = 48000; OLD = '/tmp/claude-0/-home-user-mtgtribe/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad/ex4'
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def save(p, y):
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
def lufs(p):
    o = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])
x = load('ex6v3.wav'); R = json.load(open('ex6v3_raw.json')); WW = R['original_words']
LN = json.load(open('lines_ex6.json'))           # text and word count per line (from the word check)
toks = lambda t: re.findall(r"[A-Za-z0-9']+", t)
L, WD, i = {}, {}, 0
keys = list(LN)
for n, k in enumerate(keys):
    seg = WW[i:i + len(toks(LN[k]['text']))]; i += len(seg)
    a0, b0 = seg[0]['start_time'], seg[-1]['end_time']
    prev_end = WW[i - len(seg) - 1]['end_time'] if i - len(seg) > 0 else 0.0
    next_st = WW[i]['start_time'] if i < len(WW) else len(x) / SR
    s = max(prev_end + .06, a0 - .10); e = min(next_st - .08, b0 + .14)
    y = x[int(s * SR):int(e * SR)].copy(); fi, fo = int(.012 * SR), int(.06 * SR)
    y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
    save(f'v_{k}.wav', y); g = -18.5 - lufs(f'v_{k}.wav'); save(f'v_{k}.wav', y * 10 ** (g / 20))
    L[k] = dict(file=f'v_{k}.wav', src='explainers/ex6v3.flac', a=round(s, 3), b=round(e, 3), dur=round(len(y) / SR, 3), text=LN[k]['text'])
    WD[k], j = [], 0                                  # a written word like "sign-up" is two of HeyGen's words
    for t in LN[k]['text'].split():
        m = len(toks(t)); ws = seg[j:j + m]; j += m
        WD[k].append(dict(w=t, a=round(ws[0]['start_time'] - s, 3), b=round(ws[-1]['end_time'] - s, 3)))
    assert j == len(seg), k
    print(k, L[k]['dur'], 's', round(lufs(f'v_{k}.wav'), 1), 'LUFS')
assert i == len(WW)
L4 = json.load(open(f'{OLD}/lines.json')); W4 = json.load(open(f'{OLD}/words.json'))
for k in ('hi', 'n_turn2', 'l_ifme', 'every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc'):
    L[k] = L4[k]; WD[k] = W4[k]
json.dump(L, open('lines.json', 'w'), indent=1); json.dump(WD, open('words.json', 'w')); print(len(L), 'lines')
