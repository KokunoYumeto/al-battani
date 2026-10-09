# S10 — al-Battānī's Arabic text as printed by Nallino (Part III), from the title to p. 79

Part III of Nallino's edition prints the Arabic text of the *Zīj* from the Escorial codex. The scan has its pages in descending order (the book opens from the right): printed page = 1152 − PDF page. S10 covers the Arabic title page (PDF 1153), the list of chapters (pp. 1–5, PDF 1151–1147) and the text to p. 79 (PDF 1146–1073), in reading order.

**Done:** the title page, pp. 1–5 (the invocation, the heading of the work and the codex's list of the 57 chapters with its closing formula) and the text of pp. 6–23: chapter 1, chapter 2 with the tables of the orders produced by multiplying and by dividing the sexagesimal orders, chapter 3 on chords, chapter 4 on the obliquity of the ecliptic (the observations at al-Raqqa, the declination of each degree and its six ranks), chapter 5 on the risings of the signs in the right sphere, and chapter 6 on the parallels of the equator and the inhabited places (the equator, the height of the pole, the parallels to the arctic circle). The text follows page by page.

## Read

- [p3_textus.pdf](p3_textus.pdf): every printed line at its printed place on the page (the printed page is centred on the edition page); lines that fill the measure are justified to their printed width, short lines keep their natural width. The codex's folio numbers (f. 4,r.), Nallino's line numbers (5, 10, 15, 20) and the chapter numerals stand where printed.

## Data

- `pages/AB01-PDF####.txt`: the transcription, one source line per printed line, in reading order, with the vowel signs exactly as printed. `@page PDF PRINTED`, `@c SIZE TEXT` (a centred display line), `@rule Y LEN`, `@orn Y`, `@notes` (Nallino's footnotes, Latin with Arabic), `@obs` (observations on the print). `@table NAME` … `@endtable` a ruled table, one `@tr C1 | C2 | …` per row with the cells in reading order (from the right); a cell written `=TEXT` is set horizontally, the others turned through the angle at which the table prints them; `@lab TEXT` a letter beside a table (the sides of a table). `@sig N` the printer's signature at the foot of the first page of each sheet of eight pages (1 on p. 1, 2 on p. 9, 3 on p. 17). Inline: `{n:N}` a note reference, `{num:X}` the overlined abjad numeral of a chapter, `{mL:...}` / `{mR:...}` a margin item on the left / right, `{ov:...}` overlined letters (abjad numerals), `{0}` the zero sign of the codex (kept as `{0}` in the records), `*` the asterisk that marks the start of a new folio of the codex.
- `geometry/PDF####.json`: the measured placement (baselines and extents of the lines, the rule over the notes, the note lines, the margin items; for a table its rules, the angle of its turned cells and the centre of the ink of every cell; the places of the letters beside it), in PDF points of the master scan.
- `records/AB01-PDF####.json` and `anchors.tsv`: one record per page and one row per printed line (`AB01-PDF1151-L09` …), with Nallino's line number where the page has his marginal numbers (the corrigenda cite them: «Pag. ١, lin. 18» is `AB01-PDF1151-L09`).
- `python build_textus.py` writes `p3_textus.tex`; XeLaTeX twice (Amiri for Arabic, Linux Libertine for Latin; `fonts/NallinoSigns.otf` for the zero sign of the codex, as in the other editions of the project).

## Conventions

- Vowel signs, shadda, sukun, tanwīn, madda and hamza exactly as printed; where the print has no hamza, none is supplied. The type's lām-alif ends in a club head; a hamza is a separate mark above it (measured on every doubtful case). Under an alif the print usually sets a hamza with a kasra under it (إِ), sometimes a hamza alone (إنعام, p. 7); every إ is measured: a hamza alone is one mark of about 2.5 × 2.9 pt, a hamza with kasra is a hamza over a separate stroke (or one mark at least 3.9 pt tall where the two touch).
- Final yā' with dots (ي) and without (ى), tā' marbūṭa (ة) and hā' (ه) as printed.
- Long joins (kashida) are not transcribed; the long swash form of kāf is transcribed ك.
- Where the joining stroke of a lām did not print, the lām and the next letter are separated by a hairline (0.7–0.8 pt at 2400 dpi) and the lām looks like an alif; it is transcribed as a lām, with an observation (ولكيلا and فاُطلب on p. 15, حصلت on p. 17). A stroke that stands a full letter space (3.2 pt) from the next letter is an alif: the article of «واوتر» (p. 16) and «اوتر» (p. 17) lacks its lām, as printed.
- Misprints are transcribed as printed and described in `@obs`: on p. 1 «ونجزية» (Nallino's corrigenda: «Pag. ١, lin. 18, lege وتجزية»); on p. 3 the numeral of chapter 18 printed يج for يح.

## Method and checks

Each page was read from 300-dpi images of the master scan, with every doubtful sign measured or read at 600–1800 dpi. The reading was then compared with two machine readings made independently of it, the scan's own text layer and Tesseract 5 (Arabic model), letter by letter: every word that neither machine reading confirms was checked on the scan. Every word ending in yā' was checked on a sheet of crops taken with room for the dots under the bowl. Finally every printed line was compared with the same line of the built edition, set directly under it. The transcription is AI-integrated work; no person has reviewed it.

## Credits

- al-Battānī: the text.
- C. A. Nallino: the edition of the Arabic text from the Escorial codex and the notes (Part III, Milan and Rome 1899).
- Transcription and edition: AI-integrated work in this repository, 2026.
