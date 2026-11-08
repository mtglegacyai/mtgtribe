# CONSISTENCY VERSION (MTG, 8 Nov 2026): the sign-up training's signature ending, with his banked save / share /
# 'We learn best when we teach others' / 'It pays to pay attention, and take action' lines.
# JetUP explainer #1, "JetUP and TAG Markets: the simple picture": voice placement, captions, cues -> stage/timeline.js
# and voice.wav. Built only from MTG's banked lines (no new voice, no credits). 16:9, 1920x1080, 25 fps.
import json, os, re, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json')))
WD = json.load(open(os.path.join(HERE, 'words.json')))
NEWL = json.load(open('/tmp/claude-0/-home-user-mtgtribe/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad/consist/lines/lines_new.json'))
for k in ('save', 'share', 'we', 'slog'):
    L['n_' + k] = dict(file='v_n_' + k + '.wav', dur=NEWL[k]['dur'], text=NEWL[k]['text']); WD['n_' + k] = NEWL[k]['words']

ORDER = ['hook', 'hi', 'simple', 'jet1', 'jet2', 'tag1', 'tag2', 'copyx', 'sonic', 'p70', 'p30', 'loss', 'lose', 'r88', 'learn',
         'verify', 'every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP_AFTER = {'hook': .55, 'hi': .45, 'simple': .35, 'jet2': .45, 'tag2': .4, 'sonic': .75, 'loss': .75, 'r88': .4, 'learn': .7,
             'verify': .5, 'every': .5, 'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
VO, t = [], .5
for k in ORDER:
    VO.append((k, round(t, 3)))
    t += L[k]['dur'] + GAP_AFTER.get(k, .28)
vstart = dict(VO)
vend = {k: round(vstart[k] + L[k]['dur'], 3) for k in ORDER}
TRACK_AT = round(vend['o_lgtc'] + .12, 3)        # the closing line "let's get this crypto, wherever I go" (2.98 s)
T = round(TRACK_AT + 3.25, 2)

def cue(key, word, nth=1):
    n = 0
    for w in WD[key]:
        if re.sub(r'\W', '', w['w']).lower() == word.lower():
            n += 1
            if n == nth:
                return round(vstart[key] + w['a'], 3)
    raise KeyError(key + ':' + word)

# captions: one block per voice line, numbers and names the way people read them
def fix(ws):
    out, i = [], 0
    while i < len(ws):
        w = ws[i]; nx = lambda n: ws[i + n]['w'] if i + n < len(ws) else ''
        if w['w'] == 'X' and nx(1).startswith('A') and nx(2).startswith('U'):
            j = i + 2
            while j + 1 < len(ws) and ws[j + 1]['w'].rstrip('.,') in ('U', 'S', 'D') and j - i < 5: j += 1
            out.append(dict(w='XAU/USD' + ('.' if ws[j]['w'].endswith('.') else ''), a=w['a'], b=ws[j]['b'])); i = j + 1; continue
        if w['w'] == 'C' and nx(1) == 'F' and nx(2).startswith('Ds'):
            out.append(dict(w='CFDs' + nx(2)[2:], a=w['a'], b=ws[i + 2]['b'])); i += 3; continue
        if w['w'] == 'eighty' and nx(1) == 'eight':
            out.append(dict(w='88', a=w['a'], b=ws[i + 1]['b'])); i += 2; continue
        if w['w'] == 'seventy': w = dict(w, w='70')
        if w['w'] == 'Thirty': w = dict(w, w='30')
        if w['w'] == 'percent': out[-1] = dict(out[-1], w=out[-1]['w'] + '%', b=w['b']); i += 1; continue
        out.append(w); i += 1
    return out
caps = []
for k, t0 in VO:
    ws = fix([dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)) for w in WD[k]])
    caps.append(dict(a=round(t0 - .08, 3), b=round(vend[k] + .22, 3), w=ws))

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['simple'] - .1], pic=[vstart['simple'] - .2, vstart['p70'] - .25],
         split=[vstart['p70'] - .3, vstart['lose'] - .3], risk=[vstart['lose'] - .35, vstart['verify'] - .25],
         next=[vstart['verify'] - .3, vstart['o_fin'] - .3], outro=[vstart['o_fin'] - .35, T])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}
C = dict(
    h1=cue('hook', 'automated'), h2=cue('hook', 'really'), h3=cue('hook', 'before'), h4=cue('hook', 'cent'),
    j_card=cue('jet1', 'JetUP'), j_comm=cue('jet1', 'community'), j_train=cue('jet1', 'training'), j_ai=cue('jet1', 'AI'),
    j_x1=cue('jet2', 'trade'), j_x2=cue('jet2', 'take'),
    t_card=cue('tag1', 'TAG'), t_broker=cue('tag1', 'broker'), t_acc=cue('tag2', 'account'), t_name=cue('tag2', 'name'),
    c_copy=cue('copyx', 'connect'), c_cx=cue('copyx', 'CopyX'),
    s_card=cue('sonic', 'Sonic'), s_gold=cue('sonic', 'gold'), s_xau=cue('sonic', 'X'),
    p_coin=vstart['p70'], p70=cue('p70', 'seventy'), p_yours=cue('p70', 'yours'), p30=cue('p30', 'Thirty'),
    p_broker=cue('p30', 'broker'), p_strat=cue('p30', 'strategy'), p_partner=cue('p30', 'partner'),
    p_loss=cue('loss', 'loss'), p_nofee=cue('loss', 'nobody'),
    r_lose=vstart['lose'], r88=cue('r88', 'eighty'), r_learn=cue('learn', 'learn'), r_decide=cue('learn', 'decide'),
    n_head=vstart['verify'], n_every=vstart['every'], n_every_old=vstart['every'], n_share=cue('every', 'share'),
    o_fin=vstart['o_fin'], o_thanks=vstart['o_thanks'], o_like=cue('o_thanks', 'like'), o_share=cue('o_thanks', 'share'),
    o_comment=cue('o_thanks', 'comment'), o_massive=vstart['o_massive'], o_best=vstart['o_best'], o_you=cue('o_best', 'YOU'),
    o_im=vstart['o_im'], o_lgtc=vstart['o_lgtc'], track=TRACK_AT)
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-mtgtribe/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad/consist/kit')
import mtg_ending as ME
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)
# the stage keeps its background, top bar and captions; its "next" card hands over to the signature ending, its outro steps aside
S['next'][1] = round(K['T_FAIR'] + 0.3, 3); S['outro'] = [-10, -9]
C['n_every'] = 1e9
for k_ in ('o_thanks', 'o_massive', 'o_best', 'o_im', 'o_lgtc', 'o_like', 'o_share', 'o_comment'): C[k_] = -5
EMOS = [['hi im mtg', '👋'], ['in your own name', '🔐'], ['trades gold', '🥇'], ['70 is yours', '💵'], ['nobody charges you', '✅'],
        ['you can lose your whole deposit', '⚠️'], ['so learn first', '📚']]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in allw]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p), e] for p, e in EMOS], kit=[K['T_LINKS'], T], capoff=K['END_CARD'])
json.dump(dict(cues=K, orient='h', nxt='Next: 5 checks before you try JetUP', links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
kit0 = K['T_LINKS']
body = dict(whoosh=[0.05] + [S[k][0] - .2 for k in ('hi', 'pic', 'split', 'risk', 'next')],
            tick=[C[k] - .05 for k in ('j_card', 't_card', 'c_copy', 's_card', 'p_coin', 'p70', 'p30', 'n_head')] +
                 [C[k] - .02 for k in ('j_comm', 'j_train', 'j_ai', 't_acc', 't_name', 'c_cx', 's_gold', 'p_broker', 'p_strat', 'p_partner', 'n_every_old')] +
                 [C[k] - .03 for k in ('j_x1', 'j_x2')] + [C['r_lose']],
            pop=[C['p_yours'], C['p_nofee']], click=[])
body = {k: sorted(t for t in v if 0 <= t < kit0) for k, v in body.items()}
json.dump(body, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')

N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('T =', T, 's;', len(caps), 'caption blocks; scenes', S)
