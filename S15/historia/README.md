# S15 — al-Battānī's book on the indications of the conjunctions and the eclipses (his astrological history)

Al-Battānī's *Kitāb fī dalāʾil al-qirānāt wa-l-kusūfāt*, the astrological history of the Prophet and the early caliphate, survives in one manuscript, Ankara, Dil ve Tarih-Coğrafya Fakültesi, collection Saib, 199/2, ff. 27v–42v. George Saliba edited the Arabic text in E. S. Kennedy, Colleagues and Former Students (Benno van Dalen, George Saliba, Julio Samsó), «Al-Battānī's Astrological History of the Prophet and the Early Caliphate», *Suhayl* 9 (2009–2010), pp. 13–148. The article reproduces his typeset edition as page images: the Arabic title on p. 17 and the text on the even pages 18–78, facing the English translation. This folder transcribes those pages, one line of this edition for each printed line.

**Done:** the whole Arabic edition, the title page (p. 17) and pp. 18–78, ff. 27v–42v: 32 pages, 521 lines (3 of the title, 518 of the text), 55 lines of apparatus, the 31 folio marks of the manuscript and the 15 horoscope charts of the edition (181 cells), with 224 observations. The chart identifiers follow the article's numbering of its 21 horoscopes: H01–H04, H06–H08, H10, H12, H14 and H16–H20; Horoscopes 5, 9, 11, 13, 15 and 21 have no chart in the edition.

## Read

- [historia.pdf](historia.pdf): the transcription. Every printed line is one line here, numbered in the right margin as the editors number it, with the folio of the manuscript where the edition prints it; the headings are centred; the horoscope charts are transcribed cell by cell and drawn again; the editors' apparatus follows each page.

## What the transcription keeps

- The text, the headings and the apparatus as printed, letter for letter, with the vowel signs, shaddas and hamzas that the print gives, the editors' square brackets and their spacing, and the misprints, which the observations name (for example «الكولب» for «الكواكب» on p. 22, «فك البروج» for «فلك البروج» on p. 32, «الحملل» for «الحمل» on p. 72).
- The numbers written in letters (abjad), in the text and in the charts, as printed, with the line the text sets above them, and the sign the print uses for zero (transcribed `{0}`; it has the form of a small ح with a flat top, and the PDF draws it with ح).
- The line numbers of the edition (every fifth line, and on p. 44 also lines 7 and 8) and the folios of the manuscript printed in the margin; the stroke that marks the beginning of a folio in the line.
- Paragraph indents, headings, headings set at the end of a line of text, and lines set in a smaller type.
- In the charts, every cell with its lines in the printed order. The redrawing uses one layout for all charts, a square of nine cells with the corner cells halved by their diagonals and the houses running anticlockwise from the ascendant in the top cell, as in the print; entries that the print writes vertically or across a diagonal are set horizontally in their cell, and the observations say where the print puts them.
- Not kept: the long joins (kashīdas) by which the print justifies the lines. The tanwīn of the accusative is written on the letter before the final alif, and on the lām-alif in لاً, wherever the print sets it.

## Observations

Each page file ends with observations (`@obs`), kept in the records: the folio marks, misprints and slips, the hand corrections visible in the printed pages, where the charts depart from the text and whether the apparatus notes it, the arithmetic of the numbers in the text (the periods of the conjunctions, the arcs of direction, latitudes, the lengths of the reigns) and the conversion of its dates (Seleucid years counted from Tishrin I, the Julian calendar and the arithmetical Hijra calendar), and, marked «comparator» or with the article's page, what the article's translation and commentary give where they bear on a reading. The translation and the commentary are not reproduced.

## How it was checked

Every line was read against the page images of the publication at twice their resolution or more, the numerals of the charts at 900 dpi or more. A word-by-word comparison with a rough Tesseract draft of every page then marked the words in which the two differ; ten of them were read again at 500–2400 dpi, and none needed a change. The builder checks the printed line numbers against the count of lines on every page; every text page begins with its folio, and every chart has its twelve cells (H02 also a central one).

## Files

| File | Content |
|---|---|
| `pages/AB02-PDF####.txt` | The transcription, one file per printed page (PDF page ####): the lines, the charts, the apparatus and the observations. |
| `build_historia.py` | Writes `historia.tex`, the records and the ledgers from the page files. |
| `records/AB02-PDF####.json` | One record per page: its lines with their anchors (`AB02-PDF0006-L01`), kinds, folios and printed line numbers, its charts, apparatus and observations. |
| `anchors.tsv` | Every line: anchor, printed page, line, folio, kind, text. |
| `apparatus.tsv` | Every line of the apparatus: anchor, printed page, text. |
| `folios.tsv` | The folios of the manuscript printed in the margin and the line where each begins. |
| `charts.tsv` | Every cell of every horoscope chart: chart, cell, the line after which the chart stands, text. |
| `write_disposition.py`, `page_disposition.tsv` | Every one of the 136 PDF pages of the article: its content, its role and what this session does with it. |
| `source_manifest.tsv` | The source PDF with its SHA-256. |
| `checkpoint.json` | The state of the session. |

## Not done

- The manuscript in Ankara was not consulted: the transcription is of Saliba's edition as the article prints it. The apparatus reports the manuscript's readings where the edition departs from them.
- No translation was made.

## Rebuild

```
python build_historia.py
xelatex historia.tex
xelatex historia.tex
python write_disposition.py
```

The fonts are Amiri (Arabic) and Linux Libertine O (Latin).

## Credits and licence

- al-Battānī: the text.
- George Saliba: the edition of the Arabic text and its apparatus; E. S. Kennedy, Benno van Dalen, George Saliba and Julio Samsó: the article, *Suhayl* 9 (2009–2010), pp. 13–148, licensed CC BY-NC-ND 3.0 ES. This transcription reproduces the Arabic edition (title, text, line numbers, brackets, headings, charts and apparatus) in another format, without change of content, under the same licence and with this attribution.
- Transcription, observations and scripts: AI-integrated work (Claude), 2026; no person has reviewed it. The observations and the scripts are dedicated to the public domain (CC0 1.0).
