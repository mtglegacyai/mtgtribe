# Invitation promo v2: tidy the pauses of MTG's new voice line, remap the word times, write voice.wav and stage/timing.js.
import json, os, re, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
LEAD, HOLD = 0.2, 2.4          # silence before the first word, end card hold after the last word

words = json.load(open(os.path.join(HERE, 'invite_words.json')))
w = wave.open(os.path.join(HERE, 'invite_raw.wav')); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

# pause caps: after a sentence 0.45 s, after a section (question, the times, the reasons, the three points, the risk line) 0.55 s
SECTION = {'cent?', 'India!', 'live!', 'you.', 'yourself.', 'early!', 'tonight!', 'things!', 'there!'}
cuts = []            # (source start, source end) of silence removed
for a, b in zip(words, words[1:]):
    gap = b['a'] - a['b']
    if not re.search(r'[.?!]$', a['w']): continue
    cap = .42 if a['w'] in SECTION else .32
    if gap > cap:
        mid = (a['b'] + b['a']) / 2; cut = gap - cap
        cuts.append((mid - cut / 2, mid + cut / 2))


def src2out(t):
    o = t + LEAD
    for c0, c1 in cuts:
        if t >= c1: o -= c1 - c0
        elif t > c0: o -= t - c0
    return o


# build the voice: keep everything except the cut stretches, 15 ms crossfades at each join
keep, pos = [], 0.0
for c0, c1 in cuts: keep.append((pos, c0)); pos = c1
keep.append((pos, len(x) / SR))
parts = []
f = int(.015 * SR)
for a, b in keep:
    seg = x[int(a * SR):int(b * SR)].copy()
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    parts.append(seg)
voice = np.concatenate([np.zeros(int(LEAD * SR), np.float32)] + parts)
last = src2out(words[-1]['b'])
T = round(last + HOLD, 2)
voice = np.pad(voice, (0, max(0, int(T * SR) - len(voice))))[:int(T * SR)]
with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())

W = [{'w': w['w'], 'a': round(src2out(w['a']), 3), 'b': round(src2out(w['b']), 3), 'i': i} for i, w in enumerate(words)]


def at(word, n=0, exact=False):
    # exact case when the word starts with a capital (Three:, Trading, See) or exact=True, any case otherwise
    if word[0].isupper() or exact: hits = [w for w in W if w['w'].strip('.,!?:') == word]
    else: hits = [w for w in W if w['w'].lower().strip('.,!?:') == word]
    return hits[n]['a']


C = {
    'want': at('Want'), 'gold0': at('gold'), 'works0': at('works'), 'before0': at('before'), 'cent': at('cent'),
    'hi': at('Hi'), 'mtg': at('MTG', 0), 'arch': at('Architect'), 'inviting': at('inviting'), 'live0': at('live'), 'jetup0': at('Jet'),
    'zoom': at('Zoom'), 'tonight': at('tonight'),
    'eight': at('Eight'), 'sa': at('South'), 'seven': at('Seven'), 'ng': at('Nigeria'), 'eleven': at('Eleven'), 'india': at('India'),
    'curious': at('Curious'), 'burned': at('burned'), 'come': at('come'), 'facts': at('facts'), 'ask': at('ask'), 'questions': at('questions'),
    'learn3': at("You'll"), 'three': at('three'), 'one': at('One'), 'two': at('Two'), 'hundred': at('hundred'), 'rules': at('rules'),
    'threeP': at('Three'), 'started': at('started'), 'right': at('right'),
    'trading': at('Trading', 0), 'risk': at('risk'), 'learnF': at('learn', 1), 'decide': at('decide'),
    'join': at('Join'), 'mtgU': at('MTG', 1), 'tribe': at('tribe'), 'dot': at('dot'), 'com': at('com'), 'slash': at('slash'), 'jet': at('jet', 0, True),
    'zoomU': at('zoom', 1), 'logIn': at('log'), 'ten': at('ten'), 'send': at('Send'), 'someone': at('someone'), 'there': at('there'),
    'see': at('See'), 'lgtc': at("Let's"), 'crypto': at('Crypto'),
}
SPEECH = [[round(src2out(a['a']), 3), round(src2out(b['b']), 3)] for a, b in [(words[0], words[-1])]]
# speech stretches (for ducking): split at every pause longer than 0.35 s in the output
st, spans = W[0]['a'], []
for a, b in zip(W, W[1:]):
    if b['a'] - a['b'] > .35: spans.append([st, a['b']]); st = b['a']
spans.append([st, W[-1]['b']])
TL = {'T': T, 'fps': 30, 'words': W, 'cues': C, 'spans': spans}
os.makedirs(os.path.join(HERE, 'stage'), exist_ok=True)
open(os.path.join(HERE, 'stage', 'timing.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
print('removed', round(sum(b - a for a, b in cuts), 2), 's of pauses in', len(cuts), 'places; T =', T, 's')
print({k: round(v, 2) for k, v in C.items()})
