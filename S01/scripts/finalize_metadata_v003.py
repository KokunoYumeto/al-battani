"""Write candidate metadata, not historical text. Run before the read-only audit."""
from pathlib import Path
import hashlib,json,collections,datetime,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
changes=read('ledgers/v003_changes.json'); notes=read('ledgers/critical_findings.json'); sync=read('receipts/canonical_synchronization.json')
fullpages=[1,2,28,31,47,48,61,70,71,73,75,77,80]
artifact_hashes={'reader':sha(R/'pdf/S01_NALLINO_SOURCE_v003.pdf'),'critical':sha(R/'pdf/S01_CRITICAL_NOTES_v003.pdf')}
vi=read('receipts/render_inventory_v003.json')
for x in vi:
 x['status']='DETAIL_VISUALLY_INSPECTED_BY_PRODUCING_ASSISTANT' if x['artifact']=='critical' or x['page'] in fullpages else 'RENDERED; CONTACT_SHEET_LAYOUT_INSPECTED_ONLY'
 x['qualification']='Not an independent source-reading audit.'
write('receipts/render_inventory_v003.json',vi)
contacts=[]
for p in sorted((R/'qa/v003/final').glob('contact_*.png')):contacts.append({'file':p.relative_to(R).as_posix(),'sha256':sha(p),'inspection':'All displayed reader pages visually inspected for layout; thumbnails do not establish word-level accuracy.'})
write('receipts/visual_review_v003.json',{'version':'v003','artifact_hashes':artifact_hashes,'reader_contact_layout_pages':list(range(1,81)),'reader_detail_pages':fullpages,'critical_detail_pages':[1,2,3,4],'contact_sheets':contacts,'new_native_glyph_contact':'qa/v003/native_glyphs_contact.png','new_native_glyphs_inspected':14,'issues':'No clipping, overlapping text, missing-character boxes, or misplaced image objects seen in the inspected final samples. This is a visual layout finding, not certification of all historical readings.','source_review_scope':'562 general proof candidates and 164 targeted proof candidates inspected in 92 recovered contact sheets, plus separately recorded native crops and formula samples. Candidate sets can overlap; these are not unique-line counts.','responsibility':'Producing assistant','independent_philological_audit':False})
write('receipts/build_process.json',{'status':'COMPLETED','receipt':'receipts/deterministic_builds.json','critical_receipt':'receipts/critical_notes_builds.json','qualification':'No continuing background build.'})
cp={
 'session_id':'S01','version':'v003','checkpoint_created_utc':now,
 'status':'SOURCE_REVISED_CANDIDATE; INDEPENDENT_COLD_SOURCE_AUDIT_OUTSTANDING',
 'session_complete':False,'scope_master_pages':[1,89],'owned_source_units':[2,10]+list(range(12,90)),
 'owned_unit_count':80,'physical_disposition_count':89,'text_bearing_owned_pages':78,'owned_blank_pages':[15],'frontispiece_pages':[2],
 'reader_pages':80,'reader_modern_editorial_notice_pages':1,'reader_historical_pages':79,'source_line_anchors':3996,
 'editable_math_objects':47,'transliteration_key_entries':11,'printed_corrigenda_entries':86,
 'new_tracked_decisions':len(changes),'new_text_repairs':71,'new_image_substitutions':14,
 'distinct_source_lines_changed':len({c['line_id'] for c in changes}),'distinct_source_pages_changed':len({c['master_pdf_page'] for c in changes}),
 'cumulative_tracked_repair_decisions':113,'apparatus_entries':14,
 'apparatus_status_counts':dict(collections.Counter(n['status'] for n in notes)),
 'character_interpretation_limitation_entries':10,'documented_source_loss_entries':1,
 'visual_objects_in_provenance':24,'visual_objects_inserted':22,'glyph_image_objects_inserted':18,
 'critical_apparatus_pages':4,'reader_pdf_sha256':artifact_hashes['reader'],'critical_apparatus_pdf_sha256':artifact_hashes['critical'],
 'last_fully_transcribed_source_unit':'AB01-PDF0089',
 'transcription_status_qualification':'Full-range first-pass coverage inherited from v002; v003 contains a selected source reread and 85 recorded successor decisions. Ten reading entries have exact-image dispositions, not settled character transcriptions. Not a fully verified edition.',
 'last_source_replayed_source_unit':'AB01-PDF0089','last_fully_verified_source_unit':None,
 'verification_field_definition':'Full verification includes an independent cold source/reading audit, not performed by this producing assistant or the technical checker.',
 'first_untouched_source_unit':None,'first_untouched_scope':'Within S01 only; none wholly untouched. No statement of coverage outside S01.',
 'first_character_interpretation_limitation_source_unit':'AB01-PDF0022','documented_source_loss_source_unit':'AB01-PDF0002',
 'first_source_unit_outside_S01':'AB01-PDF0090','later_sessions_executed':False,'S02_started':False,
 'canonical_Nallino_checkpoint':sync['canonical_Nallino_checkpoint'],'canonical_Nallino_sha256':sync['canonical_Nallino_sha256'],
 'canonical_Arabic_checkpoint':None,'canonical_Arabic_hash':None,'accepted_Arabic_corrections':0,'new_target_language_translations':[],
 'two_clean_builds_byte_identical':True,'technical_audit_receipt':'receipts/technical_audit_v003.json',
 'technical_audit_status':'See the separate read-only audit receipt; a technical PASS does not close S01.',
 'independent_cold_source_audit_status':'NOT_PERFORMED','human_certification_required':False,
 'remaining_release_gate':'Independent cold source/reading replay of this pinned candidate, with any findings returned as proposals rather than patches. Repairs create a successor and require renewed checks.',
 'recovery':read('receipts/workspace_recovery.json'),
 'prior_checkpoint':'history/v002/receipts/cumulative_checkpoint.json',
 'next_session_rule':'User authorizes S02 after S01 closure only; v003 does not constitute that closure.'}
write('receipts/cumulative_checkpoint.json',cp)
write('receipts/checkpoint_lineage.json',{'current':'AB01-NALLINO-S01-v003-CANDIDATE','current_digest':sync['canonical_Nallino_sha256'],'predecessor':'AB01-NALLINO-S01-v002','predecessor_digest':sync['predecessor_pages_sha256'],'predecessor_preserved':'history/v002','reason':'Selected source reread, 71 text repairs and 14 exact-image substitutions; prior candidate remains immutable.','interrupted_reread_recovery':'history/interrupted_reread/RECOVERY_INVENTORY.json','independent_audit':False})
# Remove stale active outputs/receipts only after confirming their immutable history copies.
for p in list((R/'pdf').glob('*v002*'))+list((R/'tex').glob('*v002*'))+list((R/'transcription').glob('*v002*')):
 old=R/'history/v002'/p.relative_to(R)
 assert old.is_file() and sha(old)==sha(p),str(p)
 p.unlink()
for n in ['technical_audit.json','visual_qa.json','final_render_generation.json','encoding_repair.json','proof_crop_coordinates.json','pdf_embedded_font_inventory.txt']:
 p=R/'receipts'/n;old=R/'history/v002/receipts'/n
 if p.exists():
  assert old.exists() and sha(old)==sha(p),n
  p.unlink()
# Old first-pass mutation scripts are preserved under history/v002, not exposed as current builders.
keep={'build_edition.py','rebuild.py','rebuild_critical_notes.py','check_markup.py','revision_helpers.py','native_proof_v003.py','make_v003_assets.py','adjudicate_v003.py','synchronize_v003.py','render_v003_qa.py','audit_v003_readonly.py','finalize_metadata_v003.py','package_v003.py'}
for p in (R/'scripts').glob('*.py'):
 if p.name not in keep:
  old=R/'history/v002/scripts'/p.name
  assert old.exists() and sha(old)==sha(p),str(p)
  p.unlink()
for p in R.glob('.clean_build_*'):shutil.rmtree(p)
for p in R.rglob('__pycache__'):shutil.rmtree(p)
# Make historical-only evidence groups explicit without altering their recovered files.
(R/'history/README.md').write_text('''# Superseded and recovered evidence\n\n`v002/` preserves the prior candidate files unchanged. Its receipts and status describe that predecessor, not v003. Historical mutation scripts are retained as evidence, not as recommended current build commands.\n\n`interrupted_reread/` contains 157 recovered proof-image files. Their existence shows saved proof work, not accepted corrections. The inventory pins the exact recovered bytes. v003 decisions are separately replayed and recorded in `../ledgers/v003_changes.json`.\n\nEarlier history, where present, remains recovery evidence. No historical candidate is silently promoted to fully verified status.\n''')
print(json.dumps({'checkpoint':cp['status'],'decisions':len(changes),'changed_lines':cp['distinct_source_lines_changed'],'changed_pages':cp['distinct_source_pages_changed'],'reader_detail_pages':fullpages},indent=2))
