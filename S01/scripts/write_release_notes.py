"""Write descriptive release notes from the actual candidate and audit receipts."""
from pathlib import Path
import collections,csv,datetime,hashlib,json,re
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def pair(stem,rows,columns=None):
 (R/'ledgers'/f'{stem}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 keys=columns or sorted(set().union(*(x.keys() for x in rows)))
 with (R/'ledgers'/f'{stem}.tsv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,delimiter='\t');w.writeheader()
  for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
pages=[json.loads(p.read_text()) for p in sorted((R/'transcription/pages').glob('*.json'))]
lines=[l for p in pages for s in p['sections'] for l in s['lines']]
u=load('ledgers/unresolved_readings.json'); repairs=load('ledgers/transcription_repairs.json'); sync=load('receipts/canonical_synchronization.json');build=load('receipts/deterministic_builds.json');audit=load('receipts/technical_audit.json')
assert len(lines)==3996 and len(u)==12 and audit['status']=='PASS_TECHNICAL_SCOPE_ONLY'
# Source-layer issues are not silently promoted to conjectural textual corrections.
findings=[]
for x in u:
 findings.append({'apparatus_id':x['note_id'],'issue_class':x['category'],'source_anchor':x['source_anchor'],'line_id':x['line_id'],'source_rect_pt':x['source_rect_pt'],'coordinate_granularity':x['coordinate_granularity'],'diplomatic_reading':x['displayed_reading'],'faithful_translation':'Not requested for this historical Nallino source-layer session.','proposed_critical_reading':'None adopted; see bounded alternatives.','bounded_alternatives':x['bounded_alternatives'],'required_hypotheses':'No reconstruction or modern correction assumed.','witness_evidence':x['evidence'],'reason':x['reason'],'confidence':x['confidence'],'propagation_impact':x['propagation'],'prior_notice_result':'Recorded during this source-replay session; no exhaustive claim about previous scholarship.','citation':f"Nallino (1903), SRC01 physical {x['source_anchor']}; pinned source SHA-256 in source_evidence.json.",'status':'DOCUMENTED_SOURCE_LOSS' if x['category']=='source_loss' else 'OPEN_READING'})
pair('critical_findings',findings)
# Complete textual change comparison against the preserved first-pass checkpoint.
diff=[]
for p in pages:
 old=load('history/first_pass_pages/'+p['anchor']+'.json')
 a={l['id']:l['text'] for s in old['sections'] for l in s['lines']};b={l['id']:l['text'] for s in p['sections'] for l in s['lines']}
 for k in sorted(a.keys()|b.keys()):
  if a.get(k)!=b.get(k):diff.append({'line_id':k,'before_first_pass':a.get(k),'after_v002':b.get(k),'repair_ids':[x['repair_id'] for x in repairs if x['line_id']==k]})
assert len(diff)==25 and all(x['repair_ids'] for x in diff)
pair('first_pass_text_changes',diff)
changed_receipt={'first_pass_snapshot':'history/first_pass_pages','changed_source_lines':len(diff),'tracked_repair_steps':len(repairs),'all_text_changes_have_repair_ids':True,'new_reading_layer':sync['canonical_Nallino_checkpoint'],'new_reading_sha256':sync['canonical_Nallino_sha256'],'old_unverified_checkpoint':'history/v001_cumulative_checkpoint.json','old_checkpoint_sha256':sha('history/v001_cumulative_checkpoint.json'),'reason':'A new source-replayed transcription candidate replaces the unverified extraction as the current S01 working layer; earlier evidence is retained, not overwritten.'}
(R/'receipts/checkpoint_lineage.json').write_text(json.dumps(changed_receipt,indent=2)+'\n')
# These lists record images actually inspected in this response, not merely rendered.
vis={'reader_pdf_sha256':sha('pdf/S01_NALLINO_SOURCE_v002.pdf'),'source_review':'Every physical source unit PDF1-89 received first-pass visual disposition; all text-bearing owned pages received line-by-line transcription from source renders.','source_text_pages':[10,12,13,14]+list(range(16,90)),'source_frontispiece':2,'owned_blank':15,'final_contact_sheets_inspected':[f'qa/final/contact_{a:02d}-{b:02d}.jpg' for a,b in [(1,12),(13,24),(25,36),(37,48),(49,60),(61,72),(73,80)]],'contact_scope':'All 80 reader pages; layout, boundaries and gross omission checks, not word-level certification from thumbnails.','final_detailed_reader_pages_inspected':[1,2,8,47,48,61,73,80],'detailed_scope':'Editor attribution and caveat, frontispiece, footnotes and foreign-script rendering, mathematical pages, orthographic examples, corrigendum glyph crops and terminal page.','other_source_detail_evidence':'qa/ contains source-page renders and targeted crops used in the first-pass and proof-repair stages. Some older edition renders predate the modern notice and must not be used as the final page map.','poppler_proof_inspected':'qa/final/poppler_reader_080.png','renderers':['MuPDF via PyMuPDF','Poppler pdftoppm'],'visual_result':'No clipped or overlapping text or missing-glyph boxes identified in the inspected final samples; seven contact sheets inspected. Eleven reading entries remain unresolved; one source-loss limitation is documented.','reviewer_independence':'Producing assistant; not independent cold textual audit.','critical_apparatus_reader_pages_inspected':[1,2,3],'critical_apparatus_pdf_sha256':sha('pdf/S01_CRITICAL_NOTES_v002.pdf'),'not_a_completion_claim':True}
(R/'receipts/visual_qa.json').write_text(json.dumps(vis,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
cp={'session_id':'S01','version':'v002','checkpoint_created_utc':now,'status':'FULL_RANGE_SOURCE_REPLAYED_CANDIDATE_TECHNICAL_PASS_OPEN_READINGS','session_complete':False,'scope_master_pages':[1,89],'owned_source_units':[2,10]+list(range(12,90)),'owned_unit_count':80,'physical_disposition_count':89,'text_bearing_owned_pages':78,'owned_blank_pages':[15],'frontispiece_pages':[2],'reader_pages':80,'reader_modern_editorial_notice_pages':1,'reader_historical_pages':79,'source_line_anchors':3996,'editable_math_objects':47,'transliteration_key_entries':11,'printed_corrigenda_entries':86,'tracked_proof_repair_steps':28,'first_pass_lines_changed':25,'flagged_source_entries':12,'open_reading_entries':11,'documented_source_loss_entries':1,'inline_glyph_image_fallbacks':4,'critical_apparatus_pages':3,'critical_apparatus_pdf_sha256':sha('pdf/S01_CRITICAL_NOTES_v002.pdf'),'last_fully_transcribed_source_unit':'AB01-PDF0089','transcription_status_qualification':'Complete first-pass source-layer coverage, with bounded unresolved readings and explicit image dispositions; not a fully verified edition.','last_source_replayed_source_unit':'AB01-PDF0089','last_fully_verified_source_unit':None,'verification_field_definition':'Full verification includes the independent cold source/reading audit, not performed here.','first_untouched_source_unit':None,'first_untouched_scope':'Within S01 only. No S01 page remains wholly untouched; this does not describe the rest of the corpus.','first_open_reading_source_unit':'AB01-PDF0018','documented_source_loss_source_unit':'AB01-PDF0002','first_source_unit_outside_S01':'AB01-PDF0090','later_sessions_executed':False,'canonical_Nallino_checkpoint':sync['canonical_Nallino_checkpoint'],'canonical_Nallino_sha256':sync['canonical_Nallino_sha256'],'canonical_Arabic_checkpoint':None,'canonical_Arabic_hash':None,'Arabic_source_disposition':'Not owned in this session; Arabic quotations remain Nallino apparatus.','source_identity_pass':True,'reader_pdf_sha256':sha('pdf/S01_NALLINO_SOURCE_v002.pdf'),'two_clean_builds_byte_identical':build['byte_identical'],'technical_audit_status':audit['status'],'technical_audit_checks':len(audit['checks']),'independent_cold_textual_audit':'NOT_PERFORMED','human_review_required_as_gate':False,'remaining_actions':['Adjudicate or explicitly accept the bounded open readings in critical_findings.json, preserving source evidence.','Run an independent cold source/reading audit without patching this candidate; corrections, if needed, create v003.','Rebuild and rerun technical and visual checks after any successor changes.'],'next_work_scope':'S01 only; no authorization to start S02 is asserted by this checkpoint.'}
(R/'receipts/cumulative_checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n')
# Numbered, source-anchored critical apparatus, separated from the historical reader.
notes=['# S01 v002 — Critical notes and reading limitations','',
'This apparatus belongs to the new digital production, not to Nallino’s historical prose. The reader retains Nallino’s wording; no proposed historical correction is silently substituted. Source references below are physical pages of SRC01, identified by SHA-256 `544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297`.','',
'## Status','',
'The full S01 range has a first-pass transcription or an explicit image/blank disposition. Eleven reading entries remain open. The frontispiece’s pre-existing truncation is a documented source limitation, not text that has been conjecturally supplied. Four inline glyph images avoid asserting unsupported Unicode readings.','']
for x in findings:
 notes += [f"## {x['apparatus_id']} — {x['source_anchor']}",'',f"**Class:** {x['issue_class']}. **Status:** {x['status']}.",'',f"**Reading retained:** {x['diplomatic_reading']}.",'',x['reason'],'',f"**Bounded alternatives:** {x['bounded_alternatives']}",'',f"**Anchor:** `{x['line_id']}`. **Evidence:** [{x['witness_evidence']}]({x['witness_evidence']}).",'',f"**Coordinates:** `{x['source_rect_pt']}` PDF points; {x['coordinate_granularity']}.",'',f"**Confidence:** {x['confidence']}. No critical emendation is adopted. This finding affects the Nallino source layer only; it does not patch the Arabic authorial canon.",'']
notes += ['## Recorded transcription repairs','',
'The 28 repair/encoding decisions in `ledgers/transcription_repairs.tsv` affect 25 distinct source lines relative to the preserved first-pass snapshot. They correct the digital transcription, not Nallino’s historical claims. The complete before/after line comparison is `ledgers/first_pass_text_changes.tsv`. Transient image fallbacks subsequently resolved are retained in the repair history.','',
'Examples include the printed reference `p. cccxlii` on PDF17, the accusative `Muslimum` on PDFs18–19, and the fraction `1/87` on PDF85. These readings were taken from source pixels, not modern historical or numerical expectations. The exact line identifiers, evidence and before/after strings are in the ledgers.','',
'## Historical corrigenda are not digital patches','',
'The 86 entries in `ledgers/printed_corrigenda_routing.tsv` transcribe Nallino’s own addenda/corrigenda on PDF79–89 and register their target pages. Their state is `REGISTERED_NOT_APPLIED`. References into later sessions are routes only: no later-session text has been transcribed or changed here.','',
'## Verification limits','',
'Two clean two-pass XeLaTeX builds are byte-identical. A separate read-only program passes 29 technical checks; the program was authored during the production session and is not an independent philologist. The producing assistant inspected the source and reader proofs. An independent cold source/reading audit has not been performed. No human-only certification requirement is introduced.','',
'## Source citation','',
'Nallino, C. A. (1903). [Front matter, preface, bibliography, and addenda]. In *Al-Battānī sive Albatenii opus astronomicum* (Pars prima: *Versio capitum cum animadversionibus*, pp. VII–LXXX). Ulrich Hoepli. Controlling digital witness: SRC01, physical PDF2, PDF10 and PDF12–89.','']
(R/'CRITICAL_NOTES.md').write_text('\n'.join(notes),encoding='utf-8')
readme=f'''# S01 v002 — Nallino Part I front matter and apparatus

**Current state: complete first-pass source coverage; technically checked candidate; S01 not finally closed.**

This release advances the first prompt only. It is a new, page-by-page transcription from the authoritative scans, not a relabelling of the earlier embedded-text extraction. No S02–S16 production was executed.

## Read the edition

The principal reader is [S01_NALLINO_SOURCE_v002.pdf](pdf/S01_NALLINO_SOURCE_v002.pdf). It contains 80 pages: one explicitly modern Latin editorial notice, followed by 79 historical pages (78 text-bearing source leaves and the astronomical frontispiece). The owned blank at physical PDF15 is recorded rather than typeset as a spurious text page.

Editable sources are [the complete TeX](tex/S01_NALLINO_SOURCE_v002.tex), [the page-anchored UTF-8 text](transcription/S01_NALLINO_SOURCE_v002.txt), and the structured records in `transcription/pages/`. The plain-text file retains raw LaTeX for mathematical expressions and named image references where exact glyph crops replace uncertain encodings. JSON preserves the formatting and language tags used to generate the reader.

[The separate three-page critical apparatus PDF](pdf/S01_CRITICAL_NOTES_v002.pdf), [its editable TeX](tex/S01_CRITICAL_NOTES_v002.tex), [expanded critical notes](CRITICAL_NOTES.md) and [the cumulative checkpoint](receipts/cumulative_checkpoint.json) state the unresolved issues and the precise continuation boundary. They are part of the delivery, not optional qualifications to a supposedly finished edition.

## Coverage and attribution

The session owns physical master PDF2, PDF10 and PDF12–89: 80 units. Every physical page PDF1–89 has a disposition. The text-bearing pages are PDF10, PDF12–14 and PDF16–89, totaling 78. PDF16–73 carry the preface (printed VII–LXIV), PDF74–78 the bibliography (LXV–LXIX), and PDF79–89 the addenda/corrigenda (LXX–LXXX).

All of these historical editorial materials are tagged `NALLINO_APPARATUS`, not al-Battānī’s authorial Arabic prose. Nallino’s intrinsic Arabic, Greek, Syriac and other quotations remain part of his apparatus. They are not a new parallel translation. The new first-page notice is tagged `MODERN_EDITORIAL`. No target translation language was requested for this S01 continuation, and no Arabic Zīj canonical checkpoint was used or altered.

The controlling file is `30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf`: 80,946,704 bytes, 1,162 physical PDF pages, SHA-256 `{load('ledgers/source_evidence.json')[0]['sha256']}`. The retrieval service’s 1,161-page label conflicts with the actual PDF structure and the packet manifest. All anchors here use the physical 1,162-page file, without shifting the page numbers.

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

Two clean build directories were used, with two XeLaTeX passes in each. Both outputs are byte-identical, and all 80 page rasters match between builds at 36 dpi. There are zero missing-character reports, overfull boxes, source-line width overflows or font warnings in either final log. Reader SHA-256: `{sha('pdf/S01_NALLINO_SOURCE_v002.pdf')}`.

The read-only [technical audit](receipts/technical_audit.json) passes {len(audit['checks'])} checks covering identities, page and line coverage, markup, native crop equality, formula/key/corrigendum linkage, canonical digests, deterministic builds, reader anchors and page bounds. It confirms that it did not patch production outputs. It does **not** certify the historical readings: a separate executable is not an independent philological reviewer.

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
'''
(R/'README.md').write_text(readme,encoding='utf-8')
(R/'STATUS.md').write_text(f'''# S01 v002 — execution status

Full first-pass transcription coverage of S01 has been achieved. The final reader is 80 pages, including one modern editorial notice. All 89 physical source pages have dispositions. The controlling master hash is verified.

Two clean two-pass builds are byte-identical. The {len(audit['checks'])}-test read-only technical audit passes. The final reader has no missing-character, overfull-box or font-warning reports.

Eleven reading entries remain open. One additional entry records pre-existing loss at the frontispiece edges. Four exact-source glyph crops remain in place of uncertain Unicode encodings. No independent cold textual audit has been performed. This is not a final session-completion receipt.

Last source-replayed / first-pass-transcribed unit: **AB01-PDF0089**. First wholly untouched S01 unit: **none**. Last independently fully verified unit: **none**. S02–S16 executed: **no**.

Next work remains S01: bounded reading adjudication and independent cold source/reading audit; any correction produces v003, followed by rebuild and repeated checks. No human-only certification is required.

See `receipts/cumulative_checkpoint.json`, `CRITICAL_NOTES.md` and `README.md` for the exact qualifications and evidence.
''',encoding='utf-8')
print('Release notes and candidate checkpoint written; 11 open readings + 1 documented source-loss entry.')
