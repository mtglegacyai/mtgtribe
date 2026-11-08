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
| `zoom-invite/` | `i1.mp3` (0:58) | Invitation to the JetUP Zoom presentation of Saturday 7 Nov 2026 (times, three things you'll learn, mtgtribe.com/JetUpZoom). 1 HeyGen request, `cec59c5fafe9477290a139814981b031`. `i1_words.json`: word times measured in the audio |
| `zoom-invite/` | `i2.mp3` (0:52) | **Preferred.** Advert-paced invitation (speed 1.08, "Jet Up" written as two words so it is said the same every time, as MTG asked). Request `26549e33f21444d5952fcc755fb0a1c9` |
| `tutorial/` | `p1v2.mp3` (1:30) | MTG's own tutorial, part 1 (7 Nov 2026): "Thank you for taking the time to watch this video", "In this video" overview, step lines (real name as on ID, 12-character password, email already registered, Registration successful, IB Portal email, Email verified, log in, Account Type: Partner), the recap and the part 2 preview. Request `96b2fb486ec84a8ba1a33b16dc498b21`, about 6 credits |
| `tutorial/` | `p1v3.mp3` (0:18) | Fair-play sign-up lines (MTG, 7 Nov 2026): "If I invited you, go to MTG tribe dot com slash jet up, and tap any Join Jet Up button", "If someone else invited you, use their Partner link instead", "Invited by someone else? Use their link. This video is for every team, so feel free to share it." Request `108a7fa50fe04232a83702c53060598a` |
| `tutorial/` | `p2v1.mp3` (2:00) | MTG's own tutorial, part 2 (7 Nov 2026): "In this video" (link Jet Up to TAG Markets), overview, step lines (same email and password, scroll to the Copy X banner, Register Copy X, password, tick the three boxes, Sync successful, tick and Close, Login to Copy X, username or password incorrect tip, checks that you're human, dashboard and K Y C, the TAG Markets email, Confirm email address, Verification successful, click here, back on your dashboard), the recap and the part 3 preview. Request `2e3c390e2b494680b8612363fd53ea4a`, about 7 credits |
| `tutorial/` | `p3v1.mp3` (2:25) | MTG's own tutorial, part 3 (8 Nov 2026), KYC: "In this video" (verify your identity on TAG Markets), overview, step lines (upload documents, Continue, country, Sumsub ID email and Start verification, the 6 digit code and never share it, consent and Create my account, Sumsub ID created, Identity Card, double-sided, the tips, Allow the camera, can't ask for your permission, ID scan front and back, selfie, Hold still, All set, documents on another profile, reviewed then deposit), the recap and the part 4 preview. Request `89f01eda7b2c497a826a8a085021a412`, about 7 credits |
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
