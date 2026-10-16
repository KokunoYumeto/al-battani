# S16 cold audit — 2026-10-16

Commit audited: `21ea14472489afa222e49c51d64344946e5c73f4`.

Auditor: a separate read-only program (S16/audit/cold_audit.py), written and run by the same AI (Claude) that produced the edition, in the same session; not an independent agent, and not a person.

| Check | Result | Detail |
|---|---|---|
| source SRC01 identity | PASS | nallino_pars123.pdf: sha256 544c16b6355c9b74…, 1162 pages; gate 544c16b6355c9b74…, 1162 pages |
| source SRC02 identity | PASS | pars3_uoft.pdf: sha256 f60d9c2d3a0faa6d…, 292 pages; gate f60d9c2d3a0faa6d…, 292 pages |
| source SRC06 identity | PASS | kennedy.pdf: sha256 3bc5b525639261cc…, 136 pages; gate 3bc5b525639261cc…, 136 pages |
| source SRC07 (PAL files in S14) | PASS | 123 files against S14's manifest; 0 differ |
| canonical receipt replay | PASS | 3,923 files re-hashed; 0 differ |
| table editions: running heads agree with the declared pages | PASS | 251 heads agree, 3 pages have no number in the head (half-titles, figures, first pages), 0 disagree |
| AB01 coverage replay: every master page presented or disposed | PASS | 1137 pages presented by the edition PDFs, 27 disposed, 2 both (blank pages printed in an edition and recorded as blank); gaps [], out of range [] |
| AB01 coverage replay agrees with S16/integration/coverage_ab01.tsv | PASS | 1162 pages compared; 0 disagree; 4 pages disposed as blank are printed blank in their edition: [241, 639, 747, 767] |
| pages presented twice are the recorded ones | PASS | 13 pages presented by two PDFs: [668, 669, 746, 748, 749, 750, 751, 752, 753, 754, 755, 756, 918]; recorded [668, 669, 746, 748, 749, 750, 751, 752, 753, 754, 755, 756, 918] |
| AB02 coverage replay (S15 bookmarks) | PASS | 32 pages bookmarked: PDF 5 and the even PDF pages 6-66 (as the Arabic edition's pages) |
| AB03 coverage replay (S14 bookmarks) | PASS | 122 of 122 page sides 20r-80v bookmarked |
| assembled volumes rebuild byte-identical | PASS | 2 of 2 volumes identical on a rebuild in a temporary folder |
| every bound page identical to its session page | PASS | 1,160 pages compared as pixels; 0 differ |
| session builds replayed byte-identical, session checks pass | PASS | 32 folders replayed in temporary copies; all identical |
| visual samples rendered | PASS | 20 contact sheets (master scan / edition) in S16/audit/samples; inspection recorded in audit_inspection.md |
| production unchanged by the audit | PASS | 3,962 production files hashed before and after; 0 changed |

Failures: 0.

The audit writes only into S16/audit and changes no production file; a failure is reported here and not repaired.
