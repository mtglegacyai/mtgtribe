"""ClickBaitPays Guide by MTG (mtgtribe.com/cbp): lean static site builder.

python3 cbp/_build/build.py            builds /cbp/ and /cbpcopy/ into the repo
python3 cbp/_build/og.py               renders the social preview images (needs Playwright)

One source of truth for every fact, price and link (CONFIG below). Pages: landing, dashboard (tutorials and explainers),
calculator, disclaimer and privacy, and the order form for personal copies. Videos are placeholders until MTG approves
each one: set `src` (and `poster`) on a video below and it becomes playable everywhere.
"""
import hashlib, html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # repo root
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
BRAND = os.path.join(ROOT, 'tools', 'cbp', 'brand')

# ============================================================== CONFIG (facts checked 21 and 22 November 2026)
SITE = 'https://mtgtribe.com'
BASE = '/cbp/'
ORDER = '/cbpcopy/'
NAME = 'ClickBaitPays Guide by MTG'
TODAY = '2026-11-22'
CHECKED = '21 November 2026'          # level figures read in the back office (Level 4 recording)

OWNER = {                              # a personal copy changes only this block
    'name': 'MTG', 'ref': 'https://clickbaitpays.me/join.php?ref=mtgtraffic', 'code': 'mtgtraffic',
    'wa': 'https://wa.me/27721714626', 'wa_num': '072 171 4626',
}
OFFICIAL = 'https://clickbaitpays.me/'
LOGIN = 'https://clickbaitpays.me/login.php'
OFFICIAL_FAQ = 'https://clickbaitpays.me/questions.php'
GROUP = 'https://mtgtribe.com/group/'
SOCIAL = [('tiktok', 'TikTok @joinmtgtribe', 'https://www.tiktok.com/@joinmtgtribe'),
          ('youtube', 'YouTube @mtgtribe', 'https://www.youtube.com/@mtgtribe'),
          ('whatsapp', 'MTG TRIBE on WhatsApp', GROUP),
          ('telegram', 'Telegram @mtgtribe', 'https://t.me/mtgtribe'),
          ('facebook', 'Facebook mtgtribe', 'https://www.facebook.com/mtgtribe')]
CBP_YT = 'https://www.youtube.com/@clickbaitpaysus'
PRICE_ZAR, PRICE_USD = 1000, 50

# level, campaign price, one-time activation, per click (the 90% members receive), clicks a day, campaign total (site's own)
LEVELS = [(1, 13, 1, 0.48, 3, 17.17), (2, 77, 7, 2.83, 3, 101.74), (3, 150, 15, 5.40, 3, 194.40),
          (4, 300, 30, 6.48, 5, 388.80), (5, 600, 60, 10.80, 6, 777.60), (6, 1200, 120, 12.96, 10, 1555.20),
          (7, 2400, 240, 13.50, 20, 3240.00)]

# videos: code, kind, title, one line, orientation ('h' 16:9 laptop, 'v' 9:16 phone), status, learn points, src, poster
TOUR = ('tour', 'Site tour', 'How to use this guide, click by click', 'A two-minute walk through this guide: where everything is and the order to watch the tutorials.', 'h', 'soon', [], '', '')
TUTORIALS = [
    ('t1', 'Tutorial 1', 'Your ClickBaitPays back office: a quick tour', 'Every menu item, so you always know where things are.', 'h', 'record',
     ['Your dashboard stats explained', 'Buy Ad Campaigns, Activate Earnings and Buy Login Ads', 'Click Ads, Saved Ads and Click History', 'Deposit, Withdraw, Purchase History and Pay It Forward'], '', ''),
    ('t2', 'Tutorial 2', 'How to deposit into ClickBaitPays', 'Fund your account through the Deposit page, safely.', 'h', 'record',
     ['Enter the USDT amount on the Deposit page', 'Pay through NOWPayments', 'Copy the new address every time, never reuse one', 'Wait for the confirmation'], '', ''),
    ('t3', 'Tutorial 3', 'Your first campaign on a new level: buy it, activate earning, click your daily ads', 'MTG buys a Level 4 campaign, activates Level 4 once and clicks his 5 ads.', 'h', 'soon',
     ['Log in and the 30-second login ad', 'Buy a Level 4 campaign: title, link and Preview', 'Activate Level 4 earning once (30 USDT)', 'Click your 5 daily ads and save the ones you like'], '', ''),
    ('t4', 'Tutorial 4', 'Buy another campaign on a level you already activated', 'Why the second campaign at a level needs no activation fee.', 'h', 'soon',
     ['No activation fee the second time', 'Two campaigns, two tabs on Click Ads', 'Your daily routine for 12 days', 'The 7-day hold, then your Available Balance'], '', ''),
    ('t5', 'Tutorial 5', 'How to request a withdrawal', 'Move your Available Balance to your own wallet.', 'h', 'record',
     ['Withdrawals are requested once a week', 'The 10 USDT minimum and the 10% fee', 'Your wallet address and Security PIN', 'What happens after you request'], '', ''),
    ('t6', 'Tutorial 6', 'How to create a Login Ad', 'Every member sees your link for 30 seconds when they log in, for 30 days.', 'h', 'soon',
     ['20 USDT for 30 days of guaranteed views', 'Title (30 characters) and link, then Preview', 'The two tick boxes before you buy', 'Login Ad or Ad Campaign: the difference'], '', ''),
    ('t7', 'Tutorial 7', 'How to Pay It Forward: send funds to another member', 'Help a team member get started from your Available Balance.', 'v', 'soon',
     ['Open Pay It Forward from the menu', 'Check the username twice', 'Add an optional message', 'Your Security PIN, then confirm (it cannot be undone)'], '', ''),
]
EXPLAINERS = [
    ('e1', 'Explainer', 'What is ClickBaitPays?', 'Advertisers get traffic, viewers get paid: the whole idea in one picture.', 'h', 'soon', [], '', ''),
    ('e2', 'Explainer', 'How to join ClickBaitPays', 'Free sign-up through a sponsor link, the house rules, and your first steps.', 'h', 'soon', [], '', ''),
    ('e3', 'Explainer', 'How it works: levels, activation and earnings', 'Seven levels, one activation per level, and what each click pays.', 'h', 'soon', [], '', ''),
    ('e4', 'Explainer', 'The 12 + 7 timeline', 'Click for 12 days, a 7-day hold, then your Available Balance.', 'h', 'soon', [], '', ''),
]
YOUTUBE = [   # ClickBaitPays Us channel (titles from YouTube, 14 Nov 2026)
    ('gWkLEgBFVEY', 'ClickBaitPays overview', 'The platform in a few minutes: who it is for and how it works.'),
    ('EDnb9e03B0E', 'ClickBaitPays back office walkthrough', 'A tour of the member back office.'),
    ('MiUja2RnWXY', 'ClickBaitPays income and commission plan', 'How campaigns, clicks and referral commission work.'),
    ('8rftor87kKQ', 'ClickBaitPays Q&A (29 August 2026)', 'Members\' questions answered.'),
    ('25wXab2hAB8', 'ClickBaitPays presentation (14 September 2026)', 'The full presentation.'),
]
STATUS = {'soon': 'Coming soon', 'record': 'Being recorded'}
SHORT = {'t1': 'Back office tour', 't2': 'Deposit', 't3': 'First campaign and activation', 't4': 'Another campaign, same level',
         't5': 'Withdraw', 't6': 'Login Ads', 't7': 'Pay It Forward'}

# ============================================================== small helpers
ICONS = json.load(open(os.path.join(SRC, 'icons.json'), encoding='utf-8'))
USED_ICONS = set()
HASH = {}


def esc(s):
    return html.escape(str(s), quote=True)


def ic(name, cls='ic'):
    USED_ICONS.add(name)
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def sprite():
    out = []
    for n in sorted(USED_ICONS):
        s = ICONS['i-' + n]
        out.append(f'<symbol id="i-{n}" {s["attrs"]}>{s["body"]}</symbol>')
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + ''.join(out) + '</defs></svg>'


def money(v):
    s = f'{v:,.2f}'
    return s


def plain(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def asset(path):
    return f'{BASE}assets/{path}?v={HASH.get(path, "1")}'


def join_btn(label='Join ClickBaitPays free', cls='', size=''):
    return (f'<a class="btn btn-join ring {size} {cls}" href="{esc(OWNER["ref"])}" target="_blank" rel="sponsored noopener" '
            f'data-join>{ic("userplus")}<span>{label}</span><span class="sr"> (opens the official sign-up page in a new tab)</span></a>')


def fair(cls=''):
    return f'<p class="fair {cls}">{ic("check")}Free account. Invited by someone else? Please use their link.</p>'


def note(body, icon='info', cls=''):
    return f'<div class="note {cls}">{ic(icon)}<div>{body}</div></div>'


def sec(id_, eyebrow, title, lead, body, cls=''):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ''
    return (f'<section class="sec {cls}" id="{id_}" aria-labelledby="{id_}-h"><div class="wrap">'
            f'<p class="eye">{eyebrow}</p><h2 id="{id_}-h">{title}</h2>{lead_html}{body}</div></section>')


def table(head, rows, caption, cls=''):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    trs = ''
    for r in rows:
        cells = ''
        for i, c in enumerate(r):
            tag = 'th scope="row"' if i == 0 else 'td'
            cells += f'<{tag} data-label="{esc(plain(head[i]))}">{c}</{tag.split()[0]}>'
        trs += f'<tr>{cells}</tr>'
    return f'<div class="tbl-wrap {cls}"><table class="tbl"><caption class="sr">{caption}</caption><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def frame(v, size='', label=True):
    """A device-framed video cover: laptop for 16:9, slim phone for 9:16. Placeholder until v has a src."""
    code, kind, title, line, orient, status, learn, src, poster = v
    dev = 'phone' if orient == 'v' else 'laptop'
    playable = bool(src)
    scr = (f'<img src="{esc(poster)}" alt="" loading="lazy">' if poster else
           f'<span class="ph"><img class="ph-logo" src="{asset("logo-disc-256.webp")}" alt="" width="96" height="96" loading="lazy">'
           f'<b>{esc(kind)}</b><span class="ph-t">{esc(title)}</span></span>')
    badge = '' if playable else f'<span class="soon">{ic("timer")}{STATUS[status]}</span>'
    play = f'<span class="play">{ic("play")}</span>'
    inner = f'<span class="scr">{scr}{play}{badge}</span>'
    if dev == 'laptop':
        body = f'<span class="dev laptop {size}">{inner}<span class="base"><i></i></span></span>'
    else:
        body = f'<span class="dev phone {size}"><span class="btns" aria-hidden="true"></span>{inner}<span class="island" aria-hidden="true"></span></span>'
    if playable:
        return (f'<button type="button" class="vbtn" data-src="{esc(src)}" data-poster="{esc(poster)}" data-orient="{orient}" '
                f'aria-label="Play: {esc(title)}">{body}</button>')
    return f'<div class="vbtn is-soon" role="img" aria-label="{esc(kind)}: {esc(title)}. {STATUS[status]}.">{body}</div>'


def yt_card(vid, title, line):
    thumb = asset(f'yt/{vid}.webp')
    return (f'<li class="yt"><button type="button" class="ytb" data-yt="{vid}" aria-label="Play on this page: {esc(title)}">'
            f'<span class="yt-img"><img src="{thumb}" alt="" loading="lazy" width="480" height="270"><span class="play">{ic("play")}</span></span>'
            f'<span class="yt-t">{esc(title)}</span><span class="yt-l">{esc(line)}</span></button></li>')


def social_row(cls='soc'):
    items = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{esc(label)} (opens in a new tab)">{ic(k)}</a>' for k, label, u in SOCIAL)
    return f'<div class="{cls}">{items}</div>'


# ============================================================== head, header, footer
PERSON_ID = SITE + BASE + '#mtg'
SITE_ID = SITE + BASE + '#site'
CBP_THING = {'@type': 'Organization', 'name': 'ClickBaitPays', 'url': OFFICIAL, 'sameAs': [OFFICIAL]}


def person_ld():
    return {'@type': 'Person', '@id': PERSON_ID, 'name': 'MTG (MusaTheGiant)', 'alternateName': ['MTG', 'Musa The Giant'],
            'jobTitle': 'Your Digital Architect', 'url': SITE + '/', 'sameAs': [u for k, l, u in SOCIAL if k != 'whatsapp']}


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (n, p) in enumerate(items)]}


def head(title, desc, path, og_key, ld, page_type='WebPage', noindex=False, extra_head=''):
    url = SITE + path
    og = f'{SITE}{BASE}assets/og/{og_key}.jpg?v={HASH.get("og/" + og_key + ".jpg", "1")}'
    graph = [person_ld(),
             {'@type': 'WebSite', '@id': SITE_ID, 'name': NAME, 'url': SITE + BASE, 'inLanguage': 'en-ZA', 'publisher': {'@id': PERSON_ID}},
             {'@type': page_type, '@id': url + '#page', 'url': url, 'name': title, 'description': desc, 'inLanguage': 'en-ZA',
              'isPartOf': {'@id': SITE_ID}, 'about': CBP_THING, 'author': {'@id': PERSON_ID}, 'dateModified': TODAY,
              'primaryImageOfPage': og}] + ld
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large,max-snippet:-1'
    return f'''<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="author" content="MTG (MusaTheGiant)">
<meta name="theme-color" content="#080015">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:locale" content="en_ZA">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="icon" href="{asset('favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{asset('favicon-32.png')}">
<link rel="apple-touch-icon" href="{asset('apple-touch-icon.png')}">
<link rel="manifest" href="{BASE}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap">
{extra_head}<link rel="stylesheet" href="{asset('cbp.css')}">
<script type="application/ld+json">{json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))}</script>
</head>
'''


NAV = [('How it works', BASE + '#how'), ('Levels', BASE + '#levels'), ('Join', BASE + '#join'), ('Videos', BASE + '#videos'),
       ('FAQ', BASE + '#faq'), ('Calculator', BASE + 'calculator/')]


def brand():
    return (f'<a class="brand" href="{BASE}" aria-label="{esc(NAME)}: home"><img src="{asset("logo-disc-256.webp")}" alt="" width="44" height="44">'
            f'<span><b>ClickBaitPays</b><small>Guide by MTG 👑</small></span></a>')


def header(active=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur if active == t else ""}>{t}</a>' for t, h in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top" data-top>
 <div class="wrap top-in">
  {brand()}
  <nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
  <div class="top-act">
   <a class="btn btn-dash ring sm" href="{BASE}dashboard/">{ic("layers")}<span>Dashboard</span></a>
   <button type="button" class="menu" aria-controls="site-nav" aria-expanded="false" data-menu>{ic("menu")}<span class="sr">Open the menu</span></button>
  </div>
 </div>
</header>
'''


def footer():
    return f'''<footer class="foot">
 <div class="wrap">
  <div class="foot-grid">
   <div class="foot-brand">{brand()}
    <p>An independent, plain-English guide to ClickBaitPays by MTG 👑 | Your Digital Architect. Not the official ClickBaitPays website: that is <a href="{OFFICIAL}" target="_blank" rel="noopener">clickbaitpays.me</a>.</p>
    {social_row()}
   </div>
   <nav class="foot-nav" aria-label="Guide">
    <b>Guide</b><a href="{BASE}">Home</a><a href="{BASE}dashboard/">Tutorials and explainers</a><a href="{BASE}calculator/">Calculator</a><a href="{BASE}#faq">FAQ</a>
   </nav>
   <nav class="foot-nav" aria-label="More">
    <b>More</b><a href="{ORDER}">Get your own copy</a><a href="{GROUP}">Join the MTG TRIBE</a><a href="{LOGIN}" target="_blank" rel="noopener">ClickBaitPays login</a><a href="{BASE}disclaimer/">Disclaimer and privacy</a>
   </nav>
  </div>
  <p class="risk">{ic("info")}<span>ClickBaitPays is an advertising platform, not an investment. Figures shown are the platform's own; what you earn depends on the ads you view, and nothing is guaranteed. The Join buttons carry MTG's referral link.</span></p>
  <p class="sig">Made with ❤️ by MTG 👑 | Your Digital Architect · Let's Get This Crypto! 💪</p>
 </div>
</footer>
'''


def modal():
    return f'''<div class="vm" id="vm" role="dialog" aria-modal="true" aria-label="Video player" hidden>
 <div class="vm-bg" data-close></div>
 <div class="vm-box">
  <button type="button" class="vm-x" data-close aria-label="Close the video">{ic("x")}</button>
  <div class="vm-dev" data-dev></div>
 </div>
</div>
'''


def sticky():
    return f'<div class="stick" data-stick hidden>{join_btn("Join ClickBaitPays free", size="sm")}<a class="stick-d" href="{BASE}dashboard/" aria-label="Open the tutorials dashboard">{ic("layers")}</a></div>'


def tail(scripts=True):
    js = f'<script src="{asset("cbp.js")}" defer></script>\n<script src="/assets/video-return.js?v=1" defer></script>\n' if scripts else ''
    return f'{modal()}{sprite()}\n{js}</body>\n</html>\n'


# ============================================================== page: landing
def levels_table():
    rows = [[f'Level {l}', f'{money(p)} USDT', f'{money(a)} USDT', f'{money(c)}', f'{n}', f'<b>{money(t)}</b>'] for l, p, a, c, n, t in LEVELS]
    return table(['Level', 'Campaign', 'Activation (once)', 'Per click', 'Clicks a day', 'Campaign total*'], rows,
                 'The 7 ClickBaitPays levels: price, one-time activation fee, pay per click, clicks a day and campaign total', 'levels')


FAQ = [
    ('Is ClickBaitPays free to join?',
     'Yes, creating your account is free. To take part, you buy an ad campaign (from 13 USDT at Level 1) and, to earn from clicking ads at that level, pay its one-time activation fee (from 1 USDT).'),
    ('How do members get paid?',
     'Every ad you open and view until its 15-second countdown ends pays your level\'s per-click amount, which is the 90% of the advertiser\'s cost that members receive. Your clicks collect in your campaign\'s Earned Wallet and move to your Available Balance 7 days after your 12th click day.'),
    ('What is the activation fee?',
     'A one-time fee per level, from 1 USDT (Level 1) to 240 USDT (Level 7), that unlocks earning from clicking ads at that level. It never expires, and you pay it once per level, however many campaigns you buy there. These once-per-level fees also support the platform\'s sustainability.'),
    ('When can I withdraw?',
     'A campaign runs for 12 click days. After your 12th click day its earnings are held for 7 days, then move to your Available Balance. From there you can request a withdrawal (once a week, minimum 10 USDT, 10% fee), Pay It Forward to another member, or buy your next campaign.'),
    ('When do the daily clicks reset?',
     'At midnight Panama time, which is 7:00 AM in South Africa. Complete all of your level\'s clicks in one day to count a click day. Miss a day and your 12 click days simply take a little longer.'),
    ('What is a Login Ad?',
     'An ad every member sees for 30 seconds when they log in, for 30 days, for 20 USDT. It pays you nothing: it buys guaranteed views for your link. Ad campaigns are different: they run 12 click days and, once you activate the level, pay you for clicking.'),
    ('Do I need to refer people?',
     'No. Referrals are optional: you earn from clicking the ads of your own campaign. Members who do share their link receive 10% of the campaigns their referrals buy.'),
    ('Can I use ClickBaitPays on my phone?',
     'Yes. Tap the menu button (the three lines) to open the menu. A laptop or desktop shows the back office more comfortably, which is why most of MTG\'s tutorials are recorded on a computer.'),
    ('Is ClickBaitPays an investment?',
     'No. It is an advertising platform: you buy advertising for your own link, and you are paid for viewing other members\' ads. The figures in this guide are the platform\'s own, and nothing is guaranteed.'),
    ('Is ClickBaitPays legit?',
     'MTG is an active member: his tutorials show his own campaigns, his daily clicks and completed campaigns moving to his Available Balance. Check it for yourself too: read the official FAQ at clickbaitpays.me, start with a level you are comfortable with, and only use money you can afford to lose.'),
    ('Can I have more than one account?',
     'One account per person. Up to 3 accounts are allowed per household, each for a different adult with their own email address, all under the same original sponsor.'),
    ('What can I advertise?',
     'Almost any website: your affiliate link, your business or a cause you care about. Illegal or harmful content and big sites such as Google or Facebook are not allowed. Ad titles are 30 characters at most.'),
]


def faq_html():
    items = ''.join(f'<details class="qa"><summary><span>{esc(q)}</span>{ic("chev", "ic chev")}</summary><div class="qa-a"><p>{esc(a)}</p></div></details>' for q, a in FAQ)
    return f'<div class="faq">{items}</div><p class="more">More answers in the <a href="{OFFICIAL_FAQ}" target="_blank" rel="noopener">official ClickBaitPays FAQ</a>.</p>'


def p_landing():
    title = 'ClickBaitPays: How It Works, the 7 Levels and How to Join'
    desc = 'ClickBaitPays in plain English: advertise your link, view members\' ads daily, get paid in USDT. The 7 levels from 13 USDT, fees, timeline and how to join free.'
    faq_ld = {'@type': 'FAQPage', '@id': SITE + BASE + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    howto = {'@type': 'HowTo', '@id': SITE + BASE + '#how', 'name': 'How ClickBaitPays works, step by step', 'inLanguage': 'en-ZA',
             'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': n, 'text': plain(t)} for i, (ico, n, t) in enumerate(STEPS)]}
    out = head(title, desc, BASE, 'cbp-home', [faq_ld, howto, crumbs([('MTG TRIBE', '/'), ('ClickBaitPays guide', BASE)])])
    out += '<body class="cbp">\n' + header()
    out += f'''<main id="main" tabindex="-1">
<section class="hero" aria-labelledby="hero-h">
 <div class="wrap hero-in">
  <div class="hero-copy">
   <p class="eye">{ic("cursor")}Independent guide by MTG 👑 · checked {CHECKED}</p>
   <h1 id="hero-h"><span class="h1-big">ClickBaitPays</span> <span class="h1-sub">explained: how it works, the 7 levels and how to join</span></h1>
   <p class="lead">Advertise your link to other members, view their ads each day, and get paid in USDT for every ad you view. Everything you need in plain English, from a member who clicks his own ads every day.</p>
   <div class="cta-row">{join_btn()}<a class="btn btn-ghost" href="#how">{ic("play")}<span>See how it works</span></a></div>
   {fair()}
   <ul class="facts" aria-label="Key facts">
    <li>{ic("gift")}<b>Free</b> to join</li><li>{ic("layers")}<b>7 levels</b> from 13 USDT</li><li>{ic("cal")}<b>12</b> click days</li><li>{ic("coins")}Paid in <b>USDT</b></li>
   </ul>
  </div>
  <div class="hero-vid">{frame(TOUR, 'xl')}<p class="cap">{ic("film")}<span>Site tour: how to use this guide <span class="dim">(video coming soon)</span></span></p></div>
 </div>
</section>
'''
    what = f'''<div class="two">
 <div>
  <div class="roles">
   <article class="role">{ic("mega")}<h3>Advertisers get traffic</h3><p>Buy an ad campaign and members view your link every day for 12 click days. Or buy a Login Ad that every member sees when they log in.</p></article>
   <article class="role pink">{ic("cursor")}<h3>Viewers get paid</h3><p>Open each ad, wait for the 15-second countdown, tap <b>Confirm &amp; Earn</b>. Every member does both: you advertise your link and view everyone else's.</p></article>
  </div>
  {note('<b>Think of a community noticeboard.</b> You pin your poster where members pass by, and members are paid for the time they spend reading each other\'s posters. <span class="dim">Where the picture stops: reading a noticeboard is free, while here you first buy a campaign and activate your level.</span>', 'msg', 'soft')}
  <p class="body">The ads come from members promoting real products, businesses and causes, so it is worth a look when something catches your eye. You can save any ad and come back to it later.</p>
 </div>
 <div class="side-vid">{frame(EXPLAINERS[0])}<p class="cap">{ic("film")}<span>Explainer: {EXPLAINERS[0][2]} <span class="dim">(coming soon)</span></span></p></div>
</div>'''
    out += sec('what', 'The idea', 'What is ClickBaitPays?', 'A paid-to-click advertising platform: two sides, one simple trade.', what)

    steps = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{ic(ico)}{n}</h3><p>{t}</p></div></li>' for i, (ico, n, t) in enumerate(STEPS))
    timeline = '''<figure class="tl" aria-labelledby="tl-cap">
 <div class="tl-bar" aria-hidden="true">''' + ''.join(f'<i class="d c" style="--i:{k}">{k + 1}</i>' for k in range(12)) + ''.join(f'<i class="d h" style="--i:{12 + k}"></i>' for k in range(7)) + '''<i class="d end">✓</i></div>
 <div class="tl-key"><span class="k c">12 click days</span><span class="k h">7-day hold</span><span class="k e">Available Balance</span></div>
 <figcaption id="tl-cap">Click your ads on 12 days, the earnings rest for 7 days, then they are yours to withdraw, Pay It Forward or reinvest in a new campaign.</figcaption>
</figure>'''
    how = f'''<div class="two">
 <div><ol class="steps">{steps}</ol></div>
 <div class="side-vid">{frame(EXPLAINERS[2])}<p class="cap">{ic("film")}<span>Explainer: {EXPLAINERS[2][2]} <span class="dim">(coming soon)</span></span></p>
  {timeline}
  {frame(EXPLAINERS[3])}<p class="cap">{ic("film")}<span>Explainer: {EXPLAINERS[3][2]} <span class="dim">(coming soon)</span></span></p>
 </div>
</div>
{note('<b>Miss a day? No stress.</b> Your 12 click days simply take a little longer. Daily clicks reset at midnight Panama time, which is <b>7:00 AM in South Africa</b>.', 'timer')}'''
    out += sec('how', 'Step by step', 'How ClickBaitPays works', 'Five steps, from free sign-up to your Available Balance.', how)

    lv = f'''{levels_table()}
<p class="tnote">* The platform's own figures, read in the back office on {CHECKED}. "Per click" is the 90% of the advertiser's cost that members receive; the campaign total assumes all 12 click days. You are paid only for the ads you view, and nothing is guaranteed.</p>
<div class="calc-strip">
 <div class="eg"><b>Your first campaign at a level</b> = campaign + activation<span class="eqs"><span>Level 1: 13 + 1 = <b>14 USDT</b></span><span>Level 3: 150 + 15 = <b>165 USDT</b></span><span>Level 4: 300 + 30 = <b>330 USDT</b></span></span></div>
 <a class="btn btn-ghost" href="{BASE}calculator/">{ic("calc")}<span>Work out your numbers</span></a>
</div>
{note('<b>Start at any level.</b> You do not have to go 1, 2, 3. Each level is activated once and never expires, so your next campaign at that level needs no activation fee.', 'layers')}'''
    out += sec('levels', 'Costs and figures', 'The 7 ClickBaitPays levels', 'Every level runs for 12 click days with unlimited views. Higher levels pay more per click and give you more clicks a day.', lv)

    cmp_rows = [['Cost', '20 USDT', 'From 13 USDT (Level 1)'], ['Runs for', '30 days', '12 click days'],
                ['Who sees it', 'Every member, for 30 seconds at login', 'Members clicking ads at that level'],
                ['Pays you?', 'No, it buys views for your link', 'Yes, once the level is activated']]
    out += sec('login-ads', 'Two ways to advertise', 'Login Ads or Ad Campaigns?', 'Both put your link in front of members. Only one of them also pays you to click.',
               table(['', 'Login Ad', 'Ad Campaign'], cmp_rows, 'Login Ads compared with Ad Campaigns', 'cmp'), 'alt')

    joinsteps = [('link', 'Tap Join', f'The official sign-up page opens on clickbaitpays.me with MTG as your sponsor.'),
                 ('userplus', 'Create your free account', 'Sign up from your home Wi-Fi (no VPN or mobile data while you register). One account per person.'),
                 ('play', 'Follow the tutorials', f'Log in at clickbaitpays.me/login.php, then follow Tutorial 3 to buy and activate your first campaign.')]
    js = ''.join(f'<li class="jstep"><span class="num">{i + 1}</span>{ic(a)}<h3>{b}</h3><p>{c}</p></li>' for i, (a, b, c) in enumerate(joinsteps))
    joinb = f'''<div class="two">
 <div><ol class="jsteps">{js}</ol>
  <div class="join-box">{join_btn('Join ClickBaitPays free', size='lg')}<p class="fair-big">{ic("users")}<span><b>Invited by someone else?</b> Please use their link instead. Fair is fair. 🤝</span></p></div>
  <p class="disc">The Join buttons carry MTG's referral link (sponsor code <b>{OWNER["code"]}</b>). If you join through it, MTG becomes your sponsor and receives 10% of the campaigns you buy. Your prices stay exactly the same.</p>
 </div>
 <div class="side-vid">{frame(EXPLAINERS[1])}<p class="cap">{ic("film")}<span>Explainer: {EXPLAINERS[1][2]} <span class="dim">(coming soon)</span></span></p></div>
</div>'''
    out += sec('join', 'Get started', 'How to join ClickBaitPays (free)', 'ClickBaitPays is joined through a member\'s link. Three steps and you are in.', joinb)

    tut = ''.join(f'<li class="tcard"><a href="{BASE}dashboard/#{v[0]}"><span class="tno">{v[1]}</span><b>{esc(v[2])}</b><span class="st st-{v[5]}">{ic("timer")}{STATUS[v[5]]}</span></a></li>' for v in TUTORIALS)
    yts = ''.join(yt_card(*y) for y in YOUTUBE)
    vids = f'''<h3 class="h3">{ic("film")}Step-by-step tutorials</h3>
<ol class="tgrid">{tut}</ol>
<p class="center"><a class="btn btn-dash ring" href="{BASE}dashboard/">{ic("layers")}<span>Open the tutorials dashboard</span></a></p>
<h3 class="h3">{ic("youtube")}Watch now on YouTube</h3>
<ul class="ygrid">{yts}</ul>
<p class="more">More on the <a href="{CBP_YT}" target="_blank" rel="noopener">ClickBaitPays Us YouTube channel</a>.</p>'''
    out += sec('videos', 'Watch and learn', 'ClickBaitPays videos', 'MTG\'s screen-recorded tutorials are on their way. Start with these five videos today.', vids, 'alt')
    out += sec('faq', 'Questions', 'ClickBaitPays FAQ', 'Straight answers to what people ask most.', faq_html())
    out += f'''<section class="final" aria-labelledby="final-h" data-final>
 <div class="wrap final-in">
  <img src="{asset('logo-disc-256.webp')}" alt="" width="120" height="120" loading="lazy">
  <div><h2 id="final-h">Ready to put your link in front of members?</h2>
   <p>Join free, then follow the tutorials one step at a time. We learn best when we teach others.</p>
   <div class="cta-row">{join_btn()}<a class="btn btn-ghost" href="{GROUP}">{ic("whatsapp")}<span>Questions? Join the MTG TRIBE</span></a></div>
   {fair()}
  </div>
 </div>
</section>
</main>
'''
    out += footer() + sticky() + tail()
    return out


STEPS = [
    ('userplus', 'Join free', 'Use a Join button on this page, or the link of the person who invited you. Register from your home Wi-Fi.'),
    ('wallet', 'Fund your account', 'Deposit crypto on the Deposit page. Your balance shows in USDT.'),
    ('layers', 'Buy a campaign and activate the level', 'Pick a level, add your ad title (30 characters max) and link, tap <b>Preview</b>, then <b>Confirm Purchase</b>. The first time at a level, pay its one-time activation fee so you can earn from clicking.'),
    ('cursor', 'Click your daily ads', 'Log in once a day, open each ad, wait for the 15-second countdown and tap <b>Confirm &amp; Earn</b>.'),
    ('coins', 'Use your Available Balance', 'After 12 click days and a 7-day hold, the earnings are yours: withdraw them, Pay It Forward, or buy your next campaign.'),
]


# ============================================================== page: dashboard
def p_dashboard():
    title = 'ClickBaitPays Tutorials: Step-by-Step Videos by MTG'
    desc = 'Every ClickBaitPays tutorial in order: back office tour, deposit, your first campaign and activation, daily clicks, Login Ads, withdrawals and Pay It Forward.'
    items = [{'@type': 'ListItem', 'position': i + 1, 'name': v[2], 'url': SITE + BASE + 'dashboard/#' + v[0]} for i, v in enumerate(TUTORIALS)]
    ld = [{'@type': 'ItemList', '@id': SITE + BASE + 'dashboard/#tutorials', 'name': 'ClickBaitPays tutorials by MTG', 'itemListElement': items},
          crumbs([('ClickBaitPays guide', BASE), ('Dashboard', BASE + 'dashboard/')])]
    out = head(title, desc, BASE + 'dashboard/', 'cbp-dashboard', ld, 'CollectionPage',
               extra_head='<link rel="stylesheet" href="/assets/mtg-dash.css?v=1">\n')
    out += '<body class="cbp cbp-dash">\n<a class="skip" href="#main">Skip to content</a>\n'
    nav = lambda h, i, b, s, em='': f'<a class="md-nav" href="{h}"><span class="ic">{i}</span><span class="tx"><b>{b}</b><small>{s}</small></span>{em}</a>'
    side = ''.join([
        '<p class="md-label">Start here</p>', nav('#tour', ic('compass'), 'Welcome', 'Site tour and your daily routine'),
        '<p class="md-label">Tutorials</p>'] + [nav('#' + v[0], f'<span class="rk">{i + 1}</span>', esc(SHORT[v[0]]), esc(STATUS[v[5]])) for i, v in enumerate(TUTORIALS)] + [
        '<p class="md-label">Explainers</p>'] + [nav('#' + v[0], ic('film'), esc(v[2]), esc(STATUS[v[5]])) for v in EXPLAINERS] + [
        '<p class="md-label">More</p>', nav('#yt', ic('youtube'), 'YouTube videos', 'Watch these today'),
        nav(BASE + 'calculator/', ic('calc'), 'Calculator', 'Cost, clicks and payout date'),
        nav(ORDER, ic('globe'), 'Get your own copy', 'This guide with your link'),
        nav(BASE + 'disclaimer/', ic('shield'), 'Disclaimer and privacy', 'The small print, in plain words')])
    out += f'''{sprite_placeholder()}<div class="md-shell">
<script>try{{if(localStorage.getItem('mtg-side')==='off'&&matchMedia('(min-width:1061px)').matches)document.currentScript.parentNode.classList.add('md-off')}}catch(e){{}}</script>
<aside class="md-side" id="cbp-menu" aria-label="Dashboard menu">
 <a class="side-brand" href="{BASE}" aria-label="{esc(NAME)}: home"><img src="{asset('logo-disc-256.webp')}" alt="" width="44" height="44"><span><b>ClickBaitPays</b><small>Dashboard by MTG 👑</small></span></a>
 {side}
 <div class="md-bot">
  <a class="md-btn md-home" href="{BASE}"><span class="emo" aria-hidden="true">🏡</span>Go Home</a>
  <a class="side-join" href="{esc(OWNER['ref'])}" target="_blank" rel="sponsored noopener">{ic('userplus')}Join ClickBaitPays free</a>
  {social_row('row')}
 </div>
</aside>
<button type="button" class="md-toggle" aria-controls="cbp-menu" aria-expanded="true" aria-label="Collapse menu" title="Collapse menu">{ic('chev')}</button>
<div class="md-scrim" aria-hidden="true"></div>
<div class="md-main">
<header class="md-top">
 <button type="button" class="md-menu" aria-controls="cbp-menu" aria-expanded="false" aria-label="Open menu"><span class="bars" aria-hidden="true"></span><span class="lbl">Menu</span></button>
 <nav class="md-crumb" aria-label="Breadcrumb"><a href="{BASE}">ClickBaitPays guide</a>{ic('chevr')}<span>Dashboard</span></nav>
 <div class="md-act">
  <a class="md-btn md-join md-hide-sm" href="{esc(OWNER['ref'])}" target="_blank" rel="sponsored noopener">{ic('userplus')}Join free</a>
  <a class="md-btn md-home" href="{BASE}"><span class="emo" aria-hidden="true">🏡</span>Go Home</a>
 </div>
</header>
<main id="main" class="dmain" tabindex="-1">
<section class="dhero" id="tour" aria-labelledby="dh-h">
 <div class="dhero-copy">
  <p class="eye">{ic('compass')}Start here</p>
  <h1 id="dh-h">ClickBaitPays dashboard: every tutorial, in order</h1>
  <p class="lead">Watch the site tour first, then follow the tutorials from 1 to 7. Each one shows one job in the ClickBaitPays back office, click by click, recorded by MTG on his own account.</p>
  <div class="routine" aria-labelledby="rt-h">
   <h2 id="rt-h">{ic('repeat')}Your daily routine</h2>
   <ol><li>Log in at <a href="{LOGIN}" target="_blank" rel="noopener">clickbaitpays.me/login.php</a> and view the login ad (30 seconds)</li>
    <li>Open <b>Click Ads</b> (or tap <b>Start Clicking</b>)</li>
    <li>For each ad: <b>View &amp; Earn</b>, <b>Open Ad</b>, wait 15 seconds, <b>Confirm &amp; Earn</b></li>
    <li>Done for today when it says <b>Click day complete</b>. New clicks from 7:00 AM (South Africa)</li></ol>
  </div>
 </div>
 <div class="dhero-vid">{frame(TOUR, 'xl')}<p class="cap">{ic('film')}<span>Site tour <span class="dim">(coming soon)</span></span></p></div>
</section>
'''
    def card(v, i=None):
        learn = ''.join(f'<li>{ic("check")}{esc(x)}</li>' for x in v[6])
        ul = f'<ul class="learn">{learn}</ul>' if learn else ''
        fmt = ('Vertical, recorded on a phone' if v[4] == 'v' else 'Widescreen, recorded on a computer')
        return (f'<article class="dcard{" vert" if v[4] == "v" else ""}" id="{v[0]}" aria-labelledby="{v[0]}-h">'
                f'<div class="dcard-vid">{frame(v)}</div><div class="dcard-copy"><p class="tno">{v[1]} <span class="st st-{v[5]}">{ic("timer")}{STATUS[v[5]]}</span></p>'
                f'<h3 id="{v[0]}-h">{esc(v[2])}</h3><p>{esc(v[3])}</p>{ul}<p class="fmt">{ic("phone" if v[4] == "v" else "laptop")}{fmt}</p></div></article>')
    out += '<section class="dsec" aria-labelledby="tut-h"><h2 id="tut-h" class="dh2">' + ic('film') + 'Tutorials</h2><p class="dlead">Watch them in this order. Videos appear here as soon as each one is ready.</p>'
    out += ''.join(card(v) for v in TUTORIALS) + '</section>'
    out += '<section class="dsec" aria-labelledby="exp-h"><h2 id="exp-h" class="dh2">' + ic('compass') + 'Explainers</h2><p class="dlead">Short videos that make the big ideas click.</p><div class="egrid">'
    out += ''.join(f'<article class="ecard" id="{v[0]}" aria-labelledby="{v[0]}-h">{frame(v)}<h3 id="{v[0]}-h">{esc(v[2])}</h3><p>{esc(v[3])}</p></article>' for v in EXPLAINERS) + '</div></section>'
    yts = ''.join(yt_card(*y) for y in YOUTUBE)
    out += f'<section class="dsec" id="yt" aria-labelledby="yt-h"><h2 id="yt-h" class="dh2">{ic("youtube")}Watch today on YouTube</h2><ul class="ygrid">{yts}</ul></section>'
    out += f'''<section class="dsec dcta" aria-labelledby="dc-h"><h2 id="dc-h">Not a member yet?</h2><p>Join free with MTG, then come back here and follow Tutorial 3.</p>
<div class="cta-row">{join_btn()}<a class="btn btn-ghost" href="{BASE}calculator/">{ic('calc')}<span>Open the calculator</span></a></div>{fair()}
<p class="risk">{ic('info')}<span>ClickBaitPays is an advertising platform, not an investment. Figures are the platform's own and nothing is guaranteed. The Join buttons carry MTG's referral link. <a href="{BASE}disclaimer/">Disclaimer</a>.</span></p></section>
</main>
</div>
</div>
<script src="/assets/mtg-dash.js?v=1" defer></script>
'''
    out += tail()
    return out


def sprite_placeholder():
    return '<!--SPRITE-->'


# ============================================================== page: calculator
def p_calc():
    title = 'ClickBaitPays Calculator: Cost, Daily Clicks and Payout Date'
    desc = 'Pick a ClickBaitPays level and see what you pay today, your clicks a day, the platform\'s campaign total, and roughly when it reaches your Available Balance.'
    app = {'@type': 'WebApplication', 'name': 'ClickBaitPays Calculator', 'url': SITE + BASE + 'calculator/', 'description': desc,
           'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Any (runs in a web browser)', 'browserRequirements': 'Requires JavaScript',
           'isAccessibleForFree': True, 'inLanguage': 'en-ZA', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'author': {'@id': PERSON_ID}}
    out = head(title, desc, BASE + 'calculator/', 'cbp-calculator', [app, crumbs([('ClickBaitPays guide', BASE), ('Calculator', BASE + 'calculator/')])], 'WebPage')
    out += '<body class="cbp">\n' + header('Calculator')
    chips = ''.join(f'<label class="lv"><input type="radio" name="lvl" value="{l}"{" checked" if l == 4 else ""}><span><b>Level {l}</b><small>{p:,} USDT</small></span></label>' for l, p, a, c, n, t in LEVELS)
    data = json.dumps([{'l': l, 'p': p, 'a': a, 'c': c, 'n': n, 't': t} for l, p, a, c, n, t in LEVELS])
    out += f'''<main id="main" tabindex="-1">
<section class="sec calc" aria-labelledby="c-h"><div class="wrap">
 <p class="eye">{ic('calc')}Free tool</p>
 <h1 id="c-h">ClickBaitPays calculator</h1>
 <p class="lead">Pick a level and see what you pay today, your clicks a day, the platform's campaign total and roughly when it reaches your Available Balance. It uses the platform's own figures from {CHECKED}.</p>
 <div class="tool" data-calc='{data}'>
  <form class="tool-in" onsubmit="return false" aria-describedby="c-note">
   <fieldset class="lvs"><legend>1. Choose a level</legend>{chips}</fieldset>
   <fieldset class="opt"><legend>2. Is this your first campaign at this level?</legend>
    <label class="tog"><input type="radio" name="first" value="1" checked><span>Yes, add the one-time activation</span></label>
    <label class="tog"><input type="radio" name="first" value="0"><span>No, this level is already active</span></label>
   </fieldset>
   <div class="row2">
    <div class="fld"><label for="c-n">3. Campaigns at this level</label>
     <div class="step-in"><button type="button" data-dec aria-label="One campaign less">−</button><input id="c-n" type="number" inputmode="numeric" min="1" max="5" value="1" aria-describedby="c-n-h"><button type="button" data-inc aria-label="One campaign more">+</button></div>
     <small id="c-n-h">From 1 to 5. Each campaign brings its own daily clicks.</small></div>
    <div class="fld"><label for="c-d">4. First click day</label><input id="c-d" type="date"><small>Usually the day you buy.</small></div>
   </div>
   <button type="button" class="btn btn-ghost sm reset" data-reset>{ic('refresh')}<span>Reset</span></button>
  </form>
  <div class="res" aria-live="polite">
   <div class="tile big"><span>Pay today</span><b data-o="pay">0</b><small data-o="payx"></small></div>
   <div class="tile"><span>Clicks a day</span><b data-o="clicks">0</b><small>about 15 seconds each</small></div>
   <div class="tile"><span>Earned per click day</span><b data-o="day">0</b><small data-o="dayx"></small></div>
   <div class="tile"><span>Campaign total (platform figure)</span><b data-o="tot">0</b><small data-o="totx"></small></div>
   <div class="tile"><span>Reaches your Available Balance</span><b data-o="date">-</b><small>about 19 days from your first click day, if you click every day</small></div>
   <div class="tile"><span>If you then withdraw it all</span><b data-o="net">0</b><small>after the 10% withdrawal fee</small></div>
   <p class="formula" data-o="formula"></p>
  </div>
 </div>
 {note('<b>How to read this.</b> These are the platform\'s own figures, assuming you complete every click day. You are paid only for the ads you view, nothing is guaranteed, and a missed day moves your date back by a day. Your back office always shows your exact release date. At Levels 1 and 2 the site\'s campaign total is a few cents under 12 click days, because of rounding: we show the site\'s own total.', 'info', '')}
 <p class="center"><a class="btn btn-dash ring" href="{BASE}dashboard/">{ic('layers')}<span>Watch the tutorials</span></a> {join_btn()}</p>
 {fair('center')}
</div></section>
</main>
'''
    out += footer() + sticky() + tail()
    return out


# ============================================================== page: disclaimer and privacy
def p_disc():
    title = 'Disclaimer and Privacy | ClickBaitPays Guide by MTG'
    desc = 'The small print in plain words: an independent guide, the referral link disclosure, where the figures come from, and what this site stores (nothing personal).'
    out = head(title, desc, BASE + 'disclaimer/', 'cbp-disclaimer', [crumbs([('ClickBaitPays guide', BASE), ('Disclaimer and privacy', BASE + 'disclaimer/')])])
    out += '<body class="cbp">\n' + header()
    blocks = [
        ('shield', 'An independent guide', f'This is MTG\'s own guide to ClickBaitPays, made to educate. It is not the official ClickBaitPays website (that is <a href="{OFFICIAL}" target="_blank" rel="noopener">clickbaitpays.me</a>) and it is not run by ClickBaitPays. Rules, prices and features can change: the official site always has the final word.'),
        ('link', 'The Join buttons carry MTG\'s referral link', f'Every Join button opens the official sign-up page with MTG as your sponsor (code <b>{OWNER["code"]}</b>). If you join through it, MTG receives 10% of the ad campaigns you buy, as the platform\'s referral rules describe. Your prices do not change. Invited by someone else? Please use their link instead.'),
        ('layers', 'About the figures', f'Prices, activation fees, pay per click, clicks a day and campaign totals are the platform\'s own figures, read in the ClickBaitPays back office on {CHECKED}. Campaign totals assume all 12 click days. They describe how the platform pays; they are not a promise of what you will earn.'),
        ('info', 'Advertising, not an investment', 'ClickBaitPays is an advertising platform: you buy advertising for your link and are paid for viewing other members\' ads. Nothing on this site is financial advice. Results depend on the ads you view and on the platform, and nothing is guaranteed. Start with an amount you are comfortable with and only use money you can afford to lose.'),
        ('lock', 'Privacy: what this site stores', 'Nothing personal. There are no accounts, forms that store data, or tracking cookies. The calculator runs in your own browser. Your browser remembers only whether you collapsed the dashboard menu. YouTube videos load from youtube-nocookie.com only when you press play. The copy order form opens WhatsApp with your message; nothing is saved on this site.'),
        ('msg', 'Questions', f'Message MTG on WhatsApp at <a href="{OWNER["wa"]}" target="_blank" rel="noopener">{OWNER["wa_num"]}</a>, or join the MTG TRIBE at <a href="{GROUP}">mtgtribe.com/group</a>. For account issues, contact ClickBaitPays support through the official site.'),
    ]
    body = ''.join(f'<article class="dblock">{ic(i)}<div><h2>{t}</h2><p>{b}</p></div></article>' for i, t, b in blocks)
    out += f'''<main id="main" tabindex="-1"><section class="sec" aria-labelledby="d-h"><div class="wrap narrow">
<p class="eye">{ic('shield')}The small print</p><h1 id="d-h">Disclaimer and privacy</h1>
<p class="lead">Plain words about this guide, the links on it and your privacy. Last updated {TODAY[8:10].lstrip("0")} November 2026.</p>
{body}
<p class="center">{join_btn()}</p>{fair('center')}
</div></section></main>
'''
    out += footer() + tail()
    return out


# ============================================================== page: order a copy
def p_order():
    title = 'Get Your Own ClickBaitPays Guide Website | R1,000 Once-Off'
    desc = 'This ClickBaitPays guide with your referral link on every Join button and your contact links, at mtgtribe.com/cbp/yourname or clickbaitpaysus.com/yourname.'
    prod = {'@type': 'Product', 'name': 'Your own ClickBaitPays guide website', 'description': desc, 'brand': {'@type': 'Brand', 'name': 'MTG TRIBE'},
            'image': f'{SITE}{BASE}assets/og/cbp-copy.jpg',
            'offers': [{'@type': 'Offer', 'price': str(PRICE_ZAR), 'priceCurrency': 'ZAR', 'url': SITE + ORDER, 'availability': 'https://schema.org/InStock'},
                       {'@type': 'Offer', 'price': str(PRICE_USD), 'priceCurrency': 'USD', 'url': SITE + ORDER, 'availability': 'https://schema.org/InStock'}]}
    out = head(title, desc, ORDER, 'cbp-copy', [prod, crumbs([('ClickBaitPays guide', BASE), ('Get your own copy', ORDER)])])
    out += f'<body class="cbp">\n' + header()
    perks = [('globe', 'Your own address', 'mtgtribe.com/cbp/yourname or clickbaitpaysus.com/yourname'),
             ('link', 'Your link on every Join button', 'Everyone who joins from your page joins under you'),
             ('film', 'Every video and tool', 'Tutorials, explainers, calculator and FAQ, kept up to date'),
             ('refresh', '5 free edits', 'Change your details later at no cost')]
    pk = ''.join(f'<li>{ic(i)}<b>{a}</b><span>{b}</span></li>' for i, a, b in perks)
    out += f'''<main id="main" tabindex="-1"><section class="sec order" aria-labelledby="o-h"><div class="wrap">
<div class="two">
 <div>
  <p class="eye">{ic('globe')}Your own copy</p>
  <h1 id="o-h">Get your own ClickBaitPays guide website</h1>
  <p class="lead">This exact guide, with your referral link on every Join button, your name and your contact links. Share one link and let the page explain ClickBaitPays for you, day and night.</p>
  <div class="price"><b>R1,000</b><span>or $50, once-off</span><em>Pay after it is built</em></div>
  <ul class="perks">{pk}</ul>
  {note('This is a payment to MTG for your website only. It is separate from any ClickBaitPays campaign or activation fee.', 'info')}
 </div>
 <form class="oform" data-order data-wa="{esc(OWNER['wa'])}" novalidate aria-labelledby="of-h">
  <h2 id="of-h">Order in 2 minutes</h2>
  <p class="small">It goes straight to MTG on WhatsApp. Nothing is stored on this website.</p>
  <div class="field"><label for="o-name">Your name, as it should appear *</label><input id="o-name" name="name" required autocomplete="name"></div>
  <div class="field"><label for="o-wa">Your WhatsApp number *</label><input id="o-wa" name="wa" required inputmode="tel" autocomplete="tel"></div>
  <fieldset class="field"><legend>Your address *</legend>
   <label class="tog"><input type="radio" name="domain" value="mtgtribe.com/cbp/" checked required><span><span>mtgtribe.com/cbp/<i>yourname</i></span></span></label>
   <label class="tog"><input type="radio" name="domain" value="clickbaitpaysus.com/"><span><span>clickbaitpaysus.com/<i>yourname</i></span></span></label>
  </fieldset>
  <div class="field"><label for="o-slug">The name at the end of your address *</label><input id="o-slug" name="slug" required autocapitalize="none" spellcheck="false" aria-describedby="o-slug-h"><small id="o-slug-h">Letters and numbers only. Your page: <b data-out="addr">mtgtribe.com/cbp/yourname</b></small></div>
  <div class="field"><label for="o-ref">Your ClickBaitPays referral link *</label><input id="o-ref" name="ref" required inputmode="url" placeholder="https://clickbaitpays.me/join.php?ref=yourname" aria-describedby="o-ref-h"><small id="o-ref-h">Every Join button on your page will use this link. Find it on your back office dashboard (Copy).</small></div>
  <div class="field"><label for="o-group">Your WhatsApp group link (optional)</label><input id="o-group" name="group" inputmode="url"></div>
  <div class="row2"><div class="field"><label for="o-tt">TikTok (optional)</label><input id="o-tt" name="tiktok"></div><div class="field"><label for="o-fb">Facebook (optional)</label><input id="o-fb" name="fb"></div></div>
  <div class="field"><label for="o-yt">YouTube (optional)</label><input id="o-yt" name="yt"></div>
  <fieldset class="field"><legend>How you would like to pay</legend>
   <label class="tog"><input type="radio" name="pay" value="Rand (R1,000, bank details on WhatsApp)" checked><span>Rand (bank details on WhatsApp)</span></label>
   <label class="tog"><input type="radio" name="pay" value="USDT BEP20 ($50)"><span>USDT BEP20</span></label>
   <label class="tog"><input type="radio" name="pay" value="USDT TRC20 ($50)"><span>USDT TRC20</span></label>
  </fieldset>
  <div class="field"><label for="o-notes">Anything else? (optional)</label><textarea id="o-notes" name="notes" rows="3"></textarea></div>
  <button type="submit" class="btn btn-join ring lg">{ic('whatsapp')}<span>Send my order on WhatsApp</span></button>
  <p class="sent" data-sent hidden>{ic('check')}<span>Almost done: press <b>Send</b> in WhatsApp. MTG replies on {OWNER['wa_num']}. Didn't open? <a href="{OWNER['wa']}" target="_blank" rel="noopener">Open WhatsApp</a>.</span></p>
 </form>
</div>
</div></section></main>
'''
    out += footer() + tail()
    return out


# ============================================================== extras: sitemap, llms.txt, manifest
PAGES = [('', 'p_landing', 'cbp-home', 1.0), ('dashboard/', 'p_dashboard', 'cbp-dashboard', 0.9), ('calculator/', 'p_calc', 'cbp-calculator', 0.8),
         ('disclaimer/', 'p_disc', 'cbp-disclaimer', 0.3)]


def sitemap():
    urls = [SITE + BASE + p for p, *_ in PAGES] + [SITE + ORDER]
    body = ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n'


def llms():
    lv = '\n'.join(f'- Level {l}: campaign {p:,} USDT, one-time activation {a} USDT, {c:.2f} USDT per click, {n} clicks a day, campaign total {t:,.2f} USDT (platform figures)' for l, p, a, c, n, t in LEVELS)
    return f'''# ClickBaitPays Guide by MTG (mtgtribe.com/cbp)

> An independent, plain-English guide to ClickBaitPays (clickbaitpays.me), a paid-to-click advertising platform: members buy ad campaigns to advertise their own link and are paid in USDT for viewing other members' ads. By MTG (MusaTheGiant), "Your Digital Architect", an active member. Education only, not official ClickBaitPays material, not financial advice. Figures checked {CHECKED}.

## Pages

- [ClickBaitPays explained]({SITE}{BASE}): how it works in 5 steps, the 7 levels, Login Ads vs Ad Campaigns, how to join free, videos and FAQ.
- [Tutorials dashboard]({SITE}{BASE}dashboard/): step-by-step tutorials in order (back office tour, deposit, first campaign and activation, another campaign on an active level, withdrawal, Login Ads, Pay It Forward) and explainers.
- [ClickBaitPays Calculator]({SITE}{BASE}calculator/): pay today, clicks a day, the platform's campaign total and the approximate date it reaches the Available Balance.
- [Disclaimer and privacy]({SITE}{BASE}disclaimer/)
- [Get your own copy of this guide]({SITE}{ORDER}): R1,000 or $50 once-off.

## Key facts

- Joining is free, through a member's referral link. Register from home Wi-Fi (no VPN or mobile data during sign-up). One account per person, up to 3 per household under the same sponsor.
- Each campaign runs 12 click days. A click day counts when all of that level's daily clicks are done; clicks reset at midnight Panama time (7:00 AM in South Africa).
- Each in-dashboard ad has a 15-second countdown, then Confirm & Earn. Members receive 90% of the advertiser's cost per click.
- To earn at a level, pay its one-time activation fee once; it never expires. These fees also support the platform's sustainability.
- After the 12th click day, earnings are held 7 days, then move to the Available Balance: withdraw (once a week, minimum 10 USDT, 10% fee), Pay It Forward to another member, or buy a new campaign.
- Login Ads: 20 USDT for 30 days, shown to every member for 30 seconds at login; they pay nothing, they buy views.
- Referrals are optional; sponsors receive 10% of the campaigns their referrals buy.
{lv}
'''


def manifest():
    return json.dumps({'name': NAME, 'short_name': 'ClickBaitPays', 'start_url': BASE, 'scope': BASE, 'display': 'standalone',
                       'background_color': '#080015', 'theme_color': '#080015',
                       'icons': [{'src': BASE + 'assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                 {'src': BASE + 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                                 {'src': BASE + 'assets/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}, indent=1)


# ============================================================== build
def copy_assets(dst):
    os.makedirs(dst + '/og', exist_ok=True)
    pairs = [('favicon-cursor.ico', 'favicon.ico'), ('favicon-cursor-32.png', 'favicon-32.png'), ('apple-touch-icon.png', 'apple-touch-icon.png'),
             ('icon-192.png', 'icon-192.png'), ('icon-512.png', 'icon-512.png'), ('icon-maskable-512.png', 'icon-maskable-512.png'),
             ('clickbaitpays-logo-disc-256.webp', 'logo-disc-256.webp'), ('clickbaitpays-logo-256.webp', 'logo-256.webp')]
    for a, b in pairs:
        shutil.copyfile(os.path.join(BRAND, a), os.path.join(dst, b))
    for f in ('cbp.css', 'cbp.js'):
        shutil.copyfile(os.path.join(SRC, f), os.path.join(dst, f))
    from PIL import Image                     # YouTube thumbnails, self-hosted: 4:3 letterbox cropped to 16:9
    os.makedirs(dst + '/yt', exist_ok=True)
    for vid, *_ in YOUTUBE:
        im = Image.open(os.path.join(SRC, 'yt', vid + '.jpg')).convert('RGB')
        w, h = im.size; ch = round(w * 9 / 16); top = (h - ch) // 2
        im.crop((0, top, w, top + ch)).save(os.path.join(dst, 'yt', vid + '.webp'), 'WEBP', quality=80, method=6)
    for root, _, files in os.walk(dst):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), dst).replace(os.sep, '/')
            HASH[rel] = hashlib.sha1(open(os.path.join(root, f), 'rb').read()).hexdigest()[:8]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def render(fn):
    USED_ICONS.clear()
    page = fn()
    return page.replace('<!--SPRITE-->', '')


def main():
    out = os.path.join(ROOT, 'cbp')
    copy_assets(os.path.join(out, 'assets'))
    built = {}
    for p, fn, og, pr in PAGES:
        built[p] = render(globals()[fn])
        write(os.path.join(out, p, 'index.html'), built[p])
    write(os.path.join(ROOT, 'cbpcopy', 'index.html'), render(p_order))
    write(os.path.join(out, 'sitemap.xml'), sitemap())
    write(os.path.join(out, 'llms.txt'), llms())
    write(os.path.join(out, 'manifest.webmanifest'), manifest())
    # guard: no em or en dashes anywhere in the output
    bad = []
    for root, _, files in os.walk(out):
        if '_build' in root:
            continue
        for f in files:
            if f.endswith(('.html', '.txt', '.xml', '.webmanifest', '.css', '.js')):
                t = open(os.path.join(root, f), encoding='utf-8').read()
                if '—' in t or '–' in t:
                    bad.append(os.path.join(root, f))
    t = open(os.path.join(ROOT, 'cbpcopy', 'index.html'), encoding='utf-8').read()
    if '—' in t or '–' in t:
        bad.append('cbpcopy/index.html')
    print('built', len(PAGES) + 1, 'pages;', 'DASH CHECK FAILED: ' + ', '.join(bad) if bad else 'no dashes')


if __name__ == '__main__':
    main()
