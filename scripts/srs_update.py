#!/usr/bin/env python3
"""
Apply an SRS rating to a vocab word and update vocab.json.

Usage: python3 scripts/srs_update.py <word> <rating>
  word   — key in vocab.json (Turkish word)
  rating — again | hard | good | easy

Scheduling:
  again  interval = 1,          ease - 0.15 (min 1.0)
  hard   interval = max(1, x1.2), ease - 0.15 (min 1.0)
  good   interval = max(1, x2.0), ease unchanged
  easy   interval = max(1, x2.5), ease + 0.1  (max 5.0)

Exits with code 1 and prints an error on failure.
Requires: Python 3.6+ (stdlib only)
"""

import json
import os
import shutil
import sys
import tempfile
from datetime import date, timedelta
from math import ceil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_PATH = os.path.join(BASE, "vocab", "vocab.json")

MULTIPLIERS = {
    "again": None,   # reset
    "hard":  1.2,
    "good":  2.0,
    "easy":  2.5,
}

EASE_DELTA = {
    "again": -0.15,
    "hard":  -0.15,
    "good":   0.0,
    "easy":  +0.1,
}


def apply_rating(interval, ease, rating):
    mult = MULTIPLIERS[rating]
    new_interval = 1 if mult is None else max(1, ceil(interval * mult))
    new_ease = round(min(5.0, max(1.0, ease + EASE_DELTA[rating])), 2)
    next_review = (date.today() + timedelta(days=new_interval)).isoformat()
    return new_interval, new_ease, next_review


def main():
    if len(sys.argv) != 3:
        print("Usage: srs_update.py <word> <rating>", file=sys.stderr)
        sys.exit(1)

    word, rating = sys.argv[1], sys.argv[2].lower()

    if rating not in MULTIPLIERS:
        print(f"Invalid rating '{rating}'. Use: again / hard / good / easy", file=sys.stderr)
        sys.exit(1)

    try:
        with open(VOCAB_PATH) as f:
            vocab = json.load(f)
    except FileNotFoundError:
        print(f"vocab.json not found at {VOCAB_PATH}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"vocab.json is invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if word not in vocab:
        print(f"Word '{word}' not found in vocab.json", file=sys.stderr)
        sys.exit(1)

    entry = vocab[word]
    interval = entry.get("interval", 1)
    ease = entry.get("ease", 3.0)

    if not isinstance(interval, (int, float)) or not isinstance(ease, (int, float)):
        print(f"Invalid interval or ease for '{word}'", file=sys.stderr)
        sys.exit(1)

    new_interval, new_ease, next_review = apply_rating(interval, ease, rating)

    vocab[word]["interval"] = new_interval
    vocab[word]["ease"] = new_ease
    vocab[word]["next_review"] = next_review

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=os.path.dirname(VOCAB_PATH),
            delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            json.dump(vocab, tmp, ensure_ascii=False, indent=2)
            tmp_path = tmp.name
        shutil.move(tmp_path, VOCAB_PATH)
    except Exception as e:
        print(f"Failed to write vocab.json: {e}", file=sys.stderr)
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        sys.exit(1)

    print(f"{word}: {rating} → next review in {new_interval} day{'s' if new_interval != 1 else ''} ({next_review})")


if __name__ == "__main__":
    main()
