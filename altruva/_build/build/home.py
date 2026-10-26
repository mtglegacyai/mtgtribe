"""mtgtribe.com home: a standalone "coming soon" page for the MTG TRIBE (MTG, 26 Oct 2026: "mtgtribe.com is a stand alone
home page. Make have a beautiful coming soon landing page"). The ALTRUVA guide stays at /altruva/.

v2 (26 Oct 2026, after MTG rejected the blueprint version): a sibling of the musathegiant.com home page, his design
reference: near black with an amber glow, Outfit display type with the silver and gold metallic fill, the glossy gold CTA
with the orbiting halo, the mono topic ticker, DM Sans text. Its own signature: glowing points (the tribe) rise from the
horizon and gather into the MTG crown around the headline, then stay connected like a network. One load sequence;
everything is static with reduced motion. Below the hero: the invite video in a tilted phone, the live ALTRUVA guide,
follow links and the signature footer."""
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
OUT_ROOT = '/home/claude/site/out/prod'   # for hashing files that live outside home/src (the ALTRUVA preview image)


def v(name):
    return f'/assets/{name}?v=' + hashlib.md5(open(f'{HOME_SRC}/{name}', 'rb').read()).hexdigest()[:8]


def vroot(path):
    return path + '?v=' + hashlib.md5(open(OUT_ROOT + path, 'rb').read()).hexdigest()[:8]


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


TICKER = [('▶', 'Tutorials'), ('◈', 'Explainers'), ('✦', 'Free tools'), ('◎', 'Websites built for you'), ('▲', 'Traffic strategies'),
          ('●', 'TikTok lives'), ('⟁', 'Action takers'), ('₿', 'Multiple streams of income'), ('♛', 'Lead with value')]


def page():
    core._used.clear()
    tick = ''.join(f'<span><b>{g}</b>{esc(t)}<em>/</em></span>' for g, t in TICKER)
    feats = [('graduation-cap', 'Tutorials, explainers, tips and strategies', 'Across different opportunities, not just one.'),
             ('globe', 'Websites built and duplicated for you', 'Like the ALTRUVA guide, with your own links built in.'),
             ('trending-up', 'Traffic strategies and sources', 'So the right people can actually find you.')]
    fl = ''.join(f'<li><span class="pi">{ic(i)}</span><span><b>{esc(t)}</b><span>{esc(s)}</span></span></li>' for i, t, s in feats)
    ext = ' target="_blank" rel="noopener"'
    follow = (f'<a class="chip" href="{esc(TIKTOK)}"{ext}>{ic("tiktok")}TikTok <span>@joinmtgtribe</span></a>'
              f'<a class="chip" href="{esc(WA_MTG)}"{ext}>{ic("message-circle")}WhatsApp MTG <span>{esc(WA_NUM)}</span></a>'
              f'<a class="chip" href="{esc(MTG_SITE)}"{ext}>{ic("globe")}MusaTheGiant.com</a>')
    join = (f'<span class="cta-w"><span class="halo" aria-hidden="true"></span><a class="cta" href="/group/">'
            f'<span class="wa">{ic("whatsapp")}</span>Join the MTG TRIBE{ic("arrow-right")}</a></span>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top"><nav class="wrap nav" aria-label="Main">
 <a class="brand" href="/" aria-label="MTG TRIBE home"><img src="{v("mtg-avatar.webp")}" alt="" width="38" height="38">MTG TRIBE <b aria-hidden="true">👑</b></a>
 <a class="ring" href="/altruva/">{ic("book-open-text")}<span>ALTRUVA<span class="m"> guide</span></span></a>
</nav></header>
<main id="main">
<section class="hero" id="hero" aria-labelledby="h1">
 <div class="grid" aria-hidden="true"></div><div class="spot" aria-hidden="true"></div>
 <div class="horizon" aria-hidden="true"></div>
 <canvas class="tribe" id="tribe" aria-hidden="true"></canvas>
 <div class="hero-in wrap">
  <p class="kicker" aria-label="Coming soon"><i class="dot"></i><span id="kick" aria-hidden="true">Coming soon</span></p>
  <h1 id="h1"><span class="l1">Home of the</span> <span class="l2">MTG TRIBE</span></h1>
  <p class="lede">Tutorials, explainers, free tools and honest guides by MTG, Your Digital Architect, all under one roof. The doors open soon, and the tribe is already gathering.</p>
  <div class="ctas">
   {join}
   <a class="ghost" href="#invite" id="watch"><span class="play"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5.2v13.6L19 12z" fill="currentColor"/></svg></span>Watch the invite <small>2:40</small></a>
  </div>
  <a class="live" href="/altruva/"><i aria-hidden="true"></i>Open now: <b>the ALTRUVA guide</b>{ic("arrow-right")}</a>
 </div>
 <div class="ticker" aria-hidden="true"><div class="track">{tick}{tick}</div></div>
</section>

<section class="invite" id="invite" aria-labelledby="inv-h">
 <div class="wrap inv">
  <div class="stage3d">
   <div class="phone" id="phone">
    <video id="vid" controls preload="none" playsinline poster="{v("mtg-tribe-invite-cover.webp")}" aria-label="Join the MTG TRIBE, an invite from MTG (2 minutes 40 seconds)">
     <source src="{v("mtg-tribe-invite.mp4")}" type="video/mp4">
    </video>
    <button class="vx" id="vx" type="button" aria-label="Close video" hidden>{ic("x")}</button>
   </div>
   <div class="floor" aria-hidden="true"></div>
  </div>
  <div class="inv-copy">
   <h2 id="inv-h">Meet the MTG TRIBE</h2>
   <p>A WhatsApp community for people who learn, take action and grow together. A tribe of action takers: we watch the videos, we do the work, then we teach someone else.</p>
   <ul class="feats">{fl}</ul>
   <div class="row">{join}</div>
  </div>
 </div>
</section>

<section class="open" aria-labelledby="open-h">
 <div class="wrap">
  <a class="guide" href="/altruva/">
   <span class="shot"><img src="{vroot("/altruva/img/og-land.jpg")}" alt="The ALTRUVA guide by MTG: see every dollar move before you move one" width="1200" height="630" loading="lazy" decoding="async"></span>
   <span class="gtxt"><span class="pill"><i aria-hidden="true"></i>Live now</span>
    <h2 id="open-h">The ALTRUVA guide by MTG</h2>
    <span class="p">{NV} short videos, free calculators and plain-English pages on how ALTRUVA works, from setting up your wallet to your first withdrawal.</span>
    <span class="go">Open the guide{ic("arrow-right")}</span></span>
  </a>
  <h2 class="fh">Follow along while the new home is built</h2>
  <div class="follow">{follow}</div>
 </div>
</section>
</main>
<footer class="foot"><div class="wrap">
 <p class="slog">We learn best when we teach others.</p>
 <p class="slog2">It pays to pay attention and take action.</p>
 <p class="sig">Let's Get This Crypto! 💪</p>
 <div class="fl"><strong>MTG 👑 | Your Digital Architect</strong><span><a href="{esc(MTG_SITE)}"{ext}>MusaTheGiant.com</a><a href="/altruva/">ALTRUVA guide</a><a href="/altruva/dashboard/disclaimer/">Disclaimer</a></span></div>
 <p class="fine">© 2026 MTG. Education only, not financial advice. Always do your own research.</p>
</div></footer>
<script>{JS}</script>'''


CSS = r'''
@property --ang{syntax:'<angle>';inherits:false;initial-value:0deg}
:root{--bg:#040506;--panel:#0a0c0f;--text:#f7f8fa;--body:#c3c7cd;--muted:#8a919b;--line:rgba(255,255,255,.08);
 --amber:#f2ad3c;--amber-l:#ffe2aa;--gold-t:#e8b862;--live:#3ddc84;
 --f-d:Outfit,'DM Sans',system-ui,sans-serif;--f-b:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;--f-m:'JetBrains Mono',ui-monospace,Menlo,monospace;
 --ease:cubic-bezier(.16,1,.3,1);color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/1.6 var(--f-b);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{width:100%;max-width:1180px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.ic{width:1.1em;height:1.1em;flex:none}
:focus-visible{outline:3px solid var(--amber-l);outline-offset:3px;border-radius:6px}
.skip{position:absolute;left:-999px;top:10px;z-index:50;padding:10px 14px;border-radius:10px;background:var(--amber);color:#1b1102;font-weight:800}
.skip:focus{left:12px}

/* header */
.top{position:absolute;top:0;left:0;right:0;z-index:20;padding-top:env(safe-area-inset-top,0px)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:12px;height:76px}
.brand{display:inline-flex;align-items:center;gap:12px;font:800 15px/1 var(--f-d);letter-spacing:.16em;white-space:nowrap}
.brand img{width:38px;height:38px;border-radius:50%;object-fit:cover;border:1.5px solid rgba(242,173,60,.75);box-shadow:0 0 0 3px rgba(242,173,60,.12),0 0 20px rgba(242,173,60,.25)}
.brand b{font-weight:400;letter-spacing:0}
.ring{position:relative;display:inline-flex;align-items:center;gap:8px;padding:11px 15px;border:1px solid rgba(242,173,60,.26);border-radius:11px;background:rgba(10,12,15,.7);color:var(--gold-t);font:800 12px/1 var(--f-b);letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;transition:background-color .2s,color .2s}
.ring::before{content:"";position:absolute;inset:-1px;border-radius:inherit;padding:1px;pointer-events:none;
 background:conic-gradient(from var(--ang),transparent 0 58%,#ffe3a3 74%,var(--amber) 82%,transparent 94%);
 -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box exclude,linear-gradient(#000 0 0)}
.ring:hover{background:rgba(242,173,60,.08);color:#ffd88f}

/* hero */
.hero{position:relative;min-height:100vh;min-height:100svh;display:grid;place-items:center;overflow:hidden;isolation:isolate;padding:104px 0 96px;
 background:radial-gradient(ellipse at 50% -12%,rgba(242,173,60,.15),transparent 36%),linear-gradient(180deg,#090b0d 0%,#050607 55%,#040506 100%)}
.grid,.spot,.horizon,.tribe{position:absolute;pointer-events:none}
.grid{inset:0;z-index:-3;background:linear-gradient(rgba(255,255,255,.022) 1px,transparent 1px) 0 0/64px 64px,linear-gradient(90deg,rgba(255,255,255,.022) 1px,transparent 1px) 0 0/64px 64px;
 -webkit-mask-image:linear-gradient(#000,transparent 92%);mask-image:linear-gradient(#000,transparent 92%)}
.spot{inset:0;z-index:-3;opacity:.75;background:linear-gradient(rgba(242,173,60,.2) 1px,transparent 1px) 0 0/64px 64px,linear-gradient(90deg,rgba(242,173,60,.2) 1px,transparent 1px) 0 0/64px 64px;
 -webkit-mask-image:radial-gradient(240px circle at var(--mx,50%) var(--my,40%),#000,transparent 75%);mask-image:radial-gradient(240px circle at var(--mx,50%) var(--my,40%),#000,transparent 75%)}
@media (hover:none){.spot{display:none}}
.horizon{z-index:-2;left:50%;top:calc(100% - 132px);width:max(1700px,180vw);height:1000px;transform:translateX(-50%);border-radius:50%;
 background:radial-gradient(ellipse 46% 26% at 50% 0%,rgba(242,173,60,.17),transparent 72%),#050607;
 box-shadow:0 -1px 0 rgba(255,214,138,.55),0 -14px 50px rgba(242,173,60,.2),0 -70px 170px rgba(242,173,60,.11)}
.tribe{inset:0;z-index:-1;width:100%;height:100%}
.hero-in{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center}
.kicker{position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:10px;margin:0 0 26px;padding:9px 16px;border:1px solid rgba(242,173,60,.3);border-radius:999px;
 background:rgba(13,15,18,.8);color:var(--gold-t);font:800 11.5px/1 var(--f-b);letter-spacing:.22em;text-transform:uppercase;font-variant-numeric:tabular-nums;
 -webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
.kicker .dot{width:7px;height:7px;border-radius:50%;background:var(--amber);box-shadow:0 0 0 4px rgba(242,173,60,.18),0 0 12px var(--amber)}
.kicker::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(242,173,60,.2) 50%,transparent 70%);transform:translateX(-120%)}
h1{margin:0;display:flex;flex-direction:column;align-items:center;font-family:var(--f-d);font-weight:800;line-height:.9;filter:drop-shadow(0 14px 44px rgba(242,173,60,.16))}
.l1{font-size:clamp(1.9rem,8vw,4.5rem);letter-spacing:-.045em;word-spacing:.1em;padding:0 .04em .12em;
 background:linear-gradient(180deg,#fff,#d8dadd 60%,#aeb2b8);-webkit-background-clip:text;background-clip:text;color:transparent}
.l2{font-size:clamp(3.3rem,17vw,9.6rem);word-spacing:.06em;letter-spacing:-.055em;padding:0 .06em .07em;
 background:linear-gradient(105deg,transparent 42%,rgba(255,246,222,.95) 49%,rgba(255,206,120,.9) 51%,transparent 58%) no-repeat,
  linear-gradient(180deg,#fff2d2 0%,#ffd47c 36%,#f2ad3c 64%,#c27a14 100%);
 background-size:260% 100%,100% 100%;background-position:170% 0,0 0;-webkit-background-clip:text;background-clip:text;color:transparent}
.lede{max-width:40rem;margin:30px auto 0;color:var(--body);font-size:clamp(1rem,1.45vw,1.15rem);line-height:1.7;text-wrap:pretty}
.ctas{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;margin-top:36px}
.cta-w{position:relative;display:inline-flex;border-radius:15px}
.halo{position:absolute;inset:-2px;border-radius:15px;z-index:0;filter:blur(1px);
 background:conic-gradient(from var(--ang),transparent 0 62%,rgba(255,214,138,.95) 76%,var(--amber) 82%,transparent 92%)}
.cta{position:relative;z-index:1;overflow:hidden;display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:60px;padding:13px 22px 13px 13px;
 border:1px solid rgba(255,214,138,.75);border-radius:14px;background:linear-gradient(180deg,#f6bd59 0%,#dfa02d 58%,#ca8318 100%);color:#1b1102;font:800 16.5px/1 var(--f-b);
 box-shadow:0 8px 0 rgba(113,67,6,.45),0 18px 40px rgba(0,0,0,.42),0 0 46px rgba(242,173,60,.24),inset 0 1px 0 rgba(255,255,255,.5),inset 0 -1px 0 rgba(92,53,0,.3);
 transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .18s ease}
.cta::after{content:"";position:absolute;top:0;bottom:0;left:-60%;width:40%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-18deg)}
.cta:active{transform:translateY(6px);box-shadow:0 2px 0 rgba(113,67,6,.45),0 8px 20px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.5)}
@media (hover:hover){.cta:hover{transform:translateY(-2px)}}
.cta .wa{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:linear-gradient(180deg,#3ce383,#17a552);color:#fff;
 box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 2px 6px rgba(70,35,0,.35)}
.cta .wa .ic{width:19px;height:19px}
.ghost{display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:60px;padding:12px 22px 12px 13px;border:1px solid rgba(242,173,60,.36);border-radius:14px;
 background:rgba(14,16,19,.75);color:var(--text);font:700 16px/1 var(--f-b);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);transition:border-color .2s,background-color .2s}
.ghost:hover{border-color:rgba(242,173,60,.7);background:rgba(242,173,60,.07)}
.ghost .play{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:linear-gradient(180deg,#ffd36e,#f2ad3c);color:#1b1102;
 box-shadow:0 0 0 4px rgba(242,173,60,.14),0 0 20px rgba(242,173,60,.35)}
.ghost .play .ic{width:16px;height:16px;margin-left:2px}
.ghost small{color:var(--muted);font:500 12px/1 var(--f-m);letter-spacing:.06em}
.live{display:inline-flex;align-items:center;gap:9px;margin-top:24px;padding:6px 2px;color:#a9afb7;font-size:14.5px;font-weight:600;transition:color .2s}
.live i{width:8px;height:8px;border-radius:50%;background:var(--live);box-shadow:0 0 0 4px rgba(61,220,132,.15),0 0 10px rgba(61,220,132,.6)}
.live b{color:var(--gold-t);font-weight:700}
.live .ic{width:15px;height:15px;color:var(--gold-t);transition:transform .2s}
.live:hover{color:var(--text)}.live:hover .ic{transform:translateX(3px)}
.ticker{position:absolute;left:0;right:0;bottom:0;height:46px;z-index:2;overflow:hidden;border-top:1px solid rgba(255,255,255,.06);background:rgba(4,5,6,.6);
 -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);-webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.track{display:flex;width:max-content;height:100%;align-items:center}
.track span{display:inline-flex;align-items:center;gap:10px;padding-left:26px;font:500 11px/1 var(--f-m);letter-spacing:.18em;text-transform:uppercase;color:#7f8690;white-space:nowrap}
.track b{color:var(--amber);font-weight:500}
.track em{font-style:normal;color:#3a3f46;padding-left:16px}

/* the invite */
.invite{position:relative;padding:120px 0 110px;background:radial-gradient(700px 420px at 25% 50%,rgba(242,173,60,.07),transparent 70%),linear-gradient(180deg,#040506,#07080a 45%,#060709)}
.inv{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:72px;align-items:center}
.stage3d{position:relative;display:grid;justify-items:center;perspective:1600px;padding-bottom:46px}
.phone{position:relative;width:min(300px,72vw);padding:10px;border-radius:44px;
 background:linear-gradient(150deg,#3b3427 0%,#161514 22%,#09090b 60%,#141210 100%);border:1px solid rgba(255,214,138,.42);
 box-shadow:34px 46px 90px rgba(0,0,0,.72),0 0 90px rgba(242,173,60,.17),inset 0 0 0 1px rgba(255,255,255,.04);
 transform:rotateY(-17deg) rotateX(6deg) rotateZ(2deg);transition:transform 1s var(--ease)}
.phone video{display:block;width:100%;max-width:100%;aspect-ratio:9/16;height:auto;border-radius:34px;background:#000;object-fit:cover}
.phone::after{content:"";position:absolute;inset:10px;border-radius:34px;pointer-events:none;transition:opacity .6s;
 background:linear-gradient(115deg,rgba(255,255,255,.15) 0%,rgba(255,255,255,.035) 26%,transparent 40%)}
.phone.playing{transform:none}
.phone.playing::after{opacity:0}
.vx{position:absolute;top:20px;right:20px;z-index:3;display:grid;place-items:center;width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.3);background:rgba(0,0,0,.65);color:#fff;cursor:pointer}
.vx[hidden]{display:none}
.vx .ic{width:18px;height:18px}
.floor{position:absolute;bottom:2px;left:50%;width:min(360px,84vw);height:50px;transform:translateX(-50%);border-radius:50%;
 border:1px solid rgba(242,173,60,.28);background:radial-gradient(ellipse,rgba(242,173,60,.26),transparent 70%)}
.inv-copy{min-width:0}
.inv-copy h2{margin:0 0 20px;font:800 clamp(2.3rem,4.8vw,3.9rem)/.98 var(--f-d);letter-spacing:-.04em;word-spacing:.1em;padding-bottom:.06em;text-wrap:balance;
 background:linear-gradient(180deg,#fff,#d8dadd 60%,#aeb2b8);-webkit-background-clip:text;background-clip:text;color:transparent}
.inv-copy>p{margin:0;max-width:34rem;color:var(--body);font-size:17px;line-height:1.7}
.feats{list-style:none;margin:34px 0 40px;padding:0;display:grid;gap:26px}
.feats li{display:flex;align-items:center;gap:20px}
.pi{position:relative;isolation:isolate;display:grid;place-items:center;width:52px;height:52px;flex:none;border-radius:16px;color:var(--amber);
 background:linear-gradient(180deg,#201a10,#0c0d10);border:1px solid rgba(242,173,60,.4);box-shadow:inset 0 1px 0 rgba(255,255,255,.09),0 10px 22px rgba(0,0,0,.5)}
.pi::after{content:"";position:absolute;left:-8px;right:-8px;bottom:-12px;height:15px;border-radius:50%;z-index:-1;border:1px solid rgba(242,173,60,.32);
 background:radial-gradient(ellipse,rgba(242,173,60,.22),transparent 70%)}
.pi .ic{width:23px;height:23px}
.feats b{display:block;font:700 17px/1.35 var(--f-b);color:var(--text)}
.feats li>span>span{display:block;color:var(--muted);font-size:14.5px;line-height:1.5}
.row{display:flex;flex-wrap:wrap;gap:12px}

/* open now */
.open{padding:20px 0 120px;background:#060709}
.guide{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);align-items:center;gap:48px;padding:22px 40px 22px 22px;border-radius:26px;
 border:1px solid rgba(242,173,60,.22);background:radial-gradient(640px circle at 0% 0%,rgba(242,173,60,.08),transparent 60%),linear-gradient(180deg,#0d0f12,#08090b);
 box-shadow:0 34px 90px rgba(0,0,0,.5);transition:border-color .25s}
.guide:hover{border-color:rgba(242,173,60,.5)}
.shot{display:block;border-radius:16px;overflow:hidden;border:1px solid rgba(110,170,255,.25);box-shadow:0 24px 60px rgba(0,30,90,.4)}
.shot img{width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;transition:transform .8s var(--ease)}
@media (hover:hover){.guide:hover .shot img{transform:scale(1.03)}}
.gtxt{display:block;min-width:0}
.pill{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;border:1px solid rgba(61,220,132,.35);background:rgba(61,220,132,.09);color:#8ff0bb;font:800 11px/1 var(--f-b);letter-spacing:.16em;text-transform:uppercase}
.pill i{width:7px;height:7px;border-radius:50%;background:var(--live);box-shadow:0 0 8px var(--live)}
.gtxt h2{margin:18px 0 12px;font:800 clamp(1.8rem,3.2vw,2.6rem)/1.02 var(--f-d);letter-spacing:-.03em;word-spacing:.08em;color:#fff;text-wrap:balance}
.gtxt .p{display:block;max-width:30rem;color:#b9bec5;font-size:16px;line-height:1.65}
.gtxt .go{display:inline-flex;align-items:center;gap:8px;margin-top:24px;color:var(--gold-t);font-weight:800}
.gtxt .go .ic{transition:transform .2s}
.guide:hover .go .ic{transform:translateX(4px)}
.fh{margin:64px 0 18px;text-align:center;font:700 15px/1.4 var(--f-b);color:var(--muted)}
.follow{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.chip{display:inline-flex;align-items:center;gap:10px;min-height:50px;padding:12px 18px;border-radius:13px;border:1px solid var(--line);background:rgba(255,255,255,.025);color:#e2e4e8;font-weight:700;font-size:15px;transition:border-color .2s,background-color .2s}
.chip span{color:var(--muted);font-weight:500}
.chip .ic{color:var(--gold-t)}
.chip:hover{border-color:rgba(242,173,60,.45);background:rgba(242,173,60,.05)}

/* footer */
.foot{padding:56px 0 calc(44px + env(safe-area-inset-bottom,0px));border-top:1px solid var(--line);background:linear-gradient(180deg,#07080a,#040506);text-align:center;color:var(--muted)}
.slog{margin:0;font:800 clamp(1.25rem,2.5vw,1.7rem)/1.25 var(--f-d);letter-spacing:-.015em;word-spacing:.08em;color:#eceef1;text-wrap:balance}
.slog2{margin:8px 0 0;font-size:15.5px;color:#a9afb7}
.sig{margin:12px 0 30px;font:800 18px/1.3 var(--f-b);color:var(--gold-t)}
.fl{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px 26px;font-size:14px}
.fl strong{color:#d7dade}
.fl span{display:inline-flex;flex-wrap:wrap;justify-content:center;gap:8px 20px}
.fl a:hover{color:var(--text)}
.fine{margin:14px 0 0;font-size:13px}

/* one load sequence (skipped with reduced motion) */
@media (prefers-reduced-motion:no-preference){
 .ring::before{animation:spin 6s linear infinite}
 .halo{animation:spin 4s linear infinite}
 .cta::after{animation:sheen 6s 3s ease-in-out infinite}
 .kicker{animation:up .9s .1s var(--ease) both}
 .kicker::after{animation:sheen2 1.6s 1s ease-out both}
 .kicker .dot{animation:pulse 2s ease-in-out infinite}
 .l1{animation:rise 1.1s .3s var(--ease) both}
 .l2{animation:rise 1.2s .5s var(--ease) both,sweep 1.8s 1.7s var(--ease) both}
 .lede{animation:up 1s 1s var(--ease) both}
 .hero .ctas{animation:up 1s 1.2s var(--ease) both}
 .live{animation:up 1s 1.4s var(--ease) both}
 .ticker{animation:fade 1.2s 1.8s both}
 .track{animation:tick 52s linear infinite}
 .horizon{animation:dawn 2.6s .2s ease-out both}
}
@keyframes spin{to{--ang:360deg}}
@keyframes up{from{opacity:0;transform:translateY(16px)}}
@keyframes rise{from{opacity:0;transform:translateY(.28em);filter:blur(12px)}}
@keyframes sweep{from{background-position:170% 0,0 0}to{background-position:-70% 0,0 0}}
@keyframes fade{from{opacity:0}}
@keyframes dawn{from{opacity:0;transform:translateX(-50%) translateY(60px)}}
@keyframes tick{to{transform:translateX(-50%)}}
@keyframes pulse{50%{box-shadow:0 0 0 7px rgba(242,173,60,.04),0 0 12px var(--amber)}}
@keyframes sheen{0%,80%{left:-60%}100%{left:140%}}
@keyframes sheen2{to{transform:translateX(120%)}}

@media (max-width:900px){
 .inv{grid-template-columns:minmax(0,1fr);gap:56px}
 .invite{padding:96px 0 90px}
 .phone{transform:rotateY(-10deg) rotateX(5deg) rotateZ(1.5deg)}
 .guide{grid-template-columns:minmax(0,1fr);gap:26px;padding:16px 16px 28px}
 .gtxt{padding:0 8px}
}
@media (max-width:560px){
 .nav{height:66px}
 .brand{font-size:13.5px;gap:10px}
 .brand img{width:34px;height:34px}
 .ring{padding:10px 12px;font-size:11px}
 .hero{padding:92px 0 150px}
 .horizon{top:calc(100% - 108px)}
 .follow{flex-direction:column;align-items:stretch;max-width:420px;margin:0 auto}
 .chip{justify-content:center}
 .kicker{margin-bottom:22px}
 .lede{margin-top:24px}
 .ctas{flex-direction:column;align-items:stretch;width:100%;max-width:420px;gap:14px}
 .cta-w,.cta,.ghost{width:100%}
 .feats li{align-items:flex-start}
 .row .cta-w{width:100%}
}
@media (max-width:380px){.ring .m{display:none}}
'''


# the tribe gathers into the crown: points rise from the horizon to the crown outline around the headline,
# stay gently alive and connect to drifting network points. Drawn once and left still with reduced motion.
JS = r'''
(function(){
var d=document,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var hero=d.getElementById('hero'),cv=d.getElementById('tribe'),h1=d.getElementById('h1'),cx=cv.getContext('2d');
var W=0,H=0,dpr=1,crown=[],gems=[],amb=[],t0=0,run=false,raf=0,px=0,py=0,ready=false;
var SH=[[.06,1],[0,.3],[.14,.58],[.27,.16],[.385,.52],[.5,0],[.615,.52],[.73,.16],[.86,.58],[1,.3],[.94,1],[.06,1]],PK=[1,3,5,7,9];
function rnd(a,b){return a+Math.random()*(b-a)}
function geom(){
 var r=hero.getBoundingClientRect(),b=h1.getBoundingClientRect();
 dpr=Math.min(window.devicePixelRatio||1,2);W=r.width;H=r.height;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
 var cw=Math.min(b.width*1.22,W*(W<640?.9:.96)),ch=Math.max(b.height*1.72,cw*.36),ox=b.left-r.left+b.width/2-cw/2,base=b.bottom-r.top+16,oy=base-ch;
 var P=SH.map(function(p){return[ox+p[0]*cw,oy+p[1]*ch]});
 var small=W<640,N=small?66:116,L=[],tot=0,i,k,pts=[];
 for(i=0;i<P.length-1;i++){L.push(Math.hypot(P[i+1][0]-P[i][0],P[i+1][1]-P[i][1]));tot+=L[i]}
 for(i=0;i<L.length;i++){var n=Math.max(2,Math.round(N*L[i]/tot));for(k=0;k<n;k++){var f=k/n;pts.push([P[i][0]+(P[i+1][0]-P[i][0])*f,P[i][1]+(P[i+1][1]-P[i][1])*f])}}
 crown=fit(crown,pts);
 gems=PK.map(function(j){return{x:P[j][0],y:P[j][1],big:j===5}});
 var na=small?24:48;
 if(amb.length!==na){amb=[];for(i=0;i<na;i++)amb.push({x:rnd(0,W),y:rnd(0,H*.92),vx:rnd(-.12,.12),vy:rnd(-.08,.08),a:rnd(.18,.45)})}
}
function fit(old,pts){
 if(old.length===pts.length){old.forEach(function(p,i){p.tx=pts[i][0];p.ty=pts[i][1]});return old}
 return pts.map(function(q){return{tx:q[0],ty:q[1],sx:q[0]+rnd(-.28,.28)*W,sy:H+rnd(20,160),dl:rnd(.15,1.15),ph:rnd(0,6.28),k:0,x:0,y:0}});
}
function place(list,t){
 for(var i=0;i<list.length;i++){var p=list[i],l=reduce?1:Math.min(1,Math.max(0,(t-p.dl)/1.9)),e=1-Math.pow(1-l,3),ex=l<.5?4*l*l*l:1-Math.pow(-2*l+2,3)/2;
  p.k=e;var w=reduce?0:Math.min(1,Math.max(0,t-p.dl-1.9))*1.5;
  p.x=p.sx+(p.tx-p.sx)*ex+Math.sin(t*.7+p.ph)*w+px*10;p.y=p.sy+(p.ty-p.sy)*e+Math.cos(t*.6+p.ph)*w+py*6}
}
function link(list,closed,alpha){
 for(var i=0;i<list.length-(closed?0:1);i++){var a=list[i],b=list[(i+1)%list.length],m=Math.min(a.k,b.k);if(m<.6)continue;
  cx.strokeStyle='rgba(242,173,60,'+(alpha*Math.pow((m-.6)/.4,2)).toFixed(3)+')';cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);cx.stroke()}
}
function draw(now){
 var t=reduce?9:(now-t0)/1000,i,j,a,b,dx,dy,dd;
 cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);cx.lineWidth=1;
 for(i=0;i<amb.length;i++){a=amb[i];if(!reduce){a.x+=a.vx;a.y+=a.vy;if(a.x<-20)a.x=W+20;if(a.x>W+20)a.x=-20;if(a.y<-20)a.y=H*.92;if(a.y>H*.92)a.y=-20}}
 for(i=0;i<amb.length;i++)for(j=i+1;j<amb.length;j++){a=amb[i];b=amb[j];dx=a.x-b.x;dy=a.y-b.y;dd=dx*dx+dy*dy;
  if(dd<13000){cx.strokeStyle='rgba(190,196,206,'+((1-dd/13000)*.1).toFixed(3)+')';cx.beginPath();cx.moveTo(a.x-px*4,a.y-py*3);cx.lineTo(b.x-px*4,b.y-py*3);cx.stroke()}}
 place(crown,t);
 for(i=0;i<crown.length;i+=3){a=crown[i];if(a.k<.9)continue;for(j=0;j<amb.length;j++){b=amb[j];dx=a.x-b.x;dy=a.y-b.y;dd=dx*dx+dy*dy;
  if(dd<9000){cx.strokeStyle='rgba(242,173,60,'+((1-dd/9000)*.14).toFixed(3)+')';cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x-px*4,b.y-py*3);cx.stroke()}}}
 link(crown,true,.5);
 for(i=0;i<amb.length;i++){a=amb[i];cx.fillStyle='rgba(205,210,220,'+a.a+')';cx.beginPath();cx.arc(a.x-px*4,a.y-py*3,1.1,0,6.283);cx.fill()}
 cx.fillStyle='rgba(255,222,165,.92)';
 for(i=0;i<crown.length;i++){a=crown[i];if(a.k<=0)continue;cx.globalAlpha=Math.min(1,a.k*1.4);cx.beginPath();cx.arc(a.x,a.y,1.6,0,6.283);cx.fill()}
 cx.globalAlpha=1;
 var g=reduce?1:Math.min(1,Math.max(0,(t-2.6)/.9));
 if(g>0)for(i=0;i<gems.length;i++){a=gems[i];var R=(a.big?22:15)*g*(.86+.14*Math.sin(t*1.8+i)),x=a.x+px*10,y=a.y+py*6;
  var gr=cx.createRadialGradient(x,y,0,x,y,R);gr.addColorStop(0,'rgba(255,214,138,'+(.55*g)+')');gr.addColorStop(1,'rgba(242,173,60,0)');
  cx.fillStyle=gr;cx.beginPath();cx.arc(x,y,R,0,6.283);cx.fill();cx.fillStyle='rgba(255,241,210,'+g+')';cx.beginPath();cx.arc(x,y,a.big?3.4:2.6,0,6.283);cx.fill()}
 if(run&&!reduce)raf=requestAnimationFrame(draw);
}
function start(){if(run||reduce)return;run=true;raf=requestAnimationFrame(draw)}
function stop(){run=false;cancelAnimationFrame(raf)}
function init(){geom();ready=true;t0=performance.now();if(reduce)draw(0);else start()}
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if(!ready)return;geom();if(reduce)draw(0)},150)});
if(d.fonts&&d.fonts.ready){var once=false,go=function(){if(!once){once=true;init()}};d.fonts.ready.then(go);setTimeout(go,1500)}else init();
if('IntersectionObserver'in window)new IntersectionObserver(function(e){if(!ready)return;e[0].isIntersecting?start():stop()}).observe(hero);
d.addEventListener('visibilitychange',function(){if(!ready)return;d.hidden?stop():start()});
hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();hero.style.setProperty('--mx',(e.clientX-r.left)+'px');hero.style.setProperty('--my',(e.clientY-r.top)+'px');
 px=(e.clientX-r.left)/r.width-.5;py=(e.clientY-r.top)/r.height-.5});

var kick=d.getElementById('kick');
if(!reduce){var fin=kick.textContent,gl='0123456789ABCDEF#$%&',st=performance.now()+300;
 (function f(now){var p=Math.max(0,(now-st)/1000),o='';for(var i=0;i<fin.length;i++){var c=fin[i];o+=(c===' '||p*fin.length*1.25>i+fin.length*.25*Math.random())?c:gl[(Math.random()*gl.length)|0]}
  kick.textContent=p>=1?fin:o;if(p<1)requestAnimationFrame(f)})(performance.now())}

var vid=d.getElementById('vid'),phone=d.getElementById('phone'),vx=d.getElementById('vx');
function reset(){phone.classList.remove('playing');vx.hidden=true;
 try{if(d.fullscreenElement&&d.exitFullscreen)d.exitFullscreen();if(vid.webkitDisplayingFullscreen&&vid.webkitExitFullscreen)vid.webkitExitFullscreen()}catch(e){}
 vid.load()}
vid.addEventListener('play',function(){phone.classList.add('playing');vx.hidden=false});
vid.addEventListener('ended',reset);
vx.addEventListener('click',function(){vid.pause();reset()});
d.getElementById('watch').addEventListener('click',function(e){e.preventDefault();
 phone.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});var p=vid.play();if(p&&p.catch)p.catch(function(){})});
})();
'''


def head():
    t, d = esc(TITLE), esc(DESC)
    og = SITE + v('og-home.jpg')
    alt = 'Home of the MTG TRIBE, coming soon: tutorials, explainers, free tools and honest guides by MTG, Your Digital Architect.'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="MTG">
<link rel="canonical" href="{SITE}/">
<meta name="theme-color" content="#040506">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website"><meta property="og:site_name" content="MTG TRIBE">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}/"><meta property="og:locale" content="en_ZA">
<meta property="og:image" content="{og}"><meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(alt)}">
<meta property="og:video" content="{SITE}/assets/mtg-tribe-invite.mp4"><meta property="og:video:type" content="video/mp4"><meta property="og:video:width" content="720"><meta property="og:video:height" content="1280">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{og}"><meta name="twitter:image:alt" content="{esc(alt)}">
<link rel="image_src" href="{og}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Outfit:wght@700;800&family=JetBrains+Mono:wght@500&display=swap">
<script>if(location.protocol==='http:'&&location.hostname==='mtgtribe.com')location.replace('https:'+location.href.slice(5));</script>
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld(), ensure_ascii=False, separators=(',', ':'))}</script>'''


def home_page(dst):
    """write dst/index.html and dst/assets/ (dst = repo root)"""
    os.makedirs(dst + '/assets', exist_ok=True)
    for f in os.listdir(HOME_SRC):
        shutil.copy(f'{HOME_SRC}/{f}', f'{dst}/assets/{f}')
    body = page().replace('{JS}', JS)
    html = f'<!doctype html>\n<html lang="en-ZA">\n<head>\n{head()}\n</head>\n<body>\n{core.sprite()}{body}\n</body>\n</html>\n'
    open(dst + '/index.html', 'w', encoding='utf-8').write(html)
    return dst + '/index.html'
