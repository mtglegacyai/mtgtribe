"""Dashboard pages: Start here + How it works."""
from core import *


def phero(icon, title, lead, chips_=(), pcls='', extra=''):
    ch = chips(*chips_) if chips_ else ''
    return (f'<section class="phero"><div class="wrap"><div class="phero-in">{ped(icon, "lg " + pcls)}<div>'
            f'<h1 class="h1">{title}</h1><p class="lead">{lead}</p>{ch}{extra}</div></div></div></section>')


def honest(title, body):
    return f'<div class="honest">{ic("triangle-alert")}<div><b>{title}</b> {body}</div></div>'


# ======================================================================= WELCOME
def p_home(here):
    def tiles_for(codes):
        return ''.join(f'<button type="button" class="vtile" data-play="{k}" data-vid="{k}" title="{esc(V[k]["desc"])}">'
                       f'<span class="vn">{V[k]["n"]}</span><span class="vt">{V[k]["short"]}</span>{ic("circle-check")}</button>' for k in codes)
    tiles = (f'<p class="vgl">Tutorials</p><div class="vgrid">{tiles_for(TUT)}</div>'
             f'<p class="vgl">Explainers</p><div class="vgrid">{tiles_for(EXP)}</div>'
             f'<p class="vgl">Tool trainings</p><div class="vgrid">{tiles_for(TOOL)}</div>')
    route = steps([
        ('Check the fit', f'<p>Start honest. Read <a class="inl" href="{A("dashboard/is-it-right-for-me/", here)}">Is it right for me?</a> '
                          f'and <a class="inl" href="{A("dashboard/what-makes-it-different/", here)}">What makes it different</a>. Five minutes.</p>'),
        ('Understand the plan', f'<p>{WORDS_N.get(len(EXP), len(EXP))} animated explainers, about {EXP_MIN} minutes in total. Start with '
                                f'<a class="inl" href="{A("dashboard/how-it-works/", here)}">Where every dollar goes</a>.</p>'),
        ('Join step by step', f'<p>Tutorials 1 to 3 walk you through SafePal, USDT and joining. '
                              f'<a class="inl" href="{A("dashboard/join/", here)}">Open the join guide</a>.</p>'),
        ('Use your first 72 hours', f'<p>Just joined? Your clock has started. <a class="inl" href="{A("dashboard/first-72-hours/", here)}">Your first 72 hours</a> shows what to do from minute one.</p>'),
        ('Know your dashboard', f'<p>Tutorial 7 shows every screen of the ALTRUVA app and what each number means.</p>'),
        ('Run your numbers', f'<p>Try the four <a class="inl" href="{A("dashboard/tools/withdraw-split-calculator/", here)}">calculators</a> '
                             f'with your own amounts.</p>'),
        ('Get your money out', f'<p>Explainer 6 and Tutorials 4 to 6: claim, withdraw, and cash out to your bank.</p>'),
        ('Teach someone else', f'<p>We learn best when we teach others. The <a class="inl" href="{A("dashboard/downloads/", here)}">downloads</a> '
                               f'have every video and a share message.</p>'),
    ])
    return f'''{phero("compass", "Welcome. Here's your route.",
        "Take it one stop at a time. Watch every video, even if you think you already know ALTRUVA. Come back to any page as often as you like, until you get it.",
        [("film", f"{NV} videos, about {TOTAL_MIN} minutes"), ("package", "Top package $100"), ("info", "Independent, not official")])}
{sec(f"""<div class="panel pad prog-panel"><div class="prog">
 <div class="pring" data-ring><svg viewBox="0 0 118 118" aria-hidden="true"><defs><linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="#2f9ff9"/><stop offset="1" stop-color="#eebd5c"/></linearGradient></defs><circle class="bg" cx="59" cy="59" r="50"/><circle class="fg" cx="59" cy="59" r="50"/></svg>
 <div class="val"><b data-k="n">0</b><small>of {NV} watched</small></div></div>
 <div class="stack"><div><h2 class="h3">Your progress</h2><p class="fine">Tap a video to play it. A tick appears when you finish one. Progress is saved on this device only.</p></div>{tiles}</div>
</div></div>""", id="progress")}
{sec(route, "Your route, in order", "Eight stops. Each one builds on the last, so go in order the first time.")}
{sec(f"""<div class="grid3">
 {box("The menu", "<p>Every page is in the menu, grouped in the order you'll need them. On a phone, tap <b>Menu</b> at the top.</p>", "panel-left")}
 {box("Next and Previous", "<p>The buttons at the bottom of each page walk you through everything in order. You'll never get lost.</p>", "route")}
 {box("Sign Up and Login", "<p>Both buttons copy a link and open nothing. Paste it into your wallet's browser, like SafePal's Explore.</p>", "copy")}
</div>""", "How to use this dashboard")}
{sec(f"""<div class="stack">{think("Do I have to learn everything before I start?",
    "<p>No. But don't go in blind either. Learn enough to explain it honestly to someone else, because a blind leader leading the blind is a disaster. Then keep learning as you go, and put each lesson into practice.</p>")}
{think("Is there a live presentation I can attend?",
    "<p>Yes. ALTRUVA Zoom presentations are announced in the ALTRUVA WhatsApp groups. Ask the person who introduced you to ALTRUVA to add you to the right group.</p>", alt=True, icon="video")}</div>""")}
'''


# ======================================================================= FIT
def p_fit(here):
    qs = [
        ('afford', 'I could lose $100 without it hurting my rent, food or family.'),
        ('phone', 'I have a smartphone and can install a wallet app like SafePal.'),
        ('watch', f'I\'ll watch all {NV} videos (about {TOTAL_MIN} minutes), even the ones I think I know.'),
        ('risk', 'I understand earnings are not guaranteed and depend on new deposits.'),
        ('teach', 'I\'d only share ALTRUVA once I can explain it honestly, risks included.'),
    ]
    rows = ''.join(f'<label class="fit-q"><input type="checkbox" data-fit="{k}"><span class="tg" aria-hidden="true"></span><span>{t}</span></label>' for k, t in qs)
    return f'''{phero("scale", "Is ALTRUVA right for you?",
        "An honest fit check before anything else. No pressure: not joining is a perfectly good answer.")}
{sec(f"""<div class="calc fitcheck"><div class="form panel pad" data-fitcheck><h2 class="h3">Tick what's true for you</h2>{rows}</div>
<div class="result" aria-live="polite"><div class="rbig"><small>Your fit check</small><b data-k="score">0 of 5</b></div><p data-k="msg">Tick the statements that are true for you.</p></div></div>""",
    "Five honest questions")}
{sec(f"""<div class="grid2">
 {box("It may suit you if", checks(["You want to learn how a smart contract plan works from the inside.", "You can keep your test small: the top package is $100.", "You like rules you can see on screen, in your own dashboard.", "You're willing to learn, take action and teach others honestly."]), "thumbs-up")}
 {box("It's probably not for you if", checks(["You need this money for rent, food, school fees or debt.", "You want a guaranteed return. There isn't one.", "You hope to earn without learning or sharing anything.", "You'd pressure friends or family to join."], no=True), "ban")}
</div>""", "Who it suits, and who it doesn't")}
{sec(f"""<div class="panel pad flow">
 <div class="flowrow"><span class="fnode">{ic("users")}Members' packages and reinvestments</span>{ic("arrow-right", "ic farrow")}<span class="fnode gold">{ic("blocks")}ALTRUVA smart contract</span>{ic("arrow-right", "ic farrow")}<span class="fnode">{ic("hand-coins")}Shared back to members by fixed rules</span></div>
 <p class="lead">That's the whole money flow. No outside revenue is named, so <b>earnings depend on new deposits</b>. When deposits slow down, earnings slow down. It's the most important sentence on this site.</p>
</div>""", "Where the money comes from")}
{sec(f"""<div class="stack">
{think("What's the most I can put in?", "<p>The top package is Elite at $100, and the app itself says there's nothing more to buy. Go straight to Elite and your package costs $100, plus a few cents of BNB per action for network fees.</p>")}
{think("Can I open more than one account?", "<p>Some people do. That's their own strategy and their own risk. This guide explains one account.</p>", alt=True)}
{think("So should I join?", "<p>That's your decision, and this guide won't make it for you. If it fits, the fairest test is from the inside: learn first, then try it with an amount you can afford to lose, and judge it by what your own dashboard shows. Not by what anyone promises, me included.</p>", icon="flag")}
</div>""")}
'''


# ======================================================================= DIFFERENT
def p_diff(here):
    rows = [
        ('Is there a fixed daily return?', 'No. ALTRUVA says there is no fixed ROI and no guaranteed return. Rewards depend on activity.'),
        ('Where does the money come from?', 'Members\' packages and reinvestments, shared by fixed rules. No outside revenue is named.'),
        ('What\'s the most I can put in?', 'The top package is $100. The app says there\'s nothing more to buy.'),
        ('Who holds my money before I join?', 'You do, in your own wallet. There\'s no account, username or password to hand over.'),
        ('Can someone block my withdrawal?', 'You claim and withdraw yourself, by signing in your wallet. Nobody approves it by hand. Whether the contract owner keeps special powers is a separate check: see <a class="inl" href="' + A('dashboard/safety/', here) + '#contract">renounced</a>.'),
        ('Is the contract verified, audited and renounced?', 'Not confirmed by us yet. This page will be updated. Learn to check it yourself in the Safety centre.'),
        ('Will it last?', 'Nobody knows, and anyone who promises you an answer is guessing. On Day 31 (24 Oct 2026) the app showed about 2.4 million USDT of business. Past numbers don\'t predict future ones.'),
    ]
    return f'''{phero("sparkles", "What makes ALTRUVA different",
        "If a platform let you down before, you're right to be careful. Here's what's different, and what's exactly the same.")}
{sec(think("Isn't this just like the ones that crashed?",
    "<p>In one way, yes. Like every platform of this kind, payouts come from members' deposits, so when new deposits slow down, earnings slow down. That part is the same everywhere, and nobody can promise how long it lasts.</p><p>What's different is how the risk is shaped. Look at the six points below, then decide for yourself.</p>"))}
{sec(f"""<div class="grid3">
 {box("A $100 ceiling", "<p>Three packages: $25, $50 and $100. There's no $5,000 slot to be talked into. Your package can't cost more than $100.</p>", "package")}
 {box("No promised return", "<p>No 2% a day, no fixed ROI. ALTRUVA itself says rewards depend on activity. A fixed daily promise is the red flag; this plan doesn't make one.</p>", "ban")}
 {box("You hold the keys", "<p>You join from your own Web3 wallet. Your USDT stays with you until you choose a package and sign.</p>", "key-round")}
 {box("The contract pays", "<p>Working level income lands in your balance automatically. The rest you claim yourself. You withdraw whenever you choose.</p>", "blocks")}
 {box("Rules on screen", "<p>The app shows the daily matching ledger, pool sizes, your window on the global leg and every Lucky Ticket draw.</p>", "eye")}
 {box("Reinvest built in", "<p>30% to 50% of each withdrawal goes back in as new business. It keeps money moving, and that part stays in the system.</p>", "repeat")}
</div>""", "Six things that are different")}
{sec(table(["Ask any platform", "What we found for ALTRUVA"], rows, caption="Questions to ask any smart contract platform"),
    "Questions to ask any platform", "Use these on ALTRUVA and on anything else you're offered. Good questions are your best protection.")}
{sec(f"""<div class="panel pad heal"><h2 class="h3">{ic("hand-heart")} If you lost money before</h2>
<p>That wasn't stupidity. Many of those platforms promised fixed daily returns and hid how they paid them. What you took away is priceless: you now ask better questions. Bring those questions here, and keep asking them. That's how you protect yourself, and the people you'll teach.</p></div>""")}
'''


# ======================================================================= SPLIT
SPLIT = [
    ('Global leg', 40, '#2f9ff9', 'dashboard/global-leg/', '1% from each member in your window'),
    ('Working levels', 25, '#0ce1f2', 'dashboard/working-levels/', 'Nine levels below you'),
    ('Level matching', 25, '#eebd5c', 'dashboard/level-matching/', 'The daily pool'),
    ('Ranks', 5, '#8fb3ff', 'dashboard/ranks-lucky-tickets/', 'Nexus and Legacy Crown pools'),
    ('Lucky Tickets', 5, '#faea9c', 'dashboard/ranks-lucky-tickets/', 'The 5,000 USDT draw'),
]


def splitbar(here):
    segs = ''.join(f'<a href="{A(p, here)}" style="width:{w}%;background:{c}" aria-label="{n}: {w}%"><span>{w if w >= 25 else ""}{"%" if w >= 25 else ""}</span></a>'
                   for n, w, c, p, s in SPLIT)
    leg = ''.join(f'<a href="{A(p, here)}"><i style="background:{c}"></i><span><b>{n}</b><br><small class="muted">{s}</small></span><b>${w}</b></a>' for n, w, c, p, s in SPLIT)
    return f'<div class="splitbar" role="img" aria-label="Every 100 dollars: 40 global leg, 25 working levels, 25 level matching, 5 ranks, 5 Lucky Tickets">{segs}</div><div class="legend">{leg}</div>'


def p_split(here):
    return f'''{phero("chart-pie", "Where every dollar goes",
        "Every package goes into one smart contract on BNB Smart Chain. The contract shares it back to members by fixed rules, with no admin in the middle.",
        [("coins", "100% shared by rules"), ("blocks", "BNB Smart Chain"), ("circle-play", mmss(V["e1"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack">
 <h2 class="h2">Follow $100</h2>
 <p class="lead">Here's how every $100 package is shared. Tap a colour to open its page.</p>
 {splitbar(here)}
 <p class="how num">40 + 25 + 25 + 5 + 5 = <b>100</b>. Levels that nobody qualifies for stay in the contract, so not every cent reaches a member.</p>
</div>{vid("e1", here)}</div>""")}
{sec(f"""<div class="stack">
{think("So it's like a stokvel?", "<p>A little. Everyone puts money into one pot, and the pot is shared by rules everyone can see. But unlike a stokvel, you don't get your own money back on a schedule. You earn only from deposits made by others, so nothing is guaranteed.</p>")}
{think("Who decides the rules?", "<p>The smart contract: a program on the blockchain that runs the same rules for everyone, every time. Think of a vending machine: the right coin in, the snack out, no shopkeeper. Whether anyone can still change that program is a question worth checking: see <a class='inl' href='" + A("dashboard/glossary/", here) + "#renounced'>renounced</a>.</p>", alt=True)}
</div>""")}
'''


# ======================================================================= PACKAGES
PK = [
    ('starter', 'Starter', 25, 10, '1 ticket, once 2 directs join within 3 days', 'No rank'),
    ('builder', 'Builder', 50, 15, '1 ticket', 'Unlocks Nexus'),
    ('elite', 'Elite', 100, 20, '2 tickets', 'Unlocks Legacy Crown'),
]


def p_pkg(here):
    cards = ''
    for k, n, price, w, t, r in PK:
        cards += (f'<button type="button" class="pkg" data-pkg="{k}" data-price="{price}" aria-pressed="{"true" if k == "elite" else "false"}">'
                  f'<span class="nm">{n}{ic("crown") if k == "elite" else ""}</span><span class="pr">${price}<small> once</small></span>'
                  f'<ul><li>{ic("route")}<span>Global leg: {w} up, {w} down</span></li><li>{ic("ticket")}<span>{t}</span></li>'
                  f'<li>{ic("award")}<span>{r}</span></li></ul></button>')
    return f'''{phero("package", "Packages: Starter, Builder, Elite",
        "Three fixed packages. Each one opens a wider window on the global leg, and the top one is $100.",
        [("package", "$25, $50 or $100"), ("trending-up", "Step up, never down"), ("circle-play", "Tutorial 3 shows the screen")])}
{sec(f"""<div class="pkgs" role="group" aria-label="Choose a package to see your shopping list">{cards}</div>
<div class="panel pad shop" aria-live="polite"><h2 class="h3">{ic("wallet")}<span>Your shopping list for <span data-k="name">Elite</span></span></h2>
{checks(['<b data-k="usdt">101</b> USDT on BNB Smart Chain (BEP20). One extra dollar covers small differences.', 'At least $3 to $5 of BNB in the same wallet, for network fees of a few cents each.', 'The sign-up link from the person who introduced you.'])}
<div class="btn-row"><a class="btn btn-blue btn-sm" href="{A("dashboard/join/", here)}">{ic("rocket")}<span class="lbl">Join step by step</span></a>{play_btn("t2", "How to get USDT and BNB")}</div></div>""",
    "Compare the three", "Tap a package to see exactly what you need to buy it.")}
{sec(f"""<div class="grid3">
 {box("One step at a time, or straight to the top", "<p>The ladder is $25, then $50, then $100. You can climb it step by step or go straight to Elite.</p>", "trending-up")}
 {box("Each package once", "<p>You can't buy the same package twice, and you never step down.</p>", "lock")}
 {box("Reinvest doesn't upgrade you", "<p>Reinvested money grows your total deposit, but it never changes your package or your levels.</p>", "repeat")}
</div>""", "Ladder rules from the app")}
{sec(f"""<div class="stack">
{think("Which package should I choose?", "<p>That's your call. A bigger package opens a wider window on the global leg and more Lucky Tickets, and it also puts more of your money at risk. Pick an amount you could lose without stress. <a class='inl' href='" + A("dashboard/first-72-hours/", here) + "#why-100'>Why many choose the $100 position</a>.</p>")}
{think("Why does the first purchase ask me to confirm twice?", "<p>The first confirmation is an approval: it lets ALTRUVA's contract use that amount of your USDT. The second buys the package. After that, your sponsor and your seat on the global leg never change.</p>", alt=True)}
</div>""")}
'''


# ======================================================================= GLOBAL LEG
def p_leg(here):
    seats = ''.join(f'<i data-d="{abs(i)}"{" class=you" if i == 0 else ""}></i>' for i in range(-20, 21))
    return f'''{phero("route", "The global leg, 40%",
        "Every member joins one long global line. You earn 1% each time someone inside your window deposits or reinvests.",
        [("percent", "1% per member"), ("route", "10, 15 or 20 each way"), ("circle-play", mmss(V["e2"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack">
 <h2 class="h2">See your window</h2>
 <div class="panel pad leg" data-leg>
  <div class="seg" role="group" aria-label="Package"><button type="button" data-w="10" aria-pressed="false">Starter</button><button type="button" data-w="15" aria-pressed="false">Builder</button><button type="button" data-w="20" aria-pressed="true">Elite</button></div>
  <div class="seats" aria-hidden="true">{seats}</div>
  <div class="seatkey"><span>{ic("chevron-left")}Up: joined before you</span><b class="gold">You</b><span>Down: joined after you{ic("chevron-right")}</span></div>
  <p class="legtx" aria-live="polite"><b data-k="w">20</b> up and <b data-k="w2">20</b> down are open: <b data-k="n">40</b> members can pay you 1% each time they deposit or reinvest.</p>
 </div>
 <p class="how num">Example: a member three seats behind you buys a $100 package. 1% of $100 = <b>$1</b> for you. That deposit pays $1 to each of the 40 seats around it whose windows reach it: 40 × $1 = $40, the 40%.</p>
</div>{vid("e2", here)}</div>""")}
{sec(f"""<div class="grid3">
 {box("You keep your seat", "<p>Your place on the line never changes, and new members keep joining behind you.</p>", "map-pin")}
 {box("Claim any time", "<p>Global leg income builds up live. Claim it whenever you like, then withdraw. Nothing expires.</p>", "hand-coins")}
 {box("Outside your window", "<p>If your window doesn't reach someone, their 1% isn't yours. A bigger package opens more seats.</p>", "eye-off")}
</div>""")}
{sec(think("Do I have to introduce anyone to earn from the global leg?",
    "<p>No. The global leg pays from deposits inside your window, including people you've never met. But your income depends only on those deposits, so it can slow down or stop. Unlike a real queue, nobody gets served at the front.</p>"))}
'''


# ======================================================================= WORKING LEVELS
WL = [10, 4, 2, 2, 2, 2, 1, 1, 1]


def p_wl(here):
    rows = ''.join(f'<tr data-lv="{i + 1}"><td>Level {i + 1}</td><td><b>{r}%</b></td><td>{(i // 3) + 1} direct{"s" if i >= 3 else ""}</td>'
                   f'<td class="st"><span class="open">{ic("lock-open")}Open</span><span class="shut">{ic("lock")}Closed</span></td></tr>'
                   for i, r in enumerate(WL))
    return f'''{phero("layers", "Working levels, 25%",
        "The people you introduce are your directs: level 1. Their directs are level 2, all the way down to level 9.",
        [("percent", "10, 4, 2, 2, 2, 2, 1, 1, 1"), ("users", "Directs open levels"), ("circle-play", mmss(V["e3"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack" data-wl>
 <h2 class="h2">How many directs do you have?</h2>
 <div class="seg" role="group" aria-label="Number of directs"><button type="button" data-d="0" aria-pressed="false">0</button><button type="button" data-d="1" aria-pressed="false">1</button><button type="button" data-d="2" aria-pressed="false">2</button><button type="button" data-d="3" aria-pressed="true">3 or more</button></div>
 <div class="tbl-wrap"><table class="wltable"><caption class="sr">Working level rates and how they open</caption><thead><tr><th scope="col">Level</th><th scope="col">You earn</th><th scope="col">Opens with</th><th scope="col">For you</th></tr></thead><tbody>{rows}</tbody></table></div>
 <p class="legtx" aria-live="polite"><b data-k="lv">9</b> of 9 levels open: <b data-k="pc">25</b>% of the 25%.</p>
</div>{vid("e3", here)}</div>""")}
{sec(f"""<div class="grid3">
 {box("Straight to your balance", "<p>Working level income lands in your Withdrawable Balance. No claim needed.</p>", "zap")}
 {box("Closed levels", "<p>If a level is closed for you, that share stays in the contract. It doesn't move to someone else.</p>", "lock")}
 {box("Reinvest counts too", "<p>When someone below you withdraws, their reinvested part pays working levels like fresh money.</p>", "repeat")}
</div>""")}
{sec(f"""<div class="stack"><p class="how num">Example: your direct buys a $100 package. 10% of $100 = <b>$10</b> for you. Someone on level 7 buys $100: 1% = <b>$1</b>, but only if you have 3 directs. <a class="inl" href="{A("dashboard/tools/working-level-calculator/", here)}">Try the Working Level Calculator</a>.</p>
{think("Is this a family tree, then?", "<p>It's a good way to picture it: children, grandchildren, nine generations deep. But nobody inherits anything. You only earn when people in your open levels deposit or reinvest, so nothing is guaranteed.</p>")}</div>""")}
'''


# ======================================================================= MATCHING
def p_match(here):
    return f'''{phero("arrow-left-right", "Level matching, 25%",
        "Each day, 25% of the day's business becomes a pool. Your share depends on your smaller side.",
        [("scale", "Smaller side counts"), ("clock", "Days close 00:00 UTC"), ("circle-play", mmss(V["e4"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack">
 <h2 class="h2">Your two sides</h2>
 <div class="panel pad sides">
  <div class="side-row"><span>Side 1: your biggest direct, with everyone under them</span><div class="sbar"><i style="width:100%"></i></div><b class="num">1,000</b></div>
  <div class="side-row small"><span>Side 2: all your other directs together</span><div class="sbar"><i style="width:30%"></i></div><b class="num gold">300</b></div>
  <p class="fine">New business today. Only the smaller side counts, so <b class="gold">300 is matched</b>. The extra 700 on side 1 doesn't earn matching here.</p>
 </div>
 <h2 class="h3">The real day 22 numbers</h2>
 <ol class="steps calcsteps">
  <li><div><h3>The pool</h3><p class="num">25% of the day's business: 25% of $124,304 = <b>$31,076</b></p></div></li>
  <li><div><h3>The rate</h3><p class="num">Pool divided by everyone's matched volume: $31,076 ÷ 391,251 = <b>0.0794 per unit</b></p></div></li>
  <li><div><h3>Your share</h3><p class="num">Your matched volume times the rate: 100 × 0.0794 = <b>about $7.94</b></p></div></li>
 </ol>
</div>{vid("e4", here)}</div>""")}
{sec(f"""<div class="grid3">
 {box("Grow the weaker side", "<p>Your stronger side alone earns nothing here. New business on your weaker side is what opens fresh matching.</p>", "trending-up")}
 {box("One claim, all closed days", "<p>A day closes at 00:00 UTC (02:00 in South Africa). One claim collects every closed day since your last claim.</p>", "calendar-clock")}
 {box("The rate moves daily", "<p>It depends on the whole platform's new business that day, so it can drop. Day 22 was one real day, not a promise.</p>", "trending-down")}
</div>""")}
{sec(f"""<div class="stack">{think("Why did the presentation show $2.50 per unit?", "<p>That was an example in the slides. The live app's real day 22 rate was about 0.079 per unit. Always trust the numbers in the app over a slide. <a class='inl' href='" + A("dashboard/tools/matching-calculator/", here) + "'>Try the Matching Calculator</a> with today's rate.</p>")}</div>""")}
'''


# ======================================================================= RANKS + TICKETS
TIERS = [(10, 100), (10, 50), (40, 25), (10, 20), (20, 15), (40, 10), (120, 5)]


def p_ranks(here):
    tier_rows = [[f'Tier {i + 1}', f'{n}', f'{p} USDT', f'{n * p:,} USDT'] for i, (n, p) in enumerate(TIERS)]
    tier_rows.append(['<b>Total</b>', f'<b>{sum(n for n, p in TIERS)}</b>', '', f'<b>{sum(n * p for n, p in TIERS):,} USDT</b>'])
    return f'''{phero("ticket", "Ranks and Lucky Tickets",
        "The last two shares, 5% each: rank pools for qualified members, and a prize draw every time the pool reaches 5,000 USDT.",
        [("award", "Nexus and Legacy Crown"), ("ticket", "250 winning tickets per draw"), ("circle-play", mmss(V["e5"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack">
 <h2 class="h2">Two ranks</h2>
 {table(["Rank", "Package", "To qualify (from the ALTRUVA presentation)"], [["<b>Nexus</b>", "Builder, $50", "Hold at least $50, plus 2 directs of $50 or more within 3 days"], ["<b>Legacy Crown</b>", "Elite, $100", "Hold $100, plus 2 directs of $100 or more within 3 days"]], caption="Ranks")}
 <p class="fine">The 3 days start when you join: see <a class="inl" href="{A("dashboard/first-72-hours/", here)}">Your first 72 hours</a>. Rank pools are shared among everyone who holds that rank. You claim your share from Overview, like the global leg and matching. The split between the two pools isn't shown in the app, so we don't state it.</p>
</div>{vid("e5", here)}</div>""")}
{sec(f"""<div class="grid2 tick-grid"><div class="stack">
 {table(["Tier", "Tickets", "Prize", "Paid out"], tier_rows, caption="Lucky Ticket prize tiers per draw")}
 <p class="how num">Each time the Jackpot Pool reaches 5,000 USDT, a draw shares 4,000 USDT among 250 tickets picked at random. The app doesn't say where the other 1,000 goes.</p>
</div><div class="stack">
 {table(["Package", "Tickets"], [["Starter", "1, once 2 directs join within 3 days"], ["Builder", "1"], ["Elite", "2"], ["Reinvestment", "None"]], caption="Tickets per package")}
 <figure class="ticket"><img src="{A("img/mtg-lucky-ticket-won.webp", here)}" width="529" height="342" loading="lazy" alt="MTG's own Lucky Ticket card showing WON 25.00 USDT in Draw 16, ticket ID hidden"><figcaption class="fine">A real one: one of my two tickets won 25 USDT in Draw 16. The other expired without a prize. Ticket ID hidden.</figcaption></figure>
</div></div>""", "Lucky Tickets", "Each ticket enters one draw, then it expires. A prize goes to your wallet in full: no split, no reinvest.")}
{sec(think("Is this a jackpot?", "<p>No. Think of a raffle at a school fun day: everyone gets tickets, a few win small prizes. Most tickets don't win, so never count on a prize. " + play_btn("t4", "See how to claim a prize") + "</p>"))}
'''


# ======================================================================= WITHDRAW
def p_wd(here):
    return f'''{phero("wallet", "Withdraw and reinvest",
        "Every withdrawal takes your whole balance and splits it automatically: part to your wallet, part reinvested.",
        [("percent", "50/50 up to 5,000"), ("hand-coins", "Claim first"), ("circle-play", mmss(V["e6"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack">
 <h2 class="h2">The split, by total deposit</h2>
 {table(["Your total deposit", "To your wallet", "Reinvested"], [["Up to 5,000 USDT", "<b>50%</b>", "50%"], ["5,001 to 49,999 USDT", "<b>60%</b>", "40%"], ["50,000 USDT and up", "<b>70%</b>", "30%"]], hl=0, caption="Withdrawal split")}
 <p class="fine">Total deposit means your fresh packages plus everything reinvested. You can't choose the split, and you can't withdraw part of your balance.</p>
 <p class="how num">My real withdrawal: a balance of 23.63 USDT became <b>11.81 to my wallet</b> and 11.81 reinvested. With a total deposit of 6,000, a 200 withdrawal becomes 120 to your wallet and 80 reinvested.</p>
 <div class="btn-row"><a class="btn btn-blue btn-sm" href="{A("dashboard/tools/withdraw-split-calculator/", here)}">{ic("percent")}<span class="lbl">Withdraw Split Calculator</span></a></div>
</div>{vid("e6", here)}</div>""")}
{sec(steps([
    ("Claim", "<p>Move global leg, matching and rank income into your balance. Working level income is already there.</p>" + play_btn("t5")),
    ("Withdraw everything", "<p>One tap takes the whole balance. The split happens on its own, and the network fee is a few cents of BNB.</p>"),
    ("Check your wallet", "<p>Your share lands in SafePal as USDT. From there you can cash out to your bank.</p>" + play_btn("t6")),
]), "Claim first, then withdraw", "Only claimed income is in your balance. Lucky Ticket prizes are the exception: they go to your wallet in full.")}
{sec(f"""<div class="stack">
{think("Is the reinvested part a fee?", "<p>No. It goes back in as new business: it grows your total deposit and pays working levels and matching to your uplines, like fresh money. But it never changes your package, it gives no Lucky Tickets, and you can't take it back out.</p>")}
{think("How often should I withdraw?", "<p>That's up to you. My own tip from Tutorial 5: withdraw regularly, because taking your profits out lowers your risk. Only use money you can afford to lose.</p>", alt=True)}
</div>""")}
'''
