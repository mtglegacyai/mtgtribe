"""Landing page: mtgtribe.com/altruva (a route map, no fluff)."""
from core import *


def station(n, icon, title, desc, main, subs, here, kind=''):
    """subs: list of (label, target) where target is a page path, 'play:t1', or an absolute URL"""
    links = ''
    for lab, t in subs:
        if t.startswith('play:'):
            links += f'<button type="button" class="wl" data-play="{t[5:]}">{ic("circle-play")}{lab}</button>'
        elif t.startswith('http'):
            links += f'<a class="wl" href="{esc(t)}" target="_blank" rel="noopener">{lab}</a>'
        else:
            links += f'<a class="wl" href="{A(t, here)}">{lab}</a>'
    where = f'<div class="where">{links}</div>' if links else ''
    dot = n if n else ''
    pc = {'branch': 'cy', 'wa': 'wa', 'end': ''}.get(kind, '')
    mhref = esc(main) if main.startswith('http') else A(main, here)
    ext = ' target="_blank" rel="noopener"' if main.startswith('http') else ''
    return (f'<li class="stn rv {kind}"><span class="dot" aria-hidden="true">{dot}</span><div class="card">{ped(icon, pc)}'
            f'<div class="tx"><a class="t" href="{mhref}"{ext}><b>{title}</b></a><span>{desc}</span>{where}</div>'
            f'<span class="go" aria-hidden="true">{ic("chevron-right")}</span></div></li>')


def landing():
    here = ''
    import core as _c; _c._used.clear()
    st = [
        station(1, 'compass', 'Start here', 'Your route and progress, an honest fit check, and what\'s different if you were let down before.',
                'dashboard/', [('Welcome', 'dashboard/'), ('Is it right for me?', 'dashboard/is-it-right-for-me/'), ('What makes it different', 'dashboard/what-makes-it-different/')], here),
        station(2, 'chart-pie', 'See where every dollar goes', 'The 100% split in one picture: 40, 25, 25, 5 and 5.',
                'dashboard/how-it-works/', [('The 100% split', 'dashboard/how-it-works/'), ('Explainer 1', 'play:e1')], here),
        station(3, 'layers', 'Understand each income', 'One short page and one short video for each part of the plan.',
                'dashboard/global-leg/', [('Global leg', 'dashboard/global-leg/'), ('Working levels', 'dashboard/working-levels/'),
                                          ('Level matching', 'dashboard/level-matching/'), ('Ranks and Lucky Tickets', 'dashboard/ranks-lucky-tickets/'),
                                          ('All explainers', 'dashboard/explainers/')], here),
        station(4, 'package', 'Pick your package', 'Starter $25, Builder $50 or Elite $100, side by side, with your shopping list.',
                'dashboard/packages/', [('Compare packages', 'dashboard/packages/')], here),
        station(5, 'rocket', 'Join step by step', 'Set up SafePal, fund it, join with the sign-up link, then tour your dashboard.',
                'dashboard/join/', [('Tutorial 1', 'play:t1'), ('Tutorial 2', 'play:t2'), ('Tutorial 3', 'play:t3'), ('Tutorial 7', 'play:t7')], here),
        station(6, 'timer', 'Use your first 72 hours', 'Just joined? Your clock has started: what may be waiting from minute one, why $100, and what two directs open.',
                'dashboard/first-72-hours/', [('Your first 72 hours', 'dashboard/first-72-hours/'), ('Explainer 7', 'play:e7')], here),
        station(7, 'calculator', 'Run your numbers', 'Four calculators that work on your phone. Your numbers, no promises.',
                'dashboard/tools/withdraw-split-calculator/', [('Withdraw split', 'dashboard/tools/withdraw-split-calculator/'), ('Working levels', 'dashboard/tools/working-level-calculator/'),
                                                              ('Matching', 'dashboard/tools/matching-calculator/'), ('USDT to rand', 'dashboard/tools/usdt-to-rand/')], here),
        station(8, 'wallet', 'Get your money out', 'Claim first, withdraw, cash out to your bank, and see how the reinvest split works.',
                'dashboard/withdraw-reinvest/', [('Explainer 6', 'play:e6'), ('Tutorial 4', 'play:t4'), ('Tutorial 5', 'play:t5'), ('Tutorial 6', 'play:t6')], here),
        station(9, 'shield-check', 'Answers and safety', 'Questions and myths, crypto words in plain English, and how to protect your wallet.',
                'dashboard/faq/', [('FAQ', 'dashboard/faq/'), ('Glossary', 'dashboard/glossary/'), ('Safety centre', 'dashboard/safety/')], here),
        station(10, 'download', 'Downloads', 'Every video, a two-page quick guide and a share message for your team.',
                'dashboard/downloads/', [('Videos and guide', 'dashboard/downloads/')], here),
        station(None, 'credit-card', 'Side trip: the crypto card', 'Spend your USDT with a crypto debit card. It has an income opportunity of its own.',
                'dashboard/crypto-card/', [('Crypto card', 'dashboard/crypto-card/')], here, 'branch'),
        station(None, 'message-circle', 'Side trip: the MTG TRIBE', 'A WhatsApp community for action takers. Ask questions and learn with others.',
                'dashboard/tribe/', [('WhatsApp group', WA_GROUP), ('TikTok', TIKTOK)], here, 'branch wa'),
    ]
    end = (f'<li class="stn end rv"><span class="dot" aria-hidden="true">{ic("flag")}</span><div class="card endcard">{ped("user-plus")}'
           f'<div class="tx"><b>Copy your sign-up link</b><span>When you\'re ready. The button copies MTG\'s link and opens nothing: paste it into your wallet\'s browser. '
           f'Introduced by someone else? Use their link.</span></div>{copy_btn("signup", "Copy sign-up link", size="sm")}</div></li>')
    route = f'<ol class="route" data-route><li class="fill" aria-hidden="true"></li>{"".join(st)}{end}</ol>'

    body = f'''<header class="ltop"><div class="wrap">
 <a class="brand" href="{A('', here)}" aria-label="ALTRUVA guide home"><img src="{A('img/altruva-logo-horizontal.png', here)}" width="616" height="144" alt="ALTRUVA"><span class="by"><b>Independent guide</b>by MTG 👑</span></a>
 <a class="btn btn-gold btn-sm ring" href="{A('dashboard/', here)}"><span class="emo" aria-hidden="true">📊</span><span class="lbl">Dashboard</span></a>
</div></header>
<main id="main" tabindex="-1">
<section class="hero"><div class="wrap hero-seq">
 <h1 class="h1">See every dollar move before you move a dollar.</h1>
 <p class="lead">The independent ALTRUVA guide by MTG. {NV} short videos and plain-English pages show how the plan pays, how to join safely and how money comes out. No promises. The full picture.</p>
 {chips(("film", f"{NV} videos, about {TOTAL_MIN} minutes"), ("package", "Top package $100"), ("info", "Independent, not official"))}
 <div class="stage ring" id="stage">
  <canvas aria-hidden="true"></canvas>
  <span class="soon">Coming soon</span>
  <div class="stage-in">
   <img class="em" src="{A('img/altruva-emblem-192.png', here)}" width="192" height="192" alt="">
   <h2>Your welcome video is on its way</h2>
   <p>A friendly tour: what ALTRUVA is, the words you'll hear, and exactly where to start in the dashboard.</p>
   {play_btn('e1', 'Watch Explainer 1 while you wait', 'blue')}
  </div>
 </div>
 <div class="hero-cta">
  <a class="btn btn-gold btn-lg ring" href="{A('dashboard/', here)}">{ic('layout-dashboard')}<span class="lbl">Enter the dashboard</span></a>
  <p class="sub">Free to learn. No sign-up needed to browse.</p>
 </div>
</div></section>
<section class="map" id="route"><div class="wrap">
 <div class="map-head"><h2 class="h2">Your route through ALTRUVA</h2><p class="lead">Every stop points to an exact page, video or download. Start at stop 1 and ride the line to the end.</p></div>
 {route}
 <div class="route-key"><span><i></i>Main route</span><span><i class="cy"></i>Side trips</span></div>
</div></section>
</main>
<footer class="lfoot"><div class="wrap">
 <div class="lfoot-top">
  <div class="about"><img src="{A('img/altruva-logo-horizontal.png', here)}" width="616" height="144" alt="ALTRUVA" loading="lazy"><p>Independent ALTRUVA education by MTG 👑 | Your Digital Architect.</p>
   <div class="socials"><a href="{esc(TIKTOK)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on TikTok">{ic('tiktok')}</a><a href="{esc(WA_GROUP)}" target="_blank" rel="noopener" aria-label="Join the MTG TRIBE WhatsApp group">{ic('whatsapp')}</a><a href="{esc(WA_MTG)}" target="_blank" rel="noopener" aria-label="WhatsApp MTG">{ic('message-circle')}</a></div></div>
  <div><h3>Learn</h3><ul><li><a href="{A('dashboard/', here)}">Dashboard</a></li><li><a href="{A('dashboard/explainers/', here)}">Explainer videos</a></li><li><a href="{A('dashboard/tutorials/', here)}">Tutorial videos</a></li><li><a href="{A('dashboard/faq/', here)}">FAQ</a></li><li><a href="{A('dashboard/glossary/', here)}">Glossary</a></li></ul></div>
  <div><h3>Tools</h3><ul><li><a href="{A('dashboard/tools/withdraw-split-calculator/', here)}">Withdraw Split Calculator</a></li><li><a href="{A('dashboard/tools/working-level-calculator/', here)}">Working Level Calculator</a></li><li><a href="{A('dashboard/tools/matching-calculator/', here)}">Matching Calculator</a></li><li><a href="{A('dashboard/tools/usdt-to-rand/', here)}">USDT to Rand Converter</a></li></ul></div>
  <div><h3>Connect</h3><ul><li><a href="{esc(WA_GROUP)}" target="_blank" rel="noopener">Join the MTG TRIBE</a></li><li><a href="{esc(WA_MTG)}" target="_blank" rel="noopener">WhatsApp MTG</a></li><li><a href="{esc(TIKTOK)}" target="_blank" rel="noopener">TikTok</a></li><li><a href="{A('dashboard/disclaimer/', here)}">Disclaimer</a></li></ul></div>
 </div>
 <p class="disc">{DISCLAIMER} Affiliate links: the ALTRUVA sign-up button and the <a href="{esc(CARD_GUIDE)}" target="_blank" rel="noopener">crypto card guide</a>. <a href="{A('dashboard/disclaimer/', here)}">Full disclaimer</a>.</p>
 <div class="fbot"><span>© 2026 MTG 👑 | Your Digital Architect. <a class="inl" href="{esc(MTG_SITE)}" target="_blank" rel="noopener">MusaTheGiant.com</a></span><span class="sig">Let's Get This Crypto! 💪</span></div>
</div></footer>
{overlays(here)}'''
    desc = (f'The independent ALTRUVA guide by MTG: {NV} short videos and plain-English pages on how the plan pays, '
            'how to join safely with SafePal and how money comes out. Top package $100. Free to learn.')
    hd = head('ALTRUVA Guide by MTG: plan, videos and how to join', desc, '', here)
    return hd, body
