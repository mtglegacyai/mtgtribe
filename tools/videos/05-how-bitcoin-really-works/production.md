# Production record: video 05 (10 November 2026, daily video)

Composition: `tools/video3d/src/compositions/hbw05/BitcoinWorks.tsx` (id `HBW05-9x16`), cover `Cover05-9x16`.
Files in `tools/video3d/public/videos/05/`: `script.txt` (the text sent, with `//` pause marks), `words.json`,
`captions.json`, `timeline.json`, `anchors.json` and `cues.json` (named cue times), `replacements.json`; the voice WAV is
not in git.

- **Voice: the first video in "MTG Master Voice V3"** (`65f1b9ff3f1e418496de5715a801e7dd`). HeyGen's new speech engine
  refused "MTG Master Voice V2" ("This voice is not compatible with heygen-voice-1. Create a new instant voice."; no
  credits used). MTG chose to re-clone from V2: V3 was cloned from 178 seconds of his own V2 narration (videos 04, 03,
  02 and part of 01; no noise removal; cloning cost 0 credits). He heard a 7 second test next to V2 and said "V3
  approved". Full script: one call, request `5a69e793c974415f8fc4ddbf86bd6cb2`, 61.2 s. Credits: 54 before, 1 for the
  test, 1 for the script, 52 after.
- Pauses: the new engine refuses pause tags on instant voices, so `scripts/voice_timing.py` stretched the paragraph
  gaps to 0.6 s (1.0 s after "Forever.") by inserting silence: 0.94 s added, 62.15 s in all. The teaching ends at 50.2 s
  ("give me fifty seconds"); then the tribe invite and sign-off.
- Leo: 11 moments from his existing clips (think, wow, worried, point, aha, mind blown, reassure, point, ask, wink and
  thumbs up, welcome), each started on a named cue; no new clips, no credits.
- 3D (CSS, no credits): the gold coin (hook, the miner's reward, the cover), the blocks (the chain, the coins on the
  record), the notepad that writes MTG's tip, the laptop that opens on mtgtribe.com/group.
- Sound: soft effects fitted to the story, two new ones made for it (`ping` when the computers light up, `halve` on
  each stair of the reward), plus Leo's own (aha, exhale, scribble, laptop); the theme's last line only, right after
  "Let's Get This Crypto!".
- End: the new EndScreen (tribe pill, five website pills timed to "crypto, AI and multiple income streams", his formal
  photo, the signature, mtgtribe.com in the big gold pill).
- Final: `out/hbw05-9x16.mp4`, 1:05 (65.1 s), -14.0 LUFS, true peak -1.5 dBFS, no black frames, cover embedded. A
  transcript of the voice file matches the script; the theme's last line plays from 61.9 s, right after his last word
  (61.75 s). Music: last line only, as in videos 02 to 04 (this video is 5 seconds over a minute; MTG's tutorial skill
  has a rule that videos over 60 seconds get the full track softly under speech: asked MTG which he wants for daily
  videos over a minute).
