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
