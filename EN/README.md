# al-Battānī, *al-Zīj al-Ṣābiʾ* — an English translation (in progress)

An English translation of the canons of al-Battānī's *Zīj*: the list of the 57 chapters and the chapters themselves, translated from the Arabic text as Nallino printed it in Part III of his edition (Rome, 1899), which this repository transcribes line by line in [S10](../S10/textus/), [S11](../S11/textus/) and [S12](../S12/textus/). No complete translation of the *Zīj* into a modern language exists; Nallino's Latin translation (Part I, Milan, 1903) is the only complete one.

## What the translation aims at

The English should say everything the Arabic says, in the order in which al-Battānī says it. It should also read as plain modern English. Concretely:

- **Every sentence is translated.** Nothing is summarised or left out, and no explanation is worked into the text. Every number, example and step of a procedure stands as al-Battānī gives it. Each paragraph of the English carries the anchors of the Arabic lines it translates. A script checks that every line of the Arabic text is covered once.
- **Modern English, not the English of older translations.** Short sentences where the Arabic chains clauses with *wa-* and *fa-*. No archaisms, and no calques of Latin syntax. Mathematical statements are put the way a reader of today expects them, without changing what they say: «multiply it by itself» stays a multiplication, a sine stays «the half of the chord of twice the arc» where al-Battānī defines it so, and is called the sine once he has defined it.
- **Exact technical terms, used consistently.** One English term for each Arabic term, recorded in [glossary.tsv](glossary.tsv) with Nallino's Latin equivalent. Where an English term is not self-explanatory, the glossary says what it means. The standard modern name is used where it means exactly the same thing: «the ecliptic» for *falak al-burūj*, «the equator» for *falak muʿaddil al-nahār*. A literal rendering is used where al-Battānī's notion differs from the modern one: «the horizontal shadow» and «the vertical shadow» for *al-ẓill al-mabsūṭ* and *al-ẓill al-qāʾim*, not cotangent and tangent.
- **Numbers in numerals.** Al-Battānī writes most numbers in words. The translation gives them in figures with their units (23° 35′, 365 days 5 hours), since the value is what matters and figures are easier to check. Sexagesimal fractions keep their places as written (minutes, seconds, thirds).
- **Brackets for additions.** Words that the English needs only to be grammatical are not marked. Words added for the sense stand in square brackets, sparingly.
- **Notes, kept apart from the text.** Quotations from the Qurʾān are identified in notes. A note also records where Nallino corrects the Arabic and the translation follows him, where the translation corrects a misprint that his corrigenda do not list, and where it reads the Arabic differently from Nallino. Corrections that concern only the grammatical form of a word, and do not change the English, are not noted. Pages and lines are cited by Nallino's page numbers and his marginal line numbers, which his corrigenda also use.

## Sources and checks

- **The text translated:** Nallino's Arabic text (Part III), with his apparatus of the readings of the Escorial codex and his list of corrections. Where his corrigenda correct a misprint, the translation follows the correction and says so in a note.
- **Nallino's Latin translation** (Part I, transcribed here in [S02](../S02/), [S03](../S03/versio/) and [S04](../S04/versio/)) is the authoritative check on the meaning, sentence by sentence. Its margins give the pages of the Arabic text, so the two can be aligned chapter by chapter. His footnotes also report the readings of the twelfth-century Latin version of Plato of Tivoli wherever they bear on the text. His commentary (the *Adnotationes*, from Part I p. 151) and his Arabic–Latin glossary (Part II, transcribed in [S09](../S09/glossarium/)) explain the technical terms. Nallino's Latin is a check, not a model. Its phrasing is not carried over, and where the translation departs from his reading, a note gives the reason.
- **The medieval Latin and Castilian versions.** These are Plato of Tivoli's *De motu stellarum*, printed in 1537 and 1645, and the thirteenth-century Castilian *Cánones*. They are consulted through Nallino's notes. No free scan of the printed Latin has been found yet.
- The notes cite the *Almagest* by book and chapter as in Heiberg's edition and Toomer's translation. Nallino cites Halma's edition, whose chapters of Book I are numbered differently.
- [tools/sources.py](tools/sources.py) writes, for any chapter, the Arabic lines and Nallino's Latin of the same chapter in reading order. This is the working view for translating and checking a chapter.

The work runs chapter by chapter. First the Arabic is read with Nallino's apparatus, then translated paragraph by paragraph. Each paragraph is compared with Nallino's Latin. Every number is checked against the Arabic. Then the chapter is reread once as English.

## Status

**Done:** the invocation, the list of the 57 chapters and chapters 1–6 (Part III pp. 1–28). Read [zij_en.pdf](zij_en.pdf). The chapters follow in order; the tables of Part III, whose headings and notes also need translating, come after the canons.

| File | Content |
|---|---|
| `text/C##.txt` | one file per chapter: each block of English with the anchors of the Arabic lines it translates, and its notes; the format is described at the head of `build_en.py` |
| `build_en.py`, `make_pdf.py` | check that every Arabic line of each chapter is translated once, and build the PDF deterministically |
| `alignment.tsv` | every block of the English with its Arabic lines and pages |
| `glossary.tsv` | the technical terms: Arabic, transliteration, English, Nallino's Latin |
| `tools/sources.py` | the Arabic and Nallino's Latin of a chapter side by side |
| `checkpoint.json` | the chapters done and a checksum over the chapter files |

## Credits

- al-Battānī: the text.
- C. A. Nallino: the edition of the Arabic text, the Latin translation and the notes (1899–1907).
- The translation: AI-integrated work (Claude), 2026. No person has proofread it. Dedicated to the public domain (CC0 1.0).
