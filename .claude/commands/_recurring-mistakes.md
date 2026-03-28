# Recurring Mistakes — Shared Logic

When updating the **Recurring Mistakes** table in `progress/learner.md` after a session:

1. For each error made, scan the existing table for a row where both the **Error** column and the **Rule** column match what you are about to append. If a matching row exists, skip it — do not add a duplicate.
2. If no matching row exists, append:
   ```
   | YYYY-MM-DD | [their form] | [correct form] | [rule violated] |
   ```
   For the rule name: scan the existing Rule column and reuse the closest matching name. Only coin a new name if nothing already in the table fits.
3. After appending any new rows, update the **Summary** line above the table to reflect any emerging pattern (e.g. "consistently confuses back/front vowels in dative suffix").

Do not ask for permission — write these updates automatically.
