# S06 — Mean motions in the Arab calendar (Part II pp. 19–28)

Ten tables of mean motions for the Arab (Hijra) calendar (codex fol. 164,v.–170,r.):

| Page | Argument | Rows | Motions |
|---|---|---|---|
| 19 | collected years 1, 31, 61 … 871 (the positions at the start of each 30-year step) | 30 | the Sun, the Moon, the lunar anomaly and the node, in degrees, minutes and seconds |
| 20 | single years 1–30 (the motion in that many years) | 30 | 〃 |
| 21 | months, to the end of al-muḥarram … dhū ’l-ḥiǵǵah, common and leap year | 13 | 〃 |
| 22 | days 1–30 | 30 | 〃 |
| 23 | equinoctial hours 1–24 | 24 | 〃 |
| 24 | collected years 1, 31, 61 … 871 | 30 | Saturn, Jupiter and Mars (mean longitude), and the anomalies of Venus and Mercury, in degrees and minutes |
| 25 | single years 1–30 | 30 | 〃 |
| 26 | months, to the end of al-muḥarram … dhū ’l-ḥiǵǵah | 12 | 〃 |
| 27 | days 1–30 | 30 | 〃 |
| 28 | equinoctial hours 1–24 | 24 | 〃 |

On pp. 19 and 24 the numbers are mean longitudes (and anomalies) at the beginning of the years 1, 31, 61 …; the other tables give the motion during the stated time. Venus and Mercury have no longitude column: their mean longitude is the Sun's. The superior planets have no anomaly column: their mean anomaly is the Sun's mean motion less their own. The tables count the motion of the node as direct; it is subtracted from 360° when used.

## Read

- [Part II pp. 19–28, 10 pp.](p2_mean_motions.pdf).

## Data

| File | Content |
|---|---|
| `mm_p2.tsv` | pp. 19–23: one row per printed row: page, table, argument as printed, the four motions (degrees, minutes, seconds), how each number was established (`check`), and notes. |
| `mm_pages.tsv` | pp. 19–23: folio line, Arabic and Latin title and column heads of each page. |
| `mm5_p2.tsv` | pp. 24–28: the same for the five planetary motions (degrees, minutes). |
| `mm5_pages.tsv` | pp. 24–28: folio lines, titles and heads. |
| `mm_discrepancies.tsv` | The 15 differences found, and the 4 cells that Nallino emends in his notes. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer. Each motion column is a linear function of time: the value is a + b·t (mod 360°), where t is the number of days. A column has 30 or 29 days per month, 354 days per year (355 in the leap years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26 and 29 of the 30-year cycle), and 10,631 days per 30 years. The readings of each cell were resolved against that line:

| Class | pp. 19–23 | pp. 24–28 | How established |
|---|---|---|---|
| A | 1,400 | 1,152 | Both readers give the value on the line. |
| B | 112 | 88 | One reader gives it; each cell checked by eye. |
| E | 12 | 20 | The fit flagged the row; the cell read by eye. |

`python check_mean_motions.py` refits every column from the data alone. 1,129 values lie within 3 units of the last place of their lines; the largest deviation among them is 1.8″ on pp. 19–23 and 1.6′ on pp. 24–28, the accumulated rounding of the tables. Fifteen differences are ledgered, and 0 are open:

- **p. 20, single year 26, node**: printed 127° 53′ 9″, while the line through the other 29 rows gives 127° 53′ 21″. The steps to the neighbouring rows, 18° 47′ 41″ and 18° 44′ 53″, are 10″ shorter and 12″ longer than the motions in a 355- and a 354-day year.
- **One year's lunar anomaly in two tables**: the motion of the anomaly in a common year of 354 days is printed 305° 0′ 14″ on p. 20 (single year 1) and 305° 0′ 13″ on p. 21 (dhū ’l-ḥiǵǵah, comm.).
- **p. 24, Jupiter, AH 811, 841 and 871**: printed 73° 34′, 237° 21′ and 41° 9′, each 1° below the line. The step from AH 781 (270° 46′) to AH 811 is 162° 48′; every other 30-year step of the column is 163° 47′ or 163° 48′, so the missing degree carries on to the end of the column.
- **p. 25, Jupiter, years 2, 7 and 10, and Venus, year 2**: each value is one day's motion (4′ 59″ for Jupiter, 36′ 59″ for the anomaly of Venus) below the line. These are leap years; 708, 2,480 and 3,543 days, one fewer than the rows require, give 58° 51.5′, 206° 10.3′ and 294° 32.6′ for Jupiter (printed 58° 51′, 206° 10′, 294° 33′) and 76° 29.9′ for Venus (printed 76° 30′). The rows after them count the day again.
- **p. 25, Jupiter, year 5**: printed 157° 19′ for 147° 19′.
- **One common year in pp. 25 and 26**: the motion in 354 days is 1′ greater on p. 25 (single year 1) than on p. 26 (dhū ’l-ḥiǵǵah) in every column: 11° 52′ and 11° 51′ (Saturn), 29° 26′ and 29° 25′ (Jupiter), 185° 31′ and 185° 30′ (Mars), 218° 15′ and 218° 14′ (Venus), 19° 46′ and 19° 45′ (Mercury). The daily motions implied by the 30-year steps of p. 24 give 11° 51.5′, 29° 25.8′, 185° 31.3′, 218° 15.0′ and 19° 46.4′ for 354 days. Page 25 gives these to the nearest minute. The months of p. 26 fall progressively below them and end 0.5′ to 1.4′ lower.

The script also checks that 24 hours (pp. 23 and 28) equal one day (pp. 22 and 27) in every column.

## Nallino's notes on these pages (Part II, pp. 203–204)

- **p. 19**: the codex omits the degrees of the lunar anomaly from year 661 on; Nallino restored them.
- **p. 21**: the codex gives dhū ’l-ḥiǵǵah of common years only. Nallino added the row for leap years («bisext.») at Schiaparelli's suggestion; the tables for collected and single years make the distinction unnecessary in computing.
- **pp. 22–23**: four cells are errors of the codex. This edition prints them as Nallino's table does; his corrections are in the ledger:

  | Cell | Printed | Nallino | Line through the table |
  |---|---|---|---|
  | p. 22, Sun, 10 days | 9° 51′ 25″ | 24″ | 23.4″ |
  | p. 22, node, 21 days | 1° 6′ 45″ | 44″ | 44.0″ |
  | p. 23, Sun, 3 hours | 0° 7′ 25″ | 24″ | 23.7″ |
  | p. 23, anomaly, 23 hours | 12° 31′ 13″ (codex 33″) | 14″ | 14.2″ |

- **pp. 19 and 24, column heads**: the codex heads the columns of pp. 19–23 al-masīr al-awsaṭ («iter medium»), which suits the motions of pp. 20–23. On p. 19 the numbers are mean longitudes, so Nallino's Latin heads there read «longitudo media». The Arabic heads of p. 24 are those of pp. 25–26; his Latin heads differ in the same way.
- **pp. 27–28**: Nallino notes that these pages necessarily agree with pp. 106 and 105.
- Nallino omits folio 167 of the codex, an addition unrelated to al-Battānī's tables.

## Conventions

- The first row of each table carries the signs ° ′ ″ after the numbers, as printed.
- In the Arabic heads the word for the anomaly, khāṣṣa, is printed with an undotted first letter, حاصّة or حاصة, and with the shadda only on p. 19.
- The first column head of p. 24 is printed «لسنون العربية المجموعة», without the alif of السنون.
- The dashes in the month names follow the print: p. 21 has dhū ’l-qa‘dah with a hyphen, p. 26 the long dash in al–muḥarram, dhū ’l–qa‘dah and dhū ’l–ḥiǵǵah.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
