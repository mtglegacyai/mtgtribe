# Build pipeline and site placement

Reference build: `tools/jetup-tutorial/part1/`
- `lines.py`: cuts banked and new lines (`lines.json`), `words.json` word times.
- `vo_v2.py` voice placement; `shots_v2.py` the edit (shots with clip, source start and speed, camera key points, rings,
  taps, chips, steps, scenes, window spans, plan items and cues); `make_tl3.py` builds `stage/timeline.js` and `voice.wav`.
- `stage/stage.html` + `stage/engine.js`: the scenes (intro, plan, link, window, tip, mail, next, outro).
  Needs `Anton-Regular.ttf`, `jetup-mark.png`, `mtg-face.png`, `mtg-photo-round.jpg` beside it.
- `render.js range a b frames` (4 workers in parallel), `mix_p1.py` (voice, light sound design, bed, closing track,
  loudnorm -14 LUFS, TP -1.8 target), ffmpeg x264 CRF 18, AAC 192k, faststart.
For a new part: copy the folder, write the new shot list from the recording map, keep the scenes, change texts and lists.

Checks: OCR privacy scan (zero flags), contact sheet every 3 s, speech-to-text of the final audio (every line, in order),
loudness, brightness jumps (only planned fades), the cover frame.

Site placement (recommended to MTG 7 Nov 2026): the step-by-step page of the site (JetUP: /jetup/get-started/).
Each part's video in the slim phone frame (`phone()` in the JetUP layout) at the top of its part, and a "Step-by-step
videos, one per part" strip near the top of the page. Video file in `jetup/media/`, cover 480 x 848 webp and a jpg,
VideoObject structured data. The player closes itself at the end (standing rule).
