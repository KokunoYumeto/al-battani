"""Derive transparent registers from the manually source-read page JSON.
No numeric interpolation or source-text normalization is performed here.
"""
from pathlib import Path
import json, re, csv, hashlib, shutil
R=Path(__file__).resolve().parents[1]
def dump(p,obj):
 (R/p).parent.mkdir(parents=True,exist_ok=True)
 (R/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def tsv(p,rows,fields):
 (R/p).parent.mkdir(parents=True,exist_ok=True)
 with (R/p).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows)
P=[json.loads(p.read_text()) for p in sorted((R/'transcription/pages').glob('*.json'))]
assert [d['master_pdf_page'] for d in P]==list(range(90,120))
A={d['master_pdf_page']:d for d in P}
V=json.loads((R/'ledgers/visual_objects.json').read_text())
T=json.loads((R/'ledgers/tables.json').read_text())
lines=[];math=[];margins=[];links=[];headings=[];nums=[]
for d in P:
 for sec in d['sections']:
  for l in sec['lines']:
   tx=l['text'];obj=re.fullmatch(r'<(table|figure|figureleft)>(.*?)</\1>',tx)
   kind='layout_control' if tx=='<endfigureleft/>' else 'source_object' if obj else 'source_marginal_register' if sec['role']=='margins' else 'source_text_line'
   lines.append({'anchor':l['id'],'master_pdf_page':d['master_pdf_page'],'printed_page':d['printed_page'],'source_id':'SRC01','section':sec['role'],'role':sec['authorship'],'record_kind':kind,'locator_type':'page + manually delimited zone + ordinal source line/object','pixel_line_bbox':'NOT_ASSERTED','source_markup':tx})
   if sec['role']=='margins':
    margins.append({'anchor':l['id'],'master_pdf_page':d['master_pdf_page'],'reading':tx,'disposition':'Preserved in marginal register; Arabic page references also printed in reader; original running line counters/signatures not repeated as body prose.'})
    m=re.fullmatch(r'(?:Textus )?p\.\s*(\d+)\.',tx)
    if m:links.append({'latin_anchor':d['anchor'],'latin_printed_page':d['printed_page'],'printed_arabic_page_reference':int(m[1]),'target_logical_id':'AB01-PARSIII-PRINT'+m[1].zfill(4),'basis':'Reference explicitly printed in Nallino source margin','physical_target_map':'not asserted by this batch','arabic_canonical_checkpoint':'NONE_ASSUMED','arabic_source_collation':'not performed; locator only'})
   if '<center>' in tx and re.sub('<[^>]+>','',tx).startswith('CAPUT'):headings.append({'source_anchor':l['id'],'printed_page':d['printed_page'],'heading':re.sub('<[^>]+>','',tx)})
   for k,m in enumerate(re.finditer(r'<m>(.*?)</m>',tx),1):
    math.append({'id':l['id']+f'-M{k:02}','source_line_anchor':l['id'],'master_pdf_page':d['master_pdf_page'],'printed_page':d['printed_page'],'role':sec['authorship'],'tex':m[1],'status':'SOURCE_READ_IMAGE_COMPONENT' if 'sourceglyph' in m[1] else 'SOURCE_READ_FIRST_PASS','note':'Explicit mathematical markup only; other numerical prose is indexed separately. No recalculation used to replace source values.'})
   if sec['role']!='margins':
    clean=re.sub(r'<(glyph|figure|figureleft|table)>.*?</\1>', '', tx)
    clean=re.sub(r'\\sourceglyph\{[^}]+\}', '', clean)
    clean=re.sub(r'<[^>]*>',' ',clean)
    for k,m in enumerate(re.finditer(r'\d+(?:[.,]\d+)*(?:[°′″‴])?',clean),1):
     nums.append({'id':l['id']+f'-NUM{k:02}','source_line_anchor':l['id'],'token':m[0],'classification':'literal numeric token; unit and meaning require surrounding source text'})
linefields=list(lines[0]);tsv('ledgers/line_alignment.tsv',lines,linefields)
tsv('ledgers/formula_provenance.tsv',math,list(math[0]));dump('ledgers/formula_provenance.json',math)
tsv('ledgers/numeric_token_register.tsv',nums,list(nums[0]))
tsv('ledgers/marginal_disposition.tsv',margins,list(margins[0]));tsv('ledgers/arabic_source_links.tsv',links,list(links[0]));tsv('ledgers/chapter_boundaries.tsv',headings,list(headings[0]))
rows=[]
for n in range(90,199):
 owned=n in A
 rows.append({'anchor':f'AB01-PDF{n:04}','master_pdf_page':n,'printed_page':n-89,'source_present':True,'state':'SOURCE_READ_FIRST_PASS' if owned else 'NOT_TRANSCRIBED','transcription_path':f'transcription/pages/AB01-PDF{n:04}.json' if owned else '', 'reader_page':n-88 if owned else '', 'roles':'NALLINO_TRANSLATION;NALLINO_APPARATUS','provider_matter':'Excluded from transcription; preserved only in source evidence','verification':'Direct source-image reading; batch build/technical checks and limited read-only recheck' if owned else 'No transcription claim','note':A[n]['editorial_note'] if owned else ('Preview only, not transcription.' if n<=122 else '')})
tsv('ledgers/page_disposition.tsv',rows,list(rows[0]))
# Literal tables: preserve uncertainty as image reference, not an interpolated value.
cells=[]
for t in T:
 out=R/'tables';out.mkdir(exist_ok=True)
 for suffix,sep in [('tsv','\t'),('csv',',')]:
  with (out/(t['id']+'.'+suffix)).open('w',encoding='utf8',newline='') as f:
   w=csv.writer(f,delimiter=sep,lineterminator='\n')
   for row in t['rows']:w.writerow([v if v!='[IMAGE]' else '[IMAGE:AB01-PDF0096-T01-R04-C10]' for v in row])
 for c in t['cells']:
  cells.append({'table_id':t['id'],**c})
# Existing table ledger has explicitly recorded native-grid coordinate estimates.
dump('ledgers/table_cell_provenance.json',cells)
fields=[]
for c in cells:
 for k in c:
  if k not in fields:fields.append(k)
tsv('ledgers/table_cell_provenance.tsv',[{k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in c.items()} for c in cells],fields)
# Exact supported findings, with separate unencoded readings and printed inconsistencies.
findings=[
 {'id':'S02-U001','category':'table','source_anchor':'AB01-PDF0096-T01-R04-C10','master_pdf_page':96,'printed_page':7,'source_rect':[401,550,416,562],'diplomatic_reading':'1 followed by a damaged digit, retained as source image','alternatives':'12 is plausible from the surviving strokes; no numeric reading accepted','disposition':'IMAGE_PRESERVED_UNRESOLVED','confidence':'high for pixel preservation; unresolved character reading','image':'AB01-PDF0096-T01-R04-C10','propagation':'The CSV/TSV has an image marker, not 12.'},
 {'id':'S02-U002','category':'formula','source_anchor':'AB01-PDF0101-notes_right-L003','master_pdf_page':101,'printed_page':12,'source_rect':[390.5,677,420.5,689],'diplomatic_reading':'59°3[damaged digit]′ within the numerator, retained as source image','alternatives':'59°36′ / 59°35′; 36 is supported by the body reading, but not imposed on the damaged note','disposition':'IMAGE_PRESERVED_UNRESOLVED','confidence':'high for exact image; minute digit unresolved','image':'AB01-PDF0101-G01','propagation':'No arithmetic correction; printed 72°2′ and 36°1′ retained.'},
 {'id':'S02-U003','category':'reading','source_anchor':'AB01-PDF0107-notes_right-L017','master_pdf_page':107,'printed_page':18,'source_rect':[446,685,467,698],'diplomatic_reading':'Damaged Arabic spelling following corruptum','alternatives':'No defensible complete character transcription assigned; exact image is the diplomatic object','disposition':'IMAGE_PRESERVED_UNRESOLVED','confidence':'high for pixels; character interpretation withheld','image':'AB01-PDF0107-G01','propagation':'No modern place-name substituted.'},
 {'id':'S02-C001','category':'reading','source_anchor':'AB01-PDF0105-body-L035;AB01-PDF0105-body-L038','master_pdf_page':105,'printed_page':16,'source_rect':[423,583,535,643],'diplomatic_reading':'78°23′ in the first statement; 78°28′ in the repeated value','alternatives':'Both are printed; no harmonization selected','disposition':'PRINTED_DISCREPANCY_RETAINED','confidence':'high','image':'AB01-PDF0105-values-proof','propagation':'The following 11°32′ is also retained. No emendation propagated.'},
 {'id':'S02-C002','category':'reading','source_anchor':'AB01-PDF0105-body-L040;AB01-PDF0106-body-L001','master_pdf_page':105,'printed_page':16,'source_rect':[489,650,534,669],'diplomatic_reading':'Page 16 ends umbrae; page 17 begins brae rerum rotabunt','alternatives':'Apparent repeated ending across the physical seam','disposition':'PRINTED_SEAM_RETAINED','confidence':'high','image':'AB01-PDF0105-SEAM-proof','propagation':'No deletion or joining of the repeated ending.'},
 {'id':'S02-C003','category':'reading','source_anchor':'AB01-PDF0099','master_pdf_page':99,'printed_page':10,'source_rect':None,'diplomatic_reading':'Two body calls printed (1); the second bottom note is numbered (2)','alternatives':'No replacement of the second body call with (2)','disposition':'PRINTED_NOTE_CALLS_RETAINED','confidence':'high','image':'','propagation':'Original note call and note heading both retained.'},
 {'id':'S02-P001','category':'provenance','source_anchor':'AB01-PDF0106-notes_right-L002','master_pdf_page':106,'printed_page':17,'source_rect':None,'diplomatic_reading':'Printed p.230 has an apparent overstrike on the holding-copy scan','alternatives':'Copy-specific marking; not attributed to Nallino as an authorized correction','disposition':'PRINTED_TEXT_RETAINED_COPY_MARK_IN_EVIDENCE','confidence':'mark visible; agency not established','image':'','propagation':'Underlying 230 remains in the historical transcription.'}
]
# Resolve finding line anchors directly from unique source text rather than relying on hand-entered ordinals.
for f in findings:
 if f['id']=='S02-U003':
  for sec in A[107]['sections']:
   for l in sec['lines']:
    if '<glyph>AB01-PDF0107-G01' in l['text']:f['source_anchor']=l['id']
 if f['id']=='S02-C001':
  f['source_anchor']=';'.join(l['id'] for s in A[105]['sections'] if s['role']=='body' for l in s['lines'] if ('78° 23′' in l['text'] or '78°28′' in l['text']))
 if f['id']=='S02-C002':
  f['source_anchor']=A[105]['sections'][0]['lines'][-1]['id']+';'+A[106]['sections'][0]['lines'][0]['id']
dump('ledgers/critical_findings.json',findings)
tsv('ledgers/critical_findings.tsv',findings,list(findings[0]))
tsv('ledgers/unresolved_readings.tsv',[f for f in findings if f['disposition']=='IMAGE_PRESERVED_UNRESOLVED'],list(findings[0]))
tsv('ledgers/canonical_correction_proposals.tsv',[],['proposal_id','canonical_anchor','reading','proposal','evidence','status'])
tsv('ledgers/witness_variants.tsv',[],['variant_id','source_anchor','witness','reading','status'])
dump('receipts/canonical_synchronization.json',{'session':'S02','historical_source_checkpoint':'S02_NALLINO_SOURCE_v002_print001-030','canonical_arabic_checkpoint':None,'canonical_arabic_hash':None,'reason':'This batch preserves the historical Latin translation and its apparatus. Marginal Arabic printed-page references are supplied as locators, not as an independently collated Arabic canon.','canonical_arabic_modified':False,'target_language_translations_generated':[],'new_translation_status':'NOT_REQUESTED_IN_THIS_CONTINUATION','historical_variants':'Nallino’s cited variants remain in his notes; not re-attributed as new collation.'})
for x in V:
 x['in_reader']=x['kind'] in ('figure','glyph','table_cell_glyph')
 x['in_reader_as_editable_table']=x['kind']=='table'
dump('ledgers/visual_objects.json',V)
stats={'owned_session_pages':109,'transcribed_pages':30,'remaining_pages':79,'text_line_anchors':sum(l['record_kind']=='source_text_line' for l in lines),'source_object_insertion_anchors':sum(l['record_kind']=='source_object' for l in lines),'marginal_register_records':len(margins),'explicit_math_spans':len(math),'literal_table_cells':len(cells),'tables':len(T),'native_diagrams':sum(v['kind']=='figure' for v in V),'unencoded_image_glyphs':sum(v['kind'] in ('glyph','table_cell_glyph') for v in V),'chapter_headings':len(headings),'arabic_margin_locator_records':len(links)}
dump('receipts/content_counts.json',stats)
print(json.dumps(stats,indent=2))
