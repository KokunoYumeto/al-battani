"""Two clean, two-pass XeLaTeX builds. Requires system fonts; embeds but never distributes font files."""
from pathlib import Path
import os,subprocess,tempfile,hashlib,json,shutil,sys
import fitz
R=Path(__file__).resolve().parents[1]; name='S01_NALLINO_SOURCE_v002'
subprocess.run([sys.executable,str(R/'scripts/build_edition.py')],check=True)
ENV=dict(os.environ,SOURCE_DATE_EPOCH='1790294400',FORCE_SOURCE_DATE='1',TZ='UTC')
results=[]
for label in ['A','B']:
 with tempfile.TemporaryDirectory(prefix='.clean_build_'+label+'_',dir=R) as td:
  wd=Path(td);shutil.copyfile(R/'tex'/f'{name}.tex',wd/f'{name}.tex')
  for run in [1,2]:
   cp=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'],cwd=wd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True)
   (R/'receipts'/f'build_{label}_pass{run}.txt').write_bytes(cp.stdout)
  data=(wd/f'{name}.pdf').read_bytes();log=(wd/f'{name}.log').read_text()
  (R/'receipts'/f'build_{label}.log').write_text(log)
  doc=fitz.open(stream=data,filetype='pdf')
  raster_hashes={str(i+1):hashlib.sha256(doc[i].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples).hexdigest() for i in range(len(doc))}
  results.append({'build':label,'clean_directory':True,'passes':2,'pdf_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'pages':len(doc),'missing_characters':log.count('Missing character'),'overfull_boxes':log.count('Overfull'),'source_line_overflows':log.count('SOURCEWIDTH'),'font_warnings':log.count('Font Warning'),'raster_hashes_36dpi':raster_hashes})
  if label=='B':(R/'pdf'/f'{name}.pdf').write_bytes(data)
version=subprocess.run(['xelatex','--version'],stdout=subprocess.PIPE,check=True,text=True).stdout.splitlines()[0]
receipt={'engine':version,'command':'xelatex -interaction=nonstopmode -halt-on-error S01_NALLINO_SOURCE_v002.tex','builds':results,'source_date_epoch':1790294400,'byte_identical':results[0]['pdf_sha256']==results[1]['pdf_sha256'],'all_page_rasters_identical':results[0]['raster_hashes_36dpi']==results[1]['raster_hashes_36dpi'],'font_files_distributed':False,'dependencies':['XeLaTeX','fontspec','polyglossia','amsmath','amssymb','fix-cm','fancyhdr','hyperref','graphicx','Linux Libertine O','FreeSerif','Amiri','Noto Sans Syriac'],'source_fidelity_limit':'Build and raster identity are technical tests, not proof of correct historical readings.'}
(R/'receipts/deterministic_builds.json').write_text(json.dumps(receipt,indent=2)+'\n')
if not receipt['byte_identical']:raise RuntimeError('Clean build PDFs are not byte-identical.')
if any(r[k] for r in results for k in ['missing_characters','overfull_boxes','source_line_overflows','font_warnings']):raise RuntimeError('Build quality checks failed.')
print('PASS',results[1]['pages'],'pages; two byte-identical clean builds;',results[1]['pdf_sha256'])

subprocess.run([sys.executable,str(R/'scripts/rebuild_critical_notes.py')],check=True)
