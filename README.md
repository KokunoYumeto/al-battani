# al-Battānī — source edition (work in progress)

This is a source-faithful digital edition of the works of Abū ʿAbd Allāh Muḥammad ibn Jābir al-Battānī (d. 929). It starts with the astronomical handbook *al-Zīj al-Ṣābiʾ* as edited by C. A. Nallino in *Al-Battānī sive Albatenii opus astronomicum* (Milan, 1899–1907; three parts, 1,162 scanned pages).

It is an independent working edition. Nallino's edition is in the public domain. The transcriptions, markup and checks here are AI-assisted and still in progress.

## Editions

- An Arabic source edition of al-Battānī's text and tables.
- A historical Latin edition of Nallino's translation and apparatus.
- One separate edition for each target language. There are no bilingual or facing-page readers.
- A restrained critical apparatus and machine-readable ledgers alongside each edition.

## Status

| Session | Scope | Status |
|---|---|---|
| S01 | Nallino, Part I: frontispiece, front matter, preface, bibliography, addenda/corrigenda (PDF 1–89, printed VII–LXXX) | **v003 candidate:** revised transcription with 85 recorded, source-checked decisions (71 text repairs, 14 exact-image substitutions) on 50 pages; 80-page reader and 4-page critical apparatus. Ten hard-to-read spots are kept as exact source images. The independent cold audit has not been done yet |
| S02 | Part I: Nallino's Latin translation and notes, printed pp. 1–109 (PDF 90–198) | **Candidate v009:** printed pp. 1–53 (PDF 90–142) in [S02/candidate_v009_print001-053/](S02/candidate_v009_print001-053/), line-anchored with the printed line numbers and marginal locators, and a 54-page reader. Pp. 41–53 were read line by line against the scan and the corrected readings are integrated. The earlier candidates (v006, pp. 41–43, pp. 44–48), v002 (pp. 1–30, with its 2-page critical apparatus) and the pp. 31–35 extension are kept as records. 56 pages remain; the next is printed p. 54. Checked independently, see [S02/INDEPENDENT_CHECK.md](S02/INDEPENDENT_CHECK.md) |
| S03–S04 | Part I: Nallino's Latin translation and notes, printed pp. 110–327 | not started |
| S05–S09 | Part II: tables and notes | The star table (pp. 144–177), the status tables for 1211 (pp. 178–186) and the geographical tables (pp. 33–54, and the Andalusian table on pp. 219–220) are done with their Part III counterparts (see S13); the rest is not started |
| S10–S12 | Part III: Arabic text | not started |
| S13 | Part III: tables | **Star catalogue complete:** Part III pp. 245–274 and Part II pp. 144–177 in [S13/star_catalogue/](S13/star_catalogue/). Every Part III cell (abjad numerals, with the codex's zero sign set in its own font) is checked against Part II and Nallino's codex notes: 2,604 cells agree, 279 are explained by the notes, 45 differences are ledgered after checking two scan copies, 0 are open. **Status tables for 1211 complete:** Part III pp. 275–279 and Part II pp. 178–186 in [S13/status_1211/](S13/status_1211/): 75 stars, 836 cells agree, 120 explained by Nallino's notes, 7 ledgered, 0 open. **Geographical tables complete:** Part III pp. 234–242 with Part II pp. 33–54 and 219–220 in [S13/geography/](S13/geography/): regions, cities and the Andalusian and Maghribi table, 302 rows; 969 cells agree, 60 explained by Nallino's notes, 153 blank minutes cells where Part II prints 0, 26 ledgered, 0 open. The chronological tables, the two diagrams and Nallino's note on the tables are not started |
| S14 | Commentary on Ptolemy's *Tetrabiblos* (Escorial ár. 969) | not started |
| S15 | The astrological-history work | not started |
| S16 | Integration and cold audit | not started |

**Read S01:**
- [Reader, 80 pp.](S01/pdf/S01_NALLINO_SOURCE_v003.pdf)
- [Critical apparatus, 4 pp.](S01/pdf/S01_CRITICAL_NOTES_v003.pdf)
- [TeX source](S01/tex/S01_NALLINO_SOURCE_v003.tex)
- [What is still open](S01/STATUS.md)
- [What changed from v002](S01/ledgers/v003_changes.tsv)

**Read S02 (partial):**
- [Candidate reader v009, 54 pp.](S02/candidate_v009_print001-053/pdf/S02_NALLINO_SOURCE_v009.pdf), printed pp. 1–53 ([what was checked](S02/candidate_v009_print001-053/INDEPENDENT_CHECK_v009.md))
- Earlier records: [v006 reader](S02/candidate_v006_print001-040/pdf/S02_NALLINO_SOURCE_CANDIDATE_pp001-040.pdf) (pp. 1–40), [checked pp. 41–43](S02/candidate_print041-043/S02_P041_043_CHECK.md), [checked pp. 44–48](S02/candidate_print044-048/S02_P044_048_CHECK.md)
- [v002 reader, 31 pp.](S02/pdf/S02_NALLINO_SOURCE_v002.pdf), printed pp. 1–30
- [Critical apparatus, 2 pp.](S02/pdf/S02_CRITICAL_NOTES_v002.pdf)
- [TeX source](S02/tex/S02_NALLINO_SOURCE_v002.tex) and [line-anchored text](S02/transcription/S02_NALLINO_SOURCE_v002.txt)
- [About this batch](S02/README.md)

**Read the star catalogue (S13):**
- [Part III, the Arabic tables, 30 pp.](S13/star_catalogue/p3_star_catalogue.pdf) and [Part II, the Latin tables with Nallino's notes, 34 pp.](S13/star_catalogue/p2_star_catalogue.pdf)
- [Data, checks and conventions](S13/star_catalogue/README.md); [joined dataset](S13/star_catalogue/star_catalogue_joined.tsv); [discrepancy ledger](S13/star_catalogue/discrepancies.tsv)

**Read the status tables for 1211 (S13):**
- [Part III, Arabic, 5 pp.](S13/status_1211/p3_status_1211.pdf) and [Part II, Latin with Nallino's notes, 9 pp.](S13/status_1211/p2_status_1211.pdf)
- [Data, checks and conventions](S13/status_1211/README.md)

**Read the geographical tables (S13):**
- [Part III, Arabic, 9 pp.](S13/geography/p3_geography.pdf) and [Part II, Latin with Nallino's notes, 24 pp.](S13/geography/p2_geography.pdf)
- [Data, checks and conventions](S13/geography/README.md); [joined dataset](S13/geography/geography_joined.tsv); [discrepancy ledger](S13/geography/geo_discrepancies.tsv)

Releases are archived on Zenodo under concept DOI [10.5281/zenodo.20539593](https://doi.org/10.5281/zenodo.20539593). The latest version, [10.5281/zenodo.23166966](https://doi.org/10.5281/zenodo.23166966), adds the S13 status tables for 1211 (files 840–843) and the geographical tables (files 850–853), both in both versions. It keeps the S13 star catalogue (files 80–83, first published in [10.5281/zenodo.23157330](https://doi.org/10.5281/zenodo.23157330)), the S02 v009 candidate, printed pp. 1–53 (files 70–73, first published in [10.5281/zenodo.22983296](https://doi.org/10.5281/zenodo.22983296)), S02 v002 (files 60–63, first published in [10.5281/zenodo.22970148](https://doi.org/10.5281/zenodo.22970148)) and S01 v003 (files 50–53, first published in [10.5281/zenodo.22953314](https://doi.org/10.5281/zenodo.22953314)). v002 is in version [10.5281/zenodo.22951891](https://doi.org/10.5281/zenodo.22951891) and in `S01/history/v002/`.

The project rules and the 16 session prompts are in [S01/controls/](S01/controls/). Two things are not in this repository: the intermediate QA proof images and the recovered interrupted-reread evidence (452 files, about 153 MB). They stay in the archived S01 package, which is Zenodo file 53. Likewise, S02's reading renders of the source pages (`qa/source/`, 28 files) are only in the archived S02 package.

## Earlier work (June 2026)

Earlier work was released on Zenodo as [10.5281/zenodo.20539593](https://doi.org/10.5281/zenodo.20539593) under CC0. It includes:
- a 251-page Arabic–English–Chinese text working edition
- a fixed-star catalogue (485 stars)
- a geographical gazetteer (269 places)
- a partial chronology
- the v083 TeX data

Its files are in [prior/zenodo-20584850/](prior/zenodo-20584850/), except the large packages, which stay on Zenodo. They predate the S01–S16 workflow, so they have to be replayed against the scans before reuse.

This repository is the maintained home of the edition from now on.

## Credits

- al-Battānī: author of the Arabic text and tables.
- C. A. Nallino: the edition, the Latin translation and the apparatus (1899–1907).
- The source scan's provider marks are kept out of the text and recorded in the provenance files.
