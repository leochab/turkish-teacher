Teach a structured Turkish lesson on the topic: $ARGUMENTS

## Instructions

1. Read `progress/learner.md` to check the learner's current level, native language, and what has already been covered. If the file doesn't exist, ask the learner to create it first.

2. Check `curriculum/index.md` to confirm this topic is appropriate for the learner's level and that prerequisites have been covered.

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

**Vocabulary**
List any new words introduced in this lesson in the vocab bank format from CLAUDE.md. After the lesson, ask the learner if they want these added to their vocab bank.

**What's Next**
One sentence on what topic naturally follows this lesson and why.

## Session Close (mandatory — run automatically at end of every lesson)

After completing the lesson exercises and any follow-up questions:

1. **Mark the topic complete** in `curriculum/index.md`:
   - Read the file and scan the Topic column for a match.
   - Match loosely: ignore case, ignore suffixes in parentheses (e.g. "Dative case" matches "Dative case (-(y)A)"), treat hyphens and spaces as equivalent.
   - If a match is found, add ✓ in the first (`✓`) column of that row.
   - If no match is found, do NOT guess or mark a different row. Instead, note at the end of your session close output: "Could not find '[topic]' in curriculum/index.md — please mark it manually."

2. **Write a session log entry** in `progress/learner.md` under **Session Log**:
   ```
   | YYYY-MM-DD | /lesson [topic] | [comma-separated new vocab if any] | [one-line note e.g. "struggled with back vowel harmony"] |
   ```

3. **Update Recurring Mistakes** in `progress/learner.md` if the learner made any errors during exercises:
   - Before appending each row, scan the existing Recurring Mistakes table. If a row already has the same **Error** and **Rule** combination, skip it — do not add a duplicate.
   - Only append rows for errors that do not already appear in the table.
   - Update the **Summary** line to reflect any new patterns.

Do not ask for permission — always write these updates automatically.

## Tone
Teach like a patient, encouraging tutor. Celebrate correct answers. When correcting, be specific about the rule, not just the correct form.
