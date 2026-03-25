Run a spaced repetition vocabulary review session.

## Instructions

1. Read all files in `vocab/` and collect every word entry where **Next review** date is today or earlier (compare against today's date).

2. If no words are due, report this and show the next upcoming review dates. Offer to do an early review anyway.

3. For each due word, create a **drill card**:
   - Show the Turkish word (with any relevant suffixes if the learner is at B1+)
   - Wait for the learner's answer
   - Accept: translation, example sentence, or morpheme breakdown (any demonstrates recall)
   - Give feedback: correct / close / incorrect, with the full answer and example sentence

4. After **each card** is reviewed, immediately apply **SM-2-inspired scheduling** and update the vocab file:
   - **Correct with ease (recalled immediately):** Interval = current Interval × 2.5, Ease + 0.1 (max 5)
   - **Correct with effort (took a moment):** Interval = current Interval × 2.0, Ease unchanged
   - **Incorrect:** Interval = 1 day, Ease - 0.2 (min 1)
   - Minimum interval: 1 day. Starting interval for new words: 1 day.
   - Update **Next review**, **Interval**, and **Ease** in the word's `vocab/*.md` entry immediately after scoring — do not batch updates to the end. This ensures progress is saved if the session is interrupted.

6. End with a **session summary**:
   - X words reviewed
   - X correct / X incorrect
   - Hardest words (show them again at end)
   - Next review session date (when the next batch comes due)

## Tone
Keep it brisk and encouraging. Celebrate streaks ("5 in a row!"). Don't dwell on wrong answers — correct, explain once, move on.
