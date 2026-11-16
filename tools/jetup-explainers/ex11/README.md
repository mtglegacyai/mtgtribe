# JetUP explainer #11: The Infinity Bonus, two strong wheels (15 Nov 2026)

MTG asked for the next explainer on 15 Nov 2026 ("let's craft, and engineer the next explainer video"): #11 in
`tools/learning-system/PLAN.md`, the Infinity Bonus with the 50% rule and the difference rule, for the Partner Plan
"Infinity" section. MTG approved seven new lines the same day ("Yes, record"): one request in MTG Master Voice V3, 49.0 s,
1 credit (503 before, 502 after). **Built and rendered as a preview (15 Nov 2026); not published.**

16:9, 1920x1080, 25 fps, captions burned in, the JetUP logo disc (never MTG's photo), the series' glass style, only the
four signature sounds. Calm, positive copy; JetUP's figures, never an income promise.

## The picture

A bicycle with gears. The gear is your Infinity rate, set by the team's new volume each month (JetUP's scale: $50K 1.5%,
$200K 3%, $500K 4%, $1M 5%, $3M 5.5%, $7.5M 6%, $15M 6.5%, $25M 7%, $40M 7.5%). The trip meter resets every month (only
the month's new volume counts, paid once a month). Two strong wheels: the 50% rule (the strongest line counts for at most
half of a threshold, so Infinity needs at least two strong lines). A partner in your line on their own bicycle: the
difference rule (3% minus their 1.5% leaves you 1.5% on their structure; full rate in all other lines). It opens with a
callback to explainer #6's ten glass floors: Infinity has no depth limit.

## Lines (plan.json)

New (V3, `voice/ex11v3.flac`): nhook, ntop, nbike, nmonth, nfifty, ndiff, nrecap. Banked (0 credits): nshare (explainer
#6's Profit Share line, `explainers/ex6-pack/`), the greeting, close, fair play and signature ending (`explainers/ex4-pack/`).
Speech-to-text hears every line as written (numbers as digits). HeyGen's word times for lines 3 to 7 ran 0.14 to 0.2 s
ahead of the audio: shifted in `lines_ex11.py` (ALIGN).

Facts: JetUP business plan (Oct 2026), full presentation and the "How Partners Grow" one-pager (Downloads); the Partner
Plan page "Infinity" section; `jetup-facts.md` (Infinity from $50K at 1.5% up to 7.5%). "New volume" is JetUP's term and
is not redefined.

## Build (15 Nov 2026)

- Timeline: `make_ex11.py` (voice placement, captions with the number fixes, cues on the storyboard's words, scene windows,
  emoji pops from plan.json, the signature ending's cues) writes `stage/timeline.js`, `kitcues.json` (orient h, links off,
  "Next: step-by-step, part 1"), `sfx_body.json` (9 whoosh, 19 tick, 6 pop, 3 click, never closer than 0.49 s),
  `voice.wav` and `mixcues.json`. T = 119.19 s (1:59), the ending from 72.889 s ('every'), end card 115.109 s. Pauses:
  0.6 s before each new scene, 1.3 s after the difference rule line so its last chip can be read.
- Scenes: hook 0 to 5.77 (explainer #6's ten glass floors and the title, dimmed, from the first frame; the floors light on "Ten levels", the top opens upward to an infinity sign, "No
  depth limit"), Hi 5.67 to 9.2, Profit Share 9.1 to 22.58 (ten 1.5% level bars, "Paid from the 30% share, never from client
  deposits", then the lime Infinity layer on top, from level 1, past level 10), the bicycle 22.58 to 33.8 (the gear
  cassette is the scale, the chain lands on 1.5% on "one and a half" and climbs one gear per step to 7.5% as he says it; the
  trip meter shows the matching threshold), monthly 33.8 to 39.14 (the meter rolls to $0 on "resets", the calendar flips to
  month 2), Rule 1 39.14 to 46.51 (the wheels are two lines: the strongest fills past half and only half counts, the cap
  lights on "at most half"; all other lines fill the other half; the meter counts the counted volume to the $1M example and
  the gear follows it to 5%), Rule 2 46.51 to 57.5 (a partner in your line on a gold bike in the 1.5% gear; 3% minus 1.5%
  leaves 1.5% on their structure; "All your other lines: your full rate"), recap 57.4 to 64.49 (three ticked cards and
  "JetUP's figures · check your partner account"), your turn 64.44 to 72.94 ("See the partner plan", "Join JetUP" tapped
  on its words, mtgtribe.com/jetup).
- Picture: `stage/stage.html` and `stage/engine.js` (every visual a pure function of t; one SVG bicycle drawn once and used
  for you and the partner; the gear always equals `gearOf(meter)`, so the labels, the chain and the trip meter agree in
  every frame). `stage/` also holds `Anton-Regular.ttf`, `jetup-disc.png`, `jetup-disc-small.png` (from ex10); `render.js`
  is ex10's.
- Test stills: `node render.js test <t1,...> test_build`, then
  `python3 ../../video-signature/compose_kit.py test <this dir> test_build`. 48 stills checked on 15 Nov 2026 (two or more
  per body line, t = 0, the ending's start and four composited ending frames); caption lines and off-frame text checked
  over the whole body every 0.2 s.
- Cover: `cover.html` and `shoot_cover.js` (the pill length from kitcues.json; the bicycle is taken from the stage at the
  end of Rule 1), `cover-explainer-infinity-bonus.jpg` (1920x1080, 196 KB) and `.webp` (1280x720, 63 KB).
- Render: `MTG_TRACK=<the closing track> tools/video-signature/build_part.sh <absolute ex11 dir>
  jetup-explainer-infinity-bonus.mp4`. Not rendered yet.

## Preview of 15 Nov 2026

`jetup-explainer-infinity-bonus.mp4`: 119.19 s (1:59), 1920x1080, 25 fps, 22.6 MB, -14.0 LUFS, true peak -2.7 dBFS, no
sample over 0.9, closing track from 67.84 s to the last frame, sounds 19 whoosh, 21 tick, 15 pop, 3 click; speech-to-text
hears every line in order. The first frame shows the ten floors and the title (dimmed) so it reads on its own.
