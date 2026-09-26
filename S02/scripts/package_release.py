"""Write a deterministic, bounded ZIP with a self-excluding SHA-256 manifest."""
from pathlib import Path
import csv,hashlib,zipfile,json
R=Path(__file__).resolve().parents[1]
OUT=R.parent/(R.name+'.zip')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def include(p):
    rel=p.relative_to(R)
    if not p.is_file() or '__pycache__' in rel.parts or any(x.startswith('build_') for x in rel.parts):return False
    if p.suffix.lower() in {'.otf','.ttf','.woff','.woff2','.ttc','.pyc'}:return False
    if rel.parts[0]=='scripts' and (p.name.startswith('transcribe_batch') or p.name in ['refine_batch.py','make_tables01.py']):return False
    if rel.parts[0]=='qa':
        if len(rel.parts)<3 or rel.parts[1] not in ['source','final']:return False
        if rel.parts[1]=='source':
            return p.name.startswith('reading_') and p.suffix=='.png' and 90<=int(p.stem.split('_')[-1])<=119
    return rel.as_posix()!='MANIFEST_SHA256.tsv'
files=sorted([p for p in R.rglob('*') if include(p)],key=lambda p:p.relative_to(R).as_posix())
manifest=R/'MANIFEST_SHA256.tsv'
with manifest.open('w',encoding='utf8',newline='') as f:
    w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['path','bytes','sha256'])
    for p in files:w.writerow([p.relative_to(R).as_posix(),p.stat().st_size,sha(p)])
files.append(manifest);files.sort(key=lambda p:p.relative_to(R).as_posix())
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:
        zi=zipfile.ZipInfo((Path(R.name)/p.relative_to(R)).as_posix(),date_time=(2026,9,26,0,0,0))
        zi.create_system=3;zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
with zipfile.ZipFile(OUT) as z:
    corrupt=z.testzip();entries=z.namelist()
    rows=list(csv.DictReader(z.read(R.name+'/MANIFEST_SHA256.tsv').decode().splitlines(),delimiter='\t'))
    mismatches=[]
    for row in rows:
        data=z.read(R.name+'/'+row['path'])
        if len(data)!=int(row['bytes']) or hashlib.sha256(data).hexdigest()!=row['sha256']:mismatches.append(row['path'])
    unsafe=[n for n in entries if n.startswith('/') or '..' in Path(n).parts]
    fonts=[n for n in entries if Path(n).suffix.lower() in {'.otf','.ttf','.woff','.woff2','.ttc'}]
report={'archive':OUT.name,'bytes':OUT.stat().st_size,'sha256':sha(OUT),'members':len(entries),'manifest_entries':len(rows),'crc_error':corrupt,'manifest_mismatches':mismatches,'unsafe_paths':unsafe,'font_binaries':fonts,'status':'PASS' if not any([corrupt,mismatches,unsafe,fonts]) else 'FAIL','reader_sha256':sha(R/'pdf/S02_NALLINO_SOURCE_v002.pdf'),'scope':'Historical Latin source transcription and apparatus: master PDF90–119 / printed pp.1–30. S02 partial.'}
(R.parent/(R.name+'_ZIP_VALIDATION.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
if report['status']!='PASS':raise RuntimeError('Package verification failed')
