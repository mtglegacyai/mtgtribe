# Re-time the orca takes onto the v3 word timeline so the existing Avatar V lip sync still fits.
# Speech runs are stretched with Rubber Band (R3 engine) through a word-level time map; pauses are rebuilt with room tone.
import json, subprocess, os, wave, numpy as np
SR = 44100
V3 = json.load(open('/home/claude/jv/v3/voice_v3_words.json'))
DUR = V3['duration']
GAP = 0.12            # a gap this long (in either take) is a pause, not a word join
PRE, POST = 0.035, 0.07
FADE = int(0.008 * SR)
import os
RMIN, RMAX = float(os.environ.get('RMIN', 0.82)), float(os.environ.get('RMAX', 1.32))     # stretch limits that still sound natural
LEAD_SHARE = 0.4            # where leftover lip time goes: 40% before the sound, 60% after
TOL = 0.06                  # inner word anchors only when a word would be more than 60 ms off
placed = []
BAD = []
NA = []
SPC = int(float(os.environ.get('SPC', 0.04)) * SR); LR0, LR1 = float(os.environ.get('LR0', 0.62)), float(os.environ.get('LR1', 1.75))
OUT = os.environ.get('OUT', 'voice_v5.wav')

def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def room_tone(x):
    k = int(0.3 * SR); hop = 441
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    n = k // hop; sm = np.convolve(e, np.ones(n) / n, 'valid'); i = int(np.argmin(sm[50:])) + 50
    return x[i * hop:i * hop + k].copy()

def fades(y):
    y = y.copy(); f = min(FADE, len(y) // 4)
    if f > 0: y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y

def stretch(seg, anchors, out_len, tag):
    a = f'tmp_{tag}_in.wav'; b = f'tmp_{tag}_out.wav'; m = f'tmp_{tag}.map'
    pcm = np.clip(seg * 32767, -32768, 32767).astype(np.int16)
    with wave.open(a, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    with open(m, 'w') as f:
        for s, d in anchors[1:]: f.write(f'{int(s)} {int(d)}\n')   # rubberband: never list the 0 -> 0 start point
    cmd = ['rubberband', '-q', '-3'] + (['-M', m] if len(anchors) > 1 else []) + ['-D', f'{out_len / SR:.6f}', a, b]
    subprocess.run(cmd, check=True, capture_output=True)
    y = load(b)
    BAD.append(abs(len(y) - out_len) / SR)
    if len(y) < out_len: y = np.concatenate([y, np.zeros(out_len - len(y), np.float32)])
    for p in (a, b, m): os.remove(p)
    return y[:out_len]

import difflib
VB = json.load(open('/home/claude/jv/v3/all_bilabials.json'))
def bil_pairs(part):
    sb = json.load(open(f'o{part}_bil.json'))
    db = [x for x in VB if (x[2] < V3['part2_start']) == (part == 1)]
    sm = difflib.SequenceMatcher(None, [(x[0], x[1]) for x in sb], [(x[0], x[1]) for x in db], autojunk=False)
    pairs = []
    for blk in sm.get_matching_blocks():
        for j in range(blk.size): pairs.append(((sb[blk.a + j][2] + sb[blk.a + j][3]) / 2, (db[blk.b + j][2] + db[blk.b + j][3]) / 2))
    return pairs
out = np.zeros(int(round(DUR * SR)), np.float32)
report, ratios = [], []
for part in (1, 2):
    src = json.load(open(f'o{part}_words.json'))['words']; x = load(f'o{part}_raw.wav')
    dst = [w for w in V3['words'] if w['part'] == part]
    assert len(src) == len(dst), (part, len(src), len(dst))
    for s, d in zip(src, dst):
        a, b = s['word'].strip('.,?!:;').lower(), d['word'].strip('.,?!:;').lower()
        assert a.replace('’', "'") == b.replace('’', "'"), (s['word'], d['word'])
    tone = room_tone(x)
    BP = bil_pairs(part); print('part', part, 'm/b/p pairs', len(BP))
    prev_end = 0.0
    # phrases
    runs, cur = [], [0]
    for i in range(1, len(src)):
        gs, gd = src[i]['start'] - src[i - 1]['end'], dst[i]['start'] - dst[i - 1]['end']
        if gs > GAP or gd > GAP: runs.append(cur); cur = [i]
        else: cur.append(i)
    runs.append(cur)
    for k, r in enumerate(runs):
        s0, s1 = src[r[0]]['start'], src[r[-1]]['end']; d0, d1 = dst[r[0]]['start'], dst[r[-1]]['end']
        prev_gs = s0 - src[runs[k - 1][-1]]['end'] if k else s0
        prev_gd = d0 - dst[runs[k - 1][-1]]['end'] if k else d0
        next_gs = src[runs[k + 1][0]]['start'] - s1 if k + 1 < len(runs) else len(x) / SR - s1
        next_gd = dst[runs[k + 1][0]]['start'] - d1 if k + 1 < len(runs) else DUR - d1
        pre = min(PRE, prev_gs / 2, prev_gd / 2); post = min(POST, next_gs / 2, next_gd / 2)
        S0, S1 = int((s0 - pre) * SR), int((s1 + post) * SR)
        sl, dl = s1 - s0, d1 - d0
        rr = min(RMAX, max(RMIN, dl / max(1e-3, sl)))          # one gentle, capped stretch per phrase
        L = sl * rr; p0 = d0 + (dl - L) * LEAD_SHARE              # leftover lip time split before/after the sound
        if k:                                                     # never start before the previous phrase has finished
            gap_min = 0.035 if (d0 - dst[runs[k - 1][-1]]['end']) > 0.1 else 0.0
            p0 = max(p0, prev_end + gap_min); pre = min(pre, max(0.0, (p0 - prev_end) / 2))
        D0, D1 = int(round((p0 - pre) * SR)), int(round((p0 + L + post) * SR))
        # inner anchors: word starts and m/b/p sounds, mapped into the placed window
        cand = [(src[i]['start'] - s0, dst[i]['start'] - d0, 'w') for i in r[1:]]
        cand += [(sm_ - s0, dm - d0, 'b') for sm_, dm in BP if s0 + 0.03 < sm_ < s1 - 0.03 and d0 < dm < d1]
        cand.sort()
        anchors = [(0, 0)]
        for ss, dd, kind in cand:
            want = dd * L / max(1e-3, dl)
            if abs(want - ss * rr) < (0.02 if kind == 'b' else TOL) and kind == 'w': continue
            a_s, a_d = int((ss + pre) * SR), int((want + pre) * SR)
            ps, pd = anchors[-1]
            if a_s - ps < SPC or a_d - pd < SPC: continue                       # at least 40 ms apart
            if not (LR0 < (a_d - pd) / (a_s - ps) < LR1): continue                # keep the local stretch natural
            tail_s, tail_d = int((sl + pre) * SR) - a_s, int((L + pre) * SR) - a_d   # room left to the phrase end
            if tail_s > 0 and tail_d > 0 and not (0.5 < tail_d / tail_s < 2.2): continue
            anchors.append((a_s, a_d)); NA.append(kind)
        for i in r:
            sd, ds = src[i]['end'] - src[i]['start'], dst[i]['end'] - dst[i]['start']
            if sd > 0.06: ratios.append(ds / sd)
        y = stretch(x[S0:S1], anchors, D1 - D0, f'{part}_{k}')
        out[D0:D1] += fades(y)
        placed.append((part, r[0], r[-1], p0, p0 + L, d0, d1))
        prev_end = p0 + L
        report.append((part, k, len(r), round(dl / max(1e-3, sl), 3), round(rr, 3)))
    # pauses: room tone wherever no phrase was placed
    pp = [p for p in placed if p[0] == part]
    starts = [int(round((p[3] - 0.03) * SR)) for p in pp]
    ends = [int(round((p[4] + 0.05) * SR)) for p in pp]
    lo = int(round((dst[0]['start'] - 0.3) * SR)) if part == 1 else int(round((V3['part2_start'] - 0.2) * SR))
    edges = [lo] + [e for e in ends] ; nexts = starts + [int(round(((dst[-1]['end'] + 0.7) if part == 2 else (V3['part2_start'] - 0.2)) * SR))]
    for e, n in zip([lo] + ends, starts + [nexts[-1]]):
        if n - e > 2 * FADE:
            t = np.tile(tone, (n - e) // len(tone) + 2)[:n - e]
            out[max(0, e):n] += fades(t)[:n - max(0, e)]
pcm = np.clip(out * 32767, -32768, 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
r = np.array(ratios); ph = np.array([x[3] for x in report]); pc = np.array([x[4] for x in report])
print(f'capped: {int(np.sum(np.abs(ph - pc) > 1e-3))} phrases; used stretch {pc.min():.2f} to {pc.max():.2f}'); print(f'phrases {len(report)}, wanted phrase stretch median {np.median(ph):.3f} (min {ph.min():.3f}, max {ph.max():.3f}); '
      f'word stretch p5 {np.percentile(r, 5):.2f} p50 {np.median(r):.2f} p95 {np.percentile(r, 95):.2f}; out {len(out) / SR:.2f} s')
print(f'anchors used: {NA.count("w")} word starts, {NA.count("b")} m/b/p sounds'); print(f'rubberband length error max {max(BAD) * 1000:.1f} ms over {len(BAD)} phrases')
json.dump(dict(report=report, placed=placed), open('warp_report.json', 'w'))
