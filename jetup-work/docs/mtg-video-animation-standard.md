# MTG video animation and engagement standard v2 (all projects, from 4 Nov 2026)

MTG, 4 Nov 2026: the ALTRUVA tutorials and explainers were "absolutely amazing" (the animated like, share and comment icons, the recap, the signature ending, the little sound effects and emojis). Carry all of it into every video in every project, and make each project better than the last. Never throw away what already works; enhance it. Everything here is graphics and sound work: it costs no HeyGen credits, so it is always included.

Reference build: JetUP + TAG Markets sign-up training (engine claude/video-engine/jetup/tutorial/render_tut2.py), built on the ALTRUVA engine (claude/video-engine/w16.py, tl_w1.py, gfx.py, audio16.py).

## 1. Voice (locked)
MTG Master Voice V2 (3931c505632149ceb2bbfecf2778c09c) on its default HeyGen Voice engine ("orca"). Never ElevenLabs. See claude/mtg-avatar-video-standard.md.

## 2. Everything said is seen, on the exact word
- Every element pops in on its spoken word: fade + ease-back scale pop (0.3 to 0.45 s), slight rise. Cue times come from the spoken phrase (word timings), never hard-coded seconds.
- New list items, rows and calculation lines pop in one at a time as they are said, with a soft tick.
- Calculations are revealed line by line in the order they are spoken (input, sum, answer, meaning).
- Tutorials: the screenshot dims around the control being explained (spotlight); a gold pointer glides to the button, presses it, a ripple shows the tap, with a soft click. The ring pulses in the other brand's colour so it stands out.
- The instruction panel slides in with each new step; exact on-screen labels as chips.
- Captions: sentence chunks, the word being spoken lit in the project accent colour, never covering a tap target.

## 3. Emojis and icons (MTG: "when you say like, I need to see the thumb")
- Like: 👍 thumbs-up icon. Share: 📤 share icon. Comment: 💬 comment icon. Save: 🔖 bookmark. Each pops exactly as the word is said, with a pop sound and a small particle burst (hearts float up from Like).
- Every social platform mentioned gets its badge with its own colour, emoji and handle: TikTok 🎵 @joinmtgtribe, YouTube ▶️ @mtgtribe, WhatsApp 💬 mtgtribe.com/group (the MTG TRIBE group), Telegram ✈️ @mtgtribe (channel t.me/mtgtribez), Facebook 📘 facebook.com/mtgtribe (the MTG TRIBE page, MTG confirmed 4 Nov 2026). Badges use emoji plus the platform name and colour, not copies of the platforms' logos.
- Small emoji pops on key spoken moments throughout (📱 grab your phone, 📧 email, 🔑 codes, 💰 money plan, ⚠️ warnings, 🎉 success, 👀 check twice, 📅 dates...), about one every 10 to 20 seconds, sitting just above the caption, never on top of words or tap targets.

## 4. Sound effects (sparing)
Synthesised in the engine (claude/video-engine/audio16.py recipe): soft whoosh on scene and part changes, tick on checklist items and recap ticks, pop on like/share/comment/save/bio and big slogan words, soft click on every demonstrated tap. Reference counts for an 8:42 training: 24 whooshes, 34 ticks, 11 pops, 22 clicks. Mixed under the voice; final mix -14 LUFS, true peak about -3 dBFS.

## 5. The ending sequence (every video)
1. Recap: tiles for each thing achieved, a green tick stamps on each as it is said, a progress line fills, "one tap at a time" chip.
2. Save / Share / Comment trio with icons and emojis popping on each word.
3. "We learn best when we teach others" kinetic slogan.
4. Comment prompt: comment icon, speech bubble that types the spoken question, answer chips (for example Part 1 to Part 6).
5. Links: main project URL as a big glowing pill (zoomed in, held); "Check my bio" chip with the TikTok and YouTube badges; the MTG TRIBE group URL with the WhatsApp badge.
6. "IT PAYS TO / PAY ATTENTION / & TAKE / ACTION" word by word, crown.
7. Signature outro, each line visualised: shield "Not financial advice"; THANK YOU with 👍 📤 💬 popping on like, share, comment; "Your support means everything 🙏"; "Thank yourself for taking MASSIVE ACTION today 🚀"; "YOU ARE THE BEST" with sparkles and crown; "Crypto-Regards," (Great Vibes script) MTG 👑 YOUR DIGITAL ARCHITECT; "See you on the next one 👋".
8. End card (music up): Crypto-Regards signature, "Let's Get This Crypto! 💪" (bouncing), main URL pill, all five platform badges, "Check my bio", an "Also watch" pointer to the related or previous video, one-line disclaimer.

## 6. MTG's face as the profile picture
- Wherever a crown icon or emoji stood for MTG, use his profile photo instead: the top-left brand bar (small, every frame), the "Hi, my name is MTG" intro (large), under the slogan, the signature ("Crypto-Regards, MTG") and the end card.
- Current photo (MTG, 5 Nov 2026, replaces the earlier avatar frame): his portrait in the white mtgTribe.com "Let's Get This Crypto!" evolution t-shirt, hand at his chin, gold watch, with the gold mtgTribe.com sign behind him.
- MTG, 5 Nov 2026: "I want to be fully visible": show the WHOLE square photo (face, the full t-shirt print and the sign readable) in a rounded gold frame wherever the photo appears large, and make the space for it: intro card (photo left about 600 px, name right), signature (about 580 px), slogan (about 330 px beside the words), "You are the best" (about 230 px), end card (300 to 400 px). Never crop it to a face-only circle at those sizes.
- Only the tiny brand-bar icon (about 50 px, every frame) uses a face crop, because the print cannot be read at that size.
- Built locally (claude/video-engine/profile/make_profile.py badge()). No HeyGen credits.
- Previous photo (4 Nov 2026): frame 4036 of the JetUP 5 Checks avatar video with the mtgTribe.com print added to the t-shirt. Retired.

## 7. Look
Project theme colours drive everything (JetUP: purple, pink, lime on near-black; ALTRUVA: royal, cyan, gold). MTG gold for the signature. Phone-first sizes, 16:9 unless vertical is asked for, cover thumbnail on the first frame.

## 8. Websites (MTG, 4 Nov 2026)
When a project website is built (next: the JetUP pages at mtgtribe.com/jetup), start from what worked on the ALTRUVA site (mtgtribe.com/altruva) and make it better: faster, fully optimised for search engines and AI search tools (titles, descriptions, headings, structured data, sitemap, robots, llms.txt, crawlable text for every video and tool). Preview first, publish only after MTG approves.
