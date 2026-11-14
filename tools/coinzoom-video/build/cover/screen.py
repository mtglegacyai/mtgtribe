# The cover's phone screen: the video's own card details frame (source frame 440), screen only, x3, with the same privacy
# blur and labelled pills as the video.
import os, sys
from PIL import Image, ImageFilter, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
os.environ.setdefault('MTG_FONTS', '')
import render as R
K = 3; X0, Y0, X1, Y1 = 801, 70, 1086, 670
im = R.src_frame(440).crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * K, (Y1 - Y0) * K), Image.LANCZOS).convert('RGBA')
for rect, label in R.TL['MASKS']:
    b = tuple(int(v) for v in ((rect[0] - 3 - X0) * K, (rect[1] - 3 - Y0) * K, (rect[2] + 3 - X0) * K, (rect[3] + 3 - Y0) * K))
    reg = im.crop(b).filter(ImageFilter.GaussianBlur((b[3] - b[1]) * .35))
    reg = Image.blend(reg, Image.new('RGBA', reg.size, (240, 238, 246, 255)), .45); im.paste(reg, b[:2])
    ph = int((b[3] - b[1]) * .86); pw = int(min(b[2] - b[0] - 6, max(ph * 5.2, (b[2] - b[0]) * .8)))
    R.paste_c(im, R.mask_pill(pw, ph, label), (b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
im.convert('RGB').save(os.path.join(HERE, 'screen.jpg'), quality=94); print(im.size)
