#!/usr/bin/env python3
"""
Add/update mistake entries in data/mistakes-db.json, or read top weak spots.

Usage:
  # Add or increment a mistake entry
  python3 scripts/mistakes_update.py \\
    --category vowel_harmony \\
    --subcategory "dative suffix" \\
    --rule "vowel harmony in dative suffix" \\
    --error-form "kitapa" \\
    --correct-form "kitaba" \\
    --context "learner wrote kitapa in /quiz" \\
    --command "/quiz"

  # Read top N weak spots (output matches analyze_mistakes.py format)
  python3 scripts/mistakes_update.py --read --top 5

Entry schema:
  {
    "id": "uuid-v4",
    "category": "vowel_harmony",
    "subcategory": "dative suffix",
    "rule": "vowel harmony in dative suffix",
    "error_form": "kitapa",
    "correct_form": "kitaba",
    "frequency": 3,
    "first_occurred": "2026-03-01",
    "last_occurred": "2026-03-28",
    "next_review": null,
    "examples": [
      {"date": "2026-03-28", "context": "Learner wrote kitapa", "command": "/quiz"}
    ]
  }

category enum: morphology | vowel_harmony | case | tense | vocabulary | other

Deduplication key: `rule`. If entry with same rule exists, increment frequency
and append to examples.

--read output matches analyze_mistakes.py format exactly.
Requires: Python 3.6+ (stdlib only)
"""

import argparse
import json
import math
import os
import shutil
import sys
import tempfile
import uuid
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISTAKES_DB = os.path.join(BASE, "data", "mistakes-db.json")
TEMPLATE_DB = os.path.join(BASE, "templates", "data", "mistakes-db.json")

VALID_CATEGORIES = {"morphology", "vowel_harmony", "case", "tense", "vocabulary", "other"}

# Decay constant matching analyze_mistakes.py: e^(-λ × 365) ≈ 0.05
LAMBDA = math.log(20) / 365


def load_db():
    if os.path.exists(MISTAKES_DB):
        with open(MISTAKES_DB, encoding="utf-8") as f:
            return json.load(f)
    with open(TEMPLATE_DB, encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    db_dir = os.path.dirname(MISTAKES_DB)
    os.makedirs(db_dir, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=db_dir, delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            json.dump(db, tmp, ensure_ascii=False, indent=2)
            tmp.write("\n")
            tmp_path = tmp.name
        shutil.move(tmp_path, MISTAKES_DB)
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def add_or_update(db, category, subcategory, rule, error_form, correct_form, context, command):
    today = date.today().isoformat()
    entries = db.setdefault("entries", [])

    # Find existing entry by rule (deduplication key)
    existing = next((e for e in entries if e.get("rule") == rule), None)

    example = {"date": today, "context": context or "", "command": command or ""}

    if existing:
        existing["frequency"] = existing.get("frequency", 1) + 1
        existing["last_occurred"] = today
        existing.setdefault("examples", []).append(example)
    else:
        entry = {
            "id": str(uuid.uuid4()),
            "category": category,
            "subcategory": subcategory or "",
            "rule": rule,
            "error_form": error_form or "",
            "correct_form": correct_form or "",
            "frequency": 1,
            "first_occurred": today,
            "last_occurred": today,
            "next_review": None,
            "examples": [example],
        }
        entries.append(entry)


def rank_weak_spots(db, top_n=5):
    """
    Decay-weight entries by recency, rank by score.
    Returns list of (rule, score, last_days_ago).
    Matches analyze_mistakes.py ranking logic.
    """
    today = date.today()
    entries = db.get("entries", [])

    scores = {}
    last_seen = {}

    for entry in entries:
        rule = entry.get("rule", "")
        if not rule:
            continue
        examples = entry.get("examples", [])
        if not examples:
            # Fall back to last_occurred
            date_str = entry.get("last_occurred", "")
            try:
                d = date.fromisoformat(date_str)
                days_ago = max(0, (today - d).days)
            except (ValueError, TypeError):
                days_ago = 730
            weight = math.exp(-LAMBDA * days_ago)
            scores[rule] = scores.get(rule, 0.0) + weight
            if rule not in last_seen or days_ago < last_seen[rule]:
                last_seen[rule] = days_ago
        else:
            for ex in examples:
                date_str = ex.get("date", "")
                try:
                    d = date.fromisoformat(date_str)
                    days_ago = max(0, (today - d).days)
                except (ValueError, TypeError):
                    days_ago = 730
                weight = math.exp(-LAMBDA * days_ago)
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
    """Output format matches analyze_mistakes.py exactly."""
    if not ranked:
        print("No recurring mistakes recorded yet.")
        return
    print("Top weak spots (recent mistakes weighted higher):")
    for i, (rule, score, last_days) in enumerate(ranked, start=1):
        print(f"  {i}. {rule}  (last: {_recency_label(last_days)})")


def main():
    parser = argparse.ArgumentParser(
        description="Add/update mistake entries or read top weak spots."
    )
    parser.add_argument("--read", action="store_true",
                        help="Print top weak spots and exit")
    parser.add_argument("--top", type=int, default=5,
                        help="Number of top weak spots to show (default: 5, used with --read)")
    parser.add_argument("--category", choices=sorted(VALID_CATEGORIES),
                        help="Mistake category")
    parser.add_argument("--subcategory", default="",
                        help="Mistake subcategory")
    parser.add_argument("--rule", default=None,
                        help="Rule description (deduplication key)")
    parser.add_argument("--error-form", dest="error_form", default="",
                        help="The erroneous form produced by learner")
    parser.add_argument("--correct-form", dest="correct_form", default="",
                        help="The correct form")
    parser.add_argument("--context", default="",
                        help="Context of the mistake")
    parser.add_argument("--command", default="",
                        help="Command/activity where mistake occurred")
    args = parser.parse_args()

    try:
        db = load_db()
    except Exception as e:
        print(f"Failed to load mistakes DB: {e}", file=sys.stderr)
        sys.exit(1)

    if args.read:
        ranked = rank_weak_spots(db, top_n=args.top)
        format_output(ranked)
        return

    # Write mode
    if not args.category:
        print("--category is required when adding a mistake.", file=sys.stderr)
        sys.exit(1)
    if not args.rule:
        print("--rule is required when adding a mistake.", file=sys.stderr)
        sys.exit(1)

    add_or_update(db, args.category, args.subcategory, args.rule,
                  args.error_form, args.correct_form, args.context, args.command)

    try:
        save_db(db)
    except Exception as e:
        print(f"Failed to save mistakes DB: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Mistake recorded: [{args.category}] {args.rule}")


if __name__ == "__main__":
    main()
