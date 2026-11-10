---
name: mtg-tutorial-video
description: "MTG's locked-in formula for step-by-step tutorial videos made from his own phone screen recordings (JetUP, TAG Markets, ALTRUVA, BIX, wallets, exchanges or any new platform). It covers receiving his recordings and notes, privacy masking in every frame, the fixed script structure (greeting with the JetUP logo, In this video, the steps, recap, next video, fair-play sign-up wording, the signature ending of his 9:09 sign-up training with 'We learn best when we teach others'), the vertical visual system, his approved voice with banked lines first, the build and render pipeline, the checks, and where the videos go on his websites. Use this whenever MTG (MusaTheGiant, mtgtribe.com) sends a screen recording, says 'create a tutorial video', 'part 2', 'next part', 'chop', 'step-by-step video', or gives narration notes for a recording, even if he does not name this skill. MTG: 'When I say create a tutorial video and give you everything you need, just create something that's already working perfectly.'"
---

# MTG's tutorial videos: the locked formula

MTG approved this formula on 7 November 2026 (JetUP part 1). Do not ask him to repeat any of it. Apply it automatically to
every tutorial part. His latest instruction in the chat still wins; when he changes the formula, update this skill.

Works with **mtg-creative-standard** (voice, music, brand, preview, approval) and **mtg-site-learning-system**
(facts register, consistency, links, PDFs). Where they differ on these points, this skill is newer: **no MTG photo anywhere, neither in the video nor on the
thumbnail; the official JetUP logo takes its place** (MTG, 8 Nov 2026), and the greeting says **"video"**, never "training".

## 1. Receive and store

- One part per short video ("chops"). Save his spoken notes for every part in the site's tutorial README (steps, exact
  on-screen labels, what to cut, tips), with no personal details and never a one-time code or password.
- Big files arrive via Google Drive (he shares by link; download with
  `curl -sSL -o part.mp4 "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t"`, check the byte
  size; an HTML file means the link is not shared yet). Raw recordings never go in the repository.
- Map the recording first: contact sheets every 2 to 4 seconds, then a table of source times, what each shows, keep or cut.
- Read `references/privacy.md` and run the masking before anything else.

## 2. The script structure (fixed)

1. **Greeting** with the official JetUP logo large in a gold-ringed disc: "Hi, my name is MTG, Your Digital Architect. Thank you for taking the
   time to watch this video." (banked line + new line in the JetUP voice bank).
2. **In this video:** "In this video, I'll show you how to ..." then the list of what they will do, said in 2 or 3 short
   sentences while a numbered list fills in on screen, item by item, on the word. Then "Take your time. You can pause any
   step and follow along with me."
3. **The steps** (the meat and potatoes): one action at a time, every step voiced, each ending on its success check.
4. **Recap:** "Let's recap what we covered in this video." The same list ticks off item by item as it is said.
5. **Next video:** "In the next video, part N, I'll show you how to ..." with its 2 or 3 actions on screen.
6. **Links, fair play and sharing:** "Everything I showed you, plus my links, is at MTG tribe dot com slash ...", then
   "Invited by someone else? Use their link. This video is for every team, so feel free to share it." Then "Save this video,
   so it's here when you need it. Share it with someone who's ready to start."
7. **"We learn best when we teach others."** then **"It pays to pay attention, and take action."** (MTG's favourite line and
   his slogan, banked in the sign-up training's own take: `signup-training/t3.mp3`, 0 credits).
8. **Signature outro** (banked): financial advice reminder, do your own research, thank you for every like, share and
   comment, your support means everything, thank yourself for taking massive action, YOU are the best, I'm MTG, Your
   Digital Architect, see you on the next one, Let's Get This Crypto! Then the end card, held about 3.4 s after his last
   word, with the site address (mtgtribe.com/jetup) as a large pill visible to the last frame (MTG, 8 Nov 2026).

**Steps 6 to 8 always play as the signature ending of the 9:09 sign-up training** (MTG, 8 Nov 2026: "the best transitions,
sound effects, animations, and even my favourite line ... I want consistency, professionalism, and precision across all my
videos"). See section 3a.

**Fair-play sign-up wording (MTG, 7 Nov 2026), in every video that sends people to sign up:** "If I invited you, go to MTG
tribe dot com slash ..., and tap any Join ... button. If someone else invited you, use their Partner link instead, so you
join their team." The videos must be shareable by people outside MTG's team. Use the exact button label the website uses.

Full template and wording: `references/script-template.md`.

## 3. Look and motion (vertical 1080 x 1920)

- Top bar: the small JetUP logo disc with a gold ring, "MTG" over "YOUR DIGITAL ARCHITECT", the part chip.
- Step card: gold number, title with the exact on-screen label highlighted, one-line sub.
- The screen in a slim gold-titanium window, zoomed to the action; a lime ring on what to look at; a tap ripple where he
  taps; chips for short tips; tip cards for errors (never show his mistakes).
- **The address bar is shown and ringed every time a new site or page opens**, then zoom in.
- Captions under the window with the spoken word lit; progress bar of the steps.
- **No photo of MTG** (MTG, 8 Nov 2026). Where his photo used to be (greeting, recap, next video, outro, top bar), use the
  official JetUP logo on a dark purple disc with the gold ring (`tools/jetup-tutorial/jetup-disc.png`, small version
  `jetup-disc-small.png`): large in the greeting and outro, small with his name in the recap and next-video scenes.

Details: `references/visual-system.md`.

## 3a. The signature standard: the 9:09 sign-up training is the reference (MTG, 8 Nov 2026)

Every MTG video (tutorial parts, explainers, any new video) ends, sounds and moves like the 9:09 JetUP + TAG Markets
sign-up training. Do not invent a new ending, sound set or transition style per video.

- **Ending, scene by scene, each on its spoken word:** links (big lime url pill pops on the address) and the fair-play scene
  (Invited by someone else? / Use their link / THIS VIDEO IS FOR EVERY TEAM / Feel free to share it); HELP SOMEONE START
  RIGHT (SAVE and SHARE ring icons with particle bursts); WE LEARN BEST / WHEN WE TEACH OTHERS; IT PAYS TO / PAY ATTENTION /
  & TAKE / ACTION (kinetic, burst on ACTION, JetUP disc); Not financial advice (shield, research chip); THANK YOU with Like,
  Share, Comment ring icons, bursts and floating hearts, "Your support means everything"; Thank yourself / MASSIVE ACTION;
  I wish you nothing but the best / YOU ARE THE BEST with sparkles; Crypto-Regards, MTG, YOUR DIGITAL ARCHITECT, See you on
  the next one; end card (logo disc, signature, Let's Get This Crypto! 💪, url pill, TikTok, YouTube, WhatsApp, Telegram and
  Facebook badges, a "Next:" chip, risk line). Captions stop when the end card arrives.
- **Sound effects: only the training's four synthesised sounds**, at the training's level relative to the voice (raised
  3.6 dB with the voice at -16 LUFS), never ducked: whoosh on every scene or step change, tick on every list row, tick-off
  and chip, pop on engagement (save, share, like, comment, the address, ACTION, MASSIVE, YOU), click on every demonstrated
  tap. No music bed under the steps; the closing track comes in under the ending as usual.
- **Motion:** pop-ins with ease-back, 0.3 s crossfades between scenes, particle bursts on engagement, and emoji pops above
  the caption box on key words (about every 10 to 20 s, 2 s each, never over text or tap targets).
- **Tools (copy, don't rebuild):** `tools/video-signature/` (README): `mtg_ending.py` draws the ending in 16:9 or 9:16 with
  the training engine's own helpers; `retime_part.py` inserts the banked lines and re-times a part; `compose_kit.py`
  composites the ending onto the stage frames; `mix_consistent.py` is the one mix for every video.

## 4. Voice

Only MTG Master Voice V3 (`65f1b9ff3f1e418496de5715a801e7dd`, MTG's voice since 10 Nov 2026; no model or engine override, no break tags: one paragraph per pause). The older V2 is retired, but its banked lines stay usable. Build from the voice bank first (branch
`jetup-video-work`, `jetup-work/voice-bank/`, `sentences.tsv`). Write the new lines for the part (In this video, step
lines, recap, next video) as one script and generate them in **one** request; MTG's request for the part is the approval.
Write "Jet Up" as two words. Cut at real silences, measure word times, save the new file to the voice bank with its
sentences. Report the credits used. Details: `references/voice.md`.

## 5. Build, render, check

Reference implementation: `tools/jetup-tutorial/part1/` (stage, engine, timeline builder, shot list, mix) and
`tools/tutorial-redact/`. Copy it for the next part and change only the shot list, the voice placement and the texts.
Checks before MTG sees it (all of them, every time): OCR privacy scan of every second frame of the finished video, contact
sheets, speech-to-text of the audio, loudness -14 LUFS and true peak under -1.5 dB, brightness jumps, first frame reads as
a cover. Details: `references/pipeline.md`.

## 6. Deliver and place

Send the video and the cover, with a short note: what is in it, what was checked, credits used, what is waiting on him.
Never publish without his approval. On the website, each part plays in the slim phone frame: at the top of its part on the
step-by-step page, and in a "Step-by-step videos, one per part" strip near the top of that page (`references/pipeline.md`).
Every video gets a thumbnail in the series look with the **official JetUP logo, never MTG's photo** (MTG, 8 Nov 2026: "Do
not put my profile picture on these videos, put the official JetUp logo"), and since the same day **no photo of MTG inside
the videos either** ("I want my photo out of all videos themselves too"). His voice and his name stay.
