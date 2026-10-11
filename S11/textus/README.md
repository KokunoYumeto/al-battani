# S11 — al-Battānī's Arabic text as printed by Nallino (Part III), pp. 80–153

Part III of Nallino's edition prints the Arabic text of the *Zīj* from the Escorial codex. The scan has its pages in descending order (the book opens from the right): printed page = 1152 − PDF page. S11 covers printed pp. 80–153 (PDF 1072 down to 999). It continues [S10](../../S10/textus/README.md), which holds the title pages, Nallino's corrigenda and pp. 1–79; S12 will hold pp. 154–226.

**Done:** pp. 80–86: chapter 30 continued: the end of the account of the moon's spheres and motions, with the figure of p. 81 redrawn, the causes of the eclipses of the moon and of the sun, and the account of the distances and sizes of the sun and the moon, with the two solar and the two lunar eclipses observed at al-Raqqa and Antioch. The session is in progress: pp. 87–153 are not yet transcribed.

## Read

- [p3_textus.pdf](p3_textus.pdf): every printed line at its printed place on the page, with the codex's folio numbers, Nallino's line numbers and his notes where printed.

## Data

- `pages/AB01-PDF####.txt`: the transcription, one source line per printed line, with the vowel signs exactly as printed; `@obs` lines describe what was measured or compared on the scan. The line kinds are those of S10.
- `geometry/PDF####.json`: the measured placement of the lines, the rule over the notes, the note lines and the margin items.
- `records/AB01-PDF####.json` and `anchors.tsv`: one record per page and one row per printed line (`AB01-PDF1072-L01` …), with Nallino's line number.
- `python build_textus.py` writes `p3_textus.tex` (the same script as in S10; it takes the session from the name of the folder above `textus/`); XeLaTeX twice (Amiri, Linux Libertine, `fonts/NallinoSigns.otf`).

## Conventions and checks

The conventions are those of [S10](../../S10/textus/README.md): the signs as printed, misprints kept as printed and described, a letter written with the dots that the master scan or the second copy of Part III (Internet Archive albattanisivealb00batt) shows, long joins not transcribed, abjad numerals and the letters of the constructions under the bars that are printed over them.

Each page is read from enlarged images of the master scan, with every vowel sign, hamza, sukun and bar measured. The reading is compared letter by letter with the scan's text layer and with Tesseract 5 (Arabic model), and every word that neither confirms is checked on the scan. Sweeps then compare what the transcription expects with what is measured on the page: the hamza sorts, the sukuns, the dots letter by letter, and the kasras under the lines; every place where they differ is looked at, the doubtful ones in both copies. Sheets set every signed word, every word that ends in yā' and every printed line beside the same word or line of the built edition. Nallino's corrigenda give readings for six places on pp. 88–153 (p. 88, line 6; p. 93, line 5; p. 123, note 1; p. 128, line 1; p. 137, line 10; p. 149, line 17); each is compared when its page is made, and the printed form is kept. The transcription is AI-integrated work; no person has reviewed it.

## Credits

- al-Battānī: the text.
- C. A. Nallino: the edition of the Arabic text from the Escorial codex and the notes (Part III, Milan and Rome 1899).
- Transcription and edition: AI-integrated work in this repository, 2026.
