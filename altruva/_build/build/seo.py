# Search titles (the full <title>) and meta descriptions for every page (MTG, 25 Oct 2026: search and AI discovery pass).
# Rules: title about 60 characters or less, description 120 to 160, every claim matches what the page shows, no dashes.
from config import NV
SEO_TITLE = {
 'land': 'ALTRUVA Guide by MTG: plan, videos and how to join',
 'home': 'ALTRUVA Dashboard: start here | ALTRUVA Guide by MTG',
 'fit': 'Is ALTRUVA right for me? An honest fit check | MTG',
 'diff': 'What makes ALTRUVA different | ALTRUVA Guide by MTG',
 'split': 'ALTRUVA 100% split: where every dollar goes | MTG',
 'pkg': 'ALTRUVA packages: Starter, Builder and Elite | MTG',
 'leg': 'ALTRUVA global leg explained (40%) | ALTRUVA Guide by MTG',
 'wl': 'ALTRUVA working levels explained (25%) | MTG',
 'match': 'ALTRUVA level matching explained (25%) | MTG',
 'ranks': 'ALTRUVA ranks and Lucky Tickets explained | MTG',
 'wd': 'ALTRUVA withdraw and reinvest explained | MTG',
 'first72': 'Your first 72 hours in ALTRUVA | ALTRUVA Guide by MTG',
 'join': 'How to join ALTRUVA with SafePal, step by step | MTG',
 'tut': 'ALTRUVA tutorial videos: join, withdraw, cash out | MTG',
 'exp': 'ALTRUVA explainer videos: how the plan pays | MTG',
 'c-wd': 'ALTRUVA Withdraw Split Calculator (free) | MTG',
 'c-wl': 'ALTRUVA Working Level Calculator (free) | MTG',
 'c-m': 'ALTRUVA Level Matching Calculator (free) | MTG',
 'c-zar': 'USDT to ZAR converter: USDT to rand, live rate | MTG',
 'faq': 'ALTRUVA FAQ: questions and myths answered | MTG',
 'gloss': 'ALTRUVA glossary: crypto words in plain English | MTG',
 'safe': 'ALTRUVA safety centre: protect your wallet | MTG',
 'dl': 'ALTRUVA downloads: videos, PDF guide, share kit | MTG',
 'card': 'Spend USDT with a crypto card | ALTRUVA Guide by MTG',
 'tribe': 'Join the MTG TRIBE WhatsApp community | ALTRUVA Guide by MTG',
 'disc': 'Disclaimer | ALTRUVA Guide by MTG',
}
SEO_DESC = {
 'land': f'The independent ALTRUVA guide by MTG: {NV} short videos and plain-English pages on how the plan pays, how to join safely with SafePal and how to withdraw.',
 'home': f'Start the independent ALTRUVA guide here: {NV} short videos in the right order, your progress saved as you go, and a clear route through every page and tool.',
 'fit': 'Is ALTRUVA right for you? Five honest questions, who it suits and who it does not, and where the money really comes from, before you put in a dollar.',
 'diff': 'If a smart contract platform let you down before: what is different about ALTRUVA, what is the same, and the questions to ask any platform.',
 'split': 'How every ALTRUVA package is shared: 40% global leg, 25% working levels, 25% level matching, 5% ranks and 5% Lucky Tickets, with a short video.',
 'pkg': 'Compare the ALTRUVA Starter $25, Builder $50 and Elite $100 packages: global leg window, Lucky Tickets, ranks, and a shopping list for joining.',
 'leg': 'How the ALTRUVA global leg pays 1% per member inside your window of 10, 15 or 20 seats up and down, with a worked $100 example and a short video.',
 'wl': 'ALTRUVA working levels 1 to 9 explained: the 10%, 4%, 2% and 1% rates, how your directs open each group of levels, and what happens to closed levels.',
 'match': 'How ALTRUVA level matching works: the smaller side, the daily 25% pool and the real day 22 rate per unit, worked through step by step with a video.',
 'ranks': 'ALTRUVA Nexus and Legacy Crown ranks explained, and how the Lucky Ticket draw shares 4,000 USDT among 250 tickets. Plain English and real numbers.',
 'wd': 'How ALTRUVA withdrawals split 50/50, 60/40 or 70/30 by total deposit, why you claim first, and a real withdrawal worked through, with a free calculator.',
 'first72': 'Just joined ALTRUVA? What may be waiting from minute one, why the $100 position matters, and what two directs in your first 72 hours open.',
 'join': 'Join ALTRUVA in five steps with SafePal: set up the wallet, get USDT and BNB on BNB Smart Chain, copy the sign-up link, join, then tour the app.',
 'tut': 'Seven step-by-step ALTRUVA tutorials: SafePal setup, funding, joining, claiming a prize, withdrawing and cashing out to your bank, plus five tool trainings.',
 'exp': 'Six animated ALTRUVA explainers: the 100% split, global leg, working levels, level matching, ranks and Lucky Tickets, withdraw and reinvest.',
 'c-wd': 'Free ALTRUVA withdraw split calculator: enter your balance and total deposit to see what goes to your wallet and what is reinvested, 50/50 to 70/30.',
 'c-wl': 'Free ALTRUVA working level calculator: enter deposits on levels 1 to 9 and your number of directs to see what you earn and what stays in the contract.',
 'c-m': 'Free ALTRUVA level matching calculator: your smaller side times the daily rate per unit, plus a helper that works out the rate from the daily pool.',
 'c-zar': 'Free USDT to ZAR converter: turn USDT into South African rand with a live rate, then take off your own exchange fees to see what reaches your bank.',
 'faq': 'Straight answers to the most common ALTRUVA questions: before you join, money and risk, and using the app, plus six popular myths checked against the live app.',
 'gloss': 'Smart contract, Web3, renounced, BEP20, gas and more: the crypto words in the ALTRUVA guide explained in plain English with everyday examples.',
 'safe': 'Protect your crypto wallet: six safety habits, the scam patterns to walk away from, and how to check a smart contract on BscScan yourself.',
 'dl': f'Download all {NV} ALTRUVA videos, the two-page quick guide PDF and a ready-made WhatsApp share message. Free, and every video opens on its own cover.',
 'card': 'A shorter road from USDT to spending: how a crypto debit card for USDT and USDC on BNB Smart Chain compares with cashing out through an exchange.',
 'tribe': 'The MTG TRIBE is a WhatsApp community for action takers: learn with others, ask questions and share what works. Join, WhatsApp MTG, or follow on TikTok.',
 'disc': 'This independent ALTRUVA guide is educational, not official and not financial advice. Affiliate links, risk and privacy explained.',
}


if __name__ == '__main__':
    for k in SEO_TITLE:
        t, d = SEO_TITLE[k], SEO_DESC[k]
        print(f'{k:7s} T{len(t):3d} D{len(d):3d}', 'CHECK' if len(t) > 60 or not 120 <= len(d) <= 160 else '')
