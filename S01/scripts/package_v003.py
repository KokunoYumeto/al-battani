#!/usr/bin/env python3
"""Package the sealed v003 candidate with a deterministic manifest and ZIP.
No historical text is changed. Refuses a failed/missing technical audit.
Writes archive/validation beside the package, never into the archive itself.
"""
from __future__ import annotations
from pathlib import Path
import csv, datetime, hashlib, io, json, shutil, tempfile, zipfile
R=Path(__file__).resolve().parents[1]
OUT=R.parent/(R.name+'.zip')
def digest_bytes(data):return hashlib.sha256(data).hexdigest()
def digest_file(path):return digest_bytes(path.read_bytes())
def main():
    audit=json.loads((R/'receipts/technical_audit_v003.json').read_text())
    if audit['status']!='PASS_TECHNICAL_CHECKS_ONLY' or audit['failed']:
        raise RuntimeError('A successful current technical audit is required before packaging.')
    for cache in R.rglob('__pycache__'):shutil.rmtree(cache)
    files=sorted(p for p in R.rglob('*') if p.is_file() and p!=R/'MANIFEST_SHA256.tsv')
    forbidden={'.ttf','.otf','.woff','.woff2','.pfb'}
    if any(p.is_symlink() or p.suffix.lower() in forbidden for p in files):
        raise ValueError('Unsafe symlink or font binary in package.')
    rows=[{'sha256':digest_file(p),'bytes':p.stat().st_size,'path':p.relative_to(R).as_posix()} for p in files]
    with (R/'MANIFEST_SHA256.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['sha256','bytes','path'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    files=sorted(files+[R/'MANIFEST_SHA256.tsv'])
    def archive(path):
        with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
            for p in files:
                name=R.name+'/'+p.relative_to(R).as_posix()
                info=zipfile.ZipInfo(name,date_time=(2026,9,25,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=0o100644<<16
                z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
    temp=OUT.with_suffix('.zip.partial');archive(temp);temp.replace(OUT)
    result={'artifact':OUT.name,'archive_bytes':OUT.stat().st_size,'archive_sha256':digest_file(OUT),'payload_file_count':len(files),'manifest_record_count':len(rows),'manifest_self_excluding':True,'manifest_sha256':digest_file(R/'MANIFEST_SHA256.tsv'),'archive_test':'NOT_YET_RUN','technical_audit_status':audit['status'],'technical_check_count':audit['check_count'],'session_complete':False,'independent_philological_audit':False,'font_files_distributed':False}
    errors=[]
    with zipfile.ZipFile(OUT) as z:
        bad=z.testzip()
        for row in rows:
            name=R.name+'/'+row['path'];b=z.read(name)
            if len(b)!=row['bytes'] or digest_bytes(b)!=row['sha256']:errors.append(name)
        names=z.namelist();expected={R.name+'/'+p.relative_to(R).as_posix() for p in files}
        if len(names)!=len(set(names)) or set(names)!=expected:errors.append('membership')
        if any(n.startswith('/') or '..' in Path(n).parts for n in names):errors.append('unsafe_path')
        if z.read(R.name+'/MANIFEST_SHA256.tsv')!=(R/'MANIFEST_SHA256.tsv').read_bytes():errors.append('manifest_bytes')
    if bad:errors.append('CRC:'+bad)
    result['archive_test']='PASS' if not errors else 'FAIL';result['errors']=errors
    # A second independently written ZIP tests deterministic serialization, not historical fidelity.
    compare=OUT.with_suffix('.zip.rebuild');archive(compare)
    result['second_archive_byte_identical']=digest_file(compare)==result['archive_sha256'];compare.unlink()
    if not result['second_archive_byte_identical']:errors.append('archive_nondeterminism')
    result['validation_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (R.parent/(R.name+'_ZIP_VALIDATION.json')).write_text(json.dumps(result,indent=2)+'\n')
    (R.parent/(R.name+'.zip.sha256')).write_text(result['archive_sha256']+'  '+OUT.name+'\n')
    print(json.dumps(result,indent=2))
    if errors:raise RuntimeError('Archive validation failed: '+repr(errors))
if __name__=='__main__':main()
