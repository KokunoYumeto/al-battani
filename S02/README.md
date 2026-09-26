# Al-Battani — S02 v002

## Current deliverable

This is an **editable, source-read transcription of Nallino Part I printed pp. 1–30**, corresponding to controlling master PDF90–119. It is not another embedded-text extraction or a full-page scan wrapper. The 31-page reader contains one modern Latin notice followed by the 30 historical source pages. The separate, two-page English critical apparatus explains seven reading/provenance findings; it is not a translation of the historical text.

S02 owns printed pp. 1–109 / master PDF90–198. **79 pages remain untranscribed. The next transcription page is master PDF120 / printed p. 31.** S01 is not revised or reopened here; the earlier conversational closure is carried forward, with the limits of the recovered receipts documented in `receipts/input_continuity.json`. S03 has not begun.

## Start with these files

- `pdf/S02_NALLINO_SOURCE_v002.pdf`: historical Latin translation and Nallino’s apparatus, with intrinsic Greek/Arabic quotations retained.
- `pdf/S02_CRITICAL_NOTES_v002.pdf`: separate modern critical notes and limitations.
- `transcription/pages/AB01-PDF0090.json` through `AB01-PDF0119.json`: editable production data. These files, not the old extraction or draft scripts, are the source for rebuilding.
- `transcription/S02_NALLINO_SOURCE_v002.txt`: UTF-8, line-anchored export; mathematical markup and image-object references are explicit.
- `tex/S02_NALLINO_SOURCE_v002.tex` and `tex/S02_CRITICAL_NOTES_v002.tex`: generated TeX.
- `source/SRC01_PDF0090-0119_EVIDENCE.pdf`: preserved source excerpt, including extrinsic scan matter as evidence only. Every page was raster-compared with the master.
- `receipts/cumulative_checkpoint.json`: exact continuation state.

## Coverage and editorial decisions

The batch includes 1,379 source-text line anchors, 80 marginal-register records, 101 explicitly encoded mathematical spans, two editable 11 × 11 tables (242 cells including headers), and two native-resolution diagram crops. Sixteen chapter headings are registered; this is not a claim that all sixteen chapters end within this batch.

The tables have matching literal CSV/TSV exports in `tables/` and cell provenance in `ledgers/table_cell_provenance.json`. One damaged table numeral remains an image marker, not a number inferred from the table pattern. Two further uncertain character objects in notes are preserved as exact images. Raw and presentation crops are byte-identical; no lines or labels were redrawn or strengthened.

Printed inconsistencies remain visible: the two different latitude values on p. 16, an apparent repeated word ending across pp. 16–17, and the duplicate note call on p. 10 are not silently repaired. Corrections of the working digital transcription are recorded separately in `ledgers/working_repairs.json`. One render check caught and repaired an escaped multiplication command; the repaired version was rebuilt twice and inspected again.

The historical prose is tagged `NALLINO_TRANSLATION`; Nallino’s notes and marginal evidence are tagged `NALLINO_APPARATUS`. No Arabic canonical text was created or modified, and no new target-language translation was generated. The 46 Arabic-page references copied from the printed margins are **locators only**, not completed Arabic collation.

## Source identity and coordinate limits

Controlling source: `30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf`, 80,946,704 bytes, 1,162 physical pages, SHA-256:

`544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297`

Nallino, C. A. (Ed. & Trans.). (1903). *Al-Battānī sive Albatenii opus astronomicum: Pars prima. Versio capitum cum animadversionibus*. Ulrich Hoepli.

Text-line anchors identify page, manually delimited region and ordinal line. They do **not** claim pixel-exact line rectangles. Table cell rectangles are regular-grid region estimates. Native crop rectangles and their pixel bounds are exact and replayable. Preserve the distinction between these locator types.

## Verification

Both PDFs have byte-identical outputs from two clean, two-pass XeLaTeX builds. Final logs have no recorded missing-character, overfull-box or font warnings. All reader pages were inspected in layout sheets, with detailed checks of the first and last pages, both tables, both diagrams and the three inserted uncertain objects. Both critical-note pages were inspected in full.

`receipts/read_only_audit.json` records 39 passing technical checks: source identity, exact bounded coverage, unique anchors, control-character checks, table-export consistency, native crop replay, embedded image pixels, final builds and unchanged production inputs during the audit. This separate checking program and the assistant’s visual recheck are **not** presented as an independent human or separate-model review, or as proof that every philological reading is error-free. Human certification is not a progression gate. S02 remains partial because the remaining 79 pages are not yet transcribed.

The prior continuation export contained no recoverable editable S02 transcription and recorded a source-excerpt rendering failure. Its extraction was not promoted to an authority. This batch supplies newly source-read text and a replacement excerpt that passed every page comparison; the previous archive remains unchanged.

## Rebuild

Requires Python 3, XeLaTeX, Linux Libertine O, Amiri and FreeSerif installed locally. Font files are not bundled. From the package directory run:

```sh
python scripts/build_edition.py
python scripts/build_critical.py
python scripts/build_clean.py
```

These commands regenerate TeX from the current JSON/ledgers and produce two clean builds, placing the reader and apparatus in `pdf/`. Do not rerun the archived drafting scripts: they record working states that predate later repairs.

For the full source/crop replay, place the byte-exact controlling master beside the package directory and run `python scripts/audit_readonly.py`. The original master is not duplicated in this archive. The smaller, validated 30-page evidence excerpt is included for direct reading.

`MANIFEST_SHA256.tsv` is self-excluding. `scripts/verify_manifest.py` checks every listed file without changing it. The archive includes final outputs, the current production data, source evidence, provenance, proof images and receipts; no intermediate build directories or font binaries are included.
