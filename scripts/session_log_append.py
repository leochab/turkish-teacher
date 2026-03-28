#!/usr/bin/env python3
"""
Append a session entry to data/session-log.json (single source of truth).

Usage:
  python3 scripts/session_log_append.py \\
    --command "/review" \\
    --vocab "kitap, ev" \\
    --notes "5/7 correct; missed: araba" \\
    [--date 2026-03-26] \\
    [--accuracy 0.72] \\
    [--duration 25]

  --date       YYYY-MM-DD (defaults to today)
  --command    What was covered (e.g. /review, /lesson accusative, free-form chat)
  --vocab      New vocab added, or — if none (default: —)
  --notes      Session notes
  --accuracy   Float 0.0–1.0 (optional)
  --duration   Duration in minutes (optional integer)

Exits with code 1 and prints an error on failure.
Requires: Python 3.6+ (stdlib only)
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_LOG_JSON = os.path.join(BASE, "data", "session-log.json")


def main():
    parser = argparse.ArgumentParser(
        description="Append a session entry to data/session-log.json."
    )
    parser.add_argument("--date", default=date.today().isoformat(),
                        help="Session date (YYYY-MM-DD, default: today)")
    parser.add_argument("--command", required=True,
                        help="What was covered (e.g. /review, /lesson accusative)")
    parser.add_argument("--vocab", default="—",
                        help="New vocab added, or — if none")
    parser.add_argument("--notes", required=True,
                        help="Session notes")
    parser.add_argument("--accuracy", type=float, default=None,
                        help="Accuracy as a float 0.0–1.0 (optional)")
    parser.add_argument("--duration", type=int, default=None,
                        help="Duration in minutes (optional)")
    args = parser.parse_args()

    try:
        date.fromisoformat(args.date)
    except ValueError:
        print(f"Invalid date '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    if args.accuracy is not None and not (0.0 <= args.accuracy <= 1.0):
        print(f"--accuracy {args.accuracy} out of range. Use a value between 0.0 and 1.0.", file=sys.stderr)
        sys.exit(1)

    json_dir = os.path.dirname(SESSION_LOG_JSON)
    os.makedirs(json_dir, exist_ok=True)

    if os.path.exists(SESSION_LOG_JSON):
        try:
            with open(SESSION_LOG_JSON, encoding="utf-8") as f:
                entries = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"session-log.json is corrupt: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        entries = []

    entry = {
        "date": args.date,
        "command": args.command,
        "vocab_added": args.vocab,
        "notes": args.notes,
    }
    if args.accuracy is not None:
        entry["accuracy"] = args.accuracy
    if args.duration is not None:
        entry["duration_minutes"] = args.duration
    entries.append(entry)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=json_dir,
            delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            json.dump(entries, tmp, ensure_ascii=False, indent=2)
            tmp.write("\n")
            tmp_path = tmp.name
        shutil.move(tmp_path, SESSION_LOG_JSON)
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        print(f"Failed to write session log: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Session logged: {args.date} | {args.command} | {args.vocab} | {args.notes}")


if __name__ == "__main__":
    main()
