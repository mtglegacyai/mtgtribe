# Learning system plan: JetUP and TAG Markets (mtgtribe.com/jetup)

Follows the skill **mtg-site-learning-system**. Audit done 6 November 2026 (all 13 pages, about 8,600 words). MTG has read
the report. Nothing is produced yet: we make one video at a time, after MTG supplies his links.

Status key: planned, voice approved, storyboard, preview sent, approved, live.

## Links MTG still has to supply

- [ ] JetUP **Partner link** (MTG is registering now, 7 Nov 2026). It goes on every sign-up button.
- [ ] **BIX Card referral link** (for people who only want the card; JetUP joiners use the Partner link first).
- [ ] Any other referral links for the buttons.
- [ ] MTG's own **step-by-step tutorial recording** of getting started with JetUP and TAG Markets.

## MTG's tutorial recording (started 7 Nov 2026)

MTG records one short silent phone video per part and sends his spoken notes with each. Notes, editing rules and status:
`tools/jetup-tutorial/README.md`. Format: separate short videos per part, not one long video.

## When MTG's step-by-step tutorial video arrives (do all of this without being asked again)

1. Watch it end to end and list every step, label and screen. Compare with `jetup-facts.md` and the sign-up training page;
   MTG's own recording wins on any difference (update the facts file first, then everything that uses it).
2. Cut it into chapter clips (parts 1 to 6) and put them beside the matching parts of /jetup/get-started/.
3. **Getting started PDF:** reproduce the step-by-step guide as a PDF from MTG's video steps and screens (plus anything
   useful from `jetup-facts.md`), with tappable buttons to the page, the clips and his links.
4. **Master PDF companion:** the ultimate PDF for the whole JetUP site (`references/pdf-companion.md` in the skill).
5. **Consistency pass:** check every page, video script, clip and PDF against `jetup-facts.md`. No conflicting numbers,
   steps, labels or rules anywhere. Report what changed.
6. Preview everything to MTG; publish only with his approval.

## When MTG's links arrive: the CTA rollout (JetUP site)

Every call to action on the JetUP pages carries MTG's own link, with copy that tells the visitor what happens next.
Today's placeholders to replace or upgrade:
- get-started "Before we start": the "Ask MTG for his Partner link" WhatsApp button becomes the Partner link itself
  (keep WhatsApp as the second option: "Stuck? Ask MTG").
- get-started part 1 "Open the Partner link from your sponsor": add "If MTG invited you, start here" with his link.
- Home hero, the 5 checks ending, how-it-works, promo, partner plan and FAQ endings: one clear sign-up button each.
- BIX Card page: "MTG's BIX Card link is coming" becomes a "Get your BIX Card" button with his BIX link.
- The top bar "Start the training" and the phone thumb bar stay as they are (they lead to the training first).
- Mark every referral button as MTG's referral link (the site's disclosure line), keep the risk line near it.
- Update the HowTo and FAQ structured data, titles and descriptions where the new step adds search value.
- Run the full test suite, the sideways-scroll check and a live link check, then preview to MTG.

## Voice

Voice bank: branch `jetup-video-work`, folder `jetup-work/voice-bank/` (saved 6 Nov 2026 with MTG's permission):
5 Checks and sign-up training narration, about 15 minutes, 262 sentences in `sentences.tsv`.
Check the HeyGen credit balance before any speech request.

**HeyGen voice status, 10 Nov 2026 (read before any speech request).** HeyGen's connector now speaks only with its new
model ("heygen-voice-1"). One request with MTG Master Voice V2 (3931c505632149ceb2bbfecf2778c09c) was refused: "This
voice is not compatible with heygen-voice-1. Create a new instant voice." (400, not retryable, nothing charged, 54
credits left). HeyGen's documentation: instant voices made before the new model "must be cloned again before they can
speak here"; for the closest match it suggests similarity "max" and expressiveness 0.5. The voice is still listed as
active, and every banked line stays usable. Do not retry, do not pass a model, do not use another voice ("MTG Real
Voice", "Musa Dumakude" and "Dr RaShon" are in the account but are not approved), and do not clone anything until MTG
says which way he wants: (a) he makes the audio himself in the HeyGen app with MTG Master Voice V2, if the app still
offers it, and sends the file; (b) a new clone of his own voice from a clean recording he supplies, tested against the
bank on one short line before any video uses it, and approved by his ear; (c) recorded lines only.
Waiting for new lines: explainer #3 (six lines, approved 10 Nov 2026) and explainer #4 (two lines, approved 9 Nov 2026).

## Standard: the site tour (video 0)

| # | Video | Where | Voice | Status |
|---|---|---|---|---|
| 0 | JetUP site tour, click by click: landing page, the JetUP hub, the menu on laptop and phone, all 13 pages, how to get back, first step | very top of the JetUP hub (/jetup/, JetUP's dashboard); listed first on the Videos page | mostly new lines (about 7 to 14 credits) or captions with recorded lines only | made last, once all pages and videos are done |

The main MTG TRIBE dashboard (mtgtribe.com/dashboard/) gets its own tour of the whole mtgtribe.com site, replacing MTG's
photo card at the top, when we do the main-site pass. Open question for MTG: JetUP has no dashboard of its own yet (its
Dashboard button goes to the main MTG TRIBE dashboard), so either JetUP gets its own dashboard like ALTRUVA, or the
JetUP tour sits at the top of /jetup/.

## Videos, first the six with the biggest impact

| # | Video | Where | Voice | Status |
|---|---|---|---|---|
| 1 | JetUP and TAG Markets: the simple picture (1:39, v3: positive close, no loss statistics) | home "Who does what", Videos page "Start here" | recorded lines only, 0 credits | live 8 Nov 2026 (v3 the same day) |
| 2 | Who does what: five names, one picture (minibus taxi), 2:08 | home "Five names", How it works "Who does what" | recorded + 10 new lines (3 credits, 8 Nov 2026) | live 8 Nov 2026 (v2: positive close, no loss statistics) |
| 3 | Amplify 24x made simple: exposure is the size you trade with, not money you own (market stall, + calculator demo), 2:01 | home "$155 in", How it works "Amplify 24x", Exposure Calculator, check 4, Videos page | recorded lines, 0 credits; 6 new lines (hook, stall, move, loss limit, calculator, recap: about 3 credits) approved by MTG on 10 Nov 2026, not recorded: HeyGen refused his voice (see "Voice") | preview sent 9 Nov 2026 (recorded lines; the hook, stall, calculator and loss limit play on screen only); not on the site until MTG approves. Sources: `tools/jetup-explainers/ex3/` |
| 4 | The 70/30 split: where every profit goes (+ calculator demo), about 2:09 | home "70%", How it works "70/30", Profit Split Calculator, Videos page | recorded lines; 2 new lines approved (about 1 credit), not recorded: HeyGen refused his voice on 10 Nov 2026 (see "Voice") | live 9 Nov 2026 with recorded lines; the 2 new lines can be added once MTG has decided how his voice is produced |
| 5 | The $100 Fast Start Promo: the money plan, claim it in 4 steps, the rules, "a promo is a promo", 2:18 | Promo page top, home "A promo is a promo", get-started part 6, Videos page | recorded lines only, 0 credits | live 9 Nov 2026 (Promo page claim list now 4 steps, like the video) |
| 6 | The partner plan: the rule most people miss | Partner plan top | new lines (about 4 to 6 credits) | planned |

## Next six

| # | Video | Where | Voice | Status |
|---|---|---|---|---|
| 7 | Send your deposit the right way (networks, bus route) | Get started part 4, FAQ | recorded; analogy new or on screen | planned |
| 8 | Getting your money out | How it works "Withdrawals", check 5, FAQ | recorded lines | planned |
| 9 | What "copying" really means | How it works, part 5 | mostly recorded | planned |
| 10 | Exposure Calculator walkthrough | Exposure Calculator | new lines | planned |
| 11 | Infinity Bonus, the 50% rule and the difference rule | Partner plan "Infinity" | new lines | planned |
| 12 | BIX Card: one wallet, one QR code | BIX Card | new lines; needs MTG's BIX link | planned |

## Chapter clips (no new narration)

- 5 Checks v5.1: one clip per check, for the Five Checks page and the home check cards. Status: planned.
- Sign-up training: one clip per part, from training v5 once MTG's screen recording arrives. Status: waiting.

## Pages without a video

Disclaimer, Downloads, the Videos page (it lists all videos), FAQ (each answer links to its explainer).

## PDF companion

Two PDFs, both waiting for MTG's tutorial video and links:
- **Getting started step by step** (reproduced from MTG's own video steps).
- **The master PDF companion** for the whole site (see the skill's `references/pdf-companion.md`).

## Facts and consistency

`tools/learning-system/jetup-facts.md` is the single source of truth for every JetUP number, step, label and rule.

## Links received (7 Nov 2026)

- JetUP Partner link from MTG: in `JETUP_JOIN` (`jetup/_build/layout.py`). Used by every "Join JetUP" button: top bar, side
  menu, phone thumb bar, home hero, get-started "Get ready", and the Join card at the end of every page except the
  disclaimer. Each carries the fair-play note (invited by someone else? use their Partner link). Preview on the working
  branch; live after MTG's approval. BIX Card link: still to come.
