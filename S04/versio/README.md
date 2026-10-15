# S04 — Nallino's Latin translation of the *Zīj* with his notes (Part I), pp. 219–327

Part I of Nallino's edition is his Latin translation of al-Battānī's *Zīj*, with his footnotes and, after the translation, his commentary. This folder continues the edition of the commentary from printed p. 219 (master PDF page = printed page + 89) to p. 327. Printed pp. 1–53 are in [S02 candidate v009](../../S02/candidate_v009_print001-053/README.md), pp. 54–109 in [S02/versio](../../S02/versio/README.md) and pp. 110–218 in [S03/versio](../../S03/versio/README.md), in the same line-anchored layout.

The edition is diplomatic and line-anchored: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names, its italics and its bold italic reference letters, and every line has a stable anchor.

**Done:** pp. 219–234 (16 pages, 653 anchored lines).

**Contents so far:** the commentary on chapter 28, continued (from p. 219): the longitudes of the apogee of the Sun of the Arabic astronomers concluded, the lines EF and EG of p. 46 recomputed, and the equation of the centre, with the figure after Almagest III, 5, redrawn, and al-Battānī's formula for its sine (p. 219); the formula derived for the epicycle and for the eccentric, with the second figure redrawn, the simpler forms with the tangent, and the beginning of the radii of the epicycles (p. 220); the radii of the epicycles of the Moon and the planets in a table with the readings of the codex and of Plato and the values of Ptolemy and al-Farghānī; chapter 29: the day counted from noon and from midnight, and Schiaparelli on the equation of time (p. 221), concluded: the mean times of Ptolemy and al-Battānī and the 18′ added to the Moon, Ibn Yūnus' five methods after Delambre, and the mean place of the Sun (p. 222); Theon's conversion of true into mean time, Delambre on the modern equation of time, Schiaparelli on the obscure passage of p. 49, and chapter 30: the emended figure of p. 51 (p. 223); the figure of p. 51 as the codex and Plato draw it, redrawn, with Schiaparelli on its errors, the greatest equations of the Moon after Ptolemy and the moderns, the variation, and the beginning of a note on an interpolation in p. 53 (p. 224); its end, and Schiaparelli on the lunar tables: the motion in latitude 3′ a century below Ptolemy's, why that correction is small beside the correction in longitude, and a table of the inclination and the mean motions in 100 years of Ptolemy, al-Battānī and Hansen (p. 225); Schiaparelli's verdict on these motions, and the yearly motions of the Tabula Probata, Ḥabash and al-Battānī against Ptolemy's in a table; the shadow of the Earth reaching the sphere of Venus; why Mercury and Venus are never eclipsed; and the solar eclipse of 891 (p. 226); Halley's emendations, and the eclipse of 891 recomputed from al-Battānī's tables: the mean motions summed from the era, the true places of the Sun and the Moon, and the Moon's distance from the node and latitude (p. 227); the elements of that eclipse against the codex, Plato and Halley's emendations, with two corrections of the codex, and the solar eclipse of 901 at Antioch: true and mean times and the mean motions (p. 228); that eclipse recomputed: the true places of the Sun and the Moon, the Moon's distance from the node and latitude, and the elements against the codex, Plato and Halley, with three corrections of the codex (p. 229); the lunar eclipse of 883 at ar-Raqqah: its time, its computation from al-Battānī's tables and the beginning of the comparison with the codex, Plato and Halley (p. 230); the end of that comparison, with Schiaparelli's emendation of the codex, and the lunar eclipse of 901 at Antioch: its time and its computation from al-Battānī's tables (p. 231); the elements of that eclipse against the codex, Plato and Halley, with three corrections of the codex, and Schiaparelli's general remarks on the four eclipses: their agreement with al-Battānī's tables, in a table of the errors of elongation and of time, and the beginning of the comparison with the modern lunar tables (p. 232); Ginzel's corrections of Oppolzer's Canon and Schram's tables, the reductions of al-Battānī's mean time and of the meridians of Antioch and ar-Raqqah to Greenwich, and a table of the four syzygies after al-Battānī and after Oppolzer and Ginzel (p. 233); the magnitudes of the lunar eclipses after Oppolzer, and notes on p. 58: the distance of the Moon in the epicycle, with the figure of the triangle AEL redrawn, the difference of the latitudes, al-Battānī's lunar diameter, and the beginning of the hourly motions of the Moon (p. 234).

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

- Anchors: `AB01-PDF0308-body-L019` is line 19 of the body of master PDF page 308 (printed p. 219); `notes_left` and `notes_right` are the footnote columns. `AB01-PDF0308-N01` marks the start of footnote 1, `-P03` the third paragraph of the page.
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
