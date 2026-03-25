# Vocabulary Bank

This folder stores vocabulary organized by topic. Each file covers one semantic domain.

## File Naming

`[topic].md` — e.g., `food.md`, `body.md`, `verbs-motion.md`, `adjectives-common.md`

## Entry Format

Each word entry follows this structure:

```markdown
## [turkish word]
- **Root:** [root form, e.g. git- for gitmek]
- **Part of speech:** [noun / verb / adjective / adverb / postposition]
- **English:** [primary translation]
- **Example:** [full sentence in Turkish] — [English translation]
- **Notes:** [suffix behavior, vowel harmony exception, common collocations, register]
- **Added:** [YYYY-MM-DD]
- **Next review:** [YYYY-MM-DD]
- **Interval:** [days, default 1]
- **Ease:** [1–5, default 3]
```

## Ease Score Guide

| Score | Meaning |
|-------|---------|
| 5 | Mastered — long intervals |
| 4 | Known well |
| 3 | Default / neutral |
| 2 | Shaky — review frequently |
| 1 | Difficult — review tomorrow |

## Review Scheduling

The `/review` command is the **canonical source** for the scheduling algorithm (see `.claude/commands/review.md`). Do not duplicate the formula here.

New words start at: **Next review = tomorrow, Ease = 3, Interval = 1 day.**

> The `Interval` field must be updated alongside `Next review` after every review session.
