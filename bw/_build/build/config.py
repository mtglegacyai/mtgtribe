"""Bitcoin Wealth guide by MTG (mtgtribe.com/bw): site configuration (links, facts, videos, menu)."""
import os

# The same guide is published twice (MTG, 22 Nov 2026: "replicate it onto bitcoinwealthpays.com ... when we update the BW website,
# make sure that you always also automatically update the Bitcoin Wealth Pays website as well"): mtgtribe.com/bw, the master, and the
# root of bitcoinwealthpays.com (repo MusaTheGiant/bitcoinwealthpays). build.py builds both; BW_TARGET=bwp selects the second.
TARGET = os.environ.get('BW_TARGET', 'mtgtribe')
HUB = 'https://mtgtribe.com'  # MTG's main site (the WhatsApp group, his other guides): the same from both copies
if TARGET == 'bwp':
    SITE, BASE = 'https://bitcoinwealthpays.com', '/'
else:
    SITE, BASE = 'https://mtgtribe.com', '/bw/'   # BASE: prod path prefix
HOST = SITE.split('//', 1)[1]
SITE_LABEL = HOST + BASE.rstrip('/')               # mtgtribe.com/bw or bitcoinwealthpays.com
BWP_REPO = '/home/user/bitcoinwealthpays'          # the bitcoinwealthpays.com repo, when it is cloned here
NAME = 'Bitcoin Wealth Guide by MTG'
TODAY = '2026-11-22'
LAUNCHED = '2026-11-14'       # first draft; update to the real go-live date when MTG approves

# where the build reads its inputs and writes its output (outside the public repo)
SCR = os.environ.get('BW_SCR') or '/tmp/claude-0/-home-user/612e96d5-9b21-5852-ab8a-e6cd65a7a534/scratchpad/bwsite'  # BW_SCR: another session's scratch
STUDIO = '/home/user/mtg-studio'
REPO = '/home/user/mtgtribe'
# The videos are served from Cloudflare R2, not from GitHub Pages (MTG, 22 Nov 2026: "Perfect! Put it live!", on moving the /bw
# videos to R2 before Explainer 3): the published site had reached GitHub Pages' 1 GB limit. The same day MTG gave Bitcoin Wealth a
# Cloudflare account of its own ("separate from Bellver"), with bitcoinwealthpays.com on it: bucket bitcoinwealth-media, folder
# videos/, served at media.bitcoinwealthpays.com. r2.py uploads new or changed files (the API token is on MTG's Default cloud
# environment and reaches both of his Cloudflare accounts). A video's address on the page keeps its ?v= content version.
MEDIA_URL = 'https://media.bitcoinwealthpays.com/videos/'
R2_BUCKET = 'bitcoinwealth-media'
R2_PREFIX = 'videos/'
KEEP_LOCAL_MEDIA = False      # the old copies on GitHub Pages were removed once the pages pointing at R2 were live (22 Nov 2026)

# MTG's links (confirmed current by MTG, 14 Nov 2026)
REF = 'https://vowu.io/register?ref=14638'
VALR = 'https://www.valr.com/invite/VAKM6VZY'
BINANCE = 'https://accounts.binance.com/register?ref=11139868'
WA_MTG = 'https://wa.me/27721714626'
WA_NUM = '072 171 4626'
WA_MTG_MSG = f'Hi MTG, I found your Bitcoin Wealth guide on {SITE_LABEL} and I have a question.'
GROUP = 'https://mtgtribe.com/group/'      # MTG TRIBE WhatsApp group (Zoom links are shared there)
TIKTOK = 'https://www.tiktok.com/@joinmtgtribe'
YOUTUBE = 'https://www.youtube.com/@mtgtribe'
FACEBOOK = 'https://www.facebook.com/mtgtribe'
TELEGRAM = 'https://t.me/mtgtribe'
MTG_SITE = 'https://www.musathegiant.com'
CRYPTO101 = 'https://www.musathegiant.com/101'
CARD_GUIDE = 'https://bellveraffiliates.com/'
ORDER = '/bwcopy/'                          # order form for your own Bitcoin Wealth marketing website (prod path)
JETUP_GUIDE = 'https://mtgtribe.com/jetup/'   # MTG's JetUP and TAG Markets guide (lower case: the address is case-sensitive)
CBP_SITE = 'https://clickbaitpaysus.com'
AUREUS = 'https://www.aureus.africa/mtglegacy'   # Aureus Alliance: a gold mining company that sells gold mining shares (MTG, 24 Nov 2026); MTG's link
# menu items that lead to MTG's other sites (MTG, 22 Nov 2026: "After Crypto Card, add: JetUp ... then ClickBaitPays")
MENU_EXT = {'card': CARD_GUIDE, 'jetup': JETUP_GUIDE, 'aureus': AUREUS, 'cbp': CBP_SITE}

# on-chain facts (read from BNB Smart Chain on 14 Nov 2026; see mtg-studio ONCHAIN-CHECK-2026-11-14.md)
CONTRACT = '0x1ad09b043E0Fe59243C9a18ee1c855bd7792Cd29'
BTCB = '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c'
BSCSCAN = 'https://bscscan.com/address/' + CONTRACT
BSCSCAN_BTCB = 'https://bscscan.com/token/' + BTCB + '?a=' + CONTRACT
MEMBERS = '41,013'
CHECKED = '14 November 2026'
ON_CHAIN_SINCE = 'April 2026'
CREATED = '15 April 2026'
PRICE_ZAR = 1000          # your own Bitcoin Wealth marketing website, once-off (MTG: "R1000 is the fixed one"); or $50 in USDT (MTG, 23 Nov 2026)

SHARE_MSG = ("I've been learning how Bitcoin Wealth works with this free guide by MTG. Short videos and plain pages "
             "show how it works, how to join safely and how to check every payment yourself: " + SITE + BASE.rstrip("/"))

# released videos: code, slug, title, one-line summary, seconds, source master (in mtg-studio), extras
# extras: o='h' for a 16:9 video (it plays in the laptop frame, in place; a 9:16 video plays in the phone frame, in the pop-up),
# poster (in mtg-studio), label, short, date, name
# EVERY video shows on the page as a wide (16:9) cover inside the laptop frame (MTG, 17 Nov 2026: "all the videos must have a
# horizontal thumbnail and inside a laptop frame ... to save space and to make the website look smaller and easy to browse up and
# down"). So a 9:16 video needs two covers:
#   poster: its 9:16 cover (the pop-up's phone shows it while the video loads): no address pill, a clear band in the middle
#   wide:   its 16:9 cover for the page (core.vid): the middle clear for the play button, every line short and compelling
# spot: another place for the play button, in percent, only when a cover's picture needs it
# name: the video's search name (structured data, video sitemap, watch page): written the way people search ("How to ...")
_CARTOON = 'projects/bitcoin-wealth/videos/cartoon-01-the-missing-piece/final/'
_T = 'projects/bitcoin-wealth/tutorials/'
_INTRO = 'projects/bitcoin-wealth/videos/intro-remake-leo/'
_E1 = 'projects/bitcoin-wealth/videos/explainer-01-what-is-bitcoin-wealth/'
_E2 = 'projects/bitcoin-wealth/videos/explainer-02-how-the-14-positions-pay/'
_E3 = 'projects/bitcoin-wealth/videos/explainer-03-the-12-slots-and-the-once-off/'
_E4 = 'projects/bitcoin-wealth/videos/explainer-04-better-than-a-stokvel/'
_E5 = 'projects/bitcoin-wealth/videos/explainer-05-check-it-yourself-on-bscscan/'
_E6 = 'projects/bitcoin-wealth/videos/explainer-06-your-own-bitcoin-wealth-website/'
VIDEOS = [
    ('s1', 'bitcoin-wealth-the-missing-piece-cartoon', 'The Missing Piece',
     'A short cartoon. Thandi did everything right and still ends up starting over. Leo shows her the one piece she is missing: people who build together.',
     86.8, _CARTOON + 'BW-cartoon-01-the-missing-piece-16x9.mp4',
     dict(o='h', poster=_CARTOON + 'BW-cartoon-01-website-poster-16x9.jpg', label='Cartoon', short='The Missing Piece', date='2026-11-15',
          spot=(50.0, 75.7),        # where the play button sits on the poster, in percent: the gap between the two friends
          name='The Missing Piece: a Bitcoin Wealth cartoon about building together')),
    ('t1', 'bitcoin-wealth-tutorial-1-safepal-wallet-setup', 'Set up your SafePal wallet for Bitcoin Wealth',
     'Download SafePal from the official site, create a wallet, back it up two ways, and keep only BNB, USDT and BTCB.',
     445.3, _T + '01-safepal/final/BW-Tutorial-1-SafePal-MTG.mp4',      # 17 Nov 2026: Leo speaks on the four section cards (7:25, was 7:10)
     dict(poster=_T + '01-safepal/final/BW-Tutorial-1-SafePal-website-poster-9x16.jpg',
          wide=_T + '01-safepal/final/BW-Tutorial-1-SafePal-website-poster-16x9.jpg',
          name='How to set up a SafePal wallet for Bitcoin Wealth (Tutorial 1)')),
    ('t2', 'bitcoin-wealth-tutorial-2-buy-bnb-send-to-safepal', 'Buy BNB on VALR and send it to SafePal',
     'Send rand from your bank to VALR with your own reference, buy BNB with it, and send the BNB to your SafePal wallet on BNB Smart Chain.',
     357.2, _T + '02-bank-to-valr/final/BW-Tutorial-2-Bank-to-SafePal-MTG.mp4',
     dict(poster=_T + '02-bank-to-valr/final/BW-Tutorial-2-Bank-to-SafePal-website-poster-9x16.jpg', date='2026-11-16',
          wide=_T + '02-bank-to-valr/final/BW-Tutorial-2-Bank-to-SafePal-website-poster-16x9.jpg',
          name='How to buy BNB on VALR and send it to SafePal (Bitcoin Wealth Tutorial 2)')),
    # Tutorial 3 (approved by MTG, 17 Nov 2026: "Very perfect ... I am approving this video. Please put it live")
    ('t3', 'bitcoin-wealth-tutorial-3-swap-bnb-to-btcb-activate-slot-1', 'Swap BNB for BTCB, sign up and activate slot 1',
     'Swap BNB for BTCB in SafePal, sign up with the link of the person who invited you, activate slot 1 with two confirmations, and get back into your dashboard any time.',
     370.2, _T + '03-swap-signup-activate/final/BW-Tutorial-3-Activate-Slot-1-MTG.mp4',      # 17 Nov 2026: Leo explains the Web3 wallet (6:10, was 6:02)
     dict(poster=_T + '03-swap-signup-activate/final/BW-Tutorial-3-Activate-Slot-1-website-poster-9x16.jpg', date='2026-11-17',
          wide=_T + '03-swap-signup-activate/final/BW-Tutorial-3-Activate-Slot-1-website-poster-16x9.jpg',
          name='How to join Bitcoin Wealth: swap BNB for BTCB and activate slot 1 (Tutorial 3)')),
    # a 34-second Bitcoin Wealth promo (MTG, 16 Nov 2026): four presenters, one short promo line each. The site calls it a
    # promo video and never presents it as member testimonials
    ('p1', 'bitcoin-wealth-in-34-seconds-promo', 'Bitcoin Wealth in 34 seconds',
     'A short Bitcoin Wealth promo video: four short clips about starting small, from 0.001 BTC, with a smart contract doing the paying.',
     34.3, 'projects/bitcoin-wealth/videos/promo-01-34-seconds/final/BW-promo-01-34-seconds.mp4',
     dict(poster='projects/bitcoin-wealth/videos/promo-01-34-seconds/final/BW-promo-01-website-poster-9x16.jpg', label='Promo', short='Promo video', date='2026-11-16',
          wide='projects/bitcoin-wealth/videos/promo-01-34-seconds/final/BW-promo-01-website-poster-16x9.jpg',
          name='Bitcoin Wealth in 34 seconds (promo video)')),
    # the Bitcoin Wealth presentation, remade with Leo (MTG, 20 Nov 2026: "This is the final version of the video and the thumbnails
    # ... put it live on my website"). It is the programme's own presentation, word for word, so the site shows it as that and
    # never prints its script (the site's own wording is the one checked on chain). 16:9: it plays in the laptop, in place
    ('i1', 'how-bitcoin-wealth-works-presentation', 'How Bitcoin Wealth works',
     'The Bitcoin Wealth presentation in 5 minutes, presented by Leo: what it is, the Vow Unity smart contract, where the 14 positions of a cycle pay, the 12 slots, and where to get more information.',
     319.6, _INTRO + 'final/Bitcoin-Wealth-intro-with-Leo-1080p.mp4',
     dict(o='h', poster=_INTRO + 'thumbs/out/Bitcoin-Wealth-intro-website-cover-16x9.jpg', label='Presentation', short='How it works', date='2026-11-20',
          name='How Bitcoin Wealth works: the presentation in 5 minutes, with Leo')),
    # Explainer 1, the first of the Thandi and Leo series (MTG, 21 Nov 2026: "Push the explainer video live"). Our own script, every
    # fact from the site's facts register, so the site prints the whole conversation on its page. 16:9: it plays in the laptop, in place
    ('e1', 'what-is-bitcoin-wealth-explained-in-3-minutes', 'What is Bitcoin Wealth?',
     "Thandi asks, Leo answers: Bitcoin Wealth is not a coin but a smart contract. Bitcoin, BTCB and BNB in plain words, where the money comes from, what it costs to start, and how to check every payment yourself.",
     179.8, _E1 + 'final/What-is-Bitcoin-Wealth-explainer-1-1080p.mp4',
     dict(o='h', poster=_E1 + 'thumbs/out/What-is-Bitcoin-Wealth-website-cover-16x9.jpg', short='What is Bitcoin Wealth?', date='2026-11-21',
          name="What is Bitcoin Wealth? It's not a coin. Explained in 3 minutes, with Thandi and Leo")),
    # Explainer 2 (MTG, 21 Nov 2026: "Too nice, I found the complete video. Put it live"). Our own script, every fact from the site's
    # facts register (the 14 positions table on dashboard/how-it-works/). 16:9: it plays in the laptop, in place
    ('e2', 'how-bitcoin-wealth-pays-14-positions-explained', 'How the 14 positions pay',
     "Thandi asks, Leo draws it out seat by seat: 2, then 4, then 8 positions under you, where each of the 14 payments goes, the Royal Pool from your second cycle, who fills the seats, and why there is no withdraw button.",
     199.0, _E2 + 'final/How-Bitcoin-Wealth-pays-14-positions-explainer-2-1080p.mp4',
     dict(o='h', poster=_E2 + 'thumbs/out/How-Bitcoin-Wealth-pays-14-positions-website-cover-16x9.jpg', short='The 14 positions', date='2026-11-21',
          name='How Bitcoin Wealth pays: the 14 positions explained in 3 minutes, with Thandi and Leo')),
    # Explainer 3 (MTG, 22 Nov 2026: "Perfect! Put it live!"). Our own script, every fact from the site's facts register (the 12 Slots
    # page: 12 slots doubling from 0.001 to 2.048 BTC, slot 1 paid once, slots 2 to 12 auto entry). From this episode on the close
    # has the hug. 16:9: it plays in the laptop, in place
    ('e3', 'bitcoin-wealth-12-slots-why-you-only-pay-once', 'The 12 slots and the once-off',
     "Thandi asks who pays for slots 2 to 12, and Leo shows it with two coins: 12 slots, each double the one before, slot 1 the only one you pay for, and why seat 5 of your first cycle moves you up.",
     197.4, _E3 + 'final/Bitcoin-Wealth-12-slots-explainer-3-1080p.mp4',
     dict(o='h', poster=_E3 + 'thumbs/out/Bitcoin-Wealth-12-slots-website-cover-16x9.jpg', short='The 12 slots', date='2026-11-22',
          name='The 12 Bitcoin Wealth slots: why you only pay once, explained in 3 minutes, with Thandi and Leo')),
    # Explainer 4 (MTG, 23 Nov 2026: "Put it live"). Our own script; the six questions are the stokvel page's own scorecard, word for
    # word, and the honest difference (a closed circle against one that fills only when real members join). 16:9: it plays in the laptop
    ('e4', 'bitcoin-wealth-vs-stokvel-6-questions-side-by-side', 'Better than a stokvel?',
     "Thandi asks if Bitcoin Wealth is just a stokvel on the internet, and Leo answers six honest questions side by side: who holds the money, who can see the payments, the fees, what it pays in, how much you put in, and whether your turn is guaranteed.",
     236.3, _E4 + 'final/Bitcoin-Wealth-vs-stokvel-explainer-4-1080p.mp4',
     dict(o='h', poster=_E4 + 'thumbs/out/Bitcoin-Wealth-vs-stokvel-website-cover-16x9.jpg', short='Better than a stokvel?', date='2026-11-23',
          name='Bitcoin Wealth vs a stokvel: 6 questions, side by side, explained in 4 minutes, with Thandi and Leo')),
    # Explainer 5 (MTG, 24 Nov 2026: "Perfect ... Put this video live on my website, across all the pages and sections where it will
    # make sense"). The four steps of the Check It Yourself page on a phone, a real activation of 24 Nov 2026 (member wallets masked),
    # step 4 your own wallet, then your own website (bitcoinwealthpays.com/zizi). Positive only: no owner talk in the video (MTG).
    ('e5', 'how-to-check-bitcoin-wealth-on-bscscan-4-steps', 'Check it yourself on BscScan',
     "Thandi asks how to read the open book, and Leo shows her on her phone, in four steps on BscScan: the contract, one real payment going in and straight out, the Token Holdings, and your own wallet. Then: your own Bitcoin Wealth website.",
     262.9, _E5 + 'final/Check-Bitcoin-Wealth-on-BscScan-explainer-5-1080p.mp4',
     dict(o='h', poster=_E5 + 'thumbs/out/Check-Bitcoin-Wealth-on-BscScan-website-cover-16x9.jpg', short='Check it yourself', date='2026-11-24',
          name='How to check Bitcoin Wealth on BscScan: 4 steps on your phone, explained in 4 minutes, with Thandi and Leo')),
    # Explainer 6 (MTG, 24 Nov 2026: "Let's cook the next video", after his plan of 23 Nov 2026): your own Bitcoin Wealth marketing
    # website, the price two ways (R1,000 or $50 in USDT), what traffic is, three ways to get it (ClickBaitPays the third), and the order
    # form field by field. Sells MTG's own service, so it plays on his two sites only, never on client websites (MTG, 23 Nov 2026).
    ('e6', 'your-own-bitcoin-wealth-marketing-website', 'Your own Bitcoin Wealth marketing website',
     "Thandi asks if she can have her own copy of this guide, and Leo shows her: your own Bitcoin Wealth marketing website with your link on every Join button, the price in rand or USDT, what traffic really means, three ways to get it, and how to order yours.",
     369.1, _E6 + 'final/Your-Own-Bitcoin-Wealth-Marketing-Website-explainer-6-1080p.mp4',
     dict(o='h', poster=_E6 + 'thumbs/out/Your-Own-Bitcoin-Wealth-Marketing-Website-website-cover-16x9.jpg', short='Your own website', date='2026-11-24',
          name='Your own Bitcoin Wealth marketing website: your link on every Join button, explained in 6 minutes, with Thandi and Leo')),
]
# Explainer 6 is held back from the live sites while it is made stronger (MTG, 24 Nov 2026: "Put the other edits live on the websites,
# except for the video, I still want us to make the video more powerful ... irresistible to buy the bwcopy"). The plain build (the live
# sites) leaves it out; BW_WITH_E6=1 builds it in, for the private preview.
HELD = set() if os.environ.get('BW_WITH_E6') == '1' else {'e6'}
VIDEOS = [_v for _v in VIDEOS if _v[0] not in HELD]
# planned videos (shown as "coming soon", never as playable)
PLANNED = [
    ('e7', 'Explainer', 'More on traffic, and more on crypto', 'Leo shows Thandi more about traffic, and more about crypto, together.'),
] if 'e6' not in HELD else [
    ('e6', 'Explainer', 'Your own Bitcoin Wealth marketing website', 'Thandi asks if she can have her own copy of this guide, with her own link on every Join button, and Leo shows her everything.'),
]
KIND = {'t': 'Tutorial', 'e': 'Explainer', 'k': 'Tool training', 's': 'Cartoon', 'p': 'Promo', 'i': 'Presentation'}
V = {}
for _v in VIDEOS:
    _x = _v[6] if len(_v) > 6 else {}
    V[_v[0]] = dict(code=_v[0], slug=_v[1], title=_v[2], desc=_v[3], secs=_v[4], master=_v[5], n=int(_v[0][1:]), kind=KIND[_v[0][0]],
                    label=_x.get('label', KIND[_v[0][0]] + ' ' + _v[0][1:]), o=_x.get('o', 'v'), poster=_x.get('poster'),
                    date=_x.get('date', LAUNCHED), spot=_x.get('spot'), wide=_x.get('wide'))
    V[_v[0]]['short'] = _x.get('short', _v[2])
    V[_v[0]]['name'] = _x.get('name') or f"Bitcoin Wealth {V[_v[0]]['label']}: {_v[2]}"
    assert V[_v[0]]['o'] == 'h' or V[_v[0]]['wide'], _v[0] + ': a 9:16 video needs a wide cover for the page'
SHORT = {'t1': 'Set up SafePal', 't2': 'Buy BNB, send to SafePal', 't3': 'Swap, sign up, activate slot 1'}
for _k, _s in SHORT.items():
    V[_k]['short'] = _s
NV = len(VIDEOS)
TUT = [k for k in V if k[0] == 't']
EXP = [k for k in V if k[0] == 'e']
TOOL = [k for k in V if k[0] == 'k']
TOTAL_MIN = round(sum(v[4] for v in VIDEOS) / 60)


def mmss(s):
    s = int(round(s))
    return f'{s // 60}:{s % 60:02d}'


def iso_dur(s):
    s = int(round(s))
    return f'PT{s // 60}M{s % 60}S'


# side menu: key, path (relative to /bw/), label, subtitle, icon, group
NAV = [
    # Get Started first (MTG, 14 Nov 2026: "Most people will never take time to go through everything before they get started,
    # all they want to do is join"). Menu names in Title Case (MTG, same day).
    ('home', 'dashboard/', 'Welcome', 'Start here: join in 3 stages', 'compass', 'Get Started'),
    ('join', 'dashboard/join/', 'Join Step-By-Step', 'Wallet, BNB, BTCB, slot 1', 'rocket', 'Get Started'),
    ('tut', 'dashboard/tutorials/', 'Tutorial Videos', 'Follow along, one tap at a time', 'circle-play', 'Get Started'),
    ('exp', 'dashboard/explainers/', 'Explainer Videos', 'How it works, in pictures', 'film', 'Get Started'),
    ('zoom', 'dashboard/live-on-zoom/', 'Live On Zoom', '5 evenings, 4 languages', 'video', 'Get Started'),
    ('fit', 'dashboard/is-it-right-for-me/', 'Is It Right For Me?', 'An honest fit check', 'scale', 'Before You Join'),
    ('back', 'dashboard/welcome-back/', 'Welcome Back', 'Left, stuck, or never looked?', 'heart-handshake', 'Before You Join'),
    ('what', 'dashboard/what-is-bitcoin-wealth/', 'What Is Bitcoin Wealth?', 'Bitcoin, BTCB, smart contract', 'bitcoin', 'How It Works'),
    ('hiw', 'dashboard/how-it-works/', 'The 14 Positions', '2, 4, 8 and where each pays', 'network', 'How It Works'),
    ('slots', 'dashboard/12-slots/', 'The 12 Slots', '0.001 BTC, once-off', 'layers', 'How It Works'),
    ('pool', 'dashboard/recycling-royal-pool/', 'Recycling And Royal Pool', 'After your first cycle', 'refresh-cw', 'How It Works'),
    ('stokvel', 'dashboard/stokvel/', 'Better Than A Stokvel?', 'Where it wins, how it is funded', 'users', 'How It Works'),
    ('diff', 'dashboard/what-makes-it-different/', 'What Makes It Different', 'The original, 5 checks', 'sparkles', 'How It Works'),
    ('proof', 'dashboard/check-it-yourself/', 'Check It Yourself', 'Every payment is public', 'scan-search', 'How It Works'),
    ('page', 'dashboard/bw-tribe-page/', 'Your Own Marketing Website', 'R1,000 or $50 in USDT, once-off', 'globe', 'Your Own Website'),
    ('c-btc', 'dashboard/tools/bitcoin-to-rand/', 'Bitcoin To Rand Converter', 'Live price: BTC, USD, ZAR', 'bitcoin', 'Tools'),
    ('c-slot', 'dashboard/tools/slot-calculator/', 'Slot Calculator', 'Each slot in BTC and rand', 'calculator', 'Tools'),
    ('c-halv', 'dashboard/tools/halving-countdown/', 'Halving Countdown', 'Live block height', 'hourglass', 'Tools'),
    ('faq', 'dashboard/faq/', 'FAQ', 'Straight answers', 'circle-help', 'Help'),
    ('gloss', 'dashboard/glossary/', 'Glossary', 'Crypto words, plain English', 'book-open-text', 'Help'),
    ('safe', 'dashboard/safety/', 'Safety Centre', 'Protect your wallet', 'shield-check', 'Help'),
    # More From MTG 👑, in MTG's order (24 Nov 2026): ClickBaitPays, Bellver Card, JetUP, Aureus Alliance, Join The MTG TRIBE
    ('cbp', CBP_SITE, 'ClickBaitPays', 'Got a link? Get it seen', 'mouse-pointer-click', 'More From MTG 👑'),
    ('card', 'dashboard/crypto-card/', 'Bellver Card', 'Spend your crypto', 'credit-card', 'More From MTG 👑'),
    ('jetup', JETUP_GUIDE, 'JetUP', 'Sonic AI copy trading', 'plane-takeoff', 'More From MTG 👑'),
    ('aureus', AUREUS, 'Aureus Alliance', 'Gold mining shares', 'pickaxe', 'More From MTG 👑'),
    ('tribe', 'dashboard/tribe/', 'Join The MTG TRIBE', 'WhatsApp community', 'message-circle', 'More From MTG 👑'),
]
EXTRA = [('disc', 'dashboard/disclaimer/', 'Disclaimer', 'Independent, educational', 'info', 'More From MTG 👑')]
# A page of its own for each tutorial video: the video, and every step in writing with its time (MTG, 17 Nov 2026: "all the videos
# must be named such that when people ... search for anything related to Bitcoin Wealth ... these videos can actually rank all by
# themselves"). A search engine lists a video on its own only from a page where that video is the main thing. Not in the side
# menu: they hang under Tutorial Videos. code: (path, page heading, chapters file in mtg-studio, written by tutorials/chapters.py)
WATCH_PAGES = {
    't1': ('dashboard/tutorials/safepal-wallet-setup/', 'How to set up your SafePal wallet for Bitcoin Wealth', _T + '01-safepal/final/chapters.json'),
    't2': ('dashboard/tutorials/buy-bnb-send-to-safepal/', 'How to buy BNB on VALR and send it to SafePal', _T + '02-bank-to-valr/final/chapters.json'),
    't3': ('dashboard/tutorials/swap-bnb-to-btcb-activate-slot-1/', 'How to swap BNB for BTCB and activate slot 1', _T + '03-swap-signup-activate/final/chapters.json'),
}
WATCH = {k: v[0] for k, v in WATCH_PAGES.items()}
EXTRA += [('w-' + k, v[0], f'{V[k]["label"]}: {V[k]["short"]}', 'Every step, in writing', 'circle-play', 'Get Started') for k, v in WATCH_PAGES.items()]
# The presentation's own page (MTG, 20 Nov 2026), under Explainer Videos: the video, its chapters with time buttons, and where
# each chapter is explained on the site. code: (path, page heading, chapters file in mtg-studio, written by the video's
# tools/chapters.py from its own cue times). CH: a chapter's start in seconds, for the "watch this part" cards on other pages
PRESENT = {
    'i1': ('dashboard/explainers/bitcoin-wealth-presentation/', 'How Bitcoin Wealth works: the presentation, in 5 minutes', _INTRO + 'final/chapters.json'),
}
WATCH.update({k: v[0] for k, v in PRESENT.items()})
# The explainers' own pages (MTG, 21 Nov 2026), under Explainer Videos: the video, its chapters with time buttons, and the whole
# conversation in writing (from the episode's own build: mtg-studio, the episode's tools/chapters.py). code: (path, heading, file)
EXPLAIN = {
    'e1': ('dashboard/explainers/what-is-bitcoin-wealth-video/', "What is Bitcoin Wealth? It's not a coin, explained in 3 minutes", _E1 + 'final/chapters.json'),
    'e2': ('dashboard/explainers/how-the-14-positions-pay-video/', 'How Bitcoin Wealth pays: the 14 positions, explained in 3 minutes', _E2 + 'final/chapters.json'),
    'e3': ('dashboard/explainers/the-12-slots-video/', 'The 12 Bitcoin Wealth slots: why you only pay once, explained in 3 minutes', _E3 + 'final/chapters.json'),
    'e4': ('dashboard/explainers/better-than-a-stokvel-video/', 'Bitcoin Wealth vs a stokvel: 6 questions, side by side, explained in 4 minutes', _E4 + 'final/chapters.json'),
    'e5': ('dashboard/explainers/check-it-yourself-on-bscscan-video/', 'How to check Bitcoin Wealth on BscScan: 4 steps on your phone, explained in 4 minutes', _E5 + 'final/chapters.json'),
    'e6': ('dashboard/explainers/your-own-bitcoin-wealth-marketing-website-video/', 'Your own Bitcoin Wealth marketing website: your link on every Join button, explained in 6 minutes', _E6 + 'final/chapters.json'),
}
for _k in HELD:
    EXPLAIN.pop(_k, None)
WATCH.update({k: v[0] for k, v in EXPLAIN.items()})
EXTRA += [('w-' + k, v[0], f'{V[k]["label"]}: {V[k]["short"]}', 'The video, chapter by chapter', 'film', 'How It Works') for k, v in PRESENT.items()]
EXTRA += [('w-' + k, v[0], f'{V[k]["label"]}: {V[k]["short"]}', 'The video and every word of it', 'film', 'How It Works') for k, v in EXPLAIN.items()]
import json as _json
CH = {c['key']: c['start'] for c in _json.load(open(STUDIO + '/' + PRESENT['i1'][2], encoding='utf-8'))['chapters']}
NAVD = {n[0]: n for n in NAV + EXTRA}

# Bitcoin Wealth programme facts (from the programme's own deck, as taught on bitcoinwealthpays.com)
SLOTS = [round(0.001 * 2 ** i, 3) for i in range(12)]     # 0.001 ... 2.048
LADDER = round(sum(SLOTS), 3)                             # 4.095
CYCLE1 = [('Your upline', 2, 'up'), ('Your wallet', 6, 'you'), ('Your next slot', 2, 'next'),
          ('Members below you', 3, 'below'), ('Recycle', 1, 'recycle')]
CYCLEN = [('Your upline', 2, 'up'), ('Your wallet', 7, 'you'), ('Royal Pool', 1, 'pool'),
          ('Members below you', 3, 'below'), ('Recycle', 1, 'recycle')]
RANKS = [('Ignite', 'Qualifier', 'Sponsor 2 people'), ('Beginner', 'Ranking 1', 'Reach slot 3'),
         ('Leader', 'Ranking 2', 'Reach slot 6'), ('Champion', 'Ranking 3', 'Reach slot 9'),
         ('Grand Champion', 'Ranking 4', 'Reach slot 12')]

# Zoom schedule (approved; links only inside the WhatsApp group)
ZOOM = [('Mon', '14:00', 'English'), ('Tue', '14:00', 'English'), ('Wed', '14:00', 'English'), ('Thu', '14:00', 'English'),
        ('Fri', '14:00', 'English'), ('Mon', '20:00', 'isiXhosa'), ('Tue', '20:00', 'English'), ('Wed', '20:00', 'English'),
        ('Thu', '20:00', 'isiZulu'), ('Fri', '19:00', 'Sesotho')]
ZOOM_TZ = 'Africa/Johannesburg'      # every Zoom time above is South African time (SAST, UTC+2, no daylight saving)
ZOOM_LANG = {'English': 'en', 'isiXhosa': 'xh', 'isiZulu': 'zu', 'Sesotho': 'st'}   # language codes (calendar chips, JSON-LD)
ZOOM_FROM = '2026-11-16'            # first week of the published schedule (the .ics and JSON-LD start here)
ZOOM_MIN = 60                       # a calendar reminder block, in minutes (the page shows "On now" for 90 minutes)
ZOOM_ICS = 'bitcoin-wealth-zoom-schedule.ics'   # served next to the Live On Zoom page
# MTG's words (16 Nov 2026) for the "Ask MTG directly" button: the link and its data-wa-text carry exactly this message
ZOOM_WA_TEXT = 'Hi MTG,\n\nPlease send me the Zoom link for your next Bitcoin Wealth session.\n\nThank you 😊'
ZOOM_LINE = ("We meet live on Zoom five evenings a week, in four languages. Ask the person who invited you to add you to the "
             "WhatsApp group, or tap the WhatsApp button below this video.")

INDEXNOW_KEY = 'f823902c04cfbce2c98af25999c7a9ae'


def og_file(key):
    """file name of a page's social preview picture, named for what the page is (MTG, 17 Nov 2026: every image named so search
    can read it): bitcoin-wealth-<page>-preview.jpg. The main page keeps og-land.jpg (and og-bitcoin-wealth-guide.jpg, the default)."""
    if key == 'land':
        return 'og-land.jpg'
    seg = 'bw-tribe-page-order' if key == 'order' else (NAVD[key][1].strip('/').split('/')[-1] if key in NAVD else key)
    return (seg if seg.startswith('bitcoin') or 'bitcoin-wealth' in seg else 'bitcoin-wealth-' + seg) + '-preview.jpg'

