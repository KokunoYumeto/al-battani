from pathlib import Path
import fitz,json
R=Path('/mnt/data/AB01_S01_v002'); D=fitz.open('/mnt/data/30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf')
items=[(10,(160,350,425,388),'10_name'),(13,(160,705,450,745),'13_imprint'),(17,(320,724,545,741),'17_reference'),(20,(85,200,535,330),'20_arabic'),(39,(104,142,548,195),'39_names'),(40,(74,600,295,740),'40_terms'),(43,(105,118,550,138),'43_tacite'),(43,(345,310,550,372),'43_transliteration'),(50,(305,558,546,735),'50_notes'),(51,(105,120,545,480),'51_body'),(59,(96,275,550,345),'59_quote'),(62,(82,505,546,595),'62_quote'),(80,(65,452,380,475),'80_lemma'),(82,(64,161,275,186),'82_lemma'),(85,(128,111,550,158),'85_fractions')]
rec=[]
for n,b,name in items:
 f=R/'qa'/('proof_'+name+'.png'); D[n-1].get_pixmap(matrix=fitz.Matrix(4.5,4.5),clip=fitz.Rect(b)).save(str(f)); rec.append({'page':n,'pdf_rect':b,'path':str(f.relative_to(R)),'scale':4.5})
(R/'receipts/proof_crop_coordinates.json').write_text(json.dumps(rec,indent=2)+'\n')
