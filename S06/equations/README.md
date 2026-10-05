# S06 — Equations of the Sun and the Moon, and the latitude of the Moon (Part II pp. 78–83)

The tables of the equations (codex fol. 189,v.–192,r.). Each row gives a degree n of the argument, from 1 to 180, together with 360 − n, the «ordo inversus», which has the same values. The columns are:

| Column | Content | Argument |
|---|---|---|
| Aequatio Solis | the equation of the Sun, in degrees, minutes and seconds | the mean anomaly of the Sun |
| Aequatio simplex Lunae | the simple equation of the Moon (the equation of the epicycle at the apogee of the eccentre) | the corrected anomaly of the Moon |
| Aequatio anomaliae | the correction of the anomaly (Ptolemy's prosneusis), in degrees and minutes | the double elongation |
| Portiones longinquitatis, Minuta addenda | the sixtieths of the increment to be added at intermediate distances | the double elongation |
| In longinquitate minima | the increment of the equation when the epicycle is at the perigee of the eccentre, in degrees and minutes | the corrected anomaly |
| Latitudo Lunae | the latitude of the Moon, in degrees, minutes and seconds | the argument of latitude |

## Read

- [Part II pp. 78–83, 6 pp.](p2_equations.pdf).

## Data

| File | Content |
|---|---|
| `equations_p2.tsv` | One row per printed row: page, row, n and 360 − n, the six columns (degrees, minutes and seconds as printed), how each number was established (`check`), and notes. |
| `equations_pages.tsv` | Folio lines, Arabic and Latin titles and heads. |
| `equations_discrepancies.tsv` | The departures from the computation, with all their printed and computed values, and the three cells that Nallino emends. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer. Each cell was resolved against a curve: the computation from al-Battānī's elements, corrected by the running median of the readings on which both readers agree. 2,550 numbers are in class A (both readers give the value). 127 are in class B (one reader gives it), each confirmed by Tesseract as a third reader or read by eye. 203 are in class E: the curve flagged the cell, and the whole group was read by eye.

`python check_equations.py` compares the table with the computation from al-Battānī's elements (Nallino, Part II pp. 223–227). These are: the solar eccentricity 2;4,45 and the lunar epicycle 5;15, in parts of which the radius has 60; the eccentricity of the lunar eccentre 10;19; and the greatest latitude 5°.

| Column | Computation | Agreement |
|---|---|---|
| Sun | tan q = e sin n / (1 + e cos n) | 133 of 180 within 3″ |
| Moon | tan q = r sin n / (1 + r cos n) | 139 of 180 within 3″ |
| latitude | sin b = sin n · sin 5° | 159 of 180 within 3″ |
| minutes | 60 (q(ρ) − q(60)) / (q(39;22) − q(60)) for the greatest equations q at the distance ρ of the epicycle | all 180 within 1.5 |
| prosneusis | tan p = e sin n / (ρ + e cos n) | 148 of 180 within 2′ |
| increment | the equation at the perigee distance 39;22 less the equation at the apogee | 136 of 180 within 2′ |

The arguments are n and 360 − n in every row. Consecutive values more than 3 units of their last place off in the same direction form one entry. For the Sun, the Moon and the latitude an entry is listed when one of its values is more than 5″ off, because al-Battānī's own seconds depart from the computation by 1″–3″, «perraro maiores» (Nallino). The minutes lie between 1.4 below and 0.7 above the computation: al-Battānī dropped the seconds of Ptolemy's column. The ledger holds 23 entries, and 0 are open:

- **Sun**: five stretches where the printed values depart by 6″–17″, the largest at 151°–166° (−17″ at 158°). One of them is the single value at 104°.
- **Moon, single values**: 19° (1° 31′ 25″ for 1° 30′ 25″), 41° (3° 4′ 17″, computed 3° 4′ 56.5″), 61° (4° 11′ 33″, computed 4° 11′ 55.8″), 63° (4° 17′ 8″, computed 4° 17′ 17.7″), 73° (4° 38′ 52″ for 4° 39′ 52″). Each breaks the run of the printed differences; the ledger gives the printed and computed steps.
- **Moon, stretches**: 25°–28°, 93°–99°, 106°–109°, 112°–115°, 131°–134°, 136°–139° (up to 15″). Nallino names 96°, 108°, 109° and 114° among the larger differences of al-Battānī's seconds.
- **Latitude**: 63° (4° 26′ 14″ for 4° 27′ 14″), and 133°–138°, where the values stand 3″, 10″, 10″, 20″, 20″ and 20″ above the equal latitudes of 47°–42°, which agree with the computation within 1″.
- **Prosneusis**: 123°–129°, 147°–153° and 172°–177°, up to 4.8′ above the computation.
- **Increment**: 22°–50° and 53°–54°. The values at 6°, 12°, 18°, 24° and 30° are 14′, 28′, 42′, 56′ and 70′, and the excess over the computation grows from 0.6′ at 6° to 5.5′ at 44°.

## Nallino's notes on these pages (Part II, pp. 223–227)

- **The Sun**: the table differs from Ptolemy's (Almagest III 5) because the greatest equation differs. Ptolemy gives the argument by sixes of degrees in the first and fourth quadrants and by threes in the second and third, and omits the seconds; al-Battānī gives every degree. The differences of the codex values are regular enough that Nallino corrected its errors at once, and rarely needed the computation.
- **The simple equation of the Moon**: Ptolemy computed it without seconds and roughly, so that his values often err by 1′ (once by 1′ 9″); al-Battānī computed the seconds too. Nallino checked the multiples of 6° with seven-place logarithms and the rest by interpolation. Three errors on p. 79 are to be corrected; this edition prints them as Nallino's table does:

  | Cell | Printed (codex) | Nallino | Exact |
  |---|---|---|---|
  | p. 79, 35° | 2° 40′ 12″ | 2° 40′ 52″ | 2° 40′ 52.6″ |
  | p. 79, 36° | 2° 45′ 17″ | 2° 44′ 57″ | 2° 44′ 59.5″ |
  | p. 79, 37° | 2° 49′ 42″ | 2° 49′ 2″ | 2° 49′ 4″ |

  Al-Battānī's seconds often agree exactly with the logarithmic computation; sometimes they differ by 1″–3″, rarely more (96°, 108°, 109°, 114°).
- **The equation of the anomaly** (Ptolemy's «prosthaphaereses of the apogee of the eccentre»): al-Battānī took all of Ptolemy's numbers (except at 108°: Ptolemy 13° 3′, al-Battānī 13° 2′) and interpolated the rest. Delambre judged the column right only to a minute or two. The codex heads these tables with al-ḥiṣṣah for al-ḥāṣṣah; Nallino restored al-ḥāṣṣah, as al-Battānī writes in his other tables and chapters.
- **The minutes to be added**: al-Battānī omits the seconds that Ptolemy gives.
- **The least longinquity**: the excess of the equation at the perigee over the equation at the apogee. Al-Battānī took Ptolemy's numbers, sometimes 1′ different on purpose (the greatest, 2° 40′, for Ptolemy's 2° 39′), and interpolated the rest. Delambre found Ptolemy's values sometimes right only to 2′.
- **The latitude of the Moon**: al-Battānī computed it with the rule sin(latitude) = sin(argument) · sin(greatest latitude); Schiaparelli checked it with logarithms. Ptolemy counts the argument from the northern limit, so that his 0° is al-Battānī's 90°.

## Conventions

- The first row of each table carries the marks ° ′ ″ (and ′ for the minutes), as printed.
- Only p. 78 has the Arabic heads; pp. 79–83 have the Latin heads alone. The Arabic titles of pp. 79–82 begin «من جداول», that of p. 83 «تمام جداول».
- The 4 of «204» (p. 83, 156°) is printed broken.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the check of the latitude table.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
