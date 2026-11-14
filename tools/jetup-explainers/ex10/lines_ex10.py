# JetUP explainer #10, "Know your numbers: the Exposure Calculator" (MTG approved the six new lines on 14 Nov 2026: "Yes, record (1 credit)").
# Builds every voice line the video uses as v_<key>.wav (48 kHz mono) plus lines.json and words.json:
#  - the eight new lines from MTG Master Voice V3 (one request, 1 credit), cut on HeyGen's word times with the cut edges
#    snapped to the silence around them, levelled to -18.5 LUFS like his other V3 lines;
#  - "Then you connect a strategy through CopyX." and "Your deposit goes into an M T five account at TAG Markets, in your
#    name." from the 5 Checks take o1, cut on their forced-alignment word times (o1_words.json);
#  - "Read the terms." and "A thirty percent performance fee, taken from profits only." from the sign-up training take t3:
#    one continuous stretch (8.95 to 14.055 s) split in the silence at 10.40 s, so 'perf' plays straight after 'terms'
#    with no gap (lines.json marks it "joined": true) and the pair sounds exactly like the take, its own pause included;
#  - the Myfxbook line, the greeting, "Simple, right? Now it's your turn.", the fair-play lines and the signature ending
#    from explainer #4's banked pack.
# Usage: python3 lines_ex9.py [take] [take_raw.json]   (defaults: voice/ex9v3.flac and voice/ex9v3_raw.json)
import json, os, re, subprocess, sys, tempfile, wave
import numpy as np
SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BANK = 'origin/jetup-video-work:jetup-work/voice-bank/'
# the take: an explicit path, else the FLAC saved next to this script (voice/ex9v3.flac, the same samples as HeyGen's WAV;
# also banked as explainers/ex9v3.flac on jetup-video-work once MTG's preview is done)
TAKE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'voice', 'ex10v3.flac')
RAW = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'voice', 'ex10v3_raw.json')
TMP = tempfile.mkdtemp(prefix='ex10bank_')
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
def cut(x, s, e, fade_in=.012, fade_out=.05):
    y = x[int(s * SR):int(e * SR)].copy(); fi, fo = int(fade_in * SR), int(fade_out * SR)
    if fi: y[:fi] *= np.linspace(0, 1, fi)
    if fo: y[-fo:] *= np.linspace(1, 0, fo)
    return y

PLAN = json.load(open(os.path.join(HERE, 'plan.json')))
NEW = [l for l in PLAN['lines'] if l['kind'] == 'new']
L, WD = {}, {}
# HeyGen's word times for the last four new lines run ahead of their audio: the pauses inside those lines end 0.15 to 0.22 s
# after HeyGen's word gaps (checked 13 Nov 2026 on the pauses below -44 dB and with faster-whisper; the first four lines agree
# within 0.04 s). Shift those words so the captions and every cue land on what MTG says. Same drift as explainer #8.
ALIGN = {'nex': .15, 'nown': .19, 'ndrag': .17, 'nlines': .18, 'nrecap': .2}

# 1. the eight new V3 lines
x = load(TAKE); WW = json.load(open(RAW))['original_words']; i = 0
for n, ln in enumerate(NEW):
    k, text = ln['key'], ln['text']
    seg = WW[i:i + len(toks(text))]; i += len(seg)
    assert [re.sub(r"[^a-z0-9']", '', w['text'].lower()) for w in seg] == [t.lower() for t in toks(text)], (k, seg)
    sh = ALIGN.get(k, 0.0)
    prev_end = WW[i - len(seg) - 1]['end_time'] + ALIGN.get(NEW[n - 1]['key'], 0.0) if n > 0 else 0.0
    next_st = WW[i]['start_time'] + ALIGN.get(NEW[n + 1]['key'], 0.0) if i < len(WW) else len(x) / SR
    s, e = snap(x, seg[0]['start_time'] + sh, seg[-1]['end_time'] + sh, prev_end + .06, next_st - .08)
    y = cut(x, s, e); p = os.path.join(HERE, f'v_{k}.wav'); save(p, y); save(p, y * 10 ** ((-18.5 - lufs(p)) / 20))
    L[k] = dict(file=f'v_{k}.wav', src='explainers/ex10v3.flac', a=round(s, 3), b=round(e, 3), dur=round(len(y) / SR, 3), text=text)
    WD[k], j = [], 0                                 # a written word like "read-only" is two of HeyGen's words
    for t in text.split():
        m = len(toks(t)); ws = seg[j:j + m]; j += m
        WD[k].append(dict(w=t, a=round(ws[0]['start_time'] + sh - s, 3), b=round(ws[-1]['end_time'] + sh - s, 3)))
assert i == len(WW), (i, len(WW))

# 2. four lines from explainer #3's banked pack (two from the sign-up training take t1, two in V3)
P3 = 'explainers/ex3-pack/'
L3 = json.load(open(bank(P3 + 'lines.json'))); W3 = json.load(open(bank(P3 + 'words.json')))
for k in ('six', 'expo', 'swings', 'nlimit'):
    y = load(bank(P3 + f'v_{k}.flac')); save(os.path.join(HERE, f'v_{k}.wav'), y)
    L[k] = dict(L3[k], dur=round(len(y) / SR, 3)); WD[k] = W3[k]
P4 = 'explainers/ex4-pack/'
L4 = json.load(open(bank(P4 + 'lines.json'))); W4 = json.load(open(bank(P4 + 'words.json')))

# 4. explainer #4's banked pack (the Myfxbook line, greeting, close, fair play, signature ending)
for k in ('hi', 'n_turn2', 'l_ifme', 'every', 'n_save', 'n_share', 'n_we', 'n_slog',
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
