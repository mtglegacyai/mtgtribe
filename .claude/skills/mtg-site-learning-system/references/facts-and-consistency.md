# Facts, outside sources and consistency

MTG's rule (7 Nov 2026): "We do not want conflicting information, conflicting content, conflicting videos." Every site
keeps one facts register, and everything (pages, video scripts, tutorial clips, PDFs, promos) agrees with it.

## The facts register

- File: `tools/learning-system/<site>-facts.md` in the site's repository (JetUP: `jetup-facts.md`).
- One table per topic. Each row: the fact, the exact wording to use, where it is used, and the source.
- Words and names section: pronunciation in scripts (for example "Jet Up" said as two clear words, written JetUP),
  brand names, and the words MTG does not use ("downline", "recruits").
- "Open questions for MTG": every conflict you cannot settle yourself. Do not publish an answer until he confirms.
- "Never import": what outside material must never bring onto the site.
- A source log with dates.

When a fact changes: update the register first, then every place in "Used in", then run the consistency check.

## Outside trainings, transcripts and presentations

MTG sends recordings or transcripts of other people's trainings (uplines, company calls). Treat them as a source of
practical steps, never as gospel:
1. List every concrete step, label, number and rule in it.
2. Compare each with the facts register and the site. Mark it: matches, new and useful, conflicts, or exclude.
3. Add the new and useful ones in plain words, attributed where the figure is someone else's (for example "as shown in a
   JetUP partner presentation, November 2026; confirm in your partner account").
4. Put conflicts in "Open questions for MTG". MTG's own recordings and the company's own documents win over a presenter.
5. Never import: income projections or spreadsheets, other people's earnings, advice on how much to deposit, top up or
   compound, advice on hiding money from banks, unverified company claims, other people's names, hype.
6. Do not store raw transcripts with people's names in a public repository: keep a short summary in the source log.

## The consistency pass

Run it before every publish, and always after MTG supplies a new tutorial video, explainer, PDF or link:
1. Grep the page builders for the key numbers and labels (the command lives in the facts register).
2. Read every video script (voice bank sentences), clip and PDF page against the register.
3. Watch for: amounts, percentages, time limits (30 days, 12 months, one month minimum), button labels, codes, network
   order, step order, rules for promos and withdrawals, and pronunciation.
4. Fix what disagrees, or list it under "Open questions". Report the result to MTG in a short list.

## When MTG's own step-by-step tutorial video arrives

His own recording beats every other source. Update the register from it, then: chapter clips beside the matching steps,
the Getting started PDF reproduced from his steps, the master PDF companion, and a full consistency pass. Preview, then
publish only with his approval.
