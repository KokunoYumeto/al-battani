"""Synchronize derived ledgers with the reviewed JSON; do not alter historical readings."""
from pathlib import Path
import json,re,hashlib,collections
from revision_helpers import read_rows,write_rows
R=Path(__file__).resolve().parents[1]
P={};L={}
notes=read_rows('critical_findings');changes=read_rows('v003_changes')
for p in sorted((R/'transcription/pages').glob('*.json')):
 d=json.loads(p.read_text());n=d['master_pdf_page']
 d['details'].pop('open_reading_notes',None)
 d['details']['reading_note_dispositions']=[{'id':x['apparatus_id'],'status':x['status']} for x in notes if x['source_anchor']==d['anchor']]
 d['details']['v003_change_ids']=[x['change_id'] for x in changes if x['master_pdf_page']==n]
 d['details']['verification_limit']='Inherited v002 first-pass source replay, followed by v003 targeted reread. No independent cold philological audit has been performed.'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');P[n]=d
 for s in d['sections']:
  for l in s['lines']:L[l['id']]=(n,s['role'],l['text'])
a=read_rows('line_alignment')
for x in a:
 x['text']=L[x['line_id']][2]
 x['locator_version_note']='Coordinates inherited from v002 locator calculation; current text synchronized to v003. Image fallback coordinates are separately exact in the figure ledger.'
write_rows('line_alignment',a)
f=read_rows('formula_provenance');mathproof=[]
for x in f:
 text=L[x['line_id']][2];assert x['latex'] in re.findall(r'<m>(.*?)</m>',text)
 n=x['master_pdf_page']
 if n in (56,57,42,82,85):ev=f'history/interrupted_reread/qa/source_page_{n:04d}.png'
 elif n in (25,36,43):ev='history/interrupted_reread/qa/math_other_01-04.png'
 elif n==70:ev='history/interrupted_reread/qa/math_other_05-08.png'
 elif n==83:ev='history/interrupted_reread/qa/math_other_09-12.png'
 else:raise ValueError(n)
 x['v003_reread']='Source appearance compared with stored notation by the producing assistant; no mathematical emendation.'
 x['source_reread_evidence']=ev
 mathproof.append({'object_id':x['object_id'],'line_id':x['line_id'],'evidence':ev,'decision':'Existing notation retained','responsibility':'Current producing assistant; not independent cold audit'})
write_rows('formula_provenance',f);write_rows('v003_formula_reread',mathproof)
num=[]
for lid,(n,sec,t) in L.items():
 no_glyph=re.sub(r'<glyph>.*?</glyph>','',t)
 ns=re.findall(r'\d+(?:[.,]\d+)?(?:[°′″‴]|<sup>.*?</sup>)?',no_glyph)
 if ns:num.append({'line_id':lid,'master_pdf_page':n,'literal_numeric_tokens':ns,'context':t,'index_status':'AUTOMATIC_LITERAL_INDEX; source-image IDs excluded. Not a semantic quantity inventory or numerical correction.'})
write_rows('numeric_literal_index',num)
e=read_rows('printed_corrigenda_routing')
for x in e:
 x['source_entry_lines']=[L[z][2] for z in x['source_line_ids']]
 assert x['routing_status']=='REGISTERED_NOT_APPLIED'
write_rows('printed_corrigenda_routing',e)
k=read_rows('transliteration_key')
for x in k:x['source_text']=L[x['line_id']][2]
write_rows('transliteration_key',k)
t=read_rows('table_provenance')
for x in t:
 for z,v in x.items():
  if isinstance(v,str):x[z]=v.replace('v002','v003')
write_rows('table_provenance',t)
pd=read_rows('page_disposition')
for x in pd:
 x.pop('open_notes',None)
 x['reading_note_dispositions']=[{'id':y['apparatus_id'],'status':y['status']} for y in notes if y['source_anchor']==x['anchor']]
 x['v003_change_count']=sum(z['master_pdf_page']==x['master_pdf_page'] for z in changes)
 if x['owned'] and x['master_pdf_page'] in P and x['kind']!='intrinsic_blank_verso':x['disposition']='First-pass transcription inherited from v002; v003 targeted source repairs and exact-image dispositions incorporated. Independent cold source audit outstanding.'
write_rows('page_disposition',pd)
old=json.loads((R/'history/v002/ledgers/transcription_repairs.json').read_text())
for x in old:x['introduced_in']='v002'
for x in changes:
 old.append({'repair_id':x['change_id'],'page':x['master_pdf_page'],'line_id':x['line_id'],'before':x['before'],'after':x['after'],'reason':x['reason'],'evidence':x['evidence'],'class':x['category'],'confidence':x['confidence'],'canonical_Arabic_change':'none','historical_erratum_applied':'no','introduced_in':'v003'})
write_rows('transcription_repairs',old)
se=read_rows('source_evidence');se=[x for x in se if x['source_id'] not in ('V002_RELEASE','INTERRUPTED_REREAD')]
se.append({'source_id':'V002_RELEASE','file':'AB01_S01_v002.zip','bytes':121220563,'sha256':'46152dbd96c89b587083a32472e3d05d2b6833a748489c462b140983c52adf08','authority':'Frozen prior digital candidate, not source authority','verification':'ZIP CRC and all 535 manifest entries verified at recovery; full receipt workspace_recovery.json'})
se.append({'source_id':'INTERRUPTED_REREAD','file':'history/interrupted_reread/RECOVERY_INVENTORY.json','authority':'157 recovered proof images only; no revised text or correction ledger found. Captions not reading authority.','verification':'Recovery byte hashes and inventory retained.'})
write_rows('source_evidence',se)
h=hashlib.sha256()
for p in sorted((R/'transcription/pages').glob('*.json')):h.update(p.name.encode()+b'\0'+p.read_bytes())
sync={'session':'S01','canonical_Nallino_checkpoint':'AB01-NALLINO-S01-v003-CANDIDATE','canonical_Nallino_sha256':h.hexdigest(),'digest_algorithm':'sha256 over sorted page basenames + NUL + exact JSON bytes','canonical_Arabic_checkpoint':None,'canonical_Arabic_sha256':None,'Arabic_checkpoint_disposition':'NOT_USED: S01 owns Nallino apparatus, not an Arabic authorial Zij unit. Intrinsic quotations do not constitute a new Arabic canonical edition.','accepted_Arabic_corrections':0,'target_languages_requested_in_current_instruction':[],'translation_artifacts':[],'language_sync':'No new target-language translation generated; no Arabic canonical corrections applied.','predecessor':'AB01-NALLINO-S01-v002','predecessor_pages_sha256':'93fdc19b0917d87ec1e42a27296150c857b47f63984312793b4cc677c0c2531e','release_gate':'INDEPENDENT_COLD_SOURCE_AUDIT_OUTSTANDING'}
(R/'receipts/canonical_synchronization.json').write_text(json.dumps(sync,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'lines':len(L),'pages':len(P),'changes':len(changes),'changed_lines':len({x['line_id'] for x in changes}),'changed_pages':len({x['master_pdf_page'] for x in changes}),'formulas':len(f),'key_rows':len(k),'printed_addenda':len(e),'note_statuses':dict(collections.Counter(x['status'] for x in notes)),'nallino_checkpoint_sha256':h.hexdigest()},indent=2))
