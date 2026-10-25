"""Shared helpers: links, icons, components and page shells."""
import hashlib, html, json, os, re, posixpath
from config import *

ICON_DIR = '/tmp/assets/x/lucide-static-1.61.0/package/icons/'
BRAND_DIR = '/tmp/assets/si/package/icons/'
BRANDS = {'tiktok', 'whatsapp'}

MODE = 'prod'          # 'prod' or 'preview'
HASH = {}              # asset content hashes (prod cache busting)
_used = set()          # icons used on the page being rendered


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- links
def L(target, here):
    """Link from page dir `here` (e.g. 'dashboard/faq/') to `target` (page dir like 'dashboard/' or a file
    like 'media/x.mp4', optional '#hash'). Prod: absolute /altruva/... pretty URLs. Preview: relative files."""
    frag = ''
    if '#' in target:
        target, frag = target.split('#', 1)
        frag = '#' + frag
    if target.startswith('http') or target.startswith('mailto:'):
        return target + frag
    is_page = target == '' or target.endswith('/')
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
    return btn(label, WA_GROUP, 'wa', 'whatsapp', size, ring, ext=True)


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
    return (f'<aside class="think{" alt" if alt else ""}">{ped(icon)}<div><p class="q">{q}</p>'
            f'<div class="prose">{body}</div></div></aside>')


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
        trs += f'<tr{" class=hl" if hl == i else ""}>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    cap = f'<caption class="sr">{caption}</caption>' if caption else ''
    return f'<div class="tbl-wrap"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def sec(body, title=None, lead=None, id=None, cls=''):
    head = ''
    if title:
        head = f'<div class="sec-head"><h2 class="h2">{title}</h2>' + (f'<p class="lead">{lead}</p>' if lead else '') + '</div>'
    i = f' id="{id}"' if id else ''
    return f'<section class="sec {cls}"{i}><div class="wrap">{head}{body}</div></section>'


def poster(code, here, size=720):
    v = V[code]
    return L(f'img/{v["slug"]}.webp', here), L(f'img/{v["slug"]}-360.webp', here)


def vid(code, here, cap=True):
    v = V[code]
    big, small = poster(code, here)
    src = L(f'media/{v["slug"]}.mp4', here)
    fc = ''
    if cap:
        fc = (f'<figcaption class="vcap"><span><b>{v["title"]}</b><br>{v["label"]}, {mmss(v["secs"])}</span>'
              f'<span class="wbadge">{ic("circle-check")}Watched</span>'
              f'<button type="button" class="mark" data-mark="{code}">Mark as watched</button></figcaption>')
    return (f'<figure class="vid" data-vid="{code}"><div class="vbox">'
            f'<img src="{esc(small)}" srcset="{esc(small)} 360w, {esc(big)} 720w" sizes="(max-width:760px) 90vw, 340px" '
            f'width="720" height="1280" loading="lazy" decoding="async" alt="">'
            f'<button type="button" class="vplay" data-src="{esc(src)}" data-code="{code}" '
            f'aria-label="Play {esc(v["title"])} ({mmss(v["secs"])})">'
            f'<span class="pbtn">{ic("play")}</span><span class="dur">{mmss(v["secs"])}</span></button>'
            f'</div>{fc}</figure>')


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
    """JSON for the modal player and the progress tiles"""
    d = {}
    for k, v in V.items():
        big, small = poster(k, here)
        d[k] = dict(t=v['title'], l=v['label'], st=v['short'], s=L(f'media/{v["slug"]}.mp4', here), p=small, d=mmss(v['secs']))
    return json.dumps(d, separators=(',', ':'))


# ---------------------------------------------------------------- head / SEO
def og_image(key):
    """absolute URL (with a content version) of a page's social preview thumbnail"""
    p = f'/home/claude/site/img/og-{key}.jpg'
    if key and os.path.exists(p):
        return SITE + BASE + f'img/og-{key}.jpg?v=' + hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
    return SITE + BASE + 'img/og-altruva-guide.jpg'


def og_tags(full, desc, url, key, og_type='website'):
    from ogcfg import OG
    img = og_image(key)
    alt = full.split(' | ')[0] + '. ' + (OG[key][3] if key in OG else '')
    return (f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}">\n'
            f'<meta property="og:title" content="{esc(full)}"><meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{esc(url)}"><meta property="og:locale" content="en_ZA">\n'
            f'<meta property="og:image" content="{esc(img)}"><meta property="og:image:secure_url" content="{esc(img)}">\n'
            f'<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{esc(alt.strip())}">\n'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(full)}">\n'
            f'<meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{esc(img)}">\n'
            f'<meta name="twitter:image:alt" content="{esc(alt.strip())}"><link rel="image_src" href="{esc(img)}">')


def head(title, desc, path, here, extra_ld=None, noindex=False, og_type='website', og_key=None):
    url = SITE + BASE + path
    full = title if NAME in title else f'{title} | {NAME}'
    css = L('assets/altruva.css', here)
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': SITE + BASE + '#site', 'url': SITE + BASE, 'name': NAME, 'inLanguage': 'en-ZA',
         'publisher': {'@id': SITE + BASE + '#mtg'}},
        {'@type': 'Person', '@id': SITE + BASE + '#mtg', 'name': 'MTG', 'alternateName': 'MusaTheGiant',
         'description': 'Your Digital Architect', 'url': MTG_SITE, 'sameAs': [TIKTOK, MTG_SITE]},
        {'@type': 'WebPage', '@id': url, 'url': url, 'name': full, 'description': desc, 'inLanguage': 'en-ZA',
         'isPartOf': {'@id': SITE + BASE + '#site'}, 'author': {'@id': SITE + BASE + '#mtg'},
         'dateModified': TODAY},
    ]}
    if extra_ld:
        ld['@graph'] += extra_ld
    fav = L('img/favicon-32.png', here)
    touch = L('img/apple-touch-icon.png', here)
    og = og_image(og_key)
    ld['@graph'][2]['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': og, 'width': 1200, 'height': 630}
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{esc(url)}">
<meta name="theme-color" content="#01081b">
<meta name="color-scheme" content="dark">
{og_tags(full, desc, url, og_key, og_type)}
<link rel="icon" type="image/png" sizes="32x32" href="{esc(fav)}">
<link rel="apple-touch-icon" href="{esc(touch)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Orbitron:wght@700;800&display=swap">
<link rel="stylesheet" href="{esc(css)}">
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('mtg-side')==='off'&&innerWidth>1060)document.documentElement.classList.add('side-off')}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(',', ':'))}</script>'''


def video_ld(codes, here):
    out = []
    for k in codes:
        v = V[k]
        out.append({'@type': 'VideoObject', 'name': f'ALTRUVA {v["label"]}: {v["title"]}', 'description': v['desc'],
                    'thumbnailUrl': SITE + BASE + f'img/{v["slug"]}.webp', 'uploadDate': '2026-10-24',
                    'duration': iso_dur(v['secs']), 'contentUrl': SITE + BASE + f'media/{v["slug"]}.mp4',
                    'inLanguage': 'en-ZA', 'author': {'@id': SITE + BASE + '#mtg'}})
    return out


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
<div class="sheet player" id="player" role="dialog" aria-modal="true" aria-labelledby="player-h" hidden>
 <div class="sheet-in">
  <div class="phead"><h2 id="player-h"><span data-k="title"></span></h2><button type="button" class="xbtn" data-close aria-label="Close the video">{ic('x')}</button></div>
  <div class="vbox"><video controls playsinline preload="none"></video></div>
  <div class="prow"><button type="button" class="mark" data-mark="">Mark as watched</button><span class="wbadge">{ic('circle-check')}Watched</span><button type="button" class="btn btn-ghost btn-sm" data-close>{ic('x')}<span class="lbl">Close video</span></button></div>
 </div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<button type="button" class="totop" id="totop" aria-label="Back to top"><svg class="tr" viewBox="0 0 52 52" aria-hidden="true"><circle class="bg" cx="26" cy="26" r="24"/><circle class="fg" cx="26" cy="26" r="24"/></svg>{ic('arrow-up')}</button>
<script>window.ALT={json.dumps(dict(ref=REF, login=LOGIN, join=L('dashboard/join/', here), t3=L('dashboard/tutorials/#t3', here), tut=L('dashboard/tutorials/', here)))};window.ALTV={video_data(here)};</script>
<script src="{A('assets/altruva.js', here)}" defer></script>'''


DISCLAIMER = ('<b>Independent guide.</b> This is not an official ALTRUVA website. MTG is an ALTRUVA member and made this guide '
              'to educate, not to advise: it is not financial advice and not a recommendation to join or not to join. '
              'The sign-up button carries MTG\'s referral link, so if you join through it, MTG becomes your sponsor and earns '
              'by the plan explained here. The top package is $100. Crypto and smart contracts carry real risk: only use money '
              'you can afford to lose. Figures were checked against the live app on 24 Oct 2026 and can change.')


def disc_block(here):
    return f'<p class="disc">{DISCLAIMER} <a href="{A("dashboard/disclaimer/", here)}">Read the full disclaimer</a>.</p>'


# ---------------------------------------------------------------- dashboard shell
def sidebar(key, here):
    out, group = [], None
    for k, p, label, sub, icon, g in NAV:
        if g != group:
            if group:
                out.append('</div>')
            out.append(f'<div class="sgroup" role="group" aria-label="{esc(g)}"><p class="slabel">{g}</p>')
            group = g
        cur = ' aria-current="page"' if k == key else ''
        vid_attr = ''
        out.append(f'<a class="snav" href="{A(p, here)}"{cur}{vid_attr}><span class="si">{ic(icon)}</span>'
                   f'<span class="stx"><b>{label}</b><small>{sub}</small></span></a>')
    out.append('</div>')
    return f'''<aside class="side" id="side" aria-label="Dashboard menu">
 <a class="side-top" href="{A('', here)}" aria-label="ALTRUVA guide home"><img src="{A('img/altruva-logo-horizontal.png', here)}" width="616" height="144" alt="ALTRUVA"><span>Independent guide by MTG 👑</span></a>
 <nav aria-label="Dashboard pages">{''.join(out)}</nav>
 <div class="side-bot">
  {copy_btn('signup', 'Copy sign-up link', size='sm')}
  <div class="srow"><a class="slink" href="{A('', here)}"><span aria-hidden="true">🏡</span>GO HOME</a><a class="slink" href="{esc(WA_GROUP)}" target="_blank" rel="noopener">{ic('whatsapp')}MTG TRIBE</a></div>
  <div class="srow"><a class="slink" href="{A('dashboard/disclaimer/', here)}">{ic('info')}Disclaimer</a><a class="slink" href="{esc(TIKTOK)}" target="_blank" rel="noopener">{ic('tiktok')}TikTok</a></div>
 </div>
</aside>
<button type="button" class="side-toggle" id="side-toggle" aria-controls="side" aria-expanded="true" aria-label="Hide the menu">{ic('chevron-left')}</button>
<div class="scrim" id="scrim"></div>'''


def topbar(key, here):
    k, p, label, sub, icon, g = NAVD[key]
    crumb = f'<a href="{A("dashboard/", here)}">Dashboard</a>'
    if key != 'home':
        crumb += f'{ic("chevron-right")}<span class="g">{g}</span>{ic("chevron-right")}<span>{label}</span>'
    return f'''<header class="dtop">
 <button type="button" class="menu-btn" id="menu-btn" aria-controls="side" aria-expanded="false"><span class="bars" aria-hidden="true"></span><span class="mtx">Menu</span></button>
 <a class="dlogo" href="{A('', here)}" aria-label="ALTRUVA guide home"><img src="{A('img/altruva-logo-horizontal.png', here)}" width="616" height="144" alt="ALTRUVA"><img class="em" src="{A('img/altruva-emblem-100.png', here)}" width="100" height="100" alt="ALTRUVA"></a>
 <nav class="dcrumb" aria-label="Breadcrumb">{crumb}</nav>
 <div class="dtop-act">
  {copy_btn('signup', 'Sign Up', size='sm', icon='user-plus')}
  {copy_btn('login', 'Login', style='ghost', size='sm', ring=False, icon='log-in', cls='login')}
  <a class="btn btn-ghost btn-sm ring gohome" href="{A('', here)}"><span class="emo" aria-hidden="true">🏡</span><span class="lbl">GO HOME</span></a>
 </div>
</header>'''


def pager(key, here):
    keys = [n[0] for n in NAV]
    if key not in keys:
        return ''
    i = keys.index(key)
    out = '<nav class="pager" aria-label="Previous and next page">'
    if i > 0:
        pk = NAV[i - 1]
        out += f'<a class="pg prev" href="{A(pk[1], here)}"><small>{ic("chevron-left")}Previous</small><b>{pk[2]}</b></a>'
    else:
        out += '<span></span>'
    if i < len(NAV) - 1:
        nk = NAV[i + 1]
        out += f'<a class="pg next" href="{A(nk[1], here)}"><small>Next{ic("chevron-right")}</small><b>{nk[2]}</b></a>'
    return out + '</nav>'


def next_band(here):
    return f'''<section class="sec"><div class="wrap"><div class="joinband">
 <div><h2 class="h3">Ready, or still have a question?</h2>
 <p>The sign-up button copies MTG's link and opens nothing, so you can paste it into your wallet's browser. Questions? Ask in the MTG TRIBE, or send MTG a WhatsApp message or voice note.</p></div>
 <div class="btn-row">{copy_btn('signup', 'Copy sign-up link')}{wa_group_btn(label='Ask the MTG TRIBE')}{wa_mtg_btn()}</div>
</div></div></section>'''


def dash_page(key, title, desc, body, here_extra_ld=None, show_band=True):
    k, path, label, sub, icon, g = NAVD[key]
    here = path
    global _used
    _used.clear()
    crumbs = [('ALTRUVA guide', ''), ('Dashboard', 'dashboard/')] + ([] if key == 'home' else [(label, path)])
    ld = [crumbs_ld(crumbs)] + (here_extra_ld or [])
    main = body(here) if callable(body) else body
    band = next_band(here) if show_band else ''
    content = f'''<div class="progress" aria-hidden="true"></div>
<div class="dash" id="dash">
{sidebar(key, here)}
<div class="dmain">
{topbar(key, here)}
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
{overlays(here)}'''
    hd = head(title, desc, path, here, ld, og_key=key)
    return hd, content


def wrap_doc(hd, content, body_cls='', main_page=False):
    sp = sprite()
    body = f'<a class="skip" href="#main">Skip to content</a>{sp}{content}'
    if main_page and MODE == 'preview':
        # artifact main page: the host adds the skeleton; keep our head tags at the top
        return f'{hd}\n<div class="{body_cls}">{body}</div>'
    return f'<!doctype html>\n<html lang="en-ZA">\n<head>\n{hd}\n</head>\n<body class="{body_cls}">\n{body}\n</body>\n</html>\n'
