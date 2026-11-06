# Auditing a site for explainer videos

The goal is a short, ranked list of explainers that would most improve understanding and conversion, plus the free
options, so MTG can pick one video at a time. A long list of "nice to have" videos is worse than a sharp list of the
few that matter.

## How to scan

1. List every page (the site's sitemap or every `index.html`), and for each page list its sections (each `h2`, with its
   `h3` items), its word count and the videos it already has. A quick script over the built HTML does this in seconds.
2. Read each section's actual text, not just its heading. The question for each section is: would seeing this
   explained, in MTG's voice, make a visitor understand it faster or act on it sooner?
3. Check what already exists: approved videos (which can be cut into chapter clips for free), the voice bank (which
   topics are already recorded), and MTG's step-by-step tutorial recordings (real screens to show).

## What earns an explainer (strongest first)

- **The first impression:** the page a visitor lands on first needs a 60-second "the whole thing in one picture" video.
  Most visitors will not read 2,000 words; they will watch a minute.
- **Relationships between several parties:** who holds the money, who trades, who runs the community. Confusion here
  stops people from joining, and an animated picture (arrows, connectors, little people) fixes it fast.
- **Numbers and money flows:** splits, percentages, leverage or exposure, fees, compounding, level structures. Moving
  numbers on screen ($10 becomes $7 and $3) beat any table.
- **Risk mechanics:** loss limits, leverage, what can go wrong. Showing the risk honestly builds the trust that converts.
- **Rules that change the outcome:** promo conditions, qualification rules, deadlines, "the rule most people miss".
- **Costly mistakes in a step:** wrong network, wrong link type, wrong order of steps. A 45-second "do it this way"
  video prevents lost money and lost sign-ups.
- **The business case for team builders:** the partner or compensation plan, shown as levels opening and incomes
  stacking, with "what a partner earns can be zero" said out loud.
- **Every calculator or tool:** a short walkthrough of the real tool with the visitor's own kind of numbers.

## Always on the list

- **The site tour** at the very top of the dashboard (see `site-tour-video.md`): a standard item on every report, made
  last, once the pages are finished. Put it in the report as video 0.

## What does not need one

Legal and disclaimer pages, the downloads page, the videos library page (it will list the new videos) and the FAQ
(link each answer to its explainer instead). Do not make a video that only repeats another video; fold it in.

## Free options to always include

- **Chapter clips:** cut each approved long video (for example a 5-checks video or a sign-up training) into one clip
  per chapter and place each clip in the matching section. No new voice, no credits.
- **Videos built only from recorded lines:** say which planned explainers the voice bank already covers.

## Report format (MTG reads it on his phone: headed lists, no wide tables)

```
# Explainer videos for <site>: <N> videos plus <M> sets of chapter clips (nothing made yet)
One line: every video is 16:9, 60 to 90 seconds, in the laptop frame, ending with a call-to-action card.

## First: the <k> with the biggest impact
**1. <Video title>**
- Where: <page and section names, exactly as on the site>
- What viewers see: <the visual story: objects, icons, numbers, analogy, where the picture stops>
- Why: <the understanding or conversion problem it solves>
(voice: reused lines / new lines, with credits, goes in the voice section below)

## Next: <more videos, one or two lines each>
## Chapter clips (no new narration)
## Pages I'd leave without a video (and why, one line)
## Your voice and HeyGen credits (which videos are free, which need new lines, the estimate, last known balance)
## What I need from you (links, permissions, your first pick)
```

Keep MTG's words for things (the names on his pages, his analogies), lead with the answer, and end by asking which video
he wants first. Do not start producing until he answers.
