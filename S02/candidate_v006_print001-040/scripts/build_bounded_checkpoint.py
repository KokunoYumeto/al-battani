from pathlib import Path
import re, json, zipfile, shutil, hashlib, subprocess, os, sys, traceback, copy
import fitz
from PIL import Image
R=Path('/mnt/data'); D=R/'S02_PRINT001_040_CHECKPOINT'
D.mkdir(parents=True,exist_ok=True)
for sub in ['transcription/pages','tex','pdf','source/raw','source/presentation','ledgers','receipts','tables','qa/render','history','scripts','unverified']:(D/sub).mkdir(parents=True,exist_ok=True)
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
state={'session':'S02','version':'bounded_v006','status':'NOT_YET_BUILT','assigned_master_pages':[90,198],'assigned_printed_pages':[1,109],'source_reading_status':'No new visual verification claimed while tool readbacks are unavailable. Supplied source excerpts and inherited drafts are kept distinct from full verification.','target_language_translations_generated':[],'canonical_arabic_modified':False,'human_review_required_to_continue':False,'errors':[],'new_source_records':[],'S03_started':False}
try:
 for stem in ['AB01_S02_v002','AB01_S02_v005_ACCESSIBLE']:
  zp=R/(stem+'.zip')
  with zipfile.ZipFile(zp) as z:
   if z.testzip() is not None:raise RuntimeError('Corrupt input '+stem)
   if any(Path(a).is_absolute() or '..' in Path(a).parts for a in z.namelist()):raise RuntimeError('Unsafe input path')
   z.extractall(R)
 B=R/'AB01_S02_v002'; E=R/'AB01_S02_v005_ACCESSIBLE'; W=R/'AB01_S02_v006'
 M=R/'30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf'
 if H(M)!='544c16b6355c9b74e281aded657d657224bff738366d5260e1a610d31b0d6297':raise RuntimeError('Source hash mismatch')
 doc=fitz.open(M)
 if len(doc)!=1162:raise RuntimeError('Source page-count mismatch')
 for sub in ['source/raw','source/presentation','tables']:
  origin=E/sub if (E/sub).is_dir() else B/sub
  if origin.is_dir():shutil.copytree(origin,D/sub,dirs_exist_ok=True)
 inherited=[]
 for n in range(90,125):
  name=f'AB01-PDF{n:04}.json'
  choices=[E/'transcription/pages'/name,B/'transcription/pages'/name,R/'S02_PRINT031_035_EXTENSION/pages'/name]
  src=next((p for p in choices if p.is_file()),None)
  if src is None:raise RuntimeError('Inherited page missing: '+name)
  q=json.loads(src.read_text());assert q['master_pdf_page']==n
  shutil.copy2(src,D/'transcription/pages'/name)
  inherited.append({'page':n,'sha256':H(src),'copy_sha256':H(D/'transcription/pages'/name)})
 for filename in ['tables.json','visual_objects.json','critical_findings.json']:
  src=B/'ledgers'/filename
  if src.exists():shutil.copy2(src,D/'ledgers'/filename)
 for n in range(125,130):
  src=W/f'transcription/pages/AB01-PDF{n:04}.json'
  if not src.is_file():raise RuntimeError('Restored next-page record unavailable: '+str(n))
  q=json.loads(src.read_text());assert q['master_pdf_page']==n and q['printed_page']==n-89
  # Only the pages whose source excerpt is present in the supplied conversation are eligible.
  q['status']='SOURCE_LINKED_TRANSCRIPTION_CANDIDATE_NOT_NEW_VISUAL_CERTIFICATION'
  q['method']='Restored from the bounded source excerpt for physical125–129 supplied in this conversation; native source objects retained. A final glyph-level comparison and rendered-page inspection are not asserted in this continuation.'
  (D/f'transcription/pages/AB01-PDF{n:04}.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  state['new_source_records'].append(n)
 objs=json.loads((D/'ledgers/visual_objects.json').read_text()) if (D/'ledgers/visual_objects.json').is_file() else []
 for n,obj,rect,role in [(127,'F01',[113,377,204,515],'NALLINO_TRANSLATION'),(128,'F01',[61,317,176,468],'NALLINO_APPARATUS'),(128,'F02',[360,498,483,669],'NALLINO_APPARATUS')]:
  p=doc[n-1];info=max(p.get_image_info(xrefs=True),key=lambda a:a['width']*a['height']);pm=fitz.Pixmap(doc,info['xref'])
  if pm.n not in (1,3):pm=fitz.Pixmap(fitz.csRGB,pm)
  im=Image.frombytes('L' if pm.n==1 else 'RGB',(pm.width,pm.height),pm.samples)
  x0,y0,x1,y1=info['bbox'];sx=pm.width/(x1-x0);sy=pm.height/(y1-y0)
  import math
  box=[max(0,math.floor((rect[0]-x0)*sx)),max(0,math.floor((rect[1]-y0)*sy)),min(pm.width,math.ceil((rect[2]-x0)*sx)),min(pm.height,math.ceil((rect[3]-y0)*sy))]
  a=f'AB01-PDF{n:04}-{obj}';raw=D/f'source/raw/{a}-raw.png';pre=D/f'source/presentation/{a}.png';im.crop(box).save(raw);shutil.copy2(raw,pre)
  ob={'id':a,'master_pdf_page':n,'printed_page':n-89,'role':role,'kind':'diagram','source_xref':info['xref'],'source_image_size':[pm.width,pm.height],'source_image_pdf_bbox':list(info['bbox']),'requested_pdf_rect':rect,'native_pixel_rect':box,'dimensions':list(im.crop(box).size),'operations':['decode controlling PDF image','integer native-pixel crop','byte-identical presentation copy; no retouching'],'raw_path':raw.relative_to(D).as_posix(),'presentation_path':pre.relative_to(D).as_posix(),'raw_sha256':H(raw),'presentation_sha256':H(pre),'new_visual_crop_approval':False}
  if isinstance(objs,list):objs=[x for x in objs if x.get('id')!=a]+[ob]
 (D/'ledgers/visual_objects.json').write_text(json.dumps(objs,ensure_ascii=False,indent=2)+'\n')
 (D/'receipts/inherited_identity.json').write_text(json.dumps(inherited,indent=2)+'\n')
 for n in range(90,130):
  assert (D/f'transcription/pages/AB01-PDF{n:04}.json').is_file()
 state.update({'transcribed_printed_pages':[1,40],'candidate_master_pages':[90,129],'candidate_pages':40,'remaining_source_pages':69,'last_fully_transcribed_source_unit':'AB01-PDF0129','last_fully_transcribed_field_qualification':'Candidate coverage, not a newly certified source-reading boundary.','last_fully_verified_source_unit':None,'first_untouched_source_unit':'AB01-PDF0130','status':'PARTIAL_SOURCE_LINKED_CANDIDATE'})
 page_records=[json.loads((D/f'transcription/pages/AB01-PDF{n:04}.json').read_text()) for n in range(90,130)]
 txt=[]
 for q in page_records:
  txt.append('\n## '+q['anchor']+' | printed '+str(q['printed_page'])+' | '+q['status'])
  for sec in q['sections']:
   txt.append('['+sec['role']+' | '+sec['authorship']+']')
   for l in sec['lines']:txt.append(l['id']+'\t'+l['text'])
 (D/'transcription/S02_NALLINO_SOURCE_CANDIDATE.txt').write_text('\n'.join(txt)+'\n',encoding='utf-8')
 state['text_line_anchors']=sum(len(s['lines']) for q in page_records for s in q['sections'] if s['role']!='margins')
 # Preserve the existing typeset 35-page portion rather than rebuilding it from guesses.
 txs=[p for p in (E/'tex').glob('*.tex') if 'NALLINO_SOURCE' in p.name]
 if not txs:raise RuntimeError('Inherited 35-page TeX not found')
 inherited_tex=txs[0].read_text();shutil.copy2(txs[0],D/'history/inherited_35_page_candidate.tex')
 if '\\end{document}' not in inherited_tex:raise RuntimeError('Incomplete inherited TeX')
 tex=inherited_tex.rsplit('\\end{document}',1)[0]
 # Update only the initial editorial notice; historical body text is not globally replaced.
 pos=tex.find('\\BeginSource{AB01-PDF0090}')
 if pos>=0:
  notice=tex[:pos].replace('1–35','1–40').replace('1--35','1--40').replace('PDF124','PDF129')
  tex=notice+tex[pos:]
 esc={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}
 def markup(t):
  parts=re.split(r'(<m>.*?</m>|<display>.*?</display>|<glyph>.*?</glyph>|</?(?:i|b|sp|ar|gr)>|</?center>)',t)
  out=[]
  for part in parts:
   if part.startswith('<m>'):out.append('$'+part[3:-4]+'$')
   elif part.startswith('<display>'):out.append('\\['+part[9:-10]+'\\]')
   elif part.startswith('<glyph>'):out.append('\\sourceglyph{'+part[7:-8]+'}')
   elif part in ['<i>','<b>','<sp>','<ar>','<gr>']:
    out.append({'<i>':r'\textit{','<b>':r'\textbf{','<sp>':r'\textsc{','<ar>':r'\textarabic{','<gr>':r'\textgreek{'}[part])
   elif part in ['</i>','</b>','</sp>','</ar>','</gr>']:out.append('}')
   elif part in ['<center>','</center>']:pass
   else:out.append(''.join(esc.get(c,c) for c in part))
  return ''.join(out)
 # New helper has a unique name; it does not change inherited line-setting macros.
 tex+='\n\\providecommand{\\BoundedLine}[2]{\\noindent\\hypertarget{#1}{}#2\\strut\\par}\n'
 def render_lines(lines):
  out=[];i=0
  while i<len(lines):
   l=lines[i];t=l['text'];m=re.fullmatch(r'<figure(left|right)>(.*?)</figure\1>',t)
   if m:
    side,fig=m.groups();block=[];i+=1
    while i<len(lines) and lines[i]['text']!=f'<endfigure{side}/>':block.append(lines[i]);i+=1
    fw=.23 if fig.endswith('0127-F01') else (.25 if side=='left' else .30);tw=.96-fw
    image='\\begin{minipage}[t]{'+f'{fw:.2f}\\linewidth'+'}\\vspace{0pt}\\centering\\includegraphics[width=\\linewidth]{'+fig+'.png}\\end{minipage}'
    body='\\begin{minipage}[t]{'+f'{tw:.2f}\\linewidth'+'}\\vspace{0pt}\n'+render_lines(block)+'\n\\end{minipage}'
    out.append('\\par\\noindent'+(image+'\\hfill'+body if side=='left' else body+'\\hfill'+image)+'\\par')
   elif t.startswith('<display>'):out.append('\\hypertarget{'+l['id']+'}{}'+markup(t))
   elif t.startswith('<center>'):out.append('\\par\\smallskip{\\centering\\hypertarget{'+l['id']+'}{}'+markup(t)+'\\par}\\smallskip')
   else:out.append('\\BoundedLine{'+l['id']+'}{'+markup(t)+'}')
   i+=1
  return '\n'.join(out)
 for q in page_records[35:]:
  tex+='\n\\BeginSource{'+q['anchor']+'}{'+str(q['printed_page'])+'}\n'
  secs={s['role']:s['lines'] for s in q['sections']}
  tex+=render_lines(secs.get('body',[]))+'\n\\vfill\\par\\medskip\n'
  if 'notes_full' in secs:tex+=' {\\fontsize{9}{11.5}\\selectfont\n'+render_lines(secs['notes_full'])+'}\n'
  for idx,role in enumerate(['notes_left','notes_right']):
   if role not in secs:continue
   if idx:tex+='\\hfill'
   tex+='\\begin{minipage}[t]{.48\\linewidth}\\fontsize{9}{11.5}\\selectfont\n'+render_lines(secs[role])+'\n\\end{minipage}\n'
  if 'margins' in secs:
   tex+='\\par\\smallskip{\\fontsize{7}{8}\\selectfont '+markup(' | '.join(l['text'] for l in secs['margins']))+'\\par}\n'
 tex+='\n\\end{document}\n';tp=D/'tex/S02_NALLINO_SOURCE_CANDIDATE.tex';tp.write_text(tex)
 # Unprocessed pages are explicitly parked, never counted as transcription.
 for n in range(130,199):
  (D/f'unverified/embedded_PDF{n:04}.txt').write_text(doc[n-1].get_text(sort=True))
 excerpt=fitz.open();excerpt.insert_pdf(doc,from_page=89,to_page=128);ep=D/'source/SRC01_PDF0090_0129.pdf';excerpt.save(ep,garbage=4,deflate=True,no_new_id=True)
 identity=[]
 for i in range(40):
  a=doc[i+89].get_pixmap(dpi=50).samples;b=excerpt[i].get_pixmap(dpi=50).samples
  identity.append({'master_page':i+90,'render_identical':a==b})
 (D/'receipts/source_excerpt_identity.json').write_text(json.dumps(identity,indent=2)+'\n')
 env=os.environ.copy();env.update({'SOURCE_DATE_EPOCH':'1789776000','FORCE_SOURCE_DATE':'1','TZ':'UTC'})
 builds=[]
 for clean in ['A','B']:
  out=D/f'qa/build_{clean}';out.mkdir(exist_ok=True)
  for p in out.iterdir():
   if p.is_file():p.unlink()
  attempts=[]
  for run in [1,2]:
   cmd=['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(out),tp.name]
   try:
    result=subprocess.run(cmd,cwd=tp.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
    (out/f'pass{run}.stdout.txt').write_bytes(result.stdout);attempts.append(result.returncode)
    if result.returncode:break
   except Exception as exc:attempts.append(str(exc));break
  candidate=out/(tp.stem+'.pdf')
  builds.append({'clean_build':clean,'returns':attempts,'pdf_exists':candidate.exists(),'pdf_sha256':H(candidate) if candidate.exists() else None})
 if all(x['returns']==[0,0] for x in builds):
  A=D/'qa/build_A'/ (tp.stem+'.pdf');bb=D/'qa/build_B'/(tp.stem+'.pdf')
  builds.append({'two_clean_builds_byte_identical':H(A)==H(bb)})
  shutil.copy2(A,D/'pdf/S02_NALLINO_SOURCE_CANDIDATE.pdf')
  pd=fitz.open(A);state['reader_pages']=len(pd)
  for k in sorted(set([0,len(pd)-1,*[x for x in [31,35,36,37,38,39,40] if x<len(pd)]])):
   pd[k].get_pixmap(dpi=120).save(D/f'qa/render/reader_{k+1:03}.png')
  state['build_status']='BUILT; GENERATED RENDERS NOT CLAIMED VISUALLY INSPECTED'
 else:state['build_status']='BUILD_FAILURE_RECORDED'
 (D/'receipts/build_report.json').write_text(json.dumps(builds,indent=2)+'\n')
 # Separate notes, never substitute them for the historical notes in the reader.
 note='''# S02: bounded continuation and limitations\n\nThe inherited edition covers printed pages 1–35. This package adds source-linked candidate records for printed pages 36–40 (physical125–129), restoring the geometric discussion and its three source-image diagrams. The controlling edition is Nallino's; the historical Latin and his apparatus are separately tagged. No new target-language translations are made.\n\nThe new records are not promoted to a final visual or philological verification boundary. Native diagram crops are exact-pixel derivatives but their final crop and page-layout inspection remain outstanding. Programmatic build or hash checks are not represented as visual reading.\n\nPhysical127 preserves the italicized geometric assertions criticized by Nallino and retains FM/FC in the body even where notes7/8 propose FG/FB. Physical128 preserves Nallino's and Plato's diagrammatic layers in their stated roles. Physical129 retains the printed calendrical fractions and the Halma page reference rather than silently substituting a modern value or citation.\n\nThe remaining physical130–198 files in unverified/ are embedded-text extraction only. They are explicitly not transcriptions and cannot advance coverage. Earlier speculative scratch reconstructions have not been promoted or included.\n\nS01 is unchanged. S02 is not complete. No human-review requirement blocks continuation. The next production source is physical130, printed41.\n'''
 (D/'README.md').write_text(note)
 (D/'ledgers/new_reading_limitations.tsv').write_text('anchor\tcategory\tstatus\tdisposition\nAB01-PDF0125-PDF0129\treading\tFINAL_GLYPH_REVIEW_OPEN\tCandidate wording only; source controls\nAB01-PDF0127-F01\tfigure\tNATIVE_CROP_NOT_VISUALLY_APPROVED\tUnchanged source pixels\nAB01-PDF0128-F01\tfigure\tNATIVE_CROP_NOT_VISUALLY_APPROVED\tNallino apparatus; inspect upper label and crop boundary\nAB01-PDF0128-F02\tfigure\tNATIVE_CROP_NOT_VISUALLY_APPROVED\tPlato comparator in Nallino apparatus\n')
except Exception as exc:
 state['errors'].append({'error':str(exc),'traceback':traceback.format_exc()})
 state['status']='PARTIAL_EXPORT_WITH_RECORDED_FAILURE'
 if not (D/'README.md').exists():(D/'README.md').write_text('# S02 continuation\n\nThis package records the actual saved work and failures. No new source-reading or completion claim is made. See receipts/cumulative_checkpoint.json.\n')
finally:
 (D/'receipts/cumulative_checkpoint.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
 shutil.copy2(__file__,D/'scripts/build_bounded_checkpoint.py')
 forbidden={'.ttf','.otf','.ttc','.woff','.woff2','.pfb','.pfa','.dfont'}
 members=[p for p in D.rglob('*') if p.is_file() and p.suffix.lower() not in forbidden and p.name!='MANIFEST_SHA256.tsv']
 (D/'MANIFEST_SHA256.tsv').write_text('sha256\tbytes\tpath\n'+''.join(f'{H(p)}\t{p.stat().st_size}\t{p.relative_to(D).as_posix()}\n' for p in sorted(members)))
 zp=R/'S02_PRINT001_040_CHECKPOINT.zip'
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(D.rglob('*')):
   if p.is_file() and p.suffix.lower() not in forbidden:
    info=zipfile.ZipInfo(D.name+'/'+p.relative_to(D).as_posix(),date_time=(2026,9,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(zp) as z:
  bad=z.testzip();assert bad is None
  assert all(z.read(D.name+'/'+p.relative_to(D).as_posix())==p.read_bytes() for p in members)
 (R/'S02_PRINT001_040_CHECKPOINT_ZIP_VALIDATION.json').write_text(json.dumps({'sha256':H(zp),'bytes':zp.stat().st_size,'manifest_members':len(members),'archive_integrity':'PASS','manifest_bytes_equal':True,'candidate_state':state['status']},indent=2)+'\n')
 print(json.dumps({'archive':str(zp),'state':state},ensure_ascii=False,indent=2))
