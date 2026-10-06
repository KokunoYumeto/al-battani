# S06 — Mean syzygies (Part II pp. 29–32 and 84–87)

Tables of the mean conjunctions and oppositions of the Sun and the Moon, in two sets: in Egyptian years (pp. 29–32, codex fol. 170,v.–172,r.) and in Roman years (pp. 84–87, codex fol. 192,v.–194,r.).

## Read

- [Part II pp. 29–32 and 84–87, 8 pp.](p2_syzygies.pdf).

## Data

| File | Content |
|---|---|
| `syz_p2.tsv`, `rsyz_p2.tsv` | One row per printed row of pp. 29–32 and 84–87: page, table, argument as printed (and on p. 87 the sums of the days of the months), the four columns in three places each, how each number was established (`check`), and notes. |
| `syz_pages.tsv`, `rsyz_pages.tsv` | Folio line, Arabic and Latin titles and heads of each table, and the units of its day column. |
| `syz_extra.tsv` | The line for 25 years under the table of p. 32, and the two paragraphs of eclipse limits. |
| `syz_discrepancies.tsv` | pp. 29–32: the 4 differences found, and the 6 numbers that Nallino emends in his notes. |
| `rsyz_discrepancies.tsv` | pp. 84–87: the 9 differences found, and the 6 numbers that Nallino emends in his notes. |

## Egyptian years (pp. 29–32)

The years are Egyptian years of 365 days without intercalation, counted from the era of Dhū ’l-qarnayn; each begins on 1 thoth, as do Ptolemy's years of Nabonassar. The first day of year 1 is 1 thoth of year 437 of Nabonassar, 9 November 312 BC.

| Page | Table | Rows |
|---|---|---|
| 29 | mean conjunctions in collected years 915, 940 … 1690 (periods of 25 years) | 32 |
| 30 | mean oppositions in the same years | 32 |
| 31 | parts of a month (⅙, ¼, ⅓, ½ of a lunation); 1–12 lunations; intervals of 50 … 600 years, to be added or subtracted | 4, 12, 7 |
| 32 | single years 1–24; below the frame the line for 25 years, and the eclipse limits of the Sun and the Moon | 24, 1 |

The columns give the year or the number of months; the day of the month thoth, in days and sixtieths of a day, on which the first mean conjunction or opposition of the year falls (on p. 32 the increment of the days, on p. 31 the days of the parts and lunations, and for the intervals minutes, seconds and thirds of a day); the mean longitude of the luminaries (at an opposition, the Sun's); the mean anomaly of the Moon; and the argument of latitude, the Moon's distance from the ascending node.

### How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and resolved against the line of its column: 1,164 numbers in class A (both readers give the value on the line), 126 in class B (one reader gives it; each cell checked by eye, or, for the 9 numbers that only the glyph reader saw, confirmed by Tesseract or read by eye), and 42 in class E (read by eye: the fit flagged the cell, or a reader failed on the marks of a first row).

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

### Nallino's notes on these pages (Part II, pp. 205–209)

- **The tables** follow Ptolemy's (Almagest VI 3) in construction. In the third column Ptolemy gives the Sun's distance from its apogee, and in the fifth he counts the latitude from the northern limit. The table of single years agrees exactly with Ptolemy's.
- **p. 30**: the oppositions are the conjunctions less half a lunation (14;45,55 days) and less the motions in it.
- **p. 31**, in a note by Schiaparelli: the table of months is necessary and is also in the Almagest; he suspects that the parts of a month and the intervals of years are spurious, although similar tables stand on p. 87. In the codex an unskilled reader had filled the last column of the intervals (108° 47′ 19″ for 100 years, where pp. 29–30 give 108° 48′ 23½″); the printed column is Schiaparelli's computation from al-Battānī's elements. The heads of the intervals say that for a later time the days are subtracted and the motions added.
- **p. 31**, Nallino: the last line of the parts reads «Monsis» for «Mensis». The parts and the months recur on p. 87 with two small differences: ¼ month, 57″ here and 58″ there in the days; the third month, 1″ here and 0″ there in the anomaly.
- **p. 32, the increments of the days**: four printed values, 50″, 29″, 34″ and 13″ in years 6, 11, 14 and 19, are to be read 40″, 39″, 24″ and 23″; on p. 230 Nallino calls the 29″ of year 11 a misprint. This edition prints them as Nallino's table does; his corrections are in the ledger.
- **p. 32, the eclipse limits**: al-Battānī says that he gave them on the page of the months (ch. 42 and 44); in the codex they stand under this table and on p. 88. Nallino restored the lunar limits from corrupt numbers of the codex. The printed solar limits are his first emendation; in his notes he asks that they be read 159° 44′–190° 56′, 0°–20° 16′ and 349° 4′–360°, here and on p. 88.

### Conventions

- The first row of each table carries its marks as printed: ᵈ ′ ″ for days, ° ′ ″ for degrees, and ′ ″ ‴ for the days of the intervals. The parts of a month carry no marks.
- The line for 25 years stands below the frame of p. 32, with the thirds and fourths marked ᴵᴵᴵ and ᴵⱽ.
- The «a» of «mediarum» in the title of p. 32 is printed damaged.
- The head «وسطي النيّرين» has a fatḥa over the ṭāʾ and a kasra under the yāʾ on p. 29 (وسطَيِ), and the kasra only on pp. 31–32.

## Roman years (pp. 84–87)

The days are counted from 1 ādhār (March); the Roman months of p. 87 run from ādhār to subāṭ (February), 365 days in all. Year n ends 365 n + [n/4] days after the beginning of year 1, so that the fourth, eighth … years have a day more.

| Page | Table | Rows |
|---|---|---|
| 84 | mean conjunctions in collected years 879, 903 … 1623 (periods of 24 years) | 32 |
| 85 | mean oppositions in the same years | 32 |
| 86 | single years 1–24 | 24 |
| 87 | parts of a month (½, ⅓, ¼, ⅙ of a lunation); the twelve Roman months, with the sums of their days; intervals of 48, 72, 96, 192, 288, 384 and 480 years | 4, 12, 7 |

The columns give the day of ādhār on which the first mean conjunction or opposition of the year falls, in days, minutes and seconds; the mean longitude of the luminaries (on p. 85, the Sun's, opposite the Moon); the mean anomaly of the Moon; and the argument of latitude.

### How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and resolved against the line of its column: 1,195 numbers in class A, 98 in class B (one reader gives the value, and for 2 of them only the glyph reader; each confirmed by Tesseract as a third reader or read by eye), and 39 in class E (read by eye). The sums of the days of the months (31, 61 … 365) agree with the calendar.

`python check_roman_syzygies.py` checks the tables against one another and against the mean lunation of 29;31,50,8,20 days:

- **pp. 84–85**: each row adds 4ᵈ 35′ 11″ to the day and the motions of that interval, and when the day exceeds a lunation, a lunation and its motions are subtracted (Nallino's rule, below). The day is then a line in the period number, modulo a lunation, and each motion a line in the number of lunations: 297 per period, less those subtracted. The fitted period is 4ᵈ 35′ 11.21″ (297 lunations exceed 8766 days by 4ᵈ 35′ 11.25″), and the motions in one lunation are 29° 6′ 24.78″, 25° 49′ 0.14″ and 30° 40′ 14.00″. Each row of p. 84 less the row of p. 85 is half a lunation (p. 87).
- **p. 86**: year n holds k lunations, the least number that exceeds 365 n + [n/4] days (13, 25, 38 … 297). The day is k lunations less those days, and each motion is a line in k.
- **p. 87**: the months are 1–12 lunations and the parts of a month ½, ⅓, ¼ and ⅙ of one, whole revolutions included; both are also compared with the same tables of p. 31. The intervals of 24 m years are m periods of p. 84 less the lunations that the day passes, and their motions are those of the remaining lunations.

429 values lie within 3 units of the last place of their lines. Nine differences are ledgered, and 0 are open:

- **p. 84, 1623, argument of latitude**: printed 247° 3′ 0″ for 247° 3′ 51″. The line of the column gives 247° 3′ 50.8″, and the argument of latitude of p. 85 (82° 23′ 58″) less half a lunation (195° 20′ 7″) gives 247° 3′ 51″.
- **p. 85, 1623, day**: printed 22ᵈ 15′ 35″ for 23ᵈ 15′ 35″. The line gives 23ᵈ 15′ 35.3″, and the day of p. 84 (8ᵈ 29′ 40″) plus half a lunation (14ᵈ 45′ 55″) gives 23ᵈ 15′ 35″.
- **pp. 84–85, longitude, 1287–1335 and 1431–1479**: p. 84 less p. 85 is 14° 33′ 10″, against 14° 33′ 12″ or 13″ in all the other rows (half a lunation is 14° 33′ 12″). Both columns lie within 2″ of their lines. Each stretch begins where p. 84 subtracts a lunation with a longitude of 29° 6′ 22″ (1287) or 29° 6′ 23″ (1431), where its other subtractions use 29° 6′ 25″ (975, 1119, 1599), and ends where p. 85 next subtracts one (1359, 1503).
- **p. 86, longitude, years 8–12**: 3.5″–7.1″ above the line of the column; the departures rise from +2.0″ in year 6. Where p. 86 and p. 32 hold the same number of lunations (every year but 11 and 22), p. 86 less p. 32 is +2″, +3″, +3″, +3″, +5″ and +7″ in years 6–10 and 12, and between −2″ and 0″ in the others. Nallino notes this difference (below).
- **p. 87 and p. 31**: the two differences that Nallino notes on p. 206. A quarter of a lunation is 7ᵈ 22′ 58″ on p. 87 and 57″ on p. 31; the computation gives 7ᵈ 22′ 57.53″. The anomaly of three months (ayyār) is 77° 27′ 0″ on p. 87 and 1″ on p. 31; three lunations give 77° 27′ 0.43″.
- **p. 87, 480 years, longitude**: printed 7° 33′ 26″, where 5937 lunations give 7° 33′ 29.3″. The longitude of p. 84 advances by 4° 44′ 38″ in all 26 steps without a subtracted lunation; twenty such steps less three lunations give 7° 33′ 25.7″, and this rule gives all seven longitudes of the intervals within 0.6″.
- **p. 87, 192 years, argument of latitude**: see the next section.

### The argument of latitude in the intervals of p. 87

From 192 years on, the day of an interval passes one or more lunations, and the day, the longitude and the anomaly drop them with their motions. The argument of latitude does not:

| Years | Lunations the day drops | Printed | Schiaparelli's reading | Codex | Reduced like the other columns |
|---|---|---|---|---|---|
| 192 | 1 | 153° 14′ 18″, the motion of 2376 lunations (153° 14′ 18.7″) | — | — | 122° 34′ 4.7″ (2375 lunations) |
| 288 | 1 | 229° 56′ 27″ | 229° 51′ 27″, 3564 lunations (229° 51′ 28.1″) | 18′ in the minutes | 199° 11′ 14.1″ (3563) |
| 384 | 2 | 306° 28′ 36″, 4752 lunations (306° 28′ 37.4″) | 275° 48′ 22″, 4751 lunations (275° 48′ 23.4″) | 275° 4′ 10″ | 245° 8′ 9.5″ (4750) |
| 480 | 3 | 23° 5′ 45″, 5940 lunations (23° 5′ 46.8″) | 321° 45′ 17″, 5938 lunations (321° 45′ 18.8″) | 291° 0′ 40″ | 291° 5′ 4.8″ (5937) |

The printed values are the motions of 297 lunations a period, without the reduction (at 288 years with 56′ for 51′). Schiaparelli's readings drop one lunation fewer than the day. The last column is computed with the motion of p. 84 in one lunation, 30° 40′ 14.00″; the codex value for 480 years has its degrees. The ledger keeps the printed values: Nallino's readings for 288, 384 and 480 years, and a difference at 192 years.

### Nallino's notes on these pages (Part II, p. 230)

- **pp. 84–85**: given the first line, each row adds 4ᵈ 35′ 11″ to the days and the motions of that interval to the other columns. When the days exceed a lunation (29ᵈ 31′ 50″), the conjunction found is the second of ādhār or the first of the next month: a lunation is subtracted from the days, and its motions from the other columns.
- **p. 86**: if A is the first conjunction of ādhār in a year, that of the next year falls at A + 18ᵈ 53′ 52″ if the next year is common, and at A − 1ᵈ + 18ᵈ 53′ 52″ if it is bissextile; a lunation is subtracted as before.
- **p. 86, years 11 and 22**, in a note by Schiaparelli: the codex gives 28ᵈ 9′ 39″, 358° 32′ 6″, 271° 4′ 19″, 211° 11′ 43″ for year 11 and 26ᵈ 19′ 18″, 357° 4′ 18″, 182° 8′ 39″, 62° 23′ 27″ for year 22. An interpolator took these numbers from the Egyptian table of p. 32 and kept the whole days of the Roman table. The Roman table loses a day against the Egyptian one every fourth year, so that a conjunction in thoth of the Egyptian table can fall in subāṭ (February) of the Roman one. In year 11 the Egyptian table gives 11ᵈ 47′ 37″ + 18ᵈ 53′ 52″ = 30ᵈ 41′ 29″, beyond the days of thoth, and a lunation is subtracted (1ᵈ 9′ 39″). The Roman table gives 28ᵈ 41′ 29″ of ādhār, from which nothing is subtracted. The printed rows of years 11 and 22 are the restored ones. The note obtains 28ᵈ 41′ 29″ by adding 17ᵈ 53′ 52″ to the 9ᵈ 47′ 37″ of year 10, «ob sequentem bisextilem», but that sum is 27ᵈ 41′ 29″. The table adds 18ᵈ 53′ 52″ from year 10 to year 11 and puts the step of 17ᵈ 53′ 52″ between years 11 and 12. The interpolator thought that the Roman table should be corrected after the Egyptian one and Ptolemy's; the Spanish version (f. 56,r.) follows the interpolated copy.
- **p. 86, year 6**: Nallino asks that the seconds of the days, printed 40″, be read 50″. Year 6 holds 75 lunations, and 75 lunations less 2191 days are 23ᵈ 47′ 40.4″; the rule of the same note, year 5 (4ᵈ 53′ 49″) plus 18ᵈ 53′ 52″, gives 23ᵈ 47′ 41″. Both support the printed 40″. On p. 207 Nallino corrects the same seconds of the Egyptian table the other way, 40″ for 50″.
- **p. 86, the third column**: its seconds differ by about 2″ from those of p. 32; al-Battānī appears to have computed the column anew, perhaps with a very slightly different daily motion of the elongation.
- **p. 87**: Nallino refers to p. 206 on the similar tables of p. 31. In the third table, which has many errors in the codex (especially in the last column), Schiaparelli reads 52″ for 54″ in the argument of latitude of 72 years (codex 6″); for 288 years, 184° for 189° in the anomaly and 51′ for 56′ in the argument of latitude (codex 18′); 275° 48′ 22″ for 306° 28′ 36″ at 384 years (codex 275° 4′ 10″); and 321° 45′ 17″ for 23° 5′ 45″ at 480 years (codex 291° 0′ 40″). 891 lunations give 327° 27′ 52.0″ for 72 years, and 3563 lunations 184° 55′ 36.1″ for the anomaly of 288 years. This edition prints the table as Nallino's does; the readings are in the ledger.

### Conventions

- The first row of each table carries the marks as printed: an italic superscript «dies» for the days on pp. 84–87, ᵈ for the days of the intervals, and ° ′ ″ for degrees.
- p. 85 has no Arabic head over the years.
- The Arabic title of the intervals, سنون مفردة, follows the Latin in parentheses.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the notes on pp. 31, 86 and 87.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
