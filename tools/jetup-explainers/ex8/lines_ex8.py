# JetUP explainer #8, "Getting your money out" (MTG approved the ten new lines on 12 Nov 2026: "Yes, record (1 credit)").
# Builds every voice line the video uses as v_<key>.wav (48 kHz mono) plus lines.json and words.json:
#  - the ten new lines from MTG Master Voice V3 (one request, 1 credit), cut on HeyGen's word times with the cut edges
#    snapped to the silence around them, levelled to -18.5 LUFS like his other V3 lines;
#  - "My advice?", "Don't take my word for it." and "Log in yourself, and see your own balance." from the 5 Checks takes,
#    cut on their forced-alignment word times (o1_words.json, o2_words.json);
#  - the three promo rule lines from the sign-up training take t3, at explainer #5's tested cuts;
#  - everything else (greeting, "Profits can be withdrawn any time.", "Start small...", "Let the system prove itself",
#    "Simple, right? Now it's your turn.", the fair-play lines and the signature ending) from explainer #4's banked pack.
# Usage: python3 lines_ex8.py [take] [take_raw.json]   (defaults: voice/ex8v3.flac and voice/ex8v3_raw.json)
import json, os, re, subprocess, sys, tempfile, wave
import numpy as np
SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BANK = 'origin/jetup-video-work:jetup-work/voice-bank/'
VDIR = os.environ.get('EX8_VOICE', HERE)
# the take: an explicit path, else $EX8_VOICE/ex8v3.wav, else the FLAC saved next to this script (voice/ex8v3.flac, the same
# samples as HeyGen's WAV; also banked as explainers/ex8v3.flac on jetup-video-work)
_def = os.path.join(VDIR, 'ex8v3.wav') if os.environ.get('EX8_VOICE') else os.path.join(HERE, 'voice', 'ex8v3.flac')
TAKE = sys.argv[1] if len(sys.argv) > 1 else _def
RAW = sys.argv[2] if len(sys.argv) > 2 else os.path.join(VDIR if os.environ.get('EX8_VOICE') else os.path.join(HERE, 'voice'), 'ex8v3_raw.json')
TMP = tempfile.mkdtemp(prefix='ex8bank_')
toks = lambda t: re.findall(r"[A-Za-z0-9']+", t)

def bank(path):
    """a file from MTG's voice bank (branch jetup-video-work), extracted once"""
    out = os.path.join(TMP, path.replace('/', '__'))
    if not os.path.exists(out):
        open(out, 'wb').write(subprocess.run(['git', '-C', REPO, 'show', BANK + path], capture_output=True, check=True).stdout)
    return out
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def save(p, y):
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
def lufs(p):
    o = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])
def rms_db(x, t, win=.01):
    a, b = int(t * SR), int((t + win) * SR)
    seg = x[max(0, a):max(0, b)]
    return -120.0 if len(seg) == 0 else 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
def snap(x, a0, b0, lo, hi, pre=.05, post=.07, thr=-46.0):
    """cut edges: walk out from the first and last word until 60 ms of silence (or the neighbouring words), plus a pad"""
    s = a0
    while s - .01 > lo and any(rms_db(x, s - .01 - k * .01) > thr for k in range(6)): s -= .01
    e = b0
    while e + .01 < hi and any(rms_db(x, e + k * .01) > thr for k in range(6)): e += .01
    return max(lo, s - pre), min(hi, e + post)
def cut(x, s, e):
    y = x[int(s * SR):int(e * SR)].copy(); fi, fo = int(.012 * SR), int(.05 * SR)
    y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
    return y

PLAN = json.load(open(os.path.join(HERE, 'plan.json')))
NEW = [l for l in PLAN['lines'] if l['kind'] == 'new']
L, WD = {}, {}
# HeyGen's word times for five of the new lines run ahead of their audio: the pauses in each cut line start and end
# 0.16 to 0.21 s after the word gaps (checked 12 Nov 2026 on the pauses below -44 dB and with faster-whisper; the other new
# lines agree within 0.05 s). Shift those words so the captions and every cue land on what MTG says.
ALIGN = {'nbranch': .19, 'nbasket': .17, 'nroute': .17, 'n48': .18, 'nrecap': .19}

# 1. the ten new V3 lines
x = load(TAKE); WW = json.load(open(RAW))['original_words']; i = 0
for n, ln in enumerate(NEW):
    k, text = ln['key'], ln['text']
    seg = WW[i:i + len(toks(text))]; i += len(seg)
    assert [re.sub(r"[^a-z0-9']", '', w['text'].lower()) for w in seg] == [t.lower() for t in toks(text)], (k, seg)
    prev_end = WW[i - len(seg) - 1]['end_time'] if i - len(seg) > 0 else 0.0
    next_st = WW[i]['start_time'] if i < len(WW) else len(x) / SR
    s, e = snap(x, seg[0]['start_time'], seg[-1]['end_time'], prev_end + .06, next_st - .08)
    y = cut(x, s, e); p = os.path.join(HERE, f'v_{k}.wav'); save(p, y); save(p, y * 10 ** ((-18.5 - lufs(p)) / 20))
    L[k] = dict(file=f'v_{k}.wav', src='explainers/ex8v3.flac', a=round(s, 3), b=round(e, 3), dur=round(len(y) / SR, 3), text=text)
    WD[k], j = [], 0                                 # a written word like "one-pager" is two of HeyGen's words
    for t in text.split():
        m = len(toks(t)); ws = seg[j:j + m]; j += m
        sh = ALIGN.get(k, 0.0)
        WD[k].append(dict(w=t, a=round(ws[0]['start_time'] - s + sh, 3), b=round(ws[-1]['end_time'] - s + sh, 3)))
assert i == len(WW), (i, len(WW))

# 2. three lines from the 5 Checks takes, on the forced-alignment word times
FA = {'advice': ('5-checks/o2.mp3', '5-checks/o2_words.json', 'My advice?'),
      'word': ('5-checks/o1.mp3', '5-checks/o1_words.json', "Don't take my word for it."),
      'login': ('5-checks/o1.mp3', '5-checks/o1_words.json', 'Log in yourself, and see your own balance.')}
for k, (src, wf, text) in FA.items():
    xs = load(bank(src)); ws_all = json.load(open(bank(wf)))['words']
    want = text.split()
    for a in range(len(ws_all) - len(want) + 1):
        if [w['word'] for w in ws_all[a:a + len(want)]] == want: break
    else: raise KeyError(k)
    seg = ws_all[a:a + len(want)]
    lo = ws_all[a - 1]['end'] + .04 if a > 0 else 0.0
    hi = ws_all[a + len(want)]['start'] - .04 if a + len(want) < len(ws_all) else len(xs) / SR
    s, e = snap(xs, seg[0]['start'], seg[-1]['end'], lo, hi)
    y = cut(xs, s, e); save(os.path.join(HERE, f'v_{k}.wav'), y)
    L[k] = dict(file=f'v_{k}.wav', src=src, a=round(s, 3), b=round(e, 3), dur=round(len(y) / SR, 3), text=text)
    WD[k] = [dict(w=w['word'], a=round(w['start'] - s, 3), b=round(w['end'] - s, 3)) for w in seg]

# 3. the promo rule lines from t3, at explainer #5's cuts (its words.json has their word times)
L5 = json.load(open(os.path.join(HERE, '..', 'ex5', 'lines.json'))); W5 = json.load(open(os.path.join(HERE, '..', 'ex5', 'words.json')))
t3 = load(bank('signup-training/t3.mp3'))
for k in ('bonus', 'ends', 'change'):
    s, e = L5[k]['a'], L5[k]['b']; y = cut(t3, s, e); save(os.path.join(HERE, f'v_{k}.wav'), y)
    L[k] = dict(L5[k], dur=round(len(y) / SR, 3)); WD[k] = W5[k]

# 4. explainer #4's banked pack (greeting, three 5 Checks lines, close, fair play, signature ending)
P4 = 'explainers/ex4-pack/'
L4 = json.load(open(bank(P4 + 'lines.json'))); W4 = json.load(open(bank(P4 + 'words.json')))
for k in ('hi', 'anytime', 'small', 'prove', 'n_turn2', 'l_ifme', 'every', 'n_save', 'n_share', 'n_we', 'n_slog',
          'o_fin', 'o_dyor', 'o_thanks', 'o_support', 'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc'):
    y = load(bank(P4 + f'v_{k}.flac')); save(os.path.join(HERE, f'v_{k}.wav'), y)
    L[k] = dict(L4[k], dur=round(len(y) / SR, 3)); WD[k] = W4[k]

ORDER = [l['key'] for l in PLAN['lines']] + ['n_save', 'n_share', 'n_we', 'n_slog', 'o_fin', 'o_dyor', 'o_thanks', 'o_support',
                                             'o_massive', 'o_best', 'o_im', 'o_see', 'o_lgtc']
missing = [k for k in ORDER if k not in L]
assert not missing, missing
json.dump({k: L[k] for k in ORDER}, open(os.path.join(HERE, 'lines.json'), 'w'), indent=1)
json.dump({k: WD[k] for k in ORDER}, open(os.path.join(HERE, 'words.json'), 'w'))
for k in ORDER:
    print(f"{k:10s} {L[k]['dur']:6.3f}s {lufs(os.path.join(HERE, L[k]['file'])):6.1f} LUFS  {L[k]['text']}")
print(len(ORDER), 'lines')
