#!/usr/bin/env bash
# Package this skill as a zip MTG can upload to his Claude account (Settings, Capabilities, Skills),
# so the library works in all his projects, not only this repository.
# Usage: bash .claude/skills/mtg-skill-library/scripts/package.sh [out dir]   (default: current directory)
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
out="$(cd "${1:-.}" && pwd)"
stamp="$(date +%Y-%m-%d)"
zip_path="$out/mtg-skill-library-$stamp.zip"
rm -f "$zip_path"
(cd "$(dirname "$here")" && zip -qr "$zip_path" "$(basename "$here")" -x '*/__pycache__/*' '*.pyc')
echo "$zip_path"
