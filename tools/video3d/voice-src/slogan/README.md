# MTG's slogan takes (16 November 2026)

Raw HeyGen takes of "Let's Get This Crypto!" in MTG Master Voice V3 (`65f1b9ff3f1e418496de5715a801e7dd`), one credit
each, recorded on their own after MTG asked for a deeper, slower, stronger slogan. The `.words.json` files are the word
times HeyGen returned. Finished versions: `public/voice-bank/slogan-deep-1/2/3` (make_slogan.py);
`public/voice-bank/slogan-deep` is the one every video uses (splice_slogan.py).

| Take | Text sent | Pitch (median) | Finished file |
|---|---|---|---|
| 1 | `[deep voice] Let's... Get... This... Crypto!` | 118 Hz | slogan-deep-1 (the default) |
| 2 | `[slowly] Let's get this... crypto!` | 119 Hz | slogan-deep-2 |
| 3 | `[authoritative] Let's. Get. This. Crypto!` | 139 Hz | slogan-deep-3 |

For comparison: MTG's narration sits at about 126 Hz; the old slogan inside each script came out at 240 to 270 Hz and
rose at the end.

To rebuild a finished file: `python3 scripts/make_slogan.py voice-src/slogan/take1-deep-voice.wav
voice-src/slogan/take1-deep-voice.words.json slogan-deep-1 --from 0.30` (take 2 and 3: `--from 0.26`).

## Second round, the same day (no credits)

MTG on the three finished takes: "too slow or it just breaks ... too far apart from each other. It's one thing. Let's
get this crypto ... not too slow, not too fast, not too high. Just in the perfect tone, in the perfect speed." So the
words were joined into one phrase, from the takes already paid for:
- A (`public/voice-bank/slogan-try-A-take2-joined-fast`, now also `slogan-deep`): take 2, "Let's get" as spoken, the
  gap before "this" and the long pause before "crypto" closed to 35 ms, the drawn-out "s" of "this" trimmed, then 1.12
  times faster with the pitch kept (rubberband). About 2.0 s, 119 Hz.
- B (`slogan-try-B-take1-joined-fast`): take 1's four words joined 20 ms apart, 1.12 times faster. About 1.8 s, 118 Hz.

## Third round, the same day: his normal voice (1 credit, with MTG's yes)

MTG on A and B: "I sound like I'm in a drama ... locked up in some terrible horror. Let me sound normally, just like the
rest of my voice ... not at a high pitch, not at a snail pace." Take 4 (`take4-plain.wav`): "I'm MTG, your digital
architect. Let's get this crypto." with no tags, lowercase and a full stop. The sign-off part measures 124 Hz (his
narration), the slogan 118 Hz, about 0.9 s, falling on "crypto". Finished with `make_slogan.py --plain` (no colouring,
loudness only, +0.5 dB) as `public/voice-bank/slogan-plain`, copied to `slogan-deep` (the file the tools use).
