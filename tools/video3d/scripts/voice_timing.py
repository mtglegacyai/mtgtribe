#!/usr/bin/env python3
"""Turn one HeyGen speech result into everything a video needs (HeyGen Voice 1, since 10 November 2026).

HeyGen's instant voices no longer accept <break> tags, so pauses are added here, for free: wherever the script has a
paragraph break (a line with only "//" between paragraphs), the natural gap is stretched to at least --pause seconds
by inserting silence, and every later timing is shifted. "// 1.1" asks for at least 1.1 seconds at that one spot.

  python3 scripts/voice_timing.py <result.json> <voice.wav> <script.txt> <out dir> [--pause 0.65]

result.json: the tool result (audio_url, duration, original_characters, original_words).
script.txt: the exact text sent, with a line "//" wherever a longer pause belongs (the "//" lines were NOT sent).
Writes into <out dir>: voice/s01.wav (48 kHz mono), words.json (one entry per script word, punctuation kept),
captions.json, timeline.json. Caption replacements (spoken words to digits) come from <out dir>/replacements.json:
[["twenty-one million", "21 million"], ...].
"""
import argparse, json, os, re, subprocess, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('result'); ap.add_argument('wav'); ap.add_argument('script'); ap.add_argument('out')
ap.add_argument('--pause', type=float, default=0.65)
a = ap.parse_args()

res = json.load(open(a.result))
chars = res['original_characters']
raw = open(a.script).read()
# a line "//" asks for the default pause; "// 1.1" asks for a pause of at least 1.1 seconds at that spot
parts = re.split(r'^\s*//\s*([\d.]*)\s*$', raw, flags=re.M)
paras = [re.sub(r'\s+', ' ', p).strip() for p in parts[0::2]]
want = [float(v) if v else a.pause for v in parts[1::2]]
assert all(paras), 'empty paragraph between two // lines'
text = ' '.join(paras)
sent = ''.join(c['text'] for c in chars)
assert sent == text, 'script.txt (without the // lines) must equal the text that was sent:\n' + sent[:80] + '\n' + text[:80]

# words from the character timings: start of the first letter, end of the last letter or digit
words, i = [], 0
for tok in text.split(' '):
    j = i + len(tok)
    seg = chars[i:j]
    core = [c for c in seg if re.match(r"[\w']", c['text'])] or seg
    words.append({'text': tok, 'start': core[0]['start_time'], 'end': core[-1]['end_time']})
    i = j + 1

# where the paragraphs end (word index of each paragraph's last word, except the final one)
breaks, n = [], 0
for p in paras[:-1]:
    n += len(p.split(' '))
    breaks.append(n - 1)

SR = 48000
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.wav, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, dtype='<i2')
out, cursor, shift, added = [], 0, 0.0, []
for b, target in zip(breaks, want):
    gap = words[b + 1]['start'] - words[b]['end']
    extra = max(0.0, target - gap)
    cut = int(((words[b]['end'] + words[b + 1]['start']) / 2) * SR)
    out.append(x[cursor:cut]); out.append(np.zeros(int(extra * SR), dtype='<i2')); cursor = cut
    added.append(round(extra, 3))
    for w in words[b + 1:]:
        w['start'] += extra; w['end'] += extra
out.append(x[cursor:])
y = np.concatenate(out)
os.makedirs(os.path.join(a.out, 'voice'), exist_ok=True)
with wave.open(os.path.join(a.out, 'voice', 's01.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
total = len(y) / SR

for w in words:
    w['start'] = round(w['start'], 3); w['end'] = round(w['end'], 3)
json.dump({'voice': res.get('voice'), 'request': res.get('audio_url', '').split('id=')[-1].split('.')[0], 'duration': round(total, 4),
           'pauses_added': added, 'words': words}, open(os.path.join(a.out, 'words.json'), 'w'), indent=0)

# captions: script words with punctuation; replacements merge spoken numbers and addresses
rp = os.path.join(a.out, 'replacements.json')
repl = json.load(open(rp)) if os.path.exists(rp) else []
norm = lambda s: re.sub(r"[^\w']", '', s).lower()
caps, k = [], 0
while k < len(words):
    hit = None
    for src, dst in repl:
        toks = src.split(' ')
        if [norm(w['text']) for w in words[k:k + len(toks)]] == [norm(t) for t in toks]:
            tail = re.search(r"[^\w']+$", words[k + len(toks) - 1]['text'])
            hit = (dst + (tail.group(0) if tail and not dst.endswith(tail.group(0)) else ''), len(toks)); break
    if hit:
        caps.append([hit[0], words[k]['start'], words[k + hit[1] - 1]['end']]); k += hit[1]
    else:
        caps.append([words[k]['text'], words[k]['start'], words[k]['end']]); k += 1
cj = []
for n_, (t, s, e) in enumerate(caps):
    sm = round(s * 1000); em = max(sm + 1, round(e * 1000))
    cj.append({'text': (' ' if n_ else '') + t, 'startMs': sm, 'endMs': em, 'timestampMs': (sm + em) // 2, 'confidence': None})
json.dump(cj, open(os.path.join(a.out, 'captions.json'), 'w'), indent=1)
json.dump({'gap': 0, 'durations': [round(total, 4)], 'starts': [0.0], 'total': round(total, 4)}, open(os.path.join(a.out, 'timeline.json'), 'w'), indent=1)
print(f'{len(words)} words, {total:.2f} s, pauses added {added}, {len(cj)} captions')
