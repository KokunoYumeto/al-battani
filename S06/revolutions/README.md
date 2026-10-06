# S06 — Revolutions of the years, altitudes and directions of the hours (Part II pp. 187–188)

The last two pages of the tables (codex fol. 239,v.–240,r.):

- **p. 187**: «Tabula incrementorum quibus planetarum loci medii in origine augendi sunt ad revolutiones [annorum supputandas]». For 1 to 12 «anni Romani integri» it gives the increments of eight mean motions, in degrees and minutes:
  - the Moon's mean longitude and its anomaly;
  - the northern node;
  - the mean longitudes of Saturn, Jupiter and Mars, which are also the diminutions of their anomalies;
  - the anomalies of Venus and Mercury.
- **p. 188**, three small tables:
  - «Tabula revolutionum annorum Romanorum [tropicorum]»: the «tempora ascensionum» of collected years 20 to 200 and single years 1 to 20.
  - «Tabulae horarum»: the altitude of the Sun at the end of each of the twelve temporal hours of the days of the winter and the summer solstice («Horae Capricorni», «Horae Cancri»).
  - «Tabula directionum horarum»: the direction of the Sun at the ends of the first six hours of the same days, to the seconds, north or south of the east–west line.

## Read

- [Part II pp. 187–188, 2 pp.](p2_revolutions.pdf).

## Data

| File | Content |
|---|---|
| `revolutions_p2.tsv` | One row per printed value: page, table (`increments`, `years`, `altitude`, `direction`), row, argument (years or hour), column, degrees, minutes and seconds, the quarter printed in brackets, and how the number was established (`check`). |
| `revolutions_pages.tsv` | Folio lines, titles and heads. |
| `revolutions_discrepancies.tsv` | The 7 differences found, and the 18 numbers for which Nallino gives the reading of the codex. |

## How the tables were read and checked

There are 336 numbers.

- **p. 187** (192 numbers) was read by eye and with the glyph reader and the OCR text layer: 181 numbers in class A (both machine readers give the eye's value), 7 in class B (one gives it, confirmed by Tesseract or by eye) and 4 in class E (read again by eye at 500 dpi).
- **p. 188** (66 values, 144 numbers) was read by eye and compared with the text layer row by row. 61 values agree (A). In 5 the text layer differs and a 700 dpi zoom confirms the eye's reading (E): it reads the degree sign as a 0 in «292°» and «19°», and 4 as 1 three times.

`python check_revolutions.py` makes four checks.

1. **The increments (p. 187).** «Anni integri» are not calendar years but tropical years of 365d 5h 46m 24s (Nallino p. 295). Each column is n times the motion in one such year, modulo 360°. The check fits the motion in one year to each column and compares it with al-Battānī's daily motions, taken from the 30-year steps (10,631 days) of his collected Arab years ([mean motions](../mean_motions/README.md)), times 365d 5h 46m 24s.

   | Column | Motion in one year (fitted) | From the daily motion | Difference a year |
   |---|---|---|---|
   | Moon, mean longitude | 132° 33.4′ | 132° 33.3′ | +3.2″ |
   | Moon, anomaly | 91° 51.7′ | 91° 51.7′ | +0.3″ |
   | Northern node | 19° 20.5′ | 19° 20.4′ | +5.0″ |
   | Saturn | 12° 14.1′ | 12° 14.1′ | +0.8″ |
   | Jupiter | 30° 21.8′ | 30° 21.8′ | +0.4″ |
   | Mars | 191° 24.9′ | 191° 24.8′ | +5.3″ |
   | Venus, anomaly | 225° 10.8′ | 225° 10.8′ | +2.2″ |
   | Mercury, anomaly | 54° 41.4′ | 54° 41.6′ | −13.4″ |

   - Every value but one lies within 1.7′ of its line: the steps of each column are the yearly motion rounded to the minute, now one minute larger, now one smaller.
   - **Mercury, year 6**: 327° 8′ for 328° 8′. The steps from year 5 (273° 27′) and to year 7 (22° 50′) are 53° 41′ and 55° 42′; every other step of the column is 54° 41′ or 54° 42′.
   - Mercury's column advances 0.2′ a year less than al-Battānī's daily motion gives, so that its last values stand up to 3.4′ below the products of that motion.

   The Jupiter column as printed is Nallino's emendation (see below); it lies within 0.5′ of its line.

2. **The revolutions of the years (p. 188).** The tropical year exceeds 365 days by 5h 46m 24s, which in degrees of the daily rotation («tempora ascensionum») is 86° 36′ (Nallino p. 295). Every value is n × 86° 36′ modulo 360°, the 10 collected years and the 20 single years exactly; 20 single years give the first collected line, 292° 0′.

3. **The altitudes (p. 188).** The computation is for ar-Raqqah: latitude 36° 0′, the Sun 66° 25′ from the pole at the summer solstice and 113° 35′ at the winter one (obliquity 23° 35′, Nallino p. 296). The hour angle at the end of temporal hour k is the half-day arc times (6 − k)/6.
   - Hours k and 12 − k are equal in both columns, and the twelfth hour is 0° 0′.
   - The altitudes of the summer solstice lie within 0.6′ of the computation, those of the winter solstice within 2.2′.
   - **The exception**: hours 2 and 10 of the summer solstice, 27° 1′, where the computation gives 27° 24.2′.

4. **The directions (p. 188).** The printed directions are Schiaparelli's computation (see Nallino's notes below). The check recomputes them with the same elements, and the quarters in Nallino's brackets agree with it.
   - Six of the directions of the first five hours lie within 26″ of the computation.
   - Four lie farther from it:
     - Cancer, hour 4: 11° 40′ 44″ against 11° 37′ 20″;
     - Cancer, hour 5: 33° 29′ 30″ against 33° 31′ 10″;
     - Capricorn, hour 3: 54° 56′ 30″ against 54° 51′ 39″;
     - Capricorn, hour 4: 65° 37′ 30″ against 65° 35′ 55″.
   - The sixth hour is the meridian, 90° 0′ 0″.

In all, 155 values satisfy these checks. Seven differences are ledgered, and 0 are open.

## Nallino's notes on these pages (Part II, pp. 295–296)

- **p. 187.** The table is mentioned in t. I, p. 129 (chapter LIII) and p. 148 (appendix E), and goes with the small table on the left of p. 188. The «anni integri» are tropical years of 365d 5h 46m 24s, as al-Battānī observed; the name «Romanorum» seems to Nallino a clumsy interpolation. The revolutions of the years are explained in t. I, pp. 304–305, and the use of the tables in t. I, p. 148.
- **Jupiter.** The last numbers of Jupiter are false in the codex and the Spanish version. After writing the correct 212° 33′ of year 7, the copyist wrote 182° 11′ again (corrupted into 142° 15′) and the numbers that follow it, and left out the last two, 334° 0′ and 4° 22′.

  | Year | Codex and Spanish version | Emended (printed) |
  |---|---|---|
  | 6 | 182° 51′ (نا for يا) | 182° 11′ |
  | 7 | 212° 33′ | 212° 33′ |
  | 8 | 142° 15′ (قمب يه for قفب يا) | 242° 55′ |
  | 9 | 217° 33′ (ريز for ريب; Spanish 214°) | 273° 17′ |
  | 10 | 242° 55′ (Spanish 15′) | 303° 38′ |
  | 11 | 273° 17′ (Spanish 40′) | 334° 0′ |
  | 12 | 63° 38′ (صج for سج) | 4° 22′ |

- **p. 188, the revolutions of the years.** The small table gives the angle through which the Sun's daily rotation turns in a tropical year beyond 365 whole rotations: the 5h 46m 24s by which the year exceeds 365 days, as 86° 36′ of «tempora ascensionum». It serves to find the daily motion for any number of tropical years.
- **p. 188, the hours.** The two tables on the right are mentioned in t. I, p. 138 (chapter LVI; compare t. I, p. 135 n. 1).
  - The codex heads them together «جداول ساعات تحاويل هذه السنين», «Tabulae horarum revolutionum horum annorum», a «ridiculous» corruption. The Spanish version has only the lower table.
  - They give the two ends of each hour line of a horizontal sundial, for the temporal hours of the days of the two solstices: the length of the gnomon's shadow (from the altitude) and its azimuth. The tables give the altitude and the complement of the azimuth, the «ortive or occiduous amplitude».
- **Schiaparelli's computation.** Schiaparelli's note shows how to compute both from the hour angle with Napier's analogies. A straight line joining the two points of an hour gives the hour line nearly; the true line of a temporal hour is slightly curved, and the error can reach some minutes.
  - With these formulas Schiaparelli restored the directions. The codex's numbers «were so far from the truth that they seem supplied by another hand from other elements».
  - Delambre (Histoire de l'astronomie du moyen âge, p. 60) also computed the table; his numbers agree exactly with Schiaparelli's.
  - The codex and the Spanish version have: Cancer 19° 36′ 32″, 10° 5′ 11″, 1° 18′ 35″ (Spanish 38′), 11° 21′ 31″, 32° 58′ 30″ (Spanish 35″), 79° 36′ 4″; Capricorn 36° 35′ 24″ (Spanish 37°), 46° 28′ 35″, 54° 3′ 50″, 65° 29′ 57″, 77° 24′ 57″, 85° 1′ 0″.
  - Neither names the quarter of the directions; Nallino adds them in brackets.

## Conventions

- The heads of p. 187 and of the columns of the years, hours and directions on p. 188 stand along their columns, read from the foot upwards, as printed.
- The first row of each table carries the marks as printed.
- On p. 188 each collected year stands beside two single years, as printed.
- The quarters of the directions, «[ad bor.]», «[ad austr.]» and «[id.]», are Nallino's, in his brackets.
- These pages have no signatures.

## Tools

`tools/` holds the scripts that read the pages:

- `revolution_pages.py`: the eye reading;
- `build_revolutions.py`: writes the two data files;
- the shared readers.

The scripts here:

- `python write_revolutions_ledger.py` writes the ledger;
- `python check_revolutions.py` checks the data; `--stats` gives the fitted motions and the departures;
- `python gen_revolutions.py` writes `p2_revolutions.tex` (XeLaTeX).
