---
name: mtg-tutorial-video
description: "MTG's locked-in formula for step-by-step tutorial videos made from his own phone screen recordings (JetUP, TAG Markets, ALTRUVA, BIX, wallets, exchanges or any new platform). It covers receiving his recordings and notes, privacy masking in every frame, the fixed script structure (greeting with his circle photo, In this video, the steps, recap, next video, fair-play sign-up wording, signature outro), the vertical visual system, his approved voice with banked lines first, the build and render pipeline, the checks, and where the videos go on his websites. Use this whenever MTG (MusaTheGiant, mtgtribe.com) sends a screen recording, says 'create a tutorial video', 'part 2', 'next part', 'chop', 'step-by-step video', or gives narration notes for a recording, even if he does not name this skill. MTG: 'When I say create a tutorial video and give you everything you need, just create something that's already working perfectly.'"
---

# MTG's tutorial videos: the locked formula

MTG approved this formula on 7 November 2026 (JetUP part 1). Do not ask him to repeat any of it. Apply it automatically to
every tutorial part. His latest instruction in the chat still wins; when he changes the formula, update this skill.

Works with **mtg-creative-standard** (voice, music, brand, preview, approval) and **mtg-site-learning-system**
(facts register, consistency, links, PDFs). Where they differ on these points, this skill is newer: his photo is always a
**circle**, and the greeting says **"video"**, never "training".

## 1. Receive and store

- One part per short video ("chops"). Save his spoken notes for every part in the site's tutorial README (steps, exact
  on-screen labels, what to cut, tips), with no personal details and never a one-time code or password.
- Big files arrive via Google Drive (he shares by link; download with
  `curl -sSL -o part.mp4 "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t"`, check the byte
  size; an HTML file means the link is not shared yet). Raw recordings never go in the repository.
- Map the recording first: contact sheets every 2 to 4 seconds, then a table of source times, what each shows, keep or cut.
- Read `references/privacy.md` and run the masking before anything else.

## 2. The script structure (fixed)

1. **Greeting** with his photo large in a circle: "Hi, my name is MTG, Your Digital Architect. Thank you for taking the
   time to watch this video." (banked line + new line in the JetUP voice bank).
2. **In this video:** "In this video, I'll show you how to ..." then the list of what they will do, said in 2 or 3 short
   sentences while a numbered list fills in on screen, item by item, on the word. Then "Take your time. You can pause any
   step and follow along with me."
3. **The steps** (the meat and potatoes): one action at a time, every step voiced, each ending on its success check.
4. **Recap:** "Let's recap what we covered in this video." The same list ticks off item by item as it is said.
5. **Next video:** "In the next video, part N, I'll show you how to ..." with its 2 or 3 actions on screen.
6. **Links, fair play and sharing:** "Everything I showed you, plus my links, is at MTG tribe dot com slash ...", then
   "Invited by someone else? Use their link. This video is for every team, so feel free to share it." Save and share lines.
7. **Signature outro** (banked): financial advice reminder, do your own research, thank you for every like, share and
   comment, your support means everything, thank yourself for taking massive action, YOU are the best, I'm MTG, Your
   Digital Architect, see you on the next one, Let's Get This Crypto! With his circle photo, brand line and slogan.

**Fair-play sign-up wording (MTG, 7 Nov 2026), in every video that sends people to sign up:** "If I invited you, go to MTG
tribe dot com slash ..., and tap any Join ... button. If someone else invited you, use their Partner link instead, so you
join their team." The videos must be shareable by people outside MTG's team. Use the exact button label the website uses.

Full template and wording: `references/script-template.md`.

## 3. Look and motion (vertical 1080 x 1920)

- Top bar: his face in a small gold-ringed circle, "MTG | Your Digital Architect", the part chip.
- Step card: gold number, title with the exact on-screen label highlighted, one-line sub.
- The screen in a slim gold-titanium window, zoomed to the action; a lime ring on what to look at; a tap ripple where he
  taps; chips for short tips; tip cards for errors (never show his mistakes).
- **The address bar is shown and ringed every time a new site or page opens**, then zoom in.
- Captions under the window with the spoken word lit; progress bar of the steps.
- His photo: **always a circle with a gold ring** (use the round crop, `assets/tribe/mtg-photo-round-1000.webp`), never a
  rectangle or rounded square. Large in the greeting and outro, small with his name in the recap and next-video scenes.

Details: `references/visual-system.md`.

## 4. Voice

Only MTG Master Voice V2 (`3931c505632149ceb2bbfecf2778c09c`, engine orca). Build from the voice bank first (branch
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
