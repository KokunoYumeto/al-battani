# S06 — Equations of the five planets (Part II pp. 108–137)

The tables of the planetary equations (codex fol. 208,v.–223,r.), six pages for each planet: Saturn pp. 108–113, Jupiter 114–119, Mars 120–125, Venus 126–131, Mercury 132–137. Each row gives a degree n from 1 to 180 and 360 − n (columns I and II); the five columns of values are:

| Column | Content | Argument |
|---|---|---|
| III. Aequatio anomaliae et centri | the equation of the centre, in degrees and minutes | the centrum |
| IV. Portiones duarum longinquitatum | the sixtieths for the two distances (minutes), marked «Decrescunt» where they fall and «Crescunt» where they rise | the centrum |
| V. Longinquitas maxima | the amount by which the equation of the anomaly at the greatest distance of the centre of the epicycle falls short of that at the mean distance | the anomaly |
| VI. Longinquitas media; aequatio anomaliae | the equation of the anomaly at the mean distance | the anomaly |
| VII. Longinquitas minima | the amount by which the equation of the anomaly at the least distance exceeds that at the mean distance | the anomaly |

Above the first table of each planet a line in Arabic and Latin gives the apogee in the year 1191 of Dhū ’l-qarnayn and the daily motion in anomaly: Saturn 244° 28′ and 0° 57′, Jupiter 164° 28′ and 0° 54′, Mars 126° 58′ and 0° 28′, Venus 82° 14′ (and, in Nallino's brackets, 0° 37′), Mercury 201° 28′ and 3° 6′.

## Read

- [Part II pp. 108–137, 30 pp.](p2_planets.pdf).

## Data

| File | Content |
|---|---|
| `planets_p2.tsv` | One row per printed row: page, planet, row, n and 360 − n, columns III–VII (degrees and minutes; IV in sixtieths), how each number was established (`check`), and notes. |
| `planets_pages.tsv` | Folio lines, the line above the first table of each planet, Arabic and Latin titles, heads, the notes «Decrescunt» and «Crescunt» with the argument over which they stand, and the signatures. |
| `planets_discrepancies.tsv` | The 5 differences found, and the 2 numbers that Nallino emends. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and resolved against its computed curve, then, in a second pass, against the computation corrected by the running median of the readings on which both readers agree. Of the 9,000 numbers, 7,481 are in class A (both readers give the value) and 1,327 in class B (one reader gives it). Tesseract re-read every B cell as a third reader; the 458 cells where it gave another number were read by eye, and six resolutions were corrected. 192 numbers are in class E: the curves flagged the cell and it was read by eye.

`python check_planets.py` compares the tables with the computation from the elements that Nallino gives (Part II pp. 239–244), in parts of which the radius of the deferent has 60:

| Planet | Eccentricity of the equant | Radius of the epicycle |
|---|---|---|
| Saturn | 6;50 | 6;30 |
| Jupiter | 5;30 | 11;30 |
| Mars | 12 | 39;30 |
| Venus | 2;30 | 43;10 |
| Mercury | 3 (the distance of the equant from the Earth) | 22;30 |

- **III**: sin q = 2e sin n / d, where d is the distance of the centre of the epicycle from the Earth for the centrum n (for Mercury, e sin n / d, with the circlet that carries the centre of its deferent). For Venus the column follows al-Battānī's solar eccentricity, 2;4,45 for the equant: its greatest value, 1° 59′, is the Sun's greatest equation. With Ptolemy's 2;30 it would be 2° 23′.
- **V, VI, VII**: tan p = r sin n / (D + r cos n) at the mean distance D = 60 (VI), less that at the greatest distance (V) and more that at the least (VII). For Venus the distances are Ptolemy's, 61;15 and 58;45: columns V and VII agree with them within 2.8′, and depart from the distances of al-Battānī's eccentricity by up to 20′.
- **IV**: for the outer planets and Venus the sixtieths follow 60 |cos n| within 3. For Mercury they follow, roughly, the excess of the distance of the centre of the epicycle over 60 in its greatest excess (69 − 60) and its defect in the greatest defect (60 − 55;34); between 67° and 95° they stand up to 5.8 above this. Mercury's printed sixtieths fall to 1 at 64°–65°, rise to 60 at 113°–123° and fall to 40 at 180°.

| Planet | III | IV | V | VI | VII |
|---|---|---|---|---|---|
| Saturn | 2.6′ (173) | 3.0 (158) | 1.2′ (180) | 1.9′ (180) | 3.4′ (135) |
| Jupiter | 2.2′ (179) | 2.4 (170) | 1.4′ (180) | 2.4′ (179) | 1.4′ (180) |
| Mars | 1.8′ (180) | 3.0 (175) | 3.8′ (151) | 62.0′ (165) | 5.6′ (167) |
| Venus | 1.7′ (180) | 2.0 (180) | 2.8′ (176) | 3.9′ (173) | 2.5′ (178) |
| Mercury | 2.1′ (179) | 5.8 (129) | 2.3′ (178) | 1.7′ (180) | 1.9′ (180) |

The table gives the largest departure from the computation in each column, and in brackets how many of its 180 values lie within 2′ (for IV, within 2). The arguments are n and 360 − n in every row. A value more than 3′ off its computation is listed when it, or a value of its run (consecutive values off in the same direction), is more than 4′ off (for Mercury's sixtieths, 6). A single value is also listed when it departs from the mean of its two neighbours by 2′ more than the computation does. 4,497 values satisfy these checks. Five differences are ledgered, and 0 are open:

- **Jupiter, 121°, III**: 4° 35′, the same as at 122°; the stretch runs 4° 40′, 4° 35′, 4° 35′, 4° 32′, 4° 29′ from 120° to 124°, about 1.3′ above the computation, which gives 4° 36.3′ at 121°. The 5 is printed damaged.
- **Mars, 164° and 165°, VI**: 25° 16′ and 24° 3′, each a degree and 2′ below the computation (26° 18′ and 25° 5′); the values of 163°, 166° and 167° lie within 3′ of it.
- **Mars, 169°, VI**: 19° 0′ for 19° 33′; the values of 168° and 170° lie within 3′ of the computation.
- **Mars, 159°–162°, VII**: 8° 3′, 8° 2′, 8° 0′, 7° 59′, 3′ to 6′ below the computation; the steps of the printed column are regular.
- **The line above the table of Venus**: the Arabic gives the apogee as قب يد, 102° 14′ in abjad, where the Latin has 82° 14′ (فب يد). Al-Battānī gives Venus the Sun's apogee (Schiaparelli, t. I, p. 242), 82° 17′ in his elements.

The other lines above the tables agree with their Latin: the year اقضا (1191; the leading alif counts the thousand), Saturn رمد كح and {0} نز, Jupiter قصد كح and {0} ند, Mars قكو نح and {0} كح, Mercury را كح and ج و. The daily motions in anomaly are those of the tables of mean motions (pp. 27 and 22): the Sun's 0° 59′ 8″ less 2′, 5′ and 31′ for the outer planets, and 0° 37′ and 3° 6′ for Venus and Mercury.

## Nallino's notes on these pages (Part II, pp. 238–245)

- The tables are mentioned in chapters XXXI and XLV (t. I, pp. 64 and 113–114). They rest on Ptolemy's tables in Almagest XI 11, «ἔκθεσις κανόνων τῆς κατὰ μῆκος τῶν ε′ πλανωμένων διευκρινήσεως» («exposition of the tables of the correction of the five planets in longitude»). Ptolemy gives the argument by 6° in the first and last quadrants and by 3° in the second and third; al-Battānī gives every degree, taking Ptolemy's values and interpolating the rest. He chose apter column heads.
- Al-Battānī merged into one Ptolemy's two columns of the «prosthaphaeresis of longitude» and the «difference of addition» (or «of subtraction»): his column III is the algebraic sum of Ptolemy's III and IV. His IV is Ptolemy's VIII; V, VI and VII are the same in both. Ḥabash's tables (f. 42,r.–44,v., 46,r.–48,v., 50,r.–52,v., 54,r.–56,v., 58,r.–60,v.) are built the same way.
- Two errors of the codex are to be corrected: in column III, the last line of p. 116 and the first of p. 117, 5° 15′ (يه) for 5° 14′ (يد). This edition prints them as Nallino's table does; his reading is in the ledger. In Halma's Almagest the equation of the anomaly of Venus at 174° is wrongly 14° 41′ for 14° 47′; this table has 14° 47′.
- Nallino explains Ptolemy's model of the planets (the deferent, the equant and the epicycle; for Mercury the circlet that carries the centre of the deferent) and derives the formulas used above for the equation of the centre, the distance of the centre of the epicycle and the equation of the anomaly. Ptolemy computes the equations of the anomaly at the mean distance (VI) and their changes at the greatest and least distances (V, VII), and the sixtieths (IV) for the greatest equations, those at the tangent from the Earth to the epicycle; the corrections at the other points of the epicycle keep sensibly the same proportion (Almagest XI 10).
- The elements are those of the Almagest; the Canopus inscription (the tenth year of Antoninus) has the same. In the later *Hypotheses* the radius of the epicycle of Mercury is 22;15 and the eccentricity of the equant of Saturn 6;40.

## Conventions

- The first row of each page carries the marks as printed: ° for the arguments, ° ′ in columns III, V, VI and VII, and ′ for the sixtieths.
- The notes «Decrescunt» and «Crescunt» stand over the sixtieths where they begin: «Decrescunt» at 1°, 31° and 61° on every planet; «Crescunt» at 88° (Saturn, Mars) or 89° (Jupiter, Venus) and at 91°, 121° and 151°; for Mercury «Crescunt» at 65° and 91° and «Decrescunt» again at 121° and 151°.
- Only p. 108 has the Arabic heads; the other pages have the Latin heads. The titles begin ابتداء جداول / Initium tabularum on the first page of a planet, من جداول / Ex tabulis on the following pages and تمام جداول / Finis tabularum on the last; the Latin titles of the first pages of Saturn and Venus read «semper compositae cum tribus longinquitatibus eius», the others «semper cum tribus eius longinquitatibus compositae». The Venus pages have بابعادها, the others بابعاده. The title of p. 116 ends with a comma, as printed.
- Damaged print: the «با» of بابعاده in the title of p. 112; the 0 of 0° 6′ in the first row of p. 108 (column VI); the 5 of 4° 35′ (Jupiter, 121°, III); the 4 of 24 (Mars, 114°, IV); the 8 of 1° 38′ (Venus, 126°, III); the 6 of 56 (Venus, 158°, IV).
- pp. 113, 121, 129 and 137 carry the signatures 15, 16, 17 and 18 at the foot.

## Credits

- al-Battānī: the tables (after Ptolemy).
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the note on Venus (t. I, p. 242).
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
