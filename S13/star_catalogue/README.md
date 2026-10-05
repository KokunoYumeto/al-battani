# S13 — The star catalogue, in both of Nallino's versions

Al-Battānī's catalogue of fixed stars for the year 1191 of Dhū ’l-qarnayn, as Nallino prints it twice:

| Witness | Pages | What it is |
|---|---|---|
| **Part III** (Arabic) | printed pp. 245–274 (master PDF 907–878) | The tables of the codex (Escorial, ár. 908), with the numbers in **Maghribi abjad** and the codex's special zero sign, plus Nallino's footnotes. |
| **Part II** (Latin) | printed pp. 144–177 (master PDF 593–626) | Nallino's Latin version, *Situs et magnitudines stellarum fixarum anno 1191 a Dhū ’l-qarnayn*, with Western numerals, star identifications and his notes on the codex readings. |

Both are transcribed from the scan as printed. Neither is corrected from the other.

## Read

- [Part III edition, 30 pp.](p3_star_catalogue.pdf): the Arabic tables, one page per printed page, right to left. The zero sign is set in its own font (below).
- [Part II edition, 34 pp.](p2_star_catalogue.pdf): the Latin tables with Nallino's notes, one page per printed page.

## Data

| File | Content |
|---|---|
| `p3_stars.tsv` | Part III rows in reading order: page, row, kind (star, heading, title, column head, centred line), the Arabic description, the six cells as printed, the linked Part II star, and reading notes (`doubt`). |
| `p3_footnotes.tsv`, `p3_pages.tsv` | Nallino's footnotes to Part III; the printer's signatures. |
| `p2_stars.tsv` | Part II rows: number, description, longitude, latitude, *plaga caeli*, magnitude, identification. |
| `p2_notes.tsv` | Nallino's Part II notes, with the codex readings he reports in a structured column (e.g. `lon_d=287;lon_m=20`, `mag=4`, `dir=N`). |
| `p2_pages.tsv` | Running heads, section titles and signatures of the Part II pages. |
| `discrepancies.tsv` | Every difference between the two witnesses that Nallino's notes do not explain, and every slip found in the notes, each checked in two scan copies. |
| `star_catalogue_joined.tsv` / `.json` | One row per Part III star: raw Arabic cells, decoded values, the Part II values, the codex readings from the notes, and a status per field. |

## Counts

- Part III: 489 star rows, of which 488 are linked to a Part II star. The extra row is a star the codex repeats (Aquarius 19), which Nallino leaves out of Part II.
- Part II: 489 stars in 46 constellations, with 342 notes; 218 of the notes give structured codex readings.
- A folio of the codex is lost: Argo Navis, Hydra and the first stars of Crater are missing from both versions (Part III p. 270, note 2; Part II p. 172).

## How the two versions were checked

Every Part III cell was read from the scan at 500–1200 dpi and decoded from the abjad. It was then compared with Part II: longitude (degrees, minutes), latitude (degrees, minutes), direction and magnitude. A blank direction cell repeats the one above it, and a vertical bracket covers its rows.

| Result | Cells |
|---|---|
| Agrees with Nallino's Part II value | 2,604 |
| Differs, and Nallino's note gives exactly this codex reading | 279 |
| Differs, with no matching note (ledgered) | 45 |
| Open | 0 |

Each structured codex reading in the notes was also checked the other way: it must equal the Part III reading.

Every unexplained difference was read again in a second, independent copy of the print (Internet Archive, `albattanisivealb00batt`; there the Part III page is master PDF − 865). Only differences that both copies show are ledgered.

Most ledger entries are probably misprints in one witness or omissions in Nallino's notes. A few are slips in the notes themselves:
- notes printed under the wrong star number (Corvus 5/6, Pisces 16/17, Piscis Australis 3/4);
- a note that gives the codex and edition values the wrong way round (Leo 12).

Run `python check_stars.py` to repeat the check (it exits non-zero on any unledgered difference), and `python build_joined.py` to rebuild the joined dataset.

## Conventions in the data

| Markup | Meaning |
|---|---|
| `{0}` | The codex zero sign (a ring with a bar); value 0. |
| `{zero:لا}` | A word printed for "none" in a number cell; the check reads it as 0 (Nallino: "Scilicet {0}"). |
| `{rd:ر=ز}` | The print shows the first glyph (here a ز without its dot); it is read as the second. The edition prints the first, the check uses the second. |
| `{fnN}` | Footnote mark N. |
| `{ov:اقضا}` | Overlined numeral (year numbers in titles). |
| `{BR:الشمال:n}` / `{BR}` | The vertical direction bracket and the rows it covers. |
| `{sp:…}` | Letter-spaced name; `*…*` italic, `**…**` bold, as printed. |
| ` / ` | Line break inside a cell. |

Further conventions:
- **Harakat** are transcribed as seen at 450–1000 dpi.
- **Kashida** (letter stretching) is not recorded; the `doubt` column lists where it occurs.
- **Dotless letters** in Part III are transcribed as printed and noted in the `doubt` column, e.g. a medial tooth without dots read as ى (10).
- **Nallino's own notes** are transcribed as printed, slips included.
- **Shifted rows.** In Lepus and Canis Major, the codex lost a star name but kept its numbers. Each row is linked to the star whose numbers it carries, and the `doubt` column names the star of the description. Piscis Australis 1–2 is handled the same way.

## The zero sign

The print's zero is not in Unicode. It was traced from the 600-ppi scan into a one-glyph OpenType font, `fonts/NallinoSigns.otf`, at U+E000 (script: `tools/make_zero_font.py`). The editions use it as `\AbjadZero`.

## Rebuild

```
python gen_stars.py
xelatex p3_star_catalogue.tex
xelatex p2_star_catalogue.tex
```

This needs XeLaTeX with polyglossia, Amiri, Linux Libertine O and FreeSerif.

The scripts in `tools/` cut page and cell images from the scans used for reading. They expect the scans at local paths.

## Not done yet

- An independent second reading of the Part III text (the descriptions and their harakat) by a reader other than the transcriber.
- Nallino's general remarks after the tables (*animadversiones generales*) are not part of this batch.

## Credits

- al-Battānī: the catalogue.
- C. A. Nallino: the edition of the codex (Part III), the Latin version and the notes (Part II), Milan 1899–1907.
- Transcription, data model, checks and the zero-sign font: AI-integrated work in this repository, 2026.
