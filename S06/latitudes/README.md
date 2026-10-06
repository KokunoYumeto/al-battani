# S06 — Latitudes of the planets (Part II pp. 140–141)

The tables of the latitudes of the planets (codex fol. 224,v.–225,r.). Each row gives the true anomaly n = 6°, 12° … 180°, counted from the true apogee of the epicycle, and 360° − n (the «columnae numerorum, intervallo sex graduum»). Every value is given in degrees and minutes.

- **p. 140**: «Tabula latitudinum trium planetarum superiorum». For Saturn, Jupiter and Mars there are two columns, the latitude with the centre of the epicycle at the northern limit of the deferent (Septentrio) and at the southern limit (Auster).
  - The heads say how to enter the table for the intermediate places: «Latitudo Saturni, cuius centro 50° addendi», «Latitudo Iovis, a cuius centro 20° demendi», «Latit. Martis, cuius centro nihil addendum vel demendum».
  - The right margin carries the inscription افيثخون هو الشمال فرنجيون هو الجنوب, «ἀπόγειον est septentriones, περίγειον auster».
- **p. 141**: «Tabula latitudinum duorum planetarum inferiorum». For Venus and Mercury there are two columns:
  - Inclinatio: the latitude from the inclination of the diameter of the epicycle through its apogee.
  - Obliquitas: the latitude from the obliquity of the diameter at right angles to it.
  - A last column, «Portiones latitudinum communes omnibus planetis», gives the sixtieths for the places between the limits and the nodes.

## Read

- [Part II pp. 140–141, 2 pp.](p2_latitudes.pdf).

## Data

| File | Content |
|---|---|
| `latitudes_p2.tsv` | One row per printed row and column: page, row, n and 360 − n, the column, degrees and minutes, and how each number was established (`check`: the argument 360 − n, then the degrees and minutes). The columns are `sat_n`, `sat_s`, `jup_n`, `jup_s`, `mars_n`, `mars_s` (p. 140) and `ven_inc`, `ven_obl`, `mer_inc`, `mer_obl`, `portio` (p. 141). |
| `latitudes_pages.tsv` | Folio lines, the Arabic and Latin titles, the heads, and the inscription in the margin of p. 140. |
| `latitudes_discrepancies.tsv` | The 4 departures found, and the 2 cells on which Nallino's notes comment. |

## How the tables were read and checked

Every number was read by eye from 200 dpi renders and compared with the glyph reader and the OCR text layer. There are 720 numbers: the 60 arguments 360 − n and the 660 degrees and minutes of the latitudes.

- 651 are in class A: both machine readers give the eye's value.
- 63 are in class B: one machine reader gives it. Tesseract re-read every B cell as a third reader. Where it gave another number (24 cells), the cell was read by eye; every one confirmed the value.
- 6 are in class E: neither machine reader gives the value, and the cell was read again by eye at 500 dpi.

`python check_latitudes.py` computes every column from Ptolemy's elements as Nallino gives them (Part II pp. 247–255), in parts of which the radius of the deferent has 60:

| Planet | Radius of the epicycle | Eccentricity | Inclination of the deferent | Inclination of the epicycle |
|---|---|---|---|---|
| Saturn | 6;30 | 3;25 | 2;30 | 4;30 |
| Jupiter | 11;30 | 2;45 | 1;30 | 2;30 |
| Mars | 39;30 | 6 | 1 | 2;15 |
| Venus | 43;10 | 1;15 | (0;10) | inclination 2;30, obliquity 3;30 |
| Mercury | 22;30 | 3 | (0;45) | inclination 6;15, obliquity 7 |

- **Saturn, Jupiter, Mars** (Nallino pp. 247–249). The centre of the epicycle stands at the northern or the southern limit of the deferent. The apogee of the epicycle is tilted towards the ecliptic by the inclination i of the epicycle, the deferent being inclined by i0.
  - The limits lie 50° before the apogee of the deferent for Saturn and 20° after it for Jupiter (hence the heads); for Mars they lie at the apogee and the perigee.
  - The distance d of the centre of the epicycle is taken there: Saturn 62.14 and 57.75, Jupiter 62.58 and 57.41, Mars 66 and 54.
  - With x = d cos i0 + r cos n cos(i0 − i), y = r sin n and z = d sin i0 + r cos n sin(i0 − i), the latitude is atan(z / √(x² + y²)).
- **Inclination of Venus and Mercury** (Nallino pp. 250–251). The centre of the epicycle stands at a node, 90° from the apogee of the deferent, at the distance 59.99 (Venus) or 56.72 (Mercury). The latitude is
  sin(incl.) = r |cos n| sin i / √((d + r cos n cos i)² + (r sin n)² + (r cos n sin i)²).
- **Obliquity of Venus and Mercury** (Nallino p. 253). Ptolemy takes the obliquity proportional to the equation of the anomaly at the mean distance: the greatest equation, 46° for Venus and 22° for Mercury, gives the greatest obliquity, 2° 30′. The equation is al-Battānī's own column VI of the [equations of Venus and Mercury](../planets/README.md). Both columns follow it within 1.1′.
- **Portions** (Nallino p. 254). The portions are twelve times the latitude of the Moon, whose greatest latitude is 5°, at the distance n from the limit, taken to whole minutes: 5° × 12 = 60.
  - Every value is a multiple of 12′ and is the same at n and 180° − n.
  - Its twelfth lies within 1′ of asin(sin 5° |cos n|) rounded to the minute.
  - At 24°, 36°, 42°, 48° and 72° the latitude is 1′ below the rounded value, at 84° 1′ above: for example 54° 36′ = 12 × 4° 33′ at 24°, where the latitude is 4° 34.0′.

| Column | Largest departure |
|---|---|
| Saturn, north / south | 1.3′ (36°) / 1.0′ (84°) |
| Jupiter, north / south | 1.7′ (102°) / 1.8′ (90°) |
| Mars, north / south | 1.6′ (6°) / 6.8′ (174°) |
| Venus, inclination / obliquity | 10.7′ (174°) / 0.6′ (126°) |
| Mercury, inclination / obliquity | 2.1′ (84°) / 1.1′ (126°) |

**Listing rule.** A value more than 3′ off its computation is listed when it, or a value of its run (consecutive values off in the same direction), is more than 4′ off. A single value is also listed when it departs from the mean of its two neighbours by 2′ more than the computation does.

**Result.** 325 values lie within these limits. Four departures are ledgered, and 0 are open:

- **Mars, southern limit, 174°**: 6° 36′, where the computation gives 6° 42.8′. The printed steps from 168° are 44′ and 31′, the computed 51.7′ and 22.7′. The values of 168° and 180°, 5° 52′ and 7° 7′, lie within 1.5′ of the computation.
- **Venus, inclination, 150°–156° and 168°–174°**: from 138° the column runs 1° 59′, 2° 23′, 3° 3′, 3° 44′, 4° 26′, 5° 13′, 5° 52′, 6° 22′.
  - Its steps are 24′, 40′, 41′, 42′, 47′, 39′, 30′.
  - The computation gives 1° 59.7′, 2° 26.6′, 2° 59.1′, 3° 38.2′, 4° 24.9′, 5° 16.7′, 6° 2.7′, 6° 22.3′, in steps of 26.9′, 32.5′, 39.1′, 46.7′, 51.8′, 46.0′, 19.6′.
  - The printed column advances more evenly. At both ends it agrees with the computation: 1° 2′ at the apogee of the epicycle and 6° 22′ at the perigee (Nallino p. 250 n. 4).
- **Mercury, inclination, 84°**: 0° 16′, where the computation gives 0° 13.9′. The neighbours, 0° 26′ at 78° and 0° 0′ at 90°, agree with it (0° 26.9′ and 0°).

The ledgered cells are clearly printed.

## Nallino's notes on these pages (Part II, pp. 247–255)

- **Sources.** The tables are treated in chapter XLVII (t. I, pp. 115–116) and come from Almagest XIII 5 (ed. Halma, t. II, pp. 412–413).
- **Halma's edition.**
  - Halma's edition wrongly has 45′ for 55′ in the obliquity of Mercury at 30° and 330°; this table has 0° 55′.
  - For the greatest southern latitude of Saturn Nallino refers to t. I, p. 116 n. 8. There the table has 3° 5′, as in the Latin Almagest translated from the Arabic and printed by Liechtenstein (Venice 1515). Halma's Almagest has 3° 4′, its French version wrongly 2° 4′, Theon's Canon 3° 6′; the codex text of chapter XLVII has 33° 5′. The computation gives 3° 4.2′.
- In the last column of p. 141 Nallino wrote «gradus» and «minuta», following the Escorial codex; the numbers are in fact minutes and seconds (sixtieths). The inscription in the margin of p. 140 is discussed in t. I, p. 282.
- **The outer planets.**
  - The latitude has two parts: the fixed inclination of the deferent, and the inclination of the epicycle to the deferent.
  - The true apogee of the epicycle moves on a small circle perpendicular to the deferent, so that at the limits the apogee lies between the planes of the deferent and the ecliptic and the perigee beyond the deferent. The greatest latitude therefore falls at the perigee of the epicycle.
  - Nallino derives the computation (formulas 1–3, p. 249), with which Ptolemy computed the two columns for every 6° and 3° of true anomaly, and the limits: Saturn's northern limit 50° west of the apogee, Jupiter's 20° east, Mars's at the apogee.
- **Venus and Mercury.** They have three inequalities.
  - The inclination of the deferent is variable: 10′ north for Venus and 45′ south for Mercury at the apogee and perigee of the deferent, and nothing at the nodes.
  - The inclination of the epicycle is greatest at the nodes: 2° 30′ for Venus, giving 1° 2′ at the apogee and 6° 22′ at the perigee of the epicycle as seen from the Earth; 6° 15′ for Mercury, giving 1° 46′ and 4° 5′.
  - The obliquity is greatest at the apogee and perigee of the deferent: 3° 30′ for Venus and 7° for Mercury, seen from the Earth about 2° 30′.
- **Obliquity.** Ptolemy found the greatest obliquity seen from the Earth to be 2° 27′ (apogee) and 2° 34′ (perigee) for Venus, 2° 17′ and 2° 46′ for Mercury. He tabulated it for the mean distance.
  - Rather than computing it directly, he assumed, without proof, that it is proportional to the digression of the planet. The rule is «non exacte sed proxime verum».
  - For Mercury one tenth of the obliquity is added or subtracted at the other distances.
- **Portions.** The portions come from the latitudes of the Moon, multiplied by 12. Al-Battānī (t. I, p. 116) takes 1/6 of them for Venus and 3/4 for Mercury when entering the table again with the longitude, so as not to neglect the inclination of the deferent.
- **Others on these tables.**
  - Delambre's judgement of these tables (Histoire de l'astronomie ancienne, t. II, p. 406) is hardly right: he misread Ptolemy's correction of a quarter of a degree for Mercury.
  - Haebler's view that the *Hypotheses* contain a simpler theory of latitude is mistaken.
  - The elements of the *Hypotheses* differ from the Almagest's (table on p. 255).

## Conventions

- The first row carries the marks as printed: ° for the arguments, ° ′ for the latitudes.
- A rule runs across the table between 90° and 96°.
- Only the heads of Saturn's two columns (شمال, جنوب) and of Venus's (الميل, الانحراف) have Arabic; the others are in Latin only. The head of Mercury ends with a comma, as printed. The Arabic head of the argument columns reads متفاضلة on both pages.
- These pages have no signatures.

## Tools

`tools/` holds the scripts that read the pages: `latitude_pages.py` (the eye reading), `build_latitudes.py` (writes the two data files), and the shared readers. `python write_latitudes_ledger.py` writes the ledger, `python check_latitudes.py` checks the data (`--stats` gives the distances used and the largest departure of each column), and `python gen_latitudes.py` writes `p2_latitudes.tex` (XeLaTeX).
