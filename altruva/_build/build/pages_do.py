"""Dashboard pages: Get started, Tools, Help, More."""
import os
from urllib.parse import quote
from core import *
from pages_learn import phero

MEDIA = '/home/claude/site/media/'


# ======================================================================= FIRST 72 HOURS
def p_first72(here):
    clock = f"""<div class="panel pad clock72" data-clock72>
 <h2 class="h3">{ic("timer")}<span>Your 72-hour clock</span></h2>
 <div class="fl"><label for="jt">When did you join?</label><input id="jt" class="field" type="datetime-local" step="1" data-join></div>
 <div class="btn-row"><button type="button" class="btn btn-ghost btn-sm" data-now>{ic("zap")}<span class="lbl">I joined just now</span></button><button type="button" class="mark" data-clearjoin>Clear</button></div>
 <div class="cd" aria-live="polite"><b data-k="left">72:00:00</b><small data-k="status">Set your join time to start your clock</small></div>
 <p class="fine" data-k="until">Saved on this device only.</p>
</div>"""
    return f'''{phero("timer", "Your first 72 hours",
        "You've joined. Congratulations: you took action. Now your clock has started, and the next three days matter more than any others.",
        [("timer", "72-hour window"), ("package", "Why the $100 position"), ("circle-play", mmss(V["e7"]["secs"]) + " video")])}
{sec(f"""<div class="vwrap"><div class="stack">{clock}
{checks(["Right after joining, global leg income may already be waiting: your window looks up the line too.",
         "Once your balance reaches $5, claim and withdraw to SafePal. Half goes to your wallet, half is reinvested.",
         "Two directs on your package inside 72 hours open your rank, the Starter ticket, both matching sides and working levels 1 to 6."])}
<div class="btn-row">{play_btn("k5", "How to use the clock")}</div>
</div>{vid("e7", here)}</div>""")}
{sec(f"""<div class="stack"><p class="how num">Illustration: if the 20 members ahead of you each hold $100, 1% of each is $1, so about <b>$20</b> could be waiting to claim. The real amount depends on who is in your window.</p>
{think("Why is there money before I've done anything?", "<p>Your global leg window looks up the line as well as down. The app pays 1% of each visible member's total deposit inside your window, so the members who joined before you count from the start. It isn't a bonus or a promise: it depends entirely on who is in your window.</p>")}
<div class="btn-row">{play_btn("t5")}</div></div>""", "Minute one: what may be waiting")}
{sec(f"""<div class="grid3">
 {box("Twice the window", "<p>Elite opens 20 up and 20 down: 40 members. Starter opens 10 and 10: 20 members.</p>", "route")}
 {box("Two Lucky Tickets", "<p>Elite gives two. Starter gives one, and only once two directs join within three days.</p>", "ticket")}
 {box("The top of the ladder", "<p>Elite unlocks the Legacy Crown rank, and there is nothing more to buy.</p>", "crown")}
</div>
<div class="grid2 tick-grid" style="margin-top:16px"><figure class="ticket"><img src="{A("img/mtg-lucky-ticket-won.webp", here)}" width="529" height="342" loading="lazy" alt="MTG's own Lucky Ticket card showing WON 25.00 USDT in Draw 16, ticket ID hidden"></figure>
<div class="stack"><p>My own example: Elite gave me two tickets. The first didn't win. The second won 25 USDT, paid to my wallet in full. With one ticket, there's no second chance.</p>
<div class="honest">{ic("triangle-alert")}<div><b>Be honest with yourself:</b> most tickets don't win, so never count on a prize. A bigger package also puts more money at risk. Only use money you can afford to lose.</div></div></div></div>""",
    "Why the $100 position", id="why-100")}
{sec(table(["Your package", "Two directs of", "What it opens"], [["Elite, $100", "$100 or more", "<b>Legacy Crown</b> rank"], ["Builder, $50", "$50 or more", "<b>Nexus</b> rank"], ["Starter, $25", "$25 or more", "Your <b>Lucky Ticket</b>"]], caption="What two directs inside 72 hours open")
    + '<p class="fine" style="margin-top:12px">Rank and ticket rules from the ALTRUVA presentation and the app. On any package, two directs also give you both sides for level matching and open working levels 1 to 6.</p>',
    "What two directs in 72 hours open")}
{sec(steps([
    ("Hour one: check and claim", "<p>Open your dashboard, see what's waiting, and claim it. Tutorial 7 explains every screen.</p>" + play_btn("t7")),
    ("Day one: copy your link", f"<p>Tap Network and copy your link. Share this website first, so people learn before they decide. The <a class='inl' href='{A("dashboard/downloads/", here)}'>share kit</a> has a ready message.</p>"),
    ("Days one to three: help, never push", f"<p>Walk people through the <a class='inl' href='{A("dashboard/join/", here)}'>join guide</a> and the tutorials. They should join because they understand ALTRUVA, never because you rushed them.</p>"),
    ("Before the clock runs out: check", "<p>Look at your directs, your tickets and your rank in the app, and keep learning in your WhatsApp group and on Zoom.</p>"),
]), "Your 72-hour plan", "Build from minute one, one honest step at a time.")}
{sec(f"""<div class="stack">
{think("Do I have to introduce people?", "<p>No. It's not compulsory, and the global leg can pay you without it. But the people you introduce may thank you one day, for opening their eyes to smart contracts, Web3, and a community that learns, wins and grows together. And you'll thank yourself.</p>")}
{think("What if I miss the 72 hours?", "<p>The presentation ties the ranks, and the Starter ticket, to the first three days. Everything else keeps working: the global leg, and working levels and matching open whenever directs join.</p>", alt=True)}
</div>""")}
'''


# ======================================================================= JOIN
# the five join steps (also used for the HowTo structured data)
JOIN_STEPS = [
    ("Set up SafePal", "Install SafePal, create your wallet and write your recovery phrase on paper. Never type it into a website or send it to anyone."),
    ("Fund your wallet", "Send BNB on BNB Smart Chain, swap most of it to USDT BEP20, and keep some BNB for fees."),
    ("Copy the sign-up link", "Use the link of the person who introduced you, so they stay your sponsor."),
    ("Join in SafePal Explore", "Paste the link in Explore, choose BNB Chain, pick your package, then approve and sign. Read the risk warning before you confirm."),
    ("Find your way around", "Tour Overview, Packages, Earnings, Network and More, so every number makes sense."),
]
JOIN_NEEDS = ["A smartphone with the SafePal app", "USDT on BNB Smart Chain (BEP20) for your package, plus one extra dollar",
              "At least $3 to $5 of BNB in the same wallet for network fees", "The sign-up link from the person who introduced you",
              "A pen and paper for your recovery phrase"]


def p_join(here):
    return f'''{phero("rocket", "Join step by step",
        "Five steps, one short video each. Pause the video, do the step, check your screen matches, then move on.",
        [("smartphone", "About 20 minutes"), ("wallet", "SafePal wallet"), ("coins", "USDT plus a little BNB")])}
{sec(f"""<div class="panel pad">{checks([
    "A smartphone with the <b>SafePal</b> app (MetaMask or Trust Wallet work too, but the videos use SafePal).",
    "<b>USDT on BNB Smart Chain (BEP20)</b> for your package, plus one extra dollar: 26, 51 or 101 USDT.",
    "At least <b>$3 to $5 of BNB</b> in the same wallet for network fees. Each action costs a few cents.",
    "The <b>sign-up link</b> from the person who introduced you. A pen and paper for your recovery phrase.",
])}</div>""", "What you need")}
{sec(steps([
    (JOIN_STEPS[0][0], f"<p>{JOIN_STEPS[0][1]}</p>" + play_btn("t1")),
    (JOIN_STEPS[1][0], f"<p>{JOIN_STEPS[1][1]}</p>" + play_btn("t2")),
    (JOIN_STEPS[2][0], f"<p>{JOIN_STEPS[2][1]} If that's MTG, tap below: it copies and opens nothing.</p><div class='btn-row'>{copy_btn('signup', 'Copy MTG\'s sign-up link', size='sm')}</div>"),
    (JOIN_STEPS[3][0], f"<p>{JOIN_STEPS[3][1]}</p>" + play_btn("t3")),
    (JOIN_STEPS[4][0], f"<p>{JOIN_STEPS[4][1]}</p>" + play_btn("t7")),
]), "Five steps", "The success check: the Packages page says you hold your package.")}
{sec(f"""<div class="joinband"><div><h2 class="h3">Just joined? Your 72 hours start now</h2><p>What may already be waiting, why the $100 position matters, and what two directs open inside your first three days.</p></div>
<div class="btn-row"><a class="btn btn-gold btn-sm ring" href="{A("dashboard/first-72-hours/", here)}">{ic("timer")}<span class="lbl">Your first 72 hours</span></a>{play_btn("e7")}</div></div>""")}
{sec(f"""<div class="grid3">
 {box("Claim a prize", "<p>Check your Lucky Tickets and claim a prize, in full, to your wallet.</p>" + play_btn("t4"), "ticket")}
 {box("Withdraw", "<p>Claim first, then withdraw everything to SafePal.</p>" + play_btn("t5"), "wallet")}
 {box("Cash out to your bank", "<p>SafePal to an exchange, USDT to rand, rand to your bank.</p>" + play_btn("t6"), "landmark")}
</div>""", "After you join")}
{sec(think("What if something on my screen looks different?", "<p>Apps update their screens from time to time. Look for the same words, and go slowly. Still stuck? Ask the person who introduced you, or ask in the MTG TRIBE. A screenshot helps, but hide your balances and never show your recovery phrase.</p>"))}
'''


# ======================================================================= PLAYLISTS
def playlist(codes, here, title):
    first = codes[0]
    items = ''
    for k in codes:
        v = V[k]
        big, small = poster(k, here)
        items += (f'<li><button type="button" class="pitem" id="{k}" data-pick="{k}" data-vid="{k}" aria-current="{"true" if k == first else "false"}">'
                  f'<img src="{esc(small)}" width="44" height="78" loading="lazy" alt="">'
                  f'<span class="pt" title="{esc(v["desc"])}"><b><span class="vn">{v["n"]}</span><span class="vt">{v["short"]}</span></b></span>'
                  f'<span class="pd">{mmss(v["secs"])}{ic("circle-check", "ic ok")}</span></button></li>')
    return f'''<div class="plist" data-playlist><div class="now">{vid(first, here)}<p class="fine" data-k="desc">{V[first]["desc"]}</p></div>
<div class="stack"><h2 class="h3">{title}</h2><ol>{items}</ol></div></div>'''


def p_tut(here):
    total = round(sum(V[k]['secs'] for k in TUT) / 60)
    return f'''{phero("circle-play", "Tutorial videos",
        "Seven step-by-step trainings, recorded on a real phone, plus five short trainings for this website's tools. Pause after each step and try it yourself.",
        [("film", f"7 tutorials, about {total} minutes"), ("calculator", f"{len(TOOL)} tool trainings"), ("eye-off", "Private details hidden")])}
{sec(playlist(TUT, here, "All tutorials, in order"))}
{sec(playlist(TOOL, here, "Tool trainings, in order"), "Tool trainings", f"Every tap on this website's tools, in about {round(sum(V[k]['secs'] for k in TOOL) / 60)} minutes.", id="tools")}
{sec(think("Do I really need to watch them all?", "<p>Yes, even if you think you already know ALTRUVA. Each one shows a screen you'll meet sooner or later, and knowing it before you need it saves money and stress. Then share them: we learn best when we teach others.</p>"))}
'''


def p_exp(here):
    total = round(sum(V[k]['secs'] for k in EXP) / 60)
    return f'''{phero("film", "Explainer videos",
        "Six short animated explainers: the whole plan, one part at a time, with everyday examples and the real numbers.",
        [("film", f"6 videos, about {total} minutes"), ("calculator", "Real numbers on screen"), ("triangle-alert", "Risks included")])}
{sec(playlist(EXP, here, "All explainers, in order"))}
{sec(think("Can I watch them again?", "<p>Please do. Most people need two or three views before the global leg and matching really click. Come back until you get it, then try explaining it to a friend.</p>"))}
'''


# ======================================================================= TOOLS
def field(id_, label, unit, hint='', ph='', val=''):
    v = f' value="{val}"' if val else ''
    return (f'<div class="fl"><label for="{id_}">{label}</label><div class="inwrap"><input id="{id_}" class="field" type="text" '
            f'inputmode="decimal" autocomplete="off" placeholder="{ph}"{v} data-in="{id_}"><span class="unit">{unit}</span></div>'
            + (f'<span class="hint">{hint}</span>' if hint else '') + f'<span class="err" data-err="{id_}"></span></div>')


def presets(items):
    b = ''.join(f"<button type='button' data-preset='{p}'>{n}</button>" for n, p in items)
    return f'<div class="seg presets" role="group" aria-label="Examples">{b}<button type="button" data-clear>{ic("rotate-ccw")} Clear</button></div>'


def tool_vid(code, here):
    v = V[code]
    body = (f'<div class="vwrap"><div class="stack"><p>Every tap on this page, step by step, in {mmss(v["secs"])}. '
            f'Pause the video, try it on your phone, then carry on.</p>'
            + checks([v['desc'], 'Real numbers on screen, so you can check your own.', 'Then try your own numbers, and teach someone else.'])
            + f'</div>{vid(code, here)}</div>')
    return sec(body, 'Watch the tool training', id='training')


def tool_page(icon, title, lead, chips_, form, result, notes, here, code=None):
    return f'''{phero(icon, title, lead, chips_)}
{sec(f'<div class="calc">{form}{result}</div>')}
{sec(notes)}
{tool_vid(code, here) if code else ''}'''


def p_c_wd(here):
    form = f'''<form class="form panel pad" data-calc="split" novalidate onsubmit="return false">
{field("bal", "Balance to withdraw", "USDT", "Your Withdrawable Balance, after you claim.", "23.63")}
{field("tot", "Your total deposit", "USDT", "Fresh packages plus everything reinvested so far.", "100")}
{presets([("My real example", '{"bal":"23.63","tot":"100"}'), ("Total deposit 6,000", '{"bal":"200","tot":"6000"}'), ("Total deposit 60,000", '{"bal":"1000","tot":"60000"}')])}
</form>'''
    result = f'''<div class="result" data-result="split" aria-live="polite">
 <div class="rbig"><small>To your wallet</small><b data-out="wallet">0.00 USDT</b></div>
 <div class="rbar"><i data-bar="a" style="width:50%;background:var(--gold)"></i><i data-bar="b" style="width:50%;background:var(--electric)"></i></div>
 <div class="rrow"><span>Reinvested</span><b data-out="re">0.00 USDT</b></div>
 <div class="rrow"><span>Your split</span><b data-out="tier">50% / 50%</b></div>
 <div class="rrow"><span>Total deposit after</span><b data-out="after">0.00 USDT</b></div>
 <p class="how" data-out="how">Type your balance and total deposit.</p>
</div>'''
    notes = f'''<div class="stack">{table(["Total deposit", "To wallet", "Reinvested"], [["Up to 5,000", "50%", "50%"], ["5,001 to 49,999", "60%", "40%"], ["50,000 and up", "70%", "30%"]], caption="Split tiers")}
<p class="fine">Tiers from the live ALTRUVA app, 24 Oct 2026. Amounts are cut to 2 decimals, as the app showed in MTG's real withdrawal (23.63 to 11.81 and 11.81). Lucky Ticket prizes are never split. {vlink("e6", here)}.</p></div>'''
    return tool_page("percent", "Withdraw Split Calculator", "See what reaches your wallet and what's reinvested, before you tap Withdraw.",
                     [("percent", "Split by total deposit"), ("smartphone", "Works on your phone")], form, result, notes, here, 'k2')


def p_c_wl(here):
    lv = ''.join(field(f"l{i}", f"Level {i}", "USDT", "", "0").replace('<span class="err"', f'<span class="lvpay" data-pay="{i}"></span><span class="err"', 1) for i in range(1, 10))
    form = f'''<form class="form panel pad" data-calc="wl" novalidate onsubmit="return false">
<div class="fl"><span class="lab" id="dlab">Your directs</span><div class="seg" role="group" aria-labelledby="dlab"><button type="button" data-d="0" aria-pressed="false">0</button><button type="button" data-d="1" aria-pressed="true">1</button><button type="button" data-d="2" aria-pressed="false">2</button><button type="button" data-d="3" aria-pressed="false">3 or more</button></div><span class="hint">1 direct opens levels 1 to 3, 2 open 4 to 6, 3 open 7 to 9.</span></div>
<p class="fine">New deposits or reinvestments on each level:</p>
<div class="lvgrid">{lv}</div>
{presets([("Your direct buys Elite", '{"d":"1","l1":"100"}'), ("A level 7 deposit", '{"d":"3","l7":"100"}'), ("Same, 2 directs", '{"d":"2","l7":"100"}')])}
</form>'''
    result = f'''<div class="result" data-result="wl" aria-live="polite">
 <div class="rbig"><small>You earn</small><b data-out="earn">0.00 USDT</b></div>
 <div class="rrow"><span>Levels open to you</span><b data-out="open">3 of 9</b></div>
 <div class="rrow"><span>Stays in the contract (closed levels)</span><b data-out="stay">0.00 USDT</b></div>
 <ul class="lvout" data-out="list"></ul>
 <p class="how" data-out="how">Type an amount on any level.</p>
</div>'''
    notes = f'<p class="fine">Rates from the live app: 10%, 4%, then 2% on levels 3 to 6 and 1% on levels 7 to 9. Working level income goes straight to your balance, no claim needed. {vlink("e3", here)}.</p>'
    return tool_page("calculator", "Working Level Calculator", "Work out what deposits on your nine levels pay you, and what stays in the contract when a level is closed.",
                     [("layers", "Levels 1 to 9"), ("users", "Directs open levels")], form, result, notes, here, 'k3')


def p_c_m(here):
    form = f'''<form class="form panel pad" data-calc="match" novalidate onsubmit="return false">
{field("s1", "Side 1: your biggest direct's team", "USDT", "New business today on that side.", "500")}
{field("s2", "Side 2: all your other directs", "USDT", "New business today on the other side.", "100")}
{field("rate", "Rate per unit", "per unit", "Check the day's rate in the app's matching ledger. Day 22's real rate was 0.079427.", "0.079427")}
<details class="mini"><summary>{ic("calculator")} Work out a day's rate</summary>
{field("biz", "That day's business", "USDT", "Fresh deposits plus reinvestments.", "124304.01")}
{field("all", "Everyone's matched volume", "units", "From the matching ledger.", "391251.10")}
<p class="fine" data-out="rate2">Rate = 25% of the day's business ÷ everyone's matched.</p>
<button type="button" class="btn btn-ghost btn-sm" data-userate>{ic("check")}<span class="lbl">Use this rate</span></button>
</details>
{presets([("Day 22: 100 matched", '{"s1":"500","s2":"100","rate":"0.079427"}'), ("Balanced sides", '{"s1":"300","s2":"300","rate":"0.079427"}')])}
</form>'''
    result = f'''<div class="result" data-result="match" aria-live="polite">
 <div class="rbig"><small>Your matching for the day</small><b data-out="earn">0.00 USDT</b></div>
 <div class="rbar"><i data-bar="a" style="width:0%;background:var(--gold)"></i><i data-bar="b" style="width:0%;background:rgba(120,170,255,.25)"></i></div>
 <div class="rrow"><span>Matched (the smaller side)</span><b data-out="matched">0</b></div>
 <div class="rrow"><span>Not matched (extra on the bigger side)</span><b data-out="extra">0</b></div>
 <p class="how" data-out="how">Type both sides and a rate.</p>
</div>'''
    notes = f'<p class="fine">The rate changes every day with the whole platform\'s business, so this is an illustration, not a forecast. A day closes at 00:00 UTC (02:00 in South Africa). {vlink("e4", here)}.</p>'
    return tool_page("equal", "Matching Calculator", "Your smaller side times the day's rate. Try the real day 22 numbers, then your own.",
                     [("scale", "Smaller side counts"), ("calendar-clock", "One day at a time")], form, result, notes, here, 'k4')


def p_c_zar(here):
    form = f'''<form class="form panel pad" data-calc="zar" novalidate onsubmit="return false">
<div class="seg" role="group" aria-label="Direction"><button type="button" data-dir="u2z" aria-pressed="true">USDT to rand</button><button type="button" data-dir="z2u" aria-pressed="false">Rand to USDT</button></div>
{field("amt", "Amount", "USDT", "", "100")}
<div class="pkgq" data-pkgs><span class="lab" id="pklab">Buying a package? Tap one:</span><div class="seg presets" role="group" aria-labelledby="pklab"><button type="button" data-amt="28">Starter + BNB</button><button type="button" data-amt="53">Builder + BNB</button><button type="button" data-amt="105">Elite + BNB</button></div><span class="hint">Your package plus at least $3 to $5 of BNB for network fees: 25 + 3 = 28, 50 + 3 = 53, 100 + 5 = 105.</span><p class="pkres" data-out="pkres" aria-live="polite"></p></div>
{field("zrate", "Rate", "R per USDT", "", "")}
<p class="ratebox" data-out="status">{ic("refresh-cw")}<span>Loading the live rate…</span></p>
<button type="button" class="btn btn-ghost btn-sm" data-refresh>{ic("refresh-cw")}<span class="lbl">Refresh the live rate</span></button>
{field("fee", "Fees in rand (optional)", "ZAR", "Exchange and bank fees, as shown on your exchange's screen.", "0")}
</form>'''
    result = f'''<div class="result" data-result="zar" aria-live="polite">
 <div class="rbig"><small data-out="biglab">Value in rand</small><b data-out="main">R0.00</b></div>
 <div class="rrow"><span data-out="netlab">After fees</span><b data-out="net">R0.00</b></div>
 <p class="how" data-out="how">Type an amount.</p>
</div>'''
    notes = f'''<p class="fine">Live rate: CoinGecko (USDT priced in rand), when it loads. Exchanges such as Binance and VALR show their own price, and their convert and withdrawal fees change, so the exchange screen is always the final word. {vlink("t6", here)}.</p>'''
    return tool_page("banknote", "USDT to Rand Converter", "A quick rand value for your USDT, with room for the fees your exchange shows you.",
                     [("refresh-cw", "Live rate"), ("pen-line", "Or type your own")], form, result, notes, here, 'k1')


# ======================================================================= FAQ
FAQ = [
    ('Before you join', [
        ('Is this the official ALTRUVA website?', 'No. This is an independent guide made by MTG, an ALTRUVA member, to educate. The ALTRUVA app itself is at altruva.io/app.'),
        ('Does this guide cost anything?', 'No. Every page, video and calculator here is free. You don\'t need to sign up to learn.'),
        ('What\'s the most I can put in?', 'The top package is Elite at $100, and the app says there\'s nothing more to buy. Network fees are a few cents of BNB per action. Some people open more than one account: that\'s their own strategy and their own risk.'),
        ('What do I need to start?', 'A smartphone, the SafePal wallet app, USDT on BNB Smart Chain for your package, at least $3 to $5 of BNB for fees, and the sign-up link from the person who introduced you. The Join step by step page walks you through it.'),
        ('Someone else introduced me. Which link do I use?', 'Theirs. Your sponsor never changes after you join, so use the link of the person who is helping you learn.'),
    ]),
    ('Money and risk', [
        ('Is my money guaranteed?', 'No. ALTRUVA itself says there is no fixed ROI and no guaranteed return. Earnings depend on deposits made by members.'),
        ('Where does the money come from?', 'From members\' packages and reinvestments. The smart contract shares them by fixed rules. No outside revenue is named, so when new deposits slow down, earnings slow down.'),
        ('Can I lose my $100?', 'Yes. Treat it as money you could lose. Only use an amount that wouldn\'t hurt your rent, food or family.'),
        ('Do I have to introduce people to earn?', 'Not for the global leg: it pays 1% from deposits inside your window, including people you\'ve never met. Working levels and matching depend on your directs, and ranks need directs within 3 days.'),
        ('Why is part of my withdrawal reinvested?', 'It\'s a rule of the plan. Up to a total deposit of 5,000 USDT, half goes to your wallet and half is reinvested. The reinvested part counts as new business and can\'t be taken back out.'),
        ('How do I get money to my bank?', 'Claim and withdraw to SafePal (Tutorial 5), then send USDT to an exchange such as Binance or VALR, convert to rand and withdraw (Tutorial 6).'),
    ]),
    ('Using the app', [
        ('What does "claim" mean?', 'Claiming moves earned income into your Withdrawable Balance. Global leg, matching and rank income need a claim. Working level income arrives in your balance by itself.'),
        ('When does a matching day close?', 'At 00:00 UTC, which is 02:00 in South Africa. One claim collects every closed day since your last claim.'),
        ('How much are the network fees?', 'A few cents of BNB per action on BNB Smart Chain. Joining in Tutorial 3 cost about $0.07. Keep at least $3 to $5 of BNB so you\'re never stuck.'),
        ('My wallet showed a red risk warning. What now?', 'Read it. Wallets warn about many contracts. Only continue if you understand and accept the risk. Tutorial 3 shows the screen.'),
    ]),
]
MYTHS = [
    ('You can lose thousands.', 'The top package is $100. Your package can\'t cost more, so in one account your risk is the package you buy plus small fees.'),
    ('You must recruit to earn anything.', 'The global leg pays from deposits in your window, including strangers. But nothing is guaranteed, and other incomes do need directs.'),
    ('Lucky Tickets are a jackpot.', 'Most tickets don\'t win. Each draw pays 250 tickets between 5 and 100 USDT. Never count on a prize.'),
    ('The reinvested part is a fee.', 'It isn\'t a fee. It goes back in as new business and grows your total deposit. You just can\'t take it back out.'),
    ('Someone has to approve your withdrawal.', 'You claim and withdraw yourself, by signing in your wallet. Whether the contract owner keeps special powers is a separate check: see the Safety centre.'),
    ('You need to understand everything first.', 'No. Learn enough to explain it honestly, start small if it fits, and keep learning as you go.'),
]


def p_faq(here):
    out = ''
    for g, qs in FAQ:
        items = ''.join(f'<details><summary>{q}{ic("chevron-down")}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in qs)
        out += f'<h2 class="h3 faqh">{g}</h2><div class="faq">{items}</div>'
    myths = ''.join(f'<details><summary><span><span class="myth">Myth</span>{m}</span>{ic("chevron-down")}</summary><div class="ans"><p><span class="fact">Fact</span>{f}</p></div></details>' for m, f in MYTHS)
    return f'''{phero("circle-help", "FAQ: questions and myths",
        "The questions people ask most, answered straight. Can't find yours? Ask in the MTG TRIBE.")}
{sec(f'<div class="stack">{out}</div>')}
{sec(f'<div class="faq">{myths}</div>', "Myth or fact?", "Things you may have heard about ALTRUVA, checked against the live app.")}
'''


def faq_ld():
    import re
    ents = []
    for g, qs in FAQ:
        for q, a in qs:
            ents.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    for m, f in MYTHS:
        ents.append({'@type': 'Question', 'name': f'Is it true that {m[0].lower() + m[1:].rstrip(".")}?', 'acceptedAnswer': {'@type': 'Answer', 'text': f}})
    return [{'@type': 'FAQPage', 'mainEntity': ents}]


# ======================================================================= GLOSSARY
GLOSS = [
    ('smart-contract', 'Smart contract', 'blocks', 'A program on the blockchain that runs its rules automatically, the same way for everyone.', 'A vending machine: the right coin in, the snack out, no shopkeeper.'),
    ('web3', 'Web3', 'globe', 'The part of the internet where you hold your own money and identity in a wallet, instead of a company holding an account for you.', 'Cash in your own pocket, instead of money in someone else\'s safe.'),
    ('wallet', 'Web3 wallet', 'wallet', 'An app such as SafePal, MetaMask or Trust Wallet that holds the keys to your crypto.', 'Your own house keys. Lose them, and nobody can let you back in.'),
    ('phrase', 'Recovery phrase', 'key-round', 'The 12 or 24 words that can restore your wallet on any phone. Anyone who has them can take everything.', 'The master key to your house. Never give it to anyone, ever.'),
    ('blockchain', 'Blockchain', 'link', 'A public record book kept by thousands of computers. Past pages can\'t be secretly changed.', 'A village notice board everyone watches.'),
    ('dapp', 'DApp', 'smartphone', 'A decentralised app: an app that runs on the blockchain. You open ALTRUVA as a DApp inside your wallet\'s browser (SafePal Explore).', None),
    ('bsc', 'BNB Smart Chain (BSC)', 'route', 'The blockchain ALTRUVA runs on. Fees here are a few cents.', 'The road your money travels on.'),
    ('bep20', 'BEP20', 'layers', 'The token standard on BNB Smart Chain. "USDT BEP20" means USDT on BNB Smart Chain.', 'A train must match the track. Send on the wrong network and it may not arrive.'),
    ('usdt', 'USDT', 'circle-dollar-sign', 'Tether, a stablecoin designed to stay close to one US dollar. ALTRUVA packages are paid in USDT.', None),
    ('bnb', 'BNB', 'coins', 'The coin that pays network fees on BNB Smart Chain.', 'Petrol for the car: no petrol, no trip.'),
    ('gas', 'Gas fee', 'fuel', 'The small network fee for each action, paid in BNB. It goes to the network, not to ALTRUVA.', 'A toll gate on the road.'),
    ('address', 'Wallet address', 'qr-code', 'Your public receiving address, starting with 0x. Safe to share for receiving. Always check the first and last characters.', 'Your account number for receiving.'),
    ('verified', 'Verified contract', 'badge-check', 'The contract\'s source code is published on BscScan, so anyone can read exactly what it does.', 'A recipe printed on the box.'),
    ('renounced', 'Renounced contract', 'lock', 'The owner has given up the special owner powers, usually by setting the owner to the zero address (0x000...000). Nobody can then use those powers to change the rules. It doesn\'t make a project safe or profitable: it only removes the owner\'s controls.', 'The builder hands over the house and melts the master key.'),
    ('audit', 'Audit', 'search-check', 'An outside firm checks the contract code for bugs and risks. Helpful, never a guarantee.', 'A roadworthy test for a car.'),
    ('approve', 'Approve', 'check', 'Permission for a contract to use a set amount of your USDT. ALTRUVA asks for it the first time you buy a package.', None),
    ('sign', 'Sign', 'pen-line', 'Confirming a transaction with your wallet.', 'Signing a cheque.'),
    ('claim', 'Claim', 'hand-coins', 'Moving earned income into your Withdrawable Balance, ready to withdraw.', None),
    ('direct', 'Direct', 'user-plus', 'Someone who joined with your link. Your directs are your level 1.', None),
    ('sponsor', 'Sponsor', 'users', 'The person whose link you joined with. It never changes.', None),
    ('total-deposit', 'Total deposit', 'piggy-bank', 'Your fresh packages plus everything reinvested. It decides your withdrawal split.', None),
    ('reinvest', 'Reinvest', 'repeat', 'The part of each withdrawal that goes back in as new business: 50%, 40% or 30%.', None),
    ('global-leg', 'Global leg', 'route', 'One line of every member in joining order. You earn 1% from deposits inside your window.', None),
    ('matched', 'Matched volume', 'arrow-left-right', 'The smaller of your two sides in level matching, for one day.', None),
    ('window72', '72-hour window', 'timer', 'The first three days after you join. The ALTRUVA presentation ties the ranks, and the Starter ticket, to two directs joining inside it.', 'A football transfer window: signings only count while it is open.'),
    ('utc', 'UTC', 'clock', 'The world\'s standard time. ALTRUVA days close at 00:00 UTC, 02:00 in South Africa.', None),
    ('kyc', 'KYC', 'scan-eye', 'Know Your Customer: the ID checks exchanges such as Binance and VALR require.', None),
    ('zar', 'ZAR', 'banknote', 'The South African rand.', None),
]


def p_gloss(here):
    terms = ''
    for id_, t, icn, d, like in GLOSS:
        lk = f'<p class="like"><b>Like:</b> {like}</p>' if like else ''
        terms += f'<article class="term" id="{id_}" data-term="{esc(t.lower() + " " + d.lower())}"><h3>{ic(icn)}{t}</h3><p>{d}</p>{lk}</article>'
    return f'''{phero("book-open-text", "Glossary: crypto words in plain English",
        "Every word you'll hear in the videos and the app, with an everyday example where it helps.")}
{sec(f"""<div class="gfilter"><label class="sr" for="gq">Find a word</label><input id="gq" class="field" type="search" placeholder="Find a word, like gas or renounced" autocomplete="off" data-gfilter></div>
<div class="gloss">{terms}</div><p class="fine" data-gempty hidden>No match. Try another word, or ask in the MTG TRIBE.</p>""")}
'''


# ======================================================================= SAFETY
def p_safe(here):
    return f'''{phero("shield-check", "Safety centre",
        "Six habits that protect your wallet, the scams to walk away from, and how to check a contract yourself.", pcls='cy')}
{sec(checks([
    "<b>Never share your recovery phrase.</b> Not with MTG, not with support, not with your sponsor. Nobody genuine will ever ask for it.",
    "<b>Copy links only from the person who introduced you,</b> and check it opens altruva.io. Then reopen ALTRUVA from your wallet's history.",
    "<b>Read every wallet screen before you tap Confirm.</b> The approval should match your package.",
    "<b>Keep at least $3 to $5 of BNB</b> for fees, so you're never stuck.",
    "<b>Only use money you can afford to lose,</b> and withdraw regularly.",
    "<b>Hide your balances and addresses</b> before you share a screenshot.",
]), "Six safety habits")}
{sec(checks([
    "\"Pay a fee to unlock your withdrawal.\"",
    "\"Send me your phrase so I can fix your account.\"",
    "Direct messages from \"ALTRUVA support\" or \"admin\".",
    "\"Send me USDT and I'll double it.\"",
    "Lookalike links with extra words or odd endings.",
], no=True), "Walk away if you hear", "Each of these is a scam pattern, whatever name it uses.")}
{sec(f"""{steps([
    ("Find the contract address", "<p>Ask the person who introduced you, or look in your wallet's history: the address you sent your package purchase to.</p>"),
    ("Open BscScan", "<p>Go to bscscan.com and paste the address in the search bar.</p>"),
    ("Check it's verified", "<p>Open the Contract tab. A green tick with \"Contract Source Code Verified\" means the code is public.</p>"),
    ("Check the owner", "<p>Under Read Contract, look for owner. 0x0000...0000 means ownership is renounced. Any other address still holds owner powers, so read what those functions can do.</p>"),
    ("Look for a proxy", "<p>If BscScan says the contract is a proxy, its logic can be upgraded even when the front looks renounced. Ask about it.</p>"),
])}
<div class="honest">{ic("info")}<div><b>What we know so far:</b> we haven't confirmed ALTRUVA's contract address, verification, audit or renounced status. This page will be updated when we do.</div></div>""",
    "Check a contract yourself", "Five checks anyone can do on a phone, for ALTRUVA or anything else.", id="contract")}
{sec(think("Can I take back an approval later?", "<p>Yes. BscScan's Token Approval Checker (bscscan.com/tokenapprovalchecker) lists the contracts allowed to use your tokens, and lets you revoke them. Revoking costs a few cents of BNB.</p>"))}
'''


# ======================================================================= DOWNLOADS
def mb(slug):
    p = MEDIA + slug + '.mp4'
    return f'{os.path.getsize(p) / 1e6:.1f} MB' if os.path.exists(p) else ''


def p_dl(here):
    def rows(codes):
        return ''.join(
            f'<li class="dlrow"><span class="dlt"><b><span class="vn">{V[k]["n"]}</span><span class="vt">{V[k]["short"]}</span></b><small>{mmss(V[k]["secs"])}, {mb(V[k]["slug"])}</small></span>'
            f'<a class="btn btn-ghost btn-sm" href="{A("media/" + V[k]["slug"] + ".mp4", here)}" download>{ic("download")}<span class="lbl">MP4</span></a></li>'
            for k in codes)
    wa_share = 'https://wa.me/?text=' + quote(SHARE_MSG)
    return f'''{phero("download", "Downloads",
        "Save the videos and the quick guide to your phone, and share the guide with your team.")}
{sec(f"""<div class="panel pad dlhero"><div class="phero-in">{ped("file-text", "lg")}<div class="stack"><h2 class="h3">ALTRUVA quick guide (PDF, 2 pages)</h2>
<p>Packages, the 100% split, the withdrawal split, the five joining steps, safety habits and every link, on two pages.</p>
<div class="btn-row"><a class="btn btn-gold btn-sm ring" href="{A("downloads/altruva-quick-guide-mtg.pdf", here)}" download>{ic("download")}<span class="lbl">Download the quick guide</span></a></div></div></div></div>""")}
{sec(f"""<div class="panel pad stack"><p class="fine">A ready message for WhatsApp. It points to this free guide, so people learn before they decide.</p>
<textarea class="field sharebox" rows="4" readonly aria-label="Share message">{esc(SHARE_MSG)}</textarea>
<div class="btn-row">{copy_btn("share", "Copy the message", size="sm")}{btn("Share on WhatsApp", wa_share, "wa", "whatsapp", "sm", ext=True)}</div></div>""",
    "Share kit", "We learn best when we teach others.")}
{sec(f"""<div class="grid2"><div class="stack"><h3 class="h3">Tutorials</h3><ul class="dllist">{rows(TUT)}</ul></div>
<div class="stack"><h3 class="h3">Explainers</h3><ul class="dllist">{rows(EXP)}</ul></div></div>
<div class="grid2" style="margin-top:20px"><div class="stack"><h3 class="h3">Tool trainings</h3><ul class="dllist">{rows(TOOL)}</ul></div></div>
<p class="fine">Sharing a video? Please share it as it is, with the risk notes kept in.</p>""", f"All {NV} videos")}
'''


# ======================================================================= CRYPTO CARD
def p_card(here):
    return f'''{phero("credit-card", "Spend your USDT with a crypto card",
        "Cashing out through an exchange works well (Tutorial 6). There's also a shorter road: a crypto debit card.", pcls='cy')}
{sec(f"""<div class="stack roads">
 <div class="road"><b>The exchange road</b><div class="rsteps"><span>SafePal</span>{ic("arrow-right")}<span>Exchange</span>{ic("arrow-right")}<span>Rand</span>{ic("arrow-right")}<span>Bank</span></div><span class="fine">Covered in Tutorial 6.</span></div>
 <div class="road cy"><b>The card road</b><div class="rsteps"><span>SafePal</span>{ic("arrow-right")}<span>Your card</span>{ic("arrow-right")}<span>Spend</span></div><span class="fine">Accepts USDT and USDC on BNB Smart Chain.</span></div>
</div>""", "Two roads to spending")}
{sec(f"""<div class="grid2">
 {box("One more basket", "<p>The card comes with an income opportunity of its own: one more way to avoid putting all your eggs in one basket.</p>", "layers")}
 {box("Its own rules", "<p>It's a separate product with its own fees and terms. MTG's full guide explains them before you decide.</p>", "file-text")}
</div>
<div class="btn-row" style="margin-top:22px">{btn("Open the crypto card guide", CARD_GUIDE, "gold", "credit-card", "", True, ext=True)}{wa_mtg_btn(label="Ask MTG on WhatsApp")}</div>
<p class="fine" style="margin-top:14px">The guide is MTG's own crypto card website. You can also ask your ALTRUVA sponsor. Sponsors, you're welcome to connect with MTG too.</p>""")}
'''


# ======================================================================= TRIBE
def p_tribe(here):
    return f'''{phero("message-circle", "Join the MTG TRIBE",
        "A WhatsApp community for action takers. Learn with others, ask questions, and share what works.", pcls='wa')}
{sec(f"""<div class="grid2">
 {box("What to expect", checks(["A diverse tribe: different opportunities, projects, tools, strategies, coins and tokens.", "Everything is shared for learning. Take what fits you and do your own research.", "Action takers welcome: we learn best when we teach others."]), "users")}
 {box("How to reach MTG", f"<p>WhatsApp messages and voice notes work best. MTG isn't a fan of phone calls.</p><p class='num'><b>WhatsApp: {WA_NUM}</b></p>", "mic")}
</div>
<div class="btn-row" style="margin-top:22px">{wa_group_btn('lg', 'Join the WhatsApp group', ring=True)}{wa_mtg_btn()}{btn("Follow on TikTok", TIKTOK, "ghost", "tiktok", ext=True)}</div>""")}
{sec(think("Where are the ALTRUVA Zoom links?", "<p>In the ALTRUVA WhatsApp groups. Ask the person who introduced you to ALTRUVA to add you to the right group.</p>", icon="video"))}
'''


# ======================================================================= DISCLAIMER
def p_disc(here):
    return f'''{phero("info", "Disclaimer",
        "Plain words about what this site is, and what it isn't.")}
{sec(f"""<div class="prose discfull">
<h2 class="h3">An independent guide</h2><p>This is not an official ALTRUVA website. It's made by MTG, an ALTRUVA member, to help people understand ALTRUVA before they decide anything.</p>
<h2 class="h3">Education, not advice</h2><p>Nothing here is financial, legal or tax advice, and nothing here is a recommendation to join or not to join. Always do your own research.</p>
<h2 class="h3">Affiliate links</h2><p>The Sign Up button copies MTG's ALTRUVA referral link. If you join through it, MTG becomes your sponsor and earns by the plan explained on these pages. The crypto card guide is MTG's own crypto card website and may include his referral links too.</p>
<h2 class="h3">Risk</h2><p>Earnings come from members' deposits and are not guaranteed. You can lose the money you put in. The top package is $100. Some people open more than one account: that's their own strategy and their own risk. Only use money you can afford to lose.</p>
<h2 class="h3">Facts and figures</h2><p>Figures were checked against the live ALTRUVA app on 24 Oct 2026. Apps change, so the app on your screen is always the final word. Examples are illustrations, not forecasts.</p>
<h2 class="h3">Your privacy</h2><p>This site has no sign-up, no cookies and no tracking. It remembers two things on your own device only: which videos you've watched, and whether you closed the menu. Fonts load from Google Fonts, and the rand converter asks CoinGecko for the live rate.</p>
<h2 class="h3">Names and logos</h2><p>The ALTRUVA name and logo belong to their owners and are used here only to identify what this guide is about. The videos and pages are MTG's own work.</p>
</div>""")}
'''
