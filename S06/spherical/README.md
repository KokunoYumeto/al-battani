# S06 — Sines, declination, ascensions, the longest day, shadows and the equation of days (Part II pp. 55–71)

Tables of spherical astronomy (codex fol. 176,v.–186,r.):

| Page | Table | Rows |
|---|---|---|
| 55–56 | sines of every half degree in a circle of radius 60: the arc, its supplement, and the sine in parts, minutes and seconds; three sections to a page | 180 |
| 57–58 | the declination of the Sun from the equator for every degree of longitude, with the four arcs of the ecliptic that have that declination (λ, 180° − λ, 180° + λ, 360° − λ) | 90 |
| 58 | figure: the orders of declination in ascent and descent | — |
| 58 | the right ascensions of every tenth degree of longitude, and their sines | 9 |
| 59 | half the increase of the longest day over 12 hours, in degrees of the equator (15° to an hour), for the latitudes 0° 30′ … 60°; three sections | 120 |
| 60 | the shadow of a gnomon of 12 digits for the altitudes 1° … 90°, in digits and minutes; three sections | 90 |
| 61–64 | for every degree of each sign, from Capricorn to Sagittarius: the right ascension counted from the beginning of Capricorn, and the equation of days with their nights; three signs to a page | 360 |
| 65–66 | the oblique ascensions of every tenth degree, counted from Aries, for the latitudes of the seven climes and the latitudes between them, whose longest days differ by a quarter of an hour (13ʰ to 16ʰ; latitudes 16° 39′ to 48° 53′) | 36 × 13 |
| 67 | the oblique ascensions of every tenth degree and the seasonal hours (the length of an hour of the day in degrees of the equator) for Mekkah (21° 40′), Baghdād (33° 9′) and Ḥarrān (36° 40′) | 36 × 6 |
| 68–71 | the oblique ascensions of every degree of the ecliptic, counted from Aries, at ar-Raqqah (latitude 36° 0′, longest day 14ʰ 28ᵐ), with the seasonal hours; three signs to a page | 360 |

## Read

- [Part II pp. 55–71, 17 pp.](p2_spherical.pdf).

## Data

| File | Content |
|---|---|
| `sines_p2.tsv` | The sines: page, section, row, arc, supplement, sine (parts, minutes, seconds), how each number was established (`check`). |
| `decl_p2.tsv` | The declinations: page, half, row, longitude λ, declination (degrees, minutes, seconds), the four arcs as printed, `check`. |
| `ra10_p2.tsv` | The right ascensions of the decades and their sines, `check`, notes. |
| `days59_p2.tsv` | Half the increase of the longest day: section, row, latitude, value (degrees, minutes), `check`. |
| `shadows60_p2.tsv` | The shadows: section, row, altitude, shadow (digits, minutes), `check`. |
| `raeq_p2.tsv` | Right ascensions and the equation of days: page, row, sign, longitude, ascension and equation (degrees, minutes), `check`. |
| `oblique_p2.tsv` | The oblique ascensions (and on p. 67 the seasonal hours): page, row, tenth degree, sign, one pair of columns (degrees, minutes) for each latitude, `check`. |
| `oblique_columns.tsv` | What each column of `oblique_p2.tsv` holds. |
| `raqqah_p2.tsv` | ar-Raqqah: page, row, sign, longitude, ascension and seasonal hour (degrees, minutes), `check`, notes. |
| `sph_pages.tsv` | Folio lines, Arabic and Latin titles and heads. |
| `fig58.tsv` | The labels of the figure on p. 58: the four directions, the four signs, the four orders, the 24 cells of the band. |
| `spherical_discrepancies.tsv` | The differences found on pp. 55–71, and the hour that Nallino corrects on p. 71. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer and matched against its computed value; on p. 59 every value was also read by eye, because the table departs from the computation, and on pp. 61–64 the equation of days was resolved by the agreement of the two readers and every disputed cell read by eye. 5,638 numbers are in class A (both readers give the value), 519 in class B (one reader gives it; each cell checked by eye), 95 in class E (read by eye). `python check_spherical.py` recomputes the tables:

- **sines**: 60 sin θ. Of the 180 sines, 148 agree to the second, 31 differ by 1″ and one by 2″. Every supplement is 180° − θ.
- **declination**: sin δ = sin λ · sin 23° 35′, al-Battānī's obliquity. Of the 90 declinations, 59 agree to the second, 30 differ by 1″ and one by 2″. Every arc of equal declination is exact.
- **right ascensions**: tan α = cos 23° 35′ · tan λ, and their sines 60 sin α. The 18 values differ by at most 3″, except one, which is ledgered:
  - **p. 58, the sine of the ascension of 20°**: printed 18ᵖ 57′ 10″ for 18ᵖ 59′ 9″. The printed ascension 18° 26′ 51″ lies between 18° 0′ and 18° 30′, whose sines on p. 55 are 18ᵖ 32′ 27″ and 19ᵖ 2′ 18″; the seconds agree.
- **the longest day** (p. 59): half the increase is arcsin(tan φ · tan 23° 35′). 55 of the 120 values agree to the minute, 36 differ by 1′, 9 by 2′, and 20 by 3′ to 7′. Every value more than 3′ from the computation lies in one of two runs, in which the printed values lie above it:
  - **latitudes 5° to 10° 30′**: the printed values rise by 14′ for every half degree from 5° to 8°, where the computed rise is about 13⅓′, and by 13′ and 12′ alternately from 8° to 10°. They exceed the computation by more than 3′ from 7° to 9° (by 5.0′ at 8°: printed 3° 36′, computed 3° 31.0′).
  - **latitudes 21° to 29° 30′**: the excess reaches 6.9′ at 25° 30′ (printed 12° 8′, computed 12° 1.1′) and is more than 3′ from 24° to 28° 30′; at 30° the table agrees again.
  Every value of p. 59 was read by eye; the ledger lists the two runs with all their printed and computed values.
- **shadows** (p. 60): 12 cot h. 79 of the 90 shadows agree to the minute, 11 differ by 1′.
- **right ascensions from Capricorn** (pp. 61–64): 325 of the 360 agree to the minute, 35 differ by 1′.
- **the equation of days** (pp. 61–64): computed from al-Battānī's elements (obliquity 23° 35′, solar apogee 82° 17′, greatest equation of the Sun 1° 59′ 10″) as the mean longitude of the Sun less the right ascension of its true longitude, made always positive by subtracting the least value of the year. The table's values lie, on the median, 1.0′ below this computation, and 310 of the 360 lie within 3′ of it after that shift. The others lie in four runs, listed in the ledger with all their values:
  - **Gemini 4°–7°**: up to 4.7′ above (Gemini 6°: printed 5° 32′).
  - **Leo 20° to Virgo 10°**: up to 7.3′ below. The printed values rise by 2′ a degree to Leo 22° and by 3′ a degree to Virgo 4° (3° 57′, computed 4° 4.3′), while the computed rise grows from 2′ to 4′; from Virgo 5° they rise by 4′ and 5′ and come back towards the computation.
  - **Libra 16°–25°**: up to 6.3′ above (Libra 21°: printed 7° 34′).
  - **Scorpio 21°–30°**: up to 4.1′ above (Scorpio 24°: printed 7° 31′).
  The computation reconstructs the procedure from al-Battānī's elements; its agreement with the table to about 3′ is the measure of that reconstruction, and smaller differences are not listed.
- **oblique ascensions** (pp. 65–67): the right ascension less arcsin(tan φ · tan δ), for the latitude φ printed in the head of each column, and on p. 67 the seasonal hours (180° + 2 arcsin(tan φ · tan δ)) / 12. Of the 576 ascensions 413 agree to the minute and 124 differ by 1′; of the 108 hours 90 agree and 15 differ by 1′. Every column but those of Ḥarrān fits the latitude of its head within 2.4′ (`python check_spherical.py --lat`). Ledgered:
  - **p. 65, 250°**: printed 267° 32′ for 260° 32′ (latitude 27° 28′) and 260° 16′ for 262° 16′ (30° 40′); across the row the values rise by 1° 44′ from column to column.
  - **p. 65, 210°, latitude 20° 28′**: printed 212° 21′, computed 212° 15.3′.
  - **p. 65, 50°, latitude 16° 39′**: printed 42° 3′, computed 41° 59.9′.
  - **p. 66, 80° and 280°, latitude 43° 25′**: printed 55° 14′ and 304° 46′, 3.2′ from the computation; the column fits 43° 23.4′.
  - **p. 67, the seasonal hours of Baghdād at 320° and 330°**: printed 12° 20′ and 12° 43′ for 13° 20′ and 13° 43′.
  - **p. 67, Ḥarrān**: the ascensions and the seasonal hours both fit the latitude 36° 45′ (36° 44.5′ and 36° 44.8′) rather than the 36° 40′ of the head. The four values most sensitive to the latitude, at 90°–100° and 260°–270°, lie 3.4′ to 3.8′ from the computation for 36° 40′.
- **ar-Raqqah** (pp. 68–71): the same computation for every degree at 36° 0′, which also fits the ascensions best (rms 1.0′). Of the 360 ascensions 104 agree to the minute, 205 differ by 1′ and 51 by 2′; of the 360 seasonal hours 304 agree, 55 differ by 1′ and one by 2′. No value is more than 2′ off. The one hour that Nallino corrects (p. 71, the last line: Aquarius 30°, printed 13° 33′, his 13° 34′) computes to 13° 34.7′.

## Nallino's notes on these pages (Part II, pp. 220–222)

- **pp. 55–56**: Nallino corrected 74 errors of the codex in the minutes and seconds of the 180 sines. He compared them with Ptolemy's chords (Almagest I 9, as corrected by Delambre) and with the sines for every 15′ computed by Aboul Hhassan, and recomputed doubtful values with logarithms. The sines agree very well with Ptolemy's.
- **pp. 57–58**: Ptolemy's and Theon's tables of declination are computed for the obliquity 23° 51′ 20″, so Schiaparelli corrected al-Battānī's tables by computation, leaving differences of 1″ or 2″.
- **p. 58, the figure**: in the codex figure the words for ascent and descent are interchanged, and the scribe wrote mankūs («inverted») beside both sides of the circle; the Spanish version has the same errors.
- **p. 59**: Schiaparelli corrected the table. The increase of the days is given in degrees of the equator, 15° to an equinoctial hour.
- **p. 60**: the shadows are cotangents for a radius of 12 parts, and Nallino corrected the errors of the codex with logarithms. The codex gives the first two shadows as 687ᵖ 26′ and 663ᵖ 39′ (the letters خصج for سمج, 343); the small differences in the minutes may come from al-Battānī himself, who could have found them by dividing sines computed only to the second.
- **pp. 61–64**: the right ascensions are counted from the beginning of Capricorn; 90° must be subtracted to count them from Aries. Ptolemy gives right ascensions only for every tenth degree (see p. 58), and his tables have no equation of time. In al-Battānī the equation of days is always subtracted.
- **pp. 65–66**: the oblique ascensions are counted from the beginning of Aries, not from Capricorn like the right ascensions. They differ from Ptolemy's (Almagest II 8), because the obliquity, and with it the latitudes of the climes, differ. The increase of the ascensions from one quarter hour of the longest day to the next follows a regular proportion, so the errors of the codex were easy to correct; where there was doubt, Nallino computed with al-Battānī's tables of declination and right ascension and the formula sin m = tan φ · tan δ.
- **pp. 68–71**: an Arab-African interpolator added to the titles of the codex that these are also the ascensions of Bigāyah (Bougie) and Almería, and of the places opposite them in the east and the west; the printed titles leave out these additions. On p. 71, last line, the seasonal hour of Aquarius 30° is to be read 13° 34′ for the 13° 33′ of the codex and the translation.
- **p. 67**: the «tempora horaria» (azmān as-sāʿāt, Ptolemy's ὡριαῖοι χρόνοι) are the lengths of the seasonal hours in degrees of the equator, 15° to an equinoctial hour. The next leaf of the codex, f. 183,r., is blank.
- **p. 58, the right ascensions**: they are counted from the beginning of Aries, while those of pp. 61–64 are counted from the beginning of Capricorn. In the title of the third column the codex reads «ازمان … المنصّفة» («half times») for «اوتار … المنصّفة» («half chords», sines). Ptolemy (Almagest II 8) gives the right ascensions of the decades too, without their sines and for another obliquity.

## Conventions

- The first row of each table carries its marks as printed: ° ′ for the arcs, ᵖ ′ ″ for the sines (parts of the radius 60), ° ′ ″ for the declinations and the ascensions, ° for the arcs of equal declination; the sines of the ascensions are marked ° ′ ″.
- The sines of the ascensions on p. 58 are printed in bold type, and so are they here.
- In the heads of p. 55 the third «الاوتار المنصفة» is printed «لاوتار المنصفة», without its alif, and the c of «descriptorum» in the title is damaged. The heads of p. 56 and of the right half of p. 57 are in Latin only.
- The first row of p. 60 marks the digits of the shadow «dig.», as printed.
- The Arabic titles of pp. 68 and 71 give the latitude and the hours of ar-Raqqah in letters: لو (36) and يد كح (14 28); that of p. 71 reads «ولعرض … وساعات» without the article.
- On pp. 61–64 the last ascension of Sagittarius is printed «360 0». On pp. 65–67 the names of the signs stand vertically beside their three tenth degrees, as printed; on p. 65 only the first column has the Arabic head «المطالع», and on p. 66 the head of the second column lacks its final period («Gradus ascension»). The Arabic title of p. 61 has a fatḥa on «وتعَديل»; the Arabic title of p. 64 begins «من جداول» like those of pp. 62–63, while its Latin title begins «Finis tabularum».
- The figure is redrawn from the print: a circle with an inscribed square, whose band holds the degrees 0°, 15° … 90° of the four quarters; the signs inside; the orders of declination between the square and the circle, their tops toward the circle; the four directions outside, with south (Meridies) at the top and east (Oriens) at the left. The right edge of the printed figure falls outside the scanned page: the label there is supplied as «[Occidens]» from the scan's text layer, which reads «Weedens» at that place; its Arabic is not visible.

## Credits

- al-Battānī: the tables and the figure.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907; G. V. Schiaparelli: the corrected tables of declination and of the longest day.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
