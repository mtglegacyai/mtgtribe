# Tutorial privacy tools (phone screen recordings)

Hides personal details in MTG's tutorial screen recordings, frame by frame, before any edit is shown or published. See
`.claude/skills/mtg-site-learning-system/references/tutorial-recordings.md` for the editing rules.

- `redact_lib.py`: timer bubble removal, keyboard strip, focused-field cover, banded OCR (two modes plus inverted), covers
  with labels ("Your email", "Your number").
- `redact_clip.py spec.json CLIP [--redraw]`: one clip at 30 fps to `<out>/<clip>/00000.jpg ...` plus `meta.json`.
  `--redraw` redraws from the saved analysis (no OCR) after a style change.
- `clipsheet.py CLIP STEP [out.jpg]`: contact sheet of redacted frames for checking.

**Personal words are never committed.** Put them in a private file outside the repository, one `category<TAB>regex` per
line (categories: name, email, password, phone, id), at `~/.tutorial-private-patterns.tsv` or `$TUTORIAL_PRIVATE_PATTERNS`.
Generic rules (emails, passwords with @, long digit runs, IB and CU numbers) work without it. Raw recordings stay out of the
repository too.

Run with `OMP_THREAD_LIMIT=1` and up to four clips in parallel. Always OCR-scan the finished video afterwards.
