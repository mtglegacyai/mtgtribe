# JetUP explainer #1: "JetUP and TAG Markets: the simple picture" (8 Nov 2026)

16:9, 1920x1080, 25 fps, 1:32. Built only from MTG's approved voice-bank lines (no new voice, 0 HeyGen credits):
hook from the Zoom invite (i1), the simple picture and the 70/30 split from 5 Checks (o1, o2), the 88% reminder (t2),
"learn first" (i1), the fair-play line (tutorial p1v3) and the signature outro (t3).
No MTG photo: the JetUP logo disc (MTG, 8 Nov 2026). Closing track: only its last line ("Let's get this crypto,
wherever I go!", 48.38 s to the end of the 51.36 s track) right after his last word (creative standard, 7 Nov 2026).

1. `python3 lines_ex1.py` (needs the voice-bank mp3s and sentences.tsv beside it): `lines.json`, `words.json`, `v_*.wav`
2. `python3 make_ex1.py`: `stage/timeline.js`, `voice.wav`, `mixcues.json`
3. `node render.js range a b frames` (4 workers), `python3 mix_ex1.py`, then ffmpeg (CRF 20, AAC 160k, faststart)
4. Cover: `node shoot_cover.js` (cover.html)

Checks: speech-to-text matches the script, -14.0 LUFS, true peak -2.6 dB, no personal data (graphics only), no dashes.
