# Sentence-by-sentence forced alignment (pocketsphinx), cut at the real pauses, so one slip cannot spread.
import json, re, subprocess
from pocketsphinx import Decoder
S = json.load(open('invite_tts.json'))
disp = [w['word'] for w in S['word_timestamps'] if not w['word'].startswith('<')]
def spoken(w):
    w = re.sub(r'[^A-Za-z\']', '', w)
    return {'JetUP': ['jet', 'up'], 'MTG': ['m', 't', 'g']}.get(w, [w.lower()])
# cut at every sentence pause (break tags of 0.4 s or more), at its middle, shifted by HeyGen's measured lag (0.15 s)
TS = S['word_timestamps']; starts_i, cuts = [], []
di = -1
for j, w in enumerate(TS):
    if not w['word'].startswith('<'): di += 1; continue
    if re.search(r'time="0\.[3-9]s"', w['word']) and di >= 0:
        starts_i.append(di + 1); cuts.append(round((w['start'] + w['end']) / 2 + .15, 3))
idx = [0] + starts_i + [len(disp)]
bounds = [0.0] + cuts + [S['duration']]
pcm_all = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', 'invite_raw.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
words = []; FAILED = []
for k in range(len(idx) - 1):
    a, b = bounds[k], bounds[k + 1]
    seq = [(i, s) for i in range(idx[k], idx[k + 1]) for s in spoken(disp[i])]
    pcm = pcm_all[int(a * 16000) * 2:int(b * 16000) * 2]
    d = Decoder(samprate=16000, bestpath=False)
    d.set_align_text(' '.join(s for _, s in seq))
    d.start_utt(); d.process_raw(pcm, full_utt=True); d.end_utt()
    if d.seg() is None or d.hyp() is None:
        # fallback: HeyGen's own word times shifted by the median offset measured in the other sentences
        print('chunk', k, 'did not align, using offset HeyGen times'); FAILED.append(k); continue
    segs = [(re.sub(r'\(\d+\)$', '', s.word), a + s.start_frame / 100, a + s.end_frame / 100) for s in d.seg()
            if s.word not in ('<s>', '</s>', '<sil>', '[NOISE]')]
    assert [w for w, _, _ in segs] == [s for _, s in seq], (k, segs)
    out = {}
    for (i, s), (w, wa, wb) in zip(seq, segs):
        o = out.setdefault(i, {'w': disp[i], 'a': round(wa, 3), 'b': round(wb, 3)}); o['b'] = round(wb, 3)
    words += [out[i] for i in range(idx[k], idx[k + 1])]
if FAILED:
    import statistics
    ht = [w for w in S['word_timestamps'] if not w['word'].startswith('<')]
    got = {w['w'] + str(i): w for i, w in enumerate(words)}
    offs = []
    pos = {}
    j = 0
    for k in range(len(idx) - 1):
        if k in FAILED: continue
        for i in range(idx[k], idx[k + 1]):
            offs.append(words[j]['a'] - ht[i]['start']); pos[i] = words[j]; j += 1
    off = statistics.median(offs); print('median offset', round(off, 3))
    full = []
    for k in range(len(idx) - 1):
        for i in range(idx[k], idx[k + 1]):
            full.append(pos[i] if i in pos else {'w': disp[i], 'a': round(ht[i]['start'] + off, 3), 'b': round(ht[i]['end'] + off, 3), 'est': True})
    words = full
json.dump(words, open('invite_words.json', 'w'), indent=0)
print(' '.join(f"{w['w']}@{w['a']:.2f}" for w in words if w['w'] in ('Hi,', 'One:', 'Two:', 'Three:', 'Join', 'Send', 'Crypto!')))
