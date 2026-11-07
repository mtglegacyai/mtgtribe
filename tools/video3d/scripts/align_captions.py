"""Word-by-word captions that use the APPROVED script's words with the real audio's timing.

Whisper can mishear names (MTG, Hanke, Cannes). This script takes timing from faster-whisper and words from the
script MTG approved, so captions are always spelled right. Spoken forms can be shown differently on screen with
--replace (for example "MTG tribe dot com, slash group." shown as "mtgtribe.com/group.").

Usage:
  python3 scripts/align_captions.py narration.wav spoken-script.txt out.json [--replace replacements.json] [--model small.en]
spoken-script.txt: exactly what the voice says (break tags are ignored).
replacements.json: [["spoken words as in the script", "how they appear on screen"], ...]
"""
import argparse
import difflib
import json
import re
import subprocess

import numpy as np
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument('audio')
ap.add_argument('script')
ap.add_argument('out')
ap.add_argument('--replace')
ap.add_argument('--model', default='small.en')
a = ap.parse_args()

text = re.sub(r'<break[^>]*/>', ' ', open(a.script, encoding='utf-8').read())
tokens = text.split()

pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.audio, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
model = WhisperModel(a.model, device='cpu', compute_type='int8')
segments, _ = model.transcribe(audio, language='en', word_timestamps=True, beam_size=5,
                               initial_prompt=' '.join(tokens[:60]))
words = [(w.word.strip(), w.start, w.end) for s in segments for w in s.words]


def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())


sn = [norm(t) for t in tokens]
wn = [norm(w[0]) for w in words]
times = [None] * len(tokens)
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sn, wn, autojunk=False).get_opcodes():
    if op == 'equal':
        for k in range(i2 - i1):
            times[i1 + k] = (words[j1 + k][1], words[j1 + k][2])
    elif op == 'replace':
        s, e = words[j1][1], words[j2 - 1][2]
        n = i2 - i1
        for k in range(n):
            times[i1 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)

# fill script words Whisper did not hear by interpolating between neighbours
for i, t in enumerate(times):
    if t is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev + 0.4)
        times[i] = (prev, max(prev + 0.05, min(nxt, prev + 0.4)))

caps = [{'text': tok, 'start': t[0], 'end': t[1]} for tok, t in zip(tokens, times)]

if a.replace:
    for spoken, shown in json.load(open(a.replace, encoding='utf-8')):
        sp = spoken.split()
        out, i = [], 0
        while i < len(caps):
            if [c['text'] for c in caps[i:i + len(sp)]] == sp:
                out.append({'text': shown, 'start': caps[i]['start'], 'end': caps[i + len(sp) - 1]['end']})
                i += len(sp)
            else:
                out.append(caps[i])
                i += 1
        caps = out

result = []
for i, c in enumerate(caps):
    s, e = round(c['start'] * 1000), max(round(c['start'] * 1000) + 1, round(c['end'] * 1000))
    result.append({'text': (' ' if i else '') + c['text'], 'startMs': s, 'endMs': e, 'timestampMs': (s + e) // 2,
                   'confidence': None})
json.dump(result, open(a.out, 'w', encoding='utf-8'), indent=1)
matched = sum(1 for op in difflib.SequenceMatcher(None, sn, wn, autojunk=False).get_matching_blocks() for _ in range(op.size))
print(f'{len(result)} caption words -> {a.out} ({matched} of {len(tokens)} script words matched the audio directly)')
