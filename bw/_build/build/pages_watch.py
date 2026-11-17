"""A page of its own for each tutorial video: the video on top, then every step in writing with its time.

MTG, 17 Nov 2026: "All the videos must be named such that when people browse the internet and search for anything related to
Bitcoin Wealth ... these videos can actually rank all by themselves, leading to my Bitcoin Wealth website." A search engine
lists a video on its own only from a page where that video is the main thing, and an AI search tool can only quote what is
written. So each tutorial gets this page: its search name as the heading, the video in the laptop frame, the sections as key
moments, and the words MTG says, step by step (from the tutorial's own build: mtg-studio tutorials/chapters.py).
A time button starts the video at that step. Config: WATCH_PAGES. Styles: "TUTORIAL PAGE" in bw.css.
"""
import json
from core import *
from pages_learn import phero, honest

# what a card in the video is called on the page (the cards between the steps)
CARD = {'web3': 'Why a Web3 wallet?', 'paper': 'Write your 12 words on paper', 'btcb': 'What is BTCB?', 'why2': 'Prices change every day',
        'rtp': 'Tick Real-time payment', 'copy': 'For builders: a website like this one', 'zoom': 'Live on Zoom', 'join': 'Ready to join?',
        'join3': 'Ready to join?', 'next': 'Next video', 'done3': 'All 3 tutorials done'}
# the sections of each video, in sentence case (the boards in the video show them in capitals)
SECTIONS = {
    't1': ['Download the official SafePal app', 'Back up your wallet, two ways', 'Clean up your wallet', 'What it costs to start'],
    't2': ['Deposit rand into VALR', 'Buy BNB', 'Send your BNB to SafePal'],
    't3': ['Swap BNB for BTCB', "Sign up with your sponsor's link", 'Activate slot 1', 'Get back into your dashboard, any time'],
}
LEAD = {
    't1': "Tutorial 1 of 3. Download SafePal from the official site, create a brand new wallet, back it up two ways, and keep only the three coins Bitcoin Wealth needs. Watch it, then follow every step in writing below.",
    't2': "Tutorial 2 of 3. Send rand from your bank to VALR with your own reference, buy BNB with it, and send that BNB to your SafePal wallet on BNB Smart Chain. Watch it, then follow every step in writing below.",
    't3': "Tutorial 3 of 3, the final step. Swap BNB for BTCB in SafePal, sign up with the link of the person who invited you, and activate slot 1 with two confirmations. Then see how to get back into your dashboard, any time.",
}
WATCH_ORDER = ['t1', 't2', 't3']


def load(code):
    """the video's beats, grouped: (intro beats, [(section title, start, end, beats)], closing beats)"""
    d = json.load(open(STUDIO + '/' + WATCH_PAGES[code][2], encoding='utf-8'))
    assert abs(d['total'] - V[code]['secs']) < 1.5, (code, d['total'], V[code]['secs'])
    beats = d['beats']; names = SECTIONS[code]
    boards = [i for i, b in enumerate(beats) if b['kind'] == 'board']
    assert len(boards) == len(names), (code, len(boards), len(names))
    # the closing starts at the recap (the second list of the video)
    lists = [i for i, b in enumerate(beats) if b['kind'] == 'list']
    close = lists[-1]
    intro = beats[:boards[0]]
    secs = []
    for j, i in enumerate(boards):
        end = boards[j + 1] if j + 1 < len(boards) else close
        secs.append((names[j], beats[i]['start'], beats[end]['start'], beats[i:end]))
    return intro, secs, beats[close:]


def slogan(t):
    """MTG's slogan is always written in full, with its emoji"""
    return t.replace("Let's Get This Crypto!", "Let's Get This Crypto! 💪")


def said(beat):
    """the words of one beat as paragraphs: MTG's lines together, Leo's lines marked as his"""
    out = []; buf = []
    for w in beat['words']:
        if not w['text']:
            continue
        if w['who'] == 'Leo':
            if buf:
                out.append('<p>' + esc(' '.join(buf)) + '</p>'); buf = []
            out.append(f'<p class="leo"><b>Leo, the mascot:</b> {esc(w["text"])}</p>')
        else:
            buf.append(slogan(w['text']))
    if buf:
        out.append('<p>' + esc(' '.join(buf)) + '</p>')
    return ''.join(out)


def said_plain(beats):
    return slogan(' '.join(w['text'] for b in beats for w in b['words'] if w['text']))


def jump(code, t, what):
    """a time button: it starts the video at that step"""
    return (f'<button type="button" class="tjump" data-play="{code}" data-at="{t:.1f}" aria-label="Play from {mmss(t)}: {esc(what)}">'
            f'{ic("play")}<span>{mmss(t)}</span></button>')


def watch_ld(code):
    """the video with its words and its key moments, and the steps as a how-to, for search engines and AI search"""
    intro, secs, close = load(code)
    url = SITE + BASE + WATCH[code]
    clips = [{'@type': 'Clip', 'name': name, 'startOffset': int(a), 'endOffset': int(b), 'url': f'{url}?t={int(a)}'} for name, a, b, _ in secs]
    words = ' '.join(x for x in [said_plain(intro)] + [said_plain(bs) for _, _, _, bs in secs] + [said_plain(close)] if x)
    vo = video_obj(code, extra={'transcript': words, 'hasPart': clips})
    how = {'@type': 'HowTo', 'name': WATCH_PAGES[code][1], 'description': V[code]['desc'], 'inLanguage': 'en-ZA',
           'totalTime': iso_dur(V[code]['secs']), 'video': {'@id': url + '#video-' + code},
           'step': [{'@type': 'HowToSection', 'name': name, 'position': i + 1,
                     'itemListElement': [{'@type': 'HowToStep', 'position': j + 1, 'name': b['title'], 'text': said_plain([b]), 'url': f'{url}?t={int(b["start"])}'}
                                         for j, b in enumerate(x for x in bs if x['kind'] == 'phone')]}
                    for i, (name, a, b_, bs) in enumerate(secs)]}
    return [vo, how]


def p_watch(code):
    def page(here):
        v = V[code]; path, h1, _ = WATCH_PAGES[code]
        intro, secs, close = load(code)
        i = WATCH_ORDER.index(code)
        # beside the video: what it covers, and the one action that fits this tutorial
        acts = {'t1': valr_btn() + binance_btn() + wa_group_btn(size='sm', label='Ask the MTG TRIBE'),
                't2': valr_btn() + binance_btn() + wa_group_btn(size='sm', label='Ask the MTG TRIBE'),
                't3': copy_btn('signup', 'Copy sign-up link', size='sm') + wa_group_btn(size='sm', label='Ask the MTG TRIBE')}[code]
        note = {'t1': 'No VALR or Binance account yet? Open one now, so it is verified by the time you reach Tutorial 2.',
                't2': 'Both exchanges let you buy crypto with rand. Many members keep both, as a backup.',
                't3': 'The button copies MTG\'s sign-up link. Invited by someone else? Use their link, so they stay your sponsor.'}[code]
        covers = ''.join(f'<li>{ic("circle-check")}<span><b>{esc(name)}</b> <button type="button" class="tjump sm" data-play="{code}" data-at="{a:.1f}" '
                         f'aria-label="Play from {mmss(a)}: {esc(name)}">{ic("play")}<span>{mmss(a)}</span></button></span></li>' for name, a, b, _ in secs)
        top = f"""<div class="two vstart watch-top"><div class="phone-wrap" data-watch="{code}">{vid(code, here, eager=True, hero=True)}</div>
<div class="stack"><h2 class="h3">In this video</h2><ul class="checks wcov-list">{covers}</ul>
<p class="fine">Tap a time to start the video at that part. It plays in a phone frame and closes itself at the end.</p>
<div class="btn-row">{acts}</div><p class="fine">{note}</p></div></div>"""
        # every step in writing
        n = 0; blocks = ''

        def item(b):
            """one beat as a list item: a numbered step (what the phone shows), or an aside (a card between the steps)"""
            nonlocal n
            if b['kind'] == 'phone':
                n += 1
                return (f'<li class="wstep" id="step-{n}"><span class="wn">{n}</span><div class="wb"><div class="wst"><h4>{esc(b["title"])}</h4>'
                        f'{jump(code, b["start"], b["title"])}</div>{said(b)}</div></li>')
            t = CARD.get(b['title'], b['title'])
            return (f'<li class="wstep aside"><span class="wn" aria-hidden="true">{ic("info")}</span><div class="wb"><div class="wst"><h4>{esc(t)}</h4>'
                    f'{jump(code, b["start"], t)}</div>{said(b)}</div></li>')
        opening = ''.join(said(b) for b in intro if b['kind'] in ('title', 'list'))
        pre = ''.join(item(b) for b in intro if b['kind'] not in ('title', 'list'))      # the video's step numbers start here
        blocks += (f'<div class="wsec glass"><div class="wsec-h"><h3 class="h3">Welcome</h3>{jump(code, 0, "the start")}</div><div class="wsaid">{opening}</div>'
                   + (f'<ol class="wsteps wpre">{pre}</ol>' if pre else '') + '</div>')
        for k, (name, a, b_, bs) in enumerate(secs):
            lis = ''
            for b in bs:
                if b['kind'] == 'board':
                    if b['words']:      # Leo opens the section
                        lis += f'<li class="wstep aside"><span class="wn" aria-hidden="true">{ic("message-circle")}</span><div class="wb">{said(b)}</div></li>'
                    continue
                lis += item(b)
            blocks += (f'<div class="wsec glass" id="part-{k + 1}"><div class="wsec-h"><h3 class="h3"><span class="wpart">Part {k + 1}</span>{esc(name)}</h3>'
                       f'{jump(code, a, name)}</div><ol class="wsteps">{lis}</ol></div>')
        CLOSE = dict(CARD, copy='One more thing')
        closing = ''.join((f'<h3 class="h3 wsub">{esc(CLOSE.get(b["title"], b["title"]))}</h3>' if b['kind'] == 'card' else
                           '<h3 class="h3 wsub">Recap</h3>' if b['kind'] == 'list' else '<h3 class="h3 wsub">Closing words</h3>') + said(b) for b in close)
        blocks += (f'<details class="wsec glass wclose"><summary><span class="h3">Recap and closing words</span>{ic("chevron-down")}</summary>'
                   f'<div class="wsaid">{closing}</div></details>')
        # the other tutorials
        nav = ''
        for c in WATCH_ORDER:
            cur = c == code
            tag = 'span' if cur else 'a'
            href = '' if cur else f' href="{A(WATCH[c], here)}"'
            nav += (f'<li><{tag} class="wtile glass{" on" if cur else ""}"{href}{" aria-current=page" if cur else ""}><small>{V[c]["label"]} · {mmss(V[c]["secs"])}</small>'
                    f'<b>{esc(V[c]["short"])}</b><span>{"You are here" if cur else "Open it"}</span></{tag}></li>')
        after = {'t1': ("Wallet ready?", f'Next, fund it: <a class="inl" href="{A(WATCH["t2"], here)}">Tutorial 2, buy BNB and send it to SafePal</a>.'),
                 't2': ("BNB in your SafePal?", f'Next, the final step: <a class="inl" href="{A(WATCH["t3"], here)}">Tutorial 3, swap to BTCB and activate slot 1</a>.'),
                 't3': ("Slot 1 active?", f'Share this guide with the people you invite, or get <a class="inl" href="{A("dashboard/bw-tribe-page/", here)}">your own BW Tribe Page</a> with your link inside. We learn best when we teach others.')}[code]
        return f'''{phero("circle-play", h1, LEAD[code],
        [("clock", f"{mmss(v['secs'])} video"), ("smartphone", "Recorded on MTG's phone"), ("eye-off", "Private details hidden")])}
{sec(top, sr="Watch the video")}
{sec(f'<div class="wlist">{blocks}</div>', "Every step, in writing", "The words MTG says in the video, step by step. Tap a time to watch that step.", id="steps")}
{sec(f'<ul class="wtiles">{nav}</ul>{honest(after[0], after[1])}', "The 3 tutorials, in order", id="more")}'''
    return page
