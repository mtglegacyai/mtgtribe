# Mix for JetUP explainer #1: MTG's voice, soft sound effects on the reveals, and the full 51.36 s closing track
# "They Call Me MTG" under the ending, soft under speech and ending on the last frame (MTG, 8 Nov 2026: videos longer
# than 60 seconds get the full track; shorter ones only its last line).
# Two-pass loudnorm to -14 LUFS, true peak target -2.8 dB (AAC adds up to about 1 dB).
import json, os, re, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TL = json.load(open(os.path.join(HERE, 'mixcues.json'))); T, C, S = TL['T'], TL['cues'], TL['scenes']
N = int(round(T * SR))
def rd(path, extra=()):
    raw = subprocess.run(['ffmpeg', '-v', 'error', *extra, '-i', path, '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32).reshape(-1, 2) / 32768
def write(p, x):
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
mix = np.zeros((N, 2), np.float32)
SFX = []
def add(x, t, db, _rec=True):
    if _rec: SFX.append((x, t, db, False))
    if x.ndim == 1: x = np.stack([x, x], 1)
    s = int(t * SR)
    if s >= N: return
    seg = x[:N - s] * (10 ** (db / 20)); mix[s:s + len(seg)] += seg
# voice (gentle presence lift and compression)
voice = rd(os.path.join(HERE, 'voice.wav'), ())[:N]
v = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(HERE, 'voice.wav'), '-af',
                    'highpass=f=70,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1:g=2.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2',
                    '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
voice = np.frombuffer(v, np.int16).astype(np.float32).reshape(-1, 2) / 32768
mix[:min(N, len(voice))] += voice[:N]
# sound effects
rng = np.random.default_rng(7)
def env(n, a, r): e = np.ones(n); ka, kr = int(a * SR), int(r * SR); e[:ka] = np.linspace(0, 1, ka); e[-kr:] *= np.linspace(1, 0, kr); return e
def pop(f0=700, f1=430, d=.12):
    n = int(d * SR); tt = np.arange(n) / SR; f = np.linspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 28)
def tick(f=2400, d=.05):
    n = int(d * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 90)
def whoosh(d=.5):
    n = int(d * SR); x = rng.standard_normal(n); k = 60; x = np.convolve(x, np.ones(k) / k, 'same')
    return x / (np.abs(x).max() + 1e-9) * np.sin(np.pi * np.arange(n) / n) ** 2
def chime(fs=(1046.5, 1568.0, 2093.0)):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * (3 + i)) for i, f in enumerate(fs)) / len(fs)
def impact():
    n = int(.6 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 7) + .3 * whoosh(.6)[:n] * np.exp(-tt * 9))
add(impact(), .05, -18)
for k in ('hi', 'pic', 'split', 'risk', 'next', 'outro'): add(whoosh(.5), S[k][0] - .2, -27)
for k in ('j_card', 't_card', 'c_copy', 's_card', 'p_coin', 'p70', 'p30', 'n_head'): add(pop(), C[k] - .05, -25)
for k in ('j_comm', 'j_train', 'j_ai', 't_acc', 't_name', 'c_cx', 's_gold', 'p_broker', 'p_strat', 'p_partner', 'n_every'): add(tick(), C[k] - .02, -30)
for k in ('j_x1', 'j_x2'): add(pop(380, 240, .14), C[k] - .03, -26)
add(chime(), C['p_yours'], -27); add(chime(), C['p_nofee'], -28); add(pop(300, 180, .2), C['r_lose'], -24)
for k in ('o_like', 'o_share', 'o_comment'): add(pop(), C[k] - .12, -26)
add(chime((1318.5, 1975.5, 2637.0)), C['o_you'] - .05, -26)
# the closing track: its last N samples, so it starts 51.36 s before the end and ends on the final frame
def lufs(x):
    p = os.path.join(HERE, '_m.wav'); write(p, x if x.ndim == 2 else np.stack([x, x], 1))
    out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])
vl = lufs(voice[:N]); g = 10 ** ((-16 - vl) / 20)
mix *= 0; mix[:min(N, len(voice))] += voice[:N] * g            # voice at -16 LUFS
for args in SFX: add(*args)                                     # sound effects again, on top
TRACK = os.path.join(HERE, '..', 'promo', 'track.mp3')
trk = rd(TRACK, ())
off = len(trk) - N
trk = trk[off:] if off >= 0 else np.pad(trk, ((-off, 0), (0, 0)))
trk = trk * 10 ** ((-17 - lufs(trk)) / 20)
mask = np.zeros(N)
for a, b in TL['spans']: mask[max(0, int((a - .12) * SR)):int((b + .2) * SR)] = 1
k = int(.25 * SR); ker = np.hanning(2 * k + 1); ker /= ker.sum()
n2 = 1 << (N + len(ker) - 2).bit_length()
duck = np.fft.irfft(np.fft.rfft(mask, n2) * np.fft.rfft(ker, n2), n2)[k:k + N]
t0 = max(0, -off) / SR
envm = (1 - .72 * duck) * np.clip((np.arange(N) / SR - t0) / .6, 0, 1)
mix += trk * envm[:, None]
mix[-int(.06 * SR):] *= np.linspace(1, 0, int(.06 * SR))[:, None]
write(os.path.join(HERE, 'mix_raw.wav'), mix)
p1 = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af',
                     'loudnorm=I=-14:TP=-2.8:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-2.8:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af', af, '-ar', str(SR), os.path.join(HERE, 'mix.wav')], check=True)
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(HERE, 'mix.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('mix.wav', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS, length', round(N / SR, 2), 's')
