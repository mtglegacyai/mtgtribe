# JetUP explainer #4, "The 70/30 split: where every profit goes" (MTG picked it 9 Nov 2026): voice placement, captions,
# cues -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's signature ending), sfx_body.json.
# MTG's banked lines, plus his two new lines (hook, calculator) when v_nhook.wav and v_ncalc.wav exist; without them the
# video opens with "Here is the simple picture." and the calculator demo runs on screen only.
# Calm, positive copy (MTG, 8 and 9 Nov 2026): inform, never frighten.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'consist', 'kit'))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
NEW = 'nhook' in L and 'ncalc' in L
BODY = ['seventy', 'thirty', 'ten', 'perf', 'nofee', 'nomgmt', 'myfx', 'plus30', 'before', 'times70', 'fixed']
ORDER = (['nhook', 'hi'] if NEW else ['hi', 'simple']) + BODY + (['ncalc'] if NEW else []) + ['anytime', 'small', 'prove', 'n_turn2', 'l_ifme',
         'every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
DEMO = 3.4 if NEW else 8.6                    # the calculator demo keeps going after the line (or alone, on screen only)
GAP = {'nhook': .6, 'hi': .45, 'simple': .5, 'seventy': .35, 'thirty': .4, 'ten': .7, 'perf': .35, 'nofee': .4, 'nomgmt': .7, 'myfx': .4,
       'plus30': .35, 'before': .3, 'times70': .35, 'fixed': .7 + (0 if NEW else DEMO), 'ncalc': DEMO, 'anytime': .35, 'small': .3, 'prove': .7,
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
    raise KeyError(key + ':' + word)

SEQ = [(['plus', 'thirty', 'point', 'one', 'percent'], '+30.1%'), (['thirty', 'point', 'one', 'percent'], '30.1%'), (['thirty', 'point', 'one'], '30.1'),
       (['november', 'twenty', 'twentyfour'], 'November 2024'), (['october', 'twenty', 'twentysix'], 'October 2026'),
       (['twentyone', 'percent'], '21%'), (['twentythree', 'months'], '23 months'), (['seventy', 'percent'], '70%'), (['thirty', 'percent'], '30%'),
       (['seventy', 'thirty'], '70/30'), (['ten', 'dollars'], '$10'), (['seven', 'dollars'], '$7'), (['my', 'f', 'x', 'book'], 'Myfxbook'),
       (['copy', 'x'], 'CopyX'), (['jet', 'up'], 'JetUP'), (['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup')]
def fix(ws):
    """captions: numbers and names the way people read them (70%, $10, +30.1%, Myfxbook)"""
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

calc0 = vstart['ncalc'] if NEW else vend['fixed'] + .55
hook = [0, vstart['hi'] - .15] if NEW else [vstart['simple'] - .2, vstart['seventy'] - .25]
hi = [vstart['hi'] - .25, (vstart['seventy'] if NEW else vstart['simple']) - .15]
S = dict(hook=hook, hi=hi, split=[vstart['seventy'] - .2, vstart['perf'] - .3], fees=[vstart['perf'] - .35, vstart['myfx'] - .3],
         record=[vstart['myfx'] - .35, calc0 - .3], calc=[calc0 - .35, vstart['anytime'] - .3], money=[vstart['anytime'] - .35, vstart['n_turn2'] - .3],
         turn=[vstart['n_turn2'] - .35, K['T_LINKS'] + .3], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}
if NEW:
    d1, d2, d3, d4 = cue('ncalc', 'Calculator') + .35, cue('ncalc', 'type'), cue('ncalc', 'result') + .1, cue('ncalc', 'share')
else:
    d1, d2, d3, d4 = calc0 + 1.6, calc0 + 3.4, calc0 + 5.0, calc0 + 6.6
C = dict(s_seventy=cue('seventy', 'seventy'), s_yours=cue('seventy', 'yours'), s_thirty=vstart['thirty'], s_broker=cue('thirty', 'broker'),
         s_strat=cue('thirty', 'strategy'), s_partner=cue('thirty', 'partner'), s_ten=cue('ten', 'ten'), s_seven=cue('ten', 'seven'),
         f_perf=vstart['perf'], f_profits=cue('perf', 'profits'), f_nofee=vstart['nofee'], f_nobody=cue('nofee', 'nobody'),
         f_mgmt=cue('nomgmt', 'management'), f_join=cue('nomgmt', 'join'), f_month=cue('nomgmt', 'month'), f_amp=cue('nomgmt', 'Amplify'),
         r_myfx=vstart['myfx'], r_look=cue('myfx', 'look'), r_plus=cue('plus30', 'plus'), r_nov=cue('plus30', 'November'), r_before=vstart['before'],
         r_times=vstart['times70'], r_21=cue('times70', 'twentyone'), r_months=cue('times70', 'months'), r_fixed=vstart['fixed'],
         c0=calc0, d1=round(d1, 3), d2=round(d2, 3), d3=round(d3, 3), d4=round(d4, 3), new=1 if NEW else 0,
         m_any=vstart['anytime'], m_small=vstart['small'], m_prove=vstart['prove'],
         u_simple=vstart['n_turn2'], u_turn=cue('n_turn2', 'turn'), i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'MTG'), i_join=cue('l_ifme', 'Join'))
EMOS = [['is yours', '💚'], ['look before you deposit', '👀']]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in allw]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p), e] for p, e in EMOS], kit=[K['T_LINKS'], T], capoff=K['END_CARD'])
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt='Next: the $100 Fast Start Promo', links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
kit0 = K['T_LINKS']
body = dict(whoosh=[0.05] + [S[k][0] - .2 for k in ('hi', 'split', 'fees', 'record', 'calc', 'money', 'turn')] + ([S['hook'][0] - .2] if not NEW else []),
            tick=[C[k] - .05 for k in ('s_broker', 's_strat', 's_partner', 'f_profits', 'f_mgmt', 'f_join', 'f_month', 'f_amp', 'r_nov', 'r_before', 'r_fixed', 'm_any', 'm_small', 'i_url')],
            pop=[C['s_yours'], C['s_seven'], C['f_nobody'] + .4, C['r_plus'] + .2, C['r_21'], C['m_prove'], .9 if NEW else S['hook'][0] + .6],
            click=[C['d1'], C['d2'], C['d3'], C['i_join'] + .55])
json.dump({k: sorted(x for x in v if 0 <= x < kit0) for k, v in body.items()}, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('NEW lines:', NEW, '| T =', T, 's; scenes', S); print('kit from', K['T_LINKS'], 'end card', K['END_CARD'])
