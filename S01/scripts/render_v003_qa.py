from pathlib import Path
import fitz,json,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];Q=R/'qa/v003/final';Q.mkdir(parents=True,exist_ok=True)
D=fitz.open(R/'pdf/S01_NALLINO_SOURCE_v003.pdf')
selected={1,2,3,4,5,6,8,9,13,17,24,28,30,31,32,33,34,38,41,43,47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,64,66,69,70,71,72,73,74,75,76,77,78,79,80}
records=[]
thumbs=[]
for i,p in enumerate(D):
 pix=p.get_pixmap(matrix=fitz.Matrix(0.55,.55),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((290,420));thumbs.append(im)
 if i+1 in selected:
  dest=Q/f'reader_{i+1:03d}.png';p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(dest)
  records.append({'artifact':'reader','page':i+1,'file':str(dest.relative_to(R)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'RENDERED_AWAITING_VISUAL_INSPECTION'})
for a in range(0,len(D),12):
 b=min(a+12,len(D));sheet=Image.new('RGB',(4*310,3*455),'white');draw=ImageDraw.Draw(sheet)
 for k,im in enumerate(thumbs[a:b]):
  x=(k%4)*310;y=(k//4)*455;draw.text((x+10,y+5),f'Reader {a+k+1:03d}',fill='black');sheet.paste(im,(x+10,y+25))
 sheet.save(Q/f'contact_{a+1:03d}-{b:03d}.png')
C=fitz.open(R/'pdf/S01_CRITICAL_NOTES_v003.pdf')
for i,p in enumerate(C):
 dest=Q/f'critical_{i+1:02d}.png';p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(dest)
 records.append({'artifact':'critical_notes','page':i+1,'file':str(dest.relative_to(R)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'RENDERED_AWAITING_VISUAL_INSPECTION'})
(R/'receipts/render_inventory_v003.json').write_text(json.dumps(records,indent=2)+'\n')
print(len(D),'reader pages;',len(C),'critical pages;',len(records),'detail renders')
