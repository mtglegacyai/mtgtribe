# One mix for every MTG video (MTG, 8 Nov 2026: consistency with the 9:09 sign-up training): his voice at -16 LUFS,
# the training's four synthesised sound effects (whoosh on scene changes, tick on list items, pop on engagement,
# click on taps) at the training's level relative to the voice, never ducked, and the full 51.36 s closing track
# "They Call Me MTG" ending on the final frame, soft under speech. Two-pass loudnorm to -14 LUFS, true peak -2.8 dB.
# Usage: python3 mix_consistent.py <dir>   (reads voice.wav, mixcues.json, kitcues.json, sfx_body.json)
import json, os, re, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mtg_ending as ME
D = sys.argv[1]; SR = 48000
MC = json.load(open(os.path.join(D, 'mixcues.json'))); K = json.load(open(os.path.join(D, 'kitcues.json')))
BODY = json.load(open(os.path.join(D, 'sfx_body.json')))
# The closing track (banked on branch jetup-video-work: jetup-work/audio/they-call-me-mtg-closing-track.mp3).
# Set MTG_TRACK to a local copy; the old path is kept as the fallback for the session that made the first videos.
TRACK = os.environ.get('MTG_TRACK') or '/tmp/claude-0/-home-user-mtgtribe/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad/promo/track.mp3'
T = K['T']; N = int(round(T * SR))
def ff_read(path, ch, af=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', path] + (['-af', af] if af else []) + ['-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, ch).copy()
def write(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
def lufs(x):
    p = os.path.join(D, '_m.wav'); write(p, x if x.ndim == 2 else np.stack([x, x], 1))
    out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])
vf = ('highpass=f=75,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=2.5,'
      'equalizer=f=9500:t=h:w=0.7:g=1.5,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=140:makeup=2,deesser=i=0.25')
voice = ff_read(os.path.join(D, 'voice.wav'), 1, vf)[:, 0]; voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
voice *= 10 ** ((-16 - lufs(voice)) / 20)
mask = np.zeros(N)
for a, b in MC['spans']: mask[max(0, int((a - .12) * SR)):int((b + .2) * SR)] = 1
k = int(.25 * SR); ker = np.hanning(2 * k + 1); ker /= ker.sum(); n2 = 1 << (N + len(ker) - 2).bit_length()
duck = np.fft.irfft(np.fft.rfft(mask, n2) * np.fft.rfft(ker, n2), n2)[k:k + N]
trk = ff_read(TRACK, 2); off = len(trk) - N
trk = trk[off:] if off >= 0 else np.pad(trk, ((-off, 0), (0, 0)))
trk *= 10 ** ((-17 - lufs(trk)) / 20)
t0 = max(0, -off) / SR
trk *= ((1 - .72 * duck) * np.clip((np.arange(N) / SR - t0) / .6, 0, 1))[:, None]
# sound effects: the training's bank, body events + the signature ending's events
bank = ME.sfx_bank(SR); E = ME.Ending(K['cues'], K['orient'], K.get('nxt'), K.get('links', True))
ev = {kind: list(BODY.get(kind, [])) + list(E.sfx().get(kind, [])) for kind in ('whoosh', 'tick', 'pop', 'click')}
sfx = np.zeros(N, np.float32); cnt = {}
for kind, ts in ev.items():
    last = -9
    for tt in sorted(ts):
        if tt - last < (0.35 if kind == 'whoosh' else 0.06): continue        # never stack the same sound
        s = bank[kind]().astype(np.float32) * ME.SFX_GAIN_AT_MINUS16; a = int(tt * SR)
        if 0 <= a < N: sfx[a:a + len(s)] += s[:N - a]; last = tt; cnt[kind] = cnt.get(kind, 0) + 1
mix = voice[:, None] * np.ones((1, 2)) + trk + sfx[:, None]
mix[-int(.08 * SR):] *= np.linspace(1, 0, int(.08 * SR))[:, None]
write(os.path.join(D, 'mix_raw.wav'), mix)
p1 = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(D, 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-2.8:LRA=11:print_format=json',
                     '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-2.8:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(D, 'mix_raw.wav'), '-af', af, '-ar', str(SR), os.path.join(D, 'mix.wav')], check=True)
out = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', os.path.join(D, 'mix.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print(D, 'mix.wav', re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1], 'LUFS, true peak', re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)[-1], 'dBFS,',
      round(N / SR, 2), 's; track from', round(t0, 2), 's; sfx', cnt)
