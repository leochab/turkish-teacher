#!/usr/bin/env python3
"""
Analyze the Recurring Mistakes table in progress/learner.md.
Aggregates errors by rule type and prints a ranked list of weak spots.

Usage:
  python3 scripts/analyze_mistakes.py [--top N]

  --top N   Number of top weak spots to show (default: 5)

Output is printed to stdout for consumption by Claude during /quiz and /lesson.
Requires: Python 3.6+ (stdlib only)
"""

import argparse
import os
import re
import sys
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARNER_PATH = os.path.join(BASE, "progress", "learner.md")
MISTAKES_HEADER = "## Recurring Mistakes"


def parse_mistakes_table(text):
    """
    Parse the Recurring Mistakes table from learner.md.
    Returns a list of rule strings (one per data row).
    Rows with empty Rule column are skipped.
    """
    rules = []
    in_section = False
    in_table = False
    past_separator = False

    for line in text.splitlines():
        if MISTAKES_HEADER in line:
            in_section = True
            continue
        if not in_section:
            continue
        # Stop at next section
        if line.startswith("##") and MISTAKES_HEADER not in line:
            break

        stripped = line.strip()
        if not stripped.startswith("|"):
            continue

        # Detect the header row by looking for "Rule" column
        if not in_table:
            if re.search(r"\|\s*Rule\s*\|", stripped, re.IGNORECASE):
                in_table = True
            continue

        # Skip the separator row (|---|---|...).
        # Require ≥2 dashes per cell so filler rows like "| - | - |" don't match.
        if not past_separator:
            if re.match(r"^\|(\s*:?-{2,}:?\s*\|)+$", stripped):
                past_separator = True
            continue

        # Parse data row — columns: Date | Error | Correct form | Rule
        parts = [p.strip() for p in stripped.strip("|").split("|")]
        if len(parts) < 4:
            continue

        rule = parts[3].strip()
        if rule and rule not in ("", "—", "-"):
            rules.append(rule)

    return rules


def format_output(counts, top_n):
    if not counts:
        print("No recurring mistakes recorded yet.")
        return

    print("Top weak spots (by frequency):")
    for rank, (rule, count) in enumerate(counts.most_common(top_n), start=1):
        times = f"×{count}"
        print(f"  {rank}. {rule} ({times})")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Recurring Mistakes table and rank weak spots."
    )
    parser.add_argument("--top", type=int, default=5,
                        help="Number of top weak spots to show (default: 5)")
    args = parser.parse_args()

    try:
        with open(LEARNER_PATH) as f:
            text = f.read()
    except FileNotFoundError:
        print("No mistakes recorded yet (progress/learner.md not found).", file=sys.stderr)
        sys.exit(1)

    rules = parse_mistakes_table(text)
    counts = Counter(rules)
    format_output(counts, args.top)


if __name__ == "__main__":
    main()
