# S13 — The chronological tables, in both of Nallino's versions

al-Battānī's chronological tables give, reign by reign, the years each ruler reigned and the running total from the start of the list. They have three parts:

- **The kings**, from Bukhtanaṣṣar I (Nabonassar, the epoch of Ptolemy's era) to Theodosius III: the Babylonian, Persian and Macedonian kings and the Ptolemies of Ptolemy's canon of kings (in his *Handy Tables*), continued with the Roman and Byzantine emperors. There are 99 rows, keyed K01–K99 after Part II. Each row gives the years of the reign and the running total.
- **The intervals between the eras** (*jadwal mā bayna l-tawārīkh*): eight lines, I1–I8, from Nebuchadnezzar to the ʿAbbāsids.
- **The caliphs** (*jadwal taʾrīkh al-khulafāʾ*), from the Hijra to al-Muṭīʿ. There are 58 rows, C01–C58. Each gives the years, months and days of the reign and of the running total, in lunar years.

| Witness | Pages | What it is |
|---|---|---|
| **Part III** (Arabic) | printed pp. 228–234 (master PDF 924–918; the upper table of p. 234) | The tables of the codex (Escorial, ár. 908, fol. 154,v.–157,r.). The numbers are in Maghribi abjad, with the codex's zero sign. On fol. 155,v. the hundreds are Eastern (see below). |
| **Part II** (Latin) | printed pp. 1–6 (master PDF 450–455) | Nallino's Latin tables: Western numerals, the names in Latin, and each Arabic heading with its translation. |

Both are transcribed from the scan as printed. Neither is corrected from the other.

## Read

- [Part III edition, 7 pp.](p3_chronology.pdf): the Arabic tables, right to left, one page per printed page, with the two panels of the king pages as printed, and Nallino's footnotes.
- [Part II edition, 6 pp.](p2_chronology.pdf): the Latin tables.

## Data

| File | Content |
|---|---|
| `chr_p3.tsv` | Part III rows: page, row, kind (title, column head, heading, row), section (K kings, I intervals, C caliphs), key of the Part II row, the Arabic text, the six number cells as printed (reign y m d, total y m d), and reading notes (`doubt`). |
| `chr_p3_footnotes.tsv`, `chr_p3_pages.tsv` | Nallino's footnotes to Part III, and the page signatures. |
| `chr_p2.tsv` | Part II rows: page, column (L, R; T for the full-width tables), key, Latin name, numbers as printed; Arabic headings as `Arabic//Latin`. |
| `chr_p2_pages.tsv` | Running heads, the lines above the tables (with Nallino's folio statements) and signatures of the Part II pages. |
| `chr_p2_codex.tsv` | Codex readings that Nallino reports in his notes, as structured values (so far I1 = 424, Part II p. 192). |
| `chr_discrepancies.tsv` | Differences between the witnesses that Nallino's notes do not explain, each checked in two scan copies, plus three notes on Nallino's own text (a folio statement, the spelling اتور/اثور, and a name he emended in Part III but not in Part II). |
| `chronology_joined.tsv` / `.json` | One row per Part III row: raw cells, decoded values, Part II values, codex readings, the numeral system of the row, status per field. |
| `rows/` | The page-by-page input files, with the reading notes as they were made. |

## How the two versions were checked

Every Part III number was read at 420–1500 dpi and decoded from the abjad. Each value was compared with Part II and with the codex readings in Nallino's notes:

| Result | Numbers |
|---|---|
| Agrees with Part II | 525 |
| Differs, and Nallino's note gives exactly this codex reading | 1 |
| Differs with no matching note (ledgered) | 16 |
| Open | 0 |

Each unexplained difference was read again in a second copy of the print (Internet Archive). `python check_chr.py` repeats the check. In 15 of the 16 ledgered cases the running totals show which value is consistent: the differing Part III cell is the one that does not fit. Examples: Zeno's total ضد (804) where 797 + 17 = 814; the months of Abū Bakr's total, د (4) where 10 y 2 m + 2 y 3 m 8 d needs 5. The exception is the interval from Diocletian to Heraclius, سكو (326). That is what the king list gives (933 − 607); Part II prints 336.

## Conventions

As in the star catalogue (see `../star_catalogue/README.md`). In addition:
- **The Eastern hundreds of fol. 155,v.** Nallino's footnote 8 on p. 230: «In hac pag. amanuensis oblitus est litteras numerales orientales archetypi in maghrebinicas convertere; ergo hic ض = 800, ظ = 900». The cells are entered as printed. The check reads the hundreds letter of these rows (Zeno, and the left panel of p. 230) with the Eastern value. A ض in the tens place keeps the Maghribi 90: ظضب = 992, ظصد = 964.
- **The thousand.** Totals over 1000 are printed as an ا, a gap, and the rest (ا ح = 1008). They are entered with a space and read as thousands and the rest.
- **Two tables on one page** (p. 231, the intervals and the first caliphs): the second table's row ids carry the prefix 2.
- **Names and vowels as printed.** Nallino vocalizes some words and not others; the marks are kept as printed. They were checked by rendering each page and comparing it with the scan line by line. Doubtful marks were measured: for example, a bare hamza is about 2.9 pt high, a hamza with a ḍamma touching it 6.1–6.4 pt (أُمَيَّةَ).
- **Codex forms in the footnotes** keep their printed dots, including three dots in a row below a tooth (ݐ, U+0750, p. 230 fn. 10) and dotless teeth (ى).
- **Nallino's emendations** stay as printed in Part III. His footnotes give the codex reading, and his later notes in Part II sometimes take the emendation back. For p. 229, أَرْنَب, he writes «vix recte» on Part II p. 194, and Part II translates the codex name at p. 230 L15. Both are noted in the row's `doubt`.

## Not done yet

- Part II pp. 191–198 (master PDF 640–647): Nallino's notes on these tables (*Ad pag. 1–6*), with the comparison with Ptolemy's canon, al-Bīrūnī and al-Masʿūdī. Only the codex value of I1 is entered from them so far.
- An independent second reading of the Arabic names and their harakat.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the edition of the codex (Part III), the Latin version and the notes (Part II), Milan 1899–1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
