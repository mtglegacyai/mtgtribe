# JetUP and TAG Markets: the facts register (single source of truth)

Every page of mtgtribe.com/jetup, every video script, every tutorial clip and every PDF must say the same thing as this
file. When a fact changes: update it here first, then everything listed under "Used in", then re-run the consistency
check at the bottom. Never publish content that disagrees with this file without MTG's say-so.

Last full check: 7 November 2026 (site pages, the 5 Checks v5.1 video, the sign-up training video, the JetUP Zoom promo,
the voice bank).

## The start

| Fact | Exact wording to use | Used in | Source |
|---|---|---|---|
| Start amount | About $155 in USDT or USDC: $50 into Sonic AI, $100 left in the balance for the promo, a few dollars spare | get-started, FAQ, home, training video, onboarding PDF | MTG's guide |
| Why not exactly $150 | A few cents can go on fees, so send a little more than $150 (the training uses $155) | get-started part 4 | MTG's guide; Sunday training 7 Nov 2026 |
| Password | Up to 12 characters, plus the rules shown on the sign-up screen | get-started part 1 | MTG's recording, 7 Nov 2026 (confirm on the video) |
| Sign-up tick boxes | MTG's recording (7 Nov 2026) shows no tick boxes on the sign-up form: the risk line "Trading Forex & CFDs is risky" sits under Register Now. Removed from get-started part 1 in the 7 Nov 2026 preview; the tick boxes now sit at the CopyX sync (part 2) | get-started parts 1 and 2 | MTG's part 1 and part 2 recordings |
| Email already registered | Registration fails with "email address already exists": use another email or log in | get-started part 1 | MTG's recording, 7 Nov 2026 |
| Join JetUP buttons | Every "Join JetUP" button opens MTG's Partner link (one constant, `JETUP_JOIN` in `jetup/_build/layout.py`), with the note: invited by someone else? Use their Partner link. Videos say the same | every JetUP page, tutorial videos | MTG, 7 Nov 2026 |
| Partner link, not Client link | Every member has two links. New people sign up with the Partner link | get-started part 1, FAQ | MTG's guide |
| Name at sign-up | First and last name exactly as on the ID (no nickname), or KYC fails | get-started part 1 | Sunday training 7 Nov 2026 |
| CopyX banner | A new account shows "Register CopyX": tap it. After syncing, the banner shows "User Active" with the CU number and a "Login to CopyX" button. Never register on CopyX directly ("the account will not be synchronized") | get-started part 2 | MTG's part 2 recording, 7 Nov 2026 (settles the old "Login to CopyX" vs "Register" question) |
| Sync | Enter the same password as JetUP, tick the boxes, tap "Sync Account"; "Syncing with CopyX", then "Sync successful". Then log in to TAG Markets with the same email and password; the TAG Markets email arrives (it came after the first log in for MTG): tap "Confirm email address", "Verification successful", then log in again. Confirm the email before KYC | get-started part 2, part 2 video | MTG's part 2 recording and video, 7 Nov 2026 |
| TAG Markets log in | Same email and the exact same password as JetUP (12 characters at most). "Username and password incorrect" usually means the password differs | get-started part 2, FAQ | MTG's part 2 narration, 7 Nov 2026 |
| Linked | The banner shows "User Active" and the CU number | get-started part 2 | MTG's guide |
| KYC | TAG Markets questions, then Sumsub ID and face scan, on the phone | get-started part 3 | MTG's guide |
| Deposit path | portal.tagmarkets.com, Deposit, USD, Other, 155, Next, Crypto, Submit | get-started part 4 | MTG's guide |
| Networks, in order | USDT BEP20 first, USDT TRC20 second, USDC ERC20 (highest fees) | get-started, FAQ | Site research |
| Exchanges | VALR first, Binance second (MTG's referral links), SafePal or MetaMask (official sites) | get-started, FAQ | MTG |
| Strategy | CopyX, SONIC (first in the list, no other trader), Details, Connect, Investment 50 (the screen shows a $10 minimum) | get-started part 5 | MTG's guide; Sunday training |
| Community codes | Code 1 `#9M` then Verify; code 2 `9MPromo` then Submit. Case sensitive | get-started part 5, Zoom promo | MTG's guide (codes from MTG's team) |
| Sonic terms | 30% performance fee from profits only, no management fee, no join fee, one month minimum, Amplify account | get-started part 5, how-it-works | CopyX screen |
| One month minimum (meaning) | Give the strategy at least one month (30 days) with your full amount; after that you can take your own capital out. Profits can be withdrawn any time. Promo account: your own $100 can come out after 30 days, but before 12 months that ends the promo. Not confirmed: which button stops a strategy (the red square), and what happens inside the first month | FAQ, get-started part 5 | CopyX screen "Min Investment Period: 1 Month" (guide screenshot 15); JetUP one-pager ("Your 100 USD can be withdrawn after 30 days"; "Profit: any time"); MTG, 14 Nov 2026 |
| Liquidation | Closed at a 10% loss of the starting balance, 5% with a community token | get-started, 5 checks, partner plan | CopyX screen |
| Amplify | 24x. $50 trades like $1,200, $200 like $4,800. A drop of about 4.2% equals the whole deposit | get-started, 5 checks, calculators | CopyX; maths |

## The Dennis Fast Start Promo

| Fact | Exact wording to use | Used in | Source |
|---|---|---|---|
| Claim | TAG Markets Profile, copy the CU number; jet-up.ai, orange "Dennis Fast Start Promo" tile; name, email, CU number; Join the promo; "Application received!" | get-started part 6, promo page | MTG's guide |
| Approval time | Usually a few minutes, up to 24 hours | get-started part 6 | Sunday training 7 Nov 2026 |
| Result | Two Sonic accounts under Follower Hub, Strategies: $50 and the $200 promo account | get-started part 6 | MTG's guide |
| Rules | Profits can be withdrawn any time. The $100 bonus is released after 12 months. Taking your own money out before then ends the promo. One time only | promo page, get-started, 5 checks, FAQ, videos | JetUP one-pager; MTG's guide |

## After you join

| Fact | Exact wording to use | Used in | Source |
|---|---|---|---|
| See trades | MetaTrader 5, add account, search TM Financials; login = account number, password = investor password (CopyX, Follower Hub, Strategies, eye icon); read only; Sonic trades about two or three times a day | get-started #mt5, FAQ, glossary | Sunday training 7 Nov 2026 |
| More strategies | Deposit, CopyX, SONIC, Connect, enter both codes again. The promo is not repeated | get-started #more, FAQ | Sunday training |
| Partner earnings | JetUP portal Wallet, Withdraw to the TAG wallet or an MT5 account; add your own crypto wallet under Wallets first | get-started #earnings, FAQ | Sunday training |
| Reinvest | Adds a strategy's profit back into it and starts a new one month minimum | get-started #earnings | Sunday training; CopyX terms |
| Withdrawal time | About 48 hours on average (JetUP's one-pager); fees and limits are the broker's terms | how-it-works, FAQ | JetUP one-pager |

## Partner plan (JetUP's figures, as of 4 Oct 2026)

| Fact | Exact wording to use | Used in | Source |
|---|---|---|---|
| Qualify | At least $250 of active trading to qualify as a partner | partner plan | JetUP business plan |
| Levels open | A $250 own deposit opens 3 levels. 1 to 3 direct partners: still 3 levels. From the 4th direct partner, each new direct partner opens 1 more level. 10 direct partners open all 10 | partner plan, explainer #6 | JetUP business plan (Oct 2026) and "How partners grow" one-pager |
| Client start | The sign-up training's $155 is a client start; partners check the current qualification in their partner account | partner plan, explainer #6 | partner plan page; JetUP business plan |
| Lot commission | Up to $8.00 per lot over 10 levels ($2, $1, $1, $1, then $0.50) | partner plan | JetUP business plan |
| Profit share | 1.5% on each of 10 levels, paid from the 30% share | partner plan | JetUP business plan |
| Connected accounts | Every strategy counts as a connected account (one person can have several) | (videos, if mentioned) | Sunday training |
| Infinity | From $50K new volume a month at 1.5% up to 7.5% | partner plan | JetUP business plan |
| BIX Card income | 3% spending fee; half of collected fees and card sales into the plan: L1 15%, L2 10%, L3 to L10 2.5% each, 5% leadership pool | BIX page, partner plan | JetUP partner presentation shown 7 Nov 2026 (confirm in the partner account) |

## BIX Card

| Fact | Exact wording to use | Used in | Source |
|---|---|---|---|
| Prices | App free, virtual $9.99, plastic $100.99, no top-up fee | BIX page | help.bix.fi (Sep 2026); Sunday training agrees |
| Link | KYC first; portal BIX banner (or Profile, BIX Wallets & Debit Card, Register); BixPay Settings, Scan QR; phone only: screenshot, Load from gallery; Approve; "User active" | BIX page, FAQ | MTG's BIX guide PDF; Sunday training |
| Why link now | Linking moves no money; it records the team placement for BIX commissions | BIX page, FAQ | Sunday training |
| Top up | TAG wallet withdrawal to the BIX wallet address (same network), then Top up card | BIX page | Sunday training |
| Keys | Self-custody: export the private key or recovery phrase and keep it offline | BIX page | BIX; Sunday training |
| Two links | BIX referral link for people who only want the card; JetUP Partner link first for people joining JetUP | (links rollout) | Sunday training |

## Beginner answers (MTG, 13 Nov 2026: remove fear, bust myths, keep answers short)

| Fact | Exact wording to use | Used in | Source |
|---|---|---|---|
| No recruiting needed | As a client you earn from your own strategy (70% of profit); referring anyone is never required. The partner program is optional, for members who want to help more people and build faster | FAQ, home FAQ, partner plan "Optional" | MTG; JetUP business plan |
| Why partner | "We learn best when we teach others"; more people get their own account with written rules; JetUP rewards the trading activity you help create. Never promise anyone an income | FAQ, partner plan | MTG |
| Not a pyramid | Partner rewards come from trading: Lot Commission and Global Pool from broker margin, Profit Share from the 30% share, never from client deposits | FAQ, partner plan, how-it-works #split | JetUP one-pager |
| No experience needed | Copy trading: you don't pick trades or read charts; you choose the strategy, how much to put in and when to stop; watch every trade in MT5 | FAQ, home FAQ, how-it-works #copy | site; explainer #9 |
| No promised return | No fixed, daily or guaranteed return; a promise of one is a red flag | FAQ, partner plan | JetUP business plan |
| Who holds the money | Your own MT5 account at TAG Markets, in your name; JetUP does not hold it; MTG never handles it; never send money to a person | FAQ, 5 checks | site |
| Phone only | The whole start works on a phone (MTG's step-by-step videos are phone recordings, KYC face scan, MT5 app) | FAQ | MTG's recordings |
| South Africa | TM Financials SA (Pty) Ltd, FSCA authorised, FSP 55237, for marketing services | FAQ, how-it-works, 5 checks | FSCA register |
| Fees (Sonic AI) | No management fee, no join fee; 30% of profit only when there is a profit; network fee when sending crypto; withdrawal fees and limits are the broker's terms. Do not say "no monthly fee" (JetUP membership fees not confirmed) | FAQ | CopyX screen; JetUP one-pager |

## Words and names

- Say "Jet Up" (two clear words) in every script; write "JetUP" on screen. MTG, 7 Nov 2026.
- "TAG Markets", "CopyX", "Sonic AI", "BixPay", "TM Financials" (T.M. Financials Ltd).
- Say "potential business partners" and "business partners", never "downline" or "recruits".
- TAG Markets' reminder: 88% of retail investor accounts lose money when trading CFDs. A fact for reference only: since 9 Nov 2026 (MTG) the site and the videos do not show loss statistics.

## Open questions for MTG (do not publish an answer until he confirms)

1. Settled by MTG's part 2 recording (7 Nov 2026): "Register CopyX" before linking, "User Active" and "Login to CopyX" after.
   Update get-started part 2 and the FAQ when part 2 is approved.
2. Deposit network: the Sunday presenter prefers USDC or ETH on ERC20 as "cheaper"; this site ranks BEP20, then TRC20, then
   ERC20 (normally the most expensive). The site's ranking stays unless MTG decides otherwise.
4. Risk percentage: the CopyX sync tick box says "80% of retail investors lose money"; TAG Markets' KYC reminder (and this
   site) says 88% of retail investor accounts lose money when trading CFDs. Both are TAG texts on different screens. Keep 88%
   where the site quotes the KYC reminder; quote 80% only when showing that tick box.
3. BIX commission figures come from a presentation slide. Confirm them in the partner account or an official JetUP document.

## Never import from third-party trainings

Income projections or spreadsheets (weekly rand figures, "six figure" talk, other people's earnings), advice on how much
to top up or compound, advice on hiding money from banks, unverified company claims (founding dates, licences "coming"),
other people's names, and words MTG does not use ("downline"). Teach the steps, keep the risks, leave the hype.

## Consistency check (run before every publish and after every new video or PDF)

```bash
# key numbers and words across pages, builders, scripts and PDFs text
grep -rnoiE "\$1[0-9]{2}|24x|#9M|9MPromo|12 months|30 days|one month minimum|10% |5% |BEP20|TRC20|ERC20|Login to CopyX|Register" jetup/_build/*.py
```
Then read every video script and PDF page against the tables above. Any difference is either fixed or listed under "Open
questions" for MTG.

## Source log

- 7 Nov 2026: a JetUP Sunday training (YouTube `kgV47dJprRo`, transcript supplied by MTG). Added: name as on ID, the Register
  label, SONIC first in the list, the $10 minimum note, promo approval time, MetaTrader 5 view, more strategies, withdraw and
  reinvest, BIX phone-only linking, why to link early, top-ups from TAG, private key, the portal's BIX view, BIX commissions.
  Left out: everything under "Never import".
