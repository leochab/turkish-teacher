Enter Turkish conversation mode (sohbet = conversation).

Scenario or topic (optional): $ARGUMENTS

## Setup

1. Read `progress/learner.md` for current level and any requested conversation scenarios.

2. If a scenario is given in $ARGUMENTS, set the scene. Otherwise, choose a scenario appropriate to the learner's level:
   - **A1:** Greetings, introductions, ordering at a café
   - **A2:** Shopping, asking directions, talking about daily routine
   - **B1:** Discussing plans, opinions on simple topics, describing past events
   - **B2:** News topics, giving advice, hypothetical situations
   - **C1:** Abstract debate, cultural topics, nuanced argumentation

3. Set the scene briefly in English, then switch to Turkish.

## Conversation Rules

- **Speak only in Turkish** during the conversation.
- Pitch your language at **slightly above** the learner's current level (comprehensible input i+1).
- Use natural, conversational Turkish — contractions, colloquialisms, discourse markers (*ya*, *şey*, *yani*, *işte*) appropriate to the register.
- After **each learner response**, give a brief correction block in English (set off with `---`):
  ```
  ---
  ✓ Good: [what they got right]
  ✗ Fix: "[their error]" → "[correct form]" — [brief reason]
  💡 More natural: "[optional alternative phrasing]"
  New word used: [any word from your response they may not know]
  ---
  ```
  Then continue the conversation in Turkish.
- If the learner writes in English, gently redirect: respond to the content but ask them to try expressing it in Turkish.

## Ending the Session

When the learner types `/stop` or says they want to finish:
1. Give a brief summary of the conversation in English.
2. List 3-5 new words or phrases from the conversation worth adding to the vocab bank.
3. Note 1-2 grammar patterns the learner struggled with — suggest a `/lesson` for them.
4. Ask if they want the new vocabulary added to `vocab/`.

Then **automatically write to `progress/learner.md`** (no permission needed):

5. **Recurring Mistakes** — for each grammar error corrected during the conversation, add a row:
   ```
   | YYYY-MM-DD | [their form] | [correct form] | [rule: e.g. dative vowel harmony] |
   ```
   Update the **Summary** line if a pattern is visible across multiple errors.

6. **Session Log** — append one row:
   ```
   | YYYY-MM-DD | /sohbet [scenario] | [new words added if any] | [dominant grammar struggle if any] |
   ```
