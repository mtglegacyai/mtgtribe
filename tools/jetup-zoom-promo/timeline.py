# JetUP Zoom promo (7 Nov 2026): build the voice track from MTG's approved voice bank (no new HeyGen lines)
# and write the timing map the frame engine uses (stage/timing.js).
import json, os, subprocess, numpy as np, wave

HERE = os.path.dirname(os.path.abspath(__file__))
VB = os.path.join(HERE, 'vb')
SR = 48000

# (file, source start, source end, output start, label)   all lines are MTG Master Voice V2 takes from the voice bank
CLIPS = [
    ('signup-training/t1.mp3', 17.46, 20.98, 2.90, 'hi'),        # Hi, my name is MTG, Your Digital Architect.
    ('5-checks/o1.mp3',        51.25, 65.60, 6.75, 'how'),       # TAG Markets is the broker ... That's gold, priced in US dollars.
    ('5-checks/o2.mp3',        39.25, 41.30, 21.55, 'promo'),    # The promo adds one hundred.
    ('5-checks/o2.mp3',        67.00, 74.30, 23.85, 'rules'),    # But the promo has rules. The bonus is released after twelve months ...
    ('5-checks/o2.mp3',       122.10, 124.58, 36.30, 'pays'),    # It pays to pay attention, and take action.
    ('5-checks/o2.mp3',       148.52, 152.68, 39.20, 'remind'),  # Quick reminder: none of this is financial advice. Always do your own research.
    ('5-checks/o2.mp3',       165.79, 168.45, 43.75, 'me'),      # I'm MTG, Your Digital Architect.
    ('5-checks/o2.mp3',       169.62, 170.95, 46.55, 'lgtc'),    # Let's Get This Crypto!
]
EVENT = (31.40, 36.05)    # music-only scene: live on Zoom tonight, date and the three times
T = 50.5                   # total length; the closing track ends exactly here


def words_for(f):
    if f.endswith('o1.mp3') or f.endswith('o2.mp3'):
        return json.load(open(os.path.join(VB, f.replace('.mp3', '_words.json'))))['words']
    ws = json.load(open(os.path.join(VB, f.replace('.mp3', '_tts.json'))))['word_timestamps']
    return [w for w in ws if not w['word'].startswith('<')]


def load(f, a, b):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', os.path.join(VB, f),
                          '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    n = int(.015 * SR); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    return x


voice = np.zeros(int(T * SR), np.float32)
words, clips = [], []
def snap(f, a0, b0):
    # trim to the first and last word inside [a0, b0] (forced-alignment times), with breathing room that never
    # reaches into the neighbouring words
    ws = words_for(f); inside = [w for w in ws if w['start'] >= a0 - .05 and w['start'] < b0 - .05]
    first, last = inside[0], inside[-1]
    prev = max([w['end'] for w in ws if w['end'] <= first['start'] + 1e-3] or [0])
    nxt = min([w['start'] for w in ws if w['start'] >= last['end'] - 1e-3] or [1e9])
    return max(first['start'] - .07, prev + .03), min(last['end'] + .14, nxt - .03)


for i, (f, a, b, o, lab) in enumerate(CLIPS):
    a, b = snap(f, a, b)
    x = load(f, a, b)
    s = int(o * SR); voice[s:s + len(x)] += x[:len(voice) - s]
    d = len(x) / SR
    if i + 1 < len(CLIPS): assert o + d < CLIPS[i + 1][3] - .05, ('overlap', lab)
    clips.append({'lab': lab, 'o': round(o, 3), 'e': round(o + d, 3), 'src': [f, round(a, 3), round(b, 3)]})
    for w in words_for(f):
        if w['start'] >= a - .01 and w['start'] < b - .05:
            words.append({'w': w['word'], 'a': round(o + w['start'] - a, 3), 'b': round(o + w['end'] - a, 3), 'c': lab})
assert clips[-1]['e'] < T - 2

with wave.open(os.path.join(HERE, 'voice.wav'), 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())


def cue(lab, text, nth=0):
    hits = [w for w in words if w['c'] == lab and w['w'].lower().strip('.,!?:') == text.lower()]
    return hits[nth]['a']


CUES = {
    'hi': cue('hi', 'Hi'), 'mtg1': cue('hi', 'MTG'), 'arch1': cue('hi', 'Architect'),
    'broker': cue('how', 'broker'), 'tag': cue('how', 'TAG'), 'account': cue('how', 'account'), 'name': cue('how', 'name'),
    'connect': cue('how', 'connect'), 'copyx': cue('how', 'CopyX'), 'sonic': cue('how', 'Sonic'), 'gold1': cue('how', 'gold'),
    'xau': cue('how', 'X'), 'usd': cue('how', 'U', 1), 'gold2': cue('how', 'gold', 1), 'dollars': cue('how', 'dollars'),
    'promo': cue('promo', 'promo'), 'hundred': cue('promo', 'hundred'), 'rules': cue('rules', 'rules'),
    'twelve': cue('rules', 'twelve'), 'taking': cue('rules', 'taking'), 'ends': cue('rules', 'ends'),
    'pays': cue('pays', 'pays'), 'action': cue('pays', 'action'),
    'quick': cue('remind', 'Quick'), 'advice': cue('remind', 'advice'), 'research': cue('remind', 'research'),
    'me': cue('me', "I'm"), 'lgtc': cue('lgtc', "Let's"), 'crypto': cue('lgtc', 'Crypto'),
}
TL = {'T': T, 'fps': 30, 'event': EVENT, 'clips': clips, 'words': words, 'cues': CUES}
open(os.path.join(HERE, 'stage', 'timing.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
print('clips:', [(c['lab'], c['o'], c['e']) for c in clips])
print('cues:', CUES)
print(' '.join(w['w'] for w in words))
