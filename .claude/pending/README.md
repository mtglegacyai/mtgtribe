# Waiting for MTG's approval

`readability-fixes.patch` (26 Nov 2026): the six readability fixes on mtgtribe.com, /jetup and /bw, shown to MTG on a
private preview link. Kept here (this folder is not served on the website) so nothing goes live before he approves.

When MTG approves:

1. `git apply .claude/pending/readability-fixes.patch`, then delete this folder.
2. If `jetup/assets/jetup.css` or `bw/_build/src/assets/bw.css` changed on main since 26 Nov 2026, apply the patch to
   the source files only and rebuild instead: `python3 jetup/_build/build.py`, and for /bw copy `bw.css` and re-stamp
   every page with its md5 (first 8 characters), as `.claude/skills/mtg-skill-library/references/design-review.md` says.
3. The /bw part also goes to bitcoinwealthpays.com (repo MusaTheGiant/bitcoinwealthpays): the same `bw.css` and the
   same stamp on its pages, in its own pull request.
4. Check both domains live after merging.
