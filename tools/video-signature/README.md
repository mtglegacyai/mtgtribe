# MTG's signature standard for every video (MTG, 8 Nov 2026)

> "I just noticed that the 9:09 training video has the best transitions, sound effects, animations, and even my favourite
> line that says We learn best when we teach others. I want consistency, professionalism, and precision across all my
> videos." (MTG, 8 November 2026)

The reference is the 9:09 JetUP + TAG Markets sign-up training (`jetup-work/engine/tutorial/render_tut2.py` on branch
`jetup-video-work`). This folder carries its ending, its four sounds and its motion to every other video, in 16:9 and 9:16,
with the JetUP logo disc wherever MTG's photo used to be.

## What every video gets

1. **The signature ending**, each scene on its spoken word (`mtg_ending.py`, class `Ending`):
   links (big url pill) and fair play (Invited by someone else? / Use their link / THIS VIDEO IS FOR EVERY TEAM / Feel
   free to share it), HELP SOMEONE START RIGHT (SAVE, SHARE), **WE LEARN BEST / WHEN WE TEACH OTHERS**, IT PAYS TO / PAY
   ATTENTION / & TAKE / ACTION, Not financial advice, THANK YOU (Like, Share, Comment, hearts), MASSIVE ACTION, YOU ARE THE
   BEST (sparkles), Crypto-Regards MTG signature, end card (logo, slogan, url pill, TikTok, YouTube, WhatsApp, Telegram,
   Facebook, a Next chip, risk line). The drawing helpers, easing and timings are copied from the training's engine.
2. **The voice lines** "We learn best when we teach others." and "It pays to pay attention, and take action." from the
   training's own take (`signup-training/t3.mp3`), cut by `lines_new.py` (word times in `lines_new.json`). 0 credits.
3. **The four sounds** (`sfx_bank()`): whoosh on scene and step changes, tick on list rows, tick-offs and chips, pop on
   engagement, click on taps; at the training's level relative to the voice (voice -16 LUFS, sounds +3.6 dB), never ducked.
   `mix_consistent.py` is the one mix: voice, sounds, the full 51.36 s closing track ending on the last frame, two-pass
   loudnorm to -14 LUFS with true peak -2.8 dB. Encode the audio as AAC 256k: at 192k the native encoder put a
   5-sample overshoot (+3.3 dBFS) into Part 2. `remux256.sh` and `reencode.sh` re-check loudness, peak and overshoots.
4. **Emoji pops** above the captions on key words (2 s, ease-back), as in the training (`emos/*.json`, stage `emojis()`).
   Check every pop on the finished video: none may cover a word on screen (two were dropped on 8 Nov 2026 for that reason).

## How to run it

Tutorial part (HTML stage in `tools/jetup-tutorial/partN/`):

```
python3 retime_part.py <part dir> "Next: Part 2, link JetUP to TAG Markets" emos/p1.json   # insert lines, cues, emoji
python3 sfx_body_part.py <part dir>                                                     # body sounds on the palette
./build_part.sh <part dir> <out.mp4>              # render (4 workers), composite the ending, mix, encode
python3 qa_video.py <published.mp4> <new.mp4> <kit start>   # body unchanged, loudness, speech-to-text of the ending
```

Explainer (16:9): `tools/jetup-explainers/ex1/make_ex1c.py` builds the timeline with the new lines and writes
`kitcues.json` and `sfx_body.json`; then `build_part.sh` the same way.

Videos made with the older Python engines: the sign-up training (`training_logo_patch.py`: live frame plus the difference
between a JetUP-logo render and the original square-photo render of the same frames) and the 5 Checks
(`tools/jetup-5-checks-v5/render.py` with `PHOTO` and `FACE` set to `tools/jetup-tutorial/jetup-disc.png`). Their
endings already are the reference.

`consist_site_edits.py` is the site update that published the 8 Nov 2026 versions (new file names so caches refresh).

## End card addresses (confirmed by MTG, 10 Nov 2026)

The end card shows TikTok @joinmtgtribe, YouTube @mtgtribe, WhatsApp mtgtribe.com/group, **Telegram @mtgtribe** and
**Facebook facebook.com/mtgtribe**. MTG was asked on 10 Nov 2026 because the website linked to two other addresses
(a Telegram channel ending in z and a personal Facebook profile). He confirmed the end card's two, and the website was
changed to match the same day. Leave `PLAT` in `mtg_ending.py` as it is.
