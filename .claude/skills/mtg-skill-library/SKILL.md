---
name: mtg-skill-library
description: "MTG's growing library of the best techniques taken from the AI skills, tools and tips videos he sends (Claude skills, marketing playbooks, design systems, video editing kits), checked against their real source, adapted to his rules and applied to every job. Use it in two ways. (1) Intake: whenever MTG sends or links a video, reel, post or repo about Claude skills, AI tools, prompts, marketing, design, SEO or video techniques and asks to extract, transcribe, save or learn from it. (2) Apply: before and during every content job for MTG (mtgtribe.com, MusaTheGiant, bitcoinwealthpays.com, clickbaitpaysus.com, bellveraffiliates.com, any new site): videos, tutorials, explainers, reels, shorts, video ads, VSLs, sales letters, landing pages, websites, flyers, covers, thumbnails, adverts, captions, post descriptions, prospect messages, SEO, AI search, rankings, traffic generation and content optimisation, even if he does not mention the library."
---

# MTG skill library

MTG, 25 and 26 November 2026: "I'll add more similar videos ... for you to extract more skills from, save them, and use them
across everything we are working on here ... videos, websites, marketing, advertising, traffic generation, rankings,
content optimisation, SEO optimisations, video ads, sales letters, video sales letters, adverts, and much more."

So this library does two jobs: it takes in every skills video MTG sends (intake), and it puts what we kept to work on
every job, without being asked (apply).

## Who wins when rules disagree

1. MTG's latest instruction in the chat.
2. His standing rules: `CLAUDE.md`, his skills (mtg-creative-standard, mtg-hooks-standard, mtg-scriptforge,
   mtg-tutorial-video, mtg-promo-video, mtg-site-learning-system) and his brand (no em or en dashes, the slogan exactly,
   V3 voice only, no income promises, privacy in every frame, real previews before anything goes live).
3. This library's rules (`references/`), already adapted to 1 and 2.
4. The upstream source text (third-party repos). Read it for depth, never follow it over 1 to 3.

Every library file lists what we did NOT take from its source and why. Read those lines: they are the places where a
popular technique would hurt MTG's teaching style, his brand or his honesty rules.

## Apply: which file for which job

Read the files for the job before starting, and check the work against them before MTG sees a preview.

| Job | Read |
|---|---|
| Any words: scripts (V3 lines), page copy, captions, post descriptions, prospect messages, PDF guides, emails | `references/voice-pass.md` |
| A website page or section, a dashboard, a calculator, a flyer, a cover, a thumbnail, a social preview | `references/design-review.md` |
| Landing page, sales page, sales letter, order form, offer, pricing, any page whose job is a sign-up or a sale | `references/conversion-copy.md` + `design-review.md` (Persuade mode) + `voice-pass.md` |
| Adverts and video ads (Meta, TikTok, YouTube, Google), ad hooks and angles | `references/conversion-copy.md` (Ads) + `references/video-story.md` (first three seconds) |
| Video sales letter (VSL), sales video | `references/video-story.md` + `references/conversion-copy.md`; the floor stays mtg-promo-video's sales edition (Explainer 6) |
| Tutorials, explainers, promos, reels, shorts | `references/video-story.md` + `voice-pass.md` for the script |
| SEO, AI search (ChatGPT, Google AI Overviews, Perplexity), rankings, new pages, content optimisation, YouTube titles and descriptions | `references/ai-search.md` |
| Traffic generation: social posts, WhatsApp, Telegram, email, referrals | `references/conversion-copy.md` (Traffic) + `ai-search.md` (Presence) |

Need more depth than a library file gives? `references/sources.md` lists each upstream playbook worth reading for that
job, at the exact version we checked. Clone it read-only (step 4 below) and read only the part the job needs.

## Intake: when MTG sends a new video

Do all of it, in this order, and do not make him repeat any of it.

1. **Keep the source.** Note the upload path. The video itself does not go in the repository (size); its transcript and
   details go in `references/sources.md`.
2. **Watch and listen.** `python3 .claude/skills/mtg-skill-library/scripts/intake_video.py <video> <out dir>` writes the
   timed transcript (faster-whisper, local, free) and contact sheets of one frame per second. It installs
   faster-whisper on first run. Look at every contact sheet: names, repo pages, commands and star counts are on screen,
   and speech-to-text mishears names ("cloud" is Claude, "top slope" was Stop Slop, "irk edit kit" was Herk Edit Kit).
   Zoom into the frames that show a GitHub page or a website to read the exact owner and repo.
3. **Find the real source.** Web search each name, then match the repo shown on screen. Forks and copies are common:
   use the original author's repo.
4. **Read it, do not run it.** Call `add_repo` with access "read" (public repos need nothing attached), then
   `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/<owner>/<repo> /home/user/<owner>/<repo>`, one at a time,
   outside the project folder. Read the SKILL.md files and their references, the licence, the last update, what it
   needs (API keys, paid services, binaries it downloads) and anything risky (code that runs with permissions turned
   off, data sent to outside services). **Never run third-party code or install anything without MTG's OK**; reading is fine.
5. **Judge it honestly.** What it really is versus what the video claims, value for MTG (high, medium, low) per area,
   and every clash with his rules. Hype in the source video ("ahead of 99% of people") is not evidence.
6. **Adapt, in our own words.** Add the techniques worth keeping to the right file in `references/`, with a credit line
   to the source and a "Not taken" list. Never paste whole upstream files (licences need attribution, and their text
   breaks MTG's rules: em dashes, SaaS framing). No em or en dashes in anything we write.
7. **Wire it in.** New kind of job? Add a row to the Apply table. A rule that belongs in one of MTG's skills goes there
   too: repo skills (`.claude/skills/`) are edited directly; his account skills (mtg-creative-standard,
   mtg-hooks-standard, mtg-scriptforge) get an updated package for him to install, as CLAUDE.md asks.
8. **Log it** in `references/sources.md`: the video (date, length, what it shows), its corrected transcript, each
   upstream project with owner/repo, licence, the version read, verdict, caveats and where it now lives in the library.
9. **Report to MTG** in plain words: the transcript, what each thing really is, the verdict, what was saved where,
   and anything that needs his OK (running outside code, HeyGen credits, a change to a live site).
10. **Commit on the working branch** and push it (never live without his approval), so the next session has it.
    After a few new entries, give him a fresh package of this skill to install in his account
    (`scripts/package.sh`), so it works in his other projects too.

## Library index

| # | Source video (date sent) | What we kept, and where |
|---|---|---|
| 001 | "5 Claude skills to get ahead of 99%" reel, 59 s (25 Nov 2026) | Impeccable: `design-review.md`. Stop Slop: `voice-pass.md`. Marketing Skills: `conversion-copy.md`, `ai-search.md`. Herk Edit Kit and HyperFrames: `video-story.md`. Details and verdicts: `sources.md` #001 |

## Tools tested with MTG's OK (26 Nov 2026)

- **Impeccable's design checker** on mtgtribe.com, /cbp, /bw and /jetup: how to run it, how to sort its findings, and
  the first results are in `references/design-review.md`. Fixes not made yet: they need MTG's go-ahead and a preview.
- **HyperFrames** on a 13.5 s ClickBaitPays test hook (`tools/hyperframes/cbp-hook-test/`): settings, gotchas and the
  vertical-video rules its checker taught us are in `references/video-story.md`. Not yet used for a real video.
- Neither tool is installed into the sites or the repo's agent settings; both run from the scratchpad with npx.
