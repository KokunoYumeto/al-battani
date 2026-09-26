# S02 v002 — independent check (2026-09-26)

This package was produced and self-checked by ChatGPT. The check below was made separately, by Claude,
against the package's own source excerpt (`source/SRC01_PDF0090-0119_EVIDENCE.pdf`). It is a spot check
by a second model, not a human proofread and not a full collation.

- **Manifest:** `scripts/verify_manifest.py` verifies all 212 listed files.
- **Completeness (all 30 pages):** word trigrams of the transcription export
  (`transcription/S02_NALLINO_SOURCE_v002.txt`) were compared page by page with the scan's OCR text layer,
  in both directions. Overlap is 74–95% on every page (the OCR layer is noisy), and the word counts are
  close: 13,262 transcribed against 13,628 OCR words, which also include running heads and scan noise.
  The unmatched runs on the lowest pages (PDF98, 101, 106, 107) are OCR misreadings — "dela mbre nola vit"
  for *Delambre notavit*, "plole diectis maeus" for *Ptolemaeus*, split Arabic names — or markup in the
  export (fractions, image-object references). No omitted or added passage was found.
- **Fidelity (printed pp. 7 and 12, read against the scan):**
  - Prose and notes match word for word, numbers included (e.g. 47° 42′, 23° 51′, 12° 26′, 59° 36′,
    23° 35′).
  - Printed readings are kept as printed (p. 7 *at eo maiorem*).
  - All 121 cells of the table on p. 7 match; the damaged numeral in row 3 is kept as an exact image,
    as is the damaged digit in note 4 on p. 12, rather than being guessed.
  - The marginal Arabic-page locators appear as *In margine fontis* lines.
  - Differences are layout only: no paragraph indents, and the source's marginal line numbers are not
    printed in the reader.

Not included in this repository: `qa/source/` (28 reading renders of source pages, 19 MB), which are
intermediate. They remain in the archived package (`AB01_S02_v002.zip`) on Zenodo, so the package
manifest lists them.

## Extension, printed pp. 31–35 (2026-09-26)

`extension_print031-035/` holds five page records (master PDF 120–124), delivered separately from v002. It extends the
v002 records and does not replace them. It has no reader PDF or TeX yet.

- **Manifest:** 7/7 files verified.
- **Completeness:** word-trigram overlap with the scan's OCR text layer is 85–95% in both directions on each page (PDF 120–124),
  with near-equal word counts (2,206 transcribed against 2,260 OCR words).
- **Fidelity (printed p. 32, against the scan):** body, chapter heading, both note columns and the margin locators ("p. 48.", "p. 49.")
  match line for line, including the Arabic *mayl* (ميل) and "(i. e. cos δ)".
