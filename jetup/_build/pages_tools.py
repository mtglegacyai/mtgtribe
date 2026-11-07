# Tools and library pages: two calculators (each on its own page), videos, downloads, FAQ, disclaimer
from layout import *
from urllib.parse import quote

def field(i, label, sub, val, pre='$', suf='', mode='decimal', step=None):
    p = '<span>%s</span>' % pre if pre else ''
    s = '<span class="suf">%s</span>' % suf if suf else ''
    return f'''<div class="field"><label for="{i}">{label}<small>{sub}</small></label>
 <div class="inp">{p}<input id="{i}" name="{i}" type="text" inputmode="{mode}" autocomplete="off" value="{val}" aria-describedby="{i}-err">{s}</div>
 <p class="err" id="{i}-err" aria-live="polite"></p></div>'''

def res(i, label, sub, cls=''):
    return f'<div class="res {cls}" data-ok><p>{label}<small>{sub}</small></p><span class="v" id="{i}" aria-live="polite">...</span></div>'

def build_exposure():
    path = '/jetup/tools/exposure-calculator/'
    main = f'''
{phead('i-candle2', 'Tool', 'Exposure <span class="grad">Calculator</span>',
       'Type your own money, any bonus and the Amplify multiplier, then drag a price move. See the exposure, the profit or loss, and what that move means for your own money.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Exposure Calculator', None)], ped='lime')}
<section class="sec tight" style="padding-top:0"><div class="wrap toolgrid">
 <form class="card pad" id="exp-form" novalidate aria-label="Exposure Calculator inputs">
  <p class="eyebrow" style="margin-bottom:12px">Start from an example</p>
  <div class="seg" role="group" aria-label="Examples" style="margin-bottom:20px">
   <button type="button" data-preset="150,100,24" aria-pressed="true">Training: $150 + $100</button>
   <button type="button" data-preset="50,0,24" aria-pressed="false">Sonic only: $50</button>
   <button type="button" data-preset="100,100,24" aria-pressed="false">Promo: $100 + $100</button>
  </div>
  {field('exp-own', 'Your own money in the account', 'What you deposited yourself', '150')}
  {field('exp-bonus', 'Bonus added', 'For example the $100 promo bonus. Type 0 if none', '100')}
  {field('exp-mult', 'Amplify multiplier', "JetUP's Sonic AI Amplify account uses 24x", '24', pre='', suf='x', mode='numeric')}
  <div class="field"><label for="exp-move">Price move on the trading balance<small>Drag left for a move against you, right for a move your way</small></label>
   <input class="range" id="exp-move" type="range" min="-10" max="10" step="0.1" value="-1">
   <p style="margin:0;font:700 1.5rem/1 var(--f-m)" id="exp-move-out" class="mono down">-1.0%</p></div>
  <button type="button" class="btn btn-ghost btn-sm reset" id="exp-reset">{icon('i-refresh2')}Reset</button>
 </form>
 <div class="stack">
  <div class="out" aria-label="Results">
   {res('exp-bal', 'Account balance', 'Your money plus the bonus')}
   {res('exp-ex', 'Trading exposure', 'Balance × multiplier. Not money you own', 'big')}
   {res('exp-pl', 'Profit or loss from this move', 'Exposure × the move, before costs')}
   {res('exp-ofown', 'As a share of your own money', 'How hard this move hits what you put in')}
   {res('exp-eqown', 'Move that equals all your own money', 'Your money ÷ exposure')}
   {res('exp-eqbal', 'Move that equals the whole balance', '100% ÷ multiplier')}
  </div>
  <div class="card pad" data-ok>
   <p class="small" style="margin:0;font-weight:800;color:var(--text)">Loss meter: share of your own money</p>
   <div class="meter" aria-hidden="true"><i id="exp-needle"></i></div><div class="meter-x" aria-hidden="true"><span>0%</span><span>50%</span><span>100%</span></div>
   <p class="small" id="exp-meter-t" style="margin:10px 0 0;color:var(--body)" aria-live="polite"></p>
  </div>
  <p class="how" id="exp-how" data-ok aria-label="How it was calculated"></p>
  <p class="call warn">{icon('i-alert')}<span><b>TAG Markets' rule:</b> if the trader loses more than 10% of the starting balance, the account is liquidated (closed). With a community token, 5%. This calculator shows the maths of exposure only. TAG Markets' own rules decide what happens to your account.</span></p>
  <p class="small" style="margin:0">Illustration, not a forecast. It leaves out spreads, swaps, fees and how CopyX sizes each trade. Education only, not financial advice.</p>
 </div>
</div></section>
<section class="sec tight"><div class="narrow"><div class="card pad prose rv">
 <h2>How to read it</h2>
 <p><b>Exposure</b> is the size you trade with. With the training example, $250 × 24 = $6,000. A 1% move on $6,000 is $60, which is 40% of your own $150.</p>
 <p>The <b>move that equals all your own money</b> is $150 ÷ $6,000 = 2.5%. The <b>move that equals the whole balance</b> is 100% ÷ 24 = 4.17%, which is why the training says a drop of about 4.2% is the same size as your whole deposit.</p>
 <p>Want the other side, the profit split? Try the <a href="/jetup/tools/profit-split-calculator/">Profit Split Calculator</a>.</p>
</div></div></section>
{join_cta()}'''
    app = {"@type": "WebApplication", "name": "Exposure Calculator (JetUP and TAG Markets Amplify)", "url": SITE + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    return page(path, 'Exposure Calculator: 24x Amplify on TAG Markets | MTG',
                'Free Exposure Calculator for JetUP and TAG Markets: see what 24x Amplify does to a deposit, the profit or loss from a price move, and the move that equals all your own money.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Exposure Calculator', None)], [app],
                keywords='Exposure Calculator, Amplify calculator, TAG Markets Amplify, JetUp 24x, leverage calculator, copy trading risk, MTG TRIBE')

def build_split():
    path = '/jetup/tools/profit-split-calculator/'
    main = f'''
{phead('i-split', 'Tool', 'Profit Split <span class="grad">Calculator</span>',
       'Type the amount in the strategy and the strategy result. See your 70%, the 30% performance fee, and what happens when the result is a loss.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Profit Split Calculator', None)], ped='lime')}
<section class="sec tight" style="padding-top:0"><div class="wrap toolgrid">
 <form class="card pad" id="ps-form" novalidate aria-label="Profit Split Calculator inputs">
  <p class="eyebrow" style="margin-bottom:12px">Start from an example</p>
  <div class="seg" role="group" aria-label="Examples" style="margin-bottom:20px">
   <button type="button" data-preset="50,30.1" aria-pressed="true">Myfxbook: +30.1%</button>
   <button type="button" data-preset="10,100" aria-pressed="false">$10 profit</button>
   <button type="button" data-preset="50,-10" aria-pressed="false">A loss: -10%</button>
  </div>
  {field('ps-amt', 'Amount in the strategy', 'For example the $50 in the training', '50')}
  {field('ps-pct', 'Strategy result, gross', 'Before the split. Use a minus sign for a loss', '30.1', pre='', suf='%')}
  <button type="button" class="btn btn-ghost btn-sm reset" id="ps-reset">{icon('i-refresh2')}Reset</button>
 </form>
 <div class="stack">
  <div class="out" aria-label="Results">
   {res('ps-gross', 'Strategy result', 'Amount × result')}
   {res('ps-you', 'Your share', 'Profit × 70%. A loss is all yours', 'big')}
   {res('ps-fee', 'Performance fee', 'Profit × 30%. $0 on a loss')}
   {res('ps-net', 'Your return', 'Result × 70% on a profit')}
   {res('ps-end', 'Your amount afterwards', 'Amount + your share')}
  </div>
  <p class="call info" data-ok>{icon('i-info2')}<span id="ps-note" aria-live="polite"></span></p>
  <p class="how" id="ps-how" data-ok aria-label="How it was calculated"></p>
  <p class="small" style="margin:0">Illustration, not a forecast. The +30.1% is Sonic AI's published Myfxbook result from 3 Nov 2024 to 4 Oct 2026, gross. Past results never promise future ones. It leaves out network and exchange fees. Education only, not financial advice.</p>
 </div>
</div></section>
<section class="sec tight"><div class="narrow"><div class="card pad prose rv">
 <h2>Where the 30% goes</h2>
 <p>The 30% performance fee pays the broker, the strategy provider and the partner program, and it is taken from profits only. JetUP's one-pager says the Profit Share to partners comes out of this 30%, never from client deposits.</p>
 <p>Curious what Amplify does to the same money? Try the <a href="/jetup/tools/exposure-calculator/">Exposure Calculator</a>.</p>
</div></div></section>
{join_cta()}'''
    app = {"@type": "WebApplication", "name": "Profit Split Calculator (JetUP and TAG Markets 70/30)", "url": SITE + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    return page(path, 'Profit Split Calculator: the 70/30 on TAG Markets CopyX | MTG',
                'Free Profit Split Calculator for JetUP and TAG Markets CopyX: see your 70% of a Sonic AI profit, the 30% performance fee, your return, and why a loss carries no fee.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Profit Split Calculator', None)], [app],
                keywords='profit split calculator, 70/30, TAG Markets CopyX, Sonic AI, performance fee, JetUp, MTG TRIBE')

def build_videos():
    path = '/jetup/videos/'
    main = f'''
{phead('i-film2', 'Library', 'JetUP and TAG Markets <span class="grad">videos</span>',
       'Watch first, then do. Every video opens on its own cover, plays in its own frame and closes itself when it ends.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Videos', None)])}
<section class="sec tight" style="padding-top:0"><div class="wrap stack" style="gap:30px">
 <div class="grid2" style="align-items:start">
  <div class="rv"><p class="eyebrow" style="margin-bottom:14px">1 · Watch first</p>{laptop('5checks', 'JetUP 5 Checks, by MTG (5:25)')}<p class="small center" style="margin:8px 0 0">Lost money before? Five things to check before you try again.</p></div>
  <div class="rv" style="--d:1"><p class="eyebrow" style="margin-bottom:14px">2 · Then do</p>{laptop('training', 'Sign-up training, by MTG (9:09)')}<p class="small center" style="margin:8px 0 0">Every tap: sign up, KYC, deposit, Sonic AI and the $100 promo.</p></div>
 </div>
 <div class="block rv" id="step-by-step">
  <p class="eyebrow" style="margin-bottom:6px">3 · Step by step, one part at a time</p>
  <p class="small" style="margin:0 0 16px">MTG's own phone recordings, tap by tap, with every personal detail hidden. The written steps for each part are on <a href="/jetup/get-started/#videos">Get started</a>.</p>
  <div class="vlist"><div class="vpart">{phone('tut1')}<b>Part 1</b><small>Create your JetUP account</small></div>
   <div class="vpart">{phone('tut2')}<b>Part 2</b><small>Link JetUP to TAG Markets</small></div>
   <div class="vsoon"><b>Parts 3 to 6</b><small>KYC, deposit, Sonic AI and the promo: coming next.</small></div></div>
 </div>
 <div class="card pad rv vrow" id="profit-share">
  <div>{phone('profitshare')}</div>
  <div><p class="eyebrow">4 · JetUP's own explainer</p><h2 class="h2" style="margin:10px 0 12px;font-size:clamp(1.7rem,3.4vw,2.3rem)">Profit Share explained</h2>
   <p class="lede">JetUP's official 74-second video on the 1.5% Profit Share across 10 levels. Read it with the <a href="/jetup/partner-plan/">partner plan rules</a>: what a partner earns can be zero.</p></div>
 </div>
 <p class="call info rv">{icon('i-info2')}<span>More short explainers are on the way, built from these pages. Follow <a href="{YT}" target="_blank" rel="noopener">YouTube @mtgtribe</a> or <a href="{TT}" target="_blank" rel="noopener">TikTok @joinmtgtribe</a> so the next one finds you first.</span></p>
</div></section>
{tribe_cta()}'''
    return page(path, 'JetUP and TAG Markets Videos: Trainings by MTG | MTG',
                'Watch the JetUP and TAG Markets videos: the 5 checks before you start, the sign-up training with Sonic AI and the Dennis promo, MTG\'s step-by-step phone videos (create your JetUP account, link TAG Markets) and JetUP\'s own Profit Share explainer.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Videos', None)], [ld_video('5checks'), ld_video('training'), ld_video('tut1'), ld_video('tut2'), ld_video('profitshare')])

DOWNLOADS = [
 ('jetup-tag-markets-onboarding-guide.pdf', 'pdf', 'JetUP + TAG Markets Onboarding Guide', 'The 21-page step-by-step guide with annotated screenshots: sign-up, CopyX, KYC, the deposit, Sonic AI, the community codes and the Dennis promo. Personal details are hidden.', '10.2 MB'),
 ('jetup-business-plan-oct-2026.pdf', 'pdf', 'JetUP Business Plan (Oct 2026)', "JetUP's official 14-page plan: the three pillars, the 70/30 split, the four incomes and the rewards.", '3.6 MB'),
 ('jetup-how-partners-grow-one-pager.pdf', 'pdf', 'How Partners Grow (one page)', "JetUP's one-pager: the Dennis promo, 70/30, the four incomes and its risk warning.", '0.4 MB'),
 ('bix-card-setup-and-funding-guide.pdf', 'pdf', 'BIX Card Setup and Funding Guide', 'Install, verify, fund, order a card and link BIX to the JetUP portal. 16 pages.', '2.8 MB'),
 ('jetup-full-presentation.pdf', 'pdf', 'JetUP Full Presentation', "JetUP's complete 33-slide deck.", '8.8 MB'),
 ('jetup-partner-presentation.pdf', 'pdf', 'JetUP Partner Presentation', "JetUP's 21-slide deck for partners.", '8.0 MB'),
 ('jetup-product-presentation.pdf', 'pdf', 'JetUP Product Presentation', "JetUP's 21-slide product deck.", '1.2 MB'),
]

def build_downloads():
    path = '/jetup/downloads/'
    rows = ''.join(f'''<article class="card dl rv" style="--d:{i % 3}"><span class="ft">PDF</span><div><h3>{t}</h3><p>{d} {s}.</p></div>
 <a class="btn btn-ghost btn-sm" href="/jetup/downloads/{f}" download>{icon('i-dl2')}Download</a></article>''' for i, (f, k, t, d, s) in enumerate(DOWNLOADS))
    vids = [('5checks', 'JetUP 5 Checks, by MTG', '5:25 · 1080p · 82 MB', 'jetup-5-checks-mtg-v5.mp4'), ('training', 'Sign-up training, by MTG', '9:09 · 1080p · 45 MB', 'jetup-tag-markets-signup-training-mtg.mp4'), ('profitshare', "Profit Share explained (JetUP's own)", '1:14 · vertical · 9 MB', 'jetup-profit-share-explained.mp4')]
    vrows = ''.join(f'''<article class="card dl rv" style="--d:{i}"><span class="ft mp4">MP4</span><div><h3>{t}</h3><p>{m}</p></div>
 <a class="btn btn-ghost btn-sm" href="/jetup/media/{f}" download>{icon('i-dl2')}Download</a></article>''' for i, (k, t, m, f) in enumerate(vids))
    share = "Lost money before? Check these 5 things before you try JetUP and TAG Markets, then follow the training one tap at a time: https://mtgtribe.com/jetup/"
    main = f'''
{phead('i-dl2', 'Library', 'Downloads: <span class="grad">guides, decks and videos</span>',
       'Everything worth keeping, in one place. Save it, read it offline and share it with someone who is ready to learn.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Downloads', None)])}
<section class="sec tight" style="padding-top:0"><div class="narrow stack">
 <p class="call warn rv">{icon('i-alert')}<span><b>Read the official decks with care.</b> They are JetUP's own marketing material, and some of their figures (for example "up to 1% to 1.5% daily trading profit") are JetUP's claims, not promises. Next to any number, remember: {RETAIL_LOSS} of retail CFD accounts lose money (TAG Markets), 24x Amplify makes losses bigger too, and the account is closed at a 10% loss (5% with a community token).</span></p>
 <p class="eyebrow rv" style="margin-top:10px">Guides and decks</p>
 {rows}
 <p class="eyebrow rv" style="margin-top:18px">Videos</p>
 {vrows}
 <div class="card pad rv" style="margin-top:10px"><p class="eyebrow">Share kit</p><p class="lede" style="margin:12px 0">{share}</p>
  <div class="ctas"><button type="button" class="btn btn-lime btn-sm" data-copy="{share}">{icon('i-copy2')}Copy the message</button><a class="btn btn-ghost btn-sm" href="https://wa.me/?text={quote(share)}" target="_blank" rel="noopener">{icon('i-whatsapp')}Share on WhatsApp</a></div></div>
 <p class="small rv">Coming soon: MTG's own step-by-step PDF guide, made from his own screen recording.</p>
</div></section>
{tribe_cta()}'''
    return page(path, 'JetUP and TAG Markets Downloads: PDF Guides and Videos | MTG',
                'Download the JetUP Business Plan, the How Partners Grow one-pager, the BIX Card setup guide, the official JetUP decks and MTG\'s JetUP and TAG Markets videos.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Downloads', None)])

FAQ = [
 ('Basics', [
  ('What is JetUP?', 'JetUP is a community and partner program with training and AI tools. Its portal is jetup.ibportal.io and its hub is jet-up.ai. JetUP does not trade and does not hold your money.'),
  ('What is TAG Markets?', "TAG Markets is the broker. Its trading company, T.M. Financials Ltd, is licensed in Mauritius by the FSC (licence GB21026474). Your trading account is opened there, in your own name."),
  ('How are JetUP and TAG Markets linked?', 'JetUP says on its own website that its trading accounts and transactions run through T.M. Financials Ltd, trading as TAG Markets. You create your TAG Markets account by tapping Register CopyX inside the JetUP portal (after the sync the button says Login to CopyX), so the two are linked.'),
  ('What are CopyX and Sonic AI?', "CopyX is TAG Markets' copy trading platform. Sonic AI is the strategy members connect: it trades gold (XAU/USD), and its track record is published on Myfxbook."),
 ]),
 ('Money', [
  ('How much do I need to start?', "The training uses $155 in USDT or USDC: $50 into Sonic AI, $100 left in your balance for the Dennis promo, and a few dollars spare. Keep a little extra on the exchange for the network fee. Only use money you can afford to lose."),
  ('Which network should I use for the TAG Markets deposit?', 'In this order: USDT on BEP20 (BNB Smart Chain) first, USDT on TRC20 (Tron) second, and USDC on ERC20 (Ethereum) if you prefer it, which is the most expensive. Use the same network on both sides: the wrong network means lost funds.'),
  ('Which exchange or wallet should I use?', "VALR first, Binance second, or a Web3 wallet such as SafePal or MetaMask. The VALR and Binance buttons on this site are MTG's referral links."),
  ('How is profit split?', 'When the strategy makes a profit, 70% is yours and 30% is the performance fee, which pays the broker, the strategy provider and the partner program. There is no performance fee on a loss, and no management or join fee.'),
  ('How do withdrawals work?', "Profits can be withdrawn any time, through the broker. JetUP's one-pager says withdrawals take about 48 hours on average. With the Dennis promo, taking your own money out before 12 months ends the promo. Test a small withdrawal early."),
 ]),
 ('After you join', [
  ('How do I see my trades?', "Install MetaTrader 5 (MT5), add an account and search for TM Financials, the company behind TAG Markets. Log in with your account number and investor password from CopyX, Follower Hub, Strategies (tap the eye icon). It is read only: you can watch every trade, not change anything. Sonic usually trades two or three times a day. Steps: mtgtribe.com/jetup/get-started/#mt5"),
  ('Can I open another strategy later?', "Yes. Deposit in TAG Markets, open CopyX, connect SONIC with the new amount and enter the two community codes again. Each one becomes its own account with the same rules. The Dennis Fast Start Promo is one time only, so a new strategy does not get another $100."),
  ('How do I withdraw my partner earnings?', "In the JetUP portal open your Wallet, tap Withdraw and choose your TAG wallet or one of your MT5 accounts. To send money out, add your own crypto wallet address under Wallets first. Start with a small withdrawal."),
  ('Do I have to buy the BIX Card to link BIX?', "No. Linking your BixPay wallet to the JetUP portal moves no money and costs nothing. It records your place in the team for BIX Card commissions. You can link it with a phone only: screenshot the QR code, then use Load from gallery in BixPay."),
 ]),
 ('Risk', [
  ('Can I lose money with JetUP and TAG Markets?', "Yes. Forex, CFDs and copy trading are high risk, and with 24x Amplify the swings are bigger in both directions. You can lose your whole deposit. TAG Markets' own reminder says " + RETAIL_LOSS + " of retail investor accounts lose money when trading CFDs."),
  ('What is Amplify 24x?', 'Amplify lets the account trade at 24 times its size: $50 trades like $1,200. That is exposure, the size you trade with, not money you own. A drop of about 4.2% on the trading balance is the same size as the whole account.'),
  ('When is an account closed (liquidated)?', "TAG Markets' screen says: if the trader loses more than 10% of the starting balance, your account will be liquidated. With a community token, that limit becomes 5%."),
  ('Is JetUP a scam?', "I can't answer that for you, and nobody honest can promise it either way. What you can do is check: your account is in your own name at a licensed broker, the strategy's results are public, the rules are written down, and some regulators have published warnings. The 5 checks show you where to look."),
 ]),
 ('Promo and partners', [
  ('What is the Dennis Fast Start Promo?', 'For new partners, once: your own $100 plus a $100 bonus open a Sonic AI account that trades as $4,800 with 24x Amplify. Profits can be withdrawn any time, the bonus is released after 12 months, and taking your own money out before then ends the promo. Rules can change.'),
  ('What are the community token codes?', 'In part 5, after you type 50 in Investment, tap the arrow next to Community Token. Enter #9M and tap Verify, then 9MPromo and tap Submit. Both are case sensitive. With a community token, the loss limit becomes 5%.'),
  ('Do I have to build a team?', "No. You can use it as a client only. JetUP's partner plan pays partners who build a team, and JetUP's own founder says the big money comes from building a team. What a partner earns can be zero."),
  ("Where do I get MTG's Partner link?", 'Message MTG on WhatsApp from the sign-up training page, or ask in the MTG TRIBE group at mtgtribe.com/group.'),
 ]),
]

def build_faq():
    path = '/jetup/faq/'
    allqa = [qa for _, g in FAQ for qa in g]
    blocks = ''.join('<div class="block rv"><p class="eyebrow" style="margin-bottom:14px">%s</p><div class="faq">%s</div></div>' % (
        name, ''.join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in g)) for name, g in FAQ)
    main = f'''
{phead('i-help', 'Straight answers', 'JetUP and TAG Markets <span class="grad">FAQ</span>',
       'The questions people ask before they start, answered plainly, with the risks left in.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('FAQ', None)])}
<section class="sec tight" style="padding-top:0"><div class="narrow">{blocks}
 <div class="card pad block rv center" style="display:grid;justify-items:center;gap:12px"><h2 class="h2" style="font-size:clamp(1.7rem,3.4vw,2.3rem)">Still have a question?</h2><p class="lede">Ask in the MTG TRIBE. The question most of you ask becomes the next video.</p><a class="btn btn-lime" href="{GROUP}">{icon('i-whatsapp')}Ask the tribe</a></div>
</div></section>
{join_cta()}'''
    return page(path, 'JetUP and TAG Markets FAQ: Deposits, Risks, Promo | MTG',
                'JetUP and TAG Markets questions answered: what they are, how much to start, BEP20 or TRC20, the 70/30 split, withdrawals, 24x Amplify, liquidation, the Dennis promo and the community codes.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('FAQ', None)], [ld_faq(allqa, SITE + path)])

def build_disclaimer():
    path = '/jetup/disclaimer/'
    main = f'''
{phead('i-info2', 'Please read', 'Disclaimer', 'The small print, in plain English.', [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Disclaimer', None)])}
<section class="sec tight" style="padding-top:0"><div class="narrow"><div class="card pad prose rv">
 <h2>Independent, education only</h2>
 <p>This is an independent guide by MTG. It is not official JetUP, TAG Markets, CopyX, Sonic AI or BIX material, and none of these companies has reviewed it. It is education only, not financial, investment, tax or legal advice. Always do your own research.</p>
 <h2>Trading is high risk</h2>
 <p>Trading forex and CFDs, and copy trading, carries a high risk of loss. You can lose all the money you deposit. Leverage and Amplify make losses bigger, and TAG Markets' own reminder says {RETAIL_LOSS} of retail investor accounts lose money when trading CFDs. Past results never guarantee future results. There is no fixed, daily or guaranteed return, and what a partner earns can be zero.</p>
 <h2>Figures and screens</h2>
 <p>Figures from JetUP's Business Plan and one-pager are JetUP's own, as of 4 October 2026. The Sonic AI result is the published Myfxbook figure for 3 November 2024 to 4 October 2026. Promos, fees, screens and rules change: check the current terms in your own dashboard before you act. Personal details in every screenshot are hidden.</p>
 <h2>Links</h2>
 <p>The VALR and Binance buttons are MTG's referral links. If you sign up through them, MTG may receive a reward, at no extra cost to you. Other links go to official websites.</p>
 <p>Questions? Message MTG on <a href="{WA_MTG}" target="_blank" rel="noopener">WhatsApp</a> (messages and voice notes, no calls).</p>
</div></div></section>'''
    return page(path, 'Disclaimer: JetUP and TAG Markets Guide | MTG',
                'Disclaimer for MTG\'s independent JetUP and TAG Markets guide: education only, not financial advice, trading is high risk, figures and screens change, and which links are referral links.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Disclaimer', None)])

def build_glossary():
    # every word the guide uses, explained in one or two plain sentences (MTG, 7 Nov 2026)
    from extras import GLOSSARY
    rows = ''.join(
        '<div class="gterm" id="g-%s"><h2>%s</h2><p>%s</p><a class="gmore" href="%s">See it explained %s</a></div>' % (
            k, name, d, more, icon('i-arrow2')) for k, name, pat, d, more in sorted(GLOSSARY, key=lambda g: g[1].lower()))
    path = '/jetup/glossary/'
    main = f'''
{phead('i-book', 'Every word, explained', 'The JetUP and TAG Markets <span class="grad">glossary</span>',
       'The words you will meet in this guide, in plain English. Tap any underlined word on the other pages to see its meaning right there.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Glossary', None)])}
<section class="sec tight" style="padding-top:0"><div class="narrow"><div class="card pad rv glist">{rows}</div></div></section>
{tribe_cta()}'''
    return page(path, 'JetUP and TAG Markets Glossary: CFD, KYC, Amplify, XAU/USD | MTG',
                'Plain English meanings of the words in the JetUP and TAG Markets guide: Amplify, exposure, CFD, KYC, CU number, community token, CopyX, Sonic AI, XAU/USD, MT5, network, performance fee and more.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Glossary', None)])
