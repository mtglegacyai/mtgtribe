# Explainer video spec

Everything in mtg-creative-standard applies (voice, closing track, visuals synced to the final audio, storyboard first,
preview before release). This file adds what is specific to short website explainers.

## Format

- **16:9 horizontal, 1920x1080, 25 fps**, 60 to 90 seconds. Long enough for the 51-second closing track to start about
  50 seconds before the end and sit softly under the voice; short enough to watch in one go. If a topic needs more,
  split it into two videos.
- One idea per video. If the title needs "and", it is probably two videos.
- Captions burned in, with the active word lit, large enough to read on a phone.
- Deliver: the master, a web copy (H.264 with faststart; keep it small enough for phones on mobile data, for reference
  the ALTRUVA explainers are about 2 MB per minute at 720x1280), a poster image, a thumbnail, chapter times, and a short
  posting pack (title, description, hashtags) for YouTube and TikTok.

**Closing track rule (MTG, 8 Nov 2026):** a video longer than 60 seconds gets the full 51.36 s track "They Call Me MTG",
starting 51.36 s before the end, soft under speech (about -14 dB while he speaks) and ending on the last frame; a video of
60 seconds or less gets only its last line ("Let's get this crypto, wherever I go!", 48.38 s to the end of the track)
right after his last word. Mix reference: `tools/jetup-explainers/ex1/mix_ex1.py`.

## Story shape (60 to 90 seconds)

1. **Hook (0 to 5 s):** the question the visitor already has, on screen and in his voice ("Where does your money
   actually sit?"). See mtg-hooks-standard.
2. **The picture (most of the video):** one focal point at a time. Every important noun gets an object, every number
   moves, every relationship gets a connector. Build the picture piece by piece in the order he says it.
3. **The everyday comparison** (minibus taxi, market stall, bus route, queue, seats): show it, connect it to the real
   thing, and say **where the comparison stops**.
4. **The risk or the rule** that matters, said plainly.
5. **The next step:** one clear action, the matching button on the end card, and the page it lives on.

## Visual language

- Icons, emojis, little people, drawings, arrows and connectors, ticks and crosses, counters that count up, money that
  splits, levels that unlock, gauges, phone and laptop mockups. Purposeful only: each one shows something he says.
- Sound effects: only the 9:09 sign-up training's four synthesised sounds (whoosh on scene changes, tick on list items
  and reveals, pop on engagement and key highlights, click on taps), at the training's level, never louder than the voice
  (`tools/video-signature/mix_consistent.py`). Emoji pops above the captions on key words, as in the training.
- MTG's brand bar with the JetUP logo disc, never his photo (MTG, 8 Nov 2026); the site's colours and fonts so the video
  feels like part of the page.
- **Real screens from his step-by-step tutorial recordings** wherever a real tap or button makes the point: zoom on the
  button, spotlight or arrow on it, blur or cover all personal data (names, emails, balances, IDs, addresses, QR codes
  that carry private data). Footage from his own recordings needs no credits.

## End card and calls to action

- **The ending is the 9:09 sign-up training's signature ending** (MTG, 8 Nov 2026: consistency across all his videos):
  fair-play line, HELP SOMEONE START RIGHT (save, share), WE LEARN BEST WHEN WE TEACH OTHERS, IT PAYS TO PAY ATTENTION &
  TAKE ACTION, then the signature outro and end card, all from MTG's banked lines (0 credits) and drawn by
  `tools/video-signature/mtg_ending.py` in 16:9. Explainer #1 is the 16:9 reference (`tools/jetup-explainers/ex1/`).

- **The site address in the final signature** (MTG, 8 Nov 2026): the end card shows the site's address as a large pill
  (for JetUP: mtgtribe.com/jetup) under the slogan, from "I'm MTG, Your Digital Architect" to the very last frame, so it is
  still on screen when the video stops.

- The end card shows the one or two actions that fit the video (for example "Get my Partner link", "Watch the
  step-by-step training", "Join the tribe"), each with MTG's real link for that step written as a short readable
  address, because a button inside a video cannot be tapped. The tappable versions live on the web page right under the
  player and in the PDF.
- Never put a link on screen that MTG has not supplied. If links are still missing, storyboard with placeholders and
  wait for them before the final render.

## Tutorial recordings into chapter clips

When MTG supplies a step-by-step screen recording: keep it as the full tutorial, and also export one clip per part
(each starting on that part's title, ending when the part's result is shown). Place each clip in the matching section of
the page, so a visitor stuck on one step watches only that step. Reuse the strongest moments as footage inside the
explainers.

## Check before showing MTG

Watch the finished file end to end: voice pace even, every visual on its word, captions correct, no em or en dashes on
screen, no personal data in any frame, closing track timing right, loudness about -14 LUFS, true peak below -1 dB, and
the end card readable on a phone. Then send MTG the preview file and wait for approval.
