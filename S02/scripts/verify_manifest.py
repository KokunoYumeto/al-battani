"""Verify the self-excluding package manifest without modifying any file."""
from pathlib import Path
import csv,hashlib,sys
R=Path(__file__).resolve().parents[1]
with (R/'MANIFEST_SHA256.tsv').open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
errors=[]
for row in rows:
 p=R/row['path']
 if not p.is_file():errors.append('missing '+row['path']);continue
 if p.stat().st_size!=int(row['bytes']) or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:errors.append('mismatch '+row['path'])
print(f'{len(rows)-len(errors)}/{len(rows)} manifest entries verified')
for e in errors:print(e)
sys.exit(bool(errors))
