# MTG TRIBE invite, horizontal 16:9 and vertical 9:16 (DRAFTS, not published)

Status (5 November 2026): horizontal and vertical drafts rendered and sent to MTG for review. Not on the website yet.
The current vertical invite (`/assets/mtg-tribe-invite.mp4`) stays live until MTG approves a replacement.

## What it is

- 1920x1080, 30 fps, 2:49 (2:48.8 after the voice fix). Built from the approved vertical invite: MTG's own voice and avatar, no HeyGen, no new voice.
- The voice is only trimmed in silences (`edl.json`): "Thank you for taking the time to watch this video", one "So," and three long pauses.
  Everything from 88.79 s in the source onwards is untouched, so the closing track "They Call Me MTG" still starts exactly
  50 seconds before the end.
- 13.4 s cinematic cold open (on-screen words and sound design only, no voice): burned before, lost money, lost trust,
  even got banned, still watching, you haven't given up, you're not done, it's not over until it's over, NOW.
- New on-screen punchlines and visual metaphors: every step counts, the door and invitation, learn take action grow,
  not just one, lower risk not no risk (where the analogy stops), a seat for you, blueprint build roads, no strings attached,
  shouting isn't leading, a candle loses nothing by lighting another, built not bought, gym streak, your seat is waiting,
  the YOU member card with a crown.
- Every CTA from the original: mtgtribe.com/group, Join the WhatsApp tribe, @joinmtgtribe on TikTok,
  WhatsApp MTG: 072 171 4626, voice note, not financial advice, Crypto Regards MTG, Let's Get This Crypto! 💪

## Voice fix: "thank you for every step you've taken"

MTG asked for this line to flow as one sentence. In the source, "you" fell to a sentence-final pitch and was
followed by a 0.35 s silence before "for". Fix: "you" (12.87 to 13.10 s in the source) is lifted 2 semitones with
Rubber Band, formants preserved (`audio48k_fixed.wav`), and the pause 13.10 to 13.35 s is closed in the edit list.
The silence between "thank you" and "for" is now about 110 ms. Length is now 2:48.82; the closing track still starts
exactly 50 seconds before the end.

## How it is built

1. `transcribe.py`: word-level transcript of the original audio (faster-whisper small.en) -> `transcript.json`.
2. `inv_timing.py`: the edit list and synced captions -> `timing.js`, `edl.json`.
3. `stage.html` + `engine.js` + `scenes.js`: every frame is a pure function of time. Avatar frames come from the
   original video (crop 664x374 at 28,89, upscaled to 1000x564, lanczos + light unsharp), served from `av/`.
4. `inv_render.js`: Playwright renders frames (run 4 in parallel). `inv_test.js` renders single test frames.
5. `inv_sfx_dump.js` exports the sound cues, `inv_audio.py` re-cuts the voice and synthesises the sound design (ducked under the voice).
6. ffmpeg: `hqdn3d=1.5:1.2:4:4`, x264 CRF 20, maxrate 8M, AAC 192k. Loudness matches the original (about -14 LUFS).

## Vertical 9:16 version (1080x1920)

Same timing, same soundtrack (`mix.wav`) and same scenes, laid out for a phone: `stage_v.html` + `scenes_v.js`
(the engine switches with `window.ORIENT = 'v'`). Render with `ORIENT=v node inv_render.js <from> <to> <outDir>`.
MTG sits full width on top when he explains, the host bubble sits above the captions in full-screen scenes,
captions are two lines at 60px above the zone TikTok, Reels and Shorts cover with their own buttons and text.

Rules: no em or en dashes on screen, never fake numbers or results, keep each orientation as built (16:9 stays 16:9, 9:16 stays 9:16).

## Next version (planned, MTG's request on 5 November 2026)

When Bitcoin Wealth, ClickBaitPays and the full JetUp · TAG Markets guide are finished (Bellver Affiliates is done),
remake both versions so the video names every income stream in dashboard order: Bellver Affiliates, JetUp · TAG Markets,
ClickBaitPays, Bitcoin Wealth, ALTRUVA. Keep upgrading it whenever the streams change. See the reminder in `/CLAUDE.md`.
