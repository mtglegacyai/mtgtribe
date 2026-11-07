# Production record: video 01 (7 November 2026)

Composition: `tools/video3d/src/compositions/whatif01/` (id `WhatIf01-16x9`). Timeline, spoken script, caption
replacements and captions: `tools/video3d/public/videos/01/`. Audio and Leo clips are not stored in git (regenerable);
their IDs are below.

## Voice (HeyGen, "MTG Master Voice V2", voice 3931c505632149ceb2bbfecf2778c09c, engine orca, WAV 48 kHz)

| Section | Content | Length (s) | HeyGen audio id |
|---|---|---|---|
| s01 | Hook | 13.06 | eb15339de8b046a18954c31aa1655680 |
| s02 | Greeting | 11.89 | 4f8b262030a34d318ebfb02cfa742f63 |
| s03 | Setup and guess | 24.22 | 8573ce3adf4e47d7a0083485709b3492 |
| s04 | 24.7 hours, pay bars | 23.09 | 3aece87ee4c14eaa846d30bc7db3af56 |
| s05 | Why | 21.55 | beae8729bee6487ca13d242fd1b0b4f0 |
| s06 | Coping, buy first | 28.68 | 87837600c49044af8d5d26a092b0890f |
| s07 | 14 zeros | 15.57 | 146676da3124480a930753e69d859b26 |
| s08 | Posters on money | 34.09 | a3a7180cb6a24594bb35a270cd5dc92e |
| s09 | Promise and trust | 17.08 | db12bcae9c874f22bf6bd929e7cfa8c9 |
| s10 | The lesson | 27.85 | 9ff2434965584ce9ae3914c94dd6c53d |
| s11 | Tribe call to action | 20.01 | 23143065caa0408683301b26d2917165 |
| s12 | Signature outro | 23.46 | 8d088d50d3044532a4caf40f22fd6f69 |

Download pattern: `https://resource2.heygen.ai/text_to_speech/014da4e407f0458282d5068f68cc43a5/3931c505632149ceb2bbfecf2778c09c/id=<id>.wav`.
Pronunciation spellings used in the narration (captions show the correct form): "Can Lions" (Cannes Lions),
"MTG tribe dot com, slash group" (mtgtribe.com/group), "United States dollar" (said in full).
Small wording change from the approved script: "did something the world had never seen" became "did something
remarkable" (the first could not be verified).

## Leo (HeyGen reference_to_video, 16:9, 1080p, 6 s, references: Leo 855fc4950cb54a9c91b6e829f70220dd + t-shirt 47be82b6e98e45c5a0ba430e3416aa4b)

| Clip | Action | Used in | Video id |
|---|---|---|---|
| L1 | sees the loaf, surprised | hook | a70b7a7aba7948c487f307d27252ead9 |
| L2 | open paw, asks a question | "what would you buy first?" | 3e8f6433a784442693b22bfa2eb6b38c |
| L3 | amazed, pushes up glasses | 14 zeros | 5ec9bc14742e44c6836a258a24d73e62 |
| L4 | waves, thumbs up | end card | 6783c6818cf142a3bad08bb79fa36ba0 |

## Credits

220 before the first voice line test (1 credit), 162 after all narration and Leo's clips: 59 credits for this video
(voice about 12, Leo about 47).

## Rebuild

```bash
cd tools/video3d
python3 scripts/align_captions.py public/videos/01/narration.wav public/videos/01/spoken-script.txt public/videos/01/captions.json --replace public/videos/01/caption-replacements.json
REMOTION_GL=swangle npx remotion render WhatIf01-16x9 out/whatif01-preview-raw.mp4 --concurrency=4
ffmpeg -i out/whatif01-preview-raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k out/whatif01-preview.mp4
```
