# JetUP tutorial part 2: link JetUP to TAG Markets (7 Nov 2026)

Built from MTG's own recording (raw file private, never committed), redacted with `tools/tutorial-redact/` using
`redact_spec.json` (clips A to J, with the ignore, cover, nokb and kb options). `events.md` maps the source times.

1. `python3 lines.py` (needs t1, t2, t3 from the voice bank, p1v2/p1v3 and p2v1 audio, sentences.tsv): `lines.json`, `words.json`
2. `python3 make_tl_p2.py`: `stage/timeline.js`, `voice.wav`, `mixcues.json` (edit `shots_p2.py` for the shot list)
3. `node render.js range a b frames` in 4 workers, then `python3 mix_p2.py`, then ffmpeg (see the skill's pipeline notes)

Result: 214.6 s, 1080 x 1920, -14.0 LUFS, true peak -2.3 dB, OCR privacy scan 0 flags (1,590 window frames + 644 sampled).
