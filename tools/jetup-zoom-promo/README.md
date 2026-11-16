# JetUP Zoom presentation, Saturday 7 November 2026: promo video and flyer (MTG, 7 Nov 2026)

Status: **preview sent to MTG, not published by us.** The link **mtgtribe.com/JetUpZoom** is live (`/JetUpZoom/`,
any spelling via `404.html`) and opens the Zoom meeting (ID 405 692 8305, passcode built into the link).

## Promo video (9:16, 1080x1920, 30 fps, 50.5 s, -14 LUFS)

- Voice: only lines MTG already approved in **MTG Master Voice V2** (voice bank on branch `jetup-video-work`,
  `jetup-work/voice-bank/`): no new HeyGen lines, no credits. `timeline.py` lists every clip (file, source times) and
  trims to forced-alignment word times so no neighbouring word leaks in.
- Story: hook (Automated gold trading?), "Hi, my name is MTG", the simple picture (TAG Markets broker, your account in
  your own name, CopyX, Sonic AI trades gold, XAU/USD), the $100 promo and its rules, TONIGHT with the three times,
  CTA mtgtribe.com/JetUpZoom with a tap, not financial advice, end card with the crown, MTG and the slogan.
- Closing track "They Call Me MTG" plays from the start (0.85 s into the track) so it ends exactly on the last frame,
  about 14 dB under speech, rising in the music-only parts.
- Captions follow the voice word by word. The first frame already shows the hook (WhatsApp uses it as the preview).
- **No photo of MTG in this video (MTG, 7 Nov 2026: "Don't put me in the video").** The greeting and the end card show a
  gold crown and "MTG" (with a drawn gold ring on the greeting); the top bar is text only. His voice stays.

Rebuild (scratch folder with `vb/` voice bank files, `track.mp3` and `stage/jetup-mark.png`):

```bash
python3 timeline.py      # voice.wav + stage/timing.js
python3 make_stage.py    # stage/stage.html (uses parts.txt: flyer artwork)
python3 mix.py           # mix.wav
node render.js range 0 1515 frames   # split into 4 ranges in parallel
ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out.mp4
```

## Flyer (square)

`flyer/make_simple.py` builds the clean version MTG chose (fewer words; Zoom details go in the caption),
`flyer/flyer-v1-busy.html` is the first, fuller version. Render with `flyer/render.js`.
