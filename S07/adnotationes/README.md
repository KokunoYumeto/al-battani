# S07 — Nallino's notes on the tables (Part II pp. 189–317)

Nallino's *Adnotationes* to the tables of Part II: for each table, the codex readings, the sources, the history of the tables and the explanation of their construction. The edition is diplomatic and line-anchored, in the format of the S02 edition of Part I: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names and its italics, and every line has a stable anchor.

The transcription is in progress. It begins at the half-title (p. 189) and runs page by page.

## Read

- [Part II pp. 189 onward](p2_adnotationes.pdf).

## Files

| File | Content |
|---|---|
| `pages/AB01-PDF####.txt` | The transcription of one printed page (master PDF page = printed page + 449). The format is described at the head of `build_adnotationes.py`. |
| `build_adnotationes.py` | Builds `p2_adnotationes.tex`, the page records and the anchor list from the page files. |
| `records/AB01-PDF####.json` | One record per page in the S02 schema: the body and the footnote columns, line by line, with anchors, the TeX of each line and the transcription. Observations on the print (a letter that did not print, a printed «adp.» for «adn.») are kept in `observations`. |
| `anchors.tsv` | Every printed line: anchor, printed page, section, transcription. |
| `fonts/NallinoSigns.otf` | The zero sign of the tables. |

## Conventions

- Anchors: `AB01-PDF0641-body-L012` is line 12 of the body of master PDF page 641 (printed p. 192); `notes_left`, `notes_right` and `notes` are the footnote columns. `AB01-PDF0641-N02` marks the start of footnote 2, `-P03` the third paragraph, `-H01` a heading.
- Greek, Arabic, Hebrew, Syriac and Ethiopic are transcribed in their own scripts, with the vowel signs that are printed. The transliterations follow Nallino's system as printed (*ǵ*, *ḥ*, *ṭ*, *‘*, *’*).
- Greek, Arabic, Syriac and Hebrew words, numbers, abbreviations and diacritics were read on enlarged images of the scan (600 dpi, 1-bit).
- A reading that departs from what one expects is kept as printed and described in the page record.

## Rebuild

```
python build_adnotationes.py
xelatex p2_adnotationes.tex
```

The fonts are Linux Libertine O, Amiri, FreeSerif (Greek), Frank Ruhl Hofshi (Hebrew), Segoe UI Historic (Syriac), Ebrima (Ethiopic) and Noto Serif (the capitulum ⸿ of the Spanish quotations).

This is not a human proofread.
