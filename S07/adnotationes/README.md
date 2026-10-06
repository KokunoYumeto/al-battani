# S07 — Nallino's notes on the tables (Part II pp. 189–317)

Nallino's *Adnotationes* to the tables of Part II: for each table, the codex readings, the sources, the history of the tables and the explanation of their construction. The edition is diplomatic and line-anchored, in the format of the S02 edition of Part I: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names and its italics, and every line has a stable anchor.

The transcription covers all of the notes, from the half-title (p. 189) to the ornamental rule that closes them on p. 317, and the blank p. 318: 130 printed pages and 5,758 anchored lines. The tables that the notes print (the spurious tables of pp. 299–307 among them) are set in their columns, with the heads redrawn to the print (28 figure files). 430 observations on the print are kept in the page records.

## Read

- [Part II pp. 189–318](p2_adnotationes.pdf).

## Files

| File | Content |
|---|---|
| `pages/AB01-PDF####.txt` | The transcription of one printed page (master PDF page = printed page + 449). The format is described at the head of `build_adnotationes.py`. |
| `build_adnotationes.py` | Builds `p2_adnotationes.tex`, the page records and the anchor list from the page files. |
| `records/AB01-PDF####.json` | One record per page in the S02 schema: the body and the footnote columns, line by line, with anchors, the TeX of each line and the transcription. Observations on the print (a letter that did not print, a printed «adp.» for «adn.») are kept in `observations`. |
| `anchors.tsv` | Every printed line: anchor, printed page, section, transcription. |
| `figures/` | The redrawn table heads, figures and ornaments (TikZ); `figures/src/` holds the scripts that generate the table heads from positions measured on the print. |
| `check_observations.py` | Checks the line numbers named in the observations against the transcribed lines. |
| `fonts/NallinoSigns.otf` | The zero sign of the tables. |

## Conventions

- Anchors: `AB01-PDF0641-body-L012` is line 12 of the body of master PDF page 641 (printed p. 192); `notes_left`, `notes_right` and `notes` are the footnote columns. `AB01-PDF0641-N02` marks the start of footnote 2, `-P03` the third paragraph, `-H01` a heading.
- Greek, Arabic, Hebrew, Syriac and Ethiopic are transcribed in their own scripts, with the vowel signs that are printed. The transliterations follow Nallino's system as printed (*ǵ*, *ḥ*, *ṭ*, *‘*, *’*).
- Greek, Arabic, Syriac and Hebrew words, numbers, abbreviations and diacritics were read on enlarged images of the scan (400 to 2,400 dpi).
- A reading that departs from what one expects is kept as printed and described in the page record. An observation names the line or lines it concerns; `check_observations.py` reports the quoted words that stand on another line of the page. Its five remaining reports quote the context of the observation (for example «5° 2/3», named as the fraction printed before «11° 2/8»).

## Rebuild

```
python build_adnotationes.py
xelatex p2_adnotationes.tex
```

The fonts are Linux Libertine O, Amiri, FreeSerif (Greek and the astronomical signs), Frank Ruhl Hofshi (Hebrew), Segoe UI Historic (Syriac), Ebrima (Ethiopic) and Noto Serif (the capitulum ⸿ of the Spanish quotations).

This is not a human proofread.
