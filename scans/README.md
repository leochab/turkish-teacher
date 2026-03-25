# Scans

Drop OCR text files here for processing with `/scan`.

## Workflow

1. Use your OCR app (e.g. Handy) to extract text from Turkish sources:
   - Books, textbooks, newspapers
   - Restaurant menus
   - Street signs, product labels
   - Subtitles or on-screen text

2. Save the extracted text as a `.txt` file in this folder.
   Suggested naming: `YYYY-MM-DD-[source].txt` (e.g. `2026-03-25-menu-istanbul.txt`)

3. Run `/scan` — it will automatically pick up the most recent file, or you can specify a filename: `/scan scans/2026-03-25-menu-istanbul.txt`

## What `/scan` Produces

- Cleaned/corrected text (OCR artifacts fixed)
- Full English translation
- Vocabulary extraction with difficulty ratings
- Grammar spotlight on 2-3 interesting constructions
- Vocab bank entries ready to save
- Comprehension questions

## Tips

- Turkish OCR commonly misreads: ş→s, ğ→g, ı→i, ö→o, ü→u. Don't worry — `/scan` corrects these.
- Longer texts are fine. `/scan` will prioritize the most pedagogically useful material.
- Keep scanned files in this folder as a record of your real-world Turkish encounters.
