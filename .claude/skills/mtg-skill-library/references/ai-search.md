# AI search and SEO: get found on Google, YouTube and in AI answers

Use for every new or changed page, every YouTube title and description, FAQs, watch pages, and any work on rankings,
traffic or content optimisation. MTG's 17 and 18 Nov 2026 rules already ask for this on every job (titles, descriptions,
structured data, FAQ answers, internal links, sitemaps, a page of its own for every video). This file is how.

Source: the ai-seo playbook in Marketing Skills by Corey Haines (MIT, `coreyhaines31/marketingskills` at
8fd2fcade2fd), including its YouTube citations reference. Numbers below are from the studies it cites; treat them as
direction, not promises.

## How AI answers choose sources

ChatGPT, Google AI Overviews, Perplexity, Claude and Gemini lift **passages, not pages**. A key claim that stands on its
own gets quoted; one buried in a long story does not.

## Pillar 1: structure, so a passage can be lifted

- **Lead every section with the direct answer**, then explain. Keep the answer itself short (about 40 to 60 words is a
  common rule of thumb).
- **Headings in the words people type or say:** "How to buy Canton Coin step by step", "What is Bitcoin Wealth?",
  "ClickBaitPays vs paid ads".
- **Use the block that fits the question:** a definition for "What is X?", numbered steps for "How to X", a comparison
  table for "X vs Y", pros and cons for "Is X worth it?", an FAQ for common questions, a figure with its source and date.
- One idea per paragraph. Tables beat paragraphs for comparisons; numbered lists beat paragraphs for steps.
- **Don't chop pages into fragments "for AI"**, and don't write a second version of a page for AI. Google says both hurt.
  The same page serves people and machines.

## Pillar 2: authority, so it gets trusted

The Princeton GEO study (KDD 2024) measured what lifts visibility in AI answers: quotations from named people (+41%),
statistics with sources (+31%), fluent, readable writing (+28%), citing sources (+27%), clear explanations (+14%).
Keyword stuffing made it worse (-8%).

For MTG that means:

- Facts with their source and date (an on-chain figure with the link to check it, the programme's own terms).
- MTG's first-hand experience, said plainly ("I joined in ...", what he did, what he saw). That is the experience part of
  Google's E-E-A-T, and nobody can copy it.
- A visible "Last updated" date, and a refresh when facts change.
- Never invented reviews, awards, citations or "independent" sites; they break Google's policies and trust.

## Pillar 3: presence, being where AI looks

- **YouTube is cited often by Google's AI Overviews, but models read the text, not the picture.** For every video:
  1. Speak the key answers as complete sentences, and say the important names out loud (ClickBaitPays, Bitcoin Wealth,
     JetUP, MTG). A word that is only on screen may never be seen.
  2. Upload corrected captions (names spelled right), never leave messy auto-captions.
  3. Title shaped like the question or task ("How to ..."), branding after.
  4. Chapters titled by the sub-questions people ask.
  5. A description that restates the key points as text: a short summary, what's covered, then the links (in MTG's
     label, blank line, 👉 link layout).
  6. A pinned comment with the answer in numbered steps and the key links.
  7. The thumbnail earns the click (`tools/youtube-thumbnails/`); the text earns the citation.
- **Say the same thing about MTG everywhere.** AI looks for agreement between sources, so his YouTube, TikTok, Facebook,
  Telegram and site "about" lines should describe him and each guide the same way.
- Real participation only on Reddit, Quora and communities: helpful answers, never spam.

## What we already have (keep it and extend it)

Checked 26 Nov 2026: `llms.txt` on the main site, /bw and /cbp (not yet on /jetup or /altruva); sitemaps; VideoObject
structured data on the video pages (/bw, /jetup, /altruva, Canton weekly); a page of its own for every /bw tutorial
with key moments and time buttons; a social preview for every page. New sites and pages get the same from day one.

## Quick check before a page goes to preview

- [ ] Each section opens with a direct answer a machine could quote on its own
- [ ] Headings match real questions; one H1; FAQ answers short and complete
- [ ] Facts carry a source and date; "Last updated" visible
- [ ] Structured data fits the page (FAQPage, HowTo steps, VideoObject with a search `name`), listed in the sitemap
- [ ] Internal links to the page that explains each step; no orphan page
- [ ] No content hidden behind JavaScript that does not render

## Not taken, and why

- Its advice for software companies (G2 and Capterra reviews, LinkedIn articles, product-demo pages): not MTG's market.
  Read the upstream references only if one becomes relevant.
