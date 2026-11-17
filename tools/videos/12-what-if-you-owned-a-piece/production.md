# Production record: video 12 (17 November 2026, daily video)

Composition: `tools/video3d/src/compositions/wif12/OwnAPiece.tsx` (id `WIF12-9x16`), cover `Cover12-9x16`.
Files in `tools/video3d/public/videos/12/`: `script.txt`, `words.json`, `captions.json`, `timeline.json`,
`anchors.json`, `cues.json`, `replacements.json`; the voice WAV is not in git.

- Voice: "MTG Master Voice V3" (`65f1b9ff3f1e418496de5715a801e7dd`), one call, plain text, request
  `5ea3631b25a44751a8de3ee44160c3f9`, 55.2 s (176 words, about 3.2 words a second). Credits: 190 before, 189 after
  (1 credit; the balance had dropped from 201 to 190 outside this session since the slogan take).
- The slogan: his approved recording (`public/voice-bank/slogan.wav`, MTG 16 November 2026) spliced in 0.5 s after
  "Architect." with `splice_slogan.py`; it measures 120 Hz in the finished file (his narration: 120 to 130 Hz). The
  words land on screen as he says them (`sloganWords`).
- Leo: 7 moments from his existing clips (wow, mind blown, aha, reassure, ask, wink and thumbs up, welcome); no new
  clips, no credits.
- Pictures (code, no credits): an original gold bottle (no logo, no brand colours), the company pie with one slice
  lifting out, a share certificate with a "PART OWNER" stamp, coins flowing from a 3D company block to owners, 64 rising
  bars, hundreds of tiny companies falling into an S&P 500 basket, a price line going up and down, a notepad that writes
  the first step.
- CSS 3D moments: the company block, the falling blocks into the basket, the notepad.
- Sound: soft effects fitted to the story, two new ones made for it (`fizz`, a bottle opening, and `stamp`, the share
  certificate); `make_sound.py` reports 51 effects, all soft. The theme's last line only.
- QC fixes before the render: a bigger slice and certificate, the stamp moved under the text, the falling blocks kept
  clear of the heading, a readable S&P 500 label, Leo kept clear of the owners and the heading.
- Final: `out/wif12-9x16.mp4`, 0:58 (58.1 s), -14.0 LUFS, true peak -1.4 dBFS, no black frames, cover embedded. A
  transcript of the finished file matches the script. The theme's last line starts at 54.96 s, right after his slogan
  (54.73 s), correlation 0.95.
