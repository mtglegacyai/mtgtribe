# JetUP explainer #10: Know your numbers, the Exposure Calculator (14 Nov 2026)

MTG asked for the next explainer on 14 Nov 2026 ("Let's cook the next explainer video"): #10 in
`tools/learning-system/PLAN.md`, the Exposure Calculator walkthrough. MTG approved six new lines the same day ("Yes,
record (1 credit)"): recorded in one request in MTG Master Voice V3, 44.8 s, 1 credit (42 before, 41 after).
**Built and rendered as a preview (14 Nov 2026); not published.**

16:9, 1920x1080, 25 fps, captions burned in, the JetUP logo disc (never MTG's photo), the series' glass style, only the
four signature sounds. Calm, positive copy: know your numbers before you start (MTG, 8 and 9 Nov 2026: inform, never
frighten). Explainer #3 (Amplify 24x) already shows the calculator for about 8 s; this one walks through it tap by tap.

## The picture

Checking the map before a road trip: you know the distance before you drive. The calculator is your map for Amplify.
The rest of the video is the real calculator page (mtgtribe.com/jetup/tools/exposure-calculator/) in a laptop frame,
tap by tap: the training example ($150 + $100 bonus, 24x), the balance $250 and the exposure $6,000, the three fields,
the price move slider (1% on $6,000 is $60, both ways), the two last results (2.5% equals your own $150, 4.17% equals
the whole balance), the page's own loss limit note, and the recap.

## Lines (plan.json)

New (V3, `voice/ex10v3.flac`): nhook, nex, nown, ndrag, nlines, nrecap. Banked (0 credits): six, expo, swings
(sign-up training t1 and 5 Checks), nlimit (explainer #3's V3 line) from `explainers/ex3-pack/`; the greeting, close,
fair-play lines and signature ending from `explainers/ex4-pack/`. Speech-to-text hears every line as written (numbers
as digits). HeyGen's word times for lines 2 to 6 ran 0.15 to 0.2 s ahead of the audio: shifted in `lines_ex10.py` (ALIGN).

Facts: the calculator page itself (`jetup/_build/pages_tools.py` build_exposure) and `jetup-facts.md` (24x Amplify,
the loss limit 10%, 5% with a community token). No return figures.

## Build (14 Nov 2026)

- Screens: `calc_shots.js` (repo served on port 8770 with `npx -y http-server@14.1.1 /home/user/mtgtribe -p 8770 -s -c-1`)
  shoots the real calculator page at 1280x800 (device scale 2) into `stage/calc/`: `top` (as it opens, no example lit),
  `pre`, `calc` (after tapping "Training: $150 + $100": 150, 100, 24, balance $250, exposure $6,000), `f_own`, `f_bonus`,
  `f_mult` (each field focused), `m00` and `mp02`..`mp10`, `mn02`..`mn10` (the price move from 0 to +1% and -1% in 0.2
  steps, scrolled so the slider sits mid-screen; $60 and -$60 at 1%), `lines` (the last two results, 2.50% and 4.17%) and
  `note` (the loss limit note), plus `boxes.json` / `boxes.js` (every tap and highlight target per shot). The side menu
  is folded away (the page's own state); no overlay, cookie bar or personal data on this page.
- Picture: `make_ex10.py` (timeline, captions, cues, kit cues, body sounds, voice.wav, mixcues.json), `stage/stage.html`
  and `stage/engine.js` (the road map hook, the laptop camera over one document, spotlight, highlight boxes, taps, chips,
  recap, your turn). `stage/` also holds `Anton-Regular.ttf`, `jetup-disc.png`, `jetup-disc-small.png` (from ex9).
- Test stills: `node render.js test <t1,...> test_build`, then
  `python3 ../../video-signature/compose_kit.py test <this dir> test_build`.
- Cover: `cover.html`, `shoot_cover.js` (the pill length comes from kitcues.json), `cover-explainer-know-your-numbers.jpg`
  (1920x1080) and `.webp` (1280x720).
- Render: `MTG_TRACK=<the closing track> tools/video-signature/build_part.sh <absolute ex10 dir>
  jetup-explainer-know-your-numbers.mp4`. Not rendered yet.

## Preview of 14 Nov 2026

`jetup-explainer-know-your-numbers.mp4`: 123.12 s (2:03), 1920x1080, 25 fps, 22.1 MB, -14.0 LUFS, true peak -2.6 dBFS, no
sample over 0.9, closing track from 71.77 s to the last frame, sounds 18 whoosh, 22 tick, 14 pop, 3 click; speech-to-text
hears every line in order. Render: `MTG_TRACK=<closing track> tools/video-signature/build_part.sh <absolute ex10 dir>
jetup-explainer-know-your-numbers.mp4`. Known: the real page shows its "-1.0%" readout in its own pink, kept as the real
page; while the slider returns to 0 the page briefly shows +$24 at +0.4%.
