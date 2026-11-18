# Build timeline.js and voice.wav for JetUP tutorial part 2 (link JetUP to TAG Markets), from MTG's redacted recording
# (clips2) and his voice lines (banked + the part 2 request). Same formula and stage as part 1.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, '..', 'clips2')
FPS, SR = 30, 48000
L = json.load(open(os.path.join(HERE, 'lines.json')))
WD = json.load(open(os.path.join(HERE, 'words.json')))

# ---------------- voice placement (output seconds) ----------------
VO = [('hi', .45), ('n_thanks', 4.35), ('n_inthis', 6.8), ('n_ov1', 13.2), ('n_ov2', 18.95), ('n_ov3', 24.2),
      ('takeyour', 29.95), ('pause', 31.0),
      ('jlogin', 34.3), ('s_same', 38.6),                                   # 1 log in to JetUP
      ('s_scroll', 42.0), ('never', 45.6),                                  # 2 the CopyX banner
      ('s_regcx', 51.55),                                                   # 3 Register CopyX
      ('s_pw', 53.9),                                                       # 4 password
      ('s_tick', 58.45), ('syncing', 62.0),                                 # 5 boxes, Sync Account
      ('s_synced', 64.4), ('s_close', 68.75), ('active', 72.0), ('s_login', 76.6),   # 6 User Active
      ('tagin', 82.9), ('s_tip', 88.7), ('s_human', 96.7),                  # 7 log in to TAG Markets
      ('s_dash', 102.6),                                                    # 8 the dashboard
      ('s_mail', 108.9), ('inbox', 115.0), ('spam', 116.1), ('s_confirm', 118.1), ('s_valid', 122.6), ('s_click', 126.0),
      ('s_done', 134.8),                                                    # 9 confirm the email
      ('r_intro', 139.4), ('r1', 141.55), ('r2', 147.45), ('r3', 151.8),
      ('x1', 157.6), ('x2', 163.2), ('links', 169.0), ('l_every', 176.2), ('save', 182.4), ('share', 185.3),
      ('o_fin', 188.0), ('o_dyor', 190.9), ('o_thanks', 192.9), ('o_support', 197.5), ('o_massive', 199.45),
      ('o_best', 203.45), ('o_im', 207.4), ('o_see', 210.7), ('o_lgtc', 212.0)]
T = 214.6
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
        if seq('i', 'd') and nx(2).lower().startswith('card'):
            out.append(dict(w='ID', a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if seq('c', 'u'):
            out.append(dict(w='CU', a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] in ('one.', 'one,') and out and out[-1]['w'].lower() == 'part':
            out.append(dict(w='1' + w['w'][-1], a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] in ('three.', 'three,') and out and out[-1]['w'].lower() == 'part':
            out.append(dict(w='3' + w['w'][-1], a=w['a'], b=w['b'])); i += 1; continue
        if w['w'] == 'Jet' and re.match(r'Up\b', nx(1)):
            out.append(dict(w='JetUP' + nx(1)[2:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
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
exec(open(os.path.join(HERE, 'shots_p2.py')).read())

TLd = dict(fps=FPS, T=T, words=words, spans=spans, cues=C, shots=shots, rings=rings, taps=taps, chips=chips, steps=STEPS,
           nsteps=9, scenes=SCENES, win=WIN, nocap=NOCAP, plan=PLAN, planhead='Link JetUP to TAG Markets, step by step',
           clipdir='../../clips2')
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
json.dump(dict(T=T, cues=C, spans=spans, taps=[p['t'] for p in taps] + [C['mailtap']], steps=[s['t0'] for s in STEPS], scenes=SCENES,
               rings=[r['t0'] for r in rings], chips=[c['t0'] for c in chips], shots=[(s['t0'], s['clip']) for s in shots]),
          open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('timeline.js written:', len(shots), 'shots,', len(rings), 'rings,', len(taps), 'taps,', len(chips), 'chips; T =', T)
for k in ('plan_in', 'plan_tick', 'nb', 'mailtap'):
    print(k, C[k])
