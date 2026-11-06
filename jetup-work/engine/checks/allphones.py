# Bilabial (m/b/p) times across the whole narration: per-sentence phone alignment of voice_v3.wav.
import json, subprocess, numpy as np
from pocketsphinx import Decoder
from check import norm_words
W = json.load(open('voice_v3_words.json'))['words']
pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', 'voice_v3.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
sents, cur = [], []
for w in W:
    cur.append(w)
    if w['word'][-1] in '.?!,:' and not (len(w['word']) == 2 and w['word'][0].isupper()): sents.append(cur); cur = []
if cur: sents.append(cur)
out, fails = [], 0
for i, s in enumerate(sents):
    t0 = max(0, s[0]['start'] - 0.12); t1 = s[-1]['end'] + 0.12
    if i + 1 < len(sents): t1 = min(t1, sents[i + 1][0]['start'] - 0.01)
    if i > 0: t0 = max(t0, sents[i - 1][-1]['end'] + 0.01)
    seg = pcm[int(t0 * 16000) * 2:int(t1 * 16000) * 2]
    d = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
    d.set_align_text(' '.join(norm_words([w['word'] for w in s])))
    d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
    try:
        d.set_alignment(); d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
        for w in d.get_alignment():
            for p in w:
                if p.name in ('M', 'B', 'P'):
                    out.append((w.name, p.name, round(t0 + p.start / 100, 3), round(t0 + (p.start + p.duration) / 100, 3)))
    except Exception as e:
        fails += 1
json.dump(out, open('all_bilabials.json', 'w'))
print(len(sents), 'phrases,', len(out), 'm/b/p sounds,', fails, 'phrases failed')
