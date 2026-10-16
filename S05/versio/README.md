# S05 — the front matter of Nallino's Part II, pp. [I]–XXXII

Part II of Nallino's edition (Milan, 1907) holds his Latin version of all the tables of the *Zīj*, with his remarks, a glossary and indexes. Its front matter, printed pp. [I]–XXXII (master PDF page = printed page + 417; the pages without a printed number are given in square brackets), holds the half-title, the title page and its verso with the imprint, Nallino's Praefatio, the Conspectus librorum orientalium (the list of the Oriental books cited) and the Addenda et emendanda to the three volumes. This folder edits it in the line-anchored layout of the Latin translation: printed pp. 54–109 of Part I are in [S02/versio](../../S02/versio/README.md), pp. 110–218 in [S03/versio](../../S03/versio/README.md) and pp. 219–327 in [S04/versio](../../S04/versio/README.md).

The edition is diplomatic and line-anchored: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names, its small capitals and its bold, and every line has a stable anchor.

**Done:** pp. [I]–[IV] (4 pages, 20 anchored lines).

**Contents so far:** the half-title, *Al-Battānī sive Albatenii opus astronomicum* (p. [I]), and its blank verso (p. [II]); the title page: Pubblicazioni del Reale Osservatorio di Brera in Milano, N. XL, Parte II; *Al-Battānī sive Albatenii opus astronomicum*, edited in Arabic from the Escorial codex, translated into Latin and annotated by Carlo Alfonso Nallino; Part II: the version of all the tables with remarks, a glossary and indexes; Milan, Ulrico Hoepli, 1907 (p. [III]); its verso with the imprint: Rome, 1907, printed by C. De Luigi (p. [IV]).

## Read

- [p1_versio.pdf](p1_versio.pdf): the pages transcribed so far.

## Files

| File | Content |
|---|---|
| `pages/AB01-PDF####.txt` | The transcription of one printed page. The format is described at the head of `build_versio.py`. |
| `build_versio.py` | Builds `p1_versio.tex`, the page records and the anchor list from the page files. |
| `records/AB01-PDF####.json` | One record per page in the S02 schema: the lines of the page with their anchors, the TeX of each line and the transcription. Observations on the print are kept in `observations`. |
| `anchors.tsv` | Every printed line: anchor, printed page, section, transcription. |
| `figures/src/make_figure.py` | Writes the TikZ file of a redrawn figure or ornament from its measurements, as in S04. |
| `check_observations.py` | Checks the line numbers named in the observations against the transcribed lines. |
| `fonts/NallinoSigns.otf` | The zero sign of the tables (loaded by the preamble that this edition shares with the notes on the tables). |

## Conventions

- Anchors: `AB01-PDF0420-body-L001` is line 1 of master PDF page 420 (printed p. [III]). Lines are counted on each page from its first printed line.
- The display lines of the title pages are set in the roman of the edition: the faces of the print are not imitated. Each line is scaled to a box as wide and as high as the printed line, both enlarged in the ratio of the measures (532.9 to 424.4 pt), and set in bold where the print uses a bold face. The rules are enlarged in the same ratio and keep their printed thickness.
- Marks of the scanned copy (the perforated stamp of the owning library, the mark of the digitization) are not part of the print and are not transcribed.

## How the pages are made and checked

Each page is transcribed from images of the master scan; the text layer of the scan serves only as a first draft and for the positions of the lines. Numbers, Arabic, dashes and doubtful marks are read on enlarged images (600 dpi and more). After the build, every printed line is set above the same line of the built edition and the two are compared, line by line, for the whole page.

## Rebuild

```
python build_versio.py
xelatex p1_versio.tex
xelatex p1_versio.tex
```

The fonts are Linux Libertine O, Amiri and FreeSerif (Greek), with those of the shared preamble.

This is AI-integrated work; no person has reviewed it.
