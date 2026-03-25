Process a line or short excerpt of Turkish TV dialogue and turn it into a learning opportunity.

The dialogue to process is: $ARGUMENTS

If no argument is given, ask the learner to paste the subtitle or dialogue line they want to work through.

## Instructions

### Step 1 — Display and Normalise

Show the original line as given. If the learner has copied a subtitle with encoding issues or missing diacritics (common when copy-pasting from subtitle files), make a best-effort correction — note any changes made.

If the learner provides show/episode context (e.g. "Aile, S1E3"), note it. If not, leave context blank.

### Step 2 — Translate

Provide:
1. A **literal translation** (word-by-word, preserving Turkish structure)
2. A **natural English translation** (how a native speaker would actually say it)

If the two differ significantly, explain why — this gap often reveals something about Turkish grammar or register.

### Step 3 — Register & Colloquial Analysis

TV dialogue is spoken Turkish — it often differs sharply from textbook Turkish. Flag any of the following if present:

- **Elisions and contractions:** e.g. *ne yapıyorsun* → *napıyosun*, *değil mi* → *dimi*, *bir şey* → *bişey*. Show the "full" written form alongside the spoken shortcut.
- **Colloquial particles:** *ya*, *işte*, *yani*, *şey*, *ha*, *hani*, *tamam mı* — explain the pragmatic function (filler, emphasis, hedging, tag question, etc.)
- **Register:** Is this formal (bey/hanım address, -ir aorist), neutral, informal (sen + casual tense), or slang? Why does the register fit the scene?
- **Non-standard spelling in subtitles:** Some Turkish subtitles preserve pronunciation spelling (e.g. *içinde* → *içinde* vs *içnde*). Note these if present.

### Step 4 — Morphological Breakdown

For every content word (nouns, verbs, adjectives, adverbs) in the line, provide the parse chain:

```
[word]
[root] + [suffix1] + [suffix2] ...
[ROOT-GLOSS] + [SUFFIX1-GLOSS] + [SUFFIX2-GLOSS] ...
"[English meaning]"
```

Use the table format from `/parse` for complex words:

| Segment | Morpheme | Function | Harmony note |
|---------|----------|----------|-------------|

Group by word — don't make the learner hunt for which row belongs to which word.

Focus on: tense/aspect choices (why aorist vs progressive?), dropped pronouns, postpositions, and any suffix chain worth learning.

### Step 5 — Cultural & Scene Notes

If the line contains any of the following, add a short note (1-3 sentences max per item):

- **Idioms or set phrases:** Give the literal meaning, the actual meaning, and whether it's specific to a region, age group, or register.
- **Terms of address:** Turkish TV uses *abi* (older brother, not always literal), *abla*, *hocam*, *canım*, *bey*, *hanım*, etc. as social lubricants — explain the relationship dynamic they signal.
- **Cultural context:** References to concepts a non-Turkish speaker might miss (hospitality norms, family hierarchy, political subtext in period dramas, etc.).
- **Genre register:** Dizi Turkish varies by genre. Crime/thriller: clipped, tense sentences. Family drama: long subordinate clauses, hedged speech. Comedy: wordplay, regional accents. Note the genre signature if visible.

Skip this section entirely if there is nothing culturally notable — do not force it.

### Step 6 — Grammar Spotlight

Pick 1-2 grammar points the learner may not have fully mastered (calibrate to their level in `progress/learner.md`). For each:

- Quote the relevant phrase from the line
- Explain the rule
- Give one additional example not from the dialogue

### Step 7 — Vocab Bank Offer

List any words from the line that are likely new for the learner's level. Format them in the vocab bank format from CLAUDE.md, ready to add to `vocab/`.

Ask once: "Want me to add any of these to your vocab bank?" — do not ask per-word.

If yes, append to the appropriate `vocab/*.md` file. Prefer an existing topic file; create a new one only if no suitable file exists.

### Step 8 — Session Log

After completing the analysis (and saving any vocab the learner chose), **automatically write to `progress/learner.md`** (no permission needed):

**Session Log** — append one row:
```
| YYYY-MM-DD | /dizi [show or first 4 words of line] | [vocab added, or —] | [dominant grammar point noted] |
```

## Tone

Conversational and curious — match the energy of watching TV together. Point out the interesting things, not just the correct things. If a line is funny, say so. If a character's speech reveals something about their personality or social position, mention it.

Don't exhaustively parse every function word. Focus depth on what's new or tricky for this learner's level.
