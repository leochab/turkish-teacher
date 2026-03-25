Process the following OCR-scanned Turkish text and turn it into a learning opportunity.

The text to process is either: $ARGUMENTS — or, if no argument is given, read the most recently modified file in the `scans/` folder.

## Instructions

### Step 1 — Clean the Text
OCR output often has errors with Turkish diacritics. Common OCR misreads: **s** for ş, **g** for ğ, **i** for ı, **o** for ö, **u** for ü (diacritics get dropped). Make a best-effort correction of these and other obvious OCR artifacts. Show the corrected text.

### Step 2 — Translate
Provide a natural English translation of the full text.

### Step 3 — Vocabulary Extraction
Identify all words that are likely new or challenging for the learner's current level (read from `progress/learner.md`). For each:
- Give the root form and meaning
- Note what suffixes are attached in context
- Rate rough difficulty (A1 / A2 / B1 / B2 / C1)

Present as a table:
| Word in text | Root | Meaning | Suffixes | Level |
|---|---|---|---|---|

### Step 4 — Grammar Spotlight
Pick 2-3 interesting grammar points visible in the text. For each:
- Quote the relevant phrase
- Parse it (use `/parse` style breakdown)
- Explain the grammar rule
- Connect it to what the learner has already covered (check `progress/learner.md`)

### Step 5 — Vocab Bank Update
Format the new vocabulary words in the vocab bank format defined in CLAUDE.md, ready to be added to the appropriate `vocab/*.md` file. Ask the learner which ones they want to save.

### Step 6 — Comprehension Questions
Generate 3 comprehension questions about the text in Turkish (with English translations). Appropriate to the learner's level.

### Step 7 — Session Log

After completing the scan (and any vocab the learner chose to save), **automatically write to `progress/learner.md`** (no permission needed):

**Session Log** — append one row:
```
| YYYY-MM-DD | /scan [filename or description] | [comma-separated vocab added, or —] | [source type: menu/sign/news/etc.] |
```

## Notes
- If the text appears to be a menu, sign, or label: focus on practical vocabulary and register.
- If it's literary or news text: focus on complex sentence structure and B2+ grammar.
- If it's a conversation: focus on discourse markers, register, and pragmatics.
