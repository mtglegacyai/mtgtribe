# The JetUP overview page: mtgtribe.com/jetup/
from layout import *

HOME_FAQ = [
 ('What is JetUP, and how is it linked to TAG Markets?',
  "JetUP is a community and partner program with training and AI tools. TAG Markets is the broker. JetUP says on its own website that its trading accounts and transactions run through T.M. Financials Ltd, trading as TAG Markets. Your money sits in your own account at TAG Markets, not with JetUP."),
 ('Is JetUP with TAG Markets safe?',
  "Nobody can promise that. What you can do is check: who holds your money, who regulates the broker, whether the strategy's results are public, how big the moves are and how to get out. MTG's 5 checks walk you through each one, with the sources, so you decide with your eyes open."),
 ('How much do I need to start?',
  "The sign-up training uses $155 in USDT or USDC: $50 goes into the Sonic AI strategy, $100 stays in your balance for the Dennis Fast Start Promo, and a few dollars stay spare. Start with an amount you're comfortable with, and grow from there."),
 ('Is there risk?',
  "Yes, like any trading. Prices move both ways, and 24x Amplify makes every move bigger. That's why the plan starts small ($50 into Sonic AI), and a built-in loss limit closes the account at 10% of the starting balance (5% with a community token), so you know the line before you start."),
 ('Is this official JetUP or TAG Markets material?',
  "No. This is an independent guide by MTG. It quotes JetUP and TAG Markets where it uses their figures, and it shows you where to check them yourself."),
]

TAPE = [
 ('▲', 'u', 'XAU/USD', 'gold, priced in US dollars'),
 ('▲', 'u', '70%', 'of strategy profit is yours'),
 ('●', '', '30%', 'performance fee, from profits only'),
 ('▲', 'u', '$0', 'join fee, 0% management fee'),
 ('●', '', '24x', 'Amplify: every move is bigger'),
 ('▲', 'u', 'Myfxbook', 'results you can check yourself'),
 ('●', '', '10% / 5%', 'built-in loss limit, written down'),
 ('▲', 'u', 'MT5', 'account in your own name'),
 ('●', '', '1 month', 'minimum period on Sonic AI'),
]

def tape():
    items = ''.join('<span><i class="%s" aria-hidden="true">%s</i><b>%s</b> %s</span>' % (c, a, b, t) for a, c, b, t in TAPE)
    return '<div class="tape" role="region" aria-label="Key facts"><div class="tape-in">%s<span aria-hidden="true" style="display:contents">%s</span></div></div>' % (items, items.replace('<span>', '<span aria-hidden="true">'))

def flow():
    nodes = [
     ('you', 'i-users2', 'You', 'Account holder'),
     ('jetup', None, 'JetUP', 'Community'),
     ('tag', 'i-landmark', 'TAG', 'The broker'),
     ('copyx', 'i-copyx', 'CopyX', 'Copy platform'),
     ('sonic', 'i-candle2', 'Sonic AI', 'The strategy'),
    ]
    info = {
     'you': ('You, the account holder', 'i-users2', 'You open the account, you fund it and you decide. Your money sits in an account in your own name at TAG Markets, and you can log in and see your own balance any time.'),
     'jetup': ('JetUP: the community', None, 'JetUP is the community and partner program, with training and AI tools. JetUP does not trade, and it does not hold your money. Its portal is jetup.ibportal.io and its hub is jet-up.ai.'),
     'tag': ('TAG Markets: the broker', 'i-landmark', "TAG Markets is the broker. Its trading company, T.M. Financials Ltd, is licensed in Mauritius by the FSC (Financial Services Commission). Your trading account is opened here, in your own name, at portal.tagmarkets.com."),
     'copyx': ('CopyX: the copy trading platform', 'i-copyx', "CopyX is TAG Markets' copy trading platform. It connects your account to a strategy, so the strategy's trades are copied into your account automatically."),
     'sonic': ('Sonic AI: the strategy', 'i-candle2', "Sonic AI is the main strategy members connect. It trades gold, shown as XAU/USD (the price of gold in US dollars). Its track record is published on Myfxbook, so you can look before you deposit."),
    }
    btns = []
    for k, ic, b, s in nodes:
        orb = '<img src="/jetup/img/jetup-mark-128.webp" width="44" height="44" alt="">' if ic is None else icon(ic)
        btns.append('<button type="button" class="node" data-k="%s" aria-pressed="false" aria-controls="flow-info"><span class="orb">%s</span><b>%s</b><small>%s</small></button>' % (k, orb, b, s))
    tpls = []
    for k, (h, ic, p) in info.items():
        ped = '<span class="ped lime"><b>%s</b></span>' % (icon(ic) if ic else '<img src="/jetup/img/jetup-mark-64.webp" width="26" height="26" alt="">')
        tpls.append('<template data-node="%s">%s<div><span class="tagl">Who does what</span><h3>%s</h3><p>%s</p></div></template>' % (k, ped, h, p))
    first = info['you']
    return ('<div class="flow" role="group" aria-label="Tap each part to see what it does">%s<span class="dot" aria-hidden="true"></span></div>' % ''.join(btns)
            + '<div class="card pad flow-info" id="flow-info" aria-live="polite"><span class="ped lime"><b>%s</b></span><div><span class="tagl">Who does what</span><h3>%s</h3><p>%s</p></div></div>' % (icon(first[1]), first[0], first[2])
            + ''.join(tpls))

def build_home():
    path = '/jetup/'
    v5 = VIDEOS['5checks']
    checks = [
     ('1', 'Who holds my money?', 'An MT5 (MetaTrader 5) account at TAG Markets, in your own name. Log in yourself and see your own balance.'),
     ('2', 'Who regulates the broker?', 'T.M. Financials Ltd holds FSC Mauritius licence GB21026474. Its South African company is FSCA authorised, FSP 55237, for marketing services.'),
     ('3', 'Are the results real?', 'Sonic AI publishes on Myfxbook: +30.1% gross from 3 Nov 2024 to 4 Oct 2026. Your 70% of that is about 21%. Not a forecast.'),
     ('4', 'How big are the moves?', '$250 × 24 = $6,000 of exposure, so every move is bigger, in both directions. A built-in loss limit sets the line in advance.'),
     ('5', 'Can I get out?', 'Profits can be withdrawn any time. The promo bonus comes after 12 months. Start small and test a small withdrawal early.'),
    ]
    chk_html = ''.join('''<article class="card chk rv" style="--d:%d"><span class="num">%s</span><h3>%s</h3><p>%s</p>
      <button type="button" class="tick" data-id="c%s" aria-pressed="false"><span class="bx">%s</span>I checked this</button></article>''' % (i, n, h, p, n, icon('i-check2')) for i, (n, h, p) in enumerate(checks))
    parts = [
     ('1', 'Create your JetUP account', "Your sponsor's Partner link, the sign-up form and the email check."),
     ('2', 'Link JetUP to TAG Markets', 'Tap Register CopyX inside JetUP, never register directly on CopyX.'),
     ('3', 'Verify your identity', "TAG Markets' questions, then the ID and face scan by Sumsub."),
     ('4', 'Fund your account', 'Deposit $155 in USDT or USDC on the right network.'),
     ('5', 'Connect Sonic AI', 'Invest 50 only, then the two community codes.'),
     ('6', 'Claim the Dennis promo', 'Your CU number on jet-up.ai, then see both accounts.'),
    ]
    parts_html = ''.join('<a class="card part rv" style="--d:%d" href="/jetup/get-started/#part-%s"><span class="pn">%s</span><span><h3>%s</h3><p>%s</p></span></a>' % (i % 3, n, n, h, p) for i, (n, h, p) in enumerate(parts))
    explore = [
     ('/jetup/how-it-works/', 'i-layers2', '', 'How It Works', 'Who holds what, the 70/30 split, Amplify and the loss limit, one picture at a time.'),
     ('/jetup/partner-plan/', 'i-users2', '', 'The Partner Plan', "JetUP's four incomes and rewards, in plain English, with the rules most people miss."),
     ('/jetup/tools/exposure-calculator/', 'i-candle2', 'lime', 'Exposure Calculator', 'Type your amount and a price move. See what 24x Amplify does to your own money.'),
     ('/jetup/tools/profit-split-calculator/', 'i-split', 'lime', 'Profit Split Calculator', 'See your 70% and the 30% fee on any profit, and why a loss carries no fee.'),
     ('/jetup/bix-card/', 'i-card2', '', 'BIX Card', 'The crypto wallet and Visa card inside the JetUP portal, and how to link it.'),
     ('/jetup/downloads/', 'i-dl2', '', 'Downloads', 'The Business Plan, the BIX guide, the official decks and the videos.'),
    ]
    explore_html = ''.join('<a class="card pad rv" style="--d:%d;display:grid;gap:12px" href="%s"><span class="ped %s"><b>%s</b></span><h3 class="h3">%s</h3><p class="small" style="margin:0;line-height:1.6">%s</p><span class="lime" style="display:flex;align-items:center;gap:8px;font-weight:800;font-size:14px">Open %s</span></a>' % (i % 3, h, c, icon(ic), t, p, icon('i-arrow2')) for i, (h, ic, c, t, p) in enumerate(explore))
    faq_html = ''.join('<details class="rv" style="--d:%d"><summary>%s</summary><p>%s</p></details>' % (i, q, a) for i, (q, a) in enumerate(HOME_FAQ))

    main = f'''
<section class="hero" aria-labelledby="h1">
 <div class="hero-bg" aria-hidden="true"><picture><source media="(orientation: portrait)" srcset="/jetup/img/jetup-hero-earth-portrait.webp"><img src="/jetup/img/jetup-hero-earth.webp" srcset="/jetup/img/jetup-hero-earth-720.webp 1280w, /jetup/img/jetup-hero-earth.webp 1920w" sizes="100vw" width="1920" height="1080" alt="" fetchpriority="high"></picture><video muted loop playsinline preload="none" data-hd="/jetup/media/jetup-hero-earth-1080.mp4" data-sd="/jetup/media/jetup-hero-earth-720.mp4" data-pt="/jetup/media/jetup-hero-earth-portrait.mp4" tabindex="-1"></video></div>
 <div class="wrap hero-in">
  <div>
   <p class="pill rv"><i aria-hidden="true"></i>Independent guide by MTG 👑</p>
   <h1 class="display rv" style="--d:1;margin-top:22px" id="h1"><span>Trade smarter.</span><br><span class="grad">Check first.</span></h1>
   <p class="lede rv" style="--d:2">JetUP and TAG Markets, explained in plain English: who holds your money, how copy trading works, what it costs, the rules to know, and every tap to get started. See it all before you put in a cent.</p>
   <div class="ctas rv" style="--d:3">
    {video_btn('5checks', 'btn btn-pri', '<span class="play">' + icon('i-play2', '') + '</span>Watch the 5 checks first')}
    <a class="btn btn-ghost" href="/jetup/get-started/">{icon('i-rocket2')}Start the sign-up training</a>
    {join_btn('Join JetUP', 'btn btn-lime')}
   </div>
   <ul class="chips rv" style="--d:4">
    <li class="chip">{icon('i-film2')}2 videos, about 15 minutes</li>
    <li class="chip">{icon('i-lock')}Account in your own name</li>
    <li class="chip">{icon('i-compass2')}Independent, not official</li>
   </ul>
  </div>
  <div class="rv" style="--d:2">
   {laptop('5checks', 'Watch first: 5 checks before you try JetUP (5:25)', eager=True)}
  </div>
 </div>
</section>
{tape()}

<section class="sec" id="who" aria-labelledby="who-h">
 <div class="wrap">
  <div class="shead"><p class="eyebrow rv">Who does what</p><h2 class="h2 rv" style="--d:1" id="who-h">Five names. <span class="grad">One simple picture.</span></h2>
   <p class="lede rv" style="--d:2">Most confusion starts when these get mixed up. Tap each one and watch where it sits, from you to the strategy.</p></div>
  <div class="rv" style="max-width:980px;margin:0 auto 34px">{laptop('simple', 'The simple picture, in 1:39')}</div>
  <div class="rv">{flow()}</div>
  <div class="rv" style="max-width:980px;margin:34px auto 0">{laptop('who', 'Five names, one picture: the minibus taxi (2:08)')}</div>
  <div class="card pad block rv">
   <p class="eyebrow" style="margin-bottom:14px">An everyday picture</p>
   <div class="analogy">
    <div><h3 class="h3" style="font-size:1.4rem">Think of a minibus taxi 🚐</h3>
     <p class="lede" style="margin-top:10px">You don't drive. You choose a driver, take your seat, and the driver does the driving. Copy trading works the same way.</p></div>
    <ul>
     <li><span class="e" aria-hidden="true">🧑‍✈️</span><span><b>Sonic AI is the driver.</b> It does the trading.</span></li>
     <li><span class="e" aria-hidden="true">💺</span><span><b>Your seat is booked in your name.</b> That's your TAG Markets account.</span></li>
     <li><span class="e" aria-hidden="true">🪧</span><span><b>CopyX is the route board</b> that puts you in that driver's taxi.</span></li>
     <li><span class="e" aria-hidden="true">👥</span><span><b>JetUP is the association.</b> It trains and organises the passengers.</span></li>
    </ul>
   </div>
  </div>
  <div class="block">{sonic_card()}</div>
 </div>
</section>

<section class="sec" id="split" aria-labelledby="split-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="shead"><p class="eyebrow rv">Where the money comes from</p><h2 class="h2 rv" style="--d:1" id="split-h">From every profit, <span class="grad">70% is yours.</span></h2>
   <p class="lede rv" style="--d:2">When the strategy makes a profit, you keep 70%. The other 30% is the performance fee: it pays the broker, the strategy provider and the partner program. Drag the slider and watch it split.</p></div>
  <div class="rv" style="max-width:980px;margin:0 auto 28px">{laptop('split', 'Where every profit goes, in 2:16')}</div>
  <div class="card pad split rv">
   <div>
    <label for="split-range" class="small" style="font-weight:800">If Sonic AI makes a profit of</label>
    <p class="amt" id="split-amt" aria-live="polite">$10</p>
    <input class="range" id="split-range" type="range" min="1" max="1000" step="1" value="10" aria-label="Profit in US dollars">
    <p class="small" style="margin:0">Move it, or use the arrow keys. Example only, not a forecast.</p>
   </div>
   <div class="bars">
    <div class="bar you"><div class="lab"><span>You keep 70%</span><span class="up" id="split-you">$7.00</span></div><div class="trk"><div class="fill" id="fill-you" style="width:70%"></div></div></div>
    <div class="bar cut"><div class="lab"><span>Performance fee 30%</span><span id="split-fee">$3.00</span></div><div class="trk"><div class="fill" id="fill-fee" style="width:30%"></div></div>
     <div class="fee-who"><span class="chip">Broker</span><span class="chip">Strategy provider</span><span class="chip">Partner program</span></div></div>
    <p class="call ok" style="margin:4px 0 0">{icon('i-shield2')}<span><b>And on a losing trade?</b> No performance fee at all. You only share when there is a profit.</span></p>
   </div>
  </div>
  <p class="center rv" style="margin-top:22px"><a class="btn btn-ghost" href="/jetup/tools/profit-split-calculator/">{icon('i-split')}Try the Profit Split Calculator</a></p>
 </div>
</section>

<section class="sec" id="plan" aria-labelledby="plan-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="shead"><p class="eyebrow rv">The money plan in the training</p><h2 class="h2 rv" style="--d:1" id="plan-h">$155 in. <span class="grad">$6,000 of exposure.</span></h2>
   <p class="lede rv" style="--d:2">Here's what happens to the deposit in the sign-up training, line by line. And here's the twist most people miss: exposure is the size you trade with, not money you own.</p></div>
  <div class="rv" style="max-width:980px;margin:0 auto 28px">{laptop('amplify', 'Amplify 24x made simple, in 2:13')}</div>
  <div class="grid2" style="align-items:start">
   <div class="card ticket rv" data-in>
    <div class="tk-head"><span>Order ticket</span><b>Sonic AI · Amplify 24x</b></div>
    <div class="tk-row rv-row" style="transition-delay:.05s"><span class="tki" aria-hidden="true">💵</span><p>You deposit<small>Your own money, in USDT or USDC</small></p><span class="v">$155</span></div>
    <div class="tk-row rv-row" style="transition-delay:.2s"><span class="tki" aria-hidden="true">🤖</span><p>Into the Sonic AI strategy<small>$50 × 24 = $1,200 of exposure</small></p><span class="v">$50</span></div>
    <div class="tk-row rv-row" style="transition-delay:.35s"><span class="tki" aria-hidden="true">⏳</span><p>Stays in your balance<small>For the Dennis Fast Start Promo</small></p><span class="v">$100</span></div>
    <div class="tk-row rv-row" style="transition-delay:.5s"><span class="tki" aria-hidden="true">🎁</span><p>The promo adds a bonus<small>$200 × 24 = $4,800 of exposure</small></p><span class="v up">+$100</span></div>
    <div class="tk-row rv-row" style="transition-delay:.65s"><span class="tki" aria-hidden="true">🪙</span><p>A few dollars spare<small>For small differences and fees</small></p><span class="v">$5</span></div>
    <div class="tk-row total rv-row" style="transition-delay:.8s"><span class="tki" aria-hidden="true">📈</span><p>Total exposure<small>$1,200 + $4,800</small></p><span class="v" data-count="6000" data-pre="$">$6,000</span></div>
    <p class="tk-foot">Exposure is the size you trade with, not money you own. Your own money in this plan is $150 (plus $5 spare).</p>
   </div>
   <div class="stack">
    <div class="card pad rv" style="--d:1">
     <h3 class="h3">In everyday terms: a market stall 🛒</h3>
     <p class="small" style="margin:8px 0 0;line-height:1.7;color:var(--body)">You pay for one stall, but Amplify lets you trade as if you had 24 stalls. Every move is 24 times bigger, in both directions.</p>
    </div>
    <p class="call info rv" style="--d:2">{icon('i-info2')}<span><b>Good to know:</b> a built-in loss limit closes the account if the trader's loss passes 10% of the starting balance (5% with a community token), so you always know the line in advance.</span></p>
    <a class="btn btn-lime rv" style="--d:4" href="/jetup/tools/exposure-calculator/">{icon('i-candle2')}See it in the Exposure Calculator</a>
   </div>
  </div>
 </div>
</section>

<section class="sec" id="checks" aria-labelledby="checks-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="shead"><p class="eyebrow rv">Burned before? Start here</p><h2 class="h2 rv" style="--d:1" id="checks-h">5 checks you can <span class="grad">do yourself.</span></h2>
   <p class="lede rv" style="--d:2">I'm not going to tell you this one is different. You've heard that line before. Here are five checks instead, so whatever you decide, you decide with your eyes open. Tick each one as you check it.</p></div>
  <div class="checks" data-ticks="checks">{chk_html}</div>
  <div class="prog rv"><span class="ring" data-ring="checks"><svg viewBox="0 0 72 72" aria-hidden="true"><circle class="bg" cx="36" cy="36" r="30"/><circle class="fg" cx="36" cy="36" r="30"/></svg><b>0</b></span>
   <p data-msg="of 5 checked. Your ticks stay on this phone only." data-done="All 5 checked. Now you decide with your eyes open. 👏" aria-live="polite">of 5 checked. Your ticks stay on this phone only.</p></div>
  <p class="center rv" style="margin-top:22px"><a class="btn btn-ghost" href="/jetup/five-checks/">{icon('i-search')}See every check, with the sources</a></p>
 </div>
</section>

<section class="sec" id="start" aria-labelledby="start-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="shead"><p class="eyebrow rv">Ready? One tap at a time</p><h2 class="h2 rv" style="--d:1" id="start-h">Six parts. <span class="grad">Every tap shown.</span></h2>
   <p class="lede rv" style="--d:2">Grab your phone and follow along, one tap at a time. In part five, take a moment on the account rules screen: it shows the built-in loss limit.</p></div>
  <div class="grid2" style="align-items:center;gap:clamp(20px,4vw,44px)">
   <div class="rv">{laptop('training', 'The full sign-up training (9:09)')}</div>
   <div class="stack">
    <div class="parts" style="grid-template-columns:minmax(0,1fr)">{parts_html}</div>
   </div>
  </div>
  <p class="center rv" style="margin-top:26px"><a class="btn btn-pri" href="/jetup/get-started/">{icon('i-rocket2')}Open the step-by-step guide</a></p>
 </div>
</section>

<section class="sec tight" id="promo" aria-labelledby="promo-h">
 <div class="narrow"><div class="rv" style="margin:0 0 22px">{laptop('promo', 'The $100 Fast Start Promo, in 2:18')}</div><div class="card lime-edge pad promo rv">
  <span class="hourglass" aria-hidden="true">⏳</span>
  <div><p class="eyebrow">Dennis Fast Start Promo</p><h2 class="h2" style="margin-top:10px;font-size:clamp(1.9rem,4vw,2.8rem)" id="promo-h">A promo is <span class="lime">a promo.</span></h2>
   <ul class="plist">
    <li><span class="e" aria-hidden="true">✅</span>Still running when I made this training</li>
    <li><span class="e" aria-hidden="true">⏳</span>It won't be here forever. Nobody can promise the end date</li>
    <li><span class="e" aria-hidden="true">🚀</span>Decided to start? Start while it's still on</li>
    <li><span class="e" aria-hidden="true">🔎</span>Confirm it on jet-up.ai before you deposit</li>
    <li><span class="e" aria-hidden="true">📤</span>Send this page to someone who's ready</li>
   </ul>
   <p style="margin:18px 0 0"><a class="btn btn-ghost btn-sm" href="/jetup/promo/">{icon('i-gift')}The promo rules in full</a></p></div>
 </div></div>
</section>

<section class="sec" id="explore" aria-labelledby="ex-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="shead"><p class="eyebrow rv">Go deeper</p><h2 class="h2 rv" style="--d:1" id="ex-h">Understand it <span class="grad">before you need it.</span></h2></div>
  <div class="grid3">{explore_html}</div>
 </div>
</section>

<section class="sec tight" id="risk" aria-labelledby="risk-h">
 <div class="narrow"><div class="card lime-edge pad riskbox smart rv">
  <span class="ped lime"><b>{icon('i-shield2')}</b></span>
  <div><p class="eyebrow">Smart start</p><h2 class="h2" style="margin-top:10px;font-size:clamp(1.8rem,3.6vw,2.5rem)" id="risk-h">Know these 4 things, <span class="lime">then go</span></h2>
   <ul>
    <li><span><b>Start small.</b> The plan puts $50 into Sonic AI, so you see how it moves before you add more.</span></li>
    <li><span><b>Every move is 24 times bigger, both ways.</b> That's 24x Amplify. Try it with your own numbers in the <a href="/jetup/tools/exposure-calculator/">Exposure Calculator</a>.</span></li>
    <li><span><b>The loss limit is written down:</b> 10% of the starting balance, 5% with a community token.</span></li>
    <li><span><b>Check the record yourself.</b> Sonic AI's results are public on Myfxbook, and the current rules are in your dashboard.</span></li>
   </ul></div>
 </div></div>
</section>

<section class="sec" id="mtg" aria-labelledby="mtg-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap mtg">
  <div class="photo rv"><img src="/jetup/img/mtg-photo-800.webp?v=2" width="800" height="800" alt="MTG, Your Digital Architect, in a navy blazer and white t-shirt, in a glass office above the city skyline" loading="lazy"></div>
  <div class="rv" style="--d:1">
   <p class="eyebrow">Your guide</p>
   <h2 class="h2" style="margin-top:12px" id="mtg-h">Hi, I'm <span class="mtg-gold">MTG,</span> Your Digital Architect.</h2>
   <p class="lede" style="margin-top:16px">I teach the way I'd want to be taught: one step at a time, shown on screen, with the costs and the risks in plain sight. I'm not JetUP and I'm not TAG Markets. I show you what I found, where I found it, and how to check it yourself.</p>
   <p class="lede" style="margin-top:12px">Take your time. You can pause any step and follow along with me. And once you understand it, you can help someone else learn it too. We learn best when we teach others.</p>
   <p class="sig mtg-gold">Crypto-Regards, MTG</p>
   <p class="small" style="margin:6px 0 0;font-weight:700">It pays to pay attention, and take action.</p>
  </div>
 </div>
</section>

<section class="sec tight" id="faq" aria-labelledby="faq-h">
 <div class="narrow">
  <div class="shead"><p class="eyebrow rv">Straight answers</p><h2 class="h2 rv" style="--d:1" id="faq-h">JetUP and <span class="grad">TAG Markets</span> questions</h2></div>
  <div class="faq">{faq_html}</div>
  <p class="center rv" style="margin-top:22px"><a class="btn btn-ghost btn-sm" href="/jetup/faq/">{icon('i-help')}All questions and answers</a></p>
 </div>
</section>
{tribe_cta()}
'''
    crumbs_l = [('MTG TRIBE', '/'), ('Dashboard', '/dashboard/'), ('JetUP and TAG Markets', None)]
    ld = [ld_faq(HOME_FAQ, SITE + path), ld_video('5checks'), ld_video('training'), ld_video('sonic'), ld_video('simple'), ld_video('who'), ld_video('promo'), ld_video('split'), ld_video('amplify')]
    ld[1]['@id'] = SITE + path + '#video-5-checks'
    ld[2]['@id'] = SITE + path + '#video-training'
    return page(path, 'JetUP and TAG Markets Guide: Check First, Then Start | MTG',
                "MTG's plain-English JetUP and TAG Markets guide: who holds your money, how TAG Markets copy trading with Sonic AI works, the 70/30 split, 24x Amplify, the risks and every sign-up step.",
                main, crumbs_l, ld, docked=False, og_img='/jetup/img/cover-5-checks-v5-3.jpg', og_alt='Lost money before? Check these 5 things before you try again. JetUP and TAG Markets guide by MTG')
