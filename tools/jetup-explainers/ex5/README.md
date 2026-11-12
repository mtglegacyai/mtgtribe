# JetUP explainer #5: "The $100 Fast Start Promo", 9 Nov 2026

MTG picked #5 from `tools/learning-system/PLAN.md`. Every line is his banked voice (0 HeyGen credits): the promo lines from
the sign-up training takes (`o2.mp3`, `t1.mp3`, `t3.mp3`, `t4.mp3` on branch `jetup-video-work`), the greeting and close from
explainer #1, and save, share, "We learn best when we teach others" and the slogan from explainer #2.

Copy that converts (MTG's standing rule, 8 Nov 2026): no loss statistics, no warnings beyond the promo rules he speaks
himself, a warm "Simple, right? Now it's your turn" and one action, tap any Join JetUP button.

- `lines_ex5.py`: cuts the 37 lines and their word times (`lines.json`, `words.json`).
- `make_ex5.py`: voice placement, captions (never more than two lines; $155, $50, $100, $200, 12 months, jet-up.ai, CU,
  CopyX, mtgtribe.com/jetup), cues, the signature ending's cues (`kitcues.json`, `links=False`, Next: step-by-step, part 1),
  emoji pops (🎁 on "works like this", 💵 on "you deposit") and the body sounds (`sfx_body.json`).
- `stage/`: 16:9 scenes: the $100 gift with confetti; hi; the money plan (the coin counts to $155, $50 to Sonic AI, $100
  stays for the promo, the promo adds $100 for a $200 promo account, a few dollars spare); claim it in 4 steps (CU number,
  the orange tile, the form with the Join the promo tap, the confirmation email; Application received!; the $50 and $200
  accounts); the promo rules; a promo is a promo (start while it's still on, confirm it on jet-up.ai); now it's your turn.
  Needs `Anton-Regular.ttf`, `jetup-disc*.png`, `jetup-logo.webp` beside it (copy from `../ex2/stage` sources).
- Build: `tools/video-signature/build_part.sh <dir> <out.mp4>`; QA: `tools/video-signature/qa_new.py <dir> <out.mp4>`.
- Cover: `cover.html` + `shoot_cover.js` (EXPLAINER · 2:18, gift, $50 and $200 cards, JetUP disc, no photo of MTG).
- Facts checked against `tools/learning-system/jetup-facts.md` (start amount, claim steps, result, rules).

Result: 2:18, -14.0 LUFS, true peak -2.7 dB, no sample overshoots; speech-to-text hears every line in order.
