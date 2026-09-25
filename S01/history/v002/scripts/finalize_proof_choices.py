from pathlib import Path
import json,csv
R=Path('/mnt/data/AB01_S01_v002'); rp=R/'ledgers/transcription_repairs.json';rows=json.loads(rp.read_text())
for n,old,new,reason,ev,cls in [
(74,'texle arabe','texte arabe','Printed French title reads texte.','qa/page_0074.png','transcription_error'),
(82,'<ar>واللول</ar> l. <ar>واللولوا</ar>.','<glyph>AB01-PDF0082-G01</glyph> l. <glyph>AB01-PDF0082-G02</glyph>.','Withdraw unreliable first-pass Arabic encodings; retain both exact source glyphs rather than supply a conjectural correction.','qa/82_corrected_pair.png','unresolved_encoding_image_fallback')]:
 p=R/'transcription/pages'/f'AB01-PDF{n:04d}.json'; ob=json.loads(p.read_text());ls=[l for s in ob['sections'] for l in s['lines'] if old in l['text']]; assert len(ls)==1,(n,old)
 l=ls[0];l['text']=l['text'].replace(old,new);p.write_text(json.dumps(ob,ensure_ascii=False,indent=2)+'\n')
 rows.append({'repair_id':f'S01-R{len(rows)+1:03d}','page':n,'line_id':l['id'],'before':old,'after':new,'reason':reason,'evidence':ev,'class':cls,'confidence':'high' if n==74 else 'encoding unresolved; image exact','canonical_Arabic_change':'none','historical_erratum_applied':'no'})
p=R/'transcription/pages/AB01-PDF0020.json';o=json.loads(p.read_text());o['details']['uncertainties']=['The initial letters in the Arabic word provisionally encoded المداوة remain uncertain; العداوة is an alternative. No correction is inferred from the Latin translation inimicitia.'];p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
rp.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (R/'ledgers/transcription_repairs.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
