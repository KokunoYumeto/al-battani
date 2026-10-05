# S13 — Nallino's notice before the tables (Part III p. 227)

Before the tables of Part III, Nallino prints a short notice in Arabic, *tanbīh* (master PDF 925). It says three things:

- In the Escorial codex the tables follow the chapters of the work.
- From these tables Nallino took for Part III those on chronology, geography and the names of the fixed stars. He printed them without correcting the errors in the abjad letters, which he says are very many. Readers who want them corrected should use his Latin version (Part II), which also prints the remaining tables, those that contain numbers only.
- The abjad letters in the tables have their Maghribi values, as in the codex: ص = 60, ض = 90, س = 300, ظ = 800. In the notice these four letters are printed with an overline.

## Read

- [Part III p. 227, 1 p.](p3_note227.pdf): the notice line by line as printed, centred.

## Data

`note227.tsv`: one row per printed line (title, 12 text lines, two closing lines «تم تم» and «تم»), with the vowel marks as printed and reading notes (`doubt`). Overlined letters are written `{ov:X}`.

The text was read at 520–2400 dpi and compared with a second copy of the print (Internet Archive). Marks were measured where their reading was not obvious; for example, a single round mark over a dotted letter is the letter's dot, not a sukun (مَذهب). `python gen_note227.py` writes the LaTeX edition.

## Credits

- C. A. Nallino: the notice (Part III, Milan 1899–1907).
- Transcription: AI-integrated work in this repository, 2026.
