Run the onboarding flow to set up the learner profile.

## When to invoke
- Automatically when `progress/learner.md` is unfilled (placeholder text detected).
- Manually to review or update any profile field.

## Instructions

1. Read `progress/learner.md`. If any field still contains placeholder text
   (`[your name]`, `[your native language]`, etc.), run the full Q&A below.
   Otherwise: announce "Profile already set up", show a summary of current
   values, and offer to update any specific field.

2. Ask each question one at a time, waiting for each answer:
   - "What's your name or nickname?"
   - "What's your native language?"
   - "Any other languages you speak? (or skip)"
   - "How would you rate your current Turkish level? (Complete beginner / A1 / A2 / B1 / B2 / C1)"
   - "How long have you been studying Turkish?"
   - "Why are you learning Turkish?"
   - "What's your target level, and do you have a timeline?"
   - "What matters most to you — speaking, reading, writing, or a mix?"
   - "How long do you want sessions to be? (e.g. 20–30 min)"
   - "Do you prefer grammar rules explained explicitly, or would you rather learn through examples first?"

3. Write answers into `progress/learner.md`, replacing the placeholder fields.
   Do not ask for permission.

4. Run `bash scripts/bootstrap.sh` to ensure all other data files exist.

5. Confirm: "Profile saved. Let's begin."
   Then continue with the normal session-start flow (due words, streak, next action).
