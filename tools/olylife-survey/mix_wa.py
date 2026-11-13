# Mix for the 60-second WhatsApp cut (wa/): as mix.py, but videos of 60 s or less get only the closing track's last
# line ("Let's get this crypto, wherever I go!", 48.38 s to the end) right after MTG's last word (MTG, 8 Nov 2026).
# Based on mix.py, the mix for the OlyLife survey video, following tools/video-signature/mix_consistent.py (MTG's one mix for every video):
# voice at -16 LUFS with the same voice chain, the training's four synthesised sounds at the same level, never ducked,
# and the full 51.36 s closing track "They Call Me MTG" ending on the last frame, soft under speech.
# Two-pass loudnorm to -14 LUFS, true peak -2.8 dB. Lines are levelled gently first (V3 take and banked V2 lines).
import json, os, re, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
D0 = D; D = f'{D0}/wa'
LO = json.load(open(f'{D}/lines_out.json')); SFX = json.load(open(f'{D}/sfx.json'))['sfx']
T = LO['T']; N = int(round(T * SR)); TRACK = f'{D0}/audio/track.mp3'

def ff_read(path, ch, af=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', path] + (['-af', af] if af else []) + ['-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, ch).copy()
def write(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
def lufs(x):
    p = f'{D}/_m.wav'; write(p, x if x.ndim == 2 else np.stack([x, x], 1))
    out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])

# ---- the training's four sound effects (verbatim from mtg_ending.sfx_bank)
def sfx_bank(SR=48000, seed=7):
    rng = np.random.default_rng(seed)
    def whoosh():
        n = int(0.5 * SR); x = rng.standard_normal(n).astype(np.float32); o = np.zeros(n, np.float32)
        for k in range(10):
            a, b = k * n // 10, (k + 1) * n // 10; fc = 500 + 3500 * (k / 9)
            o[a:b] = sosfilt(butter(2, [fc * 0.6, fc * 1.4], btype='band', fs=SR, output='sos'), x)[a:b]
        o *= np.sin(np.pi * np.linspace(0, 1, n)) ** 2; return o / np.abs(o).max() * 0.08
    def tick():
        n = int(0.08 * SR); tt = np.arange(n) / SR
        x = (np.sin(2 * np.pi * 1760 * tt) + 0.4 * np.sin(2 * np.pi * 3520 * tt)) * np.exp(-tt * 55); return x / np.abs(x).max() * 0.07
    def pop():
        n = int(0.12 * SR); tt = np.arange(n) / SR; f = 380 + 700 * tt / tt[-1]
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30); return x / np.abs(x).max() * 0.12
    def click():
        n = int(0.05 * SR); tt = np.arange(n) / SR
        x = rng.standard_normal(n) * np.exp(-tt * 180) + 0.6 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 120)
        x = sosfilt(butter(2, [900, 6000], btype='band', fs=SR, output='sos'), x); return x / np.abs(x).max() * 0.10
    return dict(whoosh=whoosh, tick=tick, pop=pop, click=click)
SFX_GAIN_AT_MINUS16 = 10 ** (3.6 / 20)

# ---- voice: gentle per-line levelling toward the V3 take's average, then the standard voice chain at -16 LUFS
raw = ff_read(f'{D}/voice.wav', 1)[:, 0]; raw = np.pad(raw, (0, max(0, N - len(raw))))[:N]
TARGET = -17.6
for l in LO['lines']:
    a, b = int(l['a'] * SR), int(l['b'] * SR); seg = raw[a:b]
    g = float(np.clip(0.6 * (TARGET - lufs(seg)), -1.5, 2.0)); raw[a:b] = seg * 10 ** (g / 20)
write(f'{D}/voice_lev.wav', raw[:, None])
vf = ('highpass=f=75,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=2.5,'
      'equalizer=f=9500:t=h:w=0.7:g=1.5,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=140:makeup=2,deesser=i=0.25')
voice = ff_read(f'{D}/voice_lev.wav', 1, vf)[:, 0]; voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
voice *= 10 ** ((-16 - lufs(voice)) / 20)

# ---- closing track: only its last line, right after MTG's last word, ending on the last frame
trk = ff_read(TRACK, 2); g = 10 ** ((-17 - lufs(trk)) / 20)
line = trk[int(48.38 * SR):] * g; t0 = LO['track_at']; a = int(t0 * SR)
line = line[:N - a]; fade = int(.03 * SR); line[:fade] *= np.linspace(0, 1, fade)[:, None]
trk = np.zeros((N, 2), np.float32); trk[a:a + len(line)] = line

# ---- sound effects
bank = sfx_bank(SR); sfx = np.zeros(N, np.float32); cnt = {}
for kind in ('whoosh', 'tick', 'pop', 'click'):
    last = -9
    for tt in sorted(SFX.get(kind, [])):
        if tt - last < (0.35 if kind == 'whoosh' else 0.06): continue
        s = bank[kind]().astype(np.float32) * SFX_GAIN_AT_MINUS16; a = int(tt * SR)
        if 0 <= a < N: sfx[a:a + len(s)] += s[:N - a]; last = tt; cnt[kind] = cnt.get(kind, 0) + 1
mix = voice[:, None] * np.ones((1, 2)) + trk + sfx[:, None]
mix[-int(.08 * SR):] *= np.linspace(1, 0, int(.08 * SR))[:, None]
write(f'{D}/mix_raw.wav', mix)
p1 = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', f'{D}/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.8:LRA=11:print_format=json', '-f', 'null', '-'],
                    capture_output=True, text=True).stderr
m = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-2.8:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/mix_raw.wav', '-af', af, '-ar', str(SR), f'{D}/mix.wav'], check=True)
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', f'{D}/mix.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('mix.wav', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS,',
      round(N / SR, 2), 's; track from', round(t0, 2), 's; sfx', cnt)
