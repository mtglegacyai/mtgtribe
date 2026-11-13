# 60-second WhatsApp status cut of the OlyLife survey video (MTG, 13 Nov 2026). Built from the v3 voice track
# (voice.wav + words.json, cut at the silences between words) and two new V3 lines for WhatsApp
# (survey_v3wa.wav: "Reply to this status..." and "So reply to this status... TikTok, at join MTG tribe.").
# Ends with "Let's Get This Crypto!" and the closing track's last line right after it (videos of 60 s or less).
# Writes wa/voice.wav, wa/words.json, wa/lines_out.json, stage/timeline_wa.js.
import json, os, re, subprocess, wave, difflib
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)); O = f'{D}/wa'; os.makedirs(O, exist_ok=True); SR = 48000
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
def rd(path):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()
V3 = rd(f'{D}/voice.wav'); W3 = json.load(open(f'{D}/words.json'))
WA = rd(f'{D}/voice/survey_v3wa.wav'); BW = json.load(open(f'{D}/bank/words.json'))

def frames(x):
    hop = int(0.01 * SR); return np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))[::hop]
def quiet(fr, a, b):
    """quietest 10 ms point between a and b (s)"""
    sm = np.convolve(fr, np.ones(5) / 5, 'same'); i0, i1 = int(a * 100), max(int(a * 100) + 1, int(b * 100))
    return (i0 + int(np.argmin(sm[i0:i1]))) / 100
def piece(x, fr, lo, hi, words):
    """cut x between the quiet points lo..hi, trim to speech at -48 dB, keep word times relative to the cut"""
    i0, i1 = int(lo * 100), int(hi * 100); loud = np.where(fr[i0:i1] > 10 ** (-48 / 20))[0]
    a, b = (i0 + loud[0]) / 100, (i0 + loud[-1] + 1) / 100; a0, b0 = max(lo, a - .04), min(hi, b + .10)
    y = x[int(a0 * SR):int(b0 * SR)].copy(); f1, f2 = int(.01 * SR), int(.03 * SR)
    y[:f1] *= np.linspace(0, 1, f1); y[-f2:] *= np.linspace(1, 0, f2)
    return dict(x=y, ws=[(w, max(0, s - a0), max(0, e - a0)) for w, s, e in words])

F3 = frames(V3)
def from_v3(line, first=None, last=None):
    """words of a v3 line from `first` (index) to `last` (index), cut at the silences around them"""
    ws = [w for w in W3 if w['line'] == line]; i0 = first or 0; i1 = len(ws) - 1 if last is None else last
    sel = ws[i0:i1 + 1]
    prev_end = ws[i0 - 1]['b'] if i0 > 0 else sel[0]['a'] - .25
    next_start = ws[i1 + 1]['a'] if i1 + 1 < len(ws) else sel[-1]['b'] + .3
    lo = quiet(F3, prev_end, sel[0]['a']) if i0 > 0 else sel[0]['a'] - .2
    hi = quiet(F3, sel[-1]['b'], next_start) if i1 + 1 < len(ws) else sel[-1]['b'] + .25
    return piece(V3, F3, lo, hi, [(w['w'], w['a'], w['b']) for w in sel])

# WhatsApp take: script words aligned to speech-to-text words
WHW = json.load(open(f'{D}/voice/whisper_words_wa.json'))
P_WA = [('wa1', "Reply to this status with your answers, by number."),
        ('wa2', "So reply to this status with your answers. The full video is on my TikTok, at join MTG tribe.")]
scr = [w for _, p in P_WA for w in p.split()]
sm = difflib.SequenceMatcher(None, [norm(w) for w in scr], [norm(w['w']) for w in WHW], autojunk=False)
tim = [None] * len(scr)
for blk in sm.get_matching_blocks():
    for j in range(blk.size): tim[blk.a + j] = (WHW[blk.b + j]['a'], WHW[blk.b + j]['b'])
for i in range(len(scr)):                                   # unmatched words (join MTG tribe): spread over the gap
    if tim[i] is None:
        p = next((tim[j][1] for j in range(i - 1, -1, -1) if tim[j]), 0.0)
        q = next((tim[j][0] for j in range(i + 1, len(scr)) if tim[j]), WHW[-1]['b'])
        run = [i]
        while run[-1] + 1 < len(scr) and tim[run[-1] + 1] is None: run.append(run[-1] + 1)
        st = (q - p) / len(run)
        for n, j in enumerate(run): tim[j] = (p + n * st, p + (n + 1) * st)
FW = frames(WA); n1 = len(P_WA[0][1].split())
cut = quiet(FW, tim[n1 - 1][1], tim[n1][0])
wa = {'wa1': piece(WA, FW, 0, cut, [(scr[i], *tim[i]) for i in range(n1)]),
      'wa2': piece(WA, FW, cut, len(WA) / SR - .01, [(scr[i], tim[i][0] - 0, tim[i][1]) for i in range(n1, len(scr))])}
def lgtc():
    x = rd(f'{D}/bank/v_o_lgtc.flac'); return dict(x=x, ws=[(w['w'], w['a'], w['b']) for w in BW['o_lgtc']])

hi_ws = [w for w in W3 if w['line'] == 'hi']; we = next(i for i, w in enumerate(hi_ws) if w['w'] == 'We')
sev = [w for w in W3 if w['line'] == 'seven']; qn = next(i for i, w in enumerate(sev) if w['w'].startswith('questions'))
def upto(line, word):
    ws = [w for w in W3 if w['line'] == line]; return next(i for i, w in enumerate(ws) if norm(w['w']) == word)
PLAN = [('hook', from_v3('hook'), .30), ('honest', from_v3('honest'), .28),
        ('hi', from_v3('hi', first=we), .26), ('seven', from_v3('seven', last=qn), .22), ('wa1', wa['wa1'], .34),
        ('q1', from_v3('q1'), .27), ('q2', from_v3('q2'), .27), ('q3', from_v3('q3'), .27), ('q4', from_v3('q4'), .27),
        ('q5', from_v3('q5', last=upto('q5', 'discomfort')), .27), ('q6', from_v3('q6', last=upto('q6', 'machine')), .27),
        ('q7', from_v3('q7', last=upto('q7', 'for')), .27), ('q8', from_v3('q8', last=upto('q8', 'clients')), .34),
        ('health1', from_v3('health1'), .22), ('health2', from_v3('health2', first=upto('health2', 'your'), last=upto('health2', 'first')), .34),
        ('wa2', wa['wa2'], .30), ('o_lgtc', lgtc(), 0)]
LEAD = .12; TRACK_LINE = 51.36 - 48.38; AFTER = .10
t = LEAD; pieces = []; allw = []; outl = []
for key, P, gap in PLAN:
    pieces.append((int(round(t * SR)), P['x'])); outl.append(dict(key=key, a=round(t, 3), b=round(t + len(P['x']) / SR, 3)))
    for w, s, e in P['ws']: allw.append(dict(w=w, a=round(t + s, 3), b=round(t + e, 3), line=key))
    t += len(P['x']) / SR + gap
last_word_end = outl[-1]['b']; track_at = last_word_end + AFTER; T = track_at + TRACK_LINE
# captions: the handle as people read it
for i in range(len(allw) - 2):
    if allw[i]['line'] == 'wa2' and [norm(allw[i + k]['w']) for k in range(3)] == ['join', 'mtg', 'tribe']:
        allw[i:i + 3] = [dict(w='@joinmtgtribe', a=allw[i]['a'], b=allw[i + 2]['b'], line='wa2')]; break
voice = np.zeros(int(round(T * SR)), np.float32)
for s, x in pieces: voice[s:s + len(x)] += x[:len(voice) - s]
with wave.open(f'{O}/voice.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(allw, open(f'{O}/words.json', 'w'), indent=0)
json.dump(dict(T=round(T, 3), track_at=round(track_at, 3), lines=outl), open(f'{O}/lines_out.json', 'w'), indent=1)
tl = dict(T=round(T, 3), fps=30, lines={l['key']: [l['a'], l['b']] for l in outl}, words=[[w['w'], w['a'], w['b'], w['line']] for w in allw])
open(f'{D}/stage/timeline_wa.js', 'w').write('window.TL=' + json.dumps(tl) + ';\n')
for l in outl: print(f"{l['key']:8s} {l['a']:6.2f} {l['b']:6.2f}  {' '.join(w['w'] for w in allw if w['line'] == l['key'])[:90]}")
print('T =', round(T, 2), 's; track line from', round(track_at, 2))
