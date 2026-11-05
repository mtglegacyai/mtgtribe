# MTG's full profile photo (face, mtgTribe.com t-shirt print and sign all visible) in a rounded gold frame.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
SRC = '/home/claude/face/p4/src.png'
GOLD_L, GOLD_D = (250, 228, 150), (196, 142, 44)
_src = None
_cache = {}

def photo_card(size):
    """RGBA image: the full square photo, size x size, rounded corners, gold gradient frame and soft glow."""
    global _src
    if size in _cache: return _cache[size].copy()
    if _src is None: _src = Image.open(SRC).convert('RGB')
    ring = max(4, size // 55); pad = max(14, size // 9); r = size // 12
    S = size + 2 * ring + 2 * pad
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    g = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle([pad - 4, pad - 4, S - pad + 3, S - pad + 3], r + ring + 4, fill=(232, 194, 90, 170))
    out.alpha_composite(g.filter(ImageFilter.GaussianBlur(pad * 0.55)))
    m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).rounded_rectangle([pad, pad, S - pad - 1, S - pad - 1], r + ring, fill=255)
    grad = np.zeros((S, S, 4), np.uint8); t = np.linspace(0, 1, S)[:, None] * 0.6 + np.linspace(0, 1, S)[None, :] * 0.4
    for i in range(3): grad[..., i] = (GOLD_L[i] * (1 - t) + GOLD_D[i] * t).astype(np.uint8)
    grad[..., 3] = np.array(m); out.alpha_composite(Image.fromarray(grad))
    ph = _src.resize((size, size), Image.LANCZOS).convert('RGBA')
    pm = Image.new('L', (size, size), 0); ImageDraw.Draw(pm).rounded_rectangle([0, 0, size - 1, size - 1], r, fill=255)
    ph.putalpha(pm); out.alpha_composite(ph, (pad + ring, pad + ring))
    _cache[size] = out
    return out.copy()

if __name__ == '__main__':
    photo_card(420).save('/home/claude/face/p4/photo_card_test.png')
