#!/usr/bin/env python3
"""
Read or update the mastery database at data/mastery-db.json.

Usage:
  python3 scripts/mastery_update.py --skill speaking --level 3     # set absolute
  python3 scripts/mastery_update.py --skill grammar --delta +1     # increment (clamped 0–5)
  python3 scripts/mastery_update.py --delta -1 --skill writing     # decrement
  python3 scripts/mastery_update.py --read                         # print table

--read output:
  speaking   : 3/5  (updated 2026-03-28)
  reading    : 5/5  (updated 2026-03-25)
  ...

Every write appends {"date": "YYYY-MM-DD", "level": N} to history and updates `updated`.
Level is clamped to 0–5. Uses atomic write (tempfile → shutil.move).
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
MASTERY_DB = os.path.join(BASE, "data", "mastery-db.json")
TEMPLATE_DB = os.path.join(BASE, "templates", "data", "mastery-db.json")

VALID_SKILLS = {"speaking", "reading", "writing", "grammar", "vocabulary"}
LEVEL_MIN = 0
LEVEL_MAX = 5


def load_db():
    """Load mastery DB; fall back to template structure if file missing."""
    if os.path.exists(MASTERY_DB):
        with open(MASTERY_DB, encoding="utf-8") as f:
            return json.load(f)
    # Initialize from template
    with open(TEMPLATE_DB, encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    """Atomically write db to MASTERY_DB."""
    db_dir = os.path.dirname(MASTERY_DB)
    os.makedirs(db_dir, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=db_dir, delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            json.dump(db, tmp, ensure_ascii=False, indent=2)
            tmp.write("\n")
            tmp_path = tmp.name
        shutil.move(tmp_path, MASTERY_DB)
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def read_table(db):
    """Print a human-readable table of all skills."""
    updated_global = db.get("updated")
    skills = db.get("skills", {})
    for skill in ("speaking", "reading", "writing", "grammar", "vocabulary"):
        info = skills.get(skill, {"level": 0, "history": []})
        level = info.get("level", 0)
        history = info.get("history", [])
        # Find last date this skill was updated
        if history:
            last_date = history[-1].get("date", updated_global or "never")
        else:
            last_date = updated_global or "never"
        print(f"{skill:<10}: {level}/{LEVEL_MAX}  (updated {last_date})")


def update_skill(db, skill, new_level):
    """Set skill level and record history entry."""
    today = date.today().isoformat()
    skills = db.setdefault("skills", {})
    if skill not in skills:
        skills[skill] = {"level": 0, "history": []}
    skills[skill]["level"] = new_level
    skills[skill].setdefault("history", []).append({"date": today, "level": new_level})
    db["updated"] = today


def main():
    parser = argparse.ArgumentParser(
        description="Read or update the mastery database."
    )
    parser.add_argument("--read", action="store_true",
                        help="Print current mastery table and exit")
    parser.add_argument("--skill", choices=sorted(VALID_SKILLS),
                        help="Skill to update")
    parser.add_argument("--level", type=int, default=None,
                        help="Set absolute level (0–5)")
    parser.add_argument("--delta", type=str, default=None,
                        help="Increment/decrement level (e.g. +1, -1)")
    args = parser.parse_args()

    try:
        db = load_db()
    except Exception as e:
        print(f"Failed to load mastery DB: {e}", file=sys.stderr)
        sys.exit(1)

    if args.read:
        read_table(db)
        return

    # Write mode — skill is required
    if not args.skill:
        print("--skill is required for write operations.", file=sys.stderr)
        sys.exit(1)

    if args.level is None and args.delta is None:
        print("Either --level or --delta is required.", file=sys.stderr)
        sys.exit(1)

    if args.level is not None and args.delta is not None:
        print("Specify only one of --level or --delta.", file=sys.stderr)
        sys.exit(1)

    skill_data = db.get("skills", {}).get(args.skill, {"level": 0, "history": []})
    current_level = skill_data.get("level", 0)

    if args.level is not None:
        new_level = max(LEVEL_MIN, min(LEVEL_MAX, args.level))
    else:
        # Parse delta: accepts "+1", "-1", "1", "-2", etc.
        delta_str = args.delta.strip()
        try:
            delta = int(delta_str)
        except ValueError:
            print(f"Invalid --delta value '{args.delta}'. Use e.g. +1 or -1.", file=sys.stderr)
            sys.exit(1)
        new_level = max(LEVEL_MIN, min(LEVEL_MAX, current_level + delta))

    update_skill(db, args.skill, new_level)

    try:
        save_db(db)
    except Exception as e:
        print(f"Failed to save mastery DB: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Updated {args.skill}: {current_level} → {new_level}")


if __name__ == "__main__":
    main()
