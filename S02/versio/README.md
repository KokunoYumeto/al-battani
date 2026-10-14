# S02 — Nallino's Latin translation of the *Zīj* with his notes (Part I), pp. 54–109

Part I of Nallino's edition is his Latin translation of al-Battānī's *Zīj*, with his footnotes (the readings of the codex and of Plato of Tivoli's version, corrections and references) and, after the translation, his commentary. This folder continues the edition of the translation from printed p. 54 (master PDF page = printed page + 89). Printed pp. 1–53 are in [candidate v009](../candidate_v009_print001-053/README.md), an earlier package in the same line-anchored layout.

The edition is diplomatic and line-anchored: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names, its italics and its bold italic reference letters, and every line has a stable anchor. The line numbers that the print sets beside every fifth line and the locators of the Arabic text («p. 84.») stand in the margins as printed.

**Done:** pp. 54–91 (38 pages, 1,944 anchored lines).

**Contents so far:** chapter 30 continued (pp. 54–63): the anomaly of the Moon on the epicycle, what al-Battānī keeps of Ptolemy's lunar motions and what he corrects, the causes of the eclipses of the Moon and of the Sun, the two eclipses of the Sun and the two eclipses of the Moon that al-Battānī observed, with their computed places and what Ptolemy's reckoning would give, the diameters of the Moon, of the Sun and of the shadow that follow from them, the distance of the Sun after Ptolemy, with his figure of the three circles and the cone of the shadow redrawn (p. 59), Ptolemy's reckoning of the distances and the sizes of the Sun, the Moon and the Earth and of the length of the shadow (p. 60), al-Battānī's own distances of the Moon and of the Sun (p. 61), and the light and the phases of the Moon, with the figure of ten discs of the Moon round the Earth redrawn (pp. 61–62), and how it is read (p. 63); chapter 31, on the spheres and the states of the planets (from p. 63): the four circles of each planet, the columns of the tables of equation, and the figure of the circles of a planet redrawn, with the true and the mean apogee of the epicycle (p. 64), when the equation of anomaly and centre is added and when subtracted, and the cause of the retrogradations and of the stations (p. 65); al-Battānī's corrections of the motions, the apogees and the latitudes of the planets (p. 66); chapter 32, on the eras of the Arabs, the Romans, the Copts and the Persians (from p. 66): the months of the four calendars, with the Greek names of the Coptic months, and the reckoning of the first day of an Arab year and of an Arab month (p. 67), of a Roman, a Persian and a Coptic year and month (p. 68), and the conversion of one era into another (pp. 68–71); chapter 33, on the mean and the true places of the Sun by the Roman and the Arab era, with the apogee of the Sun and its motion (pp. 71–72); chapter 34, on the corrected (equal) hours after the noon of ar-Raqqah in any place (pp. 72–73); chapter 35, on the reckoning of the ascendant and of the twelve houses by the hours, and of the hours by the ascendant (pp. 73–74); chapter 36, on the true place of the Moon in the ecliptic (p. 75); chapter 37, on the place of the northern node, the head of al-ǵawzahar (pp. 75–76); chapter 38, on the latitude of the Moon and its side (p. 76); chapter 39, on the cause of the parallax of the Moon, its parallax in latitude and in longitude, the parallaxes of Venus, Mercury and the Sun, the four limits and the reckoning of the distance of the Moon and of the Sun, the parallax of the Moon in the circle of altitude, its angles of longitude and latitude, the parallaxes of the Moon and of the Sun from the tables, the apparent place and latitude of the Moon, the correction of the angles for the latitude of the Moon, and Theon's tables of parallax and their use (pp. 76–84); chapter 40, on the distance of the Moon from the Earth by its parallax in the circle of altitude (pp. 84–85); chapter 41, on the first visibility of the new Moon, the azimuth of its place and the figure of the Moon, with al-Battānī's arc of visibility of about 12 degrees (from p. 85), the correction of the arc by the elongation and by the distance of the Moon (pp. 87–88), the morning visibility at the end of the month (p. 89), and the figure of the new Moon with its horns, redrawn (pp. 89–90), and how the new Moon is sighted with a rule or a pierced tube and an astrolabe, with the figure of the horizon, the ecliptic and the astrolabe redrawn (pp. 90–91).

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

- Anchors: `AB01-PDF0144-body-L019` is line 19 of the body of master PDF page 144 (printed p. 55); `notes_left` and `notes_right` are the footnote columns. `AB01-PDF0144-N02` marks the start of footnote 2, `-P03` the third paragraph of the page.
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
