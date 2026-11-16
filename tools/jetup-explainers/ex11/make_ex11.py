# JetUP explainer #11, "The Infinity Bonus: two strong wheels" (MTG approved the plan and the seven new lines on 15 Nov 2026):
# voice placement, captions, cues -> stage/timeline.js, voice.wav, mixcues.json, kitcues.json (the 9:09 training's
# signature ending, links off, Next: step-by-step, part 1) and sfx_body.json (whoosh, tick, pop, click only).
# The picture: explainer #6's ten glass floors open upward to an infinity sign; ten 1.5% Profit Share bars with the lime
# Infinity layer on top, past level 10; then one bicycle that stays and grows: its gear cassette is the rate scale, its
# trip meter the month's new volume, its two wheels the 50% rule, a partner's bicycle the difference rule.
# Facts: JetUP's business plan (Oct 2026), the Partner Plan page "Infinity" section, tools/learning-system/jetup-facts.md.
# Calm, positive copy (MTG, 8 and 9 Nov 2026): no warnings, no red, no example incomes, no promises.
import json, os, re, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'video-signature')))
import mtg_ending as ME
FPS, SR = 25, 48000
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words.json')))
PLAN = json.load(open(os.path.join(HERE, 'plan.json')))
BODY = ['nhook', 'hi', 'nshare', 'ntop', 'nbike', 'nmonth', 'nfifty', 'ndiff', 'nrecap', 'n_turn2', 'l_ifme', 'every']
assert BODY == [l['key'] for l in PLAN['lines']], 'body order differs from plan.json'
ORDER = BODY + ['n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
# pauses after each line: a little more before a new scene (Hi, Profit Share, the bicycle, monthly, Rule 1, Rule 2, recap);
# the Profit Share line and "It's a leadership bonus on top of the Profit Share" are one picture and flow as one thought;
# 1.3 s after the difference rule line, so its last chip (all your other lines: your full rate) can be read
GAP = {'nhook': .6, 'hi': .55, 'nshare': .4, 'ntop': .6, 'nbike': .5, 'nmonth': .6, 'nfifty': .6, 'ndiff': 1.3,
       'nrecap': .55, 'n_turn2': .45, 'l_ifme': .5, 'every': .5,
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
       (['one', 'and', 'a', 'half', 'percent'], '1.5%'), (['fifty', 'thousand', 'dollars'], '$50K'),
       (['seven', 'and', 'a', 'half'], '7.5%'), (['forty', 'million'], '$40M'), (['one', 'and', 'a', 'half'], '1.5%'),
       (['fifty', 'percent'], '50%'), (['three', 'percent'], '3%'), (['thirty', 'percent'], '30%'),
       (['ten', 'levels'], '10 levels'), (['level', 'one'], 'level 1'), (['rule', 'one'], 'Rule 1'), (['rule', 'two'], 'Rule 2'),
       (['jet', 'ups'], 'JetUP'), (['jet', 'up'], 'JetUP')]
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
PHRASE = {'to', 'and', 'so', 'because', 'but', 'or', 'in', 'on', 'for', 'with', 'when', 'if', 'that', 'which', 'from', 'paid', 'never', 'you'}
def brk(ch, limit=60):
    lens = [len(w['w']) + 1 for w in ch]; tot = sum(lens)
    if tot <= limit or len(ch) < 4: return None
    cut = [(sum(lens[:i + 1]), i) for i in range(1, len(ch) - 2)]
    commas = [(abs(n - tot / 2), i) for n, i in cut if ch[i]['w'].endswith((',', ':')) and .25 <= n / tot <= .75]
    if commas: return min(commas)[1]
    phrase = [(abs(n - tot / 2), i) for n, i in cut if nrm(ch[i + 1]['w']) in PHRASE and .3 <= n / tot <= .7]
    return min(phrase)[1] if phrase else min((abs(n - tot / 2), i) for n, i in cut)[1]
# never more than two caption lines: each caption is one phrase the picture shows at the same time; a line splits after the
# words listed here (caption words, after the fixes)
SPLIT = {'nhook': ['limit.'], 'nshare': ['level,'], 'nbike': ['gears.', 'month:'], 'nmonth': ['month:'],
         'nfifty': ['half.'], 'ndiff': ['rule:', 'structure.'], 'l_ifme': ['mtgtribe.com/jetup,']}
BRK = {'nshare': 'profit'}                                     # the break inside a caption, where the default would read worse
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
        br = next((i for i, w in enumerate(ch) if w['w'] == BRK.get(k)), None) if k in BRK and brk(ch) is not None else brk(ch)
        if br is not None: caps[-1]['br'] = br
for c0, c1 in zip(caps, caps[1:]):
    c0['b'] = min(c0['b'], c1['a'])
for k, ws in SPLIT.items():                                    # every listed split word exists in its line
    have = [w['w'] for c_ in caps for w in c_['w']]
    for s_ in ws: assert s_ in have, (k, s_)
allw = [w for c_ in caps for w in c_['w']]
assert not any(ch in w['w'] for w in allw for ch in (chr(0x2013), chr(0x2014))), 'dash in a caption'
K = ME.find_cues(allw, links=False)

C = dict(
    # hook: the ten glass floors light, the top opens upward to an infinity sign, the title, no depth limit
    h_ten=cue('nhook', 'ten'), h_levels=cue('nhook', 'levels'), h_not=cue('nhook', 'not'), h_limit=cue('nhook', 'limit'),
    h_limit_end=cue('nhook', 'limit', end=True), h_meet=cue('nhook', 'meet'), h_infinity=cue('nhook', 'infinity'),
    h_bonus=cue('nhook', 'bonus'), h_no=cue('nhook', 'no'), h_depth=cue('nhook', 'depth'), h_all_end=cue('nhook', 'all', end=True),
    # the base: Profit Share, ten 1.5% level bars, paid from the 30% share
    s_and=vstart['nshare'], s_profit=cue('nshare', 'profit'), s_one=cue('nshare', 'one'), s_percent=cue('nshare', 'percent'),
    s_strategy=cue('nshare', 'strategys'), s_every=cue('nshare', 'every'), s_open=cue('nshare', 'open'), s_level=cue('nshare', 'level'),
    s_paid=cue('nshare', 'paid'), s_thirty=cue('nshare', 'thirty'), s_never=cue('nshare', 'never'), s_client=cue('nshare', 'client'),
    # on top of Profit Share: the lime Infinity layer, from level 1, all the way down
    p_its=vstart['ntop'], p_leadership=cue('ntop', 'leadership'), p_top=cue('ntop', 'top'), p_profit=cue('ntop', 'profit'),
    p_from=cue('ntop', 'from'), p_level=cue('ntop', 'level'), p_one=cue('ntop', 'one'), p_all=cue('ntop', 'all'), p_down=cue('ntop', 'down'),
    p_down_end=cue('ntop', 'down', end=True),
    # the bicycle: the gear cassette is the scale, the trip meter the month's new volume
    b_think=vstart['nbike'], b_bicycle=cue('nbike', 'bicycle'), b_gears=cue('nbike', 'gears'), b_your=cue('nbike', 'your'),
    b_gear=cue('nbike', 'gear'), b_rate=cue('nbike', 'rate'), b_set=cue('nbike', 'set'), b_team=cue('nbike', 'teams'),
    b_new=cue('nbike', 'new'), b_volume=cue('nbike', 'volume'), b_each=cue('nbike', 'each'), b_month=cue('nbike', 'month'),
    b_from=cue('nbike', 'from'), b_one=cue('nbike', 'one'), b_fifty=cue('nbike', 'fifty'), b_dollars_end=cue('nbike', 'dollars', end=True),
    b_seven=cue('nbike', 'seven'), b_half2_end=cue('nbike', 'half', 2, end=True), b_forty=cue('nbike', 'forty'),
    b_million_end=cue('nbike', 'million', end=True),
    # monthly: the trip meter resets with a calendar flip; only the month's new volume counts; paid once a month
    m_and=vstart['nmonth'], m_trip=cue('nmonth', 'trip'), m_resets=cue('nmonth', 'resets'), m_every=cue('nmonth', 'every'),
    m_month=cue('nmonth', 'month'), m_only=cue('nmonth', 'only'), m_new=cue('nmonth', 'new'), m_counts=cue('nmonth', 'counts'),
    m_paid=cue('nmonth', 'paid'), m_once=cue('nmonth', 'once'),
    # Rule 1: two strong wheels
    f_rule=vstart['nfifty'], f_fifty=cue('nfifty', 'fifty'), f_strongest=cue('nfifty', 'strongest'), f_line=cue('nfifty', 'line'),
    f_counts=cue('nfifty', 'counts'), f_most=cue('nfifty', 'most'), f_half=cue('nfifty', 'half'), f_half_end=cue('nfifty', 'half', end=True),
    f_bike=cue('nfifty', 'bike'), f_two=cue('nfifty', 'two'), f_strong=cue('nfifty', 'strong'), f_wheels=cue('nfifty', 'wheels'),
    # Rule 2: the difference rule
    d_rule=vstart['ndiff'], d_difference=cue('ndiff', 'difference'), d_if=cue('ndiff', 'if'), d_partner=cue('ndiff', 'partner'),
    d_line=cue('ndiff', 'line'), d_reaches=cue('ndiff', 'reaches'), d_own=cue('ndiff', 'own'), d_rate=cue('ndiff', 'rate'),
    d_earn=cue('ndiff', 'earn'), d_difference2=cue('ndiff', 'difference', 2), d_structure=cue('ndiff', 'structure'),
    d_three=cue('ndiff', 'three'), d_minus=cue('ndiff', 'minus'), d_their2=cue('ndiff', 'their', 3), d_one=cue('ndiff', 'one'),
    d_leaves=cue('ndiff', 'leaves'), d_one2=cue('ndiff', 'one', 2), d_half2_end=cue('ndiff', 'half', 2, end=True),
    # recap and your turn
    rc_so=vstart['nrecap'], rc_infinity=cue('nrecap', 'infinity'), rc_gear=cue('nrecap', 'gear'), rc_whole=cue('nrecap', 'whole'),
    rc_two=cue('nrecap', 'two'), rc_wheels=cue('nrecap', 'wheels'), rc_and=cue('nrecap', 'and'), rc_diff=cue('nrecap', 'difference'),
    u_simple=vstart['n_turn2'], u_now=cue('n_turn2', 'now'), u_turn=cue('n_turn2', 'turn'),
    i_go=cue('l_ifme', 'go'), i_url=cue('l_ifme', 'mtg'), i_tap=cue('l_ifme', 'tap'), i_join=cue('l_ifme', 'join'))
C['i_press'] = round(C['i_join'] + .3, 3)                    # the Join JetUP button is tapped on "Join Jet Up"
C['h_open'] = round(C['h_limit'] - .05, 3)                   # the top floor opens upward on "the limit"
# the chain climbs the cassette one gear at a time on "to seven and a half" (1.5% on "one and a half", 7.5% as he says it)
C['b_climb'] = [round(C['b_seven'] - .35 + i * (C['b_half2_end'] - C['b_seven'] + .2) / 8, 3) for i in range(9)]
C['b_climb'][0] = round(C['b_one'] - .05, 3)

S = dict(hook=[0, vstart['hi'] - .15], hi=[vstart['hi'] - .25, vstart['nshare'] - .2],
         share=[vstart['nshare'] - .3, vstart['nbike'] - .3],
         bike=[vstart['nbike'] - .3, vstart['nmonth'] - .3], month=[vstart['nmonth'] - .3, vstart['nfifty'] - .3],
         fifty=[vstart['nfifty'] - .3, vstart['ndiff'] - .3], diff=[vstart['ndiff'] - .3, vstart['nrecap'] - .3],
         recap=[vstart['nrecap'] - .4, C['u_now'] - .05], turn=[C['u_now'] - .1, K['T_LINKS'] + .05], outro=[-10, -9])
S = {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}

EMOS = [[e['phrase'], e['emoji']] for e in PLAN['emoji_pops']]
EMO_AFTER = {}
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
# click on taps (the Join JetUP tap) and on the gear shifts; never stacked
kit0 = K['T_LINKS']
body = dict(whoosh=[C['h_open'] + .05, S['hi'][0] - .1, S['share'][0] + .05, S['bike'][0] + .1, S['month'][0] + .05, S['fifty'][0] + .05,
                    S['diff'][0] + .05, S['recap'][0] - .1, C['u_now'] - .1],
            tick=[C['h_ten'], C['s_one'], C['s_paid'], C['p_one'] - .05, C['b_gears'], C['b_team'], C['b_fifty'], C['b_forty'],
                  C['m_only'], C['m_paid'], C['f_strongest'], C['f_half'], C['d_partner'], C['d_three'], C['d_one'],
                  C['rc_gear'] - .1, C['rc_two'] - .1, C['rc_diff'] - .1, C['i_url']],
            pop=[C['h_infinity'], C['p_top'], C['m_resets'], C['f_wheels'], C['d_one2'], C['u_turn']],
            click=[C['b_climb'][0], C['b_climb'][8], C['i_press']])
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
