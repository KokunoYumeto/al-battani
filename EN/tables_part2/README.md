# English edition of the tables of Part II of al-Battānī's *Zīj*

C. A. Nallino prints al-Battānī's tables in Part II of *Al-Battānī sive Albatenii opus astronomicum* (Milan, 1907) from the Escorial codex, with the Arabic heads of the codex and his Latin translation of them. Part III prints some of the tables in Arabic as well: the chronological and the geographical tables, the circular diagrams, the star catalogue and the tables of the stars for the year 1211. These are translated from the Arabic in the English *Zīj* ([../](../), with the files in [../tables/](../tables/)). The spurious tables of pp. 297–307 are in English with Nallino's notes on them ([../nallino/](../nallino/)). This folder gives the other tables of Part II, pp. 7–188, with English in place of Nallino's Latin. No English translation of these heads has been published.

Read [tables_en.pdf](tables_en.pdf): a front page and the 116 pages of Part II pp. 7–32, 55–91, 93–143 and 187–188, in Nallino's order, with bookmarks.

## How it is made

- The pages are the readers of [S06](../../S06/), one for each family of tables, which reproduce Nallino's pages from the transcription: the numbers, the Arabic heads, the folio marks of the codex and his page numbers. `build_tables_en.py` takes the TeX of each reader and puts in place of every run of Latin text its English from [heads_en.tsv](heads_en.tsv). Nothing else is changed.
- The build stops if a run with Latin words has no English or a row of `heads_en.tsv` is not used. It compiles each family with XeLaTeX, checks that no character is missing and that every page has its running head, and joins the pages in the order of Nallino's page numbers.
- The terms are those of the English *Zīj* and its [glossary](../glossary.tsv): mean motion and mean course, the anomaly, the northern node, collected and single years, equal hours, the right sphere, the times of the hours, the equation of the days with their nights, the shares of the distances, the farthest, the mean and the nearest distance, the single equation, the first and the second station, appearance and disappearance, the fall, the stay and the clearing.
- Nallino's square brackets, which mark what he supplies, are kept. The transliterated month names stand as printed, with the English of his Latin month in brackets.

## Files

| File | Content |
|---|---|
| `heads_en.tsv` | every run of Latin text of the readers, with its English |
| `build_tables_en.py` | writes `FAMILY_en.tex` from `../../S06/FAMILY/p2_FAMILY.tex`, checks and compiles them and joins `tables_en.pdf` |
| `*_en.tex` | the English TeX of each family and of the front page |
| `tables_en.pdf` | the English tables |

## Credits

- C. A. Nallino: the edition of the tables and the Latin translation of their heads (1907), in the public domain.
- The transcription of the tables: [S06](../../S06/) of this repository.
- The English: AI-translated (Claude), 2026. No person has proofread it. Dedicated to the public domain (CC0 1.0).
