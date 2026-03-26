# Turkish Teacher

A Claude Code-powered Turkish language learning environment. Open this folder in Claude Code and you have a full Turkish tutor at your fingertips — morphology breakdown, spaced repetition, conversation practice, and a CEFR-aligned curriculum.

## Quick Start

1. **Initialize your working files**
   ```
   bash scripts/bootstrap.sh
   ```
   This copies the clean templates into their working locations (`progress/learner.md`, `vocab/vocab.json`, `curriculum/index.md`). Safe to re-run — skips files that already exist.
   > Requires Python 3.6+ (stdlib only — no pip install needed). Verify with `python3 --version`.

2. **Open this folder in Claude Code**
   ```
   cd turkish-lessons
   claude
   ```

3. **Start learning**
   Just talk to Claude — it will walk you through filling in your profile on first launch, then start the session. Or jump straight to a slash command.

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/lesson [topic]` | Structured lesson on any grammar or vocabulary topic |
| `/parse [word]` | Full morpheme-by-morpheme breakdown of any Turkish word or sentence |
| `/quiz` | 10-question quiz based on your level and weak spots |
| `/review` | Spaced repetition review of vocabulary due today |
| `/sohbet [scenario]` | Turkish conversation mode with inline corrections |

**Examples:**
```
/lesson accusative case
/parse evlerinizden
/quiz vowel harmony
/sohbet ordering coffee at a café
```

---

## Folder Structure

```
turkish-lessons/
├── README.md               ← this file
├── CLAUDE.md               ← teacher persona (read by Claude automatically)
├── templates/              ← clean copies; edit here to change structure
│   ├── progress/learner.md
│   ├── vocab/vocab.json
│   └── curriculum/index.md
├── progress/
│   └── learner.md          ← YOUR profile (gitignored — init with bootstrap.sh)
├── vocab/
│   ├── README.md           ← vocab bank format & SRS field reference
│   └── vocab.json          ← all vocabulary + SRS state (gitignored)
├── curriculum/
│   ├── index.md            ← topic completion tracker (gitignored)
│   └── reference.md        ← linguistic reference (cases, harmony, suffix ordering)
├── scripts/
│   ├── bootstrap.sh        ← init working files from templates/
│   ├── session_start.py    ← deterministic dashboard (due words, streak, suggestion)
│   ├── session_log_append.py ← appends a row to the session log in learner.md
│   └── srs_update.py       ← applies SM-2 scheduling after each vocab card
└── .claude/
    └── commands/           ← slash command definitions
```

---

## Curriculum

Full A1–C1 CEFR curriculum following the TOMER / Yunus Emre Institute progression. See `curriculum/index.md` for the complete topic map.

Progress is tracked in `progress/learner.md` — check off topics as you complete them.

---

## Turkish in a Nutshell

Turkish is **agglutinative** (suffixes stack onto roots), uses **vowel harmony** (suffix vowels match the stem), and follows **SOV word order** (Subject → Object → Verb). Once you internalize these three systems, the rest falls into place.

Example: **evlerinizden** = ev + ler + iniz + den = house + PL + 2PL.POSS + ABL = *"from your houses"*

This system is what makes Turkish feel hard at first and beautifully logical once it clicks.

---

## Contributing

Lessons are delivered dynamically by the `/lesson` skill. The skill structure is defined in `.claude/commands/lesson.md`. See `curriculum/index.md` for the full topic list and prerequisites.

PRs welcome.
