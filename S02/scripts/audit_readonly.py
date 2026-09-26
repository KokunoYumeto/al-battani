"""Read-only technical audit of the bounded S02 candidate.

Does not edit transcription, TeX, assets or PDFs. This is not a separate
human/model philological review. It writes only its audit receipt.
"""
from pathlib import Path
import json,hashlib,csv,re,io
import fitz
from PIL import Image
R=Path(__file__).resolve().parents[1]
MASTER=R.parent/'30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    return {str(p.relative_to(R)):sha(p) for name in ['transcription','tex','source','pdf','ledgers'] for p in sorted((R/name).rglob('*')) if p.is_file()}
before=snapshot();checks=[]
def ck(name,ok,detail=None):
    checks.append({'check':name,'pass':bool(ok),'detail':detail})

def load(rel):return json.loads((R/rel).read_text())
master=fitz.open(MASTER)
ck('controlling_source_hash',sha(MASTER)=='544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297')
ck('controlling_source_page_count',len(master)==1162,len(master))
pages=[json.loads(p.read_text()) for p in sorted((R/'transcription/pages').glob('*.json'))]
ck('transcribed_range_exact', [p['master_pdf_page'] for p in pages]==list(range(90,120)))
ck('physical_to_printed_map',all(p['printed_page']==p['master_pdf_page']-89 for p in pages))
lines=[l for p in pages for s in p['sections'] for l in s['lines']]
ids=[l['id'] for l in lines]
ck('all_line_ids_unique',len(ids)==len(set(ids)),len(ids))
ck('line_id_page_and_zone',all(l['id'].startswith(p['anchor']+'-'+s['role']+'-L') for p in pages for s in p['sections'] for l in s['lines']))
ck('no_control_characters_in_production_text',all(not any(ord(c)<32 for c in l['text']) for l in lines))
ck('historical_roles_separated',all(s['authorship']==('NALLINO_TRANSLATION' if s['role']=='body' else 'NALLINO_APPARATUS') for p in pages for s in p['sections']))
ck('math_markup_paired',all(l['text'].count('<m>')==l['text'].count('</m>') for l in lines))
ck('all_math_braces_balanced',all(t.count('{')==t.count('}') for l in lines for t in re.findall(r'<m>(.*?)</m>',l['text'])))
ck('multiplication_symbol_repair_present',r'\times' in next(l['text'] for l in lines if l['id']=='AB01-PDF0115-notes_right-L002'))
with (R/'ledgers/page_disposition.tsv').open() as f:disp=list(csv.DictReader(f,delimiter='\t'))
ck('all_109_owned_pages_disposed', [int(x['master_pdf_page']) for x in disp]==list(range(90,199)))
ck('only_30_pages_claim_transcription',sum(x['state']=='SOURCE_READ_FIRST_PASS' for x in disp)==30)
ck('79_remaining_pages_not_claimed',all(x['state']=='NOT_TRANSCRIBED' for x in disp[30:]))

# Verify the new excerpt against the controlling witness, page by page.
excerpt=fitz.open(R/'source/SRC01_PDF0090-0119_EVIDENCE.pdf');excerpt_details=[]
for j in range(len(excerpt)):
    a=master[j+89].get_pixmap(dpi=72,alpha=False);b=excerpt[j].get_pixmap(dpi=72,alpha=False)
    excerpt_details.append({'source_page':j+90,'equal':a.width==b.width and a.height==b.height and a.samples==b.samples})
ck('source_excerpt_30_pages',len(excerpt)==30)
ck('every_source_excerpt_page_pixel_identical',all(x['equal'] for x in excerpt_details),excerpt_details)
ck('source_excerpt_hash_matches_receipt',sha(R/'source/SRC01_PDF0090-0119_EVIDENCE.pdf')==load('receipts/source_excerpt_validation.json')['sha256'])

# Check all supplied raw/presentation crops, including proof-only crops.
objects=load('ledgers/visual_objects.json');asset_details=[]
for x in objects:
    pix=fitz.Pixmap(master,x['source_xref'])
    im=Image.frombytes('L' if pix.n==1 else 'RGB',(pix.width,pix.height),pix.samples)
    expected=im.crop(x['native_pixel_rect'])
    actual=Image.open(R/x['raw_path'])
    rect=x['native_pixel_rect'];bounds=0<=rect[0]<rect[2]<=im.width and 0<=rect[1]<rect[3]<=im.height
    detail={'id':x['id'],'in_source_bounds':bounds,'native_pixels_equal':expected.mode==actual.mode and expected.size==actual.size and expected.tobytes()==actual.tobytes(),'raw_hash_equal':sha(R/x['raw_path'])==x['raw_sha256'],'presentation_hash_equal':sha(R/x['presentation_path'])==x['presentation_sha256'],'presentation_equals_raw':(R/x['raw_path']).read_bytes()==(R/x['presentation_path']).read_bytes()}
    asset_details.append(detail)
ck('all_native_crops_replay_exactly',all(all(v for k,v in d.items() if k!='id') for d in asset_details),asset_details)
ck('figure_crop_bottom_not_clipped',next(x for x in objects if x['id']=='AB01-PDF0115-F01')['requested_pdf_rect']==[116.,300.,310.,491.])

# Literal table export consistency; no mathematical interpolation performed.
tables=load('ledgers/tables.json');cells=load('ledgers/table_cell_provenance.json');td=[]
for t in tables:
    expected=[[('[IMAGE:AB01-PDF0096-T01-R04-C10]' if v=='[IMAGE]' else v) for v in row] for row in t['rows']]
    for ext,delim in [('csv',','),('tsv','\t')]:
        with (R/'tables'/(t['id']+'.'+ext)).open() as f:actual=list(csv.reader(f,delimiter=delim))
        td.append({'file':t['id']+'.'+ext,'literal_equal':actual==expected})
ck('two_11_by_11_tables',len(tables)==2 and all(len(t['rows'])==11 and all(len(row)==11 for row in t['rows']) for t in tables))
ck('242_table_cells',len(cells)==242)
ck('table_cell_ids_unique',len({x['cell_id'] for x in cells})==242)
ck('one_unresolved_table_cell',sum(x['literal'] is None for x in cells)==1)
ck('table_exports_literal_match',all(x['literal_equal'] for x in td),td)
ck('cell_locator_rectangles_valid',all(0<=c['source_pdf_rect'][0]<c['source_pdf_rect'][2]<master[int(c['table_id'][8:12])-1].rect.width and 0<=c['source_pdf_rect'][1]<c['source_pdf_rect'][3]<master[int(c['table_id'][8:12])-1].rect.height for c in cells))

reader=fitz.open(R/'pdf/S02_NALLINO_SOURCE_v002.pdf');critical=fitz.open(R/'pdf/S02_CRITICAL_NOTES_v002.pdf')
ck('reader_has_notice_plus_30_source_pages',len(reader)==31,len(reader))
ck('critical_apparatus_is_separate',len(critical)==2,len(critical))
ck('each_reader_page_has_correct_source_anchor',all(f'AB01-PDF{90+j:04}'.lower() in reader[j+1].get_text().lower() for j in range(30)))
rt='\n'.join(p.get_text() for p in reader)
ck('no_provider_text_in_reader',all(s not in rt.lower() for s in ['digitized by google','books.google.com','princeton university']))
used=[x for x in objects if x.get('in_reader')]
embedded=[]
for xref in {img[0] for p in reader for img in p.get_images(full=True)}:
    px=fitz.Pixmap(reader,xref)
    im=Image.frombytes('L' if px.n==1 else 'RGB',(px.width,px.height),px.samples).convert('RGB')
    embedded.append((im.size,hashlib.sha256(im.tobytes()).hexdigest()))
ck('five_expected_reader_image_objects',len(used)==5 and len(embedded)==5,{'expected':len(used),'embedded':len(embedded)})
image_matches=[]
for x in used:
    im=Image.open(R/x['presentation_path']).convert('RGB')
    image_matches.append({'id':x['id'],'matched':(im.size,hashlib.sha256(im.tobytes()).hexdigest()) in embedded})
ck('reader_embeds_exact_source_image_pixels',all(x['matched'] for x in image_matches),image_matches)
for suffix,n in [('NALLINO_SOURCE',31),('CRITICAL_NOTES',2)]:
    stem='S02_'+suffix+'_v002'
    rep=load('receipts/build_report.json')
    records=[x for x in rep['records'] if x['stem']==stem]
    ck(stem+'_two_clean_builds',len(records)==2 and all(x['passes']==2 and not x['bad_log_entries'] and not x['warnings'] for x in records))
    ck(stem+'_byte_identical_builds',records[0]['sha256']==records[1]['sha256']==sha(R/'pdf'/(stem+'.pdf')))
findings=load('ledgers/critical_findings.json')
ck('seven_modern_findings_recorded',len(findings)==7)
ck('three_uncertain_objects_retained',sum(x['disposition']=='IMAGE_PRESERVED_UNRESOLVED' for x in findings)==3)
ck('no_arabic_canon_modification',load('receipts/canonical_synchronization.json').get('canonical_arabic_modified') is False)
after=snapshot();ck('audit_left_all_production_inputs_unchanged',before==after)
report={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'S02 partial candidate; physical PDF90–119 only','auditor':'Separate read-only checking program, executed by the producing assistant; not an independent human/model reading audit','checks_passed':sum(x['pass'] for x in checks),'checks_total':len(checks),'checks':checks,'frozen_production_files':before,'source_fidelity_limit':'Automated checks prove declared identities, structure and crop preservation; they do not prove every philological reading. A same-assistant direct-source first pass and bounded visual recheck are recorded separately.'}
(R/'receipts/read_only_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],report['checks_passed'],'/',len(checks))
for x in checks:
    if not x['pass']:print('FAIL:',x)
