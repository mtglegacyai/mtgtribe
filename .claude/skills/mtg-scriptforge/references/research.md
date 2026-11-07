# Research before every video

MTG, 7 November 2026: "Do thorough research with each and every single video. Find similar videos that are getting
enormous traffic on different platforms, learn from them, and make ours much better. Don't make a video for the sake of
making a video."

No script is written until the research brief exists. Research is how a video earns its place: proof that people want
it, what already works, what the winners get wrong, and exactly how MTG's version will be better.

## Learn from the winners, never copy them

Copy the **pattern**, never the **property**. Study what makes the top videos work (the hook pattern, the format, the
pacing, the length, the kind of visual, the thumbnail pattern, the question that fills the comments) and build an
original video in MTG's voice and look that does it better. Never copy their script, wording, footage, music,
thumbnail, characters or distinctive layout, and never re-upload anyone's video (mtg-creative-standard section 18).

## 1. Demand and benchmarks (5 to 10 videos for a long video, 3 to 5 for a Short)

- **YouTube (real numbers):** run `scripts/yt_research.py` in this skill with 3 to 5 searches: the topic, the hook
  format ("what if prices doubled every day"), the object ("100 trillion dollar note") and the broader idea
  ("hyperinflation explained"). It lists views, age, length and views per month, highest first. Run it gently (a few
  searches per video). If YouTube limits requests, say so; never guess a number.
- **TikTok, Instagram, Facebook, X:** web search for viral posts on the topic and the format; use links MTG sends; use
  Metricool for MTG's own accounts when it is connected. These platforms rarely show numbers to search engines, so
  record what could be checked and mark the rest "not verified".
- **Thumbnails:** download the top thumbnails (`https://i.ytimg.com/vi/<video id>/mqdefault.jpg`), tile them into one
  sheet and look at them: the hero object, the number, the words, the face, the colours.
- **Fresh vs evergreen:** views per month shows what is hot now; total views shows what lasts. A topic with old giants
  and no fresh, high-quality version is an opening.

## 2. What wins, what is missing

From the benchmarks write down:

- **Hook patterns** in the winning titles and thumbnails (a number, a superlative, "day 1", a mystery object, a face).
- **Length** of the winners for this topic, by platform.
- **Format** (explainer, challenge, story, countdown, myth buster).
- **The gap:** what they get wrong or leave out (out of date, wrong facts, hype, no African or South African angle,
  unclear visuals, no honest risks, no "what this means for you today", no conversation in the comments).
- **What viewers ask for:** questions and complaints in comments where they can be read.

## 3. The "better than" plan

At least five specific, checkable ways MTG's video beats the benchmarks, for example: verified facts with sources, a
fresher year, a local angle, a clearer visual for every idea, a stronger hook that pays off, the interaction layer,
MTG's warmth and honesty, a real next step. Then decide the length, title and thumbnail from the evidence, not habit.

## 4. Facts

Every fact in the script comes from a reliable source (official bodies, central banks, academic papers, reputable
news, museums, the protocol's own documents). List them in the brief. If sources disagree, say so in the script or
leave the fact out.

## 5. The research brief (save it with the video's files)

```
# Research brief: [working title] ([date])

Job: [goal], stage [stage], platforms [list].

## Demand
Searches run and what they show (total views, views per month, freshness).

## Benchmarks
| # | Platform | Title | Creator | Views | Age | Length | Why it works | Link |

## Thumbnail patterns

## The gap

## Our "better than" plan (5 or more points)

## Decisions
Length, title (+ 2 test titles), thumbnail concept (A and B), hook, interaction prompts, main address.

## Facts and sources

## Limits of this research
What could not be checked (for example TikTok numbers), and the research date.
```

Save it next to the script in the site project's video folder (in mtgtribe: `tools/videos/<number>-<slug>/research.md`).
Website repositories are public: strategy MTG wants private goes to his Google Drive instead.

## 6. Craft before production

Research feeds the craft. Before MTG sees a script:

- Write 5 hook options, pick the strongest against the benchmark hooks.
- Write 3 titles and 2 thumbnail concepts (one for an A/B test).
- Read the script aloud for rhythm; cut every line that does not teach, hold attention or move the viewer forward.
- Check the visual plan: something meaningful changes on screen every few seconds in a Short and at every new idea in
  a long video, with one focal point at a time.
- Check every fact against the brief.

After publishing, compare the video's numbers with the benchmarks (engagement playbook section 8) and feed what you
learn into the next brief.
