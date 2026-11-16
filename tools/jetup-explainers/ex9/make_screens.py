# MTG's real CopyX screens for explainer #9 ("What copying really means"), from his onboarding guide's screenshots
# (jetup/img/steps/guide-p14.webp, guide-p15.webp and guide-p20.webp, each 1600x900 with three phones). Each crop keeps
# one thing only, every figure is masked, and the guide's red arrows and red text boxes never appear:
#  a) stage/copyx-sonic.png: guide-p14, right-hand phone, ONLY the SONIC card (first in the CopyX list) with its logo,
#     the word SONIC and its Details button. The follower count is frosted; the ROI line, its chart and Max DD sit under
#     ONE frosted glass panel "Check the record yourself: Myfxbook"; both red arrows are painted out (the card's top
#     border and the Details button's top border are restored where the arrows crossed them). Nothing above the card.
#  b) stage/copyx-fee.png: guide-p15, left-hand phone, ONLY the "Performance Fee ... 30%" row, enlarged 3x (Lanczos).
#     No other row (Trading Days above, Min Investment below), nothing of the guide's text box or arrow.
#  c) stage/copyx-eye.png: guide-p20, right-hand phone, ONLY the SONIC Amplify card: both tab rows above it are cut
#     (no "Breached"), the blurred middle is blurred harder, the red arrow that enters it is painted out with the blur
#     round it, Deposit, Withdraw and the red square are dimmed under a soft white veil (unnamed), and the eye
#     icon stays bright for the stage's spotlight and tap.
# Checks: no arrow red left in any crop, the masked boxes carry no sharp detail (Laplacian), the fee row clears the text box.
# Usage: python3 make_screens.py   (writes the three PNGs into stage/ and prints the eye icon's position for engine.js)
import os, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'jetup', 'img', 'steps'))
OUT = os.path.join(HERE, 'stage')
LIME, INK, GLASS = (203, 251, 97), (246, 243, 255), (21, 17, 42)

def font(weight):
    """Manrope (the stage's body font) from Google Fonts, cached; the installed Poppins Bold if offline"""
    cache = os.path.join(os.path.expanduser('~'), '.cache', 'mtg-fonts'); os.makedirs(cache, exist_ok=True)
    p = os.path.join(cache, f'Manrope-{weight}.ttf')
    if not os.path.exists(p):
        try:
            css = urllib.request.urlopen(urllib.request.Request(f'https://fonts.googleapis.com/css2?family=Manrope:wght@{weight}',
                                                                headers={'User-Agent': 'Mozilla/4.0'}), timeout=20).read().decode()
            open(p, 'wb').write(urllib.request.urlopen(css.split('url(')[1].split(')')[0], timeout=20).read())
        except Exception as e:
            print('Manrope not downloaded (%s); using Poppins Bold' % e)
            return lambda s: ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', s)
    return lambda s: ImageFont.truetype(p, s)

def load(name):
    return np.array(Image.open(os.path.join(STEPS, name)).convert('RGB')).astype(np.float32)

def redness(a):
    return a[..., 0] - np.maximum(a[..., 1], a[..., 2])

def red_mask(a, grow=3, thr=40):
    """the guide's red (high R, low G and B), grown so the arrow's soft edges go too"""
    m = (redness(a) > thr) & (a[..., 0] > 140)
    return ndi.binary_dilation(m, iterations=grow) if grow else m

def inpaint(a, mask, iters=300):
    """fill the masked pixels from their surroundings: nearest clean pixel first, then diffusion to smooth the seams"""
    if not mask.any(): return a
    idx = ndi.distance_transform_edt(mask, return_distances=False, return_indices=True)
    out = a[idx[0], idx[1]].copy()
    for _ in range(iters):
        nb = (np.roll(out, 1, 0) + np.roll(out, -1, 0) + np.roll(out, 1, 1) + np.roll(out, -1, 1)) / 4
        out[mask] = nb[mask]
    return out

def restore_rows(a, mask, rows, ref_x):
    """a horizontal border under a painted-out arrow: copy each of its rows from a clean column"""
    for y in rows: a[y, mask[y]] = a[y, ref_x]
    return a

def frost(a, box, tint, k=.9, r=14):
    """destroy the detail in a box: hard blur, then settle it on a flat tint"""
    x0, y0, x1, y1 = box
    reg = Image.fromarray(np.clip(a[y0:y1, x0:x1], 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    a[y0:y1, x0:x1] = np.array(reg).astype(np.float32) * (1 - k) + np.array(tint, np.float32) * k
    return a

def sharpness(a, box):
    """mean absolute Laplacian inside a box: text and chart lines score high, a frosted box scores near zero"""
    x0, y0, x1, y1 = box
    return float(np.abs(ndi.laplace(a[y0:y1, x0:x1].mean(axis=2))).mean())

def up(a, k):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((a.shape[1] * k, a.shape[0] * k), Image.LANCZOS)

def layer(size, shape, color, alpha=255, blur=0):
    """a solid colour through a (soft) shape mask: blurring the mask, never the RGBA, so no dark fringe"""
    m = Image.new('L', size, 0); shape(ImageDraw.Draw(m))
    if blur: m = m.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 255: m = m.point(lambda v: v * alpha // 255)
    out = Image.new('RGBA', size, tuple(color) + (0,)); out.putalpha(m); return out

def rounded_alpha(img, box, r):
    """transparent outside the card's own rounded outline"""
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, r, fill=255)
    out = img.convert('RGBA'); out.putalpha(m.filter(ImageFilter.GaussianBlur(.7))); return out

# ------------------------------------------------------------------------------------------- a) the SONIC card
p14 = load('guide-p14.webp')
X0, Y0, X1, Y1 = 1163, 446, 1519, 739                     # the card (border x 1167..1515, y 450..733) and 4 px of white round it
a = p14[Y0:Y1, X0:X1].copy()
m = red_mask(a, grow=6)                                    # arrow 1 (y 425..476) over the card's top edge, arrow 2 (y 556..688) to Details
a = inpaint(a, m)
near = ndi.binary_dilation(m, iterations=5); near[527 - Y0:] = False     # the header is plain white: lift the arrow's light ringing to it
a[near & (a.min(axis=2) > 222)] = (254, 254, 253)
a = restore_rows(a, m, range(448 - Y0, 454 - Y0), 1250 - X0)      # the card's top border, under the first arrow
a = restore_rows(a, m, range(682 - Y0, 688 - Y0), 1250 - X0)      # the Details button's top border, under the second arrow's head
assert red_mask(a, grow=0).sum() == 0 and (redness(a) > 12).sum() == 0, 'red left on the SONIC card'
FOL = (1258 - X0, 489 - Y0, 1312 - X0, 513 - Y0)            # the follower count "368291" (the people icon stays)
BAND = (1176 - X0, 533 - Y0, 1507 - X0, 677 - Y0)           # ROI, +126.94%, its chart, the divider, 0.26%, Max DD
sharp0 = sharpness(a, BAND), sharpness(a, FOL)
a = frost(a, FOL, (254, 254, 253), k=.92, r=8)             # settles on the card's own white: no box shows round the pill
a = frost(a, BAND, (232, 236, 224), k=.92, r=16)
sharp1 = sharpness(a, BAND), sharpness(a, FOL)
assert sharp1[0] < .3 and sharp1[1] < .3, ('masked boxes still carry detail', sharp1)
K = 2
img = up(a, K).convert('RGBA'); W, H = img.size
fx0, fy0, fx1, fy1 = [v * K for v in FOL]                   # a soft frosted pill with five dots over the follower count
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle((fx0, fy0, fx1, fy1), (fy1 - fy0) // 2, fill=255), (243, 244, 240)))
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle((fx0, fy0, fx1, fy1), (fy1 - fy0) // 2, outline=255, width=2), (196, 200, 190)))
cy = (fy0 + fy1) / 2
img.alpha_composite(layer((W, H), lambda d: [d.ellipse(((fx0 + fx1) / 2 + (i - 2) * 15 - 4, cy - 4, (fx0 + fx1) / 2 + (i - 2) * 15 + 4, cy + 4), fill=255)
                                             for i in range(5)], (128, 132, 124)))
bx0, by0, bx1, by1 = [v * K for v in BAND]                  # ONE frosted glass panel over the whole middle band (the series' glass)
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle((bx0 + 2, by0 + 8, bx1 - 2, by1 + 2), 30, fill=255), (0, 0, 0), 80, 9))
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle((bx0, by0, bx1, by1), 30, fill=255), GLASS, 240))
grad = Image.new('L', (1, by1 - by0)); grad.putdata([int(34 * max(0, 1 - y / ((by1 - by0) * .6)) ** 1.5) for y in range(by1 - by0)])
sheen = Image.new('L', (W, H), 0); sheen.paste(grad.resize((bx1 - bx0, by1 - by0)), (bx0, by0))
pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).rounded_rectangle((bx0 + 4, by0 + 4, bx1 - 4, by1 - 4), 26, fill=255)
sh = Image.new('RGBA', (W, H), LIME + (0,)); sh.putalpha(Image.fromarray(np.minimum(np.array(sheen), np.array(pm))))
img.alpha_composite(sh)                                      # the edge-lit sheen, fading down the panel
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle((bx0, by0, bx1, by1), 30, outline=255, width=5), LIME, 235))
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle((bx0 + 12, by0 + 12, bx1 - 12, by1 - 12), 20, outline=255, width=2), LIME, 80))
F7, F8 = font(700), font(800)
t = ImageDraw.Draw(img); cxp = (bx0 + bx1) / 2
t.text((cxp, by0 + (by1 - by0) * .35), 'Check the record yourself:', font=F7(37), fill=INK, anchor='mm')
t.text((cxp, by0 + (by1 - by0) * .69), 'Myfxbook', font=F8(56), fill=LIME, anchor='mm')
img = rounded_alpha(img, ((1166 - X0) * K, (449 - Y0) * K, (1516 - X0) * K, (735 - Y0) * K), 13 * K)
img.save(os.path.join(OUT, 'copyx-sonic.png'), optimize=True)
print('stage/copyx-sonic.png', img.size, '| detail (Laplacian) in the band and the follower count: %.1f, %.1f -> %.2f, %.2f' % (sharp0 + sharp1))

# ------------------------------------------------------------------------------------------- b) the fee row
p15 = load('guide-p15.webp')
R0 = (90, 554, 434, 606)                                    # inside the dark card: Trading Days ends at 549, Min Investment starts at 610
assert R0[1] > 487 + 40, 'the crop must stay clear of the guide text box (it ends at y 487)'
row = p15[R0[1]:R0[3], R0[0]:R0[2]].copy()
assert red_mask(row, grow=0).sum() == 0, 'red in the fee row'
fee = up(row, 3)
# the crop starts at the card's own left edge (x 88), inside the lime icon's dim glow (the icon itself starts at x 100): fade the
# first 28 px (about 9 source px) in from black, so the glow rises softly out of the stage's black row, never a hard seam
fa = np.array(fee).astype(np.float32); ramp = np.clip(np.arange(fa.shape[1]) / 28., 0, 1) ** 1.3
fee = Image.fromarray(np.clip(fa * ramp[None, :, None], 0, 255).astype(np.uint8))
assert np.array(fee)[:, 34:60].max() > 180, 'the feather must not dim the lime icon'
fee.save(os.path.join(OUT, 'copyx-fee.png'), optimize=True)
print('stage/copyx-fee.png', fee.size)

# ------------------------------------------------------------------------------------------- c) the SONIC Amplify card
p20 = load('guide-p20.webp')
X0, Y0, X1, Y1 = 1078, 189, 1426, 701                      # the card (border x 1082..1421, y 195..697); the tab rows end at 183
c = p20[Y0:Y1, X0:X1].copy()
BLUR = (1086 - X0, 256 - Y0, 1418 - X0, 643 - Y0)          # the blurred middle (both accounts' figures, already blurred by MTG)
BTN = (1094 - X0, 644 - Y0, 1337 - X0, 685 - Y0)           # Deposit (x 1099..1181), Withdraw (1192..1284), the red square (1295..1331)
EYE = (1342 - X0, 647 - Y0, 1380 - X0, 679 - Y0)           # the eye icon's button (stays bright)
keep = np.zeros(c.shape[:2], bool); keep[BTN[1]:BTN[3], BTN[0]:BTN[2]] = True
tip = np.zeros(c.shape[:2], bool); tip[316 - Y0:446 - Y0, 1270 - X0:] = True      # where the arrow enters, and its soft blurred tip
m = (red_mask(c, grow=0) | (tip & (redness(c) > 3))) & ~keep
m = ndi.binary_dilation(m, iterations=6) & ~keep
c = inpaint(c, m, iters=800)
bl = BLUR
reg = Image.fromarray(np.clip(c[bl[1]:bl[3], bl[0]:bl[2]], 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))
c[bl[1]:bl[3], bl[0]:bl[2]] = np.array(reg).astype(np.float32)          # blurred harder: no figure even half readable
assert ((redness(c) > 5) & ~keep).sum() == 0, ('red or pink left outside the red square button', int(((redness(c) > 5) & ~keep).sum()))
assert sharpness(c, BLUR) < 1.0, ('detail left in the blurred middle', sharpness(c, BLUR))
K = 2
img = up(c, K).convert('RGBA'); W, H = img.size
img.alpha_composite(layer((W, H), lambda d: d.rounded_rectangle([v * K for v in BTN], 14, fill=255), (255, 255, 255), 186, 3))   # soft white veil
img = rounded_alpha(img, ((1081 - X0) * K, (194 - Y0) * K, (1423 - X0) * K, (698 - Y0) * K), 12 * K)
img.save(os.path.join(OUT, 'copyx-eye.png'), optimize=True)
eye = [round(((EYE[0] + EYE[2]) / 2) / (X1 - X0), 4), round(((EYE[1] + EYE[3]) / 2) / (Y1 - Y0), 4)]
print('stage/copyx-eye.png', img.size, '| detail in the blurred middle %.2f | eye icon at (fraction of the image)' % sharpness(c, BLUR), eye)
