# JetUP explainer #10, "Know your numbers: the Exposure Calculator" (MTG approved the plan and the six new lines on 14 Nov 2026):
# voice placement, captions, cues -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's
# signature ending, links off, Next: the 70/30 split) and sfx_body.json (whoosh, tick, pop, click only).
# The picture: a road map that turns into MTG's real Exposure Calculator in a laptop frame, then the real page tap by tap
# (calc_shots.js takes the screenshots). Facts: the calculator page itself and tools/learning-system/jetup-facts.md.
# Calm, positive copy (MTG, 8 and 9 Nov 2026): no warnings, no red; a loss is shown as the same size as the gain.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'video-signature')))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
PLAN = json.load(open(os.path.join(HERE, 'plan.json')))
BODY = ['nhook', 'hi', 'nex', 'six', 'expo', 'nown', 'ndrag', 'swings', 'nlines', 'nlimit', 'nrecap', 'n_turn2', 'l_ifme', 'every']
assert BODY == [l['key'] for l in PLAN['lines']], 'body order differs from plan.json'
ORDER = BODY + ['n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
# pauses after each line: a little more before a new scene (Hi, Step 1, Read your exposure, Step 2, Step 3, Your lines, Recap);
# "That's six thousand dollars of exposure." and the line after it flow as one thought, as do the drag line and "Bigger
# exposure means bigger swings"; 0.75 s after the swings line, so the slider settles back to no move before the page scrolls,
# and 0.8 s after the loss limit line, so its two chips can be read before the recap
GAP = {'nhook': .6, 'hi': .55, 'nex': .5, 'six': .3, 'expo': .6, 'nown': .6, 'ndrag': .35, 'swings': .75,
       'nlines': .45, 'nlimit': .8, 'nrecap': .55, 'n_turn2': .45, 'l_ifme': .5, 'every': .5,
       'n_save': .3, 'n_share': .4, 'n_we': .5, 'n_slog': .6, 'o_dyor': .35, 'o_massive': .35, 'o_best': .35, 'o_see': .2}
VO, t = [], .5
for k in ORDER:
    VO.append((k, round(t, 3))); t += L[k]['dur'] + GAP.get(k, .28)
vstart = dict(VO); vend = {k: round(vstart[k] + L[k]['dur'], 3) for k in ORDER}
T = round(vend['o_lgtc'] + .12 + 3.25, 2)

nrm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def cue(key, word, nth=1, end=False):
    n = 0
    for w in WD[key]:
        if nrm(w['w']) == word.lower():
            n += 1
            if n == nth: return round(vstart[key] + (w['b'] if end else w['a']), 3)
    raise KeyError(key + ':' + word + ':' + str(nth))

# captions: names and numbers the way people read them (longest match first)
SEQ = [(['mtg', 'tribe', 'dot', 'com', 'slash', 'jet', 'up'], 'mtgtribe.com/jetup'),
       (['one', 'hundred', 'and', 'fifty', 'dollars'], '$150'), (['one', 'hundred', 'and', 'fifty'], '$150'),
       (['one', 'hundred', 'dollar'], '$100'), (['six', 'thousand', 'dollars'], '$6,000'), (['six', 'thousand'], '$6,000'),
       (['sixty', 'dollars'], '$60'), (['two', 'and', 'a', 'half', 'percent'], '2.5%'), (['four', 'point', 'two', 'percent'], '4.2%'),
       (['ten', 'percent'], '10%'), (['five', 'percent'], '5%'), (['one', 'percent'], '1%'), (['twentyfour'], '24'),
       (['step', 'one'], 'Step 1'), (['jet', 'ups'], 'JetUP'), (['jet', 'up'], 'JetUP')]
def fix(ws):
    out, i = [], 0
    while i < len(ws):
        for seq, rep in SEQ:
            n = len(seq)
            if [nrm(w['w']) for w in ws[i:i + n]] == seq:
                tail = re.sub(r'^[A-Za-z0-9-]+', '', ws[i + n - 1]['w'])          # keeps "'s", ",", ":" and "." after the fixed words
                out.append(dict(w=rep + tail, a=ws[i]['a'], b=ws[i + n - 1]['b'])); i += n; break
        else:
            out.append(ws[i]); i += 1
    return out
# a caption too long for one line (over 60 characters) gets its line break where it reads best: at the comma nearest the
# middle, else before the phrase word nearest the middle, else at the word nearest the middle; never one word alone on a line
PHRASE = {'to', 'and', 'so', 'because', 'but', 'or', 'in', 'on', 'for', 'with', 'when', 'if', 'that', 'which'}
def brk(ch, limit=60):
    lens = [len(w['w']) + 1 for w in ch]; tot = sum(lens)
    if tot <= limit or len(ch) < 4: return None
    cut = [(sum(lens[:i + 1]), i) for i in range(1, len(ch) - 2)]
    commas = [(abs(n - tot / 2), i) for n, i in cut if ch[i]['w'].endswith(',') and .25 <= n / tot <= .75]
    if commas: return min(commas)[1]
    phrase = [(abs(n - tot / 2), i) for n, i in cut if nrm(ch[i + 1]['w']) in PHRASE and .3 <= n / tot <= .7]
    return min(phrase)[1] if phrase else min((abs(n - tot / 2), i) for n, i in cut)[1]
# never more than two caption lines: each caption is one phrase the picture shows at the same time; a line splits after the
# words listed here (caption words, after the fixes)
SPLIT = {'nex': ['example.'], 'nown': ['multiplier.'], 'nlines': ['know.', '$150,'], 'nlimit': ['start:'],
         'nrecap': ['own,'], 'l_ifme': ['mtgtribe.com/jetup,']}
BRK = {}
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
for c0, c1 in zip(caps, caps[1:]):
    c0['b'] = min(c0['b'], c1['a'])
for k, ws in SPLIT.items():                                    # every listed split word exists in its line
    have = [w['w'] for c_ in caps for w in c_['w']]
    for s_ in ws: assert s_ in have, (k, s_)
allw = [w for c_ in caps for w in c_['w']]
K = ME.find_cues(allw, links=False)

C = dict(
    # hook: the road map, the route, the pin, the title; the map turns into the calculator in a laptop
    h_before=vstart['nhook'], h_know=cue('nhook', 'know'), h_your=cue('nhook', 'your'), h_numbers=cue('nhook', 'numbers'),
    h_like=cue('nhook', 'like'), h_map=cue('nhook', 'map'), h_road=cue('nhook', 'road'), h_trip_end=cue('nhook', 'trip', end=True),
    h_my=cue('nhook', 'my'), h_exposure=cue('nhook', 'exposure'), h_calc=cue('nhook', 'calculator'), h_map2=cue('nhook', 'map', 2),
    # step 1: tap an example
    e_step=cue('nex', 'step'), e_tap=cue('nex', 'tap'), e_example=cue('nex', 'example'), e_training=cue('nex', 'training'),
    e_150=cue('nex', 'one', 3), e_own=cue('nex', 'own'), e_plus=cue('nex', 'plus'), e_100=cue('nex', 'one', 4), e_bonus=cue('nex', 'bonus'),
    # read your exposure
    x_thats=vstart['six'], x_six=cue('six', 'six'), x_exposure=cue('six', 'exposure'),
    o_exposure=vstart['expo'], o_size=cue('expo', 'size'), o_not=cue('expo', 'not'),
    # step 2: your own numbers
    w_or=vstart['nown'], w_type=cue('nown', 'type'), w_money=cue('nown', 'money'), w_bonus=cue('nown', 'bonus'), w_mult=cue('nown', 'multiplier'),
    w_sonic=cue('nown', 'sonic'), w_amplify=cue('nown', 'amplify'), w_24=cue('nown', 'twentyfour'),
    # step 3: drag a move
    d_now=vstart['ndrag'], d_drag=cue('ndrag', 'drag'), d_one=cue('ndrag', 'one'), d_six=cue('ndrag', 'six'), d_sixty=cue('ndrag', 'sixty'),
    d_either=cue('ndrag', 'either'), d_dir_end=cue('ndrag', 'direction', end=True),
    s_bigger=vstart['swings'], s_swings=cue('swings', 'swings'), s_up=cue('swings', 'up'), s_down=cue('swings', 'down'),
    # your lines to know
    n_the=vstart['nlines'], n_lines=cue('nlines', 'lines'), n_with=cue('nlines', 'with'), n_two=cue('nlines', 'two', 2),
    n_equals=cue('nlines', 'equals'), n_150=cue('nlines', 'one'), n_about=cue('nlines', 'about'), n_four=cue('nlines', 'four'),
    n_whole=cue('nlines', 'whole'),
    m_and=vstart['nlimit'], m_loss=cue('nlimit', 'loss'), m_written=cue('nlimit', 'written'), m_ten=cue('nlimit', 'ten'),
    m_five=cue('nlimit', 'five'), m_token=cue('nlimit', 'token'),
    # recap and your turn
    rc_so=vstart['nrecap'], rc_tap=cue('nrecap', 'tap'), rc_read=cue('nrecap', 'read'), rc_drag=cue('nrecap', 'drag'), rc_know=cue('nrecap', 'know'),
    u_simple=vstart['n_turn2'], u_now=cue('n_turn2', 'now'), u_turn=cue('n_turn2', 'turn'),
    i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'mtg'), i_tap=cue('l_ifme', 'tap'), i_join=cue('l_ifme', 'join'))
C['i_press'] = round(C['i_join'] + .3, 3)                    # the Join JetUP button is tapped on "Join Jet Up"
C['e_press'] = round(C['e_example'] + .2, 3)                 # the Training example is tapped on "tap an example"
C['h_morph'] = round(C['h_my'] - .1, 3)                      # the map pulls back into the laptop on "My free Exposure Calculator"
C['n_scroll'] = round(vstart['nlines'] - .3, 3)              # the page scrolls to the last two results as the line starts
C['m_scroll'] = round(C['m_and'] - .15, 3)                   # ... and on to the loss limit note

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['nex'] - .2],
         calc=[vstart['nex'] - .3, vstart['nrecap'] - .3],
         step1=[vstart['nex'] - .3, vstart['six'] - .3], read=[vstart['six'] - .3, vstart['nown'] - .3],
         step2=[vstart['nown'] - .3, vstart['ndrag'] - .3], step3=[vstart['ndrag'] - .3, vstart['nlines'] - .3],
         lines=[vstart['nlines'] - .3, vstart['nrecap'] - .3],
         recap=[vstart['nrecap'] - .4, C['u_now'] - .05], turn=[C['u_now'] - .1, K['T_LINKS'] + .05], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}

EMOS = [[e['phrase'], e['emoji']] for e in PLAN['emoji_pops']]
EMO_AFTER = {'exposure': vstart['six']}                      # "exposure" pops on "$6,000 of exposure", not on the hook's "Exposure Calculator"
def S_body(phrase, after=0.0):
    toks = [(nrm(w['w']), w['a']) for w in allw]; want = nrm(phrase)
    for i in range(len(toks)):
        if toks[i][1] < after - 1e-6: continue
        acc = ''
        for j in range(i, min(i + 6, len(toks))):
            acc += toks[j][0]
            if acc == want: return round(toks[i][1], 3)
            if not want.startswith(acc): break
    raise KeyError(phrase)
TL = dict(fps=FPS, T=T, caps=caps, scenes=S, cues=C, emos=[[S_body(p, EMO_AFTER.get(p, 0)), e] for p, e in EMOS], kit=[K['T_LINKS'], T],
          capoff=K['END_CARD'], spans={k: [vstart[k], vend[k]] for k in BODY})
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='h', nxt=PLAN['next_chip'], links=False, T=T, fps=FPS), open(os.path.join(HERE, 'kitcues.json'), 'w'), indent=1)

# body sounds, the training's palette only: whoosh on scene changes, tick on list items and chips, pop on key highlights,
# click on taps (the Training example, grabbing the price move slider, the Join JetUP tap); never stacked
kit0 = K['T_LINKS']
body = dict(whoosh=[C['h_morph'], S['hi'][0] - .2 + .1, C['e_step'] - .15, C['w_or'] - .1, C['d_now'] - .1, C['n_scroll'] + .05,
                    S['recap'][0] - .1, C['u_now'] - .1],
            tick=[C['e_150'], C['e_100'], C['x_thats'] + .05, C['o_exposure'] + .1, C['w_money'], C['w_bonus'], C['w_mult'], C['w_24'],
                  C['d_either'], C['n_lines'], C['n_two'], C['n_four'], C['m_loss'], C['m_ten'], C['m_five'],
                  C['rc_tap'] - .1, C['rc_read'] - .1, C['rc_drag'] - .1, C['rc_know'] - .1, C['i_url']],
            pop=[C['h_numbers'], C['h_trip_end'], C['x_six'], C['d_sixty'], C['u_turn']],
            click=[C['e_press'], C['d_drag'] + .1, C['i_press']])
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
