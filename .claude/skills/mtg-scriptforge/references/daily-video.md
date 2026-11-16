# Today's video (MTG: "let's create today's video")

MTG, 7 November 2026: "All I want to say every day is something like 'let's create today's video', then you do the
rest, cycling through those hooks and more, making sure each video is unique, educational, punchy." When he says that
(or anything like it), run this whole routine without asking what to make.

## 1. Read the log

`tools/videos/README.md` lists every video: number, hook format, topic, length, status. Today's video gets the next
number and a new folder `tools/videos/<nn>-<slug>/`.

## 2. Pick the hook format (rotate, never the same format two days running)

1. Did You Know ...?
2. What If ...?
3. What Everyone Ought to Know About ...
4. The Truth About ... / Myth or Fact?
5. How ... Really Works
6. The Hidden Cost of ...
7. Before You ... (a short safety checklist)
8. The Story of ... (money history)
9. Can You Guess ...? (a quiz with the answer at the end)
10. Why Most People ... (money psychology)

Then start again at 1. Change the opening line itself every time, never a copy of an earlier hook.

## MTG's direction (9 November 2026): mix it up, grow the tribe, then sell

MTG: "Talk more about Bitcoin, about crypto, about blockchain, about AI, about side hustles, and just mix it all
together ... giving tips ... without any guarantees ... speak to people who are looking for ways to make money online
... we are also growing the tribe ... I want to grow my tribe. And then I want to sell ... that order is important ...
take it up a notch ... be more compelling."

- **Who we talk to:** one person who wants to make money online, is curious about Bitcoin and crypto and wants
  multiple streams of income, but is busy, a bit confused and wary of scams. Speak to that person ("you").
- **Topic mix (rotate, never the same family two days running):** Bitcoin; crypto and blockchain; AI tools and AI
  skills; side hustles and making money online (honest tips); multiple streams of income; scam awareness; money and
  banks (at most one video in four).
- **The order: tribe first, then sell.** Every Short gives value, then invites people into the free MTG TRIBE. Selling
  happens later, in the tribe and on MTG's websites (dashboards, opportunity guides), never as a pitch in a social
  video (`compliance.md`).
- **Take it up a notch (every script passes all seven):**
  1. The first second speaks to one person and names their problem or wish ("If Bitcoin still confuses you...").
  2. A big, true, specific number or a surprise in the first 3 seconds.
  3. An open loop that pays off later ("number three is where people lose everything").
  4. Fast beats: numbered steps, short punchy sentences, a new visual every 2 to 3 seconds.
  5. One practical tip they can use today, with no guarantees.
  6. A question that invites real answers and feeds the next videos ("Ask me below, I'll answer in my next videos").
  7. The tribe invite with a reason (what they get inside), then the website.
- **CTAs:** spoken: "Join the free MTG TRIBE at MTG tribe dot com slash group". On screen: mtgtribe.com/group (join
  the tribe) and mtgtribe.com (tutorials, explainers, honest guides, risks included). mtgtribe.com/group is a page on
  MTG's own website that forwards to the WhatsApp group: if WhatsApp ever closes a group, MTG points /group somewhere
  new and every video still works. Never show or say the raw chat.whatsapp.com link.
- **What the tribe is (as mtgtribe.com describes it):** a WhatsApp community of action takers: tutorials, explainers,
  tips and strategies across different opportunities, crypto, AI skills and multiple streams of income, learning
  together. Never promise anything the tribe does not do.
- **The plan of the next videos** lives in `tools/videos/PLAN.md`; follow it unless research or MTG says otherwise.

## MTG's upgrades (10 November 2026): keep improving, a gold mine of information

MTG: "You've been doing a great job ... just keep improving." The mix so far (keys, banks, Bitcoin) is what he wants.
His additions, in his words: "a wealth, a gold mine of information, of training, of just opening people's eyes to
what is possible online these days".

- **More topics:** trading (what trading is, demo accounts, risk per trade, leverage, emotions; MTG promotes trading
  opportunities, which stay on his websites and in the tribe), gold (why people hold it, how much exists, gold and
  Bitcoin), stock markets (what a stock is, indexes, dividends), smart contracts (what they are, how they work), and
  every term in his **Crypto 101 crash course** (musathegiant.com/101: 21 lessons and a 222-term glossary, from
  wallets, exchanges, CEX and DEX, custodial and non-custodial, hot and cold, scams, wallet drainers and token approvals,
  DYOR, tokenomics, market cap and FDV, unlocks and vesting, whitepapers, on-chain detective work, AI agents and
  narratives to portfolios, market cycles, crypto debit cards and tax). Read the course page before a crypto basics
  video and teach the idea fresh, never copy its text. The topics also include diversifying: income streams,
  investment portfolios and crypto portfolios.
- **Talk to full-time employees too:** some videos speak straight to people with a job. Ask compelling questions and
  touch real pain points (one income, a salary that runs out before the month, no time, no raise, job security), then
  lead to the idea of multiple streams of income, the tribe and what is on mtgtribe.com. Respect people's jobs: never
  shame them, never promise an escape.
- **Length (updated the same day: "videos can be up to 3 minutes long"):** 60 seconds or less when everything fits;
  up to 3 minutes when the topic is bigger, as long as it stays compelling from start to finish. Always vertical 9:16.
  Voice credits: about 2 for a 50 second Short (video 03), about 5 for 2 minutes and about 7 for 3 minutes; MTG
  approved up to 8 for a longer video (10 November 2026, see the standing approval below). Check the balance first and
  say it in the preview message.
- **Compelling from start to finish:** in longer videos renew the open loop every 20 to 30 seconds ("and the next one
  surprised me most"), change the picture every 2 to 3 seconds, and put emphasis on the most important things (a short
  pause before them, bigger text, a pill, Leo's point). Plan the aha and wow moments in the script.
- **Leo more often, with precise emotions** (MTG, 10 November 2026): a Leo moment at every emotional beat, about every
  6 to 12 seconds, from his existing clips by the second (`LEO_MOMENTS`), with accents, soft sounds and the action props
  (notepad, laptop). Rules and the full table: `mascot.md` ("Leo's heart", "Leo's moments", "How often and how
  precisely"). New clips only with MTG's yes.
- **Write for his voice** (MTG: "I want people to fall in love with my voice"): short warm sentences, words he would
  say to family, a pause (`<break time="0.4s"/>`) before every reveal and after every big number, questions to the
  viewer, no tongue-twisters or long lists in one breath.
- **The end of every video** (`EndScreen` in `tools/video3d/src/components/EndScreen.tsx`): the tribe invite with
  mtgtribe.com/group in a gold pill; what people find on mtgtribe.com as **3 to 7 big pills** chosen for the topic
  (`SITE_PILLS` in `Pills.tsx`: MTG, "4 or 5, but definitely not more than 7"; only lines the site really delivers);
  then his photo, the signature and **mtgtribe.com in a big solid gold pill under it** (MTG: "make it a little bit
  bigger and maybe even put it in a pill shape, just like ... the explainer videos explaining JetUp"), plus the tribe
  address.
- **3D touches in every video, with no HeyGen credits** (MTG is running low): the CSS 3D kit
  (`tools/video3d/src/three/css3d.tsx`: `Coin3D`, a thick gold coin; `Block3D`, solid blocks, bars and data) plus the 3D
  card and pill entrances; two or three real 3D moments per video, each fitted to the story (no arbitrary spinning).
  Reuse Leo's clips; make everything else in code. Never spend credits on visuals without MTG's yes.
- **Made to be shared (MTG: "I want my videos to go viral ... shared ... liking ... saving ... getting in touch with
  me, joining my tribe ... impact worldwide"):** every video has a share prompt aimed at one specific person ("Send
  this to a friend who still doesn't get Bitcoin"), a save prompt when it is full of tips ("Save this for later"), the
  question for the comments, then the tribe. Natural asks only: no rewards, no "share with 10 friends", no "comment
  YES" (`compliance.md`).

## Tone and business fit (MTG, 8 and 9 November 2026; applied to daily videos from 11 November 2026)

- **Inform, never frighten.** MTG: "Take it easy on the warnings and on the losses and negativity ... I'm trying to
  build a business here ... create videos that are going to convert these people into action takers", and "I am
  educating them so that they can make informed decisions." Calm, positive, encouraging: the number, what it means,
  the small next step. No scare hooks, no loss statistics, no warnings piled on warnings. Honesty stays: no income
  promises, and the risk is named once, gently ("No promises: it takes time and work", "Education only").
- **Never make a video that works against what MTG promotes.** Before choosing a topic, check his income streams on
  the dashboard (`destinations.md`): Bellver Card, JetUP and TAG Markets (CopyX copy trading with the Sonic AI gold
  strategy), ClickBaitPays, Bitcoin Wealth, ALTRUVA. So no "AI trading is a scam", "copy trading is dangerous" or
  "crypto cards are a trap" videos. Explain how such things work, calmly, and let his websites do the rest.
- **Scam awareness stays welcome on clear-cut cases:** someone asking for your 12 words, fake support, "guaranteed
  profits". Told as "here is how to stay safe", never as fear.
- **For full-time employees:** respect the job ("Your job matters. Keep it."), then show the small step next to it.

## 3. Pick a fresh topic from MTG's niche

Topic families: see MTG's direction and upgrades above (Bitcoin, crypto and blockchain, smart contracts and the Crypto
101 terms, AI, side hustles and making money online, multiple streams of income, trading, gold, stocks, scam awareness,
money at most one video in four), plus bridge topics from the niche menu
(self-improvement, psychology, science, history) now and then. Never repeat a topic and angle already in the log.
Prefer topics where research shows big interest and a gap (strong long videos, weak or no Shorts).

## 4. Length and layout

Always vertical (9:16): **60 seconds or less when everything fits, up to 3 minutes when the topic is bigger** (MTG,
10 November 2026; on 7 November it was "up to 1 minute"). About 130 to 160 spoken words for a Short of about 55 seconds,
about 300 for 2 minutes, about 450 for 3 minutes, plus about 3 seconds for the theme's last line at the end. Shorts skip the greeting: hook, one idea in 3 or 4 beats, one prompt, one call to
action, short sign-off ("I'm MTG, Your Digital Architect. Let's Get This Crypto!").

## 5. Make it (same rules as every video)

1. Research brief (`scripts/yt_research.py`, at least five comparable videos with real numbers, the gap, "better than"
   points, verified facts with sources).
2. Script in MTG's voice, compliance scan (`scripts/compliance_scan.py`) and human check.
3. Voice: one HeyGen speech call for the finished script, in "MTG Master Voice V3" only (voice ID
   `65f1b9ff3f1e418496de5715a801e7dd`; see "MTG's voice" below). Credits follow MTG's standing approval below; anything
   above it (or any Leo clip) waits for his yes.
4. Leo: reuse his existing clips first (video 01: V2 asks a question, V3 amazed, V5 thinking, V6 laughs in disbelief,
   V7 makes a point, L2 open paw); new clips only with MTG's go-ahead.
5. Build in the house format (video 01 as posted): gold-and-black 2.5D scenes, 3D card entrances, slow push-in, Leo in
   gold windows, word-by-word captions, soft effects fitted to this story, only the last line of his theme ("Let's get
   this crypto, wherever I go!") right after his last word, the tribe and website card (mtgtribe.com/group and
   mtgtribe.com), his formal photo in the gold circle (since 9 November 2026), a designed cover.
6. QC frames, render, loudness -14 LUFS, checks, cover embedded, posting pack (`references/posting-pack.md`).
7. Send MTG the preview, the cover and the posting texts. He posts it himself. Never publish.
8. Add the video to the log.

## MTG's voice: "MTG Master Voice V3" (since 10 November 2026)

The only approved voice is HeyGen "MTG Master Voice V3", voice ID `65f1b9ff3f1e418496de5715a801e7dd` (MTG: "V3 sounds
better, sounds exactly like me").
HeyGen's new speech engine (HeyGen Voice 1, in use since 10 November 2026) refuses "MTG Master Voice V2"
(`3931c505632149ceb2bbfecf2778c09c`): instant voices made before it "must be cloned again". With MTG's approval that day
("V3 approved", after hearing a test next to V2), V3 was cloned from about 3 minutes of his own V2 narration (videos 01
to 04). Facts of the new engine, measured on 10 November 2026:
- `<break>` tags are refused on instant voices (error 400). Send plain text, then add the pauses afterwards, for free:
  `tools/video3d/scripts/voice_timing.py` stretches the gap wherever the script file has a `//` line (`// 1.0` for a
  longer beat) and writes the voice file, words, captions and timeline.
- Ask for timestamps (`withTimestamps: true`): the result has a time for every character and word. Omit the model and
  the output format (the file is a 44.1 kHz WAV; the tools resample to 48 kHz).
- Scenes are timed by named cues from the words (`scripts/make_cues.py` with an `anchors.json`), never guessed seconds.
- Cost: 1 credit for a 7 second line and 1 credit for a 61 second script (982 characters). Check the balance before
  and after every call and report it.
- V3 speaks a little slower than V2 (about 2.8 words a second; V2 about 3.1): about 150 words for 60 seconds.
- Everything already recorded in V2 (the voice banks, the live videos) stays usable. V2 and V3 lines sound slightly
  different, so prefer one voice per new video. A failed call (error 400) costs nothing, but ask MTG before any retry.
- Measured again on 11 November 2026: 1 credit for a 47 second script (149 words, about 3.2 words a second).
- **The spoken slogan is the banked deep take (MTG, 16 November 2026).** MTG: the slogan at the end was "too high ...
  take it down, make it deep ... make it land harder. This is a slogan, so it must feel like a slogan ... after fixing
  that, just continue using that." Measured on video 11: his narration sits at about 126 Hz, the slogan inside each
  script came out at 240 to 270 Hz and rose at the end. So "Let's Get This Crypto!" is a banked take: deep (about 119 Hz,
  falling on "crypto") and ONE connected phrase of about 2 seconds. MTG rejected the first three takes the same day
  ("too slow ... too far apart from each other. It's one thing. Let's get this crypto."): never pauses between the
  words, not too slow, not too fast, not too high. The banked version (`public/voice-bank/slogan-deep.wav`) is take 2
  (`[slowly] Let's get this... crypto!`) with the gaps closed and 1.12 times faster, finished by
  `scripts/make_slogan.py` (raw takes in `voice-src/slogan/`). Don't spend credits on new takes without MTG's yes. Every video: keep the slogan in the script sent to HeyGen (so "Your Digital
  Architect." ends naturally), then run `python3 scripts/splice_slogan.py public/videos/NN` after `voice_timing.py` and
  before `make_cues.py`; in the composition import `words.json`, take `SLOGAN = W.words.slice(-4).map((w) => w.start)`,
  pass `sloganWords={SLOGAN}` to `EndScreen` (the words land on screen one by one) and add the cue
  `[SLOGAN[3] - 0.02, 'land', 0.42]` (a soft, low landing under "Crypto!"). First used in video 11 (re-made the same
  day); waiting for MTG's verdict on version A (the default) or B (take 1 joined, a touch quicker).

## Standing approval for credits

**Approved by MTG on 7 November 2026:** up to 5 HeyGen credits per daily video for the voice recording, without
asking. **Approved by MTG on 10 November 2026:** up to 8 HeyGen credits for the voice of a longer video (over about
2 minutes, up to 3 minutes), without asking. New Leo clips (about 15 credits each) and anything above these limits
still need his yes. Check the balance with
`get_current_user` first; if a generation fails, ask before trying again.
