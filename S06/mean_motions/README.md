# S06 — Mean motions in the Arab and the Roman calendar (Part II pp. 19–28, 72–77, 102–107)

Ten tables of mean motions for the Arab (Hijra) calendar (codex fol. 164,v.–170,r.) and twelve for the Roman calendar (fol. 186,v.–189,r. and 205,v.–208,r.):

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
| 72 | collected Roman years 931, 951 … 1631 of the era of Dhū ’l-qarnayn (steps of 20 Julian years) | 36 | the Sun, the Moon, the lunar anomaly and the node, in degrees, minutes and seconds |
| 73 | single Roman years 1–20 | 20 | 〃 |
| 74 | the Roman months, ādhār [March] … subāṭ [February], common and leap year | 13 | 〃 |
| 75 | days 1–30 | 30 | 〃 |
| 76 | equinoctial hours 1–24 | 24 | 〃 |
| 77 | intervals of 20, 40 … 100, 200 … 600 Roman years | 10 | 〃 |
| 102 | collected Roman years 931, 951 … 1591 | 34 | Saturn, Jupiter and Mars (mean longitude), and the anomalies of Venus and Mercury, in degrees and minutes |
| 103 | single Roman years 1–20, with the motions in 20 years to the thirds below them; sums of 40, 60, 80, 100, 200, 400 and 600 years | 20, 7 | 〃 |
| 104 | the Roman months, ādhār [March] … subāṭ [February], common and leap year | 13 | 〃 |
| 105 | equinoctial hours 1–24 | 24 | 〃 |
| 106 | days 1–30 | 30 | 〃 |
| 107 | the motion of the fixed stars, in one frame: collected Roman years 20, 40 … 440; single years 1–20; the Roman months; days 1–30 | 22, 20, 12, 30 | degrees, minutes and seconds (collected years); minutes and seconds, with the thirds in the first and last single years and in 30 days |

On pp. 19 and 24 the numbers are mean longitudes (and anomalies) at the beginning of the years 1, 31, 61 …; the other tables give the motion during the stated time. Venus and Mercury have no longitude column: their mean longitude is the Sun's. The superior planets have no anomaly column: their mean anomaly is the Sun's mean motion less their own. The tables count the motion of the node as direct; it is subtracted from 360° when used.

## Read

- [Part II pp. 19–28, 72–77 and 102–107, 22 pp.](p2_mean_motions.pdf).

## Data

| File | Content |
|---|---|
| `mm_p2.tsv` | pp. 19–23: one row per printed row: page, table, argument as printed, the four motions (degrees, minutes, seconds), how each number was established (`check`), and notes. |
| `mm_pages.tsv` | pp. 19–23: folio line, Arabic and Latin title and column heads of each page. |
| `mm5_p2.tsv` | pp. 24–28: the same for the five planetary motions (degrees, minutes). |
| `mm5_pages.tsv` | pp. 24–28: folio lines, titles and heads. |
| `mmr_p2.tsv` | pp. 72–77: the four motions in the Roman calendar, as `mm_p2.tsv`. |
| `mmr_pages.tsv` | pp. 72–77: folio lines, titles and heads. |
| `mm5r_p2.tsv` | pp. 102–106: the five planetary motions in the Roman calendar, as `mm5_p2.tsv`; on p. 103 the single years (`single`) and the sums of years (`intervals`). |
| `mm5r_pages.tsv` | pp. 102–106: folio lines, titles, heads, the subtitle of the sums and the signature of p. 105. |
| `mm5r_extra.tsv` | The motions in 20 years printed under the single years of p. 103, to the thirds. |
| `fs_p2.tsv` | p. 107: one row per printed row of the four tables: table, row, argument (and for the months the days to their end), the degrees, minutes, seconds and thirds as printed, and `check`. |
| `mm_discrepancies.tsv` | The 32 differences found, and the 4 cells that Nallino emends in his notes. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer. Each motion column is a linear function of time: the value is a + b·t (mod 360°), where t is the number of days. In the Arab calendar a column has 30 or 29 days per month, 354 days per year (355 in the leap years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26 and 29 of the 30-year cycle), and 10,631 days per 30 years; in the Roman calendar the months of 31, 30 and 28 (29) days from March to February, 365 days per year (366 in every fourth), and 7,305 days per 20 years. The readings of each cell were resolved against that line:

| Class | pp. 19–23 | pp. 24–28 | pp. 72–77 | pp. 102–106 | How established |
|---|---|---|---|---|---|
| A | 1,385 | 1,145 | 1,445 | 1,119 | Both readers give the value on the line. |
| B | 124 | 95 | 133 | 131 | One reader gives it (for 35 numbers in all, only the glyph reader: the text layer has no token there); each cell checked by eye or by Tesseract as a third reader. |
| E | 15 | 20 | 18 | 30 | The fit flagged the row, or a reader failed; the cell read by eye. |

The numbers of p. 107 were read by eye at 260–450 dpi and compared row by row with the OCR text layer: 77 rows agree (class A); in 7 the text layer misreads a digit or misses the row, and the zoom confirms the reading (class E).

`python check_mean_motions.py` refits every column from the data alone. 2,299 values lie within 3 units of the last place of their lines; the largest deviation among them is 1.8″ on pp. 19–23, 1.6′ on pp. 24–28, 1.2″ on pp. 72–77 and 2.6′ on pp. 102–106 (Mercury's single years, below), the accumulated rounding of the tables; the 83 values of p. 107 add to these (2,382 in all). Thirty-two differences are ledgered, and 0 are open:

- **p. 20, single year 26, node**: printed 127° 53′ 9″, while the line through the other 29 rows gives 127° 53′ 21″. The steps to the neighbouring rows, 18° 47′ 41″ and 18° 44′ 53″, are 10″ shorter and 12″ longer than the motions in a 355- and a 354-day year.
- **One year's lunar anomaly in two tables**: the motion of the anomaly in a common year of 354 days is printed 305° 0′ 14″ on p. 20 (single year 1) and 305° 0′ 13″ on p. 21 (dhū ’l-ḥiǵǵah, comm.).
- **p. 24, Jupiter, AH 811, 841 and 871**: printed 73° 34′, 237° 21′ and 41° 9′, each 1° below the line. The step from AH 781 (270° 46′) to AH 811 is 162° 48′; every other 30-year step of the column is 163° 47′ or 163° 48′, so the missing degree carries on to the end of the column.
- **p. 25, Jupiter, years 2, 7 and 10, and Venus, year 2**: each value is one day's motion (4′ 59″ for Jupiter, 36′ 59″ for the anomaly of Venus) below the line. These are leap years; 708, 2,480 and 3,543 days, one fewer than the rows require, give 58° 51.5′, 206° 10.3′ and 294° 32.6′ for Jupiter (printed 58° 51′, 206° 10′, 294° 33′) and 76° 29.9′ for Venus (printed 76° 30′). The rows after them count the day again.
- **p. 25, Jupiter, year 5**: printed 157° 19′ for 147° 19′.
- **One common year in pp. 25 and 26**: the motion in 354 days is 1′ greater on p. 25 (single year 1) than on p. 26 (dhū ’l-ḥiǵǵah) in every column: 11° 52′ and 11° 51′ (Saturn), 29° 26′ and 29° 25′ (Jupiter), 185° 31′ and 185° 30′ (Mars), 218° 15′ and 218° 14′ (Venus), 19° 46′ and 19° 45′ (Mercury). The daily motions implied by the 30-year steps of p. 24 give 11° 51.5′, 29° 25.8′, 185° 31.3′, 218° 15.0′ and 19° 46.4′ for 354 days. Page 25 gives these to the nearest minute. The months of p. 26 fall progressively below them and end 0.5′ to 1.4′ lower.

- **p. 72, the year 1171 of the era, node**: printed 140° 34′ 37″ for 149° 34′ 37″; the node advances by 26° 48′ 23″ or 24″ every 20 years, and the neighbouring rows are 122° 46′ 13″ (1151) and 176° 23′ 0″ (1191).
- **pp. 75–76 against pp. 22–23**: the days and hours of the Roman calendar are the same motions as those of pp. 22–23, and nine cells of the two tables differ, each by 1″ or 2″. Five of them Nallino names as differences that come from al-Battānī himself: the Sun in 9 days (15″ on p. 75, 16″ on p. 22) and in 10 days (23″, 25″), the anomaly in 10 days (130° 38′ 59″, 130° 39′ 0″), the Moon in 14 hours (11″ on p. 76, 10″ on p. 23) and the anomaly in 10 hours (37″, 38″; exactly 5° 26′ 37″ 28‴ 17⁗). In three, pp. 75–76 have the values to which Nallino corrects pp. 22–23 (the node in 21 days, the Sun in 3 hours, the anomaly in 23 hours). The ninth is the anomaly in 24 days: 35″ on p. 75, 34″ on p. 22; the computation gives 313° 33′ 34.6″.

- **p. 102, the year 1591 of the era, Saturn**: printed 212° 45′ for 242° 45′. Saturn at 1571 (358° 2′) plus the motion in 20 years under p. 103 (244° 42′ 44″ 20‴) gives 242° 44′ 44″; every other 20-year step of the column is 244° 42′ or 244° 43′.
- **pp. 105–106 against pp. 27–28**: five cells differ by 1′. Mercury in 11 days, 34° 11′ on p. 106 and 34° 10′ on p. 27 (computed 34° 10′ 25″); Mars in 5 hours, 0° 7′ on p. 105 and 0° 6′ on p. 28 (6′ 33″); Saturn in 7 hours, 0° 0′ and 0° 1′ (35″); Jupiter in 12 hours, 0° 3′ and 0° 2′ (2′ 29.6″); Saturn in 18 hours, 0° 2′ and 0° 1′ (1′ 30.4″).

- **p. 107, 20 single years**: 18′ 11″ 24‴. Twenty years at one degree in 66 years give 18′ 10″ 54.5‴, and twenty times the motion of one year printed above it (0′ 54″ 33‴) 18′ 11″ 0‴; the collected years give 0° 18′ 11″ for 20 years. The other 83 values of the page lie within one unit of their last place of the motion of one degree in 66 Roman years (three units for the thirds).

The script also checks that 24 hours equal one day in every column (pp. 22–23, 27–28, 75–76, 105–106), that one Roman year (pp. 73, 103) equals the months to the end of a common February (pp. 74, 104), that 20 single Roman years (p. 73) equal the interval of 20 years (p. 77), and that the motions in 20 years printed under p. 103 equal its year 20 to the minute and the 20-year steps of p. 102 within 1′. Mercury's single years 10–16 on p. 103 lie 3.0′–4.2′ below the motion computed from that line (year 17, 2.0′): the step from year 9 to year 10 is 2.8′ shorter than a year's motion, and the step from year 16 to year 17 2.2′ longer. Against the line fitted to the column itself they lie within 2.6′.

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
- **pp. 27–28**: Nallino notes that these pages necessarily agree with pp. 106 and 105 (but see the five cells above).
- **pp. 72–77** (Part II pp. 222–223): the era is that of Dhū ’l-qarnayn (the Seleucids), but counted in a fictitious year that begins on 1 ādhār (March) of the year before, so that the Julian intercalation causes no difficulty. On p. 74 the codex gives subāṭ (February) of common years only; Nallino added the leap-year row, as on p. 21. On p. 77 the codex omits the motions of 20 years, perhaps because the heads give them (except for the node): the row for 20 years is Nallino's. The heads give the motion in 20 years to the sixths: the Sun 0° 11′ 10″ 14‴ 35ᴵⱽ 31ⱽ 30ⱽᴵ, the Moon 133° 35′ 33″ 11‴ 4ᴵⱽ 59ⱽ 45ⱽᴵ, the anomaly 39° 41′ 59″ 15‴ 5ᴵⱽ 38ⱽ 55ⱽᴵ.
- **pp. 102–106** (Part II p. 238): the Roman year is the same fictitious year from 1 ādhār. Why the superior planets have no anomaly column and the inferior no longitude column is explained on p. 204. The motions of these tables differ slightly from Ptolemy's over long intervals (t. I, pp. 239 and 242); on the column heads of p. 102, what is said on pp. 203–204 applies. On p. 103 the minutes of Mercury's anomaly in the single years 10 to 17, computed more roughly, differ by 1′ and 2′ from the correct ones. On p. 104 the scribe wrote 0 everywhere for subāṭ; Nallino restored the numbers and added the leap-year subāṭ, although it is superfluous (t. II, p. 223, on II, 74). pp. 105 (hours) and 106 (days) necessarily agree with pp. 28 and 27.
- **p. 107**: Nallino has no note on this page. Elsewhere (Part II p. 293) he uses al-Battānī's precession of one degree in 66 solar years.
- Nallino omits folio 167 of the codex, an addition unrelated to al-Battānī's tables.

## Conventions

- The first row of each table carries the signs ° ′ ″ after the numbers, as printed.
- In the Arabic heads the word for the anomaly, khāṣṣa, is printed with an undotted first letter, حاصّة or حاصة, and with the shadda only on p. 19.
- The first column head of p. 24 is printed «لسنون العربية المجموعة», without the alif of السنون.
- The dashes in the month names follow the print: p. 21 has dhū ’l-qa‘dah with a hyphen, p. 26 the long dash in al–muḥarram, dhū ’l–qa‘dah and dhū ’l–ḥiǵǵah.
- The rows stand in groups of five, and of four in the tables of hours (pp. 23, 28, 76, 105) and on p. 72, as printed. On p. 74 the leap-year February gives the Sun 360° 44′ 54″, past the full circle, as printed.
- On p. 103 the motions in 20 years stand under the single years, without a frame line, with the thirds below the seconds; the arguments of the sums (40 … 600) are in italic, as printed. p. 105 carries the signature 14 at the foot.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
