# Put MTG's corrected circle face (mtg-face-200-v2) inside an existing small gold-ring badge of a share image or cover.
# Everything outside the ring stays as it was. The ring is redrawn in the colour measured from the original ring.
# Usage: python3 badge_swap.py in out cx,cy,r_out,ring_w [zoom]
import sys, numpy as np
from PIL import Image, ImageDraw
FACE = '/home/user/mtgtribe/assets/tribe/mtg-face-200-v2.webp'
src, dst = sys.argv[1], sys.argv[2]
cx, cy, ro, rw = (float(v) for v in sys.argv[3].split(','))
zoom = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
K = 8
im = Image.open(src).convert('RGB'); a = np.array(im).astype(np.float32)
yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]; d = np.hypot(xx + 0.5 - cx, yy + 0.5 - cy)
ann = (d > ro - rw) & (d < ro); px = a[ann]
gold = px[(px[:, 0] - px[:, 2] > 60) & (px[:, 0] > 150)]
ring = tuple(int(v) for v in np.median(gold, 0)) if len(gold) > 10 else (226, 186, 100)
x0, y0 = int(np.floor(cx - ro - 2)), int(np.floor(cy - ro - 2)); x1, y1 = int(np.ceil(cx + ro + 2)), int(np.ceil(cy + ro + 2))
w, h = x1 - x0, y1 - y0
big = im.crop((x0, y0, x1, y1)).resize((w * K, h * K), Image.LANCZOS).convert('RGBA')
ri = ro - rw; Cx, Cy = (cx - x0) * K, (cy - y0) * K
f = Image.open(FACE).convert('RGB')
if zoom != 1.0:
    s = f.width / zoom; c = f.width / 2; f = f.crop((c - s / 2, c - s / 2, c + s / 2, c + s / 2))
D = int(round(2 * ri * K)); f = f.resize((D, D), Image.LANCZOS).convert('RGBA')
m = Image.new('L', (D, D), 0); ImageDraw.Draw(m).ellipse((0, 0, D - 1, D - 1), fill=255); f.putalpha(m)
big.alpha_composite(f, (int(round(Cx - D / 2)), int(round(Cy - D / 2))))
dr = ImageDraw.Draw(big)
dr.ellipse((Cx - ro * K, Cy - ro * K, Cx + ro * K, Cy + ro * K), outline=ring + (255,), width=int(round(rw * K)) + 2)
small = big.resize((w, h), Image.LANCZOS).convert('RGB')
mm = Image.new('L', (w * K, h * K), 0); ImageDraw.Draw(mm).ellipse((Cx - (ro + 0.4) * K, Cy - (ro + 0.4) * K, Cx + (ro + 0.4) * K, Cy + (ro + 0.4) * K), fill=255)
im.paste(small, (x0, y0), mm.resize((w, h), Image.LANCZOS))
im.save(dst, quality=92)
print(dst.split('/')[-1], 'ring colour', ring)
