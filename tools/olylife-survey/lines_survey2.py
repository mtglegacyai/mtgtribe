# v2 voice track of the OlyLife survey video (MTG, 13 Nov 2026: "Health is Wealth", tribe and multiple income streams,
# eight questions). Take A (survey_v3.wav, 20 lines, HeyGen word times) keeps every unchanged line; take B
# (survey_v3b.wav, 7 new lines, word times from speech-to-text aligned to the script) replaces or adds the rest; the
# banked signature-ending lines follow. Writes voice.wav, words.json, lines_out.json and stage/timeline.js.
import json, os, re, subprocess, wave, difflib
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
def rd(path):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()

PARAS_A = [
 ('hook', "Have you used this foot machine? The Olly Life Terra P ninety?"), ('honest', "I need your honest answer."),
 ('keep', "I keep seeing amazing videos about it. Now I want the real stories, straight from the people who use it."),
 ('hi_old', "Hi, I'm MTG, Your Digital Architect. I'm thinking of bringing this machine to my community. So before I do, I'm asking you."),
 ('seven_old', "Seven quick questions. Answer by number in the comments."),
 ('q1', "One. Why did you try it? What were you hoping it would help with?"), ('q2', "Two. How many sessions have you had, and how often?"),
 ('q3', "Three. What did you feel during your very first session?"), ('q4', "Four. What changed after a few weeks? And what didn't change?"),
 ('q5', "Five. Anything you didn't like, or any discomfort? Be honest. It helps the next person."),
 ('q6_old', "Six. Was it worth it? Would you pay for another session, or buy the machine?"),
 ('sell_old', "And if you sell it, or run sessions, this one is for you."),
 ('q7', "Seven. What do your clients come back for? And what's the one question they always ask?"),
 ('good', "Good, bad, or nothing at all, every honest answer counts."),
 ('comment', "Comment your answers, or stitch this video and tell your story on camera."),
 ('follow', "I'll read every comment, and share what you told me in my next video. So follow, and don't miss it."),
 ('tribe', "Want more honest guides like this? Join the free MTG tribe, at MTG tribe dot com slash group."),
 ('save', "Save this video, so you can come back and read the answers."),
 ('share', "And share it with someone who uses this machine. Their answer could help someone decide."),
 ('remind', "Quick reminder: this is not medical advice. Always check with your doctor first.")]
PARAS_B = [
 ('hi', "Hi, I'm MTG, Your Digital Architect. We build multiple streams of income in my tribe, and I'm considering this machine as our next one. But before I bring it to my tribe, I'm asking you."),
 ('seven', "Eight quick questions. Answer by number in the comments."),
 ('q6', "Six. Was it worth the money? Did you pay per session, or buy your own machine? Would you do it again?"),
 ('sell', "And if you sell it, or run sessions, the last two are for you."),
 ('q8', "Eight. How did you find your first clients? And where do you run your sessions?"),
 ('health1', "Why does all of this matter? Because health is wealth."),
 ('health2', "What good is money, if you're too sick to enjoy it? Your health comes first. So look after your body.")]

def cut_take(take, paras, words):
    """words: per script word (text, start, end) in take time, in order. Returns {key: dict(a, b, ws)}"""
    hop = int(0.01 * SR); fr = np.sqrt(np.convolve(take ** 2, np.ones(hop) / hop, 'same'))[::hop]
    sm = np.convolve(fr, np.ones(5) / 5, 'same'); thr = 10 ** (-48 / 20)
    lines = []; k = 0
    for key, txt in paras:
        n = len(txt.split()); ws = words[k:k + n]; k += n
        lines.append(dict(key=key, ws=ws, ha=ws[0][1], hb=ws[-1][2]))
    cuts = [0.0]
    for i in range(len(lines) - 1):
        e, s = lines[i]['hb'], lines[i + 1]['ha']; i0, i1 = int(min(e, s) * 100) - 2, int(max(e, s) * 100) + 8
        cuts.append((i0 + int(np.argmin(sm[i0:i1]))) / 100)
    cuts.append(len(take) / SR)
    out = {}
    for i, L in enumerate(lines):
        i0, i1 = int(cuts[i] * 100), min(len(fr) - 1, int(cuts[i + 1] * 100)); loud = np.where(fr[i0:i1] > thr)[0]
        a, b = (i0 + loud[0]) / 100, (i0 + loud[-1] + 1) / 100
        a0, b0 = max(cuts[i], a - 0.04), min(cuts[i + 1], b + 0.10)
        x = take[int(a0 * SR):int(b0 * SR)].copy(); f1, f2 = int(.01 * SR), int(.03 * SR)
        x[:f1] *= np.linspace(0, 1, f1); x[-f2:] *= np.linspace(1, 0, f2)
        out[L['key']] = dict(x=x, ws=[(w, max(0, s - a0), max(0, e - a0)) for w, s, e in L['ws']], cut=(a, b))
    return out

# ---- take A: HeyGen word times corrected per line by speech-to-text (as v1)
TA = json.load(open(f'{D}/voice/survey_tts.json')); WHA = json.load(open(f'{D}/voice/whisper_words.json'))
HA = [(w['text'], w['start_time'], w['end_time']) for w in TA['original_words'] if w['text'].strip()]
assert len(HA) == sum(len(p.split()) for _, p in PARAS_A)
wordsA = []; k = 0
for key, txt in PARAS_A:
    n = len(txt.split()); ws = HA[k:k + n]; k += n
    offs = []
    for w in WHA:
        if ws[0][1] - .2 <= w['a'] <= ws[-1][2] + .5:
            for t, s, e in ws:
                if norm(t) and norm(t) == norm(w['w']) and abs(s - w['a']) < .6: offs.append(w['a'] - s); break
    off = float(np.median(offs)) if offs else 0.0
    wordsA += [(t, s + off, e + off) for t, s, e in ws]
A = cut_take(rd(f'{D}/voice/survey_v3.wav'), PARAS_A, wordsA)

# ---- take B: script words aligned to speech-to-text words
WHB = json.load(open(f'{D}/voice/whisper_words_b.json'))
scr = [w for _, p in PARAS_B for w in p.split()]
sm_ = difflib.SequenceMatcher(None, [norm(w) for w in scr], [norm(w['w']) for w in WHB], autojunk=False)
tim = [None] * len(scr)
for blk in sm_.get_matching_blocks():
    for j in range(blk.size): tim[blk.a + j] = (WHB[blk.b + j]['a'], WHB[blk.b + j]['b'])
# fill the few unmatched words (numbers, "MTG") by interpolation between neighbours
for i in range(len(scr)):
    if tim[i] is None:
        p = next((tim[j][1] for j in range(i - 1, -1, -1) if tim[j]), 0.0); q = next((tim[j][0] for j in range(i + 1, len(scr)) if tim[j]), p + .3)
        run = [j for j in range(i, len(scr)) if tim[j] is None]; run = run[:next((n for n, j in enumerate(run) if j != i + n), len(run))]
        step = (q - p) / len(run)
        for n, j in enumerate(run): tim[j] = (p + n * step, p + (n + 1) * step)
print('take B unmatched script words:', [scr[i] for i in range(len(scr)) if not any(blk.a <= i < blk.a + blk.size for blk in sm_.get_matching_blocks())])
wordsB = [(scr[i], tim[i][0], tim[i][1]) for i in range(len(scr))]
B = cut_take(rd(f'{D}/voice/survey_v3b.wav'), PARAS_B, wordsB)

# ---- banked signature-ending lines (V2, as in the training)
BW = json.load(open(f'{D}/bank/words.json'))
def bank(key): return dict(x=rd(f'{D}/bank/v_{key}.flac'), ws=[(w['w'], w['a'], w['b']) for w in BW[key]])

ORDER = ['hook', 'honest', 'keep', 'hi', 'seven', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'sell', 'q7', 'q8', 'health1', 'health2',
         'good', 'comment', 'follow', 'tribe', 'save', 'share', 'n_we', 'n_slog', 'remind', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
GAP = dict(hook=0.32, honest=0.42, keep=0.42, hi=0.30, seven=0.50, q1=0.55, q2=0.55, q3=0.55, q4=0.55, q5=0.55, q6=0.50, sell=0.32, q7=0.55, q8=0.60,
           health1=0.45, health2=0.55, good=0.32, comment=0.40, follow=0.45, tribe=0.50, save=0.30, share=0.45,
           n_we=0.40, n_slog=0.50, remind=0.50, o_thanks=0.25, o_support=0.45, o_massive=0.45, o_best=0.50, o_im=0.20, o_see=0.30, o_lgtc=0.0)
LEAD, TAIL = 0.20, 3.6
pieces = []; allw = []; outl = []; t = LEAD
for key in ORDER:
    P = B.get(key) or A.get(key) or bank(key); src = 'B' if key in B else 'A' if key in A else 'bank'
    pieces.append((int(round(t * SR)), P['x'])); outl.append(dict(key=key, a=round(t, 3), b=round(t + len(P['x']) / SR, 3), src=src))
    for w, s, e in P['ws']: allw.append(dict(w=w, a=round(t + s, 3), b=round(t + e, 3), line=key))
    t += len(P['x']) / SR + GAP[key]
# captions show names the way people read them (the voice text spells them for pronunciation)
def merge(line, seq, shown, after=None):
    global allw
    for i in range(len(allw) - len(seq) + 1):
        if after and not (i > 0 and norm(allw[i - 1]['w']) == after): continue
        if all(allw[i + j]['line'] == line and norm(allw[i + j]['w']) == norm(seq[j]) for j in range(len(seq))):
            allw[i:i + len(seq)] = [dict(w=shown, a=allw[i]['a'], b=allw[i + len(seq) - 1]['b'], line=line)]; return
    raise KeyError(line + ' ' + ' '.join(seq))
merge('hook', ['Olly', 'Life'], 'OlyLife'); merge('hook', ['Terra', 'P', 'ninety?'], 'Tera-P90?')
merge('tribe', ['MTG', 'tribe', 'dot', 'com', 'slash', 'group.'], 'mtgtribe.com/group', after='at')
T = t + TAIL
voice = np.zeros(int(round(T * SR)), np.float32)
for s, x in pieces: voice[s:s + len(x)] += x[:len(voice) - s]
with wave.open(f'{D}/voice.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(allw, open(f'{D}/words.json', 'w'), indent=0)
json.dump(dict(T=round(T, 3), lines=outl), open(f'{D}/lines_out.json', 'w'), indent=1)
tl = dict(T=round(T, 3), fps=30, lines={l['key']: [l['a'], l['b']] for l in outl}, words=[[w['w'], w['a'], w['b'], w['line']] for w in allw])
open(f'{D}/stage/timeline.js', 'w').write('window.TL=' + json.dumps(tl) + ';\n')
for l in outl: print(f"{l['key']:9s} {l['src']:4s} {l['a']:7.2f} {l['b']:7.2f}")
print('T =', round(T, 2), 's,', len(allw), 'words')
