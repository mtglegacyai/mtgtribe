# JetUP 5 Checks v5.1 (6 November 2026): how it was built

Preview only. Not on the website or any channel until MTG approves. Output: `JetUP_5_Checks_MTG_v5.1.mp4`
(5:25, 1920x1080, 25 fps, -14.7 LUFS, true peak -3.4 dBFS) and a web copy of about 82 MB.

## What changed from v4.2 (5:53)

- **One steady pace.** v4 had stretched MTG's approved voice (0.82 to 1.32x, locally up to 1.75x) to fit the old
  v3 lip timing, which made it slow down and speed up. v5 uses the voice at its natural timing, evens out each
  phrase gently (0.94 to 1.10x, Rubber Band R3, formants kept), and tidies the pauses by type (sentence 0.30 to 0.40 s,
  comma 0.12 to 0.22 s, section 0.55 s). Phrase-to-phrase pace spread went from 16% to 10%, pauses top out at 0.55 s
  (v4: 1.1 s), and the delivery is about 9% brisker.
- **The avatar follows the voice.** The existing Avatar V render (HeyGen video `cb862cd0ccd3c211030c8ff49acf428d`,
  no new render) is re-timed word by word to the new voice. Slow-downs use optical-flow in-between frames, long old
  pauses play at up to 2x, cuts are hidden by a framing change. Lip check (m/b/p closures, MediaPipe landmarks):
  80 to 95% shut on the sound across the video, best offset 0 frames.
- **Script tightened** (cuts are free): removed "You can look it up yourself", "Also know this", "And if it doesn't
  feel right? That's a good decision too" and the weak "Comment below. Which check surprised you most?".
- **Two new lines** in MTG Master Voice V2 (`3931c505632149ceb2bbfecf2778c09c`, engine orca, request
  `17a5f5ef09894d95b7f8da99f7f35cff`, 1 credit): the next step (watch the step-by-step training) and a strong
  comment prompt (comment 1 to 5, the most-picked check becomes the next video). They play over full-screen scenes.
- **Visuals:** MTG's photo as a gold-ringed circle (MTG, 6 Nov 2026), every row, line and number pops in on its spoken
  word, captions light the active word, a CHECK 1 to 5 tracker, punch-in framing at each check, purposeful emoji pops,
  the JetUP mark in the top bar, a new end card that sends viewers to the step-by-step training.
- **Audio:** sharper voice (less mud, more presence and air, gentle compression), soft SFX on reveals, the closing
  track "They Call Me MTG" from 51.36 s before the end, soft under speech, rising after.

## v5.1 polish (same day)

- Avatar speed is Gaussian-smoothed inside each continuous stretch, and every frame that falls between two source
  frames is built with optical flow. Jerky frames: v5 0.89%, v5.1 0.20% (HeyGen original 0.15%).
- Lip map uses word times measured in the render's own soundtrack (`render_words.json`; the old v3 list drifted
  up to 80 ms) with the measured 140 ms lip lead. m/b/p closures on the sound: 95, 96, 88 and 80% in four stretches.
- The cover dissolves into the first card, +30.1% and $1,000,000 count up on their words, softer check hits,
  a light de-esser on the voice, larger small text. Posting pack with the new chapters: `posting-pack-v5.1.md`.

## Rebuild

Scratch layout used: `v5/work` (voice takes `o1_raw.wav`, `o2_raw.wav`, `n1_raw.wav` and the JSON in `data/`),
`v5/raw/avatar_v3.mp4` (fetch with HeyGen get_video, free), `v5/fonts` (Poppins, Anton), `v5/jetup-work` (branch
`jetup-video-work`, for the closing track and GreatVibes), brand images from branch `brand-assets`.
Needs Python 3.12+, numpy, Pillow, opencv-python-headless, pocketsphinx, mediapipe (checks only), rubberband-cli, ffmpeg.

```bash
python3 timeline.py          # voice_v5_dry.wav + tl.json (word times, avatar frame map, cuts, scenes)
python3 render.py info       # events.json
python3 mix.py               # mix_v5.wav
python3 render.py range 0 2031 p0.mp4   # ... four ranges in parallel, then concat and mux
```
