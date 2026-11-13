# Builds the voice track of the OlyLife survey video from MTG Master Voice V3 (one take, 20 lines) and the banked
# signature-ending lines, with tidy pauses. Writes voice.wav (48 kHz mono), words.json (every word, absolute time,
# with its line key) and lines_out.json (each line's start and end).
import json, os, re, subprocess, wave
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
TTS = json.load(open(f'{D}/voice/survey_tts.json'))
HW = [dict(word=w['text'], start=w['start_time'], end=w['end_time']) for w in TTS['original_words']]          # HeyGen word list (text exactly as sent)
WH = json.load(open(f'{D}/voice/whisper_words.json'))

# The 20 paragraphs, in the order they were sent, keyed. Their word counts split HeyGen's word list.
PARAS = [
 ('hook', "Have you used this foot machine? The Olly Life Terra P ninety?"),
 ('honest', "I need your honest answer."),
 ('keep', "I keep seeing amazing videos about it. Now I want the real stories, straight from the people who use it."),
 ('hi', "Hi, I'm MTG, Your Digital Architect. I'm thinking of bringing this machine to my community. So before I do, I'm asking you."),
 ('seven', "Seven quick questions. Answer by number in the comments."),
 ('q1', "One. Why did you try it? What were you hoping it would help with?"),
 ('q2', "Two. How many sessions have you had, and how often?"),
 ('q3', "Three. What did you feel during your very first session?"),
 ('q4', "Four. What changed after a few weeks? And what didn't change?"),
 ('q5', "Five. Anything you didn't like, or any discomfort? Be honest. It helps the next person."),
 ('q6', "Six. Was it worth it? Would you pay for another session, or buy the machine?"),
 ('sell', "And if you sell it, or run sessions, this one is for you."),
 ('q7', "Seven. What do your clients come back for? And what's the one question they always ask?"),
 ('good', "Good, bad, or nothing at all, every honest answer counts."),
 ('comment', "Comment your answers, or stitch this video and tell your story on camera."),
 ('follow', "I'll read every comment, and share what you told me in my next video. So follow, and don't miss it."),
 ('tribe', "Want more honest guides like this? Join the free MTG tribe, at MTG tribe dot com slash group."),
 ('save', "Save this video, so you can come back and read the answers."),
 ('share', "And share it with someone who uses this machine. Their answer could help someone decide."),
 ('remind', "Quick reminder: this is not medical advice. Always check with your doctor first."),
]
words = [w['word'] if 'word' in w else w.get('text') for w in HW]
words = [w for w in words if w and w.strip()]
HWs = [w for w in HW if (w.get('word') or w.get('text') or '').strip()]
n_need = sum(len(p.split()) for _, p in PARAS)
assert len(HWs) == n_need, (len(HWs), n_need)

def rd(path):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()
take = rd(f'{D}/voice/survey_v3.wav')
# frame energy for finding the real silences
hop = int(0.01 * SR); fr = np.sqrt(np.convolve(take ** 2, np.ones(hop) / hop, 'same'))[::hop]
thr = 10 ** (-42 / 20)
def speech_edges(a, b):
    """first and last 10 ms frame above the threshold between a and b (s)"""
    i0, i1 = int(a * 100), min(len(fr) - 1, int(b * 100))
    loud = np.where(fr[i0:i1] > thr)[0]
    return (i0 + loud[0]) / 100, (i0 + loud[-1] + 1) / 100

# whisper words in time order, for the per-line offset of HeyGen's times
wt = np.array([w['a'] for w in WH])
lines = []; k = 0
for key, txt in PARAS:
    n = len(txt.split()); ws = HWs[k:k + n]; k += n
    ha, hb = ws[0]['start'], ws[-1]['end']
    # whisper words inside this line (by time, with margin), median offset of starts
    lines.append(dict(key=key, text=txt, hw=ws, ha=ha, hb=hb))
# 1) offset of HeyGen's word times against the audio, per line (whisper words near the line's span)
for i, L in enumerate(lines):
    a, b = L['ha'] - 0.1, L['hb'] + 0.5
    sel = [w for w in WH if a - 0.1 <= w['a'] <= b]
    offs = []
    hn = [re.sub(r'[^a-z0-9]', '', w['word'].lower() if 'word' in w else w['text'].lower()) for w in L['hw']]
    for w in sel:
        t = re.sub(r'[^a-z0-9]', '', w['w'].lower())
        for j, h in enumerate(hn):
            if h and h == t and abs(L['hw'][j]['start'] - w['a']) < 0.6:
                offs.append(w['a'] - L['hw'][j]['start']); break
    L['off'] = float(np.median(offs)) if offs else 0.0
    L['n_match'] = len(offs)
# 2) cut between two lines at the quietest 10 ms frame between them (times corrected by the offset),
#    then trim each line to its speech edges at -48 dB
cuts = [0.0]
for i in range(len(lines) - 1):
    e = lines[i]['hb'] + lines[i]['off']; s = lines[i + 1]['ha'] + lines[i + 1]['off']
    i0, i1 = int(min(e, s) * 100) - 2, int(max(e, s) * 100) + 8
    sm = np.convolve(fr, np.ones(5) / 5, 'same')
    cuts.append((i0 + int(np.argmin(sm[i0:i1]))) / 100)
cuts.append(len(take) / SR)
thr = 10 ** (-48 / 20)
for i, L in enumerate(lines):
    L['a'], L['b'] = speech_edges(cuts[i], cuts[i + 1])
    L['cut'] = (cuts[i], cuts[i + 1])

# banked V2 ending lines (signature standard), with their word times relative to the file
BW = json.load(open(f'{D}/bank/words.json'))
def bank(key):
    x = rd(f'{D}/bank/v_{key}.flac'); return x, BW[key]

# ---- timeline: gaps after each line (s). Questions get a little air so the card can be read.
GAP = dict(hook=0.32, honest=0.42, keep=0.42, hi=0.30, seven=0.50, q1=0.55, q2=0.55, q3=0.55, q4=0.55, q5=0.55, q6=0.50,
           sell=0.32, q7=0.55, good=0.32, comment=0.40, follow=0.45, tribe=0.50, save=0.30, share=0.45)
order = [L['key'] for L in lines if L['key'] != 'remind']
order_end = ['n_we', 'n_slog', 'remind', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP_END = dict(n_we=0.40, n_slog=0.50, remind=0.50, o_thanks=0.25, o_support=0.45, o_massive=0.45, o_best=0.50, o_im=0.20, o_see=0.30, o_lgtc=0.0)
LEAD = 0.20                      # silence before the first word (the cover reads first)
TAIL = 3.6                       # end card after "Let's Get This Crypto!"
byk = {L['key']: L for L in lines}
pieces = []; allw = []; outl = []; t = LEAD
def place(x, ws, key, gap):
    global t
    pieces.append((int(round(t * SR)), x)); outl.append(dict(key=key, a=round(t, 3), b=round(t + len(x) / SR, 3)))
    for w in ws: allw.append(dict(w=w[0], a=round(t + w[1], 3), b=round(t + w[2], 3), line=key))
    t += len(x) / SR + gap
PAD0, PAD1 = 0.04, 0.10
for key in order + order_end:
    if key in byk:
        L = byk[key]; a0 = max(L['cut'][0], L['a'] - PAD0); b0 = min(L['cut'][1], L['b'] + PAD1)
        x = take[int(a0 * SR):int(b0 * SR)].copy()
        x[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR)); x[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
        ws = []
        for w in L['hw']:
            txt = w.get('word') or w.get('text')
            ws.append((txt, max(0, w['start'] + L['off'] - a0), max(0, w['end'] + L['off'] - a0)))
        place(x, ws, key, GAP.get(key, GAP_END.get(key, 0.4)))
    else:
        x, bw = bank(key)
        place(x, [(w['w'], w['a'], w['b']) for w in bw], key, GAP_END[key])
T = t + TAIL
voice = np.zeros(int(round(T * SR)), np.float32)
for s, x in pieces: voice[s:s + len(x)] += x[:len(voice) - s]
with wave.open(f'{D}/voice.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(allw, open(f'{D}/words.json', 'w'), indent=0)
json.dump(dict(T=round(T, 3), lines=outl), open(f'{D}/lines_out.json', 'w'), indent=1)
for L in lines: print(f"{L['key']:8s} cut {L['a']:6.2f}-{L['b']:6.2f}  heygen {L['ha']:6.2f}-{L['hb']:6.2f}  off {L['off']:+.3f} ({L['n_match']})")
print('T =', round(T, 2), 's,', len(allw), 'words')
