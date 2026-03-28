#!/usr/bin/env python3
"""
Session start dashboard for turkish-lessons.
Prints: due word count, study streak, next action suggestion, top weak spots.
Requires: Python 3.6+ (stdlib only)
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

# Import shared parser from analyze_mistakes (same scripts/ directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_mistakes import rank_weak_spots, _recency_label  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_PATH = os.path.join(BASE, "vocab", "vocab.json")
LEARNER_PATH = os.path.join(BASE, "progress", "learner.md")
SESSION_LOG_JSON = os.path.join(BASE, "data", "session-log.json")


# --- Vocab ---

def count_due_words():
    try:
        with open(VOCAB_PATH) as f:
            vocab = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
    today = date.today().isoformat()
    return sum(
        1 for v in vocab.values()
        if isinstance(v.get("next_review"), str) and v["next_review"] <= today
    )


# --- Session log ---

def load_sessions():
    """Return list of session entries from data/session-log.json, oldest first."""
    try:
        with open(SESSION_LOG_JSON, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def session_dates(sessions):
    """Return sorted list of unique session date strings, most recent first."""
    dates = set()
    for s in sessions:
        d = s.get("date", "")
        if d:
            dates.add(d)
    return sorted(dates, reverse=True)


def last_session_command(sessions):
    """Return the command field of the most recent session entry."""
    for s in reversed(sessions):
        cmd = s.get("command", "")
        if cmd:
            return cmd
    return ""


# --- Streak ---

def calculate_streak(dates):
    """
    Count consecutive days ending at today or yesterday.
    Returns (streak, last_session_date).
    """
    if not dates:
        return 0, None

    date_set = set(dates)
    today = date.today()
    yesterday = today - timedelta(days=1)
    last = datetime.strptime(dates[0], "%Y-%m-%d").date()

    # Streak is only alive if studied today or yesterday
    if today.isoformat() in date_set:
        start = today
    elif yesterday.isoformat() in date_set:
        start = yesterday
    else:
        return 0, last

    streak = 0
    current = start
    while current.isoformat() in date_set:
        streak += 1
        current -= timedelta(days=1)

    return streak, last


def format_streak(streak, last_date):
    if last_date is None:
        return "No sessions yet — let's start your streak today."

    today = date.today()
    days_ago = (today - last_date).days
    studied_today = last_date == today

    if streak == 0:
        return f"Streak reset — last studied {days_ago} day{'s' if days_ago != 1 else ''} ago"
    if streak == 1 and studied_today:
        return "Day 1 — streak started!"
    if studied_today:
        return f"🔥 {streak}-day streak"
    return f"🔥 {streak}-day streak — keep it going"


# --- Weak spots ---

def get_top_weak_spots(text, top_n=3):
    """Return top_n decay-weighted weak spots as (rule, score, last_days) tuples."""
    return rank_weak_spots(text, top_n=top_n)


# --- Next action ---

def suggest_next(due_count, last_date, session_type):
    today = date.today()
    if due_count > 0:
        return f"/review  ({due_count} word{'s' if due_count != 1 else ''} due)"
    if last_date and (today - last_date).days >= 3:
        return "/quiz  (check retention — 3+ days since last session)"
    if session_type and "/lesson" in session_type:
        topic = session_type.replace("/lesson", "").strip()
        suffix = f" {topic}" if topic else ""
        return f"/lesson{suffix}  (continue from last session)"
    return "/lesson  (start or continue a topic)"


# --- Main ---

def main():
    due = count_due_words()

    sessions = load_sessions()
    dates = session_dates(sessions)
    streak, last_date = calculate_streak(dates)
    session_type = last_session_command(sessions)

    try:
        with open(LEARNER_PATH) as f:
            learner = f.read()
        weak_spots = get_top_weak_spots(learner)
    except FileNotFoundError:
        weak_spots = []

    print(f"{due} word{'s' if due != 1 else ''} due for review")
    print(format_streak(streak, last_date))
    print(f"Suggested: {suggest_next(due, last_date, session_type)}")
    if weak_spots:
        print("Top weak spots:")
        for rank, (rule, _score, last_days) in enumerate(weak_spots, start=1):
            print(f"  {rank}. {rule}  (last: {_recency_label(last_days)})")


if __name__ == "__main__":
    main()
