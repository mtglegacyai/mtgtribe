# JetUP explainer #2: "Five names. One simple picture." (the minibus taxi), 8 Nov 2026

MTG picked #2 from `tools/learning-system/PLAN.md` and approved speaking the taxi lines (one HeyGen request, 2 credits,
voice bank `explainers/ex2v1.mp3` on branch `jetup-video-work`). Everything else is his banked voice.

- `lines_ex2.py`: cuts the 8 new lines and the banked ones (track record, log in yourself, the links line), word times.
- `make_ex2.py`: voice placement, captions (never more than two lines), cues, the signature ending's cues (`kitcues.json`,
  links on), the body sounds on the training's palette (`sfx_body.json`).
- `stage/`: 16:9 scenes: five names mixed up then one row; hi; the minibus taxi that builds line by line (driver, seat in
  your name, CopyX route board, JetUP association, you) with the five-row picture on the right; where the picture stops
  and the 88% reminder; let's verify. Needs `Anton-Regular.ttf`, `jetup-disc*.png`, `jetup-logo.webp` beside it.
- Build: `tools/video-signature/build_part.sh <dir> <out.mp4>` (render, the training's ending, one mix, AAC 256k).
- Cover: `cover.html` + `shoot_cover.js` (EXPLAINER · 2:11, the taxi, JetUP disc, no photo of MTG).
