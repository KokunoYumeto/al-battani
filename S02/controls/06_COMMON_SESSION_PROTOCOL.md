# Common session protocol

Every production prompt inherits this file and `08_UNIVERSAL_GALOIS_DERIVED_PRODUCTION_STANDARD.txt`.

## Before work

- Read the maps and verify the attached source byte/hash/page identity.
- Name the canonical Arabic checkpoint/hash being used.
- Inventory every owned source unit. If a listed unit is absent or unreadable, record the exact failure and continue with every unaffected unit; do not invent content.
- Establish `last_fully_transcribed_source_unit`, `last_fully_verified_source_unit`, and `first_untouched_source_unit`.

## Production

- Maintain stable anchors: `AB01-PDF####`, `AB02-PDF####`, or `AB03-F###r/v` plus line/table/region IDs.
- Preserve formulas, numbers, sexagesimal notation, table coordinates, diagrams, marginalia, and correction marks exactly before interpretation.
- Tag authorship/edition roles from `01_PROJECT_CONTRACT.md`.
- Table workflow: return a visual-faithful LaTeX table and a machine-readable CSV/TSV. Every row/column/header/spanner must trace to a source region. Never normalize a number silently.
- Figure workflow: editable reconstruction only if complete; otherwise return raw crop plus conservative presentation derivative, SHA-256, source rectangle, and operations.
- Do not include provider/digitizer/library matter in the scholarly body. Record it in page disposition/provenance.

## Required return

1. Arabic diplomatic/source TeX for owned AB content.
2. Separately credited historical Latin/Nallino TeX where the session owns that layer.
3. One separate faithful monolingual target-language TeX per requested language; never bilingual.
4. Restrained critical apparatus with stable note IDs and categories (`reading`, `formula`, `table`, `attribution`, `historical`, `modern clarification`).
5. Page/source disposition ledger.
6. Formula/table/figure provenance ledgers.
7. Unresolved-reading ledger with bounded alternatives and confidence.
8. Proposed canonical-correction ledger; no silent patches.
9. Canonical synchronization receipt naming the source checkpoint.
10. Deterministic file manifest and build/render receipts.
11. Cumulative checkpoint fields.

## Verification

Build twice. Render and inspect first, last, dense-table, formula, figure, and damaged/ambiguous samples. A separate cold auditor must replay source coverage, hashes, builds, and visual samples without editing the production outputs. Human review is welcome later but never a completion gate.
