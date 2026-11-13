# Tutorial privacy tools (phone screen recordings)

Hides personal details in MTG's tutorial screen recordings, frame by frame, before any edit is shown or published. See
`.claude/skills/mtg-site-learning-system/references/tutorial-recordings.md` for the editing rules.

- `redact_lib.py`: timer bubble removal, keyboard strip, focused-field cover, banded OCR (two modes plus inverted), covers
  with labels ("Your email", "Your number").
- `redact_clip.py spec.json CLIP [--redraw]`: one clip at 30 fps to `<out>/<clip>/00000.jpg ...` plus `meta.json`.
  `--redraw` redraws from the saved analysis (no OCR) after a style change.
  `--kbscan` re-reads only the keyboard frames below the blanked strip (for clips analysed before that check existed).
  Per-clip options in the spec: `focus_label`, `focus` (`[[t0, t1, label or null]]`, null leaves no field cover, for clips
  where nothing is typed), `kb: false` (no keyboard blanking), `ignore` (`[[t0, t1, [x0, y0, x1, y1]]]`, OCR false alarms
  such as a button label read as a password), `cover` (`[[t0, t1, [x0, y0, x1, y1], label]]`, a forced cover, also for a
  field where typing shows part of an email before OCR can read it) and `nokb` (`[[t0, t1]]`, dark pages such as a
  Cloudflare check that only look like a keyboard; use it only where that strip shows nothing personal). Shortening
  a clip's end in the spec and redrawing drops the frames past the new end.
- Lessons from part 2 (7 Nov 2026): a dark bottom sheet such as "Use saved password?" can pass for a keyboard and shows
  the email, so text below a keyboard is read too; always look at contact sheets, the OCR is not enough on its own; cut the
  app switcher and the recorder's own buttons at the ends of a recording.
- `clipsheet.py CLIP STEP [out.jpg]`: contact sheet of redacted frames for checking.

**Personal words are never committed.** Put them in a private file outside the repository, one `category<TAB>regex` per
line (categories: name, email, password, phone, id), at `~/.tutorial-private-patterns.tsv` or `$TUTORIAL_PRIVATE_PATTERNS`.
Generic rules (emails, passwords with @, long digit runs, IB and CU numbers) work without it. Raw recordings stay out of the
repository too.

Run with `OMP_THREAD_LIMIT=1` and up to four clips in parallel. Always OCR-scan the finished video afterwards.
