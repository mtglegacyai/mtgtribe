# Learning pages: 5 checks, how it works, partner plan, promo, BIX Card
from layout import *

def section(i, eyebrow, title, body, ic='i-info2', ped=''):
    return f'''<article class="card pad rv" id="{i}" style="scroll-margin-top:90px">
 <div class="srow"><span class="ped {ped}"><b>{icon(ic)}</b></span><div class="sbody">
 <p class="eyebrow">{eyebrow}</p><h2 class="h2" style="margin:10px 0 14px;font-size:clamp(1.7rem,3.6vw,2.4rem)">{title}</h2>
 <div class="prose">{body}</div></div></div>
</article>'''

def build_checks():
    path = '/jetup/five-checks/'
    tick = lambda n: '<button type="button" class="tick" data-id="c%s" aria-pressed="false" style="margin-top:6px"><span class="bx">%s</span>I checked this</button>' % (n, icon('i-check2'))
    c1 = section('check-1', 'Check 1 of 5', 'Who holds my money?', f'''
<p>Your deposit goes into an <b>MT5 account at TAG Markets, in your own name</b>. MT5 means MetaTrader 5, the trading app many brokers use. JetUP is the community: it does not trade, and it does not take your money.</p>
<p><b>Check it yourself:</b> don't take my word for it. Log in at portal.tagmarkets.com and see your own balance.</p>
<div class="call info">{icon('i-search')}<p>JetUP's own one-pager says: your money does not sit with JetUP, it sits in your own account at TAG Markets.</p></div>
<div data-ticks="checks">{tick(1)}</div>''', 'i-wallet2')
    c2 = section('check-2', 'Check 2 of 5', 'Who regulates the broker?', f'''
<div class="grid2" style="margin-bottom:14px">
 <div class="card pad" style="background:rgba(255,255,255,.03)"><p class="eyebrow">Licence 1 · Mauritius</p><p style="margin:10px 0 0"><b>T.M. Financials Ltd</b>, TAG Markets' trading company. Licensed by the <b>FSC</b> (Financial Services Commission, the Mauritius regulator), licence <b>GB21026474</b>.</p></div>
 <div class="card pad" style="background:rgba(255,255,255,.03)"><p class="eyebrow">Licence 2 · South Africa</p><p style="margin:10px 0 0"><b>TM Financials SA (Pty) Ltd</b>, authorised by the <b>FSCA</b> (Financial Sector Conduct Authority, our regulator), <b>FSP number 55237</b>.</p></div>
</div>
<p><b>Read the fine print.</b> TAG's own website says the South African company provides marketing services, and that trading accounts are held by the Mauritius company. So know which regulator covers your account.</p>
<div class="call warn">{icon('i-alert')}<p><b>Published regulator warnings.</b> Regulators in Austria (FMA), Luxembourg (CSSF), Slovenia (ATVP), Russia (Central Bank) and Quebec, Canada (AMF) have published warnings that TAG Markets is not authorised in their countries. I'm telling you this because you deserve the whole picture.</p></div>
<h3>Check it yourself</h3>
<ul>
 <li>FSC Mauritius: search the register of licensees on <a href="https://www.fscmauritius.org/" target="_blank" rel="noopener">fscmauritius.org</a> for licence GB21026474.</li>
 <li>FSCA: on <a href="https://www.fsca.co.za/" target="_blank" rel="noopener">fsca.co.za</a>, go to Regulated Entities and search FSP 55237.</li>
 <li>The global list of regulator warnings, IOSCO I-SCAN: search "TAG Markets" on <a href="https://www.iosco.org/i-scan/" target="_blank" rel="noopener">iosco.org/i-scan</a>.</li>
</ul>
<div data-ticks="checks">{tick(2)}</div>''', 'i-scale2')
    c3 = section('check-3', 'Check 3 of 5', 'Are the results real?', f'''
<p>Sonic AI publishes its track record on <b>Myfxbook</b>, so you can look before you deposit. It trades gold (XAU/USD).</p>
<div class="grid2" style="margin:6px 0 14px">
 <div class="card pad center" style="background:rgba(255,255,255,.03)"><p class="eyebrow" style="justify-content:center">Published result</p><p class="amt up" style="margin:12px 0 6px">+30.1%</p><p class="small" style="margin:0">3 Nov 2024 to 4 Oct 2026. Gross, before the 70/30 split</p></div>
 <div class="card pad center" style="background:rgba(255,255,255,.03)"><p class="eyebrow" style="justify-content:center">Your share</p><p class="amt" style="margin:12px 0 6px">≈ 21%</p><p class="small" style="margin:0">30.1% × 70% = 21.07%, over about 23 months. Not a forecast</p></div>
</div>
<p>So that's about 21% to you over about 23 months. <b>Not 40% a month. Not a fixed return.</b> And past results never guarantee the future.</p>
<p><b>Check it yourself:</b> search "Sonic AI" on <a href="https://www.myfxbook.com/" target="_blank" rel="noopener">myfxbook.com</a> and look at the dates, the growth and the drawdown (the biggest drop).</p>
<div data-ticks="checks">{tick(3)}</div>''', 'i-chart')
    c4 = section('check-4', 'Check 4 of 5 · the one most people skip', 'What can go wrong?', f'''
<div class="grid3" style="margin-bottom:14px">
 <div class="card pad center" style="background:rgba(255,255,255,.03)"><p class="small" style="margin:0">You put in</p><p class="amt" style="margin:8px 0">$150</p><p class="small" style="margin:0">+ $100 promo = $250</p></div>
 <div class="card pad center" style="background:rgba(255,255,255,.03)"><p class="small" style="margin:0">Amplify it</p><p class="amt" style="margin:8px 0">× 24</p><p class="small" style="margin:0">Exposure: the size you trade with</p></div>
 <div class="card pad center" style="background:rgba(255,255,255,.03)"><p class="small" style="margin:0">It trades like</p><p class="amt down" style="margin:8px 0">$6,000</p><p class="small" style="margin:0">Not money you own</p></div>
</div>
<ul>
 <li><b>Bigger exposure means bigger swings, up and down.</b> You can lose your whole deposit.</li>
 <li><b>The loss limit:</b> if the trader loses more than 10% of the starting balance, the account is liquidated (closed). With a community token, 5%.</li>
 <li><b>The broker's insolvency cover is $1,000,000 in total, for all clients together,</b> not per person. Insolvency means the broker itself going bust. Trading losses are not covered.</li>
</ul>
<p><a class="btn btn-lime btn-sm" href="/jetup/tools/exposure-calculator/">{icon('i-candle2')}Try the Exposure Calculator</a></p>
<div data-ticks="checks">{tick(4)}</div>''', 'i-alert', 'red')
    c5 = section('check-5', 'Check 5 of 5', 'Can I get out?', f'''
<ul>
 <li>💵 <b>Profits</b> can be withdrawn any time.</li>
 <li>📅 <b>The promo bonus</b> is released after 12 months.</li>
 <li>⛔ <b>Taking your own money out before 12 months</b> ends the promo.</li>
 <li>📲 Promo amounts change, so <b>check the current rules in your dashboard</b> before you start.</li>
</ul>
<div class="call lime">{icon('i-shield2')}<p><b>My advice?</b> Start small, and do a small withdrawal early. Let the system prove itself to you.</p></div>
<div data-ticks="checks">{tick(5)}</div>''', 'i-door', 'lime')
    why = f'''<div class="card pad rv"><p class="eyebrow">So why would anyone still give this a shot?</p>
<ul class="plist" style="margin-top:14px">
 <li><span class="e" aria-hidden="true">✅</span>Because you can check before you deposit.</li>
 <li><span class="e" aria-hidden="true">✅</span>Because you can start small.</li>
 <li><span class="e" aria-hidden="true">✅</span>Because the account is in your name.</li>
 <li><span class="e" aria-hidden="true">✅</span>Because the company writes down, in its own risk warning, that what a partner earns can be zero. That kind of honesty is worth noticing.</li>
</ul>
<p class="call info" style="margin-top:16px">{icon('i-info2')}<span><b>One more truth, from JetUP's own founder:</b> the big money comes from building a team, not from the trading percentage. Know that going in.</span></p>
<p class="lede" style="margin-top:16px">If you check all five and it still feels right, start small, with money you can afford to lose. And if it doesn't feel right? That's a good decision too.</p></div>'''
    main = f'''
{phead('i-shield2', 'Burned before? Start here', 'The 5 checks <span class="grad">before you try JetUP</span>',
       "If you've lost money in a trading platform, a copy trading app, or a program that promised you the world, this page is for you. You are not foolish for trying. The lesson is not to stop trying. The lesson is to verify first. So let's verify JetUP and TAG Markets, together.",
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('The 5 checks', None)],
       [icon('i-film2') + '5:25 video', icon('i-search') + 'Sources included', icon('i-check2') + 'Tick as you check'])}
<section class="sec tight" style="padding-top:0"><div class="wrap">
 <div style="max-width:980px;margin:0 auto" class="rv">{laptop('5checks', 'Watch the 5 checks (5:25), then tick each one below as you check it', eager=True)}</div>
</div></section>
<section class="sec tight"><div class="narrow stack" style="gap:20px">
 {c1}{c2}{c3}{c4}{c5}
 <div class="prog rv"><span class="ring" data-ring="checks"><svg viewBox="0 0 72 72" aria-hidden="true"><circle class="bg" cx="36" cy="36" r="30"/><circle class="fg" cx="36" cy="36" r="30"/></svg><b>0</b></span>
  <p data-msg="of 5 checked. Your ticks stay on this phone only." data-done="All 5 checked. Now you decide with your eyes open. 👏" aria-live="polite">of 5 checked.</p></div>
 {why}
 <div class="ctas rv" style="justify-content:center"><a class="btn btn-pri" href="/jetup/get-started/">{icon('i-rocket2')}It feels right: show me the steps</a><a class="btn btn-ghost" href="{GROUP}">{icon('i-whatsapp')}I have questions first</a></div>
</div></section>
{tribe_cta('Share this with someone <span class="lime">who got burned.</span>', 'Save this page, so you have the five checks when you need them. We learn best when we teach others. And if you believe in multiple streams of income and learning before you earn, join the MTG TRIBE.')}
'''
    # the five tick boxes live in separate cards: one shared store, so each card gets its own [data-ticks] wrapper with the same key
    crumbs_l = [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('The 5 checks', None)]
    faq = [('Is TAG Markets regulated?', 'TAG Markets\' trading company, T.M. Financials Ltd, holds FSC Mauritius licence GB21026474, and TM Financials SA (Pty) Ltd is FSCA authorised, FSP 55237, for marketing services. Regulators in Austria, Luxembourg, Slovenia, Russia and Quebec have published warnings that TAG Markets is not authorised in their countries.'),
           ('Are Sonic AI results real?', 'Sonic AI publishes its track record on Myfxbook: +30.1% gross from 3 Nov 2024 to 4 Oct 2026. After the 70/30 split that is about 21% to the client over about 23 months. Past results never guarantee the future.'),
           ('What can go wrong with JetUP and TAG Markets?', '24x Amplify makes swings bigger in both directions. You can lose your whole deposit, the account is closed at a 10% loss of the starting balance (5% with a community token), and the insolvency cover is $1,000,000 for all clients together.')]
    return page(path, 'JetUP and TAG Markets Review: 5 Checks Before You Start | MTG',
                'An honest JetUP and TAG Markets review in 5 checks: who holds your money, TAG Markets regulation (FSC, FSCA, warnings), Sonic AI results on Myfxbook, 24x Amplify risk and withdrawals.',
                main, crumbs_l, [ld_video('5checks'), ld_faq(faq, SITE + path)], og_img='/jetup/img/cover-5-checks-v5-3.jpg', og_alt='Lost money before? Check these 5 things before you try again')

def build_how():
    path = '/jetup/how-it-works/'
    main = f'''
{phead('i-layers2', 'How it works', 'How JetUP and TAG Markets <span class="grad">fit together</span>',
       'One picture at a time: who holds what, how copy trading works, where the 70/30 split goes, what Amplify does, and the loss limit that closes an account.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('How it works', None)])}
<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 {section('who', 'The simple picture', 'Who does what', '''
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Part</th><th>Its role</th></tr></thead><tbody>
<tr><td><b>JetUP</b></td><td style="white-space:normal">The community and partner program, with training and AI tools. Portal: jetup.ibportal.io. Hub: jet-up.ai. Does not trade, does not hold your money.</td></tr>
<tr><td><b>TAG Markets</b></td><td style="white-space:normal">The broker (T.M. Financials Ltd, FSC Mauritius). Your trading account sits here, in your own name.</td></tr>
<tr><td><b>CopyX</b></td><td style="white-space:normal">TAG Markets' copy trading platform. It copies a strategy's trades into your account.</td></tr>
<tr><td><b>Sonic AI</b></td><td style="white-space:normal">The strategy members connect. It trades gold (XAU/USD). Track record on Myfxbook.</td></tr>
<tr><td><b>BIX Card</b></td><td style="white-space:normal">Optional. A self-custody crypto wallet with a Visa card (the BixPay app), listed in the JetUP portal.</td></tr>
<tr><td><b>Bit1</b></td><td style="white-space:normal">A crypto exchange listed in the JetUP portal.</td></tr>
</tbody></table></div>
<p style="margin-top:14px">JetUP says on its own website that its trading accounts and transactions run through T.M. Financials Ltd, trading as TAG Markets.</p>''', 'i-users2')}
 {section('copy', 'Copy trading', 'What "copying" really means', '''
<p>When you connect Sonic AI on CopyX, the strategy's trades are copied into <b>your</b> account automatically. You don't pick the trades. You pick the strategy, how much to put in, and when to stop.</p>
<ul>
 <li><b>XAU/USD</b> is gold, priced in US dollars. XAU means gold, USD means US dollar.</li>
 <li>The Sonic AI terms in the training: a 30% performance fee from profits only, no management fee, no join fee, a one month minimum, and an Amplify account.</li>
 <li>The second agreement you tick says CopyX trades come from traders who are not part of TAG Markets, and TAG Markets bears no responsibility for them.</li>
</ul>''' + sonic_card(eyebrow="Watch it · JetUP's own video · 1:04", title='Sonic AI <span class="grad">in 64 seconds</span>', framed=False), 'i-copyx')}
 {section('split', 'Where the money goes', 'The 70/30 split', f'''
<p>When the strategy makes a profit, <b>70% is yours</b>. <b>30% pays the broker, the strategy provider and the partner program</b>. So if the strategy makes $10, $7 is yours. And if it makes a loss, nobody charges you a performance fee on that loss.</p>
<p>JetUP's own one-pager says the Lot Commission and the Global Pool are paid from broker margin, and the Profit Share comes from the 30% share of strategy profit, never from client deposits.</p>
<p><a class="btn btn-lime btn-sm" href="/jetup/tools/profit-split-calculator/">{icon('i-split')}Open the Profit Split Calculator</a></p>''', 'i-split')}
 {section('amplify', 'Amplify 24x', 'Exposure, not money you own', f'''
<p>Amplify lets an account trade at 24 times its size. In the training: <b>$50 × 24 = $1,200</b>, and the $200 promo account <b>× 24 = $4,800</b>. Together that's <b>$6,000 of exposure</b>. Exposure is the size you trade with, not money you own.</p>
<p>With 24x, a price move of about 4.2% (100% ÷ 24) on the trading balance is the same size as the whole account. A 1% move on $6,000 is $60.</p>
<div class="call warn">{icon('i-alert')}<p><b>The loss limit, from TAG Markets' screen:</b> if the trader loses more than 10% of the starting balance, your account will be liquidated, which means closed. With a community token, that limit becomes 5%.</p></div>
<p style="margin-top:14px"><a class="btn btn-lime btn-sm" href="/jetup/tools/exposure-calculator/">{icon('i-candle2')}Open the Exposure Calculator</a></p>''', 'i-candle2', 'red')}
 {section('withdraw', 'Getting money out', 'Withdrawals', '''
<ul>
 <li>Profits can be withdrawn any time. Withdrawals go through the broker. JetUP's one-pager says they take about 48 hours on average, and that fees and limits are the broker's terms.</li>
 <li>On the Dennis promo: the $100 bonus is released after 12 months, and taking your own money out before then ends the promo.</li>
 <li>Start small and test a small withdrawal early. Let the system prove itself to you.</li>
</ul>''', 'i-door', 'lime')}
</div></section>
{tribe_cta()}'''
    return page(path, 'How JetUP and TAG Markets Work: CopyX, Sonic AI, 70/30 | MTG',
                'How JetUP and TAG Markets fit together: your own TAG Markets account, CopyX copy trading, Sonic AI on gold (XAU/USD), the 70/30 profit split, 24x Amplify exposure and the loss limit.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('How it works', None)], [ld_video('sonic')])

def build_plan():
    path = '/jetup/partner-plan/'
    lots = [2, 1, 1, 1, .5, .5, .5, .5, .5, .5]
    bars = ''.join('<i style="height:%d%%;transition-delay:%dms"><span>$%s</span></i>' % (v / 2 * 100, i * 60, ('%.2f' % v)) for i, v in enumerate(lots))
    ps = ''.join('<i style="height:60%%;transition-delay:%dms"><span>1.5%%</span></i>' % (i * 60) for i in range(10))
    lx = ''.join('<span>L%d</span>' % (i + 1) for i in range(10))
    inf = [('$50K', '1.5%'), ('$200K', '3%'), ('$500K', '4%'), ('$1M', '5%'), ('$3M', '5.5%'), ('$7.5M', '6%'), ('$15M', '6.5%'), ('$25M', '7%'), ('$40M', '7.5%')]
    inf_rows = ''.join('<tr><td class="n">%s</td><td class="n">%s</td></tr>' % (a, b) for a, b in inf)
    main = f'''
{phead('i-users2', "JetUP's partner program", "The partner plan, <span class=\"grad\">in plain English</span>",
       "JetUP pays partners four ways, all tied to trading at TAG Markets. Here they are, with JetUP's own figures, and with the rules most people miss. Read this as information, not a promise: what a partner earns can be zero.",
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Partner plan', None)],
       [icon('i-file') + "JetUP's figures, as of 4 Oct 2026", icon('i-info2') + 'Check current terms in your partner account'])}
<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="call warn rv">{icon('i-alert')}<p><b>Before any number:</b> {RETAIL_LOSS} of retail investor accounts lose money when trading CFDs (TAG Markets' reminder), 24x Amplify makes losses bigger too, and accounts are closed at a 10% loss of the starting balance (5% with a community token). JetUP's plan says there is no fixed, daily or guaranteed return and no guaranteed income.</p></div>
 {section('qualify', 'Who qualifies', 'The rule most people miss', '''
<ul>
 <li>JetUP's plan says <b>everyone needs at least $250 of active trading</b> to qualify as a partner.</li>
 <li>A <b>$250 own deposit opens 3 levels</b>. With 1 to 3 direct partners it is still 3 levels. From the 4th direct partner, each new direct partner opens 1 more level. 10 direct partners open all 10.</li>
 <li>The sign-up training uses $155 ($150 of your own money in the strategy and the promo). That's a client start. If you want to earn as a partner, check the current qualification in your partner account first.</li>
</ul>''', 'i-key', 'lime')}
 <article class="card pad rv" id="lot" data-in>
  <p class="eyebrow">Income 1 · Lot Commission</p><h2 class="h2" style="margin:10px 0 10px;font-size:clamp(1.7rem,3.6vw,2.4rem)">Up to $8.00 per lot, 10 levels deep</h2>
  <p class="small" style="color:var(--body);line-height:1.7;margin:0">A fixed amount for every lot (a standard trade size) traded in your structure. Counted from real traded volume, not from deposits. Paid from broker margin.</p>
  <div class="levels" aria-hidden="true">{bars}</div><div class="levels-x" aria-hidden="true">{lx}</div>
  <p class="sr">Level 1: $2.00. Levels 2 to 4: $1.00 each. Levels 5 to 10: $0.50 each. Total $8.00 per lot.</p>
 </article>
 <article class="card pad rv" id="profit-share" data-in>
  <p class="eyebrow">Income 2 · Profit Share</p><h2 class="h2" style="margin:10px 0 10px;font-size:clamp(1.7rem,3.6vw,2.4rem)">1.5% on each of 10 levels</h2>
  <p class="small" style="color:var(--body);line-height:1.7;margin:0">When the Sonic AI strategy makes a profit, partners receive 1.5% of that strategy profit on each of 10 levels of their structure. It is paid out of the 30% share, never from client deposits. Levels open the same way as above.</p>
  <div class="levels" aria-hidden="true" style="height:110px">{ps}</div><div class="levels-x" aria-hidden="true">{lx}</div>
  <div style="margin-top:18px;max-width:300px;margin-inline:auto">{phone('profitshare', "JetUP's own Profit Share video (1:14)")}</div>
 </article>
 {section('infinity', 'Income 3 · Infinity Bonus', 'A leadership bonus, no depth limit', f'''
<p>An extra percentage on top of the Profit Share, from level 1 with unlimited depth, set by the <b>new</b> team volume each calendar month (not your accumulated total).</p>
<div class="tbl-wrap" style="max-width:420px"><table class="tbl"><thead><tr><th>New volume a month</th><th>Rate</th></tr></thead><tbody>{inf_rows}</tbody></table></div>
<ul style="margin-top:14px">
 <li><b>The 50% rule:</b> at most half of your qualifying volume can come from one line, so Infinity needs at least two strong lines.</li>
 <li><b>The difference rule:</b> if a partner in your line reaches their own Infinity level, you earn the difference between your rates on their structure.</li>
</ul>''', 'i-trend2')}
 {section('pool', 'Income 4 · Global Pool', 'For very large structures', '''
<ul>
 <li><b>Pool 1:</b> 1% of profit plus $1 per lot, from $300,000 of fresh capital a month.</li>
 <li><b>Pool 2:</b> 1% of profit plus $1.50 per lot, from $1,000,000 of fresh capital a month.</li>
 <li>Qualification is confirmed every month, the 50% rule applies, and it is paid from broker margin.</li>
</ul>''', 'i-coins2')}
 {section('bix', 'Income 5 · BIX Card', 'Commissions from card sales and spending', '''
<p>Half of the fees BIX collects (the 3% spending fee and the card purchases) goes into the plan: <b>15%</b> on level 1, <b>10%</b> on level 2, <b>2.5%</b> on each of levels 3 to 10, and <b>5%</b> to a leadership pool, as shown in a JetUP partner presentation (November 2026).</p>
<p>It only counts once your BixPay wallet is linked to the JetUP portal. <a href="/jetup/bix-card/#link">How to link it, even from a phone</a>.</p>''', 'i-card2')}
 {section('rewards', 'Lifestyle rewards', "JetUP's rewards, and what they really are", '''
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Reward</th><th>Team volume</th><th>For</th></tr></thead><tbody>
<tr><td>Travel voucher up to $2,000</td><td class="n">$50K</td><td>3 months in a row</td></tr>
<tr><td>Rolex up to $15,000</td><td class="n">$500K</td><td>2 months in a row</td></tr>
<tr><td>Rolex up to $25,000</td><td class="n">$1M</td><td>2 months in a row</td></tr>
<tr><td>Real estate voucher up to $1.2M</td><td class="n">$3M</td><td>6 months in a row</td></tr>
</tbody></table></div>
<p style="margin-top:14px">JetUP's notes: a voucher or its cash equivalent, the real estate voucher is towards property (not a house handed over), and only campaigns listed in your partner account are open. These are JetUP's marketing figures, not a promise.</p>''', 'i-trophy2', 'gold')}
 <div class="card pad rv"><p class="eyebrow">The honest summary</p><p class="lede" style="margin-top:12px">JetUP's own founder says the big money comes from building a team, not from the trading percentage. So if you share this, share it the right way: teach first, show the risks, and never promise anyone an income. Say "potential business partners", and treat the people who join as business partners.</p>
 <p style="margin:16px 0 0"><a class="btn btn-ghost btn-sm" href="/jetup/downloads/">{icon('i-dl2')}Download the Business Plan and the one-pager</a></p></div>
</div></section>
{tribe_cta('Build it <span class="lime">the right way.</span>', 'Leaders and team builders: join the MTG TRIBE to learn how to teach this honestly, one step at a time.')}'''
    faq = [('How does the JetUP partner plan pay?', "JetUP's plan has four incomes: Lot Commission (up to $8 per lot over 10 levels), Profit Share (1.5% of Sonic AI strategy profit on each of 10 levels), the Infinity Bonus (1.5% to 7.5% on new monthly team volume) and the Global Pool. What a partner earns can be zero."),
           ('How do I qualify as a JetUP partner?', "JetUP's plan says everyone needs at least $250 of active trading. A $250 own deposit opens 3 levels; from the 4th direct partner each new direct partner opens one more level, and 10 direct partners open all 10.")]
    return page(path, 'JetUP Partner Plan Explained: Lot Commission, Profit Share | MTG',
                "JetUP's partner plan in plain English: Lot Commission over 10 levels, 1.5% Profit Share on Sonic AI at TAG Markets, the Infinity Bonus, the Global Pool, rewards and the $250 qualification rule.",
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Partner plan', None)], [ld_faq(faq, SITE + path), ld_video('profitshare')])

def build_promo():
    path = '/jetup/promo/'
    main = f'''
{phead('i-gift', 'Dennis Fast Start Promo', 'The $100 promo, <span class="grad">rules first</span>',
       'New partners, once: your own $100 plus a $100 bonus open a Sonic AI account at TAG Markets that trades as $4,800 with 24x Amplify. Here are the rules, and how to claim it in part 6 of the training.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('Dennis Fast Start Promo', None)])}
<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="card ticket rv" data-in>
  <div class="tk-head"><span>The promo account</span><b>Sonic AI · Amplify 24x</b></div>
  <div class="tk-row rv-row"><span class="tki" aria-hidden="true">💵</span><p>Your own money<small>Left in your TAG Markets balance</small></p><span class="v">$100</span></div>
  <div class="tk-row rv-row" style="transition-delay:.15s"><span class="tki" aria-hidden="true">🎁</span><p>The promo bonus<small>Added after your application is accepted</small></p><span class="v up">+$100</span></div>
  <div class="tk-row rv-row" style="transition-delay:.3s"><span class="tki" aria-hidden="true">🧮</span><p>Promo account<small>$200 × 24</small></p><span class="v">$200</span></div>
  <div class="tk-row total rv-row" style="transition-delay:.45s"><span class="tki" aria-hidden="true">📈</span><p>Exposure<small>Not your money: risk works both ways</small></p><span class="v">$4,800</span></div>
 </div>
 {section('rules', 'Know the rules', 'The promo rules', '''
<ul>
 <li>💵 <b>Profits</b> can be withdrawn any time.</li>
 <li>📅 <b>The $100 bonus</b> is released after 12 months.</li>
 <li>⛔ <b>Taking your own money out before 12 months</b> ends the promo. JetUP's one-pager says your $100 can be withdrawn after 30 days, but doing it before 12 months liquidates the account and ends the promo.</li>
 <li>👤 <b>For new partners, once.</b></li>
 <li>📲 <b>Rules can change,</b> so check your dashboard and jet-up.ai before you deposit.</li>
</ul>''', 'i-info2', 'lime')}
 {section('claim', 'How to claim it', 'Three steps, in part 6', '''
<ol>
 <li>In TAG Markets open the menu, tap <kbd>Profile</kbd> and write down your CU number.</li>
 <li>On jet-up.ai, tap the orange <kbd>Dennis Fast Start Promo</kbd> tile. Enter your name, email and CU number exactly, then tap <kbd>Join the promo</kbd>.</li>
 <li>You'll see <kbd>Application received!</kbd> When the confirmation email arrives, check CopyX, Follower Hub, Strategies: you should see your $50 account and your $200 promo account.</li>
</ol>
<p><a href="/jetup/get-started/#part-6">Open part 6 with the screenshots</a></p>''', 'i-rocket2')}
 <div class="card lime-edge pad promo rv">
  <span class="hourglass" aria-hidden="true">⏳</span>
  <div><p class="eyebrow">And remember</p><h2 class="h2" style="margin-top:10px;font-size:clamp(1.9rem,4vw,2.8rem)">A promo is <span class="lime">a promo.</span></h2>
   <ul class="plist">
    <li><span class="e" aria-hidden="true">✅</span>Still running when I made this training</li>
    <li><span class="e" aria-hidden="true">⏳</span>It won't be here forever. Nobody can promise the end date</li>
    <li><span class="e" aria-hidden="true">🚀</span>Decided to start? Start while it's still on</li>
    <li><span class="e" aria-hidden="true">🔎</span>Confirm it on jet-up.ai before you deposit</li>
    <li><span class="e" aria-hidden="true">📤</span>Send this page to someone who's ready</li>
   </ul></div>
 </div>
</div></section>
{tribe_cta()}'''
    return page(path, 'JetUP Dennis Fast Start Promo: $100 Bonus Rules | MTG',
                'The JetUP Dennis Fast Start Promo explained: your $100 plus a $100 bonus, 24x Amplify on TAG Markets, the 12-month rule, how to claim it with your CU number on jet-up.ai, and the risks.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('Dennis Fast Start Promo', None)])

def build_bix():
    path = '/jetup/bix-card/'
    main = f'''
{phead('i-card2', 'BIX Card', 'A crypto wallet <span class="grad">with a Visa card</span>',
       'BIX is a non-custodial (self-custody) crypto wallet paired with a Visa card. You spend against your USDT or USDC while you keep control of your keys. It is listed inside the JetUP portal, and linking it takes a QR code and the same email.',
       [('MTG TRIBE', '/'), ('JetUP guide', '/jetup/'), ('BIX Card', None)],
       [icon('i-phone') + 'The BixPay app', icon('i-lock') + 'Self-custody', icon('i-info2') + 'Optional'])}
<section class="sec tight" style="padding-top:0"><div class="narrow stack" style="gap:20px">
 <div class="card pad rv vrow" id="bix-video">
  <div>{phone('bix')}</div>
  <div><p class="eyebrow">BIX's own clip · 0:10</p><h2 class="h2" style="margin:10px 0 12px;font-size:clamp(1.7rem,3.4vw,2.3rem)">See the BIX Card <span class="grad">in 10 seconds</span></h2>
   <p class="lede">The lime BIX Visa card and the BixPay app. Top up the card from your self-custody crypto wallet, then pay anywhere Visa works, or add it to Apple Pay or Google Pay.</p>
   <p class="small" style="margin-top:12px">This is BIX's own promo clip. The balance and the purchases on the screen are BIX's demo, not a real account.</p>
   <div class="ctas" style="margin-top:16px"><a class="btn btn-pri" href="#setup">{icon('i-rocket2')}Set it up in 5 steps</a><a class="btn btn-ghost" href="#link">{icon('i-link')}Link it to JetUP</a></div></div>
 </div>
 <div class="call info rv">{icon('i-info2')}<p><b>MTG's BIX Card link is coming.</b> Until then, install BixPay from the official bix.fi website. A step-by-step BIX Card video is planned.</p></div>
 {section('setup', 'Set it up', 'Five steps to your card', '''
<ol>
 <li><b>Install BixPay</b> from bix.fi, the App Store or Google Play. It is free to download.</li>
 <li><b>Create your account with the same email as your JetUP portal.</b> Write down your recovery phrase offline if it is shown, and turn on 2FA (two-factor authentication). Never share your recovery phrase: BIX will never ask for it.</li>
 <li><b>Do your KYC:</b> one current ID document (the original, not a photo of a photo) and a proof of address from this month.</li>
 <li><b>Deposit USDT or USDC on a supported network.</b> Check the network list in the app. Send a small test amount first if the network is new to you.</li>
 <li><b>Create your virtual card,</b> then top it up from your wallet. You can add it to Apple Pay or Google Pay.</li>
</ol>''', 'i-rocket2')}
 {section('link', 'Link it to JetUP', 'One QR code, same email', '''
<ol>
 <li>Do your BixPay KYC first. Then in the JetUP portal tap the <b>BIX banner</b>, or open <kbd>Profile</kbd>, then <kbd>BIX Wallets &amp; Debit Card</kbd>, and tap <kbd>Register</kbd>. A QR code opens.</li>
 <li>In BixPay go to <kbd>Settings</kbd>, then <kbd>Scan QR</kbd>, and scan the code. <b>Scan inside the app, not with your phone camera.</b></li>
 <li><b>Only have a phone?</b> Open the portal on your phone, take a screenshot of the QR code, then in BixPay tap <kbd>Scan QR</kbd> and choose <kbd>Load from gallery</kbd>.</li>
 <li>Tap <kbd>Approve</kbd>. Your wallet is linked, and the portal shows <b>User active</b>. If the banner shows <kbd>Login</kbd> instead, you are already linked: that button only opens the app stores.</li>
</ol>
<p><b>Link it now, even if you don't buy a card yet.</b> Linking moves no money. It records your place in the team, so BIX Card commissions follow the right structure later.</p>
<p>You never type an ID into a form to connect. Afterwards, your Profile shows your IDs: your IB number, your TID (the CU number used in JetUP promos) and your BIX ID. Tap the copy icon next to each one when support asks.</p>''', 'i-link')}
 {section('topup', 'Spend your crypto', 'Top up the card from TAG Markets', '''
<ol>
 <li>In BixPay copy your wallet address for the coin and network you will send.</li>
 <li>In TAG Markets withdraw from your <b>TAG wallet</b> to that address, on the same network. Check twice: the wrong network means lost funds.</li>
 <li>In BixPay tap <kbd>Top up card</kbd>, choose the amount or <kbd>Max</kbd>, and confirm. It usually lands within a minute.</li>
</ol>
<p><b>Your keys, your money.</b> BIX is self-custody: export your private key (or recovery phrase) from the app's settings and keep it offline. If you lose your phone, it is your only way back in, and nobody, not even BIX, can recover it for you.</p>''', 'i-wallet2')}
 {section('earn', 'For partners', 'BIX Card commissions', '''
<p>Spending with the card has a <b>3% transaction fee</b>. Half of the fees BIX collects, including what is paid for virtual and plastic cards, goes into JetUP's partner plan:</p>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Where it goes</th><th>Share of collected fees</th></tr></thead><tbody>
<tr><td>Level 1</td><td class="n">15%</td></tr><tr><td>Level 2</td><td class="n">10%</td></tr><tr><td>Levels 3 to 10</td><td class="n">2.5% each</td></tr><tr><td>Leadership pool</td><td class="n">5%</td></tr>
</tbody></table></div>
<p style="margin-top:14px">To see it in the portal, open the <kbd>CopyX</kbd> drop-down in the left menu and choose <kbd>BIX Crypto Wallet</kbd>: Network, Commissions and Progress (cards bought) appear. Choose <kbd>CopyX</kbd> again to switch back.</p>
<p>These figures are from a JetUP partner presentation (November 2026). Confirm the current terms in your partner account. Commissions depend on real card sales and spending, so they can be zero.</p>''', 'i-users2', 'lime')}
 {section('prices', 'What it costs', 'Prices from the BIX Help Center', '''
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Item</th><th>Price</th></tr></thead><tbody>
<tr><td>App</td><td class="n">Free</td></tr><tr><td>Virtual Visa card</td><td class="n">$9.99</td></tr><tr><td>Plastic card</td><td class="n">$100.99</td></tr><tr><td>Metal and Gold cards</td><td>Listed as coming soon</td></tr><tr><td>Card top-up fee</td><td class="n">None</td></tr><tr><td>FX and ATM fees</td><td style="white-space:normal">May apply by region: check the app</td></tr>
</tbody></table></div>
<p style="margin-top:14px">Prices were taken from help.bix.fi (September 2026). Always check fees and eligibility in the live app before you pay.</p>''', 'i-coins2', 'lime')}
 <div class="ctas rv"><a class="btn btn-ghost" href="https://bix.fi/" target="_blank" rel="noopener">{icon('i-ext2')}Official website: bix.fi</a><a class="btn btn-ghost" href="/jetup/downloads/bix-card-setup-and-funding-guide.pdf" download>{icon('i-dl2')}BIX setup guide (PDF)</a></div>
</div></section>
{tribe_cta()}'''
    return page(path, 'BIX Card with JetUP: Setup, Fees and Linking | MTG',
                'The BIX Card in the JetUP portal: the BixPay self-custody wallet and Visa card, setup, KYC, card prices, linking to the JetUP IB portal with a QR code (even from a phone), top-ups from TAG Markets and BIX Card commissions for partners.',
                main, [('MTG TRIBE', '/'), ('JetUP and TAG Markets', '/jetup/'), ('BIX Card', None)], [ld_video('bix')],
                keywords='BIX Card, BixPay, JetUP BIX Card, BIX Wallet, crypto Visa card, JetUP IB portal, TAG Markets, MTG TRIBE')
