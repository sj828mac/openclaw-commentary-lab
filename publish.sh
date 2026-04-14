#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/sync_case.py
python3 scripts/rebuild_index.py
git add .
git commit -m "chore: publish commentary updates" || true
git push
printf '\nPublished to GitHub Pages: https://sj828mac.github.io/openclaw-commentary-lab/\n'
