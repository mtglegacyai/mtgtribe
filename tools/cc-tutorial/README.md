# Tutorial: how to buy Canton Coin (CC) on Kraken (mtgtribe.com/cc)

MTG's first tutorial video for the /cc guide. He records a silent phone screen recording and narrates his notes here;
the video goes in the placeholder already on mtgtribe.com/cc. Formula: `.claude/skills/mtg-tutorial-video/`.
Status (23 Nov 2026): **built, waiting for MTG's approval.** One 7:51 vertical video from both recordings (part 2: Drive id
1VXS0vbIlRH7H15fNw3-cNeWKX4qBE8rJ). Build: mtg-studio `projects/canton/tutorials/01-buy-cc-kraken/` (README there). On this
branch: the video in `cc/media/` (720p), its covers in `cc/img/`, the player (`assets/tribe/mtg-player.*`, copied from /cbp)
and the steps on /cc brought in line with the video. Not live until MTG approves the private preview. Raw recordings never go in the repository.

## Part 1 notes (MTG, 23 Nov 2026), in the order he recorded

1. **mtgtribe.com/cc**: the step-by-step guide page (the video will live here). Scroll down to "CC right now": CC around
   7.5 cents at recording time.
2. **CoinGecko**: CC ranked #25, up 3.6% at recording time (read the exact price from the recording).
3. **VALR** (money already sent from his bank to VALR): ZAR > Buy and sell > Buy > BNB, pay with ZAR, Max (whole ZAR
   balance) > converted. Why BNB and not USDT: USDT withdrawals from VALR go over Tron only, which is expensive.
4. **Kraken app**: log in. Kraken asks for a cash deposit: scroll down, choose Crypto > BNB > Deposit > read the
   instructions > Understand > copy the BNB deposit address.
5. **VALR**: BNB wallet > Withdraw > paste the Kraken address > Use all; BNB network (BNB Smart Chain) is selected by
   default > Next > recipient details (sending to his own Kraken account) > wallet provider: Self-hosted, tick the box >
   Next > confirmation page > Confirm > open the email, Authorize > Google Authenticator code > "withdrawal request received".
6. **Kraken**: Done > back to the wallet, wait for the BNB. It arrived during the Loop part. Next (part 2): find out whether
   Kraken lets him buy CC with BNB directly or whether he must sell BNB for USD or a stablecoin first, then buy CC
   (Kraken's CC market is CC/USD).
7. **While waiting, back on mtgtribe.com/cc**: the "quick answer: buy Canton Coin" steps; the guide also shows how to set up
   a decentralized (self-custody) wallet, while this video uses a centralized exchange (Kraken).
8. **CoinGecko > CC > Markets**: "All" is selected by default (centralized and decentralized); tap Centralized. Why Kraken:
   at recording time CC is not on Binance or Coinbase (on Binance he would have deposited rand and bought CC, maybe via
   USDT or USDC first). Centralized exchanges listing CC: Bybit, Kraken, Gate, OKX, Bitget, KuCoin and others: use one
   you already have. Decentralized: Temple, Bron Intents (he said "Tempo" and "Braun": the names on CoinGecko are
   Temple Digital Group and Bron Intents).
9. **5N Loop wallet** (his decentralized wallet, linked on /cc): wallet.looptech.io in the address bar > Sign up > email >
   "check your email" > Confirm email > I understand (tick every box after reading) > confirm recovery phrase. Seven steps
   in all (the guide lists them). He thinks he skipped a step here and stopped: redo this part in the next recording.

## Part 2 notes (MTG, 23 Nov 2026), picks up back on the Kraken wallet

10. **Kraken wallet** shows the BNB balance and "Start trading now". He fiddles (first time on Kraken): Trade > Crypto >
    BNB, opens Transfer by mistake. **Cut the fiddling.**
11. **Currency to USD:** Preferences > Currency: GBP > USD. Now the BNB shows as about $63.61. Keep this step (short): it
    makes the balance readable.
12. **First try (cut or one quick line):** + > Purchase crypto > Buy > search CC ("Canton") > Instant > $63 > Continue >
    Confirm opens a bank-account payment, not BNB. So BNB cannot buy CC directly here.
13. **What works (keep, the core):** convert BNB to USDT (Tether) > Max > Confirm. Then "Buy another asset" > search
    Canton (CC) > $61 (the USDT balance) > Continue > "Buy $61 worth of Canton" > Confirm > purchase done.
14. **Check the balance:** Portfolio > Assets > Canton: **777 CC**. His first ever CC purchase.
15. Line for the voice-over: anyone with Bybit, Gate, OKX, Bitget or KuCoin can do the same there.
16. **Cut everything after this** (the Loop wallet login, Receive, copy party ID, Kraken withdraw, memo). He will show the
    withdrawal to a Loop wallet in the next tutorial. Also **cut the part 1 Loop sign-up** (he says he messed it up).

### Emails to insert as proof moments (masked)

- VALR: withdrawal confirmation, after step 5.
- Kraken: "you made a deposit" with the amount, when the BNB arrives (step 10).
- Kraken: BNB to USDT conversion, after the first half of step 13.
- Kraken: USDT to CC trade with the CC received, after step 13.

### Edit brief

- As short and straightforward as possible. Flow: /cc page (brief) > CoinGecko markets (why Kraken: not on Binance or
  Coinbase yet, other exchanges) > VALR: ZAR to BNB > Kraken: deposit address > VALR: withdraw BNB > Kraken: BNB arrives >
  USD currency > BNB to USDT > buy CC > 777 CC.
- Next video line: "In the next video, I'll show you how to withdraw your CC from an exchange like Kraken to your own
  wallet, 5N Loop." Do not mention Loop otherwise. (Next video note: Kraken asks for a memo on CC withdrawals.)
- Then on mtgtribe.com/cc: a designed thumbnail, the video in the placeholder (laptop frame for wide, phone for 9:16, per
  the video rules), and a check that the page's written steps match the video (BNB route via VALR, BNB to USDT, buy CC).
  Live only after MTG approves a private preview.

## Recording 2 notes (MTG, 23 Nov 2026, narrated while recording; still in progress)

Picks up with 774 CC on Kraken. Say "Kraken" correctly in the voice-over.

17. **Two options:** keep CC on Kraken (sell later when you choose) or withdraw it to a self-custody wallet like 5N Loop.
18. **mtgtribe.com/cc > Quick answer > "5N Loop"** opens wallet.looptech.io. New users: Sign up with email. **Research the
    official Loop sign-up steps and show them in MTG's voice as if he is showing them** (he logs in with his existing account).
19. **Loop dashboard:** "Top up your fee balance: add enough CC to enable transfers". Loop is Canton-native, so sending or
    swapping needs a little CC in the fee balance. Tap **Receive** > **Copy Party ID** (the Party ID is your receiving address).
20. **Kraken > Balances > CC > Withdraw:** paste the Party ID as the Canton network address. **Memo: leave it empty.** Loop gives
    a Party ID, not a memo; a memo is only needed when the receiving platform asks for one. Say it as MTG's own knowledge
    (never mention ChatGPT). Explain the withdraw screen in a sentence, do not read it word for word.
21. **Nickname: "My Loop Wallet"** ("add a unique nickname ... we'll use it to make withdrawals easier next time") > Add
    withdrawal (address).
22. **Test first:** 59 CC > Review: **the fee is 15 CC** (taken on top) > Confirm > "Withdrawal initiated" (view transaction
    is optional). Kraken balance now about 700 CC. Teach: always test with a small amount before sending a bigger one.
23. **Loop:** balance 0 > refresh > **59 CC arrived** within seconds.
24. **Send the rest:** Kraken > CC > Withdraw > "My Loop Wallet" already selected > 685 CC (+15 CC fee) > Review > Confirm >
    Processing > Loop refresh: arrived in seconds. Line: faster the second time because the wallet is saved. Fee note, kept
    calm: 15 CC is about $1.15 at 7 to 8 cents (no predictions).
25. **Loop > Top up** the fee balance: he tries 25 CC (first time). **Research Loop's real minimum and how the fee balance
    works**, and give the correct number in the voice-over.
26. **Top up 25 CC:** enter password. **Cut the wrong-password attempt**; mask every password field. "25 CC top up
    successful". Research and explain in his voice what the fee balance is for and why it helps (first time, plain words).
27. **Purpose fulfilled:** "how to buy Canton Coin and keep it in a wallet only you control" (he holds the keys to his Loop
    wallet). Recording 2 ends here; MTG uploads it next, then says "go".

### Final brief from MTG (23 Nov 2026)

- **One solid, crystal clear, easy to follow video** from recordings 1 and 2. Sequence it properly; say things out loud in
  his voice; read or explain the /cc page where it helps (charts, steps, disclaimers): "not financial advice, I'm showing
  what I do to build my diversified crypto portfolio".
- **Update mtgtribe.com/cc to match the video:** if the steps are more than six, change "Six simple steps" and the copy so
  it all makes sense (route: VALR rand > BNB > Kraken > USDT > CC > withdraw to 5N Loop, memo empty, test small, Kraken fee
  15 CC, Loop fee balance top-up).
- **Next video:** "In the next video, I'll show you how to buy CNTN stock" (mtgtribe.com/cntn, from the dashboard).
- **Close nicely:** thanks, the usual signature ending, and calls to action from the bottom of the page: join the MTG TRIBE
  WhatsApp group (mtgtribe.com/group), follow on TikTok and YouTube, and **especially the Bellver crypto debit card**
  (bellveraffiliates.com): MTG wants to drive traffic there.
- Show MTG a private preview before anything goes live.

## Map of recording 1 (source times, 6 second contact sheets)

| Time | Shows | Keep / cut |
|---|---|---|
| 0:00 to 0:12 | Home screen, open mtgtribe.com/cc | Cut (start on the page) |
| 0:12 to 0:48 | /cc: hero, "Video tutorial coming soon", scroll to "CC right now" (price $0.0760, 7d/30d, mcap #25, ATH) | Keep short |
| 0:48 to 1:12 | CoinGecko list: CC at #25, $0.0785, +3.6% | Keep short |
| 1:18 to 2:24 | VALR: rand balance R1,140, ZAR > Buy & Sell > Buy BNB, pay ZAR, Max, Review and confirm (0.1145 BNB for R1,139) | Keep |
| 2:30 to 2:48 | VALR BNB wallet 0.1148 BNB > Withdraw | Keep |
| 2:48 to 3:30 | Kraken app (opens in GBP), Fund with crypto > BNB Chain > instructions > I understand > deposit address + QR | Keep (mask address) |
| 3:30 to 4:06 | VALR withdraw: paste address, Use all, BNB Smart Chain, recipient details (name typed), self-hosted, Confirm withdrawal, email sent | Keep (mask name, address) |
| 4:06 to 4:42 | Black (Gmail and authenticator are secure screens), authenticator code entry, done | Keep only the code screen, masked; or a title card "approve by email and authenticator" |
| 4:48 to 5:30 | Kraken Done, waiting (balance £0.00) | Cut most |
| 5:36 to 7:30 | /cc quick answer, "Where are you?", CoinGecko > CC > Markets > CEX list (Bybit, Kraken, Gate, OKX, Bitget, KuCoin, XT), DEX (Temple, Bron Intents) | Keep short (why Kraken) |
| 7:36 to 9:45 | 5N Loop sign-up (email shown), Review Risks, Confirm Ownership | Cut (redone in recording 2), mask email if any frame stays |
| 9:48 to 10:06 | Kraken: BNB arrived (£48.55), Start trading now | Keep |
| 10:06 to 11:00 | Fiddling: Buy BNB Chain, Transfer | Cut |
| 11:00 to 11:36 | Account > Preferences > Currency GBP > US Dollar; balance $63.61 | Keep |
| 11:42 to 12:42 | + > Buy > search Cc > Canton Network > $63 > "Buy $63.00 of Canton Network" pays with Google Pay | Cut, or one line: "BNB can't buy CC directly here" |
| 12:48 to 13:48 | BNB Chain > Convert to USDT: 0.11431 BNB to 61.7774 USDT (rate 545.84, fee 0.6178 USDT) > Converted | Keep |
| 13:54 to 14:30 | Buy another asset > Cc > Canton Network > 61 USDT > "Buy 61.00 USDT of Canton Network": 774.552 CC at $0.07798, fee 0.604 USDT, pay with USDT balance > Purchased | Keep (the win) |
| 14:30 to 15:48 | Rating pop-up, Portfolio: Canton Network $59, balance 774.552 CC, CoinGecko markets again | Keep balance, cut pop-up |
| 16:00 to 17:20 | Loop sign-in (email shown), dashboard $0.00, Receive, party ID copied, Kraken CC withdraw screen (address, memo) | Replace with recording 2 |
| 17:24 to 20:28 | Kraken CC page, black screens, passkey prompt, back to /cc placeholder | Cut |

Facts from the screens: CC bought **774.552 CC** (MTG said 777) for 61 USDT at $0.07798; BNB to USDT 0.11431 BNB to
61.7774 USDT. Kraken opened in GBP (pound): show the currency switch so viewers outside the UK are not confused.

## Privacy masking (before anything else)

Mask every frame that shows: his name typed in VALR's recipient details, email addresses (Loop sign-up 8:12, sign-in 16:12, Kraken account page), and the Gmail inbox, the Kraken deposit address and VALR withdrawal
address, recipient details, balances he does not want shown, the authenticator screen, and **any Loop recovery phrase**.
If a recovery phrase was on screen in the raw recording, MTG should not keep funds in that Loop wallet (make a fresh one).

## Pronunciation (for the voice-over)

- Kraken: "KRAH-kun" (say it like "crack-en" with a long "a").
- VALR: "VAL-er" (like "valour"). MTG said "Vala": the brand writes VALR.
