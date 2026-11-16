"""Bitcoin Wealth guide by MTG (mtgtribe.com/bw): site configuration (links, facts, videos, menu)."""
import os

SITE = 'https://mtgtribe.com'
BASE = '/bw/'                 # prod path prefix
NAME = 'Bitcoin Wealth Guide by MTG'
TODAY = '2026-11-15'
LAUNCHED = '2026-11-14'       # first draft; update to the real go-live date when MTG approves

# where the build reads its inputs and writes its output (outside the public repo)
SCR = '/tmp/claude-0/-home-user/612e96d5-9b21-5852-ab8a-e6cd65a7a534/scratchpad/bwsite'
STUDIO = '/home/user/mtg-studio'
REPO = '/home/user/mtgtribe'

# MTG's links (confirmed current by MTG, 14 Nov 2026)
REF = 'https://vowu.io/register?ref=14638'
VALR = 'https://www.valr.com/invite/VAKM6VZY'
BINANCE = 'https://accounts.binance.com/register?ref=11139868'
WA_MTG = 'https://wa.me/27721714626'
WA_NUM = '072 171 4626'
WA_MTG_MSG = 'Hi MTG, I found your Bitcoin Wealth guide on mtgtribe.com/bw and I have a question.'
GROUP = 'https://mtgtribe.com/group/'      # MTG TRIBE WhatsApp group (Zoom links are shared there)
TIKTOK = 'https://www.tiktok.com/@joinmtgtribe'
YOUTUBE = 'https://www.youtube.com/@mtgtribe'
FACEBOOK = 'https://www.facebook.com/mtgtribe'
TELEGRAM = 'https://t.me/mtgtribe'
MTG_SITE = 'https://www.musathegiant.com'
CRYPTO101 = 'https://www.musathegiant.com/101'
CARD_GUIDE = 'https://bellveraffiliates.com/'
ORDER = '/bwcopy/'                          # BW Tribe Page order form (prod path)
MENU_EXT = {'card': CARD_GUIDE}

# on-chain facts (read from BNB Smart Chain on 14 Nov 2026; see mtg-studio ONCHAIN-CHECK-2026-11-14.md)
CONTRACT = '0x1ad09b043E0Fe59243C9a18ee1c855bd7792Cd29'
BTCB = '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c'
BSCSCAN = 'https://bscscan.com/address/' + CONTRACT
BSCSCAN_BTCB = 'https://bscscan.com/token/' + BTCB + '?a=' + CONTRACT
MEMBERS = '41,013'
CHECKED = '14 November 2026'
ON_CHAIN_SINCE = 'April 2026'
CREATED = '15 April 2026'
PRICE_ZAR = 1000          # BW Tribe Page, once-off (MTG: "R1000 is the fixed one")

SHARE_MSG = ("I've been learning how Bitcoin Wealth works with this free guide by MTG. Short videos and plain pages "
             "show how it works, how to join safely and how to check every payment yourself: https://mtgtribe.com/bw")

# released videos: code, slug, title, one-line summary, seconds, source master (in mtg-studio), extras
# extras: o='h' for a 16:9 video (laptop frame; 9:16 plays in the phone frame), poster (in mtg-studio), label, short, date
_CARTOON = 'projects/bitcoin-wealth/videos/cartoon-01-the-missing-piece/final/'
VIDEOS = [
    ('s1', 'bitcoin-wealth-the-missing-piece-cartoon', 'The Missing Piece',
     'A short cartoon. Thandi did everything right and still ends up starting over. Leo shows her the one piece she is missing: people who build together.',
     86.8, _CARTOON + 'BW-cartoon-01-the-missing-piece-16x9.mp4',
     dict(o='h', poster=_CARTOON + 'BW-cartoon-01-website-poster-16x9.jpg', label='Cartoon', short='The Missing Piece', date='2026-11-15',
          spot=(50.0, 75.7))),      # where the play button sits on the poster, in percent: the gap between the two friends
    ('t1', 'bitcoin-wealth-tutorial-1-safepal-wallet-setup', 'Set up your SafePal wallet for Bitcoin Wealth',
     'Download SafePal from the official site, create a wallet, back it up two ways, and keep only BNB, USDT and BTCB.',
     429.6, 'projects/bitcoin-wealth/tutorials/01-safepal/final/BW-Tutorial-1-SafePal-MTG.mp4',
     dict(poster='projects/bitcoin-wealth/tutorials/01-safepal/final/BW-Tutorial-1-SafePal-mtg-thumbnail-9x16.jpg')),
    ('t2', 'bitcoin-wealth-tutorial-2-buy-bnb-send-to-safepal', 'Buy BNB on VALR and send it to SafePal',
     'Send rand from your bank to VALR with your own reference, buy BNB with it, and send the BNB to your SafePal wallet on BNB Smart Chain.',
     349.9, 'projects/bitcoin-wealth/tutorials/02-bank-to-valr/final/BW-Tutorial-2-Bank-to-SafePal-MTG.mp4',
     dict(poster='projects/bitcoin-wealth/tutorials/02-bank-to-valr/final/BW-Tutorial-2-Bank-to-SafePal-website-poster-9x16.jpg', date='2026-11-16')),
]
# planned videos (shown as "coming soon", never as playable)
PLANNED = [
    ('t3', 'Tutorial', 'Swap, sign up, activate slot 1', 'Swap BNB for BTCB in SafePal and keep a little BNB for fees, sign up with the link of the person who invited you, and activate slot 1.'),
    ('e1', 'Explainer', 'Bitcoin Wealth in two minutes', 'Bitcoin, BTCB, the smart contract and wallet to wallet payments, in one picture.'),
    ('e2', 'Explainer', 'How the 14 positions pay', 'Two, four, eight: where all fourteen payments go, and why nine point to you.'),
    ('e3', 'Explainer', 'The 12 slots and the once-off', 'Why 0.001 BTC is the only slot you pay for, and what has to happen for the rest.'),
    ('e4', 'Explainer', 'Better than a stokvel?', 'Where Bitcoin Wealth beats the stokvel, and how each one is funded.'),
    ('e5', 'Explainer', 'Check it yourself on BscScan', 'Open the contract, read a real payment, and see the numbers with your own eyes.'),
]
KIND = {'t': 'Tutorial', 'e': 'Explainer', 'k': 'Tool training', 's': 'Cartoon'}
V = {}
for _v in VIDEOS:
    _x = _v[6] if len(_v) > 6 else {}
    V[_v[0]] = dict(code=_v[0], slug=_v[1], title=_v[2], desc=_v[3], secs=_v[4], master=_v[5], n=int(_v[0][1:]), kind=KIND[_v[0][0]],
                    label=_x.get('label', KIND[_v[0][0]] + ' ' + _v[0][1:]), o=_x.get('o', 'v'), poster=_x.get('poster'),
                    date=_x.get('date', LAUNCHED), spot=_x.get('spot'))
    V[_v[0]]['short'] = _x.get('short', _v[2])
SHORT = {'t1': 'Set up SafePal', 't2': 'Buy BNB, send to SafePal'}
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
    ('page', 'dashboard/bw-tribe-page/', 'Your BW Tribe Page', 'Your own copy, R1,000 once-off', 'globe', 'Your Own Page'),
    ('c-btc', 'dashboard/tools/bitcoin-to-rand/', 'Bitcoin To Rand Converter', 'Live price: BTC, USD, ZAR', 'bitcoin', 'Tools'),
    ('c-slot', 'dashboard/tools/slot-calculator/', 'Slot Calculator', 'Each slot in BTC and rand', 'calculator', 'Tools'),
    ('c-halv', 'dashboard/tools/halving-countdown/', 'Halving Countdown', 'Live block height', 'hourglass', 'Tools'),
    ('faq', 'dashboard/faq/', 'FAQ', 'Straight answers', 'circle-help', 'Help'),
    ('gloss', 'dashboard/glossary/', 'Glossary', 'Crypto words, plain English', 'book-open-text', 'Help'),
    ('safe', 'dashboard/safety/', 'Safety Centre', 'Protect your wallet', 'shield-check', 'Help'),
    ('card', 'dashboard/crypto-card/', 'Crypto Card', 'Spend your crypto', 'credit-card', 'More From MTG'),
    ('tribe', 'dashboard/tribe/', 'Join The MTG TRIBE', 'WhatsApp community', 'message-circle', 'More From MTG'),
]
EXTRA = [('disc', 'dashboard/disclaimer/', 'Disclaimer', 'Independent, educational', 'info', 'More From MTG')]
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
ZOOM_LINE = ("We meet live on Zoom five evenings a week, in four languages. Ask the person who invited you to add you to the "
             "WhatsApp group, or tap the WhatsApp button below this video.")

INDEXNOW_KEY = 'f823902c04cfbce2c98af25999c7a9ae'
