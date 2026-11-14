# CoinZoom narration: every voice line the video uses, as v_<key>.wav (48 kHz mono) + lines.json + words.json.
#  - new lines: MTG Master Voice V3, one request (voice/czv3.wav, 1 credit, 14 Nov 2026), cut on HeyGen's word times
#    with the edges snapped to the silence around them (the explainer #10 method);
#  - banked, 0 credits: "Hi, my name is MTG, Your Digital Architect.", "Take your time.", "You can pause any step and
#    follow along with me." (sign-up training t1), "Thank you for taking the time to watch this video." (tutorial p1v2),
#    "Simple, right? Now it's your turn.", the fair-play line and the signature ending (explainer #4 pack).
# All lines are levelled to the median loudness of the banked ending lines, so the new V3 lines sit at his usual level.
import json, os, re, subprocess, sys, wave
import numpy as np
SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..', 'bank'); OUT = os.path.join(HERE, 'lines'); os.makedirs(OUT, exist_ok=True)   # bank: ../engine/fetch_bank.sh
TAKE = os.path.join(HERE, 'voice', 'czv3.flac'); RAW = os.path.join(HERE, 'voice', 'czv3_words.json')

def load(f, ss=None, to=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss), '-to', str(to)] if ss is not None else []) + ['-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768
def save(p, y):
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
def lufs(p):
    o = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])
def rms_db(x, t, win=.01):
    a, b = int(t * SR), int((t + win) * SR); seg = x[max(0, a):max(0, b)]
    return -120.0 if len(seg) == 0 else 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
def snap(x, a0, b0, lo, hi, pre=.05, post=.07, thr=-46.0):
    s = a0
    while s - .01 > lo and any(rms_db(x, s - .01 - k * .01) > thr for k in range(6)): s -= .01
    e = b0
    while e + .01 < hi and any(rms_db(x, e + k * .01) > thr for k in range(6)): e += .01
    return max(lo, s - pre), min(hi, e + post)
def cut(x, s, e, fi=.012, fo=.05):
    y = x[int(s * SR):int(e * SR)].copy(); a, b = int(fi * SR), int(fo * SR)
    if a: y[:a] *= np.linspace(0, 1, a)
    if b: y[-b:] *= np.linspace(1, 0, b)
    return y

# ---- new lines (first word, last word) as they appear in the take
NEW = [('n_in', 'In', 'app', "In this video, I'll show you how to find your virtual CoinZoom Visa debit card in the app."),
       ('n_three', 'Three', 'confirm', 'Three quick steps: tap Spend, tap Reveal, and double tap to confirm.'),
       ('n_once', 'Once', 'app', 'Once your virtual crypto debit card is activated, it lives right inside your CoinZoom app.'),
       ('n_s1', 'Step', 'screen', 'Step one. Log in, and tap the Spend tab at the bottom of the screen.'),
       ('n_s1b', 'This', 'screen', 'This opens your card screen.'),
       ('n_s2', 'Step', 'Reveal', 'Step two. Make sure Virtual Card is selected, then tap Reveal.'),
       ('n_s3', 'Step', 'you', "Step three. The app asks you to confirm it's really you."),
       ('n_s3b', 'Double', 'confirm', 'Double tap to confirm.'),
       ('n_there', 'And', 'V', 'And there it is! Your card number, cardholder name, expiry date and CVV.'),
       ('n_copy', 'Tap', 'number', 'Tap Copy to copy your card number.'),
       ('n_keep', 'Keep', 'online', 'Keep these details private, and only enter them when you pay online.'),
       ('n_recap', "Let's", 'recap', "Let's recap."),
       ('n_recap2', 'You', 'confirm', 'You tapped Spend, tapped Reveal, and double tapped to confirm.')]
# caption spellings: what people read (the voice says "Coin Zoom" and "C V V")
SPELL = {'Coin': 'CoinZoom', 'C': 'CVV'}

x = load(TAKE); W = json.load(open(RAW))['original_words']
L, WD = {}, {}
i = 0
for key, w0, w1, text in NEW:
    while W[i]['text'] != w0: i += 1
    j = i
    PREV = {'n_there': 'V', 'n_s3': 'really'}                       # the last word's neighbour, where the word repeats
    while W[j]['text'] != w1 or (key == 'n_s1' and W[j + 1]['text'] != 'This') or (key in PREV and W[j - 1]['text'] != PREV[key]): j += 1
    lo = (W[i - 1]['end_time'] + .03) if i else 0.0
    hi = (W[j + 1]['start_time'] - .03) if j + 1 < len(W) else len(x) / SR
    s, e = snap(x, W[i]['start_time'], W[j]['end_time'], lo, hi)
    save(os.path.join(OUT, f'v_{key}.wav'), cut(x, s, e))
    ws = []
    k = i
    while k <= j:
        t = W[k]['text']; a, b = W[k]['start_time'] - s, W[k]['end_time'] - s
        if t == 'Coin' and k + 1 <= j and W[k + 1]['text'] == 'Zoom': b = W[k + 1]['end_time'] - s; k += 1; t = 'CoinZoom'
        elif t == 'C' and k + 2 <= j and W[k + 1]['text'] == 'V' and W[k + 2]['text'] == 'V': b = W[k + 2]['end_time'] - s; k += 2; t = 'CVV'
        ws.append(dict(w=t, a=round(a, 3), b=round(b, 3))); k += 1
    WD[key] = ws; L[key] = dict(file=f'v_{key}.wav', src='czv3', a=round(s, 3), b=round(e, 3), dur=round(e - s, 3), text=text)
    i = j + 1

# ---- banked lines cut from the takes (cut points as in tools/jetup-tutorial/part1/lines.json)
BANKED = [('hi', 't1.mp3', 17.61, 21.215, 'Hi, my name is MTG, Your Digital Architect.'),
          ('n_thanks', 'p1v2.mp3', 0.28, 2.385, 'Thank you for taking the time to watch this video.'),
          ('takeyour', 't1.mp3', 35.595, 36.505, 'Take your time.'),
          ('pause', 't1.mp3', 36.475, 39.04, 'You can pause any step and follow along with me.')]
for key, f, a, b, text in BANKED:
    y = load(os.path.join(B, f), a, b); y = cut(y, 0, len(y) / SR, .01, .04)
    save(os.path.join(OUT, f'v_{key}.wav'), y)
    L[key] = dict(file=f'v_{key}.wav', src=f, a=a, b=b, dur=round(len(y) / SR, 3), text=text)
# ---- banked lines already cut (explainer #4 pack) with their word times
EX4 = json.load(open(os.path.join(B, 'ex4_words.json')))
for key in ['n_turn2', 'every', 'n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support',
            'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']:
    y = load(os.path.join(B, f'v_{key}.wav')); save(os.path.join(OUT, f'v_{key}.wav'), y)
    WD[key] = EX4[key]; L[key] = dict(file=f'v_{key}.wav', src='explainers/ex4-pack', dur=round(len(y) / SR, 3),
                                      text=' '.join(w['w'] for w in EX4[key]))

# ---- level: every line to the median loudness of the banked ending lines
ref = float(np.median([lufs(os.path.join(OUT, f'v_{k}.wav')) for k in ['o_fin', 'o_thanks', 'o_massive', 'o_best', 'o_im', 'every', 'n_save']]))
for k, v in L.items():
    p = os.path.join(OUT, v['file']); lv = lufs(p)
    if k in ('o_lgtc', 'o_see', 'takeyour'): v['lufs_in'] = lv; continue        # very short: keep as banked
    y = load(p) * 10 ** ((ref - lv) / 20); save(p, y); v['lufs_in'] = lv
print('reference', round(ref, 2), 'LUFS')
json.dump(L, open(os.path.join(HERE, 'lines.json'), 'w'), indent=1)
json.dump(WD, open(os.path.join(HERE, 'words_partial.json'), 'w'), indent=1)
for k, v in L.items(): print(f"{k:10s} {v['dur']:6.2f}s  {v.get('lufs_in', 0):6.1f}  {v['text']}")
