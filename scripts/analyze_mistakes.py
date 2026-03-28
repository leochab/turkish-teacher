#!/usr/bin/env python3
"""
Analyze the Recurring Mistakes table in progress/learner.md.
Ranks weak spots using exponential time decay so recent mistakes
outweigh old ones. A mistake made ~1 year ago retains ~5% weight.

Usage:
  python3 scripts/analyze_mistakes.py [--top N]

  --top N   Number of top weak spots to show (default: 5)

Output is printed to stdout for consumption by Claude during /quiz and /lesson.
Requires: Python 3.6+ (stdlib only)
"""

import argparse
import math
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARNER_PATH = os.path.join(BASE, "progress", "learner.md")
MISTAKES_HEADER = "## Recurring Mistakes"

# λ chosen so that e^(-λ × 365) ≈ 0.05: a mistake fades to ~5% after one year.
LAMBDA = math.log(20) / 365  # ≈ 0.0082 per day


def parse_mistakes_table(text):
    """
    Parse the Recurring Mistakes table from learner.md.
    Returns a list of (rule, date_str) tuples.
    Rows with an empty Rule column are skipped.
    date_str is "" when the date cell is absent or unparseable.
    """
    entries = []
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
        if not rule or rule in ("—", "-"):
            continue

        date_str = parts[0].strip()
        entries.append((rule, date_str))

    return entries


def rank_weak_spots(text, top_n=5, today=None, lam=LAMBDA):
    """
    Decay-weight each row by how long ago it was recorded, then rank rules.
    Rules that caused mistakes recently score higher than rules only seen long ago.

    Returns a list of (rule, score, last_seen_days_ago) sorted by score desc,
    capped at top_n entries.
    """
    if today is None:
        today = date.today()

    entries = parse_mistakes_table(text)

    scores = {}    # rule -> cumulative decay score
    last_seen = {}  # rule -> days since most recent occurrence

    for rule, date_str in entries:
        try:
            d = date.fromisoformat(date_str)
            days_ago = max(0, (today - d).days)
        except (ValueError, TypeError):
            days_ago = 730  # missing / invalid date → treat as ~2 years old

        weight = math.exp(-lam * days_ago)
        scores[rule] = scores.get(rule, 0.0) + weight
        if rule not in last_seen or days_ago < last_seen[rule]:
            last_seen[rule] = days_ago

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [(rule, score, last_seen[rule]) for rule, score in ranked]


def _recency_label(days_ago):
    if days_ago == 0:
        return "today"
    if days_ago == 1:
        return "yesterday"
    return f"{days_ago} days ago"


def format_output(ranked):
    if not ranked:
        print("No recurring mistakes recorded yet.")
        return

    print("Top weak spots (recent mistakes weighted higher):")
    for i, (rule, score, last_days) in enumerate(ranked, start=1):
        print(f"  {i}. {rule}  (last: {_recency_label(last_days)})")


def main():
    parser = argparse.ArgumentParser(
        description="Rank weak spots by decay-weighted mistake frequency."
    )
    parser.add_argument("--top", type=int, default=5,
                        help="Number of top weak spots to show (default: 5)")
    args = parser.parse_args()

    try:
        with open(LEARNER_PATH) as f:
            text = f.read()
    except FileNotFoundError:
        print("progress/learner.md not found — no mistakes recorded yet.", file=sys.stderr)
        sys.exit(1)

    ranked = rank_weak_spots(text, top_n=args.top)
    format_output(ranked)


if __name__ == "__main__":
    main()
