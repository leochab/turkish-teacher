# Turkish Teacher

A Claude Code-powered Turkish language learning environment. Open this folder in Claude Code and you have a full Turkish tutor at your fingertips — morphology breakdown, spaced repetition, conversation practice, and a CEFR-aligned curriculum.

## Quick Start

1. **Open this folder in Claude Code**
   ```
   cd turkish-teacher
   claude
   ```
   > Requires Python 3.6+ (stdlib only — no pip install needed). Verify with `python3 --version`.

2. **Start learning**
   Just talk to Claude — it will initialize your files, walk you through filling in your profile on first launch, then start the session. Or jump straight to a slash command.

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/lesson [topic]` | Structured lesson on any grammar or vocabulary topic |
| `/parse [word]` | Full morpheme-by-morpheme breakdown of any Turkish word or sentence |
| `/quiz` | 10-question quiz based on your level and weak spots |
| `/review` | Spaced repetition review of vocabulary due today |
| `/sohbet` | Turkish-only conversation mode with inline corrections |
| `/setup` | Onboarding flow to set or update your learner profile |
| `/help` | Show available commands and where to start |

**Examples:**
```
/lesson accusative case
/parse evlerinizden
/quiz vowel harmony
/sohbet
```

---

## Folder Structure

```
turkish-teacher/
├── README.md               ← this file
├── CLAUDE.md               ← teacher persona (read by Claude automatically)
├── templates/              ← clean copies; edit here to change structure
│   ├── progress/learner.md
│   ├── vocab/vocab.json
│   ├── curriculum/index.json
│   └── data/               ← session-log.json, mastery-db.json, mistakes-db.json, progress-db.json
├── schemas/                ← JSON Schema Draft-07 files for all data structures
├── progress/
│   └── learner.md          ← YOUR profile (gitignored — init with bootstrap.sh)
├── vocab/
│   ├── README.md           ← vocab bank format & SRS field reference
│   └── vocab.json          ← all vocabulary + SRS state (gitignored)
├── curriculum/
│   ├── index.json          ← topic map + completion tracker (gitignored)
│   └── reference.md        ← linguistic reference (cases, harmony, suffix ordering)
├── data/                   ← runtime data files (gitignored — init with bootstrap.sh)
│   ├── session-log.json    ← session history (single source of truth)
│   ├── mastery-db.json     ← per-skill mastery levels (0–5)
│   ├── mistakes-db.json    ← structured recurring mistake entries
│   └── progress-db.json    ← session accuracy + topic-level accuracy
├── scripts/
│   ├── bootstrap.sh          ← init working files from templates/
│   ├── curriculum_query.py   ← read/write curriculum/index.json (mark topics complete)
│   ├── session_start.py      ← deterministic dashboard (due words, streak, suggestion)
│   ├── session_log_append.py ← appends a session entry to data/session-log.json
│   ├── mastery_update.py     ← read/update skill mastery levels in data/mastery-db.json
│   ├── mistakes_update.py    ← add/read recurring mistakes in data/mistakes-db.json
│   ├── progress_update.py    ← log sessions and query progress in data/progress-db.json
│   └── srs_update.py         ← applies SM-2 scheduling after each vocab card
└── .claude/
    └── commands/           ← slash command definitions
```

---

## Curriculum

Full A1–C1 CEFR curriculum following the TOMER / Yunus Emre Institute progression. See `curriculum/index.json` for the complete topic map with prerequisites.

Progress is tracked automatically in `curriculum/index.json` — Claude marks topics complete after each `/lesson`.

---

## Turkish in a Nutshell

Turkish is **agglutinative** (suffixes stack onto roots), uses **vowel harmony** (suffix vowels match the stem), and follows **SOV word order** (Subject → Object → Verb). Once you internalize these three systems, the rest falls into place.

Example: **evlerinizden** = ev + ler + iniz + den = house + PL + 2PL.POSS + ABL = *"from your houses"*

This system is what makes Turkish feel hard at first and beautifully logical once it clicks.

---

## Contributing

Lessons are delivered dynamically by the `/lesson` skill. The skill structure is defined in `.claude/commands/lesson.md`. See `curriculum/index.json` for the full topic list and prerequisites.
