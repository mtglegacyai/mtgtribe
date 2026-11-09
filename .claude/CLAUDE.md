# Notes for Claude: mtgtribe.com (MTG 👑 | Your Digital Architect)

Brand rules live in MTG's "mtg-creative-standard" skill. No em or en dashes anywhere. Never publish or push live
without MTG's approval, except the weekly Canton report: since 8 November 2026 MTG wants it published automatically,
then a notification that it is live (see `tools/canton-weekly/README.md`). Slogan, exactly: Let's Get This Crypto! 💪

## Reminder for MTG (saved 5 November 2026, at MTG's request)

**Remind MTG when the time comes.** Once these income-stream websites are finished:

- Bitcoin Wealth (bitcoinwealthpays.com), still being built
- ClickBaitPays, still being built
- JetUp · TAG Markets (mtgtribe.com/jetup), coming-soon page only, full guide still to build
- Bellver Affiliates (bellveraffiliates.com) is already finished

...come back and **remake the MTG TRIBE invite video** (both the 16:9 and the 9:16 version, see
`tools/invite-horizontal/`) so it mentions **every income stream MTG has at that point**, not only the ALTRUVA
guide it mentions today. Follow the dashboard order: 1 Bellver Affiliates, 2 JetUp · TAG Markets,
3 ClickBaitPays, 4 Bitcoin Wealth, 5 ALTRUVA.

MTG wants this video upgraded every time his income streams change, so it always reflects all of them.

Planning note: today the only stream MTG names out loud is ALTRUVA. Naming the others in his voice needs new lines in
his approved HeyGen voice "MTG Master Voice V2", which costs HeyGen credits:
ask MTG first. Without new voice lines they can be shown on screen only. Storyboard first, show a preview, never
publish without approval.

## Standing rule: how videos are shown on MTG's websites (MTG, 5 November 2026)

- **Vertical (9:16) videos** play inside a slim, premium phone frame: thin gold-titanium rim, thin black bezel,
  camera island, small side buttons. Never a cheap or bulky phone; the frame must not eat screen space.
- **Horizontal (16:9) videos** play inside a laptop frame, like the tutorials and explainers on bellveraffiliates.com.
- **When a video plays to the end, the player closes itself** (leaves full screen first) and goes back to its cover,
  like the Bellver players. Never make the viewer press close after watching the whole video.
- Reference implementation on mtgtribe.com: the invite pop-up in `index.html` (`#vm`, `.vm-vid.phone` / `.vm-vid.laptop`).
  Any link with `data-invite` opens it; `data-src`, `data-poster` and `data-orient="h"` play another video in it.

## Learning system: explainer videos, tutorial clips, PDF companion (MTG, 6 November 2026)

Every MTG website gets the system in the skill `.claude/skills/mtg-site-learning-system/` (MTG can also save it to his
account so it works for all his sites): audit every section for short 16:9 explainers in his voice, reuse his recorded lines before spending HeyGen
credits, cut his tutorials into chapter clips, and finish each site with one PDF guide with tappable buttons. One website
at a time. JetUP's plan and status: `tools/learning-system/PLAN.md`. JetUP voice bank: branch `jetup-video-work`,
`jetup-work/voice-bank/`. Do not produce a video until MTG has picked it and supplied his links.
Every opportunity is landing page, then its Dashboard button, then the dashboard: the top of every dashboard gets the
click-by-click site tour video, replacing MTG's photo card where there is one (mtgtribe.com/dashboard/ today).

## Standing rule: nothing scrolls sideways on phones (MTG, 6 November 2026)

- No page, section, table, card or button may make a visitor scroll sideways on a smartphone, at normal or larger
  Android text size. MTG's phone shows pages about 360 px wide. Test 320 to 430 px, and tablets up to 1024 px.
- Tables: build them through the page builders (`phone_tables.py` labels every cell); never set `white-space:nowrap`
  on table cells or long button labels. Before showing MTG a preview, run `tools/qa/hscroll.js` (see `tools/qa/README.md`)
  and make sure it reports nothing beyond the items it lists as fine by design.

## JetUP: what happens when MTG sends his tutorial video and his links (MTG, 7 Nov 2026)

- **His step-by-step tutorial video:** cut it into chapter clips, reproduce the **Getting started PDF** from his steps, build the
  **master PDF companion**, then run a full consistency pass (every page, video, clip and PDF) against
  `tools/learning-system/jetup-facts.md`. Details: `tools/learning-system/PLAN.md`.
- **His affiliate links (JetUP Partner link, BIX Card link):** put them on every CTA across the JetUP pages, with compelling,
  honest copy, optimised for conversions and for search and AI search. Checklist in PLAN.md.
- **No conflicting content, ever.** `jetup-facts.md` is the single source of truth. Third-party trainings feed it only after
  checking; their income claims and advice never go on the site.

## Tutorial videos: the locked formula (MTG, 7 Nov 2026)

Every step-by-step tutorial video follows `.claude/skills/mtg-tutorial-video/`: greeting ("Hi, my name is MTG, Your
Digital Architect. Thank you for taking the time to watch this video", never "training"), "In this video" list, the
steps, recap, next video, fair-play sign-up wording ("tap any Join JetUP button; invited by someone else? use their
link"), signature outro. **No photo of MTG, neither inside the videos nor on the thumbnails: the official JetUP logo
takes its place** (MTG, 8 Nov 2026), for his tutorials and for promo clips such as BIX and Sonic AI. His voice and name stay. The final signature shows mtgtribe.com/jetup (or the site's
address) to the last frame. **Closing track:** videos longer than 60 seconds get the full 51-second "They Call Me MTG" under the
ending; videos of 60 seconds or less get only its last line, right after his last word (MTG, 8 Nov 2026). Do not make MTG repeat any of this.

## Standing rule: one signature standard for every video (MTG, 8 Nov 2026)

The 9:09 JetUP + TAG Markets sign-up training is the reference: "the best transitions, sound effects, animations, and even
my favourite line, We learn best when we teach others. I want consistency, professionalism, and precision across all my
videos." Every MTG video (tutorial parts, explainers, new videos) ends with that training's signature ending (save and
share, **WE LEARN BEST WHEN WE TEACH OTHERS**, IT PAYS TO PAY ATTENTION & TAKE ACTION, thank you trio, massive action,
YOU ARE THE BEST, Crypto-Regards signature, end card with the site address), uses only its four sounds (whoosh, tick, pop,
click) at its level, and its motion (pop-ins, bursts, emoji pops on key words). Tools: `tools/video-signature/` (README);
details in `.claude/skills/mtg-tutorial-video/` section 3a. Every video uses the JetUP logo disc where his photo was.

## Standing rule: explainer copy converts, it does not intimidate (MTG, 8 Nov 2026)

"Take it easy on the warnings and on the losses and negativity... I'm trying to build a business here... create videos
that are going to convert these people into action takers." In explainers and promos: no loss statistics (no "88% of
retail accounts lose money"), no "where the picture stops" scenes, no repeated warnings. Positive, encouraging copy, a
warm recap, "now it's your turn", and one clear action (tap any Join JetUP button). The risk stays in his gentle
signature reminder and the end card's small line. Still honest: no income promises, no fake balances, no "best ever".

**The same on every web page (MTG, 9 Nov 2026):** "Warnings like this are scaring the visitors and killing my conversions...
I am educating them so that they can make informed decisions." Inform, never frighten: calm, positive facts (24x Amplify
makes every move bigger, the loss limit is written down, start small, check the record yourself) in calm info notes, never
red alert boxes. No "you can lose your whole deposit", no loss statistics, no "what can go wrong" headings, no "where the
picture stops". The risk lives in one gentle footer line and the disclaimer pages.

## Standing rule: every page has its own social preview (MTG, 9 Nov 2026)

"Customize the preview thumbnail that appears when I paste any link on socials according to what the page is...
optimized for click-through rate." Every page gets its own 1200x630 `og:image`: one big headline that says what the
page gives you, one clear visual of its subject, the exact address in a pill, under 200 KB. Tools and the formula:
`tools/og/` (README). Run `python3 tools/og/check_og.py` before publishing. A new page is not finished without its preview.

## Skills: keep them growing (MTG, 7 Nov 2026)

When something takes MTG's work to the next level, update the relevant skill in `.claude/skills/` (and give MTG the updated
package to install in his account), or create a new skill and tell him. Use the skills whenever they fit, without waiting
to be asked.
