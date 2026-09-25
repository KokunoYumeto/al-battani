"""Record source-checked successor changes; never edit the frozen predecessor."""
from pathlib import Path
import json,hashlib,datetime,csv
R=Path(__file__).resolve().parents[1]
def write_rows(name, rows):
 p=R/'ledgers'/f'{name}.json';p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 fields=list(dict.fromkeys(k for x in rows for k in x))
 with (R/'ledgers'/f'{name}.tsv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n');w.writeheader()
  for x in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x.items()})
def read_rows(name):
 p=R/'ledgers'/f'{name}.json';return json.loads(p.read_text()) if p.exists() else []
def change(lid,old,new,evidence,reason,category='digital_transcription',confidence='high'):
 n=int(lid.split('-')[1][3:]);p=R/f'transcription/pages/AB01-PDF{n:04d}.json';d=json.loads(p.read_text())
 l=next(l for s in d['sections'] for l in s['lines'] if l['id']==lid)
 assert l['text'].count(old)==1,(lid,old,l['text'])
 before=l['text'];l['text']=before.replace(old,new,1)
 records=read_rows('v003_changes');rid=f'S01-R3-{len(records)+1:03d}'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 records.append({'change_id':rid,'line_id':lid,'master_pdf_page':n,'before':before,'after':l['text'],'old_substring':old,'new_substring':new,'category':category,'reason':reason,'confidence':confidence,'evidence':evidence,'source_authority':'SRC01 native page pixels; no outside text substituted','source_sha256':'544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297','canonical_Arabic_changed':False,'status':'ACCEPTED_IN_V003_PRODUCTION_NOT_INDEPENDENTLY_AUDITED'})
 write_rows('v003_changes',records);print(rid,lid,old,'=>',new)
def review(sheet,ids,decision='Source snippets inspected; v002 retained except explicitly registered successor changes.',qualifier='Visual reread by current producing assistant; not an independent audit.'):
 rows=read_rows('v003_recovered_proof_review');assert not any(x['sheet']==sheet for x in rows)
 p=R/'history/interrupted_reread/qa'/sheet;assert p.is_file()
 rows.append({'sheet':sheet,'candidate_ids':ids,'image_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'decision':decision,'qualification':qualifier})
 write_rows('v003_recovered_proof_review',rows)
