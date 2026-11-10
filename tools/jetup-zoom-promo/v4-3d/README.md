# JetUP Zoom invitation v4, real 3D (7 Nov 2026)

MTG: "use 3D ... 100 times better". There is no separate 3D skill in MTG's account; 3D and depth are in his creative
standard (section 12). Built with three.js (WebGL, rendered in headless Chromium on SwiftShader, about 0.4 s a frame).
Same voice and timing as v3 (voice bank `zoom-invite/i2.mp3`), so no new HeyGen credits.

3D in every scene: polished gold bars dropping on "gold" with rising 3D candles and a coin rain on "single cent"; a spinning
gold crown over MTG; an invitation ticket that flips in, with a 3D TONIGHT stamp; three 3D clocks whose hands spin to
8:00, 7:00 and 11:30 as each country is said; a 3D question mark that turns orange on "burned" and becomes a check on
"come see the facts", with a live chat bubble; giant 3D numbers 1, 2, 3 with a gold stack, a gift box that opens to a
$100 coin, and a staircase being climbed; a warning sign, an opening book and a check; a 3D phone (gold rim) typing
mtgtribe.com/JetUpZoom and tapping Join, then a paper plane with a sparkle trail; gold SEE YOU TONIGHT with a coin burst.
Text, captions and the top bar are HTML over the 3D canvas so they stay sharp.

```bash
npm i three@0.160.0                      # package.json
python3 make_stage4.py                   # stage4/index.html (needs ../parts.txt, stage4/timing.js from v3, Anton-Regular.ttf, jetup-mark.png)
npx http-server . -p 8766 -a 127.0.0.1   # ES modules need http, not file://
node render4.js range 0 1560 frames      # 4 ranges in parallel
python3 mix4.py                          # v3 voice + closing track + 3D sound effects (coin clinks, clock ticks, gift pop)
ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out.mp4
```
