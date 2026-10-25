"""ALTRUVA guide by MTG: site configuration (links, videos, menu)."""

SITE = 'https://mtgtribe.com'
BASE = '/altruva/'          # prod path prefix
NAME = 'ALTRUVA Guide by MTG'
TODAY = '2026-10-25'
LAUNCHED = '2026-10-25'   # the guide went live (MTG: "Put it live now", 25 Oct 2026)

# exact values (claude/altruva-source-notes.md 5b and MTG, 25 Oct 2026)
REF = 'https://altruva.io/app/packages?ref=0x2731c9Ffa7bb6d226Ba0D6a8320CaD2d5E723997'
LOGIN = 'https://altruva.io/app'
WA_MTG = 'https://wa.me/27721714626'
WA_MTG_MSG = 'Hi MTG, I found your ALTRUVA guide on mtgtribe.com and I have a question.'
WA_NUM = '072 171 4626'
WA_GROUP = 'https://chat.whatsapp.com/DwRWt83LQO78FFlHVbtj4E?s=cl&p=a&mlu=4&ilr=4'
TIKTOK = 'https://www.tiktok.com/@joinmtgtribe'
CARD_GUIDE = 'https://bellveraffiliates.com/'
MENU_EXT = {'card': CARD_GUIDE}   # menu items that open another website in a new tab
MTG_SITE = 'https://www.musathegiant.com'
SHARE_MSG = ("I've been learning about ALTRUVA with this free guide. Short videos and plain-English pages "
             "show how it works, how to join safely and how money comes out, before you decide anything: "
             "https://mtgtribe.com/altruva")

# 13 approved videos (durations measured from the approved masters)
VIDEOS = [
    # code, slug, title, one-line summary, seconds, source master
    ('t1', 'altruva-tutorial-1-safepal-wallet-setup', 'Set up your SafePal wallet',
     'Install SafePal, create a wallet and back up your recovery phrase safely.', 178.36, 'ALTRUVA_T01_SafePal_Setup_v3.mp4'),
    ('t2', 'altruva-tutorial-2-fund-wallet-bnb-swap-usdt', 'Fund your wallet and swap to USDT',
     'Send BNB on BNB Smart Chain, swap to USDT BEP20 and keep a little BNB for fees.', 153.4, 'ALTRUVA_T02_Fund_and_Swap.mp4'),
    ('t3', 'altruva-tutorial-3-join-altruva-safepal', 'Join ALTRUVA with SafePal',
     'Open the sign-up link in SafePal Explore, choose a package, approve and sign.', 152.0, 'ALTRUVA_T03_Join_ALTRUVA.mp4'),
    ('t4', 'altruva-tutorial-4-claim-lucky-ticket-prize', 'Claim a Lucky Ticket prize',
     'Check your tickets and claim a prize straight to your wallet, in full.', 141.0, 'ALTRUVA_T04_Claim_Prize.mp4'),
    ('t5', 'altruva-tutorial-5-claim-withdraw-to-safepal', 'Claim and withdraw to SafePal',
     'Claim first, withdraw everything, and see your USDT land in SafePal.', 133.8, 'ALTRUVA_T05_Withdraw_to_SafePal.mp4'),
    ('t6', 'altruva-tutorial-6-cash-out-usdt-to-bank', 'Cash out USDT to your bank',
     'SafePal to Binance (VALR works the same), USDT to rand, rand to your bank.', 172.7, 'ALTRUVA_T06_Cash_Out_to_Bank.mp4'),
    ('t7', 'altruva-tutorial-7-dashboard-tour', 'Your ALTRUVA dashboard tour',
     'Overview, Packages, Earnings, Network and More: what every screen means.', 162.6, 'ALTRUVA_T07_Dashboard_Tour.mp4'),
    ('e1', 'altruva-explainer-1-where-every-dollar-goes', 'Where every dollar goes',
     'The 100% split: 40, 25, 25, 5 and 5, explained with a stokvel pot.', 117.0, 'ALTRUVA_E1_Where_Every_Dollar_Goes.mp4'),
    ('e2', 'altruva-explainer-2-global-leg', 'The global leg, 40%',
     'One long queue, your window up and down, and 1% per member.', 124.4, 'ALTRUVA_E2_The_Global_Leg.mp4'),
    ('e3', 'altruva-explainer-3-working-levels', 'Working levels, 25%',
     'Nine levels like a family tree, and how directs open them.', 129.3, 'ALTRUVA_E3_Working_Levels.mp4'),
    ('e4', 'altruva-explainer-4-level-matching', 'Level matching, 25%',
     'The see-saw, the smaller side and the daily pool, with real day 22 numbers.', 138.6, 'ALTRUVA_E4_Level_Matching.mp4'),
    ('e5', 'altruva-explainer-5-ranks-lucky-tickets', 'Ranks and Lucky Tickets',
     'Nexus, Legacy Crown, and how the 250-ticket draw works.', 161.1, 'ALTRUVA_E5_Ranks_and_Lucky_Tickets.mp4'),
    ('e6', 'altruva-explainer-6-withdraw-reinvest', 'Withdraw and reinvest',
     'The automatic split, 50/50 to 70/30, and why you claim first.', 139.2, 'ALTRUVA_E6_Withdraw_and_Reinvest.mp4'),
    ('e7', 'altruva-explainer-7-first-72-hours', 'Your first 72 hours',
     'What may be waiting from minute one, why the $100 position matters, and what two directs in 72 hours open.', 178.4, 'ALTRUVA_E7_Your_First_72_Hours.mp4'),
    # tool trainings: every tap on this website's tools (MTG approved the scripts, 25 Oct 2026)
    ('k1', 'altruva-tool-training-1-usdt-to-rand-converter', 'USDT to Rand Converter',
     'Check the rate, plan your package with BNB for fees, cash out, and switch to Rand to USDT.', 179.9, 'ALTRUVA_K1_USDT_to_Rand_Converter.mp4'),
    ('k2', 'altruva-tool-training-2-withdraw-split-calculator', 'Withdraw Split Calculator',
     'Your balance and total deposit in, what reaches your wallet out: the real 23.63 example and the bigger tiers.', 150.9, 'ALTRUVA_K2_Withdraw_Split_Calculator.mp4'),
    ('k3', 'altruva-tool-training-3-working-level-calculator', 'Working Level Calculator',
     'Choose your directs, type a deposit on a level, and see what it pays or what stays in the contract.', 135.0, 'ALTRUVA_K3_Working_Level_Calculator.mp4'),
    ('k4', 'altruva-tool-training-4-matching-calculator', 'Matching Calculator',
     "Both sides, the day's rate, and why only the smaller side counts, with the real day 22 numbers.", 145.8, 'ALTRUVA_K4_Matching_Calculator.mp4'),
    ('k5', 'altruva-tool-training-5-72-hour-clock', 'Your 72-hour clock',
     'Set your join time and watch your 72-hour window count down, saved on your phone only.', 121.9, 'ALTRUVA_K5_72_Hour_Clock.mp4'),
]
KIND = {'t': 'Tutorial', 'e': 'Explainer', 'k': 'Tool training'}
V = {v[0]: dict(code=v[0], slug=v[1], title=v[2], desc=v[3], secs=v[4], master=v[5], n=int(v[0][1:]),
                kind=KIND[v[0][0]], label=KIND[v[0][0]] + ' ' + v[0][1:]) for v in VIDEOS}
# short, single-line titles for lists, tiles, map links and buttons (MTG, 25 Oct 2026)
SHORT = {'t1': 'Set up SafePal', 't2': 'Fund and swap to USDT', 't3': 'Join ALTRUVA', 't4': 'Claim a prize',
         't5': 'Claim and withdraw', 't6': 'Cash out to your bank', 't7': 'Dashboard tour',
         'e1': 'Where every dollar goes', 'e2': 'The global leg', 'e3': 'Working levels', 'e4': 'Level matching',
         'e5': 'Ranks and Lucky Tickets', 'e6': 'Withdraw and reinvest', 'e7': 'Your first 72 hours',
         'k1': 'USDT to Rand Converter', 'k2': 'Withdraw Split Calculator', 'k3': 'Working Level Calculator',
         'k4': 'Matching Calculator', 'k5': 'Your 72-hour clock'}
for _k, _v in V.items():
    _v['short'] = SHORT.get(_k, _v['title'])
TOTAL_MIN = round(sum(v[4] for v in VIDEOS) / 60)
TUT = [k for k in V if k[0] == 't']
EXP = [k for k in V if k[0] == 'e']
TOOL = [k for k in V if k[0] == 'k']
NV = len(VIDEOS)
EXP_MIN = round(sum(V[k]['secs'] for k in EXP) / 60)
WORDS_N = {6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine'}


def mmss(s):
    s = int(round(s))
    return f'{s // 60}:{s % 60:02d}'


def iso_dur(s):
    s = int(round(s))
    return f'PT{s // 60}M{s % 60}S'


# side menu: key, path (relative to /altruva/), label, subtitle, icon, group
NAV = [
    ('home', 'dashboard/', 'Welcome', 'Your route and progress', 'compass', 'Start here'),
    ('fit', 'dashboard/is-it-right-for-me/', 'Is it right for me?', 'An honest fit check', 'scale', 'Start here'),
    ('diff', 'dashboard/what-makes-it-different/', 'What makes it different', 'If you tried others before', 'sparkles', 'Start here'),
    ('split', 'dashboard/how-it-works/', 'Where every dollar goes', 'The 100% split', 'chart-pie', 'How it works'),
    ('pkg', 'dashboard/packages/', 'Packages', 'Starter, Builder, Elite', 'package', 'How it works'),
    ('leg', 'dashboard/global-leg/', 'Global leg', '40%, your window', 'route', 'How it works'),
    ('wl', 'dashboard/working-levels/', 'Working levels', '25%, nine levels deep', 'layers', 'How it works'),
    ('match', 'dashboard/level-matching/', 'Level matching', '25%, the daily pool', 'arrow-left-right', 'How it works'),
    ('ranks', 'dashboard/ranks-lucky-tickets/', 'Ranks and Lucky Tickets', '5% plus 5%', 'ticket', 'How it works'),
    ('wd', 'dashboard/withdraw-reinvest/', 'Withdraw and reinvest', 'How money comes out', 'wallet', 'How it works'),
    ('join', 'dashboard/join/', 'Join step by step', 'Wallet, USDT, join', 'rocket', 'Get started'),
    ('first72', 'dashboard/first-72-hours/', 'Your first 72 hours', 'Build from minute one', 'timer', 'Get started'),
    ('tut', 'dashboard/tutorials/', 'Tutorial videos', '7 tutorials, 5 tool trainings', 'circle-play', 'Get started'),
    ('exp', 'dashboard/explainers/', 'Explainer videos', f'{len(EXP)} animated explainers', 'film', 'Get started'),
    ('c-wd', 'dashboard/tools/withdraw-split-calculator/', 'Withdraw Split Calculator', 'To wallet and reinvested', 'percent', 'Tools'),
    ('c-wl', 'dashboard/tools/working-level-calculator/', 'Working Level Calculator', 'Levels 1 to 9', 'calculator', 'Tools'),
    ('c-m', 'dashboard/tools/matching-calculator/', 'Matching Calculator', 'Smaller side times rate', 'equal', 'Tools'),
    ('c-zar', 'dashboard/tools/usdt-to-rand/', 'USDT to Rand Converter', 'Live rate, your fees', 'banknote', 'Tools'),
    ('faq', 'dashboard/faq/', 'FAQ', 'Questions and myths', 'circle-help', 'Help'),
    ('gloss', 'dashboard/glossary/', 'Glossary', 'Crypto words, plain English', 'book-open-text', 'Help'),
    ('safe', 'dashboard/safety/', 'Safety centre', 'Protect your wallet', 'shield-check', 'Help'),
    ('dl', 'dashboard/downloads/', 'Downloads', 'Videos, guide, share kit', 'download', 'Help'),
    ('card', 'dashboard/crypto-card/', 'Crypto card', 'Spend your USDT', 'credit-card', 'More from MTG'),
    ('tribe', 'dashboard/tribe/', 'Join the MTG TRIBE', 'WhatsApp community', 'message-circle', 'More from MTG'),
]
EXTRA = [('disc', 'dashboard/disclaimer/', 'Disclaimer', 'Independent, educational', 'info', 'More from MTG')]
NAVD = {n[0]: n for n in NAV + EXTRA}

# IndexNow (Bing, Yahoo via Bing, Yandex, Seznam, Naver): key file served at mtgtribe.com/<key>.txt
INDEXNOW_KEY = 'f823902c04cfbce2c98af25999c7a9ae'
