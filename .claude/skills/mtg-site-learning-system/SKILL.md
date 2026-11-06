---
name: mtg-site-learning-system
description: "MTG's learning and conversion system for every one of his websites: audit every page and section for short horizontal explainer videos, plan each video around his approved voice with the fewest HeyGen credits (reuse his recorded lines first), turn his step-by-step tutorial recordings into clips, open every dashboard with a click-by-click site tour video, and finish each website with one ultimate PDF companion guide whose tappable buttons link to the pages, the videos and his referral sign-ups. Use this whenever MTG (MusaTheGiant, mtgtribe.com) is building, finishing, upgrading or double-checking a website or a section of one (JetUP and TAG Markets, ALTRUVA, Canton, Bitcoin Wealth / bitcoinwealthpays.com, ClickBaitPays, Bellver Affiliates, MusaTheGiant.com or any new site), or asks which sections need explainer videos, wants explainers or tutorial clips made, wants a PDF guide for a site, or talks about turning a site into a 24/7 educating and converting machine, even if he does not name this system."
---

# MTG's website learning system

MTG's websites exist to educate first and convert second: a visitor should understand the opportunity from every
direction, see it explained visually in his voice, and then take action through his referral links. MTG and most of
his visitors learn best by seeing: icons, emojis, little people, connectors, drawings, movement and sound effects, with
his warm voice explaining one idea at a time. This skill is the process that turns a finished website into that
system. Apply it together with MTG's two standing skills: **mtg-creative-standard** (voice, music, visuals, brand,
preview and approval rules) and **mtg-hooks-standard** (hooks, curiosity and calls to action). If they conflict, his
latest instruction in the chat wins, then mtg-creative-standard.

## Ground rules

- **One website at a time.** Finish and polish one site before starting the next. Never change several sites in one go.
  Later, come back to the finished ones and check they have the full system (see "Sites to revisit").
- **Plan, then wait.** Never produce a video, buy HeyGen credits' worth of speech or publish anything until MTG has read
  the plan, picked the video and supplied the links it needs. One video at a time.
- **His links make it a converting machine.** Every video's end card, every page button and every PDF button should
  carry MTG's own referral or partner link for that step. If a link is missing, ask for it; never invent one and never
  use someone else's.
- **Honest, never hype.** Show the risks, the rules and "where the picture stops" for every analogy. No income promises,
  no fake balances, no "best ever". Hide personal data in every frame.
- **Brand:** MTG 👑 | Your Digital Architect. Slogan exactly "Let's Get This Crypto! 💪". No em or en dashes anywhere,
  including inside videos, PDFs and file names. Follow each site's own content rules (names or brands MTG has ruled out).
- **Every dashboard opens with a site tour.** The very top of each website's dashboard is a video that shows visitors
  around the whole site, click by click, from the landing page to the dashboard and every page.
- **Never publish or push live without MTG's approval**, and show a real preview first (a phone recording or the
  rendered file), not a description.

## The workflow

### 1. Audit every page and section
Read `references/audit.md`. Scan every page of the site and every section on it, rank where a short explainer would
most improve understanding and conversion, and write the report in the format given there. Include the zero-new-voice
options (chapter clips cut from approved videos) and the pages that should stay without a video. Send MTG the report
and stop there.

### 2. Voice plan for each video
Read `references/voice-and-credits.md`. Search the site's voice bank for lines MTG has already approved and build as much
of each script from them as possible, because reused lines cost no credits. State plainly, per video, which lines are
reused and which would be new, with a credit estimate, and let MTG decide. Never use any voice other than his approved
one, and never claim to have a copy of his voice that can say new words: new words always need a new speech request.

### 3. Storyboard, build, preview
Read `references/explainer-video-spec.md`. Storyboard first (what is seen on every spoken idea), then build, then check
the finished file yourself before showing MTG. Use his step-by-step tutorial screen recordings as real footage inside
the explainers wherever a real screen makes the point stronger, and cut each tutorial into chapter clips.

### 4. Put it on the website
Horizontal videos play in the laptop frame, vertical ones in the slim phone frame, and the player closes itself when
the video ends (MTG's standing video rule). Place each explainer beside the section it explains, add it to the site's
videos page and downloads list, give it a poster and structured data (VideoObject), and link each FAQ answer to its
explainer. Then run the site's checks, including the sideways-scroll check (`tools/qa/hscroll.js` in mtgtribe.com):
nothing on the site may scroll sideways on a phone.

### 5. The site tour at the top of the dashboard (standard on every website)
Read `references/site-tour-video.md`. Once the pages are finished, record the real site and make the click-by-click
tour: landing page, dashboard, menu (laptop and phone), every page and its key button, how to get back, and the first
step. It goes at the very top of the dashboard, is listed first on the videos page, and is re-recorded whenever the
navigation changes.

### 6. The ultimate PDF companion (last step for each website)
Read `references/pdf-companion.md`. When the site and its videos are done, build one PDF for visitors who prefer PDFs:
enough content to understand everything, mostly short summaries, and tappable buttons on every page that open the
matching web page, the explainer video and MTG's sign-up links. Check every link with
`scripts/check_pdf_links.py` before showing MTG. Add it to the site's downloads page once approved.

## Keep a plan file in each site's repository

Track the system for each site in `tools/learning-system/PLAN.md` inside that site's repository: the ranked video list,
the status of each (planned, voice approved, storyboard, preview sent, approved, live), the links MTG has supplied and
which are still missing, the voice bank location, and the PDF status. Update it whenever something changes, so the next
session picks up exactly where this one stopped.

## Sites to revisit later

When the current site is done, the next one gets the full treatment in the order MTG chooses. Finished sites to
double-check afterwards: Bellver Affiliates, ALTRUVA (mtgtribe.com/altruva), Canton Weekly and the CC and CNTN guides,
the MTG TRIBE home and dashboard, and JetUP and TAG Markets once it is complete. A revisit means: run the audit, compare
it with what the site already has (including a click-by-click site tour at the top of the dashboard; ALTRUVA's 6:29
welcome tour is a map of the site and may need real click-by-click screens added), and report the gaps before
changing anything.
