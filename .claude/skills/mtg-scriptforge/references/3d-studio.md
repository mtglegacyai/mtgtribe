# The 3D studio in any website's project

Three.js (React Three Fiber) inside Remotion, which handles the timeline, word synced captions, audio and rendering.
The same studio works for every MTG website.

## Where it lives

- In the mtgtribe.com repository it is `tools/video3d/` (the master copy).
- In the account version of this skill it is bundled as `kit/video3d/` (in this skill's base directory).

## Install it in a site's project (once per project)

1. If the project already has `tools/video3d/package.json`, skip to step 3.
2. Copy the kit, never into the site's root or a published content folder:
   ```bash
   mkdir -p tools && cp -r "<this skill's base directory>/kit/video3d" tools/video3d
   ```
3. Install (needs Node.js 20 or newer and ffmpeg). `npm install` also fetches MTG's photos from the brand-assets branch
   of mtglegacyai/mtgtribe; `remotion browser ensure` downloads Remotion's headless Chrome (about 100 MB):
   ```bash
   cd tools/video3d && npm install && npx remotion browser ensure
   ```
4. For captions from audio: `pip install faster-whisper`.
5. Check it works by rendering one frame of the demo. On a machine without a graphics card (cloud sessions) use
   software WebGL:
   ```bash
   REMOTION_GL=swangle npx remotion still Intro3D-16x9 out/check.png --frame=100
   ```
   Open the PNG: MTG's circle photo, the gold blocks, the captions and the brand bar should all be there.

The kit's own `.gitignore` keeps `node_modules/`, `out/`, MTG's photo copies and the closing track out of git. Static
sites publish what is in the repository, so never put private files in `tools/`.

## Use it

Read `tools/video3d/README.md`: make a new composition from `src/compositions/Intro3D.tsx` (a short demo) or follow
`src/compositions/whatif01/` (a full long video in 16:9 and 9:16 with Leo, sound cues and MTG's closing theme), captions with
`scripts/transcribe.py` or `scripts/align_captions.py --sections`, sound with `scripts/make_sound.py` (effects need the
GrowKaz Stickman plugin's sound kit and `pip install scipy`; the 21 made for video 01 are already in `public/sfx/`),
frame checks with `scripts/qc-stills.mjs`, preview with `npm run studio`, render with
`npx remotion render <id> out/<name>.mp4`.

Rules: animate from `useCurrentFrame()`, never the clock; load nothing from the internet during a render; set the
video length from the real audio; keep 16:9 as 16:9 and 9:16 as 9:16.

Licence: Remotion is free for individuals and companies of up to 3 people (remotion.dev/license).

## Keep the copies in step

When the master copy in mtgtribe changes, rebuild the account skill from the mtgtribe repository and give MTG the new
file to upload:

```bash
python3 tools/skills/package_skill.py mtg-scriptforge
```
