from work_helpers import R,crop
import json
crop(96,'T01',(130,451,465,766),'Multiplication lookup grid, including exterior A/B/B labels','NALLINO_TRANSLATION','table')
crop(97,'T01',(150,401,487,713),'Division lookup grid, including exterior A/B/D labels','NALLINO_TRANSLATION','table')
crop(96,'T01-R04-C10',(401,550,416,562),'Damaged second digit in the cell at row 4 column 10; do not supply the mathematically expected value','NALLINO_TRANSLATION','table_cell_glyph')
rows96='''grad.|min.|2|3|4|5|6|7|8|9|10
min.|2|3|4|5|6|7|8|9|10|11
2|3|4|5|6|7|8|9|10|11|12
3|4|5|6|7|8|9|10|11|[IMAGE]|13
4|5|6|7|8|9|10|11|12|13|14
5|6|7|8|9|10|11|12|13|14|15
6|7|8|9|10|11|12|13|14|15|16
7|8|9|10|11|12|13|14|15|16|17
8|9|10|11|12|13|14|15|16|17|18
9|10|11|12|13|14|15|16|17|18|19
10|11|12|13|14|15|16|17|18|19|20'''
rows97='''grad.|min.|2|3|4|5|6|7|8|9|10
min.|grad.|min.|2|3|4|5|6|7|8|9
2|min.|grad.|min.|2|3|4|5|6|7|8
3|2|min.|grad.|min.|2|3|4|5|6|7
4|3|2|min.|grad.|min.|2|3|4|5|6
5|4|3|2|min.|grad.|min.|2|3|4|5
6|5|4|3|2|min.|grad.|min.|2|3|4
7|6|5|4|3|2|min.|grad.|min.|2|3
8|7|6|5|4|3|2|min.|grad.|min.|2
9|8|7|6|5|4|3|2|min.|grad.|min.
10|9|8|7|6|5|4|3|2|min.|grad.'''
tables=[]
for n,text,grid,labels in [(96,rows96,[144.9,456.2,450.0,761.0],['A','B','B']),(97,rows97,[165.7,404.5,475.8,710.6],['A','B','D'])]:
 rows=[s.split('|') for s in text.splitlines()]
 cells=[]
 for ri,row in enumerate(rows):
  for ci,v in enumerate(row):
   x0,y0,x1,y1=grid; rect=[x0+(x1-x0)*ci/11,y0+(y1-y0)*ri/11,x0+(x1-x0)*(ci+1)/11,y0+(y1-y0)*(ri+1)/11]
   cells.append({'cell_id':f'AB01-PDF{n:04}-T01-R{ri+1:02}-C{ci+1:02}','row':ri+1,'column':ci+1,'source_pdf_rect':rect,'literal':v if v!='[IMAGE]' else None,'status':'TRANSCRIBED' if v!='[IMAGE]' else 'IMAGE_PRESERVED_UNRESOLVED_DIGIT','glyph_id':'AB01-PDF0096-T01-R04-C10' if v=='[IMAGE]' else None})
 tables.append({'id':f'AB01-PDF{n:04}-T01','master_pdf_page':n,'printed_page':n-89,'role':'NALLINO_TRANSLATION','shape':[11,11],'source_grid_rect':grid,'outside_labels':labels,'rows':rows,'cells':cells,'method':'Each printed cell read visually. Literal rows entered explicitly, not generated from arithmetic. Rule checks, if used, are separate from transcription.'})
(R/'ledgers/tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2)+'\n')
