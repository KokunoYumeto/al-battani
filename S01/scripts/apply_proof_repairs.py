from pathlib import Path
import json,csv
R=Path('/mnt/data/AB01_S01_v002')
repairs=[
(18,'Muslimun','Muslimum','qa/page_0018.png','Final m in accusative adjective; direct scan replay.'),
(19,'Muslimun','Muslimum','qa/page_0019.png','Final m in accusative adjective; direct scan replay.'),
(19,'eius erga excellentiam','eius excellentiam','qa/page_0019.png','Remove an unwitnessed extra word introduced in first-pass transcription.'),
(17,'p. ccxlii','p. cccxlii','qa/proof_17_reference.png','Reference has three initial C characters.'),
(24,'1901, p. 409-06','1901, p. 400-06','qa/page_0024.png','Bibliographical page reference: third digit is zero.'),
(39,'Alchaīsi','Alcharsi','qa/proof_39_names.png','Printed transliteration reads Alcharsi.'),
(40,'filamenla','filamenta','qa/proof_40_terms.png','Printed t, not l.'),
(43,'Tacile','Tacite','qa/proof_43_tacite.png','Printed t, not l.'),
(43,'ba‘al hsh-kěnāphim','ba‘al hak-kěnāphīm','qa/proof_43_transliteration.png','Resolve first-pass transliteration against enlarged type.'),
(50,'(cladens igitur','(lactans igitur','qa/proof_50_notes.png','Printed word is lactans.'),
(51,'thalīs','thalis','qa/proof_51_body.png','No macron in this portion of zenithalis.'),
(59,'[leg. Cinenī]','[leg. Cineni]','qa/proof_59_quote.png','No macron over final i.'),
(59,'experimēnti','experimenti','qa/proof_59_experimenti.png','No macron in the printed reading.'),
(62,'partiāris','partiaris','qa/proof_62_quote.png','No macron in the printed reading.'),
(62,'qne','que','qa/proof_62_que.png','Printed u, not n.'),
(85,r'<m>{}^1\!/_{37}</m>',r'<m>{}^1\!/_{87}</m>','qa/proof_85_fractions.png','Venus fraction denominator is 87, not 37; no historical value normalized.'),
]
rows=[]
for page,old,new,ev,reason in repairs:
 p=R/'transcription/pages'/f'AB01-PDF{page:04d}.json'; ob=json.loads(p.read_text())
 hits=[l for s in ob['sections'] for l in s['lines'] if old in l['text']]
 if len(hits)!=1:
  print('STOP',page,repr(old),'hits',len(hits)); raise SystemExit(1)
 l=hits[0]; before=l['text']; l['text']=before.replace(old,new,1)
 ob['source_status']='SOURCE_REPLAYED_WITH_DOCUMENTED_PROOF_REPAIRS'
 p.write_text(json.dumps(ob,ensure_ascii=False,indent=2)+'\n')
 rows.append({'repair_id':f'S01-R{len(rows)+1:03d}','page':page,'line_id':l['id'],'before':old,'after':new,'reason':reason,'evidence':ev,'class':'transcription_error','confidence':'high','canonical_Arabic_change':'none','historical_erratum_applied':'no'})
(R/'ledgers/transcription_repairs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (R/'ledgers/transcription_repairs.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
print('Repairs',len(rows))
