# Privacy scan: OCR every second frame of the finished video (the window, where CoinZoom's screens show, x1.5, normal and
# inverted, two page modes; one OCR thread per worker, about 15 minutes) for card-like numbers, expiry dates, long numbers and the private patterns in ~/.tutorial-private-patterns.tsv
# (one "category<TAB>regex" per line: the demo card's own number fragments and name go there, never in the repository).
# Usage: python3 ocr_scan.py <video.mp4> <work dir>      Zero flags before MTG sees the video.
import io, json, os, re, subprocess, sys
from multiprocessing import Pool
from PIL import Image, ImageOps
V, D = sys.argv[1], sys.argv[2]; os.makedirs(D, exist_ok=True)
if not any(f.endswith('.jpg') for f in os.listdir(D)): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', V, '-vf', 'select=not(mod(n\\,2))', '-vsync', '0', '-q:v', '2', os.path.join(D, 'o%05d.jpg')], check=True)
PAT = [('card number', re.compile(r'\d{4}\s?\d{4}\s?\d{4}')), ('long number', re.compile(r'\d{9,}')),
       ('expiry', re.compile(r'\b(0[1-9]|1[0-2])\s?/\s?[2-3]\d\b'))]
pf = os.path.expanduser('~/.tutorial-private-patterns.tsv')
if os.path.exists(pf):
    for line in open(pf):
        if '\t' in line: k, r = line.rstrip('\n').split('\t', 1); PAT.append((k, re.compile(r, re.I)))
def png(img):
    b = io.BytesIO(); img.save(b, 'PNG'); return b.getvalue()
def scan(p):
    im = Image.open(p).convert('L'); hits = []
    for c in (im.crop((240, 112, 1680, 922)).resize((2160, 1215)),):
        for img in (c, ImageOps.invert(c)):
            for psm in ('6', '11'):
                out = subprocess.run(['tesseract', '-', '-', '--psm', psm], input=png(img), capture_output=True).stdout.decode(errors='ignore')
                hits += [(k, m if isinstance(m, str) else m[0]) for k, r in PAT for m in r.findall(out)]
    return os.path.basename(p), sorted(set(hits))
fs = sorted(os.path.join(D, f) for f in os.listdir(D) if f.endswith('.jpg'))
os.environ['OMP_THREAD_LIMIT'] = '1'                 # four workers, one OCR thread each (otherwise they fight for the cores)
res = []
with Pool(4) as pool:
    for i, r in enumerate(pool.imap(scan, fs, chunksize=4)):
        res.append(r)
        if i % 200 == 0: print('scanned', i, '/', len(fs), flush=True)
flags = [(f, h) for f, h in res if h]
json.dump(flags, open(os.path.join(D, 'flags.json'), 'w'), indent=1)
print(len(fs), 'frames scanned,', len(flags), 'with flags')
for f, h in flags[:40]: print(f, h)
