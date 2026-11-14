# CoinZoom: "How to Find Your Virtual CoinZoom Visa Debit Card in the App", narrated by MTG (14 Nov 2026)

MTG sent CoinZoom's own 17-second silent clip (1280x720, title card, "Spend" tab, "Reveal", double tap to confirm, card
details, closing photo) and asked: "Use my voice to explain what is going on in this video." This folder builds the
narrated version in the series look of his 16:9 explainers, with his signature ending.
**Built and rendered as a preview (14 Nov 2026); not published.** The raw clip and the rendered video are not in the
repository.

## What is in it (1:54, 1920x1080, 30 fps)

1. Greeting (banked): "Hi, my name is MTG, Your Digital Architect." "Thank you for taking the time to watch this video."
   over CoinZoom's title card, which is also the first frame (the cover).
2. In this video panel: Tap **Spend**, Tap **Reveal**, **Double tap** to confirm; "Take your time. You can pause any step
   and follow along with me." (banked).
3. The clip, in a slim gold-titanium window, slowed to his voice: "activated" photo, step 1 (ring and tap on the Spend
   tab, gold ring on the card), step 2 (Virtual Card, tap Reveal), step 3 (Review virtual card details, double tap),
   the card details (number, name, expiry, CVV, tap Copy), "Keep these details private, and only enter them when you pay
   online", CoinZoom's own closing photo and line ("Setup recurring payments and get rewards for all your online
   shopping!", shown as CoinZoom wrote it, not narrated).
4. Recap (three cards tick on his words), "Simple, right? Now it's your turn." (banked), then the signature ending
   (banked, 0 credits): fair play, save and share, WE LEARN BEST WHEN WE TEACH OTHERS, IT PAYS TO PAY ATTENTION & TAKE
   ACTION, not financial advice, thank you, massive action, YOU ARE THE BEST, Crypto-Regards, end card.

Choices to confirm with MTG: the **official CoinZoom logo disc** takes the place where the JetUP disc sits in JetUP videos
(top bar, "Now it's your turn", slogan, signature, end card; never his photo), and the url pill and end card show
**mtgtribe.com** (there is no CoinZoom page or CoinZoom link of his on the site yet). Both are one line in `build/env.sh`.

## Voice

New lines: MTG Master Voice V3 (`65f1b9ff3f1e418496de5715a801e7dd`), one request, no model or engine override, no break
tags, 756 characters, 47.1 s, **1 credit** (6 before, 5 after), text in `voice/czv3.txt`, the take in `voice/czv3.flac`
(the same samples as HeyGen's WAV), HeyGen's word times in `voice/czv3_words.json`. Written "Coin Zoom" and "C V V" so
he says them right; captions show CoinZoom and CVV. Speech-to-text hears every line as written.
Banked (0 credits): sign-up training t1 (hi, take your time, pause), tutorial p1v2 (thank you for taking the time),
explainer #4 pack (Simple, right? and the whole signature ending). Branch `jetup-video-work`, `jetup-work/voice-bank/`.
To add the new take to the voice bank: copy `voice/czv3.*` to `jetup-work/voice-bank/explainers/` and add its rows to
`sentences.tsv`.

## Privacy

CoinZoom's demo card shows a full card number, a cardholder name and an expiry. In every frame where the details screen
can show (source frames 414 to 462, including both crossfades), those three fields are blurred and covered by labelled
pills ("Your card number", "Your name", "MM/YY"). The blur is taken from the frame itself, so it fades with the
crossfades and nothing readable is left even at half opacity. Check: `build/ocr_scan.py` OCRs every second frame of the
finished video (whole frame and the window, normal and inverted, two page modes) for the digits, the name, the expiry and
any long number. The USD 16.80 shown on the Spend screen is CoinZoom's own demo figure (not MTG's), kept as in their clip.

## Build

`build/` (copy it next to a `src720/` folder with the clip's frames, `ffmpeg -i clip.mp4 -q:v 1 -qmin 1 src720/f%04d.jpg`):

- `lines.py` cuts every line (new take on HeyGen's word times snapped to the silence, banked lines at their bank cut
  points, all levelled to the banked ending lines), `words.py` adds word times (HeyGen +0.10 s, measured against
  speech-to-text on this take; speech-to-text for the four older lines).
- `make_tl.py`: voice placement, which source frame shows when, camera moves, rings, taps, chips, step pills, panels,
  captions, emoji pops, the ending's cues (`kitcues.json`), body sounds (`sfx_body.json`), `voice.wav`.
- `render.py`: every frame in Python (PIL), the stage of the explainers, the window, the privacy blur, and the signature
  ending drawn by `mtg_ending.py`. While the camera is zoomed in, CoinZoom's large side text is replaced by their own
  plain green background (frame 165, pixel-identical elsewhere), so no half-cut words show at the window edge.
- `mtg_ending.py` and `mix_consistent.py` are `tools/video-signature/` (working branch) with one change: fonts, icons,
  the logo disc and the address come from `MTG_FONTS`, `MTG_ICONS`, `MTG_LOGO`, `MTG_URL` (JetUP defaults unchanged),
  so the same ending serves any platform. Fonts: Poppins and Manrope (fontsource, converted to TTF), Anton and Great
  Vibes (`jetup-work/engine/fonts/`), icons: lucide-static.
- `build.sh <out.mp4>`: timeline, frames (4 workers, about 70 s), the one signature mix (-14 LUFS, true peak -2.8 dB,
  the full 51.36 s closing track ending on the last frame), x264 CRF 18, AAC 256k.
- `cover/`: `screen.py` (the video's own details screen, masked), `cover.html`, `shoot.js` (1920x1080).
- `coinzoom-disc.png`: the CoinZoom mark from CoinZoom's official logo SVG (coinzoom.com), rendered at 1024 px.

## Preview of 14 Nov 2026

`coinzoom-find-your-virtual-card-mtg.mp4`: 1:54 (114.07 s), 1920x1080, 30 fps, 16.1 MB, -14.1 LUFS, true peak -2.6 dBFS,
largest sample 0.74, closing track from 62.73 s to the last frame, sounds 19 whoosh, 15 tick, 11 pop, 5 click.
Checks: speech-to-text hears every line in order (and the track's "Wherever I go" at the end); privacy OCR of every
second frame (1,711 frames): 0 flags, with a positive control (the same scan on the unmasked details frame finds the
number, the name and the expiry in all four passes); brightness: only planned fades (the In this video panel now fades
out over the clip's own cut, so the bright title card no longer flashes back at 21 s); first frame: CoinZoom's title
card in the window, MTG's top bar. Cover: `coinzoom-find-your-virtual-card-cover.jpg` (1920x1080) and `.webp` (1280x720).
Render: about 70 s of frames on 4 workers, then the mix and the encode.
