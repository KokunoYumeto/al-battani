from pathlib import Path
import json,csv
R=Path('/mnt/data/AB01_S01_v002');rows=json.loads((R/'ledgers/transcription_repairs.json').read_text())
for n,old,new,ev,reason in [(20,'<glyph>AB01-PDF0020-G01</glyph>','والعداوة','source/raw/AB01-PDF0020-G01-raw.png','Native-pixel enlargement resolves the initial connected ayn; replace the image placeholder with the witnessed word, not the Latin gloss.'),(41,'<glyph>AB01-PDF0041-G01</glyph>','ثبت','source/raw/AB01-PDF0041-G01-raw.png','Native-pixel enlargement resolves three points of tha, the point of ba, and final ta; no vowel is supplied.')]:
 p=R/'transcription/pages'/f'AB01-PDF{n:04d}.json';d=json.loads(p.read_text());ls=[l for s in d['sections'] for l in s['lines'] if old in l['text']];assert len(ls)==1
 l=ls[0];l['text']=l['text'].replace(old,new);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 rows.append({'repair_id':f'S01-R{len(rows)+1:03d}','page':n,'line_id':l['id'],'before':old,'after':new,'reason':reason,'evidence':ev,'class':'resolved_encoding_after_native_pixel_replay','confidence':'high','canonical_Arabic_change':'none','historical_erratum_applied':'no'})
(R/'ledgers/transcription_repairs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (R/'ledgers/transcription_repairs.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
