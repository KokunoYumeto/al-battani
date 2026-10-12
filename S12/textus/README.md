# S12 — al-Battānī's Arabic text as printed by Nallino (Part III), pp. 154–226

Part III of Nallino's edition prints the Arabic text of the *Zīj* from the Escorial codex. The scan has its pages in descending order (the book opens from the right): printed page = 1152 − PDF page. S12 covers printed pp. 154–226 (PDF 998 down to 926), the end of the text. It continues [S11](../../S11/textus/README.md), which holds pp. 80–153; [S10](../../S10/textus/README.md) holds the title pages, Nallino's corrigenda and pp. 1–79.

**Done:** pp. 154–155: chapter 43 continued (pp. 154–155): the end of the rule for the sides of the darkening and of the clearing by the tables, and the beginning of the construction of the figure of the lunar eclipse (the circle of the half of the two diameters, the circle of the shadow, the four sides and the marks for the centre of the moon at the beginning, the middle and the end of the eclipse), with the figure of the eclipse redrawn, the line of the moon's passage and the three circles of the moon at the beginning, the middle and the end of the eclipse, the cases of a total eclipse with and without a stay and of a partial one, and the beginning of the example worked on the letters of the figure. The session is in progress: pp. 156–226 are not yet transcribed.

## Read

- [p3_textus.pdf](p3_textus.pdf): every printed line at its printed place on the page, with the codex's folio numbers, Nallino's line numbers and his notes where printed.

## Data

- `pages/AB01-PDF####.txt`: the transcription, one source line per printed line, with the vowel signs exactly as printed; `@obs` lines describe what was measured or compared on the scan. The line kinds are those of S10.
- `geometry/PDF####.json`: the measured placement of the lines, the rule over the notes, the note lines and the margin items.
- `records/AB01-PDF####.json` and `anchors.tsv`: one record per page and one row per printed line (`AB01-PDF0998-L01` …), with Nallino's line number.
- `python build_textus.py` writes `p3_textus.tex` (the same script as in S10 and S11; it takes the session from the name of the folder above `textus/`); XeLaTeX twice (Amiri, Linux Libertine, `fonts/NallinoSigns.otf`).

## Conventions and checks

The conventions are those of [S10](../../S10/textus/README.md): the signs as printed, misprints kept as printed and described, a letter written with the dots that the master scan or the second copy of Part III (Internet Archive albattanisivealb00batt) shows, long joins not transcribed, abjad numerals and the letters of the constructions under the bars that are printed over them.

Printed forms that differ from the expected word are kept and described in `@obs`: p. 154: «القطربْن» (line 10), whose tooth after the rā' is printed with one dot (Nallino's corrigenda: «١٥٤,10, القطرَيْن»); p. 155: «نُدِير» (line 19), whose yā' is printed without its dots, with a kasra under the dāl; «دَوَائِر» (line 9) and «الدَّوَائِر» (line 20), whose tooth is printed bare, without a hamza and without dots, with a kasra under it; and «القمر» (line 4), the stem of whose lām is printed in two pieces.

Each page is read from enlarged images of the master scan, with every vowel sign, hamza, sukun and bar measured. The reading is compared letter by letter with the scan's text layer and with Tesseract 5 (Arabic model), and every word that neither confirms is checked on the scan. Sweeps then compare what the transcription expects with what is measured on the page: the hamza sorts, the sukuns, the dots letter by letter, and the kasras under the lines; every place where they differ is looked at, the doubtful ones in both copies. Sheets set every signed word, every word that ends in yā' and every printed line beside the same word or line of the built edition. Nallino's corrigenda give readings for seven places on pp. 154–217 (p. 154, line 10; p. 176, line 12; p. 198, lines 8, 15, 16 and 22; p. 217, line 18); each is compared when its page is made, and the printed form is kept. The transcription is AI-integrated work; no person has reviewed it.

## Credits

- al-Battānī: the text.
- C. A. Nallino: the edition of the Arabic text from the Escorial codex and the notes (Part III, Milan and Rome 1899).
- Transcription and edition: AI-integrated work in this repository, 2026.
