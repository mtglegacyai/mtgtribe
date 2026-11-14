# MTG's real TAG Markets screen for "Log in yourself, and see your own balance" (explainer #8): the right-hand phone of his
# onboarding guide's screenshot 08 (jetup/img/steps/guide-p08.webp). Kept: the status bar, the TAG header, the Balance
# pill and the green "My wallet balances" card, cut above the red arrow (so the arrow, My Wallet, Deposit and the
# "My Trading Accounts" block never appear), then the portal.tagmarkets.com address bar of the same phone under it.
# Both amounts are under a soft frosted pill, so no amount is readable. Writes stage/tag-balance.png.
import os
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/home/user/mtgtribe/jetup/img/steps/guide-p08.webp'
im = Image.open(SRC).convert('RGB')
X0, X1 = 1114, 1530                          # the right-hand phone's screen
TOP, BAR = (0, 483), (761, 822)              # the screen above the red arrow (My Wallet starts at 484); the address bar strip
PAGE = (239, 239, 239)                       # the page's light grey
top = im.crop((X0, TOP[0], X1, TOP[1])).copy(); W = top.size[0]

def frost(img, box, base, film, dots, r):
    """blur the box hard, settle it on a flat tint, then lay a frosted rounded pill with four soft dots on it"""
    x0, y0, x1, y1 = box
    reg = img.crop(box).filter(ImageFilter.GaussianBlur(14))
    reg = Image.blend(reg, Image.new('RGB', reg.size, base), .82)
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.size[0] - 1, reg.size[1] - 1), r, fill=255)
    img.paste(reg, box[:2], m)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle(box, r, fill=film + (150,), outline=(255, 255, 255, 120), width=2)
    cy = (y0 + y1) / 2; n = 4; gap = 15; x = (x0 + x1) / 2 - gap * (n - 1) / 2
    for k in range(n): d.ellipse((x + k * gap - 4, cy - 4, x + k * gap + 4, cy + 4), fill=dots)
    lay = lay.filter(ImageFilter.GaussianBlur(.6))
    out = img.convert('RGBA'); out.alpha_composite(lay); return out.convert('RGB')

# 1) the Balance pill's amount ("$ 0.00", dark pill, white text)
top = frost(top, (1418 - X0, 117, 1492 - X0, 153), (52, 52, 56), (120, 120, 128), (225, 225, 232, 230), 17)
# 2) the wallet card's amount ("USD $ 0.00", lime card, dark text)
top = frost(top, (1156 - X0, 431, 1332 - X0, 474), (196, 238, 104), (236, 252, 196), (70, 92, 40, 220), 21)

# close the green card at the cut with its own rounded corners (the card runs x 11..407 of the screen)
CL, CR, RAD = 11, 407, 16
mask = Image.new('L', top.size, 0); md = ImageDraw.Draw(mask)
md.rounded_rectangle((CL, 200, CR, TOP[1] - 1), RAD, fill=255)        # inside the card (and its rounded bottom)
band = Image.new('L', top.size, 0); ImageDraw.Draw(band).rectangle((CL - 2, TOP[1] - RAD - 2, CR + 2, TOP[1]), fill=255)
outside = Image.composite(Image.new('L', top.size, 0), band, mask)    # the two bottom corners outside the rounding
top.paste(Image.new('RGB', top.size, PAGE), (0, 0), outside)

gap = 26
bar = im.crop((X0, BAR[0], X1, BAR[1]))
out = Image.new('RGB', (W, TOP[1] + gap + bar.size[1] + 14), PAGE)
out.paste(top, (0, 0)); out.paste(bar, (0, TOP[1] + gap))
ImageDraw.Draw(out).rectangle((0, TOP[1] + gap + bar.size[1], W, out.size[1]), fill=bar.getpixel((4, bar.size[1] - 2)))

# checks: nothing red (the arrow) anywhere, and the two amount boxes carry no sharp text
px = out.load(); red = sum(1 for y in range(out.size[1]) for x in range(W) if px[x, y][0] > 200 and px[x, y][1] < 80 and px[x, y][2] < 80)
assert red == 0, f'{red} red pixels: the arrow is in the crop'
out.save(os.path.join(HERE, 'stage', 'tag-balance.png'), optimize=True)
print('stage/tag-balance.png', out.size)
