# al-Battānī — source edition (work in progress)

This is a source-faithful digital edition of the works of Abū ʿAbd Allāh Muḥammad ibn Jābir al-Battānī (d. 929). It starts with his astronomical handbook *al-Zīj al-Ṣābiʾ* as edited by C. A. Nallino in *Al-Battānī sive Albatenii opus astronomicum* (Milan, 1899–1907; three parts, 1,162 scanned pages).

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
| S02 | Part I: Nallino's Latin translation and notes, printed pp. 1–109 (PDF 90–198) | **v002, partial:** printed pp. 1–30 transcribed (PDF 90–119), with a 31-page reader and a 2-page critical apparatus. 79 pages remain; the next is printed p. 31. Spot-checked independently, see [S02/INDEPENDENT_CHECK.md](S02/INDEPENDENT_CHECK.md) |
| S03–S04 | Part I: Nallino's Latin translation and notes, printed pp. 110–327 | not started |
| S05–S09 | Part II: tables and notes | not started |
| S10–S13 | Part III: Arabic text and tables | not started |
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
- [Reader, 31 pp.](S02/pdf/S02_NALLINO_SOURCE_v002.pdf), printed pp. 1–30
- [Critical apparatus, 2 pp.](S02/pdf/S02_CRITICAL_NOTES_v002.pdf)
- [TeX source](S02/tex/S02_NALLINO_SOURCE_v002.tex) and [line-anchored text](S02/transcription/S02_NALLINO_SOURCE_v002.txt)
- [About this batch](S02/README.md)

Releases are archived on Zenodo under concept DOI [10.5281/zenodo.20539593](https://doi.org/10.5281/zenodo.20539593). The latest version, [10.5281/zenodo.22970148](https://doi.org/10.5281/zenodo.22970148), adds S02 v002 (files 60–63) and keeps S01 v003 (files 50–53, first published in [10.5281/zenodo.22953314](https://doi.org/10.5281/zenodo.22953314)). v002 is in version [10.5281/zenodo.22951891](https://doi.org/10.5281/zenodo.22951891) and in `S01/history/v002/`.

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
