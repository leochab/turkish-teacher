Teach a structured Turkish lesson on the topic: $ARGUMENTS

## Instructions

1. Read `progress/learner.md` to check the learner's current level, native language, and what has already been covered. If the file doesn't exist, ask the learner to create it first.

2. Run `python3 scripts/analyze_mistakes.py --top 3` and note the output (if any). Keep this in mind — you will use it in the Exercises section below.

3. Check `curriculum/index.md` to confirm this topic is appropriate for the learner's level and that prerequisites have been covered.

4. Structure the lesson as follows:

### Lesson Structure

**Introduction (1-2 sentences)**
State what the learner will be able to do by the end of this lesson. Connect it to what they already know.

**The Rule**
Explain the grammar rule or vocabulary theme clearly and concisely. For grammar:
- Show the suffix/pattern in its general form first
- Show the vowel harmony variants
- Show any consonant mutation rules that apply
- Always give the suffix ordering context (where does it sit in the chain?)

**Examples — Simple to Complex**
Give 5 examples, progressing from simple to complex:
- Start with a root word + the target suffix alone
- Add one more suffix in example 3
- Use a full sentence in examples 4-5
- Gloss every suffix in every example: *ev-ler-den* = house-PL-ABL = "from the houses"

**Common Mistakes**
List 2-3 errors learners typically make with this topic and why they're wrong.

**Exercises**
Give 5 practice exercises appropriate to the learner's level:
- Mix production (translate to Turkish) and comprehension (parse/translate from Turkish)
- Include at least one exercise targeting vowel harmony choices
- Give answers at the end under a "---" separator so the learner can self-check

**Weak-Spot Mini-Drill** *(conditional — include only if applicable)*
After the main exercises, check the `analyze_mistakes.py` output from step 2. Add the bonus section below **only if** a recorded weak spot names the same suffix or case being taught in this lesson — exact match, not category match (e.g., "vowel harmony in dative suffix" overlaps a dative-case lesson; it does NOT overlap a lesson on verb tenses or personal pronouns). When in doubt, omit the drill.

> **Bonus: Targeting your weak spot — [rule name]**
> Here are 3 extra sentences focusing on [specific pattern]. Practice these if you want extra reinforcement.

**Vocabulary**
List any new words introduced in this lesson. After the lesson, ask the learner if they want these added to their vocab bank. If yes, add them to `vocab/vocab.json` following the format in `vocab/README.md`.

**What's Next**
One sentence on what topic naturally follows this lesson and why.

## Session Close (mandatory — run automatically at end of every lesson)

After completing the lesson exercises and any follow-up questions:

1. **Mark the topic complete** using `curriculum_query.py`:
   - Identify the topic's level and number from `curriculum/index.json`.
   - Run:
     ```
     python3 scripts/curriculum_query.py --mark [LEVEL] [NUMBER]
     ```
     Example: `python3 scripts/curriculum_query.py --mark A1 9`
   - If the topic cannot be matched to a number, note: "Could not find '[topic]' in curriculum/index.json — please mark it manually with `--mark [LEVEL] [NUMBER]`."

2. **Check for level-up** immediately after marking complete:
   - Run:
     ```
     python3 -c "
     import sys; sys.path.insert(0, 'scripts')
     from curriculum_query import count_complete, all_complete
     done, total = count_complete('[LEVEL]')
     print(f'{done}/{total}')
     print('all' if all_complete('[LEVEL]') else 'not_all')
     "
     ```
   - If **all topics in the level are now complete**, announce the milestone prominently:
     ```
     🎉 Level complete! You've finished [Level] — [Level "Can do" summary from curriculum/index.md].
     You're now ready for [Next Level]. Next up: [first topic of next level].
     ```
   - Then update the **Current CEFR level** field in `progress/learner.md` to the next level.
   - If not all topics are checked, show quiet progress: "([N]/[Total] topics complete in [Level])"

3. **Write a session log entry** — run:
   ```
   python3 scripts/session_log_append.py \
     --command "/lesson [topic]" \
     --vocab "[comma-separated new vocab, or omit for —]" \
     --notes "[one-line note e.g. struggled with back vowel harmony]"
   ```
   Show the script output to confirm.

4. **Update Recurring Mistakes** — if the learner made any errors during exercises, follow `.claude/commands/_recurring-mistakes.md`.

## Tone
Teach like a patient, encouraging tutor. Celebrate correct answers. When correcting, be specific about the rule, not just the correct form.
