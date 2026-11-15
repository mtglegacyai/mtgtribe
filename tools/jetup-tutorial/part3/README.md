# JetUP tutorial part 3: verify your identity, KYC (8 Nov 2026)

Built from MTG's own recording (raw file private, never committed), redacted with `tools/tutorial-redact/` using
`redact_spec.json`: clips P to V. Clip S is the 6-digit code entry: fixed covers per keyboard layout ("Code hidden",
"Your email"), and the app switcher stretches (inbox, WhatsApp, Gmail) are blacked out and never used in the edit.
The camera steps could not be recorded (the screen recorder blocks the camera, "This site can't ask for your permission"),
so the ID scan and the selfie are recreated cards on the stage (`cam1`, `cam2`), labelled as recreated, built from MTG's two
screenshots ("Get your camera ready", the three selfie tips, Powered by Sumsub).

1. `python3 lines.py`: `lines.json`, `words.json` (new lines: request 89f01eda7b2c497a826a8a085021a412)
2. `python3 make_tl_p3.py` (shot list in `shots_p3.py`), `node render.js range a b frames` in 4 workers, `python3 mix_p3.py`
3. Site: `python3 p3_site_edits.py <repo> 3:30 PT3M30S` adds the video entry, the part 3 steps and the strips
