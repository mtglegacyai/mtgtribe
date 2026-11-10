# Build timeline.js for JetUP tutorial part 1 (MTG's own recording, redacted) and voice.wav from banked lines.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, '..', 'clips')
FPS, SR = 30, 48000
L = json.load(open(os.path.join(HERE, 'lines.json')))
WD = json.load(open(os.path.join(HERE, 'words.json')))

# ---------------- voice placement (output seconds) ----------------
exec(open(os.path.join(HERE, 'vo_v2.py')).read())
VO_ORIG, T_ORIG = list(VO), T
words, spans, vstart = [], [], {}
for k, t0 in VO:
    vstart[k] = t0
    spans.append([t0, t0 + L[k]['dur']])
    for w in WD[k]:
        words.append(dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)))

# captions: show numbers and web addresses the way people read them
def fix_words(ws):
    out, i = [], 0
    while i < len(ws):
        w = ws[i]; nx = lambda n: ws[i + n]['w'] if i + n < len(ws) else ''
        if w['w'] == 'MTG' and nx(1) == 'tribe' and nx(6).startswith('up'):
            out.append(dict(w='mtgtribe.com/jetup' + ('.' if nx(6).endswith('.') else ''), a=w['a'], b=ws[i + 6]['b'])); i += 7; continue
        if w['w'] == 'one.' and out and out[-1]['w'] == 'Part':
            out.append(dict(w='1.', a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] == 'zero.': out.append(dict(w='0.', a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] == 'Jet' and re.match(r'Up\b', nx(1)):
            out.append(dict(w='JetUP' + nx(1)[2:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] == 'I' and nx(1) == 'B' and nx(2).startswith('Portal'):
            out.append(dict(w='IB ' + nx(2), a=w['a'], b=ws[i + 2]['b'])); i += 3; continue
        if w['w'] == 'Copy' and nx(1).startswith('X'):
            out.append(dict(w='CopyX' + nx(1)[1:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] in ('twelve',): out.append(dict(w='12', a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] == 'two,' and out and out[-1]['w'] == 'part': out[-1]['w'] = 'Part'; out.append(dict(w='2,', a=w['a'], b=w['b'])); i += 1; continue
        out.append(w); i += 1
    return out
words = fix_words(words)

def cue(key, word, nth=1):
    """Absolute time a word starts inside a voice line."""
    n = 0
    for w in WD[key]:
        if re.sub(r'\W', '', w['w']).lower() == word.lower():
            n += 1
            if n == nth:
                return round(vstart[key] + w['a'], 3)
    raise KeyError(key + ':' + word)

C = dict(partner=cue('partner', 'Partner'), client=cue('partner', 'Client'), ifme=vstart['ifme'],
         individual=cue('indiv', 'Individual'), upper=cue('pw', 'uppercase'), lower=cue('pw', 'lowercase'),
         number=cue('pw', 'number'), special=cue('pw', 'special'), spaces=cue('pw', 'spaces'), zero=cue('country', 'zero'),
         code=vstart['code'], security=cue('reg', 'security'), register=cue('reg', 'Register'))

# ---------------- clips (redacted frames) ----------------
meta = {c: json.load(open(os.path.join(CLIPS, c, 'meta.json'))) for c in os.listdir(CLIPS) if os.path.isfile(os.path.join(CLIPS, c, 'meta.json'))}
missing = [c for c, m in meta.items() if m.get('placeholder')]
if missing:
    print('WARNING: placeholder clips', missing)

shots = []
def shot(clip, t0, t1, src0, speed=1.0, cam=None, xfade=0.0, flash=False):
    m = meta[clip]
    cam = cam or [[t0, 360, 781, 1.29]]
    shots.append(dict(clip=clip, t0=t0, t1=t1, src0=src0, speed=speed, cstart=m['start'], n=m['n'], xfade=xfade, flash=flash,
                      cam=[[round(a, 3), b, c, d] for a, b, c, d in cam]))
def out_t(t0, src0, speed, src):
    """Output time at which source time src is shown in a shot."""
    return round(t0 + (src - src0) / speed, 3)

rings, taps, chips = [], [], []
SPEC = os.path.join(HERE, 'shots_v2.py')
exec(open(SPEC).read())        # shots, rings, taps, chips, steps, scenes, win, nocap (kept apart so they are easy to tune)


# ---------------- v3: fair-play sign-up lines (MTG, 7 Nov 2026) -> stretch the link step, insert a line at the end ----------------
D1 = 6.65                      # the link step grows (two lines replace "If that's me...")
P_END = 173.6                  # original time where "Invited by someone else? ..." is inserted
D2 = round(L['l_every']['dur'] + .35, 3)
def Wt(t):
    if t < 37.4: return t
    if t < 42.3: return 37.4 + (t - 37.4) * (42.3 + D1 - 37.4) / (42.3 - 37.4)
    if t < P_END: return t + D1
    return t + D1 + D2
def wv(x):
    if isinstance(x, (int, float)): return round(Wt(x), 3)
    if isinstance(x, list): return [wv(v) for v in x]
    return x
for sh in shots:
    sh['t0'], sh['t1'] = wv(sh['t0']), wv(sh['t1'])
    sh['cam'] = [[wv(k[0])] + k[1:] for k in sh['cam']]
for r in rings: r['t0'], r['t1'] = wv(r['t0']), wv(r['t1'])
for p in taps: p['t'] = wv(p['t'])
for c in chips: c['t0'], c['t1'] = wv(c['t0']), wv(c['t1'])
for st_ in STEPS: st_['t0'], st_['t1'] = wv(st_['t0']), wv(st_['t1'])
SCENES = {k: wv(v) for k, v in SCENES.items()}
WIN = [wv(w) for w in WIN]
C = {k: wv(v) for k, v in C.items()}
VO = [(k, round(Wt(t), 3)) for k, t in VO_ORIG if k != 'ifme'] + [('l_ifme', 37.4), ('l_other', 44.4), ('l_every', round(Wt(173.47 - 1e-6) + .3, 3))]
VO.sort(key=lambda x: x[1])
T = round(Wt(T_ORIG), 3)
words, spans, vstart = [], [], {}
for k, t0 in VO:
    vstart[k] = t0
    spans.append([t0, t0 + L[k]['dur']])
    for w in WD[k]:
        words.append(dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)))
words = fix_words(words)
C['ifme'] = vstart['l_ifme']; C['lk_url'] = cue('l_ifme', 'MTG'); C['lk_btn'] = cue('l_ifme', 'Join'); C['linktap'] = C['lk_btn'] + .5
C['lk_other'] = vstart['l_other']; C['every'] = vstart['l_every']
SCENES['link'][1] = round(vstart['l_other'] + L['l_other']['dur'] + .35, 3)

TLd = dict(fps=FPS, T=T, words=words, spans=spans, cues=C, shots=shots, rings=rings, taps=taps, chips=chips, steps=STEPS,
           nsteps=10, scenes=SCENES, win=WIN, nocap=NOCAP, plan=PLAN)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TLd) + ';\n')

# ---------------- voice track ----------------
N = int(T * SR)
v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, spans=spans, taps=[p['t'] for p in taps] + [C['linktap'], C['mailtap']], steps=[s['t0'] for s in STEPS], scenes=SCENES,
               rings=[r['t0'] for r in rings], chips=[c['t0'] for c in chips], shots=[(s['t0'], s['clip']) for s in shots]),
          open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('timeline.js written:', len(shots), 'shots,', len(rings), 'rings,', len(taps), 'taps,', len(chips), 'chips; T =', T)
for k in ('linktap', 'individual', 'register', 'mailtap', 'plan_in', 'plan_tick', 'nb'):
    print(k, C[k])
