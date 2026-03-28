#!/usr/bin/env bash
# Initialize working files from templates.
# Safe to re-run: skips any file that already exists.

set -euo pipefail

FILES=(
  "progress/learner.md"
  "vocab/vocab.json"
  "curriculum/index.json"
)

for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    echo "skip  $f  (already exists)"
  else
    cp "templates/$f" "$f"
    echo "init  $f"
  fi
done

echo "Done."
