# MTG's profile photo: skin tone matched to the 5 Checks video (6 November 2026)

MTG: "I look too light in the picture, but my real skin colour is that in the video." The photo's skin was measured
against his skin in the 5 Checks video and moved to match. Only skin moves: the shirt, the watch, the sign, the plants,
the eyes and the background stay exactly as they were.

## What was measured (CIELAB, face skin, median)

| | L (lightness) | a (red) | b (yellow) |
|---|---|---|---|
| Old photo | 62.7 | 33.8 | 37.9 |
| 5 Checks video (3 frames) | 46.1 | 14.9 | 17.6 |
| New photo (version D, chosen), measured | 47.3 | 19.6 | 22.6 |

Version D shifts lightness by the full measured gap and the colour by 85% of it (full colour matching looked grey on the
photo's warm sunset light). The soft mask edges keep the measured result slightly above the target. Version C
(70% colour) was the warmer alternative.

## Files made with it

- `assets/tribe/mtg-profile-photo-v2.png` (1254 px master), `mtg-photo-round-720-v2.webp/.jpg`, `mtg-photo-round-1000-v2.webp`,
  `mtg-photo-720-v2.jpg`, `mtg-face-200-v2.webp`, `jetup/img/mtg-photo-480-v2.webp`, `mtg-photo-800-v2.webp`
- `assets/tribe/og-tribe.jpg` (share image, skin recoloured in place)
- Small gold-ring badges with the corrected circle face swapped in: `assets/og-home.jpg`, `assets/tribe/og-jetup.jpg`,
  `buy-cntn-south-africa/img/og-buy-cntn-south-africa.jpg`, `jetup/img/cover-signup-training.*`
- The 5 Checks video (v5.2) and the sign-up training (v4.3) use the corrected photo as a circle.

## Tools

- `tone.py`: measures photo and video skin (MediaPipe selfie_multiclass segmentation) and writes versions.
- `recolor.py in out [x0,y0,x1,y1]`: applies the same shift to any image that contains the photo (eyes protected).
- `recolor_small.py in out cx,cy,r`: the same for a tiny face (upscales the badge before segmenting).
- `badge_swap.py in out cx,cy,r_out,ring_w`: puts the corrected circle face inside an existing gold-ring badge.

Needs numpy, Pillow, opencv-python-headless, mediapipe (`selfie_multiclass_256x256.tflite`, `face_landmarker.task`).
