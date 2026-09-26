# Packet validation status — PASS

Current source-gate facts:

- Complete Nallino master: 1,162 pages, 80,946,704 bytes, SHA-256 `544C16B6355C9B74E281ADED657D657224BFF738366D5260E1A610D31B0D6297`.
- Part III comparator: 292 pages, 25,151,980 bytes, SHA-256 `F60D9C2D3A0FAA6D7841CEC0197A2B3F4FAABC5BBB32DFDC19DB9ECC3CC3DD67`.
- Astrological-history publication: 136 pages, 9,743,194 bytes, SHA-256 `3BC5B525639261CCCF1A6E78176F66C5AC2C4299DD2D0A051072CDAB149B7BEF`.
- PAL subtree: exact commit archive with 123 XML files and no unsafe paths, SHA-256 `FDD456FFB64C20ED2DB46A16862E1180379D10D619F5F46AF7B71871972049F2`.
- Representative and transition pages from all PDFs were rendered and visually inspected during source gating, including the substantive master PDF2 frontispiece and all three part boundaries.

Cold source replay passed before promotion:

- Flat upload tree: 38 files including the self-excluding manifest; zero empty files; zero files at or above 500,000,000 bytes; fewer than 40 files.
- Master topology: 32 rows cover PDF1–1162 exactly once; zero gaps and zero overlaps.
- Session map: 16 unique sessions and 16 matching paste-ready prompt files.
- Prior T01 archive: 15/15 source files byte/hash-equal to archive members.
- Round 83 archive: 40/40 source files byte/hash-equal to archive members.
- Part III page-map archive: 18/18 source files byte/hash-equal to archive members.
- PAL archive: 129 entries, 123 XML files, zero unsafe paths, zero UTF-8 errors, zero XML parse errors.
- Evidence archive: 8/8 files fully readable, zero unsafe paths.
- All three production PDFs independently report 1,162 / 292 / 136 pages through pypdf and mutool; every page content stream was read with zero failures.
- Visual QA passed for source beginnings, ends, all three part transitions, dense tables, Arabic main text, Arabic title/corrigenda, the UB edition/translation/diagram/table samples, and BEA bibliography pages.

Canonical/Desktop equality and the final global state receipt are recorded in the durable seal receipt after promotion. Human review is not a gate.
