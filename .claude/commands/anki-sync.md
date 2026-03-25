Sync vocabulary from the local vocab bank to Anki via AnkiConnect.

Deck or filter (optional): $ARGUMENTS

## Prerequisites

This skill requires:
1. **Anki desktop** running on your machine
2. **AnkiConnect plugin** installed in Anki (Tools → Add-ons → Get Add-ons → code `2055492159`)
3. AnkiConnect listening on `http://localhost:8765` (default)

If the connection fails, remind the learner to open Anki first.

## Instructions

### Step 1 — Read Vocab Files

Read all files in `vocab/`. For each word entry, collect:
- Turkish word (the `## [word]` heading)
- Root
- English translation
- Example sentence (Turkish)
- Example sentence (English)
- Notes
- Added date
- Next review date
- Interval
- Ease

### Step 2 — Determine Scope

If `$ARGUMENTS` specifies a deck name or topic filter (e.g. "food", "verbs"), only sync words from matching vocab files or whose Notes/Root match the filter.

If no argument, sync **all words** from all vocab files.

### Step 3 — Check Existing Cards

Before creating cards, check which notes already exist in Anki (by Turkish word as the front field) to avoid duplicates. Only create cards for words not already in Anki.

### Step 4 — Create Deck if Needed

Ensure a deck named **"Turkish"** exists (or the user-specified deck name). Create it if not present.

### Step 5 — Add Notes

For each new word, create a note with the following fields in the **"Basic"** note type (or closest available):

| Anki Field | Source |
|------------|--------|
| Front | Turkish word |
| Back | English translation + example sentence (Turkish) + example sentence (English) + morphological notes |

Format the Back field clearly:

```
[English translation]

Example: [Turkish sentence]
([English translation of sentence])

Notes: [suffix behavior, exceptions, collocations]
```

### Step 6 — Report Results

After syncing, report:
- X new cards added to deck "Turkish"
- X already existed (skipped)
- List any words that failed to sync and why

### Step 7 — Session Log

**Automatically write to `progress/learner.md`** (no permission needed):

**Session Log** — append one row:
```
| YYYY-MM-DD | /anki-sync [scope or —] | — | [X cards added to Anki] |
```

## Notes

- This is a **one-way sync**: vocab bank → Anki. Do not read or modify SRS data from Anki — the local vocab files remain the source of truth for scheduling.
- If the learner wants to review on mobile, they should use AnkiDroid/AnkiMobile which sync with AnkiWeb separately from this tool.
- Do not delete cards from Anki even if a word is removed from the local vocab bank.
