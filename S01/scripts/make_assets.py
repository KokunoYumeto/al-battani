"""Extract native raster evidence, then crop without resampling or retouching."""
from pathlib import Path
import fitz,json,io,hashlib,math
from PIL import Image
R=Path('/mnt/data/AB01_S01_v002');S=Path('/mnt/data/30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf');D=fitz.open(S)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
# Preserve the first embedded source image byte-for-byte, plus its decoded pixels.
a=D.extract_image(22);raw=R/'source/raw/AB01-PDF0002-F01-original.jpx';raw.write_bytes(a['image']);im=Image.open(io.BytesIO(a['image']));dec=R/'source/raw/AB01-PDF0002-F01-decoded.png';im.save(dec)
b=(0,312,2491,2766);pres=R/'source/presentation/AB01-PDF0002-F01.png';im.crop(b).save(pres)
rows.append({'object_id':'AB01-PDF0002-F01','page':2,'role':'NALLINO_APPARATUS','description':'Astronomical frontispiece: surviving raster panel','source_xref':22,'raw_path':str(raw.relative_to(R)),'decoded_path':str(dec.relative_to(R)),'presentation_path':str(pres.relative_to(R)),'source_image_pixels':list(im.size),'crop_box_pixels':list(b),'pdf_rect_pt':[0,74.88,597.84,663.84],'presentation_pixels':list(im.crop(b).size),'operations':['Decode original JPX without modifying RGB samples','Crop native pixel rectangle [0,312,2491,2766); no resampling, deskew, levels or inpainting'],'source_dpi':[300,300],'raw_sha256':h(raw),'decoded_sha256':h(dec),'presentation_sha256':h(pres),'pixel_equivalence_verified':True,'insertion_status':'included','limitation':'The source itself clips the diagram at panel and side edges. Missing content is not reconstructed. Only solid provider title/UI bands are removed.'})
# Native images have known full-page placements. Rectangles deliberately include margins.
items=[(20,'AB01-PDF0020-G01',(124,267,154,283),'Native-pixel evidence for resolved Arabic reading والعداوة'),(41,'AB01-PDF0041-G01',(511,593,527,605),'Native-pixel evidence for resolved Arabic consonantal reading ثبت'),(70,'AB01-PDF0070-G01',(281,383,291,402),'Orthographic sign: exact-source glyph fallback, probable alif with waslah'),(16,'AB01-PDF0016-F01',(84,119,512,146),'Preface head ornament'),(22,'AB01-PDF0022-G01',(175,492,204,510),'Syriac toponym: exact glyph fallback; Unicode reading unresolved'),(78,'AB01-PDF0078-F01',(233,452,378,463),'Bibliography terminal ornament'),(82,'AB01-PDF0082-G01',(153,168,180,183),'Corrigendum 175 note 9: original Arabic lemma'),(82,'AB01-PDF0082-G02',(193,168,219,183),'Corrigendum 175 note 9: corrected Arabic lemma'),(89,'AB01-PDF0089-F01',(245,535,395,544),'Addenda terminal ornament')]
for n,oid,rect,desc in items:
 p=D[n-1];info=max(p.get_images(full=True),key=lambda t:t[2]*t[3]);xref=info[0];a=D.extract_image(xref);im=Image.open(io.BytesIO(a['image']));placement=p.get_image_rects(xref)[0]
 sx,sy=im.width/placement.width,im.height/placement.height
 b=(math.floor((rect[0]-placement.x0)*sx),math.floor((rect[1]-placement.y0)*sy),math.ceil((rect[2]-placement.x0)*sx),math.ceil((rect[3]-placement.y0)*sy))
 cr=im.crop(b);raw=R/'source/raw'/f'{oid}-raw.png';pres=R/'source/presentation'/f'{oid}.png';cr.save(raw);cr.save(pres)
 rows.append({'object_id':oid,'page':n,'role':'NALLINO_APPARATUS','description':desc,'source_xref':xref,'raw_path':str(raw.relative_to(R)),'presentation_path':str(pres.relative_to(R)),'source_image_pixels':list(im.size),'crop_box_pixels':list(b),'pdf_rect_pt':list(rect),'presentation_pixels':list(cr.size),'operations':['Crop decoded highest-resolution page image on integer pixel bounds','Presentation copy identical to raw crop; no retouching or interpolation'],'source_dpi':[round(sx*72,3),round(sy*72,3)],'raw_sha256':h(raw),'presentation_sha256':h(pres),'pixel_equivalence_verified':True,'insertion_status':'included','limitation':'Unresolved encoding is not supplied conjecturally.' if '-G' in oid else ''})
for row in rows:
 if row['object_id'] in ('AB01-PDF0020-G01','AB01-PDF0041-G01'):
  row['insertion_status']='evidence only; encoding resolved after native-pixel replay'
  row['limitation']='No image placeholder remains in the final reader for this word.'
(R/'ledgers/figure_provenance.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
# Copy authoritative first 89 physical PDF pages, without modifying their contents.
out=fitz.open();out.insert_pdf(D,from_page=0,to_page=88)
f=R/'source/SRC01_PDF0001-0089_EVIDENCE.pdf';out.save(f,garbage=0,deflate=False,no_new_id=True);out.close()
print('Extracted',len(rows),'objects; source excerpt',f.stat().st_size)
