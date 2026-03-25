Generate a Turkish language quiz for the learner.

Quiz type or topic (optional): $ARGUMENTS

## Instructions

1. Read `progress/learner.md` to get:
   - Current CEFR level
   - Weak spots (prioritize these)
   - Recently completed lessons (test recent material)

2. Read `vocab/` files to pull real vocabulary the learner has been studying.

3. Generate a **10-question quiz** with a mix of question types. Choose types appropriate to the learner's level:

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
- Offer a brief targeted drill on any topic where they got 2+ wrong

Then **automatically write to `progress/learner.md`** (no permission needed):

1. **Recurring Mistakes table** — for each question answered incorrectly:
   - Scan the existing table for a row with the same **Error** and **Rule**. If found, skip — do not append a duplicate.
   - If not found, append:
     ```
     | YYYY-MM-DD | [their answer] | [correct form] | [rule violated] |
     ```
   Update the **Summary** line if a new pattern is emerging (e.g. "confuses back/front vowels in dative").

2. **Session Log** — append one row:
   ```
   | YYYY-MM-DD | /quiz [topic if given] | — | [score X/10, weakest area noted] |
   ```
