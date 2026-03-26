# Turkish Teacher

A Claude Code-powered Turkish language learning environment. Open this folder in Claude Code and you have a full Turkish tutor at your fingertips — morphology breakdown, spaced repetition, conversation practice, and a CEFR-aligned curriculum.

## Quick Start

1. **Fill in your learner profile**
   Open `progress/learner.md` and fill in your level, goals, and native language. Claude reads this at the start of every session to personalize the teaching.

2. **Open this folder in Claude Code**
   ```
   cd turkish-lessons
   claude
   ```
   > Requires Python 3.6+ (stdlib only — no pip install needed). Verify with `python3 --version`.

3. **Start learning**
   Just talk to Claude — or use one of the slash commands below.

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
├── progress/
│   └── learner.md          ← YOUR profile — fill this in first
├── vocab/
│   ├── README.md           ← vocab bank format & SRS field reference
│   └── vocab.json          ← all vocabulary + SRS state (auto-populated)
├── curriculum/
│   ├── index.md            ← full CEFR curriculum map (A1–C1)
│   └── reference.md        ← linguistic reference (cases, harmony, suffix ordering)
├── scripts/
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
