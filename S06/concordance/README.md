# S06 — The concordance of the Hijra with the Seleucid era (Part II pp. 9–18)

Ten tables, *Tabulae I–X ad inveniendam aeram Arabum per aeram Romanorum et Romanorum per Arabum* (codex fol. 158,v.–163,r.). For each Hijra year from 1 to 600 they give:

- the weekday on which the year begins (the «name» of the first day of al-Muḥarram, 1 = Sunday … 7 = Saturday);
- the year of the era of Dhū ’l-qarnayn (the Seleucid era, which al-Battānī counts from 1 September);
- the day and the Syrian month on which al-Muḥarram begins. The month name is printed at the top of each half and where the month changes; elsewhere a ditto mark » stands for it.

Nallino prints these tables only in his Latin Part II; Part III does not have them. In his note (Part II p. 203) he says he corrected the codex's small errors in the day numbers with Wüstenfeld's *Vergleichungs-Tabellen* (1854). He also says that al-Battānī's day numbers are always one less than Wüstenfeld's, because al-Battānī puts the epoch of the Hijra on Thursday 15 July 622, not 16 July (p. 199). He left out two further pages of the codex (fol. 163,v.–164,r.), which continue the table to AH 720, as spurious.

## Read

- [Part II pp. 9–18, 10 pp.](p2_concordance.pdf): the tables as printed.

## Data

| File | Content |
|---|---|
| `conc_p2.tsv` | 600 rows: page, half (L, R), row, Hijra year, weekday sign, Seleucid year, day, month (name or »), how each number was established (`check`, see below), and notes (`doubt`). |
| `conc_pages.tsv` | Per page: folio line, table number, Arabic and Latin title, the Arabic column heads (p. 9 only), signature, notes. |
| `conc_discrepancies.tsv` | The eight printed numbers that differ from the computed calendar. |
| `calendars.py` | The calendar arithmetic: Julian day numbers, the arithmetical Hijra calendar with al-Battānī's epoch (Thursday 15 July 622 = JD 1948439), weekdays, Syrian month names. |
| `build_conc.py`, `tools/` | How the data were built from the readings: a digit reader for Part II's typeface (`p2num.py`), the page reader (`p2cal.py`), the cell classification (`calverify.py`). |

## How the tables were read and checked

Every number was read twice, by a glyph reader trained on Part II's own digits and by the OCR text layer of the scan. Each reading was then compared with the computed calendar:

| Class | Numbers | How established |
|---|---|---|
| A | 1,990 | Both readers give the computed value (glyph reader with high confidence). |
| B | 371 | One reader gives it; each cell checked by eye on contact sheets. For 81 of them only the glyph reader saw the number (the text layer has no token there): Tesseract confirmed 55 and the other 26 were read by eye. |
| C | 39 | Neither reader gives it; each cell read by eye in its row. |

`python check_concordance.py` repeats the comparison: 2,392 numbers and month marks agree with the computed calendar, 8 differ and are ledgered, 0 are open. The month names and ditto marks agree everywhere.

The eight differences:

| Hijra year | Printed | Computed | |
|---|---|---|---|
| 61 | 31 aylūl | 30 aylūl | Aylūl has 30 days. |
| 145 | weekday 5 | 4 | The weekdays printed for AH 144 and 146 imply 4. |
| 198 | 1125 | 1124 | AH 197 and 198 both begin in the Seleucid year 1124. The table repeats a year in other such places (962 for AH 30 and 31, 1222 for AH 298 and 299). |
| 318 | 3 subāṭ | 2 subāṭ | The weekday printed in the row is that of 2 February. |
| 377 | 4298 | 1298 | A misprint: 1297 and 1299 stand before and after. |
| 455 | 4 kānūn II | 3 kānūn II | The weekday printed in the row is that of 3 January. |
| 459 | 1278 | 1378 | A misprint: 1377 and 1379 stand before and after. |
| 534 | 26 āb | 27 āb | The rows before and after agree with 27. |

Part II exists in one scan copy here; the second witness for these tables is the calendar computation.

## Conventions

- Numbers, month names and ditto marks are transcribed as printed, including the eight that differ from the calendar.
- A damaged digit is transcribed as the digit it is, with a note: in the Seleucid year 1340 (AH 420) only the stem and a trace of the crossbar of the 4 printed.
- Running heads, folio lines and signatures (p. 9 «2», p. 17 «3») are kept. On p. 9 the column heads of the left half have Arabic above the Latin. In that Arabic, «بقع» is printed with one dot below, for يقع.

## Credits

- al-Battānī: the tables.
- C. A. Nallino: the Latin edition and the notes (Part II), Milan 1907.
- Transcription, data model and checks: AI-integrated work in this repository, 2026.
