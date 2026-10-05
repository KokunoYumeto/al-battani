# S13 — The circular diagrams, in both of Nallino's versions

Part III prints two circular figures of the codex after the tables, on pp. 243 and 244: the diagram of the seven climes and an astrological figure. Part II gives Nallino's Latin version of each, on p. 92 and p. 299.

Each figure is transcribed from the scan as printed. Neither version is corrected from the other. The editions redraw each figure on the geometry measured from the scan (centre, ring radii, line angles), with every text at its printed place and in its printed orientation.

| Figure | Part III (Arabic) | Part II (Latin) |
|---|---|---|
| The seven climes | p. 243 (master PDF 909), codex fol. 196,v. | p. 92 (master PDF 541) |
| The astrological figure | p. 244 (master PDF 908), codex fol. 197,r. | p. 299 (master PDF 748) |

Angles in the data are degrees counterclockwise from the right-hand horizontal of the page.

## The diagram of the seven climes

The diagram gives, for each of the seven climes, the horizon distances of the rising and setting points of the beginnings of the signs (their ortive and occasive amplitudes): how far north or south of the equinoctial rising and setting point each sign begins to rise and set. The figure is a set of seven concentric rings, one per clime from the innermost (the first clime) to the outermost (the seventh), cut by sixteen radial lines.

- Each line carries the amplitude of the beginnings of two signs with the same declination, in degrees and minutes on its two sides: Pisces and Scorpio (with Taurus and Virgo), Aquarius and Sagittarius (with Gemini and Leo), Capricorn and Cancer. The horizontal line, the equinoxes (Aries, Libra), carries zeros.
- The vertical line at the top, the azimuth of the south, gives the climes and their latitudes; the one at the bottom, the azimuth of the north, gives the longest day of each clime in hours.
- Inside the innermost circle stand sixteen Greek wind names in Arabic transcription, much corrupted. In the four corners of the page are the winter and summer risings and settings of the sun, each with a further Greek name.

Nallino discusses the figure, the wind names and their Greek forms in his note *Ad pag. 92* (Part II pp. 232–235). A passage of the note signed by Schiaparelli points out that the figure, like the one in the Almagest, puts the solstitial risings and settings 22½° from the meridian, which fits no real horizon, and that the wind names were probably added by a later Greek hand.

### Read

- [Part III edition, 1 p.](p3_climates.pdf) and [Part II edition, 1 p.](p2_climates.pdf).

### Data

| File | Content |
|---|---|
| `climates_p3.tsv` | Part III: header, title, corner texts, the labels outside the outer circle (with their measured angle and radius), every ring cell (line, ring, degrees or minutes), the cells of the axes, the sixteen names of the inner circle; reading notes in `doubt`. |
| `climates_p2.tsv` | Part II: the same items for the Latin figure. |
| `climates_names_p2.tsv` | Nallino's table of the wind names (Part II p. 234): azimuth, direction, the name in the Almagest, the name in the codex, his probable restoration in Arabic and Greek. |
| `climates_discrepancies.tsv` | The differences between Part III and Part II, each checked in two scan copies. |

The page has south at the top (90) and east on the left (180); Nallino's azimuths in his table are counted from the south through the east, so azimuth = angle − 90.

### How the two versions were checked

Every Part III number was read at 420–2600 dpi on unrolled images of the rings, in the master scan and in a second copy of the print (Internet Archive). `python check_climates.py` decodes the abjad and compares:

| Result | Items |
|---|---|
| Agree with Part II (ring cells, zeros, climes, latitudes, hours, names) | 203 |
| Differ (ledgered, both copies) | 27 |
| Open | 0 |

- **24 values** differ, in 23 cells: 22 minutes and 2 degrees. Most differ in one letter, usually the tens: يط (19) for لط (39), كه (25) for مه (45), مط (49) for كط (29). The same cell in the other quadrants usually has the value of Part II. Two cells have it in no quadrant: the minutes of the first clime on the Capricorn and Cancer lines (لط 39 three times and يط 19 once, for 41) and those of the sixth clime on the same lines (نز 57 twice, يز 17, لز 37, for 43).
- **3 names** differ from the codex forms in Nallino's table: Part III shows the dot of the ف in رهفرس, the dot of the ن in سعانس and a dotted tooth in لبعوس, where the table prints رهڡرس, سعاىس and لعوس.
- **The Latin values** agree with the amplitudes computed from sin A = sin δ / cos φ, with al-Battānī's obliquity 23;35 and the clime latitudes of Nallino's note: all 21 within 2′ (largest difference 1.7′).

## The astrological figure

The figure lists, for each of the twelve signs, the planets that rule parts of it in astrology. From the outside inward:

- **The terms** (*ḥudūd*): the sign is divided among the five planets, each ruling a stretch of degrees; the five stretches add up to 30.
- **The triplicities** (*muthallathāt*): the lord by day, the lord by night and a partner, the same for the three signs of each triplicity.
- **The faces** (decans): each third of a sign, ten degrees, has a planet.
- **The house** (domicile) of each sign and its **exaltation**: the planet exalted in the sign and the degree of its exaltation. The codex also gives the exaltations of the lunar nodes, the Head in Gemini 3° and the Tail in Sagittarius 3°.

A line below the figure names the circles and adds that the figure is «not from the archetype». In Part II (pp. 308–313) Nallino explains why he regards this figure and the tables he prints after it (Part II pp. 300–307) as not al-Battānī's: al-Battānī never mentions the figure, and it concerns judicial astrology only. Nallino also compares the doctrines of terms, triplicities, faces, houses and exaltations with Ptolemy's *Tetrabiblos* and the Arabic astrologers.

In the codex the figure is badly drawn. Nallino (p. 309) says that its two innermost circles, houses and exaltations, had merged into one, and that the copyist kept the number five by splitting the circle of the triplicities in two. Part III prints the codex figure with these features and with the codex's numbers, errors included («Codicis errores etiam in circulorum descriptione servavi»). Part II gives an emended figure. Its terms follow the *Tetrabiblos* in the Frankfurt version («omnia emendavi ad fidem versionis Francofurtensis Tetrabibli»), and it gives the triplicities with the outer half for the day and the inner half for the night.

### Read

- [Part III edition, 1 p.](p3_rosa.pdf) and [Part II edition, 1 p.](p2_rosa.pdf).

### Data

| File | Content |
|---|---|
| `rosa_p3.tsv` | Part III: header, title line, closing line, footnotes, the twelve sign names (measured angle), and for each sign the five terms (planet, degrees as printed), the two triplicity rings, the three faces, the cell of the merged inner ring as printed (lines separated by « / ») and the house and exaltation read from it; reading notes in `doubt`. |
| `rosa_p2.tsv` | Part II: the same items for the Latin figure; triplicities and exaltations as Nallino's planet symbols. |
| `rosa_discrepancies.tsv` | The differences between Part III and Part II, each checked in two scan copies of Part III, and a note on Nallino's footnote marks. |

### How the two versions were checked

The Part III figure was read at 500–2600 dpi on straightened radial strips and unrolled rings, in both copies of the print. `python check_rosa.py` compares every item, with the planets mapped to one key (Arabic names, Latin names, symbols; the Persian بهرام for Mars, which Nallino notes on p. 308) and the abjad decoded:

| Result | Items |
|---|---|
| Agree with Part II | 189 |
| Differ: term degrees that Nallino emended to Ptolemy's terms | 27 |
| Differ: the exaltation degree that Nallino's note names (Jupiter in Cancer, 14 for 15, p. 313) | 1 |
| Open | 0 |

- Every planet agrees: the order of the terms in all twelve signs, all 24 triplicity rows, all 36 faces, the twelve houses and the exaltations.
- The five terms add up to 30 in every sign of Part II, and in 8 of 12 signs of Part III: Aries and Virgo give 29, Gemini 28, Scorpio 34.
- Nallino attaches his footnote on the codex reading البروج / *signorum* to different words in the two parts: in Part III to البيوت (the houses), in Part II to *facierum* (the faces). Both are kept as printed and noted in the ledger.

## Conventions

As in the star catalogue (see `../star_catalogue/README.md`). In addition:
- **The sides of a line (climes).** The degrees always stand on the side of the line toward the horizontal axis, the minutes toward the vertical axis. The column heads درج and دقائق stand above the matching columns at 67.5° and 247.5°, and above the opposite columns at 112.5° and 292.5°; they are entered where they are printed.
- **Orientation.** Texts written along the circles have their tops outward, so the lower half of each figure reads upside down on the page; the climes values of Part II are the exception and stand upright. Texts written along the radius start at the inner circle in Part III (the sign names of p. 243 start at the outer circle); in Part II they start at the outer end. The order of the terms and faces runs counterclockwise, as the signs do.
- **The top and bottom labels** of p. 243, سمت الجنوب and سمت الشمال, end in an overlined ض, the Maghribi 90 (Part II: *Azimuth meridiei, 90°*, *Azimuth septentrionis, 90°*).
- **The zero sign** of the codex stands in the inner ring of p. 244 where a sign has no exaltation (Leo, Scorpio, Aquarius); Part II prints «0°».
- **Dotless letters** keep their printed form: ى for a dotless tooth, ڡ for a dotless fā', ٮ for a dotless final bowl. Where one copy shows a mark the other lacks (a dot high above the tooth of بعدىاس in the master only), the reading follows the two copies' agreement and the note says so. One face on p. 244 is printed مشترب, with one dot under the final bowl in both copies.
- **The free stroke** in the name at 247.5° on p. 243 (افر…ىطس in Nallino's table) is entered as `{stroke}`.
- **Latin misprints** stay as printed: *Verus* and *Venns* for *Venus* in the terms of p. 299.

## Not done yet

- Nallino's notes on the two figures in Part II, *Ad pag. 92* (pp. 232–235) and *Ad pag. 299* (pp. 308–313), beyond the table of wind names.

## Credits

- al-Battānī and the codex: the figures.
- C. A. Nallino: the edition of the codex (Part III), the Latin versions and the notes (Part II), Milan 1899–1907; G. V. Schiaparelli for the passages of the note on p. 92 signed by him.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
