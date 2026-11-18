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
his approved HeyGen voice "MTG Master Voice V3", which costs HeyGen credits:
ask MTG first. Without new voice lines they can be shown on screen only. Storyboard first, show a preview, never
publish without approval.

## Standing rule: how videos are shown on MTG's websites (MTG, 5 November 2026)

- **Vertical (9:16) videos** play inside a slim, premium phone frame: thin gold-titanium rim, thin black bezel,
  camera island, small side buttons. Never a cheap or bulky phone; the frame must not eat screen space.
- **Horizontal (16:9) videos** play inside a laptop frame, like the tutorials and explainers on bellveraffiliates.com.
- **When a video plays to the end, the player closes itself** (leaves full screen first) and goes back to its cover,
  like the Bellver players. Never make the viewer press close after watching the whole video.
- **And the page goes back to exactly where the visitor pressed play** (MTG, 10 Nov 2026: "as soon as the video finishes
  playing, the visitor must be automatically scrolled to the exact section where the video is at", on every website,
  new ones too). Every page with a video loads `/assets/video-return.js` (one line, no setup: it works with pop-up,
  inline and playlist players). Copy that file to any new site. Check with `tools/qa/video-return-test.js`.
- **The whole video, always (MTG, 16 Nov 2026):** "displayed in full, nothing hidden, but at the same time not too big ... even when
  they are maximized ... all the parts of the video are displayed, and the close button is still there." So, on every site:
  the screen of the frame has exactly the video's shape and the video is never cropped (`object-fit:contain`, also in full
  screen); **nothing lies on the picture** (no camera notch, no close button, no badge, no floating button, no pop-up note);
  the frame takes its size from the **visible** screen height (`svh` in the page, `dvh` in a pop-up), so the complete player
  fits under the site's top bar on any phone; the player has its **own Full Screen** (the bar with Exit Full Screen and Close,
  and the whole video in the rest), never the browser's bare one. The button always shows its words, written **Full Screen**
  (each word capitalised), on vertical and wide videos alike, "to make sure the visitor sees it, and knows what that button
  does" (MTG, 16 Nov 2026); an icon alone is not enough. Reference: the `.pl` player on /bw (`core.player()` in
  `bw/_build/build/core.py`, "VIDEO PLAYER" in `bw.css`, "video players" in `bw.js`). Check with
  `tools/qa/player-check.js` (README there): it must report 0 failures before MTG sees a preview.
- **The play button cannot be missed (MTG, 16 Nov 2026):** "position it such that it is impossible to miss ... without it being in
  the way of important content ... whether it's a horizontal or a vertical video, make sure that the play button cannot be
  missed." On a vertical cover the button sits **in the middle** of the cover, never near the bottom. So every website cover
  is drawn with a **clear band in the middle** for it (on a 1080 x 1920 cover: y 780 to 1140; headline above, characters and
  phone below, no address pill). On a wide cover it sits in the middle too, or in the clear spot the cover names (`spot`).
  Keep its pulse and rings as they are (he likes them). `player-check.js` fails when the button is not in the middle of a
  cover, not wholly on the cover, or smaller than 52 px.
- **Every video shows on the page as a horizontal cover inside a laptop frame (MTG, 17 Nov 2026):** "all the videos must have a
  horizontal thumbnail and inside a laptop frame. Even though some of the videos actually play inside a cell phone frame when
  they play, but just to save space and to make the website look smaller and easy to browse up and down ... And the ones that
  are actually vertical when they play, they must be on a cell phone when they play. As soon as it starts playing, just like
  the ones that are already in place." So, on /bw: `core.vid(code, here)` always draws the laptop (`.pl.pl-h`) with a 16:9 cover.
  A 16:9 video plays in that laptop; a 9:16 video's cover carries `data-play` and opens the pop-up's phone (`#pl-pop`), closes
  itself at the end, and the page is back at the cover. Every 9:16 video therefore needs two covers in `config.py`: `poster`
  (9:16, shown in the pop-up while it loads) and `wide` (16:9, the middle clear for the play button, every line short and
  compelling, a label a phone can read; the build stops without it). The tutorials' wide covers are drawn by
  `tutorials/wide_cover.py` in mtg-studio. On a phone the video comes right after its heading (`.two.vfirst`).
  `player-check.js` fails when a cover is not in the laptop frame, not 16:9, its button is not in the middle (unless the cover
  names a `spot`), or pressing a vertical video's cover does not open the phone.
- **A video gets found on its own from a page of its own (MTG, 17 Nov 2026):** "all the videos must be named such that when
  people ... search for anything related to Bitcoin Wealth ... these videos can actually rank all by themselves, leading to my
  Bitcoin Wealth website." On /bw every tutorial has its own page (`WATCH_PAGES` in `config.py`, `pages_watch.py`): its search
  name as the heading ("How to ..."), the video, its sections as key moments, and every step in writing with a time button
  that starts the video at that step (`data-at`; a link with `?t=97` opens it there). The words come from the tutorial's own
  build (`tutorials/chapters.py` in mtg-studio writes `final/chapters.json`): never retype them. Each video has a search `name`
  in `config.py` (structured data, video sitemap), is listed once in `sitemap.xml` on the page where it is the main thing, and
  the sitemap carries every page's pictures. A new tutorial is not finished without its page, its `name`, its wide cover and
  its social preview (`ogpages.py`; previews are named `bitcoin-wealth-<page>-preview.jpg`).
- Reference implementation on mtgtribe.com: the invite pop-up in `index.html` (`#vm`, `.vm-vid.phone` / `.vm-vid.laptop`).
  Any link with `data-invite` opens it; `data-src`, `data-poster` and `data-orient="h"` play another video in it.
- On the Bitcoin Wealth guide (/bw): a video marked `o='h'` in `bw/_build/build/config.py` (VIDEOS) is 16:9. `core.vid()` puts it in
  the laptop (`.pl.pl-h`), it plays in place, and the pop-up player becomes a laptop for it; 9:16 videos play in the pop-up's phone (`.pl.pl-v`).
  Two files are made (720p for phones, `-1080p` for screens 1200 px and wider). `hero=True` gives the pulsing play button; the
  cover's `spot` says where on the picture the button sits, and `poster` is the website cover (no address pill, room for the
  button). First use: the cartoon at the top of /bw/dashboard/ (MTG, 15 Nov 2026).

## Standing rule: a real preview is a live page on a temporary private link (MTG, 16 Nov 2026)

"Show me a real preview first ... I mean a live preview on a temporal web link." Before a website change goes live, give MTG
a private link he can open and tap through on his phone (the built pages, published as a private page only he can open). A
screen recording or screenshots are not a preview for him. For /bw: `build.render_preview()` in `bw/_build/build/build.py`;
the steps and the host's limits are in `tools/qa/README.md` ("Private preview link"). Say what differs from the real site.

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

## MTG's voice: MTG Master Voice V3 (MTG, 10 Nov 2026)

"V3 sounds better, sounds exactly like me": from 10 Nov 2026 every new line is HeyGen **MTG Master Voice V3**, voice ID
`65f1b9ff3f1e418496de5715a801e7dd` (MTG made it himself). Call create_speech with no model and no engine override, and no break
tags (V3 does not support them: one paragraph per pause, cut with the word timestamps). The older V2
(`3931c505632149ceb2bbfecf2778c09c`) is retired: HeyGen's new voice model refuses it. Everything already recorded in V2
(the voice bank, every live video) stays usable. Still ask MTG before spending credits, never use any other voice.

## MTG's social addresses (confirmed by MTG, 10 Nov 2026)

TikTok @joinmtgtribe, YouTube @mtgtribe, WhatsApp mtgtribe.com/group, **Telegram t.me/mtgtribe (@mtgtribe)**,
**Facebook facebook.com/mtgtribe**: the same on every website page and on every video end card. The older
t.me/mtgtribez and facebook.com/Musa.TheMTG are no longer used anywhere.

## Standing rule: replies to prospects (MTG, 18 Nov 2026)

When MTG asks for a message to send a prospect (WhatsApp, DM, comment reply), give it like this, every time:

- **Plain text only, in a code block** so he can copy it: no bold, no asterisks, no markdown (WhatsApp shows them as stray characters).
- **Short, no fluff, with blank lines between parts.** "People are lazy to read": explain at the basic level in a few lines,
  then let the link do the heavy lifting. One clear CTA to the most relevant page, ideally a link that opens right at
  the explainer video (for example mtgtribe.com/jetup/how-it-works/#who). Check the link is live first.
- **Always end with his signature, exactly:**

```text
Let's Get This Crypto! 💪

Crypto-Regards,
MTG 👑 | Your Digital Architect
```

Reference message (JetUP / TAG Markets / Sonic AI): "Great question 😊 / It's Sonic AI copy trading. / 1. JetUP: the community
2. TAG Markets: the broker, where your account is opened in your own name 3. Sonic AI: the AI trader you copy / Sonic AI's
trades are copied into your account automatically. You don't need any trading experience. / This 2 minute video explains
it all 👇 / https://mtgtribe.com/jetup/how-it-works/#who", then the signature.
