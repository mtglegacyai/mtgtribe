"""Dashboard pages: Get started, Your own page, Tools, Help, More (Bitcoin Wealth), plus the order form."""
from core import *
from pages_learn import phero, honest, soon


# ======================================================================= JOIN
JOIN_NEEDS = ['A smartphone with the SafePal app', '0.001 BTC worth of BTCB, plus a little extra', 'A little BNB for network fees',
              'A VALR or Binance account to buy with rand', 'The sign-up link of the person who introduced you']
JOIN_STEPS = [
    ('Set up SafePal', 'Download SafePal from safepal.com, create a wallet, back it up two ways and keep only BNB, USDT and BTCB. Tutorial 1 shows every tap.'),
    ('Open a VALR or Binance account', 'Both let you buy crypto with rand. Many members keep both, as a backup.'),
    ('Buy BNB and send it to SafePal', 'Buy enough BNB for 0.001 BTC plus fees, then withdraw it to your SafePal BNB address on BNB Smart Chain (BEP20). Send a small test first. Tutorial 2 shows every tap.'),
    ('Swap BNB to BTCB in SafePal', 'Swap most of it to BTCB, and keep a little BNB for network fees. Never empty your BNB.'),
    ('Activate slot 1', 'Copy the sign-up link, paste it into SafePal\'s browser, connect your wallet, approve the exact amount and activate slot 1.'),
]

T2_CHECKS = ["Pay by EFT from a bank account in your own name", "Type your VALR reference exactly as VALR shows it: it is how VALR knows the money is yours",
             "Buy BNB with your rand", "Withdraw to your SafePal BNB (BEP20) address on BNB Smart Chain, and check the first and last characters"]


def p_join(here):
    st = steps([(t, f'<p>{d}</p>') for t, d in JOIN_STEPS])
    return f'''{phero("rocket", "Join step by step",
        "Three stages, five steps, from an empty phone to slot 1. Take them one at a time, and watch the tutorial for each before you tap anything.",
        [("badge-check", "0.001 BTC once-off"), ("clock", "About 30 minutes"), ("smartphone", "All on your phone")])}
{sec(f"""<div class="two vstart"><div class="stack"><h2 class="h3">What you need</h2>{checks(JOIN_NEEDS)}
<p class="fine">On the recording day of Tutorial 1, Bitcoin was about $67,000, so 0.001 BTC was about $67. With fees and a little BNB, MTG suggested preparing <b>about $76, about R1,300</b>. Prices move every minute: <a class="inl" href="{A('dashboard/tools/bitcoin-to-rand/', here)}">check today's price in rand</a>.</p>
<div class="btn-row">{valr_btn()}{binance_btn()}</div></div>
<div class="phone-wrap">{vid('t1', here)}</div></div>""", "Before you start")}
{sec(st, "The five steps")}
{sec(f"""<div class="two vstart"><div class="stack"><h2 class="h3">Tutorial 2: {V['t2']['title']}</h2><p>Steps 2 and 3, tap by tap. {V['t2']['desc']}</p>
{checks(T2_CHECKS)}
<div class="btn-row">{valr_btn()}{binance_btn()}</div></div>
<div class="phone-wrap">{vid('t2', here)}</div></div>""", "Fund your SafePal")}
{sec(f'<div class="grid2">{soon("t3")}</div>', "Tutorial 3", "Swapping to BTCB, signing up and activating slot 1, recorded on MTG's phone, is on the way. Meanwhile, ask in the MTG TRIBE.")}
{sec(honest("Before you activate.", "Approve only the exact amount you are paying, keep a little BNB for fees, and if someone else introduced you, use their link so they stay your sponsor."))}'''


# ======================================================================= VIDEOS
def p_tut(here):
    return f'''{phero("circle-play", "Tutorial videos",
        "Step-by-step trainings recorded on MTG's own phone, with every private detail hidden. Pause after each step and try it yourself.",
        [("film", f"{len(TUT)} ready, 1 on the way"), ("eye-off", "Private details hidden")])}
{sec(f"""<div class="two vstart"><div class="stack"><h2 class="h3">Tutorial 1: {V['t1']['title']}</h2><p>{V['t1']['desc']}</p>
{checks(["Download from safepal.com, never from a link in a message", "Two backups: Google Drive and paper", "Rename the wallet Bitcoin Wealth", "Keep only BNB (BEP20), USDT (BEP20) and BTCB (BEP20)"])}</div>
<div class="phone-wrap">{vid('t1', here)}</div></div>""")}
{sec(f"""<div class="two vstart"><div class="stack"><h2 class="h3">Tutorial 2: {V['t2']['title']}</h2><p>{V['t2']['desc']}</p>
{checks(T2_CHECKS)}
<p>Using Binance instead? The steps are very similar.</p>
<div class="btn-row">{valr_btn()}{binance_btn()}{wa_group_btn(size='sm')}</div></div>
<div class="phone-wrap">{vid('t2', here)}</div></div>""")}
{sec(f'<div class="grid2">{soon("t3")}</div>', "Coming next")}
{sec(think("Do I really need to watch them all?", "<p>Yes, even if you think you already know. Each one shows a screen you'll meet sooner or later. Then share them: we learn best when we teach others.</p>"))}'''


def p_exp(here):
    cards = ''.join(soon(p[0]) for p in PLANNED if p[0][0] == 'e')
    return f'''{phero("film", "Explainer videos",
        "Short animated explainers, one idea at a time, in MTG's voice. They're being made now. Until they're ready, every page in How it works shows the same idea with live diagrams.",
        [("film", "5 explainers on the way"), ("triangle-alert", "Risks included")])}
{sec(f'<div class="grid2">{cards}</div>', "On the way")}
{sec(f"""<div class="grid3">
 {box("The 14 positions", f"<p>Watch the positions fill, live. <a class='inl' href='{A('dashboard/how-it-works/', here)}'>Open</a></p>", "network")}
 {box("The 12 slots", f"<p>Every slot and the once-off. <a class='inl' href='{A('dashboard/12-slots/', here)}'>Open</a></p>", "layers")}
 {box("Better than a stokvel?", f"<p>The honest scorecard. <a class='inl' href='{A('dashboard/stokvel/', here)}'>Open</a></p>", "users")}
</div>""", "Meanwhile, see it live")}'''


# ======================================================================= ZOOM
def p_zoom(here):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    grid = ''
    for d in days:
        sess = [z for z in ZOOM if z[0] == d]
        cells = ''.join(f'<span class="zs{" eve" if t != "14:00" else ""}"><b>{t}</b>{lang}</span>' for _, t, lang in sorted(sess, key=lambda z: z[1]))
        grid += f'<div class="zday glass"><h3>{d}</h3>{cells}</div>'
    return f'''{phero("video", "Live on Zoom",
        "Meet the community, ask anything and watch it explained live. Weekdays at 14:00, and five evenings a week in four languages.",
        [("clock", "South African time (SAST)"), ("languages", "English, isiXhosa, isiZulu, Sesotho")])}
{sec(f'<div class="zgrid">{grid}</div><p class="fine center">The 14:00 sessions are in English, and questions are welcome in any language, like isiZulu.</p>', "The weekly schedule")}
{sec(f"""<div class="joinband glass"><div><h2 class="h3">How to get the Zoom link</h2><p>{ZOOM_LINE.replace(" below this video", "")} Links are only shared inside the group, never in public.</p></div>
<div class="btn-row">{wa_group_btn(label='Join the MTG TRIBE', ring=True)}</div></div>""")}'''


# ======================================================================= BW TRIBE PAGE
def p_page(here):
    return f'''{phero("globe", "Your own BW Tribe Page",
        "This whole website, with your name, your photo and your own Bitcoin Wealth link built in. One link to send to every potential business partner.",
        [("badge-check", "R1,000 once-off"), ("hand-coins", "Pay after it's built"), ("pencil", "5 free edits")])}
{sec(f"""<div class="grid3">
 {box("It does the explaining", "<p>Every tutorial, every diagram, every honest answer, ready day and night. Your potential business partners learn at their own pace.</p>", "presentation")}
 {box("Your link, everywhere", "<p>Every sign-up button copies <b>your</b> Bitcoin Wealth referral link. When someone pastes it into SafePal, they join under you.</p>", "link")}
 {box("Duplication, made easy", "<p>Your business partners can order theirs too. Same tools, same message, a team that grows the same way.</p>", "copy")}
</div>""", "Why every member needs one")}
{sec(f"""<div class="offer glass"><div class="offer-copy">
 <h2 class="h2">What you get</h2>
 {checks(["A full copy of this guide, kept up to date with new videos", "Your name and photo on it", "Your Bitcoin Wealth referral link on every sign-up button", "Your WhatsApp, WhatsApp group and social links", "Your choice of address: mtgtribe.com/bw/yourname or bitcoinwealthpays.com/yourname", "Five free edits to make it yours (from the sixth, a small fee depending on the size)"])}
 <div class="price"><b>R1,000</b><span>once-off<br><small>Pay in rand, USDT BEP20 or USDT TRC20. You agree the method with MTG on WhatsApp.</small></span></div>
 <div class="btn-row">{order_btn(size='lg')}</div>
</div><div class="offer-copy">
 <h2 class="h2">How it works</h2>
 {steps([("Fill in the order form", "<p>Two minutes. Your details go straight to MTG on WhatsApp.</p>"), ("MTG builds your page", "<p>You agree the payment method together on WhatsApp.</p>"), ("You check it", "<p>Love it? Then you pay. Changed your mind? MTG deletes it. Nothing to lose.</p>"), ("Share your one link", "<p>Send it to potential business partners, post it in your groups and on your socials.</p>")])}
</div></div>""", "Everything, up front")}
{sec(f"""<div class="lionrow"><div class="lion"><video data-deco autoplay muted loop playsinline preload="none" poster="{A('img/bitcoin-wealth-mascot-lion-bw.webp', here)}" width="540" height="960" aria-hidden="true"><source src="{L('media/bitcoin-wealth-mascot-lion-wave.mp4', here)}" type="video/mp4"></video></div>
<div class="secret glass big">{ic('lock-keyhole')}<div><b>The part we only tell owners</b><p>MTG uses a traffic source that makes it much easier to put a page like yours in front of people who already watch crypto ads all day. It has its own income stream too. No guarantee those visitors join. Once your BW Tribe Page is built, paid and yours, MTG shows you how it works, with its own tutorials and explainers.</p></div></div></div>""")}'''


# ======================================================================= TOOLS
def field(id_, label, unit, hint='', ph='', val=''):
    v = f' value="{val}"' if val else ''
    return (f'<div class="fl"><label for="{id_}">{label}</label><div class="inwrap"><input id="{id_}" class="field" type="text" '
            f'inputmode="decimal" autocomplete="off" placeholder="{ph}"{v} data-in="{id_}"><span class="unit">{unit}</span></div>'
            + (f'<span class="hint">{hint}</span>' if hint else '') + '</div>')


def ratebox():
    return (f'<p class="ratebox" data-out="status"><span>Loading the live Bitcoin price…</span></p>'
            f'<button type="button" class="btn btn-ghost btn-sm" data-refresh>{ic("refresh-cw")}<span class="lbl">Refresh the live price</span></button>')


def p_c_btc(here):
    amts = ['0.001', '0.002', '0.004', '0.008', '0.016', '0.1', '1']
    q = ''.join(f'<button type="button" data-amt="{a}" aria-pressed="{"true" if a == "0.001" else "false"}">{a}</button>' for a in amts)
    form = f'''<form class="form panel pad glass" data-btc novalidate onsubmit="return false">
<p class="lab">Quick amounts (BTC)</p><div class="seg presets wrapseg" role="group" aria-label="Quick amounts in BTC">{q}</div>
{field("btc", "Bitcoin", "BTC", "", "0.001", "0.001")}
{field("usd", "US dollars", "USD", "", "")}
{field("zar", "South African rand", "ZAR", "", "")}
<p class="fine" data-out="sats" aria-live="polite"></p>
{ratebox()}
{field("pz", "Price of 1 Bitcoin in rand", "ZAR", "Filled in from the live price. Type your exchange's price to use that instead.", "")}
<button type="button" class="btn btn-ghost btn-sm" data-reset>{ic("rotate-ccw")}<span class="lbl">Back to 0.001 BTC</span></button>
</form>'''
    notes = f'''<div class="grid2">{box("Type in any box", "<p>Type Bitcoin, dollars or rand, and the other two follow. 0.001 BTC is the Bitcoin Wealth entry for slot 1.</p>", "pen-line")}
{box("The final word", "<p>Live price: CoinGecko, when it loads. VALR and Binance show their own prices and fees, so your exchange screen is always the final word.</p>", "info")}</div>'''
    return f'''{phero("bitcoin", "Bitcoin to Rand Converter", "What is 0.001 BTC in rand right now? Type any amount in Bitcoin, dollars or rand.",
        [("refresh-cw", "Live price"), ("pen-line", "Or type your own")])}
{sec(f'<div class="calc one">{form}</div>')}
{sec(notes, sr='How the converter works')}'''


def p_c_slot(here):
    seg = ''.join(f'<button type="button" data-s="{i}" aria-pressed="{"true" if i == 1 else "false"}">{i}</button>' for i in range(1, 13))
    form = f'''<form class="form panel pad glass" data-slotcalc novalidate onsubmit="return false">
<p class="lab" id="slab">Choose a slot</p><div class="seg slots12" role="group" aria-labelledby="slab">{seg}</div>
{ratebox()}
{field("pz", "Price of 1 Bitcoin in rand", "ZAR", "Filled in from the live price. Type your own to test another price.", "")}
<div class="result" aria-live="polite">
 <div class="rbig"><small data-out="slot">Slot 1</small><b data-out="price">0.001 BTC</b><span data-out="pricez"></span></div>
 <div class="rrow"><span>Do you pay for it yourself?</span><b data-out="own"></b></div>
 <div class="rrow"><span>First full cycle: to your wallet (6 payments)</span><b><span data-out="c1"></span> <small data-out="c1z"></small></b></div>
 <div class="rrow"><span>First full cycle: 2 payments</span><b data-out="next"></b></div>
 <div class="rrow"><span>Each later cycle: to your wallet (7 payments)</span><b><span data-out="cn"></span> <small data-out="cnz"></small></b></div>
 <div class="rrow"><span>What has to be paid in by members</span><b data-out="paid"></b></div>
</div></form>'''
    return f'''{phero("calculator", "Slot Calculator", "Every Bitcoin Wealth slot in BTC and rand, and what a completed cycle sends to your wallet, at today's Bitcoin price.",
        [("layers", "12 slots"), ("refresh-cw", "Live price")])}
{sec(f'<div class="calc one">{form}</div>')}
{sec(honest("How to read this.", "These amounts arrive as the 14 positions below you fill, each with a member paying the slot price. Cycles fill at the pace your team and spillover grow. It's arithmetic, not a promise."))}'''


def p_c_halv(here):
    return f'''{phero("hourglass", "Bitcoin Halving Countdown", "About every four years, the reward for mining a new Bitcoin block is cut in half. Here's how close the next one is, live.",
        [("blocks", "Block 1,050,000"), ("refresh-cw", "Live block height")])}
{sec(f"""<div class="halv glass" data-halving>
 <div class="hc"><div><b data-out="d">0</b><small>days</small></div><div><b data-out="hh">0</b><small>hours</small></div><div><b data-out="mm">0</b><small>minutes</small></div></div>
 <p class="lead center">Estimated: <b data-out="eta">2028</b></p>
 <div class="epoch" role="img" aria-label="Progress through the current halving period"><i></i></div>
 <div class="hrow"><span>Current block <b data-out="h">0</b></span><span><b data-out="ep">0%</b> of the way</span><span>Blocks left <b data-out="left">0</b></span></div>
 {ratebox().replace('Loading the live Bitcoin price…', 'Reading the live block height…').replace('Refresh the live price', 'Refresh')}
</div>""")}
{sec(f"""<div class="grid2">
 {box("Why it matters", "<p>Fewer new Bitcoin are made after each halving, while the 21 million limit never changes. Past halvings were followed by big price moves, up and down. That's history, not a promise.</p>", "trending-up")}
 {box("How it's estimated", "<p>A new block arrives about every 10 minutes on average, so the date is an estimate. The block number, 1,050,000, is exact. The reward drops from 3.125 to 1.5625 BTC per block.</p>", "calculator")}
</div>""", sr="About the halving")}'''


# ======================================================================= FAQ
FAQ = [
    ('Before you join', [
        ('What is Bitcoin Wealth in one sentence?', 'A smart contract on BNB Smart Chain where members activate slots with BTCB, and each payment goes straight to other members\' wallets by fixed rules.'),
        ('How much does it cost to start?', 'Slot 1 costs 0.001 BTC (paid as BTCB), plus small network fees in BNB. It\'s a once-off: slots 2 to 12 are bought automatically from the cycle below, once it fills.'),
        ('Is it guaranteed to pay?', 'No. Every payout comes from another member\'s slot payment. If new activations slow down, payouts slow down. Only use money you can afford to lose.'),
        ('Do I have to introduce people?', 'Sponsoring two people is the first qualifier (Ignite) and switches on spillover. There\'s no upper limit, and nobody should ever be pressured.'),
    ]),
    ('Money and wallets', [
        ('Why BTCB and not Bitcoin?', 'The contract runs on BNB Smart Chain, which can run smart contracts. BTCB is Bitcoin\'s value on that chain, backed one to one by Bitcoin held by Binance.'),
        ('Why do I need BNB?', 'Every transaction on BNB Smart Chain pays a small fee in BNB. Without BNB nothing moves, even with plenty of BTCB in your wallet.'),
        ('How do I get paid?', 'Payouts land in your own wallet in the same transaction as the activation that triggers them. There is no withdraw button and nobody to ask.'),
        ('Where do I buy with rand?', 'On VALR or Binance. Buy BNB, send it to SafePal on BNB Smart Chain (BEP20), then swap most of it to BTCB in SafePal.'),
    ]),
    ('Trust and safety', [
        ('Can I check it myself?', 'Yes. Paste the contract address into bscscan.com and look at the transactions. The Check it yourself page shows you how, step by step.'),
        ('Is there an admin?', 'Yes. The contract has an owner wallet that can switch on an emergency mode and withdraw tokens the contract holds, among other settings. It is not renounced. We show this openly so you can judge for yourself.'),
        ('Is this an official Bitcoin Wealth site?', 'No. It\'s MTG\'s independent guide. MTG is a member, and the sign-up button carries his referral link.'),
    ]),
]


def p_faq(here):
    out = ''
    for g, qs in FAQ:
        items = ''.join(f'<details><summary>{q}{ic("chevron-down")}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in qs)
        out += f'<h2 class="h3 faqh">{g}</h2><div class="faq">{items}</div>'
    return f'''{phero("circle-help", "FAQ: straight answers", "The questions people ask most, answered plainly. Can't find yours? Ask in the MTG TRIBE.")}
{sec(f'<div class="stack">{out}</div>')}'''


def faq_ld():
    ents = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for g, qs in FAQ for q, a in qs]
    return [{'@type': 'FAQPage', 'mainEntity': ents}]


# ======================================================================= GLOSSARY
GLOSS = [
    ('bitcoin', 'Bitcoin (BTC)', 'bitcoin', 'Digital money with no bank behind it, live since 2009. Only 21 million will ever exist.', 'Digital gold: scarce, and nobody can print more.'),
    ('satoshi', 'Satoshi', 'coins', 'The smallest piece of a Bitcoin: one hundred millionth. 0.001 BTC is 100,000 satoshis.', 'Cents in a rand, but much smaller.'),
    ('btcb', 'BTCB', 'coins', 'Bitcoin\'s value on BNB Smart Chain, issued by Binance and backed one to one by Bitcoin it holds.', 'A voucher you can swap back for the real thing.'),
    ('bnb', 'BNB', 'fuel', 'The coin that pays network fees on BNB Smart Chain.', 'The postage stamp on every letter you send.'),
    ('bsc', 'BNB Smart Chain (BEP20)', 'blocks', 'The blockchain Bitcoin Wealth runs on. BEP20 is the name for tokens on it.', 'The road the delivery truck drives on.'),
    ('smart-contract', 'Smart contract', 'blocks', 'A program on the blockchain that runs its rules automatically, the same way for everyone.', 'A vending machine: the right coin in, the snack out, no shopkeeper.'),
    ('wallet', 'Web3 wallet', 'wallet', 'An app like SafePal or MetaMask that holds the keys to your crypto. You own it, not a company.', 'Your own house keys.'),
    ('phrase', 'Recovery phrase', 'key-round', 'The 12 secret words that can restore your wallet on any phone. Never share them.', 'The master key to your house. Never give out a copy.'),
    ('slot', 'Slot', 'layers', 'One of 12 levels in Bitcoin Wealth, from 0.001 BTC to 2.048 BTC.', 'Floors in a building: each one costs double the one below.'),
    ('position', 'Position', 'network', 'One of the 14 seats below you in a cycle: 2, then 4, then 8.', 'Seats on a bus that fill as people board.'),
    ('cycle', 'Cycle', 'refresh-cw', 'One round of 14 filled positions at a slot.', 'One full bus trip.'),
    ('recycle', 'Recycle', 'refresh-cw', 'When a cycle completes, one payment puts you back into the same slot so it can pay again.', 'Buying the next bus ticket from this trip\'s fares.'),
    ('auto-entry', 'Auto entry', 'arrow-up', 'Slots 2 to 12 are bought for you with two payments from your first cycle at the slot below.', 'A free upgrade, earned by filling the bus below.'),
    ('spillover', 'Spillover', 'git-merge', 'When your upline\'s team overflows, new members can land in positions below you.', 'Extra passengers sent to your bus when the one ahead is full.'),
    ('royal-pool', 'Royal Pool', 'crown', 'In later cycles one payment goes to a pool shared monthly by members who reach slot 3 and qualify.', ''),
    ('bscscan', 'BscScan', 'scan-search', 'The public website where anyone can look up BNB Smart Chain addresses and transactions.', 'A public bank statement everyone can read.'),
    ('approval', 'Token approval', 'shield-check', 'Permission you give a contract to move a token from your wallet. Approve only what you need.', 'Signing a debit order: check the amount.'),
    ('gas', 'Gas (network fee)', 'fuel', 'The small fee in BNB paid for every transaction on BNB Smart Chain.', ''),
    ('halving', 'Halving', 'hourglass', 'About every four years, the reward for mining new Bitcoin is cut in half.', ''),
    ('renounced', 'Renounced', 'user-x', 'A contract whose owner has given up control for good. Bitcoin Wealth\'s contract is not renounced.', ''),
]


def p_gloss(here):
    terms = ''
    for id_, t, icn, d, like in GLOSS:
        lk = f'<p class="like"><b>Like:</b> {like}</p>' if like else ''
        terms += f'<article class="term glass" id="{id_}" data-term="{esc(t.lower() + " " + d.lower())}"><h3>{ic(icn)}{t}</h3><p>{d}</p>{lk}</article>'
    return f'''{phero("book-open-text", "Glossary: crypto words in plain English", "Every word you'll hear in the videos and pages, with an everyday example where it helps.")}
{sec(f"""<div class="gfilter"><label class="sr" for="gq">Find a word</label><input id="gq" class="field" type="search" placeholder="Find a word, like BTCB or slot" autocomplete="off" data-gfilter></div>
<div class="gloss">{terms}</div><p class="fine" data-gempty hidden>No match. Try another word, or ask in the MTG TRIBE.</p>""", sr="All the words")}'''


# ======================================================================= SAFETY
def p_safe(here):
    habits = [
        ('key-round', 'Never share your recovery phrase', 'Nobody genuine will ever ask for it: not MTG, not support, not a "recovery service". Write it on paper, offline.'),
        ('shield-check', 'Approve only the exact amount', 'When SafePal asks to approve BTCB, approve only what you\'re paying. Review old approvals now and then.'),
        ('route', 'Right network, small test first', 'Send on BNB Smart Chain (BEP20). Send a small test amount first, then the rest.'),
        ('fuel', 'Keep some BNB', 'Never empty your BNB, or you won\'t be able to move anything.'),
        ('link', 'Type addresses yourself', 'Download apps from official websites, and type bscscan.com yourself rather than clicking links in messages.'),
        ('eye-off', 'Hide before you share', 'Cover addresses, balances and emails before you post a screenshot.'),
    ]
    h = ''.join(f'<div class="wcard glass">{ped(i)}<h3 class="h3">{t}</h3><p>{d}</p></div>' for i, t, d in habits)
    return f'''{phero("shield-check", "Safety centre", "Six habits that protect your wallet, whatever you use it for.")}
{sec(f'<div class="wgrid">{h}</div>', "Six safety habits")}
{sec(f"""<div class="grid2">{box("Walk away if someone", checks(["Asks for your recovery phrase or a screenshot of it", "Promises a fixed daily or weekly return", "Pressures you to decide today", "Asks you to send crypto to unlock a payout"], no=True), "ban")}
{box("Learn more, free", f"<p>MTG's <a class='inl' href='{esc(CRYPTO101)}' target='_blank' rel='noopener'>Crypto 101 crash course</a> covers wallets, scams, wallet drainers and token approvals in 15 short lessons.</p>", "graduation-cap")}</div>""", "Scam patterns")}'''


# ======================================================================= MORE
def p_card(here):
    return f'''{phero("credit-card", "Spend your crypto with a card", "A shorter road from crypto to everyday spending: a crypto debit card, with an income opportunity of its own.")}
{sec(f'<div class="joinband glass"><div><h2 class="h3">MTG\'s crypto card guide</h2><p>Everything about the card, step by step, on its own website.</p></div><div class="btn-row">{btn("Open the card guide", CARD_GUIDE, "gold", "external-link", ring=True, ext=True)}</div></div>')}'''


def p_tribe(here):
    return f'''{phero("message-circle", "Join the MTG TRIBE", "A free WhatsApp community of action takers who learn, execute and teach others. Many opportunities, honest guides, real people.")}
{sec(f"""<div class="grid3">
 {box("The WhatsApp group", f"<p>Ask questions, get the Zoom links, learn with others.</p><div class='btn-row'>{wa_group_btn(size='sm')}</div>", "whatsapp")}
 {box("WhatsApp MTG", f"<p>Messages and voice notes welcome (no calls): {WA_NUM}.</p><div class='btn-row'>{wa_mtg_btn(size='sm')}</div>", "message-circle")}
 {box("Follow along", f"<p>New videos land here first.</p><div class='btn-row'>{btn('TikTok', TIKTOK, 'ghost', 'tiktok', 'sm', ext=True)}{btn('YouTube', YOUTUBE, 'ghost', 'youtube', 'sm', ext=True)}{btn('Facebook', FACEBOOK, 'ghost', 'facebook', 'sm', ext=True)}{btn('Telegram', TELEGRAM, 'ghost', 'telegram', 'sm', ext=True)}</div>", "heart")}
</div>""", sr="Ways to join in")}'''


def p_disc(here):
    return f'''{phero("info", "Disclaimer", "Independent, educational, and honest about the risks.")}
{sec(f"""<div class="prose panel pad glass">
<p>{DISCLAIMER}</p>
<p><b>Referral links.</b> The Bitcoin Wealth sign-up button, the VALR and Binance buttons and the crypto card guide are MTG's referral or partner links. If you use them, MTG may earn, at no extra cost to you. If someone else introduced you, use their links.</p>
<p><b>Your copy, your rules.</b> A BW Tribe Page is a copy of this guide with the owner's own links. The owner is responsible for how they share it.</p>
<p><b>Privacy.</b> This site uses no tracking and no cookies. It saves only your watched videos and menu setting on your own device. The live tools ask CoinGecko and mempool.space for public prices and block heights.</p>
<p><b>Not financial advice.</b> Nothing here is financial, tax or legal advice. Always do your own research.</p>
</div>""")}'''


# ======================================================================= ORDER FORM (mtgtribe.com/bwcopy)
def order_page(here=''):
    import core as _c; _c._used.clear()
    home = SITE + BASE
    f = lambda n, label, ph='', req=False, hint='', typ='text': (
        f'<div class="field-w field"><label for="o-{n}">{label}{" <i>*</i>" if req else ""}</label>'
        f'<input id="o-{n}" name="{n}" type="{typ}" placeholder="{ph}" autocomplete="off"{" required" if req else ""}>'
        + (f'<small>{hint}</small>' if hint else '') + '</div>')
    pay = ''.join(f'<label class="opt"><input type="radio" name="pay" value="{v}"{" checked" if i == 0 else ""}><span>{t}</span></label>'
                  for i, (v, t) in enumerate([('Rand bank transfer', 'Rand (bank details on WhatsApp)'), ('USDT BEP20', 'USDT BEP20'), ('USDT TRC20', 'USDT TRC20')]))
    dom = ''.join(f'<label class="opt"><input type="radio" name="domain" value="{v}"{" checked" if i == 0 else ""} required><span>{v}<b>yourname</b></span></label>'
                  for i, v in enumerate(['mtgtribe.com/bw/', 'bitcoinwealthpays.com/']))
    body = f'''<header class="ltop"><div class="wrap">
 <a class="brand" href="{A('', here)}" aria-label="Bitcoin Wealth guide home">{logo(here)}</a>
 <a class="btn btn-ghost btn-sm" href="{A('dashboard/bw-tribe-page/', here)}">{ic('arrow-left')}<span class="lbl">Back to the guide</span></a>
</div></header>
<main id="main" tabindex="-1">
<section class="phero"><div class="wrap"><div class="phero-in">{ped('globe', 'lg')}<div>
 <h1 class="h1">Congratulations. Let's build your BW Tribe Page.</h1>
 <p class="lead">You're two minutes away from your own Bitcoin Wealth website, with your link inside. Fill this in and it goes straight to MTG on WhatsApp.</p>
 {chips(('badge-check', 'R1,000 once-off'), ('hand-coins', 'Pay after it is built'), ('pencil', '5 free edits'))}
</div></div></div></section>
<section class="sec"><div class="wrap">
<form class="oform glass" data-order novalidate>
 <fieldset><legend>{ic('user')}About you</legend>
  {f('name', 'Your name, as it should appear', 'Zizi', True)}
  {f('wa', 'Your WhatsApp number', '072 123 4567', True, typ='tel')}
 </fieldset>
 <fieldset><legend>{ic('globe')}Your address</legend>
  <div class="field-w field"><span class="lab">Choose the address <i>*</i></span><div class="opts">{dom}</div></div>
  {f('slug', 'The name at the end of your address', 'zizi', True, 'Letters and numbers only.')}
  <p class="addrprev">{ic('link')}<span>Your page: <b data-out="addr">mtgtribe.com/bw/yourname</b></span></p>
 </fieldset>
 <fieldset><legend>{ic('link')}Your links</legend>
  {f('ref', 'Your Bitcoin Wealth referral link', 'https://vowu.io/register?ref=...', True, 'Every sign-up button on your page will copy this link.')}
  {f('group', 'Your WhatsApp group link', 'https://chat.whatsapp.com/...', False, "No group yet? Create one first, or add it later.")}
  {f('valr', 'Your VALR referral link (optional)', 'https://www.valr.com/invite/...')}
  {f('bnb', 'Your Binance referral link (optional)', 'https://accounts.binance.com/register?ref=...')}
  {f('tiktok', 'TikTok (optional)', 'https://www.tiktok.com/@...')}
  {f('fb', 'Facebook (optional)', 'https://www.facebook.com/...')}
  {f('yt', 'YouTube (optional)', 'https://www.youtube.com/@...')}
 </fieldset>
 <fieldset><legend>{ic('wallet')}How you'd like to pay</legend>
  <div class="opts">{pay}</div><small class="fine">You only pay once your page is built and you've seen it. You'll agree the details with MTG on WhatsApp.</small>
 </fieldset>
 <fieldset><legend>{ic('pencil')}Anything else?</legend>
  <div class="field-w field"><label for="o-notes">Notes for MTG (optional)</label><textarea id="o-notes" name="notes" rows="3" placeholder="Colours, wording, anything you'd like"></textarea></div>
 </fieldset>
 <div class="osend"><button type="submit" class="btn btn-gold btn-lg ring">{ic('whatsapp')}<span class="lbl">Send my order on WhatsApp</span></button>
 <p class="fine">This opens WhatsApp with your details filled in. Nothing is stored on this website. After sending, share your profile photo in the same chat.</p></div>
 <div class="sent glass" data-sent hidden>{ic('circle-check')}<div><b>Almost done.</b><p>Press send in WhatsApp. MTG will reply on {WA_NUM}. Didn't open? <a class="inl" href="{esc(WA_MTG)}" target="_blank" rel="noopener">Open WhatsApp</a>.</p></div></div>
</form>
<div class="secret glass">{ic('lock-keyhole')}<div><b>For owners: the traffic source</b><p>Once your page is built, paid and yours, MTG shows you the traffic source he uses, with its own tutorials and explainers. It has an income stream of its own. No guarantee its visitors join.</p></div></div>
</div></section>
</main>
<footer class="lfoot"><div class="wrap"><p class="disc">{DISCLAIMER}</p>
<div class="fbot"><span>© 2026 MTG 👑 | Your Digital Architect. <a class="inl" href="{SITE}/">mtgtribe.com</a></span><span class="sig">Let's Get This Crypto! 💪</span></div></div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>window.BW={{"wa":"{WA_MTG}"}};window.BWV={{}};</script>
<script src="{A('assets/bw.js', here)}" defer></script>'''
    desc = 'Order your BW Tribe Page: your own copy of the Bitcoin Wealth guide with your referral link built in. R1,000 once-off, paid only after it is built.'
    hd = head('Order your BW Tribe Page', desc, '', here, og_key='order')
    hd = hd.replace(f'<link rel="canonical" href="{SITE}{BASE}">', f'<link rel="canonical" href="{SITE}{ORDER}">').replace(
        f'<meta property="og:url" content="{SITE}{BASE}">', f'<meta property="og:url" content="{SITE}{ORDER}">')
    return hd, body
