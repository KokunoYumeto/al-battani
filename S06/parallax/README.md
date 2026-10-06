# S06 — Parallaxes of the Sun and the Moon (Part II pp. 93–94)

Ptolemy's tables of parallax in altitude (Almagest V 18), codex fol. 197,v.–198,r. The argument is the true zenith distance z, by 2° from 2° to 90°.

| Column | Content |
|---|---|
| Parallaxis Solis | the Sun's parallax (minutes, seconds) |
| Primus terminus | the Moon's parallax at the first of Ptolemy's four distances |
| Secundus terminus [Differentia] | the parallax at the second distance less that at the first |
| Tertius terminus | the parallax at the third distance (degrees, minutes, seconds) |
| Quartus terminus [Differentia] | the parallax at the fourth distance less that at the third |
| [In apogeo] epicycli, [In perigeo] epicycli | sixtieths for the distance of the Moon on the epicycle, its centre at the apogee or at the perigee of the eccentre (argument: half the true anomaly) |
| In excentrico | sixtieths for the distance of the centre of the epicycle on the eccentre (argument: the mean elongation) |

## Read

- [Part II pp. 93–94, 2 pp.](p2_parallax.pdf).

## Data

| File | Content |
|---|---|
| `parallax_p2.tsv` | One row per printed row: page, row, z, the eight columns (minutes and seconds; the third term in degrees, minutes and seconds), how each number was established (`check`), and notes. |
| `par_pages.tsv` | Folio lines, Arabic and Latin titles and heads. |
| `par_discrepancies.tsv` | The 5 differences found. |

## How the tables were read and checked

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

## Nallino's notes on these pages (Part II, pp. 235–237)

- The tables are treated in chapter XXXIX (t. I, pp. 79–80).
- **The Sun**: the column is taken from the Almagest (V 18), as al-Battānī says; since he takes a different distance of the Sun, he tells the reader to add an eighteenth to every number of the table (t. I, pp. 257–258, and p. xxxviii, note 3). The argument is the true (geocentric) zenith distance. Ptolemy computed as if the sine of the parallax were its tangent, which in such small angles makes no sensible error, and neglected the changes of the Sun's distance.
- **The Moon**: the columns are taken from the Almagest, but in the third and fourth terms al-Battānī somewhat emended Ptolemy's cruder numbers. The argument is the true zenith distance of the Moon. Ptolemy (Almagest V 17) puts the distance of the centre of the epicycle at 59 Earth radii at the apogee and 38;43 at the perigee, and the radius of the epicycle at 5;10, so that the four terms are 64;10 (the Moon at the apogee of the eccentre and of the epicycle), 53;50 (apogee of the eccentre, perigee of the epicycle), 43;53 (perigee of the eccentre, apogee of the epicycle) and 33;33 (perigee of both). The horizontal parallaxes are 53′ 34.7″, 63′ 51.8″, 78′ 20.7″ and 102′ 28.9″; Ptolemy has 53′ 34″, 63′ 51″, 79′ 0″ and 104′ 0″.
- **The sixtieths**: with the centre of the epicycle at the apogee of the eccentre and a true anomaly of 60°, the Moon's distance is 62;48 in parts of which the first term is 65;15 and the second 54;45, so 2;27 below the first of a difference of 10;30: 14′. Ptolemy enters these columns with half the true anomaly, so the 14′ stand under 30°. For the eccentre, a double mean elongation of 60° puts the centre of the epicycle at 54;3 of the distances 60 and 39;22, 5;57 of their difference 20;38: 17′ 18″, under 30°, the simple mean elongation.
- **The use of the tables**: enter with the true zenith distance and take the parallaxes of the first and third terms with the differences beside them; multiply the differences by the sixtieths of the epicycle columns, entered with half the corrected anomaly, and add the products to the parallaxes; then multiply the difference of the two results by the sixtieths of the eccentre, entered with the mean elongation, and add the product to the smaller of them.

## Conventions

- The first row of each page carries the marks as printed: ′ ″ in every column, and ° ′ ″ for the third term.
- p. 94 has the Latin heads only. Its Arabic title has «بطاميوس» for «بطلميوس», as printed.

## Credits

- al-Battānī: the tables (after Ptolemy).
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
