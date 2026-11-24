"""Dashboard pages: Get started, Your own page, Tools, Help, More (Bitcoin Wealth), plus the order form."""
from core import *
from pages_learn import phero, honest, soon


# ======================================================================= JOIN
JOIN_NEEDS = ['A smartphone with the SafePal app', '0.001 BTC worth of BTCB, plus a little extra', 'A little BNB for network fees',
              'A VALR or Binance account to buy with rand', 'The sign-up link of the person who introduced you']
JOIN_STEPS = [
    ('Set up SafePal', 'Download SafePal from safepal.com, create a wallet, back it up two ways and keep only BNB, USDT and BTCB. Tutorial 1 shows every tap.'),
    ('Open a VALR or Binance account', 'Both let you buy crypto with rand. Many members keep both, as a backup.'),
    ('Buy BNB and send it to SafePal', 'Buy enough BNB for 0.001 BTC plus fees, then withdraw it to your SafePal BNB address on BNB Smart Chain (BEP20), and check the first and last characters of the address. Tutorial 2 shows every tap.'),
    ('Swap BNB to BTCB in SafePal', 'Swap a little more than you need (type 0.0011 BTCB), and keep some BNB for network fees. Never empty your BNB. Tutorial 3 shows every tap.'),
    ('Activate slot 1', 'Copy the sign-up link, paste it into SafePal\'s Explore tab, choose BNB Chain, check the referrer, then confirm twice in your wallet. Tutorial 3 shows every tap.'),
]

T3_CHECKS = ["Swap a little more than you need: type 0.0011 BTCB, so a little over 0.001 arrives", "Keep some BNB in your wallet for network fees",
             "On the registration page, check the referrer: it is the member ID of the person who invited you",
             "Your wallet asks twice: Approve, then Confirm again. Approve only the exact 0.001 BTC"]
T1_CHECKS = ["Download from safepal.com, never from a link in a message", "Two backups: Google Drive and paper", "Rename the wallet Bitcoin Wealth", "Keep only BNB (BEP20), USDT (BEP20) and BTCB (BEP20)"]


def written(code, here, label='Every step, in writing'):
    """the link from a video to its own page (the steps and the words, in writing)"""
    return f'<a class="btn btn-ghost btn-sm" href="{A(WATCH[code], here)}">{ic("list-checks")}<span class="lbl">{label}</span></a>'


T2_CHECKS = ["Pay by EFT from a bank account in your own name", "Type your VALR reference exactly as VALR shows it: it is how VALR knows the money is yours",
             "Buy BNB with your rand", "Withdraw to your SafePal BNB (BEP20) address on BNB Smart Chain, and check the first and last characters"]


def p_join(here):
    st = steps([(t, f'<p>{d}</p>') for t, d in JOIN_STEPS])
    return f'''{phero("rocket", "How to join Bitcoin Wealth, step by step",
        "Three stages, five steps, from an empty phone to slot 1. Take them one at a time, and watch the tutorial for each before you tap anything.",
        [("badge-check", "0.001 BTC once-off"), ("clock", "About 30 minutes"), ("smartphone", "All on your phone")])}
{sec(f"""<div class="two vstart"><div class="stack"><h3 class="h3">What you need</h3>{checks(JOIN_NEEDS)}
<p class="fine">On the recording day of Tutorial 1, Bitcoin was about $67,000, so 0.001 BTC was about $67. With fees and a little BNB, MTG suggested preparing <b>about $76, about R1,300</b>. Prices move every minute: <a class="inl" href="{A('dashboard/tools/bitcoin-to-rand/', here)}">check today's price in rand</a>.</p>
<div class="btn-row">{valr_btn()}{binance_btn()}{written('t1', here)}</div></div>
<div class="phone-wrap">{vid('t1', here)}</div></div>""", "Before you start")}
{sec(st, "The five steps")}
{sec(f"""<div class="two vstart vfirst"><div class="stack"><h3 class="h3 vhead">Tutorial 2: {V['t2']['title']}</h3><p class="vdesc">Steps 2 and 3, tap by tap. {V['t2']['desc']}</p>
{checks(T2_CHECKS)}
<div class="btn-row">{valr_btn()}{binance_btn()}{written('t2', here)}</div></div>
<div class="phone-wrap">{vid('t2', here)}</div></div>""", "Fund your SafePal")}
{sec(f"""<div class="two vstart vfirst"><div class="stack"><h3 class="h3 vhead">Tutorial 3: {V['t3']['title']}</h3><p class="vdesc">Steps 4 and 5, tap by tap. {V['t3']['desc']}</p>
{checks(T3_CHECKS)}
<div class="btn-row">{copy_btn('signup', 'Copy sign-up link', size='sm')}{written('t3', here)}</div>
<p class="fine">The button copies MTG's sign-up link. Introduced by someone else? Use their link, so they stay your sponsor.</p></div>
<div class="phone-wrap">{vid('t3', here)}</div></div>""", "Swap, sign up, activate slot 1", id="activate")}
{sec(honest("Before you activate.", "Approve only the exact amount you are paying, keep a little BNB for fees, and if someone else introduced you, use their link so they stay your sponsor."))}'''


# ======================================================================= VIDEOS
def p_tut(here):
    def block(code, n, checks_, extra=''):
        v = V[code]
        return sec(f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH[code], here)}">Tutorial {n}: {v['title']}</a></h2><p class="vdesc">{v['desc']}</p>
{checks(checks_)}{extra}
<div class="btn-row">{written(code, here)}</div></div>
<div class="phone-wrap">{vid(code, here, eager=(n == 1))}</div></div>""", id=f"tutorial-{n}")
    return f'''{phero("circle-play", "Bitcoin Wealth tutorial videos",
        "Three step-by-step videos take you from an empty phone to slot 1. Recorded on MTG's own phone, with every private detail hidden. Pause after each step and do it yourself.",
        [("film", f"{len(TUT)} tutorials, about {round(sum(V[k]['secs'] for k in TUT) / 60)} minutes"), ("list-checks", "Every step also in writing"), ("eye-off", "Private details hidden")])}
{block('t1', 1, T1_CHECKS)}
{block('t2', 2, T2_CHECKS, f'<p>Using Binance instead? The steps are very similar.</p><div class="btn-row">{valr_btn()}{binance_btn()}</div>')}
{block('t3', 3, T3_CHECKS, f'<div class="btn-row">{copy_btn("signup", "Copy sign-up link", size="sm")}{wa_group_btn(size="sm")}</div>')}
{sec(think("Do I really need to watch them all?", "<p>Yes, even if you think you already know. Each one shows a screen you'll meet sooner or later. Then share them: we learn best when we teach others.</p>"))}'''


PRESENT_CHECKS = ["What Bitcoin Wealth is, in plain pictures", "Where the 14 positions of a cycle pay", "The 12 slots, from 0.001 BTC up",
                  "Where to get more information, Zoom presentations and training"]


def p_exp(here):
    cards = ''.join(soon(p[0]) for p in PLANNED if p[0][0] == 'e')
    v = V['i1']
    # the presentation with Leo is the first video here that plays (MTG, 20 Nov 2026: "put it live on my website")
    first = f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH['i1'], here)}">{v['title']}: the presentation, with Leo</a></h2>
<p class="vdesc">The whole Bitcoin Wealth presentation in {round(v['secs'] / 60)} minutes. Leo shows it, slide by slide, and every moving part is drawn as he says it.</p>
{checks(PRESENT_CHECKS)}
<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{A(WATCH['i1'], here)}">{ic("list-checks")}<span class="lbl">All 10 chapters</span></a></div>
<p class="fine">The programme's own presentation, presented by Leo. Leo and his voice are made with AI.</p></div>
<div class="phone-wrap">{vid('i1', here)}</div></div>"""
    e = V['e1']
    # Explainer 1 comes first (MTG, 21 Nov 2026: "Push the explainer video live"): the plain-words start, then the whole plan
    e1 = f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH['e1'], here)}">Explainer 1: What is Bitcoin Wealth? It's not a coin</a></h2>
<p class="vdesc">Thandi asks what everyone asks, and Leo answers in plain words, in {mmss(e['secs'])}. Start here if you are new.</p>
{checks(["Why Bitcoin Wealth is not a coin, but a smart contract", "Bitcoin, BTCB and BNB, in plain words", "Where the money comes from, and what it costs to start"])}
<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{A(WATCH['e1'], here)}">{ic("list-checks")}<span class="lbl">Every Word, In Writing</span></a></div>
<p class="fine">Thandi and Leo, and their voices, are made with AI.</p></div>
<div class="phone-wrap">{vid('e1', here, eager=True, hero=True)}</div></div>"""
    e = V['e2']
    # Explainer 2 (MTG, 21 Nov 2026: "Put it live"): the 14 positions, seat by seat, right after the plain-words start
    e2 = f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH['e2'], here)}">Explainer 2: How the 14 positions pay</a></h2>
<p class="vdesc">Thandi asks who pays who, and Leo fills 14 seats with her, row by row, in {mmss(e['secs'])}. Watch this when you want to see where every payment goes.</p>
{checks(["The 14 seats under you: 2, then 4, then 8", "Where each of the 14 payments goes", "The Royal Pool, spillover, and why there is no withdraw button"])}
<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{A(WATCH['e2'], here)}">{ic("list-checks")}<span class="lbl">Every Word, In Writing</span></a></div>
<p class="fine">Thandi and Leo, and their voices, are made with AI.</p></div>
<div class="phone-wrap">{vid('e2', here)}</div></div>"""
    e = V['e3']
    # Explainer 3 (MTG, 22 Nov 2026: "Perfect! Put it live!"): the 12 slots and the once-off, right after where the payments go
    e3 = f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH['e3'], here)}">Explainer 3: The 12 slots and the once-off</a></h2>
<p class="vdesc">Thandi asks who pays for slots 2 to 12, and Leo shows it with two coins and seat 5, in {mmss(e['secs'])}. Watch this when you want to know what you actually pay.</p>
{checks(["The 12 slots, each double the one before", "Who pays for slot 2, and every slot after it", "What you pay: 0.001 BTC, once, plus small BNB fees"])}
<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{A(WATCH['e3'], here)}">{ic("list-checks")}<span class="lbl">Every Word, In Writing</span></a></div>
<p class="fine">Thandi and Leo, and their voices, are made with AI.</p></div>
<div class="phone-wrap">{vid('e3', here)}</div></div>"""
    e = V['e4']
    # Explainer 4 (MTG, 23 Nov 2026: "Put it live"): the stokvel side by side, after what you actually pay
    e4 = f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH['e4'], here)}">Explainer 4: Better than a stokvel?</a></h2>
<p class="vdesc">Thandi asks if Bitcoin Wealth is just a stokvel on the internet, and Leo answers six honest questions side by side, in {mmss(e['secs'])}. Watch this if you know stokvels and want the real difference.</p>
{checks(["Who holds the money, and who can see every payment", "The fees, what it pays in, and how much you put in", "Is your turn guaranteed: where the stokvel picture stops"])}
<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{A(WATCH['e4'], here)}">{ic("list-checks")}<span class="lbl">Every Word, In Writing</span></a></div>
<p class="fine">Thandi and Leo, and their voices, are made with AI.</p></div>
<div class="phone-wrap">{vid('e4', here)}</div></div>"""
    e = V['e5']
    # Explainer 5 (MTG, 24 Nov 2026: "Put this video live ... across all the pages and sections where it will make sense")
    e5 = f"""<div class="two vstart vfirst"><div class="stack"><h2 class="h3 vhead"><a class="hlink" href="{A(WATCH['e5'], here)}">Explainer 5: Check it yourself on BscScan</a></h2>
<p class="vdesc">Thandi asks how to read the open book, and Leo shows her on her phone, in four steps, with a real payment from 24 November 2026. {mmss(e['secs'])}. Watch this when you want to see it with your own eyes.</p>
{checks(["Type bscscan.com yourself and open the contract", "One real payment: in, and straight out", "Token Holdings, your own wallet, and your own website"])}
<div class="btn-row"><a class="btn btn-ghost btn-sm" href="{A(WATCH['e5'], here)}">{ic("list-checks")}<span class="lbl">Every Word, In Writing</span></a></div>
<p class="fine">Thandi and Leo, and their voices, are made with AI.</p></div>
<div class="phone-wrap">{vid('e5', here)}</div></div>"""
    n_soon = sum(1 for p in PLANNED if p[0][0] == 'e')
    n_ready = sum(1 for k in V if k[0] in 'ei')
    return f'''{phero("film", "Bitcoin Wealth explainer videos",
        "Start with Explainer 1: Thandi and Leo show what Bitcoin Wealth is in 3 minutes. Explainer 2 shows where all 14 payments go, Explainer 3 why you only pay for slot 1, Explainer 4 how it compares with a stokvel, and Explainer 5 how to check it yourself on BscScan. Then watch the whole plan in Leo's 5-minute presentation.",
        [("circle-play", f"{n_ready} ready to watch"), ("film", f"{n_soon} more explainer{'s' if n_soon != 1 else ''} on the way")])}
{sec(e1, id="explainer-1", sr="Start here: Explainer 1")}
{sec(e2, "Then: where all 14 payments go", id="explainer-2")}
{sec(e3, "Then: the 12 slots, and what you actually pay", id="explainer-3")}
{sec(e4, "Then: Bitcoin Wealth and the stokvel, side by side", id="explainer-4")}
{sec(e5, "Then: check it yourself, on your phone", id="explainer-5")}
{sec(first, "The whole plan, in 5 minutes", id="presentation")}
{sec(f'<div class="{"grid2" if cards.count("class=") > 1 and n_soon > 1 else "stack"}">{cards}</div>', "On the way")}
{sec(f"""<div class="grid3">
 {box("The 14 positions", f"<p>Watch the positions fill, live. <a class='inl' href='{A('dashboard/how-it-works/', here)}'>Open</a></p>", "network")}
 {box("The 12 slots", f"<p>Every slot and the once-off. <a class='inl' href='{A('dashboard/12-slots/', here)}'>Open</a></p>", "layers")}
 {box("Better than a stokvel?", f"<p>The honest scorecard. <a class='inl' href='{A('dashboard/stokvel/', here)}'>Open</a></p>", "users")}
</div>""", "Meanwhile, see it live")}'''


# ======================================================================= ZOOM
# Live On Zoom (MTG, 16 Nov 2026: "as beautiful as the JetUp page"). Everything comes from ZOOM in config.py: the calendar,
# the time zone table, the page script's data, the JSON-LD and the .ics. Page CSS: assets/zoom-live.css. Page script (the
# schedule maths, countdown, calendar dates, time zones; tested in Node): assets/zoom-live.js. Never write that MTG hosts them.
import datetime as _dt
from urllib.parse import quote as _quote
from zoneinfo import ZoneInfo as _Zone

ZDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ZFULL = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ZONES = [('South Africa', 'SAST', 'Africa/Johannesburg'), ('Nigeria', 'Lagos', 'Africa/Lagos'), ('United Kingdom', 'London', 'Europe/London'),
         ('Canada and US East', 'Toronto, New York', 'America/Toronto'), ('Australia', 'Sydney', 'Australia/Sydney')]
WA_ZOOM = WA_MTG + '?text=' + _quote(ZOOM_WA_TEXT)


def zsessions():
    """the ten weekly sessions in week order: dict(i, dow 0=Mon, day, full, t, h, m, lang, code, eve)"""
    out = []
    for d, t, lang in sorted(ZOOM, key=lambda z: (ZDAYS.index(z[0]), z[1])):
        h, m = map(int, t.split(':'))
        out.append(dict(dow=ZDAYS.index(d), day=d, full=ZFULL[ZDAYS.index(d)], t=t, h=h, m=m, lang=lang, code=ZOOM_LANG[lang], eve=h >= 17))
    for i, z in enumerate(out):
        z['i'] = i
    return out


def zgroups():
    """sessions with the same time and language, grouped for the table and JSON-LD (e.g. Monday to Friday 14:00 English)"""
    g = {}
    for z in zsessions():
        g.setdefault((z['t'], z['lang']), []).append(z)
    return sorted(g.values(), key=lambda ss: (ss[0]['dow'], ss[0]['t']))


def zdays_label(dows, full=True):
    names = ZFULL if full else ZDAYS
    if len(dows) == 1:
        return names[dows[0]]
    if len(dows) > 2 and dows == list(range(dows[0], dows[-1] + 1)):
        return f'{names[dows[0]]} to {names[dows[-1]]}'
    return ', '.join(names[d] for d in dows[:-1]) + ' and ' + names[dows[-1]]


def zfirst(z):
    """the first start of a session on or after ZOOM_FROM, as an aware datetime in South African time"""
    d0 = _dt.date.fromisoformat(ZOOM_FROM)
    d = d0 + _dt.timedelta(days=(z['dow'] - d0.weekday()) % 7)
    return _dt.datetime(d.year, d.month, d.day, z['h'], z['m'], tzinfo=_Zone(ZOOM_TZ))


def zutc(off):
    m = int(off.total_seconds() // 60)
    if not m:
        return 'UTC+0'
    a = abs(m)
    return 'UTC' + ('-' if m < 0 else '+') + str(a // 60) + (f':{a % 60:02d}' if a % 60 else '')


def zlang(z, cls=''):
    return f'<span class="lg l-{z["code"]}{" " + cls if cls else ""}">{z["lang"]}</span>'


def _zcal():
    days = []
    for dow in range(7):
        evs = [z for z in zsessions() if z['dow'] == dow]
        inner = ''.join(
            f'<div class="ev l-{z["code"]}{" eve" if z["eve"] else ""}" data-s="{z["i"]}"><span class="tm">{z["t"]} <small>SAST</small></span>'
            f'{zlang(z)}<span class="pt"><span class="e" aria-hidden="true">{"🌙" if z["eve"] else "☀️"}</span>{"Evening" if z["eve"] else "Afternoon"}</span>'
            f'<span class="yt"></span></div>' for z in evs) or '<p class="none">No live session</p>'
        days.append(f'<div class="day{"" if evs else " quiet"}" role="listitem" data-dow="{(dow + 1) % 7}"><div class="dh"><span class="dn">{ZDAYS[dow]}</span>'
                    f'<span class="dt"></span><span class="tdy">Today</span></div><div class="evs">{inner}</div></div>')
    return '\n'.join(days)


def _ztable():
    ref = zfirst(zsessions()[0])
    head = '<th scope="col">Session</th>' + ''.join(
        f'<th scope="col"{" class=sa" if k == 0 else ""}>{n}<small>{c}, <span class="off" data-tz="{tz}">{zutc(ref.astimezone(_Zone(tz)).utcoffset())}</span></small></th>'
        for k, (n, c, tz) in enumerate(ZONES)) + '<th scope="col" class="you js-only">Your time<small id="you-zone">your device</small></th>'
    rows = []
    for ss in zgroups():
        z0 = ss[0]
        st = zfirst(z0)
        cells = []
        for k, (n, c, tz) in enumerate(ZONES):
            lt = st.astimezone(_Zone(tz))
            shift = (lt.weekday() - z0['dow']) % 7
            dy = ''
            if shift:
                dy = f'<span class="dy">{zdays_label([(x["dow"] + shift) % 7 for x in ss], False)}</span>'
            cells.append(f'<td{" class=sa" if k == 0 else ""} data-label="{n} ({c})" data-tz="{tz}"><span class="tt">{lt:%H:%M}</span>{dy}</td>')
        cells.append('<td class="you js-only" data-label="Your time" data-tz="local"><span class="tt"></span></td>')
        note = '<small>Questions welcome in any language</small>' if z0['lang'] == 'English' and not z0['eve'] else ''
        rows.append(f'<tr data-s="{",".join(str(x["i"]) for x in ss)}">'
                    f'<th scope="row"><span class="rd">{zdays_label([x["dow"] for x in ss])}</span> {zlang(z0)}{note}</th>{"".join(cells)}</tr>')
    return (f'<table class="tzt"><caption class="sr">Each Bitcoin Wealth Zoom session in South African time and in other time zones</caption>'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>')


ZFAQ = [
    ('How do I get the Zoom link?',
     f'The Zoom links are only shared inside the MTG TRIBE WhatsApp group, never in public. Ask the person who invited you to add you to the group, '
     f'<a class="inl" href="{GROUP}" target="_blank" rel="noopener">join the group</a>, or '
     f'<a class="inl" href="{esc(WA_ZOOM)}" data-wa-text="{esc(ZOOM_WA_TEXT)}" target="_blank" rel="noopener">message MTG on WhatsApp</a> and ask for the link.'),
    ('What time is it where I live?',
     'Every time on this page is South African time (SAST, UTC+2, no daylight saving). The <a class="inl" href="#timezones">time zone table</a> '
     'shows Nigeria, the United Kingdom, Canada and US East and Australia, plus a Your time column worked out from your own device.'),
    ('Which language is each session in?',
     'Monday to Friday at 14:00 the sessions are in English, and questions are welcome in any language, like isiZulu. In the evenings: '
     + '; '.join(f'{zdays_label([x["dow"] for x in ss])} {ss[0]["t"]} {ss[0]["lang"]}' for ss in zgroups() if ss[0]['eve']) + '.'),
    ('Can I join from my phone?',
     'Yes. Zoom works on phones, tablets and computers. Install the Zoom app on your phone, then tap the link when it is shared in the group.'),
]


def zfaq_ld(url):
    return {'@type': 'FAQPage', '@id': url + '#faqpage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in ZFAQ]}


def zoom_ld(url, image):
    """EventSeries plus one Event per group of sessions (weekly eventSchedule), and the FAQ"""
    note = 'The Zoom link is shared inside the MTG TRIBE WhatsApp group.'
    where = {'@type': 'VirtualLocation', 'url': url}
    first = min(zfirst(z) for z in zsessions())
    evs = []
    for ss in zgroups():
        z0, st = ss[0], min(zfirst(z) for z in ss)
        en = st + _dt.timedelta(minutes=ZOOM_MIN)
        lab = zdays_label([x['dow'] for x in ss])
        id_ = url + f'#zoom-{z0["code"]}-{z0["t"].replace(":", "")}-{ZDAYS[z0["dow"]].lower()}'
        evs.append({'@type': 'Event', '@id': id_, 'name': f'Bitcoin Wealth live on Zoom in {z0["lang"]} ({lab} {z0["t"]})',
                    'description': f'Live Bitcoin Wealth Zoom session in {z0["lang"]}, every {lab} at {z0["t"]} South African time. {note}',
                    'url': url, 'image': image, 'inLanguage': z0['code'], 'startDate': st.isoformat(), 'endDate': en.isoformat(),
                    'eventAttendanceMode': 'https://schema.org/OnlineEventAttendanceMode', 'eventStatus': 'https://schema.org/EventScheduled',
                    'location': where, 'isAccessibleForFree': True, 'superEvent': {'@id': url + '#series'},
                    'eventSchedule': {'@type': 'Schedule', 'startDate': st.date().isoformat(), 'repeatFrequency': 'P1W',
                                      'byDay': [f'https://schema.org/{x["full"]}' for x in ss], 'startTime': z0['t'] + ':00',
                                      'endTime': en.strftime('%H:%M:%S'), 'duration': f'PT{ZOOM_MIN}M', 'scheduleTimezone': ZOOM_TZ}})
    series = {'@type': 'EventSeries', '@id': url + '#series', 'name': 'Bitcoin Wealth live Zoom sessions',
              'description': (f'{len(ZOOM)} live Bitcoin Wealth Zoom sessions every week in {len(ZOOM_LANG)} languages ('
                              + ', '.join(ZOOM_LANG) + '), in South African time. ' + note),
              'url': url, 'image': image, 'inLanguage': list(ZOOM_LANG.values()), 'startDate': first.isoformat(),
              'eventAttendanceMode': 'https://schema.org/OnlineEventAttendanceMode', 'eventStatus': 'https://schema.org/EventScheduled',
              'location': where, 'isAccessibleForFree': True, 'subEvent': [{'@id': e['@id']} for e in evs]}
    return [series] + evs + [zfaq_ld(url)]


def zoom_ics(url):
    """the weekly schedule as an iCalendar file: ten weekly events in Africa/Johannesburg (with its VTIMEZONE),
    CRLF line ends, lines folded at 75 bytes, and no Zoom link inside (it is shared in the WhatsApp group)"""
    def tx(v):
        return v.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')

    def fold(line):
        b, out = line.encode('utf-8'), []
        lim = 75
        while len(b) > lim:
            cut = lim
            while (b[cut] & 0xC0) == 0x80:      # never split a UTF-8 character
                cut -= 1
            out.append(b[:cut])
            b = b[cut:]
            lim = 74                             # continuation lines start with a space
        out.append(b)
        return b'\r\n '.join(out).decode('utf-8')
    by = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//MTG TRIBE//Bitcoin Wealth Zoom schedule//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
             'X-WR-CALNAME:Bitcoin Wealth live on Zoom', 'X-WR-TIMEZONE:' + ZOOM_TZ,
             'BEGIN:VTIMEZONE', 'TZID:' + ZOOM_TZ, 'X-LIC-LOCATION:' + ZOOM_TZ, 'BEGIN:STANDARD', 'DTSTART:19700101T000000',
             'TZOFFSETFROM:+0200', 'TZOFFSETTO:+0200', 'TZNAME:SAST', 'END:STANDARD', 'END:VTIMEZONE']
    stamp = ZOOM_FROM.replace('-', '') + 'T000000Z'
    for z in zsessions():
        st = zfirst(z)
        extra = ' Questions are welcome in any language, like isiZulu.' if z['lang'] == 'English' and not z['eve'] else ''
        lines += ['BEGIN:VEVENT', f'UID:bw-zoom-{z["day"].lower()}-{z["t"].replace(":", "")}-{z["code"]}@mtgtribe.com', 'DTSTAMP:' + stamp,
                  f'DTSTART;TZID={ZOOM_TZ}:{st:%Y%m%dT%H%M%S}', f'DURATION:PT{ZOOM_MIN}M', 'RRULE:FREQ=WEEKLY;BYDAY=' + by[z['dow']],
                  'SUMMARY:' + tx(f'Bitcoin Wealth Zoom: {z["lang"]} session ({z["full"]} {z["t"]})'),
                  'DESCRIPTION:' + tx(f'Live Bitcoin Wealth session on Zoom in {z["lang"]}.{extra} The Zoom link is shared inside the MTG TRIBE '
                                      f'WhatsApp group: {GROUP} or ask MTG on WhatsApp: {WA_MTG} Schedule and time zones: {url}'),
                  'LOCATION:' + tx('Zoom (link in the MTG TRIBE WhatsApp group)'), 'URL:' + url, 'STATUS:CONFIRMED', 'TRANSP:OPAQUE', 'END:VEVENT']
    lines.append('END:VCALENDAR')
    return '\r\n'.join(fold(x) for x in lines) + '\r\n'


def zoom_head(here):
    """the page-only stylesheet, after bw.css"""
    return f'\n<link rel="stylesheet" href="{A("assets/zoom-live.css", here)}">'


def p_zoom(here):
    ss = zsessions()
    data = json.dumps({'tz': ZOOM_TZ, 's': [dict(d=(z['dow'] + 1) % 7, h=z['h'], m=z['m'], l=z['lang'], e=int(z['eve'])) for z in ss]},
                      separators=(',', ':'), ensure_ascii=False)
    legend = ''.join(f'<span><i class="l-{c}"></i>{n}</span>' for n, c in ZOOM_LANG.items())
    hero_langs = ''.join(f'<span class="lg l-{c}">{n}</span>' for n, c in ZOOM_LANG.items())
    ics = L(here + ZOOM_ICS, here)
    wa_btn = btn('Message MTG on WhatsApp', WA_ZOOM, 'ghost', 'message-circle', 'lg', ext=True, attrs=f'data-wa-text="{esc(ZOOM_WA_TEXT)}"')
    faq = ''.join(f'<details><summary><span>{q}</span>{ic("chevron-down")}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in ZFAQ)
    evening = '; '.join(f'{zdays_label([x["dow"] for x in g])} {g[0]["t"]} {g[0]["lang"]}' for g in zgroups() if g[0]['eve'])
    rings = '<i></i>' * 10
    return f'''<section class="sec zl zl-hero" aria-labelledby="zl-h1"><div class="wrap zl-q">
 <div class="zl-hgrid">
  <div class="zl-copy">
   <div class="zl-emos" aria-hidden="true"><span>📣</span><span>🕗</span></div>
   <p class="eyebrow">Live on Zoom · {len(ss)} sessions a week</p>
   <h1 class="h1" id="zl-h1">Live on <span class="hl">Zoom</span></h1>
   <p class="lead">Meet the community, ask anything and watch it explained live. Weekdays at 14:00 in English, and five evenings a week in four languages.</p>
   <p class="zl-tz">{ic("clock")}<span>All times are South African time (SAST, UTC+2)</span></p>
   <p class="zl-langs"><span class="sr">Languages: </span>{hero_langs}</p>
   <div class="btn-row">{btn("Get the Zoom link", "#link", "gold", "whatsapp", "", True)}{btn("See the calendar", "#calendar", "ghost", "calendar-days")}</div>
  </div>
  <div class="glass nxcard" id="next" aria-labelledby="nx-name">
   <p class="nx-lab"><span class="dot" aria-hidden="true"></span><span id="nx-lab">Next live session</span></p>
   <h2 class="nx-h" id="nx-name">Every weekday on Zoom</h2>
   <p class="nx-meta js-only" id="nx-meta"></p>
   <p class="nx-when" id="nx-when">Monday to Friday at 14:00 in English. Evenings: {evening}. South African time.</p>
   <p class="cd js-only" id="nx-cd" role="timer" aria-label="Time until the session starts">
    <span class="cdu"><b id="cd-d">0</b><span>Days</span></span><span class="cdu"><b id="cd-h">0</b><span>Hours</span></span><span class="cdu"><b id="cd-m">0</b><span>Minutes</span></span>
   </p>
   <p class="nx-local js-only" id="nx-local"></p>
   <p class="nx-after js-only" id="nx-after"></p>
   {btn("Get the Zoom link", "#link", "gold", "whatsapp", "lg", cls="nx-btn")}
  </div>
 </div>
</div></section>

<section class="sec zl" id="calendar" aria-labelledby="cal-h"><div class="wrap zl-q">
 <div class="sec-head"><p class="eyebrow">The weekly calendar</p><h2 class="h2" id="cal-h">{len(ss)} sessions. <span class="hl">Every week.</span></h2>
  <p class="lead">Two sessions every weekday, one in the afternoon and one in the evening. Today is marked, and the dates follow South African time.</p></div>
 <div class="cal-wrap">
  <div class="cal">
   <div class="rings" aria-hidden="true">{rings}</div>
   <div class="band">
    <div class="ttl"><p class="kick">Bitcoin Wealth · Live on Zoom</p><p class="bt">Weekly Zoom <span class="hl">calendar</span></p>
     <p class="tzl">South African time (SAST, UTC+2)<span id="cal-week"></span></p></div>
    <img class="cal-logo" src="{A("img/bitcoin-wealth-logo-192.png", here)}" width="96" height="96" alt="" loading="lazy" decoding="async">
   </div>
   <div class="days" role="list">
{_zcal()}
   </div>
   <div class="cal-foot"><div class="legend">{legend}</div><span>Zoom link: in the WhatsApp group</span></div>
  </div>
 </div>
 <p class="fine tznote">The 14:00 sessions are in English, and questions are welcome in any language, like isiZulu.</p>
</div></section>

<section class="sec zl" id="timezones" aria-labelledby="tz-h"><div class="wrap zl-q">
 <div class="sec-head"><p class="eyebrow">Time zones</p><h2 class="h2" id="tz-h">What time is that <span class="hl">where you are?</span></h2>
  <p class="lead">The same sessions in the tribe's biggest time zones. Daylight saving is taken care of: the times follow the clocks in each country.</p></div>
 <div class="glass tzcard">{_ztable()}</div>
 <p class="fine tznote">A day tag (like <span class="dy">Tue</span>) means the session falls on a different day there. Somewhere else? The Your time column works it out from your own device.</p>
</div></section>

<section class="sec zl" id="link" aria-labelledby="link-h"><div class="wrap zl-q">
 <div class="sec-head"><p class="eyebrow">How to get the Zoom link</p><h2 class="h2" id="link-h">The link lives on <span class="hl">WhatsApp</span></h2>
  <p class="lead">The Zoom links are only shared inside the MTG TRIBE WhatsApp group, never in public. Ask the person who invited you to add you to the group, or choose the way that suits you.</p></div>
 <div class="ways">
  <div class="glass way"><p class="eyebrow">Way 1 · The group</p><h3>Join the MTG TRIBE group</h3>
   <div class="btn-row">{wa_group_btn(label='Join the MTG TRIBE', ring=True)}</div>
   <p class="what">Opens WhatsApp and the MTG TRIBE group, where the Zoom links for the sessions are shared.</p></div>
  <div class="glass way"><p class="eyebrow">Way 2 · One on one</p><h3>Ask MTG directly</h3>
   <div class="btn-row">{wa_btn}</div>
   <p class="what">Opens a private WhatsApp chat with MTG, with a short message asking for the Zoom link of the next session, ready to send.</p></div>
 </div>
</div></section>

<section class="sec zl" id="add" aria-labelledby="add-h"><div class="wrap zl-q">
 <div class="glass addcal"><span class="big" aria-hidden="true">🗓️</span>
  <div><h2 class="h3" id="add-h">Add the schedule to <span class="gold">your calendar</span></h2>
   <p>{len(ss)} weekly reminders, set in South African time, so your phone or computer shows each one in your own time. No Zoom link inside: the link is shared in the WhatsApp group.</p></div>
  <a class="btn btn-gold btn-lg ring" href="{esc(ics)}" download="{ZOOM_ICS}">{ic("calendar-plus")}<span class="lbl">Add to my calendar</span></a>
 </div>
</div></section>

<section class="sec zl" id="faq" aria-labelledby="faq-h"><div class="wrap zl-q">
 <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-h">Good to <span class="hl">know</span></h2></div>
 <div class="faq">{faq}</div>
</div></section>
<script type="application/json" id="zl-data">{data}</script>
<script src="{A("assets/zoom-live.js", here)}" defer></script>'''


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
{sec(f'<div class="stack">{jump_card("e5", 178.0, "See your own website, in a minute", "Leo shows what it looks like: this whole guide at bitcoinwealthpays.com/zizi, with Zizi&#39;s name, WhatsApp and referral link on every Join button.", here)}</div>', "See what yours could look like")}
{sec(f"""<div class="offer glass"><div class="offer-copy">
 <h2 class="h2">What you get</h2>
 {checks(["A full copy of this guide, kept up to date with new videos", "Your name and photo on it", "Your Bitcoin Wealth referral link on every sign-up button", "Your WhatsApp, WhatsApp group and social links", "Your choice of address: mtgtribe.com/bw/yourname or bitcoinwealthpays.com/yourname", "Five free edits to make it yours (from the sixth, a small fee depending on the size)"])}
 <div class="price"><b>R1,000</b><span>once-off<br><small>Pay in rand, USDT BEP20 or USDT TRC20. You agree the method with MTG on WhatsApp.</small></span></div>
 <div class="btn-row">{order_btn(size='lg')}</div>
</div><div class="offer-copy">
 <h2 class="h2">How it works</h2>
 {steps([("Fill in the order form", "<p>Two minutes. Your details go straight to MTG on WhatsApp.</p>"), ("MTG builds your page", "<p>You agree the payment method together on WhatsApp.</p>"), ("You check it", "<p>Love it? Then you pay. Changed your mind? MTG deletes it. Nothing to lose.</p>"), ("Share your one link", "<p>Send it to potential business partners, post it in your groups and on your socials.</p>")])}
</div></div>""", "Everything, up front")}
{sec(f"""<div class="secret glass big">{ic('lock-keyhole')}<div><b>The part we only tell owners</b><p>MTG uses a traffic source that makes it much easier to put a page like yours in front of people who already watch crypto ads all day. It has its own income stream too. No guarantee those visitors join. Once your BW Tribe Page is built, paid and yours, MTG shows you how it works, with its own tutorials and explainers.</p></div></div>""")}'''


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
    return f'''{phero("calculator", "Bitcoin Wealth Slot Calculator", "Every Bitcoin Wealth slot in BTC and rand, and what a completed cycle sends to your wallet, at today's Bitcoin price.",
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
        ('How much does it cost to start?', 'Slot 1 costs 0.001 BTC (paid as BTCB), plus small network fees in BNB. It\'s a once-off: slots 2 to 12 are bought automatically from the cycle below, as soon as its seat 5 is filled.'),
        ('Is it guaranteed to pay?', 'No. Every payout comes from another member\'s slot payment. If new activations slow down, payouts slow down. Only use money you can afford to lose.'),
        ('How do I join Bitcoin Wealth?', 'In three stages, all on your phone: set up a SafePal wallet, buy BNB with rand on VALR or Binance and send it to SafePal, then swap it to BTCB and activate slot 1 with the link of the person who invited you. Three tutorial videos show every tap, and each has its steps in writing.'),
        ('How do you earn Bitcoin with Bitcoin Wealth?', 'By the plan\'s rules, when the 14 positions below you fill, six of those payments land in your own wallet as BTCB (Bitcoin\'s value on BNB Smart Chain), two buy your next slot and one recycles you. Every payment comes from another member activating a slot, so it depends on those positions filling: nothing is guaranteed.'),
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
    return f'''{phero("circle-help", "Bitcoin Wealth FAQ: straight answers", "The questions people ask most, answered plainly. Can't find yours? Ask in the MTG TRIBE.")}
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
    return f'''{phero("shield-check", "Bitcoin Wealth safety centre", "Six habits that protect your wallet, whatever you use it for.")}
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
<div class="fbot"><span>© 2026 MTG 👑 | Your Digital Architect. <a class="inl" href="{HUB}/">mtgtribe.com</a></span><span class="sig">Let's Get This Crypto! 💪</span></div></div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>window.BW={{"wa":"{WA_MTG}"}};window.BWV={{}};</script>
<script src="{A('assets/bw.js', here)}" defer></script>
<script src="{HUB}/assets/zoom-cta.js?v=5" defer></script>
<script src="{HUB}/assets/wa-message.js?v=2" defer></script>'''
    desc = 'Order your BW Tribe Page: your own copy of the Bitcoin Wealth guide with your referral link built in. R1,000 once-off, paid only after it is built.'
    hd = head('Order your BW Tribe Page', desc, '', here, og_key='order')
    hd = hd.replace(f'<link rel="canonical" href="{SITE}{BASE}">', f'<link rel="canonical" href="{SITE}{ORDER}">').replace(
        f'<meta property="og:url" content="{SITE}{BASE}">', f'<meta property="og:url" content="{SITE}{ORDER}">')
    return hd, body
