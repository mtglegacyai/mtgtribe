# JetUP explainer #9, "What copying really means" (MTG approved the plan and the eight new lines on 13 Nov 2026):
# voice placement, captions, cues -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's
# signature ending, links off, Next: the 70/30 split) and sfx_body.json (whoosh, tick, pop, click only).
# The picture: a community-hall cooking class (README.md, "Scenes"). Facts: tools/learning-system/jetup-facts.md.
# Calm, positive copy (MTG, 8 and 9 Nov 2026): no warnings, no red, nothing boils over; the risk stays in the signature ending.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'video-signature')))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
PLAN = json.load(open(os.path.join(HERE, 'plan.json')))
BODY = ['nhook', 'hi', 'ncook', 'ntwist', 'npot', 'deposit', 'copyx', 'nauto', 'nyours', 'myfx', 'terms', 'perf', 'nlid', 'nrecap',
        'n_turn2', 'l_ifme', 'every']
assert BODY == [l['key'] for l in PLAN['lines']], 'body order differs from plan.json'
ORDER = BODY + ['n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
# pauses after each line: a little more before a new scene; "Your pot is your own account.", the deposit line and the CopyX
# line flow as one thought; "Read the terms." and the fee line are one stretch of MTG's take, split inside its own silence,
# so 'perf' starts exactly where 'terms' ends (lines.json marks it "joined"); 0.8 s after "You don't pick the trades" and
# after "when to stop", 0.7 s after the fee line and 1.5 s after the glass lid line, so each new chip ("You don't pick the
# trades", "When to stop", "Taken from profits only", "Read only: watch, not trade or withdraw") can be read before the scene changes
GAP = {'nhook': .6, 'hi': .55, 'ncook': .5, 'ntwist': .6,
       'npot': .3, 'deposit': .3, 'copyx': .6,
       'nauto': .8, 'nyours': .8,
       'myfx': .45, 'terms': 0.0, 'perf': .7,
       'nlid': 1.5, 'nrecap': .55, 'n_turn2': .45, 'l_ifme': .5, 'every': .5,
       'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
assert L['perf'].get('joined') and GAP['terms'] == 0, "'perf' must start exactly where 'terms' ends"
VO, t = [], .5
for k in ORDER:
    VO.append((k, round(t, 3))); t += L[k]['dur'] + GAP.get(k, .28)
vstart = dict(VO); vend = {k: round(vstart[k] + L[k]['dur'], 3) for k in ORDER}
assert abs(vstart['perf'] - (vstart['terms'] + L['terms']['dur'])) < 1e-6
T = round(vend['o_lgtc'] + .12 + 3.25, 2)

nrm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def cue(key, word, nth=1, end=False):
    n = 0
    for w in WD[key]:
        if nrm(w['w']) == word.lower():
            n += 1
            if n == nth: return round(vstart[key] + (w['b'] if end else w['a']), 3)
    raise KeyError(key + ':' + word + ':' + str(nth))

# captions: names and numbers the way people read them; "TAG Markets" stays as it is
SEQ = [(['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup'), (['m', 't', 'five'], 'MT5'),
       (['my', 'f', 'x', 'book'], 'Myfxbook'), (['thirty', 'percent'], '30%'), (['metatrader', 'five'], 'MetaTrader 5'),
       (['readonly'], 'read only'), (['copy', 'x'], 'CopyX'), (['jet', 'ups'], 'JetUP'), (['jet', 'up'], 'JetUP')]
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
# a caption too long for one line (over 60 characters) gets its line break where it reads best: at the comma nearest the
# middle, else before the phrase word ("to", "and", "so", ...) nearest the middle, else at the word nearest the middle;
# never one word alone on a line (the stage puts a <br> after word br)
PHRASE = {'to', 'and', 'so', 'because', 'but', 'or', 'in', 'on', 'for', 'with', 'when', 'if', 'that', 'which'}
def brk(ch, limit=60):
    lens = [len(w['w']) + 1 for w in ch]; tot = sum(lens)
    if tot <= limit or len(ch) < 4: return None
    cut = [(sum(lens[:i + 1]), i) for i in range(1, len(ch) - 2)]              # break after word i: two words or more per line
    commas = [(abs(n - tot / 2), i) for n, i in cut if ch[i]['w'].endswith(',') and .25 <= n / tot <= .75]
    if commas: return min(commas)[1]
    phrase = [(abs(n - tot / 2), i) for n, i in cut if nrm(ch[i + 1]['w']) in PHRASE and .3 <= n / tot <= .7]
    return min(phrase)[1] if phrase else min((abs(n - tot / 2), i) for n, i in cut)[1]
# never more than two caption lines: each caption is one phrase the picture shows at the same time; a line splits after the
# words listed here (caption words, after the fixes), the signature ending at its sentence ends as in explainer #8
SPLIT = {'ncook': ['front,'], 'deposit': [], 'nauto': ['copied?', 'automatically.'], 'nyours': ['yours?', 'choices.'],
         'nlid': ['yourself?', 'app.'], 'nrecap': ['copied.', 'account,', 'choices,']}
BRK = {'deposit': 'account'}                                 # "MT5 account" stays on one line
caps = []
for k, t0 in VO:
    ws = fix([dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)) for w in WD[k]])
    chunks, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        if i == len(ws) - 1: continue
        if k in SPLIT: hit = w['w'] in SPLIT[k]
        else: hit = (re.search(r'[.?!]$', w['w']) and len(cur) >= 4) or (re.search(r',$', w['w']) and len(cur) >= 9)
        if hit: chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    if k not in SPLIT and len(chunks) > 1 and len(chunks[-1]) < 3: tail_ = chunks.pop(); chunks[-1] += tail_
    for j, ch in enumerate(chunks):
        a = round((t0 - .08) if j == 0 else ch[0]['a'] - .05, 3)
        b = round(chunks[j + 1][0]['a'] - .05 if j + 1 < len(chunks) else vend[k] + .22, 3)
        caps.append(dict(a=a, b=b, w=ch))
        br = next(i for i, w in enumerate(ch) if w['w'] == BRK[k]) if k in BRK else brk(ch)
        if br is not None: caps[-1]['br'] = br
# a caption never outlives the start of the next one: at the joined "Read the terms." / fee line (gap 0) the swap happens in the
# take's own pause, before "A", instead of the fee caption snapping on late (the stage shows the first caption that matches)
for c0, c1 in zip(caps, caps[1:]):
    c0['b'] = min(c0['b'], c1['a'])
for k, ws in SPLIT.items():                                    # every listed split word exists in its line
    have = [w['w'] for c_ in caps for w in c_['w']]
    for s_ in ws: assert s_ in have, (k, s_)
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)

C = dict(
    # hook: the title strip lights on "Copy trading", each half of the question word by word, the slots on "stays yours"
    h_copy=vstart['nhook'], h_trading=cue('nhook', 'trading'),
    h_words=[cue('nhook', 'what'), cue('nhook', 'gets'), cue('nhook', 'copied'), cue('nhook', 'what', 2), cue('nhook', 'stays'), cue('nhook', 'yours')],
    h_copied_end=cue('nhook', 'copied', end=True), h_stays=cue('nhook', 'stays'), h_yours_end=cue('nhook', 'yours', end=True),
    # the cooking class
    k_think=vstart['ncook'], k_cooking=cue('ncook', 'cooking'), k_class=cue('ncook', 'class'), k_chef=cue('ncook', 'chef'),
    k_front=cue('ncook', 'front'), k_copy=cue('ncook', 'copy'), k_step=cue('ncook', 'step'), k_own=cue('ncook', 'own'), k_pot=cue('ncook', 'pot'),
    w_and=vstart['ntwist'], w_twist=cue('ntwist', 'twist'), w_you=cue('ntwist', 'you'), w_lift=cue('ntwist', 'lift'), w_spoon=cue('ntwist', 'spoon'),
    # your pot, your account
    p_pot=cue('npot', 'pot'), p_own=cue('npot', 'own'), p_account=cue('npot', 'account'),
    d_deposit=cue('deposit', 'deposit'), d_account=cue('deposit', 'account'), d_tag=cue('deposit', 'tag'), d_name=cue('deposit', 'name'),
    x_then=vstart['copyx'], x_connect=cue('copyx', 'connect'), x_strategy=cue('copyx', 'strategy'), x_copyx=cue('copyx', 'copyx'),
    # what gets copied
    a_what=cue('nauto', 'what'), a_trades=cue('nauto', 'strategys'), a_trades2=cue('nauto', 'trades'), a_into=cue('nauto', 'into'),
    a_account=cue('nauto', 'account'), a_auto=cue('nauto', 'automatically'), a_dont=cue('nauto', 'dont'), a_pick=cue('nauto', 'pick'),
    # what stays yours
    y_what=cue('nyours', 'what'), y_own=cue('nyours', 'own'), y_choices=cue('nyours', 'choices'), y_pick=cue('nyours', 'pick'),
    y_strategy=cue('nyours', 'strategy'), y_how=cue('nyours', 'how'), y_when=cue('nyours', 'when'), y_stop=cue('nyours', 'stop'),
    # look before you pick
    f_sonic=vstart['myfx'], f_track=cue('myfx', 'track'), f_my=cue('myfx', 'my'), f_look=cue('myfx', 'look'), f_deposit=cue('myfx', 'deposit'),
    r_read=vstart['terms'], r_terms=cue('terms', 'terms'), r_thirty=cue('perf', 'thirty'), r_perf=cue('perf', 'performance'),
    r_taken=cue('perf', 'taken'), r_profits=cue('perf', 'profits'),
    # the glass lid
    l_want=vstart['nlid'], l_pot=cue('nlid', 'pot'), l_glass=cue('nlid', 'glass'), l_lid=cue('nlid', 'lid'), l_meta=cue('nlid', 'metatrader'),
    l_with=cue('nlid', 'with'), l_investor=cue('nlid', 'investor'), l_password=cue('nlid', 'password'), l_watch=cue('nlid', 'watch'),
    l_every=cue('nlid', 'every'), l_read=cue('nlid', 'readonly'),
    # recap and your turn
    rc_so=vstart['nrecap'], rc_trades=cue('nrecap', 'trades'), rc_money=cue('nrecap', 'money'), rc_make=cue('nrecap', 'make'),
    rc_three=cue('nrecap', 'three'), rc_watch=cue('nrecap', 'watch'),
    u_simple=vstart['n_turn2'], u_now=cue('n_turn2', 'now'), u_turn=cue('n_turn2', 'turn'),
    i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'mtg'), i_tap=cue('l_ifme', 'tap'), i_join=cue('l_ifme', 'join'))
C['i_press'] = round(C['i_join'] + .3, 3)                    # the Join JetUP button is tapped on "Join Jet Up"
C['w_rest'] = round(C['w_lift'] + .05, 3)                    # the spoon lies on its rest on "lift" (carried there after "twist?")
C['w_self'] = round(C['w_spoon'] + .55, 3)                   # ... then your pot gives one stir by itself: how?
C['l_tap'] = round(C['l_password'] + .25, 3)                 # the eye icon is tapped on "password"
C['l_screen'] = round(C['l_investor'] - .35, 3)              # the real screen slides in just before "investor"

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['ncook'] - .2],
         cook=[vstart['ncook'] - .3, vstart['npot'] - .35], acct=[vstart['npot'] - .4, vstart['nauto'] - .35],
         copied=[vstart['nauto'] - .4, vstart['nyours'] - .35], yours=[vstart['nyours'] - .4, vstart['myfx'] - .35],
         look=[vstart['myfx'] - .4, vstart['nlid'] - .35], lid=[vstart['nlid'] - .4, vstart['nrecap'] - .35],
         recap=[vstart['nrecap'] - .4, C['u_now'] + .55], turn=[C['u_now'] - .25, K['T_LINKS'] + .05], outro=[-10, -9])   # the turn scene is gone before the kit's url pill
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}

EMOS = [[e['phrase'], e['emoji']] for e in PLAN['emoji_pops']]
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
# click on taps (the spoon set down on its rest, the CopyX line drawing, the eye icon, the Join JetUP tap); never stacked
kit0 = K['T_LINKS']
body = dict(whoosh=[S[k][0] - .2 for k in ('hi', 'cook', 'recap')] + [C['a_into'] - .1, C['r_read'] - .1, C['l_want'] - .15, C['u_now'] - .1],
            tick=[C['k_step'] - .05, C['k_pot'] - .05, C['p_own'], C['d_deposit'], C['d_tag'] + .05, C['x_strategy'],
                  C['a_what'], C['a_trades2'], C['y_what'], C['y_strategy'], C['y_how'], C['y_when'], C['f_my'], C['r_perf'],
                  C['l_meta'], C['l_read'], C['rc_trades'] - .1, C['rc_money'] - .1, C['rc_make'] - .1, C['rc_watch'] - .1, C['i_url']],
            pop=[C['h_copied_end'], C['h_yours_end'], C['a_dont'], C['f_sonic'] + .05, C['l_lid'], C['u_turn']],
            click=[C['w_rest'], C['x_copyx'] + .1, C['l_tap'], C['i_press']])
SFX = {k: sorted(round(x, 3) for x in v if 0 <= x < kit0) for k, v in body.items()}
allsfx = sorted((x, k) for k, v in SFX.items() for x in v)
for (x0, k0), (x1, k1) in zip(allsfx, allsfx[1:]):
    assert x1 - x0 >= .2, ('sounds stacked', k0, x0, k1, x1)
json.dump(SFX, open(os.path.join(HERE, 'sfx_body.json'), 'w'))
N = int(round(T * SR)); v = np.zeros(N, np.float32)
for k, t0 in VO:
    with wave.open(os.path.join(HERE, L[k]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(round(t0 * SR)); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, cues=C, scenes=S, spans=[[t0, vend[k]] for k, t0 in VO]), open(os.path.join(HERE, 'mixcues.json'), 'w'))
if __name__ == '__main__':
    print('T =', T, 's; kit from', K['T_LINKS'], 'end card', K['END_CARD'])
    for k in BODY: print(f'  {k:8s} {vstart[k]:7.3f} -> {vend[k]:7.3f}  {L[k]["text"]}')
    for k, (a, b) in S.items(): print(f'  scene {k:7s} {a:7.3f} -> {b:7.3f}')
    for c_ in caps:
        if c_['a'] < kit0 + 8: print(f'  cap {c_["a"]:7.3f}-{c_["b"]:7.3f} ({sum(len(w["w"]) + 1 for w in c_["w"])} ch) ' + ' '.join(w['w'] + (' /' if i == c_.get('br') else '') for i, w in enumerate(c_['w'])))
    print('  emos', TL['emos'])
    print('  sfx', {k: len(v_) for k, v_ in SFX.items()}, 'closest pair %.2f s' % min(b[0] - a[0] for a, b in zip(allsfx, allsfx[1:])))
