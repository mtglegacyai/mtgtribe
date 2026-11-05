"""Soundtrack for the horizontal MTG TRIBE invite.
Voice and closing track: MTG's approved invite audio, cut only in silences (edl.json), never re-voiced.
Sound design: synthesised here (no samples, no extra music), ducked under the voice."""
import json, wave, numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter1d

D = '/tmp/claude-0/-home-user/da468685-967b-5760-877c-9c4fad4db3c6/scratchpad/inv/'
SR = 48000
edl = json.load(open(D + 'edl.json')); cues = json.load(open(D + 'sfx.json'))['sfx']
TOTAL, CO = edl['TOTAL'], edl['CO']
N = int(round(TOTAL * SR))
# 'you' in 'thank you for' is lifted 2 semitones (formants kept) so it no longer sounds like a full stop
wf = wave.open(D + 'audio48k_fixed.wav'); src = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float64) / 32768

# ---------- voice + closing track, re-cut ----------
voice = np.zeros((N, 2))
for k, g in enumerate(edl['SEG']):
    a, b = int(round(g['a'] * SR)), min(len(src), int(round(g['b'] * SR)))
    piece = src[a:b].copy(); f = int(.008 * SR)
    if k > 0: piece[:f] *= np.linspace(0, 1, f)[:, None]
    if k < len(edl['SEG']) - 1: piece[-f:] *= np.linspace(1, 0, f)[:, None]
    o = int(round(g['o'] * SR)); n = min(len(piece), N - o); voice[o:o + n] += piece[:n]

# ---------- synth helpers ----------
rng = np.random.default_rng(42)
T = lambda d: np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def bp(x, lo, hi, order=2): return signal.sosfilt(signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, 'highpass', fs=SR, output='sos'), x)
def norm(x, peak): m = np.abs(x).max(); return x * (peak / m) if m > 0 else x
def st(x, pan=0.0, width=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    y = np.stack([x * l, x * r], 1) * 1.414
    if width: d = int(width * SR); y[:, 1] = np.concatenate([np.zeros(d), y[:-d, 1]]) if d else y[:, 1]
    return y
def sweep_bp(x, f0, f1, f2=None, q=1.2):
    """band-pass noise whose centre glides f0 -> f1 (-> f2), block by block"""
    n = len(x); out = np.zeros(n); B = 512; zi = None
    for i in range(0, n, B):
        k = i / max(1, n - 1)
        fc = (f0 * (f1 / f0) ** (k * 2) if k < .5 else f1 * (f2 / f1) ** ((k - .5) * 2)) if f2 else f0 * (f1 / f0) ** k
        lo, hi = max(30, fc / (1 + 1 / q)), min(SR / 2 - 100, fc * (1 + 1 / q))
        sos = signal.butter(2, [lo, hi], 'bandpass', fs=SR, output='sos')
        if zi is None: zi = signal.sosfilt_zi(sos) * 0
        out[i:i + B], zi = signal.sosfilt(sos, x[i:i + B], zi=zi)
    return out
IR = None
def reverb(y, wet=.25, dur=1.4):
    global IR
    if IR is None:
        t = T(dur); IR = np.stack([lp(rng.standard_normal(len(t)), 6000) * np.exp(-t * 4.2) for _ in range(2)], 1); IR /= np.abs(IR).sum(0).max() / 6
    out = np.stack([signal.fftconvolve(y[:, c], IR[:, c])[:len(y) + len(IR) - 1] for c in range(2)], 1)
    dry = np.zeros_like(out); dry[:len(y)] = y
    return dry * (1 - wet) + out * wet
def chirp(t, f0, f1, tau): f = f1 + (f0 - f1) * np.exp(-t / tau); return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ---------- the sounds ----------
def s_whoosh(d=.6, **k):
    n = noise(d); x = sweep_bp(n, 280, 2600, 520, q=1.1); t = T(d)
    env = np.where(t < d * .55, (t / (d * .55)) ** 2.2, np.exp(-(t - d * .55) / (d * .16)))
    x = norm(x * env, .5); pans = np.linspace(-.6, .6, len(x))
    return np.stack([x * np.cos((pans + 1) * np.pi / 4), x * np.sin((pans + 1) * np.pi / 4)], 1) * 1.414
def s_hit(**k):
    t = T(.9); sub = chirp(t, 95, 38, .08) * np.exp(-t / .22); body = np.sin(2 * np.pi * 140 * t) * np.exp(-t / .05)
    cl = lp(noise(.9), 3500) * np.exp(-t / .012)
    return reverb(st(norm(sub + .5 * body + .35 * cl, .8)), .18, 1.0)
def s_boom(**k):
    t = T(2.6); sub = chirp(t, 70, 26, .25) * np.exp(-t / .7); rum = lp(noise(2.6), 380) * np.exp(-t / .55); cl = hp(noise(2.6), 1500) * np.exp(-t / .03)
    return reverb(st(norm(sub + .9 * norm(rum, 1) + .4 * cl, .95)), .3, 2.0)
def s_heart(**k):
    t = T(.6); th = lambda t0, a: a * np.sin(2 * np.pi * 52 * (t - t0)) * np.exp(-np.clip(t - t0, 0, None) / .07) * (t >= t0)
    return st(norm(lp(th(0, 1) + th(.2, .7), 200), .75))
def s_drone(dur=12.5, **k):
    t = T(dur); x = sum(np.sin(2 * np.pi * f * t + p) * a for f, a, p in [(41.2, 1, 0), (41.6, .8, 1), (61.8, .5, 2), (82.4, .25, 3)])
    x += .6 * norm(lp(noise(dur), 160), 1) * (.6 + .4 * np.sin(2 * np.pi * .13 * t))
    env = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 1.2) * (.75 + .25 * np.sin(2 * np.pi * .08 * t))
    return st(norm(x * env, .32), 0, .012)
def s_swell(dur=2.5, **k):
    t = T(dur); x = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(110, 1), (164.8, .7), (220, .45), (329.6, .2)])
    x = lp(x, 900) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return reverb(st(norm(x, .26), 0, .015), .35, 1.6)
def s_riser(dur=1.9, **k):
    t = T(dur); nz = sweep_bp(noise(dur), 250, 7000, q=1.4); tone = chirp(t, 160, 900, -dur * 2) if False else np.sin(2 * np.pi * np.cumsum(160 * (900 / 160) ** (t / dur)) / SR)
    env = (t / dur) ** 2.6
    return st(norm((norm(nz, 1) + .35 * tone) * env, .6), 0, .01)
def s_scrape(**k):
    d = .55; t = T(d); x = hp(noise(d), 2200) * (rng.random(len(t)) < .02) * 3 + hp(noise(d), 3000) * .4
    return st(norm(x * np.exp(-t / .2) * np.minimum(1, t / .03), .35), .2)
def s_shimmer(**k):
    d = 1.6; t = T(d); x = sum(np.sin(2 * np.pi * f * t + rng.random() * 6) * np.exp(-t / (.4 + rng.random() * .6)) for f in [2093, 2637, 3136, 4186, 5274])
    x += .5 * bp(noise(d), 6000, 11000) * np.exp(-t / .5)
    return reverb(st(norm(x * np.minimum(1, t / .05) * (1 + .3 * np.sin(2 * np.pi * 9 * t)), .26), 0, .02), .35, 1.4)
def s_chime(**k):
    d = 2.2; t = T(d)
    bell = lambda f, t0: (t >= t0) * sum(a * np.sin(2 * np.pi * f * m * (t - t0)) * np.exp(-np.clip(t - t0, 0, None) / dd) for m, a, dd in [(1, 1, .9), (2.76, .4, .35), (5.4, .2, .15)])
    return reverb(st(norm(bell(1318.5, 0) + .8 * bell(1760, .07) + .5 * bell(2637, .14), .42), 0, .01), .35, 1.8)
def s_pop(**k):
    t = T(.14); x = chirp(t, 520, 1150, .02) * np.exp(-t / .028) + .3 * hp(noise(.14), 2000) * np.exp(-t / .004)
    return st(norm(x, .32), rng.uniform(-.3, .3))
def s_tick(**k):
    t = T(.04); return st(norm(hp(noise(.04), 3000) * np.exp(-t / .005), .28), rng.uniform(-.2, .2))
def s_type(**k):
    t = T(.06); x = bp(noise(.06), 1800, 5200) * np.exp(-t / .007) + .6 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / .015)
    return st(norm(x, rng.uniform(.22, .3)), .25)
def s_click(**k):
    t = T(.12); c = lambda t0: (t >= t0) * hp(noise(.12), 2500) * np.exp(-np.clip(t - t0, 0, None) / .004)
    return st(norm(c(0) + .7 * c(.03), .4), .3)
def s_door(**k):
    a = s_whoosh(1.3); b = s_shimmer(); out = np.zeros((max(len(a), len(b) + int(.3 * SR)), 2)); out[:len(a)] += a * .8; out[int(.3 * SR):int(.3 * SR) + len(b)] += b
    return out
def s_draw(dur=1.0, **k):
    t = T(dur); strokes = np.abs(np.sin(2 * np.pi * 3.3 * t + rng.random() * 3)) ** 3
    return st(norm(bp(noise(dur), 2800, 7000) * strokes * np.minimum(1, (dur - t) / .1), .14), .1)
def s_flow(dur=3.0, **k):
    t = T(dur); x = norm(bp(noise(dur), 700, 2200), 1) * (.5 + .5 * np.sin(2 * np.pi * 2.1 * t)) * .5
    for _ in range(int(dur * 6)):
        t0 = rng.random() * (dur - .2); f = rng.choice([2093, 2349, 2637, 3136]); x += (t >= t0) * .6 * np.sin(2 * np.pi * f * (t - t0)) * np.exp(-np.clip(t - t0, 0, None) / .06)
    return reverb(st(norm(x * np.sin(np.pi * t / dur), .14), 0, .01), .3, 1.2)
def s_grow(dur=1.4, **k):
    out = np.zeros((int((dur + .3) * SR), 2))
    for i, f in enumerate([392, 494, 587, 784]):
        p = s_pop() * .9; t0 = int(i * .28 * SR); t = T(.25); tone = st(np.sin(2 * np.pi * f * t) * np.exp(-t / .07) * .25)
        out[t0:t0 + len(tone)] += tone; out[t0:t0 + len(p)] += p * .4
    return out
def s_rain(dur=1.9, **k):
    t = T(dur); x = lp(hp(noise(dur), 900), 7000) * .4 + hp(noise(dur), 2500) * (rng.random(len(t)) < .004) * 4
    return st(norm(x * np.minimum(1, t / .3) * np.minimum(1, (dur - t) / .5), .22), 0, .02)
def s_thunder(**k):
    d = 2.8; t = T(d); crack = hp(noise(d), 800) * np.exp(-t / .06); rum = lp(noise(d), 140) * np.exp(-t / .9) * (1 + .6 * np.sin(2 * np.pi * 3 * t))
    return reverb(st(norm(.6 * norm(crack, 1) + norm(rum, 1), .8), 0, .02), .35, 2.0)
def s_stop(**k):
    d = .8; t = T(d); f = 40 + 400 * np.exp(-t / .18); ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + .4 * np.sin(2 * ph) + .2 * np.sin(3 * ph)) * np.exp(-t / .35)
    return st(norm(lp(x, 2000), .34))
def s_swing(**k):
    a = s_whoosh(.5) * .7; t = T(.05); b = st(hp(noise(.05), 2500) * np.exp(-t / .006)) * .25
    out = np.zeros((len(a) + int(.05 * SR), 2)); out[:len(a)] += a; out[len(a) - int(.02 * SR):len(a) - int(.02 * SR) + len(b)] += b; return out
def s_scan(**k):
    d = .65; t = T(d); x = np.sin(2 * np.pi * (1100 + 300 * np.sin(2 * np.pi * 22 * t)) * t) * .4 + bp(noise(d), 3000, 6000) * .3
    return st(norm(x * np.sin(np.pi * t / d), .18), -.2)
def s_shatter(**k):
    d = 1.3; t = T(d); x = hp(noise(d), 3000) * np.exp(-t / .05)
    for _ in range(40):
        t0 = rng.random() * .35; f = rng.uniform(2500, 9000); x += (t >= t0) * .35 * np.sin(2 * np.pi * f * (t - t0)) * np.exp(-np.clip(t - t0, 0, None) / rng.uniform(.03, .2))
    return reverb(st(norm(x, .45), 0, .015), .3, 1.4)
def s_rise(**k):
    t = T(.7); x = sweep_bp(noise(.7), 300, 4000, q=1.2) * (t / .7) ** 2
    return st(norm(x, .3))
def s_snip(**k):
    t = T(.2); c = lambda t0: (t >= t0) * bp(noise(.2), 3500, 9000) * np.exp(-np.clip(t - t0, 0, None) / .008)
    return st(norm(c(0) + c(.07), .35), .15)
def s_snap(**k):
    t = T(.45); f = 330 * (1 + .25 * np.exp(-t / .02)); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .09) + .5 * hp(noise(.45), 3000) * np.exp(-t / .006)
    return st(norm(x, .42), rng.uniform(-.3, .3))
def s_shout(**k):
    t = T(.42); f = 210 * (1 + .03 * np.sin(2 * np.pi * 6 * t)); saw = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    return st(norm(bp(saw, 600, 2400) * np.minimum(1, t / .03) * np.exp(-t / .18), .16), -.35)
def s_ignite(**k):
    t = T(.7); x = bp(noise(.7), 900, 4500) * np.minimum(1, t / .04) * np.exp(-t / .16) + .7 * np.sin(2 * np.pi * 90 * t) * np.exp(-t / .1)
    return reverb(st(norm(x, .3)), .2, 1.0)
def s_stamp(**k):
    t = T(.5); x = np.sin(2 * np.pi * 170 * t) * np.exp(-t / .06) + .6 * lp(noise(.5), 2500) * np.exp(-t / .015) + .5 * chirp(t, 80, 45, .05) * np.exp(-t / .12)
    return reverb(st(norm(x, .6)), .15, .9)
def s_flip(**k):
    a = s_whoosh(.35) * .6; b = s_whoosh(.3) * .5; out = np.zeros((len(a) + len(b), 2)); out[:len(a)] += a; out[int(.18 * SR):int(.18 * SR) + len(b)] += b; return out
SYN = {k[2:]: v for k, v in globals().items() if k.startswith('s_')}

# ---------- place the cues ----------
sfx = np.zeros((N + 5 * SR, 2))
for c in cues:
    fn = SYN[c['name']]; y = fn(**({'dur': c['dur']} if 'dur' in c else {}))
    i = int(round(c['t'] * SR))
    if c['name'] in ('whoosh', 'rise', 'riser', 'swing'):           # whooshes peak on the cue, not after it
        i -= int(len(y) * (.55 if c['name'] == 'whoosh' else .9)) if c['name'] != 'riser' else 0
    i = max(0, i); sfx[i:i + len(y)] += y * c['gain']
sfx = sfx[:N]

# duck the sound design under the voice (about -9 dB while MTG speaks), but leave the cold open at full strength
venv = maximum_filter1d(np.abs(voice).max(1), int(.12 * SR))
venv = signal.sosfilt(signal.butter(1, 6, 'lowpass', fs=SR, output='sos'), venv)
duck = 1 - .65 * np.clip(venv / .08, 0, 1)
COLD = 1.45; under = .62
gain = np.where(np.arange(N) / SR < CO, COLD, under) * duck
mix = voice + sfx * gain[:, None]

# peak limiter at -1 dBFS with 2 ms look-ahead
lim = .89; pk = maximum_filter1d(np.abs(mix).max(1), int(.004 * SR)); g = np.minimum(1, lim / np.maximum(pk, 1e-9))
g = signal.sosfilt(signal.butter(1, 30, 'lowpass', fs=SR, output='sos'), g); g = np.minimum(g, lim / np.maximum(pk, 1e-9) + .02)
mix = mix * np.clip(g, 0, 1)[:, None]
pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
w = wave.open(D + 'mix.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('mix written', round(N / SR, 2), 's, peak', round(float(np.abs(mix).max()), 3), 'voice peak', round(float(np.abs(voice).max()), 3))
