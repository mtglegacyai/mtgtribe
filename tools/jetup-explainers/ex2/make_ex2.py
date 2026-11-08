# JetUP explainer #2, "Five names. One simple picture." (the minibus taxi): voice placement, captions, cues ->
# stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's signature ending) and sfx_body.json.
# MTG's 8 new taxi lines (8 Nov 2026, 2 credits) plus his banked lines. 16:9, 1920x1080, 25 fps.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'consist', 'kit'))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
ORDER = ['n_hook', 'hi', 'n_taxi', 'n_driver', 'track', 'n_seat', 'tag1', 'login', 'n_board', 'n_assoc', 'jet2', 'n_you', 'n_stops', 'r88', 'learn',
         'verify', 'links', 'every', 'n_save', 'n_share', 'n_we', 'n_slog',
         'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP = {'n_hook': .55, 'hi': .45, 'n_taxi': .45, 'n_driver': .3, 'track': .55, 'n_seat': .3, 'tag1': .3, 'login': .6, 'n_board': .55, 'n_assoc': .3,
       'jet2': .55, 'n_you': .7, 'n_stops': .4, 'r88': .4, 'learn': .7, 'verify': .4, 'links': .35, 'every': .5, 'n_save': .3, 'n_share': .4,
       'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
VO, t = [], .5
for k in ORDER:
    VO.append((k, round(t, 3))); t += L[k]['dur'] + GAP.get(k, .28)
vstart = dict(VO); vend = {k: round(vstart[k] + L[k]['dur'], 3) for k in ORDER}
T = round(vend['o_lgtc'] + .12 + 3.25, 2)

def cue(key, word, nth=1):
    n = 0
    for w in WD[key]:
        if re.sub(r'\W', '', w['w']).lower() == word.lower():
            n += 1
            if n == nth: return round(vstart[key] + w['a'], 3)
    raise KeyError(key + ':' + word)

def fix(ws):
    """captions: names and numbers the way people read them"""
    out, i = [], 0
    while i < len(ws):
        w = ws[i]; nx = lambda n: ws[i + n]['w'] if i + n < len(ws) else ''
        if w['w'] == 'Jet' and re.match(r'Up\b', nx(1)): out.append(dict(w='JetUP' + nx(1)[2:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] == 'Copy' and re.match(r'X\b', nx(1)): out.append(dict(w='CopyX' + nx(1)[1:], a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] == 'My' and nx(1) == 'F' and nx(2) == 'X' and nx(3).startswith('Book'):
            out.append(dict(w='Myfxbook' + nx(3)[4:], a=w['a'], b=ws[i + 3]['b'])); i += 4; continue
        if w['w'] == 'MTG' and nx(1) == 'tribe' and nx(6).startswith('up'):
            out.append(dict(w='mtgtribe.com/jetup' + ('.' if nx(6).endswith('.') else ''), a=w['a'], b=ws[i + 6]['b'])); i += 7; continue
        if w['w'] == 'C' and nx(1) == 'F' and nx(2).startswith('Ds'): out.append(dict(w='CFDs' + nx(2)[2:], a=w['a'], b=ws[i + 2]['b'])); i += 3; continue
        if w['w'] == 'eighty' and nx(1) == 'eight':
            j = i + 2; txt = '88'
            if nx(2) == 'percent': txt = '88%'; j = i + 3
            out.append(dict(w=txt, a=w['a'], b=ws[j - 1]['b'])); i = j; continue
        out.append(w); i += 1
    return out
caps = []
for k, t0 in VO:
    ws = fix([dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)) for w in WD[k]])
    chunks, cur = [], []                     # never more than two caption lines: split long lines at sentence ends
    for i, w in enumerate(ws):
        cur.append(w)
        last = i == len(ws) - 1
        if not last and ((re.search(r'[.?!]$', w['w']) and len(cur) >= 4) or (re.search(r',$', w['w']) and len(cur) >= 11)): chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    if len(chunks) > 1 and len(chunks[-1]) < 3: chunks[-2] += chunks.pop()
    for j, ch in enumerate(chunks):
        a = round((t0 - .08) if j == 0 else ch[0]['a'] - .05, 3)
        b = round(chunks[j + 1][0]['a'] - .05 if j + 1 < len(chunks) else vend[k] + .22, 3)
        caps.append(dict(a=a, b=b, w=ch))
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=True)

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['n_taxi'] - .1], taxi=[vstart['n_taxi'] - .2, vstart['n_stops'] - .3],
         stops=[vstart['n_stops'] - .35, vstart['verify'] - .25], next=[vstart['verify'] - .3, K['T_LINKS'] + .3], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}
C = dict(h_jet=cue('n_hook', 'Jet'), h_tag=cue('n_hook', 'TAG'), h_copy=cue('n_hook', 'Copy'), h_sonic=cue('n_hook', 'Sonic'), h_you=cue('n_hook', 'you', 1),
         h_mix=cue('n_hook', 'Mix'), h_sense=cue('n_hook', 'nothing'), h_one=cue('n_hook', 'one'),
         t_taxi=cue('n_taxi', 'minibus'), t_drive=cue('n_taxi', 'dont'), t_choose=cue('n_taxi', 'choose'), t_seat=cue('n_taxi', 'seat'), t_copy=cue('n_taxi', 'Copy'),
         d_sonic=vstart['n_driver'], d_trading=cue('n_driver', 'trading'), k_track=vstart['track'], k_myfx=cue('track', 'My'),
         s_seat=vstart['n_seat'], s_name=cue('n_seat', 'name'), s_tag=cue('n_seat', 'TAG'), g_broker=vstart['tag1'], g_login=cue('login', 'Log'),
         b_board=vstart['n_board'], b_puts=cue('n_board', 'puts'), a_jet=vstart['n_assoc'], a_trains=cue('n_assoc', 'trains'),
         a_no1=vstart['jet2'], a_no2=cue('jet2', 'take'), y_you=vstart['n_you'], y_which=cue('n_you', 'which'), y_much=cue('n_you', 'much'),
         p_stops=vstart['n_stops'], p_taxi=cue('n_stops', 'taxi'), p_lose=cue('n_stops', 'lose'), p_trip=cue('n_stops', 'good'),
         r88=cue('r88', 'eighty'), r_learn=cue('learn', 'learn'), n_head=vstart['verify'])
EMOS = [['youll never forget', '🧠'], ['see your own balance', '👀'], ['so learn first', '📚']]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in allw]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p), e] for p, e in EMOS], kit=[K['T_LINKS'], T], capoff=K['END_CARD'])
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt='Next: 5 checks before you try JetUP', links=True, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
kit0 = K['T_LINKS']
body = dict(whoosh=[0.05, S['hi'][0] - .2, S['taxi'][0] - .2, C['t_taxi'] - .3, S['stops'][0] - .2, C['r88'] - .5, S['next'][0] - .2],
            tick=[C[k] - .05 for k in ('h_jet', 'h_tag', 'h_copy', 'h_sonic', 'h_you', 'd_sonic', 's_seat', 'b_board', 'a_jet', 'y_you',
                                         't_drive', 't_copy', 'k_myfx', 'g_login', 'a_no1', 'a_no2', 'p_taxi', 'p_lose', 'p_trip')] + [S['next'][0] + .5, S['next'][0] + .9],
            pop=[C['h_one']], click=[])
json.dump({k: sorted(x for x in v if 0 <= x < kit0) for k, v in body.items()}, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('T =', T, 's; scenes', S); print('kit from', K['T_LINKS'], 'end card', K['END_CARD'])
