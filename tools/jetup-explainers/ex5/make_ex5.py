# JetUP explainer #5, "The $100 Fast Start Promo" (MTG picked it 9 Nov 2026): voice placement, captions, cues ->
# stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's signature ending) and sfx_body.json.
# All MTG's banked lines, 0 credits. Positive copy (MTG, 8 Nov 2026): the rules said plainly, no loss statistics.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'consist', 'kit'))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
ORDER = ['hook', 'hi', 'plan', 'dep', 'fifty', 'hundred', 'spare', 'claim', 'cu', 'tile', 'form', 'recv', 'mail', 'two',
         'know', 'anytime', 'bonus', 'ends', 'change', 'promo', 'start', 'n_turn2', 'l_ifme',
         'every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP = {'hook': .55, 'hi': .45, 'plan': .3, 'dep': .35, 'fifty': .35, 'hundred': .4, 'spare': .7, 'claim': .45, 'cu': .45, 'tile': .45, 'form': .35,
       'recv': .5, 'mail': .4, 'two': .7, 'know': .35, 'anytime': .35, 'bonus': .35, 'ends': .35, 'change': .7, 'promo': .4, 'start': .7,
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

SEQ = [(['one', 'hundred', 'and', 'fifty', 'five', 'dollars'], '$155'), (['two', 'hundred', 'dollar'], '$200'), (['one', 'hundred', 'dollar'], '$100'),
       (['fifty', 'dollar'], '$50'), (['one', 'hundred'], '$100'), (['twelve', 'months'], '12 months'), (['jet', 'dash', 'up', 'dot', 'a', 'i'], 'jet-up.ai'),
       (['c', 'u'], 'CU'), (['copy', 'x'], 'CopyX'), (['jet', 'up'], 'JetUP'), (['fifty'], '$50'),
       (['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup')]
def fix(ws):
    """captions: names and numbers the way people read them ($155, CU number, jet-up.ai, 12 months)"""
    out, i = [], 0
    nrm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
    while i < len(ws):
        for seq, rep in SEQ:
            n = len(seq)
            if [nrm(w['w']) for w in ws[i:i + n]] == seq:
                tail = re.sub(r'^[A-Za-z0-9]+', '', ws[i + n - 1]['w'])
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
    if len(chunks) > 1 and len(chunks[-1]) < 3: chunks[-2] += chunks.pop()
    for j, ch in enumerate(chunks):
        a = round((t0 - .08) if j == 0 else ch[0]['a'] - .05, 3)
        b = round(chunks[j + 1][0]['a'] - .05 if j + 1 < len(chunks) else vend[k] + .22, 3)
        caps.append(dict(a=a, b=b, w=ch))
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['plan'] - .1], money=[vstart['plan'] - .2, vstart['claim'] - .3],
         claim=[vstart['claim'] - .35, vstart['know'] - .3], rules=[vstart['know'] - .35, vstart['promo'] - .3],
         promo=[vstart['promo'] - .35, vstart['n_turn2'] - .3], turn=[vstart['n_turn2'] - .35, K['T_LINKS'] + .3], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}
C = dict(m_plan=vstart['plan'], m_dep=cue('dep', 'deposit'), m_fifty=vstart['fifty'], m_hund=vstart['hundred'], m_adds=cue('hundred', 'adds'), m_spare=vstart['spare'],
         c_claim=vstart['claim'], c_cu=vstart['cu'], c_cun=cue('cu', 'number'), c_tile=vstart['tile'], c_orange=cue('tile', 'orange'), c_form=vstart['form'],
         c_join=cue('form', 'Join'), c_recv=vstart['recv'], c_mail=vstart['mail'], c_hub=cue('mail', 'Follower'), c_two=vstart['two'], c_50=cue('two', 'fifty'),
         c_200=cue('two', 'two', 2), r_know=vstart['know'], r_any=vstart['anytime'], r_bonus=vstart['bonus'], r_ends=vstart['ends'], r_change=vstart['change'],
         p_promo=vstart['promo'], p_start=vstart['start'], p_still=cue('start', 'still'), p_confirm=cue('start', 'confirm'),
         u_simple=vstart['n_turn2'], u_turn=cue('n_turn2', 'turn'), i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'MTG'), i_join=cue('l_ifme', 'Join'))
EMOS = [['works like this', '🎁'], ['you deposit', '💵']]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in allw]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p), e] for p, e in EMOS], kit=[K['T_LINKS'], T], capoff=K['END_CARD'])
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt='Next: step-by-step, part 1', links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)
kit0 = K['T_LINKS']
body = dict(whoosh=[0.05] + [S[k][0] - .2 for k in ('hi', 'money', 'claim', 'rules', 'promo', 'turn')],
            tick=[C[k] - .05 for k in ('m_dep', 'm_fifty', 'm_hund', 'm_spare', 'c_cu', 'c_tile', 'c_form', 'c_mail', 'r_any', 'r_bonus', 'r_ends', 'r_change', 'p_start', 'i_url')],
            pop=[C['m_adds'], C['c_recv'], C['c_200'], C['p_promo'], .9], click=[C['c_join'] + .45, C['i_join'] + .55])
json.dump({k: sorted(x for x in v if 0 <= x < kit0) for k, v in body.items()}, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
print('T =', T, 's; scenes', S); print('kit from', K['T_LINKS'], 'end card', K['END_CARD'])
