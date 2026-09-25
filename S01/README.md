# al-Battānī / Nallino — S01 v003

**Historical Nallino layer: revised transcription candidate. S01 is not yet closed.**

This package continues the first session only. It preserves Nallino’s Part I frontispiece, half-title, title, imprint, dedication, preface, bibliography, and addenda/corrigenda. No new target-language translation is included. Arabic, Greek, Syriac, Italian, and other quotations occurring within Nallino’s historical apparatus remain intrinsic quotations, not newly generated parallel editions. The Arabic authorial Zīj canon has not been changed.

## Open these files

`pdf/S01_NALLINO_SOURCE_v003.pdf` is the 80-page historical reader: one explicitly modern production notice, the preserved frontispiece, and 78 text-bearing historical source pages. `pdf/S01_CRITICAL_NOTES_v003.pdf` is a separate four-page apparatus explaining readings, image substitutions, and source limitations. Nallino’s own addenda are part of the historical reader; the modern critical notes do not replace them.

The editable reader is `tex/S01_NALLINO_SOURCE_v003.tex`. Its structured source is the 79 page records under `transcription/pages/`, including the owned blank at PDF15. `transcription/S01_NALLINO_SOURCE_v003.txt` provides the same line-anchored text with explicit markup. Image fallbacks use stable `<glyph>...</glyph>` identifiers: these are intentional references to exact source assets, not missing-file placeholders. Their paths and source rectangles are in `ledgers/figure_provenance.json` and `.tsv`.

## Scope and source identity

S01 owns physical master PDF2, PDF10, and PDF12–89, a total of 80 units. Every physical page PDF1–89 has a disposition. The text-bearing units are PDF10, PDF12–14, and PDF16–89; PDF15 is an owned blank, and PDF2 is the astronomical frontispiece. Provider service matter, library ownership marks, and binding/blank matter are not transcribed into the historical reader.

The controlling source is `30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf`: 1,162 physical pages, 80,946,704 bytes, SHA-256 `544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297`. The bundle contains its S01 evidence excerpt, `source/SRC01_PDF0001-0089_EVIDENCE.pdf`. That excerpt preserves source evidence, including extrinsic marks; it is not the cleaned reader. The Files retrieval service has reported 1,161 pages for the full master, but the physical PDF and controlling manifest report 1,162. Anchors follow the physical PDF without shifting page numbers.

All historical content here is credited as `NALLINO_APPARATUS`, not presented as al-Battānī’s authorial prose. See `controls/01_PROJECT_CONTRACT.md` and the S01 prompt for the layer and scope rules.

## What changed from v002

The recovered v002 ZIP was intact: all 535 manifest-listed files matched their recorded hashes. Its archive SHA-256 is `46152dbd96c89b587083a32472e3d05d2b6833a748489c462b140983c52adf08`. The interrupted continuation also left 157 proof-image files, totaling 49,226,935 bytes. Those were recovered byte-exactly, but no revised text or accepted-correction ledger accompanied them. They are preserved as evidence under `history/interrupted_reread/`; their existence is not itself proof that a correction was accepted.

The v003 reread has **85 recorded decisions affecting 79 distinct source lines on 50 source pages**: 71 text repairs and 14 new exact-image substitutions. Each decision records the predecessor reading, successor reading, affected anchor, evidence, confidence, and reason. The complete sequence is in `ledgers/v003_changes.json` and `.tsv`. The technical checker replays it from the immutable v002 text and tests that the resulting line map exactly equals v003. Earlier v002 decisions remain separately preserved; `transcription_repairs.json` is the cumulative 113-decision register.

Examples of text repairs include restoring a printed digraph instead of a dotted character, repairing dropped words, distinguishing bibliographical numerals, and preserving historical spelling even where it appears erroneous. These are repairs to the digital transcription, not silent emendations of Nallino’s historical text. Image substitutions preserve uncertain numerals, unusual character clusters, the distinct printed forms in correction lemmas, and two Arabic verse lines. No source damage has been conjecturally completed.

The source-line identifiers remain unchanged at **3,996 anchors**. The **47 mathematical objects** remain as witnessed notation, without mathematical emendation or recomputation. The **11-entry transliteration key** remains both a source-faithful printed list and a machine-readable register. The **86 historical addenda/corrigenda entries** are linked to their targets and marked `REGISTERED_NOT_APPLIED`; the earlier diplomatic text has not been rewritten according to them.

## Reading dispositions and images

The separate apparatus has 14 entries: three readings were confirmed and retained; ten have exact-image dispositions while character interpretation remains unresolved; one records the frontispiece’s already-truncated source edges. An image disposition preserves visible evidence. It is not a claim that every damaged character has been deciphered.

The visual-object ledger contains 24 records. Of these, 22 objects are included in the reader: four figures/ornaments and 18 glyph or text-region images. Two older crops remain evidence-only after earlier encoding resolution. Fourteen image objects are new in v003. Their raw and presentation PNGs are byte-identical integer crops from the authoritative native image. The frontispiece retains an untouched original JPX and decoded evidence image, as well as its conservative presentation crop. No inpainting, generative restoration, resampling of source crops, altered geometry, added labels, or strengthened strokes has been used.

For all images, consult `figure_provenance.json` for raw/presentation paths, native pixel rectangles, PDF coordinates, operations, dimensions, and hashes. For text-line rectangles, consult `line_alignment.json` with its explicit qualification: those locator coordinates were inherited from the v002 similarity-based locator and are **not independently verified word-level coordinates**. Current line text is synchronized to v003; exact image rectangles are recorded separately.

## Builds and checks

The reader and critical apparatus each passed two clean, two-pass XeLaTeX builds with byte-identical outputs. Both pairs also have identical all-page 36-dpi raster hashes. Their final logs report zero missing characters, overfull boxes, or font warnings; the reader also reports zero source-line width overflows. Receipts and logs are under `receipts/`.

All 80 reader pages were inspected in contact sheets for layout. Detailed final reader inspections covered pages 1, 2, 28, 31, 47, 48, 61, 70, 71, 73, 75, 77, and 80; all four critical-apparatus pages were inspected in detail. Other generated detailed renders are not falsely marked as individually inspected. The selected source reread covered 562 general proof candidates and 164 targeted candidates in 92 recovered contact sheets, with further native crops and formula samples. Those candidate sets can overlap; these are not unique-line counts or a new full line-by-line cold audit.

`receipts/technical_audit_v003.json` reports the standalone read-only program’s actual results, including change-chain replay, source crop pixels, embedded image pixels, build identities, anchors, and evidence-file hashes. The program was written by the producing assistant. It is **not an independent philological auditor**. A technically clean build or archive does not establish the correctness of every historical reading.

## Exact completion status

S01 remains a **source-revised candidate with the independent cold source/reading audit outstanding**. No independent auditor’s sign-off is claimed. No human certification gate has been introduced. The project’s required separate cold replay remains a distinct unfinished step; any resulting repair must become a successor version rather than an unrecorded patch to this candidate.

The last fully transcribed source unit is `AB01-PDF0089`, qualified by the image and uncertainty dispositions. `last_fully_verified_source_unit` remains null because full verification includes the independent audit. No S01 source page remains wholly untouched. Physical PDF90 is the beginning of S02, not work completed here. S02–S16 have not been started in this continuation.

The current Nallino JSON checkpoint is `AB01-NALLINO-S01-v003-CANDIDATE`, SHA-256 `8dd145df64a5cb9b64c56f914779b53470671798a01de69ae809db2f51bdeb4f`. This digest covers sorted page basenames, a NUL byte after each basename, and each exact page-JSON payload. It is not the PDF or ZIP hash. The canonical Arabic checkpoint is null because S01 does not own an Arabic authorial Zīj unit.

## Rebuilding and auditing

Use Python with PyMuPDF and Pillow, and a XeLaTeX installation providing the packages and system fonts named in `receipts/deterministic_builds.json`. Fonts are dependencies, not distributed files. The known build uses Linux Libertine O, FreeSerif, Amiri, and Noto Sans Syriac. The delivered PDFs embed the required font subsets.

From the unpacked package root:

```sh
python scripts/rebuild.py
python scripts/audit_v003_readonly.py > /path/outside/package/technical-audit-replay.json
```

The rebuild generates the reader and separate apparatus from the committed JSON layer, using a fixed source epoch. It does not OCR or infer text. The audit writes JSON to standard output only. With the full master next to the package, it rechecks that master’s identity; without it, it uses the bundled 89-page excerpt for native-pixel crop replay and explicitly reports that the external master’s hash was not retested.

Do not run historical first-pass mutation scripts in `history/v002/scripts/` as current production commands. The v003 mutation helpers also describe one-time editing operations, not steps needed to rebuild an already committed edition. The current build entry point is `scripts/rebuild.py`.

`MANIFEST_SHA256.tsv` lists every packaged file except itself. The ZIP validation receipt and the ZIP’s own SHA-256 are supplied beside the archive because an archive cannot contain its own final digest. Preservation history is explicitly historical; its older PASS statements and open-reading counts are not current v003 receipts.

## Bibliographical source

Nallino, C. A. (Ed. & Trans.). (1903). *Al-Battānī sive Albatenii opus astronomicum: Pars prima, versio capitum cum animadversionibus*. Ulrichus Hoepli. (Pubblicazioni del Reale Osservatorio di Brera in Milano, N. XL, Parte I.)

This citation identifies the historical Part I edition being transcribed. The supplied Google/Princeton scan is the source witness, not the author. The project’s access and provenance instructions are preserved in `controls/`.
