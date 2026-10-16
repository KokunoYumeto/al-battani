# S14 — al-Battānī's commentary on Ptolemy's *Tetrabiblos* (Escorial, RBMSL, ár. 969, ff. 20r–80v)

Al-Battānī's commentary on the *Tetrabiblos*, *Sharḥ Kitāb al-Arbaʿ maqālāt fī aḥkām ʿilm al-nujūm* (PAL work C.2.2), survives in two manuscripts, Escorial, Real Biblioteca de San Lorenzo, árabe 969, ff. 20r–80v, and Berlin, Staatsbibliothek, Sprenger 1840. This folder edits it from the transcription of the Escorial manuscript by Nadine Löhr in *Ptolemaeus Arabus et Latinus. Texts* (Bavarian Academy of Sciences and Humanities, <https://ptolemaeus.badw.de/text/M1016>), licensed CC BY 4.0, at the exact commit `762614d992ac588389f10309cb180e0a34b3459c` of <https://gitlab.lrz.de/badw-data/pal-texts>. It is a conversion of that transcription: the manuscript itself was not read for this edition.

**Done:** ff. 20r–80v, the whole commentary: 122 page sides, 2,465 lines of the manuscript, 40 chapters, 439 notes, 123 folio correspondences of the Berlin manuscript and the two tables of ff. 80r–80v.

## Read

- [commentarius.pdf](commentarius.pdf): the edition. Every line of it is one line of the manuscript as the transcription divides it (PAL's «||»), numbered in the right margin; a line that holds a marginal addition and is longer than the measure runs on to the next line of the page. Each page side of the manuscript begins with its folio number; its notes follow it. The front matter gives PAL's introduction, conventions and sigla. The PDF bookmarks lead to every folio and every chapter.

## What the edition keeps

- The text as committed, letter for letter, with PAL's normalization as PAL states it (final radicals wāw and yāʾ, hamzas and maddas normalized; shaddas added except on solar letters and relative pronouns; diacritics added where vacant). The letters are kept as they stand in the files, among them the Persian ی and ک in some words and the dotless qāf ٯ.
- PAL's editorial signs, in the places and the direction that PAL gives them: { } a reading uncertain or conjectural, {…} an illegible lacuna; [ ] in the text but to be deleted (additions by the scribe, eulogies); [[ ]] deleted by the scribe; 〈 〉 added by the editor (around a number at the head of a heading: a chapter number not given by the scribe); 〈〈 〉〉 added in the margin or between the lines. They are listed, line by line, in `signs.tsv`.
- PAL's notes, with PAL's numbers 1–439 (variants of the Berlin manuscript, B, and of Yamamoto's preliminary edition of the Arabic *Tetrabiblos*, T, and remarks on the manuscript).
- The folio correspondences of the Berlin manuscript (/B1r/ …), where PAL sets them.
- The 40 chapter headings, set in bold, with PAL's identifiers I.1–I.40.
- The two tables of ff. 80r–80v (the days of the months and what is added to the degrees of the lot of the revolution; the lords of the triplicities, the faces and the terms after Ptolemy), with their cells, spans and notes. They are set in the column order of PAL's files, which puts the names of the signs on the right, as an Arabic table reads.

## Files

| File | Content |
|---|---|
| `source/1.xml`, `source/pages/1#20r.xml` … `1#80v.xml` | PAL's files, unchanged (the work and its 122 page sides). |
| `source/evidence/` | PAL's licence file and README at the same commit, and the metadata of the commit. |
| `build_commentarius.py` | Writes `commentarius.tex`, the records and the ledgers from PAL's files. |
| `check_conversion.py` | Compares, independently of the builder, the text of PAL's files (line by line at PAL's «||», with the Berlin folio marks), PAL's notes and the cells of the tables with `anchors.tsv`, `apparatus.tsv` and `tables/`. It reports no difference. |
| `records/AB03-F###x.json` | One record per page side: its lines with their anchors (`AB03-F024r-L05`), text and TeX, the notes and Berlin folios of each line, the notes of the page side and its tables. |
| `anchors.tsv` | Every line of the manuscript: anchor, folio, line, text. |
| `apparatus.tsv` | PAL's notes: `AB03-n001` …, PAL's number, the line (or table) it belongs to, the text. |
| `berlin.tsv` | The Berlin folios and the Escorial line at which each begins. |
| `chapters.tsv` | The 40 chapter headings: PAL's identifier, the line where the heading begins, the heading. |
| `signs.tsv` | The editorial signs of each line: the sign, its meaning in PAL's conventions, what it encloses. |
| `tables/AB03-F080r-T01.tsv`, `tables/AB03-F080v-T01.tsv` | The two tables: row, column, row span, column span, text (the lines of a cell joined with « / »), notes. |
| `source_manifest.tsv` | Every source file with its path in the packet's archive and its SHA-256. |
| `page_disposition.tsv` | Every page side: its content (title page, text, a blank page, a table), its lines and tables. |
| `checkpoint.json` | The state of the session. |

## Not done

- The manuscript images were not consulted: the edition is as good as the transcription. PAL's notes record where the transcription departs from the Berlin manuscript or from Yamamoto's edition.
- No translation was made.

## Rebuild

```
python build_commentarius.py
xelatex commentarius.tex
xelatex commentarius.tex
python check_conversion.py
```

The fonts are Amiri (Arabic), Linux Libertine O (Latin) and Yu Gothic (the angle brackets of the editorial signs).

## Credits and licence

- al-Battānī: the commentary.
- Nadine Löhr, *Ptolemaeus Arabus et Latinus. Texts*: the transcription of the Escorial manuscript, its notes, signs and folio correspondences (update 25.05.2021; CC BY 4.0).
- Conversion: AI-integrated work (Claude), 2026; no person has reviewed it. This edition is a derivative of PAL's transcription and is licensed CC BY 4.0 like it.
