# HANDOFF BRIEF: MTG × JetUP + TAG Markets video project (for Claude Code)

Prepared 6 Nov 2026 from the MUSATHEGIANT.COM project. Everything below is the current, approved state. Approved wording is copied exactly; do not paraphrase it.

---

## 0. Start here (what to load first)

1. **GitHub repo:** `mtglegacyai/mtgtribe` (GitHub Pages site for mtgtribe.com; `main` is LIVE, so never push to main without MTG's explicit approval).
2. **Working files for this project:** branch **`jetup-video-work`**, folder `jetup-work/` (not live):
   - `videos/` final v4.2 videos and thumbnails
   - `engine/` all render code (tutorial engine, 5 Checks engine, voice-swap tools, profile photo frame, fonts)
   - `scripts/` spoken scripts, word for word
   - `timelines/` word timings and HeyGen speech responses
   - `screens/` onboarding guide pages at 200 dpi, rendered from the privacy-cleaned PDF
   - `audio/` closing track
   - `avatar/` avatar still
   - `docs/` posting packs, standards, v5 brief, website brief, links
3. **Brand assets:** branch **`brand-assets`**, folder `brand/` (MTG profile photo, face crop, photo frame code, JetUP logo set).
4. **Downloads for the future website:** branch **`jetup-downloads`**, folder `jetup/downloads/`.
5. **The same docs live in the claude.ai Project "MUSATHEGIANT.COM"** under `claude/` (paths listed in section 9).
6. **Skills to load:** `mtg-creative-standard` and `mtg-hooks-standard` (MTG's account skills). A proposed update to mtg-creative-standard adds Section 10a (full profile photo) and the voice-engine lock; check that MTG saved it.

---

## 1. Goal and audience

**Owner:** MTG 👑 | Your Digital Architect (Musa, Durban, South Africa). Brand hub: mtgtribe.com. Slogans: "Let's Get This Crypto! 💪", "It pays to pay attention, and take action", "We learn best when we teach others".

**Project goal:** help people join JetUP (community and partner program) and TAG Markets (the broker), connect the Sonic AI copy-trading strategy and claim the Dennis Fast Start Promo, step by step, honestly. The project also builds MTG's MTG TRIBE community and social channels. The primary CTA link on every JetUP video and post is **mtgtribe.com/jetup** (the page is not built yet).

**Audience:** everyday people, mostly South African, often on a phone. Many have lost money to trading apps or programs before (sceptics, the "burned before"). There are also action takers, dreamers, leaders and team builders who will share the videos. They are visual learners: every step must be seen, not only heard.

**Deliverables in this project:**
| # | Item | Status |
|---|---|---|
| 1 | **JetUP 5 Checks** (avatar explainer, 16:9, 5:53) | v4.2 done, awaiting MTG's final review |
| 2 | **JetUP + TAG Markets sign-up training** (voice-only tutorial, 16:9, 9:09) | v4.2 done; **v5 planned** (see section 10) |
| 3 | **JetUP website** at mtgtribe.com/jetup | Not started (brief ready) |
| 4 | Posting packs for every video | Written (docs/jetup-posting-packs.md) |

---

## 2. Every approved decision (MTG's rules for this project)

### Voice (locked 4 Nov 2026)
- Voice: **MTG Master Voice V2**, HeyGen voice ID **`3931c505632149ceb2bbfecf2778c09c`**, on its saved default engine **HeyGen Voice ("orca")**. Call `create_speech` / `create_speech_without_player` with **no engine, no settings, no language**, and confirm the response says `"engine": "orca"`. **Never ElevenLabs.** MTG's words: "Fix this once and for all. Across all the videos that I'm creating going forward, just use that same perfect voice." Later: "the voice is perfect now."
- Other voices in the account ("MTG Real Voice", "Musa Dumakude") must not be used.
- HeyGen credits are precious. Get it right first time, with no test renders. **Always report the remaining credits after any HeyGen task** (MTG: "I do not like surprises"). There were **250 credits** left on 5 Nov 2026, resetting 3 Dec 2026.
- Speech cost measured: about 2 credits per 500 characters (14 credits for 5,400 characters). A full Avatar V render costs about 48 credits per minute (5:47 = 278 credits).

### Avatar (only for avatar videos)
- Only avatar: **"Profile 7 - Executive MTG"**, look ID **`67b47edfb0a043189ff84ce5d055922c`** (navy blazer, white t-shirt, seated in his office). Engine **avatar_v**, 1080p, 16:9, native 25 fps, one continuous render from one uploaded audio file (audioAssetId).
- Motion prompt (exact): "Calm, relaxed and sincere, speaking directly to camera with steady eye contact. Small natural head nods and gentle hand movements resting on the desk. Relaxed natural mouth, no forced or crooked smile, little teeth showing. Lips close fully during pauses."
- Lip timing: Avatar V lips lead the voice by about 105 ms, so place the voice 105 ms earlier. On the 5 Checks v4 voice swap the voice sits at 0.865 s while the video starts at 1.0 s.
- MTG: calm, no teeth, no fake smile; natural hands synced to the words, never repeated.

### Music
- Closing track **"They Call Me MTG"** (51.36 s), file `jetup-work/audio/they-call-me-mtg-closing-track.mp3`. It starts **51.36 s before the video ends** (rule: about 50 s before the end), soft under speech (volume 0.09), then rises after the speech ends (+0.6 per second, up to 0.9), with a 2 s fade-in.
- Final mix: `loudnorm I=-14:TP=-2:LRA=11`, then 4x oversampled `alimiter` (0.62 for the training, 0.70 for 5 Checks). Result is about -14.5 LUFS with a true peak of about -3 dB.

### Look and animation (ALTRUVA standard, carried into every video, costs no credits)
- Everything said is seen, on the exact word: pop-ins (ease-back), list items one at a time with a soft tick, calculations line by line, spotlight plus a gold pointer, a tap ripple and a click sound on every demonstrated button, and captions with the active word lit.
- 👍 on "like", 📤 on "share", 💬 on "comment", 🔖 on "save", each with a pop sound and a particle burst. Platform badges whenever a platform is named: TikTok 🎵 @joinmtgtribe, YouTube ▶️ @mtgtribe, WhatsApp 💬 mtgtribe.com/group, Telegram ✈️ @mtgtribe, Facebook 📘 facebook.com/mtgtribe.
- Small emoji pops about every 10 to 20 s, above the captions, never on top of words or tap targets.
- SFX (synthesised): whoosh on scene changes, tick on list items, pop on like/share/comment/save, click on taps.
- Ending sequence: recap, Save/Share trio, "We learn best when we teach others", comment prompt, links, "IT PAYS TO / PAY ATTENTION / & TAKE / ACTION", signature outro visualised line by line, end card.
- Every URL spoken is shown big and held for a few seconds. Say "check my bio", never "link in my bio".
- Every calculation is shown on screen; every abbreviation is spelled out with a short definition.
- Every video opens on a cover frame that works as the thumbnail.
- **Colours:** JetUP purple (140,108,231) and pink (227,113,252), TAG Markets lime (203,251,97) on near-black (11,9,18), with panels (24,20,36). MTG's gold (232,194,90) is for his name and signature only.
- **JetUP logo (5 Nov 2026):** use it everywhere it fits (`brand-assets/brand/jetup/`). Use the white-text version on dark backgrounds and videos. Never recolour the mark.

### MTG's profile photo (approved 5 Nov 2026: "I am there in full size, in full force")
- Photo: `brand-assets/brand/mtg-profile-photo.png` (1254 × 1254). He wears the white mtgTribe.com "Let's Get This Crypto!" evolution t-shirt, hand at his chin, gold watch, with the gold mtgTribe.com sign behind him.
- **Always show the WHOLE square photo** (face, the full t-shirt print and the sign) in a rounded gold frame (`photo_card.py`). Never crop it to a face-only circle when it is shown large. Enlarge the container instead.
- Sizes used at 1920 × 1080: intro card about 600 px (photo left, name right), signature about 580 px, slogan about 330 px, "YOU are the best" about 230 px, end card 300 to 400 px. On the 5 Checks "Hi, I'm MTG" card, the photo fills the card (560 px).
- Only the tiny brand-bar icon (about 50 px, every frame) uses the face crop `mtg-profile-face-crop.png`.

### Script and engagement rules
- Greeting: "Hi, my name is MTG, Your Digital Architect. Thank you for taking the time to watch this training."
- Say "potential business partners" and "business partners", never "downline" or "recruits". Say "training", not "demo". Spell out abbreviations.
- **No em dashes or en dashes anywhere.**
- **Never mention Luno** (MTG doesn't like Luno).
- Networks in order of preference: **USDT BEP20** (Binance chain) first, **USDT TRC20** (Tron) second, **USDC ERC20** (Ethereum, the most expensive) only if preferred.
- Wallets in order: **VALR** first (button below the video on the website, MTG's link https://www.valr.com/invite/VAKM6VZY), **Binance** second (https://accounts.binance.com/register?ref=11139868), then the Web3 wallets **SafePal** and **MetaMask**, each with its logo or a wallet icon.
- **Community token codes (case sensitive, confirmed by MTG):** first code **`#9M`**, then Verify. Second code **`9MPromo`**, then Submit. Show them big on screen.
- Comment prompts must be strong (MTG rejected "Which step took you the longest?" as weak). A strong prompt has one easy word or number to type, a reason that helps the viewer, and a moment to do it now. Never use "tell me which step..." or "let me know what you think".
- Real urgency only: "a promo is a promo", said honestly (it was running when the video was made, confirm on jet-up.ai, no invented deadline).
- Identity calls to action, "Save this video" often, honest compliments, and no income promises, guarantees or hype.
- Signature outro, word for word, at the end of every script (see the scripts below).
- Privacy: blur emails, names, CU numbers, phone numbers, referral links and QR codes, wallet addresses, balances and MT account numbers in every frame.
- Preview before anything goes live. Never publish or push live without MTG's approval.
- Every video ships with a posting pack (title plus alternates, YouTube description with chapters, tags, pinned comment, TikTok caption, Threads, WhatsApp, Telegram and Facebook texts, thumbnail).
- Channels: TikTok @joinmtgtribe (auto-posted via Metricool at 3am SAST), YouTube @mtgtribe, WhatsApp, Telegram, Facebook, Threads. No Instagram or X.

---

## 3. Latest scripts, word for word (as spoken by the voice)

Spoken spellings are deliberate (for example "jet dash up dot A I" = jet-up.ai, "MTG tribe dot com slash jet up" = mtgtribe.com/jetup, "Valr" = VALR). Keep them when generating speech.

### 3a. JetUP + TAG Markets sign-up training, v4 script (1,414 words, approved 4 Nov 2026)

```text
Ready to open your JetUP and TAG Markets account, but not sure where to tap first? Grab your phone. We're going to do this together, one tap at a time. And stay with me, because in part five there's one screen most people skip, and you need to read it.

Hi, my name is MTG, Your Digital Architect. Thank you for taking the time to watch this training. By the end, you'll have your JetUP account, your TAG Markets account, your first deposit, the Sonic strategy connected, and the Dennis Fast Start Promo claimed. Take your time. You can pause any step and follow along with me.

Before we start, get these ready. One: the Partner link from the person who invited you. If that's me, you'll find it at MTG tribe dot com slash jet up. Two: your email and your phone. Three: your ID, driver's licence or passport, for K Y C. That means Know Your Customer: proving who you are. Four: a crypto exchange like Valr, Luno or Binance, with about one hundred and fifty five dollars in U S D T or U S D C. Those are digital dollars, called stablecoins. And five: two codes from your sponsor, which we'll use in part five.

You'll use three websites. Jet up dot I B portal dot I O is your JetUP portal: the community's front door. Portal dot tag markets dot com is TAG Markets, the broker, where your money sits in your own name. And jet dash up dot A I is JetUP's hub, where you claim the promo.

Here's the money plan. You deposit one hundred and fifty five dollars. Fifty goes into the Sonic strategy. One hundred stays in your balance for the Dennis Promo, which adds another one hundred. A few dollars stay spare. With twenty four times Amplify, fifty becomes twelve hundred, and two hundred becomes forty eight hundred. That's six thousand dollars of exposure. Exposure is the size you trade with, not money you own.

Part one. Create your JetUP account. Open the Partner link from your sponsor. Make sure it's the Partner link, not the Client link. On the sign up form, choose Individual. Type your first name, last name, email and a password, using English letters only. Choose your country, then type your cell number without the first zero. The country code is already there. Your password needs an uppercase letter, a lowercase letter, a number and a special character, with no spaces. Now read the two boxes before you tick them. The second one says leverage can amplify losses beyond your initial investment. Take that seriously. Then pass the security check, and tap Register Now. Check your email, and tap the verification link. Not in your inbox? Check spam or junk mail.

Part two. Link JetUP to TAG Markets. Log in at jet up dot I B portal dot I O. Scroll down to the Copy X banner, and tap Login to Copy X. Never register directly on the Copy X platform, or your account won't be linked to your team. You'll see Syncing with Copy X. Use the same email and password for TAG Markets. When it's done, the banner says User Active, with your C U number.

Part three. Verify your identity. TAG Markets asks a few questions: your income, your net worth, your investment goal, and whether you understand the risks. Answer honestly. Then read their reminder. This platform is not for residents of the European Union. You may have fewer protections than with a local provider. And eighty eight percent of retail investor accounts lose money when trading C F Ds. A C F D, or contract for difference, lets you trade a price movement without owning the asset. Next comes the identity check by Sum sub. Tap Continue, scan your ID, driver's licence or passport, and do the face scan.

Part four. Fund your account. Log in at portal dot tag markets dot com, with the same email and password. Under My wallet balances, tap Deposit. Choose U S D, tap Other, and type one hundred and fifty five. Tap Next, choose Crypto, and tap Submit. Pick the coin and network you're sending from. For example, U S D T on Tron, called T R C twenty, or U S D C on Ethereum, called E R C twenty. Copy the deposit address and the exact amount. The price is held for about fifteen minutes, so keep moving. Now open your exchange. Here it's Valr. Choose withdraw, paste the address, and choose the same network. The wrong network means lost funds, so check twice. Enter the amount, and look at the fee. Here it's seventy one cents on Ethereum. For recipient details, choose Individual, then Self hosted Wallet. Check that the address matches TAG Markets exactly. Tap Confirm Withdrawal, then Authorize Transaction in the email Valr sends you. Back in TAG Markets, wait for Payment found, then Payment successful. In this example, it took about three minutes.

Part five. Connect Sonic. Open the menu, tap Copy X, find Sonic, and tap Details, then Connect. Read the terms. A thirty percent performance fee, taken from profits only. No management fee, no join fee, a one month minimum, and an Amplify account. In Investment, type fifty. Only fifty. Leave the other one hundred in your balance for the promo. Now, the screen most people skip. It says: if the trader loses more than ten percent of the starting balance, your account will be liquidated. Liquidated means closed. With a community token, that limit becomes five percent. Here's why it matters. With twenty four times Amplify, a drop of about four point two percent on the trading balance is the same size as your whole deposit. Tap the arrow next to Community Token. Enter the first code from your sponsor, and tap Verify. Enter the second code in the new field, tap Submit, and wait for the tick. Tick both agreements. The second one says Copy X trades come from traders who are not part of TAG Markets. Then tap Copy Now. You'll see Success.

Part six. Claim the Dennis Fast Start Promo. In TAG Markets, open the menu, tap Profile, and write down your C U number. Go to jet dash up dot A I, and tap the orange Dennis Fast Start Promo tile. Enter your name, email and C U number exactly, and tap Join the promo. You'll see Application received. When the confirmation email arrives, open Copy X, then Follower Hub, then Strategies. You'll see two Sonic accounts: your fifty dollar account, and your two hundred dollar promo account. Know the promo rules. Profits can be withdrawn any time. The one hundred dollar bonus is released after twelve months. And taking your own money out before then ends the promo. Rules can change, so check your dashboard.

And remember: a promo is a promo. It was still running when I made this training, but it won't be there forever, and nobody can promise you the end date. So if you've decided to start, start while it's still on, and confirm it on jet dash up dot A I before you deposit. Then send this video to someone who's ready, so they can grab it too.

And that's it. Account, identity, deposit, strategy and promo, one tap at a time. Screens change over time, so if yours looks a little different, look for the same words. Save this video, so it's here when you need it. Share it with someone who's ready to start. We learn best when we teach others. Now, comment DONE as soon as your account is set up. Stuck on a step? Comment the Part number instead, and the step most of you ask about becomes my next video. Everything I showed you, plus my links, is at MTG tribe dot com slash jet up. Check my bio. And if you believe in learning before you earn, join my tribe at MTG tribe dot com slash group. It pays to pay attention, and take action.

Quick reminder: none of this is financial advice. Always do your own research. Thank you for tuning in, and for every like, share, and comment. Your support means everything. And thank yourself for taking massive action today to change your future! I wish you nothing but the best, because YOU are the best. I'm MTG, Your Digital Architect. See you on the next one. Let's Get This Crypto!
```

### 3b. JetUP 5 Checks, script (approved v3 script, re-voiced on orca for v4; 966 words; spoken in two parts)

Part 1:

```text
If you've lost money in a trading platform, a copy trading app, or a program that promised you the world, this video is for you. I'm not going to tell you this one is different. You've heard that line before. Instead, I'm going to give you five checks you can do yourself. So whatever you decide, you decide with your eyes open. Hi, I'm MTG, Your Digital Architect. Stay with me to the end, because check number four is the one most people skip. I know the feeling. The withdrawal that never came. The group that went quiet. The leader who stopped answering. So let me say this clearly. You are not foolish for trying. Trying means you want more for your family. The lesson is not to stop trying. The lesson is to verify first. So let's verify, together. Here is the simple picture. JetUP is a community, with training and AI tools. It does not trade, and it does not take your money. TAG Markets is the broker. You open a trading account there, in your own name. Then you connect a strategy through CopyX. The main one, Sonic AI, trades gold, shown as X A U, U S D. That's gold, priced in US dollars. When the strategy makes a profit, seventy percent is yours. Thirty percent pays the broker, the strategy provider, and the partner program. So if the strategy makes ten dollars, seven dollars is yours. And if it makes a loss, nobody charges you a performance fee on that loss. Check one. Who holds my money? Your deposit goes into an M T five account at TAG Markets, in your name. M T five means MetaTrader five, the trading app many brokers use. Don't take my word for it. Log in yourself, and see your own balance. Check two. Who regulates the broker? TAG Markets' trading company, T M Financials, is licensed in Mauritius by the F S C, the Financial Services Commission. TAG also has a South African company, authorised by the F S C A, our Financial Sector Conduct Authority, under F S P number five five, two three seven. You can look it up yourself. But read the fine print. TAG's own website says the South African company provides marketing services, and that trading accounts are held by the Mauritius company. So know which regulator covers your account. Also know this. Regulators in Austria, Luxembourg, Slovenia, Russia, and Quebec in Canada have published warnings that TAG Markets is not authorised in their countries. I'm telling you this because you deserve the whole picture. Search TAG Markets on the global regulator warning list. I've put the link on my page.
```

Part 2:

```text
Check three. Are the results real? Sonic AI publishes its track record on My F X Book, so you can look before you deposit. It shows plus thirty point one percent, from November twenty twenty-four to October twenty twenty-six. That's before the seventy thirty split. So thirty point one, times seventy percent, is about twenty-one percent to you, over about twenty-three months, before fees. Not forty percent a month. Not a fixed return. And past results never guarantee the future. Check four. What can go wrong? This is the one most people skip. JetUP's latest start promo works like this. You put in one hundred and fifty dollars. The promo adds one hundred. That's two hundred and fifty dollars. Amplify it twenty-four times, and it trades like six thousand dollars. That's exposure, not money you own. Bigger exposure means bigger swings, up and down. You can lose your whole deposit. And the broker's insolvency cover is one million dollars in total, for all clients together, not per person. Trading losses are not covered. Check five. Can I get out? Profits can be withdrawn any time. But the promo has rules. The bonus is released after twelve months, and taking your own money out before then ends the promo. Promo amounts change, so check the current rules in your dashboard before you start. My advice? Start small, and do a small withdrawal early. Let the system prove itself to you. So why would anyone still give this a shot? Because you can check before you deposit. Because you can start small. Because the account is in your name. And because the company writes down, in its own risk warning, that what a partner earns can be zero. That kind of honesty is worth noticing. One more truth, from JetUP's own founder. The big money comes from building a team, not from the trading percentage. Know that going in. If you check all five, and it still feels right, start small, with money you can afford to lose. Everything I showed you, plus my links, is at MTG tribe dot com slash jet up. And if it doesn't feel right? That's a good decision too. It pays to pay attention, and take action. If you believe in multiple streams of income, in learning before you earn, and in never putting all your eggs in one basket, join my tribe at MTG tribe dot com slash group, or message me on Telegram at MTG tribe. Check my bio. Save this video, so you have the five checks when you need them. And share it with someone who's been burned before. We learn best when we teach others. Comment below. Which check surprised you most? Quick reminder: none of this is financial advice. Always do your own research. Thank you for tuning in, and for every like, share, and comment. Your support means everything. And thank yourself for taking massive action today to change your future! I wish you nothing but the best, because YOU are the best. I'm MTG, Your Digital Architect. See you on the next one. Let's Get This Crypto!
```

---

## 4. Storyboard: sign-up training v4.2 (scene by scene, real timings from the final timeline)

Format 1920×1080, 25 fps. The cover frame plays first and the voice starts at 1.00 s. Each row starts on its spoken cue. "Screenshot" rows show a phone screenshot from the onboarding guide with a spotlight on the control, a gold pointer and tap ripple, label chips, and an instruction panel that slides in. The part tracker sits at the top, the brand bar top left (MTG photo icon), and the "JetUP × TAG Markets" pill top right.

| # | Starts | Spoken cue | On screen |
|---|---|---|---|
| 1 | 0:01.20 | "ready to open your jetup" | Cover/hero: Open your JetUP and TAG Markets account · Not sure where to tap first? |
| 2 | 0:06.48 | "grab your phone" | Cover/hero: Open your JetUP and TAG Markets account · 📱 Grab your phone: one tap at a time |
| 3 | 0:11.16 | "and stay with me" | Cover/hero: Open your JetUP and TAG Markets account · ⚠️ Part 5: the screen most people skip |
| 4 | 0:17.68 | "hi my name is mtg" | MTG intro card: full profile photo (left) + MTG / Your Digital Architect / Thank you for watching this training |
| 5 | 0:23.76 | "by the end" | list card: By the end, you'll have · (items pop in next) |
| 6 | 0:25.16 | "your jetup account" | list card: By the end, you'll have · shows: ✅ Your JetUP account |
| 7 | 0:26.52 | "your tag markets account" | list card: By the end, you'll have · shows: ✅ Your JetUP account, ✅ Your TAG Markets account |
| 8 | 0:28.32 | "your first deposit" | list card: By the end, you'll have · shows: ✅ Your JetUP account, ✅ Your TAG Markets account, ✅ Your first deposit |
| 9 | 0:29.80 | "the sonic strategy connected" | list card: By the end, you'll have · shows: ✅ Your JetUP account, ✅ Your TAG Markets account, ✅ Your first deposit, ✅ Sonic strategy connected |
| 10 | 0:31.84 | "and the dennis fast start promo claimed" | list card: By the end, you'll have · shows: ✅ Your JetUP account, ✅ Your TAG Markets account, ✅ Your first deposit, ✅ Sonic strategy connected, ✅ Dennis Fast Start Promo claimed |
| 11 | 0:34.44 | "take your time" | list card: By the end, you'll have · shows: ✅ Your JetUP account, ✅ Your TAG Markets account, ✅ Your first deposit, ✅ Sonic strategy connected, ✅ Dennis Fast Start Promo claimed |
| 12 | 0:38.80 | "before we start" | list card: Get these ready · (items pop in next) |
| 13 | 0:41.28 | "one the partner link" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you) |
| 14 | 0:44.92 | "if thats me" | url card:  |
| 15 | 0:50.52 | "two your email" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you), 📧 Your email and phone |
| 16 | 0:53.52 | "three your id" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you), 📧 Your email and phone, 🪪 ID, driver's licence or passport (for KYC) |
| 17 | 0:59.40 | "that means know your customer" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you), 📧 Your email and phone, 🪪 ID, driver's licence or passport (for KYC) |
| 18 | 1:03.12 | "four a crypto exchange" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you), 📧 Your email and phone, 🪪 ID, driver's licence or passport (for KYC), 💱 VALR, Luno or Binance (with about $155 in USDT or USDC) |
| 19 | 1:12.76 | "those are digital dollars" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you), 📧 Your email and phone, 🪪 ID, driver's licence or passport (for KYC), 💱 VALR, Luno or Binance (with about $155 in USDT or USDC) |
| 20 | 1:16.08 | "and five two codes" | list card: Get these ready · shows: 🔗 Partner link (from the person who invited you), 📧 Your email and phone, 🪪 ID, driver's licence or passport (for KYC), 💱 VALR, Luno or Binance (with about $155 in USDT or USDC), 🔑 Two codes from your sponsor (used in Part 5) |
| 21 | 1:21.40 | "youll use three websites" | sites card:  |
| 22 | 1:23.12 | "jet up dot i b portal" | sites card:  |
| 23 | 1:29.76 | "portal dot tag markets dot com is" | sites card:  |
| 24 | 1:36.16 | "and jet dash up dot a i is" | sites card:  |
| 25 | 1:41.60 | "heres the money plan" | money card:  |
| 26 | 1:43.12 | "you deposit one hundred" | money card:  |
| 27 | 1:45.76 | "fifty goes into" | money card:  |
| 28 | 1:48.40 | "one hundred stays" | money card:  |
| 29 | 1:51.32 | "which adds another" | money card:  |
| 30 | 1:53.28 | "a few dollars stay" | money card:  |
| 31 | 1:55.16 | "with twenty four times amplify fifty" | money card:  |
| 32 | 2:01.44 | "thats six thousand" | money card:  |
| 33 | 2:03.88 | "exposure is the size" | money card:  |
| 34 | 2:08.00 | "part one" | PART 1 title card:  |
| 35 | 2:11.24 | "open the partner link" | Screenshot `partner` (jetup) · Part 1: Open your sponsor's Partner link · label chips: Partner · panel lines: Every member has two links: Partner and Client. / Use the Partner link. |
| 36 | 2:16.72 | "on the sign up form" | Screenshot `signup` (jetup) · Part 1: Choose "Individual" · label chips: Individual · panel lines: Fill in the form using English letters only. |
| 37 | 2:19.44 | "type your first name" | Screenshot `signup` (jetup) · Part 1: Type your name, email and a password · label chips: First Name, Last Name, Email Address, Password |
| 38 | 2:25.68 | "choose your country" | Screenshot `signup` (jetup) · Part 1: Choose your country, then your cell number · panel lines: Type the number WITHOUT the first 0. / The country code (e.g. +27) is already there. |
| 39 | 2:31.80 | "your password needs" | Screenshot `signup` (jetup) · Part 1: Password rules · maths: ✔️ 1 uppercase letter | ✔️ 1 lowercase letter | ✔️ 1 number | ✔️ 1 special character | ✔️ no spaces |
| 40 | 2:38.96 | "now read the two boxes" | Screenshot `signup` (jetup) · Part 1: Read both boxes before you tick · warn: "I understand Leverage can amplify losses beyond the initial investment..." |
| 41 | 2:48.68 | "then pass the security" | Screenshot `signup` (jetup) · Part 1: Pass the security check, tap "Register Now" · label chips: Register Now |
| 42 | 2:52.48 | "check your email" | Screenshot `checkmail` (jetup) · Part 1: Open the verification link in your email · note: Not in your inbox? Check spam or junk mail. · ok: "Registration Successful. You can now log in." |
| 43 | 2:59.28 | "part two" | PART 2 title card:  |
| 44 | 3:02.64 | "log in at jet up" | Screenshot `login` (jetup) · Part 2: Log in to the JetUP portal · label chips: Login · url: jetup.ibportal.io |
| 45 | 3:06.88 | "scroll down to the copy x" | Screenshot `copyx` (jetup) · Part 2: Scroll down, tap "Login to CopyX" · label chips: Login to CopyX · warn: Never register directly on the CopyX platform, or your account won't be linked to your team. |
| 46 | 3:17.28 | "youll see syncing" | Screenshot `syncing` (jetup) · Part 2: Wait for "Syncing with Copy X..." · panel lines: Use the SAME email and password for TAG Markets. |
| 47 | 3:22.80 | "when its done" | Screenshot `copyx` (jetup) · Part 2: Done: the banner says "User Active" · ok: "User Active" with your CU number |
| 48 | 3:27.60 | "part three" | PART 3 title card:  |
| 49 | 3:30.72 | "tag markets asks a few" | Screenshot `apply` (tag) · Part 3: Answer TAG Markets' questions honestly · maths: • Your income | • Your net worth | • Your investment goal | • Do you understand the risks? |
| 50 | 3:39.92 | "then read their reminder" | Screenshot `apply` (tag) · Part 3: Read TAG Markets' reminder · warn: Not for residents of the European Union
You may have fewer protections than with a local provider
88% of retail investor accounts lose money when trading CFDs |
| 51 | 3:53.96 | "a c f d or contract" | Screenshot `apply` (tag) · Part 3: Read TAG Markets' reminder · definitions: CFD = Contract for Difference: you trade a price movement without owning the asset |
| 52 | 4:00.76 | "next comes the identity" | Screenshot `kyc` (tag) · Part 3: Identity check by Sumsub · label chips: Continue · panel lines: Scan your ID, driver's licence or passport. / Then do the face scan. |
| 53 | 4:09.88 | "part four" | PART 4 title card:  |
| 54 | 4:12.48 | "log in at portal dot" | Screenshot `wallet` (tag) · Part 4: Log in to TAG Markets · panel lines: Same email and password as JetUP. · url: portal.tagmarkets.com |
| 55 | 4:17.64 | "under my wallet balances" | Screenshot `wallet` (tag) · Part 4: Under "My wallet balances", tap "Deposit" · label chips: Deposit |
| 56 | 4:20.52 | "choose u s d" | Screenshot `amount` (tag) · Part 4: Choose USD, tap "Other", type 155 · label chips: Other, 155 |
| 57 | 4:25.12 | "tap next choose crypto" | Screenshot `method` (tag) · Part 4: Tap "Next", then choose "Crypto" · label chips: Next >, Crypto |
| 58 | 4:27.24 | "and tap submit" | Screenshot `submit` (tag) · Part 4: Tap "Submit" · label chips: Submit |
| 59 | 4:28.72 | "pick the coin and network" | Screenshot `coins` (tag) · Part 4: Pick your coin AND network · definitions: TRC-20 = USDT on the Tron network; ERC-20 = USDC on the Ethereum network |
| 60 | 4:42.48 | "copy the deposit address" | Screenshot `address` (tag) · Part 4: Copy the address and the exact amount · note: ⏱️ The price is held for about 15 minutes |
| 61 | 4:49.28 | "now open your exchange" | Screenshot `valr_net` (valr) · Part 4: In VALR: withdraw, paste, same network · warn: Wrong network = lost funds. Check twice. |
| 62 | 5:00.16 | "enter the amount" | Screenshot `valr_amt` (valr) · Part 4: Enter the amount, check the fee · maths: 155.00 USDC  amount | +   0.71 USDC  network fee | = 155.71 USDC  total |
| 63 | 5:05.36 | "for recipient details" | Screenshot `valr_rcpt` (valr) · Part 4: Recipient: "Individual", "Self-hosted Wallet" · label chips: Individual, Self-hosted Wallet |
| 64 | 5:10.36 | "check that the address" | Screenshot `valr_conf` (valr) · Part 4: Check the address, tap "CONFIRM WITHDRAWAL" · label chips: CONFIRM WITHDRAWAL · panel lines: The address must match TAG Markets exactly. |
| 65 | 5:15.24 | "then authorize transaction" | Screenshot `valr_mail` (valr) · Part 4: In the VALR email: "Authorize Transaction" · label chips: Authorize Transaction |
| 66 | 5:18.60 | "back in tag markets wait" | Screenshot `found` (tag) · Part 4: Back in TAG Markets: "Payment found!" · panel lines: Awaiting network confirmations... |
| 67 | 5:21.56 | "then payment successful" | Screenshot `success_pay` (tag) · Part 4: "Payment successful." · ok: About 3 minutes in this example |
| 68 | 5:27.88 | "part five" | PART 5 title card:  |
| 69 | 5:30.44 | "open the menu tap copy x" | Screenshot `menu` (tag) · Part 5: Open the menu, tap "CopyX" · label chips: Menu (top right), CopyX |
| 70 | 5:33.00 | "find sonic" | Screenshot `sonic` (tag) · Part 5: Find SONIC: "Details", then "Connect" · label chips: Details, Connect |
| 71 | 5:36.56 | "read the terms" | Screenshot `terms` (tag) · Part 5: Read the terms · maths: Performance fee   30% (from profits only) | Management fee     0% | Join fee           $0 | Minimum period     1 month | Account type       Amplify |
| 72 | 5:48.04 | "in investment type fifty" | Screenshot `terms` (tag) · Part 5: In "Investment" type 50. Only 50. · label chips: 50 · note: Leave the other $100 in your balance for the promo |
| 73 | 5:54.60 | "now the screen most people" | Screenshot `token1` (tag) · Part 5: ⚠️ The screen most people skip · warn: "If the manager loses more than 10% of starting balance, your account will be liquidated." |
| 74 | 6:03.24 | "liquidated means closed" | Screenshot `token1` (tag) · Part 5: ⚠️ The screen most people skip · warn: "If the manager loses more than 10% of starting balance, your account will be liquidated." · definitions: Liquidated = closed |
| 75 | 6:05.12 | "with a community token" | Screenshot `token1` (tag) · Part 5: With a community token: 5% · maths: No token:     closed at a 10% loss | With a token: closed at a 5% loss |
| 76 | 6:08.92 | "heres why it matters" | risk card:  |
| 77 | 6:17.52 | "tap the arrow next to community" | Screenshot `token1` (tag) · Part 5: Community Token: code 1, then "Verify" · label chips: Verify · panel lines: Your sponsor gives you both codes. |
| 78 | 6:23.92 | "enter the second code" | Screenshot `token2` (tag) · Part 5: Code 2 in the new field, then "Submit" · label chips: Submit |
| 79 | 6:26.96 | "and wait for the tick" | Screenshot `token3` (tag) · Part 5: Wait for the tick ✔️ |
| 80 | 6:28.32 | "tick both agreements" | Screenshot `token3` (tag) · Part 5: Tick both agreements · warn: "Trades on the CopyX platform are provided by traders, unaffiliated with Tag Markets. Tag Markets bears no responsibility..." |
| 81 | 6:35.08 | "then tap copy now" | Screenshot `copynow` (tag) · Part 5: Tap "Copy Now" · label chips: Copy Now |
| 82 | 6:37.00 | "youll see success" | Screenshot `success` (tag) · Part 5: "Success" · ok: Your $50 Sonic account is connected |
| 83 | 6:38.88 | "part six" | PART 6 title card:  |
| 84 | 6:42.48 | "in tag markets open the menu tap profile" | Screenshot `profile` (tag) · Part 6: Menu, "Profile": write down your CU number · panel lines: You will type it into the promo form next. |
| 85 | 6:48.20 | "go to jet dash up" | Screenshot `hub` (hub) · Part 6: Tap the orange "Dennis Fast Start Promo" tile · url: jet-up.ai |
| 86 | 6:55.08 | "enter your name email" | Screenshot `promo_form` (hub) · Part 6: Name, email, CU number: "Join the promo" · label chips: Join the promo · panel lines: Type them exactly as in TAG Markets. |
| 87 | 7:00.72 | "youll see application received" | Screenshot `received` (hub) · Part 6: "Application received!" · panel lines: Wait for the confirmation email. |
| 88 | 7:02.96 | "when the confirmation email" | Screenshot `follower` (tag) · Part 6: CopyX, then "Follower Hub" · label chips: Follower Hub |
| 89 | 7:07.36 | "then strategies" | Screenshot `follower` (tag) · Part 6: Then "Strategies" · label chips: Strategies |
| 90 | 7:09.16 | "youll see two sonic accounts" | Screenshot `strategies` (tag) · Part 6: Two Sonic accounts · maths: $50 account   × 24 = $1,200 | $200 promo    × 24 = $4,800 |
| 91 | 7:14.64 | "know the promo rules" | list card: Promo rules · (items pop in next) |
| 92 | 7:16.20 | "profits can be withdrawn" | list card: Promo rules · shows: 💵 Profits (withdraw any time) |
| 93 | 7:18.32 | "the one hundred dollar bonus" | list card: Promo rules · shows: 💵 Profits (withdraw any time), 📅 $100 bonus (released after 12 months) |
| 94 | 7:21.76 | "and taking your own money" | list card: Promo rules · shows: 💵 Profits (withdraw any time), 📅 $100 bonus (released after 12 months), ⛔ Your own money out before 12 months (ends the promo) |
| 95 | 7:25.20 | "rules can change" | list card: Promo rules · shows: 💵 Profits (withdraw any time), 📅 $100 bonus (released after 12 months), ⛔ Your own money out before 12 months (ends the promo), 📲 Rules can change (check your dashboard) |
| 96 | 7:28.24 | "and remember a promo is a promo" | promo card: promo |
| 97 | 7:31.00 | "it was still running" | promo card: promo |
| 98 | 7:33.20 | "but it wont be there forever" | promo card: promo |
| 99 | 7:37.28 | "so if youve decided to start" | promo card: promo |
| 100 | 7:40.32 | "and confirm it on jet dash up" | promo card: promo |
| 101 | 7:44.80 | "then send this video to someone" | promo card: promo |
| 102 | 7:49.12 | "and thats it" | list card: Done, one tap at a time · shows: ✅ Account, ✅ Identity, ✅ Deposit, ✅ Strategy, ✅ Promo |
| 103 | 7:56.96 | "screens change over time" | list card: Done, one tap at a time · shows: ✅ Account, ✅ Identity, ✅ Deposit, ✅ Strategy, ✅ Promo |
| 104 | 8:02.56 | "save this video" | engage card:  |
| 105 | 8:05.56 | "share it with someone" | engage card:  |
| 106 | 8:07.96 | "we learn best" | slogan card:  |
| 107 | 8:10.32 | "now comment done" | engage card:  · prompt: Comment DONE |
| 108 | 8:20.12 | "everything i showed you" | url card:  |
| 109 | 8:27.36 | "check my bio" | url card:  |
| 110 | 8:28.72 | "and if you believe in learning" | url card:  |
| 111 | 8:34.80 | "it pays to pay attention" | slogan card:  |
| 112 | 8:38.04 | "quick reminder" | notice card:  |
| 113 | 8:43.40 | "thank you for tuning in" | thanks card:  |
| 114 | 8:54.20 | "i wish you nothing but" | slogan card:  |
| 115 | 9:00.52 | "see you on the next one" | MTG intro card: full profile photo (left) + MTG / Your Digital Architect / Let's Get This Crypto! 💪 |

Animated ending (after the recap):

| Starts | Scene |
|---|---|
| 8:02.43 | Save / Share trio, header "HELP SOMEONE START RIGHT" (🔖 SAVE so it's here when you need it, 📤 SHARE with someone who's ready to start) |
| 8:07.80 | "We learn best when we teach others" |
| 8:10.18 | Comment scene: 💬 icon, bubble types "DONE" ✅, "as soon as your account is set up", chip "Stuck on a step? Comment the Part number" 🤔, Part 1 to Part 6 chips, chip "The step most of you ask about = my next video" 🎬 |
| 8:19.96 | Links: mtgtribe.com/jetup glowing pill |
| 8:27.46 | "Check my bio" chip + TikTok and YouTube badges |
| 8:28.64 | JOIN THE MTG TRIBE: mtgtribe.com/group + WhatsApp badge, "Learn before you earn" |
| 8:34.66 | "IT PAYS TO / PAY ATTENTION / & TAKE / ACTION" word by word, full photo on the left |
| 8:37.89 | Signature outro: "Not financial advice" shield |
| 8:43.50 | THANK YOU with 👍 📤 💬 popping on like, share, comment; "Your support means everything 🙏" |
| 8:50.30 | "Thank yourself for taking MASSIVE ACTION today 🚀" |
| 8:54.28 | "YOU ARE THE BEST" with sparkles, photo below |
| 8:57.94 | Crypto-Regards, MTG signature + large photo, "See you on the next one 👋" |
| 9:02.34 | End card: photo, Crypto-Regards MTG, Let's Get This Crypto! 💪, Check my bio, mtgtribe.com/jetup pill, TikTok/YouTube/WhatsApp/Telegram/Facebook badges, "Also watch: 5 checks before you try JetUP", disclaimer |

Speech ends 9:03.69 · video total 9:08.69 · recap starts 7:49.12 · voice placed at 1.00 s (cover first)

---

## 5. Storyboard: JetUP 5 Checks v4.2 (card by card, real timings)

| # | Starts | Spoken cue | Card on the left panel |
|---|---|---|---|
| 1 | 0:01.16 | "if youve lost money" | kicker: THIS VIDEO IS FOR YOU · head: Lost money before? · rows: 📉 A trading platform / 🤖 A copy trading app / 🎁 A program that promised the world |
| 2 | 0:08.28 | "im not going to tell you" | strike: "This one is different" to Check it yourself. |
| 3 | 0:13.60 | "five checks you can do" | kicker: TODAY · head: 5 checks you can do yourself · sub: So whatever you decide, you decide with your eyes open. |
| 4 | 0:18.92 | "hi im mtg" | big_emoji: full profile photo in gold frame (replaces 👑) · head: MTG · sub: Your Digital Architect · watch for check number 4 |
| 5 | 0:27.64 | "i know the feeling" | kicker: SOUND FAMILIAR? · rows: ⏳ The withdrawal that never came / 🔇 The group that went quiet / 📵 The leader who stopped answering |
| 6 | 0:36.48 | "you are not foolish" | big_emoji: ❤️ · head: You are not foolish for trying. · sub: Trying means you want more for your family. |
| 7 | 0:40.48 | "the lesson is not" | kicker: THE LESSON · strike: Stop trying to Verify first. |
| 8 | 0:47.28 | "here is the simple picture" | kicker: THE SIMPLE PICTURE · rows: 👥 JetUP: community, training and AI tools. Does NOT trade or take your money / 🏦 TAG Markets: the broker. Account in YOUR name / 🥇 CopyX: connect a strategy, e.g. Sonic AI |
| 9 | 1:06.40 | "x a u u s d" | kicker: DEFINITION · head: XAU/USD · sub: XAU = gold. USD = US dollar. XAU/USD = the price of gold in US dollars. |
| 10 | 1:12.64 | "when the strategy makes a profit" | kicker: PROFIT SPLIT · rows: ✅ 70% is yours / ⚙️ 30% pays the broker, the strategy provider and the partner program |
| 11 | 1:21.36 | "so if the strategy makes ten" | kicker: EXAMPLE · calc: $10 profit × 70% / = $7 to you |
| 12 | 1:25.68 | "and if it makes a loss" | big_emoji: 🛡️ · head: Loss = no performance fee · sub: Performance fee = the cut taken from profits only. |
| 13 | 1:30.40 | "check one" | kicker: CHECK 1 OF 5 · big_emoji: 💼 · head: Who holds my money? |
| 14 | 1:32.84 | "your deposit goes into" | kicker: CHECK 1 · rows: 🏦 Your deposit sits in an MT5 account at TAG Markets / 🪪 In YOUR name / 📖 MT5 = MetaTrader 5, the trading app many brokers use |
| 15 | 1:42.72 | "dont take my word" | big_emoji: 🔍 · head: Log in yourself. See your own balance. |
| 16 | 1:47.48 | "check two" | kicker: CHECK 2 OF 5 · big_emoji: ⚖️ · head: Who regulates the broker? |
| 17 | 1:53.68 | "licensed in mauritius" | kicker: LICENCE 1 · MAURITIUS · rows: 🏢 T.M. Financials Ltd (TAG Markets trading company) / 📜 FSC Mauritius · Licence GB21026474 / 📖 FSC = Financial Services Commission, Mauritius regulator |
| 18 | 1:57.92 | "tag also has a south african" | kicker: LICENCE 2 · SOUTH AFRICA · sub: Verify: fsca.co.za > Regulated Entities > FSP 55237 · rows: 🇿🇦 TM Financials SA (Pty) Ltd / 📜 FSCA authorised · FSP No. 55237 / 📖 FSCA = Financial Sector Conduct Authority, SA regulator |
| 19 | 2:09.88 | "read the fine print" | kicker: THE FINE PRINT (TAG WEBSITE) · rows: 📣 SA company: marketing services / 🏦 Trading accounts: held by the Mauritius company / ❓ Know which regulator covers YOUR account |
| 20 | 2:23.64 | "regulators in austria" | kicker: PUBLISHED REGULATOR WARNINGS · sub: Warnings that TAG Markets is not authorised in those countries. · rows: 🇦🇹 Austria · FMA / 🇱🇺 Luxembourg · CSSF / 🇸🇮 Slovenia · ATVP / 🇷🇺 Russia · Central Bank / 🇨🇦 Quebec, Canada · AMF |
| 21 | 2:34.20 | "i'm telling you this" | kicker: CHECK IT YOURSELF · head: Search "TAG Markets" · sub: IOSCO I-SCAN = the global list of regulator warnings. Link on mtgtribe.com/jetup |
| 22 | 2:43.00 | "check three" | kicker: CHECK 3 OF 5 · big_emoji: 📊 · head: Are the results real? |
| 23 | 2:45.60 | "sonic ai publishes" | kicker: CHECK 3 · rows: 📈 Sonic AI track record is public on Myfxbook / 👀 Look BEFORE you deposit |
| 24 | 2:51.52 | "it shows plus thirty" | kicker: PUBLISHED RESULT · head: +30.1% · sub: 3 Nov 2024 to 4 Oct 2026 · GROSS, before the 70/30 split |
| 25 | 3:00.36 | "so thirty point one times" | kicker: YOUR SHARE · sub: Before fees. Not a forecast. · calc: 30.1% × 70% / = 21.07% / ≈ 21% over ~23 months |
| 26 | 3:08.12 | "not forty percent" | rows: ❌ NOT 40% a month / ❌ NOT a fixed return / ⚠️ Past results never guarantee the future |
| 27 | 3:14.76 | "check four" | kicker: CHECK 4 OF 5 · big_emoji: ⚠️ · head: What can go wrong? · sub: The one most people skip. |
| 28 | 3:20.20 | "latest start promo" | kicker: START PROMO · calc: $150 yours / + $100 promo / = $250 |
| 29 | 3:28.68 | "amplify it twenty four" | kicker: AMPLIFY 24x · sub: Exposure = the size you trade with. NOT money you own. · calc: $250 × 24 / = $6,000 exposure |
| 30 | 3:32.88 | "thats exposure not money" | kicker: THE RISK · rows: ↕️ Bigger exposure = bigger swings, up AND down / 🔻 You can lose your whole deposit |
| 31 | 3:41.32 | "insolvency cover" | kicker: INSOLVENCY COVER · head: $1,000,000 TOTAL · sub: Insolvency = the broker itself going bust. · rows: 👥 For ALL clients together, not per person / 🚫 Trading losses NOT covered |
| 32 | 3:49.64 | "check five" | kicker: CHECK 5 OF 5 · big_emoji: 🚪 · head: Can I get out? |
| 33 | 3:51.88 | "profits can be withdrawn" | kicker: PROMO RULES · rows: 💵 Profits: withdraw any time / 📅 Bonus: released after 12 months / ⛔ Take your own money out before 12 months = promo ends / 📲 Check the current rules in your dashboard |
| 34 | 4:06.44 | "my advice" | kicker: MTG'S ADVICE · rows: 🌱 Start small / 🧪 Test a small withdrawal early / ✅ Let the system prove itself to you |
| 35 | 4:13.28 | "why would anyone still" | kicker: WHY SOME STILL GIVE IT A SHOT · rows: ✅ You can check before you deposit / ✅ You can start small / ✅ The account is in your name / ✅ Their own warning: "what a partner earns can be zero" |
| 36 | 4:29.56 | "one more truth" | kicker: FROM JETUP'S OWN FOUNDER · head: The big money comes from building a team, · sub: not from the trading percentage. Know that going in. |
| 37 | 4:38.80 | "if you check all five" | big_emoji: 🌱 · head: Start small. · sub: Only with money you can afford to lose. |
| 38 | 4:45.04 | "everything i showed you" | kicker: EVERYTHING + MY LINKS · sub: The 5 checks, the sources and how to join. |
| 39 | 4:50.52 | "and if it doesnt feel right" | head: Doesn't feel right? That's a good decision too. · sub: It pays to pay attention and take action. |
| 40 | 4:57.52 | "if you believe in multiple" | kicker: IS THIS YOU? · rows: 💡 Multiple streams of income / 📚 Learn before you earn / 🧺 Never all eggs in one basket |
| 41 | 5:03.92 | "join my tribe at" | kicker: JOIN THE MTG TRIBE · rows: ✈️ Telegram: @mtgtribe / 📲 Check my bio |
| 42 | 5:11.60 | "save this video" | rows: 🔖 SAVE this video: keep the 5 checks / 📤 SHARE it with someone who got burned / 🎓 We learn best when we teach others |
| 43 | 5:19.96 | "comment below" | big_emoji: 💬 · head: Which check surprised you most? · sub: Tell me in the comments. |
| 44 | 5:23.56 | "quick reminder" | kicker: QUICK REMINDER · head: Not financial advice. · sub: Always do your own research. |
| 45 | 5:28.28 | "thank you for tuning in" | big_emoji: 🙏 · head: Thank you for every like, share and comment. |
| 46 | 5:38.44 | "i wish you nothing but" | big_emoji: 👑 · head: YOU are the best. |

Layout: avatar on the right (Avatar V render, shifted right over a blurred copy of itself), frosted card panel on the left, brand bar on top (MTG photo icon, JetUP × TAG Markets pill, mtgtribe.com/jetup pill), captions at the bottom. Speech ends 5:47.94 · total 5:52.94.


---

## 6. Approved on-screen wording that is not in the voice

**Promo card (training, 7:28), title "A PROMO IS A PROMO" with ⏳:**
- ✅ Still running when I made this training
- ⏳ It won't be here forever. Nobody can promise the end date
- 🚀 Decided to start? Start while it's still on
- 🔎 Confirm it on jet-up.ai before you deposit
- 📤 Send this video to someone who's ready

**Comment scene (training, about 8:10):** speech bubble types "DONE" ✅, line "as soon as your account is set up", chip "🤔 Stuck on a step? Comment the Part number", chips "Part 1" to "Part 6", chip "🎬 The step most of you ask about = my next video".

**Save/Share header (training):** "HELP SOMEONE START RIGHT", with 🔖 SAVE "so it's here when you need it" and 📤 SHARE "with someone who's ready to start".

**End card (training):** "Also watch: 5 checks before you try JetUP".

**End card disclaimer (training):** "Not financial advice. Trading involves risk. Only use money you can afford to lose."

**End card disclaimer (5 Checks):** "Not financial advice. Trading involves risk. Only invest what you can afford to lose."

---

## 7. Assets: links, file names and IDs

| Asset | Where / ID |
|---|---|
| HeyGen voice | MTG Master Voice V2, `3931c505632149ceb2bbfecf2778c09c`, engine orca |
| HeyGen avatar look | Profile 7 - Executive MTG, `67b47edfb0a043189ff84ce5d055922c` |
| 5 Checks avatar render (Avatar V, 346.9 s, 278 credits) | HeyGen video ID `cb862cd0ccd3c211030c8ff49acf428d` (fetch a fresh download link with get_video; the file was not uploaded to GitHub, see section 8) |
| 5 Checks v4 voice (orca) | Speech request IDs `33ea8ee561ee45d1bdd896bc729cf65d` (part 1, 151.67 s) and `2b143091b6be4f59ac3b725b9fab606e` (part 2, 171.00 s); responses with word timestamps in `jetup-work/timelines/o1_tts.json`, `o2_tts.json` |
| Training voice (orca) | t1 `4f091d80aac64dc19677c9c6cf0efbb7` (184.40 s), t2 `37ab016f0e83407d984d9ea74128b092` (151.56 s), t3 `9b659845e99146bb8a5a74da2cd02e2a` (193.91 s), t4 promo + comment lines `2bddee20995141c4a835ade9d5484701` (31.53 s); responses in `jetup-work/timelines/t1_tts.json` to `t4_tts.json`, tagged texts in `jetup-work/scripts/` |
| Training word timings (final, 1,414 words) | `jetup-work/timelines/voice_tut_words.json` |
| 5 Checks word timings (v3 timeline the v4 voice was re-timed to) | `jetup-work/timelines/voice_v3_words.json`; overlay timeline `timeline5.json` |
| Closing track | `jetup-work/audio/they-call-me-mtg-closing-track.mp3` (51.36 s) |
| MTG profile photo | `brand-assets/brand/mtg-profile-photo.png` · https://raw.githubusercontent.com/mtglegacyai/mtgtribe/brand-assets/brand/mtg-profile-photo.png |
| Face crop (brand-bar icon only) | `brand-assets/brand/mtg-profile-face-crop.png` (crop of the photo: 560 px square from x 320, y 55) |
| Photo frame code | `brand-assets/brand/photo_card.py` (also `jetup-work/engine/profile/`) |
| JetUP logo | `brand-assets/brand/jetup/` with jetup-logo-original.png, jetup-logo-transparent.png, jetup-logo-white-text.png (dark backgrounds), jetup-mark.png |
| Onboarding screenshots | `jetup-work/screens/pg-01.png` to `pg-21.png` (200 dpi, from the cleaned PDF). The engine expects `../src16/pg-XX.png`, so point `page()` in render_tut.py at these |
| Fonts | `jetup-work/engine/fonts/` (GreatVibes, Montserrat, Oswald) plus system Poppins and Noto Color Emoji; icons are lucide SVGs (expected at `/home/claude/assets/package/icons/`, reinstall lucide-static if needed) |
| Downloads (future site) | `jetup-downloads/jetup/downloads/`: jetup-business-plan-oct-2026.pdf, bix-card-setup-and-funding-guide.pdf, jetup-full-presentation.pdf, jetup-partner-presentation.pdf, jetup-product-presentation.pdf, jetup-how-partners-grow-one-pager.pdf, jetup-tag-markets-onboarding-guide.pdf (another member's personal details masked), jetup-profit-share-explained.mp4 |
| MTG links | Binance https://accounts.binance.com/register?ref=11139868 · VALR https://www.valr.com/invite/VAKM6VZY · Bellver Card https://bellveraffiliates.com/ · WhatsApp https://wa.me/27721714626 · MTG TRIBE group https://mtgtribe.com/group (https://chat.whatsapp.com/HAaErtOVPr7G0AsnNCNsSN) · Telegram channel https://t.me/mtgtribez (personal @mtgtribe) · Facebook page https://www.facebook.com/mtgtribe · Facebook personal https://www.facebook.com/Musa.TheMTG · TikTok https://www.tiktok.com/@joinmtgtribe · YouTube https://www.youtube.com/@mtgtribe |
| JetUP sites | jetup.ibportal.io (portal), portal.tagmarkets.com (broker), jet-up.ai (hub, promo) |

---

## 8. What is rendered, and where it lives

| File | Where | Status |
|---|---|---|
| JetUP_5_Checks_MTG_v4.2.mp4 (1920×1080, 25 fps, 5:53, 8,814 frames, about -14.5 LUFS) + _thumbnail.jpg | `jetup-video-work/jetup-work/videos/` and sent to MTG in chat | Latest. orca voice re-timed to the v3 lips (85% of m/b/p closures on the sound), JetUP and TAG branding, full profile photo |
| JetUP_TAG_SignUp_Training_MTG_v4.2.mp4 (1920×1080, 25 fps, 9:09, 13,717 frames) + _thumbnail.jpg | same | Latest. Promo card, DONE / Part number comment scene, full profile photo |
| Earlier versions (5 Checks v1 to v4.1, training v1 to v4.1) | Only in the old cloud workspace and the chat | Superseded |
| Full narration tracks and the 5 Checks avatar render | Not uploaded (the upload was blocked by a safety check) | Rebuild the training narration from the t1 to t4 speech URLs in the timelines JSONs (they may expire) or ask MTG; re-download the avatar with HeyGen get_video `cb862cd0ccd3c211030c8ff49acf428d` |
| **Published publicly** | Nothing | Claude posted nothing. MTG may have posted the earlier approved 5 Checks v3 himself: ask him |

Mix recipe (training): voice delayed 1000 ms at -0.3 dB, plus music from TOTAL - 51.36 s, plus SFX at unity, amix normalize=0, loudnorm I=-14:TP=-2:LRA=11, 192 kHz alimiter limit=0.62, then 48 kHz, AAC 192k. 5 Checks: voice delayed 865 ms at +0.2 dB, music the same way, limiter 0.70.

---

## 9. Reference docs (claude.ai Project "MUSATHEGIANT.COM", and copies in `jetup-work/docs/`)
- `claude/jetup-training-v5-brief.md`: the full v5 plan (page-by-page verdict on the 21-page onboarding PDF)
- `claude/jetup-website-brief.md`: the website plan
- `claude/jetup-posting-packs.md`: posting packs for both videos (update file names to v4.2)
- `claude/mtg-video-animation-standard.md`, `claude/mtg-avatar-video-standard.md`, `claude/mtg-video-engagement-standard.md`: standards
- `claude/mtg-links.md`: links
- `claude/mtg-tribe-welcome-message.md`: MTG TRIBE pinned welcome message
- Sources: `claude/jetup-source-notes.md` (16 sources with fact checks), `claude/jetup-onboarding-steps.md`, `claude/jetup-onboarding-guide-21p.md`, `claude/jetup-business-plan-oct-2026.md`, `claude/bix-card-setup-guide.md`, `claude/jetup-profit-share-video-notes.md`, transcripts `claude/jetup-transcript-*.txt`
- Engine code: `claude/video-engine/jetup/` (tutorial/, v3/, v4-voice-swap/) and `claude/video-engine/profile/`

---

## 10. Open questions and next steps

**Waiting on MTG:**
1. His own **silent screen recording** of the full sign-up (once he has his $155) plus a transcript. This is the main footage for training v5.
2. **BIX Card referral link** and his **JetUP Partner link**.
3. **Which Facebook link** goes on new videos and the site: the MTG TRIBE page facebook.com/mtgtribe (used in the v4 end card and posting pack) or his personal facebook.com/Musa.TheMTG (he gave both; the welcome message lists both).
4. Final review of **5 Checks v4.2** and **training v4.2**, and approval of the posting packs.
5. Whether the profile-photo update to the **mtg-creative-standard** skill was saved.

**Next steps, in order:**
1. **Training v5** (`claude/jetup-training-v5-brief.md`), **10:00 maximum**. Improve v4, don't rebuild it. Use his recording as the footage, with zooms on every important button.
   - Remove Luno everywhere. The v4 "Get these 5 things ready" card still says "VALR, Luno or Binance", and the spoken script says "Valr, Luno or Binance".
   - Add the networks and wallets in priority order with logos, and a VALR button below the video.
   - Make pages 15 and 16 the core: "enter 50 only, leave 100 for the Dennis promo", Community Token #9M, Verify, 9MPromo, Submit, tick, Copy Now, each shown big.
   - Show page 20 (Follower Hub, Strategies, both accounts).
   - Update the page 19 summary.
   - Generate new voice only for the changed parts and splice it in (`splice_t4.py` method). Show MTG the script changes and a credit estimate first, and report credits after.
   - Optional: swap the "JetUP × TAG Markets" text pill for the real JetUP logo (white-text version) at no credit cost.
2. **5 Checks:** optional free fix on screen. The spoken line "Comment below. Which check surprised you most?" is the weak kind MTG dislikes, but changing the words needs a full avatar render (about 278 credits). Instead, add an on-screen reason such as "the check you pick most becomes my next video".
3. **JetUP website** at mtgtribe.com/jetup (`claude/jetup-website-brief.md`). It must be premium, "100 times more beautiful" than mtgtribe.com/altruva, with a trading look (candlesticks, charts), alive and interactive, fast, and SEO plus AI-search ready. Include the downloads page, the BIX Card section, wallet buttons and the honest risk boxes. Preview first, publish only after approval.
4. Later: turn the website sections into short explainer videos with the engine (no HeyGen credits where possible), and remake the Maria "one person's path" explainer with the corrected figures.

**Honesty guardrails for all JetUP content:** the Business Plan and Maria video contain claims that must never be presented as promises. Examples are "1% to 1.5% daily", "$100 into $4,800 of trading capital" (really $100 own + $100 bonus = $200 × 24 = $4,800 *exposure*) and "three levels open right after you register" (really a $250 own deposit is needed). Always show TAG Markets' warning that 88% of retail CFD accounts lose money, and the Amplify liquidation rule (10%, or 5% with a community token), next to any number.

Crypto-Regards, MTG 👑 | Your Digital Architect · Let's Get This Crypto! 💪
