#!/usr/bin/env python3
"""
Session start dashboard for turkish-lessons.
Prints: due word count, study streak, next action suggestion.
Requires: Python 3.6+ (stdlib only)
"""

import json
import os
import re
import sys
from datetime import date, datetime, timedelta


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_PATH = os.path.join(BASE, "vocab", "vocab.json")
LEARNER_PATH = os.path.join(BASE, "progress", "learner.md")
SESSION_LOG_HEADER = "## Session Log"


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

def parse_session_log(text):
    """Return sorted list of unique session date strings (YYYY-MM-DD), most recent first."""
    dates = set()
    in_log = False
    for line in text.splitlines():
        if SESSION_LOG_HEADER in line:
            in_log = True
            continue
        if not in_log:
            continue
        if line.startswith("##"):
            break
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            continue
        candidate = parts[1]
        if re.match(r"^\d{4}-\d{2}-\d{2}$", candidate):
            dates.add(candidate)
    return sorted(dates, reverse=True)


def last_session_type(text):
    """Return the 'What was covered' field of the most recent session log row."""
    in_log = False
    last = ""
    for line in text.splitlines():
        if SESSION_LOG_HEADER in line:
            in_log = True
            continue
        if not in_log:
            continue
        if line.startswith("##"):
            break
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3 and re.match(r"^\d{4}-\d{2}-\d{2}$", parts[1]):
            last = parts[2]
    return last


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

    try:
        with open(LEARNER_PATH) as f:
            learner = f.read()
        dates = parse_session_log(learner)
        streak, last_date = calculate_streak(dates)
        session_type = last_session_type(learner)
    except FileNotFoundError:
        dates, streak, last_date, session_type = [], 0, None, ""

    print(f"{due} word{'s' if due != 1 else ''} due for review")
    print(format_streak(streak, last_date))
    print(f"Suggested: {suggest_next(due, last_date, session_type)}")


if __name__ == "__main__":
    main()
