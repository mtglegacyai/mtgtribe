"""Build the Bitcoin Wealth guide: python3 build.py [--fast] [--media]
Writes out/prod (repo layout) under the scratchpad, then copies /bw and /bwcopy into the mtgtribe repo."""
import hashlib, os, re, shutil, subprocess, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import core
from config import *
from pages_learn import p_home, p_fit, p_back, p_what, p_hiw, p_slots, p_pool, p_stokvel, p_diff, p_proof
from pages_do import (p_join, p_tut, p_exp, p_zoom, p_page, p_c_btc, p_c_slot, p_c_halv, p_faq, faq_ld, p_gloss, p_safe,
                      p_card, p_tribe, p_disc, order_page, JOIN_STEPS, JOIN_NEEDS, GLOSS, zoom_ld, zoom_ics, zoom_head)
from pages_land import landing
from pages_watch import p_watch, watch_ld, p_present, present_ld
from seo import SEO_DESC

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'
OUT = SCR + '/out'
FONTS = SCR + '/fonts/'

PAGES = {
    'home': ('Bitcoin Wealth dashboard: start here', p_home, ['s1', 'i1', 't1', 't2', 't3']),
    'fit': ('Is Bitcoin Wealth right for me?', p_fit, None),
    'back': ('Welcome back to Bitcoin Wealth', p_back, None),
    'what': ('What is Bitcoin Wealth?', p_what, ['i1']),
    'hiw': ('How Bitcoin Wealth works: the 14 positions', p_hiw, None),
    'slots': ('The 12 slots and the once-off', p_slots, None),
    'pool': ('Recycling and the Royal Pool', p_pool, None),
    'stokvel': ('Bitcoin Wealth vs a stokvel', p_stokvel, None),
    'diff': ('What makes Bitcoin Wealth different', p_diff, None),
    'proof': ('Check Bitcoin Wealth yourself on BscScan', p_proof, None),
    'join': ('How to join Bitcoin Wealth step by step', p_join, ['t1', 't2', 't3']),
    'tut': ('Bitcoin Wealth tutorial videos', p_tut, ['t1', 't2', 't3']),
    'exp': ('Bitcoin Wealth explainer videos', p_exp, ['i1']),
    'zoom': ('Bitcoin Wealth live on Zoom', p_zoom, None),
    'page': ('Your own BW Tribe Page', p_page, None),
    'c-btc': ('Bitcoin to Rand Converter', p_c_btc, None),
    'c-slot': ('Bitcoin Wealth Slot Calculator', p_c_slot, None),
    'c-halv': ('Bitcoin Halving Countdown', p_c_halv, None),
    'faq': ('Bitcoin Wealth FAQ', p_faq, 'faq'),
    'gloss': ('Bitcoin Wealth glossary', p_gloss, None),
    'safe': ('Bitcoin Wealth safety centre', p_safe, None),
    'card': ('Spend your crypto with a card', p_card, None),
    'tribe': ('Join the MTG TRIBE', p_tribe, None),
    'disc': ('Disclaimer', p_disc, None),
}


def page_ld(key, title, desc):
    url = SITE + BASE + NAVD[key][1]
    if key.startswith('c-'):
        return [{'@type': 'WebApplication', 'name': title, 'url': url, 'description': desc, 'applicationCategory': 'FinanceApplication',
                 'operatingSystem': 'Any (runs in a web browser)', 'browserRequirements': 'Requires JavaScript', 'isAccessibleForFree': True,
                 'inLanguage': 'en-ZA', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'ZAR'},
                 'author': {'@id': core.PERSON_ID}, 'publisher': {'@id': core.PERSON_ID}}]
    if key == 'gloss':
        tid = url + '#definedtermset'
        return [{'@type': 'DefinedTermSet', '@id': tid, 'name': 'Bitcoin Wealth glossary: crypto words in plain English', 'url': url,
                 'hasDefinedTerm': [{'@type': 'DefinedTerm', 'name': t, 'description': core.plain(d + (' Like: ' + like if like else '')),
                                     'url': url + '#' + id_, 'inDefinedTermSet': {'@id': tid}} for id_, t, icn, d, like in GLOSS]}]
    if key == 'join':
        return [{'@type': 'HowTo', 'name': 'How to join Bitcoin Wealth with SafePal, step by step', 'description': desc, 'totalTime': 'PT30M',
                 'inLanguage': 'en-ZA', 'supply': [{'@type': 'HowToSupply', 'name': n} for n in JOIN_NEEDS],
                 'tool': [{'@type': 'HowToTool', 'name': 'SafePal wallet app'}],
                 'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': n, 'text': t} for i, (n, t) in enumerate(JOIN_STEPS)]}]
    if key == 'zoom':
        return zoom_ld(url, core.og_image(key))
    if key == 'page':
        return [{'@type': 'Product', 'name': 'BW Tribe Page', 'description': desc, 'brand': {'@type': 'Brand', 'name': 'MTG TRIBE'},
                 'offers': {'@type': 'Offer', 'price': str(PRICE_ZAR), 'priceCurrency': 'ZAR', 'url': SITE + ORDER, 'availability': 'https://schema.org/InStock'}}]
    return []


def sh(*a):
    subprocess.run(a, check=True)


# ------------------------------------------------------------------ images
def font(w, size, fam='Sora'):
    from PIL import ImageFont
    f = ImageFont.truetype(FONTS + f'{fam}[wght].ttf', size)
    f.set_variation_by_axes([w])
    return f


def images(dst):
    from PIL import Image, ImageDraw, ImageFilter
    os.makedirs(dst, exist_ok=True)
    logo = Image.open(SCR + '/../bwp/logo.png').convert('RGBA')
    for n in (96, 192):
        logo.resize((n, n), Image.LANCZOS).save(dst + f'/bitcoin-wealth-logo-{n}.png', optimize=True)
    logo.resize((32, 32), Image.LANCZOS).save(dst + '/favicon-32.png', optimize=True)
    bg = Image.new('RGBA', (180, 180), (5, 7, 5, 255)); bg.alpha_composite(logo.resize((156, 156), Image.LANCZOS), (12, 12))
    bg.convert('RGB').save(dst + '/apple-touch-icon.png', optimize=True)
    # mascot poster (approved /bw shirt)
    m = Image.open(STUDIO + '/brand/mascot/mtg-mascot-bw.png').convert('RGB')
    m.resize((540, 945), Image.LANCZOS).save(dst + '/bitcoin-wealth-mascot-lion-bw.webp', quality=82, method=6)
    # video posters from the approved thumbnails: 9:16 (720 and 360 wide) or 16:9 (1280 and 640 wide)
    for k, v in V.items():
        t = Image.open(STUDIO + '/' + v['poster']).convert('RGB')
        for w, suf in (((1280, ''), (640, '-640')) if v['o'] == 'h' else ((720, ''), (360, '-360'))):
            h = w * 9 // 16 if v['o'] == 'h' else w * 16 // 9
            t.resize((w, h), Image.LANCZOS).save(dst + f'/{v["slug"]}{suf}.webp', quality=82 if not suf else 80, method=6)
        if v.get('wide'):                 # the 16:9 cover the page shows for a 9:16 video (core.vid)
            t = Image.open(STUDIO + '/' + v['wide']).convert('RGB')
            for w, suf in ((1280, '-wide'), (640, '-wide-640')):
                t.resize((w, w * 9 // 16), Image.LANCZOS).save(dst + f'/{v["slug"]}{suf}.webp', quality=82 if w > 640 else 80, method=6)
    import ogpages
    sz = ogpages.build_all(dst)
    print('social previews:', len(sz), 'largest', max(sz.values()) // 1000, 'KB')


def og(path, logo, l1, l2, l3, l4, url):
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), (5, 7, 5))
    g = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse((-300, -380, 700, 400), fill=(120, 70, 0)); d.ellipse((780, 280, 1500, 900), fill=(30, 110, 20))
    g = g.filter(ImageFilter.GaussianBlur(170)); im = Image.blend(im, g, .6)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 34):
        for y in range(0, H, 34):
            d.point((x, y), fill=(60, 52, 30))
    e = logo.resize((130, 130), Image.LANCZOS); im.paste(e, (80, 70), e)
    d.text((80, 250), l1, font=font(800, 62), fill=(255, 255, 255))
    d.text((80, 325), l2, font=font(800, 62), fill=(255, 161, 1))
    d.text((80, 430), l3, font=font(700, 30, 'Manrope'), fill=(248, 188, 7))
    d.text((80, 476), l4, font=font(600, 26, 'Manrope'), fill=(200, 194, 178))
    d.rounded_rectangle((80, 545, 80 + 18 + d.textlength(url, font=font(800, 26, 'Manrope')) + 18, 593), 24, fill=(255, 161, 1))
    d.text((98, 552), url, font=font(800, 26, 'Manrope'), fill=(20, 12, 0))
    im.save(path, quality=88, optimize=True, progressive=True)


# ------------------------------------------------------------------ media (web encodes of the approved masters)
def media(dst):
    os.makedirs(dst, exist_ok=True)
    x264 = ['-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p']
    for k, v in V.items():
        src = STUDIO + '/' + v['master']
        if v['o'] == 'h':      # 16:9: a light 720p for phones and a 1080p for big screens (the player picks)
            jobs = [('', 'scale=1280:720:flags=lanczos', ['-crf', '25', '-maxrate', '1500k', '-bufsize', '3000k'], '112k'),
                    ('-1080p', 'scale=1920:1080:flags=lanczos', ['-crf', '23', '-maxrate', '3200k', '-bufsize', '6400k'], '128k')]
        else:
            jobs = [('', 'scale=720:1280:flags=lanczos', ['-crf', '27', '-maxrate', '900k', '-bufsize', '1800k'], '96k')]
        for suf, vf, rate, ab in jobs:
            out = dst + f'/{v["slug"]}{suf}.mp4'
            if not os.path.exists(out) or os.path.getmtime(src) > os.path.getmtime(out):      # a changed master is encoded again
                sh('ffmpeg', '-y', '-v', 'error', '-i', src, '-vf', vf, *x264, *rate, '-c:a', 'aac', '-b:a', ab, '-ac', '2', '-movflags', '+faststart', out)


# ------------------------------------------------------------------ pages
def render(dst):
    core.MODE = 'prod'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    base = dst + BASE.rstrip('/')
    os.makedirs(base + '/assets', exist_ok=True)
    for f in sorted(os.listdir(SRC + '/assets')):
        shutil.copy(SRC + '/assets/' + f, base + '/assets/' + f)
        core.HASH['assets/' + f] = hashlib.md5(open(SRC + '/assets/' + f, 'rb').read()).hexdigest()[:8]
    shutil.copytree(OUT + '/_img', base + '/img')
    shutil.copytree(OUT + '/_media', base + '/media')
    # a video cover that changes must show at once, not after the browser's memory of the old one runs out
    for v in V.values():
        for f in sorted(os.listdir(OUT + '/_img')):
            if f.startswith(v['slug']) and f.endswith('.webp'):
                core.HASH['img/' + f] = hashlib.md5(open(OUT + '/_img/' + f, 'rb').read()).hexdigest()[:8]
    # a video that changes (Leo's voice added to a tutorial) must play at once too, not the copy a browser kept
    for f in sorted(os.listdir(OUT + '/_media')):
        core.HASH['media/' + f] = hashlib.md5(open(OUT + '/_media/' + f, 'rb').read()).hexdigest()[:8]
    hd, body = landing()
    open(base + '/index.html', 'w').write(core.wrap_doc(hd, body, 'landing'))
    for key, (title, fn, extra) in PAGES.items():
        here = NAVD[key][1]
        desc = SEO_DESC[key]
        ld = faq_ld() if extra == 'faq' else core.video_ld(extra, here) if extra else []
        ld = ld + page_ld(key, title, desc)
        hd, content = core.dash_page(key, title, desc, fn, ld)
        os.makedirs(base + '/' + here, exist_ok=True)
        if key == 'zoom':      # page-only stylesheet, and the weekly schedule for people's calendars
            hd += zoom_head(here)
            open(base + '/' + here + ZOOM_ICS, 'w', newline='').write(zoom_ics(SITE + BASE + here))
        open(base + '/' + here + 'index.html', 'w').write(core.wrap_doc(hd, content, 'dashpage'))
    # a page of its own for each tutorial video (pages_watch.py)
    for code in WATCH_PAGES:
        key = 'w-' + code; here = NAVD[key][1]
        hd, content = core.dash_page(key, WATCH_PAGES[code][1], SEO_DESC[key], p_watch(code), watch_ld(code), parent='tut')
        os.makedirs(base + '/' + here, exist_ok=True)
        open(base + '/' + here + 'index.html', 'w').write(core.wrap_doc(hd, content, 'dashpage'))
    # the presentation's own page, under Explainer Videos (pages_watch.py)
    for code in PRESENT:
        key = 'w-' + code; here = NAVD[key][1]
        hd, content = core.dash_page(key, PRESENT[code][1], SEO_DESC[key], p_present(code), present_ld(code), parent='exp')
        os.makedirs(base + '/' + here, exist_ok=True)
        open(base + '/' + here + 'index.html', 'w').write(core.wrap_doc(hd, content, 'dashpage'))
    hd, body = order_page()
    os.makedirs(dst + ORDER, exist_ok=True)
    open(dst + ORDER + 'index.html', 'w').write(core.wrap_doc(hd, body, 'landing orderpage'))
    # sitemap for /bw, llms files. Each video is listed once, on the page where it is the main thing: a tutorial and the
    # presentation on their own pages, the promo on the main page, the cartoon on the dashboard
    wkeys = ['w-' + c for c in WATCH_PAGES]
    pkeys = ['w-' + c for c in PRESENT]
    urls = [''] + [NAVD[k][1] for k in PAGES] + [NAVD[k][1] for k in wkeys + pkeys]
    vids = {'': ['p1'], NAVD['home'][1]: ['s1']}
    vids.update({WATCH[c]: [c] for c in list(WATCH_PAGES) + list(PRESENT)})

    def vtag(c):
        v = V[c]
        return (f'<video:video><video:thumbnail_loc>{core.video_thumbs(c)[0]}</video:thumbnail_loc><video:title>{core.esc(v["name"])}</video:title>'
                f'<video:description>{core.esc(v["desc"])}</video:description><video:content_loc>{SITE}{BASE}media/{v["slug"]}.mp4</video:content_loc>'
                f'<video:duration>{int(round(v["secs"]))}</video:duration><video:publication_date>{v["date"]}T00:00:00+02:00</video:publication_date>'
                f'<video:family_friendly>yes</video:family_friendly><video:uploader info="{MTG_SITE}">MTG</video:uploader></video:video>')
    key_of = {NAVD[k][1]: k for k in list(PAGES) + wkeys + pkeys}; key_of[''] = 'land'

    def itags(u):
        """the pictures of a page, for image search: its preview picture, and the covers of the videos it is the home of"""
        locs = [core.og_image(key_of[u]).split('?')[0]] + [t for c in vids.get(u, []) for t in core.video_thumbs(c)]
        return ''.join(f'<image:image><image:loc>{core.esc(x)}</image:loc></image:image>' for x in locs)
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n' + ''.join(
              f'<url><loc>{SITE}{BASE}{u}</loc><lastmod>{TODAY}</lastmod>{itags(u)}' + ''.join(vtag(c) for c in vids.get(u, [])) + '</url>\n' for u in urls)
          + f'<url><loc>{SITE}{ORDER}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>\n')
    open(base + '/sitemap.xml', 'w').write(sm)
    import llms
    order = [('land', '')]
    for k in PAGES:      # the tutorial pages come right after Tutorial Videos
        order.append((k, NAVD[k][1]))
        if k == 'tut':
            order += [(w, NAVD[w][1]) for w in wkeys]
        if k == 'exp':      # the presentation's page comes right after Explainer Videos
            order += [(w, NAVD[w][1]) for w in pkeys]
    llms.build_llms(dst, order)


def check(dst):
    bad = []
    for r, _, fs in os.walk(dst):
        for f in fs:
            if f.endswith(('.html', '.css', '.js', '.xml', '.txt', '.ics')):
                s = open(os.path.join(r, f), encoding='utf-8').read()
                for ch, nm in (('—', 'em dash'), ('–', 'en dash')):
                    if ch in s:
                        bad.append(f'{nm} in {os.path.join(r, f)}')
                for w in ('downline', 'recruits', 'downliner', 'guaranteed returns', 'ALTRUVA', 'altruva'):
                    if re.search(w, s):
                        bad.append(f'"{w}" in {os.path.join(r, f)}')
    return bad


def install(dst):
    """copy the built /bw and /bwcopy into the repo (keeps bw/_build)"""
    for name in (BASE.strip('/'), ORDER.strip('/')):
        tgt = REPO + '/' + name
        if os.path.exists(tgt):
            for x in os.listdir(tgt):
                if x != '_build':
                    p = tgt + '/' + x
                    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        os.makedirs(tgt, exist_ok=True)
        for x in os.listdir(dst + '/' + name):
            s, t = dst + '/' + name + '/' + x, tgt + '/' + x
            shutil.copytree(s, t) if os.path.isdir(s) else shutil.copy(s, t)


def render_preview(dst):
    """private review copy (relative links, lighter video), for MTG to tap through before anything goes live"""
    import posixpath
    core.MODE = 'preview'
    core.HASH.clear()
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst + '/assets', exist_ok=True)
    for f in sorted(os.listdir(SRC + '/assets')):
        shutil.copy(SRC + '/assets/' + f, dst + '/assets/' + f)
    shutil.copy(REPO + '/assets/video-return.js', dst + '/assets/video-return.js')
    os.makedirs(dst + '/img', exist_ok=True)
    for f in os.listdir(OUT + '/_img'):
        if not f.startswith('og-') and not f.endswith('-preview.jpg'):
            shutil.copy(OUT + '/_img/' + f, dst + '/img/' + f)
    os.makedirs(dst + '/media', exist_ok=True)
    for k, v in V.items():
        for suf in (('', '-1080p') if v['o'] == 'h' else ('',)):      # the review copy uses the same files as the live site
            shutil.copy(OUT + f'/_media/{v["slug"]}{suf}.mp4', dst + f'/media/{v["slug"]}{suf}.mp4')
    files = {}
    hd, body = landing()
    files['index.html'] = core.wrap_doc(hd, body, 'landing', main_page=True)
    for key, (title, fn, extra) in PAGES.items():
        here = NAVD[key][1]
        hd, content = core.dash_page(key, title, SEO_DESC[key], fn, [])
        if key == 'zoom':
            hd += zoom_head(here)
            os.makedirs(dst + '/' + here, exist_ok=True)
            open(dst + '/' + here + ZOOM_ICS, 'w', newline='').write(zoom_ics(SITE + BASE + here))
        files[here + 'index.html'] = core.wrap_doc(hd, content, 'dashpage')
    for code in WATCH_PAGES:
        key = 'w-' + code
        hd, content = core.dash_page(key, WATCH_PAGES[code][1], SEO_DESC[key], p_watch(code), [], parent='tut')
        files[NAVD[key][1] + 'index.html'] = core.wrap_doc(hd, content, 'dashpage')
    for code in PRESENT:
        key = 'w-' + code
        hd, content = core.dash_page(key, PRESENT[code][1], SEO_DESC[key], p_present(code), [], parent='exp')
        files[NAVD[key][1] + 'index.html'] = core.wrap_doc(hd, content, 'dashpage')
    hd, body = order_page('bwcopy/')
    files['bwcopy/index.html'] = core.wrap_doc(hd, body, 'landing orderpage')
    for path, html in files.items():
        d = posixpath.dirname(path) or '.'
        html = html.replace('href="/bwcopy/"', 'href="' + posixpath.relpath('bwcopy/index.html', d) + '"')
        html = html.replace('"/assets/video-return.js?v=1"', '"' + posixpath.relpath('assets/video-return.js', d) + '"')
        os.makedirs(dst + '/' + d, exist_ok=True)
        open(dst + '/' + path, 'w').write(html)
    core.MODE = 'prod'
    return sorted(files)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    if '--fast' not in sys.argv or not os.path.exists(OUT + '/_img'):
        if os.path.exists(OUT + '/_img'):
            shutil.rmtree(OUT + '/_img')
        images(OUT + '/_img')
    media(OUT + '/_media')
    render(OUT + '/prod')
    probs = check(OUT + '/prod')
    print('\n'.join(probs) if probs else 'CHECK OK: no dashes, no banned words')
    install(OUT + '/prod')
    print('installed into', REPO)
