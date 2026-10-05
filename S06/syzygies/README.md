# S06 — Mean syzygies in Egyptian years (Part II pp. 29–32)

Tables of the mean conjunctions and oppositions of the Sun and the Moon (codex fol. 170,v.–172,r.). The years are Egyptian years of 365 days without intercalation, counted from the era of Dhū ’l-qarnayn; each begins on 1 thoth, as do Ptolemy's years of Nabonassar. The first day of year 1 is 1 thoth of year 437 of Nabonassar, 9 November 312 BC.

| Page | Table | Rows |
|---|---|---|
| 29 | mean conjunctions in collected years 915, 940 … 1690 (periods of 25 years) | 32 |
| 30 | mean oppositions in the same years | 32 |
| 31 | parts of a month (⅙, ¼, ⅓, ½ of a lunation); 1–12 lunations; intervals of 50 … 600 years, to be added or subtracted | 4, 12, 7 |
| 32 | single years 1–24; below the frame the line for 25 years, and the eclipse limits of the Sun and the Moon | 24, 1 |

The columns give the year or the number of months; the day of the month thoth, in days and sixtieths of a day, on which the first mean conjunction or opposition of the year falls (on p. 32 the increment of the days, on p. 31 the days of the parts and lunations, and for the intervals minutes, seconds and thirds of a day); the mean longitude of the luminaries (at an opposition, the Sun's); the mean anomaly of the Moon; and the argument of latitude, the Moon's distance from the ascending node.

## Read

- [Part II pp. 29–32, 4 pp.](p2_syzygies.pdf).

## Data

| File | Content |
|---|---|
| `syz_p2.tsv` | One row per printed row: page, table, argument as printed, the four columns in three places each, how each number was established (`check`), and notes. |
| `syz_pages.tsv` | Folio line, Arabic and Latin titles and heads of each table, and the units of its day column. |
| `syz_extra.tsv` | The line for 25 years under the table of p. 32, and the two paragraphs of eclipse limits. |
| `syz_discrepancies.tsv` | The 4 differences found, and the 6 numbers that Nallino emends in his notes. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and resolved against the line of its column: 1,173 numbers in class A (both readers give the value on the line), 117 in class B (one reader gives it; each cell checked by eye), and 42 in class E (read by eye: the fit flagged the cell, or a reader failed on the marks of a first row).

`python check_syzygies.py` checks the tables against one another and against the mean lunation of 29;31,50,8,20 days:

- **pp. 29–30**: each column is a line in the number of the 25-year period. Each row of p. 29 less the row of p. 30 is the half lunation of p. 31 («Monsis dimidium»): 14;45,55 days, 14° 33′ 12″, 192° 54′ 30″ and 195° 20′ 7″.
- **p. 31**: the 12 lunations are multiples of one lunation (29ᵈ 31′ 50″, 29° 6′ 25″, 25° 49′ 0″, 30° 40′ 14″). The parts of a month are ⅙, ¼, ⅓ and ½ of the motion in one lunation, whole revolutions included (385° 49′ for the anomaly, 390° 40′ 14″ for the latitude). The intervals of N years are N/25 times the line for 25 years under p. 32.
- **p. 32**: year n holds k lunations, the least whole number with k lunations ≥ 365 n days (13, 25, 38 … 297). Each motion is k times the motion in one lunation, and the increment of the days is k lunations less 365 n days.

437 values (each three places) lie within 3 units of the last place of their lines; the largest deviation is 2.6″, in the argument of latitude of year 10 on p. 32 (printed 203° 8′ 53″). Four differences are ledgered, and 0 are open:

- **p. 30, year 1190, anomaly**: printed 155° 55′ 7″ for 153° 55′ 7″.
- **p. 30, year 1465, longitude**: printed 210° 5′ 7″ for 240° 5′ 7″.
- **p. 30, year 1640, argument of latitude**: printed 111° 8′ 54″ for 211° 8′ 54″.

  Each of the three is confirmed twice: by the line of its column, and by the row of p. 29 less the half lunation.
- **p. 32, the line for 25 years, days**: printed 0ᵈ 57′ 13″ 5‴ 0ⁱᵛ. 309 lunations of 29;31,50,8,20 days are 9124;57,12,55,0 days. The day columns of pp. 29–30 (22;14,44 for 915, 20;48,24 for 1690) and the intervals of p. 31 (0;5,34,10 for 50 years) agree with the excess of 9125 days over 309 lunations, 0;2,47,5; the printed value corresponds to an excess of 0;2,46,55.

## Nallino's notes on these pages (Part II, pp. 205–209)

- **The tables** follow Ptolemy's (Almagest VI 3) in construction. In the third column Ptolemy gives the Sun's distance from its apogee, and in the fifth he counts the latitude from the northern limit. The table of single years agrees exactly with Ptolemy's.
- **p. 30**: the oppositions are the conjunctions less half a lunation (14;45,55 days) and less the motions in it.
- **p. 31**, in a note by Schiaparelli: the table of months is necessary and is also in the Almagest; he suspects that the parts of a month and the intervals of years are spurious, although similar tables stand on p. 87. In the codex an unskilled reader had filled the last column of the intervals (108° 47′ 19″ for 100 years, where pp. 29–30 give 108° 48′ 23½″); the printed column is Schiaparelli's computation from al-Battānī's elements. The heads of the intervals say that for a later time the days are subtracted and the motions added.
- **p. 31**, Nallino: the last line of the parts reads «Monsis» for «Mensis». The parts and the months recur on p. 87 with two small differences: ¼ month, 57″ here and 58″ there in the days; the third month, 1″ here and 0″ there in the anomaly.
- **p. 32, the increments of the days**: four values are to be corrected: 50″, 29″, 34″ and 13″ in years 6, 11, 14 and 19, for 40″, 39″, 24″ and 23″. This edition prints them as Nallino's table does; his corrections are in the ledger.
- **p. 32, the eclipse limits**: al-Battānī says that he gave them on the page of the months (ch. 42 and 44); in the codex they stand under this table and on p. 88. Nallino restored the lunar limits from corrupt numbers of the codex. The printed solar limits are his first emendation; in his notes he asks that they be read 159° 44′–190° 56′, 0°–20° 16′ and 349° 4′–360°, here and on p. 88.

## Conventions

- The first row of each table carries its marks as printed: ᵈ ′ ″ for days, ° ′ ″ for degrees, and ′ ″ ‴ for the days of the intervals. The parts of a month carry no marks.
- The line for 25 years stands below the frame of p. 32, with the thirds and fourths marked ᴵᴵᴵ and ᴵⱽ.
- The «a» of «mediarum» in the title of p. 32 is printed damaged.
- The head «وسطي النيّرين» has a fatḥa over the ṭāʾ and a kasra under the yāʾ on p. 29 (وسطَيِ), and the kasra only on pp. 31–32.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the note on p. 31.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
