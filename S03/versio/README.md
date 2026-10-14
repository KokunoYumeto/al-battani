# S03 — Nallino's Latin translation of the *Zīj* with his notes (Part I), pp. 110–218

Part I of Nallino's edition is his Latin translation of al-Battānī's *Zīj*, with his footnotes (the readings of the codex and of Plato of Tivoli's version, corrections and references) and, after the translation, his commentary. This folder continues the edition of the translation from printed p. 110 (master PDF page = printed page + 89) to p. 218. Printed pp. 1–53 are in [S02 candidate v009](../../S02/candidate_v009_print001-053/README.md) and pp. 54–109 in [S02/versio](../../S02/versio/README.md), in the same line-anchored layout.

The edition is diplomatic and line-anchored: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names, its italics and its bold italic reference letters, and every line has a stable anchor. The line numbers that the print sets beside every fifth line and the locators of the Arabic text («p. 84.») stand in the margins as printed.

**Done:** pp. 110–111 (2 pages, 98 anchored lines).

**Contents so far:** chapter 44 continued (from p. 110).

## Read

- [p1_versio.pdf](p1_versio.pdf): the pages transcribed so far.

## Files

| File | Content |
|---|---|
| `pages/AB01-PDF####.txt` | The transcription of one printed page. The format is described at the head of `build_versio.py`. |
| `build_versio.py` | Builds `p1_versio.tex`, the page records and the anchor list from the page files. |
| `records/AB01-PDF####.json` | One record per page in the S02 schema: the body and the footnote columns, line by line, with anchors, the TeX of each line, the transcription, the printed line number and the marginal locator. Observations on the print are kept in `observations`. |
| `anchors.tsv` | Every printed line: anchor, printed page, section, transcription. |
| `figures/` | The redrawn figures (TikZ), one file per figure; `figures/src/` holds the measurements of each figure (circles and lines fitted to the printed ink, the boxes of the letters) and `make_figure.py`, which writes the TikZ file from them. |
| `check_observations.py` | Checks the line numbers named in the observations against the transcribed lines. |
| `fonts/NallinoSigns.otf` | The zero sign of the tables (loaded by the preamble that this edition shares with the notes on the tables). |

## Conventions

- Anchors: `AB01-PDF0199-body-L019` is line 19 of the body of master PDF page 199 (printed p. 110); `notes_left` and `notes_right` are the footnote columns. `AB01-PDF0199-N02` marks the start of footnote 2, `-P03` the third paragraph of the page.
- Degrees, minutes and seconds are written with the signs that are printed (89° 30′, 0*ᵖ* 31′ 25″: the *p* of the parts is a raised italic letter).
- Arabic and Greek are transcribed in their own scripts, with the signs that are printed. The transliterations follow Nallino's system as printed. The ‘ayn of a transliteration is the turned comma ‘ that the print sets (rabī‘, sha‘bān), as in the notes on the tables (S07).
- A reading that departs from what one expects is kept as printed and described in the page record.

## How the pages are made and checked

Each page is transcribed from images of the master scan; the text layer of the scan serves only as a first draft and for the positions of the lines. Numbers, Arabic, Greek, dashes and doubtful marks are read on enlarged images (600 dpi and more). After the build, every printed line is set above the same line of the built edition and the two are compared, line by line, for the whole page.

## Rebuild

```
python build_versio.py
xelatex p1_versio.tex
```

The fonts are Linux Libertine O, Amiri and FreeSerif (Greek), with those of the shared preamble.

This is AI-integrated work; no person has reviewed it.
