"""mtgtribe.com home: a standalone "coming soon" page for the MTG TRIBE (MTG, 26 Oct 2026: "mtgtribe.com is a stand alone
home page. Make have a beautiful coming soon landing page"). The ALTRUVA guide stays at /altruva/.
Look: the MTG TRIBE identity from the invite video (black, charcoal, MTG gold, cream; WhatsApp green only on the join
button), drawn as an architect's sheet: blueprint grid, a crown-roofed building elevation and a title block."""
import hashlib, json, os, shutil
import core
from core import ic, esc
from config import SITE, BASE, TIKTOK, MTG_SITE, WA_MTG, WA_NUM, NV

HOME_SRC = '/home/claude/site/home/src'
TITLE = 'MTG TRIBE | Coming soon by MTG, Your Digital Architect'
DESC = ('The new home of the MTG TRIBE by MTG, Your Digital Architect, is coming soon. Join the tribe on WhatsApp, '
        'watch the invite video, or explore the ALTRUVA guide.')
VIDEO_SECS = 160.4
PUBLISHED = '2026-10-26'


def v(name):
    return f'/assets/{name}?v=' + hashlib.md5(open(f'{HOME_SRC}/{name}', 'rb').read()).hexdigest()[:8]


def ld():
    person = core.person_ld()
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'MTG TRIBE', 'alternateName': ['mtgtribe.com', 'MTG TRIBE by MTG'],
         'description': 'The home of the MTG TRIBE by MTG, Your Digital Architect: tutorials, explainers, free tools and honest guides.',
         'inLanguage': 'en-ZA', 'publisher': {'@id': SITE + '/#tribe'}, 'author': {'@id': core.PERSON_ID}},
        {'@type': 'Organization', '@id': SITE + '/#tribe', 'name': 'MTG TRIBE', 'url': SITE + '/',
         'description': 'A WhatsApp community for action takers who learn, take action and grow together, hosted by MTG.',
         'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/icon-512.png', 'width': 512, 'height': 512},
         'founder': {'@id': core.PERSON_ID}, 'sameAs': [TIKTOK]},
        person,
        {'@type': 'WebPage', '@id': SITE + '/#webpage', 'url': SITE + '/', 'name': TITLE, 'description': DESC, 'inLanguage': 'en-ZA',
         'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#tribe'}, 'author': {'@id': core.PERSON_ID},
         'datePublished': PUBLISHED, 'dateModified': PUBLISHED, 'video': {'@id': SITE + '/#invite'},
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + v('og-home.jpg'), 'width': 1200, 'height': 630}},
        {'@type': 'VideoObject', '@id': SITE + '/#invite', 'name': 'Join the MTG TRIBE: an invite from MTG',
         'description': 'MTG, Your Digital Architect, on what the MTG TRIBE is: a WhatsApp community for action takers, with tutorials, '
                        'explainers, tips and strategies across different opportunities, and how to join at mtgtribe.com/group.',
         'thumbnailUrl': [SITE + '/assets/mtg-tribe-invite-cover.webp'], 'uploadDate': PUBLISHED + 'T00:00:00+02:00',
         'duration': 'PT2M40S', 'contentUrl': SITE + '/assets/mtg-tribe-invite.mp4', 'encodingFormat': 'video/mp4',
         'inLanguage': 'en-ZA', 'isFamilyFriendly': True, 'author': {'@id': core.PERSON_ID}, 'publisher': {'@id': SITE + '/#tribe'}},
    ]}


# the new home as an architect's elevation: the invite video sits inside a building whose roof is the MTG crown.
# Built once on load (ground, walls rise, roof draws, gems land); static with reduced motion.
ROOF = ('<svg class="roof" viewBox="0 0 440 176" aria-hidden="true" focusable="false">'
        '<path class="r" pathLength="1" d="M1 175 L26 50 L118 120 L220 12 L322 120 L414 50 L439 175" />'
        '<path class="r eave" pathLength="1" d="M1 175 H439" />'
        '<circle class="gem" cx="26" cy="50" r="6" /><circle class="gem" cx="220" cy="12" r="8" /><circle class="gem" cx="414" cy="50" r="6" /></svg>')


def page():
    core._used.clear()
    wa = '/group/'
    links = [
        ('book-open-text', 'ALTRUVA guide', f'{NV} short videos, free calculators and plain-English pages on how ALTRUVA works.', '/altruva/', 'Open the guide', True, False),
        ('whatsapp', 'MTG TRIBE on WhatsApp', 'Learn with action takers, ask questions and share what works. You hear first when the new home opens.', wa, 'Join the group', False, False),
        ('tiktok', 'TikTok', 'Follow @joinmtgtribe for lives, tips and new videos.', TIKTOK, 'Follow', False, True),
        ('message-circle', 'WhatsApp MTG', f'Messages and voice notes work best: {WA_NUM}.', WA_MTG, 'Send a message', False, True),
        ('globe', 'MusaTheGiant.com', 'MTG\'s own website.', MTG_SITE, 'Visit', False, True),
    ]
    cards = ''
    for icn, t, d, href, act, feat, ext in links:
        tgt = ' target="_blank" rel="noopener"' if ext else ''
        cards += (f'<a class="card{" feat" if feat else ""}" href="{esc(href)}"{tgt}><span class="ci">{ic(icn)}</span>'
                  f'<span class="ct"><b>{esc(t)}</b>{"<em>Live now</em>" if feat else ""}<span>{esc(d)}</span></span>'
                  f'<span class="ca">{esc(act)}{ic("arrow-up-right" if ext else "arrow-right")}</span></a>')
    body = f'''<a class="skip" href="#main">Skip to content</a>
<header class="top wrap"><a class="brand" href="/" aria-label="MTG TRIBE home"><span class="crown" aria-hidden="true">👑</span><span>MTG TRIBE</span></a>
 <a class="toplink" href="/altruva/">ALTRUVA guide {ic("arrow-right")}</a></header>
<main id="main">
<section class="hero wrap">
 <div class="copy">
  <p class="pill">{ic("hammer")}Coming soon</p>
  <h1><span class="h1a">A new home for</span> <span class="h1b">the MTG TRIBE</span></h1>
  <p class="lead">Tutorials, explainers, free tools and honest guides by MTG, Your Digital Architect, all in one place. Built for action takers who learn, take action and grow together.</p>
  <div class="ctas">
   <a class="btn wa" href="{wa}">{ic("whatsapp")}Join the MTG TRIBE</a>
   <a class="btn ghost" href="/altruva/">{ic("book-open-text")}Explore the ALTRUVA guide</a>
  </div>
  <p class="hint">Join the WhatsApp group and you'll be the first to know when the new home opens.</p>
 </div>
 <div class="stage">
  <div class="house" role="img" aria-label="Architect's drawing of the new MTG TRIBE home: a building with a crown for a roof, with the invite video inside">
   {ROOF}
   <div class="walls"><i class="w l"></i><i class="w r"></i><i class="win l"></i><i class="win r"></i></div>
   <div class="ground"><span>Front elevation</span></div>
  </div>
  <figure class="phone">
   <video controls preload="none" playsinline poster="{v("mtg-tribe-invite-cover.webp")}" aria-label="Watch: Join the MTG TRIBE, an invite from MTG (2 minutes 40 seconds)">
    <source src="{v("mtg-tribe-invite.mp4")}" type="video/mp4">
   </video>
   <figcaption>{ic("circle-play")}Meet the MTG TRIBE <span>2:40</span></figcaption>
  </figure>
 </div>
 <dl class="block" aria-label="Title block">
  <div><dt>Project</dt><dd>mtgtribe.com</dd></div>
  <div><dt>Architect</dt><dd>MTG 👑</dd></div>
  <div><dt>Status</dt><dd class="st"><i></i>Under construction</dd></div>
  <div><dt>Open now</dt><dd><a href="/altruva/">ALTRUVA guide</a></dd></div>
 </dl>
</section>
<section class="more wrap" aria-labelledby="more-h">
 <h2 id="more-h">While the new home is being built</h2>
 <div class="cards">{cards}</div>
</section>
</main>
<footer class="foot wrap">
 <p class="slog">We learn best when we teach others.</p>
 <p class="sig">Let's Get This Crypto! 💪</p>
 <p class="fine"><span>© 2026 MTG 👑 | Your Digital Architect</span> <a href="{esc(MTG_SITE)}" target="_blank" rel="noopener">MusaTheGiant.com</a></p>
 <p class="fine">Education only, not financial advice. Always do your own research.</p>
</footer>'''
    return body


CSS = '''
/* Layout: an architect's drawing sheet. Copy left, the crown-roofed building and the invite video right; links below. */
:root{
 --ink:#09090c; --char:#121218; --panel:#18181f; --line:#2a2720; --grid:rgba(233,185,73,.07);
 --gold:#e9b949; --gold-l:#fae296; --gold-d:#aa7622; --cream:#f6efde; --mute:#a29d93; --wa:#25d366; --wa-d:#0e784a;
 --display:'Orbitron',system-ui,sans-serif; --body:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;
 color-scheme:dark;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ink);color:var(--cream);font:500 16px/1.6 var(--body);min-height:100vh;
 background-image:radial-gradient(900px 520px at 18% -8%,rgba(233,185,73,.16),transparent 70%),
  linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
 background-size:auto,40px 40px,40px 40px}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
.ic{width:1.1em;height:1.1em;flex:none;vertical-align:-.15em}
a{color:inherit}
.skip{position:absolute;left:-999px;top:8px;background:var(--gold);color:#1b1200;padding:8px 12px;border-radius:8px;font-weight:700;z-index:9}
.skip:focus{left:12px}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-block:18px}
.brand{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font:800 18px/1 var(--display);letter-spacing:.14em;color:var(--gold)}
.brand .crown{font-size:24px}
.toplink{display:inline-flex;align-items:center;gap:6px;text-decoration:none;font-weight:700;font-size:14px;color:var(--mute);padding:8px 12px;border:1px solid var(--line);border-radius:999px}
.toplink:hover{color:var(--cream);border-color:var(--gold-d)}
.hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);grid-template-areas:'copy stage' 'block stage';column-gap:48px;row-gap:28px;padding-block:20px 40px}
.copy{grid-area:copy;min-width:0;align-self:end}
main{overflow-x:clip}
.pill{display:inline-flex;align-items:center;gap:8px;margin:0;padding:7px 14px;border:1px solid rgba(233,185,73,.55);border-radius:999px;color:var(--gold);font:700 13px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;background:rgba(233,185,73,.06)}
h1{margin:20px 0 18px;font-family:var(--display);font-weight:800;line-height:1.04;letter-spacing:.01em;text-wrap:balance}
.h1a{display:block;font-size:clamp(28px,4.6vw,50px);color:var(--cream)}
.h1b{display:block;font-size:clamp(40px,7vw,78px);background:linear-gradient(180deg,var(--gold-l),var(--gold) 55%,var(--gold-d));-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 0 40px rgba(233,185,73,.25)}
.lead{margin:0;max-width:56ch;color:#d9d3c5;font-size:17px}
.ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font:800 16px/1 var(--body);padding:16px 22px;border-radius:14px;transition:transform .15s,background-color .15s,border-color .15s}
.btn .ic{width:20px;height:20px}
.btn.wa{background:var(--wa);color:#03230f;box-shadow:0 10px 30px rgba(37,211,102,.22)}
.btn.wa:hover{background:#3ee07a}
.btn.ghost{color:var(--gold);border:1.5px solid rgba(233,185,73,.6)}
.btn.ghost:hover{border-color:var(--gold);background:rgba(233,185,73,.08)}
@media (hover:hover){.btn:hover{transform:translateY(-1px)}}
.btn:focus-visible,.card:focus-visible,.toplink:focus-visible,.brand:focus-visible,.block a:focus-visible{outline:3px solid var(--gold-l);outline-offset:3px}
.hint{margin:14px 0 0;color:var(--mute);font-size:14px}
.stage{grid-area:stage;position:relative;min-width:0;justify-self:center;width:calc(var(--ph) + 2 * var(--strip) + 4px);
 display:grid;grid-template-columns:minmax(0,1fr);--strip:clamp(26px,7vw,64px);--ph:min(280px,calc(100vw - 40px - 2 * var(--strip) - 4px))}
.house{grid-area:1/1;display:grid;grid-template-rows:auto 1fr auto;pointer-events:none}
.roof{display:block;width:100%;height:auto;aspect-ratio:440/176;overflow:visible}
.roof .r{fill:none;stroke:var(--gold);stroke-width:2;stroke-linejoin:round;vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:0}
.roof .eave{stroke:var(--gold-d)}
.roof .gem{fill:var(--gold-l)}
.walls{position:relative}
.walls .w{position:absolute;top:0;bottom:0;width:2px;background:var(--gold);transform-origin:50% 100%}
.walls .w.l{left:0}.walls .w.r{right:0}
.walls .win{position:absolute;top:34px;bottom:26px;width:calc(var(--strip) * .46);opacity:.4;
 background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 32'%3E%3Cg fill='none' stroke='%23e9b949' stroke-width='1.2'%3E%3Crect x='1' y='1' width='18' height='20'/%3E%3Cpath d='M10 1v20M1 11h18'/%3E%3C/g%3E%3C/svg%3E") center top/100% auto repeat-y}
.walls .win.l{left:calc(var(--strip) * .27)}.walls .win.r{right:calc(var(--strip) * .27)}
.ground{position:relative;height:2px;margin-inline:calc(var(--strip) * -.5);background:var(--gold);margin-bottom:34px}
.ground::after{content:"";position:absolute;left:calc(var(--strip) * .5);right:calc(var(--strip) * .5);top:12px;border-top:1px dashed var(--gold-d)}
.ground span{position:absolute;left:50%;top:5px;transform:translateX(-50%);padding:0 8px;background:var(--ink);font:700 10px/1.4 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--gold-d);white-space:nowrap;z-index:1}
.phone{grid-area:1/1;align-self:end;justify-self:center;position:relative;margin:calc((var(--ph) + 2 * var(--strip) + 4px) * .4 + 12px) 0 36px;width:var(--ph);padding:9px;border-radius:34px;background:#0d0d11;border:2px solid var(--gold);
 box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 0 6px rgba(233,185,73,.08),0 0 60px rgba(233,185,73,.16)}
.phone video{display:block;width:100%;max-width:100%;aspect-ratio:9/16;height:auto;border-radius:26px;background:#000;object-fit:cover}
.phone figcaption{display:flex;align-items:center;justify-content:center;gap:8px;padding:9px 4px 3px;font-weight:700;font-size:14px;color:var(--cream)}
.phone figcaption span{color:var(--mute);font-weight:600}
.phone figcaption .ic{color:var(--gold)}
@media (prefers-reduced-motion:no-preference){
 .ground{animation:spread .6s cubic-bezier(.3,.7,.3,1) both}
 .walls .w{animation:rise .8s .35s cubic-bezier(.3,.7,.3,1) both}
 .walls .win{animation:fade .8s 1.1s ease-out both}
 .roof .r{animation:draw 1.3s 1s cubic-bezier(.6,.1,.2,1) both}
 .roof .eave{animation-delay:.9s;animation-duration:.6s}
 .roof .gem{transform-box:fill-box;transform-origin:center;animation:land .5s 2.1s cubic-bezier(.3,1.6,.5,1) both}
}
@keyframes spread{from{transform:scaleX(0)}}
@keyframes rise{from{transform:scaleY(0)}}
@keyframes fade{from{opacity:0}}
@keyframes draw{from{stroke-dashoffset:1}}
@keyframes land{from{transform:scale(0)}}
.block{grid-area:block;align-self:start;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));width:min(440px,100%);border:1.5px solid var(--gold-d);background:rgba(9,9,12,.85)}
.block div{padding:9px 12px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);min-width:0}
.block div:nth-child(2n){border-right:0}.block div:nth-child(n+3){border-bottom:0}
.block dt{font:700 10px/1.2 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--gold-d)}
.block dd{margin:3px 0 0;font-weight:700;font-size:14px;color:var(--cream);overflow-wrap:anywhere}
.block dd a{color:var(--gold)}
.block .st{display:flex;align-items:center;gap:7px}
.block .st i{width:8px;height:8px;flex:none;border-radius:50%;background:var(--gold);box-shadow:0 0 0 4px rgba(233,185,73,.18)}
@media (prefers-reduced-motion:no-preference){.block .st i{animation:pulse 1.8s ease-in-out infinite}}
@keyframes pulse{50%{box-shadow:0 0 0 7px rgba(233,185,73,.05)}}
.more{padding-block:30px 10px}
.more h2{margin:0 0 18px;font:800 clamp(20px,3vw,26px)/1.2 var(--display);letter-spacing:.03em;text-wrap:balance}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.card{display:flex;flex-direction:column;gap:12px;text-decoration:none;padding:18px;border-radius:16px;background:var(--char);border:1px solid var(--line);transition:border-color .15s,background-color .15s;min-width:0}
.card:hover{border-color:var(--gold-d);background:#16161d}
.card.feat{grid-column:1/-1;flex-direction:row;align-items:center;gap:18px;background:linear-gradient(120deg,rgba(233,185,73,.14),rgba(233,185,73,.03) 60%),var(--char);border-color:rgba(233,185,73,.45)}
.ci{display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:rgba(233,185,73,.1);color:var(--gold);flex:none}
.ci .ic{width:22px;height:22px}
.card:nth-child(2) .ci{background:rgba(37,211,102,.12);color:var(--wa)}
.ct{display:flex;flex-direction:column;gap:4px;min-width:0;flex:1}
.ct b{font-size:16px;color:var(--cream)}
.ct em{font-style:normal;align-self:flex-start;font:700 11px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:#1b1200;background:var(--gold);padding:5px 8px;border-radius:6px}
.ct span{color:var(--mute);font-size:14px}
.ca{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--gold);margin-top:auto}
.feat .ca{margin-top:0;white-space:nowrap}
.feat .ct b{font-size:19px}
.foot{padding-block:40px 34px;text-align:center}
.slog{margin:0;font:800 clamp(17px,2.4vw,22px)/1.3 var(--display);color:var(--cream);letter-spacing:.02em}
.sig{margin:8px 0 18px;font-weight:800;color:var(--gold);font-size:18px}
.fine{margin:4px 0;color:var(--mute);font-size:13px;display:flex;flex-wrap:wrap;justify-content:center;gap:6px 14px}
.fine a{color:var(--gold)}
@media (max-width:900px){
 .hero{grid-template-columns:minmax(0,1fr);grid-template-areas:'copy' 'stage' 'block';row-gap:30px;padding-top:8px}
 .block{justify-self:center}
 .cards{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:560px){
 .toplink{display:none}
 .btn{width:100%;justify-content:center}
 .cards{grid-template-columns:1fr}
 .card.feat{flex-direction:column;align-items:flex-start}
}
'''


def head():
    t, d = esc(TITLE), esc(DESC)
    og = SITE + v('og-home.jpg')
    alt = 'MTG TRIBE: a new home for the MTG TRIBE, coming soon.'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="MTG">
<link rel="canonical" href="{SITE}/">
<meta name="theme-color" content="#09090c">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website"><meta property="og:site_name" content="MTG TRIBE">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}/"><meta property="og:locale" content="en_ZA">
<meta property="og:image" content="{og}"><meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{alt}">
<meta property="og:video" content="{SITE}/assets/mtg-tribe-invite.mp4"><meta property="og:video:type" content="video/mp4"><meta property="og:video:width" content="720"><meta property="og:video:height" content="1280">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{og}"><meta name="twitter:image:alt" content="{alt}">
<link rel="image_src" href="{og}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Orbitron:wght@700;800&display=swap">
<script>if(location.protocol==='http:'&&location.hostname==='mtgtribe.com')location.replace('https:'+location.href.slice(5));</script>
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld(), ensure_ascii=False, separators=(',', ':'))}</script>'''


def home_page(dst):
    """write dst/index.html and dst/assets/ (dst = repo root)"""
    os.makedirs(dst + '/assets', exist_ok=True)
    for f in os.listdir(HOME_SRC):
        shutil.copy(f'{HOME_SRC}/{f}', f'{dst}/assets/{f}')
    body = page()
    html = f'<!doctype html>\n<html lang="en-ZA">\n<head>\n{head()}\n</head>\n<body>\n{core.sprite()}{body}\n</body>\n</html>\n'
    open(dst + '/index.html', 'w', encoding='utf-8').write(html)
    return dst + '/index.html'
