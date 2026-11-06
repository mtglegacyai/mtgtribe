# Voice swap on a finished avatar video, without a new avatar render (JetUP 5 Checks v4, 4 Nov 2026)

Problem: the 5 Checks v3 avatar (Avatar V, 278 credits) was lip-synced to an ElevenLabs take. MTG wanted his approved voice (MTG Master Voice V2 on HeyGen Voice, "orca") without paying for a new avatar render.

Method (cost: 14 credits for 5,400 characters of speech, nothing else):
1. Same approved script, plain text (no break tags), two create_speech_without_player calls (under 5,000 characters each), engine left as the saved default (response must say "orca").
2. align5.py: forced-align the orca takes sentence by sentence (pocketsphinx, windows from HeyGen's word timestamps). HeyGen's timestamps were about 0.15 s off, so always use forced alignment.
3. warp5.py: re-time the orca take onto the v3 word timeline (v3/voice_v3_words.json):
   - phrases split at any pause over 0.12 s in either take;
   - one gentle stretch per phrase with Rubber Band R3 (`rubberband -3 -M map -D seconds`), capped at 0.82 to 1.32 so it still sounds natural; leftover lip time split 40% before and 60% after the sound; a phrase never starts before the previous one ends;
   - inner anchors on word starts (when more than 60 ms off) and on every matched m/b/p sound (pairs matched with difflib on word and phone), at least 40 ms apart, local stretch 0.62 to 1.75;
   - pauses rebuilt with the take's own room tone, 8 ms fades.
   - Rubber Band gotcha: never write the "0 0" start point in the time map file, or the output length is wrong.
4. Place the voice 30 ms earlier than v3's voice (0.865 s against the video at 1.0 s), mix as before (closing track 51.36 s before the end, loudnorm -14 LUFS, TP -2, 4x limiter at 0.70).
Result: word starts within 15 ms (median), 93% within 80 ms; m/b/p lip closures on the sound 85% (v3 with its own ElevenLabs voice: 96%; v2: 44%).

Rebrand (no credits): brand5.py patches the v3 card engine (gfx.py, gfx16.py, cards.py) to the JetUP purple and pink plus TAG Markets lime theme on near-black, keeps MTG's gold for his name, and puts his profile photo in the brand bar, on the "Hi, I'm MTG" card and on the end card. compose_v5.py and render_v5.sh rebuild the overlay with the v3 timings; the audio is mixed separately and muxed.
