# English translation of al-Battānī's commentary on Ptolemy's *Tetrabiblos*

Al-Battānī's *Sharḥ Kitāb al-Arbaʿ maqālāt fī aḥkām ʿilm al-nujūm*, the earliest commentary on the *Tetrabiblos* that survives, translated into English from the Arabic of the Escorial manuscript (árabe 969, ff. 20r–80v) as Nadine Löhr transcribed it in *Ptolemaeus Arabus et Latinus* (Bavarian Academy of Sciences and Humanities, 2021, CC BY 4.0) and [S14](../../S14/commentarius/) edits it. No English translation of the commentary had been published; PAL records a partial Italian one of the part on Book III (F. Martorello, 2022).

**Done:** the whole commentary: the title page, chapters 1–40 and the colophon (ff. 20r–79v), all 2,465 lines of the manuscript, and the two tables of ff. 80r–80v, with a glossary of the technical terms. Read [commentary_en.pdf](commentary_en.pdf).

## How it is made

- Every line of the manuscript is translated, in the order of the text. Each block of the English names the first and the last line it translates; `build_commentary.py` checks that every line belongs to a block, and writes the TeX and `alignment.tsv`.
- The commentary follows the *Tetrabiblos* chapter by chapter, restating Ptolemy's doctrine and adding al-Battānī's explanations, lists, examples and procedures. F. E. Robbins's translation (Loeb, 1940; public domain) is the check on the meaning of the doctrine; its wording is not followed. The notes give the chapter of the *Tetrabiblos* in Robbins's numbering.
- The terms follow the English translation of the *Zīj* in [../](../) where the two works share them (for example «the wandering stars», «the configurations», «the cardine of the earth»).
- Editorial signs of the transcription: words supplied by the editor stand in ⟨ ⟩; words the editor marks as additions of the copyist, such as invocations, in ⟦ ⟧; words struck out by the copyist are left out; a doubtful reading is marked (?). Words added for the sense stand in square brackets. Where the English reads a word otherwise than the transcription, the note says so.
- The two tables of ff. 80r–80v are set from S14's cells, with their headings and the names of the signs and planets in English from `tables.tsv`; their numbers are given in figures, read with the Maghribi values of the abjad letters. `build_commentary.py` compares every number of the table of f. 80r with the computation from the year of the revolution of the *Zīj* (365 days 5 hours 46 minutes 24 seconds), and every name in the table of f. 80v with Ptolemy's triangles and terms; the differences are marked † and listed under the tables.

## Files

| File | Content |
|---|---|
| `text/K##.txt` | one file per chapter (K00 is the title page and the invocation): each block of English with the lines it translates, and its notes; the format is described at the head of `build_commentary.py` |
| `tables.tsv` | the English of the headings of the two tables and of the names of the signs and planets in them |
| `glossary.tsv` | the technical terms: the English of this translation, the Arabic and its transliteration, F. E. Robbins's English for Ptolemy's term (with the Greek where Robbins gives it), and what the term means; printed at the end of the PDF |
| `build_commentary.py`, `make_pdf.py` | check the coverage of the manuscript lines and build the PDF deterministically |
| `alignment.tsv` | every block of the English with its lines and folios |
| `checkpoint.json` | the chapters done and a checksum over the chapter files |

## Credits

- al-Battānī: the commentary.
- Nadine Löhr, *Ptolemaeus Arabus et Latinus. Texts*: the transcription of the Escorial manuscript (CC BY 4.0).
- The translation: AI-integrated work (Claude), 2026. No person has proofread it. Dedicated to the public domain (CC0 1.0).
