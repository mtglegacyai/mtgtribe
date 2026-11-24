"""Landing page: mtgtribe.com/bw (show how it works first, then the route)."""
from core import *


def station(n, icon, title, desc, main, subs, here, kind=''):
    links = ''
    for lab, t in subs:
        if t.startswith('play:'):
            links += f'<button type="button" class="wl" data-play="{t[5:]}">{ic("circle-play")}{lab}</button>'
        elif t.startswith('http'):
            links += f'<a class="wl" href="{esc(t)}" target="_blank" rel="noopener">{lab}</a>'
        elif t.startswith('/'):
            links += f'<a class="wl" href="{esc(t)}">{lab}</a>'
        else:
            links += f'<a class="wl" href="{A(t, here)}">{lab}</a>'
    where = f'<div class="where">{links}</div>' if links else ''
    pc = {'branch': 'cy', 'branch wa': 'wa'}.get(kind, '')
    mhref = esc(main) if main.startswith('http') else A(main, here)
    ext = ' target="_blank" rel="noopener"' if main.startswith('http') else ''
    return (f'<li class="stn rv {kind}"><span class="dot" aria-hidden="true">{n or ""}</span><div class="card">{ped(icon, pc)}'
            f'<div class="tx"><a class="t" href="{mhref}"{ext}><b>{title}</b></a><span>{desc}</span>{where}</div>'
            f'<span class="go" aria-hidden="true">{ic("chevron-right")}</span></div></li>')


def flow_stage(here, big=True):
    """One payment, wallet to wallet: a code-made 3D scene with four steps (no video credits)."""
    steps_ = [
        ('wallet', 'A member activates slot 1', 'They send 0.001 BTC worth of BTCB from their own wallet. Once.'),
        ('box', 'The smart contract splits it', 'Code on BNB Smart Chain follows fixed rules, in the same transaction.'),
        ('hand-coins', 'It lands in a member\'s own wallet', 'No withdraw button, no request, no office. It simply arrives.'),
        ('scan-search', 'Anyone can check it', 'Every payment is public on BscScan, forever. Don\'t trust. Verify.'),
    ]
    lis = ''.join(f'<li><button type="button" class="fs" data-fs><span class="fsn">{i + 1}</span><span class="fst">{ic(ic_)}<b>{t}</b><small>{d}</small></span></button></li>'
                  for i, (ic_, t, d) in enumerate(steps_))
    return f'''<div class="flow3d glass" data-flow data-tilt>
 <div class="scene" aria-hidden="true">
  <div class="node n-a"><span class="wal">{ic("wallet")}</span><small>New member</small></div>
  <div class="track t1"><i class="coin2"><b>₿</b></i></div>
  <div class="node n-c"><div class="cube"><span class="f fr">{ic("blocks")}</span><span class="f bk"></span><span class="f lf"></span><span class="f rt"></span><span class="f tp"></span><span class="f bt"></span></div><small>Smart contract</small></div>
  <div class="track t2"><i class="coin2"><b>₿</b></i></div>
  <div class="node n-b"><span class="wal you">{ic("wallet")}</span><small>A member's own wallet</small></div>
  <div class="chain">{"".join(f'<i style="--k:{k}"></i>' for k in range(9))}<span>{ic("scan-search")}Public on BscScan</span></div>
 </div>
 <ol class="fsteps" aria-label="One payment, step by step">{lis}</ol>
</div>'''


def matrix(here, cycle_toggle=True):
    seats = '<div class="mrow r0"><span class="you">YOU</span></div>'
    k = 0
    for row, n in ((1, 2), (2, 4), (3, 8)):
        cells = ''
        for _ in range(n):
            k += 1
            cells += f'<span class="seat" style="--i:{k}">{k}</span>'
        seats += f'<div class="mrow r{row}">{cells}</div>'
    parts = [('up', 'Your upline', 'Your upline'), ('you', 'Your wallet', 'Your wallet'), ('next', 'Your next slot', 'Royal Pool'),
             ('below', 'Members below you', 'Members below you'), ('recycle', 'Recycle', 'Recycle')]
    bar = ''.join(f'<span class="part p-{c}" data-part="{c}" style="--n:1"><b>1</b><small data-alt data-c1="{a}" data-cn="{b}">{a}</small></span>' for c, a, b in parts)
    tog = ('<div class="seg" role="group" aria-label="Which cycle"><button type="button" data-c="c1" aria-pressed="true">First cycle</button>'
           '<button type="button" data-c="cn" aria-pressed="false">Later cycles</button></div>') if cycle_toggle else ''
    return f'''<div class="mx glass" data-mx>
 <div class="mx-top"><p class="fine" aria-live="polite" data-k="mxs">14 positions: 2, then 4, then 8</p>
 <div class="mx-act">{tog if cycle_toggle else ''}<button type="button" class="btn btn-ghost btn-sm" data-mxplay>{ic("rotate-ccw")}<span class="lbl">Fill them again</span></button></div></div>
 <div class="mtree" aria-hidden="true">{seats}</div>
 <div class="split" data-split aria-label="Where the 14 payments go">{bar}</div>
 <p class="fine mx-note">Each position is one member paying the slot price, and each one produces one payment.
 Nine of the fourteen point to you: <span data-alt data-c1="6 to your wallet, 2 buy your next slot, 1 recycles you" data-cn="7 to your wallet, 1 recycles you, plus the Royal Pool for slot 3 qualifiers">6 to your wallet, 2 buy your next slot, 1 recycles you</span>.</p>
</div>'''


WHY = [
    ('wallet', 'Paid to your own wallet', 'No dashboard balance, no withdraw button, nobody to ask. Payouts land in the wallet only you control.'),
    ('badge-check', 'One entry, once', '0.001 BTC activates slot 1. You never pay again to move up: slots 2 to 12 are bought from the cycle below, as soon as its seat 5 is filled.'),
    ('scan-search', 'Every payment public', 'The contract and every transaction sit on BNB Smart Chain. Open BscScan and look for yourself.'),
    ('bitcoin', 'Priced in Bitcoin', 'Slots and payouts are in BTCB, Bitcoin\'s value on BNB Smart Chain. Not points, not a made-up coin.'),
    ('landmark', 'No bank, no treasurer', 'No bank in the middle and no treasurer holding the pot in a personal account. Code follows the same rules for everyone.'),
    ('video', 'People, not just code', 'Live Zoom five evenings a week, in four languages, plus a WhatsApp community that answers questions.'),
]


def why_grid():
    return '<div class="wgrid">' + ''.join(f'<div class="wcard glass" data-tilt>{ped(i)}<h3 class="h3">{t}</h3><p>{d}</p></div>' for i, t, d in WHY) + '</div>'


def scorecard():
    return f"""<div class="score glass">
  <div class="srow h"><span></span><b>Stokvel</b><b>Bitcoin Wealth</b></div>
  <div class="srow"><span>Can you see every payment?</span><em class="no">{ic('circle-x')}Trust the treasurer</em><em class="yes">{ic('circle-check')}Public on BscScan</em></div>
  <div class="srow"><span>Who holds the money?</span><em class="no">{ic('circle-x')}A person or a bank account</em><em class="yes">{ic('circle-check')}It goes straight to members' own wallets</em></div>
  <div class="srow"><span>Who takes a cut?</span><em class="no">{ic('circle-x')}Bank fees, sometimes more</em><em class="yes">{ic('circle-check')}Only small network fees</em></div>
  <div class="srow"><span>What does it pay in?</span><em class="no">{ic('circle-x')}Rand</em><em class="yes">{ic('circle-check')}Bitcoin's value (BTCB)</em></div>
  <div class="srow"><span>How much do you put in?</span><em class="no">{ic('circle-x')}Every month, for the whole cycle</em><em class="yes">{ic('circle-check')}0.001 BTC, once</em></div>
  <div class="srow stop"><span>How are payouts funded?</span><em class="no info">{ic('info')}Members take turns with the same pot</em><em class="yes info">{ic('info')}Members activating the positions below you</em></div>
 </div>"""


def watch_btn(code):
    """the gold button of a stage: it opens that stage's tutorial"""
    v = V[code]
    return (f'<button type="button" class="btn btn-gold btn-sm" data-play="{code}">{ic("play")}'
            f'<span class="lbl">Watch Tutorial {v["n"]} ({mmss(v["secs"])})</span></button>')


def start3(here, head=True):
    """the joiner's fast lane: three stages (the Join page breaks them into five steps)"""
    v = V['t1']
    st = [
        ('wallet', 'Stage 1', '10 min', 'Set up your wallet', 'SafePal from the official site, backed up two ways, with only BNB, USDT and BTCB.',
         watch_btn('t1')),
        ('coins', 'Stage 2', '15 min', 'Buy BNB, send it to SafePal', 'Buy BNB with rand on VALR or Binance, then send it to your SafePal wallet.',
         watch_btn('t2') + valr_btn(label='VALR') + binance_btn(label='Binance')),
        ('rocket', 'Stage 3', '5 min', 'Activate slot 1', 'Swap BNB for BTCB, paste the sign-up link into SafePal\'s browser and confirm twice. You pay 0.001 BTC, once.',
         watch_btn('t3') + copy_btn('signup', 'Copy sign-up link', size='sm', ring=False)),
    ]
    lis = ''.join(f'<li class="stg glass"><span class="sn">{i + 1}</span><div class="sbody"><p class="sk">{ic(icn)}<b>{k}</b> · {t}</p>'
                  f'<h3>{h}</h3><p>{d}</p><div class="btn-row">{acts}</div></div></li>' for i, (icn, k, t, h, d, acts) in enumerate(st))
    hd = ('<div class="sec-head center"><p class="eyebrow">Ready to start?</p><h2 class="h2">Join in <span class="hl">3 stages.</span></h2>'
          '<p class="lead">About 30 minutes, all on your phone. Watch, tap, done.</p></div>') if head else ''
    return (f'{hd}<ol class="stages" data-stages>{lis}</ol>'
            f'<p class="stages-more"><a class="inl" href="{A("dashboard/join/", here)}">Every tap, step by step</a> · Introduced by someone else? Use their link.</p>')


def landing():
    """Minimal and sleek (MTG, 14 Nov 2026: "minimal, sleek, and the rest of the info, videos, etc must be in a clean dashboard")."""
    here = ''
    import core as _c; _c._used.clear()
    # one card only (MTG, 16 Nov 2026: "I really want to optimise/increase traffic to this page: mtgtribe.com/bw/dashboard/join",
    # so How It Works, Check It Yourself, Better Than A Stokvel?, Free Live Tools and Live On Zoom left the home page; they are in the dashboard)
    tiles = [
        ('rocket', 'Join Step-By-Step', 'SafePal, BNB, BTCB, slot 1. One tap at a time.', 'dashboard/join/'),
    ]
    tl = ''.join(f'<a class="tile" href="{A(p, here)}">{ped(i)}<span class="tt"><b>{t}</b><small>{d}</small></span>{ic("arrow-up-right", "ic go")}</a>'
                 for i, t, d, p in tiles)
    tape_items = [('0.001 BTC', 'once-off'), ('Paid', 'wallet to wallet'), (MEMBERS, 'member IDs'), ('Since April 2026', 'on BNB Smart Chain'),
                  ('100%', 'of payments public'), ('5 evenings', 'live on Zoom'), ('R1,000', 'your own marketing website')]
    tape_one = ''.join(f'<span><i>▲</i><b>{a}</b> {b}</span>' for a, b in tape_items)
    v = V['t1']
    big, small = poster('t1', here)
    body = f"""<header class="ltop"><div class="wrap">
 <a class="brand" href="{A('', here)}" aria-label="Bitcoin Wealth guide home">{logo(here)}</a>
 <nav class="ltop-act" aria-label="Quick links"><a class="btn btn-ghost btn-sm hide-s" href="{A('dashboard/bw-tribe-page/', here)}">{ic('globe')}<span class="lbl">Your own website</span></a>
 <a class="btn btn-gold btn-sm ring" href="{A('dashboard/', here)}">{ic('layout-dashboard')}<span class="lbl">Dashboard</span></a></nav>
</div></header>
<main id="main" tabindex="-1">
<section class="lhero">
 <div class="lbg" aria-hidden="true"><canvas data-dust></canvas><i class="beam"></i><i class="beam b2"></i><i class="floor"></i></div>
 <div class="wrap lhero-in solo">
  <div class="lcopy">
   <p class="pill-eye"><i></i>Independent guide by MTG 👑</p>
   <h1 class="display"><span class="ln"><span>Collect</span></span> <span class="ln"><span>Bitcoin.</span></span> <span class="ln"><span class="hl">Together.</span></span></h1>
   <p class="lede">Bitcoin Wealth, explained in short videos. One once-off entry of 0.001 BTC, payouts straight to your own wallet, and every payment public for anyone to check.</p>
   <div class="ctas">
    <a class="btn btn-gold btn-lg ring" href="#start">{ic('rocket')}<span class="lbl">Get Started</span></a>
    <button type="button" class="btn btn-ghost btn-lg" data-play="t1">{ic('play')}<span class="lbl">Watch First ({mmss(V['t1']['secs'])})</span></button>
   </div>
   <p class="livep" data-livep hidden><i></i><span>Slot 1 today: <b data-k="z">R0</b> <small>0.001 BTC at the live price</small></span></p>
   <div class="chips mini">{chip('users', f'{MEMBERS} member IDs')}{chip('badge-check', '0.001 BTC once-off')}{chip('info', 'Independent, not official')}</div>
  </div>
 </div>
</section>
<div class="tape" aria-label="Bitcoin Wealth in short"><div class="tape-in">{tape_one}<span aria-hidden="true" class="dup">{tape_one}</span></div></div>

<section class="sec lsec promo" id="how-it-works" aria-labelledby="promo-h"><div class="wrap">
 <div class="sec-head center"><p class="eyebrow">{round(V['i1']['secs'] / 60)} minutes</p><h2 class="h2" id="promo-h">Curious? <span class="hl">See how it works.</span></h2>
 <p class="lead">Leo shows the whole Bitcoin Wealth plan, slide by slide. Then follow every step yourself, one tap at a time.</p></div>
 {vid('i1', here, cap=False, hero=True)}
 <div class="center-row promo-acts"><a class="btn btn-gold btn-lg ring" href="{A('dashboard/tutorials/', here)}">{ic('circle-play')}<span class="lbl">Watch The Step-By-Step Tutorials</span></a>
 <button type="button" class="btn btn-ghost btn-lg" data-play="p1">{ic('play')}<span class="lbl">Bitcoin Wealth In 34 Seconds</span></button></div>
 <p class="fine promo-note">The video is the programme's own presentation, presented by Leo; the 34-second button plays a short promo video. Leo and his voice are made with AI. Don't just take anyone's word for it: <a class="inl" href="{A('dashboard/check-it-yourself/', here)}">check it yourself</a>.</p>
</div></section>

<section class="sec lsec" id="start"><div class="wrap">{start3(here)}</div></section>

<section class="sec lsec"><div class="wrap">
 <div class="sec-head center"><p class="eyebrow">Everything inside</p><h2 class="h2">One clean <span class="hl">dashboard.</span></h2>
 <p class="lead">Every video, page and tool lives in the dashboard, in the right order. Start anywhere.</p></div>
 <div class="tiles{' one' if len(tiles) == 1 else ''}">{tl}</div>
 <div class="center-row"><a class="btn btn-gold btn-lg ring" href="{A('dashboard/', here)}">{ic('layout-dashboard')}<span class="lbl">Enter the dashboard</span></a></div>
</div></section>

<section class="sec lsec"><div class="wrap">
 <a class="tribeband glass" href="{A('dashboard/bw-tribe-page/', here)}" data-tilt>
  <img src="{A('img/bitcoin-wealth-mascot-lion-bw.webp', here)}" width="540" height="945" loading="lazy" alt="MTG's lion mascot in the mtgTribe.com/bw shirt">
  <span class="tb-copy"><span class="eyebrow">For members who share</span><b>Your own Bitcoin Wealth website, with your link inside.</b>
  <small>Your own Bitcoin Wealth marketing website: R1,000 or $50 in USDT, once-off. Pay only after it's built.</small></span>
  <span class="btn btn-gold ring">{ic('globe')}<span class="lbl">See your own website</span></span>
 </a>
</div></section>
</main>
<footer class="lfoot slim"><div class="wrap">
 <div class="lfoot-row">
  <a href="{A('', here)}" aria-label="Bitcoin Wealth guide home">{logo(here)}</a>
  <div class="socials"><a href="{esc(GROUP)}" target="_blank" rel="noopener" aria-label="Join the MTG TRIBE WhatsApp group">{ic('whatsapp')}</a><a href="{esc(TIKTOK)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on TikTok">{ic('tiktok')}</a><a href="{esc(YOUTUBE)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on YouTube">{ic('youtube')}</a><a href="{esc(FACEBOOK)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on Facebook">{ic('facebook')}</a><a href="{esc(TELEGRAM)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on Telegram">{ic('telegram')}</a></div>
 </div>
 <p class="disc">{DISCLAIMER} <a href="{A('dashboard/disclaimer/', here)}">Full disclaimer</a>.</p>
 <div class="fbot"><span>© 2026 MTG 👑 | Your Digital Architect. <a class="inl" href="{HUB}/">mtgtribe.com</a></span><span class="sig">Let's Get This Crypto! 💪</span></div>
</div></footer>
<nav class="bnav" aria-label="Quick menu">
 <a href="{A('', here)}" aria-current="page">{ic('house')}<span>Home</span></a>
 <a href="{A('dashboard/', here)}">{ic('layout-dashboard')}<span>Dashboard</span></a>
 <a href="#start">{ic('rocket')}<span>Start</span></a>
 <button type="button" data-copy="signup">{ic('user-plus')}<span>Sign Up</span><span class="copied" aria-live="polite">Copied ✓</span></button>
</nav>
{overlays(here)}"""
    from seo import SEO_DESC
    hd = head('Bitcoin Wealth explained by MTG: how it works, how to join, check it yourself', SEO_DESC['land'], '', here,
              extra_ld=video_ld(['p1', 'i1', 't1', 't2', 't3'], here), og_key='land')
    return hd, body
