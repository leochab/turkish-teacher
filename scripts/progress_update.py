#!/usr/bin/env python3
"""
Log sessions and query progress data in data/progress-db.json.

Usage:
  # Log a completed session
  python3 scripts/progress_update.py \\
    --command "/writing" --skill writing \\
    --accuracy 0.72 --duration 25 \\
    --topic "past tense" --vocab-added 3 \\
    --notes "scored 7/10"

  # Update topic-level accuracy
  python3 scripts/progress_update.py \\
    --update-topic "dative case" --attempts 5 --correct 3

  # Print summary block
  python3 scripts/progress_update.py --summary

  # Adaptive difficulty queries
  python3 scripts/progress_update.py --check-topic "dative case"
  python3 scripts/progress_update.py --weak-topics --threshold 0.65 --min-attempts 5

Requires: Python 3.6+ (stdlib only)
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import date, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRESS_DB = os.path.join(BASE, "data", "progress-db.json")
TEMPLATE_DB = os.path.join(BASE, "templates", "data", "progress-db.json")


def load_db():
    """Load progress DB; fall back to template if file is missing."""
    if os.path.exists(PROGRESS_DB):
        with open(PROGRESS_DB, encoding="utf-8") as f:
            return json.load(f)
    with open(TEMPLATE_DB, encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    """Atomically write db to PROGRESS_DB."""
    db_dir = os.path.dirname(PROGRESS_DB)
    os.makedirs(db_dir, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=db_dir, delete=False, suffix=".tmp", encoding="utf-8"
        ) as tmp:
            json.dump(db, tmp, ensure_ascii=False, indent=2)
            tmp.write("\n")
            tmp_path = tmp.name
        shutil.move(tmp_path, PROGRESS_DB)
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def log_session(db, command, skill, accuracy, duration, topic, vocab_added, notes):
    """Append a session record to db['sessions']."""
    today = date.today().isoformat()
    entry = {
        "date": today,
        "command": command or "",
        "skill": skill or "",
        "accuracy": accuracy,
        "duration_minutes": duration,
        "topic": topic or "",
        "vocab_added": vocab_added,
        "notes": notes or "",
    }
    db.setdefault("sessions", []).append(entry)


def update_topic(db, topic, attempts, correct):
    """Merge new attempt counts into topic_accuracy."""
    today = date.today().isoformat()
    topic_accuracy = db.setdefault("topic_accuracy", {})
    if topic in topic_accuracy:
        existing = topic_accuracy[topic]
        existing["attempts"] = existing.get("attempts", 0) + attempts
        existing["correct"] = existing.get("correct", 0) + correct
        existing["last_date"] = today
    else:
        topic_accuracy[topic] = {
            "attempts": attempts,
            "correct": correct,
            "last_date": today,
        }


def _iso_week(d):
    """Return (year, week_number) for a date."""
    return d.isocalendar()[:2]


def _compute_weekly_summary(sessions, week_year, week_num):
    """Summarize sessions belonging to a given ISO week."""
    week_sessions = []
    for s in sessions:
        try:
            d = date.fromisoformat(s["date"])
        except (ValueError, KeyError):
            continue
        if _iso_week(d) == (week_year, week_num):
            week_sessions.append(s)

    if not week_sessions:
        return None

    total_sessions = len(week_sessions)
    total_minutes = sum(s.get("duration_minutes") or 0 for s in week_sessions)
    accuracies = [s["accuracy"] for s in week_sessions if s.get("accuracy") is not None]
    avg_accuracy = round(sum(accuracies) / len(accuracies), 3) if accuracies else None
    total_vocab = sum(s.get("vocab_added") or 0 for s in week_sessions)
    topics = list({s["topic"] for s in week_sessions if s.get("topic")})

    return {
        "week": f"{week_year}-W{week_num:02d}",
        "sessions": total_sessions,
        "total_minutes": total_minutes,
        "avg_accuracy": avg_accuracy,
        "vocab_added": total_vocab,
        "topics": topics,
    }


def maybe_build_weekly_summaries(db):
    """
    Compute weekly summaries lazily for any weeks that have fully passed.
    Called when --summary is requested.
    """
    sessions = db.get("sessions", [])
    if not sessions:
        return

    today = date.today()
    current_week = _iso_week(today)

    existing_weeks = {s["week"] for s in db.get("weekly_summaries", [])}

    # Collect all weeks present in session data
    weeks_seen = set()
    for s in sessions:
        try:
            d = date.fromisoformat(s["date"])
            weeks_seen.add(_iso_week(d))
        except (ValueError, KeyError):
            continue

    for (yr, wk) in sorted(weeks_seen):
        week_key = f"{yr}-W{wk:02d}"
        if week_key in existing_weeks:
            continue
        # Only summarize completed weeks (not the current week)
        if (yr, wk) >= current_week:
            continue
        summary = _compute_weekly_summary(sessions, yr, wk)
        if summary:
            db.setdefault("weekly_summaries", []).append(summary)
            existing_weeks.add(week_key)


def print_summary(db):
    """Print a structured text summary block."""
    sessions = db.get("sessions", [])
    topic_accuracy = db.get("topic_accuracy", {})
    weekly_summaries = db.get("weekly_summaries", [])

    total_sessions = len(sessions)
    total_minutes = sum(s.get("duration_minutes") or 0 for s in sessions)
    accuracies = [s["accuracy"] for s in sessions if s.get("accuracy") is not None]
    overall_accuracy = round(sum(accuracies) / len(accuracies), 3) if accuracies else None
    total_vocab = sum(s.get("vocab_added") or 0 for s in sessions)

    print("=== Progress Summary ===")
    print(f"Total sessions    : {total_sessions}")
    print(f"Total study time  : {total_minutes} minutes")
    if overall_accuracy is not None:
        print(f"Overall accuracy  : {overall_accuracy:.0%}")
    else:
        print("Overall accuracy  : n/a")
    print(f"Total vocab added : {total_vocab}")

    if topic_accuracy:
        print("\nTopic accuracy:")
        for topic, data in sorted(topic_accuracy.items()):
            attempts = data.get("attempts", 0)
            correct = data.get("correct", 0)
            ratio = correct / attempts if attempts else 0.0
            last = data.get("last_date", "unknown")
            print(f"  {topic:<30}: {correct}/{attempts} ({ratio:.0%})  last: {last}")

    if weekly_summaries:
        print("\nRecent weekly summaries:")
        for ws in weekly_summaries[-4:]:
            acc_str = f"{ws['avg_accuracy']:.0%}" if ws.get("avg_accuracy") is not None else "n/a"
            print(
                f"  {ws['week']}: {ws['sessions']} sessions, "
                f"{ws['total_minutes']} min, accuracy {acc_str}, "
                f"vocab +{ws['vocab_added']}"
            )


def check_topic(db, topic):
    """Print accuracy stats for one topic."""
    topic_accuracy = db.get("topic_accuracy", {})
    if topic not in topic_accuracy:
        print(f"No data for topic: {topic}")
        return
    data = topic_accuracy[topic]
    attempts = data.get("attempts", 0)
    correct = data.get("correct", 0)
    ratio = correct / attempts if attempts else 0.0
    last = data.get("last_date", "unknown")
    print(f"Topic           : {topic}")
    print(f"Attempts        : {attempts}")
    print(f"Correct         : {correct}")
    print(f"Accuracy        : {ratio:.0%}")
    print(f"Last practiced  : {last}")


def weak_topics(db, threshold, min_attempts):
    """Print all topics below the accuracy threshold with sufficient attempts."""
    topic_accuracy = db.get("topic_accuracy", {})
    weak = []
    for topic, data in topic_accuracy.items():
        attempts = data.get("attempts", 0)
        correct = data.get("correct", 0)
        if attempts < min_attempts:
            continue
        ratio = correct / attempts
        if ratio < threshold:
            weak.append((topic, ratio, attempts, data.get("last_date", "unknown")))

    if not weak:
        print("No weak topics found.")
        return

    weak.sort(key=lambda x: x[1])  # sort by accuracy ascending
    print(f"Weak topics (accuracy < {threshold:.0%}, min {min_attempts} attempts):")
    for topic, ratio, attempts, last in weak:
        print(f"  {topic:<30}: {ratio:.0%}  ({attempts} attempts, last: {last})")


def main():
    parser = argparse.ArgumentParser(
        description="Log sessions and query progress data."
    )

    # Session logging
    parser.add_argument("--command", default=None,
                        help="Command/activity (e.g. /writing, /quiz)")
    parser.add_argument("--skill", default=None,
                        help="Skill area (e.g. writing, grammar)")
    parser.add_argument("--accuracy", type=float, default=None,
                        help="Accuracy as float 0.0–1.0")
    parser.add_argument("--duration", type=int, default=None,
                        help="Duration in minutes")
    parser.add_argument("--topic", default=None,
                        help="Topic covered (e.g. 'past tense')")
    parser.add_argument("--vocab-added", dest="vocab_added", type=int, default=None,
                        help="Number of new vocab items added")
    parser.add_argument("--notes", default=None,
                        help="Session notes")

    # Topic accuracy update
    parser.add_argument("--update-topic", dest="update_topic", default=None,
                        help="Topic to update accuracy for")
    parser.add_argument("--attempts", type=int, default=None,
                        help="Number of attempts (used with --update-topic)")
    parser.add_argument("--correct", type=int, default=None,
                        help="Number of correct answers (used with --update-topic)")

    # Query modes
    parser.add_argument("--summary", action="store_true",
                        help="Print progress summary block and exit")
    parser.add_argument("--check-topic", dest="check_topic", default=None,
                        help="Print accuracy stats for one topic")
    parser.add_argument("--weak-topics", dest="weak_topics", action="store_true",
                        help="Print all topics below accuracy threshold")
    parser.add_argument("--threshold", type=float, default=0.65,
                        help="Accuracy threshold for --weak-topics (default: 0.65)")
    parser.add_argument("--min-attempts", dest="min_attempts", type=int, default=5,
                        help="Minimum attempts for --weak-topics (default: 5)")

    args = parser.parse_args()

    try:
        db = load_db()
    except Exception as e:
        print(f"Failed to load progress DB: {e}", file=sys.stderr)
        sys.exit(1)

    # Query-only modes (no write)
    if args.check_topic:
        check_topic(db, args.check_topic)
        return

    if args.weak_topics:
        weak_topics(db, args.threshold, args.min_attempts)
        return

    if args.summary:
        maybe_build_weekly_summaries(db)
        try:
            save_db(db)
        except Exception as e:
            print(f"Warning: failed to save weekly summaries: {e}", file=sys.stderr)
        print_summary(db)
        return

    # Write modes
    wrote = False

    if args.update_topic:
        if args.attempts is None or args.correct is None:
            print("--attempts and --correct are required with --update-topic.", file=sys.stderr)
            sys.exit(1)
        update_topic(db, args.update_topic, args.attempts, args.correct)
        print(f"Topic accuracy updated: {args.update_topic} (+{args.correct}/{args.attempts})")
        wrote = True

    if args.command:
        log_session(db, args.command, args.skill, args.accuracy,
                    args.duration, args.topic, args.vocab_added, args.notes)
        print(f"Session logged: {args.command}")
        wrote = True

    if not wrote:
        parser.print_help()
        sys.exit(1)

    try:
        save_db(db)
    except Exception as e:
        print(f"Failed to save progress DB: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
