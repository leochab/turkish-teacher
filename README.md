# Turkish Teacher

A Claude Code-powered Turkish language learning environment. Open this folder in Claude Code and you have a full Turkish tutor at your fingertips — morphology breakdown, spaced repetition, OCR-to-lesson pipeline, conversation practice, and a CEFR-aligned curriculum.

## Quick Start

1. **Fill in your learner profile**
   Open `progress/learner.md` and fill in your level, goals, and native language. Claude reads this at the start of every session to personalize the teaching.

2. **Open this folder in Claude Code**
   ```
   cd turkish-lessons
   claude
   ```

3. **Start learning**
   Just talk to Claude — or use one of the slash commands below.

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/lesson [topic]` | Structured lesson on any grammar or vocabulary topic |
| `/parse [word]` | Full morpheme-by-morpheme breakdown of any Turkish word or sentence |
| `/scan` | Process OCR text from `scans/` — vocabulary, grammar, translation |
| `/quiz` | 10-question quiz based on your level and weak spots |
| `/review` | Spaced repetition review of vocabulary due today |
| `/sohbet [scenario]` | Turkish conversation mode with inline corrections |

**Examples:**
```
/lesson accusative case
/parse evlerinizden
/scan scans/2026-03-25-menu.txt
/quiz vowel harmony
/sohbet ordering coffee at a café
```

---

## OCR Workflow (with Handy or similar)

1. Photograph Turkish text (menu, sign, book page, subtitle)
2. Run OCR → copy text to a `.txt` file in `scans/`
3. Run `/scan` — Claude cleans the text, translates it, extracts vocabulary, spots grammar, and generates comprehension questions

---

## Folder Structure

```
turkish-lessons/
├── README.md               ← this file
├── CLAUDE.md               ← teacher persona (read by Claude automatically)
├── progress/
│   └── learner.md          ← YOUR profile — fill this in first
├── vocab/
│   ├── README.md           ← vocab bank format & SRS scheduling guide
│   └── *.md                ← vocabulary files by topic (auto-populated)
├── curriculum/
│   ├── index.md            ← full CEFR curriculum map (A1–C1)
│   └── {A1,A2,B1,B2,C1}/  ← lesson files
├── scans/
│   ├── README.md           ← OCR workflow guide
│   └── *.txt               ← drop scanned text here
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

Lesson files live in `curriculum/{level}/`. Each lesson should follow the structure in `.claude/commands/lesson.md`. See `curriculum/index.md` for the full topic list and prerequisites.

PRs welcome.
