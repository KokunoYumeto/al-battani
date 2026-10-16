# S16 — Integration, assembly and cold audit

S16 joins the work of S01–S15 into one corpus of al-Battānī's works (AB01–AB06), assembles the monolingual volumes of the *Zīj* in Nallino's edition, audits the result read-only, and closes with receipts of coverage, status and gaps. S16 transcribes no source unit.

**Done:** the integration of S01–S15; the two monolingual volumes of AB01, Nallino's Latin edition (874 pages) and the Arabic edition (290 pages), each built twice and byte-identical; a cold audit, a read-only program run by the same AI (16 checks, 0 failures); the closing receipts. A comparison made during the integration corrected three labels of the astrological figure (Part II p. 299) in S13 and S07 (below).

## Read

- [AB01_Latin_Nallino_edition.pdf](assembly/AB01_Latin_Nallino_edition.pdf): Nallino's Parts I and II: the front matter of Part I, the translation of the 57 chapters with his notes and commentary, the front matter of Part II, the tables in his Latin version, his notes on the tables, the spurious tables, the astrological figure, the glossary and the indexes. 874 pages.
- [AB01_Arabic_edition.pdf](assembly/AB01_Arabic_edition.pdf): Part III, the Arabic text of the 57 chapters and the tables of the codex, with Nallino's title pages, corrigenda and notice. 290 pages.

Each volume opens with a cover that names the commit of its sources and a contents page that gives every part's pages in Nallino and in the volume. The bookmarks give every bound part and, under it, the part's own page bookmarks: 663 of the Latin volume's 697 bookmarks and 231 of the Arabic volume's 244 name a master-scan anchor. The volumes bind the session PDFs unchanged. There is no bilingual reader. The Arabic edition of AB02 (S15) and the commentary AB03 (S14) are separate editions under their own licences, not bound here.

## Integration (`integration/`)

`python coverage_ab01.py`, `python compare_duplicates.py`, then `python integrate.py`; 15 checks, all pass (`integration_receipt.json`).

| Output | Content |
|---|---|
| `coverage_ab01.tsv` | the 1,162 master pages of Nallino's three volumes, one disposition each: 1,131 edited, 31 disposed, no gap, no overlap; the owning session and artifact |
| `coverage_ab02.tsv`, `coverage_ab03.tsv` | AB02: 136 PDF pages of *Suhayl* 9, 32 transcribed, 104 disposed (the article's own text, not reproduced); AB03: 122 page sides, 121 transcribed, 1 blank |
| `duplicates_compared.tsv` | the 12 master pages transcribed by two sessions (the tables and the figure inside Nallino's notes), compared item by item: 3,051 items, every item of the canonical transcription found in S07's |
| `repairs.tsv`, `evidence/` | the readings corrected in production after that comparison, with the scan evidence |
| `anchors_summary.tsv` | 42,388 stable anchors in 16 ledgers, unique across the corpus, each on a page its session edits |
| `roles_map.tsv`, `roles_by_kind.tsv` | every role tag and line kind of the records mapped to the roles of the project contract |
| `works.tsv` | AB01–AB06: payload, attribution, status; AB04 held as source-unacquired and attribution-questioned; AB05 and AB06 mapped by their anchors to chapters 54 and 55 of the *Zīj*, not duplicated |
| `ledgers_index.tsv`, `corrections_index.tsv`, `objects_index.tsv` | the ledgers of every session by kind; the correction ledgers (26, none open); the formulas, figures and tables, and the 13 unresolved readings kept open in S01 and S02 |
| `canonical_versions.tsv` | the canonical artifact and status of every source range |
| `canonical_receipt.tsv`, `session_digests.tsv` | every tracked file of S01–S15 (3,923) with its SHA-256; one digest per session |

### The figure on Part II p. 299

The comparison of the pages transcribed twice found three labels of the terms in the astrological figure that S13 and S07 read differently. Read on the scan, each label beside the other labels of its planet: Gemini, term 2, is printed «Inpiter» and Cancer, term 2, «Iupitor», where S13 had «Iupiter»; Virgo, term 2, is printed «Verus», where S07's redrawn figure had «Venus». The readings were corrected in the sessions that had them wrong, the editions rebuilt (S07's PDF changes on the page of the figure only), and the misprints kept as printed. `repairs.tsv` records each correction with its evidence; `evidence/make_p299_evidence.py` renders the scan sheets.

## Assembly (`assembly/`)

`python -P -E assemble.py` builds both volumes; `--check` builds them again in a temporary folder and compares the bytes. The build is deterministic (fixed date and metadata): two builds and the check give the same files. `assembly_receipt.tsv` lists every bound part with its first page and length; `volumes.tsv` the pages, bookmarks, SHA-256 and source commit of each volume. `python inspect_seams.py` renders every boundary between two bound parts, the covers, the contents and the last pages (`inspection/`); all were looked at.

## Cold audit (`audit/`)

`python cold_audit.py` replays what the production claims, by routes that do not use the integration code, and writes only into `audit/`:

- the source witnesses against the packet's source gate; PAL's files against S14's manifest;
- every file of the canonical receipt hashed again;
- the coverage of AB01 replayed from what the edition PDFs present (bookmarks, running heads of the table editions) and from the disposition ledgers, page by page against `coverage_ab01.tsv`; AB02 and AB03 from their bookmarks;
- the volumes rebuilt in a temporary folder and compared byte for byte, and every bound page compared, as rendered pixels, with the page of the session PDF it binds;
- the builders of 32 session folders run again in temporary copies, their output compared byte for byte with the committed files, and the sessions' own checks run there;
- contact sheets of master pages beside edition pages (first and last pages, dense formula and table pages, figures), inspected and recorded in `audit_inspection.md`;
- every production file hashed before and after: the audit changed none.

Result on commit 21ea144: 16 checks, 0 failures (`audit_report.md`, `audit_report.json`, `audit_run.log`). The auditor is a separate read-only program, but it was written and run by the same AI (Claude) that produced the edition, in the same session; it is not an independent agent, and no person has reviewed the corpus. `replay_s01_audit.py` also replays S01's own technical audit on S01's complete package: 47 checks, all pass (`s01_technical_audit_replay.json`).

## Receipts

- [receipts/coverage.tsv](receipts/coverage.tsv): every work, its source units and their dispositions.
- [receipts/status.tsv](receipts/status.tsv): the status of every work, every source range and its canonical artifact, both volumes, and every check of the integration and the audit.
- [receipts/gaps.tsv](receipts/gaps.tsv): every known gap with its exact boundary: AB04 unacquired; the codex of the *Zīj* not collated; Parts I and II read in one scan copy; the unresolved readings of S01 and S02 and S01's outstanding philological audit; the manuscripts of AB02 and AB03 not consulted; no target-language edition; the audit not independent of the producer.
- [checkpoint.json](checkpoint.json): the cumulative checkpoint, with the canonical checkpoint (commit and session digests) from which a translation starts.
- [MANIFEST_SHA256.tsv](MANIFEST_SHA256.tsv): every file of S16 with its size and SHA-256.

`python close_s16.py` writes the receipts, the checkpoint and the manifest from the outputs above.

Human review is welcome and is not a completion gate.

## Credits

- al-Battānī: the works. C. A. Nallino: the edition of the *Zīj* (Milan, 1899–1907), in the public domain.
- Integration, assembly, audit and receipts: AI-integrated work (Claude) in this repository, 2026, released under CC0 1.0.
