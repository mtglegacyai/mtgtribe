# Forced-align the orca takes sentence by sentence (windows from HeyGen word timestamps), same method as v3.
import json, re, sys, subprocess
from pocketsphinx import Decoder
SUB = {'authorised': 'authorized', 'copyx': 'copy x', 'jetup': 'jet up', "jetup's": "jet up's", 'metatrader': 'meta trader',
       'mtg': 'm t g', "tag's": 'tags', "markets'": 'markets'}

def toks(w):
    w = re.sub(r"[^a-z'\-]", '', w.lower()).strip("'")
    w = SUB.get(w, w)
    return [p for p in re.split(r'[\s\-]+', w) if p]

def fa(pcm, words):
    d = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
    d.set_align_text(' '.join(words))
    d.start_utt(); d.process_raw(pcm, full_utt=True); d.end_utt()
    s = d.seg()
    return None if s is None else [(re.sub(r'\(\d+\)$', '', x.word), x.start_frame / 100, (x.end_frame + 1) / 100) for x in s]

def run(name):
    J = json.load(open(f'{name}_tts.json'))
    W = [w for w in J['word_timestamps'] if w['word'] not in ('<start>', '<end>')]
    pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', f'{name}_raw.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
    dur = len(pcm) / 32000
    sents, cur = [], []
    for i, w in enumerate(W):
        cur.append(i)
        if w['word'][-1] in '.?!' or (w['word'][-1] in ',:;' and len(cur) >= 9): sents.append(cur); cur = []
    if cur: sents.append(cur)
    out = [None] * len(W); fails = 0
    for k, s in enumerate(sents):
        a = W[s[0]]['start']; b = W[s[-1]]['end']
        lo = (W[sents[k - 1][-1]]['end'] + a) / 2 if k else 0.0
        hi = (b + W[sents[k + 1][0]]['start']) / 2 if k + 1 < len(sents) else dur
        tk, owner = [], []
        for i in s:
            t = toks(W[i]['word']); tk += t; owner += [i] * len(t)
        seg = None
        for pad_lo, pad_hi in ((0, 0), (0.12, 0.15), (0.25, 0.3)):
            t0, t1 = max(0, lo - pad_lo), min(dur, hi + pad_hi)
            seg = fa(pcm[int(t0 * 16000) * 2:int(t1 * 16000) * 2], tk)
            if seg is not None: break
        ws = [x for x in (seg or []) if x[0] not in ('<sil>', '<s>', '</s>', '[NOISE]', '+NSN+', '+SPN+')]
        if seg is None or len(ws) != len(tk):
            fails += 1
            for i in s: out[i] = dict(word=W[i]['word'], start=W[i]['start'], end=W[i]['end'], src='heygen')
            continue
        for (wd, st, en), i in zip(ws, owner):
            st, en = t0 + st, t0 + en
            if out[i] is None: out[i] = dict(word=W[i]['word'], start=round(st, 3), end=round(en, 3), src='fa')
            else: out[i]['end'] = round(en, 3)
    json.dump(dict(duration=dur, words=out), open(f'{name}_words.json', 'w'), indent=0)
    dev = [abs(o['start'] - w['start']) for o, w in zip(out, W) if o['src'] == 'fa']
    print(f'{name}: {len(sents)} chunks, {fails} fell back to HeyGen times, median |fa - heygen| start {sorted(dev)[len(dev)//2]:.3f} s, max {max(dev):.3f}')

if __name__ == '__main__':
    for n in sys.argv[1:]: run(n)
