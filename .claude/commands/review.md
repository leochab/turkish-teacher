Run a spaced repetition vocabulary review session.

## Instructions

1. Read `vocab/vocab.json` and collect every entry where **next_review** is today or earlier.

2. If no words are due, report this and show the next upcoming review dates. Offer to do an early review anyway.

3. For each due word, create a **drill card**:
   - Show the Turkish word (with any relevant suffixes if the learner is at B1+)
   - Wait for the learner's answer
   - Accept: translation, example sentence, or morpheme breakdown (any demonstrates recall)
   - Give feedback: correct / close / incorrect, with the full answer and example sentence

4. After **each card** is answered, prompt the learner to rate their recall — but pre-select the most likely rating based on observable signals in their response:

   **Pre-selection rules:**
   | Signal | Pre-select |
   |--------|-----------|
   | Correct, short direct answer | **Easy** |
   | Correct, longer answer that shows working or reasoning | **Good** |
   | Incorrect or blank | **Again** |

   Hard is never pre-selected — the learner can choose it manually to override Good or Easy.

   **Prompt format** (bold = pre-selected):
   ```
   ✓ Correct — [answer]

   Again · Hard · Good · **Easy**   ← confirm or override
   ```
   or for incorrect:
   ```
   ✗ [correct answer] — [brief explanation]

   **Again** · Hard · Good · Easy   ← confirm or override
   ```
   The learner confirms by pressing Enter or typing `y`, or overrides by typing the rating name.

   Once the learner confirms or overrides the rating, run immediately (do not batch):
   ```
   python3 scripts/srs_update.py [word] [rating]
   ```
   Show the script output to the learner (e.g. "kitap: next review in 5 days").

6. End with a **session summary**:
   - X words reviewed
   - X correct / X incorrect
   - Hardest words (show them again at end)
   - Next review session date (when the next batch comes due)

7. After the session summary, **automatically write to `progress/learner.md`** (no permission needed):

   **Session Log** — append one row:
   ```
   | YYYY-MM-DD | /review | — | [X/Y correct; list any words missed 2+ times] |
   ```

   **Recurring Mistakes** — if any word was missed, follow `.claude/commands/_recurring-mistakes.md`.

## Tone
Keep it brisk and encouraging. Celebrate streaks ("5 in a row!"). Don't dwell on wrong answers — correct, explain once, move on.
