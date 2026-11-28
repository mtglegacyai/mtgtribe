"""Builds mtgtribe.com/mint (MoveMint, MINT on Solana): one page, MTG's guide (MTG, 28 Nov 2026).

python3 mint/_build/build.py            writes mint/index.html
MINT_PREVIEW=1 python3 mint/_build/build.py <out dir>   writes a private preview copy (relative links, lighter videos,
                                                         YouTube shown as a note: the preview host cannot embed it)

Videos: MEDIA below. The MP4s are not in the repository (GitHub Pages size): they live in mint/media/ locally until MTG picks
where they are hosted for the live site (Cloudflare R2, like /bw, is the plan). Change MEDIA to that address when it exists.
Every buy, sign-up and copy button uses MTG's invite link (REF), never the official site. No em or en dashes anywhere."""
import hashlib, html, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE = 'https://mtgtribe.com'
URL = SITE + '/mint/'
REF = 'https://app.movemint.vip/buy/mtg'
CA = '1PPQkxYy2wUvKkUXMnDkiDrqx5Hfp2nbDju11cvHeFW'
YT = 'bPdUpYZ1H8k'
MEDIA = '/mint/media/'
PREVIEW = os.environ.get('MINT_PREVIEW') == '1'
TODAY = '2026-11-28'

def ver(rel):
    p = os.path.join(REPO, rel.lstrip('/'))
    if not os.path.exists(p): return 'x'
    return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
def a(rel): return rel + '?v=' + ver(rel)
def esc(s): return html.escape(s, quote=True)

# ------------------------------------------------------------------ icons (lucide, ISC licence) and the player's own
ICONS = {
 'home': '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 'play': '<polygon points="6 3 20 12 6 21 6 3"/>',
 'steps': '<path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/><path d="M13 6h8"/><path d="M13 12h8"/><path d="M13 18h8"/>',
 'help': '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
 'coins': '<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/>',
 'copy': '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 'ext': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
 'shield': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 'wallet': '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
 'spark': '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
 'feet': '<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/>',
 'link': '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 'menu': '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
 'up': '<path d="m18 15-6-6-6 6"/>',
 'down': '<path d="m6 9 6 6 6-6"/>',
 'phone': '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
 'swap': '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
 'trend': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
 'zap': '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 'badge': '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>',
 'chat': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
}
SOCIAL = open(os.path.join(HERE, 'social-symbols.svg')).read()
def ic(name, cls=''): return f'<svg class="ic{(" " + cls) if cls else ""}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' +
  ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items()) +
  '<symbol id="i-max" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></symbol>'
  '<symbol id="i-min" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></symbol>'
  '<symbol id="i-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></symbol>'
  '<symbol id="i-pf" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M8 5.2v13.6a1 1 0 0 0 1.5.86l11-6.8a1 1 0 0 0 0-1.72l-11-6.8A1 1 0 0 0 8 5.2z"/></symbol>' +
  SOCIAL + '</defs></svg>')

# ------------------------------------------------------------------ the videos
# o: 'v' plays in the pop-up's phone, 'h' plays in place in the laptop. Every one shows as a 16:9 cover in the laptop.
VIDEOS = {
 'hiw': dict(o='v', file='movemint-how-it-works.mp4', cover='movemint-how-it-works', poster='movemint-how-it-works-poster.jpg', d='1:25', iso='PT1M26S',
   t='How MoveMint works: hold, share and move', bar='MoveMint · Official video', tag='Official', tagc='o',
   cap='The 3 ways MoveMint pays, from MoveMint itself', name='How MoveMint (MINT) works: the 3 ways it pays',
   desc='MoveMint\'s own 85 second explainer: holders get a share of trading fees as tokenized stocks, cash, gold, silver and copper; your buy link earns 30% of the app fee on friends\' buys; walking earns Mint Points.', up='2026-11-26'),
 'trailer': dict(o='h', file='movemint-trailer.mp4', hd='movemint-trailer-1080p.mp4', cover='movemint-trailer', d='0:49', iso='PT49S',
   t='MoveMint in 49 seconds: the official trailer', bar='MoveMint · Trailer', tag='Official', tagc='o',
   cap='Meet Bolt, Lord Rug and the treasury bill', name='MoveMint (MINT) official trailer: 49 seconds',
   desc='MoveMint\'s animated trailer: rewards sent to holders in stocks, gold, treasuries and cash, with Bolt the robot. Its targets are a goal, not a promise.', up='2026-11-27'),
 'part1': dict(o='v', file='movemint-part1.mp4', cover='movemint-part1', poster='movemint-part1-poster.jpg', d='5:12', iso='PT5M13S',
   t='MoveMint Part 1: join and make your wallet', bar='MoveMint · Part 1', tag='Step by step', tagc='',
   cap='Part 1: join with an invite and make your wallet', name='How to join MoveMint and make your MINT wallet (Part 1)',
   desc='MTG shows every tap: open an invite link, join MoveMint, make your self-custody wallet with a passkey and keep your 12 recovery words safe.', up='2026-11-28'),
 'part2': dict(o='v', file='movemint-part2.mp4', cover='movemint-part2', poster='movemint-part2-poster.jpg', d='5:39', iso='PT5M40S',
   t='MoveMint Part 2: fund your wallet and buy MINT', bar='MoveMint · Part 2', tag='Step by step', tagc='',
   cap='Part 2: SOL from Binance, swap to MINT, the app tour', name='How to buy MINT: fund your MoveMint wallet with SOL and swap (Part 2)',
   desc='MTG converts USDT to SOL on Binance, withdraws it on the Solana network to his MoveMint wallet, swaps SOL for MINT with the +20% invite bonus and tours the World, the robot icon and the Me page.', up='2026-11-28'),
}
MOMENTS = [  # founder call: where each topic starts (seconds), 8 seconds before each topic in the call's transcript, for a lead-in
 (397, 'What MoveMint is: stocks, cash, metals and bonds for holders'),
 (428, 'How drops reach your wallet, with nothing to claim'),
 (711, 'Sell your rewards or your MINT whenever you like'),
 (936, 'The more MINT you hold, the bigger your share'),
 (1201, 'The World game: walk, catch treasures, earn points'),
 (1785, 'Try the app free, even before you own MINT'),
 (2035, 'Your wallet: only you can open it'),
 (2835, 'Find the iPhone app, or use the web app'),
 (3253, 'Every drop is posted, and you can check your wallet'),
]
def mmss(s): h, r = divmod(s, 3600); m, s = divmod(r, 60); return (f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}')

def media(f, prev_ok=True):
    return MEDIA + f
def cover_img(slug, alt, eager=False):
    s640, s1280 = f'/mint/img/{slug}-cover-640.webp', f'/mint/img/{slug}-cover-1280.webp'
    return (f'<img src="{a(s640)}" srcset="{a(s640)} 640w, {a(s1280)} 1280w" sizes="(max-width:900px) 94vw, 560px" width="1280" height="720" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async" alt="{esc(alt)}">')
def bar(left, dur):
    return ('<div class="pl-bar"><span class="pl-l"><span class="pl-tx">' + esc(left) + '</span><button type="button" class="pl-b pl-max" data-pl-max aria-label="Full Screen">'
            '<svg class="ic i-max" aria-hidden="true" focusable="false"><use href="#i-max"/></svg><svg class="ic i-min" aria-hidden="true" focusable="false"><use href="#i-min"/></svg>'
            '<span class="t t-max">Full Screen</span><span class="t t-min">Exit Full Screen</span></button></span><i class="pl-cam" aria-hidden="true"></i>'
            '<span class="pl-r"><span class="pl-tx">' + esc(dur) + '</span><button type="button" class="pl-b pl-x" data-pl-x aria-label="Close the video"><span class="t">Close</span>'
            '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-x"/></svg></button></span></div>')
def laptop(fig_id, play_btn, cover, cap_b, cap_s, tag='', tagc=''):
    t = f'<span class="vtag {tagc}">{esc(tag)}</span>' if tag else ''
    return (f'<figure class="vid mtgp rv" id="{fig_id}"><div class="pl pl-h"><div class="pl-dev">{bar(cap_b, "")}<div class="pl-scr">{cover}{play_btn}</div></div>'
            f'<i class="pl-deck" aria-hidden="true"><i></i></i></div><figcaption class="vcap"><span class="vct"><b>{t}{esc(cap_b)}</b><small>{esc(cap_s)}</small></span></figcaption></figure>')
def vid(code):
    v = VIDEOS[code]
    alt = v['t'] + ': video cover'
    lab = f'Play: {v["t"]} ({v["d"]})'
    pb = '<span class="pbtn">' + '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-pf"/></svg></span>'
    if v['o'] == 'v':
        btn = f'<button type="button" class="vplay pulse" data-play="{code}" aria-label="{esc(lab)}">{pb}</button>'
    else:
        hd = (f' data-src-hd="{media(v["hd"])}?v={ver(MEDIA + v["hd"])}"' if v.get('hd') and not PREVIEW else '')
        btn = f'<button type="button" class="vplay pulse" data-code="{code}" data-src="{media(v["file"])}?v={ver(MEDIA + v["file"])}"{hd} aria-label="{esc(lab)}">{pb}</button>'
    fig = laptop('v-' + code, btn, cover_img(v['cover'], alt), v['t'], v['cap'] + ' · ' + v['d'], v['tag'], v['tagc'])
    return fig.replace(bar(v['t'], ''), bar(v['bar'], v['d']))
def founder_vid():
    lab = 'Play: MoveMint explained by the founder, the full call (1:15:00)'
    btn = (f'<button type="button" class="vplay pulse" data-code="founder" data-yt="{YT}" aria-label="{esc(lab)}"><span class="pbtn">'
           '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-pf"/></svg></span></button>')
    fig = laptop('founder-video', btn, cover_img('movemint-founder-presentation', 'MoveMint explained by the founder: video cover'),
                 'MoveMint explained by the founder', 'The full founder call on Zoom · 1:15:00', 'Full call', 'o')
    return fig.replace(bar('MoveMint explained by the founder', ''), bar('MoveMint · Founder call', '1:15:00'))

# ------------------------------------------------------------------ words
TITLE = 'MoveMint (MINT): What It Is and How to Buy It, Step by Step'
DESC = ('MoveMint (MINT) on Solana drops tokenized stocks, gold, silver and cash into holders\' wallets. Watch the videos, copy the real '
        'contract address and start in 4 steps with MTG.')
OG_T = 'MoveMint (MINT): hold it, get stocks in your wallet'
OG_D = 'The videos, the real contract address and 4 simple steps to start without mistakes. MTG\'s guide to MoveMint on Solana.'

FAQ = [
 ('What is MoveMint (MINT)?',
  ['MoveMint is a Solana project with a coin called MINT and an app. A share of the fees from MINT trades buys tokenized stocks, cash coins, gold, silver and copper, and drops them into the wallets of people who hold MINT. The app also has a walking game, MoveMint World, where you collect Mint Points.']),
 ('Do I get real shares?',
  ['You get tokenized stocks. A tokenized stock is a token that follows the price of a real company\'s shares, such as Apple or Nvidia. It is not the same as owning shares at a broker and it carries no voting rights, but it lives in your own wallet and you can hold it or sell it whenever you like. For many people in the tribe, it is their first time holding stocks at all.']),
 ('Do I need to claim my rewards?',
  ['No. Holder drops land in your wallet by themselves, and you can see each one. Only Mint Points from the walking game are turned into MINT in the app, once approved.']),
 ('How much will I receive?',
  ['It depends on how much MINT is traded and how much MINT you hold compared with everyone else. The more you hold, the bigger your share, and the amounts change from round to round. Nobody can promise a figure, so start with an amount you are comfortable with.']),
 ('How do I buy MINT?',
  ['Inside the MoveMint app, with SOL, after you join with an invite link. Joining with an invite gives you +20% more MINT on your buy, sent to your wallet once approved. The steps above, and MTG\'s Part 1 and Part 2 videos, show every tap.']),
 ('What does buying cost?',
  ['The app keeps a 10% fee on buys, and the Solana network charges a tiny fee in SOL. With an invite you also receive +20% more MINT once approved. Keep a little SOL in your wallet so you can always pay network fees.']),
 ('Is there an Android app?',
  ['The MoveMint World app is on the App Store for iPhone and iPad. On Android, use the web app at app.movemint.vip in your phone\'s browser: everything works there, and an Android app is on the way.']),
 ('Who controls my wallet?',
  ['You do. The MoveMint wallet is made on your device and locked with your Face ID or fingerprint. MoveMint cannot open it. Your 12 recovery words are the only way back in if you change phones, so write them on paper and never share them.']),
 ('Can I sell my MINT or my rewards?',
  ['Yes, whenever you like. There is no lock-up and no waiting period. MINT and the tokens you receive go up and down in price, like any crypto.']),
 ('What is the MINT contract address?',
  [f'{CA}. That is MoveMint (MINT) on Solana. Tokens with the same name can exist, so always check the address before you buy anywhere.']),
 ('Can I start small?',
  ['Yes. MTG tested MoveMint first with just $10 to see every step for himself. Start with an amount that lets you sleep well, and add more when you are comfortable.']),
 ('Is this the official MoveMint website?',
  ['No. This is MTG\'s independent guide. The official website is movemint.vip. MTG is a MoveMint member: when you buy with his invite link, he receives part of the app fee. It costs you nothing extra, and you get the +20% bonus. Invited by someone else? Use their link.']),
]

# The hero headline carries data-overlay for tools/qa/overlap.js: Anton's glyph boxes are taller than its tight line height,
# so the boxes of two coloured words on stacked lines touch while the letters themselves never do.
def page():
    vjs = {}
    for k, v in VIDEOS.items():
        if v['o'] != 'v': continue
        vjs[k] = {'t': v['t'], 'bar': v['bar'], 'd': v['d'], 'o': 'v', 's': f'{media(v["file"])}?v={ver(MEDIA + v["file"])}', 'p': a('/mint/img/' + v['poster'])}
    css = open(os.path.join(HERE, 'mint.css')).read()
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S); css = re.sub(r'\s*\n\s*', '', css)
    js = open(os.path.join(HERE, 'mint.js')).read()
    ld = jsonld()
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><div class="a">' + ''.join(f'<p>{esc(p)}</p>' for p in ps) + '</div></details>' for q, ps in FAQ).replace(CA + '.', f'<code class="ca-in">{CA}</code>.')
    li = lambda s, t: f'<li><a href="https://www.youtube.com/watch?v={YT}&amp;t={s}s" data-at="{s}" target="_blank" rel="noopener"><time datetime="PT{s // 60}M{s % 60}S">{mmss(s)}</time><span>{esc(t)}</span></a></li>'
    moments = '<ol>' + ''.join(li(s, t) for s, t in MOMENTS[:5]) + '</ol><details><summary>Show ' + str(len(MOMENTS) - 5) + ' more moments</summary><ol start="6">' + ''.join(li(s, t) for s, t in MOMENTS[5:]) + '</ol></details>'
    tape_items = [('AAPL', 'Apple'), ('NVDA', 'Nvidia'), ('TSLA', 'Tesla'), ('MSFT', 'Microsoft'), ('AMZN', 'Amazon'), ('GOOGL', 'Google'), ('KO', 'Coca-Cola'),
                  ('MCD', "McDonald's"), ('GME', 'GameStop'), ('GOLD', 'Gold'), ('SILVER', 'Silver'), ('COPPER', 'Copper'), ('USDC', 'Cash coin'), ('T-BILL', 'US Treasury')]
    tape = ''.join(f'<li><b>{esc(t)}</b>{esc(n)}</li>' for t, n in tape_items)
    tape_dup = ''.join(f'<li aria-hidden="true"><b>{esc(t)}</b>{esc(n)}</li>' for t, n in tape_items)
    R = f'href="{REF}" target="_blank" rel="sponsored noopener"'
    body = f'''<a class="skip" href="#main">Skip to the guide</a>
<div class="sky" aria-hidden="true"><i></i><i></i><i></i></div>
{SPRITE}
<header class="top"><div class="wrap">
 <a class="brand" href="#top" aria-label="MoveMint guide by MTG: back to the top"><span class="crown" aria-hidden="true">👑</span><span class="bt"><b>MTG</b><small>MINT guide</small></span></a>
 <nav class="nav" aria-label="Sections"><a href="#what">How it pays</a><a href="#videos">Videos</a><a href="#start">4 steps</a><a href="#faq">FAQ</a></nav>
 <a class="btn btn-gold cta-sm" {R}>Get MINT {ic('arrow', 'go')}</a>
 <button class="menu-b" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drop">{ic('menu', 'i-open')}<svg class="ic i-close" aria-hidden="true" focusable="false"><use href="#i-x"/></svg></button>
</div></header>
<nav class="drop" id="drop" aria-label="Sections"><a href="#top">{ic('home')}Top</a><a href="#what">{ic('coins')}How MoveMint pays</a><a href="#videos">{ic('play')}Videos</a><a href="#start">{ic('steps')}Start in 4 steps</a><a href="#faq">{ic('help')}Questions</a><a {R}>{ic('zap')}Get MINT with MTG's invite</a></nav>

<main id="main">
<section class="hero" id="top"><div class="wrap hero-in">
 <div>
  <p class="eye"><i aria-hidden="true"></i>MoveMint (MINT) on Solana</p>
  <h1 data-overlay><span class="sr">MoveMint (MINT) guide: </span>Hold <span class="k">MINT</span>. Get <span class="g">stocks</span> dropped in your wallet.</h1>
  <p class="lead">MoveMint shares its trading fees with <b>MINT holders</b> as tokenized stocks from <b>20+ companies</b>, plus gold, silver and cash, straight into your own wallet. <b>Nothing to claim.</b> Here is everything you need, in the right order, so you start in minutes without mistakes.</p>
  <div class="hero-cta">
   <a class="btn btn-gold" {R}><span class="two">Get MINT with MTG's invite<small>+20% bonus MINT on your buy</small></span>{ic('arrow', 'go')}</a>
   <button class="btn btn-ghost" type="button" data-play="hiw">{ic('play')}<span class="two">Watch how it works<small>1 minute 25 seconds</small></span></button>
  </div>
  <ul class="trust"><li>{ic('zap')}On Solana</li><li>{ic('wallet')}Your own wallet</li><li>{ic('badge')}Nothing to claim</li><li>{ic('phone')}iPhone app and web app</li></ul>
 </div>
 <div class="stage" data-tilt="8" aria-hidden="true"><div class="tilt">
  <div class="glow"></div><div class="ring"></div><div class="ring r2"></div><div class="floor"></div>
  <div class="orbit"><span class="coin o1">AAPL</span><span class="coin s o2">SILVER</span><span class="coin m o3">NVDA</span><span class="coin o4">GOLD</span><span class="coin c o5">COPPER</span><span class="coin m o6">TSLA</span></div>
  <img class="bolt" src="{a('/mint/img/bolt-720.webp')}" srcset="{a('/mint/img/bolt-420.webp')} 420w, {a('/mint/img/bolt-720.webp')} 720w" sizes="(max-width:940px) 60vw, 330px" width="720" height="764" alt="" fetchpriority="high" decoding="async">
  <div class="wcard">{ic('wallet')}Holder drops, straight to your wallet <span>📈🥇🥈💵</span></div>
 </div></div>
</div>
<div class="wrap"><div class="ca rv" id="ca">
 <p class="ca-h">MINT contract address (Solana) <span class="ok">{ic('shield')}Checked on chain: MoveMint (MINT)</span></p>
 <div class="ca-row"><code class="addr" id="ca-addr">{CA}</code>
  <div class="ca-btns"><button class="btn btn-gold cta-sm" type="button" data-copy="{CA}" data-copied="Contract address copied">{ic('copy')}<span class="lbl">Copy address</span></button>
   <a class="btn btn-ghost cta-sm" href="https://solscan.io/token/{CA}" target="_blank" rel="noopener">Solscan {ic('ext')}</a>
   <a class="btn btn-ghost cta-sm" href="https://dexscreener.com/solana/{CA}" target="_blank" rel="noopener">Live price {ic('ext')}</a></div></div>
 <p class="ca-note"><b>Only this address is the real MINT.</b> Coins with the same name can exist, so check the address before you buy anywhere. Total supply: about 1 billion MINT.</p>
</div></div></section>

<section class="sec" id="what"><div class="wrap">
 <p class="kick rv">{ic('coins')}How it pays</p>
 <h2 class="rv">Three ways MoveMint <span class="k">pays you</span></h2>
 <p class="sub rv">Hold, share and move. That is the whole idea, in MoveMint's own words.</p>
 <div class="cards">
  <article class="card rv" data-tilt="5"><span class="num" aria-hidden="true">1</span><div class="ico">{ic('wallet')}</div><h3>Hold MINT</h3>
   <p>Every trade of MINT pays a fee. A share of those fees buys tokenized stocks, cash, gold, silver and copper, dropped straight into holders' wallets. Nothing to claim. The more you hold, the bigger your share.</p></article>
  <article class="card rv" data-tilt="5"><span class="num" aria-hidden="true">2</span><div class="ico">{ic('link')}</div><h3>Share your buy link</h3>
   <p>When a friend buys MINT in the app with your link, the app keeps a 10% fee and 30% of that fee is yours, in SOL or MINT, on every buy they make. Your friend gets 20% more MINT as a bonus.</p>
   <span class="ex"><b>Example from MoveMint's video:</b> a friend buys with 10 SOL, the fee is 1 SOL, and 0.3 SOL is yours.</span></article>
  <article class="card rv" data-tilt="5"><span class="num" aria-hidden="true">3</span><div class="ico">{ic('feet')}</div><h3>Walk and play</h3>
   <p>Walk the MoveMint World, catch treasures and collect Mint Points. Points can turn into MINT when approved, and you get 10% of the points your friends earn.</p></article>
 </div>
 <div class="pic rv">
  <svg viewBox="0 0 130 130" role="img" aria-label="A pizza with one slice lifted out"><defs><radialGradient id="pz" cx="50%" cy="45%"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#e59a3a"/></radialGradient></defs>
   <circle cx="65" cy="65" r="58" fill="#b8692a"/><circle cx="65" cy="65" r="50" fill="url(#pz)"/>
   <g fill="#d6402f"><circle cx="45" cy="50" r="7"/><circle cx="80" cy="42" r="6"/><circle cx="52" cy="85" r="6"/><circle cx="88" cy="78" r="7"/></g>
   <g stroke="#9a5420" stroke-width="2"><line x1="65" y1="65" x2="65" y2="7"/><line x1="65" y1="65" x2="115" y2="94"/><line x1="65" y1="65" x2="15" y2="94"/></g>
   <g class="sl"><path d="M65 65 L65 7 A58 58 0 0 1 115 94 Z" fill="#b8692a"/><path d="M65 65 L65 15 A50 50 0 0 1 108 90 Z" fill="url(#pz)"/><circle cx="84" cy="52" r="6" fill="#d6402f"/><circle cx="96" cy="76" r="5" fill="#40e4a8"/></g></svg>
  <div><h3>Picture a pizza shop 🍕</h3>
   <p>Every MINT trade is like a pizza sold. A slice of every sale goes into a shared pot, and the pot buys treats (stocks, gold, silver, cash) that are shared out to everyone holding MINT: a bigger hold gets a bigger slice. How full the pot gets depends on how much MINT is traded, so the slices change from round to round.</p></div>
 </div>
 <h3 class="vhead rv">{ic('trend')}What can land in your wallet</h3>
 <div class="tape rv" aria-label="Examples of rewards"><ul>{tape}{tape_dup}</ul></div>
 <div class="kinds">
  <div class="kind rv"><span class="e" aria-hidden="true">📈</span>Stocks<small>20+ companies</small></div>
  <div class="kind rv"><span class="e" aria-hidden="true">🥇</span>Gold<small>tokenized</small></div>
  <div class="kind rv"><span class="e" aria-hidden="true">🥈</span>Silver<small>tokenized</small></div>
  <div class="kind rv"><span class="e" aria-hidden="true">🟠</span>Copper<small>miners fund</small></div>
  <div class="kind rv"><span class="e" aria-hidden="true">💵</span>Cash coins<small>digital dollars</small></div>
  <div class="kind rv"><span class="e" aria-hidden="true">🏦</span>US Treasuries<small>tokenized bonds</small></div>
 </div>
 <div class="calm rv">{ic('spark')}<p>Each round pays in one kind. A tokenized stock follows the price of the real company's shares; it is not the same as shares at a broker and carries no voting rights. You hold it in your own wallet and can sell it whenever you like.</p></div>
</div></section>

<section class="sec" id="videos"><div class="wrap">
 <p class="kick rv">{ic('play')}Videos</p>
 <h2 class="rv">Watch first, <span class="k">then start</span></h2>
 <p class="sub rv">Two short official videos, MTG's two step-by-step tutorials, and the full founder call. Every MoveMint video MTG makes lives right here.</p>
 <div class="vgrid two">{vid('hiw')}{vid('trailer')}</div>
 <h3 class="vhead rv" id="tutorials">{ic('steps')}Step by step with MTG</h3>
 <div class="vgrid two">{vid('part1')}{vid('part2')}</div>
 <h3 class="vhead rv">{ic('chat')}The full founder call</h3>
 <div class="founder">{founder_vid()}
  <div class="moments rv"><h3>{ic('play')}Jump to a topic</h3><p>Tap a moment and the call starts right there.</p>{moments}
   <p class="fine">A live Zoom call with the MoveMint founder. Plans and opinions in it are the speakers' own, not promises.</p></div>
 </div>
</div></section>

<section class="sec" id="start"><div class="wrap">
 <p class="kick rv">{ic('steps')}Start here</p>
 <h2 class="rv">Start in <span class="k">4 steps</span></h2>
 <p class="sub rv">About 15 minutes, one step at a time. Each step ends with a check, so you always know it worked.</p>
 <ol class="steps">
  <li class="step rv"><h3>Join with an invite and make your wallet</h3>
   <ol><li>Open MTG's invite link and sign up.</li><li>Tap <b>Make my wallet</b>. It is made on your phone and locked with your Face ID or fingerprint.</li><li>Write your 12 recovery words on paper and keep them offline.</li></ol>
   <p class="check">✅ <span><b>Success check:</b> you see "You're in" and your MoveMint wallet opens.</span></p>
   <div class="acts"><a class="btn btn-gold" {R}>Open MTG's invite {ic('arrow', 'go')}</a><button class="btn btn-ghost" type="button" data-play="part1">{ic('play')}Watch Part 1 (5:12)</button></div></li>
  <li class="step rv"><h3>Send SOL to your MoveMint wallet</h3>
   <ol><li>Buy SOL on an exchange such as Binance. MTG converts USDT to SOL there.</li><li>In MoveMint, copy your Solana wallet address.</li><li>On the exchange, withdraw SOL on the <b>Solana</b> network to that address. Check the first and last 4 characters.</li></ol>
   <p class="check">✅ <span><b>Success check:</b> your SOL shows in your MoveMint wallet.</span></p>
   <div class="acts"><button class="btn btn-ghost" type="button" data-play="part2">{ic('play')}Watch Part 2 (5:39)</button></div></li>
  <li class="step rv"><h3>Swap SOL for MINT, inside MoveMint</h3>
   <ol><li>Tap <b>Buy</b>, enter how much SOL to swap and confirm.</li><li>Keep a little SOL for network fees.</li><li>Your +20% invite bonus is sent to your wallet once approved.</li></ol>
   <p class="check">✅ <span><b>Success check:</b> you see "Swapped" and your MINT balance. The bonus follows after approval.</span></p></li>
  <li class="step rv"><h3>Hold, walk and share</h3>
   <ol><li>Hold your MINT: drops land in your wallet by themselves.</li><li>Take the World tour with Bolt. Tap the robot icon to replay it any time.</li><li>Walk to collect Mint Points, and share your own buy link from the Me page.</li></ol>
   <p class="check">✅ <span><b>Success check:</b> your first holder drop shows in your wallet.</span></p></li>
 </ol>
 <div class="tips rv"><h3>{ic('shield')}Good to know before you start</h3><ul>
  <li>{ic('check')}<span><b>Use the contract address above.</b> Coins with the same name can exist.</span></li>
  <li>{ic('check')}<span><b>Withdraw SOL on the Solana network</b>, and send a small amount first if it is your first time.</span></li>
  <li>{ic('check')}<span><b>Keep a little SOL</b> in your wallet for network fees.</span></li>
  <li>{ic('check')}<span><b>Your 12 words stay on paper.</b> Never in a screenshot, never shared. Nobody from MoveMint will ever ask for them.</span></li>
  <li>{ic('check')}<span><b>Buy inside MoveMint with an invite</b> to get the +20% bonus.</span></li>
  <li>{ic('check')}<span><b>Start small.</b> MTG tested every step first with just $10.</span></li>
 </ul></div>
</div></section>

<section class="sec" id="faq"><div class="wrap">
 <p class="kick rv">{ic('help')}Questions</p>
 <h2 class="rv">Short <span class="k">answers</span></h2>
 <div class="faq rv">{faq_html}</div>

 <div class="join rv" id="join">
  <img src="{a('/mint/img/bolt-420.webp')}" width="420" height="446" alt="" loading="lazy" decoding="async">
  <h2>Your first MINT is <span class="k">a few taps away</span></h2>
  <p class="sub">Join with MTG's invite, make your wallet, send SOL and swap. The videos above show every tap.</p>
  <div class="acts"><a class="btn btn-gold" {R}><span class="two">Get MINT with MTG's invite<small>+20% bonus MINT on your buy</small></span>{ic('arrow', 'go')}</a>
   <button class="btn btn-ghost" type="button" data-copy="{REF}" data-copied="MTG's invite link copied">{ic('copy')}<span class="lbl">Copy invite link</span></button>
   <a class="btn btn-ghost" href="{('https://mtgtribe.com' if PREVIEW else '')}/group/">{ic('chat')}Questions? Ask the tribe</a></div>
  <p class="disc"><b>Fair play:</b> MTG receives part of the app fee when you buy with his link. It costs you nothing extra, and you get the bonus. Invited by someone else? Use their link.</p>
  <p class="disc">MINT and the tokens it drops go up and down in price, and rewards depend on trading. Start with an amount you are comfortable with.</p>
 </div>
</div></section>
</main>

<footer class="foot"><div class="wrap">
 <ul class="socs" aria-label="Follow MTG">
  <li><a href="{('https://mtgtribe.com' if PREVIEW else '')}/group/">{ic('users')}WhatsApp group</a></li>
  <li><a href="https://t.me/mtgtribe" target="_blank" rel="noopener me">{ic('telegram')}Telegram</a></li>
  <li><a href="https://www.facebook.com/mtgtribe" target="_blank" rel="noopener me">{ic('facebook')}Facebook</a></li>
  <li><a href="https://www.tiktok.com/@joinmtgtribe" target="_blank" rel="noopener me">{ic('tiktok')}TikTok</a></li>
  <li><a href="https://www.youtube.com/@mtgtribe" target="_blank" rel="noopener me">{ic('youtube')}YouTube</a></li>
 </ul>
 <p class="slog">We learn best when we teach others.</p>
 <p class="sig">Let's Get This Crypto! 💪</p>
 <div class="fl"><strong>MTG 👑 | Your Digital Architect</strong><span>{STREAMS}</span>
  <span>Official MoveMint website, for reference: <a href="https://movemint.vip" target="_blank" rel="noopener">movemint.vip</a></span></div>
 <p class="fine">© 2026 MTG. An independent guide by a MoveMint member, not official MoveMint material. Education only, not financial advice. Always do your own research.</p>
</div></footer>

<nav class="qbar" aria-label="Quick links"><a href="#top">{ic('home')}Home</a><a href="#videos">{ic('play')}Videos</a><a {R} class="go">{ic('zap')}Get MINT</a><a href="#start">{ic('steps')}Steps</a><a href="#faq">{ic('help')}FAQ</a></nav>
<div class="ud" data-ud><button type="button" data-up aria-label="Back to the top">{ic('up')}</button><button type="button" data-down aria-label="Next section">{ic('down')}</button></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>

<div class="sheet player" id="player" role="dialog" aria-modal="true" aria-label="Video player" hidden><div class="sheet-in"><div class="pl pl-v" id="pl-pop"><div class="pl-dev">{bar('', '')}<div class="pl-scr"></div></div><i class="pl-deck" aria-hidden="true"><i></i></i></div></div></div>
<script>window.__mtgUD=1;window.MTGV={json.dumps(vjs, separators=(',', ':'))};{'window.MTG_PREVIEW=1;' if PREVIEW else ''}</script>
<script src="{a('/assets/tribe/mtg-player.js')}" defer></script>
<script>{js}</script>
<script src="{a('/assets/video-return.js')}" defer></script>'''
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(DESC)}">
<meta name="keywords" content="MoveMint, MINT token, MoveMint MINT, how to buy MINT, MoveMint contract address, MoveMint app, MoveMint World, tokenized stocks Solana, move to earn, MINT Solana">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="MTG">
<link rel="canonical" href="{URL}">
<meta name="theme-color" content="#031110">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="article"><meta property="og:site_name" content="MTG TRIBE"><meta property="og:locale" content="en_GB">
<meta property="og:title" content="{esc(OG_T)}">
<meta property="og:description" content="{esc(OG_D)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{SITE}{a('/mint/img/og-movemint.jpg')}"><meta property="og:image:secure_url" content="{SITE}{a('/mint/img/og-movemint.jpg')}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Hold MINT, get stocks in your wallet: MTG's MoveMint guide at mtgtribe.com/mint">
<meta property="article:published_time" content="{TODAY}T12:00:00+02:00"><meta property="article:modified_time" content="{TODAY}T12:00:00+02:00">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(OG_T)}">
<meta name="twitter:description" content="{esc(OG_D)}">
<meta name="twitter:image" content="{SITE}{a('/mint/img/og-movemint.jpg')}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500&display=swap">
<link rel="preload" as="image" href="{a('/mint/img/bolt-720.webp')}" imagesrcset="{a('/mint/img/bolt-420.webp')} 420w, {a('/mint/img/bolt-720.webp')} 720w" imagesizes="(max-width:940px) 60vw, 330px">
<link rel="stylesheet" href="{a('/assets/tribe/mtg-player.css')}">
<script>if(location.protocol==='http:'&&location.hostname==='mtgtribe.com')location.replace('https:'+location.href.slice(5));if('IntersectionObserver' in window&&!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))document.documentElement.classList.add('js');</script>
<style>{css}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
'''
    return head + body + '\n</body>\n</html>\n'

STREAMS = ('<a href="/">MTG TRIBE home</a><a href="https://bellveraffiliates.com/" target="_blank" rel="noopener">Bellver Cards</a><a href="/cbp/">ClickBaitPays</a>'
           '<a href="https://prenet.world/ref/mtg" target="_blank" rel="sponsored noopener">PRENET</a><a href="https://bitcoinwealthpays.com/" target="_blank" rel="noopener">Bitcoin Wealth</a>'
           '<a href="/jetup/">JetUp · TAG Markets</a><a href="https://www.aureus.africa/mtglegacy" target="_blank" rel="sponsored noopener">Aureus Alliance</a>')

def jsonld():
    mtg = {'@id': SITE + '/altruva/#mtg'}
    tribe = {'@id': SITE + '/#tribe'}
    img = {'@type': 'ImageObject', 'url': SITE + '/mint/img/og-movemint.jpg', 'width': 1200, 'height': 630}
    vids = []
    for k, v in VIDEOS.items():
        vids.append({'@type': 'VideoObject', '@id': URL + '#video-' + k, 'name': v['name'], 'description': v['desc'],
                     'thumbnailUrl': [SITE + f'/mint/img/{v["cover"]}-cover-1280.webp'], 'uploadDate': v['up'] + 'T12:00:00+02:00', 'duration': v['iso'],
                     'contentUrl': SITE + MEDIA + v['file'], 'embedUrl': URL + '#v-' + k, 'inLanguage': 'en',
                     'author': (mtg if k.startswith('part') else {'@type': 'Organization', 'name': 'MoveMint', 'url': 'https://movemint.vip'}), 'publisher': tribe})
    vids.append({'@type': 'VideoObject', '@id': URL + '#video-founder', 'name': 'MoveMint (MINT) explained: the full founder presentation',
                 'description': 'The MoveMint founder\'s live Zoom call: how holders receive tokenized stocks, cash, metals and bonds, the MoveMint World walking game, the self-custody wallet and questions from members.',
                 'thumbnailUrl': [SITE + '/mint/img/movemint-founder-presentation-cover-1280.webp'], 'uploadDate': TODAY + 'T12:00:00+02:00', 'duration': 'PT1H15M',
                 'embedUrl': f'https://www.youtube.com/embed/{YT}', 'url': f'https://www.youtube.com/watch?v={YT}', 'inLanguage': 'en',
                 'hasPart': [{'@type': 'Clip', 'name': t, 'startOffset': s, 'url': f'https://www.youtube.com/watch?v={YT}&t={s}s'} for s, t in MOMENTS]})
    howto = {'@type': 'HowTo', '@id': URL + '#howto', 'name': 'How to buy MoveMint (MINT)', 'description': 'Join MoveMint with an invite, make your wallet, send SOL and swap it for MINT inside the app.',
             'totalTime': 'PT15M', 'supply': [{'@type': 'HowToSupply', 'name': 'A phone with Face ID or a fingerprint reader'}, {'@type': 'HowToSupply', 'name': 'SOL, for example bought on Binance'}],
             'step': [
              {'@type': 'HowToStep', 'position': 1, 'name': 'Join with an invite and make your wallet', 'url': URL + '#start', 'text': 'Open an invite link, sign up, tap Make my wallet (locked with your Face ID or fingerprint) and write your 12 recovery words on paper.'},
              {'@type': 'HowToStep', 'position': 2, 'name': 'Send SOL to your MoveMint wallet', 'url': URL + '#start', 'text': 'Buy SOL on an exchange such as Binance, copy your MoveMint Solana address and withdraw SOL on the Solana network. Check the first and last 4 characters.'},
              {'@type': 'HowToStep', 'position': 3, 'name': 'Swap SOL for MINT inside MoveMint', 'url': URL + '#start', 'text': 'Tap Buy, enter how much SOL to swap and confirm. Keep a little SOL for fees. The +20% invite bonus is sent once approved.'},
              {'@type': 'HowToStep', 'position': 4, 'name': 'Hold, walk and share', 'url': URL + '#start', 'text': 'Hold MINT and holder drops land in your wallet. Take the World tour, walk to collect Mint Points and share your buy link.'}],
             'video': {'@id': URL + '#video-part1'}}
    faq = {'@type': 'FAQPage', '@id': URL + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(ps)}} for q, ps in FAQ]}
    g = [
     {'@type': 'WebPage', '@id': URL + '#webpage', 'url': URL, 'name': TITLE, 'description': DESC, 'inLanguage': 'en', 'isPartOf': {'@id': SITE + '/#website'},
      'breadcrumb': {'@id': URL + '#breadcrumb'}, 'primaryImageOfPage': img, 'datePublished': TODAY, 'dateModified': TODAY, 'author': mtg,
      'about': {'@type': 'Thing', 'name': 'MoveMint', 'alternateName': 'MINT', 'url': 'https://movemint.vip', 'description': 'MoveMint (MINT), a Solana token whose holders receive tokenized stocks, cash, gold, silver and copper from trading fees. Contract address ' + CA + '.'},
      'video': [{'@id': URL + '#video-' + k} for k in list(VIDEOS) + ['founder']]},
     {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'MTG TRIBE', 'publisher': tribe},
     {'@type': 'BreadcrumbList', '@id': URL + '#breadcrumb', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'MTG TRIBE', 'item': SITE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': 'MoveMint (MINT) guide', 'item': URL}]},
     howto, faq] + vids
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False).replace('</', '<\\/')

def sitemap_url():
    def x(s): return html.escape(s, quote=False)
    vs = ''
    for k, v in VIDEOS.items():
        sec = sum(int(p) * 60 ** i for i, p in enumerate(reversed(v['d'].split(':'))))
        vs += (f'<video:video><video:thumbnail_loc>{SITE}/mint/img/{v["cover"]}-cover-1280.webp</video:thumbnail_loc><video:title>{x(v["name"])}</video:title>'
               f'<video:description>{x(v["desc"])}</video:description><video:content_loc>{SITE}{MEDIA}{v["file"]}</video:content_loc><video:duration>{sec}</video:duration>'
               f'<video:publication_date>{v["up"]}T12:00:00+02:00</video:publication_date><video:family_friendly>yes</video:family_friendly></video:video>')
    vs += (f'<video:video><video:thumbnail_loc>{SITE}/mint/img/movemint-founder-presentation-cover-1280.webp</video:thumbnail_loc><video:title>MoveMint (MINT) explained: the full founder presentation</video:title>'
           f'<video:description>The MoveMint founder\'s live Zoom call: tokenized stocks, cash, metals and bonds for holders, the MoveMint World walking game and the self-custody wallet.</video:description>'
           f'<video:player_loc>https://www.youtube.com/embed/{YT}</video:player_loc><video:duration>4500</video:duration><video:publication_date>{TODAY}T12:00:00+02:00</video:publication_date><video:family_friendly>yes</video:family_friendly></video:video>')
    return (f'<url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><image:image><image:loc>{SITE}/mint/img/og-movemint.jpg</image:loc><image:title>MoveMint (MINT): hold it, get stocks in your wallet</image:title></image:image>'
            f'<image:image><image:loc>{SITE}/mint/img/bolt-720.webp</image:loc><image:title>Bolt, the MoveMint robot</image:title></image:image>{vs}</url>')

def update_sitemap():
    p = os.path.join(REPO, 'sitemap-home.xml'); s = open(p).read()
    s = re.sub(r'<url><loc>' + re.escape(URL) + r'</loc>.*?</url>\n', '', s, flags=re.S)
    anchor = '<url><loc>' + SITE + '/dashboard/</loc>'
    i = s.index(anchor); j = s.index('</url>\n', i) + len('</url>\n')
    s = s[:j] + sitemap_url() + '\n' + s[j:]
    open(p, 'w').write(s)
    q = os.path.join(REPO, 'sitemap.xml'); m = open(q).read()
    m = re.sub(r'(<loc>https://mtgtribe.com/sitemap-home.xml</loc><lastmod>)[^<]+', r'\g<1>' + TODAY, m)
    open(q, 'w').write(m)

if __name__ == '__main__':
    out = page()
    bad = [c for c in ('\u2014', '\u2013') if c in out]
    if bad: sys.exit('em or en dash found in the page: ' + repr(bad))
    if PREVIEW:
        dst = sys.argv[1]
        out = out.replace('href="/assets/favicon-32.png"', 'href="assets/favicon-32.png"').replace('href="/assets/apple-touch-icon.png"', 'href="assets/apple-touch-icon.png"')
        out = re.sub(r'(src|href|srcset|imagesrcset|data-src|data-src-hd)="/(mint|assets)/', r'\1="\2/', out)
        out = re.sub(r'(, )/(mint|assets)/', r'\1\2/', out)
        out = out.replace('"s":"/mint/', '"s":"mint/').replace('"p":"/mint/', '"p":"mint/')
        out = re.sub(r'href="/(?!/)', 'href="https://mtgtribe.com/', out)
        out = out.replace('<title>' + esc(TITLE) + '</title>', '<title>MoveMint MINT Guide</title>\n<link rel="artifact-thumbnail" href="mint/img/og-movemint.jpg">')
        open(os.path.join(dst, 'index.html'), 'w').write(out)
        print('preview written to', dst)
    else:
        open(os.path.join(REPO, 'mint', 'index.html'), 'w').write(out)
        update_sitemap()
        print('mint/index.html', len(out) // 1024, 'KB; sitemap-home.xml updated')
