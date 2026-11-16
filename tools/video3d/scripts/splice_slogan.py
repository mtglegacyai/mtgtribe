"""Put MTG's approved slogan (public/voice-bank/slogan.wav: his normal voice, approved 16 November 2026) at the end of a video's voice.

Run it after voice_timing.py and before make_cues.py:
  python3 scripts/splice_slogan.py public/videos/NN [--bank public/voice-bank/slogan] [--gap 0.5]
The script still sends "Let's Get This Crypto!" to HeyGen (so "Your Digital Architect." keeps its natural ending);
this replaces those four spoken words with the banked take, `--gap` seconds after the word before them, and rewrites
voice/s01.wav, words.json, captions.json and timeline.json. Running it twice is safe (it replaces the last four words).
"""
import argparse, json, os, re, wave
import numpy as np

SR = 48000
ap = argparse.ArgumentParser()
ap.add_argument('dir'); ap.add_argument('--bank', default='public/voice-bank/slogan'); ap.add_argument('--gap', type=float, default=0.5)
a = ap.parse_args()

norm = lambda s: re.sub(r"[^\w']", '', s).lower()
W = json.load(open(os.path.join(a.dir, 'words.json')))
words = W['words']
assert [norm(w['text']) for w in words[-4:]] == ["let's", 'get', 'this', 'crypto'], [w['text'] for w in words[-4:]]
before = words[-5]
bank = json.load(open(a.bank + '.json'))

def read(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

voice = read(os.path.join(a.dir, 'voice', 's01.wav'))
take = read(a.bank + '.wav')
cut = int((before['end'] + 0.04) * SR)
fade = int(0.03 * SR)
head = voice[:cut].astype(np.float32)
head[-fade:] *= np.linspace(1, 0, fade)
start = before['end'] + a.gap
y = np.concatenate([head, np.zeros(int(start * SR) - cut, np.float32), take.astype(np.float32)])
with wave.open(os.path.join(a.dir, 'voice', 's01.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
total = round(len(y) / SR, 4)

new = [{'text': o['text'], 'start': round(start + b['start'], 3), 'end': round(start + b['end'], 3)} for o, b in zip(words[-4:], bank['words'])]
W['words'] = words[:-4] + new
W['duration'] = total; W['slogan'] = os.path.basename(a.bank)
json.dump(W, open(os.path.join(a.dir, 'words.json'), 'w'), indent=0)

caps = json.load(open(os.path.join(a.dir, 'captions.json')))
first = round(words[-4]['start'] * 1000)
caps = [c for c in caps if c['startMs'] < first]
for w in new:
    sm, em = round(w['start'] * 1000), round(w['end'] * 1000)
    caps.append({'text': ' ' + w['text'], 'startMs': sm, 'endMs': em, 'timestampMs': (sm + em) // 2, 'confidence': None})
json.dump(caps, open(os.path.join(a.dir, 'captions.json'), 'w'), indent=1)
json.dump({'gap': 0, 'durations': [total], 'starts': [0.0], 'total': total}, open(os.path.join(a.dir, 'timeline.json'), 'w'), indent=1)
print(f'slogan {os.path.basename(a.bank)} at {start:.2f} s, ends {new[-1]["end"]:.2f} s; voice now {total:.2f} s')
