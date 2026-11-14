"""Bitcoin Wealth guide by MTG (mtgtribe.com/bw): site configuration (links, facts, videos, menu)."""
import os

SITE = 'https://mtgtribe.com'
BASE = '/bw/'                 # prod path prefix
NAME = 'Bitcoin Wealth Guide by MTG'
TODAY = '2026-11-14'
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

# released videos: code, slug, title, one-line summary, seconds, source master (in mtg-studio)
VIDEOS = [
    ('t1', 'bitcoin-wealth-tutorial-1-safepal-wallet-setup', 'Set up your SafePal wallet for Bitcoin Wealth',
     'Download SafePal from the official site, create a wallet, back it up two ways, and keep only BNB, USDT and BTCB.',
     429.6, 'projects/bitcoin-wealth/tutorials/01-safepal/final/BW-Tutorial-1-SafePal-MTG.mp4'),
]
# planned videos (shown as "coming soon", never as playable)
PLANNED = [
    ('t2', 'Tutorial', 'Fund SafePal and swap to BTCB', 'Buy BNB on VALR or Binance, send it on BNB Smart Chain, swap to BTCB, keep BNB for fees.'),
    ('t3', 'Tutorial', 'Join Bitcoin Wealth with SafePal', 'Paste the sign-up link in SafePal\'s browser, approve the exact amount and activate slot 1.'),
    ('e1', 'Explainer', 'Bitcoin Wealth in two minutes', 'Bitcoin, BTCB, the smart contract and wallet to wallet payments, in one picture.'),
    ('e2', 'Explainer', 'How the 14 positions pay', 'Two, four, eight: where all fourteen payments go, and why nine point to you.'),
    ('e3', 'Explainer', 'The 12 slots and the once-off', 'Why 0.001 BTC is the only slot you pay for, and what has to happen for the rest.'),
    ('e4', 'Explainer', 'Better than a stokvel?', 'Where Bitcoin Wealth beats the stokvel, and the one place the comparison stops.'),
    ('e5', 'Explainer', 'Check it yourself on BscScan', 'Open the contract, read a real payment, and see the numbers with your own eyes.'),
]
KIND = {'t': 'Tutorial', 'e': 'Explainer', 'k': 'Tool training'}
V = {v[0]: dict(code=v[0], slug=v[1], title=v[2], desc=v[3], secs=v[4], master=v[5], n=int(v[0][1:]),
                kind=KIND[v[0][0]], label=KIND[v[0][0]] + ' ' + v[0][1:]) for v in VIDEOS}
SHORT = {'t1': 'Set up SafePal'}
for _k, _v in V.items():
    _v['short'] = SHORT.get(_k, _v['title'])
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
    ('home', 'dashboard/', 'Welcome', 'Your route and progress', 'compass', 'Start here'),
    ('fit', 'dashboard/is-it-right-for-me/', 'Is it right for me?', 'An honest fit check', 'scale', 'Start here'),
    ('back', 'dashboard/welcome-back/', 'Welcome back', 'Left, stuck, or never looked?', 'heart-handshake', 'Start here'),
    ('what', 'dashboard/what-is-bitcoin-wealth/', 'What is Bitcoin Wealth?', 'Bitcoin, BTCB, smart contract', 'bitcoin', 'How it works'),
    ('hiw', 'dashboard/how-it-works/', 'The 14 positions', '2, 4, 8 and where each pays', 'network', 'How it works'),
    ('slots', 'dashboard/12-slots/', 'The 12 slots', '0.001 BTC, once-off', 'layers', 'How it works'),
    ('pool', 'dashboard/recycling-royal-pool/', 'Recycling and Royal Pool', 'After your first cycle', 'refresh-cw', 'How it works'),
    ('stokvel', 'dashboard/stokvel/', 'Better than a stokvel?', 'Where it wins, where it stops', 'users', 'How it works'),
    ('diff', 'dashboard/what-makes-it-different/', 'What makes it different', 'The original, 5 checks', 'sparkles', 'How it works'),
    ('proof', 'dashboard/check-it-yourself/', 'Check it yourself', 'Every payment is public', 'scan-search', 'How it works'),
    ('join', 'dashboard/join/', 'Join step by step', 'Wallet, BNB, BTCB, join', 'rocket', 'Get started'),
    ('tut', 'dashboard/tutorials/', 'Tutorial videos', 'Follow along, one tap at a time', 'circle-play', 'Get started'),
    ('exp', 'dashboard/explainers/', 'Explainer videos', 'How it works, in pictures', 'film', 'Get started'),
    ('zoom', 'dashboard/live-on-zoom/', 'Live on Zoom', '5 evenings, 4 languages', 'video', 'Get started'),
    ('page', 'dashboard/bw-tribe-page/', 'Your BW Tribe Page', 'Your own copy, R1,000 once-off', 'globe', 'Your own page'),
    ('c-btc', 'dashboard/tools/bitcoin-to-rand/', 'Bitcoin to Rand Converter', 'Live price: BTC, USD, ZAR', 'bitcoin', 'Tools'),
    ('c-slot', 'dashboard/tools/slot-calculator/', 'Slot Calculator', 'Each slot in BTC and rand', 'calculator', 'Tools'),
    ('c-halv', 'dashboard/tools/halving-countdown/', 'Halving Countdown', 'Live block height', 'hourglass', 'Tools'),
    ('faq', 'dashboard/faq/', 'FAQ', 'Straight answers', 'circle-help', 'Help'),
    ('gloss', 'dashboard/glossary/', 'Glossary', 'Crypto words, plain English', 'book-open-text', 'Help'),
    ('safe', 'dashboard/safety/', 'Safety centre', 'Protect your wallet', 'shield-check', 'Help'),
    ('card', 'dashboard/crypto-card/', 'Crypto card', 'Spend your crypto', 'credit-card', 'More from MTG'),
    ('tribe', 'dashboard/tribe/', 'Join the MTG TRIBE', 'WhatsApp community', 'message-circle', 'More from MTG'),
]
EXTRA = [('disc', 'dashboard/disclaimer/', 'Disclaimer', 'Independent, educational', 'info', 'More from MTG')]
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
