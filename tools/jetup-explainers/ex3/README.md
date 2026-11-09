# JetUP explainer #3: "Amplify 24x made simple" (the market stall), 9 Nov 2026

MTG asked for the next explainer on 9 Nov 2026: #3 from `tools/learning-system/PLAN.md`. The first preview (2:01) is built
from his banked voice only (0 HeyGen credits): the money plan and Amplify lines from the sign-up training take `t1.mp3`,
"Bigger exposure means bigger swings, up and down" and "Start small" from the 5 Checks take `o2.mp3`, the greeting and
close from explainer #1, and save, share, "We learn best when we teach others" and the slogan from explainer #2.

About 22 seconds of the body have no voice yet and play on screen only, with the four signature sounds: the hook
(0 to 3.3 s), the market stall (8.5 to 15.5 s), the calculator demo (42.3 to 50.5 s) and the loss limit (53.6 to 59.2 s).
Six new lines in his voice would cover them (see "Next step"). **Not approved yet: do not record before MTG says so.**

Copy that converts (MTG's standing rules, 8 and 9 Nov 2026): inform, never frighten. No loss statistics, no warnings
beyond his gentle signature reminder and the end card's small line, a warm "Simple, right? Now it's your turn" and one
action, tap any Join JetUP button.

- `lines_ex3.py`: cuts the 12 banked lines and their word times, plus the shared greeting, close and signature lines
  from explainers #1 and #2 (`lines.json`, `words.json`).
- `make_ex3.py`: voice placement, captions ($155, $50, $100, 24x, $1,200, $4,800, $6,000, mtgtribe.com/jetup), cues,
  the signature ending's cues (`kitcues.json`, `links=False`, Next: the 70/30 split), body sounds. It switches to the new
  lines by itself once all six are in `lines.json`.
- `calc_shots.js`: real screenshots of the Exposure Calculator (the training plan $6,000, Sonic only $1,200) for the demo
  scene; `stage/calc/boxes.json` holds the tap targets.
- `stage/`: scenes: hook ($50 trades like $1,200, one word: Amplify 24x); hi; the market stall (you pay for one stall,
  Amplify lets you trade the size of 24); the money plan ($155 in: $50 Sonic, $100 balance, $100 promo bonus, $5 spare);
  Amplify 24x ($50 becomes $1,200, $200 becomes $4,800, $6,000 of exposure); what is exposure (the size you trade with,
  not money you own); try your own numbers (the real calculator in a laptop, tap by tap); bigger size, bigger moves
  (1% of $250 is $2.50, 1% of $6,000 is $60, up and down); the loss limit is written down (10% of the starting balance,
  5% with a community token); a bigger size, not extra money (start small, a small withdrawal early); now it's your turn.
- `cover.html`, `shoot_cover.js`: the 16:9 cover ("EXPLAINER · 2:01", "AMPLIFY 24X MADE SIMPLE", the 24 stalls, $50 x 24 = $1,200).
- Build: `tools/video-signature/build_part.sh <dir> <out.mp4>`; QA: `tools/video-signature/qa_new.py <dir> <out.mp4>`.
  Preview of 9 Nov 2026: 120.84 s, 1920x1080, 25 fps, -14.1 LUFS, true peak -2.6 dBFS, full closing track from 69.49 s.
- Facts checked against `tools/learning-system/jetup-facts.md` (24x Amplify, the $155 money plan, liquidation at a 10%
  loss of the starting balance, 5% with a community token). "$6,000 of exposure" includes the promo bonus:
  ($50 + $100 + $100) x 24. No return figures are shown.
- No photo of MTG: the JetUP logo disc takes its place. Series style kept (as explainers #1, #2, #4, #5).

## Next step: the six new lines (waiting for MTG's approval, about 3 credits)

Proposed on 9 Nov 2026, about 700 characters, plain text, voice "MTG Master Voice V2"
(3931c505632149ceb2bbfecf2778c09c), no engine parameter (the reply must say engine "orca"):

1. `nhook`: Fifty dollars that trades like twelve hundred. How? One word: Amplify. Let me show you.
2. `nstall`: Think of a market stall. You pay for one stall, but Amplify lets you trade as if you had twenty-four.
3. `nmove`: Same market, same prices. Every move is twenty-four times bigger, in both directions.
4. `nlimit`: And the loss limit is written down before you start: ten percent of the starting balance, or five percent
   with a community token.
5. `ncalc`: Want to try it with your own numbers? Open the Exposure Calculator on my page, type an amount, and see your
   trading size in one tap.
6. `nrecap`: So that's Amplify: a bigger trading size, not extra money. Start small, and learn how it moves.

HeyGen's speech access returned "Bearer token expired/revoked" in the session that built this video (9 Nov 2026), so
recording needs a new session after MTG reconnects HeyGen. Then: check out branch `jetup-video-work`, take the working
pack in `jetup-work/voice-bank/explainers/ex3-pack/` (every cut line as FLAC, `lines.json`, `words.json`, and its README
with the exact speech request), record the six lines in one call, cut them into `v_nhook.wav`, `v_nstall.wav`,
`v_nmove.wav`, `v_nlimit.wav`, `v_ncalc.wav`, `v_nrecap.wav`, add them to `lines.json` and `words.json`, rebuild with
`make_ex3.py` and `build_part.sh`, QA, and show MTG the preview. With the new lines the video opens on the spoken hook,
"Here is the simple picture" and the two 5 Checks lines step aside for the new ones, and the length changes a little.

## When MTG approves it for the site

File name: `jetup/media/jetup-explainer-amplify-24x.mp4` (cover `jetup/img/` as the other explainers). Places: home
"$155 in. $6,000 of exposure.", How It Works "Amplify 24x", the Exposure Calculator page, check 4 on the 5 Checks page,
the Videos page and the downloads list. Then VideoObject data, `python3 tools/og/check_og.py`, `tools/qa/hscroll.js`,
the full tests, and `PLAN.md`.
