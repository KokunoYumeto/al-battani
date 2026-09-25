# Project contract

## Objective

Create a source-faithful, author-aware, independently auditable corpus from the attached witnesses. The Project is reader-complete at Tier A when all 57 chapters and all tables of the extant *Zīj* have complete dispositions and separate monolingual editions. Tier B is complete only to the exact payload/access states in the maps; never infer missing manuscript pixels.

## Authorship and edition layers

Use stable role tags:

- `AB_TEXT`: al-Battānī’s Arabic prose.
- `AB_TABLE`: al-Battānī’s tabular or diagrammatic content.
- `AB_SMALL_WORK`: securely attributed smaller work.
- `NALLINO_TRANSLATION`: Nallino’s Latin translation.
- `NALLINO_APPARATUS`: Nallino’s prefaces, notes, corrections, indices, and editorial matter.
- `MODERN_EDITORIAL`: later edition, translation, recomputation, or commentary.
- `COPY_PROVENANCE`: holding-copy marks, presentation statements, bindings, labels.
- `SCAN_EXTRINSIC`: digitizer/provider UI, service cards, watermarks, barcodes.
- `UNCERTAIN`: unresolved boundary, reading, or attribution.

Never present Nallino or modern editorial material as al-Battānī’s authorship. Never strip their credit when preserving those layers.

## Edition architecture

Return separate artifacts:

1. Arabic diplomatic/source edition keyed to source anchors.
2. Historical Latin/Nallino edition only for the Nallino layer assigned in S01–S09.
3. One faithful monolingual target-language edition per language.
4. One restrained critical apparatus keyed to stable IDs, not colored chat boxes.
5. Machine-readable page/table/figure/evidence/unresolved ledgers.

No bilingual artifact is permitted. Translation begins from a named canonical Arabic checkpoint and rechecks the authoritative pixels. Translation findings are correction proposals, never silent patches.

## Source priority

1. Exact source pixels or exact committed transcription for the owned unit.
2. Alternate high-resolution witness for damaged/ambiguous regions.
3. Edition apparatus and published translations as labelled comparators.
4. OCR, prior working TeX, and prior outputs as untrusted recovery evidence.

## Fidelity and presentation

Preserve mathematical content before elegance. Editable LaTeX/TikZ/SVG is preferred only when every visible relation is reproduced. Otherwise preserve a raw crop and make a conservative crop/deskew/grayscale/levels derivative without inpainting, label changes, geometry changes, or conjectural completion. Increase contrast only when faint source content remains demonstrably intact.

## Completion

A session closes only after every owned unit is transcribed or explicitly disposed; outputs build; representative and boundary pages are rendered and inspected; hashes and evidence are returned; and a separate cold auditor replays without patching. Human certification may arrive later but is never required for release.
