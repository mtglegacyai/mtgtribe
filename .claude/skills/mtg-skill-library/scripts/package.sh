#!/usr/bin/env bash
# Package this skill for MTG's Claude account, so the library works in all his projects, not only this repository.
# Makes two files, because claude.ai offers two upload routes (27 Nov 2026):
#   mtg-skill-library-skill-<date>.zip   for Customize > Skills > + > Create skill > Upload a skill (the skill folder)
#   mtg-skill-library-plugin-<date>.zip  for the newer Plugins page: Add > Upload plugin (the skill inside a plugin:
#                                        .claude-plugin/plugin.json + skills/mtg-skill-library/, per claude.com/docs/plugins/build)
# Usage: bash .claude/skills/mtg-skill-library/scripts/package.sh [out dir]   (default: current directory)
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
name="$(basename "$here")"
out="$(cd "${1:-.}" && pwd)"
stamp="$(date +%Y-%m-%d)"
version="${VERSION:-1.0.$(date +%Y%m%d)}"
skill_zip="$out/$name-skill-$stamp.zip"
plugin_zip="$out/$name-plugin-$stamp.zip"
rm -f "$skill_zip" "$plugin_zip"

# 1. The skill on its own: the skill folder at the top of the zip.
(cd "$(dirname "$here")" && zip -qr "$skill_zip" "$name" -x '*/__pycache__/*' '*.pyc')

# 2. The same skill wrapped as a plugin.
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/$name/.claude-plugin" "$tmp/$name/skills"
cp -r "$here" "$tmp/$name/skills/$name"
find "$tmp/$name" -name '__pycache__' -prune -exec rm -rf {} +
cat > "$tmp/$name/.claude-plugin/plugin.json" <<EOF
{
  "name": "$name",
  "displayName": "MTG Skill Library",
  "version": "$version",
  "description": "MTG's library of the best techniques from the AI skills videos he sends, checked against their source, adapted to his rules and applied to every job: videos, websites, ads, SEO, sales letters and more.",
  "author": { "name": "MTG", "url": "https://mtgtribe.com" }
}
EOF
python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$tmp/$name/.claude-plugin/plugin.json"
(cd "$tmp" && zip -qr "$plugin_zip" "$name" -x '*/__pycache__/*' '*.pyc')
echo "$skill_zip"
echo "$plugin_zip"
