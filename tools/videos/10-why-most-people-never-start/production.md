# Production record: video 10 (15 November 2026, daily video)

Composition: `tools/video3d/src/compositions/wmp10/SecondIncome.tsx` (id `WMP10-9x16`), cover `Cover10-9x16`.
Files in `tools/video3d/public/videos/10/`: `script.txt` (the text sent, with `//` pause marks), `words.json`,
`captions.json`, `timeline.json`, `anchors.json`, `cues.json`, `replacements.json`; the voice WAV is not in git.

- Voice: "MTG Master Voice V3" (`65f1b9ff3f1e418496de5715a801e7dd`), one call, plain text, request
  `9bef512c913a41b8b002ef6227397a53`, 62.8 s (188 words, about 3.0 words a second). Credits: 504 before, 503 after
  (1 credit; MTG's balance had been topped up since video 09, when it stood at 40).
- Pauses: `--pause 0.5`; the natural pauses were long enough (0.03 s and 0.11 s added). Total voice track 62.9 s.
- Leo: 8 moments from his existing clips (reassure, worried, aha, thumbs up, wow, ask, wink and thumbs up, welcome),
  each on a named cue; the worry is answered by the aha in the next beat. No new clips, no credits.
- Pictures (code, no credits): four people with one in gold, three hurdle cards with their survey shares, a huge 3D
  "STEP 1" that shrinks into a small gold step, a clock that fills 20 minutes, example skills, the 120-hour counter,
  fifteen day tiles, a staircase the person climbs.
- CSS 3D moments: the big step (Block3D), the clock turning in, the flipping cards.
- Sound: soft effects fitted to the story, two new ones made for it (`step`, a soft footstep up a stair, and `shrink`,
  something big made small); `make_sound.py` reports 46 effects, all soft. The theme's last line only.
- End: EndScreen with pills timed to "crypto, AI and multiple income streams", his formal photo, the signature and
  mtgtribe.com in the big gold pill.
- Final: `out/wmp10-9x16.mp4`, 1:06 (66.0 s), -14.0 LUFS, true peak -1.4 dBFS, no black frames, cover embedded. A
  transcript of the finished file matches the script word for word. The theme's last line starts at 62.83 s, right
  after his last word (62.59 s): confirmed by matching the end of the file against the theme itself (correlation
  0.93), because the transcriber did not write out the sung line this time.
- Length: just over a minute, by choice: three hurdles, the reframe, the step and the arithmetic needed the room
  (MTG, 10 November 2026: up to 3 minutes when the topic needs it).
