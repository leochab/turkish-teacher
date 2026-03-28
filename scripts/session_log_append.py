#!/usr/bin/env python3
"""
Append a session log row to progress/learner.md and data/session-log.json.

Usage:
  python3 scripts/session_log_append.py \\
    --date 2026-03-26 \\
    --command "/review" \\
    --vocab "kitap, ev" \\
    --notes "5/7 correct; missed: araba" \\
    [--accuracy 0.72] \\
    [--duration 25]

  --date       YYYY-MM-DD (defaults to today)
  --command    What was covered (e.g. /review, /lesson accusative, free-form chat)
  --vocab      New vocab added, or — if none (default: —)
  --notes      Session notes
  --accuracy   Float 0.0–1.0 (optional)
  --duration   Duration in minutes (optional integer)

The row is appended under the first "## Session Log" table found in learner.md.
A JSON object is also appended to data/session-log.json.
Exits with code 1 and prints an error on failure.
Requires: Python 3.6+ (stdlib only)
"""

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARNER_PATH = os.path.join(BASE, "progress", "learner.md")
SESSION_LOG_JSON = os.path.join(BASE, "data", "session-log.json")
SESSION_LOG_HEADER = "## Session Log"


def escape_cell(value):
    """Escape pipe characters inside a table cell."""
    return value.replace("|", "\\|")


def build_row(date_str, command, vocab, notes):
    for field_name, value in [("date", date_str), ("command", command),
                               ("vocab", vocab), ("notes", notes)]:
        if "\n" in value or "\r" in value:
            raise ValueError(f"--{field_name} contains a newline, which would break the markdown table")
    cells = [date_str, command, vocab, notes]
    return "| " + " | ".join(escape_cell(c) for c in cells) + " |"


def find_table_bounds(lines):
    """
    Return (header_idx, separator_idx, first_data_idx, last_data_idx) for the
    Session Log table, or raise ValueError if the table cannot be found.
    """
    in_session_log = False
    header_idx = separator_idx = None

    for i, line in enumerate(lines):
        if SESSION_LOG_HEADER in line:
            in_session_log = True
            continue
        if not in_session_log:
            continue
        # Stop scanning if we hit another section header
        if line.startswith("##") and SESSION_LOG_HEADER not in line:
            break
        stripped = line.strip()
        if header_idx is None and stripped.startswith("|") and "Date" in stripped:
            header_idx = i
            continue
        if header_idx is not None and separator_idx is None:
            if stripped.startswith("|") and re.match(r"^\|[-| :]+\|$", stripped):
                separator_idx = i
                continue

    if header_idx is None or separator_idx is None:
        raise ValueError(
            f"Could not find the Session Log table in {LEARNER_PATH}.\n"
            "Expected a markdown table with a 'Date' column under '## Session Log'."
        )

    # Find the range of existing data rows (including blank placeholder rows)
    first_data_idx = separator_idx + 1
    last_data_idx = separator_idx  # start below separator

    for i in range(first_data_idx, len(lines)):
        stripped = lines[i].strip()
        if not stripped:
            break  # blank line ends the table
        if stripped.startswith("##"):
            break  # next section ends the table
        if stripped.startswith("|"):
            last_data_idx = i

    return header_idx, separator_idx, first_data_idx, last_data_idx


def append_row(content, new_row):
    lines = content.splitlines(keepends=True)

    # Normalise: ensure file ends with a newline for consistent reconstruction
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"

    _, _, first_data_idx, last_data_idx = find_table_bounds(lines)

    # Collect existing data rows, dropping blank placeholder rows (all pipes, no dates)
    data_rows = []
    for i in range(first_data_idx, last_data_idx + 1):
        stripped = lines[i].strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        # Skip rows where all cells are empty (placeholder rows)
        if any(c for c in cells):
            data_rows.append(lines[i])

    # Build replacement: existing real rows + new row
    new_row_line = new_row + "\n"
    replacement = data_rows + [new_row_line]

    # If there is non-blank content immediately after the table, insert a blank
    # line separator so the markdown heading/paragraph is not glued to the table.
    remaining = lines[last_data_idx + 1:]
    if remaining and remaining[0].strip():
        replacement.append("\n")

    new_lines = lines[:first_data_idx] + replacement + remaining
    return "".join(new_lines)


def append_json_entry(date_str, command, vocab, notes, accuracy, duration):
    """Append a JSON entry to data/session-log.json using atomic write."""
    json_dir = os.path.dirname(SESSION_LOG_JSON)
    os.makedirs(json_dir, exist_ok=True)

    # Load existing entries (initialize to [] if file missing or empty)
    if os.path.exists(SESSION_LOG_JSON):
        try:
            with open(SESSION_LOG_JSON, encoding="utf-8") as f:
                entries = json.load(f)
        except (json.JSONDecodeError, ValueError):
            entries = []
    else:
        entries = []

    entry = {
        "date": date_str,
        "command": command,
        "vocab_added": vocab,
        "notes": notes,
        "accuracy": accuracy,
        "duration_minutes": duration,
    }
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
        raise e


def main():
    parser = argparse.ArgumentParser(
        description="Append a row to the Session Log in progress/learner.md and data/session-log.json."
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

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date):
        print(f"Invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(LEARNER_PATH) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"learner.md not found at {LEARNER_PATH}", file=sys.stderr)
        sys.exit(1)

    try:
        new_row = build_row(args.date, args.command, args.vocab, args.notes)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    try:
        updated = append_row(content, new_row)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=os.path.dirname(LEARNER_PATH),
            delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            tmp.write(updated)
            tmp_path = tmp.name
        shutil.move(tmp_path, LEARNER_PATH)
    except Exception as e:
        print(f"Failed to write session log: {e}", file=sys.stderr)
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        sys.exit(1)

    try:
        append_json_entry(args.date, args.command, args.vocab, args.notes,
                          args.accuracy, args.duration)
    except Exception as e:
        print(f"Warning: failed to write JSON session log: {e}", file=sys.stderr)
        # Don't exit 1 — markdown write already succeeded

    print(f"Session log updated: {args.date} | {args.command} | {args.vocab} | {args.notes}")


if __name__ == "__main__":
    main()
