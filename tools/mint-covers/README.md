# MoveMint covers (mtgtribe.com/mint, 28 Nov 2026)

`make.py` writes one HTML per cover, `shoot.js` renders them with Playwright (Google font Manrope, Anton here, Noto Color Emoji):

    python3 make.py && node shoot.js hiw trailer founder part1 part2 yt og

- `hiw`, `trailer`, `founder`, `part1`, `part2`: the page's 16:9 covers. Text on the left, the picture on the right, the middle
  kept clear for the play button (MTG, 16 Nov 2026). Saved as `mint/img/<slug>-cover-1280.webp` and `-640.webp`.
- `yt`: the YouTube thumbnail for the founder presentation (youtu.be/bPdUpYZ1H8k), replacing YouTube's own frame (MTG asked
  for a new one). The finished file is `MoveMint-Founder-Presentation-YouTube-thumbnail-1280x720.jpg`.
- `og`: the page's social preview, `mint/img/og-movemint.jpg` (1200x630, under 200 KB).
- No photo of MTG: the gold "MTG 👑" disc takes its place, as in his MoveMint videos. `rug.jpg` is a still from MoveMint's
  own trailer; `screen1.jpg` and `screen2.jpg` are frames from MTG's redacted tutorials.

- `ytt.html` (with `bolt34.jpg`, a still from the trailer at 0:34): the YouTube thumbnail for the 49 second trailer,
  `MoveMint-Trailer-YouTube-thumbnail-1280x720.jpg` (no duration badge: YouTube adds its own). `node shoot.js ytt`.
- `tiktok.html` (with `bolt-sq.jpg`): the vertical TikTok cover for the trailer, `MoveMint-Trailer-TikTok-cover-1080x1920.jpg`; every word sits inside the
  middle 3:4 part (y 240 to 1680) that TikTok shows in the profile grid. `node shoot-tall.js tiktok`.
