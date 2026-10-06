# S06 — Parallaxes (Part II pp. 93–101)

The tables of parallax, codex fol. 197,v.–205,r.: Ptolemy's tables of parallax in altitude (pp. 93–94), and the parallaxes of the Moon in longitude and latitude in the seven climes (pp. 95–101).

## Read

- [Part II pp. 93–101, 9 pp.](p2_parallax.pdf).

## Data

| File | Content |
|---|---|
| `parallax_p2.tsv` | pp. 93–94, one row per printed row: page, row, z, the eight columns (minutes and seconds; the third term in degrees, minutes and seconds), how each number was established (`check`), and notes. |
| `par_pages.tsv` | pp. 93–94: folio lines, Arabic and Latin titles and heads. |
| `par_discrepancies.tsv` | pp. 93–94: the 5 differences found. |
| `clime_p2.tsv` | pp. 95–101, one row per printed row: page, folio, sign, row, the line of the print within its half, the hour as printed, the parallax in longitude and in latitude (minutes), «+» where the latitude is northern, the mark «bor.» or «austr.» over the value, `check`, notes. |
| `clime_pages.tsv` | pp. 95–101: folio lines, titles and heads of each half, its number of lines, and the lines before which the print leaves a wider space. |
| `clime_discrepancies.tsv` | pp. 95–101: the 4 numbers that Nallino emends. |

## Parallaxes in altitude (pp. 93–94)

Ptolemy's tables (Almagest V 18). The argument is the true zenith distance z, by 2° from 2° to 90°.

| Column | Content |
|---|---|
| Parallaxis Solis | the Sun's parallax (minutes, seconds) |
| Primus terminus | the Moon's parallax at the first of Ptolemy's four distances |
| Secundus terminus [Differentia] | the parallax at the second distance less that at the first |
| Tertius terminus | the parallax at the third distance (degrees, minutes, seconds) |
| Quartus terminus [Differentia] | the parallax at the fourth distance less that at the third |
| [In apogeo] epicycli, [In perigeo] epicycli | sixtieths for the distance of the Moon on the epicycle, its centre at the apogee or at the perigee of the eccentre (argument: half the true anomaly) |
| In excentrico | sixtieths for the distance of the centre of the epicycle on the eccentre (argument: the mean elongation) |

### How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and resolved against its computed curve, or, where a column departs from its computation by more than the reading tolerance (the third and fourth terms, the sixtieths), against the value on which both readers agree: 679 numbers in class A, 32 in class B (each confirmed by Tesseract as a third reader or read by eye), and 54 in class E (read by eye).

`python check_parallax.py` checks the columns with the elements Nallino gives (Part II pp. 235–237):

- **The Sun, the first term, the second less the first**: tan p = sin π sin z / (1 − sin π cos z), with sin π the Earth's radius over the distance (the Sun 1210 radii; the Moon 64;10 and 53;50). All 135 values lie within 2.1″.
- **The third term and the fourth less the third**: at 90° they are the horizontal parallaxes 79′ and 104′ less 79′. Below, they grow by steps that never increase from one row to the next: 165″ from 2° to 10°, then 160″, 150″, 140″ … for the third term (from 2′ 40″ at 2°); 50″ to 32°, then 40″, 30″ … for the difference. They stand below the computation with 79′ and 104′ by up to 62.6″ and 44.1″.
- **The sixtieths** are computed at every 6° of the argument and divided in thirds between; the values between lie within 1″ of the thirds. The values at multiples of 6° lie within 5″ of the computation (60 times the change of the distance: an epicycle of 5;15 about a centre at 60 or at 39;22, and an eccentricity of 10;19). In the column for the epicycle at the apogee, the values at 6°, 12° and 66° stand 6″, 18″ and 12″ above the computation and agree with their neighbours. They equal the portions of the table of correction on p. 89 at twice the argument; that table has the same values throughout ([S06/eclipses](../eclipses/README.md)).

351 values satisfy their checks. Five differences are ledgered, and 0 are open; each is a single value that the column's own steps or thirds contradict:

- **Epicycle at the apogee, 48°**: 31′ 43″ for 31′ 48″, which both neighbouring stretches give (steps of 124″) and which p. 89 has at 96°.
- **Epicycle at the perigee, 50°**: 33′ 11″ for 33′ 14″, a third of the way from 48° to 54°.
- **Epicycle at the perigee, 78°**: 56′ 3″ for 57′ 3″, which both neighbouring stretches give (steps of 71″ and 44″).
- **Eccentre, 56°**: 43′ 39″ for 43′ 49″, a third of the way from 54° to 60°.
- **Eccentre, 72°**: 55′ 41″ for 55′ 21″, which both neighbouring stretches give (steps of 72″ and 51″) and the computation gives exactly.

### Nallino's notes on these pages (Part II, pp. 235–237)

- The tables are treated in chapter XXXIX (t. I, pp. 79–80).
- **The Sun**: the column is taken from the Almagest (V 18), as al-Battānī says; since he takes a different distance of the Sun, he tells the reader to add an eighteenth to every number of the table (t. I, pp. 257–258, and p. xxxviii, note 3). The argument is the true (geocentric) zenith distance. Ptolemy computed as if the sine of the parallax were its tangent, which in such small angles makes no sensible error, and neglected the changes of the Sun's distance.
- **The Moon**: the columns are taken from the Almagest, but in the third and fourth terms al-Battānī somewhat emended Ptolemy's cruder numbers. The argument is the true zenith distance of the Moon. Ptolemy (Almagest V 17) puts the distance of the centre of the epicycle at 59 Earth radii at the apogee and 38;43 at the perigee, and the radius of the epicycle at 5;10, so that the four terms are 64;10 (the Moon at the apogee of the eccentre and of the epicycle), 53;50 (apogee of the eccentre, perigee of the epicycle), 43;53 (perigee of the eccentre, apogee of the epicycle) and 33;33 (perigee of both). The horizontal parallaxes are 53′ 34.7″, 63′ 51.8″, 78′ 20.7″ and 102′ 28.9″; Ptolemy has 53′ 34″, 63′ 51″, 79′ 0″ and 104′ 0″.
- **The sixtieths**: with the centre of the epicycle at the apogee of the eccentre and a true anomaly of 60°, the Moon's distance is 62;48 in parts of which the first term is 65;15 and the second 54;45, so 2;27 below the first of a difference of 10;30: 14′. Ptolemy enters these columns with half the true anomaly, so the 14′ stand under 30°. For the eccentre, a double mean elongation of 60° puts the centre of the epicycle at 54;3 of the distances 60 and 39;22, 5;57 of their difference 20;38: 17′ 18″, under 30°, the simple mean elongation.
- **The use of the tables**: enter with the true zenith distance and take the parallaxes of the first and third terms with the differences beside them; multiply the differences by the sixtieths of the epicycle columns, entered with half the corrected anomaly, and add the products to the parallaxes; then multiply the difference of the two results by the sixtieths of the eccentre, entered with the mean elongation, and add the product to the smaller of them.

### Conventions

- The first row of each page carries the marks as printed: ′ ″ in every column, and ° ′ ″ for the third term.
- p. 94 has the Latin heads only. Its Arabic title has «بطاميوس» for «بطلميوس», as printed.

## Parallaxes in longitude and latitude in the seven climes (pp. 95–101)

One page for each clime, in two halves with their own folio lines: Cancer to Sagittarius above, Capricorn to Gemini below. For each sign the table gives the hours before and after the culmination of the beginning of the sign, the first and last rows holding the half-day arc, and the parallax of the Moon in longitude and in latitude, in minutes.

| Page | Clime | Latitude (title) | Longest day |
|---|---|---|---|
| 95 | I | 16° 32′ | 13ʰ |
| 96 | II | 24° | 13ʰ 30ᵐ |
| 97 | III | 30° 40′ | 14ʰ |
| 98 | IV | 36° 22′ | 14ʰ 30ᵐ |
| 99 | V | 41° 15′ | 15ʰ |
| 100 | VI | 45° 22′ | 15ʰ 30ᵐ |
| 101 | VII | 48° 13′ | 16ʰ |

### How the tables were read and checked

Each sign column was read by the glyph reader and by the OCR text layer. The glyph reader takes Nallino's «+» for a digit, so a «+» was looked for twice: in the text layer, and in the image (a sign whose middle row is inked across its width, followed by the digits). A value was taken where both readers give the same digits and both tests agree on the «+». Otherwise the value printed in the mirror table decided between the two readings, and each value so taken was also read by eye. The rest were read by eye. Of the 1,158 rows (longitude, latitude and its direction), 1,000 are in class A (both readers agree), 127 in class M (one reader and the mirror table, checked by eye), and 31 in class E (read by eye). In one row both readers gave 43 where the print has 45 (p. 95, Aries, the 4th hour after culmination); the mirror table showed it. The marks «bor.» and «austr.» were found in the text layer (93) and by eye (3).

`python check_climes.py` checks:

- **The mirror tables**: each table prints the values of the sign placed symmetrically to it about the meridian of the solstices, backwards in time: Leo and Gemini, Virgo and Taurus, Libra and Aries, Scorpio and Pisces, Sagittarius and Aquarius; Cancer and Capricorn each with themselves. Of the 586 pairs of rows, 585 agree; the other is Nallino's emendation on p. 97 (below).
- **The hours**: the half-day arcs of signs of opposite declination add up to 12ʰ (within 1 minute; 7ʰ 16′ and 4ʰ 45′ in the fifth clime are both rounded up); Libra and Aries have 6ʰ; the longest day of the title is twice the half-day of Cancer. Every half-day agrees with the computation for the latitude at which the longest day of the title holds, with the obliquity 23° 35′, within 1 minute (in the first clime within 3: its arcs are rounded to 5 minutes).
- **The latitudes of the titles** against those at which the longest days hold: they agree in climes III–VI; those of climes I, II and VII are Nallino's emendations (below).

701 checks pass, and the only differences are the four numbers that Nallino emends.

### Nallino's notes on these pages (Part II, p. 237)

- The tables are mentioned in chapters XL and XLIV (t. I, pp. 84, 105, 110), and their use is taught in chapter XXXIX (t. I, pp. 82–84). As al-Battānī himself says (t. I, p. 82), they are taken from Theon's Handy Tables and do not always serve for exact computations. In the titles he changed Theon's latitudes of the climes, computed for the obliquity 23° 51′ 20″, as his obliquity of 23° 35′ required.
- Where the version has «culm.», the codex has only a line across the page, marked at one end خط الزوال («linea meridiei») and at the other خط نصف النهار («linea meridiani»); Nallino translated «culminationem» on Schiaparelli's advice, since these lines concern the passage of the first point of Cancer, of Leo etc. through the meridian. To show which parallaxes in latitude are positive, he prefixed «+» to them; the codex has only the marks «austr.» and «bor.». When the parallaxes in longitude are added and when subtracted follows from t. I, pp. 84 and 262–263: at the culmination of a sign they are positive from Cancer to Capricorn, negative from Capricorn to Cancer, and nil in Cancer and Capricorn.
- The faulty numbers of the codex were easy to correct, since in each clime every parallax is given twice; the comparison with Theon made the corrections more certain. Theon's tables are full of misprints in Halma's edition, and more in its French version.
- He kept the latitudes of the climes in the titles as the codex has them, wrongly, and reads: p. 95, 16° 39′ (لط) for 16° 32′ (لب), precisely 16° 38′ 48″; p. 96, 24° 5′ (ه) for 24° (the zero sign of the minutes omitted), precisely 24° 4′ 47″; p. 101, 48° 53′ (نج) for 48° 13′ (يج), precisely 48° 52′ 46″. The check gives 16° 38.8′, 24° 4.8′ and 48° 52.6′. The first two errors also stand in the codex in the tables of p. 65, where he corrected them in the version.
- p. 97, at the second hour of Cancer after culmination: 22′ for 21′ in the longitude; the second hour before culmination has 22′.

### Conventions

- The rows stand on the lines of the print: in each half, the rows of the shorter columns leave blank the lines next to the culmination, and on p. 95 the wider spaces between groups of rows are kept.
- The marks «bor.» and «austr.» stand over the first value of a column and wherever the direction of the latitude changes, as printed.
- The first row of each column carries the marks of the units (ʰ for the hours, ′ for the minutes of the parallaxes). An integer half-day has ʰ only in the first row.
- p. 95 has Arabic heads over the hours and over the first parallax; the other pages have Latin heads. The pages read «Hor. Geminorum.», p. 95 «Horae Geminorum.»; pp. 98–99 have «Tabula» for «Tabulae» in the title.

## Credits

- al-Battānī: the tables (after Ptolemy and Theon).
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the rendering «culm.».
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
