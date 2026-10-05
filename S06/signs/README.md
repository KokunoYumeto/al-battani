# S06 — The weekday signs of the years and months (Part II pp. 7–8)

Two tables for finding the weekday on which a year or month begins. A «sign» is a weekday number, 1 = Sunday … 7 = Saturday.

- **p. 7** (codex fol. 157,v.): *Tabula ad invenienda initia annorum et mensium Arabicorum per differentia signa, quae [tamen] unam eandemque rem indicant.* It gives the signs of the Arab (Hijra) years, for the collected years 30, 60 … 210 and the single years 1–30, and of the Arab months. They are given in two schemes. In scheme I (left) the sign of a single year is the weekday of its first day. Scheme II (right) is the same information shifted, and it marks the leap years with B. The number of days of each month stands between the two schemes. Nallino explains both schemes in his note (Part II p. 198). He regards scheme II, which the Spanish version omits, as spurious.
- **p. 8** (fol. 158,r.): *Signa mensium Romanorum secundum aeram Dhū ’l-qarnayn, quae est per 28 dividenda et uno anno augenda.* It gives the signs of the twelve Syrian months, beginning with Aylūl (September), for the 28 years of the solar cycle. It also has a column of the leap-year quarters (15, 30, 45, B). The heads give each month's Arabic form of the Latin name (ستنبر September … اغشت Augustus), the Syrian name and the number of days. Nallino discusses these name forms on Part II pp. 201–203.

Nallino prints these tables only in Part II.

## Read

- [Part II pp. 7–8, 2 pp.](p2_signs.pdf).

## Data

| File | Content |
|---|---|
| `p7_signs.tsv` | p. 7: part (collected, single, month), scheme (I, II), year or month, sign, leap-year mark (scheme II), days of the month. |
| `p8_signs.tsv` | p. 8: the 28 years with the twelve month signs and the leap-year column. |
| `signs_heads.tsv` | Titles and column heads of both pages, Arabic and Latin. |
| `signs_discrepancies.tsv` | One difference, in a head of p. 8. |

## How the tables were read and checked

- **p. 7**: every value was read by eye at 300 dpi.
- **p. 8**: every value was read by the glyph reader and the OCR text layer. The 31 cells that both readers did not confirm were checked by eye.

`python check_signs.py` recomputes every value from the calendar (`calendars.py`):

- p. 7, scheme I: the sign of a single year is the weekday of 1 al-Muḥarram; the collected years advance 5 weekdays for every 30 years; a month's sign is the number of days before it, mod 7.
- p. 7, scheme II: as scheme I, with the single years shifted by 2 and the months by 5.
- p. 8: the weekday of the first of each month for the Seleucid years Y with (Y + 1) mod 28 = row.

Result: 527 values agree, 0 are open. One difference is ledgered. The head of the Kānūn II (January) column on p. 8 gives «30 d.», but January has 31 days, and the signs printed in that column count 31.

The printed values equal the computed ones everywhere. `build_signs.py` therefore writes the data from the computation, and the readings above are the evidence that this is what the page prints.

## Credits

- al-Battānī: the tables (scheme II of p. 7 and the Latin month names of p. 8 probably by later hands, as Nallino argues).
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
