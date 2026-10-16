# S15 — al-Battānī's book on the indications of the conjunctions and the eclipses (his astrological history)

Al-Battānī's *Kitāb fī dalāʾil al-qirānāt wa-l-kusūfāt*, the astrological history of the Prophet and the early caliphate, survives in one manuscript, Ankara, Dil ve Tarih-Coğrafya Fakültesi, collection Saib, 199/2, ff. 27v–42v. George Saliba edited the Arabic text in E. S. Kennedy, Colleagues and Former Students (Benno van Dalen, George Saliba, Julio Samsó), «Al-Battānī's Astrological History of the Prophet and the Early Caliphate», *Suhayl* 9 (2009–2010), pp. 13–148. The article reproduces his typeset edition as page images on the even pages 18–78, facing the English translation. This folder transcribes those pages, one line of this edition for each printed line.

**In progress.** Transcribed: pp. 18–64 (PDF pages 6–52), ff. 27v–39r: 24 of the 31 pages of the Arabic text, 404 lines, 46 lines of apparatus and 11 horoscope charts (those of the article's Horoscopes 1–4, 6, 7, 8, 10, 12, 14 and 16; the article numbers 21 horoscopes, and Horoscopes 5, 9, 11, 13 and 15 have no chart). Not yet transcribed: pp. 66–78 (PDF pages 54–66).

## Read

- [historia.pdf](historia.pdf): the transcription. Every printed line is one line here, numbered in the right margin as the editors number it, with the folio of the manuscript where the edition prints it; the headings are centred; the horoscope charts are transcribed cell by cell and drawn again; the editors' apparatus follows each page.

## What the transcription keeps

- The text, the headings and the apparatus as printed, letter for letter, with the vowel signs, shaddas and hamzas that the print gives, the editors' square brackets and their spacing, and the misprints, which the observations name (for example «الكولب» for «الكواكب» on p. 22, «فك البروج» for «فلك البروج» on p. 32).
- The numbers written in letters (abjad), in the text and in the charts, as printed, with the line the text sets above them, and the sign the print uses for zero (transcribed `{0}`; it has the form of a small ح with a flat top). The chart identifiers (H01, …) follow the article's numbering of the horoscopes.
- The line numbers of the edition (every fifth line) and the folios of the manuscript printed in the margin; the stroke that marks the beginning of a folio in the line.
- Paragraph indents and headings.
- Not kept: the long joins (kashīdas) by which the print justifies the lines. The tanwīn of the accusative is written on the letter before the final alif, and on the lām-alif in لاً, wherever the print sets it.

## Observations

Each page file ends with observations (`@obs`), kept in the records: the folio marks, misprints and slips, the hand corrections visible in the printed pages, the arithmetic of the numbers in the text (the periods of the conjunctions, dates, latitudes), and, marked «comparator», what the article's translation and commentary give where they bear on a reading. The translation and the commentary are not reproduced.

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
| `source_manifest.tsv` | The source PDF with its SHA-256. |
| `checkpoint.json` | The state of the session. |

## Rebuild

```
python build_historia.py
xelatex historia.tex
xelatex historia.tex
```

The fonts are Amiri (Arabic) and Linux Libertine O (Latin).

## Credits and licence

- al-Battānī: the text.
- George Saliba: the edition of the Arabic text and its apparatus; E. S. Kennedy, Benno van Dalen, George Saliba and Julio Samsó: the article, *Suhayl* 9 (2009–2010), pp. 13–148, licensed CC BY-NC-ND 3.0 ES. This transcription reproduces the Arabic edition (text, line numbers, brackets, headings, charts and apparatus) in another format, without change of content, under the same licence and with this attribution.
- Transcription, observations and scripts: AI-integrated work (Claude), 2026; no person has reviewed it. The observations and the scripts are dedicated to the public domain (CC0 1.0).
