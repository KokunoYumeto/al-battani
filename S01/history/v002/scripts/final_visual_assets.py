"""Render the final reader for inspection; no OCR or image retouching."""
from pathlib import Path
import json,fitz,subprocess,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
pdf=R/'pdf/S01_NALLINO_SOURCE_v002.pdf'; d=fitz.open(pdf)
source=[None,2,10,12,13,14]+list(range(16,90))
assert len(source)==len(d)==80
mapping=[{'edition_page':i+1,'master_pdf_page':n,'anchor':f'AB01-PDF{n:04d}' if n else None,'role':'NALLINO_APPARATUS' if n else 'MODERN_EDITORIAL'} for i,n in enumerate(source)]
(R/'receipts/output_page_map.json').write_text(json.dumps(mapping,indent=2)+'\n')
Q=R/'qa/final';Q.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
thumbs=[]
for i,p in enumerate(d):
 pix=p.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False)
 im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
 im.thumbnail((290,422))
 tile=Image.new('RGB',(310,462),'white');tile.paste(im,((310-im.width)//2,31))
 txt=f'Reader {i+1:02d} / '+(f'SRC {source[i]:04d}' if source[i] else 'editorial notice')
 ImageDraw.Draw(tile).text((10,6),txt,fill='black',font=font)
 thumbs.append(tile)
for start in range(0,80,12):
 group=thumbs[start:start+12]; canvas=Image.new('RGB',(1240,1386),'#dddddd')
 for j,tile in enumerate(group):canvas.paste(tile,((j%4)*310,(j//4)*462))
 canvas.save(Q/f'contact_{start+1:02d}-{min(start+12,80):02d}.jpg',quality=92)
# Detailed actual reader proof samples. These are rendering derivatives, not raw evidence.
samples=[1,2,4,7,8,13,47,48,61,63,64,65,70,73,75,80]
for n in samples:
 p=d[n-1];p.get_pixmap(matrix=fitz.Matrix(2.3,2.3),alpha=False).save(Q/f'reader_{n:03d}.png')
# At least one final renderer is Poppler, independent of the fitz proof renderer.
cmd=['pdftoppm','-f','80','-l','80','-scale-to','1800','-png','-singlefile',str(pdf),str(Q/'poppler_reader_080')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
(R/'receipts/final_render_generation.json').write_text(json.dumps({'reader_pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'reader_pages':80,'contact_sheet_pages':list(range(1,81)),'detailed_reader_pages':samples,'fitz_scale':2.3,'poppler_command':cmd,'rendering_is_not_inspection':True},indent=2)+'\n')
print('Generated seven contact sheets, sixteen detailed samples, and Poppler final-page proof.')
