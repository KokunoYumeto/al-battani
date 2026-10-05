# S13 — The geographical tables, in both of Nallino's versions

al-Battānī gives the longitude and latitude, in degrees and minutes, of the regions (the heading speaks of 94) and of the cities, after the *Book of the Figure of the Earth* (*kitāb ṣūrat al-arḍ*). Nallino numbers the rows 1–273; his table of cities begins with no. 94. A later table of 29 Andalusian and Maghribi cities follows in the codex.

| Witness | Pages | What it is |
|---|---|---|
| **Part III** (Arabic) | printed pp. 234–242 (master PDF 918–910) | The tables of the codex (Escorial, ár. 908, fol. 172,v.–176,r.), with the numbers in Maghribi abjad and the codex's zero sign. The 94 regions (*jadwal awsāṭ al-buldān*), the cities (*min asmāʾ al-buldān*), and on fol. 176,r. the table *aṭwāl madāʾin wa-maʿāqil maʿrūfa mumtaḥana wa-ʿurūḍuhā bi-l-Andalus wa-l-Maghrib*. |
| **Part II** (Latin) | printed pp. 33–54 (master PDF 482–503) | Nallino's *Tabula mediorum punctorum regionum* (nos. 1–93) and *Tabula latitudinum et longitudinum urbium* (nos. 94–273): Western numerals, transliterated names, and notes with identifications, Ptolemy's and al-Khuwārizmī's values, and the codex readings. |
| **Part II** (Latin) | printed pp. 219–220 (master PDF 668–669) | The Andalusian and Maghribi table, given in Nallino's apparatus as a table with a notes column. Its rows are unnumbered there and keyed here A01–A17 (first series) and B01–B12 (second series). |

Both are transcribed from the scan as printed. Neither is corrected from the other.

## Read

- [Part III edition, 9 pp.](p3_geography.pdf): the Arabic tables, right to left, one page per printed page, with the two panels of each page as printed and Nallino's footnotes.
- [Part II edition, 24 pp.](p2_geography.pdf): the Latin tables with Nallino's notes, and the Andalusian table with its notes column.

## Data

| File | Content |
|---|---|
| `geo_p3.tsv` | Part III rows: page, row, kind (title, folio line, column head, row), section (REG, CIT, AND), key of the Part II row, the Arabic name, longitude and latitude cells as printed, and reading notes (`doubt`). |
| `geo_p3_footnotes.tsv`, `geo_p3_pages.tsv` | Nallino's footnotes to Part III; folio lines and signatures. |
| `geo_p2.tsv` | Part II rows: page, column (L, R; T for the table with a notes column), number or key, name, values as printed (italics as `*…*`). |
| `geo_p2_notes.tsv` | Nallino's notes, with the codex readings he reports in a structured column (e.g. `lon_d=106`); the notes column of pp. 219–220; the paragraphs between table and footnotes (key `¶1`); his footnotes (key `*`). |
| `geo_p2_pages.tsv` | Running heads, titles and signatures of the Part II pages. |
| `geo_discrepancies.tsv` | Differences between the witnesses that Nallino's notes do not explain, each checked in two scan copies, and two notes on Nallino's own text. |
| `geography_joined.tsv` / `.json` | One row per Part III row: raw cells, decoded values, Part II values, codex readings, Part II name and notes column, status per field. |

## How the two versions were checked

Every Part III cell was read at 500–3600 dpi and decoded from the abjad, then compared with Part II and with the codex readings in Nallino's notes:

| Result | Cells |
|---|---|
| Agrees with Part II | 969 |
| Differs, and Nallino's note gives exactly this codex reading | 60 |
| Blank minutes cell where Part II prints 0 | 153 |
| Differs with no matching note (ledgered) | 26 |
| Open | 0 |

Each unexplained difference was read again in a second copy of the print (Internet Archive). Every structured note value must also equal the Part III reading. `python check_geo.py` repeats the check. The check also finds differences that a first reading passes over: the longitude of Ṭūs (p. 241, صب = 62 against Part II's 92) was found this way and then confirmed in both copies.

On pp. 219–220 Part II's values are the codex values themselves (suspect ones in italics, emendations in the notes column), so the Part III cells must agree with them one by one.

## Conventions

As in the star catalogue (see `../star_catalogue/README.md`). In addition:
- **Two panels per page.** Part III prints each page as a right and a left panel; the right panel is read first. A second table on the same page has row ids with the prefix 2 (p. 241). Where the two panels' column heads differ in print, each panel has its own head (`H01R`, `H01L`).
- **Blank minutes.** A minutes cell left blank in Part III where Part II prints 0 is counted separately, not as agreement.
- **Dotless heads take the code point of their reading:** ٯ (U+066F) read ق; ڡ (U+06A1) read ف; ڧ (U+06A7, a head with one dot read as qāf, as in Nallino's note 270: «in scriptura maghrebina ڧ = ق»). A dotless tooth is ى (U+0649); a dotless final bowl is ٮ (U+066E).
- **An extra printed letter** is kept: the latitude of Aṣīlā’ is printed ه له, with U+200C keeping the print's non-joining; it is ledgered.
- **Ottoman letters** in Nallino's notes are kept apart: ڭ (U+06AD, kāf with three dots) and گ (U+06AF).

## Not done yet

- Part II pp. 214–218 (master PDF 663–667): Nallino's index of the places by region and his comparison with the Castilian version and the Escorial codex.
- An independent second reading of the Arabic names and their harakat.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the edition of the codex (Part III), the Latin version and the notes (Part II), Milan 1899–1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
