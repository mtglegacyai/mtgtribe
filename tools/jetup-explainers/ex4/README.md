# JetUP explainer #4: "The 70/30 split: where every profit goes", 9 Nov 2026

MTG picked #4 from `tools/learning-system/PLAN.md` and approved two new lines in his voice (about 1 credit): the hook
("Seventy, thirty. Two numbers that decide where every profit goes. Let me show you.") and the calculator line ("Want to try
it with your own numbers? Open the Profit Split Calculator on my page, type an amount and a result, and see your share in
one tap."). HeyGen's connection had expired on 9 Nov 2026, so the first preview uses his banked lines only: it opens with
"Here is the simple picture." and the calculator demo runs on screen. Once the two lines are recorded, save them as
`v_nhook.wav` and `v_ncalc.wav` with their words in `lines.json`/`words.json`; `make_ex4.py` switches to them by itself.

- `lines_ex4.py`: cuts the 15 banked lines (5 Checks o1/o2, sign-up training t3) and their word times, plus the shared
  greeting, close and signature lines from explainers #1 and #2.
- `make_ex4.py`: timeline, captions (70%, $10, $7, +30.1%, Myfxbook, 21%), cues, signature ending cues, body sounds.
- `calc_shots.js`: real screenshots of the Profit Split Calculator ($10 profit, the Myfxbook preset, typing 100) for the
  demo scene; `stage/calc/boxes.json` holds the tap targets.
- `stage/`: scenes: 70/30 hook; hi; the profit bar splits 70/30 and the 30% fans out (TAG Markets the broker, Sonic AI the
  strategy provider, JetUP the partner program), $10 becomes $7 + $3; only on profit ($0 fee on a losing trade, no
  management or join fee, 1 month minimum, Amplify account); check the record (Myfxbook line drawing forward, +30.1%,
  30.1% x 70% = about 21%, not a fixed return); try your own numbers (the real calculator in a laptop, tap by tap); your
  money, your pace (profits any time, start small, a small withdrawal early); now it's your turn.
- Build: `tools/video-signature/build_part.sh <dir> <out.mp4>`; QA: `tools/video-signature/qa_new.py <dir> <out.mp4>`.
- Facts checked against `tools/learning-system/jetup-facts.md` (70/30, fee only on profit, no management or join fee,
  Myfxbook +30.1% from 3 Nov 2024 to 4 Oct 2026).
