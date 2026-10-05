# S06 — Sines, declination and right ascensions (Part II pp. 55–58)

Tables of spherical astronomy (codex fol. 176,v.–178,r.):

| Page | Table | Rows |
|---|---|---|
| 55–56 | sines of every half degree in a circle of radius 60: the arc, its supplement, and the sine in parts, minutes and seconds; three sections to a page | 180 |
| 57–58 | the declination of the Sun from the equator for every degree of longitude, with the four arcs of the ecliptic that have that declination (λ, 180° − λ, 180° + λ, 360° − λ) | 90 |
| 58 | figure: the orders of declination in ascent and descent | — |
| 58 | the right ascensions of every tenth degree of longitude, and their sines | 9 |

## Read

- [Part II pp. 55–58, 4 pp.](p2_spherical.pdf).

## Data

| File | Content |
|---|---|
| `sines_p2.tsv` | The sines: page, section, row, arc, supplement, sine (parts, minutes, seconds), how each number was established (`check`). |
| `decl_p2.tsv` | The declinations: page, half, row, longitude λ, declination (degrees, minutes, seconds), the four arcs as printed, `check`. |
| `ra10_p2.tsv` | The right ascensions of the decades and their sines, `check`, notes. |
| `sph_pages.tsv` | Folio lines, Arabic and Latin titles and heads. |
| `fig58.tsv` | The labels of the figure on p. 58: the four directions, the four signs, the four orders, the 24 cells of the band. |
| `spherical_discrepancies.tsv` | The one difference found. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and matched against its computed value (1,431 numbers in class A, both readers give the value; 135 in class B, one reader gives it, each cell checked by eye; 18 in class E, read by eye). `python check_spherical.py` recomputes the tables:

- **sines**: 60 sin θ. Of the 180 sines, 148 agree to the second, 31 differ by 1″ and one by 2″. Every supplement is 180° − θ.
- **declination**: sin δ = sin λ · sin 23° 35′, al-Battānī's obliquity. Of the 90 declinations, 59 agree to the second, 30 differ by 1″ and one by 2″. Every arc of equal declination is exact.
- **right ascensions**: tan α = cos 23° 35′ · tan λ, and their sines 60 sin α. The 18 values differ by at most 3″, except one, which is ledgered:
  - **p. 58, the sine of the ascension of 20°**: printed 18ᵖ 57′ 10″ for 18ᵖ 59′ 9″. The printed ascension 18° 26′ 51″ lies between 18° 0′ and 18° 30′, whose sines on p. 55 are 18ᵖ 32′ 27″ and 19ᵖ 2′ 18″; the seconds agree.

## Nallino's notes on these pages (Part II, pp. 220–221)

- **pp. 55–56**: Nallino corrected 74 errors of the codex in the minutes and seconds of the 180 sines. He compared them with Ptolemy's chords (Almagest I 9, as corrected by Delambre) and with the sines for every 15′ computed by Aboul Hhassan, and recomputed doubtful values with logarithms. The sines agree very well with Ptolemy's.
- **pp. 57–58**: Ptolemy's and Theon's tables of declination are computed for the obliquity 23° 51′ 20″, so Schiaparelli corrected al-Battānī's tables by computation, leaving differences of 1″ or 2″.
- **p. 58, the figure**: in the codex figure the words for ascent and descent are interchanged, and the scribe wrote mankūs («inverted») beside both sides of the circle; the Spanish version has the same errors.
- **p. 58, the right ascensions**: they are counted from the beginning of Aries, while those of pp. 61–64 are counted from the beginning of Capricorn. In the title of the third column the codex reads «ازمان … المنصّفة» («half times») for «اوتار … المنصّفة» («half chords», sines). Ptolemy (Almagest II 8) gives the right ascensions of the decades too, without their sines and for another obliquity.

## Conventions

- The first row of each table carries its marks as printed: ° ′ for the arcs, ᵖ ′ ″ for the sines (parts of the radius 60), ° ′ ″ for the declinations and the ascensions, ° for the arcs of equal declination; the sines of the ascensions are marked ° ′ ″.
- The sines of the ascensions on p. 58 are printed in bold type, and so are they here.
- In the heads of p. 55 the third «الاوتار المنصفة» is printed «لاوتار المنصفة», without its alif, and the c of «descriptorum» in the title is damaged. The heads of p. 56 and of the right half of p. 57 are in Latin only.
- The figure is redrawn from the print: a circle with an inscribed square, whose band holds the degrees 0°, 15° … 90° of the four quarters; the signs inside; the orders of declination between the square and the circle, their tops toward the circle; the four directions outside, with south (Meridies) at the top and east (Oriens) at the left. The right edge of the printed figure falls outside the scanned page: the label there is supplied as «[Occidens]» from the scan's text layer, which reads «Weedens» at that place; its Arabic is not visible.

## Credits

- al-Battānī: the tables and the figure.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the corrected tables of declination.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
