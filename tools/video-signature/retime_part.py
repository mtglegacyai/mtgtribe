# Consistency upgrade for a JetUP tutorial part (MTG, 8 Nov 2026): keep everything up to "Share it with someone who's
# ready to start", then insert MTG's banked "We learn best when we teach others." and "It pays to pay attention, and take
# action." (from the sign-up training's own voice take), push the outro later, and hand the ending over to the training's
# signature ending (mtg_ending.py). Writes stage/timeline.js, voice.wav, kitcues.json and mixcues.json in the part folder
# (the previous versions are kept in pre_consist/).
# Usage: python3 retime_part.py <part dir> "<end card next chip>" "<emoji json>"
import json, os, re, shutil, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mtg_ending as ME
D, NXT = sys.argv[1], sys.argv[2]
EMOS = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
SR = 48000
NEW = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lines', 'lines_new.json')))
LINES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lines')
bk = os.path.join(D, 'pre_consist'); os.makedirs(bk, exist_ok=True)
for f in ('stage/timeline.js', 'voice.wav', 'mixcues.json'):
    if not os.path.exists(os.path.join(bk, os.path.basename(f))): shutil.copy(os.path.join(D, f), os.path.join(bk, os.path.basename(f)))
src = open(os.path.join(bk, 'timeline.js')).read()
TL = json.loads(src[src.index('=') + 1:].strip().rstrip(';'))
MC = json.load(open(os.path.join(bk, 'mixcues.json')))
with wave.open(os.path.join(bk, 'voice.wav')) as w: V = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
norm = lambda s: re.sub(r'[^a-z0-9 ]', '', s.lower())
spans = TL['spans']; words = TL['words']
def text_of(sp): return ' '.join(w['w'] for w in words if w['a'] >= sp[0] - .01 and w['b'] <= sp[1] + .05)
idx = {k: next(i for i, sp in enumerate(spans) if norm(text_of(sp)).startswith(k)) for k in
       ('everything i showed you', 'share it with someone', 'quick reminder')}
i_share, i_quick = idx['share it with someone'], idx['quick reminder']
assert i_quick == i_share + 1, 'unexpected line order'
# new placement: lines up to "share" keep their times; we-learn, slogan, then the outro lines with their original gaps
g_we, g_slog, g_quick = 0.40, 0.50, 0.60
t_we = round(spans[i_share][1] + g_we, 3); t_slog = round(t_we + NEW['we']['dur'] + g_slog, 3)
shift = round(t_slog + NEW['slog']['dur'] + g_quick - spans[i_quick][0], 3)
cut = spans[i_share][1] + 0.05                      # everything after this moves by `shift`
new_spans = [list(s) for s in spans[:i_quick]] + [[t_we, round(t_we + NEW['we']['dur'], 3)], [t_slog, round(t_slog + NEW['slog']['dur'], 3)]] \
            + [[round(a + shift, 3), round(b + shift, 3)] for a, b in spans[i_quick:]]
new_words = [w for w in words if w['a'] < cut]
for key, t0 in (('we', t_we), ('slog', t_slog)):
    new_words += [dict(w=w['w'], a=round(t0 + w['a'], 3), b=round(t0 + w['b'], 3)) for w in NEW[key]['words']]
new_words += [dict(w=w['w'], a=round(w['a'] + shift, 3), b=round(w['b'] + shift, 3)) for w in words if w['a'] >= cut]
lgtc_end = new_spans[-1][1]
T = round(lgtc_end + 0.12 + 3.25, 2)               # end card holds about 3.4 s after his last word (as explainer #1)
# voice: original up to the cut, then the outro lines moved, plus the two banked lines
N = int(round(T * SR)); v = np.zeros(N, np.float32); c0 = int(cut * SR); v[:c0] = V[:c0]
for a, b in spans[i_quick:]:
    seg = V[int(round(a * SR)):int(round(b * SR))]; s = int(round((a + shift) * SR)); v[s:s + len(seg)] += seg[:max(0, N - s)]
for key, t0 in (('we', t_we), ('slog', t_slog)):
    with wave.open(os.path.join(LINES_DIR, NEW[key]['file'])) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    s = int(round(t0 * SR)); v[s:s + len(x)] += x[:N - s]
with wave.open(os.path.join(D, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
# cues for the signature ending
K = ME.find_cues(new_words, links=True)
# the stage keeps its background, top bar and captions; its own "next" extras and outro step aside for the ending
TL['T'] = T; TL['words'] = new_words; TL['spans'] = new_spans
TL['scenes']['next'][1] = round(K['T_LINKS'] + 0.3, 3); TL['scenes']['outro'] = [-10, -9]
for k in ('links_url', 'every', 'save', 'share'): TL['cues'][k] = 1e9
for k in ('o_thanks', 'o_massive', 'o_best', 'o_im', 'o_lgtc'): TL['cues'][k] = -5     # the old outro messages never show
TL['nocap'] = TL.get('nocap', []) + [[K['END_CARD'], T + 1]]
def S_body(phrase):
    toks = [(re.sub(r'[^a-z0-9]', '', w['w'].lower()), w['a']) for w in new_words]; ph = phrase.split()
    for i in range(len(toks) - len(ph) + 1):
        if all(toks[i + k][0] == ph[k] for k in range(len(ph))): return round(toks[i][1], 3)
    raise KeyError('emoji phrase not found: ' + phrase)
TL['emos'] = [[S_body(ph), e] for ph, e in EMOS]; TL['kit'] = [K['T_LINKS'], T]
open(os.path.join(D, 'stage', 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL) + ';\n')
json.dump(dict(cues=K, orient='v', nxt=NXT, links=True, T=T, fps=TL['fps']), open(os.path.join(D, 'kitcues.json'), 'w'), indent=1)
MC.update(T=T, spans=new_spans, kit=K)
json.dump(MC, open(os.path.join(D, 'mixcues.json'), 'w'))
print(D, 'T', TL['T'] if False else T, '(was', MC.get('T_old', spans[-1][1]), ') shift', shift, 'we', t_we, 'slog', t_slog, 'kit from', K['T_LINKS'], 'end card', K['END_CARD'])
