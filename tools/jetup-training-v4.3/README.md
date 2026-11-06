# JetUP + TAG Markets sign-up training v4.3 (6 November 2026): circle photo, corrected skin tone

v4.2 showed MTG's photo as a rounded square in its original, lighter tone (opening card, slogan, "You are the best",
signature, end card) plus a small face badge in the top bar of every frame. MTG asked for the circle photo everywhere,
with his real skin tone from the 5 Checks video. v4.3 changes only the photo. Words, voice, music, timing, screens and
captions are the approved v4.2, and the audio track is copied bit for bit.

## How it was made (no HeyGen credits)

The v4.2 narration audio was not kept, so the video could not simply be re-rendered. Instead:

1. The v4.2 engine (`jetup-video-work` branch, `jetup-work/engine/tutorial/render_tut2.py`) was run twice for every
   frame that shows the photo or where the picture moves: once as v4.2 (old square card, old face) and once with the
   gold-ringed circle card and the corrected photo (`drive.py`, `CIRCLE=1`). Same engine, same fonts, same timing.
2. `composite.py`: live v4.2 frame + (circle render minus square render). Everything that is not the photo cancels
   out, so the text and screens stay the original pixels, with no seams. On all other frames the static badge change is added.
3. `aligncheck.py`: every engine frame was checked against the live frame (badge median 7.1, whole frame median 2.2,
   no frame above 15: compression noise only, so every patched frame is the same moment).

Rendered: 1,273 of 13,717 frames (17.68 to 24.00 s opening card, 514.66 s to the end, and the short camera moves).
Missing guide screenshots were blank stand-ins; they are identical in both renders and cancel out.

Covers `jetup/img/cover-signup-training*.{jpg,webp}` are the corrected first frame.
