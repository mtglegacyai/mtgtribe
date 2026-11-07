"""Word-by-word captions that use the APPROVED script's words with the real audio's timing.

Whisper can mishear names (MTG, Hanke, Cannes). This script takes timing from faster-whisper and words from the
script MTG approved, so captions are always spelled right. Spoken forms can be shown differently on screen with
--replace (for example "MTG tribe dot com, slash group." shown as "mtgtribe.com/group.").

Usage:
  python3 scripts/align_captions.py narration.wav spoken-script.txt out.json [--replace replacements.json] [--model small.en]
  python3 scripts/align_captions.py voice/ spoken-script.txt out.json --sections timeline.json [--replace ...]
spoken-script.txt: exactly what the voice says (break tags are ignored).
--sections: the audio argument is a folder of section files (s01.wav, s02.wav, ...), the script has one line per section
  and timeline.json holds each section's start in seconds. Aligning section by section is more reliable: Whisper can
  skip or bunch words at the very start of a long file (it did on video 01's hook).
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
ap.add_argument('--sections')
a = ap.parse_args()

model = WhisperModel(a.model, device='cpu', compute_type='int8')


def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())


def align(audio_path, text, offset=0.0):
    """Script words with Whisper's timing for one audio file. Returns (captions, words matched directly)."""
    tokens = re.sub(r'<break[^>]*/>', ' ', text).split()
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio_path, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         check=True, capture_output=True).stdout
    audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    sn = [norm(t) for t in tokens]
    # Whisper with the script as a prompt is usually better, but on some files the prompt makes it skip most of the
    # audio (video 01, section 4). Run both ways and keep the transcript that matches more script words.
    best = None
    for prompt in (' '.join(tokens[:60]), None):
        segments, _ = model.transcribe(audio, language='en', word_timestamps=True, beam_size=5, initial_prompt=prompt)
        ws = [(w.word.strip(), w.start, w.end) for s in segments for w in s.words]
        m = difflib.SequenceMatcher(None, sn, [norm(w[0]) for w in ws], autojunk=False)
        score = sum(b.size for b in m.get_matching_blocks())
        if best is None or score > best[0]:
            best = (score, ws, m)
    _, words, sm = best
    times = [None] * len(tokens)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
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
    matched = sum(b.size for b in sm.get_matching_blocks())
    return [{'text': tok, 'start': t[0] + offset, 'end': t[1] + offset} for tok, t in zip(tokens, times)], matched, len(tokens)


script = open(a.script, encoding='utf-8').read()
if a.sections:
    import os
    starts = json.load(open(a.sections, encoding='utf-8'))['starts']
    lines = [ln for ln in script.splitlines() if ln.strip()]
    files = sorted(f for f in os.listdir(a.audio) if f.endswith('.wav'))
    if not (len(lines) == len(files) == len(starts)):
        raise SystemExit(f'{len(lines)} script lines, {len(files)} section files, {len(starts)} starts: they must match')
    caps, matched, total = [], 0, 0
    for line, f, st in zip(lines, files, starts):
        c, m, n = align(os.path.join(a.audio, f), line, st)
        caps += c
        matched += m
        total += n
else:
    caps, matched, total = align(a.audio, script)

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
print(f'{len(result)} caption words -> {a.out} ({matched} of {total} script words matched the audio directly)')
