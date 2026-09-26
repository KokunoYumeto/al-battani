# S02 v009 — accepted scan corrections and cumulative continuation

## What this successor changes
The user’s scan-checked readings for printed pages41–43 (physical PDF130–132)
are accepted. All nine U-flags are closed. The additional macrons, punctuation,
time units, small-capital sexagesimal order signs, italics, spaced names and164-verso
locator are incorporated. The five outstanding margin locators, printed line
numbers and repeated line-initial quotation signs are encoded in the line form.
The source seam43/44 is preserved exactly; no word is supplied or dropped.

The named checked TeX file was not found. This successor implements the complete
correction message; it does not claim to have imported that separately named file.

## Contents
- `tex/S02_P041_043_checked.tex`: self-contained checked block; inputs no page files.
- `pdf/S02_P041_043_checked.pdf`: built only when the recorded build succeeded.
- `tex/S02_NALLINO_SOURCE_v009.tex`: cumulative historical reader, pp.1–53.
- `tex/S02_P044_053_source_replayed.tex`: separate continuation candidate.
- `transcription/pages`: contiguous page records1–53; first40 byte-unchanged.
- `ledgers/accepted_user_corrections.tsv`: every accepted reading/style/line-form edit.
- `ledgers/page_disposition.tsv`: all109 assigned pages; untouched pages are explicit.
- `source`: original-image evidence and documented native-pixel crops.
- `receipts`: actual build logs, source-excerpt pixel checks and exact checkpoint.

## Status and responsibility
This is not completion of S02. User scan verification is credited as such;
restored line-anchored continuation pages are candidates, not newly certified
philological readings. A successful technical build is not a visual reading audit.
The current export does not assert that the newly generated render has received
final visual inspection. One damaged glyph at PDF140l1 is preserved as an image;
the hidden part is not guessed. Printed mathematical/reference discrepancies stay
in the text and are documented separately.

No Arabic canonical change, new target-language translation, S01 modification,
or S03 production is included. Human certification is not required to continue.

## Rebuild
Install XeLaTeX with the fonts named in the TeX preamble (font binaries are not
included). From `tex/`, run XeLaTeX twice on the named document. Relative paths to
`source/presentation` and the restored historical table dependencies are retained.
`python scripts/build_edition.py` regenerates the TeX from page records and the
unchanged historical first40 TeX held under `history/`.
`new_pages.py` is the construction record; do not rerun it as a review operation:
it precedes the responsibility/status updates recorded by `finalize.py`.

Continue at physical PDF143 / printed page54. See
`receipts/cumulative_checkpoint.json` for granular verification, not merely a
single inherited last-verified value.
