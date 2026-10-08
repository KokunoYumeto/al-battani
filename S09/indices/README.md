# S09 — Nallino's indexes (Part II pp. 359–413)

Nallino's two indexes to the edition: the *Index geographicus* (pp. 359–372) and the *Index historicus* (pp. 373–413). Each entry gives a name, often with its Arabic or Greek form transcribed in italics, and the places where it occurs: italic numbers are the places of al-Battānī's text, upright numbers those of Nallino's notes (as the introduction of p. 359 says); numbers after «II» are pages of Part II, the others of Part I. The edition is diplomatic and line-anchored, in the format of the S09 edition of the glossary: every printed line is one line of the edition, with its hyphenation, its punctuation, its letter-spaced names and its italics, and every line has a stable anchor.

The transcription is in progress. It begins at the title page of the Index geographicus (p. 359) and runs page by page; pp. 359–370 are done (the introduction and the entries from Ābaskūn to as-Sūs).

## Read

- [Part II pp. 359 onward](p2_indices.pdf).

## Files

| File | Content |
|---|---|
| `pages/AB01-PDF####.txt` | The transcription of one printed page (master PDF page = printed page + 449). The format is described at the head of `build_indices.py`. |
| `build_indices.py` | Builds `p2_indices.tex`, the page records and the anchor list from the page files. It is the engine of `S09/glossarium/build_glossarium.py` with a body in two columns: `@colL` and `@colR` begin the left and the right column of a page, each with its own printed baselines, and a thin rule is set between them as printed. |
| `records/AB01-PDF####.json` | One record per page in the S02 schema: the head of the page and the two columns, line by line, with anchors, the TeX of each line and the transcription. Observations on the print are kept in `observations`. |
| `anchors.tsv` | Every printed line: anchor, printed page, section, transcription. |
| `check_observations.py` | Checks the line numbers named in the observations against the transcribed lines. |
| `fonts/NallinoSigns.otf` | The zero sign of the tables (shared with the glossary). |

## Conventions

- Anchors: `AB01-PDF0808-col_left-L005` is line 5 of the left column of master PDF page 808 (printed p. 359); `col_right` is the right column and `body` the head of the page (title and introduction). The entries are anchored per column (`AB01-PDF0808-col_left-E01`, ...).
- Each entry begins at the left edge of its column; its continuation lines are indented as printed (10.7 PDF points). An entry that runs from the foot of one column to the head of the next continues there as a continuation line.
- The transcriptions of Arabic, Persian and other names keep the diacritics that are printed: macrons, the dots under ḥ, ṣ, ṭ, ḍ, ẓ, the ‘ of ʿayn and the ’ of hamza, and ǵ (g with an acute), Nallino's transcription of the letter jīm (ج), as in Ādharbayǵān and al-Aflāǵ. Small differences of the print (a dot over a macron, a letter printed broken) are kept or described in the page record.
- The lowercase ḥ of the transcriptions is cast as one sort whose dot below is joined to the foot of the h, so that at low resolution the letter looks like a b with a dot or an h with a breve below (al-Muḥammadiyyah, al-ḥaǵar, p. 367); it is transcribed ḥ. The other letters with a dot below (ṣ, ṭ, ḍ, ẓ, Ḥ) carry a separate round dot.
- Italic and upright numbers are distinguished as printed: they separate the places of al-Battānī's text from those of Nallino's notes.
- The lines are set at their printed baselines (`@baselines`, measured on the scan for each line of each column).
- The dot of i and the bar of ī are told apart by measurement (`_intake/notes/tools_s09/macron_audit.py` in the working files: a dot is 1.1–1.4 points wide and round, a bar 1.6–2.4 points wide and flat), since the two are hard to separate by eye in the bold type of the index.
- A reading that departs from what one expects is kept as printed and described in the page record.

## Rebuild

```
python build_indices.py
xelatex p2_indices.tex
```

The fonts are those of the glossary: Linux Libertine O, Amiri, FreeSerif, Frank Ruhl Hofshi, Segoe UI Historic, Ebrima and Noto Serif.

This is not a human proofread.
