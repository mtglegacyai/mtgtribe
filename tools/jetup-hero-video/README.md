# JetUP hero background video (MTG, 10 Nov 2026)

MTG: "Find me or create a similar video with no audio, HD, I want you to put it as a background on the mtgtribe.com/JetUp
page, replacing the current candlestick chart." Made in code, in JetUP's colours, so there is no stock licence to track.

- `stage/index.html`: the scene in three.js (r160): a night Earth with real city lights (`stage/night.jpg`, NASA Earth
  Observatory "The earth at night", public domain, from Wikimedia Commons), purple network arcs with travelling light, a
  slim gold beam rising from the horizon (Cairo), twinkling stars and a slow camera drift on a closed path, so the
  20-second loop is seamless. URL settings: `w`, `h`, `fov`, `cy`, `cz`, `ty`, `lat0`, `lon0`, `beam`.
- `render.js`: `node render.js range <from> <to> <outDir> [w h]` renders frames (needs `three` in `node_modules` next to
  `stage/`, and a static server on port 8772 serving this folder). 30 fps, 600 frames.
- Wide film: 1920x1080, defaults. Upright film for phones and upright tablets: 720x1280 with
  `Q="fov=60&cy=.6&cz=1.7&ty=.7"`.
- Encode: `ffmpeg -framerate 30 -i f%04d.png -c:v libx264 -profile:v high -preset slow -crf 23 -pix_fmt yuv420p
  -movflags +faststart -an` (crf 25 for 720p, 24 for the upright film). No sound track.
- On the site: `jetup/media/jetup-hero-earth-1080.mp4` (4.5 MB), `-720.mp4` (1.7 MB), `-portrait.mp4` (2.2 MB), stills
  `jetup/img/jetup-hero-earth*.webp`. `jetup/assets/jetup.js` shows the still at once, loads the right film after the
  page, never with reduced motion or data saver, and pauses it off screen. Credit on the JetUP disclaimer page.
- Build-only folder: keep it off the live site when publishing (like the other tools).
