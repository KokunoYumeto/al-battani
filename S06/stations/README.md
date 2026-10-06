# S06 — Stations of the planets (Part II pp. 138–139)

The tables of the stations (codex fol. 223,v.–224,r.): p. 138 for Saturn, Jupiter and Mars («Tabulae stationum trium planetarum superiorum ad cognoscendos regressus et progressus»), p. 139 for Venus and Mercury («Tabulae stationum duorum planetarum inferiorum …»). Each row gives an argument n = 6°, 12° … 180° and 360° − n (the «columnae numerorum, intervallo sex graduum»). The argument is the true centre: the distance of the centre of the epicycle from the apogee of the deferent, seen from the Earth. For each planet two columns give degrees and minutes:

| Column | Content |
|---|---|
| Statio I | the corrected anomaly, counted from the true apogee of the epicycle, at which the planet stands still and begins to retrogress |
| Statio II | the corrected anomaly at which it stands still again and resumes its direct motion |

## Read

- [Part II pp. 138–139, 2 pp.](p2_stations.pdf).

## Data

| File | Content |
|---|---|
| `stations_p2.tsv` | One row per printed row and planet: page, planet, row, n and 360 − n, Statio I and Statio II (degrees, minutes), how each number was established (`check`: the argument 360 − n, then the degrees and minutes of each station), and notes. |
| `stations_pages.tsv` | Folio lines, the Arabic and Latin titles, and the heads of the argument columns, of the planets and of the stations. |
| `stations_discrepancies.tsv` | No differences were found. The file records the stations of Mars at 90°, for which Nallino reports the reading of the codex. |

## How the tables were read and checked

Every number was read by eye from 200 dpi renders and compared with the glyph reader and the OCR text layer. There are 660 numbers: the 60 arguments 360 − n and the 600 degrees and minutes of the stations.

- 464 are in class A: both machine readers give the eye's value.
- 163 are in class B: one machine reader gives it (for 3 of them only the glyph reader, the text layer having no token there). Tesseract re-read every B cell as a third reader. Where it gave another number (47 cells), the cell was read by eye at 900 dpi; every one confirmed the value.
- 33 are in class E: neither machine reader gives the value, and the cell was read again by eye at 500 dpi.

`python check_stations.py` makes these checks:

- **360 − n** in every row: 150 of 150.
- **Statio I + Statio II = 360°** in every row: 150 of 150. Nallino (p. 245) shows why: if the first station falls at the corrected anomaly 180° − ψ, the second falls at 180° + ψ.
- **Statio I against the construction Nallino describes** (pp. 245–247).
  - Ptolemy finds the station point by Apollonius's condition, using the true velocities of the epicycle and of the planet. He does this for the greatest, the mean and the least distance of the centre of the epicycle from the Earth.
  - For any other position he changes the station at the mean distance in proportion to the change of the distance: statio = statio media ± II × III / I.
  - The distance is taken at the true centre, the argument of these tables.
  - The elements are Ptolemy's, in parts of which the radius of the deferent has 60:

| Planet | Eccentricity of the deferent | Radius of the epicycle |
|---|---|---|
| Saturn | 3;25 | 6;30 |
| Jupiter | 2;45 | 11;30 |
| Mars | 6 | 39;30 |
| Venus | 1;15 | 43;10 |
| Mercury | 3 (with the circlet that carries the centre of its deferent) | 22;30 |

Saturn, Venus and Mercury follow the proportion of the distance.

Jupiter and Mars follow instead the proportion of the change of the greatest equation of the epicycle, asin(r / d). This is the quantity on which Ptolemy builds the sixtieths of his planetary tables (see the [notes to pp. 108–137](../planets/README.md)). For Mars, whose epicycle is large, the two rules differ by up to 8′. The table follows the second: r.m.s. 0.46′ against 3.67′. For Jupiter the second rule fits better too: 1.14′ against 1.30′.

Mars is computed every 12°. Its values at 18°, 30° … 174° are the means of their neighbours, so its column advances in equal pairs of steps: 10′, 10′, 18′, 18′, 24′, 24′, 30′, 30′, 35′, 35′, 38′, 38′ and so on. Two of the means are 1′ above: 165° 39′ at 114° and 167° 37′ at 138°.

The three stations of each planet are fitted to its 30 values by least squares:

| Planet | Proportion | Greatest distance | Mean distance | Least distance | Largest departure | r.m.s. |
|---|---|---|---|---|---|---|
| Saturn | distance | 112° 44.4′ | 114° 8.1′ | 115° 29.2′ | 0.6′ | 0.34′ |
| Jupiter | greatest equation | 124° 3.8′ | 125° 38.8′ | 127° 11.7′ | 3.2′ (114°) | 1.14′ |
| Mars | greatest equation, every 12° | 157° 29.2′ | 163° 8.3′ | 169° 13.9′ | 1.0′ | 0.46′ |
| Venus | distance | 165° 51.5′ | 167° 9.0′ | 168° 20.2′ | 1.5′ | 0.64′ |
| Mercury | distance | 147° 14.2′ | 145° 5.0′ | 144° 28.8′ | 1.3′ | 0.50′ |

**Listing rule.** A value more than 3′ off its computation is listed when it, or a value of its run (consecutive values off in the same direction), is more than 4′ off. A single value is also listed when it departs from the mean of its two neighbours by 2′ more than the computation does.

**Result.** All 150 values satisfy these checks. No differences are found, and 0 are open.

**Jupiter's course.** The values from 102° to 120° stand 1.3′ to 3.2′ below the computation. Those from 66° to 90° stand 1.1′ to 1.6′ above it. The steps of the column are regular (8′, 8′, 8′, 10′, 10′ from 96° to 126°), so this is the course of the table itself, not a misprint.

## Nallino's notes on these pages (Part II, pp. 245–247)

- The tables are treated in chapter XLVI (t. I, p. 114) and in the spurious appendix D (t. I, p. 147).
- **Comparison with Ptolemy and Theon.**
  - The tables differ in the minutes from Ptolemy's (Almagest XII 7, ed. Halma t. II pp. 354–355). Ptolemy took the mean centre (τὸ περιοδικὸν μῆκος) as the argument of his tables; Theon and al-Battānī take the true centre.
  - The tables agree with Theon's (t. III pp. 11–15). Nallino checked the numbers of the codex against them.
- **Jupiter, Statio I at 42° and 54°.** Theon has 124° 21′ and 124° 46′. Al-Battānī has the correct 124° 28′ and 124° 43′, and the computation gives 124° 28.3′ and 124° 43.3′. The note prints the second pair as 128° 46′ and 128° 43′; the table has 124° 43′.
- **Mars at 90°.** Following Schiaparelli, the minutes of the stations of Mars at 90° are wrong in Theon and in the Escorial codex: 25′ and 35′ for 22′ and 38′. The table prints 163° 22′ and 196° 38′. 163° 22′ is the mean of the values at 84° and 96°, and the computation gives 163° 22.5′.
- The sum of the two stations is always 360°.
- **Ptolemy's theory of stations** (Almagest XII 1–7).
  - A planet retrogresses when half the chord that the line from the Earth cuts in the epicycle has to the outer part of that line a greater ratio than the velocity of the epicycle has to that of the planet. It is stationary when the two ratios are equal.
  - The true velocities of the epicycle and of the planet follow from the equations of the centre.
  - The station point is found from PE × DE = KE × TE (Euclid III 36) and the angles LHT and HEL.
  - Nallino also gives the true arc of retrogradation, corrected for the motion of the epicycle in half the time of retrogradation, and calls it «solutio quidem adproximata, sed sufficiens».
- **Interpolation.** Ptolemy computes the stations for the greatest, the mean and the least distance and interpolates statio = statio media ± II × III / I, at every 6° of the mean elongation (in Theon and al-Battānī, of the true elongation). The stations are assumed to grow or shrink in proportion to the geocentric distance; this «licet verum non sit, insensibilem tamen errorem gignit».
- The two columns of each planet give the corrected anomalies (αἱ τῆς διευκρινημένης ἀνωμαλίας ἀποχαὶ ἀπὸ τῶν φαινομένων ἀπογείων τῶν ἐπικύκλων) that produce the first and the second station.

## Conventions

- The first row carries the marks as printed: ° for the arguments, ° ′ for the stations.
- Only Saturn's station heads have Arabic (المقام الاول, المقام الثاني); the others are in Latin only. The Arabic head of the argument columns reads المتفاضلة on p. 138 and متفاضلة on p. 139.
- These pages have no signatures.

## Tools

`tools/` holds the scripts that read the pages: `station_pages.py` (the eye reading and the expected values), `build_stations.py` (writes the two data files), and the shared readers. `python write_stations_ledger.py` writes the ledger, `python check_stations.py` checks the data (`--stats` gives the fit of each planet), and `python gen_stations.py` writes `p2_stations.tex` (XeLaTeX).
