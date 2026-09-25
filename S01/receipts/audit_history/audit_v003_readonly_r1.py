#!/usr/bin/env python3
"""Read-only technical audit of S01 v003. Writes JSON to stdout only.
This program does not determine historical readings and is not a substitute
for an independent philological cold audit. Run from any working directory.
"""
from __future__ import annotations
import collections, hashlib, io, json, re, sys
from pathlib import Path
import fitz
from PIL import Image

R = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE = '544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297'
checks: list[dict] = []
def sha_bytes(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def sha(p: Path) -> str: return sha_bytes(p.read_bytes())
def load(n: str): return json.loads((R/n).read_text(encoding='utf-8'))
def check(name: str, ok: bool, detail=None):
    checks.append({'check': name, 'pass': bool(ok), 'detail': detail})
def line_map(directory: Path):
    out={}; pages=[]
    for p in sorted(directory.glob('*.json')):
        d=json.loads(p.read_text()); pages.append(d)
        for s in d['sections']:
            for l in s['lines']:
                if l['id'] in out: raise ValueError('Duplicate anchor '+l['id'])
                out[l['id']]=l['text']
    return out,pages

def run():
    full=R.parent/'30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf'
    excerpt=R/'source/SRC01_PDF0001-0089_EVIDENCE.pdf'
    source=fitz.open(full if full.exists() else excerpt)
    if full.exists():
        check('controlling_master_bytes_hash_pages',len(source)==1162 and full.stat().st_size==80946704 and sha(full)==EXPECTED_SOURCE,{'pages':len(source),'sha256':sha(full)})
    else:
        check('master_identity_not_retested_without_external_master',True,'Full master absent; bundled 89-page source excerpt used for crop replay. Master hash is provenance, not newly verified in this mode.')
    ex=fitz.open(excerpt)
    check('bundled_source_excerpt_89_physical_pages',len(ex)==89,{'sha256':sha(excerpt),'pages':len(ex)})
    dispositions=load('ledgers/page_disposition.json')
    expected_owned=[2,10]+list(range(12,90))
    check('exact_physical_dispositions',len(dispositions)==89 and sorted(x['master_pdf_page'] for x in dispositions)==list(range(1,90)))
    check('exact_owned_source_units',sorted(x['master_pdf_page'] for x in dispositions if x['owned'])==expected_owned,{'owned_count':len(expected_owned)})
    current,pages=line_map(R/'transcription/pages')
    previous,oldpages=line_map(R/'history/v002/transcription/pages')
    check('page_record_coverage',sorted(d['master_pdf_page'] for d in pages)==[10]+list(range(12,90)),len(pages))
    check('line_anchors_unique_unchanged',len(current)==3996 and set(current)==set(previous),len(current))
    check('text_bearing_pages_and_owned_blank',sum(bool(d['sections']) for d in pages)==78 and not next(d for d in pages if d['master_pdf_page']==15)['sections'])
    check('authorship_and_source_hash',all(d['role']=='NALLINO_APPARATUS' and d['source_sha256']==EXPECTED_SOURCE for d in pages))
    changes=load('ledgers/v003_changes.json'); replay=dict(previous); chain_errors=[]
    for c in changes:
        lid=c['line_id']
        if replay.get(lid)!=c['before']:chain_errors.append(c['change_id'])
        replay[lid]=c['after']
    check('all_changes_replay_from_immutable_v002',not chain_errors and replay==current,{'decisions':len(changes),'changed_lines':len({c['line_id'] for c in changes}),'changed_pages':len({c['master_pdf_page'] for c in changes}),'chain_errors':chain_errors})
    check('85_tracked_decisions_unique_ids',len(changes)==85 and len({c['change_id'] for c in changes})==85)
    check('source_evidence_exists_for_every_change',all((R/c['evidence']).is_file() and c['source_sha256']==EXPECTED_SOURCE and not c['canonical_Arabic_changed'] for c in changes))
    alignment=load('ledgers/line_alignment.json')
    check('current_text_alignment_exact',len(alignment)==3996 and {x['line_id']:x['text'] for x in alignment}==current)
    check('locator_uncertainty_not_concealed',all(x['locator_verification']=='NOT_INDEPENDENTLY_VERIFIED' and 'inherited' in x['locator_version_note'].lower() for x in alignment))
    errs=[]; math_objects=[]; glyphs=[]
    for d in pages:
        for sec in d['sections']:
            stack=[]
            for l in sec['lines']:
                for m in re.finditer(r'</?(i|n|ar|gr|sy|small|sup|m|glyph|b)>',l['text']):
                    tag=m.group(1)
                    if m.group().startswith('</'):
                        if not stack or stack[-1]!=tag:errs.append(l['id'])
                        else:stack.pop()
                    else:stack.append(tag)
                math_objects.extend((l['id'],v) for v in re.findall(r'<m>(.*?)</m>',l['text']))
                glyphs.extend(re.findall(r'<glyph>(.*?)</glyph>',l['text']))
            if stack:errs.append(d['anchor']+':'+sec['role'])
    check('section_markup_balanced',not errs,errs)
    old_math=[(lid,x) for lid,text in previous.items() for x in re.findall(r'<m>(.*?)</m>',text)]
    formula=load('ledgers/formula_provenance.json')
    check('47_math_objects_preserved_not_recomputed',len(math_objects)==47 and math_objects==old_math and [(x['line_id'],x['latex']) for x in formula]==math_objects)
    check('formula_source_review_evidence_present',all((R/x['source_reread_evidence']).is_file() and not x['arithmetic_recomputed'] and not x['silent_correction'] for x in formula))
    key=load('ledgers/transliteration_key.json')
    check('11_entry_transliteration_key_anchored',len(key)==11 and all(x['line_id'] in current for x in key))
    corrigenda=load('ledgers/printed_corrigenda_routing.json')
    check('86_historical_corrigenda_registered_not_applied',len(corrigenda)==86 and all(x['routing_status']=='REGISTERED_NOT_APPLIED' and x['canonical_Arabic_change']=='none' for x in corrigenda))
    check('corrigenda_source_lines_current',all(x['source_entry_lines']==[current[i] for i in x['source_line_ids']] for x in corrigenda))
    notes=load('ledgers/critical_findings.json'); counts=dict(collections.Counter(x['status'] for x in notes))
    check('14_apparatus_entries_explicit_dispositions',len(notes)==14 and counts=={'DOCUMENTED_SOURCE_LOSS':1,'RESOLVED_RETAINED':3,'DISPOSED_IMAGE_FALLBACK':10},counts)
    check('apparatus_ledgers_synchronized',notes==load('ledgers/unresolved_readings.json')==load('ledgers/v003_adjudications.json'))
    figs=load('ledgers/figure_provenance.json'); new=load('ledgers/v003_native_glyph_assets.json')
    check('24_unique_visual_objects_14_new',len(figs)==24 and len({f['object_id'] for f in figs})==24 and len(new)==14)
    check('18_referenced_glyphs_have_provenance',len(glyphs)==18 and len(set(glyphs))==18 and set(glyphs)<={f['object_id'] for f in figs},glyphs)
    asset_errors=[]; crop_errors=[]; source_signatures={}; current_image=None; current_page=None
    for f in sorted(figs,key=lambda f:f.get('master_pdf_page',f.get('page'))):
        for field in ('raw','presentation'):
            p=R/f[field+'_path']
            if not p.is_file() or sha(p)!=f[field+'_sha256']:asset_errors.append(f['object_id']+':'+field)
        n=f.get('master_pdf_page',f.get('page'))
        if n!=current_page:
            current_image=None
            items=source[n-1].get_images(full=True)
            x=max(items,key=lambda x:x[2]*x[3])[0]
            current_image=Image.open(io.BytesIO(source.extract_image(x)['image'])).convert('RGB')
            source_signatures[n]=(current_image.size,sha_bytes(current_image.tobytes()))
            current_page=n
        desired=current_image.crop(tuple(f['crop_box_pixels']))
        actual=Image.open(R/f['presentation_path']).convert('RGB')
        if actual.size!=desired.size or actual.tobytes()!=desired.tobytes():crop_errors.append(f['object_id'])
    check('all_raw_and_presentation_file_hashes',not asset_errors,asset_errors)
    check('all_24_presentation_crops_replay_exact_native_pixels',not crop_errors,crop_errors)
    check('14_new_raw_and_presentation_byte_identical',all(sha(R/f['raw_path'])==sha(R/f['presentation_path']) for f in new))
    if full.exists():
        diff=[]
        current_image=None
        for n,sig in source_signatures.items():
            x=max(ex[n-1].get_images(full=True),key=lambda z:z[2]*z[3])[0]
            eim=Image.open(io.BytesIO(ex.extract_image(x)['image'])).convert('RGB')
            if (eim.size,sha_bytes(eim.tobytes()))!=sig:diff.append(n)
            eim=None
        check('source_excerpt_matches_master_at_every_asset_page',not diff,{'pages':sorted(source_signatures),'mismatches':diff})
    active={f['object_id']:f for f in figs if f['insertion_status']=='included' or f['insertion_status']=='INSERTED_IN_V003_READER'}
    pdfpaths={'reader':'pdf/S01_NALLINO_SOURCE_v003.pdf','critical':'pdf/S01_CRITICAL_NOTES_v003.pdf'}
    reader=fitz.open(R/pdfpaths['reader']); actual_images={}
    for p in reader:
        for inf in p.get_images(full=True):
            x=inf[0]
            if x not in actual_images:
                pm=fitz.Pixmap(reader,x)
                if pm.colorspace.n!=3:pm=fitz.Pixmap(fitz.csRGB,pm)
                actual_images[x]=(pm.width,pm.height,sha_bytes(pm.samples))
    absent=[]
    for gid,f in active.items():
        im=Image.open(R/f['presentation_path']).convert('RGB'); signature=(im.width,im.height,sha_bytes(im.tobytes()))
        if signature not in actual_images.values():absent.append(gid)
    check('22_visual_objects_embedded_with_exact_pixels',len(active)==22 and not absent,{'active_objects':len(active),'unmatched':absent})
    for kind,receipt,expectedpages in [('reader','receipts/deterministic_builds.json',80),('critical','receipts/critical_notes_builds.json',4)]:
        d=load(receipt); pdf=R/pdfpaths[kind]; doc=fitz.open(pdf)
        check(kind+'_two_clean_two_pass_builds',len(d['builds'])==2 and all(x['clean_directory'] and x['passes']==2 for x in d['builds']))
        check(kind+'_byte_identical_to_both_build_receipts',d['byte_identical'] and len(doc)==expectedpages and all(x['pdf_sha256']==sha(pdf) and x['pages']==expectedpages for x in d['builds']),{'sha256':sha(pdf),'pages':len(doc)})
        check(kind+'_clean_final_logs',all(not x.get(k,0) for x in d['builds'] for k in ('missing_characters','overfull_boxes','source_line_overflows','font_warnings')))
        rh={str(i+1):sha_bytes(doc[i].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples) for i in range(len(doc))}
        check(kind+'_all_page_rasters_replayed_36dpi',d['all_page_rasters_identical'] and all(x['raster_hashes_36dpi']==rh for x in d['builds']))
    tex=(R/'tex/S01_NALLINO_SOURCE_v003.tex').read_text()
    check('every_line_has_TeX_anchor',all('{'+lid+'}' in tex for lid in current))
    digest=hashlib.sha256()
    for p in sorted((R/'transcription/pages').glob('*.json')):digest.update(p.name.encode()+b'\0'+p.read_bytes())
    sync=load('receipts/canonical_synchronization.json')
    check('canonical_JSON_digest_matches_sync',digest.hexdigest()==sync['canonical_Nallino_sha256'],digest.hexdigest())
    check('no_new_translations_or_Arabic_canonical_patch',not sync['translation_artifacts'] and sync['accepted_Arabic_corrections']==0 and sync['canonical_Arabic_checkpoint'] is None)
    cp=load('receipts/cumulative_checkpoint.json')
    check('checkpoint_explicitly_open_S01_only',cp['version']=='v003' and cp['session_complete'] is False and cp['later_sessions_executed'] is False and cp['last_fully_verified_source_unit'] is None)
    inventory=load('history/interrupted_reread/RECOVERY_INVENTORY.json')
    check('all_157_recovered_proof_files_hash_verified',len(inventory)==157 and all(sha(R/'history/interrupted_reread'/x['path'])==x['sha256'] for x in inventory))
    review=load('ledgers/v003_recovered_proof_review.json')
    check('92_reviewed_contact_sheets_present_and_pinned',len(review)==92 and all(sha(R/'history/interrupted_reread/qa'/x['sheet'])==x['image_sha256'] for x in review),len(review))
    vi=load('receipts/render_inventory_v003.json')
    check('54_detail_render_files_present_and_pinned',len(vi)==54 and all(sha(R/x['file'])==x['sha256'] for x in vi))
    visual=load('receipts/visual_review_v003.json')
    check('visual_review_pins_current_PDFs',all(visual['artifact_hashes'][k]==sha(R/v) for k,v in pdfpaths.items()) and visual['reader_contact_layout_pages']==list(range(1,81)))
    forbidden=[p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and p.suffix.lower() in ('.ttf','.otf','.woff','.woff2','.pfb')]
    check('no_font_binaries_distributed',not forbidden,forbidden)
    check('no_executed_S02_artifacts',not any(p.name.startswith(('S02_NALLINO','S02_ARABIC','S02_TRANSLATION')) for p in R.rglob('*') if p.is_file()))
    check('current_PDFs_only_v003',sorted(p.name for p in (R/'pdf').glob('*.pdf'))==['S01_CRITICAL_NOTES_v003.pdf','S01_NALLINO_SOURCE_v003.pdf'])
    historical=R/'history/v002'; baseline=R.parent/'recovered_v002/AB01_S01_v002'
    if baseline.exists():
        diffs=[p.relative_to(historical).as_posix() for p in historical.rglob('*') if p.is_file() and (not (baseline/p.relative_to(historical)).is_file() or sha(p)!=sha(baseline/p.relative_to(historical)))]
        check('preserved_v002_history_byte_unchanged',not diffs,diffs)

try:
    run()
except Exception as exc:
    check('audit_execution_exception',False,repr(exc))
passed=all(x['pass'] for x in checks)
report={'schema_version':1,'artifact':'AB01-NALLINO-S01-v003-CANDIDATE','status':'PASS_TECHNICAL_CHECKS_ONLY' if passed else 'FAIL',
        'auditor':'Standalone read-only Python process; program written by the producing assistant',
        'independent_philological_audit':False,'source_reading_completion_certified':False,
        'qualification':'These tests verify package consistency, change replay, image pixels and reported builds. They do not independently adjudicate historical readings or close S01.',
        'check_count':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if passed else 1)
