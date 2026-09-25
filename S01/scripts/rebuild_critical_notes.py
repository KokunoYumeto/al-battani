"""Build the separate v003 critical apparatus from the current evidence ledgers.
No new target-language translation is generated. System fonts are not distributed.
"""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,tempfile
import fitz
R=Path(__file__).resolve().parents[1];name='S01_CRITICAL_NOTES_v003'
notes=json.loads((R/'ledgers/critical_findings.json').read_text())
changes=json.loads((R/'ledgers/v003_changes.json').read_text())
ESC={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','&':r'\&','#':r'\#','_':r'\_','$':r'\$','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
def esc(s):return ''.join(ESC.get(c,c) for c in str(s))
def text(s):
 out=[];pos=0
 for m in re.finditer(r'[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+|[\u0700-\u074f]+|[\u0370-\u03ff\u1f00-\u1fff]+',str(s)):
  out.append(esc(str(s)[pos:m.start()]));v=m.group()
  if '\u0700'<=v[0]<='\u074f':out.append(r'\RL{{\syriacfont '+esc(v)+'}}')
  elif ('\u0370'<=v[0]<='\u03ff') or ('\u1f00'<=v[0]<='\u1fff'):out.append(r'\textgreek{'+esc(v)+'}')
  else:out.append(r'\textarabic{'+esc(v)+'}')
  pos=m.end()
 out.append(esc(str(s)[pos:]));return ''.join(out)
num_resolved=sum(x['status']=='RESOLVED_RETAINED' for x in notes)
num_image=sum(x['status']=='DISPOSED_IMAGE_FALLBACK' for x in notes)
num_text=sum(x['category']=='digital_transcription' for x in changes)
num_fallback=sum(x['category']=='source_image_fallback' for x in changes)
out=[r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=23mm,headheight=14pt]{geometry}
\usepackage{fontspec,graphicx}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic,greek}
\setmainfont{Linux Libertine O}
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\syriacfont{Noto Sans Syriac}[Script=Syriac]
\usepackage{fancyhdr}
\usepackage[unicode,hidelinks]{hyperref}
\hypersetup{pdftitle={S01 v003 - Critical notes and source limitations},pdfauthor={Digital editorial apparatus; AI-assisted production}}
\graphicspath{{../source/presentation/}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{S01 v003 — Critical notes}\fancyhead[R]{Modern editorial apparatus}\fancyfoot[C]{\thepage}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\emergencystretch=2em
\begin{document}
\begin{center}{\Large Critical notes and source limitations}\par
{\large Nallino, Part I: front matter and apparatus}\par
S01 v003 — 25 September 2026\end{center}
These notes belong to the digital production, not to Nallino's historical prose. The historical reader is a separate artifact. Intrinsic quotations in Nallino retain their original languages; no new parallel translation has been generated.

The first-pass transcription covers the complete S01 range. This successor records a targeted reread of recovered proof material, not a new independently audited full transcription. Historical wording and errors remain distinguished from errors introduced by the digital transcription.
''',text(f'The ledger contains {len(changes)} successor decisions: {num_text} digital text repairs and {num_fallback} new image-fallback substitutions. Of the {len(notes)} critical entries, {num_resolved} now retain source-supported character readings, {num_image} preserve unresolved character distinctions through exact source images, and one records truncation already present in the frontispiece. Image preservation does not settle the interpretation of an uncertain character.'),r'''
Source identifiers are physical pages of the pinned master, SRC01, not the reader's pagination. Every figure crop has a native-image rectangle and checksum. Nallino's own printed addenda are transcribed and routed, never silently applied to the earlier text.
''']
for x in notes:
 n=int(x['source_anchor'].split('PDF')[1]);reader=2 if n==2 else n-9
 label={'RESOLVED_RETAINED':'source reading retained','DISPOSED_IMAGE_FALLBACK':'exact-image disposition; interpretation limited','DOCUMENTED_SOURCE_LOSS':'source loss documented'}.get(x['status'],x['status'].replace('_',' ').lower())
 out += [r'\par\noindent\begin{minipage}{\linewidth}',r'\subsection*{'+esc(x['apparatus_id']+' — '+x['source_anchor'])+'}',r'\textit{'+esc(label+f'; reader p. {reader}')+'}',text(x['reason'])]
 oids=x.get('object_ids',[])
 if oids:
  for k,oid in enumerate(oids):
   if oid.startswith('AB01-PDF0084'):
    out.append(r'\par\begin{center}\includegraphics[width=.80\linewidth]{'+oid+r'.png}\end{center}')
   else:
    out.append(r'\includegraphics[height=6mm]{'+oid+r'.png}\hspace{4mm}')
  out.append(r'\par')
 else:out.append(r'\textbf{Reading.} '+text(x['diplomatic_reading'])+'.')
 if x['status']!='RESOLVED_RETAINED':out.append(r'\textbf{Interpretive limit.} '+text(x['bounded_alternatives'])+'.')
 out.append(r'\textbf{Location.} {\small\texttt{'+esc(x['line_id'])+r'}}. '+('Individual crop coordinates and object hashes are recorded in the figure ledger.' if oids else esc(x['coordinate_granularity'])+'.'))
 out.append(r'\end{minipage}\par\smallskip')
out += [r'''\section*{Version history, preservation and audit status}
The v002 release is preserved unchanged. All 535 files recorded in its self-excluding manifest matched their saved hashes. The interrupted reread left 157 recoverable proof images, but no revised transcription or decision ledger was found with them. Those images are preserved as recovery evidence; their headings were not accepted as reading authority.

The current producing assistant visually reread 562 general proof candidates and 164 targeted candidates. The counts refer to candidate snippets, with possible overlap, not 726 separate pages or an independent word-by-word audit. Confirmed differences were recorded as before/after decisions. Dense mathematical pages and the other formula-bearing source regions were also reread. No mathematical recalculation was used to overwrite the historical text.

The 86 historical addenda/corrigenda entries remain \texttt{REGISTERED\_NOT\_APPLIED}. Future-session anchors are routing references only. S02 has not begun. The Arabic authorial canon has not been altered.

The included rebuild program performs two clean two-pass builds and records their hashes. The read-only technical audit verifies file identity, coverage, exact native crop pixels, anchor consistency and build receipts. These are technical tests, not independent philological certification. The producing assistant is responsible for this reread and the changes; a separate cold source/reading auditor has not replayed this successor. S01 therefore remains open at that release gate.

Line-alignment rectangles inherited from embedded-text similarity are locator candidates, not independently certified measurements of every source line. Native image-crop coordinates have a separate pixel-equality check. Precise uncertainties are disclosed, rather than supplied from expected spelling, grammar or numerical coherence.

\section*{Source citation}
Nallino, C. A. (1903). [Front matter, preface, bibliography, and addenda]. In \textit{Al-Battānī sive Albatenii opus astronomicum} (Pars prima: \textit{Versio capitum cum animadversionibus}, pp. VII–LXXX). Ulrich Hoepli. Controlling digital witness: SRC01, physical PDF2, PDF10 and PDF12–89.

{\small Source SHA-256:\par\texttt{544c16b6355c9b74e281aded657d6572}\par\texttt{24bff738366d5260e1a610d31b0d6297}\par}
\end{document}''']
(R/'tex'/f'{name}.tex').write_text('\n'.join(out)+'\n')
env=dict(os.environ,SOURCE_DATE_EPOCH='1790294400',FORCE_SOURCE_DATE='1',TZ='UTC');receipts=[]
for label in ['A','B']:
 with tempfile.TemporaryDirectory(prefix='.notes_build_'+label+'_',dir=R) as td:
  wd=Path(td);shutil.copyfile(R/'tex'/f'{name}.tex',wd/f'{name}.tex')
  for run in [1,2]:
   cp=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'],cwd=wd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   (R/'receipts'/f'critical_build_{label}_pass{run}.txt').write_bytes(cp.stdout)
   if cp.returncode:raise RuntimeError(cp.stdout.decode(errors='replace')[-5000:])
  data=(wd/f'{name}.pdf').read_bytes();log=(wd/f'{name}.log').read_text();(R/'receipts'/f'critical_build_{label}.log').write_text(log)
  d=fitz.open(stream=data,filetype='pdf')
  receipts.append({'build':label,'passes':2,'clean_directory':True,'pdf_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'pages':len(d),'missing_characters':log.count('Missing character'),'overfull_boxes':log.count('Overfull'),'font_warnings':log.count('Font Warning'),'raster_hashes_36dpi':{str(i+1):hashlib.sha256(d[i].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples).hexdigest() for i in range(len(d))}})
  if label=='B':(R/'pdf'/f'{name}.pdf').write_bytes(data)
r={'artifact':name,'builds':receipts,'byte_identical':receipts[0]['pdf_sha256']==receipts[1]['pdf_sha256'],'all_page_rasters_identical':receipts[0]['raster_hashes_36dpi']==receipts[1]['raster_hashes_36dpi'],'source_date_epoch':1790294400,'font_files_distributed':False,'independent_philological_audit':False}
(R/'receipts/critical_notes_builds.json').write_text(json.dumps(r,indent=2)+'\n')
assert r['byte_identical'] and r['all_page_rasters_identical']
assert not any(b[k] for b in receipts for k in ['missing_characters','overfull_boxes','font_warnings'])
print('Critical notes PASS',receipts[-1]['pages'],'pages;',receipts[-1]['pdf_sha256'])
