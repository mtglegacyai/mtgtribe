"""ClickBaitPays Guide by MTG (mtgtribe.com/cbp): static site builder.

python3 cbp/_build/build.py                 builds /cbp/ and /cbpcopy/ into the repo
python3 cbp/_build/build.py --preview DIR   writes a private review copy with relative links (tools/qa/README.md)
NODE_PATH=$(npm root -g) python3 cbp/_build/covers.py   draws the wide video covers (assets/v/*.webp)
NODE_PATH=$(npm root -g) python3 cbp/_build/og.py       draws every page's social preview (assets/og/*.jpg)

Layout (MTG, 22 Nov 2026: "clean pages, to the point pages. Each page must target one section, one idea at a time ... the
dashboard navigation menu is there for a reason ... navigation arrows back and forward, up and down"):
- the main page is short: three videos (Welcome, Income Strategy, Back Office Walkthrough), then the way into the dashboard;
- the dashboard holds everything else, one short page per topic, each with its video, one call to action, the Previous and
  Next arrows (top and bottom of the page) and the Up and Down buttons;
- every video is a wide cover in the slim laptop frame (CLAUDE.md, 17 Nov 2026); 16:9 videos play in place, 9:16 videos
  open the pop-up's phone; the player has its own Full Screen and Close bar and closes itself at the end.
One source of truth for every fact, price and link: CONFIG below.
"""
import hashlib, html, json, os, posixpath, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # repo root
HERE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE_DIR, 'src')
BRAND = os.path.join(ROOT, 'tools', 'cbp', 'brand')

# ============================================================== CONFIG (facts checked 21 and 22 November 2026)
SITE = 'https://mtgtribe.com'
BASE = '/cbp/'
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

# Videos. yt: a YouTube video on the ClickBaitPays Us channel (plays in place, from youtube-nocookie.com).
# src: a video file (when MTG's own tutorials are ready). Neither: a placeholder ("Coming soon" or "Being recorded").
# o: 'h' 16:9 (plays in the laptop) or 'v' 9:16 (opens the pop-up's phone). Cover: assets/v/<code>.webp (covers.py).
V = {
    'welcome': dict(label='Video 1', title='Welcome to ClickBaitPays', short='Welcome', yt='gWkLEgBFVEY', secs=351,
                    line='What ClickBaitPays is, who it is for, and how a click turns into USDT.'),
    'strategy': dict(label='Video 2', title='Compensation plan and income strategy', short='Compensation plan', yt='MiUja2RnWXY', secs=457,
                     line='The plan with real-world examples, and the 10% referral commission.'),
    'backoffice': dict(label='Video 3', title='Back office walkthrough', short='Back office', yt='EDnb9e03B0E', secs=686,
                       line='Every part of the member back office, so you know your way around before you start.'),
    'presentation': dict(label='Presentation', title='The full presentation (14 Sept 2026)', short='Presentation', yt='25wXab2hAB8', secs=947,
                         line='How it works from start to finish: ads, campaigns and withdrawals.'),
    'qa': dict(label='Live Q&A', title='Members\' questions answered (29 Aug 2026)', short='Live Q&A', yt='8rftor87kKQ', secs=1361,
               line='Ad viewing, affiliates, Pay It Forward, withdrawals and strategy, answered live.'),
    'tour': dict(label='Site tour', title='How to use this guide', short='How to use this guide', status='soon',
                 line='Where everything is, and the order to watch the tutorials.'),
    'e1': dict(label='Explainer', title='Got a link? Get it seen', short='Promote your link', status='soon',
               line='Put any program in front of real people, and get paid while you do.'),
    'e2': dict(label='Explainer', title='How to join ClickBaitPays', short='How to join', status='soon',
               line='Free sign-up through a member\'s link, the house rules and your first steps.'),
    'e3': dict(label='Explainer', title='Levels, activation and earnings', short='The levels', status='soon',
               line='Seven levels, one activation per level, and what each click pays.'),
    'e4': dict(label='Explainer', title='The 12 + 7 timeline', short='12 + 7 timeline', status='soon',
               line='Click for 12 days, a 7-day hold, then your Available Balance.'),
    't1': dict(label='Tutorial 1', title='Your back office: a quick tour', short='Back office tour', status='record',
               line='Every menu item, so you always know where things are.'),
    't2': dict(label='Tutorial 2', title='How to deposit USDT', short='Deposit', status='record',
               line='Fund your account through the Deposit page, safely.'),
    't3': dict(label='Tutorial 3', title='Your first campaign on a new level', short='First campaign', status='soon',
               line='Buy a Level 4 campaign, activate Level 4 once and click the 5 daily ads.'),
    't4': dict(label='Tutorial 4', title='Another campaign on an active level', short='Another campaign', status='soon',
               line='Why the second campaign at a level needs no activation fee.'),
    't5': dict(label='Tutorial 5', title='How to request a withdrawal', short='Withdraw', status='record',
               line='Move your Available Balance to your own wallet.'),
    't6': dict(label='Tutorial 6', title='How to create a Login Ad', short='Login Ad', status='soon',
               line='Every member sees your link for 30 seconds when they log in, for 30 days.'),
    't7': dict(label='Tutorial 7', title='How to Pay It Forward', short='Pay It Forward', status='soon', o='v',
               line='Help a team member get started from your Available Balance.'),
}
for _k, _v in V.items():
    _v.setdefault('o', 'h')
    _v['code'] = _k
STATUS = {'soon': 'Coming soon', 'record': 'Being recorded'}

# THE MESSAGE (MTG, 22 Nov 2026): if it has a link, ClickBaitPays gets it seen, and pays you while it does. tools/cbp/MESSAGE.md
PROGRAMS = ['BellverCards', 'Bitcoin Wealth', 'JetUP', 'XFUSION', 'Solar Group', 'Aureus Alliance', 'Stokvel and smart contract platforms',
            'MLM programs', 'Affiliate programs', 'Digital products', 'Your own business']
STORY = ('I was clicking my daily ads when a BellverCards ad caught my eye. I opened it, I liked what I saw, and I joined. '
         'Today I am earning with BellverCards and ranking up. One ad, in front of the right person, at the right time. '
         'It worked on me. It can work for your link.')
NICHES = [
    ('users', 'Team builders and MLM leaders', 'JetUP, XFUSION, Solar Group, Aureus Alliance: a team grows one yes at a time. More eyes on your link means more chances at a yes. Fish with a net, not a single line.'),
    ('layers', 'Stokvel and smart contract platforms', 'Bitcoin Wealth and every stokvel run on new members. ClickBaitPays members already fund accounts in crypto, so a wallet and a smart contract do not scare them off.'),
    ('card', 'Card and crypto programs', 'BellverCards is how MTG proved it: he found it through an ad right here, joined, and is ranking up. Your program could be the next ad someone acts on.'),
    ('link', 'Affiliate marketers', 'No clicks, no commissions. ClickBaitPays turns your affiliate link into daily visits from real people, and pays you while it does.'),
    ('gift', 'Digital product sellers', 'A great product nobody sees is a secret, not a business. Put your sales page where people are already looking.'),
    ('globe', 'Any business with a website', 'A shop on a street nobody walks down sells nothing. ClickBaitPays is the busy street, and people are paid to stop and look.'),
]
STREAMS = [
    ('trend', 'Your program grows', 'Your ad sends real people to BellverCards, Bitcoin Wealth, JetUP or whatever you promote. The ones it speaks to join, buy or sign up under you.'),
    ('coins', 'Your clicks pay', 'While your ad works, you view theirs and get paid in USDT: from 0.48 to 13.50 per click, by level, every click day.'),
    ('users', 'Your referrals pay', 'Share your ClickBaitPays link and receive 10% of the campaigns your referrals buy. Optional, and it stacks.'),
]
CLONE = ['It sells the real reason people join: traffic for what they already promote',
         'Every step on video, in laptop and phone players that close themselves at the end',
         'A compensation plan page with the numbers, a 3D level staircase and a calculator',
         'An Is It Legit? page that turns doubters into members',
         'Built for phones: a quick bar, and nothing scrolls sideways',
         'Your link on every Join button, your WhatsApp group and socials on every page',
         'Built to be found: search titles, social previews and structured data on every page',
         'Kept up to date as MTG adds new videos']


def mmss(s):
    return f'{s // 60}:{s % 60:02d}'


def playable(code):
    return bool(V[code].get('yt') or V[code].get('src'))


# The menu, in reading order: (key, page path under /cbp/ ('cbpcopy/' is the order page at /cbpcopy/), menu label, menu line, icon, group).
# The Previous and Next arrows follow this order.
NAV = [
    ('home', 'dashboard/', 'Welcome', 'Start here, in order', 'compass', 'Start Here'),
    ('what', 'dashboard/what-is-clickbaitpays/', 'What Is ClickBaitPays?', 'Advertise, view, get paid', 'cursor', 'Start Here'),
    ('grow', 'dashboard/promote-your-link/', 'Promote Your Link', 'Traffic for any program', 'mega', 'Start Here'),
    ('plan', 'dashboard/compensation-plan/', 'Compensation Plan', 'How you earn, on video', 'coins', 'Start Here'),
    ('how', 'dashboard/how-it-works/', 'How It Works', 'Five steps, start to payout', 'map', 'Start Here'),
    ('join', 'dashboard/join/', 'How To Join', 'Free, through a member\'s link', 'userplus', 'Start Here'),
    ('levels', 'dashboard/levels/', 'The 7 Levels', 'Prices, clicks and activation', 'layers', 'Levels And Earnings'),
    ('timeline', 'dashboard/timeline/', 'The 12 + 7 Timeline', 'When your earnings are yours', 'cal', 'Levels And Earnings'),
    ('calc', 'calculator/', 'Calculator', 'Cost, clicks and payout date', 'calc', 'Levels And Earnings'),
    ('daily', 'dashboard/daily-routine/', 'Your Daily Routine', 'Log in, click, done', 'repeat', 'Every Day'),
    ('tutorials', 'dashboard/tutorials/', 'All Tutorials', 'Seven, in the right order', 'film', 'Tutorials'),
    ('t1', 'dashboard/tutorials/back-office-tour/', 'Back Office Tour', 'Tutorial 1', 'n1', 'Tutorials'),
    ('t2', 'dashboard/tutorials/deposit/', 'Deposit USDT', 'Tutorial 2', 'n2', 'Tutorials'),
    ('t3', 'dashboard/tutorials/first-campaign/', 'Your First Campaign', 'Tutorial 3', 'n3', 'Tutorials'),
    ('t4', 'dashboard/tutorials/another-campaign/', 'Another Campaign', 'Tutorial 4', 'n4', 'Tutorials'),
    ('t5', 'dashboard/tutorials/withdraw/', 'Withdraw', 'Tutorial 5', 'n5', 'Tutorials'),
    ('t6', 'dashboard/tutorials/login-ad/', 'Create A Login Ad', 'Tutorial 6', 'n6', 'Tutorials'),
    ('t7', 'dashboard/tutorials/pay-it-forward/', 'Pay It Forward', 'Tutorial 7', 'n7', 'Tutorials'),
    ('videos', 'dashboard/videos/', 'Video Library', 'Every video in one place', 'youtube', 'Help'),
    ('legit', 'dashboard/is-clickbaitpays-legit/', 'Is It Legit?', 'Check it for yourself', 'shield', 'Help'),
    ('faq', 'dashboard/faq/', 'FAQ', 'Straight answers, and the live Q&A', 'help', 'Help'),
    ('disc', 'disclaimer/', 'Disclaimer', 'The small print, in plain words', 'info', 'Help'),
    ('copy', 'cbpcopy/', 'Get This Website', 'Your own copy, your link', 'globe', 'More From MTG'),
]
MENU_EXT = [('tribe', GROUP, 'Join The MTG TRIBE', 'WhatsApp community', 'whatsapp', 'More From MTG')]   # in the menu, not in the page order
OLD_PATHS = {'dashboard/income-strategy/': 'plan', 'dashboard/grow-what-you-promote/': 'grow'}      # addresses that moved: a short forwarding page stays behind
NAVD = {n[0]: n for n in NAV}
KEYS = [n[0] for n in NAV]

# search titles (60 characters at most) and descriptions (about 155 characters) for every page
SEO = {
    'landing': ('ClickBaitPays: Promote Any Link and Get Paid to View Ads',
                'Got a link? ClickBaitPays puts BellverCards, Bitcoin Wealth, JetUP, MLM, affiliate and stokvel links in front of real people, and pays you in USDT to view ads.'),
    'home': ('ClickBaitPays Dashboard: Every Topic and Tutorial, in Order',
             'The ClickBaitPays dashboard by MTG: one short page per topic, from the compensation plan and how to join to the 7 levels, the 12 + 7 timeline and tutorials.'),
    'what': ('What Is ClickBaitPays? The Paid-to-Click Platform Explained',
             'ClickBaitPays explained simply: put any link in front of real people, get paid in USDT to view their ads, and grow every income stream you already have.'),
    'grow': ('Promote Your Link on ClickBaitPays: Traffic for Any Program',
             'Promote BellverCards, Bitcoin Wealth, JetUP, XFUSION, MLM, affiliate, stokvel or digital product links to real people on ClickBaitPays, and get paid too.'),
    'plan': ('ClickBaitPays Compensation Plan Explained, With Video',
             'The ClickBaitPays compensation plan in plain English: pay per click at all 7 levels, the one-time activation, the 10% referral commission and the 12 + 7 payout.'),
    'how': ('How ClickBaitPays Works: 5 Steps From Sign-Up to Payout',
            'How ClickBaitPays works in 5 steps: join free, fund your account, buy and activate a campaign, click your daily ads, then use your Available Balance.'),
    'join': ('How to Join ClickBaitPays Free: 3 Steps and the House Rules',
             'Join ClickBaitPays free in 3 steps through a member\'s link. The house rules: home Wi-Fi only, one account per person, up to 3 per household, same sponsor.'),
    'levels': ('ClickBaitPays Levels: Prices, Activation and Pay Per Click',
               'All 7 ClickBaitPays levels in one table: the campaign price, the one-time activation fee, pay per click, clicks a day and the platform\'s own campaign total.'),
    'timeline': ('ClickBaitPays 12 + 7 Timeline: When Your Earnings Are Yours',
                 'Click your ClickBaitPays ads on 12 days, the earnings rest 7 days, then they reach your Available Balance. Clicks reset at 7:00 AM in South Africa.'),
    'calc': ('ClickBaitPays Calculator: Cost, Daily Clicks and Payout Date',
             'Pick a ClickBaitPays level and see what you pay today, your clicks a day, the platform\'s campaign total and roughly when it reaches your Available Balance.'),
    'daily': ('ClickBaitPays Daily Routine: How to Click Your Ads Each Day',
              'Your ClickBaitPays daily routine in 4 steps: log in, open Click Ads, view each ad for 15 seconds, Confirm and Earn. New clicks every day from 7:00 AM SAST.'),
    'tutorials': ('ClickBaitPays Tutorials: 7 Step-by-Step Videos, in Order',
                  'Every ClickBaitPays tutorial in order: back office tour, deposit, your first campaign, another campaign, withdrawal, Login Ads and Pay It Forward.'),
    't1': ('ClickBaitPays Back Office Tour: Every Menu Item Explained',
           'A quick tour of the ClickBaitPays back office: your dashboard, ad campaigns, activation, Click Ads, deposits, withdrawals and Pay It Forward, step by step.'),
    't2': ('How to Deposit USDT Into ClickBaitPays, Step by Step',
           'How to deposit USDT into ClickBaitPays safely: enter the amount, pay through NOWPayments, use a fresh address every time and wait for the confirmation.'),
    't3': ('How to Buy and Activate Your First ClickBaitPays Campaign',
           'Buy your first ClickBaitPays ad campaign on a new level, activate earning once, and click your daily ads: title, link, Preview, Confirm Purchase, step by step.'),
    't4': ('ClickBaitPays: Buy Another Campaign on an Active Level',
           'Buy another ClickBaitPays campaign on a level you already activated: no activation fee the second time, two tabs on Click Ads, and the 12 + 7 timeline.'),
    't5': ('How to Withdraw From ClickBaitPays: Rules and Steps',
           'How to request a ClickBaitPays withdrawal: once a week, a 10 USDT minimum and a 10% fee, your wallet address and your Security PIN, step by step.'),
    't6': ('How to Create a ClickBaitPays Login Ad (20 USDT, 30 Days)',
           'Create a ClickBaitPays Login Ad: every member sees your link for 30 seconds when they log in, for 30 days, for 20 USDT. Title, link, Preview, step by step.'),
    't7': ('How to Pay It Forward on ClickBaitPays: Send to a Member',
           'Pay It Forward on ClickBaitPays: send funds from your Available Balance to another member. Check the username twice, add a message, confirm with your PIN.'),
    'videos': ('ClickBaitPays Videos: Overview, Strategy, Tutorials and Q&A',
               'Every ClickBaitPays video in one place: the welcome video, income strategy, back office walkthrough, the full presentation, the live Q&A and the tutorials.'),
    'legit': ('Is ClickBaitPays Legit? A Member\'s Honest Look (2026)',
              'Is ClickBaitPays legit or a scam? What it is, where the pay comes from, what MTG sees in his own account, and how to check it yourself with a small start.'),
    'faq': ('ClickBaitPays FAQ: Straight Answers to the Top Questions',
            'ClickBaitPays questions answered: is it free, how members get paid, the activation fee, withdrawals, logging in, Login Ads and referrals. Plus a live Q&A.'),
    'copy': ('Get This ClickBaitPays Website: Your Link, R1,000 Once-Off',
             'Own this ClickBaitPays guide with your referral link on every Join button, every video and tutorial, at mtgtribe.com/cbp/yourname. Pay only if you like it.'),
    'disc': ('Disclaimer and Privacy | ClickBaitPays Guide by MTG',
             'The small print in plain words: an independent ClickBaitPays guide, the referral link disclosure, where the figures come from and what this site stores.'),
}

# ============================================================== small helpers
ICONS = json.load(open(os.path.join(SRC, 'icons.json'), encoding='utf-8'))
_LINE = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICONS.update({
    'i-max': {'attrs': _LINE, 'body': '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>'},
    'i-min': {'attrs': _LINE, 'body': '<path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/>'},
    'i-up': {'attrs': _LINE.replace('"2"', '"2.4"'), 'body': '<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>'},
    'i-dn': {'attrs': _LINE.replace('"2"', '"2.4"'), 'body': '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>'},
    'i-chl': {'attrs': _LINE.replace('"2"', '"2.4"'), 'body': '<path d="m15 18-6-6 6-6"/>'},
    'i-chr': {'attrs': _LINE.replace('"2"', '"2.4"'), 'body': '<path d="m9 18 6-6-6-6"/>'},
    'i-login': {'attrs': _LINE, 'body': '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="m10 17 5-5-5-5"/><path d="M15 12H3"/>'},
    'i-pf': {'attrs': 'viewBox="0 0 24 24" fill="currentColor" stroke="none"', 'body': '<path d="M8 5.2v13.6a1 1 0 0 0 1.5.86l11-6.8a1 1 0 0 0 0-1.72l-11-6.8A1 1 0 0 0 8 5.2z"/>'},
})
for _n in range(1, 8):      # number badges for the tutorials in the menu
    ICONS[f'i-n{_n}'] = {'attrs': 'viewBox="0 0 24 24"', 'body': f'<text x="12" y="17" text-anchor="middle" font-family="Orbitron,sans-serif" font-weight="900" font-size="14" fill="currentColor">{_n}</text>'}
USED_ICONS = set()
HASH = {}
MODE = 'prod'          # 'prod' or 'preview'


def esc(s):
    return html.escape(str(s), quote=True)


def ic(name, cls='ic'):
    USED_ICONS.add(name)
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def sprite():
    out = []
    for n in sorted(USED_ICONS):
        s = ICONS['i-' + n]
        out.append(f'<symbol id="i-{n}" {s["attrs"]}>{s["body"]}</symbol>')
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + ''.join(out) + '</defs></svg>'


def money(v):
    return f'{v:,.2f}'


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def prod_url(path):
    """the live address of a page or file path under /cbp/ ('cbpcopy/...' lives at /cbpcopy/)"""
    return '/' + path if path.startswith('cbpcopy/') else BASE + path


def L(target, here):
    """link from the page at `here` to `target` (page paths end in '/', files do not; '#frag' allowed).
    Live: absolute addresses with a content version on files. Preview: relative links to files."""
    frag = ''
    if '#' in target:
        target, frag = target.split('#', 1)
        frag = '#' + frag
    if target.startswith(('http', 'mailto:')):
        return target + frag
    is_page = target == '' or target.endswith('/')
    if MODE == 'prod':
        url = prod_url(target)
        if not is_page and target.startswith('assets/') and target[7:] in HASH:
            url += '?v=' + HASH[target[7:]]
        return url + frag
    tgt = (target + 'index.html') if is_page else target
    if target == '' and frag and here == '':
        return frag
    return posixpath.relpath(tgt, here.rstrip('/') or '.') + frag


def A(target, here):
    return esc(L(target, here))


def page_link(key, here):
    return A(NAVD[key][1], here)


# ============================================================== components
def btn(label, href, kind='ghost', icon=None, cls='', ext=False, attrs=''):
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="btn btn-{kind} {cls}" href="{href}"{tgt} {attrs}>{ic(icon) if icon else ""}<span>{label}</span></a>'


def join_btn(label='Join ClickBaitPays Free', cls='', size=''):
    return (f'<a class="btn btn-join ring {size} {cls}" href="{esc(OWNER["ref"])}" target="_blank" rel="sponsored noopener" '
            f'data-join>{ic("userplus")}<span>{label}</span><span class="sr"> (opens the official sign-up page in a new tab)</span></a>')


def dash_btn(here, label='Open The Dashboard', cls='', size=''):
    return f'<a class="btn btn-dash ring {size} {cls}" href="{A("dashboard/", here)}">{ic("layers")}<span>{label}</span></a>'


def fair(cls=''):
    return f'<p class="fair {cls}">{ic("check")}<span>Free account. Invited by someone else? Please use their link.</span></p>'


def note(body, icon='info', cls=''):
    return f'<div class="note {cls}">{ic(icon)}<div>{body}</div></div>'


def checks(items):
    return '<ul class="checks">' + ''.join(f'<li>{ic("check")}<span>{i}</span></li>' for i in items) + '</ul>'


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


def cover(code, here):
    return L(f'assets/v/{code}.webp', here), L(f'assets/v/{code}-640.webp', here)


def bar_text(v):
    return f'{v["label"]} · {v["short"]}'


def player(wide=True, inner='', left='', right='', pid=''):
    """The one video player (MTG, 16 Nov 2026), as on /bw: the slim laptop for a 16:9 video, the slim phone for a 9:16 one.
    The screen has the video's own shape and nothing lies on the picture: the camera, Full Screen and Close sit in the bar."""
    idattr = f' id="{pid}"' if pid else ''
    return (f'<div class="pl {"pl-h" if wide else "pl-v"}"{idattr}><div class="pl-dev"><div class="pl-bar">'
            f'<span class="pl-l"><span class="pl-tx">{left}</span>'
            f'<button type="button" class="pl-b pl-max" data-pl-max aria-label="Full Screen">{ic("max", "ic i-max")}{ic("min", "ic i-min")}'
            f'<span class="t t-max">Full Screen</span><span class="t t-min">Exit Full Screen</span></button></span>'
            f'<i class="pl-cam" aria-hidden="true"></i>'
            f'<span class="pl-r"><span class="pl-tx">{right}</span>'
            f'<button type="button" class="pl-b pl-x" data-pl-x aria-label="Close the video"><span class="t">Close</span>{ic("x")}</button></span>'
            f'</div><div class="pl-scr">{inner}</div></div><i class="pl-deck" aria-hidden="true"><i></i></i></div>')


def vid(code, here, hero=False, cap=True, eager=False, num=None):
    """A video on the page: ALWAYS a wide cover in the slim laptop frame (CLAUDE.md, 17 Nov 2026).
    A 16:9 video plays in place; a 9:16 video opens the pop-up's phone; a placeholder says when it is coming."""
    v = V[code]
    big, small = cover(code, here)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    img = (f'<img src="{esc(small)}" srcset="{esc(small)} 640w, {esc(big)} 1280w" sizes="(max-width:900px) 94vw, 680px" width="1280" height="720" '
           f'{load} decoding="async" alt="{esc(v["title"])}: video cover">')
    if playable(code):
        how = (f'data-yt="{v["yt"]}"' if v.get('yt') else f'data-src="{esc(L(v["src"], here))}"') if v['o'] == 'h' else f'data-play="{code}"'
        ctl = (f'<button type="button" class="vplay{" pulse" if hero else ""}" {how} data-code="{code}" '
               f'aria-label="Play {esc(v["title"])} ({mmss(v["secs"])})"><span class="pbtn">{ic("pf")}</span></button>')
        right = mmss(v['secs'])
    else:
        ctl = (f'<button type="button" class="vsoon" data-soon="{esc(v["title"])}" aria-label="{esc(v["title"])}: {STATUS[v["status"]]}">'
               f'<span class="vs-in">{ic("timer")}<b>{STATUS[v["status"]]}</b></span></button>')
        right = STATUS[v['status']]
    fc = ''
    if cap:
        n = f'<span class="vnum">{num}</span>' if num else ''
        fc = (f'<figcaption class="vcap">{n}<span class="vct"><b>{esc(v["title"])}</b><small>{esc(v["label"])} · '
              f'{mmss(v["secs"]) if playable(code) else STATUS[v["status"]]}</small></span></figcaption>')
    return f'<figure class="vid" data-vid="{code}">{player(True, img + ctl, esc(bar_text(v)), right)}{fc}</figure>'


def vrow(code, here, href=None):
    """a compact video row: the cover, what it is, one button. Plays in the pop-up (real) or links to its page (coming)."""
    v = V[code]
    big, small = cover(code, here)
    meta = f'{v["label"]} · {mmss(v["secs"]) if playable(code) else STATUS[v["status"]]}'
    img = f'<img src="{esc(small)}" width="640" height="360" loading="lazy" decoding="async" alt="">'
    if playable(code):
        return (f'<button type="button" class="vrow" data-play="{code}" aria-label="Play {esc(v["title"])} ({mmss(v["secs"])})">{img}'
                f'<span class="vr-t"><small>{esc(meta)}</small><b>{esc(v["title"])}</b><span>{esc(v["line"])}</span></span>'
                f'<span class="vr-go play">{ic("pf")}<span>Play</span></span></button>')
    return (f'<a class="vrow soon" href="{href}">{img}<span class="vr-t"><small>{esc(meta)}</small><b>{esc(v["title"])}</b><span>{esc(v["line"])}</span></span>'
            f'<span class="vr-go">{ic("chr")}<span>Open</span></span></a>')


def social_row(cls='soc'):
    items = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{esc(label)} (opens in a new tab)">{ic(k)}</a>' for k, label, u in SOCIAL)
    return f'<div class="{cls}">{items}</div>'


def video_data(here):
    """what the pop-up player needs to play a video by its code"""
    d = {}
    for k, v in V.items():
        if not playable(k):
            continue
        big, small = cover(k, here)
        d[k] = dict(t=v['title'], o=v['o'], d=mmss(v['secs']), p=big, bar=bar_text(v))
        if v.get('yt'):
            d[k]['yt'] = v['yt']
        else:
            d[k]['s'] = L(v['src'], here)
    return json.dumps(d, separators=(',', ':'), ensure_ascii=False)


# ============================================================== head
PERSON_ID = SITE + BASE + '#mtg'
SITE_ID = SITE + BASE + '#site'
CBP_THING = {'@type': 'Organization', 'name': 'ClickBaitPays', 'url': OFFICIAL, 'sameAs': [OFFICIAL]}


def person_ld():
    return {'@type': 'Person', '@id': PERSON_ID, 'name': 'MTG (MusaTheGiant)', 'alternateName': ['MTG', 'Musa The Giant'],
            'jobTitle': 'Your Digital Architect', 'url': SITE + '/', 'sameAs': [u for k, l, u in SOCIAL if k != 'whatsapp']}


def crumbs_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': p if p.startswith('http') else SITE + prod_url(p)} for i, (n, p) in enumerate(items)]}


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap">')

def head(key, path, here, ld, page_type='WebPage', extra=''):
    title, desc = SEO[key]
    url = SITE + prod_url(path)
    og = f'{SITE}{BASE}assets/og/cbp-{key}.jpg?v={HASH.get("og/cbp-" + key + ".jpg", "1")}'
    graph = [person_ld(),
             {'@type': 'WebSite', '@id': SITE_ID, 'name': NAME, 'url': SITE + BASE, 'inLanguage': 'en-ZA', 'publisher': {'@id': PERSON_ID}},
             {'@type': page_type, '@id': url + '#page', 'url': url, 'name': title, 'description': desc, 'inLanguage': 'en-ZA',
              'isPartOf': {'@id': SITE_ID}, 'about': CBP_THING, 'author': {'@id': PERSON_ID}, 'dateModified': TODAY,
              'primaryImageOfPage': {'@type': 'ImageObject', 'url': og, 'width': 1200, 'height': 630}}] + ld
    for x in ld:
        if x.get('@type') == 'BreadcrumbList':
            x['@id'] = url + '#breadcrumb'
            graph[2]['breadcrumb'] = {'@id': x['@id']}
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="MTG (MusaTheGiant)">
<meta name="theme-color" content="#080015">
<meta name="color-scheme" content="dark">
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
<link rel="icon" href="{A('assets/favicon.ico', here)}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{A('assets/favicon-32.png', here)}">
<link rel="apple-touch-icon" href="{A('assets/apple-touch-icon.png', here)}">
<link rel="manifest" href="{A('manifest.webmanifest', here)}">
{FONTS}
{extra}<link rel="stylesheet" href="{A('assets/cbp.css', here)}">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))}</script>'''


# ============================================================== shared pieces of every page
def brand(here, cls='brand'):
    return (f'<a class="{cls}" href="{A("", here)}" aria-label="{esc(NAME)}: home"><img src="{A("assets/logo-disc-256.webp", here)}" alt="" width="44" height="44">'
            f'<span class="bt"><b>ClickBaitPays</b><small>Guide by MTG 👑</small></span></a>')


def updown():
    """the Up and Down buttons (MTG, 22 Nov 2026: "navigation arrows ... up and down"): Up goes to the top, Down to the next part"""
    return (f'<div class="ud" data-ud><button type="button" class="ud-b" data-up aria-label="Up: back to the top" title="Back to the top">{ic("up")}</button>'
            f'<button type="button" class="ud-b" data-down aria-label="Down: the next part of this page" title="Next part">{ic("dn")}</button></div>')


def qbar(key, here, landing=False):
    """the quick bar at the bottom of a phone (MTG, 22 Nov 2026: the plan and the videos "easily accessible ... easy to navigate to"):
    Home, Videos, Join (in the middle), Plan, and the menu"""
    def item(k, href, icon, label):
        cur = ' aria-current="page"' if k == key else ''
        return f'<a class="qb" href="{href}"{cur}>{ic(icon)}<span>{label}</span></a>'
    last = (f'<a class="qb" href="{A("dashboard/", here)}">{ic("menu")}<span>Menu</span></a>' if landing else
            f'<button type="button" class="qb" data-qmenu aria-controls="cbp-menu">{ic("menu")}<span>Menu</span></button>')
    return (f'<nav class="qbar" aria-label="Quick menu">{item("landing", A("", here), "home", "Home")}{item("videos", page_link("videos", here), "film", "Videos")}'
            f'<a class="qb qb-join" href="{esc(OWNER["ref"])}" target="_blank" rel="sponsored noopener">{ic("userplus")}<span>Join Free</span></a>'
            f'{item("plan", page_link("plan", here), "coins", "Plan")}{last}</nav>')


def popup():
    return (f'<div class="sheet player" id="player" role="dialog" aria-modal="true" aria-label="Video player" hidden><div class="sheet-in">'
            f'{player(True, pid="pl-pop")}</div></div><div class="toast" id="toast" role="status" aria-live="polite"></div>')


def scripts(here):
    flag = 'window.CBP_PREVIEW=1;' if MODE == 'preview' else ''      # the private preview cannot embed YouTube
    js = f'<script>{flag}window.CBPV={video_data(here)};</script>\n<script src="{A("assets/cbp.js", here)}" defer></script>\n'
    if MODE == 'prod':
        js += ('<script src="/assets/video-return.js?v=1" defer></script>\n<script src="/assets/zoom-cta.js?v=5" defer></script>\n'
               '<script src="/assets/wa-message.js?v=3" defer></script>\n')
    else:
        js += f'<script src="{A("assets/video-return.js", here)}" defer></script>\n<script src="{A("assets/wa-message.js", here)}" defer></script>\n'
    return js


def copy_btn(here, label='Get This Website', cls=''):
    return f'<a class="btn btn-gold ring {cls}" href="{page_link("copy", here)}">{ic("globe")}<span>{label}</span></a>'


def plan_btn(here, label='See The Compensation Plan', cls=''):
    return f'<a class="btn btn-dash ring {cls}" href="{page_link("plan", here)}">{ic("coins")}<span>{label}</span></a>'


RISK = ('ClickBaitPays is an advertising platform, not an investment. Figures shown are the platform\'s own; what you earn depends '
        'on the ads you view, and nothing is guaranteed. The Join buttons carry MTG\'s referral link.')


def doc(head_html, body_cls, body):
    """the whole page. In a preview, the main page leaves out the document skeleton (the host adds it)."""
    page = f'<a class="skip" href="#main">Skip to content</a>{sprite()}{body}'
    return f'<!doctype html>\n<html lang="en-ZA">\n<head>\n{head_html}\n</head>\n<body class="{body_cls}">\n{page}\n</body>\n</html>\n'


# ---------------------------------------------------------------- dashboard shell
def sidebar(key, here):
    out, group = [], None
    for k, p, label, sub, icon, g in NAV + MENU_EXT:
        if g != group:
            out.append(f'<p class="md-label">{g}</p>')
            group = g
        if k in dict((m[0], m) for m in MENU_EXT):
            out.append(f'<a class="md-nav ext" href="{esc(p)}" target="_blank" rel="noopener"><span class="ic">{ic(icon)}</span><span class="tx"><b>{label}</b><small>{sub}</small></span>'
                       f'{ic("ext", "ic xl")}<span class="sr">(opens in a new tab)</span></a>')
            continue
        cur = ' aria-current="page"' if k == key else ''
        cls = ' tut' if k[0] == 't' and k[1:].isdigit() else (' gold' if k in ('plan', 'copy') else '')
        out.append(f'<a class="md-nav{cls}" href="{A(p, here)}"{cur}><span class="ic">{ic(icon)}</span><span class="tx"><b>{label}</b><small>{sub}</small></span></a>')
    soc = {k: (l, u) for k, l, u in SOCIAL}
    b = lambda href, icon, label, cls='', ext=True: (f'<a class="sbtn {cls}" href="{href}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{icon}<span>{label}</span></a>')
    grid = ''.join([
        b(LOGIN, ic('login'), 'Member Login'),
        b(page_link('copy', here), ic('globe'), 'Get This Website', 'gold', False),
        b(A('', here), '<span class="emo" aria-hidden="true">🏡</span>', 'Go Home', '', False),
        b(GROUP, ic('whatsapp'), 'MTG TRIBE'),
        b(soc['tiktok'][1], ic('tiktok'), 'TikTok'),
        b(soc['youtube'][1], ic('youtube'), 'YouTube')])       # MTG, 22 Nov 2026: six buttons, trimmed from ten
    return f'''<aside class="md-side" id="cbp-menu" aria-label="Dashboard menu">
 <a class="side-brand" href="{A('', here)}" aria-label="{esc(NAME)}: home"><img src="{A('assets/logo-disc-256.webp', here)}" alt="" width="44" height="44"><span><b>ClickBaitPays</b><small>Dashboard by MTG 👑</small></span></a>
 <nav aria-label="Dashboard pages">{''.join(out)}</nav>
 <div class="md-bot">
  <a class="side-join" href="{esc(OWNER['ref'])}" target="_blank" rel="sponsored noopener">{ic('userplus')}Join ClickBaitPays Free</a>
  <div class="sgrid">{grid}</div>
 </div>
</aside>
<button type="button" class="md-toggle" aria-controls="cbp-menu" aria-expanded="true" aria-label="Collapse menu" title="Collapse menu">{ic('chl')}</button>
<div class="md-scrim" aria-hidden="true"></div>'''


def neighbours(key):
    i = KEYS.index(key)
    return (NAVD[KEYS[i - 1]] if i > 0 else None), (NAVD[KEYS[i + 1]] if i < len(KEYS) - 1 else None), i


def arrows(key, here):
    """Previous and Next at the top of the page, beside its heading"""
    p, n, i = neighbours(key)
    a = f'<a class="pa" href="{A(p[1], here)}" rel="prev" aria-label="Previous page: {esc(p[2])}" title="Previous: {esc(p[2])}">{ic("chl")}</a>' if p else '<span class="pa off" aria-hidden="true">' + ic('chl') + '</span>'
    b = f'<a class="pa" href="{A(n[1], here)}" rel="next" aria-label="Next page: {esc(n[2])}" title="Next: {esc(n[2])}">{ic("chr")}</a>' if n else '<span class="pa off" aria-hidden="true">' + ic('chr') + '</span>'
    return f'<nav class="parr" aria-label="Previous and next page">{a}<span class="pc">{i + 1} / {len(KEYS)}</span>{b}</nav>'


def pager(key, here):
    p, n, i = neighbours(key)
    out = '<nav class="pager" aria-label="Previous and next page">'
    out += (f'<a class="pg prev" href="{A(p[1], here)}"><small>{ic("chl")}Previous</small><b>{p[2]}</b></a>' if p else '<span></span>')
    out += (f'<a class="pg next" href="{A(n[1], here)}"><small>Next{ic("chr")}</small><b>{n[2]}</b></a>' if n else
            f'<a class="pg next" href="{A("dashboard/", here)}"><small>Back to the start{ic("chr")}</small><b>Welcome</b></a>')
    return out + '</nav>'


def phead(key, here, h1, lead, eyebrow=None):
    k, p, label, sub, icon, g = NAVD[key]
    eb = eyebrow or g
    icon = 'film' if icon.startswith('n') and icon[1:].isdigit() else icon
    return (f'<header class="phead"><div class="ph-top"><p class="eye">{ic(icon)}{eb}</p>{arrows(key, here)}</div>'
            f'<h1>{h1}</h1><p class="lead">{lead}</p></header>')


def pchips():
    """every kind of program people promote, as glowing chips that pop in: if it has a link, it belongs here"""
    ch = ''.join(f'<li style="--i:{k}">{esc(p)}</li>' for k, p in enumerate(PROGRAMS))
    return f'<ul class="pchips rv" aria-label="Programs you can promote on ClickBaitPays">{ch}<li class="you" style="--i:{len(PROGRAMS)}">+ your link</li></ul>'


def story(here):
    """MTG's own proof: he found BellverCards through an ad on ClickBaitPays"""
    return (f'<figure class="story t3d rv"><span class="q" aria-hidden="true">“</span><blockquote><p>{STORY}</p></blockquote>'
            f'<figcaption><img class="mtg" src="{A("assets/mtg-photo.webp", here)}" alt="MTG" width="64" height="64" loading="lazy"><span><b>MTG 👑 | Your Digital Architect</b>'
            f'<small>His own experience, not a promise: what you get depends on your offer and your ad.</small></span></figcaption></figure>')


def niches():
    return '<div class="pcards niches">' + ''.join(f'<article class="pcard t3d">{ic(i)}<h3>{t}</h3><p>{b}</p></article>' for i, t, b in NICHES) + '</div>'


def streams():
    return ('<div class="pcards streams">' + ''.join(f'<article class="pcard t3d"><span class="pn">{k + 1}</span>{ic(i)}<h3>{t}</h3><p>{b}</p></article>'
            for k, (i, t, b) in enumerate(STREAMS)) + '</div>')


def endband(here, show_copy=True):
    """the end of every page: two clear next steps, join, or own this exact website (MTG, 22 Nov 2026: "I want to sell it like hotcakes")"""
    join = (f'<div class="eb t3d"><img src="{A("assets/logo-disc-256.webp", here)}" alt="" width="56" height="56" loading="lazy">'
            f'<h2>Got a link? Get it seen.</h2><p>Promote BellverCards, Bitcoin Wealth, JetUP or any program with a link, and get paid in USDT to view ads while you do.</p>{join_btn()}{fair()}</div>')
    own = (f'<div class="eb eb-own t3d"><span class="eb-ic">{ic("globe")}</span><h2>Want this exact website, with your link?</h2>'
           f'<p>The ClickBaitPays guide that sells the real reason people join: traffic for what they already promote. Your link on every button. R1,000 or $50 once-off, and you pay only if you like it.</p>{copy_btn(here)}</div>')
    return f'<section class="endband rv" aria-label="Your next step">{join}{own if show_copy else ""}</section>'


def dash_page(key, here_ld, main, page_type='WebPage', band=True):
    k, path, label, sub, icon, g = NAVD[key]
    here = path
    USED_ICONS.clear()
    crumbs = [('ClickBaitPays guide', ''), ('Dashboard', 'dashboard/')] + ([] if key == 'home' else [(label, path)])
    ld = [crumbs_ld(crumbs)] + (here_ld or [])
    hd = head(key, path, here, ld, page_type, extra=f'<link rel="stylesheet" href="{A("assets/mtg-dash.css", here) if MODE == "preview" else "/assets/mtg-dash.css?v=1"}">\n')
    body_main = main(here) if callable(main) else main
    crumb = f'<a href="{A("", here)}">Guide</a>{ic("chr")}' + (f'<a href="{A("dashboard/", here)}">Dashboard</a>{ic("chr")}<span>{label}</span>' if key != 'home' else '<span>Dashboard</span>')
    jb = endband(here, band != 'join') if band else ''
    body = f'''<div class="md-shell">
<script>try{{if(localStorage.getItem('mtg-side')==='off'&&matchMedia('(min-width:1061px)').matches)document.currentScript.parentNode.classList.add('md-off')}}catch(e){{}}</script>
{sidebar(key, here)}
<div class="md-main">
<header class="md-top">
 <button type="button" class="md-menu" aria-controls="cbp-menu" aria-expanded="false" aria-label="Open menu"><span class="bars" aria-hidden="true"></span><span class="lbl">Menu</span></button>
 <a class="top-logo" href="{A('', here)}" aria-label="{esc(NAME)}: home"><img src="{A('assets/logo-disc-256.webp', here)}" alt="" width="36" height="36"></a>
 <nav class="md-crumb" aria-label="Breadcrumb">{crumb}</nav>
 <div class="md-act">
  <a class="md-btn md-plan" href="{page_link('plan', here)}">{ic('coins')}<span class="l">Compensation Plan</span><span class="s">Plan</span></a>
  <a class="md-btn md-join" href="{esc(OWNER['ref'])}" target="_blank" rel="sponsored noopener">{ic('userplus')}<span>Join Free</span></a>
  <a class="md-btn md-home" href="{A('', here)}"><span class="emo" aria-hidden="true">🏡</span><span class="lbl">Go Home</span></a>
 </div>
</header>
<main id="main" class="dmain" tabindex="-1">
{body_main}
{jb}
{pager(key, here)}
</main>
<footer class="dfoot"><p class="risk">{ic('info')}<span>{RISK} <a href="{A('disclaimer/', here)}">Disclaimer</a>.</span></p>
<p class="sig">© 2026 MTG 👑 | Your Digital Architect · Let's Get This Crypto! 💪</p></footer>
</div>
</div>
{qbar(key, here)}{updown()}{popup()}
<script src="{A('assets/mtg-dash.js', here) if MODE == 'preview' else '/assets/mtg-dash.js?v=1'}" defer></script>
{scripts(here)}'''
    return doc(hd, 'cbp cbp-dash has-qbar', body)


def two(video_html, side_html):
    """the video and what it covers, side by side on a computer; on a phone the video comes first"""
    return f'<div class="two">{video_html}<div class="side">{side_html}</div></div>'


def side_box(title, items, icon='info'):
    return f'<div class="sbox"><h2 class="h3">{ic(icon)}{title}</h2>{checks(items)}</div>'


def sec(title, body, id_=None, lead=None):
    i = f' id="{id_}"' if id_ else ''
    ld = f'<p class="slead">{lead}</p>' if lead else ''
    return f'<section class="dsec"{i}><h2 class="h2">{title}</h2>{ld}{body}</section>'


# ============================================================== content
STEPS = [
    ('userplus', 'Join free', 'Use a Join button in this guide, or the link of the person who invited you. Register from your home Wi-Fi.', 'join'),
    ('wallet', 'Fund your account', 'Deposit crypto on the Deposit page. Your balance shows in USDT.', 't2'),
    ('layers', 'Buy a campaign and activate the level', 'Pick a level, add your ad title (30 characters at most) and link, tap <b>Preview</b>, then <b>Confirm Purchase</b>. The first time at a level, pay its one-time activation fee so you can earn from clicking.', 't3'),
    ('cursor', 'Click your daily ads', 'Log in once a day, open each ad, wait for the 15-second countdown and tap <b>Confirm &amp; Earn</b>.', 'daily'),
    ('coins', 'Use your Available Balance', 'After 12 click days and a 7-day hold, the earnings are yours: withdraw them, Pay It Forward, or buy your next campaign.', 'timeline'),
]

FAQ = [
    ('What can I promote on ClickBaitPays?',
     'If it has a link, you can promote it: BellverCards, Bitcoin Wealth, JetUP, XFUSION, Solar Group, Aureus Alliance, stokvel and smart contract platforms, MLM and affiliate programs, digital products or your own business. Illegal or harmful content and big sites such as Google or Facebook are not allowed. Ad titles are 30 characters at most.'),
    ('Can ClickBaitPays bring sign-ups to my team or program?',
     'It brings real people to your link: members open your page and view it for a 15-second countdown, every click day. The ones it speaks to can join, buy or sign up under you. MTG found BellverCards through an ad on ClickBaitPays, joined, and is ranking up. What you get depends on your offer and your ad, and nothing is guaranteed.'),
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
    ('How do I log in to ClickBaitPays?',
     'Go to clickbaitpays.me/login.php (the Member Login button in this guide\'s menu opens it) and log in with your email and password. A login ad shows for 30 seconds, then your back office opens.'),
    ('Is ClickBaitPays a scam?',
     'It is an advertising platform, not an investment: you buy views for your link and you are paid for viewing other members\' ads. Judge it on exactly that, and test it yourself with a small start. The page Is It Legit? in this guide shows how.'),
    ('Is ClickBaitPays an investment?',
     'No. It is an advertising platform: you buy advertising for your own link, and you are paid for viewing other members\' ads. The figures in this guide are the platform\'s own, and nothing is guaranteed.'),
    ('Is ClickBaitPays legit?',
     'MTG is an active member: his screen recordings for the tutorials in this guide show his own campaigns, his daily clicks and completed campaigns moving to his Available Balance. Check it for yourself too: read the official FAQ at clickbaitpays.me, start with a level you are comfortable with, and only use money you can afford to lose.'),
    ('Can I have more than one account?',
     'One account per person. Up to 3 accounts are allowed per household, each for a different adult with their own email address, all under the same original sponsor.'),
]

# every tutorial page: its video (a tutorial's own recording when ready; until then the closest real video), what it covers, and every step in writing
TUT = {
    't1': dict(video='backoffice', h1='Your ClickBaitPays back office: a quick tour',
               lead='Know your way around before you spend a cent: every menu item and what it is for.',
               learn=['Your dashboard: stats and your referral link', 'Where you advertise and unlock earning', 'Where you click your daily ads', 'Where your money comes and goes'],
               steps=[('Log in', f'Go to <a href="{LOGIN}" target="_blank" rel="noopener">clickbaitpays.me/login.php</a>. A login ad shows for 30 seconds, then your dashboard opens.'),
                      ('Your dashboard', 'Your stats at a glance, and your referral link with a <b>Copy</b> button.'),
                      ('Advertise and unlock earning', '<b>Buy Ad Campaigns</b>, <b>Activate Earnings</b> and <b>Buy Login Ads</b>.'),
                      ('Your daily clicks', '<b>Click Ads</b>, <b>Saved Ads</b> and <b>Click History</b>.'),
                      ('Your money', '<b>Deposit</b>, <b>Withdraw</b>, <b>Purchase History</b> and <b>Pay It Forward</b>.'),
                      ('On a phone', 'Tap the menu button (the three lines) to open the menu.')],
               soon='MTG\'s own click-by-click tour is being recorded. Until then, the Back Office Walkthrough above shows every part of it.'),
    't2': dict(h1='How to deposit USDT into ClickBaitPays',
               lead='Fund your account through the Deposit page, safely, in a few minutes.',
               learn=['Enter the USDT amount', 'Pay through NOWPayments', 'A fresh address every time', 'Wait for the confirmation'],
               steps=[('Open Deposit', 'In the menu, tap <b>Deposit</b> and enter the amount in USDT.'),
                      ('Pay through NOWPayments', 'The payment page opens with the address and the network to send on.'),
                      ('Copy the new address', 'Copy the address shown for this deposit. Never reuse an old one: every deposit gets its own.'),
                      ('Send from your wallet', 'Send the exact amount on the network shown, from your wallet or exchange.'),
                      ('Wait for the confirmation', 'Once the network confirms, your balance shows in USDT.')]),
    't3': dict(h1='How to buy and activate your first ClickBaitPays campaign',
               lead='MTG buys a Level 4 campaign, activates Level 4 once, and clicks his 5 daily ads.',
               learn=['Log in and the 30-second login ad', 'Buy a campaign: title, link and Preview', 'Activate the level once', 'Click your daily ads and save the ones you like'],
               steps=[('Log in', 'View the login ad for 30 seconds.'),
                      ('Buy Ad Campaigns', 'Pick your level, for example Level 4 at 300 USDT.'),
                      ('Your ad', 'Add your ad title (30 characters at most) and your link.'),
                      ('Preview first', 'Tap <b>Preview</b> and check your ad, then tap <b>Confirm Purchase</b>.'),
                      ('Activate the level', 'Open <b>Activate Earnings</b> and activate the level once (Level 4: 30 USDT). It never expires.'),
                      ('Click your ads', 'Open <b>Click Ads</b>. For each ad: <b>View &amp; Earn</b>, <b>Open Ad</b>, wait 15 seconds, <b>Confirm &amp; Earn</b>.'),
                      ('Save what you like', 'Save any ad you want to come back to later.')]),
    't4': dict(h1='How to buy another campaign on a level you already activated',
               lead='Your second campaign at a level needs no activation fee: buy it and click.',
               learn=['No activation fee the second time', 'Two campaigns, two tabs on Click Ads', 'Your routine for 12 click days', 'The 7-day hold, then your Available Balance'],
               steps=[('Buy Ad Campaigns', 'Pick the level you already activated and buy the campaign (title, link, Preview, Confirm Purchase).'),
                      ('No activation fee', 'The level is already active, so there is nothing more to pay.'),
                      ('Two tabs', '<b>Click Ads</b> now shows a tab for each campaign. Complete the clicks of each one every day.'),
                      ('12 + 7', 'Each campaign runs 12 click days, then its earnings rest 7 days before they reach your Available Balance.')]),
    't5': dict(h1='How to request a withdrawal from ClickBaitPays',
               lead='Move your Available Balance to your own wallet, once a week.',
               learn=['Once a week', 'The 10 USDT minimum and the 10% fee', 'Your wallet address and Security PIN', 'After you request'],
               steps=[('Open Withdraw', 'In the menu, tap <b>Withdraw</b>.'),
                      ('Know the rules', 'Withdrawals are requested once a week. The minimum is 10 USDT and the fee is 10%.'),
                      ('Your wallet address', 'Paste your wallet address and check it twice: crypto sent to a wrong address cannot be returned.'),
                      ('Your Security PIN', 'Enter your Security PIN and submit the request.')]),
    't6': dict(h1='How to create a ClickBaitPays Login Ad',
               lead='20 USDT puts your link in front of every member for 30 seconds when they log in, for 30 days.',
               learn=['20 USDT for 30 days of views', 'Title (30 characters) and link, then Preview', 'The two tick boxes before you buy', 'Login Ad or Ad Campaign: the difference'],
               steps=[('Open Buy Login Ads', 'In the menu, tap <b>Buy Login Ads</b>.'),
                      ('Your ad', 'Add your title (30 characters at most) and your link.'),
                      ('Preview first', 'Tap <b>Preview</b> and check it.'),
                      ('Tick and buy', 'Tick the two boxes, then buy. Your Login Ad runs for 30 days.')]),
    't7': dict(h1='How to Pay It Forward on ClickBaitPays',
               lead='Send funds from your Available Balance to another member, to help them get started.',
               learn=['Open Pay It Forward', 'Check the username twice', 'Add an optional message', 'Your Security PIN, then confirm'],
               steps=[('Open Pay It Forward', 'In the menu, tap <b>Pay It Forward</b>.'),
                      ('The username', 'Enter the member\'s username and check it twice.'),
                      ('Amount and message', 'Enter the amount, and a message if you like.'),
                      ('Confirm', 'Enter your Security PIN and confirm. A payment cannot be undone.')]),
}


# ============================================================== pages
def old_links(here, m):
    """links shared before 22 Nov 2026 pointed at sections of one long page (/cbp/#levels): they now open that topic's page"""
    j = json.dumps({h: L(NAVD[k][1], here) for h, k in m.items()})
    return f'<script>(function(){{var m={j},h=location.hash.slice(1);if(m[h])location.replace(m[h])}})()</script>'


def p_landing():
    """the main page: short. Three videos, the one idea that matters, then the dashboard and your own copy (MTG, 22 Nov 2026)."""
    here = ''
    USED_ICONS.clear()
    howto = {'@type': 'HowTo', 'name': 'How ClickBaitPays works, step by step', 'inLanguage': 'en-ZA',
             'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': n, 'text': plain(t), 'url': SITE + prod_url(NAVD[k][1])} for i, (ico, n, t, k) in enumerate(STEPS)]}
    hd = head('landing', '', here, [howto, crumbs_ld([('MTG TRIBE', SITE + '/'), ('ClickBaitPays guide', '')])])
    tiles = [('grow', 'Promote Your Link'), ('plan', 'Compensation Plan'), ('levels', 'The 7 Levels'),
             ('join', 'How To Join'), ('tutorials', 'Step-By-Step Tutorials'), ('legit', 'Is It Legit?')]
    tl = ''.join(f'<a class="tile t3d" href="{page_link(k, here)}"><span class="ti">{ic(NAVD[k][4])}</span><b>{t}</b><small>{NAVD[k][3]}</small>{ic("chr", "ic go")}</a>' for k, t in tiles)
    flow = [('eye', 'Your link gets seen', 'Members open your page and stay for a 15-second countdown. Real people, real eyes, every single click day.'),
            ('userplus', 'The right ones act', 'The ones it speaks to join your team, buy your product or sign up under you. That is exactly how MTG found BellverCards.'),
            ('coins', 'You get paid too', 'While your ad works, you view theirs and earn USDT: from 0.48 to 13.50 per click, by level.')]
    fl = ''.join(f'<article class="fcard t3d"><span class="fn">{i + 1}</span><span class="fi">{ic(a)}</span><h3>{b}</h3><p>{c}</p></article>' for i, (a, b, c) in enumerate(flow))
    body = f'''<header class="top"><div class="wrap top-in">{brand(here)}
 <div class="top-act"><a class="btn btn-ghost sm hide-sm" href="{page_link('plan', here)}">{ic('coins')}<span>Compensation Plan</span></a>
 <a class="btn btn-dash ring sm" href="{A('dashboard/', here)}">{ic('layers')}<span>Dashboard</span></a></div>
</div></header>
<main id="main" tabindex="-1">
<section class="hero" aria-labelledby="hero-h"><div class="wrap hero-in">
 <div class="hero-copy">
  <p class="eye">{ic('cursor')}Independent guide by MTG 👑</p>
  <h1 id="hero-h"><span class="h1-k">ClickBaitPays</span><span class="h1-big">Got a link? <em>Get it seen.</em></span></h1>
  <p class="lead"><b>BellverCards. Bitcoin Wealth. JetUP. A stokvel, an MLM, an affiliate offer, a digital product.</b> If it has a link, ClickBaitPays puts it in front of real people who open it, every single day. And you get paid in USDT to view their ads while it happens.</p>
  <div class="cta-row">{join_btn()}{plan_btn(here, 'Compensation Plan')}</div>
  {fair()}
  <ul class="facts" aria-label="Key facts"><li>{ic('mega')}<b>Any link</b> gets seen</li><li>{ic('coins')}Paid in <b>USDT</b></li><li>{ic('gift')}<b>Free</b> to join</li></ul>
 </div>
 <div class="hero-vid">{vid('welcome', here, hero=True, eager=True, num='1')}</div>
</div></section>
<section class="flow rv" aria-labelledby="flow-h"><div class="wrap">
 <div class="more-head"><h2 id="flow-h">If it has a link, it belongs on ClickBaitPays</h2><p>Every business needs eyes. Every team needs sign-ups. Every affiliate needs clicks. This is where you get them, and get paid.</p></div>
 {pchips()}
 <div class="fcards">{fl}</div>
 <p class="flow-more"><a class="btn btn-gold ring" href="{page_link('grow', here)}">{ic('mega')}<span>See How To Promote Your Link</span></a></p>
</div></section>
<section class="more rv" aria-labelledby="more-h"><div class="wrap">
 <div class="more-head"><h2 id="more-h">Then these two, and you know it all</h2><p>The compensation plan, then the back office. About 20 minutes together.</p></div>
 <div class="vgrid">{vid('strategy', here, num='2')}{vid('backoffice', here, num='3')}</div>
</div></section>
<section class="proof rv" aria-label="MTG's own story"><div class="wrap">{story(here)}</div></section>
<section class="dband rv" aria-labelledby="db-h" data-final><div class="wrap">
 <div class="db-in">
  <div class="db-copy"><p class="eye">{ic('layers')}Next: the dashboard</p><h2 id="db-h">Everything else, one short page at a time</h2>
   <p>Pick a topic, watch its video, tap Next. How to promote your link, the compensation plan, the levels, every tutorial step by step, and how to check it all yourself.</p>
   <div class="cta-row">{dash_btn(here, size='lg')}</div></div>
  <div class="tiles">{tl}</div>
 </div>
</div></section>
{own_band(here)}
</main>
<footer class="foot"><div class="wrap">
 <div class="foot-in">{brand(here)}
  <nav class="foot-nav" aria-label="Guide"><a href="{A('dashboard/', here)}">Dashboard</a><a href="{page_link('plan', here)}">Compensation Plan</a><a href="{page_link('tutorials', here)}">Tutorials</a><a href="{page_link('calc', here)}">Calculator</a><a href="{page_link('faq', here)}">FAQ</a><a href="{LOGIN}" target="_blank" rel="noopener">Member Login</a><a href="{page_link('copy', here)}">Get This Website</a><a href="{page_link('disc', here)}">Disclaimer</a></nav>
  {social_row()}
 </div>
 <p class="risk">{ic('info')}<span>{RISK} Independent guide, not the official site (that is <a href="{OFFICIAL}" target="_blank" rel="noopener">clickbaitpays.me</a>).</span></p>
 <p class="sig">© 2026 MTG 👑 | Your Digital Architect · Let's Get This Crypto! 💪</p>
</div></footer>
{qbar('landing', here, landing=True)}{updown()}{popup()}
{old_links(here, {'what': 'what', 'how': 'how', 'levels': 'levels', 'login-ads': 't6', 'join': 'join', 'videos': 'videos', 'faq': 'faq'})}
{scripts(here)}'''
    return doc(hd, 'cbp cbp-land has-qbar', body)


def browser_mock(slug='yourname'):
    """a small 3D browser window showing your own copy of this website"""
    return (f'<div class="bmock t3d" aria-hidden="true"><div class="bm-bar"><i></i><i></i><i></i><span class="bm-url">mtgtribe.com/cbp/<b>{slug}</b></span></div>'
            f'<div class="bm-body"><span class="bm-logo"></span><span class="bm-h">Got a link? <em>Get it seen.</em></span><span class="bm-v"><i></i></span>'
            f'<span class="bm-btn">Join Free <small>(your link)</small></span></div></div>')


def own_band(here):
    """own this exact website: on the main page. Why clone this one, not just any ClickBaitPays page."""
    return (f'<section class="own rv" aria-labelledby="own-h"><div class="wrap"><div class="own-in">'
            f'<div class="own-copy"><p class="eye gold">{ic("globe")}Your own copy</p><h2 id="own-h">Own the ClickBaitPays website that sells the real reason people join</h2>'
            f'<p>Most ClickBaitPays pages repeat the official brochure. This one sells traffic for what people already promote, shows every step on video, and walks your visitors to your link, day and night. You share one link. It does the heavy lifting.</p>'
            f'{checks(CLONE[:5])}<p class="own-price"><b>R1,000</b> or <b>$50</b> once-off, with your link on every button. <span>Pay only if you like it.</span></p>'
            f'<div class="cta-row">{copy_btn(here, "Get This Website")}</div></div>'
            f'<div class="own-vis">{browser_mock()}</div></div></div></section>')


def p_home(here):
    first = [('what', 'What is ClickBaitPays?'), ('grow', 'Got a link? Promote it here'), ('plan', 'The compensation plan, on video'), ('join', 'How to join, free')]
    fl = ''.join(f'<li><a href="{page_link(k, here)}"><span class="n">{i + 1}</span><span>{t}</span>{ic("chr")}</a></li>' for i, (k, t) in enumerate(first))
    groups, out = [], ''
    for k, p, label, sub, icon, g in NAV:
        if k == 'home':
            continue
        if not groups or groups[-1][0] != g:
            groups.append((g, []))
        groups[-1][1].append((k, p, label, sub, icon))
    for g, items in groups:
        tl = ''.join(f'<a class="tile t3d" href="{A(p, here)}"><span class="ti">{ic(icon)}</span><b>{label}</b><small>{sub}</small>{ic("chr", "ic go")}</a>' for k, p, label, sub, icon in items)
        out += f'<div class="tgroup"><h3 class="tg-h">{g}</h3><div class="tiles">{tl}</div></div>'
    return (phead('home', here, 'Welcome to your ClickBaitPays dashboard',
                  'One topic per page, in order. Use the menu, or the arrows to go forward and back.', 'Start here')
            + two(vid('tour', here, hero=True), f'<div class="sbox"><h2 class="h3">{ic("compass")}Your first 4 pages</h2><ol class="first">{fl}</ol></div>')
            + sec('Every topic', out, 'topics')
            + old_links(here, {**{k: k for k in TUT}, 'tour': 'home', 'e1': 'what', 'e2': 'join', 'e3': 'levels', 'e4': 'timeline', 'yt': 'videos'}))


def p_what(here):
    roles = (f'<div class="roles"><article class="role t3d">{ic("mega")}<h3>Advertisers get traffic</h3><p>Buy an ad campaign and members view your link every day for 12 click days.</p></article>'
             f'<article class="role pink t3d">{ic("cursor")}<h3>Viewers get paid</h3><p>Open each ad, wait for the 15-second countdown, tap <b>Confirm &amp; Earn</b>. Paid in USDT.</p></article></div>'
             + note('<b>Every member does both.</b> Think of a community noticeboard: you pin your poster where members pass by, and members are paid for the time they spend reading each other\'s posters.', 'msg', 'soft'))
    nxt = (f'<div class="ccards two-up"><a class="ccard t3d" href="{page_link("grow", here)}">{ic("mega")}<b>Promote your link</b><span>BellverCards, Bitcoin Wealth, JetUP, any program: get it seen.</span><small>Next{ic("chr")}</small></a>'
           f'<a class="ccard t3d" href="{page_link("plan", here)}">{ic("coins")}<b>The compensation plan</b><span>How members earn, on video, with the numbers.</span><small>Watch{ic("chr")}</small></a></div>')
    return (phead('what', here, 'What is ClickBaitPays?', 'A paid-to-click advertising platform with the twist that matters: you put your own link in front of real people, and you get paid in USDT to view theirs.')
            + two(vid('welcome', here, hero=True), side_box('In 30 seconds', ['Your link in front of real people for 12 click days', 'Get paid in USDT to view their ads', 'Any program with a link: BellverCards, Bitcoin Wealth, JetUP', 'Free to join, campaigns from 13 USDT'], 'timer'))
            + sec('Two sides, one simple trade', roles) + sec('If it has a link, it belongs here', pchips()) + sec('Where to next', nxt))


def p_grow(here):
    why = [('btc', 'They already use crypto', 'Members fund their accounts in USDT. Wallets, deposits and sign-up links are everyday stuff to them, so a crypto offer clicks fast.'),
           ('eye', 'They are already looking', 'Opening ads is part of every member\'s day. Your page gets a 15-second view with their full attention, not a thumb flicking past.'),
           ('film', 'Your page can close the deal', 'Send them to a page that explains with video, like this one, and the ones it speaks to can say yes on their own, any time of day.')]
    cards = ''.join(f'<article class="pcard t3d"><span class="pn">{i + 1}</span>{ic(a)}<h3>{b}</h3><p>{c}</p></article>' for i, (a, b, c) in enumerate(why))
    cmp_rows = [['Cost', 'From 13 USDT (Level 1)', '20 USDT'], ['Runs for', '12 click days', '30 days'],
                ['Who sees it', 'Members clicking ads at that level', 'Every member, 30 seconds at login'],
                ['Pays you?', 'Yes, once the level is activated', 'No, it buys views']]
    ways = (table(['', 'Ad Campaign', 'Login Ad'], cmp_rows, 'Ad Campaigns compared with Login Ads', 'cmp')
            + f'<div class="cta-row">{btn("Tutorial 3: Your First Campaign", page_link("t3", here), "ghost", "layers")}{btn("Tutorial 6: Create A Login Ad", page_link("t6", here), "ghost", "eye")}</div>')
    tips = checks(['Lead with what they get, in 30 characters or less: the win, then the name',
                   'Send them to a page that explains with video, so they can say yes on their own',
                   'Tap Preview before you buy, every time',
                   'Keep it legal and honest: big sites such as Google or Facebook are not allowed'])
    bill = note('<b>Think of a billboard on the busiest street in town,</b> except here every passer-by is paid to stop, open it and look for 15 seconds. That is the traffic your link gets.', 'mega', 'soft')
    return (phead('grow', here, 'Got a link? Put it in front of real people, every day.',
                  'BellverCards, Bitcoin Wealth, JetUP, XFUSION, a stokvel, an MLM, an affiliate offer, a digital product. If it has a link, ClickBaitPays sends real people to it, and pays you in USDT to view their ads while it does.')
            + two(vid('e1', here), side_box('What you get', ['Real people opening your page, every click day', 'Sign-ups, sales and team members from the ones it speaks to', 'USDT for viewing ads while your ad works', 'From 13 USDT for 12 click days'], 'mega'))
            + sec('If it has a link, it belongs here', pchips() + bill)
            + sec('Who needs this? Anyone with a link.', niches(), lead='Every business needs eyes. Every team needs sign-ups. Every affiliate needs clicks.')
            + sec('It worked on MTG', story(here))
            + sec('Why these visitors act', f'<div class="pcards">{cards}</div>')
            + sec('Three streams of income, one account', streams())
            + sec('Two ways to put your link in front of members', ways)
            + sec('Write an ad that gets the click', tips))


def p_how(here):
    steps = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{n}</h3><p>{t}</p><a class="more-l" href="{page_link(k, here)}">{NAVD[k][2]}{ic("chr")}</a></div></li>'
                    for i, (ico, n, t, k) in enumerate(STEPS))
    return (phead('how', here, 'How ClickBaitPays works, in 5 steps', 'From free sign-up to your Available Balance. Each step has its own page.')
            + two(vid('presentation', here, hero=True), side_box('In this presentation', ['How the ads work', 'Campaigns and levels', 'How withdrawals work', 'The full picture in one go'], 'film'))
            + sec('The 5 steps', f'<ol class="steps">{steps}</ol>'))


def p_join(here):
    js = [('Tap Join', 'The official sign-up page opens on clickbaitpays.me with MTG as your sponsor.'),
          ('Create your free account', 'From your home Wi-Fi: no VPN or mobile data while you register.'),
          ('Follow the tutorials', 'Log in, then follow Tutorial 2 (deposit) and Tutorial 3 (your first campaign).')]
    st = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(js))
    box = (f'<div class="join-box">{join_btn(size="lg")}<p class="fair-big">{ic("users")}<span><b>Invited by someone else?</b> Please use their link instead. Fair is fair. 🤝</span></p></div>'
           f'<p class="disc">The Join buttons carry MTG\'s referral link (sponsor code <b>{OWNER["code"]}</b>). If you join through it, MTG becomes your sponsor and receives 10% of the campaigns you buy. Your prices stay exactly the same.</p>')
    return (phead('join', here, 'How to join ClickBaitPays (free)', 'ClickBaitPays is joined through a member\'s link. Three steps and you are in.')
            + two(vid('e2', here), side_box('The house rules', ['Sign up from your home Wi-Fi', 'One account per person', 'Up to 3 per household, each adult with their own email', 'All under the same sponsor']))
            + sec('3 steps', f'<ol class="steps">{st}</ol>{box}'))


def levels_table():
    """the table on a computer; on a phone the same figures as two columns of level cards (shorter than a stacked table)"""
    rows = [[f'Level {l}', f'{money(p)} USDT', f'{money(a)} USDT', f'{money(c)}', f'{n}', f'<b>{money(t)}</b>'] for l, p, a, c, n, t in LEVELS]
    tbl = table(['Level', 'Campaign', 'Activation (once)', 'Per click', 'Clicks a day', 'Campaign total*'], rows,
                'The 7 ClickBaitPays levels: price, one-time activation fee, pay per click, clicks a day and campaign total', 'levels')
    cards = ''.join(f'<li class="lvc{" top" if l == 7 else ""}"><small>Level {l}</small><b>{p:,} <i>USDT</i></b><span>+ {a:,} activation, once</span>'
                    f'<span>{n} clicks a day, {c:.2f} each</span><em>Total* {money(t)}</em></li>' for l, p, a, c, n, t in LEVELS)
    return tbl + f'<ul class="lvcards" aria-hidden="true">{cards}</ul>'



def p_levels(here):
    body = (levels_table()
            + f'<p class="tnote">* The platform\'s own figures, read in the back office on {CHECKED}. "Per click" is the 90% of the advertiser\'s cost that members receive; the campaign total assumes all 12 click days. You are paid only for the ads you view, and nothing is guaranteed.</p>'
            + f'<div class="calc-strip"><div class="eg"><b>Your first campaign at a level</b> = campaign + activation<span class="eqs"><span>Level 1: 13 + 1 = <b>14 USDT</b></span><span>Level 4: 300 + 30 = <b>330 USDT</b></span></span></div>'
              f'<a class="btn btn-ghost" href="{page_link("calc", here)}">{ic("calc")}<span>Work Out Your Numbers</span></a></div>')
    return (phead('levels', here, 'The 7 ClickBaitPays levels', 'Every level runs 12 click days. Higher levels pay more per click and give you more clicks a day.')
            + two(vid('e3', here), side_box('Good to know', ['Start at any level', 'Activate a level once: it never expires', 'Your next campaign there: no activation fee', 'Activation fees support the platform\'s sustainability']))
            + sec('All 7 levels', stairs() + body))


def timeline():
    return ('<figure class="tl" aria-labelledby="tl-cap"><div class="tl-bar" aria-hidden="true">'
            + ''.join(f'<i class="d c" style="--i:{k}">{k + 1}</i>' for k in range(12)) + ''.join(f'<i class="d h" style="--i:{12 + k}"></i>' for k in range(7))
            + '<i class="d end">✓</i></div><div class="tl-key"><span class="k c">12 click days</span><span class="k h">7-day hold</span><span class="k e">Available Balance</span></div>'
            '<figcaption id="tl-cap">Click every day and your earnings reach your Available Balance on day 19.</figcaption></figure>')


def p_timeline(here):
    ch = [('wallet', 'Withdraw', 'Once a week, to your own wallet.', 't5'), ('send', 'Pay It Forward', 'Help a team member get started.', 't7'),
          ('repeat', 'Buy your next campaign', 'Keep it going, no new deposit needed.', 't4')]
    cards = ''.join(f'<a class="ccard t3d" href="{page_link(k, here)}">{ic(i)}<b>{a}</b><span>{b}</span><small>{NAVD[k][3]}: {NAVD[k][2]}{ic("chr")}</small></a>' for i, a, b, k in ch)
    return (phead('timeline', here, 'The 12 + 7 timeline: when your earnings are yours', 'Click your ads on 12 days, the earnings rest for 7 days, then they move to your Available Balance.')
            + two(vid('e4', here), side_box('Good to know', ['A click day counts when all your daily clicks are done', 'New clicks every day from 7:00 AM (South Africa)', 'Miss a day? Your 12 days just take a little longer']))
            + sec('The timeline', timeline())
            + sec('Then you choose', f'<div class="ccards">{cards}</div>'))


def stairs():
    """the 7 levels as a 3D staircase: each step a glowing block with its price and pay per click"""
    st = ''.join(f'<li class="st3" style="--i:{k}"><span class="blk"><i class="tp"></i><i class="fr"><b>L{l}</b><small>{p:,}</small></i><i class="sd"></i></span>'
                 f'<span class="cap">{c:.2f}<small>per click</small></span></li>' for k, (l, p, a, c, n, t) in enumerate(LEVELS))
    return (f'<figure class="stairs rv" aria-label="The 7 levels from 13 to 2,400 USDT; pay per click from 0.48 to 13.50 USDT">'
            f'<ol class="st-row">{st}</ol><figcaption>Campaign price in USDT on each step, pay per click below it. The platform\'s own figures.</figcaption></figure>')


def p_plan(here):
    stats = [(90, '%', 'of each click\'s cost goes to the member who views it'), (7, '', 'levels, from 13 to 2,400 USDT'),
             (10, '%', 'referral commission, if you share your link'), (19, '', 'days from your first click to your Available Balance')]
    st = ''.join(f'<div class="stat t3d"><b><span data-count="{n}">{n}</span>{u}</b><span>{t}</span></div>' for n, u, t in stats)
    ways = [('mega', 'Traffic for what you promote', 'Your campaign puts your link in front of real people for 12 click days. Every sign-up it brings to BellverCards, Bitcoin Wealth, JetUP or your own program grows your other income streams.'),
            ('coins', 'Get paid to view', 'Your level\'s pay per click, from 0.48 USDT at Level 1 to 13.50 USDT at Level 7, for 3 to 20 ads a day.'),
            ('users', '10% referral commission', 'When someone joins ClickBaitPays with your link, you receive 10% of the campaigns they buy. Optional, and it stacks.')]
    wc = ''.join(f'<article class="pcard t3d"><span class="pn">{i + 1}</span>{ic(a)}<h3>{b}</h3><p>{c}</p></article>' for i, (a, b, c) in enumerate(ways))
    then = (f'<div class="ccards">' + ''.join(f'<a class="ccard t3d" href="{page_link(k, here)}">{ic(i)}<b>{a}</b><span>{b}</span><small>{NAVD[k][3]}: {NAVD[k][2]}{ic("chr")}</small></a>'
            for i, a, b, k in [('wallet', 'Withdraw', 'Once a week, to your own wallet.', 't5'), ('send', 'Pay It Forward', 'Help a team member get started.', 't7'),
                               ('repeat', 'Buy your next campaign', 'Keep it going, a level up when you are ready.', 't4')]) + '</div>')
    more = f'<div class="vrows">{vrow("presentation", here)}{vrow("qa", here)}</div>'
    return (phead('plan', here, 'ClickBaitPays compensation plan, explained', 'Three ways ClickBaitPays works for you, the numbers at every level, and when your earnings are yours. Watch first, then check the numbers.', 'The money page')
            + two(vid('strategy', here, hero=True), side_box('In this video', ['The plan, with real-world examples', 'Growing level by level', 'The 10% referral commission'], 'film'))
            + f'<div class="stats rv">{st}</div>'
            + sec('3 streams of income, one account', f'<div class="pcards">{wc}</div>', lead='Your program grows, your clicks pay, your referrals pay.')
            + sec('The numbers at every level', stairs() + levels_table()
                  + f'<p class="tnote">* The platform\'s own figures, read in the back office on {CHECKED}. The total assumes all 12 click days. You are paid only for the ads you view, and nothing is guaranteed.</p>'
                  + f'<div class="cta-row">{btn("Work Out Your Numbers", page_link("calc", here), "ghost", "calc")}{btn("The 7 Levels In Detail", page_link("levels", here), "ghost", "layers")}</div>')
            + sec('When your earnings are yours', timeline() + then)
            + sec('Want the full picture?', more, lead='The complete presentation and a live Q&amp;A with members\' questions.'))


def p_legit(here):
    facts = [('mega', 'It is an advertising platform', 'You buy ad campaigns for your link and members view ads, paid per view. It is not an investment, and this guide never sells it as one.'),
             ('coins', 'Where the pay comes from', 'Campaign spend: members receive 90% of each click\'s cost. Once-per-level activation fees support the platform\'s sustainability.'),
             ('eye', 'What MTG sees', 'MTG clicks his own ads every day, and found BellverCards through an ad here: he joined and is ranking up. His screen recordings for the tutorials in this guide show his own campaigns, his daily clicks, and completed campaigns moving to his Available Balance.'),
             ('msg', 'Read a bad review?', 'Many reviews judge ClickBaitPays as an investment scheme. Judge it as what it is, a traffic source: does your link get views, and do your views get paid? A small start answers both.')]
    fb = ''.join(f'<article class="dblock t3d">{ic(i)}<div><h3>{t}</h3><p>{b}</p></div></article>' for i, t, b in facts)
    chk = [('Join free', 'Creating your account costs nothing, so you can look around the back office first.'),
           ('Start small', 'Level 1 costs 14 USDT the first time (13 for the campaign, 1 to activate the level).'),
           ('Click every day', 'Watch your campaign\'s Earned Wallet grow in your back office, click by click.'),
           ('See it arrive', 'After 12 click days and a 7-day hold it reaches your Available Balance. Withdraw it (10 USDT minimum) or use it.')]
    st = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(chk))
    return (phead('legit', here, 'Is ClickBaitPays legit?', 'What it is, where the pay comes from, what MTG sees in his own account, and how to check it yourself with a small start.')
            + two(vid('qa', here), side_box('In this live Q&amp;A', ['Members\' questions, answered live', 'Withdrawals and Pay It Forward', 'Strategy and proof'], 'film'))
            + sec('The facts, plainly', f'<div class="dgrid">{fb}</div>')
            + sec('From MTG\'s own account', story(here))
            + sec('Check it yourself in 4 steps', f'<ol class="steps">{st}</ol>'
                  + note('<b>Your pace, your amount.</b> Start with an amount you are comfortable with, and grow from your Available Balance when you are ready.', 'info')))


def p_calc(here):
    chips = ''.join(f'<label class="lv"><input type="radio" name="lvl" value="{l}"{" checked" if l == 4 else ""}><span><b>Level {l}</b><small>{p:,} USDT</small></span></label>' for l, p, a, c, n, t in LEVELS)
    data = json.dumps([{'l': l, 'p': p, 'a': a, 'c': c, 'n': n, 't': t} for l, p, a, c, n, t in LEVELS])
    return (phead('calc', here, 'ClickBaitPays calculator', f'Pick a level: what you pay today, your clicks a day, the platform\'s total and your payout date. Platform figures from {CHECKED}.', 'Free tool')
            + f'''<div class="tool" data-calc='{data}'>
 <form class="tool-in" onsubmit="return false">
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
  <div class="rtile big"><span>Pay today</span><b data-o="pay">0</b><small data-o="payx"></small></div>
  <div class="rtile"><span>Clicks a day</span><b data-o="clicks">0</b><small>about 15 seconds each</small></div>
  <div class="rtile"><span>Earned per click day</span><b data-o="day">0</b><small data-o="dayx"></small></div>
  <div class="rtile"><span>Campaign total (platform figure)</span><b data-o="tot">0</b><small data-o="totx"></small></div>
  <div class="rtile"><span>Reaches your Available Balance</span><b data-o="date">-</b><small>day 19, if you click every day</small></div>
  <div class="rtile"><span>If you then withdraw it all</span><b data-o="net">0</b><small>after the 10% withdrawal fee</small></div>
  <p class="formula" data-o="formula"></p>
 </div>
</div>
{note("<b>How to read this.</b> These are the platform's own figures, assuming you complete every click day. You are paid only for the ads you view, nothing is guaranteed, and a missed day moves your date back by a day. At Levels 1 and 2 the site's campaign total is a few cents under 12 click days, because of rounding: we show the site's own total.", 'info')}''')


def p_daily(here):
    st = [('Log in', f'At <a href="{LOGIN}" target="_blank" rel="noopener">clickbaitpays.me/login.php</a>. View the login ad (30 seconds).'),
          ('Open Click Ads', 'Or tap <b>Start Clicking</b> on your dashboard.'),
          ('View each ad', '<b>View &amp; Earn</b>, <b>Open Ad</b>, wait for the 15-second countdown, then <b>Confirm &amp; Earn</b>.'),
          ('Done for today', 'When it says <b>Click day complete</b>. New clicks from 7:00 AM (South Africa).')]
    s = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(st))
    return (phead('daily', here, 'Your daily ClickBaitPays routine', 'A few minutes a day: log in, click your ads, done.')
            + two(vid('t3', here), side_box('Good to know', ['Clicks reset at midnight Panama time: 7:00 AM in South Africa', 'Do all your level\'s clicks to count the day', 'Save the ads you like for later']))
            + sec('4 steps, every day', f'<ol class="steps">{s}</ol>'))


def p_tutorials(here):
    rows = ''
    for k in ['t1', 't2', 't3', 't4', 't5', 't6', 't7']:
        vc = TUT[k].get('video', k)
        meta = f'{V[k]["label"]} · ' + ('watch now' if playable(vc) else STATUS[V[k]['status']])
        rows += (f'<a class="vrow{"" if playable(vc) else " soon"}" href="{page_link(k, here)}"><img src="{esc(cover(vc, here)[1])}" width="640" height="360" loading="lazy" decoding="async" alt="">'
                 f'<span class="vr-t"><small>{esc(meta)}</small><b>{esc(TUT[k]["h1"])}</b><span>{esc(V[k]["line"])}</span></span>'
                 f'<span class="vr-go">{ic("chr")}<span>Open</span></span></a>')
    return (phead('tutorials', here, 'ClickBaitPays tutorials, step by step', 'Seven short tutorials, in the order you need them. Each one shows one job in the back office, click by click.')
            + f'<div class="vrows">{rows}</div>')


def p_tut(key):
    t = TUT[key]

    def build(here):
        vcode = t.get('video', key)
        steps = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(t['steps']))
        extra = ''
        if key == 't6':
            cmp_rows = [['Cost', '20 USDT', 'From 13 USDT (Level 1)'], ['Runs for', '30 days', '12 click days'],
                        ['Who sees it', 'Every member, 30 seconds at login', 'Members clicking ads at that level'],
                        ['Pays you?', 'No, it buys views', 'Yes, once the level is activated']]
            extra = sec('Login Ad or Ad Campaign?', table(['', 'Login Ad', 'Ad Campaign'], cmp_rows, 'Login Ads compared with Ad Campaigns', 'cmp'))
        if key == 't3':
            extra = note('<b>The activation fee, once per level.</b> It unlocks earning from clicking at that level and never expires. These once-per-level fees also support the platform\'s sustainability.', 'layers')
        if key == 't7':
            extra = note('<b>Recorded on a phone:</b> when it is ready, this tutorial plays upright, in a phone frame.', 'phone')
        soon = note(t['soon'], 'film') if t.get('soon') else ''
        return (phead(key, here, t['h1'], t['lead'], V[key]['label'])
                + two(vid(vcode, here, hero=playable(vcode)), side_box('In this tutorial', t['learn'], 'film'))
                + soon + sec('Step by step', f'<ol class="steps">{steps}</ol>') + extra)
    return build


def p_videos(here):
    now = ''.join(vrow(k, here) for k in ['welcome', 'strategy', 'backoffice', 'presentation', 'qa'])
    links = {'tour': 'home', 'e2': 'join', 'e3': 'levels', 'e4': 'timeline', 't1': 't1', 't2': 't2', 't3': 't3', 't4': 't4', 't5': 't5', 't6': 't6', 't7': 't7'}
    soon = ''.join(vrow(k, here, page_link(p, here)) for k, p in links.items())
    return (phead('videos', here, 'Every ClickBaitPays video', 'Five to watch today, and MTG\'s own tutorials and explainers as they arrive.')
            + sec('Watch now', f'<div class="vrows">{now}</div>')
            + sec('On the way', f'<div class="vrows">{soon}</div>', lead=f'More on the <a href="{CBP_YT}" target="_blank" rel="noopener">ClickBaitPays Us YouTube channel</a>.'))


def p_faq(here):
    items = ''.join(f'<details class="qa"><summary><span>{esc(q)}</span>{ic("chr", "ic chev")}</summary><div class="qa-a"><p>{esc(a)}</p></div></details>' for q, a in FAQ)
    return (phead('faq', here, 'ClickBaitPays FAQ', 'Straight answers to what people ask most, and a full live Q&amp;A to watch.')
            + f'<div class="faq">{items}</div><p class="more-t">More answers in the <a href="{OFFICIAL_FAQ}" target="_blank" rel="noopener">official ClickBaitPays FAQ</a>.</p>'
            + sec('Watch the live Q&amp;A', two(vid('qa', here), side_box('Answered live', ['Ad viewing', 'Affiliates and referrals', 'Pay It Forward', 'Withdrawals and strategy'], 'film'))))


def p_copy(here):
    how = [('Send the form', 'Two minutes. It goes straight to MTG on WhatsApp.'),
           ('MTG builds your copy', 'Your name, your referral link on every Join button, your contact links. You get your link to check.'),
           ('Like it? Pay once', 'R1,000 or $50, by bank transfer, USDT BEP20 or USDT TRC20. Not for you? It is deleted and you owe nothing.')]
    hw = ''.join(f'<li class="step"><span class="num">{i + 1}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(how))
    perks = [('globe', 'Your own address', 'mtgtribe.com/cbp/yourname or clickbaitpaysus.com/yourname'),
             ('link', 'Your link on every Join button', 'Everyone who joins from your page joins your team'),
             ('film', 'Every video, tutorial and tool', 'Kept up to date as MTG adds new videos'),
             ('users', 'Your community, front and centre', 'Your WhatsApp group, TikTok, Facebook and YouTube'),
             ('trend', 'Built to be found', 'Search titles, social previews and structured data on every page'),
             ('refresh', '5 free edits', 'Change your details later at no cost')]
    pk = ''.join(f'<li class="t3d">{ic(i)}<b>{a}</b><span>{b}</span></li>' for i, a, b in perks)
    return (phead('copy', here, 'Get this website, with your link on every button', 'The ClickBaitPays guide that sells the real reason people join: traffic for what they already promote. Every video, the compensation plan and every tutorial, with your link on every Join button. You share one link. It does the rest.', 'Your own copy')
            + f'''<div class="two order">
 <div class="order-l">
  {browser_mock()}
  <div class="price t3d"><b>R1,000</b><span>or $50, once-off</span><em>{ic('check')}Pay only if you like it</em></div>
  <h2 class="h2">Why clone this one</h2>
  <p class="slead">Most ClickBaitPays pages repeat the official brochure. This one sells.</p>
  {checks(CLONE)}
  <h2 class="h2">How it works</h2>
  <ol class="steps one">{hw}</ol>
  <h2 class="h2">What you get</h2>
  <ul class="perks">{pk}</ul>
  {note('This is a payment to MTG for your website only. It is separate from any ClickBaitPays campaign or activation fee.', 'info')}
 </div>
 <form class="oform" id="order" data-order data-wa="{esc(OWNER['wa'])}" novalidate aria-labelledby="of-h">
  <h2 id="of-h">Order in 2 minutes</h2>
  <p class="small">It goes straight to MTG on WhatsApp. Nothing is stored on this website.</p>
  <div class="field"><label for="o-name">Your name, as it should appear *</label><input id="o-name" name="name" required autocomplete="name"></div>
  <div class="field"><label for="o-wa">Your WhatsApp number *</label><input id="o-wa" name="wa" required inputmode="tel" autocomplete="tel"></div>
  <fieldset class="field"><legend>Your address *</legend>
   <label class="tog"><input type="radio" name="domain" value="mtgtribe.com/cbp/" checked required><span><span>mtgtribe.com/cbp/<wbr><i>yourname</i></span></span></label>
   <label class="tog"><input type="radio" name="domain" value="clickbaitpaysus.com/"><span><span>clickbaitpaysus.com/<wbr><i>yourname</i></span></span></label>
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
  <button type="submit" class="btn btn-join ring lg">{ic('whatsapp')}<span>Send My Order On WhatsApp</span></button>
  <p class="sent" data-sent hidden>{ic('check')}<span>Almost done: press <b>Send</b> in WhatsApp. MTG replies on {OWNER['wa_num']}. Didn't open? <a href="{OWNER['wa']}" target="_blank" rel="noopener">Open WhatsApp</a>.</span></p>
 </form>
</div>''')


def p_disc(here):
    blocks = [
        ('shield', 'An independent guide', f'This is MTG\'s own guide to ClickBaitPays, made to educate. It is not the official ClickBaitPays website (that is <a href="{OFFICIAL}" target="_blank" rel="noopener">clickbaitpays.me</a>) and it is not run by ClickBaitPays. Rules, prices and features can change: the official site always has the final word.'),
        ('link', 'The Join buttons carry MTG\'s referral link', f'Every Join button opens the official sign-up page with MTG as your sponsor (code <b>{OWNER["code"]}</b>). If you join through it, MTG receives 10% of the ad campaigns you buy, as the platform\'s referral rules describe. Your prices do not change. Invited by someone else? Please use their link instead.'),
        ('layers', 'About the figures', f'Prices, activation fees, pay per click, clicks a day and campaign totals are the platform\'s own figures, read in the ClickBaitPays back office on {CHECKED}. Campaign totals assume all 12 click days. They describe how the platform pays; they are not a promise of what you will earn.'),
        ('info', 'Advertising, not an investment', 'ClickBaitPays is an advertising platform: you buy advertising for your link and are paid for viewing other members\' ads. Nothing on this site is financial advice. Results depend on the ads you view and on the platform, and nothing is guaranteed. Start with an amount you are comfortable with and only use money you can afford to lose.'),
        ('lock', 'Privacy: what this site stores', 'Nothing personal. There are no accounts, forms that store data, or tracking cookies. The calculator runs in your own browser. Your browser remembers only whether you collapsed the dashboard menu. YouTube videos load from youtube-nocookie.com only when you press play. The copy order form opens WhatsApp with your message; nothing is saved on this site.'),
        ('msg', 'Questions', f'Message MTG on WhatsApp at <a href="{OWNER["wa"]}" target="_blank" rel="noopener">{OWNER["wa_num"]}</a>, or join the MTG TRIBE at <a href="{GROUP}">mtgtribe.com/group</a>. For account issues, contact ClickBaitPays support through the official site.'),
    ]
    body = '<div class="dgrid">' + ''.join(f'<article class="dblock t3d">{ic(i)}<div><h2>{t}</h2><p>{b}</p></div></article>' for i, t, b in blocks) + '</div>'
    return phead('disc', here, 'Disclaimer and privacy', f'Plain words about this guide, the links on it and your privacy. Last updated {int(TODAY[8:10])} November 2026.', 'The small print') + body


# ============================================================== every page
def page_specs():
    """key: (builder, extra structured data, page type, join band)"""
    faq_ld = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    how_ld = {'@type': 'HowTo', 'name': 'How ClickBaitPays works, step by step', 'inLanguage': 'en-ZA',
              'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': n, 'text': plain(t)} for i, (ico, n, t, k) in enumerate(STEPS)]}
    app = {'@type': 'WebApplication', 'name': 'ClickBaitPays Calculator', 'url': SITE + BASE + 'calculator/', 'description': SEO['calc'][1],
           'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Any (runs in a web browser)', 'browserRequirements': 'Requires JavaScript',
           'isAccessibleForFree': True, 'inLanguage': 'en-ZA', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'author': {'@id': PERSON_ID}}
    tut_list = {'@type': 'ItemList', 'name': 'ClickBaitPays tutorials by MTG', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': TUT[k]['h1'], 'url': SITE + prod_url(NAVD[k][1])} for i, k in enumerate(['t1', 't2', 't3', 't4', 't5', 't6', 't7'])]}
    prod = {'@type': 'Product', 'name': 'Your own ClickBaitPays guide website', 'description': SEO['copy'][1], 'brand': {'@type': 'Brand', 'name': 'MTG TRIBE'},
            'image': f'{SITE}{BASE}assets/og/cbp-copy.jpg',
            'offers': [{'@type': 'Offer', 'price': str(PRICE_ZAR), 'priceCurrency': 'ZAR', 'url': SITE + '/cbpcopy/', 'availability': 'https://schema.org/InStock'},
                       {'@type': 'Offer', 'price': str(PRICE_USD), 'priceCurrency': 'USD', 'url': SITE + '/cbpcopy/', 'availability': 'https://schema.org/InStock'}]}
    specs = {'home': (p_home, [], 'CollectionPage', True), 'what': (p_what, [], 'WebPage', True), 'how': (p_how, [how_ld], 'WebPage', True),
             'join': (p_join, [], 'WebPage', False), 'levels': (p_levels, [], 'WebPage', True), 'timeline': (p_timeline, [], 'WebPage', True),
             'plan': (p_plan, [], 'WebPage', True), 'calc': (p_calc, [app], 'WebPage', True), 'daily': (p_daily, [], 'WebPage', True),
             'grow': (p_grow, [], 'WebPage', True), 'legit': (p_legit, [], 'WebPage', True),
             'tutorials': (p_tutorials, [tut_list], 'CollectionPage', True), 'videos': (p_videos, [], 'CollectionPage', True),
             'faq': (p_faq, [faq_ld], 'FAQPage', True), 'copy': (p_copy, [prod], 'WebPage', 'join'), 'disc': (p_disc, [], 'WebPage', True)}
    for k in TUT:
        how = {'@type': 'HowTo', 'name': TUT[k]['h1'], 'inLanguage': 'en-ZA',
               'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': a, 'text': plain(b)} for i, (a, b) in enumerate(TUT[k]['steps'])]}
        specs[k] = (p_tut(k), [how], 'WebPage', True)
    return specs


# ============================================================== extras: sitemap, llms.txt, manifest
def sitemap():
    def img(code):
        return f'<image:image><image:loc>{SITE}{BASE}assets/v/{code}.webp</image:loc></image:image>'
    vids = {'home': 'tour', 'what': 'welcome', 'grow': 'e1', 'how': 'presentation', 'join': 'e2', 'levels': 'e3', 'timeline': 'e4', 'plan': 'strategy', 'legit': 'qa',
            'daily': 't3', 'faq': 'qa', **{k: TUT[k].get('video', k) for k in TUT}}
    urls = [(SITE + BASE, img('welcome') + img('strategy') + img('backoffice'))]
    urls += [(SITE + prod_url(p), img(vids[k]) if k in vids else '') for k, p, *_ in NAV]
    body = ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod>{i}</url>' for u, i in urls)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{body}</urlset>\n')


def llms():
    lv = '\n'.join(f'- Level {l}: campaign {p:,} USDT, one-time activation {a} USDT, {c:.2f} USDT per click, {n} clicks a day, campaign total {t:,.2f} USDT (platform figures)' for l, p, a, c, n, t in LEVELS)
    pages = '\n'.join(f'- [{label}]({SITE}{prod_url(p)}): {SEO[k][1]}' for k, p, label, *_ in NAV)
    return f'''# ClickBaitPays Guide by MTG (mtgtribe.com/cbp)

> An independent, plain-English guide to ClickBaitPays (clickbaitpays.me), a paid-to-click advertising platform: members buy ad campaigns to advertise their own link and are paid in USDT for viewing other members' ads. By MTG (MusaTheGiant), "Your Digital Architect", an active member. Education only, not official ClickBaitPays material, not financial advice. Figures checked {CHECKED}.

## Start here

- [ClickBaitPays in 3 videos]({SITE}{BASE}): Welcome to ClickBaitPays, the income strategy and the back office walkthrough, then the dashboard.

## Dashboard pages (one topic each)

{pages}

## Key facts

- Joining is free, through a member's referral link. Register from home Wi-Fi (no VPN or mobile data during sign-up). One account per person, up to 3 per household under the same sponsor.
- Each campaign runs 12 click days. A click day counts when all of that level's daily clicks are done; clicks reset at midnight Panama time (7:00 AM in South Africa).
- Each in-dashboard ad has a 15-second countdown, then Confirm & Earn. Members receive 90% of the advertiser's cost per click.
- To earn at a level, pay its one-time activation fee once; it never expires. These fees also support the platform's sustainability.
- After the 12th click day, earnings are held 7 days, then move to the Available Balance: withdraw (once a week, minimum 10 USDT, 10% fee), Pay It Forward to another member, or buy a new campaign.
- Login Ads: 20 USDT for 30 days, shown to every member for 30 seconds at login; they pay nothing, they buy views.
- Referrals are optional; sponsors receive 10% of the campaigns their referrals buy.
- What members promote: any program with a link, for example BellverCards, Bitcoin Wealth, JetUP, XFUSION, Solar Group, Aureus Alliance, stokvel and smart contract platforms, MLM and affiliate programs, digital products and their own businesses. Each view is a real member opening the advertiser's page for a 15-second countdown.
- MTG's own experience: he found BellverCards through an ad on ClickBaitPays, joined, and is earning and ranking up (his experience, not a promise).
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
             ('clickbaitpays-logo-disc-256.webp', 'logo-disc-256.webp'), ('clickbaitpays-logo-256.webp', 'logo-256.webp'),
             ('mtg-photo-256.webp', 'mtg-photo.webp')]          # MTG's photo on his story card (MTG, 22 Nov 2026)
    for a, b in pairs:
        shutil.copyfile(os.path.join(BRAND, a), os.path.join(dst, b))
    for f in ('cbp.css', 'cbp.js'):
        shutil.copyfile(os.path.join(SRC, f), os.path.join(dst, f))
    if os.path.isdir(dst + '/yt'):                 # the old YouTube thumbnails gave way to the wide covers
        shutil.rmtree(dst + '/yt')
    missing = [c for c in V for f in (c + '.webp', c + '-640.webp') if not os.path.exists(os.path.join(dst, 'v', f))]
    if missing:                                   # every video needs its wide cover (covers.py draws them)
        sys.exit('missing video covers: ' + ', '.join(sorted(set(missing))) + '. Run covers.py first.')
    for root, _, files in os.walk(dst):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), dst).replace(os.sep, '/')
            HASH[rel] = hashlib.sha1(open(os.path.join(root, f), 'rb').read()).hexdigest()[:8]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def forward(old, key):
    """a page that moved: it sends the visitor (and search engines) to its new address"""
    to = L(NAVD[key][1], old)
    url = SITE + prod_url(NAVD[key][1])
    og = f'{SITE}{BASE}assets/og/cbp-{key}.jpg?v={HASH.get("og/cbp-" + key + ".jpg", "1")}'
    return (f'<!doctype html>\n<html lang="en-ZA">\n<head>\n<meta charset="utf-8">\n<title>{esc(SEO[key][0])}</title>\n<meta name="robots" content="noindex,follow">\n'
            f'<link rel="canonical" href="{url}">\n<meta http-equiv="refresh" content="0; url={esc(to)}">\n'
            f'<meta property="og:title" content="{esc(SEO[key][0])}">\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{og}">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{esc(SEO[key][0])}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{og}">\n'
            f'<script>location.replace({json.dumps(to)}+location.hash)</script>\n</head>\n<body><p><a href="{esc(to)}">{esc(NAVD[key][2])}</a></p></body>\n</html>\n')


def all_pages():
    """{page path under /cbp/: html}"""
    out = {'': p_landing()}
    for key, (fn, ld, ptype, band) in page_specs().items():
        out[NAVD[key][1]] = dash_page(key, ld, fn, ptype, band)
    for old, key in OLD_PATHS.items():
        out[old] = forward(old, key)
    return out


def check_seo():
    for k, (t, dsc) in SEO.items():
        if len(t) > 60 or not (120 <= len(dsc) <= 160):
            print(f'  SEO length: {k}: title {len(t)}, description {len(dsc)}')


def main():
    global MODE
    if '--preview' in sys.argv:
        return render_preview(sys.argv[sys.argv.index('--preview') + 1])
    out = os.path.join(ROOT, 'cbp')
    copy_assets(os.path.join(out, 'assets'))
    pages = all_pages()
    for p, h in pages.items():
        write(os.path.join(ROOT, prod_url(p).lstrip('/'), 'index.html'), h)
    write(os.path.join(out, 'sitemap.xml'), sitemap())
    write(os.path.join(out, 'llms.txt'), llms())
    write(os.path.join(out, 'manifest.webmanifest'), manifest())
    check_seo()
    bad = [p for p, h in pages.items() if '\u2014' in h or '\u2013' in h]
    for f in ('cbp.css', 'cbp.js', 'llms.txt', 'sitemap.xml'):
        t = open(os.path.join(out, 'assets' if f.startswith('cbp.') else '', f), encoding='utf-8').read()
        if '\u2014' in t or '\u2013' in t:
            bad.append(f)
    print('built', len(pages), 'pages;', 'DASH CHECK FAILED: ' + ', '.join(bad) if bad else 'no dashes')


def render_preview(dst):
    """private review copy for MTG (tools/qa/README.md, "Private preview link"): relative links, every file local"""
    global MODE
    copy_assets(os.path.join(ROOT, 'cbp', 'assets'))
    MODE = 'preview'
    os.makedirs(dst, exist_ok=True)
    shutil.copytree(os.path.join(ROOT, 'cbp', 'assets'), os.path.join(dst, 'assets'), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('og'))           # the social previews are not part of the pages
    for f in ('video-return.js', 'wa-message.js', 'mtg-dash.css', 'mtg-dash.js'):
        shutil.copy(os.path.join(ROOT, 'assets', f), os.path.join(dst, 'assets', f))
    pages = all_pages()
    for p, h in pages.items():
        h = re.sub(r'<link rel="manifest"[^>]*>\n?', '', h)
        if p == '':          # the main page: the host adds the document skeleton, so it starts with our head tags (a short title)
            h = re.sub(r'<title>.*?</title>', '<title>ClickBaitPays Guide</title>', h, count=1)
            hd = h.split('<head>\n', 1)[1].split('\n</head>', 1)[0]
            body_cls = re.search(r'<body class="([^"]*)">', h).group(1)
            body = h.split(f'<body class="{body_cls}">\n', 1)[1].rsplit('\n</body>', 1)[0]
            h = f'{hd}\n<div class="{body_cls}">{body}</div>\n'
        write(os.path.join(dst, p, 'index.html'), h)
    MODE = 'prod'
    print('preview:', len(pages), 'pages in', dst)
    return sorted(pages)


if __name__ == '__main__':
    main()
