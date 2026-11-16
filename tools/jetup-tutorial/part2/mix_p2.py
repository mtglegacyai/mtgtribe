# JetUP tutorial part 1: mix MTG's voice, the closing track "They Call Me MTG" (ends exactly at the last frame,
# soft under speech, rising after) and light sound design synced to the visuals. Output: mix.wav (-14 LUFS).
import json, os, re, subprocess, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TL = json.load(open(os.path.join(HERE, 'mixcues.json')))
TRACK = os.path.join(HERE, '..', '..', 'promo', 'track.mp3')
T, C = TL['T'], TL['cues']
N = int(T * SR)
rng = np.random.default_rng(7)


def ff_read(path, ch, extra=()):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, *extra, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()


def lufs(x):
    p = os.path.join(HERE, '_m.wav'); write(p, x)
    out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])


def write(path, x):
    x = np.atleast_2d(x.T).T if x.ndim == 1 else x
    with wave.open(path, 'wb') as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


# ---------- voice: clean, present, gently compressed, -16 LUFS ----------
vf = ('highpass=f=75,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=2.5,'
      'equalizer=f=9500:t=h:w=0.7:g=1.5,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=140:makeup=2,deesser=i=0.25')
voice = ff_read(os.path.join(HERE, 'voice.wav'), 1, ['-af', vf])[:, 0]
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
voice *= 10 ** ((-16 - lufs(voice)) / 20)

# speech mask (1 while MTG speaks), smoothed for ducking
mask = np.zeros(N)
for a, b in TL['spans']:
    mask[int((a - .12) * SR):int((b + .2) * SR)] = 1
def fconv(x, k):
    """np.convolve(x, k, 'same') by FFT (same result, seconds instead of minutes)."""
    n = len(x) + len(k) - 1; N = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(k, N), N)[:n]
    s = (len(k) - 1) // 2
    return y[s:s + len(x)]
def smooth(m, sec):
    k = int(sec * SR); ker = np.hanning(2 * k + 1); ker /= ker.sum()
    return fconv(m, ker)
duck = smooth(mask, .25)

# ---------- closing track: last 50.5 s of the 51.36 s track, so it ends on the final frame ----------
trk = ff_read(TRACK, 2)
off = len(trk) - N
trk = trk[off:] if off >= 0 else np.pad(trk, ((-off, 0), (0, 0)))
trk *= 10 ** ((-17 - lufs(trk)) / 20)              # music-only level
env = 1 - .72 * duck                                 # about -14 dB under speech
t0 = max(0, -off) / SR                              # the track starts 51.36 s before the end
env *= np.clip((np.arange(N) / SR - t0) / .6, 0, 1)
trk *= env[:, None]

# ---------- sound design ----------
sfx = np.zeros((N, 2))
def add(sig, t, gain_db, pan=0):
    s = int(t * SR); sig = sig[:max(0, N - s)] * 10 ** (gain_db / 20)
    sfx[s:s + len(sig), 0] += sig * (1 - max(0, pan)); sfx[s:s + len(sig), 1] += sig * (1 + min(0, pan))
def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def lowpass(x, fc):
    """One-pole low-pass, as an FFT convolution with its (truncated) impulse response."""
    a = np.exp(-2 * np.pi * fc / SR); L = int(np.ceil(np.log(1e-9) / np.log(a))) + 1
    h = (1 - a) * a ** np.arange(L)
    n = len(x) + L - 1; N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(h, N), N)[:len(x)]
def whoosh(d=.5, up=True):
    n = int(d * SR); x = rng.standard_normal(n)
    # sweep: blend of two lowpassed noises, crossfaded, gives a moving band
    lo, hi = lowpass(x, 500), x - lowpass(x, 2500)
    k = np.linspace(0, 1, n) if up else np.linspace(1, 0, n)
    y = (1 - k) * lo + k * hi * .6
    return y * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 / (np.abs(y).max() + 1e-9)
def impact():
    n = int(.7 * SR); tt = np.arange(n) / SR
    f = 48 + 60 * np.exp(-tt / .06); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, .22)
    click = lowpass(rng.standard_normal(n), 1800) * env_exp(n, .015) * 2
    y = body + click; return y / np.abs(y).max()
def pop(f0=720, f1=430, d=.12):
    n = int(d * SR); tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt / .03)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, .035); return y / np.abs(y).max()
def tick(f=2300):
    n = int(.05 * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * tt) * env_exp(n, .008); return y / np.abs(y).max()
def chime(notes=(1318.5, 1975.5, 2637.0), d=1.1):
    n = int(d * SR); tt = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * tt) * env_exp(n, .35 / (1 + i * .5)) / (1 + i) for i, f in enumerate(notes))
    y *= np.clip(tt / .004, 0, 1); return y / np.abs(y).max()
def sparkle():
    y = np.zeros(int(.6 * SR))
    for i, f in enumerate([2093, 2637, 3136, 4186]):
        c = chime((f,), .35); s = int(i * .07 * SR); y[s:s + len(c)] += c[:len(y) - s] * (.8 - i * .12)
    return y / np.abs(y).max()
def thud():
    n = int(.25 * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * (70 + 40 * np.exp(-tt / .03)) * tt) * env_exp(n, .07); return y / np.abs(y).max()


# a very soft bed under the first part, until the closing track comes in (chord follows the steps)
n = int((t0 + 1.5) * SR); tt = np.arange(n) / SR
roots = [110, 98, 116.5, 103.8]
bed = np.zeros(n)
edges = [0] + [s for s in TL['steps'] if s < t0] + [t0 + 1.5]
for i in range(len(edges) - 1):
    a, b = int(edges[i] * SR), int(edges[i + 1] * SR)
    r = roots[i % len(roots)]; seg = tt[a:b]
    bed[a:b] = sum(np.sin(2 * np.pi * f * seg + k) for k, f in enumerate((r, r * 1.5, r * 2, r * 3))) / 4
bed = lowpass(bed, 900)
fade = np.clip(tt / 1.5, 0, 1) * np.clip((t0 + 1.2 - tt) / 1.5, 0, 1)
k = int(.25 * SR); ker = np.hanning(2 * k + 1); ker /= ker.sum()
bed = fconv(bed, ker) * fade * (1 + .1 * np.sin(2 * np.pi * .25 * tt))
add(bed / (np.abs(bed).max() + 1e-9), 0, -31)

# sound design: title hit, a whoosh at every step, a soft click on every tap, pops on highlights, chimes on success
add(impact(), .15, -16); add(sparkle(), .5, -27)
for s in TL['steps']: add(whoosh(.45), s - .3, -27)
for sc in ('tip', 'mail', 'recap', 'next', 'outro'): add(whoosh(.5), TL['scenes'][sc][0] - .3, -25)
add(pop(), TL['scenes']['tip'][0] + .1, -24)
for t in TL['taps']: add(tick(2600), t - .01, -21); add(pop(520, 330, .1), t, -27)
for t in TL['rings']: add(pop(700, 450, .1), t, -30)
for t in TL['chips']: add(tick(2000), t, -30)
for key in [k for k in C if k.startswith('suc_')]:
    add(chime(), C[key], -26)
for t in C['plan_in']: add(pop(680, 420, .1), t - .1, -27)
for i, t in enumerate(C['plan_tick']): add(tick(2000 + 90 * i), t - .03, -24)
add(chime((1318.5, 1975.5, 2637.0, 3520.0)), C['plan_tick'][-1] + .3, -25)
for t in C['nb']: add(pop(640, 400, .1), t - .15, -26)
for k in ('o_like', 'o_share', 'o_comment'): add(pop(), C[k] - .15, -25)
add(sparkle(), C['o_you'] - .05, -24); add(impact(), C['o_lgtc'] - .2, -18); add(sparkle(), C['o_lgtc'] + .1, -25)
add(chime(), .55, -27)
sfx *= (1 - .45 * duck)[:, None]

mixd = voice[:, None] * np.ones((1, 2)) + trk + sfx
mixd[-int(.08 * SR):] *= np.linspace(1, 0, int(.08 * SR))[:, None]
write(os.path.join(HERE, 'mix_raw.wav'), mixd)
p1 = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af',
                     'loudnorm=I=-14:TP=-2.8:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-2.8:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af', af, '-ar', str(SR), os.path.join(HERE, 'mix.wav')], check=True)
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(HERE, 'mix.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
print('mix.wav', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS, length', round(N / SR, 2), 's')
print('closing track starts at', round(t0, 2), 's')
