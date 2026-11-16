# JetUP Zoom INVITATION promo v2 (7 Nov 2026), the version MTG asked for

MTG on v1: "This is an invitation. Talk to them, invite them, give them reason why they want to come ... three bullet points."
v2 is a new script in **MTG Master Voice V2** (one HeyGen request, `cec59c5fafe9477290a139814981b031`, saved in the voice bank
on branch `jetup-video-work`, `jetup-work/voice-bank/zoom-invite/`). No photo of MTG (his instruction).

Script: hook (see how automated gold trading really works before you put in a single cent), "Hi, I'm MTG ... I'm inviting you
to a live JetUP presentation on Zoom, tonight", the three times, why come (curious or burned before: see the facts, ask your
questions live), the three things you'll learn (what JetUP is and how the gold trading works; the $100 Fast Start bonus and its
rules; how to get started step by step if it's right for you), trading carries risk so learn first then decide, join at
mtgtribe.com/JetUpZoom and log in ten minutes early, send this to someone, see you tonight, Let's Get This Crypto!

58.4 s, 1080x1920, 30 fps, -14 LUFS. Pauses capped (0.45 s after a sentence, 0.55 s after a section; 2.9 s removed) so it stays
under WhatsApp's 60 s status limit. Closing track ends on the last frame (starts at 7.05 s), a soft pad carries the hook.

```bash
python3 align2.py        # word times measured in the audio (pocketsphinx, sentence by sentence) -> invite_words.json
python3 timeline2.py     # tidy pauses -> voice.wav + stage/timing.js (word fix for "or been burned before?" measured on the waveform)
python3 make_stage2.py   # stage/stage.html (needs ../parts.txt and stage/jetup-mark.png)
python3 mix2.py          # mix.wav (needs ../track.mp3)
node render.js range 0 1752 frames   # 4 ranges in parallel, then ffmpeg as in ../README.md
```
