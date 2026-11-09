# Build timeline.js and voice.wav for JetUP tutorial part 3 (verify your identity, KYC), from MTG's redacted recording
# (clips3) and his voice lines (banked + the part 2 request). Same formula and stage as part 1.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, '..', 'clips3')
FPS, SR = 30, 48000
L = json.load(open(os.path.join(HERE, 'lines.json')))
WD = json.load(open(os.path.join(HERE, 'words.json')))

# ---------------- voice placement (output seconds) ----------------
VO = [('hi', .45), ('n_thanks', 4.35), ('n_inthis', 6.8), ('n_ov1', 13.75), ('n_ov2', 18.7), ('n_ov3', 24.35),
      ('takeyour', 29.2), ('pause', 30.25),
      ('s_dash', 33.5),                                                      # 1 upload documents
      ('sumsub', 37.9), ('s_cont', 40.8),                                    # 2 Sumsub, Continue
      ('s_country', 44.3),                                                   # 3 country
      ('s_email', 48.6),                                                     # 4 Sumsub ID email
      ('s_code', 57.6), ('inbox', 63.4), ('spam', 64.5),                     # 5 the code
      ('s_save', 66.6), ('s_created', 70.5),                                 # 6 Sumsub ID account
      ('s_doc', 75.5), ('s_double', 79.4),                                   # 7 the document
      ('s_ready', 84.8), ('s_allow', 91.7), ('s_bubble', 95.0),              # 8 tips, camera, tip card
      ('s_scan', 102.5), ('s_selfie', 110.6), ('s_hold', 117.9), ('s_done', 120.2),   # 9 scan, selfie, submitted
      ('s_other', 126.6),                                                    # tip card: another profile
      ('r_intro', 137.4), ('r1', 139.55), ('r2', 143.95), ('r3', 149.1),
      ('x1', 153.8), ('x2', 158.45), ('links', 163.8), ('l_every', 171.0), ('save', 177.2), ('share', 180.1),
      ('o_fin', 182.8), ('o_dyor', 185.7), ('o_thanks', 187.7), ('o_support', 192.3), ('o_massive', 194.25),
      ('o_best', 198.25), ('o_im', 202.2), ('o_see', 205.5), ('o_lgtc', 206.8)]
T = 209.4
words, spans, vstart = [], [], {}
for k, t0 in VO:
    vstart[k] = t0
    spans.append([t0, round(t0 + L[k]['dur'], 3)])
    for w in WD[k]:
        words.append(dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)))
for (k, a), (k2, b) in zip(VO, VO[1:]):
    assert a + L[k]['dur'] <= b + 1e-6, f'voice overlap {k} -> {k2}'

# captions: numbers, web addresses and names the way people read them
def fix_words(ws):
    out, i = [], 0
    def nx(n): return ws[i + n]['w'] if i + n < len(ws) else ''
    def seq(*xs): return all(re.sub(r'\W', '', nx(j)).lower() == x for j, x in enumerate(xs))
    while i < len(ws):
        w = ws[i]
        if seq('mtg', 'tribe', 'dot', 'com', 'slash', 'jet') and nx(6).lower().startswith('up'):
            out.append(dict(w='mtgtribe.com/jetup' + ('.' if nx(6).endswith('.') else ''), a=w['a'], b=ws[i + 6]['b'])); i += 7; continue
        if seq('jet', 'up', 'dot', 'i', 'b', 'portal', 'dot', 'i', 'o'):
            out.append(dict(w='jetup.ibportal.io' + ('.' if nx(8).endswith('.') else ''), a=w['a'], b=ws[i + 8]['b'])); i += 9; continue
        if seq('portal', 'dot', 'tag', 'markets', 'dot', 'com'):
            out.append(dict(w='portal.tagmarkets.com' + (',' if nx(5).endswith(',') else ''), a=w['a'], b=ws[i + 5]['b'])); i += 6; continue
        if seq('k', 'y', 'c'):
            out.append(dict(w='KYC' + nx(2)[1:], a=w['a'], b=ws[i + 2]['b'])); i += 3; continue
        if seq('i', 'd'):
            out.append(dict(w='ID' + nx(1)[1:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if seq('c', 'u'):
            out.append(dict(w='CU', a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] in ('one.', 'one,') and out and out[-1]['w'].lower() == 'part':
            out.append(dict(w='1' + w['w'][-1], a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] in ('three.', 'three,') and out and out[-1]['w'].lower() == 'part':
            out.append(dict(w='3' + w['w'][-1], a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] in ('four.', 'four,') and out and out[-1]['w'].lower() == 'part':
            out.append(dict(w='4' + w['w'][-1], a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] == 'Jet' and re.match(r'Up\b', nx(1)):
            out.append(dict(w='JetUP' + nx(1)[2:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] == 'Sum' and nx(1).lower().startswith('sub'):
            out.append(dict(w='Sumsub' + nx(1)[3:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] == 'Copy' and nx(1).startswith('X'):
            out.append(dict(w='CopyX' + nx(1)[1:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
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

C = {}

# ---------------- clips (redacted frames) ----------------
meta = {c: json.load(open(os.path.join(CLIPS, c, 'meta.json'))) for c in os.listdir(CLIPS) if os.path.isfile(os.path.join(CLIPS, c, 'meta.json'))}
shots = []
def shot(clip, t0, t1, src0, speed=1.0, cam=None, xfade=0.0, flash=False):
    m = meta[clip]
    assert m['start'] - 1e-6 <= src0 and src0 + (t1 - t0) * speed <= m['end'] + .05, f'shot outside clip {clip}: {src0} speed {speed}'
    cam = cam or [[t0, 360, 781, 1.29]]
    shots.append(dict(clip=clip, t0=round(t0, 3), t1=round(t1, 3), src0=round(src0, 3), speed=round(speed, 4), cstart=m['start'],
                      n=m['n'], xfade=xfade, flash=flash, cam=[[round(a, 3), b, c, d] for a, b, c, d in cam]))
def out_t(t0, src0, speed, src):
    """Output time at which source time src is shown in a shot."""
    return round(t0 + (src - src0) / speed, 3)

rings, taps, chips = [], [], []
exec(open(os.path.join(HERE, 'shots_p3.py')).read())

TLd = dict(fps=FPS, T=T, words=words, spans=spans, cues=C, shots=shots, rings=rings, taps=taps, chips=chips, steps=STEPS,
           nsteps=9, scenes=SCENES, win=WIN, nocap=NOCAP, plan=PLAN, planhead='Verify your identity on TAG Markets, step by step',
           clipdir='../../clips3')
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
json.dump(dict(T=T, cues=C, spans=spans, taps=[p['t'] for p in taps] + ([C['mailtap']] if C.get('mailtap', -1) > 0 else []), steps=[s['t0'] for s in STEPS], scenes=SCENES,
               rings=[r['t0'] for r in rings], chips=[c['t0'] for c in chips], shots=[(s['t0'], s['clip']) for s in shots]),
          open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('timeline.js written:', len(shots), 'shots,', len(rings), 'rings,', len(taps), 'taps,', len(chips), 'chips; T =', T)
for k in ('plan_in', 'plan_tick', 'nb', 'mailtap'):
    print(k, C[k])
