# S13 — The circular diagrams, in both of Nallino's versions

## The diagram of the seven climes

The diagram gives, for each of the seven climes, the horizon distances of the rising and setting points of the beginnings of the signs (their ortive and occasive amplitudes): how far north or south of the equinoctial rising and setting point each sign begins to rise and set. The figure is a set of seven concentric rings, one per clime from the innermost (the first clime) to the outermost (the seventh), cut by sixteen radial lines.

- Each line carries the amplitude of the beginnings of two signs with the same declination, in degrees and minutes on its two sides: Pisces and Scorpio (with Taurus and Virgo), Aquarius and Sagittarius (with Gemini and Leo), Capricorn and Cancer. The horizontal line, the equinoxes (Aries, Libra), carries zeros.
- The vertical line at the top, the azimuth of the south, gives the climes and their latitudes; the one at the bottom, the azimuth of the north, gives the longest day of each clime in hours.
- Inside the innermost circle stand sixteen Greek wind names in Arabic transcription, much corrupted. In the four corners of the page are the winter and summer risings and settings of the sun, each with a further Greek name.

Nallino discusses the figure, the wind names and their Greek forms in his note *Ad pag. 92* (Part II pp. 232–235). A passage of the note signed by Schiaparelli points out that the figure, like the one in the Almagest, puts the solstitial risings and settings 22½° from the meridian, which fits no real horizon, and that the wind names were probably added by a later Greek hand.

| Witness | Pages | What it is |
|---|---|---|
| **Part III** (Arabic) | printed p. 243 (master PDF 909) | The figure of the codex (Escorial, ár. 908, fol. 196,v.), with its numbers in Maghribi abjad and the codex's zero sign. |
| **Part II** (Latin) | printed p. 92 (master PDF 541) | Nallino's Latin figure: Western numerals, the same layout, the wind names restored. |

Both are transcribed from the scan as printed. Neither is corrected from the other.

## Read

- [Part III edition, 1 p.](p3_climates.pdf): the Arabic figure, drawn on the measured geometry of the print, every text at its printed place and in its printed orientation.
- [Part II edition, 1 p.](p2_climates.pdf): the Latin figure.

## Data

| File | Content |
|---|---|
| `climates_p3.tsv` | Part III: header, title, corner texts, the labels outside the outer circle (with their measured angle and radius), every ring cell (line, ring, degrees or minutes), the cells of the axes, the sixteen names of the inner circle; reading notes in `doubt`. |
| `climates_p2.tsv` | Part II: the same items for the Latin figure. |
| `climates_names_p2.tsv` | Nallino's table of the wind names (Part II p. 234): azimuth, direction, the name in the Almagest, the name in the codex, his probable restoration in Arabic and Greek. |
| `climates_discrepancies.tsv` | The differences between Part III and Part II, each checked in two scan copies. |
| `rows/` | The reading files from which `build_climates.py` writes the TSV data. |

Angles are degrees counterclockwise from the right-hand horizontal of the page. The page has south at the top (90) and east on the left (180); Nallino's azimuths in his table are counted from the south through the east, so azimuth = angle − 90.

## How the two versions were checked

Every Part III number was read at 420–2600 dpi on unrolled images of the rings, in the master scan and in a second copy of the print (Internet Archive). `python check_climates.py` decodes the abjad and compares:

| Result | Items |
|---|---|
| Agree with Part II (ring cells, zeros, climes, latitudes, hours, names) | 203 |
| Differ (ledgered, both copies) | 27 |
| Open | 0 |

- **24 values** differ, in 23 cells: 22 minutes and 2 degrees. Most differ in one letter, usually the tens: يط (19) for لط (39), كه (25) for مه (45), مط (49) for كط (29). The same cell in the other quadrants usually has the value of Part II. Two cells have it in no quadrant: the minutes of the first clime on the Capricorn and Cancer lines (لط 39 three times and يط 19 once, for 41) and those of the sixth clime on the same lines (نز 57 twice, يز 17, لز 37, for 43).
- **3 names** differ from the codex forms in Nallino's table: Part III shows the dot of the ف in رهفرس, the dot of the ن in سعانس and a dotted tooth in لبعوس, where the table prints رهڡرس, سعاىس and لعوس.
- **The Latin values** agree with the amplitudes computed from sin A = sin δ / cos φ, with al-Battānī's obliquity 23;35 and the clime latitudes of Nallino's note: all 21 within 2′ (largest difference 1.7′).

## Conventions

As in the star catalogue (see `../star_catalogue/README.md`). In addition:
- **The sides of a line.** The degrees always stand on the side of the line toward the horizontal axis, the minutes toward the vertical axis. The column heads درج and دقائق stand above the matching columns at 67.5° and 247.5°, and above the opposite columns at 112.5° and 292.5°; they are entered where they are printed.
- **Orientation.** The ring cells of Part III are written along the circles with their tops outward, so the lower half reads upside down on the page. The sign names outside the outer circle start at the circle and run outward; the names inside the innermost circle start at that circle and run inward. Part II keeps its values upright on the page.
- **The top and bottom labels** سمت الجنوب and سمت الشمال end in an overlined ض, the Maghribi 90 (Part II: *Azimuth meridiei, 90°*, *Azimuth septentrionis, 90°*).
- **Dotless letters** keep their printed form: ى for a dotless tooth, ڡ for a dotless fā', ٮ for a dotless final bowl. Where one copy shows a mark the other lacks (a dot high above the tooth of بعدىاس in the master only), the reading follows the two copies' agreement and the note says so.
- **The free stroke** in the name at 247.5° (افر…ىطس in Nallino's table) is entered as `{stroke}`.

## Not done yet

- The second diagram, Part III p. 244 (fol. 197,r., the planets' terms, triplicities, faces, houses and exaltations), which has no Latin figure in Part II.
- Nallino's note *Ad pag. 92* (Part II pp. 232–235) beyond the table of names: the Greek and Latin text of the note itself.

## Credits

- al-Battānī: the diagram.
- C. A. Nallino: the edition of the codex (Part III), the Latin version and the notes (Part II), Milan 1899–1907; G. V. Schiaparelli for the passages of the note signed by him.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
