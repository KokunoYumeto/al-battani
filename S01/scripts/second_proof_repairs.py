from pathlib import Path
import json,csv
R=Path('/mnt/data/AB01_S01_v002');rows=json.loads((R/'ledgers/transcription_repairs.json').read_text())
items=[
(22,'<gr>Βκτάνῃ</gr>','<gr>Βιτάνῃ</gr>','qa/22_Greek_b.png','Printed second letter is iota, not kappa.','transcription_error'),
(42,'Ahābā','Ahăbā','qa/42_Ahaba.png','Breve over the first a, macron over the last a.','transcription_error'),
(72,'ḏ, ǧ, ġ, ch, š, ḳ','ḏ, ǧ, ġ, ch, š, ṯ','qa/72_suter_key.png','Last Suter character is t with line below, not k with dot below.','transcription_error'),
(70,'<ar>نهى</ar>','<ar>تهى</ar>','qa/70_prepared.png','Initial letter has two dots: ta, not nun.','transcription_error'),
(70,'<ar>اختفاوه</ar>','<ar>اختفاؤه</ar>','qa/70_orthography_new.png','The printed regular form carries hamza on waw; preserve the distinction being discussed.','transcription_error'),
(70,'<ar>اٙ</ar>','<glyph>AB01-PDF0070-G01</glyph>','qa/70_special.png','Withdraw an unsupported special-mark encoding; display exact sign instead.','unresolved_encoding_image_fallback'),
(20,'الدَّيْن والمداوة والمرض','الدَّيْن <glyph>AB01-PDF0020-G01</glyph> والمرض','qa/20_clause_final.png','Do not settle the initial consonant from the Latin gloss; preserve exact source word.','unresolved_encoding_image_fallback'),
(41,'وانما ثبت اماكن','وانما <glyph>AB01-PDF0041-G01</glyph> اماكن','qa/41_arabic_full.png','Preserve the small ambiguous verb as exact source pixels.','unresolved_encoding_image_fallback')]
for n,old,new,ev,reason,cls in items:
 p=R/'transcription/pages'/f'AB01-PDF{n:04d}.json';d=json.loads(p.read_text());ls=[l for s in d['sections'] for l in s['lines'] if old in l['text']];assert len(ls)==1,(n,old)
 l=ls[0];l['text']=l['text'].replace(old,new);d['source_status']='SOURCE_REPLAYED_WITH_DOCUMENTED_PROOF_REPAIRS';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 rows.append({'repair_id':f'S01-R{len(rows)+1:03d}','page':n,'line_id':l['id'],'before':old,'after':new,'reason':reason,'evidence':ev,'class':cls,'confidence':'high' if cls=='transcription_error' else 'encoding unresolved; image exact','canonical_Arabic_change':'none','historical_erratum_applied':'no'})
(R/'ledgers/transcription_repairs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (R/'ledgers/transcription_repairs.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
print(len(rows),'repairs/encoding withdrawals')
