"""Create and verify a self-excluding SHA-256 manifest and deterministic ZIP."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
MAN='MANIFEST_SHA256.tsv'
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!=MAN and '__pycache__' not in p.parts and not any(x.startswith('.clean_build_') or x.startswith('.notes_build_') for x in p.parts))
assert not any(p.suffix.lower() in ('.ttf','.otf','.ttc','.woff','.woff2') for p in files)
rows=[(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size,str(p.relative_to(R))) for p in files]
(R/MAN).write_text('# Self-excluding SHA-256 manifest. Paths are relative to AB01_S01_v002.\nsha256\tbytes\tpath\n'+'\n'.join(f'{h}\t{n}\t{p}' for h,n,p in rows)+'\n')
archive=R.parent/'AB01_S01_v002.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files+[R/MAN]):
  info=zipfile.ZipInfo(R.name+'/'+str(p.relative_to(R)),date_time=(2026,9,25,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=0o100644<<16
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
# Verify the finished archive, not merely the files before compression.
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for h,n,rel in rows:
  data=z.read(R.name+'/'+rel)
  assert len(data)==n and hashlib.sha256(data).hexdigest()==h,rel
 data=z.read(R.name+'/'+MAN);assert data==(R/MAN).read_bytes()
summary={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'manifest_entries':len(rows),'zip_entries':len(rows)+1,'all_archive_payload_hashes_verified':True,'zip_crc_check':'PASS','fixed_zip_timestamp_utc':'2026-09-25T00:00:00Z','font_binaries_included':False,'note':'The ZIP is deterministic for these frozen payload bytes. The archive receipt itself is external to avoid a self-referential checksum.'}
(R.parent/'AB01_S01_v002_ARCHIVE_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
