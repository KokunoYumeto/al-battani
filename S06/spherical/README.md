# S06 — Sines, declination, ascensions, the longest day and shadows (Part II pp. 55–60)

Tables of spherical astronomy (codex fol. 176,v.–179,r.):

| Page | Table | Rows |
|---|---|---|
| 55–56 | sines of every half degree in a circle of radius 60: the arc, its supplement, and the sine in parts, minutes and seconds; three sections to a page | 180 |
| 57–58 | the declination of the Sun from the equator for every degree of longitude, with the four arcs of the ecliptic that have that declination (λ, 180° − λ, 180° + λ, 360° − λ) | 90 |
| 58 | figure: the orders of declination in ascent and descent | — |
| 58 | the right ascensions of every tenth degree of longitude, and their sines | 9 |
| 59 | half the increase of the longest day over 12 hours, in degrees of the equator (15° to an hour), for the latitudes 0° 30′ … 60°; three sections | 120 |
| 60 | the shadow of a gnomon of 12 digits for the altitudes 1° … 90°, in digits and minutes; three sections | 90 |

## Read

- [Part II pp. 55–60, 6 pp.](p2_spherical.pdf).

## Data

| File | Content |
|---|---|
| `sines_p2.tsv` | The sines: page, section, row, arc, supplement, sine (parts, minutes, seconds), how each number was established (`check`). |
| `decl_p2.tsv` | The declinations: page, half, row, longitude λ, declination (degrees, minutes, seconds), the four arcs as printed, `check`. |
| `ra10_p2.tsv` | The right ascensions of the decades and their sines, `check`, notes. |
| `days59_p2.tsv` | Half the increase of the longest day: section, row, latitude, value (degrees, minutes), `check`. |
| `shadows60_p2.tsv` | The shadows: section, row, altitude, shadow (digits, minutes), `check`. |
| `sph_pages.tsv` | Folio lines, Arabic and Latin titles and heads. |
| `fig58.tsv` | The labels of the figure on p. 58: the four directions, the four signs, the four orders, the 24 cells of the band. |
| `spherical_discrepancies.tsv` | The differences found: one value and two runs. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and matched against its computed value; on p. 59 every value was also read by eye, because the table departs from the computation. 1,811 numbers are in class A (both readers give the value), 172 in class B (one reader gives it; each cell checked by eye), 21 in class E (read by eye). `python check_spherical.py` recomputes the tables:

- **sines**: 60 sin θ. Of the 180 sines, 148 agree to the second, 31 differ by 1″ and one by 2″. Every supplement is 180° − θ.
- **declination**: sin δ = sin λ · sin 23° 35′, al-Battānī's obliquity. Of the 90 declinations, 59 agree to the second, 30 differ by 1″ and one by 2″. Every arc of equal declination is exact.
- **right ascensions**: tan α = cos 23° 35′ · tan λ, and their sines 60 sin α. The 18 values differ by at most 3″, except one, which is ledgered:
  - **p. 58, the sine of the ascension of 20°**: printed 18ᵖ 57′ 10″ for 18ᵖ 59′ 9″. The printed ascension 18° 26′ 51″ lies between 18° 0′ and 18° 30′, whose sines on p. 55 are 18ᵖ 32′ 27″ and 19ᵖ 2′ 18″; the seconds agree.
- **the longest day** (p. 59): half the increase is arcsin(tan φ · tan 23° 35′). 55 of the 120 values agree to the minute, 36 differ by 1′, 9 by 2′, and 20 by 3′ to 7′. Every value more than 3′ from the computation lies in one of two runs, in which the printed values lie above it:
  - **latitudes 5° to 10° 30′**: the printed values rise by 14′ for every half degree from 5° to 8°, where the computed rise is about 13⅓′, and by 13′ and 12′ alternately from 8° to 10°. They exceed the computation by more than 3′ from 7° to 9° (by 5.0′ at 8°: printed 3° 36′, computed 3° 31.0′).
  - **latitudes 21° to 29° 30′**: the excess reaches 6.9′ at 25° 30′ (printed 12° 8′, computed 12° 1.1′) and is more than 3′ from 24° to 28° 30′; at 30° the table agrees again.
  Every value of p. 59 was read by eye; the ledger lists the two runs with all their printed and computed values.
- **shadows** (p. 60): 12 cot h. 79 of the 90 shadows agree to the minute, 11 differ by 1′.

## Nallino's notes on these pages (Part II, pp. 220–221)

- **pp. 55–56**: Nallino corrected 74 errors of the codex in the minutes and seconds of the 180 sines. He compared them with Ptolemy's chords (Almagest I 9, as corrected by Delambre) and with the sines for every 15′ computed by Aboul Hhassan, and recomputed doubtful values with logarithms. The sines agree very well with Ptolemy's.
- **pp. 57–58**: Ptolemy's and Theon's tables of declination are computed for the obliquity 23° 51′ 20″, so Schiaparelli corrected al-Battānī's tables by computation, leaving differences of 1″ or 2″.
- **p. 58, the figure**: in the codex figure the words for ascent and descent are interchanged, and the scribe wrote mankūs («inverted») beside both sides of the circle; the Spanish version has the same errors.
- **p. 59**: Schiaparelli corrected the table. The increase of the days is given in degrees of the equator, 15° to an equinoctial hour.
- **p. 60**: the shadows are cotangents for a radius of 12 parts, and Nallino corrected the errors of the codex with logarithms. The codex gives the first two shadows as 687ᵖ 26′ and 663ᵖ 39′ (the letters خصج for سمج, 343); the small differences in the minutes may come from al-Battānī himself, who could have found them by dividing sines computed only to the second.
- **p. 58, the right ascensions**: they are counted from the beginning of Aries, while those of pp. 61–64 are counted from the beginning of Capricorn. In the title of the third column the codex reads «ازمان … المنصّفة» («half times») for «اوتار … المنصّفة» («half chords», sines). Ptolemy (Almagest II 8) gives the right ascensions of the decades too, without their sines and for another obliquity.

## Conventions

- The first row of each table carries its marks as printed: ° ′ for the arcs, ᵖ ′ ″ for the sines (parts of the radius 60), ° ′ ″ for the declinations and the ascensions, ° for the arcs of equal declination; the sines of the ascensions are marked ° ′ ″.
- The sines of the ascensions on p. 58 are printed in bold type, and so are they here.
- In the heads of p. 55 the third «الاوتار المنصفة» is printed «لاوتار المنصفة», without its alif, and the c of «descriptorum» in the title is damaged. The heads of p. 56 and of the right half of p. 57 are in Latin only.
- The first row of p. 60 marks the digits of the shadow «dig.», as printed.
- The figure is redrawn from the print: a circle with an inscribed square, whose band holds the degrees 0°, 15° … 90° of the four quarters; the signs inside; the orders of declination between the square and the circle, their tops toward the circle; the four directions outside, with south (Meridies) at the top and east (Oriens) at the left. The right edge of the printed figure falls outside the scanned page: the label there is supplied as «[Occidens]» from the scan's text layer, which reads «Weedens» at that place; its Arabic is not visible.

## Credits

- al-Battānī: the tables and the figure.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the corrected tables of declination and of the longest day.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
