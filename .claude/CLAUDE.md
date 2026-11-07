# Notes for Claude: mtgtribe.com (MTG 👑 | Your Digital Architect)

Brand rules live in MTG's "mtg-creative-standard" skill. No em or en dashes anywhere. Never publish or push live
without MTG's approval. Slogan, exactly: Let's Get This Crypto! 💪

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

## Standing rule: MTG's profile photo is always a circle (MTG, 7 November 2026)

"Always put my profile picture in a circle, not in the current shape." In every video, page, thumbnail and graphic,
MTG's profile photo is shown in a circle with a gold gradient ring and a soft gold glow. This replaces the square with
rounded corners in section 10a of the mtg-creative-standard skill. Everything else in 10a still applies: use the whole
photo (face, mtgTribe.com t-shirt print and sign visible, never a zoomed face-only crop), show it large and make room
in the layout, and use the small face crop only for the tiny brand bar icon. Reference code: `PhotoCard` in
`tools/video3d/src/components/PhotoCard.tsx`. Python pipelines that use `brand/photo_card.py` (brand-assets branch)
need the same circle before their next render.

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

## 3D video studio (MTG, 7 November 2026)

**Length (MTG, 7 November 2026): every video is a vertical Short of at most 60 seconds** ("I like the short videos
more, up to 1 minute, and not longer"). No long videos unless he asks.
**Music (MTG, 7 November 2026): only the last line of his theme "They Call Me MTG", "Let's get this crypto, wherever I go!" (about 3 s),
right after his last word, ending with the video ("Don't play the entire theme song, just only play
the very last few seconds"). No other music anywhere. Code: `ClosingTrack` plays it by default and `closingTail()` in
`src/brand.ts` sizes the end card for it.

**House format (MTG, 7 November 2026): the format of video 01 as he posted it** (`src/compositions/whatif01/`,
composition `WhatIf01-9x16`, file `out/whatif01-v6-9x16.mp4`): gold-and-black scenes with 3D card entrances and a slow
camera push-in, Leo in gold windows, word-by-word captions, soft sound effects fitted to the story, his theme at the end,
the mtgtribe.com card and a designed cover. It renders in about 20 minutes. The full Three.js version
(`WhatIf01-3D-9x16`, `scenes3d.tsx`) was stopped at MTG's request ("takes too long to make"): do not use full Three.js
scenes for whole videos unless he asks; small 3D touches are fine when they render fast.

3D animated videos are made in `tools/video3d/`: Three.js (React Three Fiber) inside Remotion, which handles the
timeline, captions, audio and rendering. Read `tools/video3d/README.md` first. In cloud sessions there is no graphics
card: render with `REMOTION_GL=swangle`. Animate from `useCurrentFrame()`, never the clock. Captions come from the final
audio (`scripts/transcribe.py`). Same rules as every video: approved voice only, MTG's full photo, his theme's last line at the
very end, preview before anything is published. Every video gets sound effects from the **soft palette** made in
code (`scripts/make_sound.py`; `check` must say "all soft"; MTG: "soft, interesting ... not the ones that almost hurt the
ear"), never louder than his voice and **chosen to fit each video's story** (new soft effects are designed when a moment
needs one; MTG: "do not just use one and the same sound effects, even if they do not fit"), but **no background music
under the video** (MTG, 7 November 2026: the music bed was "too loud, I don't like it. Remove it completely"): only his
theme's last line at the end (see Music above). Videos are vertical Shorts of at most 60 seconds.
**Every video sends people to mtgtribe.com, never to the WhatsApp group link** (MTG, 7 November 2026: WhatsApp can
suspend accounts, the website is always there and links to his socials and the tribe); say what they will find there
(tutorials, explainers, honest guides to multiple income streams, risks included).
**The greeting names the real type of each video** (MTG, 7 November 2026): "Thank you for taking the time to watch this
video / tutorial / explainer video / guide / training ...", chosen per video ("training" only for a real training); reuse
the voice bank's recorded greeting with the right word before spending credits.
**Every video comes with a designed cover** (MTG, 7 November 2026): a 9:16 PNG safe for the 3:4 profile-grid crop, embedded in the MP4 as cover art and handed over with the video, so he can
attach it when posting. MTG is not sure how to update a skill: when he approves a change, rebuild the upload file
and walk him through uploading it to his claude.ai account, one step at a time.

## Video ideas and scripts: MTG ScriptForge (MTG, 7 November 2026)

**Daily video (MTG, 7 November 2026):** when MTG says "let's create today's video", run the routine in
`.claude/skills/mtg-scriptforge/references/daily-video.md` end to end: next hook format in the rotation (Did You Know,
What If, What Everyone Ought to Know About, ...), a fresh topic from his niche, research, script, voice, house format,
cover, posting pack, preview. The log of videos is `tools/videos/README.md`. MTG pre-approved up to 5 HeyGen credits per
daily video for the voice (7 November 2026); new Leo clips and anything more still need his yes.

MTG's ScriptForge prompt, adapted to his niche, is the skill `.claude/skills/mtg-scriptforge/`: niche menu, 10 ideas,
full script with visual and build cues, Shorts plan. Bridge topics (self-improvement, psychology, What If, science,
history) pull in new viewers and end on the MTG TRIBE; his own niche sends people to the right page
(`references/destinations.md`). It works for ALL his websites (MTG, 7 November 2026): the account version bundles the
3D studio as `kit/video3d/`, which installs into any site's project. After changing the skill or `tools/video3d/`,
rebuild the upload file with `python3 tools/skills/package_skill.py mtg-scriptforge` and give MTG the new
`tools/skills/dist/mtg-scriptforge.skill` to upload to his claude.ai account.

**This is MTG's business (MTG, 7 November 2026).** Every video gets a job (reach, engagement, traffic, leads, sign-ups
and sales, team or tribe growth), an interaction layer (questions, guesses, votes, takeaways, share prompts), the right
website address at the right moment, the right length, and a posting pack. Method:
`.claude/skills/mtg-scriptforge/references/engagement-and-conversion.md` and `references/posting-pack.md`. The same
rules are section 5a of the updated mtg-hooks-standard (upload file in `tools/skills/dist/`). On-screen site in videos:
mtgtribe.com (the 3D brand bar can show another site's address for a video about that site).

**Research before every video (MTG, 7 November 2026: "don't make a video for the sake of making a video").** No script
without a research brief: the similar videos winning big on YouTube, TikTok and Instagram with real numbers
(`.claude/skills/mtg-scriptforge/scripts/yt_research.py` for YouTube), what wins, the gap, at least five "better than"
points, verified facts. Learn the pattern, never copy the property. Briefs and scripts live in `tools/videos/<nn>-<slug>/`.

**Platform compliance for every video (MTG, 7 November 2026: "I don't want my videos banned or removed, or my channels
shut down").** Every video passes the gate in `.claude/skills/mtg-scriptforge/references/compliance.md` (scan with
`scripts/compliance_scan.py`, human check, platform labels). Social platforms carry education, trust and the tribe;
compensation plans, recruitment, sign-up links into programs that pay from recruiting, returns and paid draws (for
example ALTRUVA's plan and Lucky Tickets, JetUp's partner plan and promo) stay on MTG's websites and in the WhatsApp
tribe. MTG's HeyGen voice is synthetic: switch on the AI label on YouTube, TikTok and Meta. Never promise a video is
"100% safe"; say what was checked.

**MTG's mascot: Leo (MTG, 7 November 2026).** An original lion named Leo, in MTG's evolution t-shirt, round gold glasses and a gold
watch, in a black-and-gold studio. Design rules, HeyGen asset IDs and the clip recipe: `.claude/skills/mtg-scriptforge/
references/mascot.md` (reference picture in the skill's `assets/`). About 15 credits per 8-second clip: 4 to 6 per
long video, ask MTG before a batch. Never the spiky orange tuft (too close to a famous film lion).
