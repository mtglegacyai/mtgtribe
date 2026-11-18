# Composite MTG's signature ending (mtg_ending.py) onto stage frames.
#   python3 compose_kit.py test <dir> <frames_in_dir>        -> composites every t*.jpg test still (names carry the time)
#   python3 compose_kit.py frames <dir> <frames_dir> [jobs]  -> composites the ending onto f#####.jpg in place (kit range only)
import json, os, sys, re, glob
from multiprocessing import Pool
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mtg_ending as ME

def load(d):
    K = json.load(open(os.path.join(d, 'kitcues.json')))
    return K, ME.Ending(K['cues'], K['orient'], K.get('nxt'), K.get('links', True))

def comp_file(args):
    d, path, t, out = args
    _, E = _EN[d]
    im = Image.open(path).convert('RGBA'); ov = E.overlay(t)
    im.alpha_composite(ov); im.convert('RGB').save(out, quality=94)
    return out

_EN = {}
def init(d): _EN[d] = load(d)

if __name__ == '__main__':
    mode, d, fdir = sys.argv[1], sys.argv[2], sys.argv[3]
    K, E = load(d); fps = K['fps']
    if mode == 'test':
        jobs = []
        for p in sorted(glob.glob(os.path.join(fdir, 't*.jpg'))):
            t = float(re.findall(r't([\d.]+)\.jpg', os.path.basename(p))[0])
            jobs.append((d, p, t, os.path.join(fdir, 'k' + os.path.basename(p)[1:])))
    else:
        f0 = int(np.floor(E.start * fps)); f1 = int(round(K['T'] * fps))
        jobs = [(d, os.path.join(fdir, f'f{f:05d}.jpg'), f / fps, os.path.join(fdir, f'f{f:05d}.jpg')) for f in range(f0, f1)]
        missing = [j[1] for j in jobs if not os.path.exists(j[1])]
        if missing: raise SystemExit(f'{len(missing)} frames missing, first {missing[0]}')
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    with Pool(n, initializer=init, initargs=(d,)) as pool:
        for i, _ in enumerate(pool.imap(comp_file, jobs, chunksize=8)):
            if i % 300 == 0: print('composited', i, '/', len(jobs), flush=True)
    print('done', len(jobs), 'frames')
