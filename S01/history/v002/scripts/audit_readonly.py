"""Replay technical invariants without editing the production candidate.

This is a separate process, not an independent philologist. Its result is strictly
technical: it does not certify the spelling, pointing, or meaning of the source.
Only the requested audit report is written. Run after rebuild.py.
"""
from pathlib import Path
import argparse, collections, hashlib, io, json, re, sys
import fitz
from PIL import Image

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    ap.add_argument('--master',type=Path,default=Path('/mnt/data/30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf'))
    ap.add_argument('--report',type=Path)
    a=ap.parse_args(); r=a.root.resolve()
    report=a.report or r/'receipts/technical_audit.json'
    load=lambda s: json.loads((r/s).read_text(encoding='utf-8'))
    checks=[]
    def check(name,ok,detail):
        checks.append({'test':name,'status':'PASS' if ok else 'FAIL','detail':detail})
    # Freeze production payload hashes before reading it. Reports may change; production may not.
    production=[p for folder in ('transcription','tex','pdf','source','ledgers') for p in (r/folder).rglob('*') if p.is_file()]
    before={str(p.relative_to(r)):digest(p) for p in production}
    expected='544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297'
    if not a.master.is_file():
        check('controlling master available',False,str(a.master))
        master=None
    else:
        check('controlling master exact identity',digest(a.master)==expected and a.master.stat().st_size==80946704,'Expected 80,946,704 bytes and pinned SHA-256.')
        master=fitz.open(a.master)
        check('physical master page count',len(master)==1162,{'actual':len(master),'retrieval_index_count_not_used':1161})
    excerpt=fitz.open(r/'source/SRC01_PDF0001-0089_EVIDENCE.pdf')
    check('evidence excerpt page count',len(excerpt)==89,len(excerpt))
    mismatches=[]
    if master:
        for i in range(89):
            p=master[i].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
            q=excerpt[i].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
            if (p.width,p.height,p.samples)!=(q.width,q.height,q.samples):mismatches.append(i+1)
        check('all excerpt pages visually equivalent to master at 36 dpi',not mismatches,{'pages_tested':89,'mismatch_pages':mismatches,'limit':'render equivalence, not a word-reading test'})
    ledger=load('ledgers/page_disposition.json'); owned={2,10,*range(12,90)}
    check('all physical units disposed exactly once',len(ledger)==89 and sorted(x['master_pdf_page'] for x in ledger)==list(range(1,90)),{'rows':len(ledger),'scope':'PDF1-89'})
    check('bounded ownership exact', {x['master_pdf_page'] for x in ledger if x['owned']}==owned,{'owned':len(owned),'sessions_after_S01_started':False})
    files=sorted((r/'transcription/pages').glob('*.json')); pages=[json.loads(p.read_text()) for p in files]
    check('page-record coverage',len(pages)==79 and {x['master_pdf_page'] for x in pages}==owned-{2},{'records':len(pages),'frontispiece_separately_preserved':True})
    lines=[l for p in pages for s in p['sections'] for l in s['lines']]; ids=[l['id'] for l in lines]
    check('unique source-line anchors',len(ids)==len(set(ids))==3996,{'total':len(ids),'unique':len(set(ids))})
    tex=(r/'tex/S01_NALLINO_SOURCE_v002.tex').read_text()
    check('all line anchors occur in generated TeX',all(i in tex for i in ids),{'missing':[i for i in ids if i not in tex]})
    alignment=load('ledgers/line_alignment.json')
    check('alignment ledger complete and qualified',{x['line_id'] for x in alignment}==set(ids) and all(x['locator_verification']=='NOT_INDEPENDENTLY_VERIFIED' for x in alignment),{'rows':len(alignment),'rectangles':'OCR-derived locator candidates, not certified reading boxes'})
    errors=[]; tags=re.compile(r'</?(i|n|ar|gr|sy|small|sup|m|glyph|b)>')
    for p in pages:
        for s in p['sections']:
            stack=[]
            for l in s['lines']:
                if any(ord(c)<32 for c in l['text']):errors.append([l['id'],'control character'])
                for m in tags.finditer(l['text']):
                    key=m.group(1)
                    if m.group().startswith('</'):
                        if not stack or stack[-1]!=key:errors.append([l['id'],'unmatched closing tag',key])
                        else:stack.pop()
                    else:stack.append(key)
            if stack:errors.append([p['anchor'],s['role'],'unclosed',stack])
    check('markup nesting and encoding controls',not errors,errors)
    glyphs=[g for l in lines for g in re.findall(r'<glyph>(.*?)</glyph>',l['text'])]
    check('bounded inline image fallbacks',set(glyphs)=={'AB01-PDF0022-G01','AB01-PDF0070-G01','AB01-PDF0082-G01','AB01-PDF0082-G02'} and len(glyphs)==4,glyphs)
    figs=load('ledgers/figure_provenance.json'); failures=[]
    for f in figs:
        raw=r/f['raw_path']; pres=r/f['presentation_path']
        if digest(raw)!=f['raw_sha256'] or digest(pres)!=f['presentation_sha256']:failures.append([f['object_id'],'hash'])
        if master:
            embedded=master.extract_image(f['source_xref'])['image']
            im=Image.open(io.BytesIO(embedded)); crop=im.crop(tuple(f['crop_box_pixels']))
            actual=Image.open(pres)
            if crop.mode!=actual.mode or crop.size!=actual.size or crop.tobytes()!=actual.tobytes():failures.append([f['object_id'],'native pixel mismatch'])
            if f['object_id']=='AB01-PDF0002-F01' and raw.read_bytes()!=embedded:failures.append([f['object_id'],'raw JPX not exact'])
    check('all figure crops equal native source pixels',not failures,{'objects':len(figs),'failures':failures,'operations':'integer crop only; frontispiece JPX also byte-exact'})
    check('fallbacks all linked to assets',set(glyphs)<={x['object_id'] for x in figs},glyphs)
    forms=load('ledgers/formula_provenance.json')
    math_count=sum(len(re.findall(r'<m>.*?</m>',l['text'])) for l in lines)
    check('formula ledger coverage',len(forms)==math_count==47,{'objects':len(forms),'source_math_spans':math_count,'recomputation':'none'})
    key=load('ledgers/transliteration_key.json')
    check('printed transliteration key coverage',len(key)==11 and all(x['line_id'] in ids for x in key),{'entries':len(key),'no_invented_reader_column_headers':True})
    corrections=load('ledgers/printed_corrigenda_routing.json'); bad=[]
    for c in corrections:
        if not set(c['source_line_ids'])<=set(ids):bad.append(c['corrigendum_id'])
        if any(not 16<=int(x.rsplit('PDF',1)[1])<=416 for x in c['target_anchors']):bad.append(c['corrigendum_id'])
    check('printed corrigenda routes valid',len(corrections)==86 and not bad,{'entries':len(corrections),'bad_routes':bad,'critical_limit':'routes recorded; Nallino corrections not silently applied'})
    sync=load('receipts/canonical_synchronization.json')
    h=hashlib.sha256()
    for p in files:h.update(p.name.encode());h.update(b'\0');h.update(p.read_bytes())
    check('canonical Nallino checkpoint digest',h.hexdigest()==sync['canonical_Nallino_sha256'],h.hexdigest())
    check('Arabic canon untouched',sync['canonical_Arabic_checkpoint'] is None and sync['accepted_Arabic_corrections']==0,{'Arabic_checkpoint':None,'translation_languages':sync['target_languages_requested_in_current_instruction']})
    build=load('receipts/deterministic_builds.json'); pdf=r/'pdf/S01_NALLINO_SOURCE_v002.pdf'; doc=fitz.open(pdf)
    check('two clean two-pass builds',len(build['builds'])==2 and all(b['clean_directory'] and b['passes']==2 for b in build['builds']),{'builds':2,'passes_each':2})
    check('final PDF equals both builds',build['byte_identical'] and all(b['pdf_sha256']==digest(pdf) for b in build['builds']),digest(pdf))
    check('all 80 page rasters reproducible',build['all_page_rasters_identical'] and all(len(b['raster_hashes_36dpi'])==80 for b in build['builds']),'36 dpi; A and B')
    check('clean compile diagnostics',not any(b[k] for b in build['builds'] for k in ('missing_characters','overfull_boxes','source_line_overflows','font_warnings')),{b['build']:{k:b[k] for k in ('missing_characters','overfull_boxes','source_line_overflows','font_warnings')} for b in build['builds']})
    mapping=load('receipts/output_page_map.json');bad_anchor=[];outside=[];fulltext=''
    for i,p in enumerate(doc):
        t=p.get_text();fulltext+=t+'\n';m=mapping[i]
        if m['anchor'] and m['anchor'] not in t:bad_anchor.append(i+1)
        for b in p.get_text('blocks'):
            if len(b)>6 and b[6]==0 and (b[0]<-1 or b[1]<-1 or b[2]>p.rect.width+1 or b[3]>p.rect.height+1):outside.append(i+1)
    check('reader page sequence and anchors',len(doc)==80 and not bad_anchor and [m['master_pdf_page'] for m in mapping]==[None,2,10,12,13,14]+list(range(16,90)),{'pages':len(doc),'missing_anchors':bad_anchor,'modern_editor_notice_pages':1,'historical_pages':79})
    check('text blocks inside page bounds',not outside,{'out_of_bounds_pages':sorted(set(outside)),'limit':'does not detect every possible internal overlap'})
    unwanted=[s for s in ['Digitized by Google','Original from','books.google.com'] if s.lower() in fulltext.lower()]
    check('provider text absent from reader',not unwanted,unwanted)
    critical=load('receipts/critical_notes_builds.json'); critical_path=r/critical['artifact']; cd=fitz.open(critical_path)
    ct='\n'.join(p.get_text() for p in cd)
    critical_ok=(critical['byte_identical'] and len(critical['builds'])==2
        and all(b['clean_directory'] and b['passes']==2 and b['pdf_sha256']==digest(critical_path) for b in critical['builds'])
        and not any(b[k] for b in critical['builds'] for k in ('missing_characters','overfull_boxes','font_warnings'))
        and all(x['note_id'] in ct for x in load('ledgers/unresolved_readings.json')))
    check('separate critical apparatus coverage and clean builds',critical_ok,{'pages':len(cd),'apparatus_notes':12,'role':'MODERN_EDITORIAL','byte_identical':critical['byte_identical'],'pdf_sha256':digest(critical_path)})
    font_files=[str(p.relative_to(r)) for p in r.rglob('*') if p.suffix.lower() in ('.ttf','.otf','.woff','.woff2','.ttc')]
    check('no font files distributed',not font_files,font_files)
    after={str(p.relative_to(r)):digest(p) for p in production}
    check('production outputs not patched by audit',before==after,{'payload_files_frozen':len(before)})
    result={'status':'PASS_TECHNICAL_SCOPE_ONLY' if all(c['status']=='PASS' for c in checks) else 'FAIL_TECHNICAL_SCOPE','audit_mode':'read-only separate executable process','independent_philological_audit':False,'auditor_identity_limit':'Script authored in the production session. Separate execution does not make it an independent textual reviewer.','textual_fidelity_certified':False,'flagged_source_entries':len(load('ledgers/unresolved_readings.json')),'open_reading_entries':sum(x['status']=='OPEN' for x in load('ledgers/unresolved_readings.json')),'documented_source_loss_entries':sum(x['category']=='source_loss' for x in load('ledgers/unresolved_readings.json')),'checks':checks,'remaining_release_gate':'Independent cold source/reading audit and disposition of open reading issues; no human-only certification requirement.'}
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(result['status'],len(checks),'checks;',sum(c['status']=='FAIL' for c in checks),'failures')
    return 0 if result['status']=='PASS_TECHNICAL_SCOPE_ONLY' else 1
if __name__=='__main__':sys.exit(main())
