# JetUP 5 Checks v5 audio: sharper voice, soft SFX on what appears, closing track "They Call Me MTG" in the last 51.36 s.
import json, os, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TL = json.load(open(os.path.join(HERE, 'tl.json')))
EV = json.load(open(os.path.join(HERE, 'events.json')))
TOTAL, SPEECH_END = TL['total'], TL['speech_end']
TRACK = os.path.join(HERE, '..', 'jetup-work', 'audio', 'they-call-me-mtg-closing-track.mp3')
N = int(TOTAL * SR)
rng = np.random.default_rng(7)

def wav_out(p, y, ch=1):
    y = np.clip(y, -1, 1)
    with wave.open(p, 'wb') as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())

def env(n, a, d):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d); return e

def whoosh(dur=0.42, lo=500, hi=3500, gain=0.085):
    n = int(dur * SR); x = rng.standard_normal(n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    X *= np.exp(-0.5 * ((np.log(f + 1) - np.log((lo * hi) ** 0.5)) / 0.75) ** 2)
    y = np.fft.irfft(X, n); y /= np.abs(y).max() + 1e-9
    t = np.arange(n) / n; e = np.sin(np.pi * t) ** 1.6
    return y * e * gain

def tick(gain=0.06):
    n = int(0.045 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2300 * t) * 0.6 + np.sin(2 * np.pi * 4100 * t) * 0.4) * np.exp(-t / 0.008) * gain

def pop(gain=0.16):
    n = int(0.12 * SR); t = np.arange(n) / SR; f = 520 + 900 * (t / t[-1])
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035) * gain

def impact(gain=0.14):
    n = int(0.6 * SR); t = np.arange(n) / SR; f = 95 * np.exp(-t * 3) + 45
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    return y * gain + whoosh(0.6, 200, 1500, gain * 0.35)[:n]

sfx = np.zeros(N + SR, np.float32)
def put(t, y):
    a = int(t * SR); b = min(len(sfx), a + len(y)); sfx[a:b] += y[:b - a]

checks = set(round(t, 2) for t in EV['checks'])
for t in EV['cards'][1:]:
    if round(t, 2) in checks: put(t - 0.05, impact())
    else: put(t - 0.12, whoosh())
last = -1
for t, kind in sorted(EV['els']):
    if kind == 'row' and t - last > 0.18: put(t, tick()); last = t
for t in EV['pops']: put(t, pop())
for t0, t1, els in EV['scenes']:
    put(t0 - 0.15, whoosh(0.7, 300, 5000, 0.14)); put(t1 - 0.1, whoosh(0.5, 400, 4000, 0.10))
    last = -1
    for t, kind in sorted(els):
        if t - last > 0.18: put(t, tick(0.05) if kind != 'row' else pop(0.10)); last = t
put(EV['end'] - 0.4, whoosh(0.8, 300, 5000, 0.14))

# voice: decode, then sharpen (less mud, more presence and air, gentle compression)
voice_raw = os.path.join(HERE, 'voice_v5_dry.wav'); voice = os.path.join(HERE, 'voice_v5.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', voice_raw, '-af',
                'highpass=f=70,equalizer=f=260:t=q:w=1.1:g=-2.2,equalizer=f=3300:t=q:w=1.0:g=2.6,equalizer=f=9500:t=q:w=0.9:g=1.6,'
                'acompressor=threshold=-21dB:ratio=2.4:attack=6:release=140:makeup=2.2,deesser=i=0.3:m=0.5:f=0.55,aresample=48000', '-ac', '1', voice], check=True)
wav_out(os.path.join(HERE, 'sfx.wav'), sfx[:N])

# music: starts 51.36 s before the end, soft under speech (0.09), rises after the speech (+0.6/s to 0.9), 2 s fade in
MS = max(0.0, TOTAL - 51.36); SL = SPEECH_END - MS
vol = f"if(lt(t,{SL:.3f}),0.09,min(0.9,0.09+(t-{SL:.3f})*0.6))"
out = os.path.join(HERE, 'mix_v5.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', voice, '-i', os.path.join(HERE, 'sfx.wav'), '-i', TRACK, '-filter_complex',
    f"[0:a]volume=0dB[v];[1:a]volume=0dB[s];"
    f"[2:a]aresample=48000,atrim=0:{TOTAL - MS:.3f},volume='{vol}':eval=frame,afade=t=in:st=0:d=2,adelay={int(MS * 1000)}|{int(MS * 1000)}[m];"
    f"[v][s][m]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOTAL:.3f},"
    f"loudnorm=I=-14:TP=-2:LRA=11,aresample=192000,alimiter=limit=0.70:level=disabled,aresample=48000[a]",
    '-map', '[a]', '-ac', '2', out], check=True)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('\n'.join(l for l in r.splitlines() if any(k in l for k in ('I:', 'LRA:', 'Peak:'))))
print(f'music from {MS:.2f}s, speech ends {SPEECH_END:.2f}s, total {TOTAL:.2f}s')
