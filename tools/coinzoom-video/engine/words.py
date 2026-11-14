# Word times for every line (relative to the line's own start): HeyGen's for the new lines (+0.10 s: HeyGen's times run
# about 0.1 s ahead of the audio, measured against speech-to-text on this take), the explainer #4 pack's for its lines,
# speech-to-text for the four lines cut from the older takes (mapped onto the exact text, proportional fallback).
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stt import load16
from faster_whisper import WhisperModel
HERE = os.path.abspath(sys.argv[1])          # the video folder (python3 words.py <video dir>)
L = json.load(open(os.path.join(HERE, 'lines.json'))); WD = json.load(open(os.path.join(HERE, 'words_partial.json')))
ALIGN = 0.10
for k, v in L.items():
    if str(v.get('src', '')).startswith('cz'):          # the new V3 take of this video
        WD[k] = [dict(w=w['w'], a=round(min(w['a'] + ALIGN, v['dur']), 3), b=round(min(w['b'] + ALIGN, v['dur']), 3)) for w in WD[k]]
m = WhisperModel('small.en', device='cpu', compute_type='int8')
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
for k in ['hi', 'n_thanks', 'takeyour', 'pause']:
    toks = L[k]['text'].split()
    segs, _ = m.transcribe(load16(os.path.join(HERE, 'lines', L[k]['file'])), beam_size=5, word_timestamps=True)
    ws = [w for s in segs for w in s.words]
    if [norm(w.word) for w in ws] == [norm(t) for t in toks]:
        WD[k] = [dict(w=t, a=round(w.start, 3), b=round(w.end, 3)) for t, w in zip(toks, ws)]; how = 'stt'
    else:
        a0, b0 = (ws[0].start, ws[-1].end) if ws else (0.05, L[k]['dur'] - 0.05)
        n = sum(len(t) for t in toks); acc = 0; out = []
        for t in toks:
            a = a0 + (b0 - a0) * acc / n; acc += len(t); out.append(dict(w=t, a=round(a, 3), b=round(a0 + (b0 - a0) * acc / n, 3)))
        WD[k] = out; how = 'proportional (heard: ' + ' '.join(w.word for w in ws) + ')'
    print(k, how)
json.dump(WD, open(os.path.join(HERE, 'words.json'), 'w'), indent=1)
print(len(WD), 'lines with word times')
