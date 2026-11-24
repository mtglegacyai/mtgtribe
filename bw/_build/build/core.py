"""Shared helpers: links, icons, components and page shells."""
import hashlib, html, json, os, re, posixpath
from config import *

ICON_DIR = SCR + '/npm/x/lucide-static-1.61.0/package/icons/'
BRAND_DIR = SCR + '/npm/x/simple-icons-16.37.0/package/icons/'
BRANDS = {'tiktok', 'whatsapp', 'youtube', 'facebook', 'binance', 'telegram'}

MODE = 'prod'          # 'prod' or 'preview'
HASH = {}              # asset content hashes (prod cache busting)
_used = set()          # icons used on the page being rendered


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- links
def L(target, here):
    """Link from page dir `here` (e.g. 'dashboard/faq/') to `target` (page dir like 'dashboard/' or a file
    like 'media/x.mp4', optional '#hash'). Prod: absolute /bw/... pretty URLs. Preview: relative files."""
    frag = ''
    if '#' in target:
        target, frag = target.split('#', 1)
        frag = '#' + frag
    if target.startswith('http') or target.startswith('mailto:'):
        return target + frag
    is_page = target == '' or target.endswith('/')
    if MODE == 'prod' and target.startswith('media/'):      # the videos live on Cloudflare R2 (config MEDIA_URL)
        return MEDIA_URL + target[6:] + ('?v=' + HASH[target] if target in HASH else '') + frag
    if MODE == 'prod':
        url = BASE + target
        if not is_page and target in HASH:
            url += '?v=' + HASH[target]
        return url + frag
    # preview: relative path to a file
    tgt = (target + 'index.html') if is_page else target
    rel = posixpath.relpath(tgt, here.rstrip('/') or '.')
    return rel + frag


def A(target, here):
    return esc(L(target, here))


# ---------------------------------------------------------------- icons
def _svg_inner(name):
    p = (BRAND_DIR if name in BRANDS else ICON_DIR) + name + '.svg'
    s = open(p).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '', s)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1).strip()
    return re.sub(r'\s+', ' ', inner)


def ic(name, cls='ic'):
    _used.add(name)
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def sprite():
    out = []
    for n in sorted(_used):
        if n in BRANDS:
            out.append(f'<symbol id="i-{n}" viewBox="0 0 24 24" fill="currentColor" stroke="none">{_svg_inner(n)}</symbol>')
        else:
            out.append(f'<symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                       f'stroke-linecap="round" stroke-linejoin="round">{_svg_inner(n)}</symbol>')
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            + ''.join(out) + '</defs></svg>')


# ---------------------------------------------------------------- components
def btn(label, href=None, kind='gold', icon=None, size='', ring=False, cls='', attrs='', ext=False):
    c = f'btn btn-{kind}' + (f' btn-{size}' if size else '') + (' ring' if ring else '') + (f' {cls}' if cls else '')
    inner = (ic(icon) if icon else '') + f'<span class="lbl">{label}</span>'
    if href:
        tgt = ' target="_blank" rel="noopener"' if ext else ''
        return f'<a class="{c}" href="{esc(href)}"{tgt} {attrs}>{inner}</a>'
    return f'<button type="button" class="{c}" {attrs}>{inner}</button>'


def copy_btn(kind='signup', label='Copy my sign-up link', style='gold', size='', ring=True, icon='copy', cls=''):
    c = f'btn btn-{style}' + (f' btn-{size}' if size else '') + (' ring' if ring else '') + (f' {cls}' if cls else '')
    return (f'<button type="button" class="{c}" data-copy="{kind}">{ic(icon)}<span class="lbl">{label}</span>'
            f'<span class="copied" aria-live="polite">Copied ✓</span></button>')


def wa_group_btn(size='', label='Join the MTG TRIBE', ring=False):
    return btn(label, GROUP, 'wa', 'whatsapp', size, ring, ext=True)


def valr_btn(size='sm', kind='ghost', label='Open a VALR account'):
    return btn(label, VALR, kind, 'landmark', size, ext=True)


def binance_btn(size='sm', kind='ghost', label='Open a Binance account'):
    return btn(label, BINANCE, kind, 'binance', size, ext=True)


def order_btn(label='Get your own marketing website', size='', kind='gold', ring=True):
    return btn(label, ORDER, kind, 'globe', size, ring)


def wa_mtg_btn(size='', label='WhatsApp MTG', kind='ghost'):
    from urllib.parse import quote
    return btn(label, WA_MTG + '?text=' + quote(WA_MTG_MSG), kind, 'message-circle', size, ext=True)


def chip(icon, text, cls=''):
    return f'<span class="chip {cls}">{ic(icon)}{text}</span>'


def chips(*items):
    return '<div class="chips">' + ''.join(chip(*i) for i in items) + '</div>'


def ped(icon, cls=''):
    return f'<span class="ped {cls}">{ic(icon)}</span>'


def think(q, body, alt=False, icon='message-circle'):
    return (f'<div class="think{" alt" if alt else ""}" role="note">{ped(icon)}<div><p class="q">{q}</p>'
            f'<div class="prose">{body}</div></div></div>')


def box(title, body, icon=None):
    return f'<div class="box"><h3 class="h3">{ic(icon) if icon else ""}{title}</h3>{body}</div>'


def checks(items, no=False):
    icn = 'circle-x' if no else 'circle-check'
    return f'<ul class="checks{" no" if no else ""}">' + ''.join(f'<li>{ic(icn)}<span>{i}</span></li>' for i in items) + '</ul>'


def steps(items):
    return '<ol class="steps">' + ''.join(f'<li><div><h3>{t}</h3>{b}</div></li>' for t, b in items) + '</ol>'


def table(head, rows, hl=None, caption=None):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    trs = ''
    for i, r in enumerate(rows):
        trs += f'<tr{" class=hl" if hl == i else ""}>' + ''.join(
            f'<td data-l="{esc(plain(head[j]))}">{c}</td>' if plain(head[j]) else f'<td class="rh">{c}</td>' for j, c in enumerate(r)) + '</tr>'
    cap = f'<caption class="sr">{caption}</caption>' if caption else ''
    return f'<div class="tbl-wrap"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def sec(body, title=None, lead=None, id=None, cls='', sr=None):
    """a page section. sr: a heading for screen readers and search only, where the design shows none (keeps h1, h2, h3 in order)"""
    head = f'<h2 class="sr">{sr}</h2>' if sr else ''
    if title:
        head = f'<div class="sec-head"><h2 class="h2">{title}</h2>' + (f'<p class="lead">{lead}</p>' if lead else '') + '</div>'
    i = f' id="{id}"' if id else ''
    return f'<section class="sec {cls}"{i}><div class="wrap">{head}{body}</div></section>'


def poster(code, here, size=720):
    """(big, small) poster of a video in its own shape: 720 and 360 wide for 9:16, 1280 and 640 wide for 16:9"""
    v = V[code]
    return L(f'img/{v["slug"]}.webp', here), L(f'img/{v["slug"]}-{"640" if v["o"] == "h" else "360"}.webp', here)


def cover(code, here):
    """(big, small) wide cover of a video, the one the page shows in the laptop frame: 1280 and 640 wide.
    A 16:9 video's cover is its poster; a 9:16 video has its own wide cover (config: wide)."""
    v = V[code]
    if v['o'] == 'h':
        return poster(code, here)
    return L(f'img/{v["slug"]}-wide.webp', here), L(f'img/{v["slug"]}-wide-640.webp', here)


BAR = {'t3': 'Activate slot 1'}      # a shorter name where the short name does not fit the bar of a 320 px phone with large text


def bar_text(v):
    """what the player's bar says beside the camera: the series and the short name ("Tutorial 2 · Buy BNB, send to SafePal")"""
    return f'{v["label"]} · {BAR.get(v["code"], v["short"])}' if v['code'][0] in 'tek' else v['title']


def player(wide=False, cover='', left='', right='', pid=''):
    """The one video player (MTG, 16 Nov 2026): the slim gold phone for a 9:16 video, the slim laptop for a 16:9 one.
    The screen has the video's own shape and nothing lies on the picture: the camera, Full Screen and Close sit in the
    bar above it. Styles: "VIDEO PLAYER" in bw.css. Behaviour: "video players" in bw.js."""
    return (f'<div class="pl {"pl-h" if wide else "pl-v"}"{f' id="{pid}"' if pid else ""}><div class="pl-dev"><div class="pl-bar">'
            f'<span class="pl-l"><span class="pl-tx">{left}</span>'
            f'<button type="button" class="pl-b pl-max" data-pl-max aria-label="Full Screen">{ic("maximize-2", "ic i-max")}{ic("minimize-2", "ic i-min")}'
            f'<span class="t t-max">Full Screen</span><span class="t t-min">Exit Full Screen</span></button></span>'
            f'<i class="pl-cam" aria-hidden="true"></i>'
            f'<span class="pl-r"><span class="pl-tx">{right}</span>'
            f'<button type="button" class="pl-b pl-x" data-pl-x aria-label="Close the video"><span class="t">Close</span>{ic("x")}</button></span>'
            f'</div><div class="pl-scr">{cover}</div></div><i class="pl-deck" aria-hidden="true"><i></i></i></div>')


def vid(code, here, cap=True, eager=False, hero=False):
    """A video on the page: ALWAYS a wide (16:9) cover inside the laptop frame (MTG, 17 Nov 2026: "all the videos must have a
    horizontal thumbnail and inside a laptop frame ... to save space and to make the website look smaller and easy to browse").
    - a 16:9 video plays in place, in that laptop;
    - a 9:16 video opens in the pop-up, in the phone frame ("they must be on a cell phone when they play").
    Either way it closes itself at the end and the page is back where the visitor pressed play.
    The bar shows what it is and how long; nothing covers the picture. hero: the pulsing play button."""
    v = V[code]
    big, small = cover(code, here)
    wide = v['o'] == 'h'
    fc = ''
    if cap:
        fc = (f'<figcaption class="vcap"><span><b>{v["title"]}</b><br>{v["label"]}, {mmss(v["secs"])}</span>'
              f'<span class="wbadge">{ic("circle-check")}Watched</span>'
              f'<button type="button" class="mark" data-mark="{code}">Mark as watched</button></figcaption>')
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    spot = f' style="--px:{v["spot"][0]}%;--py:{v["spot"][1]}%"' if v.get('spot') else ''
    if wide:        # plays in place: the light file for phones, the 1080p for big screens
        how = f'data-src="{esc(L("media/%s.mp4" % v["slug"], here))}" data-src-hd="{esc(L("media/%s-1080p.mp4" % v["slug"], here))}"'
    else:           # opens the pop-up's phone
        how = f'data-play="{code}"'
    img = (f'<img src="{esc(small)}" srcset="{esc(small)} 640w, {esc(big)} 1280w" sizes="(max-width:900px) 94vw, 640px" width="1280" height="720" '
           f'{load} decoding="async" alt="{esc(v["name"])}: video cover">')
    btn = (f'<button type="button" class="vplay{" pulse" if hero else ""}" {how} data-code="{code}"{spot} '
           f'aria-label="Play {esc(v["title"])} ({mmss(v["secs"])})"><span class="pbtn">{ic("play")}</span></button>')
    return (f'<figure class="vid vid16" data-vid="{code}">'
            f'{player(True, img + btn, esc(bar_text(v)), mmss(v["secs"]))}{fc}</figure>')


def wide_cover(code, here):
    """kept for older calls: every video is a wide cover in the laptop frame now (vid)"""
    return vid(code, here, cap=False, hero=True)


def clock(t):
    """a moment of a video the way its player shows it (seconds dropped, never rounded up): 88.7 is 1:28"""
    return f'{int(t) // 60}:{int(t) % 60:02d}'


def jump_card(code, at, title, text, here):
    """A "watch this part" card (MTG, 20 Nov 2026: the presentation on the pages it explains). The whole card is one button:
    it opens that video in the pop-up at that second. The picture is the video's own cover, so the card shows what plays."""
    v = V[code]
    big, small = cover(code, here)
    return (f'<button type="button" class="vjump glass" data-play="{code}" data-at="{at:.1f}" aria-label="Play {esc(v["title"])} from {clock(at)}: {esc(title)}">'
            f'<img src="{esc(small)}" width="640" height="360" loading="lazy" decoding="async" alt="">'
            f'<span class="vj-t"><small>{v["label"]} · from {clock(at)}</small><b>{title}</b><span>{text}</span></span>'
            f'<span class="btn btn-gold btn-sm">{ic("play")}<span class="lbl">Watch from {clock(at)}</span></span></button>')


def play_btn(code, label=None, kind='ghost', size='sm'):
    v = V[code]
    label = label or v['short']
    return (f'<button type="button" class="btn btn-{kind} btn-{size}" data-play="{code}">{ic("circle-play")}'
            f'<span class="lbl">{label}</span></button>')


def vlink(code, here):
    """inline text link that opens the video in the player sheet"""
    v = V[code]
    return f'<button type="button" class="inl linkbtn" data-play="{code}">Watch the {v["short"]} video</button>'


def video_data(here):
    """JSON for the pop-up player and the progress tiles (o: 'h' = 16:9, plays in the laptop; p and pb: the small and the big cover)"""
    d = {}
    for k, v in V.items():
        big, small = poster(k, here)
        d[k] = dict(t=v['title'], l=v['label'], st=v['short'], s=L(f'media/{v["slug"]}.mp4', here), p=small, pb=big, d=mmss(v['secs']))
        if v['o'] == 'h':
            d[k].update(o='h', hd=L(f'media/{v["slug"]}-1080p.mp4', here))
    return json.dumps(d, separators=(',', ':'))


# ---------------------------------------------------------------- head / SEO
def og_image(key):
    """absolute URL (with a content version) of a page's social preview thumbnail"""
    p = SCR + '/out/_img/' + (og_file(key) if key else 'x')
    if key and os.path.exists(p):
        return SITE + BASE + 'img/' + og_file(key) + '?v=' + hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    return SITE + BASE + 'img/og-bitcoin-wealth-guide.jpg'


def og_tags(full, desc, url, key, og_type='website'):
    from ogcfg import OG
    img = og_image(key)
    alt = full.split(' | ')[0] + '. ' + (OG[key][3] if key in OG and len(OG[key]) > 3 else 'Bitcoin Wealth guide by MTG')
    return (f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}">\n'
            f'<meta property="og:title" content="{esc(full)}"><meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{esc(url)}"><meta property="og:locale" content="en_ZA">\n'
            f'<meta property="og:image" content="{esc(img)}"><meta property="og:image:secure_url" content="{esc(img)}">\n'
            f'<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{esc(alt.strip())}">\n'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(full)}">\n'
            f'<meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{esc(img)}">\n'
            f'<meta name="twitter:image:alt" content="{esc(alt.strip())}"><link rel="image_src" href="{esc(img)}">')


PERSON_ID = SITE + BASE + '#mtg'
SITE_ID = SITE + BASE + '#site'
# what each page is, for search engines and AI assistants (schema.org page types)
PAGE_TYPE = {'tut': 'CollectionPage', 'exp': 'CollectionPage', 'home': 'CollectionPage'}
BW_THING = {'@type': 'Thing', 'name': 'Bitcoin Wealth', 'alternateName': ['BW', 'Bitcoin Wealth Vow Unity'],
                 'description': 'A Bitcoin matrix programme run by a smart contract on BNB Smart Chain: members enter once with 0.001 BTC (as BTCB) and payments move wallet to wallet.'}


def plain(s):
    """text without tags or entities, for structured data"""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def person_ld():
    return {'@type': 'Person', '@id': PERSON_ID, 'name': 'MTG', 'alternateName': ['MusaTheGiant', 'Musa the Giant'],
            'jobTitle': 'Your Digital Architect',
            'description': 'MTG, Your Digital Architect: creator of independent, plain-English crypto education, videos and free tools, and host of the MTG TRIBE community.',
            'url': MTG_SITE, 'sameAs': [MTG_SITE, TIKTOK, YOUTUBE, FACEBOOK, TELEGRAM],
            'knowsAbout': ['Bitcoin', 'Bitcoin Wealth', 'BTCB', 'Web3 wallets', 'SafePal', 'BNB Smart Chain', 'Crypto safety', 'Affiliate marketing']}


def head(title, desc, path, here, extra_ld=None, noindex=False, og_type='website', og_key=None):
    from seo import SEO_TITLE
    url = SITE + BASE + path
    full = SEO_TITLE.get(og_key) or (title if NAME in title else f'{title} | {NAME}')
    css = L('assets/bw.css', here)
    page = {'@type': PAGE_TYPE.get(og_key, 'WebPage'), '@id': url + '#webpage', 'url': url, 'name': full, 'description': desc,
            'inLanguage': 'en-ZA', 'isPartOf': {'@id': SITE_ID}, 'author': {'@id': PERSON_ID}, 'publisher': {'@id': PERSON_ID},
            'about': BW_THING, 'isAccessibleForFree': True, 'datePublished': LAUNCHED, 'dateModified': TODAY}
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': SITE_ID, 'url': SITE + BASE, 'name': NAME, 'alternateName': ['Bitcoin Wealth Guide', 'MTG Bitcoin Wealth', SITE_LABEL],
         'description': 'Independent, plain-English Bitcoin Wealth education by MTG: how it works, how to join safely, free tools, and how to check every payment on the blockchain.',
         'inLanguage': 'en-ZA', 'publisher': {'@id': PERSON_ID}, 'author': {'@id': PERSON_ID}},
        person_ld(), page,
    ]}
    for x in extra_ld or []:
        if x.get('@type') == 'BreadcrumbList':
            x['@id'] = url + '#breadcrumb'
            page['breadcrumb'] = {'@id': x['@id']}
        elif x.get('@type') == 'VideoObject':
            x['@id'] = url + '#video-' + x.pop('_code', str(len(ld['@graph'])))
            x['isPartOf'] = {'@id': url + '#webpage'}
            page.setdefault('video', []).append({'@id': x['@id']})
        elif x.get('@type') in ('FAQPage', 'HowTo', 'WebApplication', 'DefinedTermSet'):
            x.setdefault('@id', url + '#' + x['@type'].lower())
            page.setdefault('hasPart', []).append({'@id': x['@id']})
        ld['@graph'].append(x)
    fav = L('img/favicon-32.png', here)
    touch = L('img/apple-touch-icon.png', here)
    og = og_image(og_key)
    page['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': og, 'width': 1200, 'height': 630}
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="MTG">
<link rel="canonical" href="{esc(url)}">
<meta name="theme-color" content="#050705">
<meta name="color-scheme" content="dark">
{og_tags(full, desc, url, og_key, og_type)}
<link rel="icon" type="image/png" sizes="32x32" href="{esc(fav)}">
<link rel="apple-touch-icon" href="{esc(touch)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@500;600;700;800&family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@600;700&display=swap">
<link rel="stylesheet" href="{esc(css)}">
<script>if(location.protocol==='http:'&&location.hostname==='{HOST}')location.replace('https:'+location.href.slice(5));document.documentElement.classList.add('js');try{{if(localStorage.getItem('mtg-side')==='off'&&innerWidth>1060)document.documentElement.classList.add('side-off')}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(',', ':'))}</script>'''


def video_thumbs(code):
    """absolute URLs of a video's covers: the wide one first (search results show 16:9), then its own shape"""
    v = V[code]
    t = [SITE + BASE + f'img/{v["slug"]}.webp']
    if v['o'] != 'h':
        t.insert(0, SITE + BASE + f'img/{v["slug"]}-wide.webp')
    return t


def video_obj(code, here_url=None, extra=None):
    """schema.org VideoObject of a released video. extra: more properties (a watch page adds the transcript and key moments)"""
    v = V[code]
    o = {'@type': 'VideoObject', '_code': code, 'name': v['name'], 'description': v['desc'],
         'thumbnailUrl': video_thumbs(code), 'uploadDate': v['date'] + 'T00:00:00+02:00',
         'duration': iso_dur(v['secs']), 'contentUrl': MEDIA_URL + f'{v["slug"]}.mp4', 'encodingFormat': 'video/mp4', 'inLanguage': 'en-ZA',
         'isFamilyFriendly': True, 'isAccessibleForFree': True, 'author': {'@id': PERSON_ID}, 'publisher': {'@id': PERSON_ID},
         'about': BW_THING}
    if v['o'] != 'h':
        o.update(width=720, height=1280)
    else:
        o.update(width=1280, height=720)
    if code in WATCH:                     # the video's own page
        o['url'] = SITE + BASE + WATCH[code]
    if code[0] == 'p':                    # a promo video is shown by MTG, not made by him
        del o['author']
    o.update(extra or {})
    return o


def video_ld(codes, here):
    return [video_obj(k) for k in codes]


def crumbs_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + BASE + p} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- global overlays
def overlays(here):
    return f'''<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-h" hidden>
 <div class="sheet-in">
  <button type="button" class="x" data-close>Close {ic('x')}</button>
  <h2 id="sheet-h">{ic('circle-check')}<span data-k="title">Copied</span></h2>
  <p class="fine" data-k="sub"></p>
  <textarea class="linkbox" readonly rows="3" aria-label="The copied link"></textarea>
  <ol data-k="steps"></ol>
  <p class="fine" data-k="note"></p>
  <div class="btn-row" data-k="acts"></div>
 </div>
</div>
<div class="sheet player" id="player" role="dialog" aria-modal="true" aria-label="Video player" hidden>
 <div class="sheet-in">{player(pid='pl-pop')}</div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<button type="button" class="totop" id="totop" aria-label="Back to top"><svg class="tr" viewBox="0 0 52 52" aria-hidden="true"><circle class="bg" cx="26" cy="26" r="24"/><circle class="fg" cx="26" cy="26" r="24"/></svg>{ic('arrow-up')}</button>
<script>window.BW={json.dumps(dict(ref=REF, valr=VALR, binance=BINANCE, order=ORDER, join=L('dashboard/join/', here), tut=L('dashboard/tutorials/', here), wa=WA_MTG))};window.BWV={video_data(here)};</script>
<script src="{A('assets/bw.js', here)}" defer></script>
<script src="/assets/video-return.js?v=1" defer></script>
<script src="https://mtgtribe.com/assets/zoom-cta.js?v=5" defer></script>
<script src="https://mtgtribe.com/assets/wa-message.js?v=2" defer></script>'''


DISCLAIMER = ('<b>Independent guide.</b> This is not an official Bitcoin Wealth website. MTG is a Bitcoin Wealth member and made this guide '
              'to educate, not to advise: it is not financial advice and not a recommendation to join or not to join. '
              'The sign-up button carries MTG\'s referral link, so if you join through it, MTG becomes your sponsor and earns '
              'by the plan explained here. The VALR and Binance buttons are MTG\'s referral links too. Payouts come only from other members\' '
              'slot payments: nothing is guaranteed, and you can lose what you put in. Only use money you can afford to lose. '
              f'On-chain figures were read on {CHECKED} and change every day.')


def disc_block(here):
    return f'<p class="disc">{DISCLAIMER} <a href="{A("dashboard/disclaimer/", here)}">Read the full disclaimer</a>.</p>'


# ---------------------------------------------------------------- dashboard shell
def logo(here, cls='blogo'):
    return (f'<span class="{cls}"><img src="{A("img/bitcoin-wealth-logo-96.png", here)}" width="96" height="96" alt="Bitcoin Wealth logo">'
            f'<span class="bt"><b>Bitcoin Wealth</b><small>Guide by MTG 👑</small></span></span>')


def sidebar(key, here):
    out, group = [], None
    for k, p, label, sub, icon, g in NAV:
        if g != group:
            if group:
                out.append('</div>')
            out.append(f'<div class="sgroup" role="group" aria-label="{esc(g)}"><p class="slabel">{g}</p>')
            group = g
        cur = ' aria-current="page"' if k == key else ''
        if k in MENU_EXT:
            out.append(f'<a class="snav ext" href="{esc(MENU_EXT[k])}" target="_blank" rel="noopener"{cur}><span class="si">{ic(icon)}</span>'
                       f'<span class="stx"><b>{label}</b><small>{sub}</small></span>{ic("external-link", "ic xl")}'
                       f'<span class="sr">(opens in a new tab)</span></a>')
            continue
        out.append(f'<a class="snav" href="{A(p, here)}"{cur}><span class="si">{ic(icon)}</span>'
                   f'<span class="stx"><b>{label}</b><small>{sub}</small></span></a>')
    out.append('</div>')
    return f"""<aside class="side" id="side" aria-label="Dashboard menu">
 <a class="side-top" href="{A('', here)}" aria-label="Bitcoin Wealth guide home">{logo(here)}</a>
 <nav aria-label="Dashboard pages">{''.join(out)}</nav>
 <div class="side-bot">
  {copy_btn('signup', 'Copy sign-up link', size='sm')}
  <div class="srow"><a class="slink" href="{A('', here)}"><span aria-hidden="true">🏡</span>GO HOME</a><a class="slink" href="{esc(GROUP)}" target="_blank" rel="noopener">{ic('whatsapp')}MTG TRIBE</a></div>
  <div class="srow"><a class="slink" href="{esc(TIKTOK)}" target="_blank" rel="noopener">{ic('tiktok')}TikTok</a><a class="slink" href="{esc(YOUTUBE)}" target="_blank" rel="noopener">{ic('youtube')}YouTube</a></div>
  <div class="srow"><a class="slink" href="{esc(TELEGRAM)}" target="_blank" rel="noopener">{ic('telegram')}Telegram</a><a class="slink" href="{esc(FACEBOOK)}" target="_blank" rel="noopener">{ic('facebook')}Facebook</a></div>
  <div class="srow"><a class="slink" style="grid-column:1/-1" href="{A('dashboard/disclaimer/', here)}">{ic('info')}Disclaimer</a></div>
 </div>
</aside>
<button type="button" class="side-toggle" id="side-toggle" aria-controls="side" aria-expanded="true" aria-label="Hide the menu">{ic('chevron-left')}</button>
<div class="scrim" id="scrim"></div>"""


def topbar(key, here, parent=None):
    k, p, label, sub, icon, g = NAVD[key]
    crumb = f'<a href="{A("dashboard/", here)}">Dashboard</a>'
    if parent:          # a page under a menu page (a tutorial's own page under Tutorial Videos)
        crumb += f'{ic("chevron-right")}<a class="g" href="{A(NAVD[parent][1], here)}">{NAVD[parent][2]}</a>{ic("chevron-right")}<span>{label.split(":")[0]}</span>'
    elif key != 'home':
        crumb += f'{ic("chevron-right")}<span class="g">{g}</span>{ic("chevron-right")}<span>{label}</span>'
    return f"""<header class="dtop">
 <button type="button" class="menu-btn" id="menu-btn" aria-label="Menu" aria-controls="side" aria-expanded="false"><span class="bars" aria-hidden="true"></span><span class="mtx">Menu</span></button>
 <a class="dlogo" href="{A('', here)}" aria-label="Bitcoin Wealth guide home">{logo(here, 'blogo sm')}</a>
 <nav class="dcrumb" aria-label="Breadcrumb">{crumb}</nav>
 <div class="dtop-act">
  {copy_btn('signup', 'Sign Up', size='sm', icon='user-plus')}
  <a class="btn btn-ghost btn-sm tribepg" href="{A('dashboard/bw-tribe-page/', here)}">{ic('globe')}<span class="lbl">Your own website</span></a>
  <a class="btn btn-ghost btn-sm ring gohome" href="{A('', here)}"><span class="emo" aria-hidden="true">🏡</span><span class="lbl">GO HOME</span></a>
 </div>
</header>"""


def pager(key, here):
    keys = [n[0] for n in NAV if n[0] not in MENU_EXT]
    if key not in keys:
        return ''
    navs = [n for n in NAV if n[0] not in MENU_EXT]
    i = keys.index(key)
    out = '<nav class="pager" aria-label="Previous and next page">'
    if i > 0:
        pk = navs[i - 1]
        out += f'<a class="pg prev" href="{A(pk[1], here)}"><small>{ic("chevron-left")}Previous</small><b>{pk[2]}</b></a>'
    else:
        out += '<span></span>'
    if i < len(navs) - 1:
        nk = navs[i + 1]
        out += f'<a class="pg next" href="{A(nk[1], here)}"><small>Next{ic("chevron-right")}</small><b>{nk[2]}</b></a>'
    return out + '</nav>'


def next_band(here):
    return f"""<section class="sec"><div class="wrap"><div class="joinband glass">
 <div><h2 class="h3">Ready, or still have a question?</h2>
 <p>The sign-up button copies MTG's link and opens nothing, so you can paste it into SafePal's browser. Questions? Ask in the MTG TRIBE, or send MTG a WhatsApp message or voice note.</p></div>
 <div class="btn-row">{copy_btn('signup', 'Copy sign-up link')}{wa_group_btn(label='Ask the MTG TRIBE')}{wa_mtg_btn()}</div>
</div></div></section>"""


def dash_page(key, title, desc, body, here_extra_ld=None, show_band=True, parent=None):
    """parent: the menu page this page hangs under (lit in the menu, shown in the breadcrumb)"""
    k, path, label, sub, icon, g = NAVD[key]
    here = path
    global _used
    _used.clear()
    crumbs = ([('Bitcoin Wealth guide', ''), ('Dashboard', 'dashboard/')] + ([(NAVD[parent][2], NAVD[parent][1])] if parent else [])
              + ([] if key == 'home' else [(label, path)]))
    ld = [crumbs_ld(crumbs)] + (here_extra_ld or [])
    main = body(here) if callable(body) else body
    band = next_band(here) if show_band else ''
    content = f"""<div class="progress" aria-hidden="true"></div>
<div class="dash" id="dash">
{sidebar(parent or key, here)}
<div class="dmain">
{topbar(key, here, parent)}
<main id="main" tabindex="-1">
{main}
{band}
<div class="wrap">{pager(key, here)}</div>
</main>
<footer class="dfoot"><div class="wrap">
 {disc_block(here)}
 <div class="fbot"><span>© 2026 MTG 👑 | Your Digital Architect. <a class="inl" href="{esc(MTG_SITE)}" target="_blank" rel="noopener">MusaTheGiant.com</a></span><span class="sig">Let's Get This Crypto! 💪</span></div>
</div></footer>
</div>
</div>
{overlays(here)}"""
    hd = head(title, desc, path, here, ld, og_key=key)
    return hd, content


def tc(text):
    """Title Case for button labels (MTG, 14 Nov 2026): every word starts with a capital, hyphenated parts too.
    Words that are addresses (with a dot) and words already in capitals stay as they are."""
    def word(w):
        if not w or '.' in w.strip('.?!') or w.startswith('&'):
            return w
        return '-'.join(p[:1].upper() + p[1:] for p in w.split('-'))
    return ''.join(word(w) if not w.isspace() else w for w in re.split(r'(\s+)', text))


def title_buttons(html_):
    html_ = re.sub(r'(<span class="lbl">)([^<]*)(</span>)', lambda m: m.group(1) + tc(m.group(2)) + m.group(3), html_)
    return re.sub(r'(<button type="button" class="mark"[^>]*>)([^<]*)(</button>)', lambda m: m.group(1) + tc(m.group(2)) + m.group(3), html_)


def wrap_doc(hd, content, body_cls='', main_page=False):
    content = title_buttons(content)
    sp = sprite()
    body = f'<a class="skip" href="#main">Skip to content</a>{sp}{content}'
    if main_page and MODE == 'preview':
        # private preview page: the host adds the document skeleton, so keep our head tags at the top
        return f'{hd}\n<div class="{body_cls}">{body}</div>'
    return f'<!doctype html>\n<html lang="en-ZA">\n<head>\n{hd}\n</head>\n<body class="{body_cls}">\n{body}\n</body>\n</html>\n'
