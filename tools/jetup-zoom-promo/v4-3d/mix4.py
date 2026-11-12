# JetUP Zoom promo: mix MTG's voice, the closing track "They Call Me MTG" (ends exactly at the last frame,
# soft under speech, rising after) and light sound design synced to the visuals. Output: mix.wav (-14 LUFS).
import json, os, re, subprocess, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TL = json.loads(re.sub(r'^window\.TL = |;\s*$', '', open(os.path.join(HERE, 'stage4', 'timing.js')).read()))
TRACK = os.path.join(HERE, '..', 'track.mp3')
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
def smooth(m, sec):
    k = int(sec * SR); ker = np.hanning(2 * k + 1); ker /= ker.sum()
    return np.convolve(m, ker, 'same')
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
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
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

# hook: a soft pad and riser carry the first seconds until the closing track comes in
if t0 > 1.5:
    n = int((t0 + 1) * SR); tt = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * f * tt + i) for i, f in enumerate((110, 164.8, 220, 329.6))) / 4
    pad *= np.clip(tt / .4, 0, 1) * np.clip((t0 + .6 - tt) / 1.2, 0, 1) * (1 + .15 * np.sin(2 * np.pi * .5 * tt))
    add(lowpass(pad, 1200) / np.abs(lowpass(pad, 1200)).max(), 0, -27)
add(impact(), .2, -11); add(whoosh(.45, False), C['gold0'] - .15, -21); add(thud(), C['gold0'] + .3, -15)
add(pop(), C['works0'] - .5, -25); add(pop(560, 340, .16), C['before0'] - .05, -22); add(tick(2400), C['cent'], -25)
# invitation
add(whoosh(.5), C['hi'] - .5, -25); add(chime(), C['hi'] - .2, -27); add(pop(), C['mtg'] - .25, -25)
add(whoosh(.55), C['inviting'] - .3, -23); add(sparkle(), C['inviting'] - .05, -24); add(pop(), C['live0'] - .1, -27)
add(pop(640, 400), C['zoom'] - .15, -24); add(impact(), C['tonight'] - .02, -14)
# times
add(whoosh(.5), C['eight'] - .55, -25)
for k in ('eight', 'seven', 'eleven'): add(tick(1900), C[k] - .2, -22)
# why come
add(whoosh(.45), C['curious'] - .4, -26); add(pop(520, 330, .14), C['curious'] - .1, -23); add(pop(520, 330, .14), C['burned'] - .4, -23)
add(chime((1318.5, 1975.5)), C['come'] - .05, -27); add(chime((1567.98, 2349.3)), C['ask'] - .15, -28)
# three things
add(whoosh(.5), C['learn3'] - .4, -25); add(pop(), C['learn3'] - .1, -24)
for k in ('one', 'two', 'threeP'): add(pop(640, 400), C[k] - .12, -22); add(tick(2200), C[k] - .05, -27)
# decide
add(whoosh(.45), C['trading'] - .4, -26); add(thud(), C['trading'] - .05, -18); add(pop(), C['learnF'] - .2, -24); add(chime(), C['decide'] - .35, -26)
# join + share
add(whoosh(.5), C['join'] - .4, -25); add(pop(560, 340, .16), C['join'] - .1, -22)
for k in ('mtgU', 'tribe', 'dot', 'com', 'slash', 'jet', 'zoomU'): add(tick(2000), C[k] - .02, -29)
add(tick(2600), C['zoomU'] + .55, -18); add(chime((1975.5, 2637)), C['zoomU'] + .58, -27); add(pop(), C['logIn'] - .1, -25)
add(whoosh(.5), C['send'] - .15, -25); add(whoosh(.7), C['someone'] - .1, -24)
# see you tonight
add(whoosh(.5), C['see'] - .4, -25); add(impact(), C['see'] - .08, -15)
for d in (.35, .5, .65): add(tick(1800), C['see'] + d, -26)
add(sparkle(), C['lgtc'] - .05, -25)

# 3D moments (v4): coin clinks, clock ticks, gift pop
def clink(f=3200):
    n = int(.25 * SR); tt = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt / (.06 / k)) / k for k in (1, 1.51, 2.27))
    return y / np.abs(y).max()
rc = np.random.default_rng(3)
for i in range(9): add(clink(2600 + 900 * rc.random()), C['cent'] - .2 + i * .09 + .05 * rc.random(), -27, rc.uniform(-.6, .6))
for k in ('eight', 'seven', 'eleven'):
    for j in range(6): add(tick(3000), C[k] - .1 + j * .13, -31, .2)
add(pop(480, 300, .18), C['hundred'] - .3, -21); add(sparkle(), C['hundred'] - .1, -26)
for i in range(7): add(clink(2400 + 1000 * rc.random()), C['see'] + i * .07, -28, rc.uniform(-.7, .7))
for j in range(4): add(tick(1500 + 200 * j), C['started'] - .3 + j * (C['right'] - C['started'] + .5) / 4, -27)
sfx *= (1 - .45 * duck)[:, None]    # keep effects tucked under the voice

mixd = voice[:, None] * np.ones((1, 2)) + trk + sfx
mixd[-int(.08 * SR):] *= np.linspace(1, 0, int(.08 * SR))[:, None]   # no click on the track's final hit
write(os.path.join(HERE, 'mix_raw.wav'), mixd)
# master: two-pass loudnorm to -14 LUFS, true peak -1.5 dBTP
p1 = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af',
                     'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af', af, '-ar', str(SR), os.path.join(HERE, 'mix.wav')], check=True)
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(HERE, 'mix.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
print('mix.wav', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS, length', round(N / SR, 2), 's')
print('track offset (s into the track):', round(off / SR, 2))
