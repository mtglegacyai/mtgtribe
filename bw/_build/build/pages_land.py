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
    lis = ''.join(f'<li data-fs tabindex="0" role="button"><span class="fsn">{i + 1}</span><span class="fst">{ic(ic_)}<b>{t}</b><small>{d}</small></span></li>'
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


def landing():
    here = ''
    import core as _c; _c._used.clear()
    st = [
        station(1, 'compass', 'Start here', 'Your route, an honest fit check, and a word for anyone who left or got stuck.',
                'dashboard/', [('Welcome', 'dashboard/'), ('Is it right for me?', 'dashboard/is-it-right-for-me/'), ('Welcome back', 'dashboard/welcome-back/')], here),
        station(2, 'bitcoin', 'Understand Bitcoin Wealth', 'Bitcoin, BTCB and the smart contract, in plain words.',
                'dashboard/what-is-bitcoin-wealth/', [('What is Bitcoin Wealth?', 'dashboard/what-is-bitcoin-wealth/')], here),
        station(3, 'network', 'See how it pays', 'The 14 positions, the 12 slots, recycling and the Royal Pool.',
                'dashboard/how-it-works/', [('The 14 positions', 'dashboard/how-it-works/'), ('The 12 slots', 'dashboard/12-slots/'),
                                            ('Recycling and Royal Pool', 'dashboard/recycling-royal-pool/')], here),
        station(4, 'users', 'Compare it honestly', 'Against a stokvel, against the newer copycats, and against your own checks.',
                'dashboard/stokvel/', [('Better than a stokvel?', 'dashboard/stokvel/'), ('What makes it different', 'dashboard/what-makes-it-different/'),
                                       ('Check it yourself', 'dashboard/check-it-yourself/')], here),
        station(5, 'rocket', 'Join step by step', 'Set up SafePal, buy on VALR or Binance, swap to BTCB, then activate slot 1.',
                'dashboard/join/', [(V['t1']['short'], 'play:t1'), ('Join step by step', 'dashboard/join/')], here),
        station(6, 'calculator', 'Run your numbers', 'Live Bitcoin price in rand, every slot in rand, and the halving countdown.',
                'dashboard/tools/bitcoin-to-rand/', [('Bitcoin to Rand', 'dashboard/tools/bitcoin-to-rand/'), ('Slot Calculator', 'dashboard/tools/slot-calculator/'),
                                                     ('Halving Countdown', 'dashboard/tools/halving-countdown/')], here),
        station(7, 'video', 'Meet us live', 'Zoom five evenings a week, in four languages.', 'dashboard/live-on-zoom/', [('Live on Zoom', 'dashboard/live-on-zoom/')], here),
        station(8, 'globe', 'Get your own BW Tribe Page', 'This whole website, with your name and your links on it. R1,000 once-off, paid after it\'s built.',
                'dashboard/bw-tribe-page/', [('See what you get', 'dashboard/bw-tribe-page/'), ('Order form', ORDER)], here),
        station(None, 'shield-check', 'Side trip: answers and safety', 'Straight answers, crypto words in plain English, and how to protect your wallet.',
                'dashboard/faq/', [('FAQ', 'dashboard/faq/'), ('Glossary', 'dashboard/glossary/'), ('Safety centre', 'dashboard/safety/')], here, 'branch'),
        station(None, 'message-circle', 'Side trip: the MTG TRIBE', 'A WhatsApp community for action takers. Ask, learn and grow together.',
                'dashboard/tribe/', [('WhatsApp group', GROUP), ('TikTok', TIKTOK), ('YouTube', YOUTUBE)], here, 'branch wa'),
    ]
    end = (f'<li class="stn end rv"><span class="dot" aria-hidden="true">{ic("flag")}</span><div class="card endcard">{ped("user-plus")}'
           f'<div class="tx"><b>Copy your sign-up link</b><span>When you\'re ready. The button copies MTG\'s link and opens nothing: paste it into SafePal\'s browser. '
           f'Introduced by someone else? Use their link.</span></div>{copy_btn("signup", "Copy sign-up link", size="sm")}</div></li>')
    route = f'<ol class="route" data-route><li class="fill" aria-hidden="true"></li>{"".join(st)}{end}</ol>'

    why = [
        ('wallet', 'Paid to your own wallet', 'No dashboard balance, no withdraw button, no admin to ask. Payouts land in the wallet only you control.'),
        ('badge-check', 'One entry, once', '0.001 BTC activates slot 1. You never pay again to move up: slots 2 to 12 are bought from the cycle below, once it fills.'),
        ('scan-search', 'Every payment public', 'The contract and every transaction sit on BNB Smart Chain. Open BscScan and look for yourself.'),
        ('bitcoin', 'Priced in Bitcoin', 'Slots and payouts are in BTCB, Bitcoin\'s value on BNB Smart Chain. Not points, not a made-up coin.'),
        ('landmark', 'No bank, no treasurer', 'No bank in the middle and no treasurer holding the pot in a personal account. Code follows the same rules for everyone.'),
        ('video', 'People, not just code', 'Live Zoom five evenings a week, in four languages, plus a WhatsApp community that answers questions.'),
    ]
    whyc = ''.join(f'<div class="wcard glass" data-tilt>{ped(i)}<h3 class="h3">{t}</h3><p>{d}</p></div>' for i, t, d in why)

    body = f'''<header class="ltop"><div class="wrap">
 <a class="brand" href="{A('', here)}" aria-label="Bitcoin Wealth guide home">{logo(here)}</a>
 <nav class="ltop-act" aria-label="Quick links"><a class="btn btn-ghost btn-sm hide-s" href="{A('dashboard/bw-tribe-page/', here)}">{ic('globe')}<span class="lbl">BW Tribe Page</span></a>
 <a class="btn btn-gold btn-sm ring" href="{A('dashboard/', here)}"><span class="emo" aria-hidden="true">📊</span><span class="lbl">Dashboard</span></a></nav>
</div></header>
<main id="main" tabindex="-1">
<section class="hero bwhero"><div class="wrap">
 <div class="hero-grid">
  <div class="hero-copy">
   <p class="kicker"><span class="coin3d sm" aria-hidden="true"><i class="cf"><b>₿</b></i><i class="cb"><b>₿</b></i></span>The original Bitcoin Wealth, explained by MTG</p>
   <h1 class="h1">Collect Bitcoin together. <span class="hl">Check every payment yourself.</span></h1>
   <p class="lead">Short videos and plain pages show you exactly how Bitcoin Wealth works: one once-off entry of 0.001 BTC, payouts that land in your own wallet, and a public record anyone can read. Nothing promised. Everything checkable.</p>
   <div class="hero-cta">
    <a class="btn btn-gold btn-lg ring" href="#how">{ic('play')}<span class="lbl">See how it works</span></a>
    <a class="btn btn-ghost btn-lg" href="{A('dashboard/', here)}">{ic('layout-dashboard')}<span class="lbl">Enter the dashboard</span></a>
   </div>
   <p class="sub">Free to learn. No sign-up needed to browse.</p>
  </div>
  <div class="hero-art" aria-hidden="true">
   <div class="orbit"><span class="coin3d xl"><i class="cf"><b>₿</b></i><i class="cb"><b>₿</b></i></span>
   <span class="o o1">0.001 BTC</span><span class="o o2">Wallet to wallet</span><span class="o o3">BNB Smart Chain</span></div>
  </div>
 </div>
 <div class="proof glass">
  <div class="pf"><b class="num"><span data-count="41013">{MEMBERS}</span></b><small>member IDs on the contract</small></div>
  <div class="pf"><b class="num">0.001 BTC</b><small>once-off, to activate slot 1</small></div>
  <div class="pf"><b class="num">Since {ON_CHAIN_SINCE}</b><small>on BNB Smart Chain</small></div>
  <div class="pf"><b class="num">100%</b><small>of payments public on BscScan</small></div>
  <p class="fine pfn">Read from the Bitcoin Wealth contract on {CHECKED}. <a class="inl" href="{A('dashboard/check-it-yourself/', here)}">Check it yourself</a>.</p>
 </div>
</div></section>

<section class="sec" id="how"><div class="wrap">
 <div class="sec-head center"><p class="eyebrow">See it before you believe it</p><h2 class="h2">One payment, start to finish</h2>
 <p class="lead">This is the whole idea in four moves. Tap any step.</p></div>
 {flow_stage(here)}
 <p class="honest-line">{ic('info')}<span>Every payout is another member's slot payment, moved wallet to wallet. No product, trading or mining: the community grows it together.</span></p>
</div></section>

<section class="sec"><div class="wrap two">
 <div class="sec-head"><p class="eyebrow">The engine</p><h2 class="h2">14 positions. Watch them fill.</h2>
 <p class="lead">Below you sit 2, then 4, then 8 positions. When a member takes a position, their payment goes straight out by fixed rules. Here's where all fourteen go.</p>
 <div class="btn-row"><a class="btn btn-ghost" href="{A('dashboard/how-it-works/', here)}">{ic('network')}<span class="lbl">The 14 positions, explained</span></a></div></div>
 {matrix(here)}
</div></section>

<section class="sec"><div class="wrap">
 <div class="sec-head center"><p class="eyebrow">Why people come home</p><h2 class="h2">What Bitcoin Wealth gets right</h2>
 <p class="lead">Members who tried the newer, shinier platforms keep coming back here, MTG included. These are the reasons, and every one can be checked.</p></div>
 <div class="wgrid">{whyc}</div>
</div></section>

<section class="sec"><div class="wrap">
 <div class="sec-head center"><p class="eyebrow">The honest scorecard</p><h2 class="h2">Better than a stokvel?</h2>
 <p class="lead">In four ways, yes. And here's how each one is funded.</p></div>
 <div class="score glass">
  <div class="srow h"><span></span><b>Stokvel</b><b>Bitcoin Wealth</b></div>
  <div class="srow"><span>Can you see every payment?</span><em class="no">{ic('circle-x')}Trust the treasurer</em><em class="yes">{ic('circle-check')}Public on BscScan</em></div>
  <div class="srow"><span>Who holds the money?</span><em class="no">{ic('circle-x')}A person or a bank account</em><em class="yes">{ic('circle-check')}It goes straight to members' own wallets</em></div>
  <div class="srow"><span>Who takes a cut?</span><em class="no">{ic('circle-x')}Bank fees, sometimes more</em><em class="yes">{ic('circle-check')}Only small network fees</em></div>
  <div class="srow"><span>What does it pay in?</span><em class="no">{ic('circle-x')}Rand</em><em class="yes">{ic('circle-check')}Bitcoin's value (BTCB)</em></div>
  <div class="srow stop"><span>How are payouts funded?</span><em class="no info">{ic('info')}Members take turns with the same pot</em><em class="yes info">{ic('info')}Members activating the positions below you</em></div>
 </div>
 <div class="center-row"><a class="btn btn-ghost" href="{A('dashboard/stokvel/', here)}">{ic('users')}<span class="lbl">Read the full comparison</span></a></div>
</div></section>

<section class="sec"><div class="wrap">
 <div class="sec-head center"><p class="eyebrow">Wherever you're coming from</p><h2 class="h2">Ignored it? Tried it? Left it?</h2></div>
 <div class="grid3">
  <div class="aud glass" data-tilt>{ped('eye')}<h3 class="h3">You scrolled past it</h3><p>Fair. There's a lot of noise. Give it ten minutes with clear eyes: look at how the money moves, then check it on the blockchain.</p></div>
  <div class="aud glass" data-tilt>{ped('rotate-ccw')}<h3 class="h3">You tried, and felt stuck</h3><p>Your first two business partners can take longer than you expect. This time, learn it properly, share it honestly, and give it time.</p></div>
  <div class="aud glass" data-tilt>{ped('house')}<h3 class="h3">You left for something newer</h3><p>Welcome home. Bitcoin Wealth is still here, still running, with every payment on chain. Compare it with anything, using the same five checks.</p></div>
 </div>
 <div class="center-row"><a class="btn btn-gold ring" href="{A('dashboard/welcome-back/', here)}">{ic('heart-handshake')}<span class="lbl">Take a fresh look</span></a></div>
</div></section>

<section class="sec"><div class="wrap two vstart">
 <div class="sec-head"><p class="eyebrow">Tutorial 1 of 3</p><h2 class="h2">Start with your own wallet</h2>
 <p class="lead">MTG sets up SafePal on his phone, one tap at a time: the official download, two backups, and a clean wallet with only BNB, USDT and BTCB.</p>
 {checks(["Download from the official website, never a link in a message", "Back up two ways: cloud and paper", "Keep only the three coins Bitcoin Wealth needs"])}
 <p class="fine">Next: buy on VALR or Binance, swap to BTCB, and join. Those tutorials are on the way.</p>
 <div class="btn-row">{valr_btn()}{binance_btn()}</div></div>
 <div class="phone-wrap">{vid('t1', here)}</div>
</div></section>

<section class="sec" id="tribe-page"><div class="wrap">
 <div class="offer glass" data-tilt>
  <div class="offer-copy">
   <p class="eyebrow">For members who share</p>
   <h2 class="h2">Get this whole website, with <span class="hl">your</span> link inside</h2>
   <p class="lead">Your BW Tribe Page is a copy of this guide with your name, your photo and your own Bitcoin Wealth link built in. One link to send to every potential business partner. It teaches, answers and shows the tutorials for you, day and night.</p>
   {checks(["Your address: mtgtribe.com/bw/yourname or bitcoinwealthpays.com/yourname", "Every sign-up button carries your referral link", "Five free edits to make it yours"])}
   <div class="price"><b>R1,000</b><span>once-off<br><small>Pay only after it's built. Change your mind? Nothing to lose.</small></span></div>
   <div class="btn-row"><a class="btn btn-gold btn-lg ring" href="{esc(ORDER)}">{ic('globe')}<span class="lbl">Order your BW Tribe Page</span></a>
   <a class="btn btn-ghost" href="{A('dashboard/bw-tribe-page/', here)}">{ic('list-checks')}<span class="lbl">See everything you get</span></a></div>
  </div>
  <div class="offer-art">
   <div class="lion"><video data-deco autoplay muted loop playsinline preload="none" poster="{A('img/bitcoin-wealth-mascot-lion-bw.webp', here)}" width="540" height="960" aria-hidden="true"><source src="{L('media/bitcoin-wealth-mascot-lion-wave.mp4', here)}" type="video/mp4"></video></div>
   <div class="secret glass">{ic('lock-keyhole')}<div><b>One more thing, for owners only</b><p>There's a traffic source that puts pages like yours in front of people who already watch crypto ads all day, and it pays an income of its own. No guarantee they join. Owners get the full story, the tutorials and the explainers.</p></div></div>
  </div>
 </div>
</div></section>

<section class="map" id="route"><div class="wrap">
 <div class="map-head"><h2 class="h2">Your route through Bitcoin Wealth</h2><p class="lead">Every stop opens an exact page, video or tool. Start at stop 1 and follow the line.</p></div>
 {route}
 <div class="route-key"><span><i></i>Main route</span><span><i class="cy"></i>Side trips</span></div>
</div></section>

<section class="sec"><div class="wrap"><div class="joinband glass">
 <div><h2 class="h3">Don't learn this alone</h2><p>{ZOOM_LINE.replace(" below this video", "")}</p></div>
 <div class="btn-row">{wa_group_btn(label='Join the free MTG TRIBE', ring=True)}<a class="btn btn-ghost" href="{A('dashboard/live-on-zoom/', here)}">{ic('video')}<span class="lbl">Zoom schedule</span></a></div>
</div></div></section>
</main>
<footer class="lfoot"><div class="wrap">
 <div class="lfoot-top">
  <div class="about">{logo(here)}<p>Independent Bitcoin Wealth education by MTG 👑 | Your Digital Architect.</p>
   <div class="socials"><a href="{esc(TIKTOK)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on TikTok">{ic('tiktok')}</a><a href="{esc(YOUTUBE)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on YouTube">{ic('youtube')}</a><a href="{esc(FACEBOOK)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on Facebook">{ic('facebook')}</a><a href="{esc(TELEGRAM)}" target="_blank" rel="noopener" aria-label="MTG TRIBE on Telegram">{ic('telegram')}</a><a href="{esc(GROUP)}" target="_blank" rel="noopener" aria-label="Join the MTG TRIBE WhatsApp group">{ic('whatsapp')}</a></div></div>
  <div><h3>Learn</h3><ul><li><a href="{A('dashboard/', here)}">Dashboard</a></li><li><a href="{A('dashboard/what-is-bitcoin-wealth/', here)}">What is Bitcoin Wealth?</a></li><li><a href="{A('dashboard/how-it-works/', here)}">The 14 positions</a></li><li><a href="{A('dashboard/tutorials/', here)}">Tutorial videos</a></li><li><a href="{A('dashboard/faq/', here)}">FAQ</a></li></ul></div>
  <div><h3>Tools</h3><ul><li><a href="{A('dashboard/tools/bitcoin-to-rand/', here)}">Bitcoin to Rand Converter</a></li><li><a href="{A('dashboard/tools/slot-calculator/', here)}">Slot Calculator</a></li><li><a href="{A('dashboard/tools/halving-countdown/', here)}">Halving Countdown</a></li><li><a href="{A('dashboard/bw-tribe-page/', here)}">BW Tribe Page</a></li></ul></div>
  <div><h3>Connect</h3><ul><li><a href="{esc(GROUP)}" target="_blank" rel="noopener">Join the MTG TRIBE</a></li><li><a href="{esc(WA_MTG)}" target="_blank" rel="noopener">WhatsApp MTG</a></li><li><a href="{esc(VALR)}" target="_blank" rel="noopener">VALR</a></li><li><a href="{esc(BINANCE)}" target="_blank" rel="noopener">Binance</a></li><li><a href="{A('dashboard/disclaimer/', here)}">Disclaimer</a></li></ul></div>
 </div>
 <p class="disc">{DISCLAIMER} <a href="{A('dashboard/disclaimer/', here)}">Full disclaimer</a>.</p>
 <div class="fbot"><span>© 2026 MTG 👑 | Your Digital Architect. <a class="inl" href="{SITE}/" >mtgtribe.com</a></span><span class="sig">Let's Get This Crypto! 💪</span></div>
</div></footer>
{overlays(here)}'''
    from seo import SEO_DESC
    hd = head('Bitcoin Wealth explained by MTG: how it works, how to join, check it yourself', SEO_DESC['land'], '', here,
              extra_ld=video_ld(['t1'], here), og_key='land')
    return hd, body
