Show the learner what they can do and where to start.

## Instructions

1. Read `progress/learner.md`. If the file is unfilled (fields still contain placeholder text like `[your name]`),
   do not render help — instead say: "Let's set up your profile first before we look at commands.
   I'll ask you a few quick questions." Then run the onboarding flow from CLAUDE.md.

2. From `learner.md`, get:
   - The learner's name (use it in the greeting)
   - Current CEFR level

3. Use `curriculum_query.py` to determine the suggested next step:
   - Run `python3 scripts/curriculum_query.py --check [LEVEL]` where LEVEL is the learner's current CEFR level.
   - The first topic shown without ✓ is the next lesson to suggest.
   - If all topics at the current level are complete (`python3 -c "import sys; sys.path.insert(0,'scripts'); from curriculum_query import all_complete; print(all_complete('[LEVEL]'))"` returns `True`), show:
     "You've finished all [Level] topics! You're ready for [Next Level].
     Next up: `/lesson [first topic of next level]`"
   - If the learner is at C1 and all C1 topics are done, show:
     "You've completed the full curriculum! Focus on `/sohbet` for fluency
     or `/quiz` on any topic to keep sharp."
   - If no topics are complete yet, suggest: `/lesson the Turkish alphabet`

4. Run `python3 scripts/session_start.py` and read its full output: vocab due count, streak, suggested next action, and top weak spots (if any recorded).
   Use the vocab due count to determine whether to recommend `/review` first.
   Include the weak spots in the help screen if any are shown.

5. Run `python3 -c "import sys; sys.path.insert(0,'scripts'); from curriculum_query import count_complete; done,total=count_complete('[LEVEL]'); print(f'{done}/{total}')"` to get the "X of Y topics complete in [Level]" count.

6. Output the help screen using the template below.

---

### Template

Hi [name]! Here's what you can do:

**Available commands**

| Command | What it does | Example |
|---------|-------------|---------|
| `/lesson [topic]` | Structured lesson with examples, exercises, and answers | `/lesson vowel harmony` |
| `/parse [word or sentence]` | Full morpheme-by-morpheme breakdown with glosses | `/parse gidiyorum` |
| `/quiz` | 10-question quiz tailored to your level and weak spots | `/quiz` or `/quiz verb tenses` |
| `/review` | Spaced repetition flashcard session for due vocabulary | `/review` |
| `/sohbet` | Turkish-only conversation mode — Claude corrects inline | `/sohbet` |
| `/setup` | Run (or re-run) the onboarding flow to set or update your learner profile | `/setup` |
| `/help` | Show this screen | `/help` |

---

**Where to start**

Level: [CEFR level] — [X of Y topics complete in this level]

[If vocab is due per session_start.py output]:
You have [N] word(s) due for review — run `/review` to clear them first, then continue with a lesson.

[If no vocab is due]:
No vocab due today.

[If weak spots shown in session_start.py output]:
Top weak spots:
[paste the ranked list from session_start.py here]

Next lesson: **[next unchecked topic]** — `/lesson [topic name]`

---

**Tips**

- `/lesson` topics follow the curriculum order — you can name them freely and Claude will match them.
- `/parse` works on any Turkish word or sentence, including things you find outside lessons.
- `/quiz` without arguments picks topics automatically; add a topic name to focus on a specific area.
- `/sohbet` switches to Turkish-only mode — type `dur` to exit.

---

## Session Close

N/A — `/help` is informational only. Do not write a session log entry.
