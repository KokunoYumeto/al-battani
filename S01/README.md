# S01 v002 — Nallino Part I front matter and apparatus

**Current state: complete first-pass source coverage; technically checked candidate; S01 not finally closed.**

This release advances the first prompt only. It is a new, page-by-page transcription from the authoritative scans, not a relabelling of the earlier embedded-text extraction. No S02–S16 production was executed.

## Read the edition

The principal reader is [S01_NALLINO_SOURCE_v002.pdf](pdf/S01_NALLINO_SOURCE_v002.pdf). It contains 80 pages: one explicitly modern Latin editorial notice, followed by 79 historical pages (78 text-bearing source leaves and the astronomical frontispiece). The owned blank at physical PDF15 is recorded rather than typeset as a spurious text page.

Editable sources are [the complete TeX](tex/S01_NALLINO_SOURCE_v002.tex), [the page-anchored UTF-8 text](transcription/S01_NALLINO_SOURCE_v002.txt), and the structured records in `transcription/pages/`. The plain-text file retains raw LaTeX for mathematical expressions and named image references where exact glyph crops replace uncertain encodings. JSON preserves the formatting and language tags used to generate the reader.

[The separate three-page critical apparatus PDF](pdf/S01_CRITICAL_NOTES_v002.pdf), [its editable TeX](tex/S01_CRITICAL_NOTES_v002.tex), [expanded critical notes](CRITICAL_NOTES.md) and [the cumulative checkpoint](receipts/cumulative_checkpoint.json) state the unresolved issues and the precise continuation boundary. They are part of the delivery, not optional qualifications to a supposedly finished edition.

## Coverage and attribution

The session owns physical master PDF2, PDF10 and PDF12–89: 80 units. Every physical page PDF1–89 has a disposition. The text-bearing pages are PDF10, PDF12–14 and PDF16–89, totaling 78. PDF16–73 carry the preface (printed VII–LXIV), PDF74–78 the bibliography (LXV–LXIX), and PDF79–89 the addenda/corrigenda (LXX–LXXX).

All of these historical editorial materials are tagged `NALLINO_APPARATUS`, not al-Battānī’s authorial Arabic prose. Nallino’s intrinsic Arabic, Greek, Syriac and other quotations remain part of his apparatus. They are not a new parallel translation. The new first-page notice is tagged `MODERN_EDITORIAL`. No target translation language was requested for this S01 continuation, and no Arabic Zīj canonical checkpoint was used or altered.

The controlling file is `30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf`: 80,946,704 bytes, 1,162 physical PDF pages, SHA-256 `544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297`. The retrieval service’s 1,161-page label conflicts with the actual PDF structure and the packet manifest. All anchors here use the physical 1,162-page file, without shifting the page numbers.

The included [untouched source excerpt](source/SRC01_PDF0001-0089_EVIDENCE.pdf) preserves physical pages 1–89. Its 89 rendered pages match the corresponding master pages at the audit’s 36-dpi comparison resolution. The complete master remains a separately supplied project source, not an implied missing part of this S01 bundle.

## What changed from the preceding checkpoint

The previous checkpoint recorded preservation and unverified extraction, with no fully transcribed source unit. This candidate provides 3,996 source-line anchors across the complete S01 text range, 47 editable mathematical objects, the 11-entry printed transliteration key, and 86 routed historical addenda/corrigenda entries. The raw frontispiece and a conservative presentation crop are now included in the reader.

There are 28 tracked proof-repair/encoding decisions affecting 25 distinct source lines relative to the preserved first-pass snapshot. The full before/after comparison is [first_pass_text_changes.tsv](ledgers/first_pass_text_changes.tsv); the reasons and evidence are in [transcription_repairs.tsv](ledgers/transcription_repairs.tsv). Encoding-only repairs to four early construction files are recorded separately. No historical printed erratum is silently applied to an earlier source page.

The old checkpoint receipts and the pre-repair source records are retained under `history/`. Older proof images are evidence of the process, not the final edition. Only `pdf/S01_NALLINO_SOURCE_v002.pdf` and `qa/final/` represent the current reader.

## Images and difficult readings

The frontispiece is preserved from its native 300-dpi JPX image. The presentation derivative crops the provider UI bands on integer pixel bounds `[0, 312, 2491, 2766)`; it does not redraw, deskew, sharpen or fill the diagram. The source itself already truncates labels and outer material at its edges. The derivative cannot recover that loss and does not pretend to do so.

Native-pixel crops also preserve the preface and terminal ornaments, the Syriac word on PDF22, an orthographic sign on PDF70, and two Arabic corrigendum lemmas on PDF82. These four inline glyph images remain in the reader rather than being replaced by unsupported Unicode guesses. Two additional Arabic crops from PDFs20 and 41 remain evidence only: their consonantal readings were resolved and typed into the final source layer.

Eleven reading entries remain unresolved, principally small diacritics, unusual glyphs and a printed old/new lemma distinction. One additional flagged entry records the frontispiece’s pre-existing source loss. See [critical_findings.tsv](ledgers/critical_findings.tsv) and [unresolved_readings.tsv](ledgers/unresolved_readings.tsv). A bounded uncertainty is not permission to invent a reading.

## Ledgers and provenance

The ledgers provide page dispositions, line alignment, figures, mathematical notation, the transliteration key, literal numeric strings, historical corrigendum routes, recorded witness variants, source identities, repairs and open findings. JSON and TSV versions are supplied. The numeric-literal index is a search aid, not a recomputation or a claim that every numeral has received an independent second check.

Source line identifiers refer to the page, section and ordinal within that section. Where a PDF rectangle was estimated using the embedded-text layer, the ledger explicitly labels it an unverified locator candidate. These rectangles are not presented as 3,996 independently measured word/line boxes. Exact native image crop rectangles are separately recorded in `figure_provenance.json`.

Nallino’s descriptions of other manuscripts and authors remain historical testimony in his voice. They do not constitute a new collation of missing manuscripts, a modern factual endorsement, or a correction based on outside research.

## Builds and checks

Two clean build directories were used, with two XeLaTeX passes in each. Both outputs are byte-identical, and all 80 page rasters match between builds at 36 dpi. There are zero missing-character reports, overfull boxes, source-line width overflows or font warnings in either final log. Reader SHA-256: `ea44955e9074edacb1a076626facb7f818e5cfb9795591eb5307661214f475bd`.

The read-only [technical audit](receipts/technical_audit.json) passes 29 checks covering identities, page and line coverage, markup, native crop equality, formula/key/corrigendum linkage, canonical digests, deterministic builds, reader anchors and page bounds. It confirms that it did not patch production outputs. It does **not** certify the historical readings: a separate executable is not an independent philological reviewer.

All seven final contact sheets were inspected, covering all 80 reader pages. Detailed proofs include the frontispiece, dense notes, mathematical pages, orthographic examples, glyph fallbacks and last page. The final page was also rendered and inspected using Poppler. Scope and limitations are recorded in [visual_qa.json](receipts/visual_qa.json).

## Rebuilding and auditing

From the extracted package directory, run:

```sh
python scripts/rebuild.py
python scripts/audit_readonly.py --master /path/to/30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf
```

The build needs Python with PyMuPDF, XeLaTeX and the listed TeX packages, plus system fonts Linux Libertine O, FreeSerif, Amiri and Noto Sans Syriac. Pillow is needed for native-crop auditing; Poppler is needed to regenerate the second-renderer proof. Font files are not distributed. The pinned build epoch is 2026-09-25 00:00 UTC; exact byte reproduction additionally depends on the recorded TeX/font environment. Font identities and the engine are documented in receipts, without bundling font binaries.

The `batch_*.py` files and proof-repair scripts are production history, not the rebuild entry point. Rerunning those scripts can recreate superseded first-pass states. Build the current edition from the final page JSON records with `rebuild.py` instead.

## Continuation boundary

`last_fully_transcribed_source_unit` is `AB01-PDF0089`, qualified as complete first-pass coverage with disclosed uncertainties and image dispositions. There is no wholly untouched page remaining **within S01**. `last_fully_verified_source_unit` remains null because the independent cold source/reading audit has not been performed.

S01 therefore remains open for the bounded reading decisions and independent cold audit, not for another round of bulk extraction. The documented source loss may be accepted as a source limitation; it need not be conjecturally repaired. Any accepted correction after this candidate must create a successor checkpoint and preserve this one. No human-only approval gate is imposed. S02 has not begun.

## Source citation

Nallino, C. A. (1903). [Front matter, preface, bibliography, and addenda]. In *Al-Battānī sive Albatenii opus astronomicum* (Pars prima: *Versio capitum cum animadversionibus*, pp. VII–LXXX). Ulrich Hoepli. Controlling digital witness: SRC01, physical PDF2, PDF10 and PDF12–89.

Historical editorial authorship: Carlo Alfonso Nallino. Digital transcription, markup, proofs and technical checks: AI-assisted production in this conversation, 2026. Source-provider and holding-copy matter are retained only in the source evidence and provenance, not silently included as scholarly text.
