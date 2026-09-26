from work_helpers import *
repairs=[]
def replace(n,old,new,reason,evidence):
 p=R/f'transcription/pages/AB01-PDF{n:04}.json';d=json.loads(p.read_text());found=False
 for s in d['sections']:
  for l in s['lines']:
   if old in l['text']:
    before=l['text'];l['text']=before.replace(old,new);found=True
    repairs.append({'anchor':l['id'],'before':before,'after':l['text'],'reason':reason,'evidence':evidence})
 if not found:
  for sec in d['sections']:
   for l in sec['lines']:
    if new in l['text']:repairs.append({'anchor':l['id'],'before':l['text'].replace(new,old),'after':l['text'],'reason':reason,'evidence':evidence});found=True
  if not found:raise ValueError((n,old))
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
replace(105,'motum habant','motum habeant','Native source visibly has habeant; correction of working transcription, not an emendation of Nallino.','AB01-PDF0105-WORD-habeant')
crop(107,'G01',(446,685,467,698),'Damaged Arabic spelling at end of note11. Tight native crop excludes neighbouring Latin and the following full stop; no conjectural character encoding.')
crop(101,'G01',(390.5,677,420.5,690),'Numerator addend in Nallino note4: 59°3[damaged digit]′. Preserve the damaged character instead of resolving it by arithmetic.')
p=R/'transcription/pages/AB01-PDF0101.json';d=json.loads(p.read_text())
for s in d['sections']:
 for l in s['lines']:
  if s['role']=='notes_right' and '<m>' in l['text'] and '59' in l['text']:
   print('PATCH TARGET',l)
   old=l['text'];new=old.replace(r'59°\,36′',r'\text{\sourceglyph{AB01-PDF0101-G01}}').replace('59° 36′',r'\text{\sourceglyph{AB01-PDF0101-G01}}')
   if new==old:raise ValueError(old)
   l['text']=new;repairs.append({'anchor':l['id'],'before':old,'after':new,'reason':'Native source damage: do not silently resolve the second minute digit from the correct sum. Image-preserving encoding.','evidence':'AB01-PDF0101-FORMULA-proof'})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ledger=R/'ledgers/working_repairs.json';existing=json.loads(ledger.read_text());ledger.write_text(json.dumps(existing+repairs,ensure_ascii=False,indent=2)+'\n')
