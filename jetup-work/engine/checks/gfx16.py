# 16:9 (1920x1080) overlays for the JetUP "5 Checks" video, built on the vertical card renderer in gfx.py
from PIL import Image, ImageDraw, ImageFilter
import gfx
from gfx import F, emoji, wrap, GOLD, WHITE, GREY, BG, CARD

W, H = 1920, 1080
SHIFT = 330                         # avatar moved right so the panel never covers him
PX, PY, PW, PH = 48, 118, 764, 830  # glass panel
CAP_CX, CAP_W, CAP_BOTTOM = 1350, 940, 1046


def card_small(c):
    """Render a card with the 1080-wide engine, then scale it into the panel."""
    RW = 900                          # render width: text ends up about 85% of the vertical size
    oldW, oldH = gfx.W, gfx.PANEL_H
    gfx.W, gfx.PANEL_H = RW, int(PH * RW / PW)
    try:
        big = gfx.card(c)
    finally:
        gfx.W, gfx.PANEL_H = oldW, oldH
    return big.resize((PW, PH), Image.LANCZOS)


def chrome(img):
    d = ImageDraw.Draw(img)
    # brand, top left
    d.rounded_rectangle((PX, 30, PX + 520, 92), 31, fill=(10, 10, 12, 210), outline=GOLD, width=2)
    emoji(img, '👑', PX + 18, 40, 42)
    d.text((PX + 72, 36), 'MTG', font=F('b', 36), fill=GOLD)
    d.text((PX + 160, 46), '|  Your Digital Architect', font=F('m', 24), fill=WHITE)
    # url, top right
    t = 'mtgtribe.com/jetup'
    f = F('sb', 28)
    tw = d.textlength(t, font=f)
    d.rounded_rectangle((W - 48 - tw - 48, 32, W - 48, 90), 29, fill=(10, 10, 12, 210), outline=GOLD, width=2)
    d.text((W - 48 - tw - 24, 61), t, font=f, fill=WHITE, anchor='lm')


def caption(img, text):
    if not text:
        return
    d = ImageDraw.Draw(img)
    f = F('sb', 46)
    lines = wrap(d, text, f, CAP_W)[:2]
    lh = 60
    th = lh * len(lines) + 26
    wmax = max(d.textlength(l, font=f) for l in lines)
    y0 = CAP_BOTTOM - th
    d.rounded_rectangle((CAP_CX - wmax / 2 - 30, y0, CAP_CX + wmax / 2 + 30, CAP_BOTTOM), 22, fill=(0, 0, 0, 205))
    for i, l in enumerate(lines):
        d.text((CAP_CX, y0 + 13 + i * lh + lh // 2), l, font=f, fill=WHITE, anchor='mm')


def overlay(card_layer, cap):
    """Transparent full-frame overlay: panel + card + chrome + caption."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((PX, PY, PX + PW, PY + PH), 30, fill=(12, 12, 16, 200), outline=(201, 160, 52, 255), width=2)
    if card_layer is not None:
        im.alpha_composite(card_layer, (PX, PY))
    chrome(im)
    caption(im, cap)
    return im


def cover(still):
    im = Image.new('RGBA', (W, H), BG + (255,))
    av = still.convert('RGBA').resize((W, H), Image.LANCZOS)
    im.alpha_composite(av, (SHIFT, 0))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for x in range(1000):
        gd.line((x, 0, x, H), fill=BG + (int(255 * min(1, max(0, (1000 - x) / 420))),))
    im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    chrome(im)
    d.text((80, 300), 'LOST MONEY', font=F('b', 118), fill=WHITE)
    d.text((80, 430), 'BEFORE?', font=F('b', 150), fill=GOLD)
    d.text((84, 630), 'Check these 5 things', font=F('sb', 54), fill=WHITE)
    d.text((84, 700), 'before you try again.', font=F('sb', 54), fill=WHITE)
    d.rounded_rectangle((84, 810, 560, 890), 40, outline=GOLD, width=3)
    d.text((322, 850), 'JetUP  ·  TAG Markets', font=F('sb', 36), fill=GOLD, anchor='mm')
    return im.convert('RGB')


def endcard():
    im = Image.new('RGBA', (W, H), BG + (255,))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse((200, 200, 1720, 1200), fill=(201, 160, 52, 30))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    d = ImageDraw.Draw(im)
    emoji(im, '👑', 290, 190, 200)
    d.text((390, 520), 'MTG', font=F('b', 170), fill=GOLD, anchor='mm')
    d.text((390, 640), 'Your Digital Architect', font=F('m', 46), fill=WHITE, anchor='mm')
    d.text((390, 760), "Let's Get This Crypto!", font=F('b', 52), fill=WHITE, anchor='mm')
    emoji(im, '💪', 680, 726, 64)
    rows = [('🌐', 'mtgtribe.com/jetup'), ('👥', 'mtgtribe.com/group'), ('✈️', 'Telegram  @mtgtribe'), ('📲', 'Check my bio')]
    y = 230
    for e, t in rows:
        d.rounded_rectangle((900, y, 1760, y + 120), 60, fill=CARD, outline=GOLD, width=2)
        emoji(im, e, 945, y + 28, 64)
        d.text((1040, y + 60), t, font=F('sb', 50), fill=WHITE, anchor='lm')
        y += 150
    d.text((W // 2, 940), 'Not financial advice. Trading involves risk. Only invest what you can afford to lose.',
           font=F('m', 32), fill=GREY, anchor='mm')
    return im.convert('RGB')
