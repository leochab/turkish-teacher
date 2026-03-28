Generate a Turkish language quiz for the learner.

Quiz type or topic (optional): $ARGUMENTS

## Instructions

1. Run `python3 scripts/analyze_mistakes.py --top 3` and read the output. Note any weak spots — these drive question weighting in step 4.

2. Read `progress/learner.md` to get:
   - Current CEFR level
   - Recently completed lessons (test recent material)
   - "What I've Covered" section for any manually flagged weak topics

3. Read `vocab/vocab.json` to pull real vocabulary the learner has been studying.

4. Generate a **10-question quiz** with a mix of question types. Choose types appropriate to the learner's level.

   **Weak-spot weighting rule:** If weak spots were recorded, at least 4 of the 10 questions must target those rules. Spread across the top 1–3 weak spots (not all 4 on one rule). If fewer than 4 questions can be meaningfully constructed for the recorded weak rules at the learner's level, fill the remainder with recent lesson material and note why.

   If no mistakes are recorded yet, distribute question types freely.

### Question Types (mix at least 4 types)

**A. Suffix completion**
Fill in the correct suffix (tests vowel harmony and case/tense knowledge):
> *Ev___ gidiyorum.* (I am going to the house.) → Answer: *eve*

**B. Morpheme parse**
Parse a word into its components:
> Parse *okullarda* → Answer: okul+lar+da = school+PL+LOC = "in the schools"

**C. Translation — Turkish to English**
Translate a Turkish sentence to English.

**D. Translation — English to Turkish**
Translate an English sentence to Turkish. For higher levels, specify a particular grammatical structure to use.

**E. Error correction**
Find and fix the mistake in a Turkish sentence. Briefly explain the error.

**F. Vowel harmony choice**
Choose the correct suffix variant:
> *kitap + dan/den* → Answer: *kitaptan* (back vowel stem, consonant softening)

**G. Word order**
Arrange the given words/phrases into a correct Turkish sentence.

**H. Verb conjugation**
Conjugate a given verb in the specified tense and person.

### Format

Number each question clearly. Do NOT show answers inline.

After all 10 questions, add a `---` separator followed by the **Answer Key** with brief explanations for each answer (not just the correct form — explain *why*).

### After Grading

When the learner shares their answers, grade them and:
- Note which question types they struggled with
- Report how they did on weak-spot questions specifically (e.g., "You got 3/4 weak-spot questions right — vowel harmony in dative is improving!")
- Offer a brief targeted drill on any topic where they got 2+ wrong

Then **automatically update session data** (no permission needed):

1. **Recurring Mistakes** — for each question answered incorrectly, follow `.claude/commands/_recurring-mistakes.md`.

2. **Session Log** — run:
   ```
   python3 scripts/session_log_append.py \
     --command "/quiz [topic if given]" \
     --notes "[score X/10; weakest area noted]"
   ```
   Omit `--vocab` (defaults to —). Show the script output to confirm.
