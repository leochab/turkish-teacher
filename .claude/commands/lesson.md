Teach a structured Turkish lesson on the topic: $ARGUMENTS

## Instructions

1. Read `progress/learner.md` to check the learner's current level, native language, and what has already been covered. If the file doesn't exist, ask the learner to create it first.

2. Run `python3 scripts/analyze_mistakes.py` and note the top 3 weak spots (if any). Keep this output in mind — you will use it in the Exercises section below.

3. Check `curriculum/index.md` to confirm this topic is appropriate for the learner's level and that prerequisites have been covered.

3. Structure the lesson as follows:

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
After the main exercises, check the `analyze_mistakes.py` output from step 2. If any of the top 3 weak spots are **related to this lesson topic** (e.g., the lesson is on dative case and "vowel harmony in dative suffix" is a recorded weak spot), add a clearly labelled bonus section:

> **Bonus: Targeting your weak spot — [rule name]**
> Here are 3 extra sentences focusing on [specific pattern]. Practice these if you want extra reinforcement.

If no weak spots overlap with this topic, omit this section entirely — do not manufacture a drill for unrelated rules.

**Vocabulary**
List any new words introduced in this lesson. After the lesson, ask the learner if they want these added to their vocab bank. If yes, add them to `vocab/vocab.json` following the format in `vocab/README.md`.

**What's Next**
One sentence on what topic naturally follows this lesson and why.

## Session Close (mandatory — run automatically at end of every lesson)

After completing the lesson exercises and any follow-up questions:

1. **Mark the topic complete** in `curriculum/index.md`:
   - Read the file and scan the Topic column for a match.
   - Match loosely: ignore case, ignore suffixes in parentheses (e.g. "Dative case" matches "Dative case (-(y)A)"), treat hyphens and spaces as equivalent.
   - If a match is found, add ✓ in the first (`✓`) column of that row.
   - If no match is found, do NOT guess or mark a different row. Instead, note at the end of your session close output: "Could not find '[topic]' in curriculum/index.md — please mark it manually."

2. **Check for level-up** immediately after marking the ✓:
   - Count the total topics and the ✓-marked topics in the current level's section (A1 has 12, A2 has 12, B1 has 10, B2 has 8, C1 has 5).
   - If **all topics in the level are now checked**, announce the milestone prominently:
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
