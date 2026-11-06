# Verify every word of a paused take: align breaks to real silences, then force-align each chunk's words.
import json, re, sys, subprocess, numpy as np
from pocketsphinx import Decoder
from align import align
SUB = {'done': 'done', 'jet': 'jet', 'binance': 'buy nance', 'ds': 'dees', 'ethereum': 'a theory um', 'lowercase': 'lower case', 'luno': 'loo no',
       'stablecoins': 'stable coins', 'syncing': 'sinking', 'uppercase': 'upper case', 'valr': 'valor', 'authorised': 'authorized', 'copyx': 'copy x', 'jetup': 'jet up', "jetup's": "jet up's", 'metatrader': 'meta trader',
       'mtg': 'm t g', "tag's": 'tags', "markets'": 'markets'}
def norm_words(ws):
    out = []
    for w in ws:
        w = re.sub(r"[^a-z'\-]", '', w.lower()).strip("'")
        w = SUB.get(w, w)
        out += [p for p in re.split(r'[\s\-]+', w) if p]
    return out
def fa(pcm16k, words):
    d = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
    d.set_align_text(' '.join(words))
    d.start_utt(); d.process_raw(pcm16k, full_utt=True); d.end_utt()
    segs = d.seg()
    return None if segs is None else [(s.word, s.start_frame / 100, (s.end_frame + 1) / 100) for s in segs]
def run(name):
    seq, a, e, R, B, match = align(name)
    pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', f'{name}_raw.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
    dur = len(pcm) / 32000
    # chunk boundaries in real audio: only at matched breaks
    cuts = [(-1, 0.0, 0.0)]   # (break seq index, silence start, silence end)
    for bi, i in enumerate(B):
        if bi in match: cuts.append((i, R[match[bi]][0], R[match[bi]][1]))
    cuts.append((len(seq), dur, dur))
    results, problems = [], []
    for k in range(len(cuts) - 1):
        i0, p_start, s_end = cuts[k]; i1, s_start, n_end = cuts[k + 1]
        words = [w['word'] for w in seq[i0 + 1:i1] if not w['word'].startswith('<break')]
        nw = norm_words(words)
        t0, t1 = max(0, min(s_end - 0.05, (p_start + s_end) / 2)), min(dur, max(s_start + 0.05, (s_start + n_end) / 2))
        seg = fa(pcm[int(t0 * 16000) * 2:int(t1 * 16000) * 2], nw)
        for dt0, dt1 in ((0, 0.3), (0.15, 0.3), (0.3, 0.5)):   # retry with a wider window (HeyGen Voice tails run into the pause)
            if seg is not None: break
            t0, t1 = max(0, t0 - dt0), min(dur, t1 + dt1)
            seg = fa(pcm[int(t0 * 16000) * 2:int(t1 * 16000) * 2], nw)
        if seg is None:
            problems.append(('ALIGN FAIL', round(t0, 2), ' '.join(words))); continue
        ws = [(re.sub(r'\(\d+\)$', '', w), t0 + s, t0 + e) for w, s, e in seg if w not in ('<sil>', '<s>', '</s>', '[NOISE]')]
        for w, s, e in ws:
            if e - s < 0.075 and w not in ('a', 'the', 'to', 'in', 'an', 'of', 'i', 'it', 'at', 'on', 'or', 'as'):
                problems.append(('SHORT', round(s, 2), w, round(e - s, 3), ' '.join(words)[:60]))
        results.append(dict(text=words, t0=t0, t1=t1, aligned=ws))
    json.dump(dict(chunks=results, silences=R, breaks=B, match={str(k): v for k, v in match.items()}), open(f'{name}_check.json', 'w'))
    print(f'{name}: {len(cuts)-1} chunks, {len(problems)} flags')
    for p in problems: print('   ', p)
if __name__ == '__main__':
    for n in sys.argv[1:]: run(n)
