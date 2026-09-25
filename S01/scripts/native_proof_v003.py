"""Native-pixel proof crops. Search results are locators, not reading authority."""
from pathlib import Path
import fitz,io,math,json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1]
S=Path('/mnt/data/30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf')
def crop(n,rect,name):
 with fitz.open(S) as d:
  p=d[n-1];info=max(p.get_images(full=True),key=lambda t:t[2]*t[3]);xref=info[0];im=Image.open(io.BytesIO(d.extract_image(xref)['image']))
  pos=p.get_image_rects(xref)[0];sx,sy=im.width/pos.width,im.height/pos.height
  b=(math.floor((rect[0]-pos.x0)*sx),math.floor((rect[1]-pos.y0)*sy),math.ceil((rect[2]-pos.x0)*sx),math.ceil((rect[3]-pos.y0)*sy))
  assert 0<=b[0]<b[2]<=im.width and 0<=b[1]<b[3]<=im.height
  q=R/'qa/v003'/f'{name}.png';im.crop(b).save(q)
  rec={'page':n,'xref':xref,'pdf_rect_pt':list(rect),'crop_box_pixels':list(b),'placement_rect_pt':list(pos),'source_image_pixels':list(im.size),'path':str(q.relative_to(R)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'operations':['Native decoded image crop only; no resampling or retouching.']}
  (q.with_suffix('.json')).write_text(json.dumps(rec,indent=2)+'\n')
  return q
if __name__=='__main__':
 for n,rect,name in [(39,[264,325,315,345],'p39_alkekengi'),(50,[450,658,485,676],'p50_Balan'),(37,[369,350,425,372],'p37_106_102')]: print(crop(n,rect,name))
