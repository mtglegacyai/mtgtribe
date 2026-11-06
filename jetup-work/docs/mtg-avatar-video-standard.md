# MTG avatar video standard (locked 4 Nov 2026)

## Voice lock (MTG, 4 Nov 2026: "use that same perfect voice across all the videos going forward")
Every video (tutorial, explainer, advert, avatar or voice only) uses MTG Master Voice V2 (3931c505632149ceb2bbfecf2778c09c) on HeyGen Voice ("orca"), the voice's saved default engine: the same sound as his ALTRUVA trainings, SafePal tutorial, MTG TRIBE invite video and the Bellver plan. Call the speech tool without an engine override and confirm the response shows "engine": "orca" before using the audio.
Mistake not to repeat: the JetUP 5 Checks videos and the first JetUP sign-up training were voiced with engine elevenlabs + eleven_multilingual_v2. Same voice ID, different engine, and MTG rejected the sound ("you didn't use my original voice"). The sign-up training was re-voiced on orca the same day, and the 5 Checks video was re-voiced as v4 (see "Changing only the voice" below).
Other voices in the account ("MTG Real Voice", "Musa Dumakude") are not to be used.

MTG approved the JetUP 5 Checks v3 result. Every future video that uses his avatar must match it on the first render. HeyGen credits are scarce: do not spend them on versions or tests.

## Locked settings (do not change)
| Item | Setting |
|---|---|
| Avatar | "Profile 7 - Executive MTG", look ID 67b47edfb0a043189ff84ce5d055922c (navy blazer, white t-shirt, seated in office). The only avatar to use. |
| Voice | MTG Master Voice V2, ID 3931c505632149ceb2bbfecf2778c09c |
| Speech | create_speech or create_speech_without_player with NO engine, NO settings and NO language: the voice's saved default, HeyGen Voice ("orca"), speed 1.0. Check the result says "engine": "orca". Never ElevenLabs (see Voice lock). |
| Engine | avatar_v, 1080p, 16:9 (9:16 only when a vertical video is asked for) |
| Motion prompt | Calm, relaxed and sincere, speaking directly to camera with steady eye contact. Small natural head nods and gentle hand movements resting on the desk. Relaxed natural mouth, no forced or crooked smile, little teeth showing. Lips close fully during pauses. |
| Take | One continuous render from one uploaded audio file (audioAssetId). No joins. |
| Lip timing | Avatar V lips lead the voice by about 105 ms. In assembly, place the voice 105 ms earlier than the video. Verify: at least 95% of m/b/p lip closures land on the sound (v3: 97.7%). |
| Frame rate | Native 25 fps, no conversion |

## Voice and pauses
- Write the script with full punctuation. Add break tags: comma 0.2s, full stop or question 0.4s, paragraph 0.7s.
- Normalise pauses to: comma 0.22 to 0.32 s, full stop 0.42 to 0.55 s, question 0.46 to 0.60 s, paragraph 0.78 to 0.90 s, mid-phrase hesitation max 0.16 s. HeyGen Voice keeps natural breaths in its pauses, so use claude/video-engine/jetup/tutorial/pace_orca.py (silence threshold -48 dB, pauses found from the break tags and merged across breaths, edits only in pure silence). The older v3 pace.py was built for ElevenLabs takes (-58 dB).
- HeyGen Voice output is about -20 LUFS already (no +12.6 dB gain needed).
- Forced-align every phrase to confirm no word is dropped before uploading. HeyGen's word timestamps can be about 0.15 s off: always use forced alignment for timing.
- Captions and cards are timed from the forced-aligned words.

## Changing only the voice on a finished avatar video (4 Nov 2026)
Never re-render the avatar just to change the voice. Proven on JetUP 5 Checks v4: same script on orca as plain text (14 credits for 5,400 characters), forced-align, then re-time the new take onto the old word and m/b/p timings with Rubber Band (capped stretch 0.82 to 1.32 per phrase), voice placed 30 ms earlier than the old one. Result: 85% of m/b/p lip closures on the sound (v2 had 44%, v3 with its own voice 96%), no avatar cost. Method and code: claude/video-engine/jetup/v4-voice-swap/. Graphics and colours are rebuilt locally at no cost.

## Credit rules
- No engine tests: the settings above are proven. The avatar render settings (Avatar V, 105 ms lip lead) were measured with an ElevenLabs take; re-check the m/b/p lip score on the first orca-voiced avatar video (no extra render needed, measure the final one).
- Lock the spoken script before the avatar render. Changing spoken words after the render means a full re-render.
- Graphics, captions, cards, colours and music can be changed later at no HeyGen cost.
- Measured cost: full 5:47 Avatar V render = 278 credits (about 48 per minute). Speech on HeyGen Voice (orca): 14 credits for 5,400 characters of plain text (4 Nov 2026), about 2 credits per 500 characters.
- Always report remaining credits after any HeyGen task.

## What can change per project
- Theme colours, card styling and page design may follow each project's look.
- The avatar, voice, pace, pauses and lip-sync method never change.
