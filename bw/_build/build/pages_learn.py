"""Dashboard pages: Start here + How it works (Bitcoin Wealth)."""
from core import *
from pages_land import matrix, flow_stage, why_grid, scorecard


def phero(icon, title, lead, chips_=(), pcls='', extra=''):
    ch = chips(*chips_) if chips_ else ''
    return (f'<section class="phero"><div class="wrap"><div class="phero-in">{ped(icon, "lg " + pcls)}<div>'
            f'<h1 class="h1">{title}</h1><p class="lead">{lead}</p>{ch}{extra}</div></div></div></section>')


def honest(title, body):
    """a calm info note (MTG, 9 Nov 2026: inform, never frighten)"""
    return f'<div class="note">{ic("info")}<div><b>{title}</b> {body}</div></div>'


def soon(code, compact=False):
    """a planned video, shown honestly as coming soon (never playable)"""
    p = {x[0]: x for x in PLANNED}[code]
    return (f'<div class="soon glass{" sm" if compact else ""}"><span class="sbadge">{ic("clock")}Coming soon</span>'
            f'<b>{p[1]} {code[1:]}: {p[2]}</b><small>{p[3]}</small></div>')


def src_fact(t):
    return f'<p class="srcf">{ic("file-text")}<span><b>From the programme\'s own presentation.</b> {t}</span></p>'


FAQ_BACK = "dashboard/faq/"


# ======================================================================= WELCOME
def p_home(here):
    tiles = ''.join(f'<button type="button" class="vtile" data-play="{k}" data-vid="{k}" title="{esc(V[k]["desc"])}">'
                    f'<span class="vn">{V[k]["n"]}</span><span class="vt">{V[k]["short"]}</span>{ic("circle-check")}</button>' for k in TUT)
    tiles += ''.join(f'<span class="vtile off" title="{esc(p[3])}"><span class="vn">{p[0][1:]}</span><span class="vt">{p[2]}</span><small>Soon</small></span>'
                     for p in PLANNED if p[0][0] == 't')
    etiles = ''.join(f'<span class="vtile off" title="{esc(p[3])}"><span class="vn">{p[0][1:]}</span><span class="vt">{p[2]}</span><small>Soon</small></span>'
                     for p in PLANNED if p[0][0] == 'e')
    route = steps([
        ('Check the fit', f'<p>Start honest. <a class="inl" href="{A("dashboard/is-it-right-for-me/", here)}">Is it right for me?</a> takes two minutes.</p>'),
        ('Understand the idea', f'<p><a class="inl" href="{A("dashboard/what-is-bitcoin-wealth/", here)}">What is Bitcoin Wealth?</a> Bitcoin, BTCB and the smart contract, in plain words.</p>'),
        ('See how it pays', f'<p><a class="inl" href="{A("dashboard/how-it-works/", here)}">The 14 positions</a>, then <a class="inl" href="{A("dashboard/12-slots/", here)}">the 12 slots</a>. Watch the positions fill.</p>'),
        ('Compare it honestly', f'<p>Against <a class="inl" href="{A("dashboard/stokvel/", here)}">a stokvel</a> and against the newer copycats, then <a class="inl" href="{A("dashboard/check-it-yourself/", here)}">check it yourself</a> on BscScan.</p>'),
        ('Join step by step', f'<p>SafePal first (Tutorial 1 is ready), then BNB, BTCB and slot 1. <a class="inl" href="{A("dashboard/join/", here)}">Open the join guide</a>.</p>'),
        ('Meet the community', f'<p>Live on <a class="inl" href="{A("dashboard/live-on-zoom/", here)}">Zoom</a> five evenings a week, and every day in the MTG TRIBE.</p>'),
        ('Teach someone else', f'<p>We learn best when we teach others. Share this guide, or get your own <a class="inl" href="{A("dashboard/bw-tribe-page/", here)}">BW Tribe Page</a> with your link inside.</p>'),
    ])
    return f'''{phero("compass", "Welcome. Here's your route.",
        "Take it one stop at a time. Watch every video, even if you think you already know Bitcoin Wealth. Come back to any page as often as you like, until you get it.",
        [("users", f"{MEMBERS} member IDs ({CHECKED})"), ("badge-check", "0.001 BTC once-off"), ("info", "Independent, not official")])}
{sec(f"""<div class="panel pad prog-panel glass"><div class="prog">
 <div class="pring" data-ring><svg viewBox="0 0 118 118" aria-hidden="true"><defs><linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="#3fc11f"/><stop offset="1" stop-color="#ffa101"/></linearGradient></defs><circle class="bg" cx="59" cy="59" r="50"/><circle class="fg" cx="59" cy="59" r="50"/></svg>
 <div class="val"><b data-k="n">0</b><small>of {NV} watched</small></div></div>
 <div class="stack"><div><h2 class="h3">Your progress</h2><p class="fine">Tap a video to play it. A tick appears when you finish one. Progress is saved on this device only. New videos appear here as they're released.</p></div>
 <p class="vgl">Tutorials</p><div class="vgrid">{tiles}</div><p class="vgl">Explainers</p><div class="vgrid">{etiles}</div></div>
</div></div>""", id="progress")}
{sec(route, "Your route, in order", "Seven stops. Each one builds on the last, so go in order the first time.")}
{sec(f"""<div class="grid3">
 {box("The menu", "<p>Every page is in the menu, grouped in the order you'll need it. On a phone, tap <b>Menu</b> at the top.</p>", "panel-left")}
 {box("Next and Previous", "<p>The buttons at the bottom of each page walk you through everything in order. You'll never get lost.</p>", "route")}
 {box("Sign Up", "<p>The button copies MTG's link and opens nothing. Paste it into SafePal's browser when you're ready.</p>", "copy")}
</div>""", "How to use this dashboard")}
{sec(f"""<div class="stack">{think("Do I have to learn everything before I start?",
    "<p>No. But don't go in blind either. Learn enough to explain it honestly to someone else, then keep learning as you go and put each lesson into practice.</p>")}
{think("Is there a live presentation I can attend?",
    f"<p>Yes, five evenings a week in four languages. Ask the person who invited you to add you to the WhatsApp group, or join the MTG TRIBE. <a class='inl' href='{A('dashboard/live-on-zoom/', here)}'>See the Zoom schedule</a>.</p>", alt=True, icon="video")}</div>""")}
'''


# ======================================================================= FIT
def p_fit(here):
    qs = [
        ('afford', 'I could lose the 0.001 BTC entry (plus fees) without it hurting my rent, food or family.'),
        ('phone', 'I have a smartphone and can install a wallet app like SafePal.'),
        ('learn', 'I\'ll learn how the 14 positions and the 12 slots work before I join.'),
        ('risk', 'I understand payouts depend on new members filling positions, and nothing is guaranteed.'),
        ('teach', 'I\'d only share Bitcoin Wealth once I can explain it honestly, risks included.'),
    ]
    rows = ''.join(f'<label class="fit-q"><input type="checkbox" data-fit="{k}"><span class="tg" aria-hidden="true"></span><span>{t}</span></label>' for k, t in qs)
    return f'''{phero("scale", "Is Bitcoin Wealth right for you?",
        "An honest fit check before anything else. No pressure: not joining is a perfectly good answer.")}
{sec(f"""<div class="calc fitcheck"><div class="form panel pad glass" data-fitcheck><h2 class="h3">Tick what's true for you</h2>{rows}</div>
<div class="result" aria-live="polite"><div class="rbig"><small>Your fit check</small><b data-k="score">0 of 5</b></div><p data-k="msg">Tick the statements that are true for you.</p></div></div>""",
    "Five honest questions")}
{sec(f"""<div class="grid2">
 {box("It may suit you if", checks(["You want to collect Bitcoin's value together with other people.", "You like a small, once-off start: 0.001 BTC plus network fees.", "You want payouts in your own wallet, with every payment public.", "You're willing to learn, share honestly and give it time."]), "thumbs-up")}
 {box("It's probably not for you if", checks(["You need this money for rent, food, school fees or debt.", "You're looking for a fixed or promised return.", "You won't introduce anyone. Two business partners switch on your progress.", "You'd pressure friends or family to join."], no=True), "ban")}
</div>""", "Who it suits, and who it doesn't")}
{sec(f"""<div class="panel pad flow glass">
 <div class="flowrow"><span class="fnode">{ic("users")}Members activate slots</span>{ic("arrow-right", "ic farrow")}<span class="fnode gold">{ic("blocks")}Bitcoin Wealth smart contract</span>{ic("arrow-right", "ic farrow")}<span class="fnode">{ic("wallet")}Members' own wallets</span></div>
 <p class="lead">That's the whole money flow, in the open. No product, trading or mining is involved: <b>payouts come from members activating slots</b>, so they grow as the community grows.</p>
</div>""", "Where the money comes from")}'''


# ======================================================================= WELCOME BACK
def p_back(here):
    return f'''{phero("heart-handshake", "Welcome back. Take a fresh look.",
        "Maybe you scrolled past. Maybe you tried and felt stuck. Maybe you left for something newer. Whichever it is, this page is for you.")}
{sec(f"""<div class="grid3">
 <div class="aud glass">{ped('eye')}<h3 class="h3">If you ignored it</h3><p>Give it ten minutes. Watch one payment move, see the 14 positions fill, then open BscScan and check it yourself. Decide on what you see, not on what anyone says.</p></div>
 <div class="aud glass">{ped('rotate-ccw')}<h3 class="h3">If you felt stuck</h3><p>Progress starts when your first two business partners join. That can take longer than you expect. This time: learn it properly, share it honestly, and give it more time.</p></div>
 <div class="aud glass">{ped('house')}<h3 class="h3">If you left</h3><p>Bitcoin Wealth is still here, still running, with every payment on chain. Members who tried newer platforms are coming back, MTG included.</p></div>
</div>""", "Wherever you're coming from")}
{sec(f"""<div class="facts4">
 <div class="fact glass"><b class="num"><span data-count="41013">{MEMBERS}</span></b><small>member IDs on the contract</small></div>
 <div class="fact glass"><b class="num">{ON_CHAIN_SINCE}</b><small>on chain since</small></div>
 <div class="fact glass"><b class="num">0.001 BTC</b><small>the only slot you pay for</small></div>
 <div class="fact glass"><b class="num">48</b><small>payouts to members' wallets in 15 hours</small></div>
</div><p class="fine center">Read from the contract on {CHECKED}. <a class="inl" href="{A('dashboard/check-it-yourself/', here)}">How to check these yourself</a>.</p>""",
    "What's still true today")}
{sec(f"""<div class="grid2">
 {box("Before you jump on the next new thing", "<p>New platforms appear every month, many of them copies with a new name. Before you put a cent anywhere, run the same five checks on every one of them, Bitcoin Wealth included.</p>" + f'<p><a class="inl" href="{A("dashboard/what-makes-it-different/", here)}">The 5-point check</a></p>', "search-check")}
 {box("This time, a real plan", checks(["Learn the 14 positions and 12 slots first", "Set up your wallet properly (Tutorial 1)", "Introduce two business partners, honestly", "Join a Zoom session and ask questions", "Give it months, not days"]), "list-checks")}
</div>""", "Give it a proper try")}'''


# ======================================================================= WHAT IS BITCOIN WEALTH
def p_what(here):
    return f'''{phero("bitcoin", "What is Bitcoin Wealth?",
        "A community way to collect Bitcoin's value. A smart contract on BNB Smart Chain takes each member's slot payment and sends it straight to other members' wallets, by fixed rules, in public.",
        [("badge-check", "0.001 BTC once-off"), ("wallet", "Wallet to wallet"), ("scan-search", "Public on BscScan")])}
{sec(flow_stage(here), "The idea in four moves", "Tap a step to see it.")}
{sec(f"""<div class="grid2">
 {box("Bitcoin is the money", "<p>Bitcoin is digital money with no bank behind it. It started in January 2009, after the 2008 financial crisis. Only 21 million will ever exist, and every four years the halving cuts how many new ones are made. That's why people call it digital gold.</p>", "bitcoin")}
 {box("Bitcoin Wealth is a program", "<p>Bitcoin Wealth is not a coin. It's a smart contract: code that runs on BNB Smart Chain and moves Bitcoin's value between members by fixed rules. The engine is called Vow Unity.</p>", "blocks")}
 {box("BTCB is Bitcoin's value on BNB Smart Chain", "<p>The contract pays in BTCB, a token that tracks Bitcoin one to one and is backed by Bitcoin held by Binance. It is not Bitcoin on the Bitcoin network, but it can be swapped for Bitcoin.</p>", "coins")}
 {box("BNB pays the fees", "<p>Every action on BNB Smart Chain costs a small network fee, paid in BNB. Keep a little BNB in your wallet, or nothing will move. Think of it as the postage stamp.</p>", "fuel")}
</div>""", "Four words that make it click")}
{sec(f"""<div class="panel pad glass"><div class="cmp2">
 <div><h3 class="h3">{ic('bitcoin')}Bitcoin</h3><p>The money. Lives on its own blockchain. You can buy it, hold it and send it.</p></div>
 <div><h3 class="h3">{ic('blocks')}Bitcoin Wealth</h3><p>A set of rules in code. It doesn't create Bitcoin. It moves members' BTCB from one wallet to another, the moment a slot is activated.</p></div>
</div></div>
{honest("Where the money comes from.", "Every payout is another member's slot payment, moved wallet to wallet by the contract. No product, trading or mining is involved.")}""",
    "Bitcoin vs Bitcoin Wealth")}
{sec(f"""<div class="stack">{soon('e1')}<p class="fine">Want the Bitcoin basics first? MTG's free <a class="inl" href="{esc(CRYPTO101)}" target="_blank" rel="noopener">Crypto 101 crash course</a> has 15 short lessons.</p></div>""", "Watch it explained")}'''


# ======================================================================= THE 14 POSITIONS
def p_hiw(here):
    rows = [[f'<b>{n}</b>', str(c1), str(cn)] for (n, c1, _), (_, cn, _) in zip(CYCLE1, CYCLEN)]
    rows[2][0] = '<b>Your next slot</b> (first cycle) / <b>Royal Pool</b> (later)'
    return f'''{phero("network", "The 14 positions",
        "Below you sit 2, then 4, then 8 positions: 14 in all. Each position is one member paying the slot price, and each one produces one payment. Here's where all fourteen go.",
        [("users", "2 + 4 + 8 = 14"), ("wallet", "6 to your wallet"), ("arrow-up", "2 buy your next slot")])}
{sec(matrix(here), "Watch the positions fill", "Then switch between the first cycle and later cycles.")}
{sec(table(["Where the payment goes", "First cycle", "Later cycles"], rows + [["<b>Total</b>", "14", "14"]], hl=1, caption="Where the 14 payments go") +
     src_fact("Cycle 1: 2 to your upline, 6 to your wallet, 2 to your next slot, 3 to members below you, 1 recycles you. Later cycles: 7 to your wallet and 1 to the Royal Pool instead of the next slot."),
     "All fourteen, in one table")}
{sec(f"""<div class="grid3">
 {box("Nine point to you", "<p>6 to your wallet, 2 buy your next slot and 1 recycles you. That's why the programme says each slot can pay nine times its price.</p>", "target")}
 {box("No withdraw button", "<p>The contract splits each payment in the same transaction and sends it to the members' own wallets. You don't request anything.</p>", "zap")}
 {box("Spillover", "<p>Positions below you can be filled by people you didn't introduce, when your upline's team overflows. It changes who fills a seat, not that someone has to.</p>", "git-merge")}
</div>""", "Three things to remember")}
{sec(honest("How a cycle completes.", "Each of the 14 positions is filled by a member taking that seat, whether you introduced them or spillover brings them. That's why sharing and teaching others matter.") + soon('e2'), "Good to know")}'''


# ======================================================================= THE 12 SLOTS
def p_slots(here):
    cells = ''.join(f'<div class="slotc glass{" one" if i == 0 else ""}" style="--i:{i}"><small>Slot {i + 1}</small><b>{s:g} BTC</b><em>{"You pay this once" if i == 0 else "Auto entry"}</em></div>'
                    for i, s in enumerate(SLOTS))
    return f'''{phero("layers", "The 12 slots, and the once-off",
        "Twelve slots, each double the one before, from 0.001 BTC to 2.048 BTC. You pay for slot 1 only. Every slot above it is bought for you from the cycle below, once that cycle fills.",
        [("badge-check", "You pay 0.001 BTC once"), ("layers", f"Full ladder {LADDER} BTC"), ("refresh-cw", "Slots never expire")])}
{sec(f'<div class="ladder">{cells}</div>' + src_fact(f"Slot 1 is a plain entry. Slots 2 to 12 are marked Auto Entry: each is bought with two of the fourteen payments from your first cycle at the slot below. The full ladder totals {LADDER} BTC."),
     "Every slot, side by side")}
{sec(f"""<div class="grid2">
 {box("Your own outlay", "<p><b>0.001 BTC plus network fees.</b> That's it. You never pay again to move up the slots. MTG's point: it's a once-off, not a subscription.</p>", "badge-check")}
 {box("What moves you up", "<p>Auto entry buys slot 2 when your slot 1 cycle fills with 14 members. Your first two business partners and spillover from above fill it.</p>", "arrow-up")}
</div>
<div class="btn-row center-row"><a class="btn btn-gold ring" href="{A('dashboard/tools/slot-calculator/', here)}">{ic('calculator')}<span class="lbl">See every slot in rand</span></a></div>""",
    "What it costs you")}
{sec(soon('e3'), "Watch it explained")}'''


# ======================================================================= RECYCLING AND ROYAL POOL
def p_pool(here):
    return f'''{phero("refresh-cw", "Recycling and the Royal Pool",
        "When a cycle completes, one payment puts you back into the same slot, so it can pay again. From your second cycle at a slot, the split changes slightly.",
        [("wallet", "7 to your wallet"), ("crown", "1 to the Royal Pool"), ("refresh-cw", "1 recycles you")])}
{sec(matrix(here), "First cycle vs later cycles", "Switch to Later cycles: your next slot is already bought, so one payment moves to your wallet and one to the Royal Pool.")}
{sec(f"""<div class="grid2">
 {box("Recycling", "<p>Position 14 places you at the bottom of a fresh cycle at the same slot. The programme says there's no limit on recycles and no expiry on slots.</p>", "refresh-cw")}
 {box("The Royal Pool", "<p>In later cycles, one payment goes to the Royal Pool, held in the contract. Members who reach slot 3 and qualify by the 21st share it on the last day of the month.</p>", "crown")}
</div>""" + honest("Good to know.", f"The monthly Royal Pool rules come from a member's written explanation, not the deck itself. The pool waits in the contract until month-end. <a class='inl' href='{A('dashboard/check-it-yourself/', here)}'>See what the contract allows</a>.") ,
    "Two ideas, plainly")}'''


# ======================================================================= STOKVEL
def p_stokvel(here):
    rows = [
        ['Can you see every payment?', 'Only if the treasurer shows you', '<b>Yes</b>, on BscScan, forever'],
        ['Who holds the money?', 'A treasurer or a bank account', '<b>Members\' own wallets</b> (the Royal Pool waits in the contract)'],
        ['Who takes a cut?', 'Bank fees, sometimes more', '<b>Only small network fees</b>'],
        ['What does it pay in?', 'Rand', '<b>BTCB</b>, Bitcoin\'s value'],
        ['How much do you put in?', 'Every month, for the whole cycle', '<b>0.001 BTC, once</b>'],
        ['How are payouts funded?', 'Members take turns with the same pot', 'Members activating the positions below you'],
    ]
    return f'''{phero("users", "Better than a stokvel?",
        "Stokvels are trusted by millions of South Africans, and for good reason. Bitcoin Wealth shares the spirit: ordinary people pooling, no bank in the middle. Here's where it does better, and how each one is funded.")}
{sec(scorecard(), "Side by side")}
{sec(f"""<div class="grid2">
 {box("Where Bitcoin Wealth wins", checks(["Transparency: every payment public, nobody has to be trusted to report it", "Peer to peer: payouts go straight to members' wallets", "No middleman holding the pot, no bank charges", "One small entry instead of monthly contributions", "Priced in Bitcoin's value, not rand"]), "trophy")}
 {box("How each one is funded", checks(["A stokvel is a closed circle: the same members take turns with the same pot", "Bitcoin Wealth is open: each cycle is completed by members activating the positions below you", "So it grows as the community grows, which is why teaching others matters"]), "info")}
</div>""", "The verdict")}
{sec(soon('e4'), "Watch it explained")}'''


# ======================================================================= WHAT MAKES IT DIFFERENT
def p_diff(here):
    five = [
        ('clock', 'How long has it been running?', f'Bitcoin Wealth\'s contract has been on chain since {ON_CHAIN_SINCE}, with {MEMBERS} member IDs by {CHECKED}. Ask the same of any newer platform.'),
        ('file-code', 'Is the contract public?', 'Open the address on BscScan. You can read the transactions, the token transfers and the contract itself.'),
        ('wallet', 'Who holds the money?', 'In Bitcoin Wealth, slot payments go straight to members\' own wallets in the same transaction. A platform where money sits in a dashboard balance is a different design.'),
        ('user-cog', 'Can an admin change the rules or move funds?', 'Be honest about this one. Bitcoin Wealth\'s contract has an owner wallet with an emergency withdrawal for what the contract holds. Check every platform for the same.'),
        ('scan-search', 'Can you see real payments?', 'Yes: every activation and every payout is a public transaction. If a platform can\'t show you this, walk away.'),
    ]
    items = ''.join(f'<li class="chk5 glass">{ped(i)}<div><h3 class="h3">{n + 1}. {q}</h3><p>{a}</p></div></li>' for n, (i, q, a) in enumerate(five))
    return f'''{phero("sparkles", "What makes Bitcoin Wealth different",
        "New smart contract platforms appear all the time, many of them copies with a new name. We don't name them. We give you five checks that work on any of them, and show how Bitcoin Wealth does on each.")}
{sec(why_grid(), "What Bitcoin Wealth gets right", "Members who tried the newer, shinier platforms keep coming back, MTG included. These are the reasons, and every one can be checked.")}
{sec(f'<ol class="five">{items}</ol>', "The 5-point check")}
{sec(f"""<div class="grid2">
 {box("The original", f"<p>MTG calls Bitcoin Wealth the original: priced in Bitcoin, paid wallet to wallet, open on BscScan, and still running. {MEMBERS} member IDs say people keep choosing it.</p>", "award")}
 {box("Don't trust. Verify.", f"<p>You don't have to believe MTG or anyone else. Every claim on this page can be checked in a few minutes. <a class='inl' href='{A('dashboard/check-it-yourself/', here)}'>Here's how</a>.</p>", "scan-search")}
</div>""", "Why that matters")}'''


# ======================================================================= CHECK IT YOURSELF
def p_proof(here):
    return f'''{phero("scan-search", "Check it yourself",
        "Don't take anyone's word for it, including MTG's. Bitcoin Wealth runs on a public blockchain, so you can look at the contract and every payment yourself. Here's what we found, and how to find it.",
        [("calendar", f"Checked {CHECKED}"), ("blocks", "BNB Smart Chain")])}
{sec(f"""<div class="addr glass"><small>The Bitcoin Wealth contract (from the programme's own deck)</small><code>{CONTRACT}</code>
<div class="btn-row"><button type="button" class="btn btn-ghost btn-sm" data-copy="contract">{ic('copy')}<span class="lbl">Copy address</span><span class="copied" aria-live="polite">Copied ✓</span></button>
<a class="btn btn-gold btn-sm" href="{esc(BSCSCAN)}" target="_blank" rel="noopener">{ic('external-link')}<span class="lbl">Open on BscScan</span></a></div>
<p class="fine">Tip: type it into bscscan.com yourself rather than trusting a link someone sends you.</p></div>""", "The address")}
{sec(f"""<div class="facts4">
 <div class="fact glass"><b class="num">{MEMBERS}</b><small>member IDs (the contract's own counter)</small></div>
 <div class="fact glass"><b class="num">41.009 BTC</b><small>the contract's own total counter</small></div>
 <div class="fact glass"><b class="num">{CREATED}</b><small>contract created</small></div>
 <div class="fact glass"><b class="num">46 of 63</b><small>payments in 15 hours paid straight on, same transaction</small></div>
</div>
<p class="fine center">Read directly from BNB Smart Chain on {CHECKED} (13 Nov 22:55 to 14 Nov 13:55 UTC for the payment sample). The other 17 stayed in the contract, which is where the Royal Pool is held.</p>""",
    "What the blockchain showed")}
{sec(steps([
    ('Open the contract on BscScan', '<p>Paste the address into bscscan.com. The Transactions tab lists every activation.</p>'),
    ('Open one recent transaction', '<p>Look at "ERC-20 Tokens Transferred". One activation of 0.001 BTCB shows the payment going on to a member\'s wallet in the same transaction.</p>'),
    ('Check the Token Holdings', '<p>The contract holds some BTCB: that\'s the Royal Pool waiting for its monthly payout.</p>'),
    ('Read the Contract tab', '<p>Look for functions only the owner can use. Knowing them is part of doing your own research.</p>'),
]), "Four steps, five minutes")}
{sec(honest("What the code allows.", "The contract has an owner wallet (the wallet that created it). It is not renounced. That wallet can switch on an emergency mode and withdraw tokens the contract holds, change the token address and pool addresses, and update a member's slots. BTCB in your own wallet stays under your keys, so approve only the exact amount when you activate a slot. We show you all this because you deserve the full picture.") +
     f'<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{esc(BSCSCAN_BTCB)}" target="_blank" rel="noopener">{ic("external-link")}<span class="lbl">BTCB held by the contract</span></a></div>' + soon('e5'),
    "The full picture")}'''
