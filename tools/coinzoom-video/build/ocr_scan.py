# Privacy scan: OCR every second frame of the finished video (the whole frame and the window, normal and inverted, two
# page modes) for card-like numbers, expiry dates, long numbers and the private patterns in ~/.tutorial-private-patterns.tsv
# (one "category<TAB>regex" per line: the demo card's own number fragments and name go there, never in the repository).
# Usage: python3 ocr_scan.py <video.mp4> <work dir>      Zero flags before MTG sees the video.
import io, json, os, re, subprocess, sys
from multiprocessing import Pool
from PIL import Image, ImageOps
V, D = sys.argv[1], sys.argv[2]; os.makedirs(D, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', V, '-vf', 'select=not(mod(n\\,2))', '-vsync', '0', '-q:v', '2', os.path.join(D, 'o%05d.jpg')], check=True)
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
    for c in (im, im.crop((240, 112, 1680, 922)).resize((2880, 1620))):
        for img in (c, ImageOps.invert(c)):
            for psm in ('6', '11'):
                out = subprocess.run(['tesseract', '-', '-', '--psm', psm], input=png(img), capture_output=True).stdout.decode(errors='ignore')
                hits += [(k, m if isinstance(m, str) else m[0]) for k, r in PAT for m in r.findall(out)]
    return os.path.basename(p), sorted(set(hits))
fs = sorted(os.path.join(D, f) for f in os.listdir(D) if f.endswith('.jpg'))
with Pool(4) as pool: res = pool.map(scan, fs, chunksize=8)
flags = [(f, h) for f, h in res if h]
json.dump(flags, open(os.path.join(D, 'flags.json'), 'w'), indent=1)
print(len(fs), 'frames scanned,', len(flags), 'with flags')
for f, h in flags[:40]: print(f, h)
