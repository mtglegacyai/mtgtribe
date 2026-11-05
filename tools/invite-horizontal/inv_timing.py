"""Edit decision list for the horizontal MTG TRIBE invite.
Source = the approved vertical invite (voice + closing track). Only silences are cut, everything from 88.85s on is untouched,
so the closing track still starts 50 s before the end."""
import json, wave, numpy as np
D = '/tmp/claude-0/-home-user/da468685-967b-5760-877c-9c4fad4db3c6/scratchpad/inv/'
CO = 13.4                      # cinematic cold open (text + sound design, no voice)
CUTS = [(0.0, 3.45), (6.10, 20.25), (21.50, 36.0), (36.30, 88.40), (88.85, 160.4)]

wf = wave.open(D + 'audio48k.wav'); sr = wf.getframerate()
a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768
mono = np.abs(a.mean(1))
def quiet(t, span=.07):        # move a cut point to the quietest 10 ms nearby
    best, bt = 9, t
    for c in np.arange(t - span, t + span, .005):
        if c <= 0 or c >= 160.39: continue
        e = mono[int(c * sr):int((c + .01) * sr)].mean()
        if e < best: best, bt = e, c
    return round(float(bt), 3)
segs = []
for i, (s0, s1) in enumerate(CUTS):
    s0 = s0 if i == 0 else quiet(s0)
    s1 = s1 if i == len(CUTS) - 1 else quiet(s1)
    segs.append([s0, s1])
off = CO; SEG = []
for s0, s1 in segs:
    SEG.append({'a': s0, 'b': s1, 'o': round(off, 3)}); off += s1 - s0
TOTAL = round(off, 3)
def mapS(s):
    for g in SEG:
        if s < g['a']: return g['o']
        if s <= g['b']: return g['o'] + s - g['a']
    return TOTAL

T = json.load(open(D + 'transcript.json'))
W = [w for s in T for w in s['words']]
fix = {'MTG,': 'MTG,', 'Tribe.': 'TRIBE.', 'Tribe?': 'TRIBE?', 'Tribe': 'TRIBE', 'Altruva': 'ALTRUVA'}
words = []
i = 0
while i < len(W):
    w = W[i]; t = w['w'].strip()
    if t.startswith('MTGtribe'):           # "MTGtribe .com slash group" -> one token
        j = i
        while not W[j]['w'].strip().startswith('group'): j += 1
        words.append({'w': 'mtgtribe.com/group', 's': w['s'], 'e': W[j]['e']}); i = j + 1; continue
    if t.startswith('joinMTGtribe'): t = '@joinmtgtribe.'
    if t == 'so' and W[i + 1]['w'].strip() == '-called':
        words.append({'w': 'so-called', 's': w['s'], 'e': W[i + 1]['e']}); i += 2; continue
    t = fix.get(t, t)
    words.append({'w': t, 's': w['s'], 'e': w['e']}); i += 1
# keep words inside the kept segments, map to output time
out = []
for w in words:
    mid = (w['s'] + w['e']) / 2
    if any(g['a'] <= mid <= g['b'] for g in SEG):
        out.append({'w': w['w'], 's': round(mapS(w['s']), 3), 'e': round(mapS(w['e']), 3), 'src': w['s']})
out[-1]['w'] = 'Crypto! 💪'; out[-2]['w'] = 'This'; out[-3]['w'] = 'Get'
# caption chunks: whole phrases (split on punctuation), packed up to 40 characters, long phrases split evenly
for k, w in enumerate(out):
    if w['w'] == 'what': w['w'] = 'What'
    if w['w'] == 'at' and k + 1 < len(out) and out[k + 1]['w'].startswith('@'): w['w'] = 'at'
phrases, cur = [], []
for k, w in enumerate(out):
    cur.append(w)
    nxt = out[k + 1] if k + 1 < len(out) else None
    if w['w'][-1] in '.,?!' or not nxt or nxt['s'] - w['e'] > .45: phrases.append(cur); cur = []
L = lambda ws: len(' '.join(x['w'] for x in ws))
pieces = []
for ph in phrases:
    if L(ph) <= 40: pieces.append(ph); continue
    STOP = {'the', 'a', 'to', 'of', 'is', 'for', 'and', 'at', 'on', 'but', 'pay', 'who', 'in', 'my', 'your', 'we', 'you'}
    best = min(range(1, len(ph)), key=lambda j: max(L(ph[:j]), L(ph[j:])) + (14 if ph[j - 1]['w'].lower() in STOP else 0))
    for part in (ph[:best], ph[best:]):
        if L(part) <= 44: pieces.append(part)
        else:
            m = len(part) // 2; pieces += [part[:m], part[m:]]
chunks, cur = [], []
for ph in pieces:
    end_prev = cur and cur[-1]['w'][-1] in '.?!'
    if cur and (end_prev or L(cur + ph) > 40 or ph[0]['s'] - cur[-1]['e'] > .6):
        chunks.append(cur); cur = []
    cur = cur + ph
if cur: chunks.append(cur)
# no orphan chunk of one or two short words: join it to its neighbour inside the same sentence
fixed = []
for c in chunks:
    if fixed and len(c) <= 2 and L(fixed[-1] + c) <= 46 and fixed[-1][-1]['w'][-1] not in '.?!': fixed[-1] = fixed[-1] + c
    else: fixed.append(c)
chunks = [{'s': c[0]['s'], 'e': c[-1]['e'], 'w': [dict(x) for x in c]} for c in fixed]
open(D + 'video/timing.js', 'w').write('window.TIMING=' + json.dumps({'CO': CO, 'SEG': SEG, 'TOTAL': TOTAL, 'CHUNKS': chunks}) + ';\n')
json.dump({'CO': CO, 'SEG': SEG, 'TOTAL': TOTAL}, open(D + 'edl.json', 'w'), indent=1)
print('segments', SEG); print('total', TOTAL, 'closing track starts', round(TOTAL - mapS(110.4), 2), 's before end')
for c in chunks: print(f"{c['s']:7.2f} {' '.join(x['w'] for x in c['w'])}")
