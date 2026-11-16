"""MTG's spoken slogan, "Let's Get This Crypto!", as one banked take that every video ends with (MTG, 16 November 2026).

MTG: the TTS slogan at the end of each script came out "too high ... take it down, make it deep, make it land harder.
This is a slogan, so it must feel like a slogan." Measured on video 11: his narration sits at about 126 Hz, but the
slogan jumped to about 240 to 270 Hz and rose at the end. So the slogan is recorded once, on its own, in his approved
voice (MTG Master Voice V3) with a HeyGen delivery tag ([deep voice], [slowly] ...), finished here (warmth, gentle
compression, a short room) and saved to public/voice-bank/. `splice_slogan.py` then puts it at the end of every video.

Usage:
  python3 scripts/make_slogan.py <take.wav> <words.json> <out name> [--from 0.30] [--ref public/videos/11/voice/s01.wav]
    words.json: [["Let's", start, end], ["Get", ...], ["This", ...], ["Crypto!", ...]] in seconds of the take
    writes public/voice-bank/<out name>.wav (48 kHz mono) and <out name>.json (word times in the new file)
"""
import argparse, json, os, subprocess, wave
import numpy as np

SR = 48000
ap = argparse.ArgumentParser()
ap.add_argument('take'); ap.add_argument('words'); ap.add_argument('name')
ap.add_argument('--from', dest='start', type=float, default=0.3, help='cut the take here (just before "Let\'s")')
ap.add_argument('--ref', default='public/videos/11/voice/s01.wav', help='narration to match the loudness to')
ap.add_argument('--lift', type=float, default=1.5, help='dB above the narration: a slogan sits a little forward')
a = ap.parse_args()

CHAIN = ','.join([
    'highpass=f=60',
    'bass=g=3:f=120:w=0.7',  # warmth and weight in the chest of the voice
    'equalizer=f=3000:t=q:w=1.2:g=1.5',  # a little presence so the words stay clear
    'acompressor=threshold=-22dB:ratio=3:attack=6:release=160:makeup=2',  # every word lands at full strength
    'aecho=0.85:0.5:32|64:0.07|0.04',  # a short, warm room: a stage, not an echo
])

def load(path, filt=None, start=0.0):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', path]
    if filt: cmd += ['-af', filt]
    cmd += ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).copy()

def active_rms(x):
    fr = int(0.05 * SR)
    r = np.array([np.sqrt((x[i:i + fr] ** 2).mean()) for i in range(0, len(x) - fr, fr)])
    loud = r[r > r.max() * 0.15]
    return float(np.sqrt((loud ** 2).mean()))

ref = load(a.ref)[: int(50 * SR)]
target = active_rms(ref) * 10 ** (a.lift / 20)
gain_db = 20 * np.log10(target / active_rms(load(a.take, CHAIN, a.start)))
for _ in range(3):  # a gentle limiter holds the peaks at -2 dBFS, so nudge the gain until the words sit at the target
    y = load(a.take, f'{CHAIN},volume={gain_db:.2f}dB,alimiter=limit=0.79:attack=4:release=60:level=disabled', a.start)
    gain_db += 20 * np.log10(target / active_rms(y))
gain = 10 ** (gain_db / 20)
fade = int(0.012 * SR)
y[:fade] *= np.linspace(0, 1, fade)
y[-int(0.08 * SR):] *= np.linspace(1, 0, int(0.08 * SR))
os.makedirs('public/voice-bank', exist_ok=True)
out = os.path.join('public/voice-bank', a.name)
with wave.open(out + '.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
words = [{'text': t, 'start': round(s - a.start, 3), 'end': round(e - a.start, 3)} for t, s, e in json.load(open(a.words))]
json.dump({'take': os.path.basename(a.take), 'duration': round(len(y) / SR, 3), 'words': words}, open(out + '.json', 'w'), indent=1)
print(f'{out}.wav: {len(y) / SR:.2f} s, gain {20 * np.log10(gain):+.1f} dB, words {[w["text"] for w in words]}')
