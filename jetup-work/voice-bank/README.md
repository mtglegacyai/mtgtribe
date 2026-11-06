# MTG voice bank: JetUP + TAG Markets (saved 6 November 2026, with MTG's permission)

Every line MTG has approved so far for JetUP, in his approved HeyGen voice **MTG Master Voice V2**
(voice ID `3931c505632149ceb2bbfecf2778c09c`, engine `orca`). These are the exact files HeyGen produced (MP3,
44.1 kHz, mono), saved before HeyGen's download links expire. About 15 minutes, 262 sentences.

**Reuse these first.** A new explainer built only from these lines costs no HeyGen credits. New lines are made in the
same voice only when MTG approves the credits for that video (measured: 14 credits for 5,400 characters; budget about
2 credits per 500 characters).

| Folder | Files | What it is |
|---|---|---|
| `5-checks/` | `o1.mp3` (2:32), `o2.mp3` (2:51), `n1.mp3` (0:16) | 5 Checks narration (o1 = part 1, o2 = part 2), n1 = the v5 next-step and comment lines |
| `signup-training/` | `t1.mp3` (3:04), `t2.mp3` (2:32), `t3.mp3` (3:14), `t4.mp3` (0:32) | Sign-up training narration, parts 1 to 6 plus the promo and comment lines |

- `*_tts.json`: HeyGen's own response for each file, with **word-by-word timings** (`word_timestamps`) and the request ID.
- `5-checks/*_words.json`: word timings measured in the audio itself (forced alignment); use these for the 5 Checks takes.
- `*-spoken.txt`, `t*_tagged.txt`, `t4.txt`: the exact scripts that were sent to HeyGen.
- `sentences.tsv`: every sentence, with its file, start and end time in seconds. Search it for the line you need.

## Cut one sentence (example)

```bash
ffmpeg -ss 7.80 -to 9.95 -i 5-checks/o1.mp3 -af "afade=t=in:d=0.02,afade=t=out:st=2.10:d=0.05" line.wav
```

Leave about 0.05 s before the first word and 0.15 s after the last one, and join lines on natural pauses.

## Topics already covered (good for explainers)

- The simple picture: JetUP, TAG Markets, CopyX, Sonic AI, XAU/USD (5 Checks part 1)
- 70/30 split, $10 to $7, no fee on a loss (5 Checks part 1)
- Who holds my money, regulators and warnings, Myfxbook track record (5 Checks)
- Exposure: $150 + $100 promo, x24, $6,000; $50 to $1,200 and $200 to $4,800 (5 Checks part 2, training)
- Loss limit 10%, 5% with a community token; leverage warning (training)
- Withdrawals and the promo rules, start small, small test withdrawal (5 Checks part 2, training)
- Partner link vs Client link, sign-up, KYC, deposit network and amount, Sonic AI codes, CU number, promo claim (training)
- Closing lines: mtgtribe.com/jetup, mtgtribe.com/group, Telegram, save and share, "It pays to pay attention, and take action"

Not covered yet (needs new lines): the partner plan (levels, lot commission, Infinity, Global Pool, rewards), the BIX Card,
and the calculator walkthroughs.
