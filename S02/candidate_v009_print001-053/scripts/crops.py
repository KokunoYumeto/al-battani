from pathlib import Path
import fitz,json,math,hashlib,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf'
def crop(n,ident,rect,kind='proof',role='NALLINO_APPARATUS'):
 doc=fitz.open(SOURCE);p=doc[n-1];info=max(p.get_image_info(xrefs=True),key=lambda a:a['width']*a['height']);pm=fitz.Pixmap(doc,info['xref'])
 if pm.n not in (1,3):pm=fitz.Pixmap(fitz.csRGB,pm)
 im=Image.frombytes('L' if pm.n==1 else 'RGB',(pm.width,pm.height),pm.samples);a,b,c,d=info['bbox'];sx=pm.width/(c-a);sy=pm.height/(d-b)
 box=[max(0,math.floor((rect[0]-a)*sx)),max(0,math.floor((rect[1]-b)*sy)),min(pm.width,math.ceil((rect[2]-a)*sx)),min(pm.height,math.ceil((rect[3]-b)*sy))]
 fragment=im.crop(box);asset=f'AB01-PDF{n:04}-{ident}';raw=ROOT/f'source/raw/{asset}-raw.png';fragment.save(raw);pre=ROOT/f'source/presentation/{asset}.png';shutil.copy2(raw,pre)
 H=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
 ob={'id':asset,'source':'SRC01','master_pdf_page':n,'printed_page':n-89,'kind':kind,'role':role,'source_xref':info['xref'],'source_image_pdf_bbox':list(info['bbox']),'source_image_size':[pm.width,pm.height],'requested_pdf_rect':rect,'native_pixel_rect':box,'dimensions':list(fragment.size),'raw_path':raw.relative_to(ROOT).as_posix(),'presentation_path':pre.relative_to(ROOT).as_posix(),'raw_sha256':H(raw),'presentation_sha256':H(pre),'operations':['decode controlling source image','integer native-pixel rectangle extraction','byte-identical PNG presentation copy'],'visual_inspection':'PENDING'}
 meta=ROOT/'ledgers/new_visual_objects.json';obs=json.loads(meta.read_text()) if meta.exists() else [];obs=[x for x in obs if x['id']!=asset]+[ob];meta.write_text(json.dumps(obs,indent=2)+'\n');return ob
if __name__=='__main__':
 for n,rect in [(133,[111,438,314,632]),(135,[118,346,330,568]),(136,[63,483,299,649])]:crop(n,'F01',rect,'diagram','NALLINO_TRANSLATION')
 crop(134,'PROOF-GREEK',[61,684,276,756]);crop(134,'PROOF-SECET',[352,233,470,255]);crop(135,'PROOF-N15',[347,669,487,685])
