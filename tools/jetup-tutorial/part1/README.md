# Part 1 build (create your JetUP account), preview 7 Nov 2026

- `lines.py`: cuts MTG's banked voice lines (voice bank on branch `jetup-video-work`) at real silences; `words.json` word times.
- `shots.py`: the edit (shots, camera, rings, taps, chips, steps); `make_tl.py` writes `stage/timeline.js` and `voice.wav`.
- `stage/`: the 1080x1920 stage (every frame a pure function of t); `render.js` renders frames with Playwright.
- `mix_p1.py`: voice, light sound design, the closing track ending on the last frame, -14 LUFS.
- Redacted frames come from `tools/tutorial-redact/` (clips A to M of MTG's recording; raw and frames are never committed).
  Stage also needs `Anton-Regular.ttf` and `jetup-mark.png` (from the promo builds) beside `stage.html`.
