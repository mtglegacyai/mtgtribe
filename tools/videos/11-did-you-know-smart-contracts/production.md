# Production record: video 11 (16 November 2026, daily video)

Composition: `tools/video3d/src/compositions/dyk11/SmartContracts.tsx` (id `DYK11-9x16`), cover `Cover11-9x16`.
Files in `tools/video3d/public/videos/11/`: `script.txt` (the text sent, with `//` pause marks), `words.json`,
`captions.json`, `timeline.json`, `anchors.json`, `cues.json`, `replacements.json`; the voice WAV is not in git.

- Voice: "MTG Master Voice V3" (`65f1b9ff3f1e418496de5715a801e7dd`), one call, plain text, request
  `a4b14e9ca975408a9f36989ec4c3cc93`, 58.4 s (177 words, about 3.0 words a second). Credits: 208 before, 207 after
  (1 credit; the balance had dropped from 503 to 208 outside this session since video 10).
- Pauses: `--pause 0.5`; 0.15 s added before the tip (the `// 0.7` beat) and 0.03 s before the question. Total
  voice track 58.6 s.
- Leo: 9 moments from his existing clips (wow, smile, think, worried, reassure, thumbs up, ask, wink and thumbs up,
  laugh, welcome), each on a named cue; the worry is answered at once by the reassuring tip. No new clips, no credits.
- Pictures (code, no credits): three middlemen crossed out, the $70 billion counter with its source, a vending machine
  drawn in code (a coin goes in, the keypad lights B2, a can drops), 3D blocks linked in a chain, "IF / THEN" typed as
  code, the fix-or-lock comparison, a slim phone with a wallet approval request (made-up site, no brand).
- CSS 3D moments: the gold contract block, the turning vending machine, the chain of blocks, the turning phone.
- Sound: soft effects fitted to the story, two new ones made for it (`vend`, a can dropping into the tray, and
  `keypad`, three soft keypad beeps); `make_sound.py` reports 48 effects, all soft. The theme's last line only.
- End: EndScreen with the pills crypto, wallet and keys, AI, multiple streams and the tribe, his formal photo, the
  signature and mtgtribe.com in the big gold pill.
- QC fix: the comparison cards were made taller so the small vending machine no longer covers its label; the video
  was rendered again after the fix.
- Final: `out/dyk11-9x16.mp4`, 1:01 (61.3 s), -14.1 LUFS, true peak -1.5 dBFS, no black frames, cover embedded. A
  transcript of the finished file matches the script. The theme's last line starts at 58.16 s, right after his last
  word (57.90 s), confirmed by matching the end of the file against the theme (correlation 0.94).

## Re-made the same day: the deep slogan (MTG, 16 November 2026)

MTG: "Let's get this crypto ... it's too high. I just want it to be deep and slow and strong ... make it land harder.
This is a slogan, so it must feel like a slogan." Measured: the slogan at the end of the take sat at about 240 to 270 Hz
and rose at the end (his narration: about 126 Hz).
- Three takes of the slogan alone in MTG Master Voice V3 with HeyGen delivery tags (`[deep voice]`, `[slowly]`,
  `[authoritative]`): 3 credits (205 before, 202 after; the balance had dropped from 207 to 205 outside this session).
  Today's voice total: 4 credits, within the 5 approved per daily video.
- Take 1 (`[deep voice] Let's... Get... This... Crypto!`, about 118 Hz, falling to about 86 Hz on "Crypto") finished
  with `make_slogan.py` (warmth, gentle compression, a short room, 1.5 dB above the narration) and spliced in with
  `splice_slogan.py`, 0.45 s after "Architect.". On screen the four words now land one by one with his voice, "Crypto!"
  bigger with a gold glow, then the website pill; a new soft effect, `land`, sits under "Crypto!".
- Final: `out/dyk11-9x16.mp4`, 1:03 (63.4 s), -14.1 LUFS, true peak -1.3 dBFS, cover embedded. The slogan measures
  118 Hz in the finished file; the theme's last line starts at 60.23 s, right after "Crypto!" (59.99 s), correlation
  0.93.
