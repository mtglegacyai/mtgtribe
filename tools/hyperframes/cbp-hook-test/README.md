# HyperFrames test: ClickBaitPays hook (TEST, not for posting)

Made 26 Nov 2026, with MTG's OK, to test HeyGen's HyperFrames (HTML to video) beside our own engine. A silent 13.5 s
vertical clip, 1080 x 1920, 30 fps: "GOT A LINK?" with the programs people promote, "GET IT SEEN.", real people
arriving at a link ("every click day"), then the ClickBaitPays logo, mtgtribe.com/cbp, "A traffic source, not an
investment." and MTG's signature line. Copy from `tools/cbp/MESSAGE.md`. No voice, no music, no HeyGen credits.
Not a finished video: a real one gets MTG's V3 voice, the closing track's last line and the signature ending.

## Build it

From this folder, with the settings that keep tracking off and use the container's browser:

```bash
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium HYPERFRAMES_CHROME_SANDBOX=0
npx -y hyperframes@0.9.92 check --json
npx -y hyperframes@0.9.92 snapshot --at 0,4.2,7.75,13 --no-end --output /tmp/snaps
npx -y hyperframes@0.9.92 render --output /tmp/cbp-hyperframes-test.mp4
```

Rendered in 41 s on 26 Nov 2026. `check` passes. Never run `publish` (it uploads to HeyGen; removed from package.json)
or the `events` usage beacon without MTG's OK. Renders and `.hyperframes/` stay out of the repo.

## What is in it

- `index.html`: the composition (four beats, one GSAP timeline, every frame a function of time).
- `compositions/components/headline-slam.html` and `cta-lockup.html`: HyperFrames registry blocks (Apache 2.0,
  heygen-com/hyperframes), edited for vertical: two-line headline, smaller overshoot, Orbitron spacing, larger
  microcopy, narrower lines to stay out of TikTok's button rail.
- `assets/fonts/`: Orbitron 900 (`f1.ttf`), Poppins 600 (`f2.ttf`) and 800 (`f3.ttf`), from Google Fonts (SIL Open
  Font License). `assets/cbp-disc.png`: the ClickBaitPays logo disc from `tools/cbp/brand/`.

Lessons from this test live in `.claude/skills/mtg-skill-library/references/video-story.md`.
