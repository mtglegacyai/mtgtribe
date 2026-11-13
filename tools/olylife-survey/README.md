# OlyLife Tera-P90 honest survey video (TikTok, 13 Nov 2026)

MTG asked on 13 Nov 2026 for a short survey video in his voice: ask people who have used the OlyLife THz Tera-P90 (and
sellers and session hosts) for their real experience, with strong hooks, comment and share prompts, OlyLife green
colours, emoji pops, made to trend on TikTok. **Preview only; MTG posts it after he approves it.** Facts it relies on:
`tools/olylife/olylife-facts.md`. Caption, pinned comment and after-posting steps: `posting-pack.md`.

v3: 2:18 (138.0 s), 9:16, 1080x1920, 30 fps. Mix -14 LUFS, true peak -2.8 dB. (v1 and v2: 2:00.)

## WhatsApp status cut (13 Nov 2026): 59.7 s

MTG asked for the 60-second status version. Built from the v3 voice (`lines_wa.py` cuts it at the silences between
words) plus two new V3 lines for WhatsApp, one request (`9df1d8b4cbe34070a94faecba984ad55`, take
`voice/survey_v3wa.flac`; the balance went from 44 to 42): "Reply to this status with your answers, by number." and
"So reply to this status with your answers. The full video is on my TikTok, at join MTG tribe."

Spoken: hook, honest answer, "We build multiple streams of income in my tribe... I'm asking you", "Eight quick
questions" + reply line, all eight questions (short form spoken, full wording on screen; questions 7 and 8 carry a
"SELLERS & SESSION HOSTS" tag because the seller line is cut), "Why does all of this matter? Because health is
wealth. Your health comes first.", the reply and TikTok line, "Let's Get This Crypto!", then the closing track's last
line ("Let's get this crypto, wherever I go!") on the end card (videos of 60 s or less, MTG 8 Nov 2026). The full
signature ending does not fit in a status; the end card (photo, Crypto-Regards, slogan, url, all five platforms)
closes it. Stage: `stage/stage_wa.html` with `stage/timeline_wa.js` (`STAGE=stage_wa.html node render.js ...`),
mix `mix_wa.py`, checks `qa_wa.py`.

## v3 (13 Nov 2026): Health is Wealth, the tribe, eight questions

MTG: "throw in that Health is Wealth slogan... a reminder that our health comes first", "replace community with Tribe",
frame it as one of the tribe's multiple income streams, improve the questions. Seven new lines in V3, one request
(`133bc33e4bbb484282b410eabb5c6a71`, take `voice/survey_v3b.flac`), the unchanged lines keep the first take
(`lines_survey2.py` builds both). 2:18.

- Intro: "We build multiple streams of income in my tribe, and I'm considering this machine as our next one. But before
  I bring it to my tribe, I'm asking you." (was "bringing this machine to my community")
- "Eight quick questions." Question 6 asks what people really paid: "Was it worth the money? Did you pay per session,
  or buy your own machine? Would you do it again?" Sellers get two: "the last two are for you", then new question 8:
  "How did you find your first clients? And where do you run your sessions?"
- **Health is Wealth**, its own scene right after the last question, before the comment call (the emotional peak, and
  the reason honest answers matter): "Why does all of this matter? Because health is wealth." / "What good is money,
  if you're too sick to enjoy it? Your health comes first. So look after your body." (MTG's own idea, 12 Nov 2026.)
  Echoed as a "💚 Health is wealth" chip on the "not medical advice" scene.
- Captions now show names as people read them: "OlyLife Tera-P90?" and "mtgtribe.com/group" (the voice text spells
  them for pronunciation; v1 and v2 showed the spelled-out words).

## Script v1 (MTG Master Voice V3, one request, 20 lines, 1,442 characters)

Hook: "Have you used this foot machine? The Olly Life Terra P ninety?" / "I need your honest answer." / "I keep seeing
amazing videos about it. Now I want the real stories, straight from the people who use it." / Hi, why I'm asking
(bringing it to my community) / "Seven quick questions. Answer by number in the comments."

1. Why did you try it? What were you hoping it would help with?
2. How many sessions have you had, and how often?
3. What did you feel during your very first session?
4. What changed after a few weeks? And what didn't change?
5. Anything you didn't like, or any discomfort? Be honest. It helps the next person.
6. Was it worth it? Would you pay for another session, or buy the machine?
   (re-hook) "And if you sell it, or run sessions, this one is for you."
7. What do your clients come back for? And what's the one question they always ask?

Then: good, bad or nothing at all, every honest answer counts / comment or stitch / "I'll read every comment, and share
what you told me in my next video. So follow" / the free MTG tribe at mtgtribe.com/group / save (to come back and read
the answers) / share with someone who uses the machine / "Quick reminder: this is not medical advice. Always check with
your doctor first."

"Olly Life" and "Terra P ninety" are spelled for the voice (heard as OlyLife Tera-P90). HeyGen request
`b83b066a1ed6455480b780dff04f7fc9`, **1 credit** (46 before, 45 after; MTG allowed up to 20); the take and HeyGen's reply with word times are in `voice/`. Speech-to-text heard
every line as written.

**Signature ending (0 credits):** MTG's banked lines from the 9:09 training (V2, branch `jetup-video-work`,
`ex3-pack`): "We learn best when we teach others.", "It pays to pay attention, and take action.", thank you, your
support, massive action, you are the best, I'm MTG, see you on the next one, Let's Get This Crypto!. Scene order,
motion and the four sounds follow `tools/video-signature/` (branch `claude/ecstatic-brown-dpla5l`), redrawn in OlyLife
green with MTG's crown disc (no JetUP logo, no photo). The fair-play sign-up scene is left out (nothing to sign up
for) and "not financial advice" became "not medical advice".

## Visuals

- **MTG's photo (MTG, 13 Nov 2026: "Use this image for my intro and outro, I am MTG"):** in the gold ring on "Hi,
  I'm MTG" (intro), on "I'm MTG, Your Digital Architect" (signature) and on the end card that follows it.
  `stage/mtg-photo.jpg` is his photo cropped square with a little ceiling added above the head so the ring does not
  cut it. The top bar and the other ending scenes keep the crown disc. v2 = v1 with the photo.

- The device is our own three.js model (`stage/device.js`): white body, champagne base, two brushed plates, the
  display reading "30 01" (30 minutes, level 1). No third-party photos or clips anywhere.
- Every line and word pops on its spoken cue; captions light the active word; a 1 to 7 question tracker; emoji in
  every scene; the two sample comments are labelled "Example answer" (never invented testimonials).
- Kept clear of TikTok's buttons and caption area (key text between y 160 and 1520, x 60 to 1020).

## Build

```bash
python3 lines_survey.py            # voice.wav, words.json, lines_out.json (cuts the take, adds the banked ending)
# stage/timeline.js is written from words.json and lines_out.json (see the snippet at the end of lines_survey.py runs)
python3 -m http.server 8765 &      # the stage loads three.js as ES modules, so it needs http
node render.js sfx > sfx_raw.txt   # cue times of the four sounds (then saved as sfx.json)
node render.js range 0 3591 frames # or 4 workers; rebalance.sh hands the missing frames to 4 list workers
python3 mix.py                     # mix.wav (needs audio/track.mp3 from jetup-video-work and the bank/ lines)
ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -movflags +faststart -shortest olylife-survey.mp4
python3 qa.py olylife-survey.mp4
```

Needs node with playwright, three@0.169.0 (`npm install`), Python with numpy, scipy, Pillow, faster-whisper, ffmpeg.
Fonts (Anton, Montserrat, Oswald, GreatVibes) go into `stage/` from `jetup-work/engine/fonts/` on `jetup-video-work`;
the closing track goes to `audio/track.mp3` and the banked ending lines to `bank/` (ex3-pack, same branch).
