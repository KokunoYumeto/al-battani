"""Construct coverage/provenance ledgers without promoting uncertain readings."""
from pathlib import Path
from collections import Counter
import json,csv,re,hashlib,unicodedata,difflib,datetime
import fitz
from rapidfuzz.fuzz import ratio as fast_ratio
R=Path(__file__).resolve().parents[1];S=Path('/mnt/data/30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf');D=fitz.open(S)
SH=hashlib.sha256(S.read_bytes()).hexdigest();OWN=[2,10]+list(range(12,90));PAGES={int(p.stem[-4:]):json.loads(p.read_text()) for p in (R/'transcription/pages').glob('*.json')}
TAG=re.compile(r'</?(?:i|n|ar|gr|sy|small|sup|m|glyph|b)>')
def plain(s):return TAG.sub('',s)
def write(name,rows,fields=None):
 (R/'ledgers'/f'{name}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 fields=fields or list(rows[0])
 with (R/'ledgers'/f'{name}.tsv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader()
  for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
def line(n,term):
 hits=[l for s in PAGES[n]['sections'] for l in s['lines'] if term in l['text']]
 return hits[0]['id'] if hits else f'AB01-PDF{n:04d}'
# Explicit unresolved readings. The recorded pixels are authoritative, not alternatives.
U=[]
def u(n,cat,term,display,alts,evidence,reason,rect=None):
 U.append({'note_id':f'S01-U{len(U)+1:03d}','category':cat,'source_anchor':f'AB01-PDF{n:04d}','line_id':line(n,term) if n in PAGES else f'AB01-PDF{n:04d}', 'displayed_reading':display,'bounded_alternatives':alts,'status':'DOCUMENTED_SOURCE_LOSS' if cat=='source_loss' else 'OPEN','confidence':'unresolved; source image retained','evidence':evidence,'reason':reason,'source_rect_pt':list(rect) if rect else list(D[n-1].rect),'coordinate_granularity':'review region' if rect else 'whole source page; exact page anchor, not a fabricated line box','critical_emendation':'none','propagation':'Nallino source layer only; Arabic authorial canon unchanged'})
u(2,'source_loss','','surviving astronomical panel','No reconstruction of the missing edges is proposed.','source/raw/AB01-PDF0002-F01-original.jpx','The source panel is already cut at top/bottom and lateral edges. Cropping the provider bands cannot recover lost information.',(0,74.88,597.84,663.84))
u(18,'reading','المثبتة','المثبتة / المبينة','المثبتة or المثبّتة; المبينة or المبيّنة','qa/p18_detail.png','Consonantal text is retained; exact small shaddah/vowel marks in note 5 remain uncertain.')
u(22,'reading','AB01-PDF0022-G01','exact source Syriac glyph image','Possible unvocalized bases ܒܛܢ / ܒܛܢܢ; vowel/diacritic encoding not resolved','source/presentation/AB01-PDF0022-G01.png','The entire visible Syriac sign sequence is preserved instead of conjecturally supplying Unicode.',(175,492,204,510))
u(40,'reading','زِگ','زِگ','زِگ / زیگ','qa/proof_40_terms.png','Persian letter/vowel differentiation remains provisional in the first-pass text; no etymological normalization.',(73,630,303,700))
u(40,'reading','βιβλιον','βιβλιον','βιβλιον / βιβλίον','qa/40_greek.png','The small Greek accent is not securely distinguished from the scan in the note quotation.')
u(56,'formula',r'\text{i. e.}','i. e.','i. e. / t. e. (first printed letter damaged)','qa/page_0056.png','The connective between two equivalent forms has a damaged first letter. This does not change the copied formulae.')
u(70,'reading','AB01-PDF0070-G01','exact source orthographic sign image','ٱ (alif with waslah) is plausible; separate alif plus unidentified upper sign remains possible','source/presentation/AB01-PDF0070-G01.png','An unsupported special-mark Unicode encoding has been withdrawn.',(281,383,291,402))
u(70,'reading','جزوأً','جزوأً; تَهَيَّأَ; تِلْقَاء; تَلِهِ','Recorded consonants retained; precise vowel/sign attachment at these examples remains provisional','qa/70_orthography_new.png','Small historical Arabic vocalization marks require further glyph-level comparison; no wholesale modernization of the spelling examples.',(70,380,550,552))
u(79,'reading','XV, adn. 3','Subbī / Ṣubbī; الصَّباء / الصُّبَّاء','Latin consonant distinction confirmed; Arabic shaddah/vowel placements provisional','qa/79_corrigendum.png','Both sides of Nallino’s own corrigendum are preserved. The correction is not silently applied to printed p. XV.')
u(80,'reading','29,36','terrestrium / terrestrium','The left lemma may be terrestri·um, with a small point or ink mark between i and u; the right is terrestrium. No different word ending is conjectured','qa/proof_80_lemma.png','The native crop shows a possible small point in the left lemma. Its status as intended punctuation or stray ink is unresolved; the source-layer encoding is not silently changed.',(65,452,380,475))
u(82,'reading','AB01-PDF0082-G01','two exact source Arabic glyph images','Tentative encodings واللول / واللولوا are withdrawn; alternative consonantal separation not promoted','qa/82_corrected_pair.png','The original and corrected forms in the 175, note 9 entry are retained independently as exact images.',(153,168,219,183))
u(84,'reading','خُذِ','vocalized Arabic two-line verse','Consonantal verse retained; vowel placements in تُمِرُّ / تَدُلَّ and final case-vowels remain provisional','qa/84_verse.png','The first hemistich is placed on the right as in the source. No normalization based on the accompanying Latin translation.')
write('unresolved_readings',U)
# Resolved issues which did not require emendation: recorded as checks, not repairs.
resolved=[(20,'والعداوة','Native pixels resolve the Arabic consonants; original tentative encoding corrected without using the Latin gloss as authority.','source/raw/AB01-PDF0020-G01-raw.png'),(41,'ثبت','Native pixels resolve the printed consonantal pointing; no vocalization is added.','source/raw/AB01-PDF0041-G01-raw.png'),(10,'AL-BATTĀNĪ','Macrons confirmed on the half-title.','qa/proof_10_name.png'),(13,'ROMAE','Imprint wording and terminal punctuation confirmed.','qa/proof_13_imprint.png'),(22,'Κοραία','Greek proper names rechecked; one iota/kappa transcription error corrected in repair ledger.','qa/late_proof_contact.png'),(30,'σχηματισμός','Missing closing parenthesis retained as witnessed; no silent punctuation repair.','qa/30_L.png'),(30,'συνῳκειωμένοι','Greek quotation rechecked, including iota-subscript and printed λαμπήνη without tau.','qa/30_R.png'),(46,'Tertio libro','Greek note accentuation replayed; no additional correction promoted.','qa/46_Greek_note.png'),(49,'4″32‴','Seconds and thirds retained; not silently converted to minutes and seconds.','qa/page_0049.png'),(53,'Χαρανιώτ','Greek name and bracketed ending confirmed.','qa/53_Greek_name.png'),(57,'R^2','Displayed superscripts and ± sign compared with source; repeated multiplication sign at wrap retained.','qa/page_0057.png'),(72,'ḏ,','Transliteration comparison key replayed; final Suter character corrected to ṯ.','qa/72_suter_key.png'),(85,'87','Fractions enlarged; Venus denominator corrected to 87, other small denominators retained.','qa/proof_85_fractions.png'),(87,'الحوالة','Printed Arabic transmission-chain spellings retained without historical identification or normalization.','qa/87_chain.png')]
write('resolved_source_checks',[{'check_id':f'S01-C{i:03d}','page':n,'line_id':line(n,term),'finding':finding,'evidence':ev,'authority':'SRC01 source pixels','result':'REPLAYED_BY_PRODUCING_ASSISTANT_NOT_INDEPENDENT_AUDIT'} for i,(n,term,finding,ev) in enumerate(resolved,1)])
# Superseded provisional flags remain in history/first_pass_pages; final page metadata points at ledgers.
for n,d in PAGES.items():
 dt=d['details']; oldkeys=[k for k in ['uncertainties','uncertain_readings','reading_flags'] if k in dt]
 for k in oldkeys:dt.pop(k)
 dt['open_reading_notes']=[x['note_id'] for x in U if x['source_anchor']==d['anchor']]
 dt['proof_repairs']=[x['repair_id'] for x in json.loads((R/'ledgers/transcription_repairs.json').read_text()) if x['page']==n]
 dt['verification_limit']='Direct source replay by the producing assistant; independent textual audit not performed.'
 (R/'transcription/pages'/f'AB01-PDF{n:04d}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# Each physical source unit gets one disposition, not one inferred from an OCR page index.
rows=[]
for n in range(1,90):
 owned=n in OWN
 if n==1:kind,role,disp='provider_service_card','SCAN_EXTRINSIC','Excluded from reader; untouched evidence retained'
 elif n==2:kind,role,disp='astronomical_frontispiece','NALLINO_APPARATUS','Raw image and conservative native-pixel panel crop retained; included as figure'
 elif n==3:kind,role,disp='library_plate','COPY_PROVENANCE','Excluded from reader; copy-specific evidence retained'
 elif n in list(range(4,10))+[11]:kind,role,disp='blank_or_binding','COPY_PROVENANCE','No intrinsic text; excluded from reader, recorded in topology'
 elif n==15:kind,role,disp='intrinsic_blank_verso','NALLINO_APPARATUS','Owned blank explicitly disposed; no phantom transcription'
 else:kind,role,disp=PAGES[n]['kind'],'NALLINO_APPARATUS','Source-replayed first-pass transcription included; open readings remain explicitly registered'
 imgs=D[n-1].get_images(full=True);largest=max(imgs,key=lambda t:t[2]*t[3]) if imgs else None
 rows.append({'master_pdf_page':n,'anchor':f'AB01-PDF{n:04d}','owned':owned,'kind':kind,'role':role,'disposition':disp,'source_sha256':SH,'physical_page_available':True,'visual_review':'Direct first-pass visual inspection; not independent audit','transcription_file':f'transcription/pages/AB01-PDF{n:04d}.json' if n in PAGES else '', 'primary_image_xref':largest[0] if largest else '', 'primary_image_pixels':[largest[2],largest[3]] if largest else [],'source_page_rect_pt':list(D[n-1].rect),'provider_marks_in_reader':False,'open_notes':[u['note_id'] for u in U if u['source_anchor']==f'AB01-PDF{n:04d}']})
write('page_disposition',rows)
# Embedded text is used here ONLY as a locator, never to alter a transcription.
def norm(t):
 t=unicodedata.normalize('NFKD',plain(t)).casefold()
 return ''.join(c for c in t if c.isalnum())
A=[]
for n,d in sorted(PAGES.items()):
 candidates=[]
 for b in D[n-1].get_text('dict', flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']:
  for l in b.get('lines',[]):
   t=''.join(s['text'] for s in l['spans']);nt=norm(t)
   if len(nt)>8:candidates.append((nt,l['bbox']))
 for sec in d['sections']:
  for l in sec['lines']:
   nt=norm(l['text']);best=(0,None)
   for x,b in candidates:
    if min(len(nt),len(x))<.5*max(len(nt),len(x)):continue
    sc=fast_ratio(nt,x)/100
    if sc>best[0]:best=(sc,b)
   box=list(best[1]) if best[0]>=.72 else list(D[n-1].rect)
   A.append({'line_id':l['id'],'master_pdf_page':n,'section':sec['role'],'source_line_ordinal_in_section':int(l['id'][-3:]),'source_rect_pt':box,'locator_method':'embedded-text similarity locator, not reading authority' if best[0]>=.72 else 'whole source page fallback','locator_similarity':round(best[0],4),'locator_verification':'NOT_INDEPENDENTLY_VERIFIED','text':l['text']})
write('line_alignment',A)
# Mathematical and numerical tokens stay in the historical notation.
F=[];NN=[]
for n,d in sorted(PAGES.items()):
 for s in d['sections']:
  for l in s['lines']:
   for j,m in enumerate(re.finditer(r'<m>(.*?)</m>',l['text']),1):F.append({'object_id':l['id']+f'-M{j:02d}','master_pdf_page':n,'line_id':l['id'],'latex':m.group(1),'role':'NALLINO_APPARATUS','disposition':'editable source notation retained','arithmetic_recomputed':False,'silent_correction':False})
   # This is a literal-token index, not a semantic extraction of all quantities.
   nums=re.findall(r'\d+(?:[.,]\d+)?(?:[°′″‴]|<sup>.*?</sup>)?',l['text'])
   if nums:NN.append({'line_id':l['id'],'master_pdf_page':n,'literal_numeric_tokens':nums,'context':l['text'],'index_status':'AUTOMATIC_LITERAL_INDEX_NOT_A_TABLE_OR_NUMERICAL_CORRECTION'})
write('formula_provenance',F)
write('numeric_literal_index',NN)
# Key: no invented original column headings. This is a structured extraction of the printed list.
K=[]
for n in (72,73):
 for l in PAGES[n]['sections'][0]['lines']:
  t=l['text']
  if (n==72 and (t.startswith('’ (') or t.startswith('‘ (') or re.match(r'<i>(dh|ǵ|gh|kh)</i>',t))) or (n==73 and (re.match(r'<i>(sh|th|w|ḍ,)',t) or t.startswith('Vocales longae'))):
   K.append({'key_row_id':f'S01-T01-R{len(K)+1:02d}','table_id':'S01-T01','line_id':l['id'],'master_pdf_page':n,'source_text':t,'source_structure':'one printed list entry; no original column headings','source_role':'NALLINO_APPARATUS'})
write('transliteration_key',K)
write('table_provenance',[{'table_id':'S01-T01','source_units':'AB01-PDF0072;AB01-PDF0073','kind':'printed transliteration list, structured as a key','rows':len(K),'machine_readable':'ledgers/transliteration_key.tsv','latex':'tex/S01_TRANSLITERATION_KEY.tex','source_faithful_main_representation':'same original list in S01_NALLINO_SOURCE_v002.tex','unwitnessed_grid_headers':'none in the reader; TSV column names are editorial metadata'},{'table_id':'S01-F01','source_units':'AB01-PDF0002','kind':'composite numerical astronomical diagram, not a rectangular grid','rows':'not applicable','machine_readable':'figure_provenance.json identifies exact pixels; numerical cells not conjecturally extracted','latex':'figure insertion in S01_NALLINO_SOURCE_v002.tex','source_faithful_main_representation':'exact raster panel','unwitnessed_grid_headers':'none'}])
# Route Nallino's printed addenda to the cited Part I page anchors, without applying them.
def roman(s):
 v={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000};tot=0;prev=0
 for c in reversed(s):x=v[c];tot+=(-x if x<prev else x);prev=max(prev,x)
 return tot
E=[];cur=None
for n in range(79,90):
 for l in PAGES[n]['sections'][0]['lines']:
  t=l['text'];m=re.match(r'^(?:Pag\.\s*)?([IVXLCDM]+|\d+)(?:[–-](\d+|[IVXLCDM]+))?(?=[,:])',t)
  if m and m.group(1).isdigit() and int(m.group(1))>327:m=None
  if m:
   if cur:E.append(cur)
   aa=m.group(1);bb=m.group(2) or aa;rom=not aa.isdigit();a=roman(aa) if rom else int(aa);b=roman(bb) if rom else int(bb)
   targets=list(range(a+9,b+10)) if rom else list(range(a+89,b+90))
   cur={'corrigendum_id':f'S01-E{len(E)+1:03d}','printed_target':aa+('–'+bb if bb!=aa else ''),'target_layer':'Part I Nallino apparatus' if rom else 'Part I Latin translation/notes','target_anchors':[f'AB01-PDF{x:04d}' for x in targets],'source_line_ids':[],'source_pages':[],'source_entry_lines':[],'routing_status':'REGISTERED_NOT_APPLIED','canonical_Arabic_change':'none'}
  if cur:
   cur['source_line_ids'].append(l['id']);cur['source_entry_lines'].append(t)
   if n not in cur['source_pages']:cur['source_pages'].append(n)
if cur:E.append(cur)
write('printed_corrigenda_routing',E)
write('proposed_canonical_corrections',[],['proposal_id','source_anchor','canonical_Arabic_checkpoint','proposal','status'])
write('witness_variants',[{'witness_scope':'Nallino’s reported variant readings and sigla','status':'Transcribed as Nallino apparatus, not new manuscript collation','source':'all relevant page/line anchors in transcription JSON','new_external_witness_collation':False,'comparator_Part_III':'Not used for S01; different owned source range'}])
write('source_evidence',[{'source_id':'SRC01','file':S.name,'sha256':SH,'bytes':S.stat().st_size,'physical_pages_fitz':len(D),'owned_units':OWN,'index_discrepancy':'Files retrieval labels this source 1161 pages; physical PDF and controlling manifest report 1162. All S01 anchors use the physical PDF, without a shift.','authority':'Authoritative source pixels; embedded text only a locator/comparison aid'},{'source_id':'PRIOR_S01','file':'S01_EXECUTION_BUNDLE.zip','sha256':hashlib.sha256(Path('/mnt/data/S01_EXECUTION_BUNDLE.zip').read_bytes()).hexdigest(),'bytes':Path('/mnt/data/S01_EXECUTION_BUNDLE.zip').stat().st_size,'physical_pages_fitz':'not applicable','owned_units':'recovery only','index_discrepancy':'not applicable','authority':'Prior unverified extraction; not source authority'}])
# JSON shape is the source checkpoint; its digest is independent of mtime/path.
canon=hashlib.sha256()
for n in sorted(PAGES):
 p=R/'transcription/pages'/f'AB01-PDF{n:04d}.json';canon.update(p.name.encode()+b'\0'+p.read_bytes())
checkpoint=canon.hexdigest()
receipt={'session':'S01','canonical_Nallino_checkpoint':'AB01-NALLINO-S01-v002','canonical_Nallino_sha256':checkpoint,'digest_algorithm':'sha256 over lexicographically sorted page basenames + NUL + exact JSON bytes','canonical_Arabic_checkpoint':None,'canonical_Arabic_sha256':None,'Arabic_checkpoint_disposition':'NOT_USED: no Arabic authorial Zij unit is owned by S01. Arabic quotations belong to Nallino apparatus.','accepted_Arabic_corrections':0,'target_languages_requested_in_current_instruction':[],'translation_artifacts':'none; no target-language translation silently inferred','language_sync':'No translations are promoted from unverified Arabic working-state material.'}
(R/'receipts/canonical_synchronization.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print('Ledgers:',len(A),'lines;',len(F),'math objects;',len(K),'key entries;',len(E),'printed addenda entries;',len(U),'open notes.')
