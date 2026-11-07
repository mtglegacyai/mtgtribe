# Production record: video 01 (7 November 2026)

Composition: `tools/video3d/src/compositions/whatif01/` (ids `WhatIf01-16x9` and `WhatIf01-9x16`, one set of scenes that
switches layout on the composition's shape). Timeline, spoken script, caption
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

### Leo, vertical (9:16, 1080x1890, about 6.6 s each, same references), made for v2

| Clip | Action | Used in | Video id |
|---|---|---|---|
| V1 | sees the loaf, surprised | hook (both layouts) | f3fad5b8cb83451aaed72e9352681bfc |
| V2 | open paw, asks a question | "what would you buy first?" (9:16; 16:9 keeps L2 full screen) | b5c1ee6817c24ac6836c9c46d53f9701 |
| V3 | amazed, pushes up glasses | 14 zeros | 2533218ef65e4dcb8ce3007408a67ced |
| V4 | waves, thumbs up | end card | 6252c4ef2c7042369e4eb70d4814f7a0 |
| V5 | chin on paw, thinks | "causes are debated, one is clear" | 0d09e71b68bc4c45bc878e760595a646 |
| V6 | laughs in disbelief, shrugs | the poster on money, Cannes Lions | e2767a9c2ae94fb6ad85332763f54ce7 |
| V7 | calm, one finger raised | "the lesson" | da69e6bf38aa4faebb777422079d6397 |

In 16:9 the vertical clips play in a tall gold window on the right; in 9:16 they play in a tall window (face and the
whole t-shirt print above the captions) or a face window under a panel. L1, L3 and L4 are kept but no longer used.

## Sound (v2, all made in code, no licences needed)

- Effects (v4): MTG found some v3 effects "too loud and too sharp". The whole palette was replaced by soft effects
  made in code (`scripts/make_sound.py`, 19 effects, all pass `check`), and every scene was re-cued with fewer,
  meaningful ones: rising notes as the price doubles, a soft clock into "24.7 hours", falling notes as the pay melts,
  swells into the reveals, a tension pulse before the guess and before "the part most people miss". Measured: the
  loudest effect moment went from about 10 dB above his voice (v3) to about his voice level (v4).
- No background music (v3). v2 had a code-made music bed under the whole video; MTG (7 Nov 2026): "too loud, I don't
  like it. Remove it completely, and only play my theme music towards the end." Removed, with its files.
- Closing track (v3): MTG's theme "They Call Me MTG" (his mp3, 51.4 s, mastered at about -14 LUFS; kept in
  `public/music/they-call-me-mtg.mp3`, not in git) from 50 seconds before the end, about 12 dB under his voice while he
  speaks (pauses under 1 s stay ducked, so it never pumps), then in the clear on a 5-second end card after his last
  word, fading out with the last frame.

## Narration timing (v2, v3)

Gaps between sections cut from about 0.7 s to 0.2 s (faster pacing): total 4:23.7 (was 4:27). Captions are aligned
section by section (`--sections`), because aligning the whole file let Whisper bunch the hook's first words together.

## Credits

220 before the first voice line test (1 credit), 162 after all narration and Leo's clips: 59 credits for this video
(voice about 12, Leo about 47). v2 vertical clips V1 to V7: 77 credits (balance 85 afterwards, renews 3 December 2026).
Total for video 01 so far: 136 credits.

## Rebuild

```bash
cd tools/video3d
python3 scripts/make_sound.py sfx
python3 scripts/align_captions.py public/videos/01/voice public/videos/01/spoken-script.txt public/videos/01/captions.json --sections public/videos/01/timeline.json --replace public/videos/01/caption-replacements.json
REMOTION_GL=swangle npx remotion render WhatIf01-16x9 out/whatif01-v2-16x9-raw.mp4 --concurrency=4
REMOTION_GL=swangle npx remotion render WhatIf01-9x16 out/whatif01-v2-9x16-raw.mp4 --concurrency=4
# two-pass loudness to -14 LUFS (see the 3D studio README), AAC 192k, faststart
# Final v2 files (7 Nov 2026): out/whatif01-v2-16x9.mp4 and out/whatif01-v2-9x16.mp4, 4:24, -14.1 LUFS, true peak
# -1.1 dBFS, no black frames. The sound mix was rendered once (audio only, --codec=wav) and put into both videos.
# v3 (vertical only, MTG wants it for socials first): no music bed, theme from 50 s before the end, end card 5 s,
# 4:28. Made from the v2 vertical render: new sound mix, the two v2 patches and the new ending frames 7880 to 8032.
```

## Real 3D sample (7 November 2026)

MTG asked which parts of video 01 are 3D. Honest answer: none of the graphics. They are flat layers tilted in
perspective (CSS 3D); only Leo's clips are 3D-animated. To show the difference, the hook was rebuilt in real 3D
(Three.js): `src/compositions/whatif01/Hook3D.tsx`, composition `Hook3D-9x16`, file `out/hook3d-sample.mp4` (13.2 s).
A black-and-gold studio with depth (gold arches, reflective floor, fog), a 3D loaf on a pedestal, the price extruded in
gold Anton (`public/fonts/anton.typeface.json`, made by `scripts/make-typeface.mjs`), and up to 170 gold coins that rain
down and pile up as the price doubles. Renders at about 1 frame per second per core in software WebGL (swangle).

