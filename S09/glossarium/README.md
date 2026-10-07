# S09 — Nallino's Glossarium (Part II pp. 319–358)

Nallino's *Glossarium* of al-Battānī's technical vocabulary: Arabic headwords, often vowelled, with their Latin, Greek and Arabic explanations and with references to the pages and lines of the Arabic text (Part III), printed in Arabic-Indic numerals. The edition is diplomatic and line-anchored, in the format of the S07 edition of the notes on the tables: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names and its italics, and every line has a stable anchor.

The transcription is in progress. It begins at the title page of the glossary (p. 319) and runs page by page; pp. 319–327 are done (the introduction, pp. 319–321, and the entries from ابد to حرف).

## Read

- [Part II pp. 319 onward](p2_glossarium.pdf).

## Files

| File | Content |
|---|---|
| `pages/AB01-PDF####.txt` | The transcription of one printed page (master PDF page = printed page + 449). The format is described at the head of `build_glossarium.py`. |
| `build_glossarium.py` | Builds `p2_glossarium.tex`, the page records and the anchor list from the page files. It is the engine of `S07/adnotationes/build_adnotationes.py`, with the Arabic-Indic numerals set in the Arabic font, overlined letters of figures, a short rule of a given length, and the lines set at their printed baselines (`@baselines`, `@noterule`). |
| `records/AB01-PDF####.json` | One record per page in the S02 schema: the body and the footnote columns, line by line, with anchors, the TeX of each line and the transcription. Observations on the print are kept in `observations`. |
| `anchors.tsv` | Every printed line: anchor, printed page, section, transcription. |
| `check_observations.py` | Checks the line numbers named in the observations against the transcribed lines. |
| `fonts/NallinoSigns.otf` | The zero sign of the tables. |

## Conventions

- Anchors: `AB01-PDF0768-body-L004` is line 4 of the body of master PDF page 768 (printed p. 319); `notes_left`, `notes_right` and `notes` are the footnote columns.
- Each entry begins at the left margin with its Arabic headword, usually the unvowelled root, then a dash and the vowelled forms; its continuation lines are indented as printed (21.2 PDF points). The entries are anchored per page (`AB01-PDF0771-body-E01`, ...).
- Arabic is transcribed with the vowel signs, shaddas and sukūns that are printed. The page references to the Arabic text are transcribed in the Arabic-Indic digits of the print (U+0660–0669, ٢٥٦ = 256), most significant digit first; the line numbers printed beside them as small figures are transcribed as subscripts.
- Elongated joins (kashīda) are not transcribed, as in S07; the observations record them. A vowel sign printed over a join is given to its letter.
- Each Arabic example is a run read from the right inside the Latin text, which runs from the left. An example broken at the end of a line has its first words at the right end of that line and its last words at the beginning of the next; each line gives its own words in reading order.
- The vowel signs open the printed lines unevenly. Each page file gives the printed baselines of its lines (`@baselines`, measured on the scan) and the position of the rule over the notes (`@noterule`); the build sets every line there.
- Greek, Arabic, Syriac and Hebrew words, numbers and diacritics are read on enlarged images of the scan (up to 3,000 dpi).
- The Greek type has two sorts of theta, θ and ϑ; each is transcribed as printed. It casts ὁ (omicron with the rough breathing) as one sort that resembles δ (ὁ Κρατήρ, ὁ Βοώτης, ὁρίζων); it is transcribed ὁ.
- The rule over the footnotes is printed 115 points (40.6 mm) long and centred; the edition sets it so.
- A reading that departs from what one expects is kept as printed and described in the page record (for example «دراع» printed without the dot of dhāl on p. 319).

## Rebuild

```
python build_glossarium.py
xelatex p2_glossarium.tex
```

The fonts are those of S07: Linux Libertine O, Amiri, FreeSerif, Frank Ruhl Hofshi, Segoe UI Historic, Ebrima and Noto Serif.

This is not a human proofread.
