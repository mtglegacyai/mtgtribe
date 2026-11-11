# clipsheet.py <clip> <step> [out] : redacted frames every <step> frames, labelled with frame index and source time
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
cid, step = sys.argv[1], int(sys.argv[2])
out = sys.argv[3] if len(sys.argv) > 3 else f'qa_{cid}.jpg'
m = json.load(open(f'clips/{cid}/meta.json'))
idx = list(range(0, m['n'], step))
sc = 0.34; tw, th = int(720 * sc), int(1562 * sc)
cols = 10; rows = (len(idx) + cols - 1) // cols
sh = Image.new('RGB', (cols * (tw + 4), rows * (th + 18)), 'white')
f = ImageFont.load_default()
for k, i in enumerate(idx):
    im = Image.open(f'clips/{cid}/{i:05d}.jpg').resize((tw, th))
    x, y = (k % cols) * (tw + 4), (k // cols) * (th + 18)
    sh.paste(im, (x, y + 16))
    ImageDraw.Draw(sh).text((x + 2, y + 2), f'{i} {m["start"] + i / 30:.2f}', fill='black', font=f)
sh.save(out, quality=85); print(out, len(idx))
