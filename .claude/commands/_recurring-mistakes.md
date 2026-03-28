# Recurring Mistakes — Shared Logic

When recording mistakes after a session, run `mistakes_update.py` for each error (no permission needed):

```bash
python3 scripts/mistakes_update.py \
  --category [morphology|vowel_harmony|case|tense|vocabulary|other] \
  --rule "[rule violated, e.g. vowel harmony in dative suffix]" \
  --error-form "[what the learner wrote]" \
  --correct-form "[correct form]" \
  --context "[the sentence or word where the error occurred]" \
  --command "[current command, e.g. /quiz]"
```

The script deduplicates on `--rule` — if the same rule already exists in `data/mistakes-db.json`, it increments the frequency count and appends the new example rather than creating a duplicate entry.

After running, update the **Summary** line in the `## Recurring Mistakes` section of `progress/learner.md` to reflect any emerging pattern (e.g. "consistently confuses back/front vowels in dative suffix"). The markdown summary is a human-readable overview; the authoritative data lives in `data/mistakes-db.json`.

Do not ask for permission — write these updates automatically.
