# S06 — Mean motions of the Sun, the Moon, the lunar anomaly and the node (Part II pp. 19–23)

Five tables of mean motions for the Arab (Hijra) calendar (codex fol. 164,v.–166,v.):

| Page | Argument | Rows |
|---|---|---|
| 19 | collected years 1, 31, 61 … 871 (the positions at the start of each 30-year step) | 30 |
| 20 | single years 1–30 (the motion in that many years) | 30 |
| 21 | months, to the end of al-muḥarram … dhū ’l-ḥiǵǵah, common and leap year | 13 |
| 22 | days 1–30 | 30 |
| 23 | equinoctial hours 1–24 | 24 |

Each row gives four motions in degrees, minutes and seconds: the mean longitude of the Sun («Solis longitudo media» or «iter medium»), the mean longitude of the Moon, the mean anomaly of the Moon, and the motion of the ascending node.

## Read

- [Part II pp. 19–23, 5 pp.](p2_mean_motions.pdf).

## Data

| File | Content |
|---|---|
| `mm_p2.tsv` | One row per printed row: page, table, argument as printed, the four motions (degrees, minutes, seconds), how each number was established (`check`), and notes. |
| `mm_pages.tsv` | Folio line, Arabic and Latin title and column heads of each page. |
| `mm_discrepancies.tsv` | The two differences found. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer. Each motion column is a linear function of time: the value is a + b·t (mod 360°), where t is the number of days. A column has 30 days per month, 354 or 355 per year, and 10,631 per 30 years. The readings of each cell were resolved against that line:

| Class | Numbers | How established |
|---|---|---|
| A | 1,401 | Both readers give the value on the line. |
| B | 111 | One reader gives it; each cell checked by eye. |
| E | 12 | The fit flagged the row; the cell read by eye. |

`python check_mean_motions.py` refits every column from the data alone. 507 values lie within 3″ of their lines (largest deviation 2.1″, the accumulated rounding of the tables). Two differences are ledgered, and 0 are open:

- **p. 20, single year 26, node**: printed 127° 53′ 9″, while the line through the other 29 rows gives 127° 53′ 20″. The steps to the neighbouring rows miss those of a 355- and a 354-day year by the same 11″.
- **One year's anomaly in two tables**: the motion of the anomaly in a common year of 354 days is printed 305° 0′ 14″ on p. 20 (single year 1) and 305° 0′ 13″ on p. 21 (dhū ’l-ḥiǵǵah, comm.).

The script also checks that 24 hours on p. 23 equal one day on p. 22 in every column.

## Conventions

- The first row of each table carries the signs ° ′ ″ after the numbers, as printed.
- In the Arabic heads the word for the anomaly is printed حاصّة or حاصة, with ḥāʾ undotted, and with the shadda only on p. 19.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
