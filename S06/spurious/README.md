# S06 — The spurious tables (Part II pp. 297–307)

The tables that follow al-Battānī's own tables in the codex (fol. 240,v.–244,r.), which Nallino prints apart as «Tabulae spuriae»:

- p. 297: the half-title «TABULAE SPURIAE», with the signature 38;
- p. 298 is blank;
- p. 299, the «rosa astrologica», is edited with its Part III counterpart in [S13](../../S13/);
- pp. 300–307 hold eight tables, listed below.

| Page | Table | Rows and columns |
|---|---|---|
| 300 | «Tabula ad invenienda signa initiorum annorum et mensium Arabum. Ex opere astronomico Maslamae.» | the signs (weekdays) of the beginnings of the Arab years: decades 0, 10 … 210 and the years 1 … 9 after each; the months with their days and signs |
| 301 | «Tabula signorum Arabum» and «Tabula signorum Persarum» | the signs of the collected Arab years 30 … 900 and of the single years 1 … 30; the signs of the Arab months; the signs of the twelve Persian months in each of seven columns |
| 302 | «Tabula signorum Syrorum, intercalatione mense Decembri posita secundum methodum Romanorum» | the signs of the twelve months, October … September, for the years 1 … 28; the column of intercalation; the multiples of 28 to be subtracted |
| 303 | «Tabula ad cognoscenda initia annorum et mensium Coptorum; et est intercalatio in fine anni» | the signs of the twelve Coptic months for the years 1 … 28; the bisextiles |
| 304 | «Tabula conversionis aerarum in alias, secundum annos Arabicos collectos» | the Roman, Coptic and Persian years, months, days (and fractions) of the collected Arab years 30 … 660 |
| 305 | «Tabula conversionis aerarum in alias, secundum singulos Arabum annos et menses» | the same for the single Arab years 1 … 30, and the months and days of the Arab months |
| 306 | «Tabula coniunctionum Solis et Lunae in annis Arabicis collectis» | for the collected Arab years 1, 31 … 631: I the days, hours and minutes of the first mean conjunction after the beginning of the year; II the mean longitude of the luminaries; III the anomaly of the Moon; IV the motion of latitude (signs, degrees, minutes, seconds) |
| 307 | «Tabula oppositionum Solis et Lunae in annis Arabicis collectis» | the same for the first mean opposition |

A sign is the number of the weekday: 1 Sunday … 7 Saturday.

## Read

- [Part II pp. 297 and 300–307, 9 pp.](p2_spurious.pdf).

## Data

| File | Content |
|---|---|
| `spurious_p2.tsv` | One row per printed number: page, table, row, argument, column, value, how it was established (`check`), and notes. |
| `spurious_heads.tsv` | The titles and heads of every page in Arabic and Latin, the folio lines and the signatures. |
| `spurious_discrepancies.tsv` | The last two lines of p. 304, which Nallino restored, with the numbers of the codex. No other difference was found. |

## How the tables were read and checked

Every number was read by the glyph reader and by the OCR text layer, against the value the computation of its table gives (below). Of the 2,334 numbers:

- 1,863 are in class A: both readers give the value.
- 384 are in class B: one reader gives it.
  - 252 of them were read by eye on contact sheets beside their computed values.
  - For the other 132 only the glyph reader saw the number, the text layer having no token there. Tesseract confirmed 96 of them, and the other 36 were read by eye. Two of these were misread by the glyph reader, 4 for the printed 5: p. 300, year 91, and p. 302, year 27, June. The data have the printed 5.
- 87 are in class E: neither reader gives the value, and the cell was read by eye. They include the signs and the days of the months on pp. 300–301, which were read by eye only.

`python check_spurious.py` computes every table.

**p. 300 (Maslamah's signs).** The signs of the years are the weekday of 1 al-muḥarram less one (Nallino p. 314). AH 1 began on a Thursday, the astronomical epoch of the Hijra. A year has 354 days, and 355 in the years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26 and 29 of the 30-year cycle.
- All 220 signs of the years agree, compared modulo 7.
- The sign of the decade 0 is printed 0. Year 0 began on a Sunday, whose sign less one is 0; the same sign is printed 7 at the decade 210.
- The decade 210 repeats the decade 0: 210 years are 74,417 days, exactly 10,631 weeks.
- The signs of the months, 1 3 4 6 7 2 3 5 6 1 2 4, are one more than the days before each month modulo 7. The months have 30 and 29 days in turn, the last «29 et 11/30».
- Nallino's example holds: AH 680 = 3 × 210 + 50, and the sign of 50, 1, plus that of al-muḥarram, 1, gives 2, a Monday.

**p. 301.**
- The sign of 30k collected years is 5k modulo 7, since 10,631 days are 1,518 weeks and 5 days.
- The single years 1 … 30 and their signs are as on p. 300, and so are the signs of the months.
- The Persian signs serve the era of Yazdegerd, whose years have 365 days = 52 weeks + 1 day. The column is the remainder of the year when divided by 7. 1 farwardīn of year 1 was a Tuesday; the months have 30 days, and the five added days follow ābān-māh.
- All 84 Persian signs agree, and so does Nallino's example: tīr-māh of Y 200 (200 = 7 × 28 + 4) began on a Thursday (5).

**p. 302.** The table counts the Seleucid years from Monday 1 October 312 BC, the era of Dhū ’l-qarnayn in common use (Nallino p. 316). The leap day comes at the end of February in the years 3, 7, 11 …, whose February falls in a Julian leap year.
- All 336 signs agree.
- The signs themselves show where the leap day falls, as Nallino argues against the title: March has the sign of February in the 21 common years and one more in the 7 leap years, and January always has the sign of December plus 3 (31 days = 4 weeks + 3).
- The column of intercalation runs 30, 45, «Bisext.» (then B), 15, the quarter days in sixtieths.
- The last column holds the multiples of 28, 28k and 28(k + 29), for k = 1 … 29.

**p. 303.** The Coptic table assumes an era beginning on a Friday (Nallino p. 316). The year has twelve months of 30 days and five added days (Misrī 35), and a sixth added day at the end of the years 2, 6, 10 … («et est intercalatio in fine anni»). All 336 signs agree, and so does the column of the bisextiles (45, «Bisext.» then B, 15, 30).

**p. 304.** For 30k Arab years (10,631k days) the Roman and the Coptic years are counted from their initia: 932 years 9 months 17 days 0 fractions, and 337 years 10 months 19 days 45 fractions, before the Hijra.
- These years have 365¼ days in twelve months of 30 days, and the fractions are sixtieths of a day.
- The Persian years (365 days) are counted from 9 years 11 months 9 days after the Hijra.
- All 242 numbers agree, including the twelve months that follow from months of 30 days, as under 60 (Roman) and 600 (Coptic).
- The initia in the Arabic heads (Maghribi abjad: غلب ط يز {0}, سلز ي يط مه, ط يا ط) equal their Latin.

**p. 305.**
- For the single Arab years 1 … 30 the Syrian (Roman) and Persian counts of their days agree, 210 numbers.
- The B marks the 11 leap years.
- The months and days of the Arab months (1 0, 1 29, 2 29 … 11 24) are the days to the end of each month, in months of 30.

**pp. 306–307 (the syzygies).**
- **Column I.** The days are constant (29; 14) and the hours and minutes advance by 20 minutes a line: 360 synodic months exceed 10,631 days by 20 minutes (al-Battānī's month gives 19.99 minutes). I of the conjunctions is I of the oppositions plus 14d 18h 22m in all 22 lines.
- **Columns II–IV.** Each advances by a constant step, and every value lies within 1.2″ of its line.
- **The 6 signs.** IV of the conjunctions equals IV of the oppositions plus 6 signs in all 22 lines, as Nallino says it must (p. 317).
- **Comparison with al-Battānī.** Nallino could not say from which elements the tables were built. The check compares them with al-Battānī's own radices and daily motions, from his tables of mean motions ([S06/mean_motions](../mean_motions/README.md)).

| | Conjunctions | Oppositions | al-Battānī |
|---|---|---|---|
| step of II (30 years) | 1s 8° 28′ 39.2″ | 1s 8° 28′ 39.3″ | 1s 8° 28′ 39.3″ (the Sun in 360 synodic months) |
| step of III | 9s 24° 0′ 50.4″ | 9s 24° 0′ 51.9″ | 9s 24° 0′ 51.2″ (the lunar anomaly) |
| step of IV | 8s 1° 24′ 4.1″ | 8s 1° 24′ 4.1″ | 8s 1° 23′ 58.9″ (the argument of latitude) |
| first line, I | 29d 1h 23m | 14d 7h 1m | 29d 1h 23.5m; 14d 7h 1.5m (the first mean conjunction and opposition after the epoch) |
| first line, II | 4s 22° 36′ 31″ | 4s 8° 3′ 15″ | 4s 22° 36′ 32″; 4s 8° 3′ 19″ |
| first line, III | 4s 6° 9′ 19″ | 9s 23° 13′ 49″ | 4s 6° 9′ 10″; 9s 23° 14′ 40″ |
| first line, IV | 0s 2° 30′ 58″ | 6s 2° 30′ 58″ | 0s 17° 54′ 9″; 6s 2° 34′ 2″ |

- **Columns I and II** follow al-Battānī's elements within a few seconds.
- **Column III** starts 9″ and 51″ from them.
- **Column IV.** For the oppositions it starts 3′ 4″ from them and advances 5.1″ more every 30 years. For the conjunctions it is the oppositions' value plus 6 signs. With al-Battānī's motions, however, the argument of latitude advances 6s 15° 20′ from a mean opposition to the following mean conjunction, so the conjunctions' column stands 15° 23′ below the computation.

All 1,828 values agree with their computation; the ledger holds only the four restorations of p. 304.

## Nallino's notes on these pages (Part II, pp. 308–317)

- **Why spurious.** All these tables but one are missing from the Spanish version.
  - The «rosa astrologica» (p. 299) is never mentioned by al-Battānī. It serves only judicial astrology, not the astronomical computations of astrologers. Its title ends وليست من الاصل, «and it is not from the archetype». In its circle of the houses Mars is once named by the Persian *bahrām*, a word al-Battānī never uses; everywhere else the rosa has the Arabic *mirrīkh*, so *bahrām* comes from a copyist.
  - The other tables follow those of pp. 187–188 in the codex, which by appendix E (t. I, p. 148: «… per tabulas quas in fine libri posuimus») ended the book, as they end the Spanish version. They cannot have been moved there by the copyists from elsewhere in the book, because they certainly do not come from al-Battānī.
- **Where they come from.**
  - **pp. 300–301** are said in their titles to come from the astronomical work of the Spanish Arab Maslamah [al-Maǵrīṭī] (born in Madrid, it seems, lived in Cordoba, died in 398, beginning 16 September 1007). The table of the Arab signs repeats p. 7 on a method quite different from al-Battānī's (t. I, p. 145). Al-Battānī does not use the Persian chronology and never mentions such a table.
  - **p. 302** is useless beside p. 8, which gives the signs of the years and months of Dhū ’l-qarnayn. The month names in their Latin form (pp. 201–203) and the word *as-Suryān* for the Syrians, unknown to al-Battānī, are suspect. The signs refer to the Julian years of Dhū ’l-qarnayn counted from October, not from September as al-Battānī counts them.
  - **p. 303** is never mentioned. It rests on fixed years, while al-Battānī treats the Coptic years as vague years counted from the era of Dhū ’l-qarnayn (p. 205). Whether its era is the Alexandrine one that al-Battānī uses or that of Diocletian is not clear; both begin on a Friday.
  - **pp. 304–305** are mentioned in no chapter and refer to Roman and Coptic eras different from al-Battānī's; *as-Suryān* on p. 305 is suspect.
  - **pp. 306–307** are of no use to al-Battānī, who always computes syzygies with the Roman years of Dhū ’l-qarnayn or the Coptic ones. Their counting by signs, degrees and so on, from the beginning of each sign rather than from Aries, is foreign to his usage. It does not occur even in his star catalogue, where Ptolemy had used it.
  - It is not improbable that pp. 302–307 too come from Maslamah's work. Maslamah could not have left out tables of the syzygies in the years of the Hijra, since he is known to have adapted others' canons to the Arab years.
- **The two small tables of cities.** The two small spurious tables of the longitudes and latitudes of cities of North Africa and Spain are treated on pp. 218–220 (edited in [S13](../../S13/)).
- **p. 300.**
  - The table covers 210 years because the signs then repeat (t. I, p. 323).
  - Maslamah deliberately lowered the signs of the years, both single and collected, by one and raised those of the months by one. To find the beginning of a month, add the sign of the month to that of the year; for the beginning of a year, add the sign of al-muḥarram, 1.
  - Since Maslamah has a year 0, it would have been simpler to change neither.
  - The same table opens the Spanish version of az-Zarqālī's tables (*Libro de las tablas del Zarquiel*), f. 94,r. of the codex that holds the Spanish version of al-Battānī.
- **p. 301.**
  - **The Arab signs** are reduced by one, those of the months raised by one, as on p. 300, and are used in the same way without the division by 210. The table of p. 300 can therefore be called perpetual.
  - **The Persian signs** are explained by the seven-year cycle and Nallino's example above.
  - **The added days.** The five added days stand after ābān-māh by common usage, as the table itself shows. Some Arab astronomers, for convenience, put them at the end of the year, as Ulugh Beg does.
- **p. 302.**
  - **The title.** Its words «intercalatione mense Decembri posita iuxta methodum Romanorum» are «ineptissima interpolatio»: the signs show the leap day at the end of February. A reader who saw the bisextiles marked between the columns of December and January took December to have 32 days in leap years. That is «unheard of in chronology».
  - **The error spread.** Later writers of Spain and North Africa nevertheless repeated it:
    - the *Libro de las taulas alfonsies* (about 1272): some add the leap day to December, others to February;
    - Muḥammad as-Sūsī, *al-Mumtaʿ fī sharḥ al-maqnaʿ*, and his *al-Maṭlaʿ ʿalà masāʾil al-maqnaʿ*;
    - Muḥammad ibn aṭ-Ṭayyib al-ʿAlamī (died 1134 or 1135 H.);
    - Saḥnūn al-Wānsharīshī.
  - **The signs.** They are true, not lowered by one as on p. 8. The table agrees with al-Bīrūnī's *Chronology* (p. 195 text, 175 transl.) and with Ulugh Beg (p. 18 text, 17 transl.), who however lack the convenient list of the multiples of 28. On the 28-year cycle, t. I, p. 323.
- **p. 303.** What this Coptic era of fixed (Julian) years is, is not clear.
  - The sign of Tūt shows that it began on a Friday. That fits the era of Augustus mentioned by al-Battānī (t. I, pp. 244–245), and also the era of Diocletian still used by the Copts, whose epoch is Friday 29 August 284.
  - The author (Maslamah?) probably meant the era of Diocletian, since the next table uses it; the era of Augustus was hardly used among the Arabs (t. I, p. 245).
- **pp. 304–305.** The first table determines the eras with certainty. The epoch of the Hijra is 15 July 622, as with the Arab astronomers: 621 Julian years and 196 days after the beginning of the Christian era.
  - **The Roman column.** Its initium, 932 years 9 months 17 days before the Hijra (932 years and 287 days), falls 311 years and 91 days before the Christian era. That is 1 October 312 BC, the era of Dhū ’l-qarnayn or of the Seleucids in common use.
  - **The Coptic column.** Its 337 years and 319 days before the Hijra lead to 283 years and 242 days after the beginning of the Christian era. Since 284 is a leap year, that is Friday 29 August 284, the epoch of the era of the Martyrs or of Diocletian.
  - **The Persian column.** The 9 vague years, 11 months and 9 days (3,624 days) are the known interval between the Hijra of the astronomers and the era of Yazdegerd, whose epoch is Tuesday 16 June 632 (t. I, p. 69).
  - **The interpolator.** The table probably ended at AH 600. An interpolator who did not understand the months of 30 days extended it, treating the year as twelve months only, and put numbers of his own in place of the correct ones that Nallino prints:

    | Year | Roman, codex | Coptic, codex |
    |---|---|---|
    | 630 | 1544 0 10 15 | 928 (sic) 1 13 0 |
    | 660 | 1573 1 19 0 | 967 (sic) 2 21 45 |

  - **The Spanish version.** Strangely, it also gives both these tables (f. 36,r.), placed after the concordance of the years of the Hijra and the Roman years. Its collected years of the Hijra run only from 330 to 600. Its titles are «Annos de Alexandre el macedonio, que son bissiestos», «Annos de declacianos, et son bissiestos», «Annos de diezdeiart, et non son bissiestos» and, for the Syrians in the single years, «Todos los annos bissiestos. Romanos et egipcianos». Its scribe did not understand the fractions and called them *defflectiones*.
- **pp. 306–307.**
  - **The latitude of the conjunctions.** In the table of conjunctions, the last ten lines of the motion of latitude are full of errors and gaps in the codex. They are easily restored by computation and by comparison with the oppositions, from which they must differ by exactly 6 signs.
  - **The oppositions.** In the table of oppositions, many of the last 12 seconds of column II and of the last 11 minutes of column IV were faulty.
  - Nallino prints these restorations without the readings of the codex. The check confirms that the printed values lie on their lines and keep the difference of 6 signs.

## Conventions

- The half-title has the signature 38, p. 305 the signature 39.
- The heads set along their columns are read from the foot upwards, as printed.
- The months of pp. 300, 301 and 305 stand beside the rows as printed, evenly spaced from the first month to the last.
- **p. 300.** The sign of the decade 0 is printed 0.
- **p. 301.** The Arabic heads المبسوطة («single») and المجموعة («collected») stand over the collected and the single years respectively, the reverse of their meaning; Nallino's Latin heads follow the columns.
- **p. 302.**
  - The head of the multiples reads «[qu sunt]» as printed.
  - The first B of the column of intercalation is printed «Bisext.».
  - There is a stray mark after the 6 of June in year 6 and a dot after the 2 of September in year 7.
  - The 8 of 280 and the 2 of 1428 are printed broken.
- **p. 303.** The first bisextile is printed «Bisext.»; there is a dot after the 2 of Bawūnah in year 11.
- **p. 304.** There is a dot after the 6 of the Roman months under 210.
- **pp. 306–307.** The first rows carry the marks as printed. Under 241 the conjunctions print column II as 2s 30° 25′ 44″, with 30° for the next sign's 0°.

## Tools

`tools/` holds the scripts that read the pages:

- `spurious_pages.py`: the computations that guided the reading;
- `build_spurious.py`: writes the data files;
- `eye_sheet.py`: the contact sheets;
- `audit_glyph_only.py`: the third reading of the cells that only the glyph reader saw;
- the shared readers.

The scripts here:

- `python write_spurious_ledger.py` writes the ledger;
- `python check_spurious.py` checks the data; `--stats` gives the comparison of the syzygies with al-Battānī's elements;
- `python gen_spurious.py` writes `p2_spurious.tex` (XeLaTeX).
