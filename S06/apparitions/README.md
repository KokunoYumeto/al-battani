# S06 — Elongations for the apparitions and occultations of the planets (Part II pp. 142–143)

The tables of the elongations of the planets from the true Sun at their apparitions and occultations, «in oriente et occidente, ad latitudinem 36° 0′» (codex fol. 225,v.–226,r.). Each row is the beginning of a sign, where the planet stands; each value is in degrees and minutes.

- **p. 142**: «Tabula elongationum trium planetarum superiorum ad cognoscendas apparitiones et occultationes …». Saturn, Jupiter and Mars each have two columns:
  - Apparitio, «Ortus matutinus»: the first rising in the morning;
  - Occultatio, «Occasus vespertinus»: the last setting in the evening.
- **p. 143**: «Tabula elongationum duorum planetarum inferiorum …». Venus and Mercury each have four columns, each head giving the range of the anomaly in which the phenomenon falls:
  - under Apparitio, «Ortus vespertinus» (Venus 0°–137°, Mercury 0°–112°) and «Occasus matutinus» (223°–360°, 248°–360°);
  - under Occultatio, «Ortus matutinus» (180°–223°, 180°–248°) and «Occasus vespertinus» (137°–180°, 112°–180°).

## Read

- [Part II pp. 142–143, 2 pp.](p2_apparitions.pdf).

## Data

| File | Content |
|---|---|
| `apparitions_p2.tsv` | One row per printed row and column: page, row, sign, column, degrees and minutes, and how each number was established (`check`). The columns are `sat_app`, `sat_occ`, `jup_app`, `jup_occ`, `mars_app`, `mars_occ` (p. 142), and for Venus and Mercury `ven_ort_vesp`, `ven_occ_mat`, `ven_ort_mat`, `ven_occ_vesp`, `mer_…` (p. 143), in the order printed. |
| `apparitions_pages.tsv` | Folio lines, the Arabic and Latin titles, and the heads of the signs, of the planets and of the single columns. |
| `apparitions_readings.tsv` | Nallino's lists of the readings of Theon and of the Latin Almagest of 1515 that differ from the printed numbers (Part II pp. 267–268), with his marks «false» and «uncertain», and the degrees he restores on p. 269. |
| `apparitions_discrepancies.tsv` | The 60 numbers that Nallino's notes correct, the 6 values that depart from the computation and the 1 identity that fails, each with its explanation. |

## How the tables were read and checked

Every number was read by eye from 200 dpi renders and compared with the glyph reader and the OCR text layer. Of the 336 numbers, 313 are in class A (both machine readers give the eye's value) and 23 in class B (one gives it). Tesseract re-read the B cells as a third reader; the 10 where it gave another number were read by eye at 900 dpi and all confirm the value.

**The printed numbers.** These are Schiaparelli's approximate restorations («quantitates proxime a Schiaparelli restitutae», Nallino p. 262). Nallino lists where the codex, the Spanish version, Ḥabash and the Alphonsine tables differ from them (pp. 262–265). After the pages were printed he compared two further sources (pp. 266–268):

- Theon's tables of the phases for the fourth clime (longest day 14½ hours, latitude 36°), whose columns all agree with these tables;
- the Latin Almagest translated from the Arabic by Gerard of Cremona and printed by Liechtenstein (Venice 1515), f. 152,r., which gives a quarter of this table in place of Ptolemy's.

His ruling (p. 269) has two parts:

- adopt every reading of Theon and of the Latin Almagest that he marks neither false nor uncertain;
- restore the degrees 2° of the evening setting of Venus.

The check applies these readings. They change 60 numbers, one or both places of a value, and the ledger records each of them (kind «noted»). For Pisces in the evening setting of Venus, the degrees come from the restoration and the minutes, 31′, from Theon and the Latin Almagest. The codex has 1° 31′ there, and Ḥabash 2° 31′. At Taurus in the occultation of Saturn, Nallino adopts Theon's 7′, although he marks the same 7′ of the Latin Almagest false.

`python check_apparitions.py` then makes four checks.

1. **The heads.** The anomalies in the heads of p. 143, in Maghribi abjad (for example قلز = 137, ركج = 223, سص = 360, رمح = 248), equal their Latin: 8 of 8.

2. **The identities.** The angle between the ecliptic and the horizon is the same at points equally distant from an equinox, and at a rising point and the opposite point setting at the same moment (Nallino p. 259). If the latitude is neglected, as al-Battānī does for Mars (Nallino p. 260), three identities follow:
   - the apparitions at λ and −λ are equal;
   - so are the occultations;
   - the apparition at λ equals the occultation at λ + 180°.

   Jupiter's table is symmetric about the equinoxes too. Of these 32 identities, 19 hold as printed and 31 with Nallino's readings. The one that fails pairs the apparition of Mars at Libra with its occultation at Aries:
   - Theon's readings are 14° 42′ and 14° 52′;
   - the printed table has 14° 52′ and 14° 37′;
   - the computation below gives 14° 50.8′ for both.

3. **The computation.** Nallino could not reconstruct the computation of these tables. He worked Ptolemy's rule for Mars with Ptolemy's arcus visionis of 11° 30′, at Aries, Leo and Virgo, where the codex is certain. He found 22° 43′, 12° 51′ and 11° 58′ against the table's 29° 0′, 16° 7′ and 15° 8′, and could not explain the difference (pp. 258–261). The rule is:

   elongation = arcus visionis / sin θ ∓ latitude · cot θ

   Here θ is the angle between the ecliptic and the horizon at the planet's place: the eastern horizon for a phenomenon at rising, the western one for a phenomenon at setting. The check computes θ exactly for latitude 36° and al-Battānī's obliquity, 23° 35′; Nallino's 30° 25′, 63° 30′ 57″ and 73° 50′ 26″ for Aries, Leo and Virgo agree.

   **The arcus visionis.** With 14° 30′ in place of 11° 30′, Nallino's three values become 28° 38′, 16° 12′ and 15° 6′. Fitted freely, the arcus visionis of the columns come out at 12.97°–12.99° (Saturn), 8.97°–8.99° (Jupiter), 14.52° (Mars), 6.99° and 7.03° (Venus near the superior conjunction), 5.00° (Venus near the inferior conjunction) and 11.96°–12.21° (Mercury). The check therefore fixes them at 13°, 9°, 14° 30′, 7°, 5° and 12°. The Almagest's values are 11°, 10°, 11° 30′, 5° and 10° (Nallino p. 257).

   **The latitude.** For Saturn and Jupiter the latitude term is k cos(λ − λN). λN is the northern limit given by al-Battānī's apogees: 194° 28′ for Saturn and 184° 28′ for Jupiter (Nallino p. 259). The fitted k is −2.19° and −1.94° for Saturn, −1.16° and −1.03° for Jupiter, against latitudes of about 2° 6′ and 1° 8′ at the anomaly of 20° in the [table of latitudes](../latitudes/README.md). Mars has no latitude term. For Venus and Mercury the term is kc cos λ + ks sin λ.

   **Fitting.** The coefficients are fitted to each column as corrected by Nallino's readings. At most three values per column are set aside, each departing by more than three times the robust spread and by more than 10′.

   | Column | Horizon | Arcus visionis | r.m.s. | Printed values | With the other horizon |
   |---|---|---|---|---|---|
   | Saturn, apparitio | E | 13° | 6.5′ (Gemini set aside) | 9.9′ | 5° 7′ |
   | Saturn, occultatio | W | 13° | 9.8′ | 12.7′ | 3° 12′ |
   | Jupiter, apparitio | E | 9° | 5.9′ | 10.6′ | 3° 4′ |
   | Jupiter, occultatio | W | 9° | 5.5′ | 5.5′ | 1° 56′ |
   | Mars, apparitio | E | 14° 30′ | 9.3′ | 19.3′ | 9° 33′ |
   | Mars, occultatio | W | 14° 30′ | 8.9′ | 27.0′ | 9° 32′ |
   | Venus, «ortus vespertinus» | **E** | 7° | 3.8′ | 31.4′ | 2° 30′ |
   | Venus, «occasus matutinus» | **W** | 7° | 7.2′ (Virgo, Sagittarius set aside) | 15.9′ | 1° 15′ |
   | Venus, «ortus matutinus» | **W** | 5° | 4.6′ | 1° 11.6′ | 5° 41′ |
   | Venus, «occasus vespertinus» | — | — | not reproduced | | |
   | Mercury, «ortus vespertinus» | **E** | 12° | 4.8′ (Gemini, Pisces set aside) | 15.9′ | 3° 31′ |
   | Mercury, «occasus matutinus» | **W** | 12° | 11.5′ | 14.1′ | 3° 19′ |
   | Mercury, «ortus matutinus» | E | 12° | 10.6′ (Taurus set aside) | 24.0′ | 3° 30′ |
   | Mercury, «occasus vespertinus» | W | 12° | 4.9′ (Cancer, Sagittarius set aside) | 33.2′ | 3° 54′ |

   The r.m.s. is that of the corrected values the fit uses. «Printed values» gives the printed numbers against the same computation. The last column gives the corrected values against the other horizon, with the arcus visionis and the latitude terms fitted freely.

   **The horizons in bold.** Their values follow the opposite horizon to the phenomenon their head names. The values under «ortus vespertinus» are those of a phenomenon at the eastern horizon, and those under «occasus matutinus» of one at the western horizon. For example, Mercury's «ortus vespertinus» is largest at Aries (24° 10′), where the ecliptic meets the eastern horizon at 30° and the western at 78°. The same holds for the third column of Venus. Nallino notes only that the general titles «apparitio» and «occultatio» are misplaced (p. 269).

   **The last column of Venus.** It is reproduced with neither horizon: r.m.s. 1° 7′ (E) and 1° 44′ (W) with Nallino's readings, 44′ and 31′ as printed. It is not checked.

4. **The listing.** A value of the corrected table more than 30′ from its computation is listed. 150 values lie within 30′. Six are ledgered (kind «value»):
   - **Venus, «occasus matutinus», Virgo**: 10° 46′, computed 10° 13′. Of the witnesses only Ḥabash differs (47′).
   - **Venus, «occasus matutinus», Sagittarius**: Theon, the Latin Almagest, the codex and Ḥabash have 12° 27′, 1° 20′ above the computation, 11° 7′. Schiaparelli's printed 10° 47′ lies 20′ below it.
   - **Mercury, «ortus vespertinus», Pisces**: 24° 38′, computed 23° 59′. Every witness agrees except Theon's uncertain 35′ and the Latin Almagest's false 18′.
   - **Mercury, «ortus matutinus», Taurus**: 25° 23′, computed 24° 17′. Ḥabash has 24°, the Alphonsine tables 24° 32′ and the Latin Almagest 24°, which Nallino marks uncertain. 24° 23′ would lie 6′ from the computation.
   - **Mercury, «occasus vespertinus», Cancer**: 19° 48′ in every witness, computed 18° 44′.
   - **Mercury, «occasus vespertinus», Sagittarius**: every witness has 17° 41′ (the printed number is 16° 41′). The computation gives 15° 41′.

**How the corrections fare.** Of Nallino's 60 corrections, 54 fall in computed columns, and 47 of these lie closer to the computation than the printed number.

- In some columns they bring the values onto the computation: Mars's apparitions and occultations (r.m.s. 19′ and 27′ as printed, 9′ with the readings), Venus's «ortus vespertinus» (31′ to 4′) and its «ortus matutinus» (1° 12′ to 5′).
- Four lie farther from the computation than the printed number:
  - Venus's «occasus matutinus» at Sagittarius: 12° 27′ lies 80′ from it, the printed number 20′;
  - Mercury's «occasus vespertinus» at Sagittarius: 120′ against 60′;
  - Mercury's «ortus matutinus» at Capricornus: Theon's 12° 56′ lies 22′ from it, the printed 12° 36′ 3′;
  - Mars's apparition at Libra: Theon's 42′ lies 9′ from it, the printed 52′ 1′ (see the identities above).
- In three more, both the reading and the printed number lie within 15′ of the computation: Saturn's occultation at Taurus, Jupiter's apparition at Gemini and Mars's apparition at Pisces.
- At Saturn's occultation at Capricornus, Theon's 16° 56′ and the printed 16° 6′ both lie about 25′ from the computation. The codex, the Spanish version and the Alphonsine tables have 16° 36′, 4′ from it.

## Nallino's notes on these pages (Part II, pp. 255–269)

- **Sources.** The tables are treated in chapter XLVIII (t. I, pp. 117–118), which teaches their use. Ptolemy treats the phases of the planets with respect to the Sun in Almagest XIII 7–10, with necessarily different tables. The inferior planets have both a morning and an evening apparition and occultation; Nallino explains this after Barhebraeus.
- **Ptolemy's method.**
  - The elongation needed depends on the planet's magnitude, the angle of the horizon with the ecliptic, and the planet's latitude.
  - Ptolemy keeps one arc fixed for each planet, the *arcus visionis*: the arc of the vertical circle between the horizon and the Sun when the planet appears or disappears.
  - From observations in the clime of Phoenicia he found it to be 11° for Saturn, 10° for Jupiter, 11° 30′ for Mars, 5° for Venus and 10° for Mercury.
  - Nallino reduces the computation to the rule above (exactly, sin elongation = sin arcus visionis / sin θ, the difference being negligible), and gives Ptolemy's statement that he built his tables in this way for the beginnings of the signs.
- **Why al-Battānī's table differs from Ptolemy's.** It is for latitude 36°, not about 33°. The obliquity differs. Precession has changed the latitudes of the planets at given longitudes.
- **The latitudes.** Neither Ptolemy nor al-Battānī says how the latitudes were taken. Nallino spent much time in vain on the construction. Neither the astronomers from Peurbach to Riccioli nor Delambre and the later historians attempted it (or perhaps they gave it up), so he could not emend the codex with certainty.
  - The kind of phase follows from the corrected anomaly. Theon and al-Battānī (t. I, p. 117) give the anomalies near which the phases occur somewhat differently from Ḥabash (table on p. 258).
  - From the symmetries of the tables Nallino infers where the nodes lie. Saturn's nodes are near the middle of Cancer and Capricorn: al-Battānī's apogee 244° 28′ less 50° gives the northern limit 194° 28′. Jupiter's are 4½° after the beginnings of Cancer and Capricorn: the limit is at 184° 28′. In Mars he finds that al-Battānī neglected the latitude: its nodes lie at 36° 58′ and 216° 58′ and its greatest latitudes are 4° 21′ N and 7° 7′ S, but near the anomaly of 20° the latitude is only 11′ N and 5′ S, and its effect at most 5′–7′.
- **Origin.** Whether al-Battānī computed the tables or received them is uncertain. The passage t. III, p. 178 can be read «wuḍiʿat» («were set down») or «waḍaʿtu» («I set down»); Nallino holds the first (p. 266).
  - Copyists' errors apart, the numbers agree with Ḥabash's table for the fourth clime (φ = 36°). The Alphonsine tables took over the same table without naming its source.
  - The Alphonsine errors are European. 77′ for 27′ (Venus, occasus matutinus, Sagittarius). 32′ for 23′ and 88′ for 8′ (Mercury, ortus matutinus, Taurus and Libra). 31′ for 0′ (Venus, ortus vespertinus, Aries), probably because an Arabic copy marked a zero with لا («not»), which the translator took for the numeral 31.
- **Theon.** The table of Theon's Canones (t. III, pp. 30–31) is Ptolemy's. His tables for the seven climes (t. III, pp. 16–29, longest days from 13 to 16 hours by half hours) differ entirely from Ptolemy's, and those of the fourth clime agree with al-Battānī's. Halma's edition is full of errors, but with the Greek readings the errors of the codex can almost everywhere be corrected.
  - Theon's obliquity, 23° 51′, changes the angles only slightly: 30° 9′, 31° 49′, 50° 1′, 63° 36′, 74° 4′ at Aries, Taurus, Cancer, Leo, Virgo, against al-Battānī's 30° 25′, 32° 26′, 50° 5′, 63° 31′, 73° 50′.
  - The apogees Theon uses do not fit the tables, while al-Battānī's do (p. 259), so the origin of the tables remains perplexing.
- **The ruling (p. 269).** The readings of Theon and of the Latin Almagest, and the restoration of the 2° of the evening setting of Venus, are applied as described above.
  - The codex's arrangement of the four columns of Venus and Mercury under the general titles «apparitio» and «occultatio» can hardly be right: the two risings belong under apparition and the two settings under occultation.
  - The Spanish version avoids this, heading all four «parescimiento de Venus (Mercurio) et so ascondimiento».

## Conventions

- The first row carries the marks as printed: ° and ′.
- The sign names end with a period, as printed.
- The head of the apparition of Venus is printed رؤية الزسرة for الزهرة. This edition prints it as it stands; `apparitions_pages.tsv` marks it with `{rd:س=ه}`.
- The title of p. 142 has للرؤية, that of p. 143 للروية.
- In the first head of Venus the ل of العشيات is printed short, so that the word looks like انعشيات.
- The heads of p. 143 write the zero of «a 0°» with the zero sign.
- These pages have no signatures.

## Tools

`tools/` holds the scripts that read the pages:

- `apparition_pages.py`: the eye reading;
- `build_apparitions.py`: writes the two data files;
- the shared readers.

The scripts here:

- `python write_apparitions_ledger.py` writes the ledger. The notes of the noted entries are generated from the readings and the computation.
- `python check_apparitions.py` checks the data; `--stats` gives the computation of each column, `--list` the ledgered differences.
- `python gen_apparitions.py` writes `p2_apparitions.tex` (XeLaTeX).
