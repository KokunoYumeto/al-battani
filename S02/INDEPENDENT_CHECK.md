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

## Candidate "bounded_v006", printed pp. 1–40 (2026-09-26)

`candidate_v006_print001-040/` is ChatGPT's cumulative checkpoint (`S02_PRINT001_040_CHECKPOINT.zip`, 183 files, manifest 183/183).
Pp. 1–35 are byte-identical to v002 plus the pp. 31–35 extension. Pp. 36–40 (master PDF 125–129) are new.

- **Build.** The checkpoint records "BUILD_FAILURE_RECORDED". Its TeX includes `tex/tables/AB01-PDF0096-T01.tex` and `…0097-T01.tex`,
  which were not in the package, so XeLaTeX stopped after 7 pages. With those two files copied from v002 (the tables are unchanged),
  XeLaTeX ×2 builds cleanly here: 41 pages, no errors, no missing characters, no overfull boxes. That build is `pdf/S02_NALLINO_SOURCE_CANDIDATE_pp001-040.pdf`.
  There is no critical-apparatus PDF in this checkpoint; v002's covers pp. 1–30.
- **Completeness, pp. 36–40.** Word-trigram overlap with the scan's OCR layer is 78–94% in both directions on each page, with near-equal word counts.
- **Fidelity.** Printed pp. 38 and 39 were read against the scan in full.
  - They match: body, italicised geometric assertions, bracketed insertions, all ten notes of p. 38 (with the fraction GM = BC×FG/FB = BC×FM/FC),
    the numbers (1558ᵖ 51′, 25ᵖ 58′ 51″, 25° 39′ ½, 4082ᵖ 19′, 63ᵖ 54′, …), and the margin locators.
  - Both diagrams are exact crops.
- **Not included here.** `unverified/` (embedded-text extraction for PDF 130–198, which the checkpoint itself says is not transcription) and
  `qa/build_A`, `qa/build_B` (the two 7-page failed builds). Both are in the original ZIP.

## Candidate, printed pp. 41–43 (2026-09-26)

`candidate_print041-043/` holds ChatGPT's text-level LuaLaTeX candidate for master PDF 130–132, unchanged, next to a checked copy. The full record is in
[`S02_P041_043_CHECK.md`](candidate_print041-043/S02_P041_043_CHECK.md).

- **Build.** LuaLaTeX ×2 builds 3 pages with no errors, no missing characters and no overfull boxes. This holds for both files.
- **Completeness.** Word-trigram overlap with the OCR layer is 82–94% in both directions. The unmatched runs are hyphenation and OCR noise.
- **Fidelity.** All three pages were read line by line against the scan.
  - All nine flagged readings are resolved:
    - 285, not the OCR's 287
    - 1/20, [ἄρχων], 2/5 and PKLRMY as read
    - the note-4 formula transcribed
    - the order signs are small capitals (IV, V, VI)
    - note 9 reads 30^IV and 42^VI
    - two missing ")" kept as printed
  - Ten further readings are corrected:
    - two copied from the OCR layer: *efficiant*, *Pachon*
    - 365° for 365ᵈ, twice
    - "164, r." for "164,v."
    - the macron in al-Battānī (three places)
    - three dashes restored
    - an added parenthesis removed
  - Typography is aligned with pp. 1–40.
  - Every change is listed in `ledgers/checked_changes.tsv`.
- **Still paragraph-level.** Marginal locators (pp. 62–66 of the Arabic), line numbers and line-initial guillemets need the line-anchored form of pp. 1–40.
