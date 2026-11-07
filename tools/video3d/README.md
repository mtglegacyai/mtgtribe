# MTG 3D Video Studio (Three.js + Remotion)

Status (7 November 2026): installed, set up and tested. The demo below is a technical test, not a video for publishing.

Everything for 3D animated videos lives in this folder:

| Job | Tool | Version |
|---|---|---|
| 3D scenes, lights, materials, camera moves | Three.js, React Three Fiber, drei | three 0.187.0, fiber 9.8.2, drei 10.7.9 |
| 3D inside the video timeline, frame exact | @remotion/three (`<ThreeCanvas>`) | 4.0.541 |
| Timeline, audio, rendering to MP4 | Remotion (studio, renderer, `<Html5Audio>`) | 4.0.541 |
| Word by word captions | @remotion/captions + `scripts/transcribe.py` (faster-whisper) | 4.0.541 |
| Audio length, waveforms | mediabunny, @remotion/media-utils | 1.64.0, 4.0.541 |
| Brand fonts (Anton, Manrope, JetBrains Mono), offline | @fontsource + @remotion/fonts | 5.3.0 |

All versions are pinned exactly. Remotion packages must always share one version: upgrade them together with
`npx remotion upgrade`.

## One time setup on a new computer

Needs Node.js 20 or newer, ffmpeg, and Python 3 (only for automatic captions).

```bash
cd tools/video3d
```

```bash
npm install
```

```bash
npm run setup
```

```bash
pip install faster-whisper
```

`npm install` also copies MTG's profile photo and face crop from the `brand-assets` branch into `public/brand/`.
`npm run setup` repeats that and downloads Remotion's own headless Chrome (about 100 MB).

## Daily use

Open the studio (live preview with a timeline, scrub frame by frame, edit props):

```bash
npm run studio
```

Render the demo in both orientations to `out/`:

```bash
npm run render:demo
```

Render one composition, or one still frame to check a moment:

```bash
npx remotion render Intro3D-16x9 out/my-video.mp4
```

```bash
npx remotion still Intro3D-9x16 out/check.png --frame=100
```

### On a server or a Claude cloud session (no graphics card)

Three.js needs WebGL. Without a graphics card, switch to software WebGL, or the render stops with
"Error creating WebGL context":

```bash
REMOTION_GL=swangle npm run render:demo
```

Software rendering is slow (the 6 second demo took about 3 minutes per orientation). On MTG's own computer with a
graphics card, the default (`angle`) is much faster.

## Make a new video, step by step

1. **Voice.** Put the final narration in `public/voice/` (MTG's approved HeyGen voice "MTG Master Voice V2" only, or
   lines he already recorded). Never a different voice.
2. **Captions from the real audio:**
   ```bash
   python3 scripts/transcribe.py public/voice/my-video.m4a public/captions/my-video.json
   ```
   Then read the captions back while listening: names like MTG, ALTRUVA or JetUP can be misheard.
   When the narration is made in sections (one HeyGen file per section), use the script's own words with Whisper's
   timing, section by section (more reliable than one long file):
   ```bash
   python3 scripts/align_captions.py public/videos/01/voice public/videos/01/spoken-script.txt public/videos/01/captions.json --sections public/videos/01/timeline.json --replace public/videos/01/caption-replacements.json
   ```
   Existing transcripts (like `tools/invite-horizontal/transcript.json`) or .srt files convert with
   `npm run captions -- <input> <output.json> --from <s> --to <s>`.
3. **Storyboard** the beats (what is said, what the viewer sees, when) before building expensive scenes.
4. **Build the scene.** Copy `src/compositions/Intro3D.tsx` as a starting point and register it in `src/Root.tsx`
   (one composition for 16:9, one for 9:16). Reuse the parts:
   - `src/three/Studio.tsx`: `StudioLights` (premium gold product light, offline) and `CameraRig`.
   - `src/three/BuildingBlocks.tsx`: example of 3D objects that land exactly on spoken words.
   - `src/components/Captions.tsx`: word by word captions, the spoken word in gold, kept inside the safe area.
   - `src/components/PhotoCard.tsx`: MTG's photo, always in a circle with a gold ring (his rule since 7 November 2026). `BrandBar.tsx`: the small brand bar.
   - `src/components/ClosingTrack.tsx`: only the last line of "They Call Me MTG", "Let's get this crypto, wherever
     I go!" (about 3 s), ending with the video (MTG, 7 November 2026). Size the end card with `closingTail()` from
     `src/brand.ts` so the line plays right after his last word.
   - `src/lib/media.ts`: exact audio length, captions loading, word start frames for syncing.
   - Video 01 (`src/compositions/whatif01/`) is the reference for a full long video: one set of scenes for 16:9 and
     9:16, 3D card entrances (`Flip`), a slow camera push-in (`Stage`), Leo clips in gold windows (`LeoClip`) and
     sound effects on spoken words (`Cues`).
5. **Sound (MTG, 7 November 2026): sound effects yes, background music no.** Effects are made in code, so there are
   no licences or copyright claims. The only music is MTG's theme at the end (his rule: no music bed under the video).
   ```bash
   python3 scripts/make_sound.py sfx                                    # effects into public/sfx/ (shared)
   ```
   MTG's rule: soft, warm, suspenseful effects only ("not the ones that almost hurt the ear"). The palette is listed
   at the top of `scripts/make_sound.py` (air, swell, tension, reveal, drop, glow, chime, pluck1 to pluck5, tick, count,
   clock, thud, coin, paper, shutter). It needs only numpy and ffmpeg, and `python3 scripts/make_sound.py check` measures
   every file (warm tone, nothing above 6 kHz, no instant clicks, same loudness). Volumes 0.3 to 0.6 keep every effect
   under his voice; once his theme plays, use only toneless effects (air, thud, tick) so nothing clashes with it.
6. **Check frames before the full render** (one browser for all stills, much faster than `remotion still`):
   ```bash
   npx remotion bundle --out-dir=/tmp/bundle
   node scripts/qc-stills.mjs /tmp/bundle /tmp/qc WhatIf01-9x16 public/videos/01/timeline.json 1:3 1:12.5 8:33
   ```
7. **Preview** in `npm run studio`, then render, then watch the MP4 with sound.
8. **Show MTG the preview.** Never publish or upload without his approval.

## Three rules for 3D in Remotion

- **Animate from the frame number, never from the clock.** Use `useCurrentFrame()` with `interpolate()`,
  `spring()` and `Easing`. Do not animate with `useFrame((state, delta) => ...)` timing or `Date.now()`: Remotion renders
  frames out of order and in parallel, so clock based motion breaks.
- **Load nothing from the internet during a render.** No drei `<Environment preset>` (it downloads HDR files) and no
  3D text fonts from a CDN. Use `StudioLights` (local light formers) and HTML text on top of the canvas, which is also
  sharper.
- **Sync to the audio, not to guesses.** Land actions on caption word times (`wordStartFrames`), and set the video
  length from the real audio file in `calculateMetadata` (see `Intro3D.tsx`).

## The demo: `Intro3D-16x9` and `Intro3D-9x16`

About 6.3 seconds. MTG's own recorded line "Hi, my name is MTG, Your Digital Architect" (cut from the live invite video
at 13.0 to 16.85 s, no new HeyGen credits), his full photo, name and title appearing on his words, eight 3D gold blocks
that land on his eight spoken words and build a cube ("the architect builds"), word by word captions, then the slogan.
Checked in the rendered MP4s: picture, sound (about -15 LUFS, same as the source), caption and block timing, no
overlaps in either orientation.

It is a working test of the setup and a starting point, not a finished production: no closing track (the file is not
in this repository), no outro.

## Folder map

```
tools/video3d/
  remotion.config.ts      render settings (H.264, CRF 18, WebGL mode)
  src/Root.tsx            list of compositions (videos)
  src/brand.ts            colours, brand lines, file paths
  src/fonts.ts            brand fonts, bundled locally
  src/compositions/       one file per video
  src/components/         captions, photo card, brand bar, closing track
  src/three/              3D lights, camera, objects
  src/lib/                media helpers, safe areas for 16:9 and 9:16
  scripts/                transcribe.py, align_captions.py, make_sound.py, qc-stills.mjs, whisper-to-captions.mjs,
                          fetch-brand.mjs
  public/                 voice, captions, music and brand files used by videos
  out/                    rendered videos (not saved in git)
```

## Licence note

Remotion is free for individuals and for companies with up to 3 people; bigger companies need a paid company licence.
Check https://www.remotion.dev/license if MTG's business grows past that. Three.js and the other packages are MIT
licensed; the fonts are SIL Open Font License.

## Troubleshooting

- **"Error creating WebGL context"**: no graphics card. Render with `REMOTION_GL=swangle`.
- **MTG's photo missing / image error**: run `npm run setup` (it fetches `public/brand/` from the `brand-assets` branch).
- **Captions out of sync**: re-run `scripts/transcribe.py` on the final audio after every narration change.
- **Fonts look wrong**: they load from `node_modules/@fontsource`; run `npm install` again.
