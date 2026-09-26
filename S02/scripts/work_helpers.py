"""Local source reading helpers; no OCR and no conjectural text generation."""
from pathlib import Path
import fitz, json, re, hashlib, csv, io
from PIL import Image
R=Path(__file__).resolve().parents[1]
MASTER=R.parent/'30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf'
def source(n):
 d=fitz.open(MASTER); return d,n-1

def preview(n):
 d,i=source(n); p=d[i]
 clip=fitz.Rect(40,70,p.rect.width-35,p.rect.height-65) if n!=90 else fitz.Rect(40,197,p.rect.width-35,770)
 p.get_pixmap(dpi=180,clip=clip).save(R/f'qa/source/reading_{n:04}.png')
 return str(R/f'qa/source/reading_{n:04}.png')

def save_page(n,text,kind='text',notes=''):
 """Save fully hand-adjudicated page markup. Sections separated by [body]/[notes_left]/[notes_right]."""
 parts=re.split(r'^\[(body|notes_left|notes_right|notes_full|margins)\]\s*$',text,flags=re.M)
 sections=[]
 for role,txt in zip(parts[1::2],parts[2::2]):
  lines=[]
  for i,t in enumerate(txt.strip().splitlines(),1):
   if not t.strip(): continue
   lines.append({'id':f'AB01-PDF{n:04}-{role}-L{len(lines)+1:03}','text':t.rstrip()})
  sections.append({'role':role,'authorship':'NALLINO_TRANSLATION' if role=='body' else 'NALLINO_APPARATUS','lines':lines})
 data={'anchor':f'AB01-PDF{n:04}','master_pdf_page':n,'printed_page':n-89,'kind':kind,'source':'SRC01','status':'SOURCE_READ_FIRST_PASS','method':'Manual transcription/adjudication against rendered source pixels; embedded text used only as a comparison aid. No new OCR.','editorial_note':notes,'sections':sections}
 (R/f'transcription/pages/AB01-PDF{n:04}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def crop(n,obj,rect,description,role='NALLINO_APPARATUS',mode='glyph'):
 """Lossless native-image crop using a PDF-point region. No interpolated resampling."""
 d,i=source(n);p=d[i]
 imgs=p.get_image_info(xrefs=True)
 main=max(imgs,key=lambda im:im['width']*im['height'])
 xref=main['xref'];pix=fitz.Pixmap(d,xref)
 im=Image.frombytes('L' if pix.n==1 else 'RGB',(pix.width,pix.height),pix.samples)
 box=fitz.Rect(main['bbox']); r=fitz.Rect(rect)
 import math
 px=[max(0,math.floor((r.x0-box.x0)*im.width/box.width)),max(0,math.floor((r.y0-box.y0)*im.height/box.height)),min(im.width,math.ceil((r.x1-box.x0)*im.width/box.width)),min(im.height,math.ceil((r.y1-box.y0)*im.height/box.height))]
 out=im.crop(px); oid=f'AB01-PDF{n:04}-{obj}'
 raw=R/f'source/raw/{oid}-raw.png';pre=R/f'source/presentation/{oid}.png';out.save(raw);pre.write_bytes(raw.read_bytes())
 rec={'id':oid,'master_pdf_page':n,'printed_page':n-89,'role':role,'kind':mode,'description':description,'source_xref':xref,'source_image_size':[im.width,im.height],'source_image_pdf_bbox':list(box),'requested_pdf_rect':list(r),'native_pixel_rect':px,'dimensions':list(out.size),'operations':['decode authoritative native image','integer-bounded lossless crop','presentation copy byte-identical to raw crop'],'raw_path':str(raw.relative_to(R)),'presentation_path':str(pre.relative_to(R)),'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'presentation_sha256':hashlib.sha256(pre.read_bytes()).hexdigest()}
 ledger=R/'ledgers/visual_objects.json'; rows=json.loads(ledger.read_text()) if ledger.exists() else [];rows=[x for x in rows if x['id']!=oid];rows.append(rec);ledger.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 return oid

def extraction(n):
 d,i=source(n);return d[i].get_text(sort=True)
if __name__=='__main__':
 import sys
 for s in sys.argv[1:]:
  n=int(s);print('\n=====MASTER',n,'PRINT',n-89,'=====\n',extraction(n));print(preview(n))
