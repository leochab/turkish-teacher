# Vocabulary Bank

All vocabulary is stored in `vocab/vocab.json` as a single JSON object keyed by Turkish word.

## Entry Format

```json
{
  "kitap": {
    "root": "kitap",
    "pos": "noun",
    "topic": "objects",
    "english": "book",
    "example_tr": "Kitabı aldım.",
    "example_en": "I took the book.",
    "notes": "Final p softens to b before vowel suffixes: kitap → kitabı",
    "added": "YYYY-MM-DD",
    "next_review": "YYYY-MM-DD",
    "interval": 1,
    "ease": 3.0
  }
}
```

## Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `root` | string | Base dictionary form |
| `pos` | string | Part of speech: noun / verb / adjective / adverb / postposition |
| `topic` | string | Semantic grouping (e.g. objects, verbs, food, travel) |
| `english` | string | Primary translation |
| `example_tr` | string | Example sentence in Turkish |
| `example_en` | string | English translation of the example |
| `notes` | string | Suffix behavior, harmony exceptions, collocations, register |
| `added` | date | YYYY-MM-DD |
| `next_review` | date | YYYY-MM-DD — updated by `/review` after each card |
| `interval` | number | Days until next review — updated by `/review` |
| `ease` | number | 1.0–5.0, default 3.0 — updated by `/review` |

## SRS Starting Values

New words: `next_review` = tomorrow, `interval` = 1, `ease` = 3.0.

The `/review` command is the canonical source for the scheduling algorithm. See `.claude/commands/review.md`.
