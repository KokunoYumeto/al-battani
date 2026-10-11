# S11 — al-Battānī's Arabic text as printed by Nallino (Part III), pp. 80–153

Part III of Nallino's edition prints the Arabic text of the *Zīj* from the Escorial codex. The scan has its pages in descending order (the book opens from the right): printed page = 1152 − PDF page. S11 covers printed pp. 80–153 (PDF 1072 down to 999). It continues [S10](../../S10/textus/README.md), which holds the title pages, Nallino's corrigenda and pp. 1–79; S12 will hold pp. 154–226.

**Done:** pp. 80–100: chapter 30 to its end: the end of the account of the moon's spheres and motions, with the figure of p. 81 redrawn, the causes of the eclipses of the moon and of the sun, the account of the distances and sizes of the sun and the moon, with the two solar and the two lunar eclipses observed at al-Raqqa and Antioch and the diameters of the moon, the sun and the shadow found from them, the construction for the distance of the sun, with the figure of p. 89 redrawn, the sun's distance, diameter and bulk reckoned from it, the length of the shadow, the same reckoning with al-Battānī's own diameters, the account of the moon's light and, on p. 94, its figure, redrawn with its ten circles of the moon, their hatched dark halves and its 59 letters and words, beside the ten lines of text of that page; chapter 31, on the spheres of the five planets (pp. 95–100), with the figure of a planet's spheres on p. 96 redrawn, the cause of the planets' retrogradation on p. 98 and, on p. 99, al-Battānī's corrections of the planets' mean motions and the reason why tables of the anomaly of the upper planets and of the course of the two lower ones are not given; and the beginning of chapter 32, on the eras of the Arabs, the Romans, the Copts and the Persians (p. 100), with the names of the Arabic, the Roman and the Persian months. The session is in progress: pp. 101–153 are not yet transcribed.

## Read

- [p3_textus.pdf](p3_textus.pdf): every printed line at its printed place on the page, with the codex's folio numbers, Nallino's line numbers and his notes where printed.

## Data

- `pages/AB01-PDF####.txt`: the transcription, one source line per printed line, with the vowel signs exactly as printed; `@obs` lines describe what was measured or compared on the scan. The line kinds are those of S10.
- `geometry/PDF####.json`: the measured placement of the lines, the rule over the notes, the note lines and the margin items.
- `records/AB01-PDF####.json` and `anchors.tsv`: one record per page and one row per printed line (`AB01-PDF1072-L01` …), with Nallino's line number.
- `python build_textus.py` writes `p3_textus.tex` (the same script as in S10; it takes the session from the name of the folder above `textus/`); XeLaTeX twice (Amiri, Linux Libertine, `fonts/NallinoSigns.otf`).

## Conventions and checks

The conventions are those of [S10](../../S10/textus/README.md): the signs as printed, misprints kept as printed and described, a letter written with the dots that the master scan or the second copy of Part III (Internet Archive albattanisivealb00batt) shows, long joins not transcribed, abjad numerals and the letters of the constructions under the bars that are printed over them.

Printed forms that differ from the expected word are kept and described in `@obs`: p. 82: «حاصّة», «الحاصّة» and «لحاصّة», each printed without the dot of the khā' (for خاصّة); p. 88: «تَعْيِيرًا», printed with an ʿayn (Nallino's corrigenda: «Pag. ٨٨, lin. 6 lege تَغْيِيرًا»), and «دوائِر», whose tooth is printed without its hamza; p. 89: «دارة», the first word of the page, printed without the tooth and its hamza (for دائرة); p. 90: «والغَمْق», printed with a dot over the ʿayn (for والعمق); «المَثل» and «المَثلَيْن» (twice), with a fatha over the mīm where the page has مِثْل elsewhere; and the reference «2» on line 6, printed where the reference to note 7 belongs; p. 93: «المَضِيءَ» (line 5; Nallino's corrigenda: «٩٣,5, المُضِيء») and «المَضِيء» (line 10), with a fatha over the mīm; p. 94: the numeral «قف» (180), whose fā' is printed without its dot; p. 95: «الحاصَّة» (lines 8 and 18) and «الحاصّة» (line 12), printed without the dot of the khā' (for الخاصّة), and «جَاْتُ» (line 17), with a sukun over an alif that has no hamza; p. 97: «الحاصّة» and «الحاصَّة», five times, printed without the dot of the khā' (for الخاصّة); p. 98: «حاصَّة» and «الحاصّة» (line 1), without the dot of the khā'; «بَدْئًِّا» (line 9), one tooth with the hamza over it and the two dots of a yā' and a kasra under it; «تُحدّ» (line 11), with the damma over the tā'; p. 99: «حاصَّتهما», «حاصّة» (twice), «حاصّتها», «وحاصّة» and «لحاصّة», printed without the dot of the khā' (for خاصّة).

Each page is read from enlarged images of the master scan, with every vowel sign, hamza, sukun and bar measured. The reading is compared letter by letter with the scan's text layer and with Tesseract 5 (Arabic model), and every word that neither confirms is checked on the scan. Sweeps then compare what the transcription expects with what is measured on the page: the hamza sorts, the sukuns, the dots letter by letter, and the kasras under the lines; every place where they differ is looked at, the doubtful ones in both copies. Sheets set every signed word, every word that ends in yā' and every printed line beside the same word or line of the built edition. Nallino's corrigenda give readings for six places on pp. 88–153 (p. 88, line 6; p. 93, line 5; p. 123, note 1; p. 128, line 1; p. 137, line 10; p. 149, line 17); each is compared when its page is made, and the printed form is kept. The transcription is AI-integrated work; no person has reviewed it.

## Credits

- al-Battānī: the text.
- C. A. Nallino: the edition of the Arabic text from the Escorial codex and the notes (Part III, Milan and Rome 1899).
- Transcription and edition: AI-integrated work in this repository, 2026.
