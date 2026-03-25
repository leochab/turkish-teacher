Sync vocabulary from the local vocab bank to Anki via AnkiConnect.

Deck or filter (optional): $ARGUMENTS

## Prerequisites

This skill requires:
1. **Anki desktop** running on your machine
2. **AnkiConnect plugin** installed in Anki (Tools → Add-ons → Get Add-ons → code `2055492159`)
3. AnkiConnect listening on `http://localhost:8765` (default)

## Instructions

### Step 0 — Verify Connection

Before doing anything else, call a lightweight AnkiConnect method (e.g. `deckNames` or equivalent) to confirm Anki is running and reachable.

- If the call **succeeds**: proceed to Step 1.
- If the call **fails**: stop immediately and tell the learner: "Anki doesn't appear to be running. Open Anki desktop and try again." Do not read vocab files or write a session log.

### Step 1 — Read Vocab Files

Read all files in `vocab/`. Skip `README.md`. For each word entry (identified by a `## [word]` heading), collect:
- Turkish word
- Root
- English translation
- Example sentence (Turkish)
- Example sentence (English)
- Notes

If no word entries exist (only README), report "No vocabulary to sync yet — add words via /lesson or /review first" and stop. Do not write a session log.

### Step 2 — Determine Scope

If `$ARGUMENTS` specifies a topic filter (e.g. "food", "verbs"), only sync words from matching vocab files or whose Notes/Root match the filter.

If no argument, sync **all words** from all vocab files.

### Step 3 — Check Existing Cards

Attempt to query Anki for existing notes by Turkish word (Front field) to avoid duplicates. If the MCP server does not support note querying, skip this step and note in the report that duplicate checking was unavailable — Anki's own duplicate detection will catch any conflicts on import.

### Step 4 — Create Deck if Needed

Ensure a deck named **"Turkish"** exists (or the user-specified deck name). Create it if not present.

### Step 5 — Add Notes

For each new word, create a note using the **"Basic"** note type:

| Anki Field | Value |
|------------|-------|
| Front | Turkish word |
| Back | HTML-formatted content (see below) |

Format the Back field as HTML so it renders correctly on all Anki clients (desktop, AnkiDroid, AnkiMobile):

```html
<b>[English translation]</b>
<br><br>
<i>Example:</i> [Turkish sentence]<br>
[English translation of sentence]
<br><br>
<small>[suffix behavior, exceptions, collocations]</small>
```

If a word fails to create (e.g. note type mismatch, AnkiConnect error), record it and continue — do not abort the entire sync for one failure.

### Step 6 — Report Results

After syncing, report:
- X new cards added to deck "Turkish"
- X already existed (skipped)
- X failed — list each word and the reason

### Step 7 — Session Log

**Automatically write to `progress/learner.md`** (no permission needed):

**Session Log** — append one row:
```
| YYYY-MM-DD | /anki-sync [scope or —] | — | [X new / Y skipped / Z failed] |
```

If 0 words were synced because the vocab bank is empty, write:
```
| YYYY-MM-DD | /anki-sync | — | vocab bank empty, nothing to sync |
```

## Notes

- This is a **one-way sync**: vocab bank → Anki. Do not read or modify SRS data from Anki — the local vocab files remain the source of truth for scheduling. Anki is for mobile review convenience only.
- Do not delete cards from Anki even if a word is removed from the local vocab bank.
- If the learner reviews on AnkiDroid/AnkiMobile, those reviews are tracked in Anki only — they do not update the local `/review` SRS schedule. This is intentional: use `/review` for rigorous scheduled study, Anki for casual mobile exposure.
