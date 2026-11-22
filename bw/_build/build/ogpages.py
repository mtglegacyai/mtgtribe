"""One social preview per page (MTG, 9 Nov 2026; formula in tools/og/README.md): a big headline that says what the page
gives you, one clear visual of its subject, the exact address in a pill, the Bitcoin Wealth logo disc. 1200x630, under 200 KB."""
import io, math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from config import *

F = SCR + '/fonts/'
W, H = 1200, 630

SPECS = {
    # key: (eyebrow, headline lines, visual)
    'land': ('Bitcoin Wealth, explained by MTG', ['Collect Bitcoin', 'together.', 'Check every payment.'], 'coin'),
    'home': ('Start here', ['Your route', 'through', 'Bitcoin Wealth'], 'coin'),
    'fit': ('An honest fit check', ['Is it right', 'for you?', '5 quick questions'], 'check'),
    'back': ('Ignored it? Tried it? Left it?', ['Welcome back.', 'Take a fresh', 'look.'], 'mascot'),
    'what': ('In plain words', ['What is', 'Bitcoin Wealth?'], 'coin'),
    'hiw': ('How it works', ['14 positions.', 'Where every', 'payment goes'], 'tree'),
    'slots': ('The once-off', ['12 slots.', 'You pay', '0.001 BTC once'], 'ladder'),
    'pool': ('After your first cycle', ['Recycling', 'and the', 'Royal Pool'], 'tree'),
    'stokvel': ('The scorecard', ['Better than', 'a stokvel?'], 'check'),
    'diff': ('Works on any platform', ['5 checks', 'before you', 'start anywhere'], 'check'),
    'proof': ('Every payment is public', ['Check it', 'yourself on', 'BscScan'], 'proof'),
    'join': ('Step by step', ['Join Bitcoin', 'Wealth in', '5 steps'], 'thumb'),
    'tut': ('3 tutorial videos', ['Join Bitcoin', 'Wealth,', 'every tap shown'], 'thumb:3'),
    'w-t1': ('Tutorial 1 of 3', ['Set up', 'SafePal,', 'the safe way'], 'thumb:1'),
    'w-t2': ('Tutorial 2 of 3', ['Buy BNB.', 'Send it to', 'SafePal.'], 'thumb:2'),
    'w-t3': ('Tutorial 3 of 3', ['Activate', 'slot 1,', 'step by step'], 'thumb:3'),
    'exp': ('Explainer videos', ['How it works,', 'in pictures'], 'tree'),
    'w-i1': ('Explained in 5 minutes', ['How Bitcoin', 'Wealth', 'works'], 'leo'),
    'w-e1': ('Thandi asks, Leo answers', ["It's not", 'a coin.', 'So what is it?'], 'duo'),
    'w-e2': ('Thandi asks, Leo answers', ['14 seats.', '14 payments.', 'Where do they go?'], 'tree'),
    'w-e3': ('Thandi asks, Leo answers', ['12 slots.', 'Why you pay', 'for one only'], 'ladder'),
    'zoom': ('Meet the community', ['Live on Zoom.', '5 evenings,', '4 languages'], 'zoom'),
    'page': ('R1,000 once-off', ['Your own', 'Bitcoin Wealth', 'website'], 'mascot'),
    'order': ('Pay after it is built', ['Order your', 'BW Tribe Page'], 'mascot'),
    'c-btc': ('Free tool, live price', ['What is', '0.001 BTC', 'in rand?'], 'calc'),
    'c-slot': ('Free tool, live price', ['Every slot', 'in rand,', 'live'], 'ladder'),
    'c-halv': ('Free tool, live', ['Next Bitcoin', 'halving:', 'the countdown'], 'halv'),
    'faq': ('Bitcoin Wealth FAQ', ['Straight', 'answers'], 'check'),
    'gloss': ('Glossary', ['Crypto words,', 'plain English'], 'coin'),
    'safe': ('Safety centre', ['6 habits that', 'protect your', 'wallet'], 'check'),
    'card': ('Crypto card', ['Spend your', 'crypto with', 'a card'], 'coin'),
    'tribe': ('Free community', ['Join the', 'MTG TRIBE'], 'mascot'),
    'disc': ('Independent guide', ['Disclaimer'], 'coin'),
}


def font(name, size, w=None):
    f = ImageFont.truetype(F + name, size)
    if w:
        f.set_variation_by_axes([w])
    return f


def background():
    im = Image.new('RGB', (W, H), (5, 7, 5))
    g = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse((-320, -380, 640, 380), fill=(130, 74, 0)); d.ellipse((760, 260, 1520, 920), fill=(28, 104, 18))
    g = g.filter(ImageFilter.GaussianBlur(170)); im = Image.blend(im, g, .62)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 34):
        for y in range(0, H, 34):
            d.point((x, y), fill=(58, 50, 30))
    return im


def coin(im, cx, cy, r):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(40, 0, -1):
        a = int(90 * (k / 40) ** 2)
        d.ellipse((cx - r - k * 3, cy - r - k * 3, cx + r + k * 3, cy + r + k * 3), outline=(255, 161, 1, a // 6))
    for i in range(r, 0, -1):
        t = i / r
        col = (int(196 + 59 * (1 - t) ** .6), int(110 + 120 * (1 - t) ** .8), int(0 + 90 * (1 - t) ** 2))
        d.ellipse((cx - i - int(r * .12 * (1 - t)), cy - i - int(r * .12 * (1 - t)), cx + i - int(r * .12 * (1 - t)), cy + i - int(r * .12 * (1 - t))), fill=col)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 233, 160), width=max(4, r // 18))
    d.ellipse((cx - r * .82, cy - r * .82, cx + r * .82, cy + r * .82), outline=(255, 220, 130, 140), width=3)
    f = font('Sora[wght].ttf', int(r * 1.15), 800)
    d.text((cx + 4, cy + 6), '₿', font=f, fill=(150, 70, 0), anchor='mm')
    d.text((cx, cy), '₿', font=f, fill=(255, 248, 225), anchor='mm')
    im.paste(lay, (0, 0), lay)


def visual(im, kind):
    d = ImageDraw.Draw(im)
    cx, cy = 930, 330
    if kind == 'coin':
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((cx - 230, cy - 230, cx + 230, cy + 230), fill=(255, 161, 1, 120))
        glow = glow.filter(ImageFilter.GaussianBlur(60)); im.paste(glow, (0, 0), glow)
        lg = Image.open(SCR + '/../bwp/logo.png').convert('RGBA').resize((360, 360), Image.LANCZOS)
        im.paste(lg, (cx - 180, cy - 180), lg)
    elif kind in ('tree',):
        rows = [(1, 0), (2, 1), (4, 3), (8, 7)]
        y = 150
        for n, _ in rows:
            gap = 34 if n == 8 else 70
            rr = 23 if n == 8 else 30
            if n == 1:
                d.rounded_rectangle((cx - 70, y - 26, cx + 70, y + 26), 26, fill=(248, 188, 7))
                d.text((cx, y), 'YOU', font=font('Sora[wght].ttf', 30, 800), fill=(30, 18, 0), anchor='mm')
            else:
                tot = n * rr * 2 + (n - 1) * (gap - rr * 2 + 10)
                x0 = cx - tot / 2 + rr
                for i in range(n):
                    x = x0 + i * (rr * 2 + gap - rr * 2 + 10)
                    d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 161, 1), outline=(255, 230, 160), width=3)
            y += 110
        d.text((cx, y - 20), '2 + 4 + 8 = 14', font=font('Manrope[wght].ttf', 30, 800), fill=(230, 225, 211), anchor='mm')
    elif kind == 'ladder':
        x = 720
        for i in range(12):
            h = 26 + i * 27
            col = (255, 161, 1) if i == 0 else (63, 193, 31)
            d.rounded_rectangle((x, 520 - h, x + 30, 520), 8, fill=col)
            x += 38
        d.text((735, 545), '0.001', font=font('Manrope[wght].ttf', 24, 800), fill=(255, 161, 1))
        d.text((1150, 545), '2.048 BTC', font=font('Manrope[wght].ttf', 24, 800), fill=(192, 255, 114), anchor='ra')
    elif kind == 'check':
        items = ['Every payment public', 'Paid to your own wallet', 'No bank in the middle', '0.001 BTC once-off']
        y = 175
        for t in items:
            d.rounded_rectangle((700, y - 34, 1150, y + 34), 22, fill=(20, 26, 16), outline=(255, 190, 90), width=2)
            d.ellipse((718, y - 18, 754, y + 18), fill=(63, 193, 31))
            d.line((727, y, 734, y + 8), fill=(255, 255, 255), width=5); d.line((734, y + 8, 746, y - 8), fill=(255, 255, 255), width=5)
            d.text((772, y), t, font=font('Manrope[wght].ttf', 28, 800), fill=(240, 235, 222), anchor='lm')
            y += 92
    elif kind == 'proof':
        d.rounded_rectangle((690, 150, 1160, 470), 26, fill=(14, 18, 11), outline=(255, 190, 90), width=2)
        d.text((720, 190), 'Contract', font=font('Manrope[wght].ttf', 26, 700), fill=(168, 162, 145))
        d.text((720, 232), '0x1ad09b04...92Cd29', font=font('Manrope[wght].ttf', 34, 800), fill=(192, 255, 114))
        d.text((720, 300), f'{MEMBERS} member IDs', font=font('Sora[wght].ttf', 40, 800), fill=(255, 161, 1))
        d.text((720, 360), f'On chain since {ON_CHAIN_SINCE}', font=font('Manrope[wght].ttf', 28, 700), fill=(230, 225, 211))
        d.text((720, 408), f'Checked {CHECKED}', font=font('Manrope[wght].ttf', 24, 600), fill=(168, 162, 145))
    elif kind == 'calc':
        d.rounded_rectangle((700, 170, 1160, 470), 28, fill=(14, 18, 11), outline=(255, 190, 90), width=2)
        d.text((930, 250), '0.001 BTC', font=font('Sora[wght].ttf', 62, 800), fill=(255, 161, 1), anchor='mm')
        d.text((930, 330), 'in', font=font('Manrope[wght].ttf', 34, 700), fill=(168, 162, 145), anchor='mm')
        d.text((930, 405), 'Rand  ·  Dollars', font=font('Manrope[wght].ttf', 40, 800), fill=(192, 255, 114), anchor='mm')
    elif kind == 'halv':
        d.rounded_rectangle((700, 180, 1160, 460), 28, fill=(14, 18, 11), outline=(255, 190, 90), width=2)
        d.text((930, 250), 'Block', font=font('Manrope[wght].ttf', 32, 700), fill=(168, 162, 145), anchor='mm')
        d.text((930, 320), '1,050,000', font=font('Sora[wght].ttf', 72, 800), fill=(255, 161, 1), anchor='mm')
        d.rounded_rectangle((740, 395, 1120, 415), 10, fill=(40, 46, 34)); d.rounded_rectangle((740, 395, 990, 415), 10, fill=(63, 193, 31))
    elif kind == 'zoom':
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']; langs = ['isiXhosa', 'English', 'English', 'isiZulu', 'Sesotho']
        x = 700
        for dd, lg in zip(days, langs):
            d.rounded_rectangle((x, 190, x + 84, 450), 18, fill=(16, 22, 13), outline=(255, 190, 90), width=2)
            d.text((x + 42, 225), dd, font=font('Sora[wght].ttf', 26, 800), fill=(255, 161, 1), anchor='mm')
            d.text((x + 42, 300), '14:00', font=font('Manrope[wght].ttf', 20, 800), fill=(230, 225, 211), anchor='mm')
            d.text((x + 42, 360), '19:00' if dd == 'Fri' else '20:00', font=font('Manrope[wght].ttf', 20, 800), fill=(192, 255, 114), anchor='mm')
            d.text((x + 42, 395), lg[:7], font=font('Manrope[wght].ttf', 15, 700), fill=(168, 162, 145), anchor='mm')
            x += 94
    elif kind == 'leo':
        # Leo as he presents the Bitcoin Wealth presentation (the cut-out of its thumbnails), standing on the picture's bottom edge
        m = Image.open(STUDIO + '/projects/bitcoin-wealth/videos/intro-remake-leo/thumbs/assets/leo-hello.png').convert('RGBA')
        hgt = 600; m = m.resize((int(m.width * hgt / m.height), hgt), Image.LANCZOS)
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((cx - 250, 120, cx + 250, 620), fill=(255, 161, 1, 95))
        glow = glow.filter(ImageFilter.GaussianBlur(70)); im.paste(glow, (0, 0), glow)
        im.paste(m, (cx - m.width // 2, H - hgt + 40), m)
    elif kind == 'duo':
        # Thandi and Leo, as on the explainer's thumbnails (their cut-outs), side by side on the picture's bottom edge
        A = STUDIO + '/projects/bitcoin-wealth/videos/explainer-01-what-is-bitcoin-wealth/thumbs/assets/'
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((cx - 330, 140, cx + 330, 640), fill=(255, 161, 1, 85))
        glow = glow.filter(ImageFilter.GaussianBlur(70)); im.paste(glow, (0, 0), glow)
        for f, x, sz, row in (('leo-smile.png', cx + 115, 560, 880), ('thandi-asks.png', cx - 150, 530, 885)):
            m = Image.open(A + f).convert('RGBA').crop((0, 0, 1080, row)); m = m.resize((int(1080 * sz / 1080), int(row * sz / 1080)), Image.LANCZOS)
            im.paste(m, (x - m.width // 2, H - m.height), m)
    elif kind == 'mascot' or kind.startswith('thumb'):
        # thumb, thumb:1, thumb:2, thumb:3: the vertical thumbnail of that tutorial
        THUMBS = {'1': '01-safepal/final/BW-Tutorial-1-SafePal-mtg-thumbnail-9x16.jpg', '2': '02-bank-to-valr/final/BW-Tutorial-2-Bank-to-SafePal-mtg-thumbnail-9x16.jpg',
                  '3': '03-swap-signup-activate/final/BW-Tutorial-3-Activate-Slot-1-mtg-thumbnail-9x16.jpg'}
        src = (STUDIO + '/brand/mascot/mtg-mascot-bw.png') if kind == 'mascot' else \
              (STUDIO + '/projects/bitcoin-wealth/tutorials/' + THUMBS[kind.partition(':')[2] or '1'])
        m = Image.open(src).convert('RGB')
        th, tw = 520, int(520 * 9 / 16)
        m = m.resize((tw, int(tw * m.height / m.width)), Image.LANCZOS).crop((0, 0, tw, th))
        mask = Image.new('L', (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw, th), 34, fill=255)
        x0, y0 = cx - tw // 2, 55
        ImageDraw.Draw(im).rounded_rectangle((x0 - 8, y0 - 8, x0 + tw + 8, y0 + th + 8), 40, fill=(4, 4, 4), outline=(242, 198, 109), width=3)
        im.paste(m, (x0, y0), mask)


def make(key, path, url_path):
    eyebrow, lines, kind = SPECS[key]
    im = background()
    visual(im, kind)
    d = ImageDraw.Draw(im)
    logo = Image.open(SCR + '/../bwp/logo.png').convert('RGBA').resize((74, 74), Image.LANCZOS)
    im.paste(logo, (70, 52), logo)
    fe = font('Manrope[wght].ttf', 24, 800)
    tw = d.textlength(eyebrow, font=fe)
    d.rounded_rectangle((164, 66, 164 + tw + 36, 112), 23, fill=(30, 26, 12), outline=(255, 161, 1), width=2)
    d.text((182, 89), eyebrow, font=fe, fill=(255, 211, 107), anchor='lm')
    size = 104 if len(lines) <= 2 else 92
    while True:
        fh = font('Anton-Regular.ttf', size)
        if max(d.textlength(t.upper(), font=fh) for t in lines) <= 590 or size < 60:
            break
        size -= 4
    y = 150 if len(lines) == 3 else 175
    for i, t in enumerate(lines):
        col = (255, 161, 1) if i == len(lines) - 1 else (255, 255, 255)
        d.text((70, y), t.upper(), font=fh, fill=col)
        y += int(size * 1.08)
    url = (HOST + url_path).rstrip('/')
    fu = font('Manrope[wght].ttf', 28, 800)
    while d.textlength(url, font=fu) > 560:
        fu = font('Manrope[wght].ttf', fu.size - 2, 800)
    uw = d.textlength(url, font=fu)
    d.rounded_rectangle((70, 540, 70 + uw + 40, 592), 26, fill=(255, 161, 1))
    d.text((90, 566), url, font=fu, fill=(20, 12, 0), anchor='lm')
    q = 86
    while True:
        b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
        if b.tell() < 195000 or q < 60:
            break
        q -= 4
    open(path, 'wb').write(b.getvalue())
    return b.tell()


def build_all(dst):
    sizes = {}
    for key in SPECS:
        if key == 'land':
            up = BASE
        elif key == 'order':
            up = ORDER
        else:
            up = BASE + NAVD[key][1]
        name = 'og-bitcoin-wealth-guide.jpg' if key == 'land' else og_file(key)
        sizes[key] = make(key, dst + '/' + name, up)
        if key == 'land':
            make(key, dst + '/og-land.jpg', up)
    return sizes
