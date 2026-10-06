# S06 — Tables for computing eclipses (Part II pp. 88–91)

The tables of al-Battānī's chapters on eclipses (codex fol. 194,v.–196,r.).

| Page | Table | Rows |
|---|---|---|
| 88 | the true hourly motions of the Sun and the Moon at the syzygies, for the anomaly 0°, 6° … 180° (and 360° less it); a small table of increments for 1°–7° of mean elongation; the limits of solar and lunar eclipses, in Arabic and Latin | 31, 7 |
| 89 | the table of correction (6° … 180°): the portions of the distance of the Moon, and the corrections for the epicycle and the eccentre; the table of digits: the eclipsed area of the solar and the lunar disc for 1–12 digits of the diameter, and the inclinations at the beginning and end of a solar eclipse and of the immersion and emersion of a lunar one, for 0–21 digits | 30, 12, 23 |
| 90 | lunar eclipses at the greatest and the least distance: true latitude of the Moon, arc of incidence, half duration of totality, digits of the lunar diameter eclipsed; under each table the interval of the latitudes | 23, 23 |
| 91 | solar eclipses at the greatest and the least distance of the Moon: apparent latitude, digits of the solar diameter eclipsed, arc of incidence; under each table the interval of the latitudes | 13, 14 |

## Read

- [Part II pp. 88–91, 4 pp.](p2_eclipses.pdf).

## Data

| File | Content |
|---|---|
| `motions_p2.tsv` | p. 88: the anomaly n and 360 − n, and the hourly motions of the Sun and the Moon in minutes and seconds; the increments (degrees of elongation; minutes and seconds). |
| `correction_p2.tsv` | p. 89: n and 360 − n, the portions (minutes, seconds), and the corrections for the epicycle and the eccentre (minutes). |
| `digits_p2.tsv` | p. 89: the areas (digits 1–12; the Sun and the Moon in digits and minutes of a digit) and the inclinations (digits 0–21 and «compl.»; degrees). |
| `eclipses_p2.tsv` | pp. 90–91: the four tables, latitude, incidence and (for the Moon) half duration in minutes and seconds; the digits of the last row as printed («21 31 30» for 21ᵈ 31′ 30″). |
| `ecl_pages.tsv` | Folio lines, Arabic and Latin titles and heads, the lines under the tables of pp. 90–91, and the signature on p. 89. |
| `ecl_text.tsv` | The eclipse limits of p. 88, in Arabic and in Latin. |
| `ecl_discrepancies.tsv` | The 15 differences found, and the 3 numbers that Nallino emends in his notes. |

Every data row records how each number was established (`check`) and notes (`doubt`).

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and resolved against its computed curve: 815 numbers in class A (both readers give the value), 46 in class B (one reader gives it, and for 11 of them only the glyph reader saw the number; each confirmed by Tesseract as a third reader or read by eye), and 38 in class E (read by eye: the marks of the first rows, the last rows of pp. 90–91, and the cells that depart from the computation). Where a column departs from its computation by more than the reading tolerance (the portions, the areas, the inclinations), the value on which both readers agree was taken as its curve.

`python check_eclipses.py` recomputes every column with the elements that the tables themselves use:

- **p. 88, hourly motions**: the Sun's mean hourly motion (0.98565176° / 24) times 1 − q′(n), and the Moon's (13.17639871° / 24) less q′(n) times the hourly motion in anomaly (13.06498287° / 24), where q is the equation of the eccentre (2;4,45) or of the epicycle (5;15). All 62 values lie within 1.4″. The increments are n″ for n degrees.
- **p. 89, correction**: the portions are 60′ times the fraction of the change of the Moon's distance between the apogee and the perigee of the epicycle (5;15, at the apogee of the eccentre); the values at odd multiples of 6° are the means of their neighbours. The epicycle column is 12 times the same fraction, and the eccentre column 32 times the fraction of the change of the distance of the centre of the epicycle (eccentricity 10;19) at the double elongation; both lie within 0.7′.
- **p. 89, areas**: the part of the disc covered when d twelfths of its diameter are covered, by a disc of the same size (the Sun) or by the shadow of 2 3/5 lunar radii (the Moon). The printed values are multiples of 5′.
- **p. 89, inclinations**: sin i = 1 − d / D, with D = 12.4 digits for the Sun (a lunar radius about 1.07 times the solar) and 21.6 for the Moon (the shadow of 2 3/5 lunar radii); at the end of the immersion sin i = (3.6 − d / 6) / 1.6. All 69 values lie within 0.7°.
- **p. 90**: the latitude falls from the sum of the radii of the shadow and the Moon, S = 53′ at the greatest distance and 63′ 36″ at the least, by a twelfth of the lunar diameter a digit (29′ 30″ and 35′ 20″; these and the radius of the shadow follow from the first row and from 12 digits, where the eclipse becomes total). The incidence is √(S² − b²), less the half duration √((r_u − r_m)² − b²) once the eclipse is total.
- **p. 91**: the latitude falls from S = 31′ (34′ at the least distance) by a twelfth of the solar diameter, 32′ 30″, a digit; the incidence is √(S² − b²).
- **The texts**: the limits of p. 88 agree with those of p. 32, and their Arabic numbers (Maghribi abjad) with the Latin; the Arabic lines under pp. 90–91 agree with the Latin.

427 values lie within the tolerance of their columns (2″–3″ for the motions, latitudes, incidences and durations; 5″ for the portions at multiples of 12°; 5′ for the areas; 1 unit for the whole minutes and degrees). Fifteen differences are ledgered, and 0 are open:

- **Portions** at 12° and 24° (0′ 42″ and 2′ 42″, computed 0′ 36″ and 2′ 24″) and at 132° (49′ 30″, computed 49′ 18″); the means at 6°, 30°, 126° and 138° follow the printed values, and at 18° Nallino reads the mean, 1′ 42″, for the printed 1′ 22″. The other multiples of 12° lie within 4.8″.
- **Areas**: the Sun at 9–11 digits (8ᵈ 20′, 9ᵈ 40′, 10ᵈ 50′, computed 8ᵈ 13′, 9ᵈ 28′, 10ᵈ 44′); the Moon at 1 digit (0ᵈ 30′, computed 0ᵈ 25′) and at 9–10 digits (9ᵈ 10′ and 10ᵈ 20′, computed 9ᵈ 17′ and 10ᵈ 26′).
- **Lunar eclipses at the greatest distance**: the incidences of 3, 4 and 5 digits (26′ 7″, 29′ 45″, 33′ 16″; computed 26′ 58″, 30′ 45″, 33′ 56″), of 12 digits (47′ 7″, computed 47′ 30″) and of 14 digits (35′ 19″, computed 35′ 15″). The digits of the last row, 21ᵈ 31′ 30″: 12 × 53′ / 29′ 30″ is 21ᵈ 33′ 34″.
- **Lunar eclipses at the least distance**: the half durations of 19, 20 and 21 digits and of the last row (27′ 42″, 28′ 12″, 28′ 53″, 28′ 56″) against 27′ 13″, 27′ 52″, 28′ 13″ and 28′ 16″. At latitude 0 the half duration is r_u − r_m, which the latitude column gives as 28′ 16″ at 12 digits; the incidence of that row is 2 r_m, 35′ 20″, as printed. The last two values exceed the computation by 40″; in Maghribi abjad 13 is يج and 53 نج, 16 يو and 56 نو. The interval under the table, 0° 2′ 56″ 30‴, also in the Arabic line: the latitudes fall by 2′ 56″ 40‴ a digit, from 63′ 36″ to 1′ 46″ in 21 digits.
- **Solar eclipses**: the incidences of 5 and 10 digits at the greatest distance (25′ 47″ and 30′ 49″, computed 25′ 37″ and 30′ 45″) and of 4 digits at the least (24′ 50″, computed 24′ 53″). The digits of the last row at the greatest distance, 11ᵈ 23′ 30″: 12 × 31′ / 32′ 30″ is 11ᵈ 26′ 46″. At the least distance the last row, 12ᵈ 33′, agrees (12ᵈ 33′ 14″).

The tables of the least distance differ in one parameter: the solar table takes 34′ for the sum of the radii, a lunar radius of 17′ 45″, where the lunar table takes 17′ 40″ (a diameter of 35′ 20″).

## Nallino's notes on these pages (Part II, pp. 231–232)

- **p. 88, the hourly motions**: mentioned in chapter XLII (t. I, p. 94); the table is not in Ptolemy. The small table on the right is mentioned in t. I, pp. 94 and 150; Schiaparelli explains it in t. I, p. 273, note a.
- **p. 88, the solar eclipse limits**: to be read 159° 44′–190° 56′, 0°–20° 16′ and 349° 4′–360°, as on p. 32 (Nallino's note on p. 209). This edition prints them as Nallino's text does; his reading is in the ledger. The Arabic text has the same numbers as the Latin.
- **p. 89, the table of correction**: mentioned in chapters XXXIX, XLI, XLIII and XLIV. It is Ptolemy's table of correction (Almagest VI 8), which gives only the sixtieths of the differences; Theon's Handy Tables have all its columns. At 18° Nallino reads 1′ 42″ for 1′ 22″. The portions are proportional parts of the change of the diameter of the Moon (or the Sun) between the apogee and the perigee, for the diameter at the corrected anomaly of the Moon; with the anomaly of the Sun as argument they serve for the change of the solar parallax (t. I, p. 80). The two other columns, which the scribe of the codex ran together into one, give the correction of the lunar parallax in latitude and longitude for the epicycle (argument: the corrected anomaly of the Moon) and for the eccentre (argument: twice the mean elongation). All the columns stand in the Alphonsine Tables under the title «Tabula aequationis diversitatis aspectus sive tabula Attacium», where «attacium» is *at-taqwīm*, al-Battānī's name for this correction.
- **p. 89, the digits eclipsed**: the three columns are mentioned in chapters XLIII and XLIV and stand in Ptolemy (Almagest VI 8) and in Theon. In the third column, at 3 digits, Ptolemy has 2 1/15 (2ᵈ 4′) and Theon 2 1/5; at 9 digits Nallino notes a wrong reading in Halma's edition of Ptolemy, 9ᵈ 10′ for 9ᵈ ½ (al-Battānī's table has 9ᵈ 10′).
- **p. 89, the inclinations**: mentioned in chapters XLIII and XLIV; the tables stand also in Ptolemy (Almagest VI 11) and in Theon, with whose help Nallino corrected small errors of the codex. The numbers follow sin i = R · (latitude of the Moon) / (radius of the Sun + radius of the Moon) in solar eclipses, and / (radius of the shadow ± radius of the Moon) in lunar ones; the argument is the digits eclipsed.
- **p. 90**: Ptolemy (Almagest VI 7) has similar tables, but with the Moon's true distance from the northern limit as argument (intervals of 30′ at the greatest distance and 34′ at the least), and all his numbers differ. Theon, like al-Battānī, takes the true latitude of the Moon; he also calls the half duration «mora», but omits the seconds and computes more roughly.
- **p. 91**: the argument is the apparent latitude of the Moon (the true latitude ± the parallax), as in Theon; Ptolemy takes the apparent distance from the northern limit, with intervals of 30′, and his other numbers differ.

## Conventions

- The first row of each table carries its marks as printed: ′ ″ for minutes and seconds, ° for degrees, an italic superscript «dig.» for the digits on p. 89, and ᵈ ′ ″ in the last rows of pp. 90–91.
- On p. 89 the left part of the table of digits (1–12) stands on every other line of the right part (0–21 and «compl.»), as printed.
- The ᵈ of 12ᵈ 33′ (p. 91) is printed damaged.
- The Arabic numbers of the texts are in Maghribi abjad (ص 60, ض 90, س 300), with the codex's zero sign.
- The kashīdas that stretch Arabic words in the print are not reproduced.
- p. 89 carries the signature 12 at the foot.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
