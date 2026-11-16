# JetUP explainer #3, "Amplify 24x: the size you trade with" (the market stall): voice placement, captions, cues
# -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's signature ending), sfx_body.json.
# Built from MTG's banked lines (0 credits). When his six new lines exist in lines.json (nhook, nstall, nmove, nlimit,
# ncalc, nrecap) the video switches to them by itself; without them the hook, the market stall, the loss limit and the
# calculator run on screen only.
# Calm, positive copy (MTG, 8 and 9 Nov 2026): inform, never frighten.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'consist', 'kit'))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
NEW = all(k in L for k in ('nhook', 'nstall', 'nmove', 'nlimit', 'ncalc', 'nrecap'))
PLAN = ['plan', 'dep', 'sonic', 'promo', 'spare', 'amp', 'six', 'expo']
TAIL = ['n_turn2', 'l_ifme', 'every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
MOVE, RECAP = ('nmove', 'nrecap') if NEW else ('swings', 'small')
ORDER = (['nhook', 'hi', 'nstall'] + PLAN + ['ncalc', 'nmove', 'nlimit', 'nrecap', 'prove'] if NEW else ['hi', 'simple'] + PLAN + ['swings', 'small', 'prove']) + TAIL
STALL, DEMO, LIM = 7.6, 7.3, 4.4              # on-screen-only passages of the banked version (seconds)
GAP = {'nhook': .6, 'hi': .45, 'simple': STALL, 'nstall': 1.7, 'plan': .3, 'dep': .15, 'sonic': .4, 'promo': .2, 'spare': .75, 'amp': .3, 'six': .7,
       'expo': 1.0 if NEW else 1.25 + DEMO, 'ncalc': 3.4, 'swings': 1.5 + LIM, 'nmove': 1.0, 'nlimit': .7, 'small': .3, 'nrecap': .3, 'prove': .7,
       'n_turn2': .45, 'l_ifme': .5, 'every': .5, 'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
VO, t = [], (.5 if NEW else 3.4)              # banked: the hook plays on screen first, then "Hi, I'm MTG"
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
def cw(key, words, frac):
    """a word cue in a new line: the first of these words that was heard, else that fraction of the line"""
    for w in words:
        try: return cue(key, w)
        except KeyError: pass
    return round(vstart[key] + frac * L[key]['dur'], 3)

SEQ = [(['one', 'hundred', 'and', 'fifty', 'five', 'dollars'], '$155'), (['forty', 'eight', 'hundred'], '$4,800'), (['six', 'thousand', 'dollars'], '$6,000'),
       (['twenty', 'four', 'times'], '24x'), (['twentyfour', 'times'], '24x'), (['twelve', 'hundred'], '$1,200'), (['two', 'hundred'], '$200'),
       (['one', 'hundred'], '$100'), (['fifty', 'dollars'], '$50'), (['ten', 'percent'], '10%'), (['five', 'percent'], '5%'), (['twentyfour'], '24'),
       (['fifty'], '$50'), (['jet', 'up'], 'JetUP'), (['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup')]
def fix(ws):
    """captions: numbers and names the way people read them ($155, 24x, $1,200, JetUP)"""
    out, i = [], 0
    nrm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
    while i < len(ws):
        for seq, rep in SEQ:
            n = len(seq)
            if [nrm(w['w']) for w in ws[i:i + n]] == seq:
                tail = re.sub(r'^[A-Za-z0-9-]+', '', ws[i + n - 1]['w'])
                out.append(dict(w=rep + tail, a=ws[i]['a'], b=ws[i + n - 1]['b'])); i += n; break
        else:
            out.append(ws[i]); i += 1
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
    if len(chunks) > 1 and len(chunks[-1]) < 3: tail_ = chunks.pop(); chunks[-1] += tail_
    for j, ch in enumerate(chunks):
        a = round((t0 - .08) if j == 0 else ch[0]['a'] - .05, 3)
        b = round(chunks[j + 1][0]['a'] - .05 if j + 1 < len(chunks) else vend[k] + .22, 3)
        caps.append(dict(a=a, b=b, w=ch))
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)

# ---- scenes ----
st0 = vstart['nstall'] if NEW else vstart['simple']
calc0 = vstart['ncalc'] if NEW else vend['expo'] + 1.25
lim0 = vstart['nlimit'] if NEW else vend['swings'] + 1.5
S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, st0 - .15], stall=[st0 - .2, vstart['plan'] - .3], plan=[vstart['plan'] - .35, vstart['amp'] - .3],
         amp=[vstart['amp'] - .35, vstart['expo'] - .3], expo=[vstart['expo'] - .35, calc0 - .3], calc=[calc0 - .35, vstart[MOVE] - .3],
         swings=[vstart[MOVE] - .35, lim0 - .3], limit=[lim0 - .35, vstart[RECAP] - .3], small=[vstart[RECAP] - .35, vstart['n_turn2'] - .3],
         turn=[vstart['n_turn2'] - .35, K['T_LINKS'] + .3], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}

# ---- cues ----
if NEW:
    h = dict(h_50=vstart['nhook'], h_like=cw('nhook', ['trades'], .2), h_12=cw('nhook', ['twelve'], .32), h_word=cw('nhook', ['Amplify'], .7))
    a = dict(a_pop=vstart['nstall'] + .1, a_one=cw('nstall', ['pay'], .3), a_shrink=cw('nstall', ['Amplify'], .55) - .2, a_24=cw('nstall', ['twentyfour', 'twenty', '24'], .86))
    a['a_leg'] = vend['nstall'] + .25
    d1, d3 = cw('ncalc', ['Calculator'], .45) + .35, cw('ncalc', ['see'], .78)
    d2, d4 = d1 + .55, d3 + .55
    w = dict(w_big=cw('nmove', ['Every'], .4), w_up=cw('nmove', ['both'], .84))
    w['w_down'] = w['w_up'] + .3
    lm = dict(l_ten=cw('nlimit', ['ten', '10'], .55), l_five=cw('nlimit', ['five', '5'], .78))
    r = dict(r_0=vstart['nrecap'] + .1, r_small=cw('nrecap', ['Start'], .62), r_prove=vstart['prove'])
else:
    h = dict(h_50=.3, h_like=.85, h_12=1.25, h_word=1.95)
    e0 = vend['simple']
    a = dict(a_pop=S['stall'][0] + .3, a_one=e0 + .35, a_shrink=e0 + 2.2, a_24=e0 + 4.2, a_leg=e0 + 5.3)
    d1, d3 = calc0 + 1.3, calc0 + 4.2
    d2, d4 = d1 + .55, d3 + .55
    w = dict(w_big=vstart['swings'] + 1.0, w_up=vstart['swings'] + 2.06, w_down=vstart['swings'] + 2.32)
    lm = dict(l_ten=lim0 + 1.1, l_five=lim0 + 2.0)
    r = dict(r_0=S['small'][0] + .25, r_small=vstart['small'], r_prove=vstart['prove'])
C = dict(p_plan=vstart['plan'], p_dep=vstart['dep'], p_sonic=vstart['sonic'] + .4, p_bal=vstart['promo'], p_bonus=vstart['promo'] + 3.1, p_200=vstart['promo'] + 3.8,
         p_spare=vstart['spare'] + .1,
         m_24=vstart['amp'] + .2, m_50=vstart['amp'] + 1.93, m_12=vstart['amp'] + 2.52, m_200=vstart['amp'] + 3.86, m_48=vstart['amp'] + 4.78, m_six=vstart['six'] + .34,
         e_expo=vstart['expo'], e_size=vstart['expo'] + 1.02, e_not=vstart['expo'] + 2.48,
         c0=calc0, d1=d1, d2=d2, d3=d3, d4=d4, l0=lim0, new=1 if NEW else 0,
         u_simple=vstart['n_turn2'], u_turn=cue('n_turn2', 'turn'), i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'MTG'), i_join=cue('l_ifme', 'Join'))
for d in (h, a, w, lm, r): C.update(d)
C = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in C.items()}
EMOS = [['money plan', '💰'], ['up and down', '📊'], ['prove itself', '✅']]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in allw]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    return None
emos = [[S_body(p), e] for p, e in EMOS if S_body(p) is not None]
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=emos, kit=[K['T_LINKS'], T], capoff=K['END_CARD'])
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt='Next: the 70/30 split', links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
kit0 = K['T_LINKS']
body = dict(whoosh=[0.05, C['a_shrink']] + [S[k][0] - .2 for k in ('hi', 'stall', 'plan', 'amp', 'expo', 'calc', 'swings', 'limit', 'small', 'turn')],
            tick=[C[k] - .05 for k in ('h_like', 'a_one', 'p_sonic', 'p_bal', 'p_bonus', 'p_spare', 'm_50', 'm_200', 'e_size', 'l_ten', 'l_five', 'r_small', 'i_url')] + ([C['r_0'] - .05] if NEW else [])
                 + [C['a_shrink'] + x for x in (.7, 1.0, 1.3, 1.6)] + [C['a_leg'], C['a_leg'] + .35],
            pop=[C['h_12'], C['h_word'], C['a_pop'] + .1, C['a_24'], C['p_dep'] + .15, C['p_200'] + .1, C['m_12'], C['m_48'], C['m_six'], C['e_not'], C['w_big'] + .15,
                 C['d2'], C['d4'], C['r_prove']],
            click=[C['d1'], C['d3'], C['i_join'] + .55])
json.dump({k: sorted(round(x, 3) for x in v if 0 <= x < kit0) for k, v in body.items()}, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as wv: x = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('NEW lines:', NEW, '| T =', T, 's'); [print(' ', k, v_) for k, v_ in S.items()]
print('kit from', K['T_LINKS'], 'end card', K['END_CARD']); print('cues', C)
for c_ in caps[:22]: print(' ', c_['a'], c_['b'], ' '.join(w_['w'] for w_ in c_['w']))
