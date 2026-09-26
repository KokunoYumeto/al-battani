from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
HELPERS=r'''
\newcommand{\qfrac}[2]{{}^{#1}\!/_{{#2}}}
\newcommand{\Name}[1]{{\addfontfeatures{LetterSpace=4.0}#1}}
\newcommand{\Indent}{\hspace*{1.6em}}
\newcommand{\CenterLine}[1]{\makebox[\linewidth][c]{{\fontsize{12}{15}\selectfont #1}}}
\newlength{\FullSourceWidth}\newlength{\GutterOffset}\newif\ifNumbersLeft
\newcommand{\DSource}[2]{\BeginSource{AB01-PDF#1}{#2}%
 \setlength{\FullSourceWidth}{\textwidth}\setlength{\GutterOffset}{0pt}%
 \ifodd#2\relax\NumbersLefttrue\else\NumbersLeftfalse\fi}
\newsavebox{\DLBox}
\newcommand{\DLine}[4]{%
 \par\noindent\hypertarget{#1}{}%
 \ifx\relax#2\relax\else
   \ifNumbersLeft
    \rlap{\kern-\GutterOffset\llap{\fontsize{7}{8}\selectfont #2\hspace{3mm}}}%
   \else
    \rlap{\kern\dimexpr\FullSourceWidth-\GutterOffset\relax\hspace{3mm}{\fontsize{7}{8}\selectfont #2}}%
   \fi
 \fi
 \ifx\relax#3\relax\else
   \ifNumbersLeft
    \rlap{\kern\dimexpr\FullSourceWidth-\GutterOffset\relax\hspace{3mm}{\fontsize{7}{8}\selectfont #3}}%
   \else
    \rlap{\kern-\GutterOffset\llap{\fontsize{7}{8}\selectfont #3\hspace{3mm}}}%
   \fi
 \fi
 \sbox{\DLBox}{\strut #4}%
 \ifdim\wd\DLBox>\linewidth\typeout{DIPLOMATICWIDTH|#1|\the\wd\DLBox|\the\linewidth}\fi
 \usebox{\DLBox}\strut\par}
'''
def lines_tex(lines,locs=None,previous=None,numbered=False):
 out=[];last=previous
 for l in lines:
  n=l['source_line_no'];t=l['tex'];loc=(locs or {}).get(n,'')
  if numbered and last is not None and n>last+1:out.append(r'\vspace{'+str((n-last-1)*13.8)+'pt}')
  if l.get('semantic_anchor'):out.append(r'\hypertarget{'+l['semantic_anchor']+'}{}')
  show=str(n) if numbered and n is not None and n>0 and n%5==0 else ''
  out.append(r'\DLine{'+l['id']+'}{'+show+'}{'+loc+'}{'+t+'}');last=n
 return '\n'.join(out)
def page_tex(q):
 p=q['master_pdf_page'];out=[r'\DSource{'+f'{p:04}'+'}{'+str(q['printed_page'])+'}'];secs={s['role']:s['lines'] for s in q['sections']};body=secs['body'];locs={a['line']:a['text'] for a in q.get('margin_locators',[])};figures=q.get('figures',[]);i=0;last=None
 while i<len(body):
  l=body[i];n=l['source_line_no'];f=next((f for f in figures if f['start_line']==n),None)
  if f:
   block=[]
   while i<len(body) and body[i]['source_line_no']<=f['end_line']:block.append(body[i]);i+=1
   iw=f['image_width_fraction'];tw=f['text_width_fraction'];off=1-tw
   im=r'\begin{minipage}[t]{'+str(iw)+r'\FullSourceWidth}\vspace{0pt}\centering\hypertarget{'+f['id']+r'}{}\includegraphics[width=\linewidth]{'+f['id']+r'.png}\end{minipage}'
   tx=r'\begin{minipage}[t]{'+str(tw)+r'\FullSourceWidth}\vspace{0pt}\setlength{\GutterOffset}{'+str(off)+r'\FullSourceWidth}'+'\n'+lines_tex(block,locs,last,True)+r'\end{minipage}'
   out.append(r'\par\noindent'+im+r'\hfill'+tx+r'\par');last=block[-1]['source_line_no']
  else:out.append(lines_tex([l],locs,last,True));last=n;i+=1
 out.append(r'\par\vspace{6pt}\hrule height.25pt\vspace{5pt}')
 for k,role in enumerate(['notes_left','notes_right']):
  out.append((r'\hfill' if k else r'\noindent')+r'\begin{minipage}[t]{.48\textwidth}\vspace{0pt}\fontsize{9}{11.5}\selectfont\setlength{\GutterOffset}{0pt}');out.append(lines_tex(secs[role]));out.append(r'\end{minipage}')
 if q.get('signature'):out.append(r'\par\vspace{5mm}\hfill{\fontsize{8}{10}\selectfont '+q['signature']+r'}\hspace{10mm}')
 return '\n'.join(out)+'\n'
def generate():
 base=(ROOT/'history/S02_PRINT001_040_CHECKPOINT/tex/S02_NALLINO_SOURCE_CANDIDATE.tex').read_text();oldbody=base[base.index(r'\BeginSource{AB01-PDF0090}'):].rsplit(r'\end{document}',1)[0]
 preamble=base.split(r'\begin{document}',1)[0].replace('S02 v002','S02 v009')+HELPERS
 records=[json.loads(p.read_text()) for p in sorted((ROOT/'transcription/pages').glob('*.json'))];new=[q for q in records if q['master_pdf_page']>=130];last=records[-1]['printed_page']
 for q in new:(ROOT/f'tex/pages/{q["anchor"]}.tex').write_text(page_tex(q))
 notice=r'''\begin{document}
\thispagestyle{empty}
\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE OPUS ASTRONOMICUM\par
\vspace{5mm}\large Caroli Alphonsi Nallino versio Latina et adnotationes\par\vspace{8mm}
\Large S02 --- editio diplomatica in progressu\par\vspace{4mm}\large Paginae impressae 1--LASTPAGE\end{center}
\vspace{12mm}\noindent Paginae 1--40 ex exemplari priore receptae sunt, lectionibus non mutatis. Paginae 41--43 secundum collatorem et imagines fontis recognitae sunt; signa lectionum U01--U09 soluta et correctiones in registro separato consignatae sunt. Paginae 44--LASTPAGE cum imaginibus fontis collatae sunt. Examen totius sessionis nondum absolutum est.\par
\vspace{4mm}\noindent Nova translatio in linguas alias non continetur. Lectiones, formulae et discrepantiae editionis historicae non tacite emendantur. Numeri marginales et locatores in paginis noviter descriptis ad lineas fontis referuntur.\par
'''.replace('LASTPAGE',str(last))
 cumulative=preamble+notice+oldbody+'\n'+'\n'.join(r'\input{pages/'+q['anchor']+'.tex}' for q in new)+'\n'+r'\end{document}'+'\n'
 (ROOT/'tex/S02_NALLINO_SOURCE_v009.tex').write_text(cumulative)
 for lo,hi,name in [(130,132,'S02_P041_043_checked'),(133,records[-1]['master_pdf_page'],f'S02_P044_{last:03}_source_replayed')]:
  # Single-file standalone documents: no hidden \input dependencies.
  fragments='\n'.join(page_tex(q) for q in new if lo<=q['master_pdf_page']<=hi)
  text=preamble+'\n'+r'\begin{document}'+'\n'+r'\setcounter{page}{'+str(lo-89)+'}\n'+fragments+r'\end{document}'+'\n'
  (ROOT/'tex'/f'{name}.tex').write_text(text)
 print('Generated',last,'source pages with',len(new),'new page fragments')
 return records
if __name__=='__main__':generate()
