#!/usr/bin/env bash
# Initialize working files from templates.
# Safe to re-run: skips any file that already exists.

set -euo pipefail

# Always run from the repository root regardless of invocation directory
cd "$(dirname "$0")/.."

# Ensure the data directory exists
mkdir -p data

FILES=(
  "progress/learner.md"
  "vocab/vocab.json"
  "curriculum/index.json"
  "data/session-log.json"
  "data/mastery-db.json"
  "data/mistakes-db.json"
  "data/progress-db.json"
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
