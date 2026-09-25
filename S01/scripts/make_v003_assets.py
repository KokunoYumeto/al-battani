"""Preserve difficult printed clusters as native-image objects, without redrawing.
Source PDF placement is used only to find the decoded native pixel rectangle.
"""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
from native_proof_v003 import crop
from revision_helpers import read_rows,write_rows
R=Path(__file__).resolve().parents[1]
SPECS=[
(37,'G01',[373,353,409.5,370],'Ambiguous terminal digit in first page number; 100/106–102 retained as pixels'),
(40,'G01',[237,687.3,260,704],'Printed Persian word, complete consonant and upper-sign cluster'),
(70,'G02',[127,415,146,432],'Accusative orthography example; sign placement unnormalized'),
(70,'G03',[465,414,482,433],'Vocalized verbal example; hamzah and vowels retained'),
(70,'G04',[306,474.5,328,494],'Vocalized tilqa example; final and lower signs retained'),
(70,'G05',[386,491,399,507.5],'Vocalized final-vowel example; lower marks retained'),
(70,'G06',[271,474.5,290.5,493],'Vocalized talaqqa example; unnormalized printed signs'),
(70,'G07',[327.5,491,341.5,506.6],'Vocalized sammi example; lower vowel mark retained'),
(79,'G01',[335.5,491.5,357.5,506.5],'Left/original Arabic lemma in the historical XV, note 3 corrigendum'),
(79,'G02',[426,490,449,506.5],'Right/corrected Arabic lemma in the historical XV, note 3 corrigendum'),
(80,'G01',[119,456,177,470.5],'Left terrestri·um lemma: exact midline point retained without interpreting it'),
(84,'G01',[170,487,394,507.5],'First full Arabic verse line, with original right-to-left hemistich arrangement'),
(84,'G02',[170,508,394,526],'Second full Arabic verse line, with original right-to-left hemistich arrangement'),
(86,'G01',[178,279,222,294.5],'Ambiguous printed precipua/previpua title word; no conjectural regularization'),
]
records=[x for x in read_rows('figure_provenance') if x['object_id'] not in {f'AB01-PDF{n:04d}-{z}' for n,z,_,_ in SPECS}]
new=[]
for n,s,r,desc in SPECS:
 oid=f'AB01-PDF{n:04d}-{s}'
 assert not any(z['object_id']==oid for z in records),(oid,'exists')
 p=crop(n,r,oid+'_proof');m=json.loads(p.with_suffix('.json').read_text())
 raw=R/'source/raw'/f'{oid}-raw.png';pres=R/'source/presentation'/f'{oid}.png'
 shutil.copy2(p,raw);shutil.copy2(p,pres)
 im=Image.open(p)
 row={'object_id':oid,'master_pdf_page':n,'role':'NALLINO_APPARATUS','description':desc,'source_id':'SRC01','source_xref':m['xref'],'source_image_pixels':m['source_image_pixels'],'crop_box_pixels':m['crop_box_pixels'],'source_rect_pt':r,'pdf_rect_pt':r,'source_image_placement_rect_pt':m['placement_rect_pt'],'raw_path':str(raw.relative_to(R)),'presentation_path':str(pres.relative_to(R)),'presentation_pixels':list(im.size),'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'presentation_sha256':hashlib.sha256(pres.read_bytes()).hexdigest(),'source_dpi':'native decoded source image; no resampling','operations':'Decode authoritative PDF image; integer crop only. Raw crop and presentation PNG are byte-identical. No filtering, resampling, retouching or inpainting.','pixel_equivalence':True,'insertion_status':'INSERTED_IN_V003_READER','limitation':'Exact visual evidence retained; an image fallback is not a claimed character-level adjudication.'}
 records.append(row);new.append(row)
write_rows('figure_provenance',records)
write_rows('v003_native_glyph_assets',new)
# A contact sheet is QA evidence only, not the source or presentation derivative.
W=1250;Y=0;panels=[]
for z in new:
 im=Image.open(R/z['presentation_path']).convert('RGB');im.thumbnail((W-40,160))
 pan=Image.new('RGB',(W,max(65,im.height+45)),'white');d=ImageDraw.Draw(pan);d.text((10,5),z['object_id']+'  '+z['description'],fill='black');pan.paste(im,(15,32));panels.append(pan)
out=Image.new('RGB',(W,sum(p.height for p in panels)),'white')
for p in panels:out.paste(p,(0,Y));Y+=p.height
out.save(R/'qa/v003/native_glyphs_contact.png')
print('New objects',len(new))
