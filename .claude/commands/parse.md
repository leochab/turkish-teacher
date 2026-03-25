Perform a full morphological breakdown of the following Turkish word or sentence: $ARGUMENTS

## Instructions

For **each word** in the input:

1. **Identify the root** — the base form found in a dictionary. Note if it's a verb root, noun root, adjective, etc.

2. **List every suffix** in order, for each suffix provide:
   - The suffix in its abstract form (e.g., `-lAr` for plural, using capital letters for harmony slots)
   - The actual realized form in this word (e.g., `-ler`)
   - The grammatical function (e.g., plural, 2nd person plural possessive, ablative case)
   - The vowel harmony rule that determined this vowel choice
   - Any consonant mutation that occurred (softening, buffer insertion)

3. **Show the parse chain** in this format:
   ```
   evlerinizden
   ev + ler + iniz + den
   house + PL + 2PL.POSS + ABL
   "from your houses"
   ```

4. **Explain the meaning** of the whole word/sentence in natural English.

5. **Flag anything unusual** — exceptions to vowel harmony, irregular roots, loanwords, fossilized forms.

For **sentences**, also:
- Label the sentence structure (SOV, topicalized, etc.)
- Identify the tense, aspect, mood of the main verb
- Note any postpositions and what case they govern
- Flag any participle or nominalization constructions

## Output Format

Use a clean, readable format. For complex words, use a table:

| Segment | Morpheme | Function | Harmony note |
|---------|----------|----------|-------------|
| ev | ev (house) | Noun root | — |
| ler | -lAr | Plural | Front stem → -ler |
| iniz | -(n)Iz | 2PL possessive | Front → -iniz |
| den | -DAn | Ablative | Front → -den |

**Full gloss:** ev-ler-iniz-den = house-PL-2PL.POSS-ABL = "from your houses"

## Vocab Bank Offer

After completing the breakdown, check `progress/learner.md` for the learner's current level. Then:

- For any word the learner is unlikely to know at their level, offer to add it to the vocab bank in the format defined in CLAUDE.md.
- Ask once: "Want me to add [word(s)] to your vocab bank?" — do not ask per-word.
- If yes, append to the appropriate `vocab/*.md` file (create the file if no suitable one exists).

Do not write a session log entry. `/parse` is a lookup tool, often called mid-lesson or mid-conversation — logging every invocation would flood the session history.

## Tone
Be precise and educational. This is a learning tool — explain every choice, don't just label it.
