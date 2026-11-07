# Account skills: build the upload files

MTG keeps his skills in his claude.ai account so they work on every website. The master copies of the skills made in
this repository live in `.claude/skills/`. This script turns one into a `.skill` file he can upload:

```bash
python3 tools/skills/package_skill.py mtg-scriptforge
```

The file lands in `tools/skills/dist/` (not saved in git). For `mtg-scriptforge` the script also bundles the 3D studio
(`tools/video3d/`, only the files git tracks) as `kit/video3d/`, so the skill can install the studio into any site's
project. It refuses to build when the description is too long or a dash rule is broken.

Rebuild and re-upload whenever the skill or the studio changes.

If the full ScriptForge file will not upload (it bundles the studio, about 2 MB), build the skill text only:
`python3 tools/skills/package_skill.py mtg-scriptforge --no-kit` makes `dist/mtg-scriptforge-small.skill` (about
180 KB). It works the same in claude.ai; only the copy of the studio for other sites' projects is left out.

