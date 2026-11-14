# CoinZoom how-to clips, narrated by MTG (series, from 14 Nov 2026)

MTG sends CoinZoom's own short, silent how-to clips and asks: "Use my voice to explain what is going on in this video."
Each one becomes a 16:9 video in the series look of his explainers: his greeting, an In this video list, the clip in a
slim gold-titanium window that zooms to every tap, his narration with captions, a recap, "Now it's your turn", and his
signature ending. **Previews only; nothing here is published.** The raw clips and the rendered videos are not in the
repository.

| # | Folder | Clip | Video | New voice | Status |
|---|---|---|---|---|---|
| 1 | `01-virtual-card/` | How to Find Your Virtual CoinZoom Visa Debit Card in the App (17 s, 1280x720) | 1:54 | 756 chars, 47.1 s, 1 credit | MTG: "Excellent!" (14 Nov 2026) |
| 2 | `02-load-cash/` | How to Load Cash into your CoinZoom Account (18 s, 1920x1080, 60 fps) | 1:58 | 797 chars, 50.1 s, 1 credit | preview, 14 Nov 2026 |

Settled with MTG (video 1, 14 Nov 2026, approved as "Excellent!"): the **official CoinZoom logo disc** sits where the
JetUP disc sits in JetUP videos (never his photo), and the url pill and end card show **mtgtribe.com** (no CoinZoom page
or link of his on the site yet; one line in `engine/env.sh`, `MTG_URL`).

## The recipe for the next clip (copy `02-load-cash/`)

1. Frames: `ffmpeg -i clip.mp4 -vf fps=30 -q:v 1 -qmin 1 <video dir>/src1080/f%04d.jpg` (or `src720/`). Map the clip:
   contact sheet every 0.5 s, a motion list per frame, zoomed crops of every phone screen (exact labels), the frames
   where CoinZoom's own tap circles show (hold the frame before them), a frame of the plain background for the plate.
2. Facts: only what the clip shows, checked against coinzoom.com or support.coinzoom.com; no fee or limit numbers in the
   voice (they change by store and over time; point to the screen instead). Calm and positive (MTG, 8 and 9 Nov 2026).
3. Script: "In this video, I'll show you how to ...", "N quick steps: ...", one line per step, a short tip, the result,
   "Let's recap. You ...". Write "Coin Zoom", "U S", "Seven Eleven", "C V V" so he says them right; `lines.py` merges
   them back for the captions. About 800 characters is one credit. One create_speech request, MTG Master Voice V3
   (`65f1b9ff3f1e418496de5715a801e7dd`), no model, no break tags, one paragraph per pause, with timestamps.
4. `lines.py` (NEW list: key, first word, last word, caption text), `../engine/words.py .`, then `make_tl.py`: voice
   order and gaps, the source segments (holds and short plays of the clip's own transitions), camera moves, rings, taps,
   chips (`'L'` puts a chip left of the phone), step pills, privacy masks, the plate, the panels' texts.
5. Test stills: `python3 ../engine/render.py . test <t1,t2,...> test` and `python3 ../engine/sheet.py test sheet.jpg 0 8`.
6. Build: `../engine/build.sh . <out.mp4>` (frames on 4 workers in about 70 s, the one signature mix, x264 CRF 18).
7. Checks: `../engine/ocr_scan.py <out.mp4> ocr` (every second frame, zero flags; private patterns in
   `~/.tutorial-private-patterns.tsv`, never in the repository), `../engine/stt.py <out.mp4>` (every line in order),
   loudness (-14 LUFS, true peak under -1.5 dB), brightness jumps (only planned fades), contact sheet every 3 s.
8. Cover: `cover/cover.html` + `cover/shoot.js` (1920x1080 jpg, 1280x720 webp), a real screen from the clip.

## Privacy, per video

- Video 1: CoinZoom's demo card shows a full card number, a name and an expiry: blurred under "Your card number",
  "Your name", "MM/YY" in every frame the details screen can show (both crossfades included). The Spend screen's
  USD 16.80 was left as in CoinZoom's clip.
- Video 2: the one-time barcode and its number are blurred under "Your barcode"; CoinZoom's demo wallet balance
  (BAL / AVAIL) under "Balance hidden" and the coin amounts column blurred, so no balance reads as MTG's.
- The blur is taken from each frame itself, so it follows the clip's own fades; the labels fade with how fully the
  screen is in (measured against a frame where it is fully in).

## Engine (`engine/`)

- `render.py <video dir> range|test ...`: every frame in Python (PIL) from the video's `timeline.json`: the explainer
  stage, the window, the camera, the plate (while zoomed in, the clip's big side text is replaced by its own plain
  background, fully from 1.2x), the privacy blur, rings, taps, chips, pills, panels (3 or 4 rows and recap cards),
  captions with the spoken word lit, emoji pops, and the signature ending.
- `mtg_ending.py`, `mix_consistent.py`: `tools/video-signature/` (working branch) with one change: fonts, icons, the logo
  disc and the address come from `MTG_FONTS`, `MTG_ICONS`, `MTG_LOGO`, `MTG_URL` (JetUP defaults unchanged).
- `fetch_bank.sh`: the banked takes (sign-up training t1, tutorial p1v2, the explainer #4 pack) into `../bank/`.
- `words.py`, `stt.py` (faster-whisper small.en), `ocr_scan.py` (tesseract, one thread per worker), `sheet.py`,
  `build.sh`, `env.sh`, `coinzoom-disc.png` (the mark from CoinZoom's official logo SVG on coinzoom.com, 1024 px).
- Local assets (not in the repository) in `assets/`: Poppins and Manrope (fontsource, converted to TTF), Anton and
  Great Vibes (`jetup-work/engine/fonts/`), lucide-static icons, the closing track
  (`jetup-work/audio/they-call-me-mtg-closing-track.mp3`).

## Previews of 14 Nov 2026

1. `coinzoom-find-your-virtual-card-mtg.mp4`: 1:54 (114.07 s), 16.1 MB, -14.1 LUFS, true peak -2.6 dBFS, closing track
   from 62.73 s; speech-to-text hears every line in order; privacy OCR of 1,711 frames: 0 flags, with a positive
   control (the same scan on the unmasked details frame finds the number, name and expiry in all four passes).
2. `coinzoom-load-cash-mtg.mp4`: 1:58 (117.76 s), 17.0 MB, -14.0 LUFS, true peak -2.6 dBFS, closing track from
   66.41 s; speech-to-text hears every line in order; privacy OCR of 1,766 frames: 0 flags, with a positive control (on
   the unmasked frames the same scan finds the barcode number and the wallet balances); brightness: only planned fades.
