# MTG's spoken slogan (approved 16 November 2026)

MTG: "I like that one, much better, use it going forward across all my videos that use that short ending."

- Approved recording: `public/voice-bank/slogan.wav` ("Let's get this crypto", about 0.9 s, about 118 Hz, his normal
  voice, no effects) with its word times in `slogan.json`. Every video with the short ending gets it through
  `scripts/splice_slogan.py`. Do not record the slogan again.
- Raw take: `take4-plain.wav` (MTG Master Voice V3, `65f1b9ff3f1e418496de5715a801e7dd`, 1 credit), text sent:
  "I'm MTG, your digital architect. Let's get this crypto." with no tags, lowercase and a full stop. Word times from
  HeyGen in `take4-plain.words.json`. Rebuild: `python3 scripts/make_slogan.py voice-src/slogan/take4-plain.wav
  voice-src/slogan/take4-plain.words.json slogan --from 2.80 --plain --lift 0.5`, then cut the file at 1.06 s.

Why: the slogan inside each script comes out at 200 to 270 Hz (capitals and "!" make the voice shout it) while his
narration sits at 120 to 130 Hz. Rejected the same day (takes deleted): delivery tags ([deep voice], [slowly],
[authoritative]), gaps between the words, slowing down, echo or bass, a landing sound. MTG: "too slow ... too far
apart", "like I'm in a drama ... some terrible horror", "Let me sound normally, just like the rest of my voice ... not
at a high pitch, not at a snail pace."
