# JetUP 5 Checks v5: one steady pace.
# The approved orca voice is used at its natural timing (v4 had stretched it 0.82 to 1.32x onto the old v3 lip timing).
# Phrase speeds are gently evened out, pauses are tidied by type, four weak lines are cut, two new lines are added,
# and the AVATAR is re-timed to follow the voice (not the other way round), so the lips stay in sync.
import json, re, os, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '..', 'work')
SR, FPS = 44100, 25
COVER = 1.0          # cover frame (thumbnail) before the voice starts
LEAD = 0.14          # measured: the Avatar V lips close on m/b/p about 140 ms before their own audio
T_RATE = 5.6         # target syllables per second (natural take: 5.4)
COMPRESS = 0.4       # keep 40% of each phrase's natural deviation from the target
A_MIN, A_MAX = 0.94, 1.10
MAX_PAUSE_SPEED = 2.0

def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

SRC = {k: load(os.path.join(WORK, f'{k}_raw.wav')) for k in ('o1', 'o2', 'n1')}
O = [dict(w, src='o1') for w in json.load(open(os.path.join(WORK, 'o1_words.json')))['words']] + \
    [dict(w, src='o2') for w in json.load(open(os.path.join(WORK, 'o2_words.json')))['words']]
V3 = json.load(open(os.path.join(WORK, 'render_words.json')))['words']     # word times in the HeyGen render's own soundtrack (the old v3 list drifts up to 80 ms)
N = [dict(w, src='n1') for w in json.load(open(os.path.join(WORK, 'n1_words.json')))['words']]
assert len(O) == len(V3) == 967 and len(N) == 54

# ---- the edit: avatar blocks (word indexes into O / V3) and voice-over blocks (indexes into N)
SEQ = [('A', 0, 358),      # ... "under F S P number five five, two three seven."   [cut: "You can look it up yourself."]
       ('A', 364, 397),    # "But read the fine print." ... "covers your account."    [cut: "Also know this."]
       ('A', 400, 800),    # "Regulators in Austria" ... "slash jet up."               [cut: "And if it doesn't feel right? That's a good decision too."]
       ('V', 0, 31),       # NEW: "So here's your next step. Watch my step-by-step training ... on your phone."
       ('A', 811, 892),    # "It pays to pay attention, and take action." ... "We learn best when we teach others."  [cut: "Comment below. Which check surprised you most?"]
       ('V', 31, 54),      # NEW: "Now, comment the number of the check you'll do first, one to five. ..."
       ('A', 899, 967)]    # "Quick reminder" ... "Let's Get This Crypto!"
SECTION_STARTS = {62, 140, 256, 303, 448, 528, 621, 687, 765, 899}   # before these words: a slightly longer breath

def syl(w):
    w = re.sub(r'[^a-z]', '', w.lower())
    n = len(re.findall(r'[aeiouy]+', w)) if w else 1
    if w.endswith('e') and n > 1 and not w.endswith('le'): n -= 1
    return max(1, n)

def spoken_syl(w):
    t = w.strip('.,?!:;')
    if re.fullmatch(r'[A-Z]', t): return 1            # spelled letters: "X A U"
    return syl(t)

# ---- 1. phrases
items = []           # one per word in output order: dict(kind, idx, word, src, s, e, v3s, v3e)
for kind, a, b in SEQ:
    for i in range(a, b):
        w = O[i] if kind == 'A' else N[i]
        items.append(dict(kind=kind, idx=i, word=w['word'], src=w['src'], s=w['start'], e=w['end'],
                          v3s=V3[i]['start'] if kind == 'A' else None, v3e=V3[i]['end'] if kind == 'A' else None))

def joined(p, q):
    """True when q follows p directly in the same source take (no edit in between)."""
    return p['kind'] == q['kind'] and p['src'] == q['src'] and q['idx'] == p['idx'] + 1

phrases, cur = [], [0]
for k in range(1, len(items)):
    p, q = items[k - 1], items[k]
    gap = q['s'] - p['e']
    brk = (not joined(p, q)) or gap > 0.12 or (p['word'][-1] in '.,?!:;' and gap > 0.05)
    if brk: phrases.append(cur); cur = [k]
    else: cur.append(k)
phrases.append(cur)

# ---- 2. per-phrase speed and the pause before each phrase
def pause_for(p, q, natural):
    if q['kind'] != p['kind'] or (q['kind'] == 'A' and q['idx'] in SECTION_STARTS): return 0.55
    last = p['word'][-1]
    if p['kind'] == 'A' and p['idx'] in (257, 304, 449, 529, 622):     # "Check one." -> straight into the question
        return 0.26
    if natural is None: natural = 0.36
    if last in '.!': return float(np.clip(natural, 0.30, 0.40))
    if last == '?': return float(np.clip(natural, 0.32, 0.45))
    if last in ',:;': return float(np.clip(natural, 0.12, 0.22))
    return float(np.clip(natural, 0.06, 0.14))

out_t = COVER + 0.22
plan = []
for n, ph in enumerate(phrases):
    ws = [items[k] for k in ph]
    s0, s1 = ws[0]['s'], ws[-1]['e']
    dur = s1 - s0
    sy = sum(spoken_syl(w['word']) for w in ws)
    if len(ws) <= 3 or dur < 0.9:
        a = 1.03
    else:
        r = sy / dur
        a = float(np.clip((T_RATE * (r / T_RATE) ** COMPRESS) / r, A_MIN, A_MAX))
    if n:
        p, q = items[phrases[n - 1][-1]], ws[0]
        natural = q['s'] - p['e'] if joined(p, q) else None
        out_t += pause_for(p, q, natural)
    plan.append(dict(ph=ph, a=a, s0=s0, s1=s1, out0=out_t))
    for k in ph:
        it = items[k]
        it['ns'] = out_t + (it['s'] - s0) / a
        it['ne'] = out_t + (it['e'] - s0) / a
    out_t += dur / a
speech_end = out_t

# ---- 3. render the voice track (Rubber Band R3 per phrase, room tone in the pauses)
def room_tone(x):
    hop = 441; e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    k = 30; sm = np.convolve(e, np.ones(k) / k, 'valid'); i = int(np.argmin(sm[50:])) + 50
    return x[i * hop:i * hop + int(0.3 * SR)].copy()
tone = room_tone(SRC['o1'])
total_len = int((speech_end + 1.0) * SR)
voice = np.zeros(total_len, np.float32)
voice[:] = np.resize(tone, total_len) * 0.6
PRE, POST = 0.04, 0.08
tmp = os.path.join(HERE, 'tmp'); os.makedirs(tmp, exist_ok=True)
for n, pl in enumerate(plan):
    ws = [items[k] for k in pl['ph']]; src = ws[0]['src']; x = SRC[src]
    # padding that never reaches into the neighbouring phrase of the same take
    prev_e = items[plan[n - 1]['ph'][-1]]['e'] if n and items[plan[n - 1]['ph'][-1]]['src'] == src else -9
    next_s = items[plan[n + 1]['ph'][0]]['s'] if n + 1 < len(plan) and items[plan[n + 1]['ph'][0]]['src'] == src else 1e9
    pre = min(PRE, max(0.0, (pl['s0'] - prev_e) / 2)) if prev_e > -9 else PRE
    post = min(POST, max(0.0, (next_s - pl['s1']) / 2)) if next_s < 1e9 else POST
    a0, a1 = int((pl['s0'] - pre) * SR), int((pl['s1'] + post) * SR)
    seg = x[max(0, a0):a1]
    if abs(pl['a'] - 1) > 1e-3:
        fi, fo = os.path.join(tmp, 'i.wav'), os.path.join(tmp, 'o.wav')
        with wave.open(fi, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(['rubberband', '-q', '-3', '--formant', '-T', f'{pl["a"]:.5f}', fi, fo], check=True, capture_output=True)
        seg = load(fo)
    if src == 'n1': seg = seg * (10 ** (0.9 / 20))      # the new lines came out 0.9 dB quieter than the original takes
    f = min(int(0.008 * SR), len(seg) // 4)
    seg = seg.copy(); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    at = int((pl['out0'] - pre / pl['a']) * SR)
    end = min(total_len, at + len(seg))
    # cross-fade into the room tone under the phrase
    voice[at:end] = voice[at:end] * 0.0 + seg[:end - at]
    # short room-tone fades either side are already there; nothing else needed
def wav_out(p, y):
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
wav_out(os.path.join(HERE, 'voice_v5_dry.wav'), voice)

# ---- 4. the avatar time map: output time -> v3 render time (lips follow the new voice)
anchors = []        # (out_t, v3_t, flag)  flag: 'w' word anchor, 'cut' hard cut after, 'xf' soft skip after
A = [it for it in items if it['kind'] == 'A']
first = A[0]
anchors.append((COVER, max(0.0, first['v3s'] - (first['ns'] - COVER)), 'w'))
cuts, xfades, scenes = [], [], []
for k, it in enumerate(items):
    if it['kind'] != 'A': continue
    anchors.append((it['ns'], it['v3s'], 'w'))
    nxt = items[k + 1] if k + 1 < len(items) else None
    # inside a run of speech (next word follows within 50 ms) only word starts are anchors, so the speed is spread
    # over the whole word instead of jumping across the old take's micro-gaps
    if nxt is not None and nxt['kind'] == 'A' and nxt['idx'] == it['idx'] + 1 and nxt['ns'] - it['ne'] < 0.05:
        continue
    anchors.append((it['ne'], it['v3e'], 'w'))
    if nxt is None: continue
    if nxt['kind'] == 'A':
        o0, o1 = it['ne'], nxt['ns']; v0, v1 = it['v3e'], nxt['v3s']
        if nxt['idx'] == it['idx'] + 1:
            r = (v1 - v0) / max(1e-3, o1 - o0)
            if r > MAX_PAUSE_SPEED:     # long old pause: play both ends at the capped speed, skip the middle with a soft blend
                h = (o1 - o0) / 2
                anchors.append((o0 + h, v0 + h * MAX_PAUSE_SPEED, 'xf')); anchors.append((o0 + h + 1e-4, v1 - h * MAX_PAUSE_SPEED, 'w'))
                xfades.append(o0 + h)
        else:                           # a cut line: hard cut in the middle of the pause, hidden by a framing change
            h = (o1 - o0) / 2
            anchors.append((o0 + h, v0 + h, 'cut')); anchors.append((o0 + h + 1e-4, v1 - h, 'w'))
            cuts.append(o0 + h)
    else:                               # into a full-screen voice-over scene
        j = k + 1
        while j < len(items) and items[j]['kind'] == 'V': j += 1
        back = items[j]
        o0, o1 = it['ne'], back['ns']
        scenes.append(dict(t0=it['ne'] + 0.06, t1=back['ns'] - 0.06, words=[x for x in items[k + 1:j]]))
        h = min(1.2, (o1 - o0) / 2)
        anchors.append((o0 + h, it['v3e'] + h, 'cut')); anchors.append((o1 - h, back['v3s'] - h, 'w'))
        cuts.append(None)
last = A[-1]
anchors.append((speech_end + 6.0, last['v3e'] + 6.0, 'w'))
anchors.sort(key=lambda x: x[0])
# make it strictly increasing in output time, never backwards in source time (except across cuts)
clean = [anchors[0]]
for a in anchors[1:]:
    if a[0] <= clean[-1][0] + 1e-5: continue
    if clean[-1][2] not in ('cut', 'xf') and a[1] < clean[-1][1]: a = (a[0], clean[-1][1] + 1e-4, a[2])
    clean.append(a)
anchors = clean

TOTAL = speech_end + 0.7 + 5.0       # 0.7 s breath after "Let's Get This Crypto!", then the 5 s end card
nfr = int(round(TOTAL * FPS))
src_frames, seg_id = [], []
ai = 0; seg = 0
for f in range(nfr):
    t = f / FPS
    if t < COVER: src_frames.append(0); seg_id.append(0); continue
    while ai + 1 < len(anchors) and anchors[ai + 1][0] <= t:
        if anchors[ai + 1][2] == 'w' and anchors[ai][2] in ('cut', 'xf'): seg += 1
        ai += 1
    a, b = anchors[ai], anchors[min(ai + 1, len(anchors) - 1)]
    if a[2] in ('cut', 'xf') or b[0] == a[0]: v = a[1]
    else: v = a[1] + (b[1] - a[1]) * (t - a[0]) / (b[0] - a[0])
    src_frames.append(round(max(0.0, v - LEAD) * FPS, 3))
    seg_id.append(seg)
# local video speed report
sp = np.diff(np.array(src_frames, float)); sp = sp[(sp >= 0) & (sp < 6)]
words_out = [dict(w=it['word'], s=round(it['ns'], 3), e=round(it['ne'], 3), kind=it['kind'], idx=it['idx']) for it in items]
json.dump(dict(fps=FPS, cover=COVER, speech_end=speech_end, total=TOTAL, frames=src_frames, cuts=[c for c in cuts if c],
               xfades=xfades, scenes=[dict(t0=s['t0'], t1=s['t1']) for s in scenes], words=words_out),
          open(os.path.join(HERE, 'tl.json'), 'w'))
ass = [p['a'] for p in plan]
print(f'phrases {len(plan)}, speech {speech_end - COVER:.1f}s, total {TOTAL:.1f}s ({int(TOTAL // 60)}:{TOTAL % 60:04.1f})')
print(f'audio speed per phrase: min {min(ass):.3f} median {np.median(ass):.3f} max {max(ass):.3f}')
print(f'video speed (frames per output frame): mean {sp.mean():.3f}, p5 {np.percentile(sp, 5):.0f} p95 {np.percentile(sp, 95):.0f}; skipped pauses {len(xfades)}, cuts {len([c for c in cuts if c])}, scenes {len(scenes)}')
