"""Word-level captions from a voice file, with faster-whisper (the same engine as tools/invite-horizontal).

Writes Remotion captions (Caption[] for @remotion/captions) straight away.

Setup once:  pip install faster-whisper   (ffmpeg must be installed too)
Usage:       python3 scripts/transcribe.py public/voice/my-voice.m4a public/captions/my-voice.json
Options:     --model small.en (default; base.en is faster, medium.en more accurate)
             --raw transcript.json   also keep the full faster-whisper output
The first run downloads the model from huggingface.co (small.en is about 480 MB).
Always read the captions back against the audio: names like MTG, ALTRUVA or JetUP can still be misheard.
"""
import argparse
import json
import os
import re
import subprocess

import numpy as np
from faster_whisper import WhisperModel

PROMPT = ('MTG, MusaTheGiant.com, Your Digital Architect, MTG TRIBE, mtgtribe.com, ALTRUVA, Bellver Affiliates, '
          'JetUP, TAG Markets, ClickBaitPays, Bitcoin Wealth, WhatsApp, TikTok, Crypto Regards. '
          "Let's Get This Crypto!")
DASHES = re.compile(r'\s*[\u2013\u2014]\s*')  # MTG's rule: no em or en dashes on screen

ap = argparse.ArgumentParser()
ap.add_argument('audio')
ap.add_argument('out')
ap.add_argument('--model', default='small.en')
ap.add_argument('--raw')
a = ap.parse_args()

# Decode with ffmpeg (any audio or video file) to 16 kHz mono, the format Whisper expects.
# This avoids PyAV version problems inside faster-whisper.
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.audio, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0

model = WhisperModel(a.model, device='cpu', compute_type='int8')
segments, _ = model.transcribe(audio, language='en', word_timestamps=True, beam_size=5, initial_prompt=PROMPT)

raw, captions = [], []
for seg in segments:
    words = [{'w': w.word, 's': round(w.start, 3), 'e': round(w.end, 3), 'p': round(w.probability, 3)} for w in seg.words]
    raw.append({'start': seg.start, 'end': seg.end, 'text': seg.text.strip(), 'words': words})
    print(f'{seg.start:7.2f} {seg.end:7.2f} {seg.text.strip()}', flush=True)
    for w in words:
        start, end = round(w['s'] * 1000), max(round(w['s'] * 1000) + 1, round(w['e'] * 1000))
        text = DASHES.sub(', ', w['w'])
        captions.append({'text': text, 'startMs': start, 'endMs': end,
                         'timestampMs': (start + end) // 2, 'confidence': w['p']})

if captions:
    captions[0]['text'] = captions[0]['text'].lstrip()
os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
with open(a.out, 'w') as f:
    json.dump(captions, f, indent=1)
if a.raw:
    with open(a.raw, 'w') as f:
        json.dump(raw, f, indent=1)

low = [c for c in captions if c['confidence'] < 0.6]
print(f'{len(captions)} words -> {a.out}')
if low:
    print('Check these words by ear (low confidence): ' +
          ', '.join(f'"{c["text"].strip()}" at {c["startMs"] / 1000:.2f}s' for c in low))
