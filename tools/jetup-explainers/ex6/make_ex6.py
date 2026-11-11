# JetUP explainer #6, "The partner plan: the rule most people miss" (MTG approved the nine new lines on 11 Nov 2026):
# voice placement, captions, cues -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's
# signature ending), sfx_body.json. Facts: tools/learning-system/jetup-facts.md (partner plan, levels open).
# Calm, positive copy (MTG, 8 and 9 Nov 2026): inform, never frighten. JetUP's figures, no income promises.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/mtgtribe/tools/video-signature')
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
ORDER = ['nhook', 'hi', 'nlevel', 'nfloors', 'nqual', 'nfourth', 'nlots', 'nshare', 'nclient', 'nrecap', 'n_turn2', 'l_ifme', 'every',
         'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP = {'nhook': .6, 'hi': .45, 'nlevel': .6, 'nfloors': .45, 'nqual': .5, 'nfourth': 1.0, 'nlots': .6, 'nshare': .7, 'nclient': .7, 'nrecap': .6,
       'n_turn2': .45, 'l_ifme': .5, 'every': .5, 'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
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
    raise KeyError(key + ':' + word + ':' + str(nth))

SEQ = [(['two', 'hundred', 'and', 'fifty', 'dollars'], '$250'), (['one', 'hundred', 'and', 'fifty', 'five', 'dollars'], '$155'),
       (['one', 'and', 'a', 'half', 'percent'], '1.5%'), (['thirty', 'percent'], '30%'), (['eight', 'dollars'], '$8'), (['two', 'dollars'], '$2'),
       (['one', 'dollar'], '$1'), (['fifty', 'cents'], '50 cents'), (['copy', 'x'], 'CopyX'), (['jet', 'up'], 'JetUP'),
       (['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup')]
def fix(ws):
    """captions: money and percentages the way people read them ($250, 1.5%, $8)"""
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
        if not last and ((re.search(r'[.?!:]$', w['w']) and len(cur) >= 4) or (re.search(r',$', w['w']) and len(cur) >= 9)): chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    if len(chunks) > 1 and len(chunks[-1]) < 3: tail_ = chunks.pop(); chunks[-1] += tail_
    for j, ch in enumerate(chunks):
        a = round((t0 - .08) if j == 0 else ch[0]['a'] - .05, 3)
        b = round(chunks[j + 1][0]['a'] - .05 if j + 1 < len(chunks) else vend[k] + .22, 3)
        caps.append(dict(a=a, b=b, w=ch))
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['nlevel'] - .15], level=[vstart['nlevel'] - .2, vstart['nfloors'] - .3],
         build=[vstart['nfloors'] - .35, vstart['nlots'] - .3], lots=[vstart['nlots'] - .35, vstart['nshare'] - .3],
         share=[vstart['nshare'] - .35, vstart['nclient'] - .3], client=[vstart['nclient'] - .35, vstart['nrecap'] - .3],
         recap=[vstart['nrecap'] - .35, vstart['n_turn2'] - .3], turn=[vstart['n_turn2'] - .35, K['T_LINKS'] + .3], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}
C = dict(h_only=cue('nhook', 'only'), h_open=cue('nhook', 'open'), h_rule=cue('nhook', 'rule'),
         l_direct=cue('nlevel', 'direct'), l_one=cue('nlevel', 'one'), l_they=cue('nlevel', 'they'), l_two=cue('nlevel', 'two'),
         l_ten=cue('nlevel', 'ten'), l_deep=cue('nlevel', 'deep'),
         b_ten=cue('nfloors', 'ten'), b_card=cue('nfloors', 'access'), b_opens=cue('nfloors', 'opens'), b_unl=cue('nfloors', 'unlocked'),
         q_250=cue('nqual', 'two'), q_qual=cue('nqual', 'qualify'), q_one=cue('nqual', 'one'), q_three=cue('nqual', 'three'), q_str=cue('nqual', 'straight'),
         f_1=cue('nfourth', 'One'), f_2=cue('nfourth', 'two'), f_3=cue('nfourth', 'three'), f_still=cue('nfourth', 'Still'),
         f_fourth=cue('nfourth', 'fourth'), f_every=cue('nfourth', 'every'), f_next=cue('nfourth', 'next'), f_ten=cue('nfourth', 'Ten'),
         f_all=cue('nfourth', 'all'),
         p_pay=cue('nlots', 'pay'), p_lot=cue('nlots', 'Lot'), p_l1=cue('nlots', 'one'), p_l24=cue('nlots', 'one', 2), p_l510=cue('nlots', 'fifty'),
         p_eight=cue('nlots', 'eight'), p_real=cue('nlots', 'real'), p_dep=cue('nlots', 'deposits'),
         s_profit=cue('nshare', 'Profit'), s_one=cue('nshare', 'one'), s_every=cue('nshare', 'every'), s_paid=cue('nshare', 'paid'),
         s_thirty=cue('nshare', 'thirty'), s_never=cue('nshare', 'never'),
         c_train=cue('nclient', 'signup'), c_client=cue('nclient', 'client'), c_155=cue('nclient', 'one'), c_earn=cue('nclient', 'earn'),
         c_check=cue('nclient', 'check'), c_acct=cue('nclient', 'account'),
         r_250=cue('nrecap', 'two'), r_three=cue('nrecap', 'levels'), r_fourth=cue('nrecap', 'fourth'), r_next=cue('nrecap', 'next'),
         u_turn=cue('n_turn2', 'turn'), i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'MTG'), i_join=cue('l_ifme', 'Join'))
# the counter of direct partners after the 4th, one per beat through "every new one opens the next floor", 10 on "Ten"
steps = np.linspace(C['f_every'] - .05, C['f_ten'] - .45, 6)[:5]   # 5, 6, 7, 8, 9
C['f_cnt'] = [C['f_1'], C['f_2'], C['f_3'], C['f_fourth']] + [round(float(x), 3) for x in steps] + [C['f_ten']]
EMOS = [['open all ten', '🎉'], ['your partner account', '🔎']]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in allw]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p), e] for p, e in EMOS], kit=[K['T_LINKS'], T], capoff=K['END_CARD'])
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt='Next: the 70/30 split', links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
kit0 = K['T_LINKS']
body = dict(whoosh=[0.05] + [S[k][0] - .2 for k in ('hi', 'level', 'build', 'lots', 'share', 'client', 'recap', 'turn')],
            tick=[C['l_one'], C['l_two'], C['q_one'], C['q_three'] - .1] + C['f_cnt'][:3] + [C['p_l1'], C['p_l24'], C['p_l510'], C['s_every'],
                  C['r_250'], C['r_fourth'], C['i_url']],
            pop=[.9, C['h_rule'], C['l_deep'], C['f_fourth'], C['f_all'], C['p_eight'], C['s_never'], C['c_check'], C['r_next']],
            click=[C['b_card'] + .2, C['i_join'] + .55])
json.dump({k: sorted(x for x in v if 0 <= x < kit0) for k, v in body.items()}, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('T =', T, 's; scenes', S); print('kit from', K['T_LINKS'], 'end card', K['END_CARD'])
