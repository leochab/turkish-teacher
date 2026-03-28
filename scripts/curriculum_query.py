#!/usr/bin/env python3
"""
curriculum_query.py — utility module for reading/writing curriculum/index.json.

Public API
----------
get_next_topic(level)        -> dict | None
mark_complete(level, number) -> None
count_complete(level)        -> tuple[int, int]
all_complete(level)          -> bool
get_topic(level, number)     -> dict

Debug flag
----------
Run directly to inspect the curriculum:
    python3 scripts/curriculum_query.py --check [level]
    python3 scripts/curriculum_query.py --mark <level> <number>
"""

import contextlib
import json
import os
import sys
import tempfile

_CURRICULUM_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "curriculum", "index.json",
)


def _load() -> dict:
    try:
        with open(_CURRICULUM_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"curriculum/index.json not found — run 'bash scripts/bootstrap.sh' first.\n"
            f"(Expected path: {_CURRICULUM_PATH})"
        ) from None


def _save(data: dict) -> None:
    """Atomic write: write to a temp file then rename."""
    dir_ = os.path.dirname(_CURRICULUM_PATH)
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".curriculum_tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, _CURRICULUM_PATH)
    except Exception:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def _find_level(data: dict, level: str) -> dict | None:
    for lvl in data["levels"]:
        if lvl["level"].upper() == level.upper():
            return lvl
    return None


def _find_topic(lvl: dict, number: int) -> dict | None:
    for topic in lvl["topics"]:
        if topic["number"] == number:
            return topic
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_next_topic(level: str) -> dict | None:
    """Return the first uncompleted topic dict at *level*, or None if all done."""
    data = _load()
    lvl = _find_level(data, level)
    if lvl is None:
        raise ValueError(f"Unknown level: {level!r}")
    for topic in lvl["topics"]:
        if not topic.get("completed", False):
            return topic
    return None


def mark_complete(level: str, number: int) -> None:
    """Set completed=true for the topic at *level* with the given *number*."""
    data = _load()
    lvl = _find_level(data, level)
    if lvl is None:
        raise ValueError(f"Unknown level: {level!r}")
    topic = _find_topic(lvl, number)
    if topic is None:
        raise ValueError(f"Topic {number} not found in level {level!r}")
    topic["completed"] = True
    _save(data)


def count_complete(level: str) -> tuple:
    """Return (completed_count, total_count) for *level*."""
    data = _load()
    lvl = _find_level(data, level)
    if lvl is None:
        raise ValueError(f"Unknown level: {level!r}")
    topics = lvl["topics"]
    done = sum(1 for t in topics if t.get("completed", False))
    return done, len(topics)


def all_complete(level: str) -> bool:
    done, total = count_complete(level)
    return done == total


def get_topic(level: str, number: int) -> dict:
    """Return the topic dict for *level*/*number*. Raises ValueError if not found."""
    data = _load()
    lvl = _find_level(data, level)
    if lvl is None:
        raise ValueError(f"Unknown level: {level!r}")
    topic = _find_topic(lvl, number)
    if topic is None:
        raise ValueError(f"Topic {number} not found in level {level!r}")
    return topic


# ---------------------------------------------------------------------------
# CLI (debug / session-close helper)
# ---------------------------------------------------------------------------

def _cmd_check(level: str | None) -> None:
    data = _load()
    levels = data["levels"] if level is None else [_find_level(data, level)]
    for lvl in levels:
        if lvl is None:
            print(f"Level not found.", file=sys.stderr)
            sys.exit(1)
        done, total = count_complete(lvl["level"])
        print(f"\n{lvl['level']} — {done}/{total} complete")
        for t in lvl["topics"]:
            mark = "✓" if t.get("completed") else " "
            print(f"  [{mark}] {t['number']:02d}. {t['topic']}")


def _cmd_mark(level: str, number: int) -> None:
    mark_complete(level, number)
    topic = get_topic(level, number)
    done, total = count_complete(level)
    print(f"Marked complete: {level}/{number:02d} — {topic['topic']}")
    print(f"Progress: {done}/{total} topics complete in {level}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--check":
        level_arg = args[1].upper() if len(args) > 1 else None
        _cmd_check(level_arg)
    elif args[0] == "--mark":
        if len(args) < 3:
            print("Usage: curriculum_query.py --mark <LEVEL> <NUMBER>", file=sys.stderr)
            sys.exit(1)
        _cmd_mark(args[1].upper(), int(args[2]))
    else:
        print(__doc__)
        sys.exit(0)
