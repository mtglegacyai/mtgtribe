"""Builds an uploadable skill file (.skill, a zip) from a skill in .claude/skills/.

MTG uploads the file to his claude.ai account, so the skill works on every website, not only in this repository.
Some skills carry a kit: the files git tracks in a tools folder are bundled inside the skill (see KITS).

Usage (from anywhere in the repository):
    python3 tools/skills/package_skill.py mtg-scriptforge [--out tools/skills/dist]
"""
import argparse
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# skill name -> list of (folder in this repo, path inside the skill)
KITS = {
    'mtg-scriptforge': [('tools/video3d', 'kit/video3d')],
}

ap = argparse.ArgumentParser()
ap.add_argument('skill')
ap.add_argument('--out', default=None)
ap.add_argument('--no-kit', action='store_true', help='leave out the bundled tools kit (smaller file, skill text only)')
a = ap.parse_args()

root = Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip())
src = root / '.claude' / 'skills' / a.skill
if not (src / 'SKILL.md').exists():
    sys.exit(f'No skill at {src}')
out_dir = Path(a.out) if a.out else root / 'tools' / 'skills' / 'dist'
out_dir.mkdir(parents=True, exist_ok=True)

# Check the frontmatter the way claude.ai does.
text = (src / 'SKILL.md').read_text(encoding='utf-8')
m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
if not m:
    sys.exit('SKILL.md has no frontmatter')
fm = m.group(1)
name = re.search(r'^name:\s*(.+)$', fm, re.M).group(1).strip().strip('"')
desc = re.search(r'^description:\s*"?(.*?)"?\s*$', fm, re.M).group(1)
problems = []
try:  # claude.ai parses the frontmatter as YAML: an unescaped quote inside the description makes the upload fail
    import yaml
    yaml.safe_load(fm)
except ImportError:
    pass
except Exception as e:
    problems.append('frontmatter is not valid YAML (check quotes inside the description): ' + str(e).splitlines()[0])
if name != a.skill:
    problems.append(f'name "{name}" does not match the folder "{a.skill}"')
if len(desc) > 1024:
    problems.append(f'description is {len(desc)} characters (max 1024)')
if '<' in desc or '>' in desc:
    problems.append('description contains angle brackets')
if re.search('[\u2013\u2014]', text):
    problems.append('SKILL.md contains an em or en dash (MTG rule)')
if problems:
    sys.exit('Not packaged:\n  ' + '\n  '.join(problems))

files = []  # (path on disk, path inside the zip)
for p in sorted(src.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc':
        files.append((p, Path(a.skill) / p.relative_to(src)))
for folder, inside in ([] if a.no_kit else KITS.get(a.skill, [])):
    tracked = subprocess.run(['git', 'ls-files'], cwd=root / folder, capture_output=True, text=True, check=True).stdout.split('\n')
    for rel in filter(None, tracked):
        files.append((root / folder / rel, Path(a.skill) / inside / rel))

skill_mds = [z for _, z in files if z.name == 'SKILL.md']
if len(skill_mds) != 1:
    sys.exit(f'A skill must contain exactly one SKILL.md, found {len(skill_mds)}')

target = out_dir / (f'{a.skill}-small.skill' if a.no_kit else f'{a.skill}.skill')
with tempfile.TemporaryDirectory() as tmp:
    tmp_zip = Path(tmp) / target.name
    with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for disk, inside in files:
            z.write(disk, inside.as_posix())
    target.write_bytes(tmp_zip.read_bytes())
    target.with_suffix('.zip').write_bytes(tmp_zip.read_bytes())  # claude.ai's upload asks for a ZIP
print(f'{target} ({len(files)} files, {target.stat().st_size // 1024} KB)')
