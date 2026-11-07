# Build pipeline and site placement

Reference builds: `tools/jetup-tutorial/part1/` and `tools/jetup-tutorial/part2/` (part 2 is the cleaner one to copy:
`make_tl_p2.py` + `shots_p2.py`, no time warp; `clipdir`, `planhead` and `nsteps` come from the timeline)
- `lines.py`: cuts banked and new lines (`lines.json`), `words.json` word times.
- `vo_v2.py` voice placement; `shots_v2.py` the edit (shots with clip, source start and speed, camera key points, rings,
  taps, chips, steps, scenes, window spans, plan items and cues); `make_tl3.py` builds `stage/timeline.js` and `voice.wav`.
- `stage/stage.html` + `stage/engine.js`: the scenes (intro, plan, link, window, tip, mail, next, outro).
  Needs `Anton-Regular.ttf`, `jetup-mark.png`, `mtg-face.png`, `mtg-photo-round.jpg` beside it.
- `render.js range a b frames` (4 workers in parallel), `mix_p1.py` (voice, light sound design, bed, closing track,
  loudnorm -14 LUFS, TP -2.8 target, because AAC raises the true peak by about 0.5 to 1 dB; measure the encoded file),
  ffmpeg x264 CRF 18, AAC 192k, faststart. `mix_p2.py` filters by FFT: the old sample loop and direct convolution took
  over 15 minutes under load, the FFT version 25 seconds.
For a new part: copy the folder, write the new shot list from the recording map, keep the scenes, change texts and lists.

Checks: OCR privacy scan (zero flags), contact sheet every 3 s, speech-to-text of the final audio (every line, in order),
loudness, brightness jumps (only planned fades), the cover frame. A cut between a dark page (Cloudflare check) and a white
page flashes: give that shot `xfade=.35` (the incoming frame sits above the outgoing one: `#imA` z-index 2, `#imB` 1) and
end the outgoing shot before the page itself changes. Look at the contact sheets of every redacted clip before building:
the OCR alone missed a password manager sheet (see `tools/tutorial-redact/README.md`).

Site placement (recommended to MTG 7 Nov 2026): the step-by-step page of the site (JetUP: /jetup/get-started/).
Each part's video in the slim phone frame (`phone()` in the JetUP layout) at the top of its part, and a "Step-by-step
videos, one per part" strip near the top of the page. Video file in `jetup/media/`, its series thumbnail as the cover (see below), VideoObject structured data.
Also list each part on the site's Videos page (`#step-by-step`).

Thumbnails (MTG, 7 Nov 2026: "make sure all the videos have a beautiful thumbnail"): `tools/jetup-tutorial/thumbs/`
(`make_thumbs.py`, `shoot.js`). One series look: lime "JETUP STEP BY STEP" pill, a huge gold Anton "PART N", a 92 px
title with the key words in lime, his full photo in a 476 px circle with the gold ring (left), a tilted gold-titanium
phone with a real redacted screen from that part (right), a green-tick success badge (the real success check of the
part), "MTG 👑 | YOUR DIGITAL ARCHITECT". Keep clear: the camera island (top centre), the play button (centre) and the
duration tag (bottom left) of the site's phone card. Export a 1080 x 1920 jpg and a 720 x 1280 webp, new file name
per version so caches refresh. Check it at 270 px wide, as the site shows it. The player closes itself at the end (standing rule).
