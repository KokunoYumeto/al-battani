# S02 v009 — independent check (2026-09-26)

ChatGPT's cumulative package `AB01_S02_v009.zip` (sha256 `7a21da0c9e90b0a8…`, 345 files) covers Nallino's Part I, printed pp. 1–53 (master PDF 90–142), in line-anchored form: the printed line numbers and the marginal locators to the Arabic text are recorded for every line. This folder is that package with six corrections applied (below), without `qa/` (17.5 MB of intermediate renders) and without `history/` (copies of v002 and the v006 candidate, which are already in this repository). The package as delivered is archived on Zenodo.

This check was made by Claude against the scan, not by a human proofreader.

## What was checked

- **Manifest.** All 344 listed files verify (sha256). Six page-record and TeX files and two PDFs in this folder now differ from the manifest because of the corrections; `ledgers/independent_check_corrections.tsv` lists them.
- **Builds.** All three documents build here with XeLaTeX ×2: the reader (54 pp.), the checked pp. 41–43 (3 pp.) and pp. 44–53 (10 pp.). There are no errors, missing characters or overfull boxes. The reader TeX also builds on its own from a clean folder.
- **Pp. 1–40.** All 40 page records and the inherited TeX are byte-identical to the v006 candidate in `../candidate_v006_print001-040/`.
- **Pp. 41–48.** Every reading corrected in the earlier checks (`../candidate_print041-043/`, `../candidate_print044-048/`) is in v009. That includes 285, *efficiunt*, *Pachōn*, 365ᵈ, the order signs IV V VI, fol. 164 v., the note-4 formula, al-Battānī, al-Farghānī and 1ᵖ in p. 46 n. 14. A word-by-word comparison of the rendered text found only layout differences. The 13 new margin locators match the positions recorded from the scan.
- **Pp. 49–53** (new). Word-trigram overlap with the scan's OCR layer is 85–90% in both directions. Two parallel checkers read every body line, every note, the line numbers and the locators against the scan at 200 dpi, zooming to 600–1600 dpi on doubtful spots. Each finding below was then confirmed from the scan crops.
  - **P. 49** matches completely.
  - **P. 51:** the damaged first glyph (line 1) is kept as an exact image and nothing is guessed. The printed repetition "in / in" (lines 20–21) is kept.
  - **P. 52 n. 1:** the citation "p. 293-206)" is exactly as printed.

## Corrections applied here

| Printed page, line | v009 | Print |
|---|---|---|
| 50, ll. 19, 30, 34 | versus partem contrariam *successionis* signorum | *successioni* signorum (dative, all three times; the fourth occurrence, l. 24, was already right) |
| 51, l. 27 | Lunae a puncto A Solis *determinantur* (*a*) | *determinatur* |
| 52, l. 21 | lineae AH*.* quam 5ᵖ ¹/₄ | lineae AH*,* quam (a comma, 1200 dpi) |
| 53, l. 9 | Cum autem *semidia-* / trus | *semidiame-* / trus (semidiametrus) |

The corrections are made in the page records (`transcription/pages/AB01-PDF0139–0142.json`), the page TeX and the pp. 44–53 TeX. The two PDFs were rebuilt: `pdf/S02_NALLINO_SOURCE_v009.pdf` and `pdf/S02_P044_053_source_replayed.pdf`.

## Typographic, not changed

- On p. 53 (ll. 19–20) the numerals inside the italic passage are italic in print. The build sets them upright because they are in math mode.
- The apparatus letters are bold italic in print and italic here, which is the convention of pp. 1–40.
- Page ranges printed with a hyphen are set with an en dash, consistently.
- The p. 50 chapter title has a hanging indent in print; here it is centred.
