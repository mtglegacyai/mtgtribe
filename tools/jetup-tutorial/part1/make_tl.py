# Build timeline.js for JetUP tutorial part 1 (MTG's own recording, redacted) and voice.wav from banked lines.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, '..', 'clips')
FPS, SR = 30, 48000
L = json.load(open(os.path.join(HERE, 'lines.json')))
WD = json.load(open(os.path.join(HERE, 'words.json')))

# ---------------- voice placement (output seconds) ----------------
VO = [('p1', .30), ('create', 1.12), ('open', 3.45), ('partner', 5.85), ('ifme', 9.05), ('indiv', 15.35), ('type', 18.55),
      ('pw', 30.1), ('country', 39.2), ('code', 46.2), ('reg', 50.6), ('mail', 62.3), ('inbox', 69.1), ('spam', 70.35),
      ('links', 98.4), ('save', 106.0), ('pays', 109.2)]
T = 113.6
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
        if w['w'] == 'MTG' and nx(1) == 'tribe':
            out.append(dict(w='mtgtribe.com/jetup' + ('.' if nx(6).endswith('.') else ''), a=w['a'], b=ws[i + 6]['b'])); i += 7; continue
        if w['w'] == 'one.' and out and out[-1]['w'] == 'Part':
            out.append(dict(w='1.', a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] == 'zero.': out.append(dict(w='0.', a=w['a'], b=w['b'])); i += 1; continue
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

C = dict(partner=cue('partner', 'Partner'), client=cue('partner', 'Client'), ifme=vstart['ifme'], linktap=13.35,
         individual=cue('indiv', 'Individual'), english=cue('type', 'English'),
         upper=cue('pw', 'uppercase'), lower=cue('pw', 'lowercase'), number=cue('pw', 'number'), special=cue('pw', 'special'),
         spaces=cue('pw', 'spaces'), zero=cue('country', 'zero'), code=vstart['code'], security=cue('reg', 'security'),
         register=cue('reg', 'Register'), mail=vstart['mail'], mailtap=72.6,
         links_url=cue('links', 'MTG'), save=vstart['save'], pays=vstart['pays'])

# ---------------- clips (redacted frames) ----------------
meta = {c: json.load(open(os.path.join(CLIPS, c, 'meta.json'))) for c in os.listdir(CLIPS) if os.path.isfile(os.path.join(CLIPS, c, 'meta.json'))}
for c, (s0, e0) in dict(G=(116.6, 124.0), L=(299.0, 305.5)).items():     # still being redacted: placeholder for test frames
    meta.setdefault(c, dict(start=s0, n=int((e0 - s0) * FPS), placeholder=True))
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
SPEC = os.path.join(HERE, 'shots.py')
exec(open(SPEC).read())        # shots, rings, taps, chips, steps, scenes, win, nocap (kept apart so they are easy to tune)

TLd = dict(fps=FPS, T=T, words=words, spans=spans, cues=C, shots=shots, rings=rings, taps=taps, chips=chips, steps=STEPS,
           nsteps=10, scenes=SCENES, win=WIN, nocap=NOCAP)
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
json.dump(dict(T=T, cues=C, spans=spans, taps=[p['t'] for p in taps], steps=[s['t0'] for s in STEPS], scenes=SCENES,
               rings=[r['t0'] for r in rings], chips=[c['t0'] for c in chips], shots=[(s['t0'], s['clip']) for s in shots]),
          open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('timeline.js written:', len(shots), 'shots,', len(rings), 'rings,', len(taps), 'taps,', len(chips), 'chips; T =', T)
for k in ('linktap', 'individual', 'register', 'mailtap'):
    print(k, C[k])
