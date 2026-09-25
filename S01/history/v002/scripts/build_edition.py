"""Generate a line-anchored historical Nallino edition from the reviewed JSON layer.
No text is inferred from OCR in this build. Fonts are system dependencies, not bundled.
"""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
PAGES=sorted((R/'transcription/pages').glob('*.json'))
TAG=re.compile(r'</?(?:i|n|ar|gr|sy|small|sup|m|glyph|b)>')
OPEN={'i':r'{\itshape ','n':r'{\addfontfeatures{LetterSpace=1.0} ','ar':r'\textarabic{\upshape ','gr':r'\textgreek{','sy':r'\RL{{\syriacfont ','small':r'{\small ','sup':r'\textsuperscript{','b':r'{\bfseries '}
CLOSE={k:'}' for k in OPEN};CLOSE['sy']='}}'
ESC={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','&':r'\&','#':r'\#','_':r'\_','$':r'\$','^':r'\textasciicircum{}','~':r'\textasciitilde{}','⁂':r'\asterism{}'}
def esc(t):return ''.join(ESC.get(c,c) for c in t)
def math(t):return t.replace('′',r'^{\prime}').replace('″',r'^{\prime\prime}').replace('‴',r'^{\prime\prime\prime}').replace('°',r'^{\circ}')
def line_tex(t,stack):
    # Tags can span source lines. Close/reopen only typographic groups at line boundaries.
    out=''.join(OPEN[k] for k in stack);pos=0; mode=None; buf=''
    for m in TAG.finditer(t):
        chunk=t[pos:m.start()]
        if mode in ('m','glyph'):buf+=chunk
        else:out+=esc(chunk)
        token=m.group();key=token.strip('</>');closing=token.startswith('</')
        if key in ('m','glyph'):
            if not closing:mode=key;buf=''
            else:
                if key=='m':out+=r'\('+ (r'\displaystyle ' if re.fullmatch(r'<m>.*</m>[.,;]?',t) else '')+math(buf)+r'\)'
                else:out+=r'\sourceglyph{'+buf+'}'
                mode=None;buf=''
        elif closing:
            assert stack and stack[-1]==key,(t,key,stack)
            stack.pop();out+=CLOSE[key]
        else:stack.append(key);out+=OPEN[key]
        pos=m.end()
    assert mode is None,('math/glyph spans source lines',t)
    out+=esc(t[pos:]);out+=''.join(CLOSE[k] for k in reversed(stack));return out

def sec_tex(sec,n):
    st=[];out=[]
    for line_index,l in enumerate(sec['lines']):
        t=l['text'];content=line_tex(t,st)
        # The original Arabic verse has its first hemistich in the right-hand column.
        if n==84 and len(re.findall(r'<ar>.*?</ar>',t))==2 and re.fullmatch(r'<ar>.*?</ar>\s+<ar>.*?</ar>',t):
            a,b=re.findall(r'<ar>(.*?)</ar>',t)
            content=r'\hbox to \linewidth{\hfil\textarabic{'+esc(b)+r'}\hfil\textarabic{'+esc(a)+r'}\hfil}'
        if re.fullmatch(r'<m>.*</m>[.,;]?',t):
            content=r'\hbox to \linewidth{\hfil '+content+r'\hfil}'
        if sec['role']=='body' and ((n==74 and line_index<3) or (n==79 and line_index==0)):
            if line_index==0:out.append(r'\vspace{13mm}')
            fs='18' if line_index==0 else '10'
            content=r'\hbox to \linewidth{\hfil{\fontsize{'+fs+r'}{22}\selectfont '+content+r'}\hfil}'
            if (n==74 and line_index==2) or n==79:content+=r''
        out.append('% '+l['id'])
        out.append(r'\SourceLine{'+l['id']+'}{'+content+'}')
        if sec['role']=='body' and ((n==74 and line_index==2) or (n==79 and line_index==0)):out.append(r'\vspace{9mm}')
    assert not st,(n,sec['role'],st)
    return '\n'.join(out)

preamble=r'''\documentclass[11pt]{article}
\usepackage[paperwidth=220mm,paperheight=320mm,left=17.5mm,right=17.5mm,top=20mm,bottom=20mm,headheight=12pt,headsep=12pt,footskip=15pt]{geometry}
\usepackage{fix-cm}
\usepackage{fontspec}
\usepackage{amsmath,amssymb,graphicx}
\usepackage{fancyhdr}
\usepackage[unicode,hidelinks,bookmarksopen=false]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{latin}
\setotherlanguages{arabic,greek}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\arabicfont{Amiri}[Script=Arabic,Scale=1.0]
\newfontfamily\syriacfont{Noto Sans Syriac}[Script=Syriac,Scale=0.9]
\graphicspath{{../source/presentation/}}
\hypersetup{pdftitle={Nallino: Praefatio, conspectus, addenda et emendanda. S01 v002},pdfauthor={Carlo Alfonso Nallino},pdfsubject={Historical Nallino layer. Source-first transcription candidate; unresolved readings documented separately.}}
\pagestyle{fancy}\fancyhf{}
\newcommand{\leftfolio}{}\newcommand{\rightfolio}{}
\fancyhead[L]{\fontsize{8}{10}\selectfont\leftfolio}
\fancyhead[C]{\fontsize{8}{10}\selectfont\leftmark}
\fancyhead[R]{\fontsize{8}{10}\selectfont\rightfolio}
\fancyfoot[L]{\fontsize{7.5}{9}\selectfont\rightmark}
\fancyfoot[R]{\fontsize{7.5}{9}\selectfont\thepage}
\renewcommand{\headrulewidth}{0.25pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\setlength{\emergencystretch}{0pt}
\newcommand{\asterism}{\raisebox{0.4ex}{\scriptsize *}\kern-0.5em\raisebox{-0.5ex}{\scriptsize **}}
\newcommand{\sourceglyph}[1]{\raisebox{-0.20em}{\includegraphics[height=1.30em]{#1.png}}}
\newsavebox{\sourcelinebox}
\newcommand{\SourceLine}[2]{%
 \sbox{\sourcelinebox}{\strut\hypertarget{#1}{}#2}%
 \ifdim\wd\sourcelinebox>\linewidth\typeout{SOURCEWIDTH|#1|\the\wd\sourcelinebox|\the\linewidth}\fi%
 \noindent\usebox{\sourcelinebox}\par}
\newcommand{\BeginSource}[2]{\clearpage\gdef\leftfolio{}\gdef\rightfolio{}\markboth{#2}{#1}\hypertarget{#1}{}\pdfbookmark[0]{#1}{book-#1}\fontsize{12}{14.8}\selectfont}
\newcommand{\NotesStart}{\par\vspace{7pt}\hrule height0.25pt\vspace{5pt}\fontsize{10}{12.25}\selectfont}
\tracinglostchars=2
\begin{document}
'''
out=[preamble]
out.append(r"""
\markboth{ADMONITIO EDITIONIS DIGITALIS}{S01-v002 — MODERN\_EDITORIAL}
\hypertarget{S01-v002-EDITORIAL-NOTICE}{}
\pdfbookmark[0]{Admonitio editionis digitalis}{editorial-notice}
\vspace*{25mm}
\begin{center}
{\fontsize{11}{15}\selectfont\addfontfeatures{LetterSpace=3} CAROLUS ALPHONSUS NALLINO\par}
\vspace{12mm}
{\fontsize{25}{34}\selectfont Praefatio\par Conspectus librorum\par Addenda et emendanda\par}
\vspace{10mm}
{\fontsize{12}{17}\selectfont\itshape Pars prima, 1903\par}
\vspace{18mm}
{\fontsize{10}{14}\selectfont S01 · v002\par}
\end{center}
\vspace{12mm}
\fontsize{11}{16}\selectfont
Haec materia ad Nallini apparatum pertinet, non ad textum Arabicum auctoris.
Loci aliis linguis ab ipso Nallino relati in sua forma servati sunt.\par\medskip
Transcriptio per totum ambitum fontis prima vice recognita est.
Lectiones incertae in indice separato recensentur; signa nondum certo expressa
imaginibus fontis servantur. Addenda Nallini describuntur, non tacite locis prioribus inseruntur.\par\medskip
Figura astronomica in ipso fonte mutila est. Quae desunt non sunt restituta;
solae fasciae instrumenti digitalis extrinsecus additae a figura exhibita abscissae sunt.\par\medskip
Recognitio independens omnium verborum nondum facta est.
Textus editabilis, imagines integrae, lectionum rationes, indices locorum et
signaturae SHA-256 in fasciculo huius editionis separatim praebentur.\par\medskip
Fons: exemplar digitale SRC01, paginae 2, 10, 12–89.
Dispositiones omnium paginarum 1–89 in indice continentur.
""")
out += [r'\BeginSource{AB01-PDF0002}{FIGURA ASTRONOMICA}',r'\vspace*{25mm}',r'\begin{center}\includegraphics[width=\textwidth]{AB01-PDF0002-F01.png}\end{center}']
plain=['NALLINO_APPARATUS — S01 v002','Source-faithful transcription candidate, not independently certified.','AB01-PDF0002: astronomical diagram preserved in source/presentation/AB01-PDF0002-F01.png.']
for p in PAGES:
    d=json.loads(p.read_text());n=d['master_pdf_page'];anchor=d['anchor'];kind=d['kind']
    plain+=['\n'+'='*64,anchor+' | '+d['header']+' | '+kind]
    for s in d['sections']:
        plain.append('['+s['role']+']')
        for l in s['lines']:
            # Keep explicit glyph references in the plain-text layer.
            t=re.sub(r'<glyph>(.*?)</glyph>',r'[source glyph: \1]',l['text'])
            t=TAG.sub('',t);plain.append(l['id']+'\t'+t)
    if kind=='blank':continue
    header=d['header']
    romans=re.findall(r'\b[IVXLCDM]+\b',header)
    folio=romans[-1] if romans else ''
    running=re.sub(r'\b[IVXLCDM]+\b','',header).replace('|','').replace('—','').strip()
    if n==16:running=''
    out.append(r'\BeginSource{'+anchor+'}{'+esc(running)+'}')
    if folio:
        name='leftfolio' if n%2 else 'rightfolio'
        out.append(chr(92)+'gdef'+chr(92)+name+'{'+folio+'}')
    sections={s['role']:s for s in d['sections']}
    body=sections.get('body',{'role':'body','lines':[]})
    if kind=='half_title':
        out+=[r'\vspace*{70mm}\begin{center}\fontsize{13}{21}\selectfont']
        st=[]
        for l in body['lines']:out.append(r'\hypertarget{'+l['id']+'}{}'+line_tex(l['text'],st)+r'\par')
        out.append(r'\end{center}')
    elif kind=='title':
        out.append(r'\begin{center}')
        st=[]
        for i,l in enumerate(body['lines']):
            if i in [3,5,9,11]:out.append(r'\vspace{'+{3:'15',5:'10',9:'25',11:'30'}[i]+r'mm}')
            size=21 if i==4 else 13 if i in [3,8,9] else 9
            out.append(r'{\fontsize{'+str(size)+'}{'+str(size*1.7)+r'}\selectfont '+r'\hypertarget{'+l['id']+'}{}'+line_tex(l['text'],st)+r'\par}')
        out.append(r'\end{center}')
    elif kind=='imprint':
        out += [r'\vspace*{215mm}\begin{center}\fontsize{9}{12}\selectfont']
        st=[]
        for l in body['lines']:out.append(r'\hypertarget{'+l['id']+'}{}'+line_tex(l['text'],st)+r'\par')
        out.append(r'\end{center}')
    elif kind=='dedication':
        out += [r'\vspace*{78mm}\begin{center}\fontsize{12}{24}\selectfont'];st=[]
        for l in body['lines']:out.append(r'\hypertarget{'+l['id']+'}{}'+line_tex(l['text'],st)+r'\par')
        out.append(r'\end{center}')
    else:
        if n==16:
            out += [r'\begin{center}\includegraphics[width=.91\textwidth]{AB01-PDF0016-F01.png}\par\vspace{20mm}{\fontsize{20}{26}\selectfont PRAEFATIO}\end{center}\vspace{17mm}']
        # A source page stays intact. Excess height/width is reported by the build, not hidden.
        out.append(r'\begin{minipage}[t]{\textwidth}')
        out.append(sec_tex(body,n))
        if any(k.startswith('notes') for k in sections):
            out.append(r'\NotesStart')
            if 'notes_full' in sections:out.append(sec_tex(sections['notes_full'],n))
            if 'notes_left' in sections or 'notes_right' in sections:
                out.append(r'\noindent\begin{minipage}[t]{.485\linewidth}\fontsize{10}{12.25}\selectfont')
                out.append(sec_tex(sections.get('notes_left',{'role':'notes_left','lines':[]}),n))
                out.append(r'\end{minipage}\hfill\begin{minipage}[t]{.485\linewidth}\fontsize{10}{12.25}\selectfont')
                out.append(sec_tex(sections.get('notes_right',{'role':'notes_right','lines':[]}),n))
                out.append(r'\end{minipage}')
        out.append(r'\end{minipage}')
        if n in (78,89):out.append(r'\par\vspace{42mm}\begin{center}\includegraphics[width=49mm]{AB01-PDF'+f'{n:04d}'+r'-F01.png}\end{center}')
        if d['details'].get('signature') or d['details'].get('printing_signature'):out.append(r'\par\vspace{6pt}\hfill{\fontsize{8}{10}\selectfont '+esc(d['details'].get('signature',d['details'].get('printing_signature')))+'}')
out.append(r'\end{document}')
(R/'tex/S01_NALLINO_SOURCE_v002.tex').write_text('\n'.join(out)+'\n')
(R/'transcription/S01_NALLINO_SOURCE_v002.txt').write_text('\n'.join(plain)+'\n')
print('Generated TeX',len('\n'.join(out)),'characters; line-anchored text written.')

key=[]
for n in (72,73):
 d=json.loads((R/'transcription/pages'/f'AB01-PDF{n:04d}.json').read_text())
 chosen=[l for l in d['sections'][0]['lines'] if any(l['id']==k['line_id'] for k in json.loads((R/'ledgers/transliteration_key.json').read_text()))]
 key.append(sec_tex({'role':'body','lines':chosen},n))
(R/'tex/S01_TRANSLITERATION_KEY.tex').write_text('% Printed source list; use the main edition preamble. No invented source column headings.\n'+ '\n'.join(key)+'\n')
