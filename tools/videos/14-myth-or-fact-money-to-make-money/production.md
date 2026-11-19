# Production record: video 14 (19 November 2026, daily video)

Composition: `tools/video3d/src/compositions/mof14/MoneyMyth.tsx` (id `MOF14-9x16`), cover `Cover14-9x16`.
Files in `tools/video3d/public/videos/14/`: `script.txt`, `words.json`, `captions.json`, `timeline.json`,
`anchors.json`, `cues.json`, `replacements.json`; the voice WAV is not in git.

- Voice: "MTG Master Voice V3" (`65f1b9ff3f1e418496de5715a801e7dd`), one call, plain text, request
  `0f56ee2b88b24f7087832925fe613b1b`, 61.2 s (176 words, about 2.9 words a second). Credits: 1153 before, 1152 after
  (1 credit).
- Pauses: `--pause 0.5`; 0.27 s added before the verdict (the `// 0.7` beat).
- The slogan: his approved recording, spliced in 0.5 s after "Architect."; 128 Hz in the finished file.
- Leo: 10 moments from his existing clips (think, thumbs up, smile, aha, laugh, reassure, ask, wink and thumbs up,
  wave, welcome); no new clips, no credits.
- Pictures (code, no credits): the claim card with MYTH and FACT buttons, the 44% counter with its source, three need
  cards tilting in with ticks, three tool tiles whose price tags flip from $$$ to $0 FREE, a start-up receipt, a
  turning hourglass, "MOSTLY MYTH" stamped on the claim.
- CSS 3D moments: the need cards tilting in, the price tags turning over, the flipping claim and receipt.
- Sound: soft effects fitted to the story, two new ones made for it (`pricetag`, a tag flipping to $0, and `verdict`, a
  soft ta-da), plus `stamp` for "MOSTLY MYTH"; `make_sound.py` reports 55 effects, all soft. The theme's last line only.
- QC fixes before the render: bigger tool tiles, the hourglass and Leo kept clear of the price note, a wave after the
  wink so the share prompt never stands empty.
- Final: `out/mof14-9x16.mp4`, 1:04 (64.4 s), -14.0 LUFS, true peak -1.5 dBFS, no black frames, cover embedded. A
  transcript of the finished file matches the script. The theme's last line starts at 61.26 s, right after his slogan
  (61.02 s), correlation 0.95.
