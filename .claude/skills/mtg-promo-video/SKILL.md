---
name: mtg-promo-video
description: "MTG's standard for short promo and invitation videos: Zoom calls, webinars, launches, live events and offers, vertical first, built like an advert. It covers the invitation script (talk to them, give reasons to come, three things they will learn, when and how to join), his approved voice and pronunciation, advert pace, real 3D motion, a short memorable CTA link, the first frame as the preview, the closing track, captions and the checks before preview. Use this whenever MTG (mtgtribe.com, MusaTheGiant) asks for a promo, invite, teaser, advert, announcement or reel video, a video to go with a flyer, or anything that promotes an event or call, even if he does not say promo."
---

# MTG's promo and invitation videos

Lessons from the JetUP Zoom invitation (7 November 2026), in MTG's words: "This is an invitation. Talk to them, invite
them, give them reason why they want to come", "think of an advert", "put some oomph in it", "use 3D". Apply with
**mtg-creative-standard** (voice, music, brand, preview, approval) and **mtg-hooks-standard** (hooks and CTAs). MTG's
latest instruction in the chat wins.

## 1. The script is an invitation, not an explainer

A promo exists to make people show up. Build it in this order, about 140 to 160 words for under 60 seconds:
1. **Hook** (one line): a question or promise they care about. Example: "Want to see how automated gold trading really
   works, before you put in a single cent?"
2. **Personal invitation:** "Hi, I'm MTG, Your Digital Architect, and I'm inviting you to ... on Zoom, tonight!"
3. **When:** say the time for every audience country (for example South Africa, Nigeria, India). Name the country, not a
   region, when time zones differ inside the region.
4. **Why come:** speak to their situation ("Curious? Been burned before?") and the payoff ("see the facts, ask your
   questions live").
5. **Three things they'll learn:** "One ... Two ... Three ...", short and concrete, each one something the event really
   covers. Check it with MTG if unsure.
6. **Honest line:** risk and "learn first, then decide for yourself". No income promises.
7. **How to join:** the short link, said out loud, plus "log in ten minutes early".
8. **Share and close:** "Send this to someone who should be there. See you tonight! Let's Get This Crypto!"

Never reuse old explainer lines as a promo: they explain but don't invite.

## 2. Voice, pronunciation and pace

- Only MTG Master Voice V2 (see mtg-creative-standard). Reuse banked lines only when they fit the invitation; new lines
  cost credits, so state the estimate (about 2 credits per 500 characters) and generate the agreed script once.
- **Pronunciation:** write names the way they must be said. "Jet Up" as two words (screens show JetUP), "MTG tribe dot com
  slash jet up zoom", "P M", numbers in words.
- **Advert pace:** speed about 1.08, short sentences, exclamation marks for energy, break tags of 0.1 to 0.3 s only.
  After generating, cap pauses at about 0.32 s inside a section and 0.42 s between sections.
- Measure word timings from the audio (forced alignment per sentence), not only from HeyGen's estimates, and check a
  waveform where they disagree.

## 3. Look and motion

- **Vertical 9:16 first** (WhatsApp status, TikTok, Reels), under 60 seconds so it fits one WhatsApp status.
- **The first frame is the preview:** the hook headline and a visual must already be on screen at frame 0.
- **Real 3D** where it explains or excites: lit, metallic objects with depth (gold bars, coins, tickets, clocks set to
  the event times, phones typing the link, numbers 1 2 3, checks, gift boxes). Built with three.js and rendered frame
  by frame; text, captions and the top bar stay as sharp 2D on top.
- **Everything said is seen, on the word:** each country lights up as it is said, each of the three points pops on
  "One / Two / Three", the link types in as it is spoken and gets tapped.
- Advert energy with balance: fast entrances (0.3 to 0.4 s), a small punch-in on key words, a soft flash at scene changes,
  but every line stays on screen long enough to read.
- Captions with the spoken word lit; numbers and addresses shown the way people read them ($100, 11:30, mtgtribe.com/...).
- MTG's photo: follow his latest instruction for the video (for the 7 Nov 2026 Zoom promo he said "Don't put me in the
  video"); ask if unclear.

## 4. The call to action link

- Use a short, memorable address on mtgtribe.com that redirects to the real destination (for example
  mtgtribe.com/JetUpZoom to the Zoom link), with a preview card for WhatsApp and Facebook. Test every spelling (capitals
  and lower case) on the live site before the video goes out.
- The same link goes in the caption text for people who prefer to tap.

## 5. Sound

The closing track "They Call Me MTG" ends on the last frame (it starts about 51 s before the end; for shorter videos use
a fitted excerpt). Duck it under speech, let it rise in the gaps. Light sound design on the moments that matter: whooshes
on scene changes, pops and ticks on reveals, coin clinks on coins. Master to about -14 LUFS, true peak -1.5 dB.

## 6. Checks before MTG sees it

- Speech-to-text on the finished file: every line heard as written, nothing clipped.
- Frames pulled at the key words: each visual lands on its word.
- A brightness scan over all frames: only the planned flashes jump.
- Length under 60 s, the first frame reads well, no dashes, brand line and slogan exact.
- Send the video, a cover image, the script and the credits used. Never publish it yourself.

Keep the build files in the repository (`tools/<project>-promo/`, not published) and new voice lines in the voice bank.
