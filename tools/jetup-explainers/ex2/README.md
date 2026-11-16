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

## v2 (MTG, 8 Nov 2026): copy that converts, never intimidates

MTG: "Take it easy on the warnings and on the losses and negativity... I'm trying to convert these people into action
takers." Removed: "where the picture stops", the 88% line and "learn first". The red chips became "Your money stays in your
name". New close (one request, 1 credit, voice bank `explainers/ex2v2.mp3`): "So that's the whole picture..." with the
five rows lighting up while the taxi drives on, then "Simple, right? Now it's your turn. Take your seat." and his banked
"If I invited you, go to MTG tribe dot com slash jet up, and tap any Join Jet Up button" with the button tapped on screen.
The signature ending starts at the fair-play line (`links=False`). 2:08.
