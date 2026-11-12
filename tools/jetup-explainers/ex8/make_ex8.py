# JetUP explainer #8, "Getting your money out" (MTG approved the plan and the ten new lines on 12 Nov 2026):
# voice placement, captions, cues -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's
# signature ending, links off, Next: step-by-step, part 1) and sfx_body.json (whoosh, tick, pop, click only).
# The picture: a fruit tree in your own backyard (README.md, "Scenes"). Facts: tools/learning-system/jetup-facts.md.
# Calm, positive copy (MTG, 8 and 9 Nov 2026): no warnings, no red, nothing falls; the risk stays in the signature ending.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/mtgtribe/tools/video-signature')
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
PLAN = json.load(open(os.path.join(HERE, 'plan.json')))
BODY = ['nhook', 'hi', 'ntree', 'nyard', 'nmoney', 'nfruit', 'anytime', 'nbranch', 'bonus', 'ends', 'change', 'nbasket', 'nroute', 'n48',
        'advice', 'small', 'prove', 'word', 'login', 'nrecap', 'n_turn2', 'l_ifme', 'every']
assert BODY == [l['key'] for l in PLAN['lines']], 'body order differs from plan.json'
ORDER = BODY + ['n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
# pauses after each line: a little more before a new scene; "ends" sits tight after "bonus" (the same take), so "then" still
# means twelve months; about 1 s after the 48 hours line so both chips can be read before the scene changes
GAP = {'nhook': .6, 'hi': .5, 'ntree': .6, 'nyard': .4, 'nmoney': .35, 'nfruit': .4, 'anytime': .6,
       'nbranch': .45, 'bonus': .2, 'ends': .45, 'change': .65,
       'nbasket': .5, 'nroute': .5, 'n48': 1.15,
       'advice': .3, 'small': .45, 'prove': .45, 'word': .3, 'login': .7,
       'nrecap': .55, 'n_turn2': .45, 'l_ifme': .5, 'every': .5,
       'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
VO, t = [], .5
for k in ORDER:
    VO.append((k, round(t, 3))); t += L[k]['dur'] + GAP.get(k, .28)
vstart = dict(VO); vend = {k: round(vstart[k] + L[k]['dur'], 3) for k in ORDER}
T = round(vend['o_lgtc'] + .12 + 3.25, 2)

nrm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def cue(key, word, nth=1):
    n = 0
    for w in WD[key]:
        if nrm(w['w']) == word.lower():
            n += 1
            if n == nth: return round(vstart[key] + w['a'], 3)
    raise KeyError(key + ':' + word + ':' + str(nth))
def cue_end(key, word, nth=1):
    n = 0
    for w in WD[key]:
        if nrm(w['w']) == word.lower():
            n += 1
            if n == nth: return round(vstart[key] + w['b'], 3)
    raise KeyError(key + ':' + word + ':' + str(nth))

# captions: names and numbers the way people read them; "TAG Markets" stays as it is
SEQ = [(['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup'), (['one', 'hundred', 'dollar'], '$100'),
       (['twelve', 'months'], '12 months'), (['fortyeight', 'hours'], '48 hours'), (['jet', 'ups'], 'JetUP'), (['jet', 'up'], 'JetUP'),
       (['copy', 'x'], 'CopyX')]
def fix(ws):
    out, i = [], 0
    while i < len(ws):
        for seq, rep in SEQ:
            n = len(seq)
            if [nrm(w['w']) for w in ws[i:i + n]] == seq:
                tail = re.sub(r'^[A-Za-z0-9-]+', '', ws[i + n - 1]['w'])          # keeps "'s", "," and "." after the fixed words
                out.append(dict(w=rep + tail, a=ws[i]['a'], b=ws[i + n - 1]['b'])); i += n; break
        else:
            out.append(ws[i]); i += 1
    return out
# never more than two caption lines: split long lines at sentence ends (and the recap at its colon and every comma, so each
# caption matches the card that comes in with it)
SPLIT_COMMA = {'nrecap'}
caps = []
for k, t0 in VO:
    ws = fix([dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)) for w in WD[k]])
    chunks, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        last = i == len(ws) - 1
        end = r'[.?!:]$' if k in SPLIT_COMMA else r'[.?!]$'
        if not last and ((re.search(end, w['w']) and len(cur) >= 4) or (re.search(r',$', w['w']) and (len(cur) >= 9 or (k in SPLIT_COMMA and len(cur) >= 4)))):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    if len(chunks) > 1 and len(chunks[-1]) < 3: tail_ = chunks.pop(); chunks[-1] += tail_
    for j, ch in enumerate(chunks):
        a = round((t0 - .08) if j == 0 else ch[0]['a'] - .05, 3)
        b = round(chunks[j + 1][0]['a'] - .05 if j + 1 < len(chunks) else vend[k] + .22, 3)
        caps.append(dict(a=a, b=b, w=ch))
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)

C = dict(
    # hook: the question lights word by word, then the door becomes the gate with the small mango behind it
    h_words=[cue('nhook', w) for w in ('can', 'i', 'get', 'my', 'money', 'out')], h_out_end=cue_end('nhook', 'out'),
    h_answer=cue('nhook', 'answer'), h_growing=cue('nhook', 'growing'), h_back=cue('nhook', 'backyard'),
    # the fruit tree
    t_think=vstart['ntree'], t_fruit=cue('ntree', 'fruit'), t_tree=cue('ntree', 'tree'),
    y_back=cue('nyard', 'backyard'), y_account=cue('nyard', 'account'), y_tag=cue('nyard', 'tag'), y_own=cue('nyard', 'own'),
    m_tree=cue('nmoney', 'tree'), m_own=cue('nmoney', 'own'), m_money=cue('nmoney', 'money'),
    f_bears=cue('nfruit', 'bears'), f_fruit=cue('nfruit', 'fruit'), f_profit=cue('nfruit', 'profit'),
    a_prof=vstart['anytime'], a_with=cue('anytime', 'withdrawn'), a_any=cue('anytime', 'any'),
    # the gift branch
    g_promo=cue('nbranch', 'promo'), g_gift=cue('nbranch', 'gift'), g_tied=cue('nbranch', 'tied'), g_tree=cue('nbranch', 'tree'),
    b_bonus=cue('bonus', 'bonus'), b_rel=cue('bonus', 'released'), b_twelve=cue('bonus', 'twelve'), b_months=cue('bonus', 'months'),
    e_taking=cue('ends', 'taking'), e_own=cue('ends', 'own'), e_out=cue('ends', 'out'), e_ends=cue('ends', 'ends'),
    c_rules=vstart['change'], c_check=cue('change', 'check'), c_dash=cue('change', 'dashboard'),
    # into your basket
    k_where=cue('nbasket', 'where'), k_into=cue('nbasket', 'into'), k_basket=cue('nbasket', 'basket'), k_crypto=cue('nbasket', 'crypto'),
    r_with=vstart['nroute'], r_broker=cue('nroute', 'broker'), r_wallet=cue('nroute', 'wallet'), r_address=cue('nroute', 'address'),
    r_same=cue('nroute', 'same'), r_network=cue('nroute', 'network'), r_both=cue('nroute', 'both'), r_sides=cue('nroute', 'sides'),
    r_arrive=cue('nroute', 'arrive'), r_safely=cue('nroute', 'safely'),
    n_jet=vstart['n48'], n_says=cue('n48', 'says'), n_48=cue('n48', 'fortyeight'), n_on=cue('n48', 'on'), n_avg=cue('n48', 'average'),
    # one small fruit first
    s_advice=vstart['advice'], s_start=vstart['small'], s_small2=cue('small', 'small', 2), s_with=cue('small', 'withdrawal'),
    s_early=cue('small', 'early'), p_let=vstart['prove'], p_prove=cue('prove', 'prove'),
    w_dont=vstart['word'], w_word=cue('word', 'word'), l_log=vstart['login'], l_see=cue('login', 'see'), l_bal=cue('login', 'balance'),
    # recap and your turn
    rc_so=vstart['nrecap'], rc_pick=cue('nrecap', 'pick'), rc_let=cue('nrecap', 'let'), rc_keep=cue('nrecap', 'keep'),
    rc_start=cue('nrecap', 'start'), rc_small=cue('nrecap', 'small'),
    u_simple=vstart['n_turn2'], u_now=cue('n_turn2', 'now'), u_turn=cue('n_turn2', 'turn'),
    i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'mtg'), i_tap=cue('l_ifme', 'tap'), i_join=cue('l_ifme', 'join'))
C['i_press'] = round(C['i_join'] + .3, 3)                    # the Join JetUP button is tapped on "Join Jet Up"
C['s_pick'] = round(C['s_start'] + .25, 3)                   # the small mango is picked on "Start small"
C['s_land'] = round(C['s_early'] + .05, 3)                   # ... and lands in the basket on "early"
C['w_key'] = round(C['w_word'] + .05, 3)                     # the key turns in the name plate on "my word"
C['g_open'] = round(C['t_think'] - .1, 3)                    # the gate's latch clicks open as "Think of a fruit tree" starts

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['ntree'] - .2],
         tree=[vstart['ntree'] - .3, vstart['nbranch'] - .35], gift=[vstart['nbranch'] - .4, vstart['nbasket'] - .35],
         basket=[vstart['nbasket'] - .4, vstart['advice'] - .12], small=[vstart['advice'] - .2, vstart['nrecap'] - .35],
         recap=[vstart['nrecap'] - .4, C['u_now'] + .55], turn=[C['u_now'] - .25, K['T_LINKS'] + .3], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}

EMOS = [[e['phrase'].replace('forty-eight', '48'), e['emoji']] for e in PLAN['emoji_pops']]     # caption words: "48 hours"
def S_body(phrase):
    toks = [(nrm(w['w']), w['a']) for w in allw]; want = nrm(phrase)
    for i in range(len(toks)):
        acc = ''
        for j in range(i, min(i + 6, len(toks))):
            acc += toks[j][0]
            if acc == want: return round(toks[i][1], 3)
            if not want.startswith(acc): break
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p), e] for p, e in EMOS], kit=[K['T_LINKS'], T], capoff=K['END_CARD'],
          spans={k: [vstart[k], vend[k]] for k in BODY})
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt=PLAN['next_chip'], links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)

# body sounds, the training's palette only: whoosh on scene changes, tick on list items and labels, pop on key highlights,
# click on taps (the gate's latch, the hand at the mango, the first pick, the key, the Join JetUP tap)
kit0 = K['T_LINKS']
body = dict(whoosh=[C['h_back'] - .1] + [S[k][0] - .2 for k in ('hi', 'tree', 'basket', 'small', 'recap')] + [C['g_gift'] - .15, C['u_now'] - .1],
            tick=[C['y_account'] - .05, C['m_money'] - .05, C['f_bears'] + .1, C['c_check'] - .05, C['k_crypto'] - .05, C['r_with'] + .05,
                  C['r_address'] - .05, C['r_network'], C['r_sides'], C['n_48'] - .05, C['n_on'], C['s_land'],
                  C['rc_pick'] - .1, C['rc_let'] - .1, C['rc_start'] - .1, C['i_url']],
            pop=[C['h_out_end'], C['a_any'], C['b_months'] + .05, C['k_basket'], C['r_safely'], C['p_prove'], C['u_turn']],
            click=[C['g_open'], C['a_with'] + .1, C['s_pick'], C['w_key'], C['i_press']])
json.dump({k: sorted(round(x, 3) for x in v if 0 <= x < kit0) for k, v in body.items()}, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(t0 * SR); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
if __name__ == '__main__':
    print('T =', T, 's; kit from', K['T_LINKS'], 'end card', K['END_CARD'])
    for k in BODY: print(f'  {k:8s} {vstart[k]:7.3f} -> {vend[k]:7.3f}  {L[k]["text"]}')
    for k, (a, b) in S.items(): print(f'  scene {k:7s} {a:7.3f} -> {b:7.3f}')
    for c_ in caps:
        if c_['a'] < kit0 + 8: print(f'  cap {c_["a"]:7.3f}-{c_["b"]:7.3f} ({sum(len(w["w"]) + 1 for w in c_["w"])} ch) ' + ' '.join(w['w'] for w in c_['w']))
    print('  emos', TL['emos'])
    print('  sfx', {k: len(v_) for k, v_ in json.load(open(os.path.join(HERE, 'sfx_body.json'))).items()})
