from pathlib import Path
import json
ROOT=Path('/mnt/data/AB01_S01_v002')
def put(n, header='', body='', left='', right='', fullnotes='', kind='text', details=None):
    sections=[]
    for role,txt in [('body',body),('notes_left',left),('notes_right',right),('notes_full',fullnotes)]:
        if txt.strip():
            lines=txt.strip('\n').splitlines()
            sections.append({'role':role,'lines':[{'id':f'AB01-PDF{n:04d}-{role}-L{i:03d}','text':t} for i,t in enumerate(lines,1)]})
    obj={'anchor':f'AB01-PDF{n:04d}','master_pdf_page':n,'role':'NALLINO_APPARATUS','header':header,'kind':kind,
         'source_status':'SOURCE_REPLAYED_FIRST_PASS','method':'Direct visual reading of authoritative SRC01 pixels; embedded text is recovery evidence only.',
         'source_sha256':'544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297',
         'sections':sections,'details':details or {}}
    (ROOT/'transcription/pages'/f'AB01-PDF{n:04d}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n, sum(len(s['lines']) for s in sections),'lines')
