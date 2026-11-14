import sys, glob
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + '/t*.png'))[int(sys.argv[3]):int(sys.argv[4])]
cols = 2; w, h = 960, 540; rows = (len(fs) + cols - 1) // cols
s = Image.new('RGB', (w * cols, h * rows), (0, 0, 0))
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((w, h)); ImageDraw.Draw(im).text((8, 8), f.split('/')[-1], fill=(255, 0, 255))
    s.paste(im, ((i % cols) * w, (i // cols) * h))
s.save(sys.argv[2])
