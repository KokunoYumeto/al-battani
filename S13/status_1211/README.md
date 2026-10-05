# S13 — The status tables of the bright fixed stars for the year 1211, in both of Nallino's versions

For about 75 bright stars (*ḥālāt al-kawākib al-thābita al-mashhūra*), al-Battānī tabulates their position for the year 1211 of Dhū ’l-qarnayn, at the latitude of al-Raqqa (36°):
- the declination and its direction;
- the meridian altitude;
- half the time above the horizon (the semi-diurnal arc);
- the degrees of the ecliptic that culminate, rise and set with the star.

| Witness | Pages | What it is |
|---|---|---|
| **Part III** (Arabic) | printed pp. 275–279 (master PDF 877–873) | The tables of the codex (Escorial, ár. 908, fol. 237,v.–239,r.) in three magnitude classes, with the numbers in Maghribi abjad and the codex's zero sign. The third table (from fol. 238,v.) has no magnitude column. |
| **Part II** (Latin) | printed pp. 178–186 (master PDF 627–635) | Nallino's *Status praecipuarum stellarum fixarum anno 1211 a Dhū ’l-qarnayn*, with Western numerals, star identifications and his notes on the codex readings (based on Schiaparelli's recomputations). |

Both are transcribed from the scan as printed. Neither is corrected from the other.

## Read

- [Part III edition, 5 pp.](p3_status_1211.pdf): the Arabic tables, right to left, one page per printed page. Two texts printed inside the tables are set where they stand:
  - the note on the eight circumpolar stars, printed vertically across their columns;
  - the sentence that replaces the numbers of a star that never rises at al-Raqqa.
- [Part II edition, 9 pp.](p2_status_1211.pdf): the Latin tables with Nallino's notes.

## Data

| File | Content |
|---|---|
| `st_p3.tsv` | Part III rows: page, row, kind (title, column head, star, `vnote`/`hnote` for the printed texts), table (M1–M3), star number, the Arabic name, the 13 numeric cells and the direction as printed, the magnitude, and reading notes (`doubt`). |
| `st_p3_footnotes.tsv`, `st_p3_pages.tsv` | Nallino's footnotes to Part III; folio labels. |
| `st_p2.tsv`, `st_p2_notes.tsv`, `st_p2_pages.tsv` | Part II rows; Nallino's notes, with the codex readings he reports in a structured column (e.g. `half_d=103;ris_m=35`); running heads and signatures. |
| `st_discrepancies.tsv` | Differences between the witnesses that Nallino's notes do not explain, and slips found in the notes, each checked in two scan copies. |
| `status_1211_joined.tsv` / `.json` | One row per Part III star row: raw cells, decoded values, Part II values, codex readings, status per field. |

## How the two versions were checked

Every Part III cell was read at 500–1600 dpi and decoded from the abjad, then compared with Part II and with the codex readings in Nallino's notes:

| Result | Cells |
|---|---|
| Agrees with Part II | 836 |
| Differs, and Nallino's note gives exactly this codex reading | 120 |
| Differs with no matching note (ledgered) | 7 |
| Open | 0 |

Each unexplained difference was read again in a second copy of the print (Internet Archive). Every structured note value must also equal the Part III reading. `python check_status.py -a` repeats the check. It also lists, for information only, where the meridian altitude (54° ± δ) or the semi-diurnal arc computed from the declination differs from the table. Every such case coincides with a codex error that Nallino notes, or with a ledgered cell.

The two-way check also caught three of my own misreadings before anything was ledgered: ص read for ض twice, and ص read for س.

## Conventions

As in the star catalogue (see `../star_catalogue/README.md`). In addition:
- **`{zero:لا}`**: the word لا ("none") printed in a minutes cell, read as 0. Nallino himself writes لا for 0′ in his note 75.
- **Eastern-abjad forms** inside the Maghribi codex are kept as printed and ledgered:
  - سو for 66 (Maghribi value 306);
  - شل for 330 (Maghribi value 1030).
- **Dotless letters** whose reading is fixed by Part II, the arithmetic or Nallino's note are written with `{rd:printed=read}`, for example `{rd:ٯ=ق}` for a qāf/fāʾ without dots.

## Not done yet

An independent second reading of the Arabic names and their harakat.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the edition of the codex (Part III), the Latin version and the notes (Part II), Milan 1899–1907. G. V. Schiaparelli: the recomputations on which Nallino's notes rest.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
